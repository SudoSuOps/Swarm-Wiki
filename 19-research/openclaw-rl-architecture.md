# OpenClaw-RL Architecture — Continuous Agent Self-Improvement

**Source**: Grok enterprise playbook — Gen-Verse/OpenClaw-RL implementation
**Status**: FUTURE PRODUCT LANE — Tier 2 recurring revenue

## The Architecture (4 async components)

```
SERVING (inference)     → Client talks to agent normally
                              ↓ (X-Session-Id headers)
ROLLOUT (trajectory)    → Captures full session traces with tool calls
                              ↓
PRM JUDGE (scoring)     → Scores every STEP from next-state feedback
                              ↓
TRAINER (RL update)     → Binary RL (GRPO) + OPD → updates weights async
                              ↓
SERVING (hot-swap)      → New weights loaded, client never notices
```

Fully async. Clients never see training latency. Weights improve in background.

## Three Training Methods

| Method | What | Fixes |
|--------|------|-------|
| **Binary RL (GRPO)** | Reward signal from task success/failure | Tool-call accuracy, completion correctness |
| **PRM (Process Reward Model)** | Score every intermediate step, not just final result | Loops, bad recovery, state loss |
| **OPD (On-Policy Distillation)** | Extract corrective hints from hindsight ("you should have checked memory first") | Hallucinated success, bad escalation |
| **Combination** (recommended) | All three together | Everything |

## How It Maps to Our Failure Taxonomy

```
Tool-call failure       → PRM scores each tool call step independently
Hallucinated success    → PRM detects "claimed done but tool returned error"
Loops                   → PRM penalizes repeated identical actions
Bad recovery            → OPD injects "you should have tried X instead"
Lost state              → Full trajectory includes MEMORY.md context
Runtime instability     → Continuous weight updates adapt to config changes
```

## What This Means for Swarm & Bee

### The Three Product Layers

```
LAYER 1: WEIGHT (one-time buy)
  AgentHash + ClawHash pairs
  Download → cook → deploy
  $80-$320
  THE INGREDIENTS

LAYER 2: COOK (one-time service)  
  We cook the LoRA for you
  Custom dataset + fine-tune + eval
  $5K-$25K
  THE CHEF

LAYER 3: RL (recurring)
  Continuous improvement loop
  Every conversation → training signal
  Agent gets smarter daily
  $2K/month
  THE LIVING WEIGHT — monthly recurring revenue
```

### Layer 3 = SwarmRefinery + Tribunal in Production

```
CURRENT TRIBUNAL:
  Batch scoring → deeds → Merkle → Hedera
  Runs on our hardware
  Processes pairs we generated

FUTURE TRIBUNAL (RL mode):
  Real-time scoring → PRM judge → weight updates
  Runs on client's hardware (or our managed hosting)
  Processes the client's ACTUAL conversations
  Every failed tool call = training signal
  Every recovery = positive reinforcement
  
  The tribunal becomes the PRM.
  The deed becomes the reward signal.
  The weight improves continuously.
```

### Our Advantage for RL

The PRM (Process Reward Model) in OpenClaw-RL is basically a simplified version of our tribunal:
- PRM scores each step → our tribunal scores each pair on 5 dimensions
- PRM uses next-state feedback → our tribunal uses 2-pass validation
- PRM runs on 1 model → our tribunal uses 2 independent scales

**We can BE the PRM.** Our dual-scale tribunal architecture is MORE rigorous than the single-model PRM. If we expose the tribunal as an API (which we already have via the MCP server), a client's RL loop can use OUR tribunal as its reward model.

```
CLIENT RL LOOP:
  Agent acts → outcome captured
  Outcome sent to swarmandbee.ai/tribunal/api
  Tribunal weighs it (dual scale, 5 dimensions)
  Weight sent back as reward signal
  Agent weights updated

  = TRIBUNAL-AS-A-SERVICE for RL
  = Monthly recurring revenue
  = The tribunal becomes the product, not just the quality gate
```

## Hardware Requirements

```
MINIMUM (what we have now):
  2x RTX 6000 96GB — can run RL on 14B-32B models
  Serves 1-2 clients in RL mode

WITH FLEET (48x RTX 4500):
  Can run RL on 70B+ models
  32 GPUs for rollout + 16 for PRM/trainer
  Serves 10+ clients simultaneously

GROK'S REFERENCE (128x RTX 6000):
  Full enterprise: 64 actor + 32 rollout + 32 PRM
  128 parallel rollouts
  Serves 50+ clients
```

## The Roadmap

```
NOW:    Weight Shop (Tier 1) — sell pairs, $80-$320
NEXT:   Enterprise Cook (Tier 2) — cook for clients, $5K-$25K  
FUTURE: RL-as-a-Service (Tier 3) — continuous improvement, $2K/month
        Tribunal-as-a-Service — our dual-scale as the PRM, API pricing

Each tier builds on the previous.
Each tier needs the tribunal.
The tribunal is the moat at every tier.
```

---

*The weight is the one-time buy. The RL is the subscription.*
*The tribunal is the reward model. The deed is the receipt.*
*Every conversation makes the agent smarter. Every improvement is provable.*
