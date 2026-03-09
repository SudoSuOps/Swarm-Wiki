# Training Patterns

Universal training recipe used across all Swarm models. Every model follows this pattern with minor parameter adjustments for size.

## Framework

- **Training**: Unsloth FastLanguageModel + TRL SFTTrainer
- **Model loading**: `FastLanguageModel.from_pretrained()` + `get_peft_model()`
- **Tokenizer**: `AutoTokenizer.from_pretrained()` separately -- bypass Unsloth VL dispatch bug
- **Hardware**: swarmrails Blackwell GPUs (27B/35B) or whale RTX 3090 (2B/9B)
- **Precision**: bf16 only. No fp16, no QLoRA, no int8.

## Critical Settings

These are non-negotiable. Violating any of them produces a bad model.

| Setting | Value | Why |
|---------|-------|-----|
| `packing=True` | Always | 6x speedup -- without it, padding fills sequences |
| `bf16=True` | Always | No QLoRA for Qwen3.5 |
| `load_in_4bit=False` | Always | bf16 LoRA only |
| `enable_thinking=False` | In chat template | Training data has direct responses, not think traces |
| `use_gradient_checkpointing="unsloth"` | Always | Reduces activation memory |

### 1. packing=True

Always enable packing in the SFTTrainer. Packing concatenates multiple short training examples into a single sequence, filling the context window efficiently. Without packing, short examples waste most of the context window on padding.

**Impact**: 6x training speedup. A 14-hour training run becomes 84 hours without packing.

### 2. AutoTokenizer Bypass

Qwen3.5 triggers a VL (vision-language) model dispatch bug in HuggingFace AutoTokenizer via unsloth_zoo. When you call `AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")`, it detects VL capabilities and loads a vision tokenizer that corrupts text-only training.

**Fix**: Load the tokenizer separately using `AutoTokenizer.from_pretrained()` outside of Unsloth's model loading path.

### 3. No QLoRA for Qwen3.5

Qwen3.5 architecture has "higher than normal quantization differences" (per Alibaba's documentation). Quantizing the base model before applying LoRA adapters introduces noise that the adapter cannot compensate for.

**Rule**: bf16 LoRA only. Full precision base model, trainable adapter in bf16.

### 4. LoRA Must Target Both Layer Types

Qwen3.5 has two types of layers: GDN (75%) and standard attention (25%). The LoRA target modules must include projections from BOTH types:

```python
target_modules=[
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]
```

Missing GDN layers means only 25% of attention is trainable. Missing standard attention means the full-context reasoning layers are frozen.

## Hyperparameters by Model Size

| Param | 2B | 9B | 27B | 35B MoE |
|-------|-----|-----|------|---------|
| GPU | 3090 (24GB) | 3090 (24GB) | Blackwell (96GB) | Blackwell (96GB) |
| Batch size | 4 | 4 | 2 | 2 |
| Gradient accumulation | 8 | 8 | 16 | 16 |
| Effective batch size | 32 | 32 | 32 | 32 |
| LoRA r (rank) | 32 | 64 | 64 | 64 |
| LoRA alpha | 16 | 32 | 32 | 32 |
| Learning rate | 1e-5 | 1e-5 | 2e-5 | 1e-5 |
| LR schedule | Cosine | Cosine | Cosine | Cosine |
| Epoch cap | 0.6 | 0.6 | 0.6 | 0.6 |
| Warmup ratio | 0.05 | 0.05 | 0.05 | 0.05 |
| Weight decay | 0.01 | 0.01 | 0.01 | 0.01 |

### Why 0.6 Epoch Cap

Training for a full epoch on large datasets risks overfitting, especially with LoRA where the adapter has limited capacity. 0.6 epochs exposes the model to 60% of the training data in a single pass, which is sufficient for convergence when combined with early stopping.

### Effective Batch Size of 32

All models target an effective batch size of 32 regardless of model size. Larger models use smaller per-device batches with higher gradient accumulation to compensate. This keeps the optimization dynamics consistent across the fleet.

## Early Stopping

| Parameter | Value |
|-----------|-------|
| Patience | 3 evaluation cycles |
| Metric | eval_loss |
| Threshold | 0.001 |
| load_best_model_at_end | True |
| metric_for_best_model | eval_loss |
| Eval frequency | Every 200 steps |
| Max eval samples | 500 |

When eval_loss has not improved by more than 0.001 for 3 consecutive evaluations (600 steps), training stops. This prevents wasted compute on a model that has already converged.

**Why cap eval at 500**: Early runs used large eval sets (3,291+ samples). Without packing on eval, this took 13+ hours of eval time alone. Capping at 500 samples reduced eval time to ~2 minutes per cycle with no meaningful change in early stopping accuracy.

## VRAM Budgets

| Model Size | Minimum VRAM | Recommended | Hardware |
|------------|-------------|-------------|----------|
| 2B | 8GB | 24GB (3090) | whale |
| 9B | 24GB | 24GB (3090) | whale |
| 27B Dense | 96GB | 96GB (Blackwell) | swarmrails GPU1 |
| 35B MoE | 96GB | 96GB (Blackwell) | swarmrails GPU1 |

The 27B and 35B both require the RTX PRO 6000 Blackwell (96GB). The 35B MoE fits because only 3B parameters are active per token, but the full 35B of expert weights must reside in VRAM for the router to function.

## Data Assembly Rules

### System Prompt Diversity

**Minimum**: 30 unique system prompts per training set.
**Maximum share**: No single system prompt may exceed 10% of the training set.

This is the single most important lesson from the SwarmCRE-35B v1 failure. That model used only 2 system prompts across 78K pairs. The result: the model memorized the prompt template instead of learning the underlying task. It performed perfectly on in-distribution prompts and collapsed on anything else.

### Task Type Diversity

**Minimum**: 26 unique task types per training set.

Different task types force the model to learn generalizable reasoning patterns rather than task-specific shortcuts. CRE uses 8 task types. Medical uses 16 pharma task types. Capital markets uses 8 cook streams.

### Start-Phrase Entropy

**Target**: Less than 4% top-1 5-token prefix share.

If more than 4% of training responses start with the same 5 tokens, the model will learn to produce that prefix on every response. Enforce start-phrase diversity by varying response openings across the training set.

### Difficulty Balance

| Tier | Share |
|------|-------|
| Bronze | 20% |
| Silver | 20% |
| Gold | 15% |
| High | 30% |
| Platinum | 15% |

Heavier weighting toward High difficulty ensures the model stretches beyond simple recall without overwhelming it with adversarial edge cases.

### Multi-Phase Assembly

Large training sets are assembled in phases, each emphasizing a different capability:

| Phase | Purpose | Example (SwarmCurator-27B) |
|-------|---------|---------------------------|
| Phase 1: Methodology | How to reason about the domain | 27,700 pairs |
| Phase 2: Operations | How to execute domain tasks | 19,900 pairs |
| Phase 3: Strategic | How to make high-level decisions | 18,125 pairs |

### Pool Assembly (Capital Markets Pattern)

For complex domains, training data is assembled from weighted pools:

| Pool | Share | Purpose |
|------|-------|---------|
| Diversified | 60% | Broad coverage across all task types |
| Risk-weighted (RPA) | 25% | Stress tests, tail events, edge cases |
| Specialized (Macro+Graph) | 8% | Domain-specific deep dives |
| Golden | 4% | Hand-verified exemplars from production |
| Mutations | 3% | Deliberately perturbed scenarios for robustness |

## Post-Training Pipeline

### 1. Merge

```python
model.save_pretrained_merged("merged_16bit")
```

Merges LoRA adapter weights into the base model via Unsloth's merge utilities. Produces a full-weight checkpoint.

**Warning**: Unsloth merge bakes VL (vision-language) weights from the base model into the merged checkpoint, even for text-only fine-tunes. This causes issues with vLLM deployment.

### 2. Quantize

GGUF quantization for edge and lightweight inference:

```bash
llama-quantize merged_16bit/model.gguf output.Q4_K_M.gguf Q4_K_M
```

| Format | Size vs bf16 | Quality | Use Case |
|--------|-------------|---------|----------|
| Q4_K_M | ~40% | Minimal loss | Edge devices, mobile |
| Q8_0 | ~50% | Near-lossless | Local testing, backup |
| F16 | ~100% | Lossless | When vLLM unavailable |

### 3. Deploy

**vLLM (production)**: bf16 serving on Blackwell GPUs.

Required flags for all Qwen3.5 models:
```bash
--skip-mm-profiling --enforce-eager --limit-mm-per-prompt '{"image": 0}'
```

Required config fix: Copy `vision_config` from base model's config.json into merged config.json. Ensure `out_hidden_size` matches text model's `hidden_size`.

**Alternative**: GGUF via llama-server works without the vision_config fix.

Recommended vLLM settings:
- Flash attention: ON
- KV cache quantization: q4_0
- Context length: 32K (sufficient for most tasks)
- Parallel slots: 4

### 4. Evaluate

Run eval suite against held-out test sets:
- JSON validity rate
- Verdict match accuracy
- Score MAE
- Task completion rate
- A/B comparison against previous model version

## Lessons Learned

1. **v1 failure (template memorization)**: 78K pairs with 2 system prompts. Model memorized templates, not tasks. Fix: 30+ prompts, 26+ task types.
2. **packing=True**: 6x speedup with no quality loss. Mandatory for all runs.
3. **QLoRA on Qwen3.5**: Does not work. bf16 LoRA only.
4. **Eval overhead**: 3,291 eval samples without packing + eval every 50 steps = 13h of eval time. Fix: cap eval at 500, eval every 200 steps.
5. **Think mode in training**: Template always adds `<think>` token. Must explicitly pass `enable_thinking=False` when training data has direct responses.
6. **Batch padding waste**: Variable-length prompts with batch_size=4 creates massive left-pad overhead. Packing fixes this completely.
7. **Greedy decoding**: `do_sample=False` breaks Qwen3.5 thinking mode entirely. Never use it, even for inference after training.
8. **train_on_responses_only**: Consider for reasoning models -- masks instruction tokens so learning capacity focuses on response generation, not prompt memorization.
