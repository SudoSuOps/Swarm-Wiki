# Capital Markets Intelligence Engine

## 7-Layer Architecture

```
Deal Input -> Normalization -> Feature Engineering -> Retrieval -> Reasoning -> Decision -> Output
```

### Layer Details

1. **Input**: Property details, rent roll, NOI, occupancy, market, debt terms, capital stack, sponsor profile, macro assumptions. Formats: form, CSV/JSON, API, manual.
2. **Normalization**: Field mapping, missing detection, unit normalization, sanity checks -> canonical schema.
3. **Feature Engineering**: Cap rate, DSCR, debt yield, loan constant, LTV, LTC, break-even occupancy, equity multiple, IRR sensitivity, refinance probability.
4. **Retrieval**: Context-aware intelligence retrieval — similar deals, distress cases, sector data, workout examples, spread behavior.
5. **Reasoning**: 5 specialist analyst modules — Underwriting, Credit, Capital Markets, Distress, Investment Committee.
6. **Decision**: Structured output — approve / approve_with_conditions / restructure / decline / watchlist / distressed_opportunity. Confidence score, risk flags, loan recommendation.
7. **Output**: Decision summary, full underwriting memo, sensitivity table, credit committee view, JSON API, signal score.

## 4 Product Modes

| Mode | Use Case | Speed |
|------|----------|-------|
| Deal Screen | "Should I look at this deal?" | Fast |
| Credit Memo | Full structured memo for lenders/funds | Medium |
| Scenario Lab | "What happens if rates move 200bps?" | Interactive |
| Distress Mode | Workouts, foreclosure, rescue capital, loan-to-own | Deep |

## Model Stack

- **9B/27B**: Fast screening, structured memo generation
- **35B**: Platinum analysis, hard cases, committee-grade
- **Deterministic**: All math computed by code (DSCR, sensitivity), never by LLM

## MVP (Ship Fast)

Inputs: asset type, purchase price, NOI, rate, requested leverage, market, exit cap

Outputs: max loan size, DSCR, decision, 3 risk flags, 1-page memo

## Eval Suite

- 180 prompts in `eval_swarmcapital.jsonl`
- 11 domains, 5 tiers (Bronze -> Silver -> Gold -> High -> Platinum)
- Decision intelligence prompts test the full engine pipeline
- Temporal deal evolution: same deal across 2019 acquisition -> 2023 rate shock -> 2025 distress/exit
