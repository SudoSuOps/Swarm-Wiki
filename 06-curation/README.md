# Curation

The curator fleet is the multi-vertical orchestrator that turns raw signals and data into platinum training pairs. It sits between the signal layer (ingestion) and the dataset factory (output), deciding what to cook, how to cook it, and whether the result meets quality standards.

## Fleet Architecture

Three-tier model hierarchy:

| Tier | Model | Role | Endpoint |
|------|-------|------|----------|
| Head | SwarmCurator-27B | Strategic decisions, complex analysis | swarmrails:8082 (vLLM, GPU1 Blackwell) |
| Analyst | SwarmCurator-9B | Detailed signal analysis, task planning | swarmrails:8081 (vLLM, GPU0 RTX PRO 4500) |
| Worker | SwarmCurator-2B | Classification, routing, triage | whale or edge nodes |

Each tier has an LLM endpoint plus an algorithmic fallback. The fleet operates with zero GPUs (fallbacks only), upgrades as models come online, and scales to full three-tier when all endpoints are available.

## 7-Middleware Chain

Processing flows through 7 ordered middlewares (see [middleware.md](middleware.md)):

```
SignalIngestion -> Classification(2B) -> Analysis(9B) -> Strategy(27B) -> QualityGate -> StateUpdate -> Dispatch
```

## 13 Domains

| Domain | Status | Focus |
|--------|--------|-------|
| aviation | COOKING | Safety (ASRS), maintenance, research (OpenAlex). 3-node cook fleet |
| cre | OPERATIONAL | Deal manufacturing, underwriting, capital markets |
| medical | OPERATIONAL | Drug interactions, dosing, reconciliation, safety |
| ai | OPERATIONAL | AI/ML research, model architectures |
| energy | OPERATIONAL | Grid, renewables, nuclear, storage |
| legal | OPERATIONAL | Regulatory, compliance, case analysis |
| crypto | OPERATIONAL | DeFi, protocol analysis, market structure |
| finance | OPERATIONAL | Capital markets, fixed income, derivatives |
| economic | OPERATIONAL | Macro, labor, trade, monetary policy |
| climate | OPERATIONAL | Environmental, emissions, adaptation |
| software | OPERATIONAL | Architecture, security, systems |
| supply_chain | OPERATIONAL | Logistics, procurement, optimization |
| patents | OPERATIONAL | IP analysis, prior art, claims |

See [verticals.md](verticals.md) for vertical configuration and the BaseVertical ABC.

## Plugin Architecture

Verticals implement the `BaseVertical` ABC, making it straightforward to add new domains. Each vertical defines task types, system prompts, quality criteria, and asset types. Configuration lives in `curator/verticals.yaml`.

## CLI

```bash
python3 -m curator fleet              # Run fleet orchestrator
python3 -m curator fleet --dry-run    # Show what would happen without executing
python3 -m curator skills             # List discovered skills
python3 -m curator skills --vertical cre  # List CRE skills only
```

## Prompt Machine (Added 2026-03-15)

The Prompt Machine is an automated prompt evolution system that closes the loop between cook output quality and prompt selection. See [prompt-machine.md](prompt-machine.md) for full details.

Key components:
- **Prompt Registry**: Shared library (cook-domain-prompts repo), SHA-256 hashed for tracking
- **Softmax Allocation**: Temperature-scaled weighting from telemetry scores (t=0.5, 5% floor)
- **8 Structured Mutations**: 4 axes (specificity, reasoning, numeric, persona) x 2 parents
- **Extinction Rule**: avg < 85 + 200 pairs -> prompt removed from pool
- **Telemetry**: 6 endpoints on hive-ledger for leaderboard, domain matrix, timeline, adoption

## Related

- [prompt-machine.md](prompt-machine.md) -- Prompt evolution, mutations, softmax allocation
- [middleware.md](middleware.md) -- 7-middleware chain details
- [orchestrator.md](orchestrator.md) -- State machine, planner, assembler, validator, publisher
- [verticals.md](verticals.md) -- 5 verticals and BaseVertical ABC
- [skills-discovery.md](skills-discovery.md) -- SKILL.md format and discovery system
