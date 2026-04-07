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
| 2 | Add few-shot exemplars from RJ deeds | Auto-CoT | LOW | MEDIUM | **DONE — NO ACTION** |
| 3 | Per-dimension CoT scoring | CoT for Assessment | LOW | MEDIUM | **SHIPPED** |
| 4 | APE-optimize scoring_prompt.py | APE | MEDIUM | HIGH | **SHIPPED** |
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

### 2026-04-05 — Few-Shot Exemplars (Auto-CoT #7, #13) — NO ACTION

**Change**: Added 3 tier-spanning exemplars (RJ/Honey/Propolis, medical domain) to scoring prompt
**File**: scoring_prompt.py (not modified — experiment only)
**Eval set**: 500 pairs, RJ tier, score > 0.85
**Baseline (zero-shot)**: mean=0.9321, JB agree=98.0%
**Treatment (few-shot)**: mean=0.9168, JB agree=96.8%
**Delta**: -0.0153 score, -1.2% agreement
**Per-domain**: grants agreement improved (+0.0081), legal improved (+0.0209), medical worsened (-0.0191)
**Decision**: NO ACTION — overall agreement worsened. Exemplars from one domain help cross-domain scoring but hurt same-domain via self-reference. Zero-shot prompt is robust at 98% agreement.
**Note**: Negative result — documents that single-domain exemplars are not the right approach. Domain-specific or cross-domain-only exemplars may warrant future testing.

### 2026-04-05 — Per-Dimension CoT (#12, #15) — HOLD

**Change**: Replaced holistic 5-dim scoring with per-dimension independent scoring + average
**File**: scoring_prompt.py (not modified — experiment only)
**Eval set**: 500 pairs, RJ tier, score > 0.85
**Baseline (holistic)**: mean=0.9320 (stdev=0.0454), JB agree=98.0%
**Treatment (per-dim)**: mean=0.9154 (stdev=0.0357), JB agree=99.0%
**Delta**: -0.0165 score, **+1.0% agreement** (first improvement), 21% tighter score spread
**Dimension finding**: specificity=0.849 is weakest; structure=0.968 is strongest
**Per-domain**: grants agreement +19%, medical/legal slightly worse
**Decision**: **SHIPPED** — Judge B validated. Per-dimension scoring deployed to production 2026-04-05 13:51 UTC.
**Key finding**: Specificity is the corpus quality gap. Feed back into pair generation prompts.
**Ship note**: First per-dimension deed SB-2026-0405-019819 confirmed — both judges independently scored specificity=0.85, structure=0.90. 10 data points per deed. 20 new DB columns (bin + deeds). Tribunal runner + deed recorder restarted.

### 2026-04-06 — APE Prompt Optimization (APE #3, OPRO #11) — SHIPPED

**Change**: Added negative exemplar + rubric anchors to scoring prompt opening sentence
**File**: scoring_prompt.py — line 10 modified
**Optimizer**: qwen2.5:32b (different arch from judge, 2.5x larger)
**Judge**: gemma3:12b (Judge A — production scorer)
**Eval set**: 100 pairs (eval_set_100.json — RJ tier, medical + grants)
**Baseline**: mean=0.9236, stdev=0.0300, specificity=0.8673, structure=0.9629
**Treatment (V3 — negative exemplars + rubric anchors)**: mean=0.8735, stdev=0.0445, specificity=0.7895, structure=0.9382
**Delta**: -0.0501 mean, specificity **+9.0% stricter**, spread **+48.3% wider**, structure -2.6%
**Per-domain**: grants mean=0.8926 (n=65), medical mean=0.8422 (n=32) — both safely above RJ 0.75
**Gate**: PASSED — specificity +9.0% (gate: 5%), spread +48.3% (wider = better discrimination)
**Decision**: **SHIPPED** — V3 deployed to production scoring_prompt.py

**What was added**: One sentence to the prompt opening: "For instance, a score of 0.5 for specificity means the response is generic and not sufficiently tailored. Use these scoring anchors: 0.0-0.3 = poor, 0.4-0.6 = adequate, 0.7-0.8 = good, 0.9-1.0 = excellent."

**Why V3 over V5 (aggressive calibration)**: V5 scored medical pairs at 0.7806 mean — too close to the 0.75 RJ threshold. Known-good pairs would be reclassified as honey. V3 is strict enough to fix inflation without over-correcting.

**Why V3 over V1 (rubric anchors only)**: V3 hit specificity harder (-9.0% vs -5.3%) and had wider spread (+48.3% vs +43.7%). The negative exemplar ("0.5 means generic") teaches the judge what BAD looks like — rubric anchors alone don't.

**APE methodology**: Generated 10 candidate prompts via qwen2.5:32b optimizer, screened all 10 on 30 pairs, advanced top 3 to finals on full 100 pairs. Zero errors across 730 scoring calls. Full results: `SwarmTribunal/experiments/exp004_results.json`

**10 variant strategies tested**: rubric anchors, strict auditor persona, negative exemplars, dimension reorder, explicit calibration, red flags, reason-before-score, combo approaches. Key finding: red flags (V6) did nothing; reason-before-score (V7) added spread without fixing inflation; negative exemplars (V3) were the most effective per-token intervention.
