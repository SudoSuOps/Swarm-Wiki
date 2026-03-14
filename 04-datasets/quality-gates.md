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
