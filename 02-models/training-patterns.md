# Training Patterns

Universal Unsloth training recipe proven across all Swarm models.

## Framework

- **Unsloth** `FastLanguageModel.from_pretrained()` + `get_peft_model()`
- **TRL** `SFTTrainer` with `SFTConfig`
- **AutoTokenizer** bypass: Must use `AutoTokenizer.from_pretrained()` separately (Qwen3.5 VL dispatch bug in unsloth_zoo)

## Critical Settings

| Setting | Value | Why |
|---------|-------|-----|
| `packing=True` | Always | 6x speedup — without it, padding fills sequences |
| `bf16=True` | Always | No QLoRA for Qwen3.5 |
| `enable_thinking=False` | In chat template | Our training data has direct responses |
| `load_in_4bit=False` | Always | bf16 LoRA only |
| `use_gradient_checkpointing="unsloth"` | Always | Reduces activation memory |

## Hyperparameters by Model Size

| Param | 2B | 9B | 27B | 35B MoE |
|-------|-----|-----|------|---------|
| GPU | 3090 (24GB) | 3090 (24GB) | Blackwell (96GB) | Blackwell (96GB) |
| Batch | 4 | 4 | 2 | 2 |
| Grad Accum | 8 | 8 | 16 | 16 |
| Effective Batch | 32 | 32 | 32 | 32 |
| LoRA r | 32 | 64 | 64 | 64 |
| LoRA alpha | 16 | 32 | 32 | 32 |
| LR | 1e-5 | 1e-5 | 2e-5 | 1e-5 |
| LR Schedule | cosine | cosine | cosine | cosine |
| Epoch Cap | 0.6 | 0.6 | 0.6 | 0.6 |
| Warmup Ratio | 0.05 | 0.05 | 0.05 | 0.05 |
| Weight Decay | 0.01 | 0.01 | 0.01 | 0.01 |

## Early Stopping

- patience=3 on `eval_loss`
- threshold=0.001
- `load_best_model_at_end=True`
- `metric_for_best_model="eval_loss"`
- Max eval samples: 500 (no packing on eval = slow)
- Eval every: 200 steps

## LoRA Targets

```python
target_modules=[
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]
```

IMPORTANT: Since 75% of layers are GDN, verify Unsloth targets BOTH GDN projections AND standard attention projections. Missing GDN layers = training only 25% of attention.

## Data Quality Rules

- **System prompt diversity**: 30+ unique prompts, no single prompt > 10% share
- **Task diversity**: 26+ task types minimum
- **Start-phrase entropy**: < 4% top-1 5-token prefix
- **Difficulty balance**: Bronze 20%, Silver 20%, Gold 15%, High 30%, Platinum 15%

## Lessons Learned

1. **v1 failure**: 78K pairs with 2 system prompts -> template memorization, not learning
2. **Diversity is key**: More system prompts + task types = better generalization
3. **QLoRA on MoE**: SwarmCRE-35B v1 used QLoRA — Unsloth says bf16 LoRA only for Qwen3.5
4. **Eval overhead**: 3,291 eval samples x no packing x eval_steps=50 = 13h eval. Fix: cap eval to 500, eval every 200 steps
5. **Think mode confusion**: Template ALWAYS adds `<think>` — must explicitly pass `enable_thinking=False`
6. **Batch padding waste**: batch_size=4 + variable prompts = massive left-pad overhead. Packing fixes this.
7. **Greedy decoding**: `do_sample=False` breaks thinking mode entirely. Never use it.

## vLLM Deployment Issue

Unsloth merge bakes VL (vision-language) weights into the model. vLLM fails with weight shape mismatch.

**Workaround**: Copy `vision_config` from base Qwen3.5 model into merged `config.json`, ensuring `out_hidden_size` matches text model's `hidden_size`.

**Alternative**: Use GGUF via llama-server (works perfectly).

## Post-Training Pipeline

1. `save_pretrained_merged("merged_16bit")` — merge LoRA into base
2. Quantize: `llama-quantize` to Q4_K_M / Q8_0 / F16
3. Deploy: vLLM (bf16 production) or llama-server (GGUF)
4. Eval: run eval suite, compare to baseline
