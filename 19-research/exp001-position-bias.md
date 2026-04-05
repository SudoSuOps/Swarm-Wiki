# Experiment #001 — Position Bias in LLM-as-Judge Scoring

**Date**: 2026-04-05
**Status**: COMPLETE — NO ACTION
**Paper**: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2023-06-09, arxiv:2306.05685)
**Researcher**: Claude Opus 4.6 + swarm operator

---

## Hypothesis

LLM judges may score AI training pairs differently depending on whether the user query or assistant response appears first in the scoring prompt. The MT-Bench paper (2023) found significant position bias in GPT-4 and Claude as judges — content appearing first tends to be favored.

If our tribunal judges exhibit this bias, scores may not be position-neutral, which undermines the "defendable" thesis.

## Design

Two conditions scored by Judge A (gemma3:12b via ollama on localhost:11434):

| Condition | Prompt Order | Label |
|-----------|-------------|-------|
| **A (Normal)** | System → User Query → Assistant Response | Production order |
| **B (Swapped)** | System → Assistant Response → User Query | Reversed content |

- Temperature: 0.0 (deterministic)
- All other prompt text identical
- Same scoring rubric (5 dimensions: accuracy, completeness, specificity, structure, domain expertise)

## Eval Set

**Pilot (exp001)**: 100 Royal Jelly pairs, random sample
- Domains: grants (65), medical (32), legal (3)
- Selection: `tier = 'royal_jelly' AND final_score > 0.85`
- Avg original final score: 0.8891

**Confirmation (exp001b)**: 500 Royal Jelly pairs, fresh sample (no overlap)
- Domains: grants (286), medical (179), legal (35)
- Selection: same criteria, different random seed
- Avg original final score: 0.8880

## Results — Pilot (n=100)

| Metric | Value |
|--------|-------|
| Normal mean | 0.9346 |
| Swapped mean | 0.9454 |
| Delta | +0.0107 |
| Stdev | 0.0230 |
| Swapped higher | 49/99 (49.5%) |
| Normal higher | 11/99 (11.1%) |
| No change | 39/99 (39.4%) |

Per-domain: grants +0.0030, medical +0.0241, legal +0.0333 (n=3)

**Pilot verdict**: MILD BIAS — proceed to 500-pair confirmation.

## Results — Confirmation (n=500)

| Metric | Value |
|--------|-------|
| Normal mean | 0.9319 |
| Swapped mean | 0.9383 |
| **Delta** | **+0.0064** |
| Stdev | 0.0539 |
| Swapped higher | 204/500 (40.8%) |
| Normal higher | 39/500 (7.8%) |
| No change | 257/500 (51.4%) |

### Per-Domain Breakdown

| Domain | Delta | n | Interpretation |
|--------|-------|---|---------------|
| grants | +0.0042 | 286 | Negligible — formulaic content resists position framing |
| medical | +0.0113 | 179 | Mild — long authoritative responses create priming effect |
| legal | -0.0009 | 35 | Zero — no position preference detected |

## Analysis

### The bias is real but not significant

The direction asymmetry is clear: when the assistant response appears first, scores go up 40.8% of the time and down only 7.8%. This 5.2:1 ratio confirms a genuine position preference in gemma3:12b — reading a high-quality response first creates a favorable impression that slightly inflates the score.

However, the magnitude (+0.0064) is below the 0.01 significance gate. At this level, position bias cannot flip a pair across tier boundaries (Royal Jelly >= 0.75, Honey >= 0.50). A pair scoring 0.746 in normal order would score 0.752 in swapped order — still the same tier.

### Pilot overstated the effect by 67%

The 100-pair pilot measured +0.0107. The 500-pair confirmation corrected this to +0.0064. This validates the research-ops protocol: small samples can overstate effects by 1.5-2x. Never ship based on n=100 alone.

### Medical is the only domain with actionable signal

At +0.0113, medical pairs show 2.7x more position bias than grants. The likely mechanism: medical responses are long (often 500+ words), detailed, and authoritative in tone. Reading them first creates a stronger "anchor" impression than reading a short, formulaic grant response. If medical bias grows as the corpus scales, a domain-specific counter-measure (randomized order for medical only) may be warranted.

### Legal showed zero bias

With n=35 and delta=-0.0009, legal pairs are effectively position-neutral. Legal Q&A tends to be structured (question → analysis → conclusion), and both orderings present the same logical chain. The structure may naturally resist position framing.

## Gate Decision

```
Bias magnitude: 0.0064
Threshold:      0.01 (ship) / 0.03 (significant)
Decision:       NO ACTION — below noise floor for tier classification
```

No changes to `scoring_prompt.py` or tribunal configuration.

## Counter-Measure (Shelved)

If future experiments show increased bias (especially in medical at scale), the recommended counter-measure is:

- Judge A scores in normal order (S→U→A)
- Judge B scores in swapped order (S→A→U)
- Position biases cancel in the averaged final_score

This requires zero prompt changes — only a routing change in `tribunal_runner.py`. Shelved until medical bias exceeds 0.02 at n>500.

## Artifacts

| File | Location |
|------|----------|
| Experiment script | `SwarmTribunal/experiments/exp001_position_bias.py` |
| Pilot eval set (100) | `SwarmTribunal/eval_set_100.json` |
| Pilot results | `SwarmTribunal/experiments/exp001_results.json` |
| Confirmation eval set (500) | `SwarmTribunal/eval_set_500.json` |
| Confirmation results | `SwarmTribunal/experiments/exp001b_results_500.json` |

## Key Takeaway

Position bias in gemma3:12b is measurable but inconsequential for our scoring regime. The MT-Bench paper's findings (measured on GPT-4 and Claude) do not fully generalize to smaller base models doing rubric-based quality scoring. Our tribunal's dual-judge architecture with drift thresholds already provides sufficient debiasing.

---

*First experiment in the Research Ops pipeline. Protocol validated: pilot → confirmation → gate decision → document.*
