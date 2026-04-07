# Finding: The Five Coordinates — Proof of Location at the Deed Level

**Date**: 2026-04-05
**Source**: Research Ops Experiment #003 (Per-Dimension CoT Scoring)
**Status**: Validated by Judge A (n=500), Judge B validation in progress

---

## The Finding

A single score is an appraisal. Five dimension scores are an inspection report.

When we broke the tribunal's holistic scoring into five independent dimension chains, we didn't just get marginally better agreement (+1.0%). We got something more valuable: the first quantified X-ray of our corpus quality — and a new product layer.

Every deed now has location coordinates.

## The Five Coordinates

```
DEED: SB-2026-0405-012345
TIER: Royal Jelly (0.87)

LOCATION COORDINATES:
  structure:        0.97  ← well-built property
  domain_expertise: 0.94  ← right neighborhood
  accuracy:         0.93  ← clean title
  completeness:     0.90  ← all rooms finished
  specificity:      0.83  ← needs better curb appeal
```

In CRE terms:
- **Structure** = Is the building well-constructed? (Organization, flow, actionability)
- **Domain Expertise** = Is it in the right neighborhood? (Real knowledge, not generic)
- **Accuracy** = Is the title clean? (Facts correct, no liens)
- **Completeness** = Are all the rooms finished? (Fully addresses the scope)
- **Specificity** = Does it have curb appeal? (Concrete details, not boilerplate)

## Corpus Baseline (n=500 Royal Jelly pairs, Judge A)

| Dimension | Mean | Stdev | Interpretation |
|-----------|------|-------|---------------|
| structure | 0.968 | 0.033 | Strongest. The data pipeline produces well-organized responses. |
| domain_expertise | 0.940 | 0.072 | High but widest variance. Some domains deeper than others. |
| accuracy | 0.930 | 0.048 | Strong factual correctness across the board. |
| completeness | 0.899 | 0.052 | Good. Room to improve scope coverage. |
| **specificity** | **0.849** | **0.063** | **Weakest. The quality gap. The curb appeal problem.** |

## The Specificity Gap

Specificity at 0.849 is 12 points below structure at 0.968. This is the single largest quality lever in the corpus.

Responses tend toward generic advice when they should give concrete numbers, named entities, exact procedures, and actionable steps. A medical response that says "consider further evaluation" instead of "order a CT angiogram of the chest and draw a D-dimer" scores lower on specificity.

**Actionable**: Feed back into pair generation prompts:
> "Be specific. Use concrete numbers, named entities, exact procedures, and actionable steps. Avoid generic advice like 'consult a specialist' — name the specialty, the test, the threshold."

This is the highest-ROI quality intervention for increasing Royal Jelly yield.

## Why This Matters — The Inspection Report

An appraisal says: "This property is worth $850K."

An inspection report says: "The foundation is solid (structure: 0.97), it's in a Class A neighborhood (domain expertise: 0.94), title is clean (accuracy: 0.93), all rooms are finished (completeness: 0.90), but the curb appeal needs work (specificity: 0.83). Fix the landscaping and it's a $900K property."

The buyer of a Swarm & Bee dataset doesn't just get "0.87 Royal Jelly." They get the breakdown that proves why, and the prescription for what to improve. The deed becomes a diagnostic tool, not just a quality stamp.

With dual scales, each deed carries **10 data points** (5 dimensions x 2 scales). Two independent architectures (gemma3:12b + qwen2.5:32b) producing dimension-level agreement. Unimpeachable.

## Integration Points

| System | What Changes |
|--------|-------------|
| `scoring_prompt.py` | Per-dimension output format (pending Judge B validation) |
| Deed schema | 10 new fields: `{dim}_{judge}` for each dimension x judge |
| Deed Recorder | Parse and store dimension scores |
| Shop API | Dimension breakdown in deed detail view |
| Offering Memorandum | "Inspection report" framing for investors |
| Swarm-Inspector | Validate dimension consistency across judges |
| swarmandbee.ai/deed | Visual dimension breakdown (radar chart or bar chart) |

## The Proof of Location Stack

```
Layer 1: DEED         — proves provenance (where the data came from)
Layer 2: TITLE        — insures quality (guarantee the score)
Layer 3: PROOF OF LOCATION — proves outcome (the relocation worked)
Layer 4: INSPECTION REPORT — proves WHY (the five coordinates)
         ↑ NEW — unlocked by per-dimension scoring
```

The inspection report is the fourth layer of proof. It completes the stack from "what" to "why."

## Experimental Evidence

| Metric | Holistic (current) | Per-Dimension | Delta |
|--------|-------------------|---------------|-------|
| Inter-judge agreement | 98.0% | 99.0% | +1.0% |
| Score spread (stdev) | 0.0454 | 0.0357 | -21% (tighter) |
| Mean |JA-JB| | 0.0623 | 0.0583 | -6.4% (better) |
| Latency | 4.0s | 4.4s | +10% |
| Tier changes | — | net zero | stable |

The per-dimension format improves every calibration metric while adding only 0.4s per pair. The latency cost is justified by the 5x increase in deed defensibility.

---

*The glass wall doesn't just get thicker. It gets transparent in the right places — showing exactly what's behind each score, not hiding behind a single number.*
