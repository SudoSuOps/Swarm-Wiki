# Enterprise Cookbook — Two-Tier Business Model

**Source**: Grok enterprise playbook + Swarm & Bee production economics
**Status**: BUSINESS MODEL VALIDATED

## Two Tiers

```
TIER 1: WEIGHT SHOP (self-serve)
  swarmandbee.ai/shop
  Download weight → cook yourself → deploy
  $0.016-$0.048/lb × 5,000 lbs = $80-$240
  Client provides their own GPU (RTX 4090/4500, $2,750)
  Cook time: 2-4 hours
  Includes: 5 formats + deed certs + OM + Unsloth code snippet + eval script
  
  WHO: Solo builders, small teams, OpenClaw operators
  WHY: "I know how to cook, I just need better ingredients"

TIER 2: ENTERPRISE (managed cook)
  Custom agent build → we cook it for you
  $5K-$25K per custom Clawbot
  + monthly RL hosting (continuous improvement)
  
  Client provides: 30-day session history or domain docs
  We provide: memory engineering + trace collection + synthetic gen +
              fine-tune (LoRA or full SFT) + eval suite + deployment
  
  WHO: Companies deploying 5-50+ agents, enterprise compliance
  WHY: "I don't have 40 hours. Build me a reliable agent."
```

## Enterprise Delivery Workflow

```
WEEK 1: ONBOARD
  Client provides 30-day session history or domain docs
  We build base memory files (SOUL.md + MEMORY.md + DREAMS.md)
  Domain assessment: which failure categories are they hitting?

WEEK 2: FORGE
  Collect + label real failure traces
  Generate synthetic trajectories targeting their pain points
  5K-50K pairs (tribunal-weighed, deed-backed)
  Contrastive pairs: bad response + good response

WEEK 3: COOK
  LoRA on their preferred base model (Qwen 3.5 32B default)
  r=32, alpha=64, 2 epochs, QLoRA 4-bit
  Eval suite: 200-test benchmark (tool accuracy, loop rate, etc.)
  Before/after chart = the deliverable

WEEK 4: DEPLOY + RL
  Deploy hardened model (client self-hosted or our managed hosting)
  OpenClaw-RL layer for continuous improvement
  Nightly DREAMS + git PR reviews
  Monthly weight refresh (virgin jelly subscription)
```

## Enterprise Pricing

| Tier | What | Price | Margin |
|------|------|-------|--------|
| **Starter** | Memory engineering + 5K pair dataset | $5,000 | High |
| **Professional** | + LoRA fine-tune + eval suite | $15,000 | High |
| **Enterprise** | + full SFT + RL + managed hosting | $25,000 + $2K/mo | Recurring |
| **Weight only** (shop) | 5,000 lbs download | $80-$320 | 20x energy |

## Hardware Economics

```
OUR RIG (current):
  2x RTX PRO 6000 96GB + 1x RTX 4500 32GB = 224GB VRAM
  Can serve: 2-3 enterprise clients simultaneously
  Can cook: LoRA on 32B in 4h, full SFT on 14B
  
OUR RIG (with fleet — 48x RTX 4500):
  + 1,536 GB VRAM
  Can serve: 50+ enterprise clients
  Can cook: full SFT on 70B, parallel client jobs
  Synthetic gen: 50K pairs in <1 hour

GROK'S REFERENCE (128x RTX 6000):
  12,288 GB VRAM
  "This turns your hardware into a client-delivery factory"
  We don't need 128 GPUs to start. We need them to scale.
```

## The ClawForge Vision

Grok describes a "ClawForge meta-agent" that spawns, trains, and deploys client-specific sub-agents automatically. That's SwarmRefinery:

```
SwarmRefinery = ClawForge

  SHIFT 1: Collect client traces + tribunal weigh
  SHIFT 2: Cook (LoRA/SFT) + eval
  SHIFT 3: Deploy + RL + monitoring

  The refinery IS the factory.
  The tribunal IS the quality gate.
  The deeds ARE the proof of work.
```

## Why We Win at Enterprise

| Capability | Generic AI Consultancy | Swarm & Bee |
|-----------|----------------------|-------------|
| Data quality | "We'll clean your data" | Dual-scale tribunal, 5 dimensions, 0.85 threshold |
| Provenance | "Trust us" | SHA-256 → Merkle → Hedera anchor |
| Failure taxonomy | Generic best practices | 10 failure labels from real X/HN signal |
| Eval | "It feels better" | Before/after metrics with deed-backed proof |
| Continuous | One-time delivery | Virgin jelly subscription + RL loop |
| Price | $50K-$200K consulting | $5K-$25K + $2K/mo |

---

*Tier 1: sell the ingredients ($80-$320)*
*Tier 2: sell the cooking service ($5K-$25K)*
*Both need the tribunal. Both need the deeds.*
*The quality gate is the moat at every tier.*
