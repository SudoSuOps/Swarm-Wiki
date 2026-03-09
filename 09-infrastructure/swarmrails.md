# swarmrails

Primary training and inference node.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | Intel Xeon w9-3475X 36C/72T, AMX (bf16, int8, tile) |
| RAM | 256GB DDR5 Kingston Fury |
| Storage | 3.6TB NVMe (2.9TB free) |
| GPU 0 | RTX PRO 4500 Blackwell (32GB, sm_120, Bus 0x90) — installed 2026-03-08 |
| GPU 1 | RTX PRO 6000 Blackwell (96GB, sm_120, Bus 0xCA) |
| NIC | Intel X710 10G |

Both GPUs sm_120 Blackwell — single CUDA toolkit, no split builds needed.

## Software

- vLLM 0.17.0 (PyTorch CUDA 12.8)
- Unsloth 2026.3.4
- Transformers 5.2.0
- llama.cpp at `/home/swarm/llama.cpp/` (needs rebuild for sm_120)
- Python 3.11+, uv 0.10.6

## Ports

| Port | Service |
|------|---------|
| 8081 | SwarmCurator-9B (vLLM, GPU 0) |
| 8082 | SwarmCurator-27B / SwarmCapitalMarkets-27B (vLLM, GPU 1) |

## Key Paths

| Path | Content |
|------|---------|
| /data2/swarmcurator-9b-p2/merged/ | SwarmCurator-9B merged (19GB) |
| /data2/swarmcurator-27b/merged/ | SwarmCurator-27B merged (52GB) |
| /data2/swarmcapitalmarkets/ | Capital markets training data + scripts |
| /data2/swarmpharma-35b/ | SwarmPharma-35B model |
| /data2/swarm-research-32b/ | SwarmResearch-32B (legacy) |
| /data2/swarm-qwen27b/ | Training layout (scripts, configs, logs) |

## GPU Ordering

Always set `CUDA_DEVICE_ORDER=PCI_BUS_ID`:
- GPU 0 = RTX PRO 4500 (32GB, Bus 0x90)
- GPU 1 = RTX PRO 6000 (96GB, Bus 0xCA)

## Power Limits

```bash
sudo nvidia-smi -i 0 -pl 200   # RTX PRO 4500
sudo nvidia-smi -i 1 -pl 350   # RTX PRO 6000
```

## Access

```bash
ssh swarmrails
```
