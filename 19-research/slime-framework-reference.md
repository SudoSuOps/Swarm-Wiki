# Slime Framework Reference — The RL Engine

**Source**: Grok technical deep-dive on THUDM/slime (github.com/THUDM/slime)
**Status**: TECHNICAL REFERENCE — Future integration path
**Relevance**: PRM judge component = where our tribunal plugs in

## What Slime Is

SGLang-native LLM post-training framework for RL scaling. Developed by THUDM (Tsinghua / Z.ai). Powers GLM-5 training + OpenClaw-RL.

In plain English: turns any self-hosted model into a live-learning agent by decoupling serving, rollout, judging, and training into four independent async loops.

## 4-Component Architecture

```
┌──────────────────────────────────────────────────┐
│  SGLang Server (inference)                        │
│  8-16 GPUs — OpenAI-compatible API               │
│  Client talks to agent here. Never blocked.      │
├──────────────────────────────────────────────────┤
│  Rollout Worker (trajectory capture)              │
│  32-64 GPUs — parallel environment collection    │
│  Captures: prompt → tool call → result → outcome │
├──────────────────────────────────────────────────┤
│  PRM Judge (step-level scoring)          ← US    │
│  16-32 GPUs — rewards each step                  │
│  Binary: good/bad/neutral from next-state        │
│  THIS IS WHERE OUR TRIBUNAL PLUGS IN             │
├──────────────────────────────────────────────────┤
│  Megatron Trainer (weight updates)               │
│  64-128 GPUs — LoRA/full SFT/RL                 │
│  Hot-swaps weights after every batch             │
│  Client never notices the update                 │
└──────────────────────────────────────────────────┘
```

All four components run completely independently. No blocking. Weights hot-swap.

## Two Optimization Methods

| Method | How It Works | Fixes |
|--------|-------------|-------|
| **GRPO (Binary RL)** | PRM scores each turn good/bad/neutral from next-state feedback (user re-query, tool error, etc.) | Tool-call accuracy, completion correctness |
| **OPD (Hindsight-Guided On-Policy Distillation)** | Extracts concrete corrective hints and applies token-level directional supervision | Recovery logic, state management |
| **Combination** (recommended) | Both running together | Everything |

## The Tribunal-as-PRM Opportunity

Slime's PRM judge is a **single model** that scores each step. It's the weakest component — a single judge with no cross-validation.

Our tribunal is a **dual-scale** system:
- Two independent models (different architectures, different hardware)
- 5 weight dimensions (not just binary good/bad)
- 2-pass validation with drift detection
- Merkle-anchored provenance

```
SLIME PRM:                    SWARM TRIBUNAL:
  1 model                       2 models (independent scales)
  binary score                  5-dimension weight vector
  1 pass                        2-pass with drift threshold
  no provenance                 SHA-256 → Merkle → Hedera
  "was it good?"                "how heavy is it, in 5 coordinates?"
```

**Integration path**: Replace or augment Slime's PRM with a tribunal API call. Every step in the RL trajectory gets weighed on our dual scale. The weight becomes the reward signal. The deed becomes the training receipt.

```python
# Replace Slime's default PRM with Tribunal API
def tribunal_prm(trajectory_step):
    response = requests.post("https://swarmandbee.ai/tribunal/api/weigh", json={
        "messages": trajectory_step["messages"],
        "domain": trajectory_step["domain"],
    })
    weight = response.json()  # 5 dimensions + consensus weight
    return weight["final_weight"]  # scalar reward for RL
```

## Hardware Mapping

```
SLIME DEFAULT (8 GPUs):
  2 serving + 2 rollout + 2 PRM + 2 trainer

OUR RIG NOW (3 GPUs, 224GB):
  1 serving (GPU0, 96GB) + 1 rollout/PRM (GPU1, 96GB) + 1 trainer (GPU2, 32GB)
  Can run RL on 14B-27B models
  Single client

WITH FLEET (48x RTX 4500 + 2x RTX 6000):
  4 serving + 16 rollout + 8 PRM + 22 trainer
  Can run RL on 70B models
  10+ parallel clients

GROK REFERENCE (128x RTX 6000):
  16 serving + 32 rollout + 32 PRM + 48 trainer
  Can run RL on 405B models
  50+ parallel clients
```

## Dependencies

```
Python 3.12, conda
PyTorch 2.9.1+cu129 (Blackwell native)
SGLang (serving)
Megatron-LM (distributed training)
DeepEP kernels (async training)
flash-attn (optional, recommended)
OpenClaw-RL (application layer)
```

## When To Build This

```
NOT NOW. Calibrate first.

SEQUENCE:
  1. ✅ Weight Shop (Tier 1) — selling pairs
  2. → ClawHash calibration run (in progress — 41/100)
  3. → AgentHash first experiment (100 tasks × 3 models)
  4. → Enterprise Cook (Tier 2) — $5K-$25K
  5. → Slime integration — Tier 3 RL-as-a-Service
  6. → Tribunal-as-PRM API — usage-based pricing

Don't skip steps. The calibration run proves the pipeline.
The enterprise cook proves the market.
The RL layer proves the moat.
```

---

*Slime is the engine. OpenClaw-RL is the car. Our tribunal is the fuel gauge.*
*Every step scored. Every improvement provable. Every receipt on-chain.*
