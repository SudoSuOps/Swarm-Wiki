# Quality Gates

All quality enforcement uses deterministic code -- no LLM calls. Gates live in `data/factory/gates.py`.

## 6 Deterministic Gates

### 1. json_valid
Validates that the output parses as valid JSON when the task schema expects JSON output. Rejects malformed responses immediately.

### 2. output_length
Enforces minimum character counts:
- JSON responses: minimum 20 characters
- Text responses: minimum 50 characters

Catches empty, truncated, or degenerate outputs.

### 3. numeric_verify
Compares computed values against gold targets from the skeleton. Tolerances:
- Money values: within $1.00
- Rates (cap rate, interest, etc.): within 0.01
- DSCR and ratios: within 0.01

This gate is the reason sb-cre went from 881K factory output to 643K promoted pairs -- 27% of pairs had numeric errors and were rejected.

### 4. concept_present
Checks that domain-specific terms appear in the response. Requires a minimum of 2 hits from the relevant domain vocabulary. Catches off-topic or generic responses that lack domain grounding.

### 5. dedup
SHA-256 fingerprint on normalized text (lowercased, whitespace-stripped), per RJP-1 standard. Any pair whose fingerprint matches an existing pair in the current shard is rejected. Prevents near-identical outputs from inflating the dataset.

### 6. degenerate
Regex pattern: `(.{40,})\1{2,}`

Detects degenerate repetition -- any 40+ character substring repeated 3 or more times. This catches LLM failure modes where the model enters a repetition loop. Matched pairs are rejected outright.

## CoVe Promotion Scoring

After deterministic gates, surviving pairs can be promoted via CoVe (Chain of Verification). This is an LLM-based step using two models in sequence.

### 5 Scoring Criteria (each 1-5)

| Criterion | What It Measures |
|-----------|-----------------|
| accuracy | Factual and numeric correctness |
| completeness | All required elements addressed |
| structure | Proper formatting and organization |
| relevance | On-topic for the vertical and task type |
| sft_quality | Suitable as a supervised fine-tuning example |

### Promotion Thresholds

A pair is promoted to **royal_jelly** tier (RJP-1) if ALL of the following hold:
- Total score >= 20 out of 25
- Every individual criterion >= 3
- Accuracy >= 4

Pairs that pass gates but fall below CoVe promotion thresholds are assigned lower RJP-1 tiers based on JellyScore: honey (>= 85), pollen (>= 70), or propolis (< 70).

**Legacy mapping**: Factory "PLATINUM" = royal_jelly, factory "GOLD" = honey.

## Gate Application Order

Gates run in sequence. A pair that fails any gate is immediately rejected with the gate name and failure reason logged. The order is:

1. json_valid (fast reject for parse failures)
2. output_length (fast reject for empty/short)
3. degenerate (fast reject for repetition)
4. dedup (fingerprint check)
5. concept_present (domain relevance)
6. numeric_verify (math accuracy -- most expensive check)

This ordering minimizes compute by running cheap checks first.

## RJ Quality Filter (3-Gate, Added 2026-03-15)

Cook scripts now run an additional 3-gate quality filter that scores response quality on three axes. This replaced the old binary pass/fail gate that was producing false propolis scores.

### 1. mechanism (Causal Reasoning)

Regex scan for causal connectors: `because`, `therefore`, `which allows`, `this leads to`, `by enabling`, `due to`, `as a result`, `consequently`, `resulting in`, `contributed to`, `led to`, `mitigated`, etc.

Score: count of unique causal connector matches. Measures whether the response explains **why** things happen, not just **what** happened.

### 2. tradeoff (Decision Boundaries)

Regex scan for decision boundary phrases: `instead of`, `better when`, `worse when`, `fails if`, `trade-off`, `however`, `at the cost of`, `limitation`, `advantage over`, `should have`, `could have been avoided`, `deviation from`, etc.

Score: count of unique tradeoff phrase matches. Measures whether the response identifies **conditions that change the outcome**.

### 3. density (Domain Technical Terms)

Regex scan for domain-specific vocabulary. Each domain has its own term list:

- **Aviation**: altitude, airspeed, ATC, TCAS, GPWS, go-around, METAR, CRM, sterile cockpit, etc. (100+ terms)
- **CRE**: cap rate, NOI, DSCR, absorption, tenant, lease, vacancy, etc.
- Other domains: similar domain-specific term lists

Score: count of unique domain term matches. Measures **domain grounding** -- responses that use real terminology vs. generic filler.

### Filler Penalty

A fourth regex scans for generic filler: `widely used`, `very important`, `significant impact`, `plays a key role`, `has been shown`, `in recent years`, etc. Each filler hit reduces the overall score.

### Scoring

```
rj_score = mechanism_hits + tradeoff_hits + density_bucket - filler_penalty
```

Where density_bucket maps raw term count to 0-3 (0-2 terms: 0, 3-5: 1, 6-10: 2, 11+: 3).

The rj_score (0-3) maps to base verification scores:
- 3 -> 90 (honey/royal_jelly)
- 2 -> 78 (pollen/honey)
- 1 -> 55 (propolis)
- 0 -> 30 (propolis, rejected)

Pairs scoring 0 are rejected outright. Bonus points (up to +5) for high mechanism + tradeoff counts can push a score-90 pair to 95 (royal_jelly).

### Impact

Before RJ quality gates (old cook scripts): ASRS pairs scored 30/propolis universally.
After RJ quality gates: same model, same data, now scores 90-95 (honey/royal_jelly). The quality filter was the missing piece -- it enforces the reasoning depth that RJ-aligned prompts are designed to elicit.
