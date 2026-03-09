# Medical Skills (9)

Pharmaceutical and clinical decision support skills. Each skill enforces safety constraints and produces structured outputs suitable for clinical review workflows.

## Skill Inventory

| # | Skill Name | Description | Spec Path |
|---|-----------|-------------|-----------|
| 1 | `drug_interaction` | Check drug-drug interactions -- severity, mechanism, clinical significance | `skills/medical/drug_interaction/SKILL.md` |
| 2 | `med_reconciliation` | Medication reconciliation -- compare admission/discharge/transfer med lists | `skills/medical/med_reconciliation/SKILL.md` |
| 3 | `dose_calculator` | Dosage calculation -- weight-based, renal-adjusted, pediatric, geriatric | `skills/medical/dose_calculator/SKILL.md` |
| 4 | `anticoag_advisor` | Anticoagulation management -- INR targets, bridging, reversal protocols | `skills/medical/anticoag_advisor/SKILL.md` |
| 5 | `allergy_check` | Allergy and cross-reactivity screening -- drug class awareness | `skills/medical/allergy_check/SKILL.md` |
| 6 | `pgx_advisor` | Pharmacogenomic advisor -- CYP enzyme interactions, genotype-guided dosing | `skills/medical/pgx_advisor/SKILL.md` |
| 7 | `adverse_event` | Adverse event identification and reporting -- FDA MedWatch categories | `skills/medical/adverse_event/SKILL.md` |
| 8 | `pregnancy_safety` | Pregnancy safety classification -- FDA categories, lactation risk | `skills/medical/pregnancy_safety/SKILL.md` |
| 9 | `med_safety` | General medication safety -- black box warnings, REMS, contraindications | `skills/medical/med_safety/SKILL.md` |

## Clinical Workflow Coverage

```
Admission       → med_reconciliation, allergy_check, drug_interaction
Prescribing     → dose_calculator, pgx_advisor, pregnancy_safety
Monitoring      → anticoag_advisor, adverse_event, med_safety
Discharge       → med_reconciliation, drug_interaction
```

## Usage

```bash
# Check drug interactions
curl -X POST https://router.swarmandbee.com/skill/drug_interaction \
  -H "Content-Type: application/json" \
  -d '{"medications": ["warfarin", "amiodarone", "aspirin"]}'

# Calculate dose
curl -X POST https://router.swarmandbee.com/skill/dose_calculator \
  -H "Content-Type: application/json" \
  -d '{"drug": "vancomycin", "weight_kg": 70, "creatinine_clearance": 45}'

# Get skill spec
curl https://router.swarmandbee.com/skill/drug_interaction/spec
```

## Training Data

Medical skills are backed by training data in the `sb-medical` R2 bucket:

- ~432,196 pairs total (403,572 base + 28,624 trajectory-enhanced pharma)
- 85 specialties
- 28,624 trajectory pairs across 27 shards, 16 pharma task types
- CoVe promoted: 8,532 PASS / 2,192 FAIL (79.6% pass rate)

## Safety Notes

All medical skills include explicit disclaimers that outputs are for clinical decision support only and require human review. No skill produces outputs labeled as definitive clinical recommendations. The structured output format is designed to surface relevant information to clinicians, not replace clinical judgment.
