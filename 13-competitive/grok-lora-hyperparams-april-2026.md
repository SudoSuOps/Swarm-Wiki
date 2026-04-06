# Grok LoRA Hyperparameters — The Cookbook Recipe the Market Wants

**Source**: Grok X signal analysis — battle-tested LoRA playbook for OpenClaw agents
**Status**: COOKBOOK RECIPE VALIDATION

## The Recipe (validated by production builders)

### Dataset: 1K-5K pairs, quality > quantity

```
Format:      ChatML / ShareGPT JSONL
Structure:   system → user → assistant (tool call) → tool response → 
             assistant (validation/recovery) → final answer
Must include: failures + corrections + recovery trajectories
Per tool:    50-100 examples minimum
Edge cases:  ambiguous queries, partial failures, state recovery
Train on:    completions only (mask user/tool parts) → +1% agentic accuracy
```

### Hyperparameters: The Sweet Spot

| Param | Value | Notes |
|-------|-------|-------|
| Rank (r) | 16-32 | 16 for most agents, 32 for complex schemas |
| Alpha | 16-32 (2x rank) | use_rslora=True for stability at r>=32 |
| Dropout | 0 (or 0.05-0.1) | Only if overfitting on small datasets |
| Target modules | ALL linear | q,k,v,o,gate,up,down_proj |
| Learning rate | 2e-4 | 1e-4 if loss explodes, cosine + 5-10% warmup |
| Epochs | 1-3 (usually 1-2) | >3 = overfitting + hallucinations |
| Batch size | 2-4 + grad_accum 4-8 | Effective batch ~16 |
| Quantization | QLoRA 4-bit NF4 | Train in same precision you serve |
| bias | "none" | |
| weight_decay | 0.01 | |
| Seed | 3407 | Reproducibility |

### Eval Metrics (what success looks like)

```
tool_selection_accuracy    > 90%  (right tool for the job)
argument_parsing_accuracy  > 85%  (correct JSON schema)
refusal_rate_when_needed   > 95%  (no tool when none needed)
loop_rate                  < 2%   (bounded retries)
hallucinated_success_rate  < 1%   (verified before claiming done)
```

### Cost

```
Cook time:   2-4 hours on RTX 4090 (or 4500 Blackwell)
Rental cost: $1-5 on cloud 4090
Our cost:    $0.31 on RTX PRO 6000 at 300W cap
```

## What This Means for Swarm & Bee

### The Product Is the Data, Not the Cook

```
THE COOK:
  $1-5 on any 4090
  2-4 hours
  Unsloth makes it trivial
  Any builder can do this

THE DATA:
  1K-5K high-quality pairs
  Must include failures + recovery
  Must cover edge cases
  Must be validated
  THIS IS THE HARD PART
  THIS IS WHAT WE SELL

"The cook is cheap. The data is the product."
```

### Our Weight vs Their DIY

| Dimension | Their DIY | Swarm & Bee |
|-----------|-----------|-------------|
| **Source** | Export 30 sessions, hope for diversity | 33 CVE-sourced templates × mutations × 3 personas |
| **Quality gate** | None — cook and hope | Dual-scale tribunal, 5 dimensions, 0.85 threshold |
| **Provenance** | "I exported this from my chat history" | SHA-256 fingerprint → Merkle → Hedera anchor |
| **Format** | Whatever they can export | 5 formats included (JSONL, CSV, Alpaca, ShareGPT, HF) |
| **Edge cases** | Whatever they happened to encounter | Systematic: 6 sub-algos × 10 failure labels |
| **Cost** | 40+ hours manual work | $80-$320 download |
| **Validation** | "It feels better" | Before/after metrics with deed-backed proof |

### The Cookbook Recipe We Should Publish

```
RECIPE: "Bake a Reliable Agent"

INGREDIENTS:
  5,000 lbs AgentHash weight (swarmandbee.ai/shop)  — $80
  OR 1,000 lbs ClawHash weight                      — $48
  OR both                                            — $320
  1 base model (Qwen 3.5 14B recommended)
  1 GPU (RTX 4090/4500, 2-4 hours)

OVEN SETTINGS (Unsloth):
  r=16, alpha=32, use_rslora=True
  target_modules=ALL linear
  lr=2e-4, cosine, 5% warmup
  epochs=2, QLoRA 4-bit NF4
  batch=2, grad_accum=8
  train_on_completions_only=True

STEPS:
  1. Download weight → already in 5 formats
  2. pip install unsloth
  3. Load Qwen3.5-14B + our JSONL
  4. Train (2-4 hours, $1-5 compute)
  5. Merge adapter → deploy to Ollama
  6. Point OpenClaw at hardened model

EXPECTED RESULT (from builder reports):
  Tool-call success: 40-60% → 90%+
  Manual interventions: 5-10x fewer
  Loops: eliminated with bounded retry training
  Hallucinated success: eliminated with validation training

PROOF:
  Every pair in the weight has a deed certificate
  Every deed has 5 weight coordinates
  Every batch has a Merkle root on Hedera
  Run swarmandbee.ai/deed/ to verify any pair
```

### Hyperparams We Should Include in the OM

The Offering Memorandum for each weight package should include:
- Recommended hyperparameters (from this playbook)
- Eval script (tool_selection_accuracy, loop_rate, etc.)
- Before/after benchmark template
- Unsloth code snippet ready to paste

This turns the weight from "a dataset" into "a complete cooking kit."

## The Unsloth Code Snippet (include in every package)

```python
from unsloth import FastLanguageModel

# Load base model
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen2.5-14B",  # or Qwen3.5 when available
    dtype=None,
    load_in_4bit=True,
)

# Add LoRA adapter
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                     "gate_proj","up_proj","down_proj"],
    lora_alpha=32,
    lora_dropout=0,
    use_rslora=True,
)

# Load Swarm & Bee weight (already in JSONL chat format)
from datasets import load_dataset
dataset = load_dataset("json", data_files="training_data.jsonl")

# Train
from trl import SFTTrainer, SFTConfig
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    args=SFTConfig(
        output_dir="./clawbot-hardened",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        num_train_epochs=2,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        weight_decay=0.01,
        seed=3407,
        logging_steps=10,
    ),
    tokenizer=tokenizer,
)
trainer.train()

# Merge and deploy
model.save_pretrained_merged("clawbot-hardened-merged", tokenizer)
# Then: ollama create clawbot-hardened -f Modelfile
```

---

*The cook is $5. The data is $80-$320. The quality gate is our moat.*
*Grok just wrote our customer's README. We sell the ingredients.*
