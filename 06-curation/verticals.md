# Verticals

The curator fleet supports 5 verticals, each implementing the `BaseVertical` ABC from `curator/verticals/`. Configuration lives in `curator/verticals.yaml`.

## BaseVertical ABC

Every vertical must implement:

- `task_types()` -- List of valid task types for this vertical
- `system_prompt(task_type)` -- System message for the given task
- `quality_criteria()` -- Vertical-specific quality checks beyond the 6 universal gates
- `asset_types()` -- Domain-specific asset/entity classifications (if applicable)

This plugin architecture makes adding a new vertical straightforward: implement the ABC, add a YAML entry, and the middleware chain picks it up automatically.

## Vertical Inventory

### CRE (Commercial Real Estate)
- **Status**: OPERATIONAL
- **Focus**: Deal manufacturing, underwriting, capital markets, market intelligence
- **Task types**: underwriting_calc, ic_memo, lease_reasoning, market_comp, t12, rent_roll, lease_abstract, risk_triage, debt_maturity
- **Asset types**: infill_warehouse, small_bay, flex, cross_dock, cold_storage, IOS, micro_fulfillment, data_center, industrial_land
- **Dataset**: sb-cre (643,382 pairs, 10 specialties)
- **Notes**: The founding vertical. Built on decades of real brokerage deal-making experience. Every task type maps to a real step in the CRE deal lifecycle.

### Medical
- **Status**: OPERATIONAL
- **Focus**: Drug interactions, dosing calculations, medication reconciliation, safety checks
- **Task types**: drug_interaction, dose_calculator, med_reconciliation, anticoag_advisor, allergy_check, pgx_advisor, adverse_event, pregnancy_safety, med_safety
- **Dataset**: sb-medical (432,196 pairs, 85 specialties)
- **Notes**: Includes 28,624 trajectory-enhanced pharma pairs with 5-step reasoning chains across 16 pharma task types.

### Aviation
- **Status**: OPERATIONAL
- **Focus**: Safety analysis, maintenance scheduling, logistics optimization
- **Dataset**: sb-aviation (45,222 pairs, 157 specialties)
- **Notes**: 25,014 pairs ground on whale (RTX 3090) to supplement the initial 20,208 pair base.

### Drone
- **Status**: OPERATIONAL
- **Focus**: Regulatory compliance, flight operations, route planning
- **Dataset**: sb-drone (6,755 pairs, 176 specialties)
- **Notes**: Newest vertical. High specialty count relative to pair count -- broad coverage, shallow depth. Priority for next grind cycle.

### Signal
- **Status**: OPERATIONAL
- **Focus**: Market intelligence, trend detection, cross-vertical correlation
- **Notes**: Meta-vertical that processes signal pipeline output. Generates market analysis and trend report pairs rather than domain-specific task pairs.

## Configuration (verticals.yaml)

Each vertical entry in `curator/verticals.yaml` defines:

```yaml
cre:
  name: Commercial Real Estate
  enabled: true
  task_types:
    - underwriting_calc
    - ic_memo
    - lease_reasoning
    # ...
  system_prompt_template: "You are a senior CRE analyst..."
  quality_criteria:
    numeric_tolerance: 0.01
    required_concepts: ["cap_rate", "noi", "dscr"]
  asset_types:
    - infill_warehouse
    - small_bay
    # ...
```

The middleware chain reads this config via FleetContext and passes it to the relevant vertical implementation at each processing step.

## Adding a New Vertical

1. Create `curator/verticals/new_vertical.py` implementing `BaseVertical`
2. Add entry to `curator/verticals.yaml`
3. Create SKILL.md files in `skills/new_vertical/` (optional, for skill-aware tasks)
4. Create R2 bucket `sb-new-vertical` for data storage
5. Run `python3 -m curator fleet --dry-run` to verify discovery and routing
