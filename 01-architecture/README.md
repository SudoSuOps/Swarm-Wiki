# Swarm Architecture

Swarm is an industrial AI intelligence infrastructure built on a four-layer stack. Every layer has a job, every model earns its slot, and nothing ships without passing through the gate.

## The Four-Layer Stack

### L1 -- SwarmSignal (The Radar)

Market intelligence engine. 11 signal workers run on 15-minute cycles, scraping public data sources for actionable events: EDGAR filings, county records, lease expirations, tenant movements, rate changes, construction permits. Each signal gets scored by EntityScorer and tracked by VelocityTracker. High-priority signals (P1-P3) fire immediately to Discord and the curator pipeline.

Hardware: Runs on edge devices (Jetson Orin Nano, zima-edge-1 Intel N150). The SwarmSignal-2B model classifies and prioritizes at the edge with zero cloud dependency.

### L2 -- Swarm Infrastructure (The Factory Floor)

Judge and Curate. This is AI observing AI. The curator fleet (2B/9B/27B) ingests signals, classifies them, generates training pairs, and validates output quality. The factory pipeline (skeleton, generate, gate, promote, publish) converts raw intelligence into verified training data.

Six deterministic gates replace what was once a standalone judge model: JSON validity, schema compliance, enum validation, verdict match, score MAE, and confidence thresholds. The 27B model handles subjective quality calls that deterministic rules cannot.

Hardware: Inference runs on swarmrails (RTX PRO 4500 Blackwell 32GB + RTX PRO 6000 Blackwell 96GB). Training runs on the same Blackwell GPUs via Unsloth.

### L3 -- Vertical Systems (The Revenue Layer)

Domain-specific models trained on curated intelligence objects:

- **CRE** (Commercial Real Estate): SwarmCRE-35B, 19 skills, 643K pairs, 10 specialties. Underwriting, IC memos, lease analysis, market comps, deal tracking.
- **Medical**: SwarmPharma-35B, 9 skills, 432K pairs, 85 specialties. Drug interactions, dose calculations, adverse events, pregnancy safety.
- **Aviation**: 45K pairs, 157 specialties. Maintenance, compliance, flight operations.
- **Capital Markets**: SwarmCapitalMarkets-27B (training), 45K pairs. CMBS, debt maturity, rate advisory, deal origination.

### L4 -- SwarmLedger (The Trust Layer)

Provenance and verification via Hedera Hashgraph. Every intelligence object can be sealed with a SHA-256 hash published to HCS (Hedera Consensus Service), producing a guarantee.json with on-chain provenance. HTS tokens (Block, Pair, Model, Deed, Dataset) provide asset tracking. 8 registered agents operate on mainnet.

## Hardware Mapping

```
Edge Devices          Inference Servers         Training Rigs
--------------        -------------------       ----------------
Jetson Orin Nano      RTX PRO 4500 (32GB)       Same Blackwell GPUs
  SwarmSignal-2B        SwarmCurator-9B            Unsloth bf16 LoRA
  Q4_K_M GGUF          vLLM bf16, 165 tok/s       packing=True
  CPU inference         swarmrails:8081            r=64, alpha=32

zima-edge-1 (N150)   RTX PRO 6000 (96GB)
  SwarmSignal-2B        SwarmCurator-27B
  15-min cycles         vLLM bf16, 88 tok/s
  Discord bridge        swarmrails:8082

                      whale RTX 3090 (24GB)
                        SwarmCurator-2B
                        BeeMini Router
```

## Intelligence Feedback Loop

The system is self-reinforcing:

1. **Signal detects** -- Workers find market events (EDGAR filing, lease expiration, rate change)
2. **Curate produces** -- Factory generates training pairs from detected signals
3. **Models improve** -- New pairs train the next generation of vertical models
4. **Judge validates** -- Deterministic gates + 27B subjective review verify quality
5. **Signal detects again** -- Better models produce better signals, which produce better data

This is not a one-shot pipeline. Every cycle through the loop makes the next cycle sharper. The data builds on itself because the models that process signals are trained on the output of previous signal cycles.

## Key Design Principles

- **Bottom up, no bloat.** Every model, every skill, every gate exists because it maps to a real step in how deals actually get done.
- **Signal first.** Nothing happens without a market event. No hallucinated analysis, no speculative generation.
- **Every model earns its slot.** If a model does not measurably improve output quality or reduce latency, it gets cut.
- **Deterministic where possible, LLM where necessary.** Six hard gates handle what rules can handle. The 27B handles what rules cannot.
