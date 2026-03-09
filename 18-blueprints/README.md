# Blueprints

Product and technical blueprints defining the Swarm & Bee vision.

## Documents

| Blueprint | Date | Scope |
|-----------|------|-------|
| [SwarmCurator-9B Blueprint](swarmcurator-9b-blueprint.md) | 2026-03-06 | Autonomous data engineering AI — replaces algorithmic planning with LLM reasoning |
| [Last-Mile AI Appliances](lastmile-blueprint.md) | 2026-02-24 | Physical edge devices (BeeMini, BeePro, BeeRack) running domain agents on-premises |

## Vision Summary

```
CLOUD (Swarm HQ)                    EDGE (Customer Site)
─────────────────                   ────────────────────
SwarmCurator-27B (head)             BeeMini ($249, 4B, 10W)
SwarmCurator-9B (ops)               BeePro ($599, 9B, 40W)
SwarmCapitalMarkets-27B             BeeRack ($3,500/mo, 27B, 350W)
SwarmPharma-35B
                                    95% local decisions
2-5% escalations ◄────────────────► 5% cloud escalation

Training flywheel:                  Data never leaves device
escalations → new pairs → retrain   Hedera receipts → chain
→ deploy via OTA updates            $0.0001/receipt
```
