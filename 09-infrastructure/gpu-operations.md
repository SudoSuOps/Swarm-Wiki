# GPU Operations

## Power Limits

```bash
# Set after every boot
sudo nvidia-smi -i 0 -pl 200   # RTX PRO 4500 (32GB) — 200W
sudo nvidia-smi -i 1 -pl 350   # RTX PRO 6000 (96GB) — 350W
```

## CUDA Ordering

Always set on swarmrails:
```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
```

- GPU 0 = RTX PRO 4500 Blackwell (32GB, Bus 0x90)
- GPU 1 = RTX PRO 6000 Blackwell (96GB, Bus 0xCA)

## vLLM Required Flags (Qwen3.5)

```bash
--language-model-only       # Skip vision encoder
--skip-mm-profiling         # Skip multimodal profiling
--enforce-eager             # FA2 incompatible with sm_120
--limit-mm-per-prompt '{"image": 0}'  # No image inputs
```

## Config Fix for Merged Models

After Unsloth merge, copy `vision_config` from base Qwen3.5 model into merged `config.json`. The `out_hidden_size` must match the text model's `hidden_size`.

## Benchmarks

| Model | Throughput | VRAM | Concurrent Streams |
|-------|-----------|------|-------------------|
| 9B bf16 (GPU 0) | 165 tok/s | 23.5GB | 4 |
| 27B bf16 (GPU 1) | 88 tok/s | 93GB | 4 |
| Combined | ~1,740 pairs/hr | — | — |

## Blackwell sm_120 Compatibility

Pre-built CUDA acceleration packages are incompatible with sm_120:
- flash_attn — undefined symbol
- causal_conv1d — no kernel for sm_120
- flash-linear-attention — falls back to torch

All training works with eager attention fallback, just slower (~122s/step for 27B).
