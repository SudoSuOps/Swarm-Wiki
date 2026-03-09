# Cook Scripts

Cook scripts generate synthetic training data by prompting large API-hosted models (Together.ai) and collecting structured outputs. Every cook script follows the same CLI pattern and writes sharded JSONL to local disk or R2.

## Together.ai Models

| Role | Model ID | Purpose |
|------|----------|---------|
| GEN | `Qwen/Qwen3-Next-80B-A3B-Instruct` | Primary generation |
| PASS | `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` | Validation / quality pass |

## Universal CLI Pattern

```bash
# Preview what will be generated (no API calls)
TOGETHER_KEY=... python3 -m data.cook_name --dry-run

# Generate all streams with 50 concurrent workers
TOGETHER_KEY=... python3 -m data.cook_name --stream all --workers 50

# Check progress mid-run
TOGETHER_KEY=... python3 -m data.cook_name --status

# Assemble shards into final training JSONL
TOGETHER_KEY=... python3 -m data.cook_name --assemble
```

---

## 1. cook_swarmcurator_9b.py (swarmrouter)

The primary curator cook. Generates multi-turn instruction pairs for the 9B analysis tier.

- **Output**: ~30,000 pairs
- **System prompts**: 30 distinct personas
- **Task types**: 26 -- signal classification, entity extraction, sentiment analysis, market summary, risk assessment, trend detection, event correlation, data normalization, source evaluation, priority ranking, anomaly detection, pattern recognition, temporal analysis, geographic clustering, sector mapping, confidence scoring, chain-of-thought reasoning, comparative analysis, forecast generation, alert composition, report structuring, query decomposition, context retrieval, fact verification, citation linking, response synthesis
- **Methodology**: Each system prompt is paired with multiple task types. The GEN model produces the completion, PASS model validates structure and quality. Failed pairs are retried once then discarded.
- **Cost**: ~$150 at current Together.ai rates

```bash
TOGETHER_KEY=... python3 -m data.cook_swarmcurator_9b --stream all --workers 50
```

## 2. cook_swarmcurator_ops.py (swarmrouter)

Operational-tier cook for fleet management, monitoring, and system health tasks.

- **Output**: ~20,000 pairs
- **System prompts**: 13 operational personas
- **Task types**: 7 -- health check interpretation, resource allocation, load balancing decisions, error triage, deployment planning, capacity forecasting, incident response
- **Cost**: ~$100

```bash
TOGETHER_KEY=... python3 -m data.cook_swarmcurator_ops --stream all --workers 50
```

## 3. cook_swarmcurator_27b.py (swarmrouter)

Strategic-tier cook for high-level decision-making and cross-domain reasoning.

- **Output**: ~18,000 pairs
- **System prompts**: 20 strategic personas
- **Task types**: 8 -- strategic planning, cross-vertical synthesis, portfolio-level analysis, market regime detection, risk aggregation, capital allocation reasoning, regulatory impact assessment, competitive intelligence synthesis
- **Cost**: ~$90

```bash
TOGETHER_KEY=... python3 -m data.cook_swarmcurator_27b --stream all --workers 50
```

## 4. cook_swarmcurator_2b.py (swarmrouter)

Worker-tier cook for fast classification and routing at the edge.

- **Output**: ~9,400 pairs
- **System prompts**: 10 worker personas
- **Task types**: 5 -- signal classification, priority assignment, vertical routing, urgency detection, duplicate flagging
- **Cost**: ~$47

```bash
TOGETHER_KEY=... python3 -m data.cook_swarmcurator_2b --stream all --workers 50
```

## 5. cook_signal_orders.py (swarmrouter)

Generates triage and order data from signal heat scores. Translates raw signal classifications into actionable orders for downstream processing.

- **Output**: Variable (depends on signal volume)
- **Input**: Signal heat scores from SwarmSignal pipeline
- **Output format**: Structured orders with priority, action type, target entity, and confidence

```bash
TOGETHER_KEY=... python3 -m data.cook_signal_orders --stream all
```

## 6. cre_capital_cook.py (swarm-capital-markets)

The capital markets data factory. Eight parallel generation streams covering the full lifecycle of CRE debt and equity transactions.

- **Output**: Variable per stream
- **Streams**: 8 -- debt origination, equity placement, loan workout, distressed assets, capital stack optimization, credit committee, deal packaging, waterfall modeling
- **Task types**: 70+ across all streams
- **Cost**: ~$200-400 depending on volume

```bash
TOGETHER_KEY=... python3 -m data.cre_capital_cook --stream all --workers 50
```

## 7. cook_rpa.py (swarm-capital-markets)

RPA (Robotic Process Automation) cook generating process automation training data across 5 personas using the 235B model for maximum quality.

- **Output**: Variable
- **Personas**: 5 -- loan processor, underwriting analyst, closing coordinator, servicing specialist, compliance officer
- **Model**: Uses PASS (235B) model for generation (not GEN) due to quality requirements

```bash
TOGETHER_KEY=... python3 -m data.cook_rpa --stream all
```

## 8. cook_golden_pairs.py (swarm-capital-markets)

High-quality seed pairs from curated expert prompts. Each of the 109 prompts generates 3 variants (temperature variation) for robust coverage.

- **Output**: 327 pairs (109 x 3 variants)
- **Purpose**: Golden reference set for eval and fine-tuning anchors
- **Quality**: Every pair manually reviewed or PASS-validated

```bash
TOGETHER_KEY=... python3 -m data.cook_golden_pairs --stream all
```

## 9. cook_platinum_mutations.py (swarm-capital-markets)

Hedge-fund grade mutations of golden pairs. Takes existing high-quality pairs and generates adversarial, edge-case, and stress-test variants.

- **Output**: Variable (multiplier on golden pairs)
- **Mutation types**: Parameter perturbation, assumption inversion, market regime shifts, regulatory scenario changes
- **Purpose**: Hardening the model against real-world edge cases

```bash
TOGETHER_KEY=... python3 -m data.cook_platinum_mutations --stream all
```

## 10. make_swarmcre.py (swarmrouter)

Deterministic CRE dataset factory. No API calls required -- generates structured training data from parameterized deal templates using pure Python.

- **Output**: 904,780 records (1.69 GB)
- **Path**: `data/swarmcre_dataset/output/swarmcre_train.jsonl`
- **Deals**: 100,000 synthetic deals x ~10 tasks each
- **Asset types**: 9 -- infill_warehouse, small_bay, flex, cross_dock, cold_storage, IOS, micro_fulfillment, data_center, industrial_land
- **Task types**: 8 -- underwriting_calc (32%), ic_memo (22%), lease_reasoning (15%), market_comp (11%), t12/rent_roll/lease_abstract (~7% each), risk_triage (5%)
- **Pass rate**: 99.2%
- **Performance**: ~100 seconds on 8 CPU cores
- **Eval outputs**: eval_gold_2k.jsonl, eval_hard_500.jsonl, eval_adversarial_500.jsonl (3,000 total)

```bash
# Full factory run
python3 -m data.swarmcre_dataset.make_swarmcre --deals 100000 --shards 10

# Eval sets only
python3 -m data.swarmcre_dataset.make_swarmcre --eval-only

# Status check
python3 -m data.swarmcre_dataset.make_swarmcre --status

# With LLM enrichment (requires API key)
python3 -m data.swarmcre_dataset.make_swarmcre --deals 100000 --shards 10 --enrich
```

### Data Center Grinder Extensions

The DC grinder adds specialized constants for data center underwriting:

- `NVIDIA_GPU_SPECS`: H100 through Vera Rubin power/cooling profiles
- `BLOCKCHAIN_SPECS`: ERC-1400, HTS, tokenization parameters
- `ROI_DATA_SOURCES`: GPU compute ROI benchmarks

These are injected via `constants.py` in the swarmcre_dataset module.
