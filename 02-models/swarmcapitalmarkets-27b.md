# SwarmCapitalMarkets-27B

Capital markets specialist. Covers CMBS, debt maturity analysis, rate advisory, equity advisory, deal origination, macro causality, and deal graph analysis. Currently training on swarmrails.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-27B Dense |
| Architecture | 64 layers, 5120 hidden dim, all 27B active |
| Training method | bf16 LoRA r=64 alpha=32 |
| Training pairs | 45,039 |
| Steps | 844 |
| Step time | ~126 seconds |
| Estimated total time | ~29.5 hours |
| Status | TRAINING |
| Checkpoint | swarmrails:/data2/swarmcapitalmarkets/ |
| Deploy target | swarmrails:8082 vLLM bf16 |

## Training Data Assembly

5-pool assembly with intentional diversity weighting:

| Pool | Share | Pairs | Content |
|------|-------|-------|---------|
| Diversified | 60% | ~27,000 | Broad capital markets coverage across all 8 cook streams |
| RPA (Risk-Parity Augmented) | 25% | ~11,200 | Risk-weighted scenarios, stress tests, tail events |
| Macro + Graph | 8% | ~3,600 | Macroeconomic causality chains, deal relationship graphs |
| Golden | 4% | ~1,800 | Hand-verified exemplars from production signals |
| Mutations | 3% | ~1,400 | Deliberately perturbed scenarios to test robustness |

## 8 Cook Streams

Each cook stream generates training pairs for a specific capital markets domain:

| Stream | Content |
|--------|---------|
| debt_maturity | Loan maturity analysis, refinancing risk, prepayment scenarios |
| cmbs_distress | CMBS loan watchlist, special servicing, workout analysis |
| rate_advisory | Interest rate hedging, swap analysis, rate lock recommendations |
| equity_advisory | Equity raise structuring, LP/GP splits, promote waterfalls |
| valuation_advisory | DCF, direct cap, sales comparison across asset classes |
| deal_origination | Deal sourcing, relationship mapping, pipeline management |
| macro_causality | Fed policy impact chains, yield curve analysis, recession indicators |
| deal_graph | Multi-party deal structures, entity relationships, capital stack mapping |

The debt_maturity stream was the first to grind: 1,500/5,000 pairs completed at 46.6 pairs/minute when the grinder was last checked. Pairs upload to the R2 banking bucket with zero errors.

## Evaluation Framework

| Metric | Value |
|--------|-------|
| Eval prompts | 180 |
| Domains | 11 |
| Difficulty tiers | 5 |

Evaluation covers 11 capital markets domains with 5 difficulty tiers (basic recall through multi-step adversarial). This is more granular than the CRE eval suite because capital markets tasks involve more numerical precision and more complex multi-party structures.

## Deployment Plan

After training completes, SwarmCapitalMarkets-27B deploys to swarmrails:8082 via vLLM, replacing SwarmCurator-27B on that port during capital markets inference sessions. Both models share the same base architecture (Qwen3.5-27B Dense) and the same vLLM configuration.

Long-term: Dedicated GPU allocation as the fleet scales. The capital markets model needs consistent availability for production signal processing, not time-shared with the curator.

## Relationship to CRE

Capital markets is adjacent to but distinct from CRE vertical work:

- **CRE** deals with property-level intelligence: underwriting, lease analysis, tenant evaluation, market comps
- **Capital Markets** deals with financing-level intelligence: debt structures, equity raises, rate hedging, CMBS surveillance

A complete CRE deal involves both: the property analysis (SwarmCRE) and the financing analysis (SwarmCapitalMarkets). The deal machine maps capital markets to the Escrow and Due Diligence stages, where financing terms are negotiated and verified.
