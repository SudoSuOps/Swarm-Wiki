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
| 1 | Test position bias (swap Q&A order) | MT-Bench | LOW | HIGH | TODO |
| 2 | Add few-shot exemplars from RJ deeds | Auto-CoT | LOW | MEDIUM | TODO |
| 3 | Per-dimension CoT scoring | CoT for Assessment | LOW | MEDIUM | TODO |
| 4 | APE-optimize scoring_prompt.py | APE | MEDIUM | HIGH | TODO |
| 5 | Debate pass for high-drift pairs | ChatEval | MEDIUM | MEDIUM | TODO |
| 6 | Chain-of-Verification 2nd pass | CoVe | MEDIUM | MEDIUM | TODO |
| 7 | STaR bootstrap Judge C from traces | STaR | HIGH | HIGH | TODO |
| 8 | Domain-specific judge selection | Dynamic LLM-Agent | HIGH | MEDIUM | TODO |

---

## Experiment Log

*No experiments run yet. First experiment: position bias test after Gemma 4 cook finishes and GPU0 frees up.*
