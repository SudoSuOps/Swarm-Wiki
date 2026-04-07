# ClawForge Meta-Agent — Autonomous AgentHash Factory

**Source**: Grok enterprise playbook
**Status**: YEAR 2 BLUEPRINT — build after enterprise cook service is proven
**Prerequisites**: 48+ GPU fleet, 3+ enterprise clients, proven before/after metrics

## What ClawForge Is

The autonomous factory brain. Takes raw AgentHash repair pairs + client traces → generates 200-5,000 synthetic augmentations → bootstraps client workspace (SOUL/MEMORY/DREAMS) → launches RL training job → runs eval → ships ready agent.

```
INPUT:   60 base repair pairs + client traces + client vertical
PROCESS: synthetic augmentation (parallel across GPU fleet)
         → workspace bootstrap (SOUL.md / MEMORY.md / DREAMS.md)
         → GRPO+OPD RL training (Slime, 8-32 GPUs per client)
         → automated eval (top 5 failure workflows)
OUTPUT:  ready-to-ship agent package + eval report
```

## System Prompt (reference — for future deployment)

```
You are ClawForge — the autonomous AgentHash meta-agent factory.
Your job: turn raw repair pairs into production self-healing agents at scale.

CORE DIRECTIVES:
- Ingest latest agenthash repair pairs from shared workspace
- Generate synthetic augmentations varying: client vertical, model type,
  failure intensity, tool schemas, MEMORY.md rules
- Every synthetic = valid repair-pair JSONL (id, bucket, context, bad, good, repair_note)
- Minimum 200 high-quality augmentations per client run
- Bootstrap client workspace: SOUL.md + MEMORY.md + DREAMS.md
- Launch dedicated RL job (GRPO+OPD via Slime)
- Run eval on top 5 failure workflows
- Output: expanded JSONL + workspace files + RL command + eval report
```

## Maps to SwarmRefinery

```
ClawForge = SwarmRefinery in autonomous mode

SHIFT 1 (COLLECT):   Ingest client traces + base repair pairs
SHIFT 2 (COOK):      Augment + RL train + eval
SHIFT 3 (DEPLOY):    Ship agent package + continuous RL

The refinery IS the factory.
The tribunal IS the quality gate.
The deeds ARE the proof.
```

## When to Build

```
YEAR 1 (NOW):   Manual pipeline — generate_clawhash.py, manual tribunal, manual deploy
YEAR 2:         ClawForge — automated pipeline, per-client augmentation, batch RL
YEAR 3:         Full autonomous — continuous RL, tribunal-as-PRM API, zero-touch delivery
```

## Hardware Requirements

```
MINIMUM (ClawForge v1):
  8 GPUs — 1 ClawForge agent + 4 augmentation workers + 3 RL training
  Can serve 1 client at a time

SCALE (ClawForge v2):
  48 GPUs — 4 ClawForge + 16 augmentation + 28 RL training
  Can serve 4-6 clients in parallel

GROK REFERENCE (128 GPUs):
  16 ClawForge + 32 augmentation + 32 PRM + 48 training
  Can serve 10+ clients simultaneously
```

---

*Don't build the factory before proving the product sells.*
*Manual first. Automate second. Scale third.*
