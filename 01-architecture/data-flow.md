# Data Flow

End-to-end path from raw market signal to deployed model, with every intermediate stage documented.

## Pipeline Overview

```
Signal Workers (11)
    |
    v
EntityScorer + VelocityTracker
    |
    v
Integration Bridges
    |-- event bridge    --> D1 database (22 event types, 5 categories)
    |-- memory bridge   --> Vectorize index (768 dims, cosine, BGE-Base)
    |-- curator bridge  --> Curator Planner
    |-- R2 bridge       --> R2 bucket storage (sb-cre, sb-medical, sb-aviation, etc.)
    |-- discord bridge  --> #swarm-signal channel (P1-P3 alerts)
    |-- hedera bridge   --> HCS topics (mainnet)
    |
    v
Curator Planner (signal heat -> cook orders)
    |
    v
Factory Pipeline
    |-- skeleton    --> Generate deal/scenario structure
    |-- generate    --> LLM produces instruction-response pairs
    |-- gate        --> 6 deterministic checks
    |-- promote     --> CoVe verification → RJP-1 tiers (royal_jelly/honey/pollen/propolis)
    |-- publish     --> R2 upload + manifest update
    |-- ledger      --> hive-ledger (Merkle seal + Hedera HCS anchor)
    |-- warehouse   --> hive-warehouse (catalog + fulfillment API)
    |
    v
Training (Unsloth LoRA on swarmrails GPUs)
    |
    v
Deploy
    |-- merge       --> LoRA weights into base model
    |-- quantize    --> GGUF (Q4_K_M, Q8_0, F16) for edge/inference
    |-- vLLM        --> bf16 serving on Blackwell GPUs
    |
    v
Eval
    |-- JSON validity rate
    |-- Verdict match accuracy
    |-- Score MAE
    |-- Benchmark suite (300 prompts, 10 categories)
    |
    v
Fleet Deployment
    |-- Cook fleet: 3 nodes running base 4B + Prompt Machine
    |-- SwarmJelly-4B on CPU (self-healing loop)
    |-- Edge cook on Jetson Orin (12 pairs/hr)
    |-- Signal classification on zima-edge-1
```

## Stage 1: Signal Ingestion

11 signal workers run on 15-minute cycles. Each worker targets a specific public data source:

- EDGAR filings (REIT 10-K/10-Q, 15 tickers active)
- County assessor and recorder databases
- Lease expiration feeds
- Construction permit databases
- Tenant movement trackers
- Industrial sale listings
- Rate change monitors
- Zoning change feeds
- News aggregators
- Supply chain logistics data
- Economic development announcements

Each raw signal passes through EntityScorer (assigns relevance score based on entity profile, market context, and historical patterns) and VelocityTracker (detects acceleration -- an entity showing up 3x in a week matters more than 3x in a year).

Signals are prioritized:
- **P1**: Act now. Immediate market impact. Fires to Discord within seconds.
- **P2**: Watch. Developing situation. Logged and queued for curator review.
- **P3**: Background. Useful for training data but not time-sensitive.
- **Noise**: Filtered out. Does not enter the pipeline.

## Stage 2: Integration Bridges

Six bridges fan signals out to their destinations:

**Event Bridge**: Writes to D1 database. 22 event types across 5 categories (deal, supply, ownership, macro, tenant). Each event gets entity extraction and resolution -- "Prologis" and "PLD" resolve to the same entity.

**Memory Bridge**: Embeds signal content via BGE-Base (768 dimensions) and indexes in Cloudflare Vectorize. Enables semantic search across all historical signals via `/memory/search`.

**Curator Bridge**: Passes scored signals to the Curator Planner. The planner converts signal heat (volume and priority of signals in a domain) into cook orders for the factory.

**R2 Bridge**: Stores raw signal payloads and generated pairs in Cloudflare R2 buckets. Each vertical has its own bucket (sb-cre, sb-medical, sb-aviation, sb-drone, sb-core).

**Discord Bridge**: Posts P1-P3 signals to #swarm-signal channel via webhook. Provides human-readable summaries for monitoring.

**Hedera Bridge**: Publishes signal hashes to HCS topics on mainnet. Creates immutable provenance chain from raw signal through final intelligence object.

## Stage 3: Curator Fleet Processing

The curator fleet operates as a 7-middleware chain:

1. **SignalIngestion**: Receives scored signals from the curator bridge
2. **Classification (2B)**: SwarmCurator-2B classifies signal type, vertical, and priority
3. **Analysis (9B)**: SwarmCurator-9B performs detailed signal analysis -- what does this event mean for the market?
4. **Strategy (27B)**: SwarmCurator-27B makes strategic decisions -- should we cook new training pairs? Which skills need updating? What market reports should generate?
5. **QualityGate**: Deterministic validation of curator outputs
6. **StateUpdate**: Updates fleet state in `.state/fleet_runs.jsonl`
7. **Dispatch**: Routes cook orders to the factory, alerts to Discord, seals to Hedera

Each tier has both an LLM endpoint and an algorithmic fallback. The fleet works with zero GPUs (all fallbacks) and upgrades automatically as models come online.

## Stage 4: Factory Pipeline

The factory converts cook orders into training-ready data:

**Skeleton**: Generates the structure of a training pair. For CRE: deal parameters (asset type, cap rate, NOI, market, tenant), task type (underwriting, IC memo, lease analysis), and complexity tier.

**Generate**: An LLM (Together.ai Llama-3.3-70B or local vLLM) produces the instruction-response pair. System prompts rotate across 30+ unique templates to prevent memorization. 26+ task types ensure diversity.

**Gate**: Six deterministic checks per RJP-1, in sequence:
1. **json_valid** -- is the output valid JSON?
2. **output_length** -- minimum character counts (JSON: 20, text: 50)
3. **degenerate** -- no 40+ char repeated patterns
4. **dedup** -- SHA-256 fingerprint uniqueness within shard
5. **concept_present** -- domain-specific terms present (min 2 hits)
6. **numeric_verify** -- computed values match gold targets within tolerance

**Promote**: CoVe (Chain of Verification) pass. Pairs that clear all gates are scored via the RJP-1 JellyScore formula and assigned canonical tiers: royal_jelly (>= 95), honey (>= 85), pollen (>= 70), or propolis (< 70). Pairs below propolis threshold are logged with failure reasons for analysis.

**Publish**: Promoted pairs upload to the appropriate R2 bucket with updated manifest. Shard files follow naming convention: `{vertical}_{task}_{shard_num}.jsonl`.

## Stage 5: Training

All training uses Unsloth FastLanguageModel + TRL SFTTrainer on swarmrails Blackwell GPUs.

Key parameters (universal):
- bf16 LoRA only (no QLoRA for Qwen3.5)
- packing=True (6x speedup)
- AutoTokenizer bypass (Qwen3.5 VL dispatch bug)
- LoRA r=64, alpha=32 (r=32 for 2B)
- Early stopping patience=3 on eval_loss

Training data is assembled from promoted pairs across multiple cook streams. System prompt diversity is enforced: no single prompt can exceed 10% of the training set.

## Stage 6: Deployment

**Merge**: LoRA adapter weights merge into the base model via Unsloth's merge utilities. Produces a full-weight checkpoint.

**Quantize**: GGUF quantization for edge and lightweight inference:
- Q4_K_M: ~40% of bf16 size, minimal quality loss, used on edge devices
- Q8_0: ~50% of bf16 size, near-lossless, used for local testing
- F16: Full precision GGUF, used when vLLM is not available

**vLLM Serve**: Production inference via vLLM 0.17.0 on swarmrails:
- 9B bf16 on port 8081 (GPU0, 23.5GB VRAM, 165 tok/s at 4 concurrent)
- 27B bf16 on port 8082 (GPU1, 93GB VRAM, 88 tok/s at 4 concurrent)
- Required flags: `--skip-mm-profiling --enforce-eager --limit-mm-per-prompt '{"image": 0}'`

## Stage 7: Evaluation

Post-deployment eval runs against held-out test sets:

- **Standard eval**: 300 prompts across 10 categories
- **Deep eval**: 100 prompts across 9 categories with multi-step reasoning
- **Metrics**: JSON validity rate, verdict match accuracy, score MAE, task completion rate
- **A/B comparison**: New model vs. previous version on identical prompts

Results feed back into the curator planner: weak performance in a category triggers targeted cook orders for that domain.
