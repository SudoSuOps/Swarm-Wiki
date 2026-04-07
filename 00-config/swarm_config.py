#!/usr/bin/env python3
"""
Swarm Config Loader — Single Source of Truth
=============================================
Every service loads config from ~/Swarm-Wiki/00-config/swarm.yaml.
One file. One place. One change propagates everywhere.

Usage:
    from swarm_config import cfg

    # Weight classes
    cfg.rj_threshold        # 0.85
    cfg.honey_threshold     # 0.70

    # Scales
    cfg.scale_a_model       # "gemma3:12b"
    cfg.scale_b_model       # "qwen2.5:32b"
    cfg.valid_scales        # {"gemma3:12b", "gemma4:31b", ...}

    # Domain config
    cfg.get_scales("clawhash")  # ("gemma4:31b", "qwen3.5:27b")
    cfg.get_price("medhash")    # 0.0072

    # Tribunal
    cfg.drift_threshold     # 0.15
    cfg.tribunal_temp       # 0.1

    # Classify
    cfg.classify(0.91)      # "royal_jelly"
    cfg.classify(0.75)      # "honey"
    cfg.classify(0.60)      # "propolis"

Install:
    # Symlink into any project that needs it
    ln -sf ~/Swarm-Wiki/00-config/swarm_config.py ~/google-gemma-4-FTW/swarm_config.py
    ln -sf ~/Swarm-Wiki/00-config/swarm_config.py ~/SwarmTribunal/swarm_config.py
    ln -sf ~/Swarm-Wiki/00-config/swarm_config.py ~/SwarmOS/swarmos/swarm_config.py
"""

import os
import sys
from pathlib import Path

# Find the config file — check common locations
_CONFIG_SEARCH = [
    Path(__file__).parent / "swarm.yaml",
    Path.home() / "Swarm-Wiki" / "00-config" / "swarm.yaml",
    Path("/home/swarm/Swarm-Wiki/00-config/swarm.yaml"),
]


def _load_yaml(path):
    """Load YAML without requiring PyYAML — parse the subset we use."""
    try:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback: minimal YAML parser for flat/nested dicts
        # Good enough for our config structure
        import json
        import re

        with open(path) as f:
            lines = f.readlines()

        # Strip comments and empty lines, build a simplified structure
        result = {}
        stack = [(result, -1)]

        for line in lines:
            stripped = line.split("#")[0].rstrip()
            if not stripped or stripped.isspace():
                continue

            indent = len(line) - len(line.lstrip())
            content = stripped.strip()

            if content.startswith("- "):
                # List item
                parent, _ = stack[-1]
                if isinstance(parent, dict):
                    # Find the last key added and convert to list
                    last_key = list(parent.keys())[-1]
                    if not isinstance(parent[last_key], list):
                        parent[last_key] = []
                    parent[last_key].append(content[2:].strip().strip('"').strip("'"))
                continue

            if ":" in content:
                key, _, val = content.partition(":")
                key = key.strip()
                val = val.strip()

                # Pop stack to correct level
                while len(stack) > 1 and stack[-1][1] >= indent:
                    stack.pop()

                parent, _ = stack[-1]

                if val:
                    # Scalar value
                    val = val.strip('"').strip("'")
                    # Type coercion
                    if val.lower() in ("true", "yes"):
                        val = True
                    elif val.lower() in ("false", "no"):
                        val = False
                    else:
                        try:
                            val = int(val)
                        except ValueError:
                            try:
                                val = float(val)
                            except ValueError:
                                pass
                    parent[key] = val
                else:
                    # Nested dict
                    parent[key] = {}
                    stack.append((parent[key], indent))

        return result


class SwarmConfig:
    """Centralized config loaded from swarm.yaml."""

    def __init__(self):
        self._data = None
        self._path = None
        self._load()

    def _load(self):
        for path in _CONFIG_SEARCH:
            if path.exists():
                self._path = path
                self._data = _load_yaml(path)
                return
        print(f"[FATAL] swarm.yaml not found. Searched: {_CONFIG_SEARCH}", file=sys.stderr)
        print(f"[FATAL] Create ~/Swarm-Wiki/00-config/swarm.yaml or symlink swarm_config.py", file=sys.stderr)
        raise SystemExit(1)

    def reload(self):
        """Reload config from disk."""
        self._load()

    # ─── Weight Classes ────────────────────────────────────────

    @property
    def rj_threshold(self):
        return self._data["weight_classes"]["royal_jelly"]["threshold"]

    @property
    def honey_threshold(self):
        return self._data["weight_classes"]["honey"]["threshold"]

    def classify(self, weight):
        """Classify a consensus weight into a tier."""
        if weight >= self.rj_threshold:
            return "royal_jelly"
        elif weight >= self.honey_threshold:
            return "honey"
        return "propolis"

    # ─── Scales ────────────────────────────────────────────────

    @property
    def valid_scales(self):
        return set(self._data["scales"]["valid_models"])

    @property
    def minimum_scale_params(self):
        return self._data["scales"]["minimum_params"]

    @property
    def scale_a_model(self):
        return self._data["scales"]["standard"]["scale_a"]["model"]

    @property
    def scale_b_model(self):
        return self._data["scales"]["standard"]["scale_b"]["model"]

    def get_scales(self, domain):
        """Get scale models for a domain. Returns (scale_a_model, scale_b_model)."""
        tier = self._data.get("domain_scales", {}).get(domain, "standard")
        cfg = self._data["scales"].get(tier, self._data["scales"]["standard"])
        return cfg["scale_a"]["model"], cfg["scale_b"]["model"]

    def validate_scale(self, model_name):
        """Check if a model is approved for use as a scale. Raises SystemExit if not."""
        if model_name not in self.valid_scales:
            print(f"[FATAL] Model '{model_name}' not in approved scales: {self.valid_scales}", file=sys.stderr)
            print(f"[FATAL] Standing rule: NEVER use models smaller than {self.minimum_scale_params}B.", file=sys.stderr)
            raise SystemExit(1)

    # ─── Domain-Hash ───────────────────────────────────────────

    def get_price(self, domain_hash):
        """Get price per pound for a domain-hash algorithm."""
        return self._data.get("domain_hash", {}).get(domain_hash, {}).get("price_per_lb", 0)

    def get_rj_rate(self, domain_hash):
        """Get RJ pairs per hour for a domain-hash."""
        return self._data.get("domain_hash", {}).get(domain_hash, {}).get("rj_per_hour", 0)

    # ─── Tribunal ──────────────────────────────────────────────

    @property
    def drift_threshold(self):
        return self._data["tribunal"]["drift_threshold"]

    @property
    def tribunal_temp(self):
        return self._data["tribunal"]["temperature"]

    @property
    def tribunal_max_tokens(self):
        return self._data["tribunal"]["max_tokens"]

    @property
    def tribunal_batch_size(self):
        return self._data["tribunal"]["batch_size"]

    # ─── Red/Blue ──────────────────────────────────────────────

    @property
    def red_team_model(self):
        return self._data["red_blue"]["red_team"]["model"]

    @property
    def blue_team_model(self):
        return self._data["red_blue"]["blue_team"]["model"]

    # ─── Database ──────────────────────────────────────────────

    @property
    def database_url(self):
        return os.environ.get("DATABASE_URL", self._data.get("database", {}).get("url", ""))

    # ─── Infrastructure ────────────────────────────────────────

    @property
    def total_vram_gb(self):
        return self._data.get("infrastructure", {}).get("swarmrails", {}).get("total_vram_gb", 0)

    # ─── Deed Writer ───────────────────────────────────────────

    @property
    def deed_writer_model(self):
        return self._data.get("deed_writer", {}).get("default_model", "gemma3:12b")

    @property
    def valid_deed_writers(self):
        return set(self._data.get("deed_writer", {}).get("valid_models", []))

    # ─── Info ──────────────────────────────────────────────────

    @property
    def config_path(self):
        return str(self._path)

    def __repr__(self):
        return f"SwarmConfig(path={self._path}, rj={self.rj_threshold}, scales={self.scale_a_model}+{self.scale_b_model})"


# Module-level singleton — import and use directly
cfg = SwarmConfig()
