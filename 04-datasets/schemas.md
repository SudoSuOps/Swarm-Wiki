# Schemas

## Pair Format

Every training pair uses the OpenAI messages schema:

```json
{
  "messages": [
    {"role": "system", "content": "You are a senior CRE analyst..."},
    {"role": "user", "content": "Underwrite this industrial STNL deal..."},
    {"role": "assistant", "content": "Based on the provided lease terms..."}
  ]
}
```

One pair per line in JSONL files. The system message sets the persona and vertical context. The user message contains the task prompt. The assistant message is the training target.

## Labels

Each pair carries metadata labels used for filtering, balancing, and evaluation.

### CRE Labels

| Label | Values | Purpose |
|-------|--------|---------|
| asset_type | infill_warehouse, small_bay, flex, cross_dock, cold_storage, IOS, micro_fulfillment, data_center, industrial_land | Property classification |
| market | Major US MSAs | Geographic context |
| analysis_type | underwriting_calc, ic_memo, lease_reasoning, market_comp, t12, rent_roll, lease_abstract, risk_triage | Task classification |
| capital_stack_type | senior_debt, mezzanine, preferred_equity, joint_venture, bridge, construction | Financing structure |
| risk_type | credit, market, environmental, regulatory, tenant, interest_rate | Risk category |
| decision_class | approve, approve_with_conditions, restructure, decline, watchlist, distressed_opportunity | Underwriting outcome |
| difficulty | easy, medium, hard, expert | Complexity tier |

### Trajectory Label

Pairs with multi-step reasoning carry `trajectory: true` and include a 5-step chain:

1. **IDENTIFY** -- Extract key variables and constraints from the prompt
2. **CALCULATE** -- Perform required computations (NOI, cap rate, DSCR, etc.)
3. **ANALYZE** -- Interpret results in market and deal context
4. **EVALUATE** -- Assess risk factors and opportunity quality
5. **RECOMMEND** -- Provide actionable conclusion with conditions

Currently applied to 28,624 pharma pairs in sb-medical and select CRE tasks.

## Numeric Conventions

All CRE pairs follow strict numeric formatting rules to ensure consistency across the dataset and enable deterministic verification:

| Value Type | Convention | Example |
|------------|-----------|---------|
| Interest/cap rates | Decimal form | 0.065 (not 6.5%) |
| Square footage | Integer | 125000 (not 125,000 or 125K) |
| DSCR | 2 decimal places | 1.25 |
| Loan amounts | Rounded to $100K | $12,500,000 (not $12,487,322) |
| Dollar values | Standard notation | $8,750,000 |
| Percentages in text | Explicit | "6.5%" when written in prose |

These conventions allow the numeric_verify gate to compare computed values against skeleton gold targets with tight tolerances.

## File Naming

- Training data: `swarmcre_train.jsonl`, `shard_NNNN.jsonl`
- Evaluation: `eval_gold_2k.jsonl`, `eval_hard_500.jsonl`, `eval_adversarial_500.jsonl`
- Promoted: `platinum_promoted.jsonl`, `failed.jsonl`
- Master files: `MASTER_PLATINUM.jsonl`, `MASTER_GOLD.jsonl`
