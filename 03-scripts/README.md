# Scripts Inventory

All cook, train, deploy, and eval scripts across the Swarm ecosystem.

## Script Matrix

| Script | Repo | Purpose | GPU Required | CLI Example |
|--------|------|---------|--------------|-------------|
| `cook_swarmcurator_9b.py` | swarmrouter | 30K curator pairs, 26 task types | None (API) | `TOGETHER_KEY=... python3 -m data.cook_swarmcurator_9b --stream all --workers 50` |
| `cook_swarmcurator_ops.py` | swarmrouter | 20K ops pairs, 7 task types | None (API) | `TOGETHER_KEY=... python3 -m data.cook_swarmcurator_ops --stream all --workers 50` |
| `cook_swarmcurator_27b.py` | swarmrouter | 18K strategic pairs, 8 task types | None (API) | `TOGETHER_KEY=... python3 -m data.cook_swarmcurator_27b --stream all --workers 50` |
| `cook_swarmcurator_2b.py` | swarmrouter | 9.4K worker pairs, 5 task types | None (API) | `TOGETHER_KEY=... python3 -m data.cook_swarmcurator_2b --stream all --workers 50` |
| `cook_signal_orders.py` | swarmrouter | Triage & order generation from signal heat | None (API) | `TOGETHER_KEY=... python3 -m data.cook_signal_orders --stream all` |
| `cre_capital_cook.py` | swarm-capital-markets | 8-stream capital markets, 70+ tasks | None (API) | `TOGETHER_KEY=... python3 -m data.cre_capital_cook --stream all --workers 50` |
| `cook_rpa.py` | swarm-capital-markets | RPA 5 personas, 235B model | None (API) | `TOGETHER_KEY=... python3 -m data.cook_rpa --stream all` |
| `cook_golden_pairs.py` | swarm-capital-markets | 109 prompts x 3 variants | None (API) | `TOGETHER_KEY=... python3 -m data.cook_golden_pairs --stream all` |
| `cook_platinum_mutations.py` | swarm-capital-markets | Hedge-fund grade mutations | None (API) | `TOGETHER_KEY=... python3 -m data.cook_platinum_mutations --stream all` |
| `make_swarmcre.py` | swarmrouter | Deterministic CRE factory (904K records) | None (CPU) | `python3 -m data.swarmcre_dataset.make_swarmcre --deals 100000 --shards 10` |
| `train_swarmcurator_9b_p1.py` | swarmrouter | 9B phase 1 training | 24GB (3090) | `CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_9b_p1.py` |
| `train_swarmcurator_9b_p2.py` | swarmrouter | 9B phase 2 training | 24GB (3090) | `CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_9b_p2.py` |
| `train_swarmcurator_27b_v1.py` | swarmrouter | 27B training | 96GB (Blackwell) | `CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 train_swarmcurator_27b_v1.py` |
| `train_swarmcurator_2b.py` | swarmrouter | 2B worker training | 24GB (3090) | `CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 train_swarmcurator_2b.py` |
| `train_swarmcapitalmarkets_27b.py` | swarm-capital-markets | 27B capital markets | 96GB (Blackwell) | `CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 train_swarmcapitalmarkets_27b.py` |
| `run_merge.sh` | swarmrails | Unsloth merge to bf16 | Any | `bash run_merge.sh` |
| `run_serve.sh` | swarmrails | vLLM serve merged model | Blackwell | `bash run_serve.sh` |
| `run_infer.sh` | swarmrails | Quick inference test | Any | `bash run_infer.sh` |

## Universal CLI Pattern (Cook Scripts)

```bash
# Dry run (estimate cost, no API calls)
TOGETHER_KEY=... python3 -m data.cook_name --dry-run

# Full generation
TOGETHER_KEY=... python3 -m data.cook_name --stream all --workers 50

# Check progress
TOGETHER_KEY=... python3 -m data.cook_name --status

# Assemble shards into final JSONL
TOGETHER_KEY=... python3 -m data.cook_name --assemble
```

## Together.ai Models

| Role | Model | Cost |
|------|-------|------|
| GEN (generation) | `Qwen/Qwen3-Next-80B-A3B-Instruct` | ~$0.005/pair |
| PASS (validation) | `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` | ~$0.003/pair |

## Section Index

- [Cook Scripts](cook-scripts.md) -- Data generation pipelines
- [Train Scripts](train-scripts.md) -- Fine-tuning configurations
- [Deploy Scripts](deploy-scripts.md) -- Merge, quantize, serve
- [Eval Scripts](eval-scripts.md) -- Evaluation suites and benchmarks
