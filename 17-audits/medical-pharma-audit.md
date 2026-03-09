# Medical & Pharma Audit

## Market Position: Defensible But Crowded

Healthcare captures ~50% of all vertical AI spend (~$1.5B in 2025).

## Competitors

| Player | Valuation | Focus | Fine-tuned? |
|--------|-----------|-------|-------------|
| Hippocratic AI | $3.5B | Patient-facing clinical AI agents | YES |
| Insilico Medicine | IPO'd (HK) | AI drug discovery (Pharma.AI) | YES |
| Google Med-PaLM | Internal | Clinical question answering | YES |
| Recursion | Public ($4B+) | AI drug discovery platform | YES |
| Tempus | $6.1B | Precision medicine, genomics | YES |

## Swarm Medical Assets

| Asset | Count |
|-------|-------|
| Medical training pairs | 432,196 |
| Pharma trajectory pairs | 28,624 |
| Medical specialties | 92 |
| Pharma task types | 16 |
| Medical skills | 9 |
| CoVe pass rate | 77.9% (medical), 76.1% (aviation) |

### Medical Skills (9)

drug_interaction, med_reconciliation, dose_calculator, anticoag_advisor, allergy_check, pgx_advisor, adverse_event, pregnancy_safety, med_safety

### Pharma Trajectory (Unique Differentiator)

5-step clinical pharmacist trajectory:
```
IDENTIFY -> MECHANISM -> ASSESS -> CALCULATE -> RECOMMEND
```

28,624 trajectory-enhanced pairs, 27 shards, labeled `trajectory=true v1`. This sequential reasoning format is unique in the market.

## SwarmPharma-35B

| Property | Value |
|----------|-------|
| Base | Qwen3.5-35B-A3B (MoE) |
| Status | DONE |
| Training pairs | 25,600 |
| Steps | 2,402 |
| Final loss | 0.337 |
| Location | swarmrails:/data2/swarmpharma-35b/ |
| GGUF | Q4_K_M (20GB) |
| Quality | Zero quantization loss (Q4_K_M eval = fp16 eval) |

## Competitive Differentiation

**Strengths:**
- 432K medical + 29K pharma pairs is substantial volume
- 5-step trajectory format is unique
- CoVe 2-stage verification (rewrite + 235B verify)
- SwarmPharma-35B trained with excellent loss (0.337)
- 92 medical specialties — broad coverage

**Risks:**
- Well-funded competitors with regulatory expertise (FDA pathways, HIPAA)
- Commercialization requires clinical validation partnerships
- Healthcare is HIGH RISK under EU AI Act (health/safety decisions)
- Medical AI requires formal clinical trials for patient-facing deployment

## Regulatory Exposure

### EU AI Act (August 2, 2026)

Medical AI = HIGH RISK classification. Requirements:
- Risk management framework (NOT STARTED)
- Technical documentation (PARTIAL)
- Bias assessment (NOT STARTED)
- Human oversight mechanisms (NOT STARTED)

### FDA

- January 2025 draft guidance for AI-enabled device software functions
- If SwarmPharma-35B influences GxP decisions, device-level controls required
- Clinical validation studies needed before any patient-facing deployment

## Growth Targets

| Vertical | Current | Target (6mo) | Priority |
|----------|---------|--------------|----------|
| Medical | 432K | 500K | P1 |
| Pharma | 29K | 100K | P1 |

## R2 Buckets

- `sb-medical`: ~432,196 pairs (403,572 base + 28,624 trajectory)
  - trajectory/ prefix: 28,624 pairs, 27 shards
- CoVe promoted medical: 8,532 PASS, 2,192 FAIL
