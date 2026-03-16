# Infrastructure

Hardware fleet for training, inference, and edge deployment.

## Fleet Overview

| Node | CPU | RAM | GPU | Role | SSH |
|------|-----|-----|-----|------|-----|
| swarmrails | Xeon w9-3475X 36C/72T | 256GB DDR5 | RTX PRO 4500 (32GB) + RTX PRO 6000 (96GB) | Primary training + inference | `ssh swarmrails` |
| whale | Ryzen 9 5900X 12C/24T | 64GB DDR4 | RTX 3090 (24GB) | Secondary training/eval | `ssh whale` |
| signal-edge-01 | Jetson Orin Nano | 8GB | Orin iGPU (sm_87) | Edge cook node | `ssh sigedge@192.168.0.79` |
| zima-edge-1 | Intel N150 4C/4T | 14GB LPDDR5 | None (CPU only) | Signal + edge services | `ssh dev@192.168.0.70` |

## Total Compute

| Resource | Total |
|----------|-------|
| GPU VRAM | 160GB (32 + 96 + 24 + 8) |
| System RAM | 342GB (256 + 64 + 8 + 14) |
| CPU Cores | 56C/100T |
| NVMe Storage | ~6TB |
| Network | 10G (swarmrails + whale NICs) + 1G (edge) |

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
| Unsloth | 2026.2.1 | whale, swarmrails |
| llama.cpp | latest | swarmrails (sm_86 only, needs rebuild), signal-edge-01 (sm_87) |
| Python | 3.13 | local |
| Python | 3.12.3 | whale |
| uv | 0.10.6 | local, whale, swarmrails |

## Fleet Distribution (Active 2026-03-16)

```
Cook (OpenAlex)   -> swarmrails GPU 0+1 (dual 4B base, 16 workers, ~810 tok/s)
Cook (ASRS)       -> whale (4B base, 4 workers, RJ-gated)
Cook (Edge)       -> signal-edge-01 (4B Q4_K_M, full GPU offload, 12 pairs/hr)
Self-Healing      -> swarmrails CPU (SwarmJelly-4B, AMX, 1083 tok/s)
Signal Processing -> zima-edge-1 (CPU, 15min cycles)
```

All cook nodes run base Qwen3.5-4B with the Prompt Machine (10 mutations, softmax allocation). Fine-tuned model inference (9B, 27B) paused while the cook fleet scales to 1.5M+ verified pairs.

## Section Index

- [swarmrails](swarmrails.md) -- Primary GPU server
- [whale](whale.md) -- Secondary training/eval node
- [Edge Nodes](edge-nodes.md) -- Jetson + Zima edge devices
- [GPU Operations](gpu-operations.md) -- Power limits, CUDA, vLLM flags
- [Networking](networking.md) -- IPs, ports, SSH, Cloudflare
