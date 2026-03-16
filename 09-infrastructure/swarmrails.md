# swarmrails

Primary training and inference node. Dual Blackwell GPUs with 128GB combined VRAM.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | Intel Xeon w9-3475X 36C/72T, AMX (bf16, int8, tile) |
| RAM | 256GB DDR5 Kingston Fury |
| Storage | 3.6TB NVMe (2.9TB free) |
| GPU 0 | RTX PRO 4500 Blackwell (32GB, sm_120, Bus 0x90) -- installed 2026-03-08 |
| GPU 1 | RTX PRO 6000 Blackwell (96GB, sm_120, Bus 0xCA) |
| NIC | Intel X710 10G |

Both GPUs sm_120 Blackwell -- single CUDA toolkit, no split builds needed.

## Software

| Package | Version |
|---------|---------|
| vLLM | 0.17.0 (PyTorch CUDA 12.8, native sm_86 + sm_120) |
| Unsloth | 2026.3.4 |
| Transformers | 5.2.0 |
| Python | 3.11+ |
| uv | 0.10.6 |
| llama.cpp | At `/home/swarm/llama.cpp/` (built sm_86, needs rebuild for sm_120) |

## Ports

| Port | Service | GPU | Model |
|------|---------|-----|-------|
| 8080 | FastAPI router proxy | CPU | swarmrouter-v2 (Ollama) |
| 8081 | vLLM | GPU 0 (4500, 32GB) | Qwen3.5-4B base (cook, 8 workers) |
| 8083 | vLLM | GPU 1 (6000, 96GB) | Qwen3.5-4B base (cook, 8 workers) |
| 8085 | llama-server | CPU (AMX) | SwarmJelly-4B Q4_K_M (mlock, 1083 tok/s) |

**Note**: GPUs switched from fine-tuned model inference to base 4B cooking as of 2026-03-15. Base 4B + RJ-aligned prompts matches fine-tuned 9B quality (see key finding in [models README](../02-models/README.md)).

## Key Paths

| Path | Content |
|------|---------|
| `/data2/swarmcurator-9b-p2/merged/` | SwarmCurator-9B merged (19GB) |
| `/data2/swarmcurator-27b/merged/` | SwarmCurator-27B merged (52GB) |
| `/data2/swarmcapitalmarkets/` | Capital markets training data + scripts |
| `/data2/swarmpharma-35b/` | SwarmPharma-35B model |
| `/data2/swarm-research-32b/` | SwarmResearch-32B (legacy) |
| `/data2/swarm-qwen27b/` | Training layout (scripts, configs, logs) |
| `/data2/swarm_router_train/` | Router proxy code + decision logs |
| `/tmp/start_vllm_9b.sh` | Launch script for 9B on :8081 |
| `/tmp/start_vllm_27b.sh` | Launch script for 27B on :8082 |

## GPU Ordering

Always set `CUDA_DEVICE_ORDER=PCI_BUS_ID`:

| Index | GPU | VRAM | Bus |
|-------|-----|------|-----|
| 0 | RTX PRO 4500 | 32GB | 0x90 |
| 1 | RTX PRO 6000 | 96GB | 0xCA |

## Power Limits

```bash
sudo nvidia-smi -i 0 -pl 200   # RTX PRO 4500
sudo nvidia-smi -i 1 -pl 350   # RTX PRO 6000
```

## vLLM Launch

```bash
vllm serve /data2/swarmcurator-9b-p2/merged/ \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}' \
  --port 8081
```

Required config fix: copy `vision_config` from base Qwen3.5 into merged `config.json` (`out_hidden_size` must match text `hidden_size`).

## Benchmarks

### Current (Cook Fleet Mode)

| Model | Throughput | VRAM | Workers |
|-------|-----------|------|---------|
| 4B base (GPU 0) | ~400 tok/s | ~9GB | 8 |
| 4B base (GPU 1) | ~410 tok/s | ~9GB | 8 |
| Combined | ~810 tok/s | ~18GB | 16 |
| SwarmJelly CPU | 1,083 tok/s prompt | 0 (AMX) | 1 |

### Previous (Inference Mode)

| Model | Sequential | 4 Concurrent | VRAM |
|-------|-----------|-------------|------|
| 9B bf16 (GPU 0) | ~45 tok/s | 165 tok/s | 23.5GB |
| 27B bf16 (GPU 1) | ~25 tok/s | 88 tok/s | 93GB |

## Access

```bash
ssh swarmrails
```
