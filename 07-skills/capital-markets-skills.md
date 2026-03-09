# Capital Markets Skills (7)

CRE debt and equity transaction skills in the `swarm-capital-markets` repo. These cover the full lifecycle of capital markets transactions from deal intake through distribution waterfall modeling.

## Skill Inventory

| # | Skill Name | Description | Spec Path |
|---|-----------|-------------|-----------|
| 1 | `deal_packet` | Parse, normalize, and structure deal inputs from raw documents | `skills/capital_markets/deal_packet/SKILL.md` |
| 2 | `underwrite` | Loan sizing, DSCR calculation, debt yield analysis, binding constraint identification | `skills/capital_markets/underwrite/SKILL.md` |
| 3 | `credit_committee` | IC memo generation, risk assessment, approval recommendation | `skills/capital_markets/credit_committee/SKILL.md` |
| 4 | `distress_analyzer` | Distress diagnosis -- default triggers, recovery path analysis, timeline estimation | `skills/capital_markets/distress_analyzer/SKILL.md` |
| 5 | `loan_workout` | Restructuring options, forbearance terms, note sale analysis, modification scenarios | `skills/capital_markets/loan_workout/SKILL.md` |
| 6 | `cap_stack_builder` | Capital stack optimization -- senior/mezz/equity layering, cost of capital minimization | `skills/capital_markets/cap_stack_builder/SKILL.md` |
| 7 | `waterfall_model` | JV and fund distribution waterfalls -- preferred returns, catch-up, promote tiers | `skills/capital_markets/waterfall_model/SKILL.md` |

## Deal Lifecycle Mapping

```
Deal Intake     → deal_packet
Underwriting    → underwrite, cap_stack_builder
Committee       → credit_committee
Distress        → distress_analyzer, loan_workout
Distribution    → waterfall_model
```

## Skill Files

Each capital markets skill includes:

| File | Status | Description |
|------|--------|-------------|
| `SKILL.md` | All 7 | YAML frontmatter + markdown spec |
| `schema.json` | All 7 | JSON Schema for inputs/outputs |
| `validator.js` | Some | Runtime validation for numeric fields and constraint checks |

## Training Data

Capital markets skills are backed by data from the `cre_capital_cook.py` pipeline:

- 8 generation streams with 70+ task types
- Golden pairs: 109 prompts x 3 variants (cook_golden_pairs.py)
- Platinum mutations: hedge-fund grade adversarial variants
- RPA data: 5 personas for process automation
- Eval: 180 prompts, 11 domains, 5 tiers (Bronze through Platinum)

## Underwriting Calculations

The `underwrite` skill performs deterministic calculations that are validated by the factory gates in `data/factory/gates.py`:

| Metric | Formula |
|--------|---------|
| DSCR | NOI / Annual Debt Service |
| Debt Yield | NOI / Loan Amount |
| LTV | Loan Amount / Appraised Value |
| Debt Service | Loan Amount x Mortgage Constant |
| Binding Constraint | min(max LTV, max DSCR, max debt yield) determines loan size |

These are not LLM-generated -- they are deterministic code gates that validate the LLM's output. The 27B model reasons about context and recommendations; the gates enforce mathematical correctness.

## Usage

```bash
# Underwrite a deal
curl -X POST https://router.swarmandbee.com/skill/underwrite \
  -H "Content-Type: application/json" \
  -d '{
    "noi": 500000,
    "purchase_price": 7000000,
    "loan_amount": 4900000,
    "interest_rate": 0.065,
    "amortization_years": 30
  }'

# Generate IC memo
curl -X POST https://router.swarmandbee.com/skill/credit_committee \
  -H "Content-Type: application/json" \
  -d '{"deal_id": "deal_123", "include_risk_matrix": true}'

# Model waterfall distribution
curl -X POST https://router.swarmandbee.com/skill/waterfall_model \
  -H "Content-Type: application/json" \
  -d '{
    "total_distribution": 2500000,
    "lp_commitment": 8000000,
    "gp_commitment": 2000000,
    "preferred_return": 0.08,
    "promote_tiers": [{"irr": 0.12, "split": [0.80, 0.20]}, {"irr": 0.18, "split": [0.60, 0.40]}]
  }'
```
