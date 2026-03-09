# Infrastructure & GPU Audit

## vLLM on Blackwell (sm_120)

### Current Deployment

| Model | Port | GPU | VRAM | Throughput (4x concurrent) |
|-------|------|-----|------|---------------------------|
| SwarmCurator-9B bf16 | 8081 | GPU 0 (RTX PRO 4500, 32GB) | 23.5GB | 165 tok/s |
| SwarmCurator-27B bf16 | 8082 | GPU 1 (RTX PRO 6000, 96GB) | 93GB | 88 tok/s |
| Combined | -- | -- | -- | ~1,740 pairs/hr |

### vLLM 0.17.0 Required Flags (Qwen3.5)

```bash
vllm serve /path/to/merged \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}' \
  --port 808N
```

| Flag | Reason |
|------|--------|
| `--language-model-only` | Skip vision encoder (text-only fine-tunes) |
| `--skip-mm-profiling` | Prevents multimodal memory profiling crash |
| `--enforce-eager` | FA2 incompatible with sm_120, avoids CUDA graph issues |
| `--limit-mm-per-prompt '{"image": 0}'` | Disables image input processing |

### Config Fix for Merged Models

After Unsloth merge, copy `vision_config` from base Qwen3.5 into merged `config.json`. `out_hidden_size` must match text `hidden_size`. Without this, vLLM crashes on dimension mismatch.

## Qwen3.5 Architecture

### Gated Delta Networks (GDN)

- **75% GDN layers** (linear attention) + **25% standard attention**
- Block pattern: 3x GDN + 1x standard attention
- Vocab: 248,320 tokens (63% larger than Qwen3's 151,936)
- Context: 262K native, 1M via YaRN

### Model Family

| Size | Params | Active | Architecture | VRAM (bf16) |
|------|--------|--------|-------------|-------------|
| 2B | 2.4B | 2.4B | Dense | ~6GB |
| 9B | 9.3B | 9.3B | Dense | ~19GB |
| 27B | 27.2B | 27.2B | Dense | ~55GB |
| 35B | 35B | 3B | MoE (A3B) | ~70GB |

### Training Rules (Non-Negotiable)

| Rule | Why |
|------|-----|
| bf16 LoRA only (no QLoRA) | Qwen3.5 has higher quantization sensitivity |
| packing=True | 6x speedup (14h -> 84h without) |
| AutoTokenizer bypass | Qwen3.5 VL dispatch bug in HuggingFace |
| enable_thinking=False | Training data has direct responses |
| LoRA targets both GDN + attention | Missing either = partial training |

### Known Issues

| Issue | Impact |
|-------|--------|
| #48 KV-cache + thinking disabled | Potential inference bugs |
| #33 Undertrained long tokens | Quality degrades at extreme lengths |
| #26 reasoning_content in tool calls | Tool use format issues |
| flash_attn undefined symbol | Does not load on sm_120 |
| causal_conv1d no sm_120 kernel | Falls back to torch |

## NVIDIA Blackwell (sm_120)

### GPU Specs (swarmrails)

| GPU | VRAM | SM | Bus | Power Limit |
|-----|------|----|-----|-------------|
| RTX PRO 4500 | 32GB | sm_120 | 0x90 | 200W |
| RTX PRO 6000 | 96GB | sm_120 | 0xCA | 350W |

### Compatibility

| Package | Status on sm_120 |
|---------|-----------------|
| flash_attn | undefined symbol — does not load |
| causal_conv1d | no kernel for sm_120 |
| flash-linear-attention | falls back to torch |
| vLLM 0.17.0 | Works with `--enforce-eager` |
| Unsloth | Works (eager attention fallback, ~122s/step for 27B) |
| PyTorch CUDA 12.8 | Native sm_120 support |

### Performance vs H100

RTX PRO 6000 Blackwell is 1.63x faster than H100 for inference (per factory_protocol.py audit). Lower cost, consumer-grade, no NVLink.

### llama.cpp Status

| Node | Build | Status |
|------|-------|--------|
| swarmrails | sm_86 | Needs rebuild for sm_120 |
| signal-edge-01 | sm_87 | Operational |

## Compute Economics

| Resource | Total Fleet |
|----------|-------------|
| GPU VRAM | 160GB (32 + 96 + 24 + 8) |
| System RAM | 342GB |
| CPU Cores | 56C/100T |
| NVMe | ~6TB |
| Network | 10G (swarmrails + whale) + 1G (edge) |

### Cost Comparison

| Item | Self-Hosted | Cloud Equivalent |
|------|------------|-----------------|
| CapEx (hardware) | ~$15.8K | -- |
| Monthly power | ~$150-200 | ~$3,000-5,000 (H100 rental) |
| Breakeven | 112 days | -- |

Data sovereignty: all training data, models, and inference stay on-premises. No cloud egress, no API dependency for core pipeline.
