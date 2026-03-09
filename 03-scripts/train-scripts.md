# Train Scripts

All fine-tuning scripts use Unsloth with bf16 LoRA. Every script follows the same universal configuration pattern with per-model adjustments for batch size and GPU assignment.

## Universal Training Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Precision | bf16 | No QLoRA -- full bf16 LoRA only |
| LoRA rank | r=64 | Consistent across all models |
| Packing | `packing=True` | 6x speedup over padding |
| Epoch cap | 0.6 | Prevents overfitting on synthetic data |
| Early stopping | patience=3 | Stops if val loss plateaus |
| Tokenizer | AutoTokenizer bypass | Required workaround for Qwen3.5 VL dispatch bug |
| Framework | Unsloth 2026.2.1 | Installed on whale and swarmrails |

### AutoTokenizer Bypass

Qwen3.5 models trigger a VL (vision-language) tokenizer dispatch bug when using `AutoTokenizer.from_pretrained()`. All train scripts must bypass this by loading the tokenizer class directly rather than through the Auto dispatcher.

### GPU Ordering

Always set `CUDA_DEVICE_ORDER=PCI_BUS_ID` on swarmrails to ensure consistent GPU assignment:
- GPU 0 = RTX PRO 4500 Blackwell (32GB, Bus 0x90)
- GPU 1 = RTX PRO 6000 Blackwell (96GB, Bus 0xCA)

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=N python3 train_script.py
```

---

## train_swarmcurator_9b_p1.py (swarmrouter)

Phase 1 training of SwarmCurator-9B. First pass on the core curator dataset.

| Parameter | Value |
|-----------|-------|
| Base model | Qwen3.5-9B |
| Training data | ~30K pairs (cook_swarmcurator_9b output) |
| GPU | 24GB (RTX 3090 on whale, or RTX PRO 4500 on swarmrails) |
| Batch size | 4 |
| Gradient accumulation | 8 |
| Effective batch | 32 |

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_9b_p1.py
```

## train_swarmcurator_9b_p2.py (swarmrouter)

Phase 2 training. Continues from P1 checkpoint with operational data mixed in.

| Parameter | Value |
|-----------|-------|
| Base model | P1 checkpoint |
| Training data | ~46K pairs (P1 data + ops data merged) |
| GPU | 24GB (RTX 3090 on whale, or RTX PRO 4500 on swarmrails) |
| Batch size | 4 |
| Steps | 414 |
| Final loss | 0.707 |
| Output | swarmrails:/data2/swarmcurator-9b-p2/merged/ |

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_9b_p2.py
```

## train_swarmcurator_27b_v1.py (swarmrouter)

The 27B strategic head. Requires the RTX PRO 6000 (96GB) on swarmrails.

| Parameter | Value |
|-----------|-------|
| Base model | Qwen3.5-27B Dense |
| Training data | ~62K pairs |
| GPU | 96GB (RTX PRO 6000 Blackwell on swarmrails) |
| Batch size | 2 |
| Gradient accumulation | 16 |
| Effective batch | 32 |
| Steps | 1,000 |
| Final loss | 0.477 |
| Output | swarmrails:/data2/swarmcurator-27b/ |

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 train_swarmcurator_27b_v1.py
```

## train_swarmcurator_2b.py (swarmrouter)

The 2B edge worker model. Trains on whale's RTX 3090.

| Parameter | Value |
|-----------|-------|
| Base model | Qwen3.5-2B |
| Training data | ~9.4K pairs |
| GPU | 24GB (RTX 3090 on whale) |
| Batch size | 4 |
| Steps | 224 |
| Final loss | 0.880 |
| Output | whale:~/swarmcurator-2b/merged/ |

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_2b.py
```

## train_swarmcapitalmarkets_27b.py (swarm-capital-markets)

Capital markets specialist. Trains on the RTX PRO 6000 (96GB) on swarmrails.

| Parameter | Value |
|-----------|-------|
| Base model | Qwen3.5-27B Dense |
| Training data | Capital markets cook outputs |
| GPU | 96GB (RTX PRO 6000 Blackwell on swarmrails) |
| Batch size | 2 |
| Gradient accumulation | 16 |
| Effective batch | 32 |

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 train_swarmcapitalmarkets_27b.py
```

## Training Results Summary

| Model | Base | Pairs | Steps | Final Loss | Location |
|-------|------|-------|-------|------------|----------|
| SwarmCurator-9B | Qwen3.5-9B | 46K | 414 | 0.707 | swarmrails:/data2/swarmcurator-9b-p2/merged/ |
| SwarmCurator-27B | Qwen3.5-27B Dense | 62K | 1,000 | 0.477 | swarmrails:/data2/swarmcurator-27b/ |
| SwarmCurator-2B | Qwen3.5-2B | 9.4K | 224 | 0.880 | whale:~/swarmcurator-2b/merged/ |
| SwarmPharma-35B | Qwen3.5-35B-A3B | 25.6K | 2,402 | 0.337 | swarmrails:/data2/swarmpharma-35b/ |
| SwarmCRE-35B v2 | Qwen3.5-35B-A3B | 100K | 5,000 | gen gap | NAS:/mnt/swarm/models/swarmcre-35b-v2/ |
| SwarmResearch-32B | Qwen2.5-32B | 35.5K | 2,220 | 0.635 | swarmrails:/data2/swarm-research-32b/ |
| BeeMini (Router v2) | Qwen2.5-3B | 60K | 693 | 0.026 | swarmrouter-v2-q4_k_m.gguf (1.8GB) |

## Key Lessons Learned

1. **packing=True** is mandatory -- 6x speedup over padded training with no quality loss
2. **AutoTokenizer bypass** is required for all Qwen3.5 models due to VL dispatch bug
3. **0.6 epoch cap** prevents overfitting on synthetic data -- loss curves validated this empirically
4. **batch=4 grad_accum=8** is the sweet spot for 24GB GPUs; batch=2 grad_accum=16 for 96GB
5. **Early stopping patience=3** catches generalization gaps before they waste GPU hours
