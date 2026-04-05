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
| 4 | APE-optimize scoring_prompt.py | APE | MEDIUM | HIGH | **RUNNING** |
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

### 2026-04-05 — APE Prompt Optimization (APE #3, OPRO #11) — RUNNING

**Change**: Use a stronger LLM (qwen2.5:32b) to generate 10 variant scoring prompts, evaluate each against ground truth, select the winner.
**File**: scoring_prompt.py (will be modified if winner found)
**Optimizer**: qwen2.5:32b (19.9GB Q4) — different architecture family from judge (Qwen vs Gemma), 2.5x larger than judge. Avoids self-preference bias.
**Judge**: gemma3:12b (Judge A — production scorer)
**Eval set**: 100 pairs (eval_set_100.json — RJ tier, medical + grants + legal)
**Baseline**: Current production SCORING_PROMPT (per-dimension CoT from EXP-003)

**Design**:
- Round 1 SCREENING: 10 variants × 30 pairs = 300 scoring calls (~50 min)
- Round 2 FINALS: top 3 variants × 100 pairs = 300 calls (~50 min) + Judge B cross-validation
- Total: ~2-3 hours

**Meta-prompt strategy**:
- Feed optimizer: current prompt + 5 example pairs with known scores
- Tell it what's weak: specificity inflation (0.849), structure inflation (0.968)
- Ask for 10 complete replacement variants
- Constraints: must keep 5-dim JSON format, must keep per-dim reasoning

**Gate**: Ship if ANY of:
- >2% inter-judge agreement improvement
- >5% specificity dimension improvement (stricter scoring)
- Tighter score distribution (lower stdev) without losing discrimination

**Status**: Running in parallel terminal. Results pending.
