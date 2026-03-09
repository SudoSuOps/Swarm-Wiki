# R2 Buckets

All training data and artifacts are stored in Cloudflare R2. Cloudflare account: `6abec5e82728df0610a98be9364918e4`.

## Training Data Buckets

### sb-cre
- **Pairs**: 643,382
- **Specialties**: 10
- **Asset types**: infill_warehouse, small_bay, flex, cross_dock, cold_storage, IOS, micro_fulfillment, data_center, industrial_land
- **Task types**: underwriting_calc (32%), ic_memo (22%), lease_reasoning (15%), market_comp (11%), t12/rent_roll/lease_abstract (~7% each), risk_triage (5%)
- **Origin**: Promoted from 881K factory output via math verification. Pairs that failed numeric_verify were rejected, leaving 643K verified survivors.

### sb-medical
- **Pairs**: 432,196 total
  - 403,572 base medical pairs across 85 specialties
  - 28,624 trajectory-enhanced pharma pairs (27 shards in `trajectory/` prefix)
- **Specialties**: 85
- **Trajectory pairs**: Labeled `trajectory=true v1`, cover 16 pharma task types. Each pair includes 5-step reasoning chain (IDENTIFY, CALCULATE, ANALYZE, EVALUATE, RECOMMEND).

### sb-aviation
- **Pairs**: 45,222 total
  - 20,208 existing pairs
  - 25,014 new pairs ground on whale (RTX 3090)
- **Specialties**: 157

### sb-core
- **Pairs**: 31,347 total
  - 23,344 existing pairs
  - 8,003 new legal/medicine pairs
- **Specialties**: 3

### sb-drone
- **Pairs**: 6,755
- **Specialties**: 176

## Artifact Buckets

### sb-intelligence
Intelligence Objects -- finalized, verified, structured CRE data products (PIO, portfolio objects). These are the output of the SwarmRouter pipeline, not raw training data.

### sb-models
Model artifacts: merged weights, LoRA adapters, GGUF quantizations.

### sb-judge
Judge training data. Archived after SwarmJudge was killed (2026-03-06). Judge capability rolled into SwarmCurator-27B as a task type.

### sb-judge-traces
Agent trace data originally collected for judge model training. Retained for potential RL use.

## Operational Buckets

### swarm-scripts
Training scripts archive: 23 objects covering judge, pharma, med, specialist, CRE, and swarmrails-live scripts.

### swarm-ops
API keys and operational secrets: 2 objects.

### block-0
Genesis NFTs: 303 objects.

### Legacy

| Bucket | Objects | Notes |
|--------|---------|-------|
| swarm-apedia-vault | 8,720 | Legacy knowledge base |
| swarm-vault | 353 | Legacy storage |

## Shard Naming Convention

All data buckets use sequential shard naming: `shard_NNNN.jsonl` (e.g., `shard_0001.jsonl`, `shard_0002.jsonl`). SafeStore pushes a new shard every 500 pairs.
