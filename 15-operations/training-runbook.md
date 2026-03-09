# Training Runbook

Step-by-step for a new model training run.

## 1. Cook Data

```bash
# Dry run first
TOGETHER_KEY=... python3 -m data.cook_name --dry-run

# Full cook
TOGETHER_KEY=... python3 -m data.cook_name --stream all --workers 50

# Monitor
TOGETHER_KEY=... python3 -m data.cook_name --status

# Assemble when done
TOGETHER_KEY=... python3 -m data.cook_name --assemble
```

## 2. Assemble Dataset

```bash
python3 -m data.assemble_final --dry-run  # Preview
python3 -m data.assemble_final            # Build train + eval JSONL
```

Checks: dedup, system prompt diversity (no single prompt > 10%), task balance, difficulty distribution, start-phrase entropy (< 4%).

## 3. Upload to swarmrails

```bash
scp train.jsonl swarmrails:/data2/modelname/
scp eval.jsonl swarmrails:/data2/modelname/
scp train_script.py swarmrails:/data2/modelname/
```

## 4. Configure Training

Key hyperparameters (universal recipe):

| Param | 2B | 9B | 27B | 35B MoE |
|-------|-----|-----|------|---------|
| GPU | 3090 (24GB) | 3090 (24GB) | Blackwell (96GB) | Blackwell (96GB) |
| Batch | 4 | 4 | 2 | 2 |
| Grad Accum | 8 | 8 | 16 | 16 |
| Effective Batch | 32 | 32 | 32 | 32 |
| LoRA r | 32 | 64 | 64 | 64 |
| LoRA alpha | 16 | 32 | 32 | 32 |
| LR | 1e-5 | 1e-5 | 2e-5 | 1e-5 |
| Epoch Cap | 0.6 | 0.6 | 0.6 | 0.6 |

Critical flags:
- `packing=True` (6x speedup)
- `AutoTokenizer.from_pretrained()` (NOT Unsloth's tokenizer — VL dispatch bug)
- `enable_thinking=False` in chat template (our data has direct responses)
- `bf16=True` (no QLoRA for Qwen3.5)

## 5. Launch Training

```bash
# Smoke test first (500 samples)
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
  python3 train_script.py --smoke-test

# Full run
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
  nohup python3 train_script.py > train.log 2>&1 &
echo $!
```

## 6. Monitor

```bash
# Loss at step 10 (first logging interval)
tail -f train.log | grep -E "loss|eval"

# GPU status
nvidia-smi

# Eval every 200 steps, early stopping patience=3
```

## 7. Merge

```bash
# Unsloth merge (happens automatically in most scripts)
# Or manually:
python3 scripts/merge_lora.py --adapter /path/to/lora --output /path/to/merged
```

## 8. Deploy

```bash
# vLLM (production)
vllm serve /path/to/merged \
  --served-model-name model-name \
  --port 808N \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}'

# OR llama-server (GGUF)
llama-quantize /path/to/merged/model.safetensors output.gguf Q4_K_M
llama-server -m output.gguf -ngl 99 -c 32768 --port 808N
```

## 9. Verify

```bash
curl -s http://localhost:808N/health
python3 scripts/infer_test.py --endpoint http://localhost:808N/v1 --n 10
```
