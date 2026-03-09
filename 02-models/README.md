# Swarm Model Fleet

Every model in the Swarm ecosystem, its status, and where it runs.

## Fleet Roster

| Model | Base | Status | Pairs | Steps | Loss | Location |
|-------|------|--------|-------|-------|------|----------|
| [SwarmCurator-27B](swarmcurator-27b.md) | Qwen3.5-27B Dense | DEPLOYED | 62K | 1,000 | 0.477 | swarmrails:8082 vLLM bf16 GPU1/Blackwell |
| [SwarmCurator-9B](swarmcurator-9b.md) | Qwen3.5-9B | DEPLOYED | 46K | 414 | 0.707 | swarmrails:8081 vLLM bf16 GPU0 |
| [SwarmCurator-2B](swarmcurator-2b.md) | Qwen3.5-2B | DONE | 9.4K | 224 | 0.880 | whale:~/swarmcurator-2b/merged/ |
| [SwarmCapitalMarkets-27B](swarmcapitalmarkets-27b.md) | Qwen3.5-27B Dense | TRAINING | 45K | 844 | TBD | swarmrails:/data2/swarmcapitalmarkets/ |
| [SwarmPharma-35B](swarmpharma-35b.md) | Qwen3.5-35B-A3B | DONE | 25.6K | 2,402 | 0.337 | swarmrails:/data2/swarmpharma-35b/ |
| [SwarmCRE-35B](swarmcre-35b.md) | Qwen3.5-35B-A3B | STOPPED | 100K | 5,000 | gen gap | NAS |
| [SwarmResearch-32B](swarmresearch-32b.md) | Qwen2.5-32B | DONE | 35.5K | 2,220 | 0.635 | swarmrails:/data2/swarm-research-32b/ |
| [BeeMini Router v2](beemini-router.md) | Qwen2.5-3B | DONE | 60K | 693 | 0.026 | swarmrouter-v2-q4_k_m.gguf (1.8GB) |
| [SwarmSignal-2B](swarmcurator-2b.md) | Qwen3.5-2B | LIVE | Custom | 224 | 0.880 | signal-edge-01, zima-edge-1 |

## Fleet Topology

```
                    Strategic Layer
                   SwarmCurator-27B (Blackwell 96GB)
                   SwarmCapitalMarkets-27B (training)
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

## Training Pattern

All models follow the same recipe. See [training-patterns.md](training-patterns.md) for the full reference.

Short version:
- Unsloth FastLanguageModel + TRL SFTTrainer
- bf16 LoRA only (no QLoRA for Qwen3.5)
- packing=True, AutoTokenizer bypass
- 30+ system prompts, 26+ task types, no single prompt > 10%
- Early stopping patience=3 on eval_loss

## Deployment Targets

| Tier | Hardware | Models | Serving |
|------|----------|--------|---------|
| Edge | Jetson Orin Nano 8GB | SwarmSignal-2B Q4_K_M | llama.cpp CPU |
| Edge | zima-edge-1 N150 14GB | SwarmSignal-2B Q4_K_M | Python + systemd |
| Inference | whale RTX 3090 24GB | SwarmCurator-2B, BeeMini | llama-server / vLLM |
| Inference | swarmrails GPU0 32GB | SwarmCurator-9B bf16 | vLLM 0.17.0 |
| Strategic | swarmrails GPU1 96GB | SwarmCurator-27B bf16 | vLLM 0.17.0 |
| Training | swarmrails both GPUs | Any model up to 35B | Unsloth |

## Grand Data Numbers

- 1,158,902+ training pairs across all verticals
- 643K CRE, 432K Medical, 45K Aviation, 6.7K Drone, 31K Core
- R2 buckets: sb-cre, sb-medical, sb-aviation, sb-drone, sb-core, sb-judge
