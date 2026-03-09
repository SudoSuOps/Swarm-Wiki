# Regulatory Audit

## EU AI Act (CRITICAL — August 2, 2026)

**Deadline**: 5 months away. High-risk AI systems must comply.

### Risk Classification

| Vertical | Risk Level | Reason |
|----------|-----------|--------|
| Medical/Pharma | HIGH RISK | Health/safety decisions |
| CRE Underwriting | HIGH RISK | Creditworthiness assessment |
| Aviation | HIGH RISK | Critical infrastructure |
| Signal/Curation | LOWER RISK | Internal tooling |

### Compliance Status

| Requirement | Status | Action Needed |
|-------------|--------|---------------|
| Risk management framework | NOT STARTED | Document risk assessment per vertical |
| Technical documentation | PARTIAL | Code comments + MEMORY.md exist, need formal docs |
| Data governance measures | PARTIAL | Quality gates + provenance exist, need formal policy |
| Bias assessment | NOT STARTED | Statistical bias analysis of training data |
| Human oversight mechanisms | NOT STARTED | Define human review checkpoints |
| Operational logging | PARTIAL | Supabase logs exist, need formalization |
| Transparency obligations | NOT STARTED | User-facing AI disclosure |

**Penalties**: Up to 35M EUR or 7% of worldwide turnover.

### Recommendation

Begin EU AI Act compliance documentation immediately. The data governance foundation exists (quality gates, manifests, Supabase logging) but needs formal documentation and policy wrapping. Start with CRE (lowest regulatory friction, highest commercial readiness).

## FDA (Medical/Pharma)

- January 2025 draft guidance for AI-enabled device software functions
- If SwarmPharma-35B influences GxP decisions, device-level controls required
- Clinical validation studies needed before patient-facing deployment
- 21 CFR Part 11 compliance for electronic records

## FAA (Aviation)

- Roadmap for AI Safety Assurance published
- Existing authorities cover AI in ATC and onboard systems
- Any aviation-specific model deployment requires FAA engagement
- ITAR implications for defense-adjacent aviation data

## Data Sovereignty

All training data, models, and inference run on-premises (swarmrails, whale). No cloud dependency for core pipeline.

| Aspect | Status |
|--------|--------|
| Data residency | On-premises (US) |
| Model weights | Self-hosted |
| Inference | Self-hosted (vLLM, llama-server) |
| API calls (cook) | Together.ai (external, for generation only) |
| Storage | R2 (Cloudflare) + local NVMe |

## License Compliance

| Source | License | Risk |
|--------|---------|------|
| Qwen3.5 base models | Apache 2.0 | Low |
| Together.ai API outputs | Check ToS for derivative works | Medium |
| Public records (EDGAR, assessor) | Public domain | Low |
| Unsloth | Apache 2.0 | Low |
| vLLM | Apache 2.0 | Low |

**Action**: Document provenance and usage rights for all training data sources. Synthetic data from Together.ai API may have usage restrictions.

## Priority Actions

### P0 (Next 30 Days)

1. EU AI Act documentation sprint — formal data governance docs for CRE
2. Seal eval sets — SHA256-lock, separate from training R2 buckets
3. Cross-vertical dedup audit — MinHash sweep to quantify contamination

### P1 (Next 90 Days)

4. Enable experiment tracking (W&B or MLflow)
5. Data lineage document per vertical (source -> cook -> gate -> R2 -> train -> model)
6. License audit for all training data sources
