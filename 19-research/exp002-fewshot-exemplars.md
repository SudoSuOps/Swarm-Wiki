# Experiment #002 — Few-Shot Exemplars from Royal Jelly Deeds

**Date**: 2026-04-05
**Status**: COMPLETE — NO ACTION
**Papers**: Auto-CoT (arxiv:2210.03493), Automate-CoT (arxiv:2302.12822)
**Researcher**: Claude Opus 4.6 + swarm operator

---

## Hypothesis

Adding 3 tier-spanning exemplars (Royal Jelly / Honey / Propolis) to the scoring prompt will calibrate Judge A's scoring to better match Judge B, improving inter-judge agreement. The exemplars anchor what different quality levels look like, replacing the current zero-shot approach.

## Design

| Condition | Prompt | Exemplars |
|-----------|--------|-----------|
| **Baseline** | Current zero-shot (5 dimensions, JSON output) | None |
| **Treatment** | Same + 3 condensed exemplars before the pair | RJ (0.92), Honey (0.45), Propolis (0.05) |

- All exemplars sourced from medical domain deeds (highest reasoning quality)
- Condensed format: domain summary + score + reasoning (not full pair text)
- Judge: gemma3:12b via ollama, temperature=0.0
- Eval set: 500 Royal Jelly pairs (same set as exp001b)

## Results

| Metric | Baseline | Few-Shot | Delta |
|--------|----------|----------|-------|
| Mean score | 0.9321 | 0.9168 | -0.0153 |
| Stdev | — | — | 0.0647 |
| Agree rate (< 0.15 drift) | 98.0% | 96.8% | -1.2% |
| Mean |JA-JB| | 0.0622 | 0.0629 | +0.0007 |
| Latency | 2.8s | 3.0s | +0.2s |

### Direction

| Outcome | Count | % |
|---------|-------|---|
| Baseline higher | 281 | 56.2% |
| Few-shot higher | 119 | 23.8% |
| No change (< 0.005) | 100 | 20.0% |

### Per-Domain

| Domain | Delta | Baseline |JA-JB| | Few-Shot |JA-JB| | Agreement | n |
|--------|-------|-------------------|-------------------|-----------|---|
| grants | -0.0045 | 0.0771 | 0.0690 | IMPROVED | 286 |
| legal | -0.0357 | 0.0603 | 0.0394 | IMPROVED | 35 |
| medical | -0.0284 | 0.0386 | 0.0577 | WORSENED | 179 |

### Tier Classification Changes

- Unchanged: 494/500
- RJ → lower: 5
- Lower → RJ: 1
- Net: -4 Royal Jelly pairs

## Analysis

### The exemplars made the judge stricter, not more calibrated

The few-shot prompt shifted Judge A's scoring distribution downward by 0.0153 across all domains. This is a recalibration effect — the exemplars set a higher bar for what constitutes quality. The 0.92 exemplar (best score shown) may have anchored the model's sense of "maximum quality" lower than it naturally scores.

### Cross-domain calibration helped; same-domain self-reference hurt

All three exemplars were medical domain. For non-medical domains (grants, legal), the exemplars improved Judge A's agreement with Judge B — the medical examples taught stricter evaluation that better matched Judge B's already-stricter scoring.

For medical pairs, the opposite occurred. Judge A compared medical pairs against the exemplar medical pairs rather than evaluating on their own merits. This created a self-referential distortion that worsened agreement (0.0386 → 0.0577).

### Legal saw the largest agreement improvement

Legal pairs improved from 0.0603 to 0.0394 mean disagreement — a 35% improvement. Judge A was previously too generous on legal pairs relative to Judge B. The exemplars calibrated it closer.

## Gate Decision

```
Agreement delta: -1.2% (overall worsened)
Threshold:       +2% improvement to ship
Decision:        NO ACTION
```

The cross-domain benefit (grants, legal improved) was offset by the medical self-reference penalty. Net effect: 4 fewer Royal Jelly pairs and worse overall agreement.

## Future Directions

1. **Domain-specific exemplars**: Use grants exemplars for grants, medical for medical. Avoids self-reference while preserving calibration benefit.
2. **Cross-domain only**: Include exemplars from OTHER domains only, never from the pair's own domain.
3. **Selective few-shot**: Apply exemplars only when the judge's first pass produces a borderline score (0.70-0.80).
4. **More exemplar variety**: Test 5+ exemplars spanning more score points.

These are variations for future experiments, not the current priority.

## Artifacts

| File | Location |
|------|----------|
| Experiment script | `SwarmTribunal/experiments/exp002_fewshot_exemplars.py` |
| Results (JSON) | `SwarmTribunal/experiments/exp002_results.json` |
| Eval set (shared) | `SwarmTribunal/eval_set_500.json` |

## Key Takeaway

The zero-shot scoring prompt achieves 98.0% inter-judge agreement. Few-shot exemplars from a single domain improve cross-domain calibration but hurt same-domain scoring through self-reference. The current zero-shot design is robust and difficult to improve with simple exemplar injection. Per-dimension CoT (exp003) is the next approach to try.

---

*Second experiment in the Research Ops pipeline. Negative result documented — prevents repeating this specific approach.*
