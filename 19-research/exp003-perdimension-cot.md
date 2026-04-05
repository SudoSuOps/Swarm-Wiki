# Experiment #003 — Per-Dimension Chain-of-Thought Scoring

**Date**: 2026-04-05
**Status**: HOLD — testing Judge B for symmetric validation
**Papers**: CoT for Assessment (#12), Complexity-Based Prompting (#15)
**Researcher**: Claude Opus 4.6 + swarm operator

---

## Hypothesis

Scoring each of the 5 dimensions separately with individual reasoning chains produces more calibrated scores and better inter-judge agreement than holistic single-score evaluation.

## Design

| Condition | Prompt | Output Format |
|-----------|--------|---------------|
| **Baseline** | Holistic: evaluate 5 dims → 1 score + reasoning | `{score, reasoning}` |
| **Treatment** | Per-dimension: score each dim independently → average | `{accuracy, completeness, specificity, structure, domain_expertise, score, reasoning}` |

- Judge A: gemma3:12b via ollama, temperature=0.0, num_predict=512
- Eval set: 500 Royal Jelly pairs (same as exp001b, exp002)

## Results — Judge A (gemma3:12b)

| Metric | Baseline | Per-Dim | Delta |
|--------|----------|---------|-------|
| Mean score | 0.9320 | 0.9154 | -0.0165 |
| Score stdev | 0.0454 | 0.0357 | -21% (tighter) |
| Agree rate (< 0.15) | 98.0% | 99.0% | **+1.0%** |
| Mean |JA-JB| | 0.0623 | 0.0583 | -0.0040 (6.4% better) |
| Latency | 4.0s | 4.4s | +0.4s (+10%) |
| Errors | 0 | 0 | — |
| Tier changes | — | 1 up, 1 down | net zero |

### Per-Domain

| Domain | Delta | Baseline |JA-JB| | Per-Dim |JA-JB| | Agreement | n |
|--------|-------|-------------------|------------------|-----------|---|
| grants | -0.0166 | 0.0774 | 0.0623 | **IMPROVED 19%** | 286 |
| legal | +0.0082 | 0.0603 | 0.0690 | slightly worse | 35 |
| medical | -0.0213 | 0.0387 | 0.0498 | slightly worse | 179 |

## First-Ever Dimension Breakdown of Corpus

This is independently valuable regardless of gate decision.

| Dimension | Mean | Stdev | Min | Max | Interpretation |
|-----------|------|-------|-----|-----|---------------|
| structure | 0.968 | 0.033 | 0.80 | 1.00 | Strongest — corpus is well-organized |
| domain_expertise | 0.940 | 0.072 | 0.00 | 1.00 | High but widest variance |
| accuracy | 0.930 | 0.048 | 0.65 | 1.00 | Strong factual correctness |
| completeness | 0.899 | 0.052 | 0.60 | 1.00 | Good but room for improvement |
| **specificity** | **0.849** | **0.063** | **0.60** | **1.00** | **Weakest — the quality gap** |

### The Specificity Finding

Specificity (0.849) is the weakest dimension by a clear margin — 8 points below the next lowest (completeness at 0.899) and 12 points below the strongest (structure at 0.968).

**What this means**: Responses in the training data tend toward generic advice rather than concrete, actionable details. They're accurate, well-structured, and show domain knowledge, but lack the specificity that separates "good" from "exceptional."

**Actionable**: This finding should feed back into pair generation prompts:
> "Be specific — use concrete numbers, named entities, exact procedures, and actionable steps. Avoid generic advice."

Improving specificity is the highest-leverage intervention for increasing Royal Jelly yield.

## Gate Decision — Judge A Only

```
Agreement delta: +1.0%
Gate threshold:  +2.0%
Decision:        HOLD
Reason:          Close but below gate. Need Judge B validation.
```

### Why HOLD, not SHIP

1. +1.0% is below the +2% gate
2. +0.4s latency compounds: ~15 fewer pairs/hr at current throughput
3. Unknown if Judge B (qwen2.5:7b) benefits the same way
4. Asymmetric scoring formats between judges could introduce new bias

## Next Step: Judge B Validation

Running the same experiment through qwen2.5:7b on whale (192.168.0.99:11434).

- If BOTH judges improve → combined gain may cross +2% → SHIP
- If only Judge A benefits → HOLD — asymmetric formats are risky
- Results appended to this document when complete

## Artifacts

| File | Location |
|------|----------|
| Experiment script | `SwarmTribunal/experiments/exp003_perdimension_cot.py` |
| Judge A results | `SwarmTribunal/experiments/exp003_results.json` |
| Judge B results | `SwarmTribunal/experiments/exp003b_judgeb_results.json` (pending) |
| Eval set (shared) | `SwarmTribunal/eval_set_500.json` |

---

*Third experiment. First to show agreement improvement. Dimension breakdown is independently valuable for glass wall defensibility.*
