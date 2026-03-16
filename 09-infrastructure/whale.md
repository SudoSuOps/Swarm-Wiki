# whale

Secondary training and evaluation rig. Single RTX 3090 in full x16 bandwidth slot.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen 9 5900X 12C/24T |
| RAM | 64GB DDR4 |
| Storage | Samsung 990 EVO 1TB |
| GPU | RTX 3090 (24GB, Gen4 x16, 65.4 TFLOPS FP16, sm_86) |
| NIC | Intel X540-AT2 10G (dual-port, Gen2 x4, not cabled yet) |
| Mobo | MSI B550 Tomahawk |

### Hardware History

Previously had 2x RTX 3090, but GPU 0 was in a crippled chipset x4 slot (only 31.5 TFLOPS -- less than half theoretical). Hardware swap on Feb 27, 2026: removed both 3090s, installed single 3090 in the top x16 slot for full bandwidth, and the 10G NIC in the freed x4 slot.

## Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| FP16 | 65.4 TFLOPS | 92% of theoretical |
| Host-to-Device | 13.0 GB/s | PCIe Gen4 x16 |
| RAM STREAM copy | 36.6 GB/s | DDR4 dual channel |

## Software

| Package | Version |
|---------|---------|
| Python | 3.12.3 |
| Unsloth | 2026.2.1 |
| uv | 0.10.6 |

Full ML stack verified. Use `uv sync` (lightweight) or `uv sync --group train` (ML dependencies).

## Current Role: ASRS Cook Node

Whale is dedicated to ASRS aviation cooking with the patched RJ-quality-gated cook script.

| Service | Port | Model | Workers |
|---------|------|-------|---------|
| vLLM (ASRS cook) | 8085 | Qwen3.5-4B base | 4 |
| cook_watcher | -- | SwarmRadar triage | -- |

Cook script: `cook_asrs.py` with 3-gate RJ quality filter (mechanism + tradeoff + density).
Output: `~/swarm-radar/cooked_asrs_full.jsonl` (4,658+ pairs and growing).

### ASRS Quality Gates

The ASRS cook adds aviation-specific RJ gates on top of standard gates:
- **mechanism**: Causal connectors (because, therefore, which allows, this leads to...)
- **tradeoff**: Decision boundary phrases (instead of, better when, fails if, tradeoff...)
- **density**: Aviation technical terms (altitude, ATC, TCAS, GPWS, go-around...)
- **filler penalty**: Generic phrases (widely used, very important...) reduce score

Pairs scoring < 2/3 gates are rejected. Output uses `metadata` schema (not legacy `_audit`).

## Legacy Models

| Model | Format | Size | Port |
|-------|--------|------|------|
| SwarmCurator-2B | Merged bf16 | ~4GB | -- (at `~/swarmcurator-2b/merged/`) |
| BeeMini (Router v2) | Q4_K_M GGUF | 1.8GB | -- (not active) |

## Training Capability

whale handles all models up to 24GB VRAM:

| Model Size | Fits | Config |
|------------|------|--------|
| 2B | Yes | batch=4, grad_accum=8 |
| 9B | Yes | batch=4, grad_accum=8, bf16 LoRA |
| 27B | No | Requires 96GB (use swarmrails GPU 1) |
| 35B MoE (3B active) | Yes | batch=4, ~18GB with LoRA |

## Access

```bash
ssh whale  # swarm@192.168.0.99, key auth
```
