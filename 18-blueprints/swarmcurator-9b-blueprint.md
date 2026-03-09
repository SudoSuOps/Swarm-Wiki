# SwarmCurator-9B Blueprint

**Source**: `~/Desktop/SWARMCURATOR_9B_BLUEPRINT.md` (766 lines)
**Date**: 2026-03-06

## Concept

Replace algorithmic cook planning (`heat * 10 + gap / 1000`) with LLM-based reasoning. The 9B model analyzes market signals, R2 inventory gaps, gate pass rates, and model eval scores to generate reasoned cook orders with explanations.

## 7 Task Types

| Task Type | Share | Purpose |
|-----------|-------|---------|
| Signal Analysis | 25% | Analyze market trends, identify opportunities |
| Inventory Assessment | 15% | Gap analysis across R2 buckets |
| Cook Order Generation | 25% | Prioritized data cooking decisions |
| Quality Monitoring | 15% | Gate failure diagnosis and fixes |
| Training Readiness | 10% | Model readiness assessment |
| Cost Optimization | 5% | Budget efficiency across API spend |
| Pipeline Orchestration | 5% | Execution steps with checkpoints |

## Decision Framework

**Inputs** (structured context):
- Signal heat maps (topic velocity, entity scores)
- R2 inventory (pair counts per vertical/specialty)
- Gate pass rates (6-gate + CoVe results)
- Model eval scores (loss curves, accuracy metrics)

**Outputs** (structured decisions):
- Cook orders (vertical, stream, target count, priority)
- Rationale traces (why this cook, what signal triggered it)
- Quality alerts (anomalous gate failures, data drift)

## Training Strategy

| Phase | Pairs | Method |
|-------|-------|--------|
| Phase 1: Seed | 5K | Together.ai generation from real scenarios |
| Phase 2: Self-play | 15K | Model generates, human curates |
| Phase 3: Production | Ongoing | Real pipeline decisions become training data |

## Training Config

- Base: Qwen3.5-9B
- Method: bf16 LoRA, packing=True
- LR: 5e-5
- Epochs: 1
- GPU: swarmrails GPU 0 (RTX PRO 4500, 32GB)

## Integration

New `curator/planner.py` mode:
- `_plan_with_curator()` — LLM-based planning
- `_plan_algorithmic()` — Fallback (existing heat-based)
- Hybrid mode: algorithmic generates baseline, LLM reviews and adjusts

## Success Criteria

| Metric | Target |
|--------|--------|
| Gate pass rate | >= 85% on cook orders |
| Cost efficiency | 20%+ improvement over algorithmic |
| Human agreement | 80%+ on rationale quality |

## Risk Mitigation

- Hallucination prevention: validate all numeric claims against R2 actuals
- Duplication: cross-reference cook orders against recent runs
- Diversity: enforce system prompt and task type diversity rules
- Fallback: hybrid mode always available
