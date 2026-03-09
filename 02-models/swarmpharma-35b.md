# SwarmPharma-35B

Pharmaceutical and medical intelligence specialist. Built on the Qwen3.5 MoE architecture with 256 experts and only 3B active parameters per token, making it efficient enough to run inference on a single 24GB GPU in quantized form.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-35B-A3B (MoE) |
| Architecture | 256 experts, 8+1 active per token, 3B active params |
| Expert intermediate dim | 512 |
| Total parameters | 35B (3B active) |
| Vocabulary | 248,320 tokens |
| Context | 262K native, 1M via YaRN |
| Training method | bf16 LoRA r=64 alpha=32 |
| Training pairs | 25,600 |
| Steps | 2,402 |
| Train loss | 0.337 |
| Training hardware | swarmrails Blackwell |
| Checkpoint | swarmrails:/data2/swarmpharma-35b/ |
| GGUF | Q4_K_M ~20GB |

## Training Data

25,600 pairs across 85 medical specialties, sourced from the sb-medical R2 bucket (432,196 total pairs available).

Training data composition:
- **Base medical pairs**: 403,572 pairs across 85 specialties (pool)
- **Trajectory-enhanced pharma**: 28,624 pairs with intermediate reasoning steps, 27 shards, 16 pharma task types
- **Training subset**: 25,600 selected pairs emphasizing pharma-specific tasks with trajectory enhancement

The trajectory-enhanced pairs (labeled `trajectory=true v1`) include step-by-step reasoning chains. Instead of just providing the final drug interaction assessment or dose calculation, these pairs show the model how to reason through pharmacokinetics, contraindication checks, and patient-specific factors.

### 16 Pharma Task Types

The 28,624 trajectory pairs cover 16 distinct pharmaceutical tasks, ensuring the model can handle the full scope of clinical pharmacy work rather than overfitting to a narrow set of queries.

## Loss Characteristics

Final train loss of 0.337 is the lowest across all Swarm models. This reflects:
- High consistency in pharmaceutical data (drug interactions follow deterministic rules)
- Trajectory pairs provide explicit reasoning chains the model can learn directly
- MoE architecture allows different experts to specialize in different drug classes

## Medical Skills (9 total)

SwarmPharma-35B powers the medical skills defined in SKILL.md:

| Skill | Description |
|-------|-------------|
| drug_interaction | Check interactions between multiple medications |
| med_reconciliation | Reconcile medication lists across care transitions |
| dose_calculator | Calculate dosing based on patient parameters |
| anticoag_advisor | Anticoagulation therapy management |
| allergy_check | Cross-reference allergies against prescribed medications |
| pgx_advisor | Pharmacogenomics-guided prescribing |
| adverse_event | Adverse event detection and reporting |
| pregnancy_safety | Medication safety during pregnancy |
| med_safety | General medication safety assessment |

## MoE Architecture Notes

The 35B-A3B MoE architecture is key to SwarmPharma's deployment efficiency:

- **256 total experts** with 8+1 (8 routed + 1 shared) active per token
- **3B active parameters** per forward pass -- comparable compute to a 3B dense model
- **Expert specialization**: Different experts activate for different drug classes, interaction types, and clinical scenarios
- **VRAM**: ~20GB quantized (Q4_K_M), ~96GB bf16

This means SwarmPharma can run on a single RTX 3090 (24GB) in Q4_K_M format while delivering specialist-grade output in its trained domain.

**Ollama limitation**: Ollama does NOT support Qwen3.5-35B MoE architecture as of March 2026. Use llama-server or vLLM for inference.

## CoVe Verification Results

Medical pairs underwent CoVe (Chain of Verification) before training:
- **PASS**: 8,532 records (platinum promoted) at `/home/swarm/Desktop/gold-for-cove/promoted/platinum_promoted.jsonl`
- **FAIL**: 2,192 records at `/home/swarm/Desktop/gold-for-cove/promoted/failed.jsonl`
- **Criteria**: accuracy, completeness, structure, relevance, sft_quality
- **Pass rate**: ~79.5%

The high fail rate (20.5%) compared to CRE data reflects the stricter accuracy requirements for medical content. A wrong cap rate is a bad deal; a wrong drug interaction is a patient safety issue.
