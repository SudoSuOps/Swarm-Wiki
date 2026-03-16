# Infrastructure

Hardware fleet for training, inference, and edge deployment.

## Fleet Overview

| Node | CPU | RAM | GPU | Role | SSH |
|------|-----|-----|-----|------|-----|
| swarmrails | Xeon w9-3475X 36C/72T | 256GB DDR5 | RTX PRO 4500 (32GB) + RTX PRO 6000 (96GB) | Primary training + inference | `ssh swarmrails` |
| whale | Ryzen 9 5900X 12C/24T | 64GB DDR4 | RTX 3090 (24GB) | Secondary training/eval | `ssh whale` |
| signal-edge-01 | Jetson Orin Nano | 8GB | Orin iGPU (sm_87) | Edge cook node | `ssh sigedge@192.168.0.79` |
| zima-edge-1 (bee) | Intel N150 4C/4T | 16GB DDR5 | None (CPU only) | Finalize + audit + staging + signal | `ssh dev@192.168.0.70` |
| nas (DS1525+) | AMD Ryzen V1500B 4C/8T | 8GB ECC DDR4 | None | NFS storage + model vault | `ssh admin@192.168.0.102` |

## Total Compute

| Resource | Total |
|----------|-------|
| GPU VRAM | 160GB (32 + 96 + 24 + 8) |
| System RAM | 350GB (256 + 64 + 8 + 16 + 8) |
| CPU Cores | 60C/108T |
| NVMe Storage | ~6TB + 1.8TB NAS RAID 1 |
| Network | 10G (swarmrails + whale NICs) + 1G (edge + NAS) |

## GPU Architecture

Both swarmrails GPUs are Blackwell (sm_120) -- single CUDA toolkit, no split builds needed. whale has Ampere (sm_86). Jetson has Orin (sm_87).

| GPU | Architecture | SM | VRAM | Node |
|-----|-------------|-----|------|------|
| RTX PRO 4500 | Blackwell | sm_120 | 32GB | swarmrails GPU 0 |
| RTX PRO 6000 | Blackwell | sm_120 | 96GB | swarmrails GPU 1 |
| RTX 3090 | Ampere | sm_86 | 24GB | whale |
| Orin Nano | Orin | sm_87 | 8GB shared | signal-edge-01 |

## Software Stack

| Component | Version | Nodes |
|-----------|---------|-------|
| CUDA | 12.8 | swarmrails |
| CUDA | 12.6 | signal-edge-01 |
| PyTorch | CUDA 12.8 | swarmrails |
| vLLM | 0.17.0 | swarmrails |
| Unsloth | 2026.3.4 | whale, swarmrails |
| llama.cpp | latest | swarmrails (sm_86 only, needs rebuild), signal-edge-01 (sm_87) |
| Python | 3.13 | local |
| Python | 3.12.3 | whale |
| uv | 0.10.6 | local, whale, swarmrails |

## Fleet Distribution (Active 2026-03-16)

```
Cook (OpenAlex)   -> swarmrails GPU 1 (Nemotron Nano FP8, 20 workers, 0.8 pairs/s)
Cook (Legal)      -> OpenRouter fleet (12 workers, 8.2/min)
Cook (ASRS)       -> whale (4B base, 4 workers, RJ-gated)
Cook (Edge)       -> signal-edge-01 (4B Q4_K_M, full GPU offload, 12 pairs/hr)
Self-Healing      -> swarmrails GPU 0 (SwarmJelly-4B BF16, RTX 4500)
Finalize/Audit    -> bee (N150, auto-watcher + MinIO staging)
Signal Processing -> bee (swarmsignal, 29K sources/day)
Storage           -> NAS (Synology DS1525+, NFS to all nodes)
Controller        -> swarmrails :9000 (orchestration daemon)
```

Cook fleet runs Nemotron Nano (FP8) on GPU 1 and base Qwen3.5-4B on whale/jetson, all with RJ-aligned prompts from cook-domain-prompts (15 domains). SwarmJelly GPU inference on RTX 4500 processes propolis failures into training pairs.

## Section Index

- [swarmrails](swarmrails.md) -- Primary GPU server
- [whale](whale.md) -- Secondary training/eval node
- [Edge Nodes](edge-nodes.md) -- Jetson + Zima/Bee edge devices
- [NAS](nas.md) -- Synology DS1525+ storage backbone
- [Swarm Controller](swarm-controller.md) -- Central orchestration daemon (:9000)
- [GPU Operations](gpu-operations.md) -- Power limits, CUDA, vLLM flags
- [Networking](networking.md) -- IPs, ports, SSH, Cloudflare
