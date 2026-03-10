# Swarm Model Fleet

Every model in the Swarm ecosystem, its status, and where it runs.

## Fleet Roster

| Model | Base | Status | Pairs | Steps | Loss | Location |
|-------|------|--------|-------|-------|------|----------|
| [SwarmAtlas-27B](swarm-atlas-27b.md) | Qwen3.5-27B Dense | DEPLOYED | 45K | 844 | 0.419 | swarmrails:8082 vLLM bf16 GPU1/Blackwell |
| [SwarmCurator-27B](swarmcurator-27b.md) | Qwen3.5-27B Dense | SUPERSEDED | 62K | 1,000 | 0.477 | swarmrails:/data2/swarmcurator-27b/merged/ |
| [SwarmCurator-9B](swarmcurator-9b.md) | Qwen3.5-9B | DEPLOYED | 46K | 414 | 0.707 | swarmrails:8081 vLLM bf16 GPU0 |
| [SwarmCurator-2B](swarmcurator-2b.md) | Qwen3.5-2B | DONE | 9.4K | 224 | 0.880 | whale:~/swarmcurator-2b/merged/ |
| [SwarmPharma-35B](swarmpharma-35b.md) | Qwen3.5-35B-A3B | DONE | 25.6K | 2,402 | 0.337 | swarmrails:/data2/swarmpharma-35b/ |
| [SwarmCRE-35B](swarmcre-35b.md) | Qwen3.5-35B-A3B | STOPPED | 100K | 5,000 | gen gap | NAS |
| [SwarmResearch-32B](swarmresearch-32b.md) | Qwen2.5-32B | DONE | 35.5K | 2,220 | 0.635 | swarmrails:/data2/swarm-research-32b/ |
| [BeeMini Router v2](beemini-router.md) | Qwen2.5-3B | DONE | 60K | 693 | 0.026 | swarmrouter-v2-q4_k_m.gguf (1.8GB) |
| [SwarmSignal-2B](swarmcurator-2b.md) | Qwen3.5-2B | LIVE | Custom | 224 | 0.880 | signal-edge-01, zima-edge-1 |

## Fleet Topology

```
                    Strategic Layer
                   SwarmAtlas-27B (Blackwell 96GB)
                          |
                   Operational Layer
                   SwarmCurator-9B (RTX PRO 4500 32GB)
                          |
                   Specialist Layer
                   SwarmPharma-35B (3B active params)
                   SwarmCRE-35B v2 (3B active params)
                   SwarmResearch-32B (legacy)
                          |
                   Edge Layer
                   SwarmCurator-2B / SwarmSignal-2B
                   BeeMini Router v2
```

## Architecture Generations

**Generation 1 (Qwen2.5)**: SwarmResearch-32B and BeeMini Router v2. Dense transformers with standard attention throughout. Still operational but being superseded.

**Generation 2 (Qwen3.5)**: All other models. Gated Delta Network architecture -- 75% linear attention (O(n)), 25% standard attention. 248K vocabulary. 262K native context. See [qwen35-reference.md](qwen35-reference.md) for full architecture details.

Two form factors in Gen 2:
- **Dense** (9B, 27B): All parameters active on every token. Higher per-token quality, higher VRAM.
- **MoE** (35B-A3B): 256 experts, 8+1 active per token, only 3B parameters active. Lower VRAM, specialist-grade output in trained domains.

## Gold Standard Build

All Qwen3.5 models follow the **Swarm Gold Standard** — a proven training playbook documented at:

**Repo**: [`swarm-qwen-27B-Gold-Standard-Build-LLM`](https://github.com/SudoSuOps/swarm-qwen-27B-Gold-Standard-Build-LLM)

SwarmAtlas-27B (loss **0.419**, 844 steps, 29.32h) is the best build to date, beating the Curator-27B reference (0.477). Every future model starts from this config or gets nuked.

### Config by Tier

| Parameter | 27B | 9B | 2B |
|-----------|-----|----|----|
| LoRA r / alpha | 64 / 32 | 64 / 32 | 32 / 16 |
| Learning Rate | 1e-5 | 1e-5 | 2e-5 |
| Batch × Accum | 2 × 16 | 4 × 8 | 8 × 4 |
| **Effective Batch** | **32** | **32** | **32** |
| Max Seq Len | 4096 | 4096 | 2048 |
| Epoch Fraction | 0.6 | 0.6 | 0.8 |

### Invariants (all tiers)

- Unsloth FastLanguageModel + TRL SFTTrainer
- bf16 LoRA only (no QLoRA for Qwen3.5 — higher quantization error)
- AutoTokenizer bypass (Qwen3.5 VL dispatch bug in unsloth_zoo)
- packing=True (may be skipped by Unsloth VL detection — OK)
- 30+ system prompts, no single prompt > 15%
- Cosine LR scheduler, 5% warmup, weight decay 0.01
- Early stopping patience=3 on eval_loss
- SHA256 on every dataset, MANIFEST.json on every build
- vision_config fix post-merge for vLLM serving

See [gold-standard-build.md](gold-standard-build.md) for the full specification.

## Deployment Targets

| Tier | Hardware | Models | Serving |
|------|----------|--------|---------|
| Edge | Jetson Orin Nano 8GB | SwarmSignal-2B Q4_K_M | llama.cpp CPU |
| Edge | zima-edge-1 N150 14GB | SwarmSignal-2B Q4_K_M | Python + systemd |
| Inference | whale RTX 3090 24GB | SwarmCurator-2B, BeeMini | llama-server / vLLM |
| Inference | swarmrails GPU0 32GB | SwarmCurator-9B bf16 | vLLM 0.17.0 |
| Strategic | swarmrails GPU1 96GB | SwarmAtlas-27B bf16 | vLLM 0.17.0 |
| Training | swarmrails both GPUs | Any model up to 35B | Unsloth |

## Grand Data Numbers

- 1,158,902+ training pairs across all verticals
- 643K CRE, 432K Medical, 45K Aviation, 6.7K Drone, 31K Core
- R2 buckets: sb-cre, sb-medical, sb-aviation, sb-drone, sb-core, sb-judge
