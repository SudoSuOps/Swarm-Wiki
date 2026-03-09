# SwarmCRE-35B

The commercial real estate vertical model. Three versions tell the story of how Swarm learned to train models properly.

## Version History

### v1 -- The QLoRA Mistake

First attempt used QLoRA (quantized LoRA) on Qwen3.5-35B-A3B. This does not work with Qwen3.5 architecture. The model produced degraded output with artifacts from quantization noise bleeding into the adapter weights.

**Lesson**: Qwen3.5 requires bf16 LoRA only. No QLoRA. This applies to all model sizes.

### v2 -- The Generalization Gap

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-35B-A3B (MoE) |
| Training method | bf16 LoRA r=64 alpha=32 |
| Training pairs | 100,000 |
| Steps | 5,000 |
| Status | STOPPED |
| Reason | Generalization gap |
| Checkpoint | NAS:/mnt/swarm/models/swarmcre-35b-v2/ |

v2 trained on 100K pairs and ran for 5,000 steps. Training loss looked good, but the model showed a generalization gap -- it performed well on training-distribution prompts but degraded on out-of-distribution queries. The model had memorized templates rather than learning CRE reasoning.

Root cause identified: insufficient system prompt diversity. The v2 training set used only 2 system prompts across 78K pairs. The model learned to pattern-match on the prompt template rather than the underlying task.

This failure directly informed the training pattern now used across all Swarm models: 30+ unique system prompts, no single prompt exceeding 10% of the training set, 26+ task types.

### v3 -- Planned (SwarmCRE Fleet)

v3 is not a single model but a 4-model fleet. See `swarmcre_build_plan.md` for the full specification.

| Model | Base | Purpose |
|-------|------|---------|
| SwarmCRE-4B | Qwen3.5-4B | Mobile/edge, voice + text app |
| SwarmCRE-9B | Qwen3.5-9B | Desktop appliance |
| SwarmCRE-27B | Qwen3.5-27B Dense | Inference server |
| SwarmCRE-35B v3 | Qwen3.5-35B-A3B | Heavy analysis |

**Plan**: Cook 150K new economy pairs, train 9B first (validates data quality), then 27B, then 35B, then distill to 4B.

**Goal**: Voice + text app store for CRE brokers, desktop appliance, HCS-sealed intelligence objects.

**Estimated cost**: ~$80 API + ~56h GPU sequential.

## CRE Dataset

The CRE training data factory is the most mature in the Swarm ecosystem.

| Metric | Value |
|--------|-------|
| Total pairs | 643,382 (promoted from 881K factory via math verification) |
| Specialties | 10 |
| Asset types | 9 |
| Task types | 8 |
| Source | /home/swarm/Desktop/swarmrouter/data/swarmcre_dataset/ |
| Output | data/swarmcre_dataset/output/swarmcre_train.jsonl (1.69 GB) |

### 9 Asset Types

infill_warehouse, small_bay, flex, cross_dock, cold_storage, IOS (industrial outdoor storage), micro_fulfillment, data_center, industrial_land

### 8 Task Types (with distribution)

| Task | Share | Description |
|------|-------|-------------|
| underwriting_calc | 32% | Cap rate, NOI, IRR, cash-on-cash calculations |
| ic_memo | 22% | Investment committee memoranda |
| lease_reasoning | 15% | Lease structure analysis and comparison |
| market_comp | 11% | Comparable sales and market analysis |
| t12 | ~7% | Trailing 12-month income/expense analysis |
| rent_roll | ~7% | Rent roll analysis and tenant evaluation |
| lease_abstract | ~7% | Lease abstracting and key term extraction |
| risk_triage | 5% | Risk identification and mitigation |

### Eval Sets

| Set | Size | Purpose |
|-----|------|---------|
| eval_gold_2k.jsonl | 2,000 | Standard evaluation |
| eval_hard_500.jsonl | 500 | Difficult edge cases |
| eval_adversarial_500.jsonl | 500 | Adversarial/trick prompts |
| **Total eval** | **3,000** | |

### Data Center Grinder

The DC (data center) asset type includes specialized constants:
- **NVIDIA_GPU_SPECS**: H100 through Vera Rubin generation
- **BLOCKCHAIN_SPECS**: ERC-1400, HTS, tokenization parameters
- **ROI_DATA_SOURCES**: Power cost, cooling efficiency, rack density metrics

### Factory CLI

```bash
python3 -m data.swarmcre_dataset.make_swarmcre \
  --deals N \
  --shards N \
  [--enrich] \
  [--eval-only] \
  [--status]
```

Build: 100K deals x 10 tasks = ~1M target, 99.2% gate pass rate, 100 seconds on 8 cores.

## 19 CRE Skills

SwarmCRE powers the CRE skills defined in SKILL.md:

broker_senior, broker_junior, intelligence_query, bookmaker, deal_tracker, developer, signal_scraper, investor, exchange_1031, market_report, lead_scorer, email_composer, comp_analyzer, rent_roll_analyzer, debt_analyzer, tax_assessor, site_selector, portfolio_optimizer, news_digest
