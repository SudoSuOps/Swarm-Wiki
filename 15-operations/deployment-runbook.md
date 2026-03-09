# Deployment Runbook

## vLLM Deployment (Production)

### Prerequisites

- vLLM 0.17.0+ with PyTorch CUDA 12.8
- Merged model (not LoRA adapter)
- Qwen3.5 config fix applied (see below)

### Qwen3.5 Config Fix

After Unsloth merge, the `config.json` may have incorrect vision config. Fix:

1. Copy `vision_config` from base Qwen3.5 model into merged `config.json`
2. Ensure `out_hidden_size` matches the text model's `hidden_size`
3. This is required because Unsloth bakes VL architecture into the merge

### Launch Commands

```bash
# 9B on GPU 0 (RTX PRO 4500, 32GB)
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
  vllm serve /data2/swarmcurator-9b-p2/merged/ \
  --served-model-name swarmcurator-9b \
  --port 8081 \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}'

# 27B on GPU 1 (RTX PRO 6000, 96GB)
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
  vllm serve /data2/swarmcurator-27b/merged/ \
  --served-model-name swarmcurator-27b \
  --port 8082 \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}'
```

### Required Flags (Qwen3.5)

| Flag | Why |
|------|-----|
| `--language-model-only` | Skip vision encoder loading |
| `--skip-mm-profiling` | Skip multimodal profiling |
| `--enforce-eager` | FA2 incompatible with sm_120 Blackwell |
| `--limit-mm-per-prompt '{"image": 0}'` | No image inputs |

### Benchmarks

| Model | Throughput | VRAM | Concurrent |
|-------|-----------|------|------------|
| 9B bf16 | 165 tok/s | 23.5GB | 4 |
| 27B bf16 | 88 tok/s | 93GB | 4 |
| Combined | ~1,740 pairs/hr | — | — |

## llama-server Deployment (GGUF)

```bash
# Quantize first
llama-quantize /path/to/merged/ output-q4_k_m.gguf Q4_K_M

# Serve
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 \
  llama-server -m output-q4_k_m.gguf \
  -ngl 99 -c 32768 -fa on \
  --cache-type-k q4_0 --cache-type-v q4_0 \
  --port 8081 --host 0.0.0.0 -t 12
```

## GPU Power Management

```bash
# Set power limits (run once after boot)
sudo nvidia-smi -i 0 -pl 200   # RTX PRO 4500 (32GB)
sudo nvidia-smi -i 1 -pl 350   # RTX PRO 6000 (96GB)
```

## Verification

```bash
# Health check
curl -s http://localhost:8081/health
curl -s http://localhost:8082/health

# Quick inference test
curl -s http://localhost:8082/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"swarmcurator-27b","messages":[{"role":"user","content":"What is DSCR?"}],"max_tokens":200}'

# Full eval
python3 scripts/infer_test.py --endpoint http://localhost:8082/v1 --n 10
```

## Cloudflare Workers Deploy

```bash
cd worker && npx wrangler deploy --remote
cd worker && npx wrangler tail --remote
```

Always use `--remote` flag. Account: 6abec5e82728df0610a98be9364918e4
