# Infrastructure

Hardware fleet for training, inference, and edge deployment.

## Fleet Overview

| Node | CPU | RAM | GPU | Role | SSH |
|------|-----|-----|-----|------|-----|
| swarmrails | Xeon w9-3475X 36C/72T | 256GB DDR5 | RTX PRO 4500 (32GB) + RTX PRO 6000 (96GB) | Primary training + inference | `ssh swarmrails` |
| whale | Ryzen 9 5900X 12C/24T | 64GB DDR4 | RTX 3090 (24GB) | Secondary training/eval | `ssh whale` |
| signal-edge-01 | Jetson Orin Nano | 8GB | Orin iGPU (sm_87) | Edge inference | `ssh sigedge@192.168.1.95` |
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

## Fleet Distribution Vision

```
Training          -> swarmrails (Blackwell GPUs)
27B Inference     -> swarmrails GPU 1 (RTX PRO 6000, 96GB)
9B Inference      -> swarmrails GPU 0 (RTX PRO 4500, 32GB)
2B/Edge Inference -> whale (RTX 3090) or signal-edge-01 (Jetson)
Signal Processing -> zima-edge-1 (CPU, 15min cycles)
Router            -> whale (BeeMini GGUF on :8081)
```

## Section Index

- [swarmrails](swarmrails.md) -- Primary GPU server
- [whale](whale.md) -- Secondary training/eval node
- [Edge Nodes](edge-nodes.md) -- Jetson + Zima edge devices
- [GPU Operations](gpu-operations.md) -- Power limits, CUDA, vLLM flags
- [Networking](networking.md) -- IPs, ports, SSH, Cloudflare
