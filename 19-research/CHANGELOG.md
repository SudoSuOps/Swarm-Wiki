# Research Ops Changelog

Every improvement tested against Royal Jelly ground truth. No change ships without a measured delta.

## Status Legend

- **SHIPPED** — Improvement measured, deployed to production
- **HOLD** — Promising but inconclusive, needs larger eval set
- **REVERTED** — Made things worse, documented and moved on
- **TODO** — In the priority queue

## Priority Queue

| # | Improvement | Paper | Effort | Impact | Status |
|---|------------|-------|--------|--------|--------|
| 1 | Test position bias (swap Q&A order) | MT-Bench | LOW | HIGH | **DONE — NO ACTION** |
| 2 | Add few-shot exemplars from RJ deeds | Auto-CoT | LOW | MEDIUM | TODO |
| 3 | Per-dimension CoT scoring | CoT for Assessment | LOW | MEDIUM | TODO |
| 4 | APE-optimize scoring_prompt.py | APE | MEDIUM | HIGH | TODO |
| 5 | Debate pass for high-drift pairs | ChatEval | MEDIUM | MEDIUM | TODO |
| 6 | Chain-of-Verification 2nd pass | CoVe | MEDIUM | MEDIUM | TODO |
| 7 | STaR bootstrap Judge C from traces | STaR | HIGH | HIGH | TODO |
| 8 | Domain-specific judge selection | Dynamic LLM-Agent | HIGH | MEDIUM | TODO |

---

## Experiment Log

### 2026-04-05 — Position Bias (MT-Bench #4) — NO ACTION

**Change**: Swapped user/assistant order in scoring prompt (S→U→A vs S→A→U)
**File**: scoring_prompt.py (not modified — experiment only)
**Eval set**: 600 pairs total (100 pilot + 500 confirmation), RJ tier, score > 0.85
**Baseline (normal)**: mean=0.9319 (n=500)
**Treatment (swapped)**: mean=0.9383 (n=500)
**Delta**: +0.0064 (stdev=0.0539) — below 0.01 significance gate
**Direction**: 40.8% higher swapped, 7.8% higher normal, 51.4% unchanged
**Per-domain**: grants +0.0042 (n=286), medical +0.0113 (n=179), legal -0.0009 (n=35)
**Decision**: NO ACTION — bias exists but is below noise floor for tier classification. Medical shows mild domain-specific bias (+0.0113) worth monitoring. No prompt change warranted.
**Note**: 100-pair pilot showed +0.0107, 500-pair confirmation corrected to +0.0064. Confirms protocol: always run confirmation before shipping.
