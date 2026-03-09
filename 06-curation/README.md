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

## 5 Verticals

| Vertical | Status | Focus |
|----------|--------|-------|
| CRE | OPERATIONAL | Deal manufacturing, underwriting, capital markets |
| Medical | OPERATIONAL | Drug interactions, dosing, reconciliation, safety |
| Aviation | OPERATIONAL | Safety, maintenance, logistics |
| Drone | OPERATIONAL | Regulatory, operations, routing |
| Signal | OPERATIONAL | Market intelligence, trend detection |

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

## Related

- [middleware.md](middleware.md) -- 7-middleware chain details
- [orchestrator.md](orchestrator.md) -- State machine, planner, assembler, validator, publisher
- [verticals.md](verticals.md) -- 5 verticals and BaseVertical ABC
- [skills-discovery.md](skills-discovery.md) -- SKILL.md format and discovery system
