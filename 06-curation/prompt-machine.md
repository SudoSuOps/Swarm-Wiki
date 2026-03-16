# Prompt Machine

Automated prompt evolution system that discovers which system prompts produce the highest-scoring pairs. Deployed 2026-03-15.

## Architecture

```
Prompt Registry (cook-domain-prompts repo)
    |
    v
Telemetry API (hive-ledger /api/telemetry/prompts/*)
    |
    v
Softmax Allocation (cook_openalex.py weighted_prompt_choice)
    |
    v
Mutation Generation (4 axes x 2 parents = 8 mutations)
    |
    v
Extinction Rule (avg < 85 + 200 pairs -> removed)
```

## Key Finding

**The prompt was the bottleneck, not the model.** Old prompts scored 0.4-0.5 reasoning_depth, producing pollen-tier output. RJ-aligned prompts with explicit reasoning cues and domain grounding score 1.0, pushing the same base 4B model to 90.9 avg (honey/royal_jelly). This discovery powers the entire cook fleet.

## Prompt Registry

Shared prompt library in `cook-domain-prompts` repo (`pip install`-able). 13 domains + default. Each prompt is SHA-256 hashed (truncated to 16 hex chars) for tracking.

```python
from cook_domain_prompts import get_prompts
prompts = get_prompts("aviation")  # Returns list of system prompt strings
```

## Softmax Allocation

Prompts are weighted by telemetry performance using temperature-scaled softmax:

```
weight(p) = exp((score(p) - max_score) / temperature) / sum(exp(...))
```

- **Temperature**: 0.5 (aggressive exploitation, top prompts get most traffic)
- **Floor**: 5% minimum allocation per prompt (prevents starvation)
- **Exploration floor**: 10% for mutations with < 200 pairs (bootstraps new prompts)
- **Scores**: Fetched from `/api/telemetry/prompts` leaderboard

## Mutations

8 structured mutations derived from 2 parent prompts across 4 axes:

| Axis | What It Pushes | Example Cue |
|------|---------------|-------------|
| specificity_pressure | Named entities, measurable effects, operational thresholds | "cite measurable effects" |
| reasoning_cues | Cause-effect chains, implications, constraint analysis | "trace cause-and-effect chains" |
| numeric_density | Rates, ratios, deltas, confidence intervals | "calculate rates, ratios, deltas" |
| persona_grounding | Professional credentials, experience markers | "CCIM/MAI-credentialed" |

Each axis is crossed with each parent prompt (2 parents x 4 axes = 8 mutations). All mutations append the standard `_RJ_SYSTEM_SUFFIX` for RJ alignment.

### Early Results (2026-03-16)

All 8 mutations outperform both parents in early telemetry:
- Parents: 90.0 - 90.5 avg
- Mutations: 91 - 95 avg (small sample, still bootstrapping)

## Extinction Rule

Prompts are removed from the pool when they demonstrate sustained underperformance:

```
if pair_count >= 200 AND avg_score < 85:
    exclude from candidates  # extinct
```

This prevents proven losers from consuming allocation. The 200-pair threshold ensures statistical significance before extinction.

## Telemetry Endpoints

All public, no auth. Served from hive-ledger:

| Endpoint | Returns |
|----------|---------|
| `GET /api/telemetry/prompts` | Leaderboard: avg_score, honey_rate, pair_count per hash |
| `GET /api/telemetry/prompts/domains` | Prompt x domain matrix |
| `GET /api/telemetry/prompts/models` | Prompt x model matrix |
| `GET /api/telemetry/prompts/timeline` | Temporal trends per prompt |
| `GET /api/telemetry/prompts/adoption` | Usage rates, first/last seen |
| `GET /api/telemetry/prompts/:hash` | Single prompt detail |

## Hash Propagation

Every pair carries three hash fields through the entire pipeline:

| Field | What It Tracks |
|-------|---------------|
| `prompt_hash` | Combined hash of system prompt + instruction (primary key for telemetry) |
| `system_prompt_hash` | SHA-256 of the system prompt text alone |
| `instruction_hash` | SHA-256 of the instruction template (not yet populated by all cook scripts) |

Hashes flow: cook script -> finalize_batch.py -> hive-ledger D1 -> telemetry API -> softmax allocation -> cook script (closed loop).

## Files

| File | Role |
|------|------|
| `/data2/cook-domain-prompts/` | Shared prompt library (pip-installable) |
| `/data2/openalex/cook_openalex.py` | Cook script with softmax allocation + mutations |
| `/data2/hive-ledger/src/routes/telemetry.js` | Telemetry API endpoints |
| `/data2/hive-ledger/scripts/finalize_batch.py` | Hash computation + propagation |
