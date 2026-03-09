# Gold Standard Build Specification

**Repo**: [`swarm-qwen-27B-Gold-Standard-Build-LLM`](https://github.com/SudoSuOps/swarm-qwen-27B-Gold-Standard-Build-LLM)

The definitive playbook for training best-in-class Qwen3.5 fine-tunes. If it's not perfect, we nuke it.

## Proven Results

| Model | Base | Loss | Steps | Time | Data |
|-------|------|------|-------|------|------|
| **SwarmCurator-27B-v1** | Qwen3.5-27B Dense | **0.477** | 1,000 | 14.38h | 62K pairs (3 phases) |
| **SwarmCurator-9B-P2** | Qwen3.5-9B | **0.707** | 414 | 3.37h | 22K pairs |
| **SwarmCurator-9B-P1** | Qwen3.5-9B | **0.665** | 500 | 2.49h | 27K pairs |
| **SwarmCurator-2B-v1** | Qwen3.5-2B | **0.880** | 224 | 0.54h | 9K pairs |

SwarmCurator-27B-v1 at **0.477 loss** is the best build to date.

## The Rules

1. **LR 1e-5 for 27B/9B. 2e-5 for 2B only.** Higher rates overshoot on clean data.
2. **Never full epoch.** 0.6 cap (27B/9B), 0.8 cap (2B). Early stopping kills it sooner if needed.
3. **No QLoRA.** Qwen3.5 has higher quantization error. bf16 LoRA only.
4. **Clean retrain from base.** Don't continue from merged checkpoints.
5. **AutoTokenizer bypass.** Unsloth's tokenizer dispatch is broken for Qwen3.5 VL models.
6. **System prompt diversity >= 30.** Fewer = template memorization.
7. **SHA256 everything.** Every dataset, every assembly, every checkpoint.
8. **MANIFEST.json on every build.** Full provenance.
9. **vision_config fix post-merge.** Unsloth strips it. vLLM needs it.
10. **If it's wrong, nuke it.** Don't rescue bad builds.

## Repo Structure

```
swarm-qwen-27B-Gold-Standard-Build-LLM/
├── train/
│   ├── gold_standard_27b.py      # THE 27B template
│   ├── gold_standard_9b.py       # 9B template
│   ├── gold_standard_2b.py       # 2B edge template
│   └── config.py                 # All 3 tiers
├── data/
│   ├── assembly.md               # Data prep standards
│   └── quality_gates.md          # 6 deterministic gates
├── deploy/
│   ├── fix_vision_config.py      # Qwen3.5 VL fix
│   ├── launch_27b.sh / 9b.sh    # vLLM launch
│   └── benchmark.py              # Throughput benchmark
├── manifests/                    # Build receipts
├── vision_configs/               # Exact configs for vLLM
├── fixes/                        # Known bugs
└── hardware/                     # VRAM budgets
```

## Quick Start

```bash
# 1. Clone the playbook
git clone git@github.com:SudoSuOps/swarm-qwen-27B-Gold-Standard-Build-LLM.git

# 2. Copy the right template (27b, 9b, or 2b)
cp train/gold_standard_27b.py /data2/your_model/train.py

# 3. Edit CONFIG section (data paths, build name)
# 4. Train
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 train.py

# 5. Fix vision config for vLLM
python3 deploy/fix_vision_config.py /path/to/merged/ --base Qwen/Qwen3.5-27B

# 6. Deploy
./deploy/launch_27b.sh
```

## Key Lessons Learned

- **LR 2e-5 was tried on CapitalMarkets-27B** — caught, killed, restarted with 1e-5. Optimizer states from wrong LR are toxic; must start fresh from step 0.
- **`killall python3` on a training box kills training too.** Use specific PIDs.
- **Packing is skipped by Unsloth** (VL model detection) — still works fine, just slower per step.
- **Eval set must be capped** at 500 for 27B — 3K+ samples without packing = 34 min per eval.
- **`enable_thinking=False` in format_chat** subtly changes tokenization — don't override, use defaults.
