# Factory Protocol

The dataset factory is a 10-stage pipeline that produces verified training pairs from structured deal skeletons. Code lives in `data/factory/`.

## Pipeline Stages

### 1. Skeleton
Generate deal structure: asset type, market, tenant, lease terms, capital stack. Deterministic -- no LLM calls. Skeletons define the numeric ground truth that all downstream stages must preserve.

### 2. Generate
Two-tier LLM generation via Together.ai:
- **GEN pass**: `Qwen/Qwen3-Next-80B-A3B-Instruct` generates the initial pair from the skeleton
- **PASS rewrite**: `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` rewrites for quality and correctness

Cost: approximately $0.005/pair on Together.ai serverless.

### 3. Validate
Schema and sanity checks. Ensures the output is valid JSON with the correct messages structure, all required fields are present, and values are within plausible ranges.

### 4. Judge
Quality scoring. Originally a separate SwarmJudge model -- killed 2026-03-06. Now handled by:
- 6 deterministic gates in `data/factory/gates.py` (see [quality-gates.md](quality-gates.md))
- SwarmCurator-27B for subjective quality assessment when needed

### 5. Trajectory
5-step reasoning enhancement for complex pairs:
1. **IDENTIFY** -- Extract key variables and constraints
2. **CALCULATE** -- Perform required computations
3. **ANALYZE** -- Interpret results in context
4. **EVALUATE** -- Assess risk/opportunity
5. **RECOMMEND** -- Provide actionable conclusion

Applied to pharma pairs (28,624 trajectory-enhanced in sb-medical) and select CRE tasks. Pairs are labeled `trajectory=true`.

### 6. Promote
CoVe (Chain of Verification) two-stage promotion:
- **Rewrite**: Llama-3.3-70B-Instruct-Turbo rewrites the pair
- **Score**: Qwen-235B scores on 5 criteria (each 1-5):
  - accuracy
  - completeness
  - structure
  - relevance
  - sft_quality

**Promotion thresholds**: total >= 20/25, all criteria >= 3, accuracy >= 4.

Promoted data paths:
- Medical PASS: `/home/swarm/Desktop/gold-for-cove/promoted/platinum_promoted.jsonl` (8,532 records)
- Medical FAIL: `/home/swarm/Desktop/gold-for-cove/promoted/failed.jsonl` (2,192 records)
- Aviation PASS: `/home/swarm/Desktop/swarmrouter/aviation_promoted/platinum_promoted.jsonl` (15,236 records)
- Aviation FAIL: `/home/swarm/Desktop/swarmrouter/aviation_promoted/failed.jsonl` (3,945 records)

### 7. Failure
Failure mode handling and retry logic. Pairs that fail any gate get logged with the failure reason and can be retried with adjusted prompts or parameters.

### 8. Dedup
MD5 fingerprint on normalized text. The normalized form strips whitespace and lowercases before hashing. Duplicates are rejected at the shard level.

### 9. Audit
18 integrated audits run across the dataset checking for distribution balance, label consistency, numeric accuracy, and format compliance.

### 10. Publish
Three destinations:
- **R2**: Per-vertical bucket upload as JSONL shards
- **Supabase**: Streaming insert for queryable access
- **HCS Seal**: SHA-256 hash published to Hedera Consensus Service for immutable provenance (via `data/factory/merkle.py` + `hedera_bridge.py` + `guarantee.py`)

## CRE Factory

The CRE-specific factory lives at `/home/swarm/Desktop/swarmrouter/data/swarmcre_dataset/`.

- **Output**: `data/swarmcre_dataset/output/swarmcre_train.jsonl` (904,780 records, 1.69 GB)
- **Eval sets**: `eval_gold_2k.jsonl`, `eval_hard_500.jsonl`, `eval_adversarial_500.jsonl` (3,000 total)
- **Build**: 100K deals x 10 tasks = ~1M target, 99.2% pass rate, 100 seconds on 8 cores
- **CLI**: `python3 -m data.swarmcre_dataset.make_swarmcre --deals N --shards N [--enrich] [--eval-only] [--status]`

## Capital Markets Cook

Active grinder for capital markets vertical. Example: debt_maturity task at 46.6 pairs/min, targeting 5,000 pairs per task type. Data publishes to R2 banking prefix with zero errors.
