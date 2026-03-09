# GPU Operations

Power management, CUDA configuration, vLLM launch requirements, and performance benchmarks.

## Power Limits

Set after every boot to prevent thermal throttling and manage power draw:

```bash
# RTX PRO 4500 Blackwell (32GB) -- swarmrails GPU 0
sudo nvidia-smi -i 0 -pl 200

# RTX PRO 6000 Blackwell (96GB) -- swarmrails GPU 1
sudo nvidia-smi -i 1 -pl 350
```

Default power limits are higher. Capping prevents sustained thermal throttling and reduces power costs.

## CUDA Device Ordering

Always set on swarmrails for consistent GPU numbering:

```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
```

| CUDA Index | GPU | VRAM | PCI Bus |
|------------|-----|------|---------|
| 0 | RTX PRO 4500 | 32GB | 0x90 |
| 1 | RTX PRO 6000 | 96GB | 0xCA |

Without `PCI_BUS_ID`, CUDA may reorder GPUs between reboots. All training and serving scripts assume this ordering.

```bash
# Train 9B on GPU 0 (32GB)
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_9b_p2.py

# Train 27B on GPU 1 (96GB)
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 train_swarmcurator_27b_v1.py
```

## vLLM Required Flags (Qwen3.5)

Qwen3.5 models require specific flags due to their hybrid vision-language architecture:

```bash
vllm serve /path/to/merged \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}' \
  --port 808N
```

| Flag | Required | Reason |
|------|----------|--------|
| `--language-model-only` | Yes | Skip vision encoder loading (text only) |
| `--skip-mm-profiling` | Yes | Prevents multimodal memory profiling crash |
| `--enforce-eager` | Yes | FA2 incompatible with sm_120, avoids CUDA graph issues |
| `--limit-mm-per-prompt '{"image": 0}'` | Yes | Disables image input processing |

## Config Fix for Merged Models

After Unsloth merge, copy `vision_config` from base Qwen3.5 model into merged `config.json`. The `out_hidden_size` must match the text model's `hidden_size`. If they differ, vLLM crashes on startup with a dimension mismatch error.

```python
import json

base = json.load(open('/path/to/base/qwen3.5/config.json'))
merged = json.load(open('/path/to/merged/config.json'))
merged['vision_config'] = base['vision_config']
json.dump(merged, open('/path/to/merged/config.json', 'w'), indent=2)
```

## Benchmarks

### vLLM Inference (swarmrails)

| Model | Port | GPU | VRAM Used | Sequential | 4 Concurrent |
|-------|------|-----|-----------|------------|-------------|
| SwarmCurator-9B bf16 | 8081 | GPU 0 (4500) | 23.5GB | ~45 tok/s | 165 tok/s |
| SwarmCurator-27B bf16 | 8082 | GPU 1 (6000) | 93GB | ~25 tok/s | 88 tok/s |
| Combined | -- | -- | -- | -- | ~1,740 pairs/hr |

3.6x improvement with concurrent batching over sequential. Cook pipeline supports `--vllm --workers 4`.

### whale RTX 3090

| Metric | Value | % Theoretical |
|--------|-------|---------------|
| FP16 TFLOPS | 65.4 | 92% |
| Host-to-Device | 13.0 GB/s | -- |
| RAM STREAM copy | 36.6 GB/s | -- |

Previous config had 2x 3090 but GPU 0 was in crippled chipset x4 slot (31.5 TFLOPS). Hardware swap Feb 27: single 3090 in top x16 slot (full bandwidth), 10G NIC in x4 slot.

## Blackwell sm_120 Compatibility

Pre-built CUDA acceleration packages are incompatible with sm_120:

| Package | Status |
|---------|--------|
| flash_attn | undefined symbol -- does not load |
| causal_conv1d | no kernel for sm_120 |
| flash-linear-attention | falls back to torch |

All training works with eager attention fallback, just slower (~122s/step for 27B). vLLM with `--enforce-eager` handles inference correctly.

## llama.cpp Status

| Node | Build Target | Status |
|------|-------------|--------|
| swarmrails | sm_86 | Built at `/home/swarm/llama.cpp/`, needs rebuild for sm_120 |
| signal-edge-01 | sm_87 | Built, operational for edge inference |

Includes `llama-cli`, `llama-server`, `llama-quantize`. CPU quantization works regardless of GPU build target.

## Monitoring

```bash
# Real-time GPU utilization
watch -n 1 nvidia-smi

# Structured query
nvidia-smi --query-gpu=name,memory.used,memory.total,temperature.gpu,power.draw --format=csv

# vLLM health checks
curl http://localhost:8081/health
curl http://localhost:8082/health
```
