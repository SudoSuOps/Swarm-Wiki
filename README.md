# SwarmWiki

Single source of truth for all Swarm & Bee IP. Industrial AI Intelligence Infrastructure.

**Founded by Donovan Mackey** — 30-year CRE broker, Senior Managing Director at Marcus & Millichap, $8B in closed sales. The CRE vertical is built on decades of deal-making experience, not theory.

## Dashboard

| Metric | Count | Details |
|--------|-------|---------|
| Trained Models | 9 | 3 deployed, 1 training (CapitalMarkets-27B), 5 done |
| Skills | 35 | 19 CRE + 9 medical + 7 capital markets |
| Signal Workers | 11 | Real-time, 3-tier scheduling (15min/1hr/6hr) |
| Verified Pairs | 1,158,902+ | Across 5 verticals in R2 |
| Verticals | 5 | CRE, Medical, Aviation, Drone, Signal |
| GPU Nodes | 4 | swarmrails (2x Blackwell), whale (3090), Jetson, zima |
| HCS Topics | 5 | Mainnet immutable audit trails |
| HTS Tokens | 5 | Tokenized asset classes |
| API Endpoints | 40+ | router.swarmandbee.com |
| Repos | 17 | Full production ecosystem |

*Last updated: 2026-03-09*

## Architecture

```
Signal Workers (11 sources, real-time)
    -> SwarmCurator Fleet (27B + 9B + 2B)
    -> Vertical Models (CRE, Medical, Aviation, Pharma)
    -> Intelligence Objects (verified, structured)
    -> HCS Seal (SHA256 + guarantee.json)
    -> HTS Token (Deed per IO)
```

## Four-Layer Intelligence Stack

| Layer | Name | Role |
|-------|------|------|
| L1 | [SwarmSignal](05-signal/) | Market intelligence engine — the radar |
| L2 | [Swarm Infrastructure](06-curation/) | Judge + Curate — the factory floor |
| L3 | [Vertical Systems](02-models/) | CRE, Medical, Aviation, Pharma — revenue layer |
| L4 | [SwarmLedger](10-hedera/) | Trust + provenance — Hedera HCS/HTS |

## Sections

| # | Section | What's Inside |
|---|---------|---------------|
| 01 | [Architecture](01-architecture/) | Four-layer stack, deal machine mapping, data flow, glossary |
| 02 | [Models](02-models/) | Fleet roster, 9 model pages, Qwen3.5 reference, training patterns |
| 03 | [Scripts](03-scripts/) | Cook, train, deploy, eval script inventory |
| 04 | [Datasets](04-datasets/) | R2 inventory, factory protocol, quality gates, schemas |
| 05 | [Signal](05-signal/) | 11 workers, scorer, velocity, integrations, edge deployment |
| 06 | [Curation](06-curation/) | Middleware chain, orchestrator, verticals, skills discovery |
| 07 | [Skills](07-skills/) | 35 skills, SKILL.md format, validators, schemas |
| 08 | [API](08-api/) | 40+ endpoints, wallet metering, event machine, IOs |
| 09 | [Infrastructure](09-infrastructure/) | GPU cluster, networking, vLLM deployment |
| 10 | [Hedera](10-hedera/) | Mainnet deployment, agents, bridge, tokenization |
| 11 | [swarmbee.ai](11-swarmbee-ai/) | Web properties, Cloudflare Workers |
| 12 | [Repos](12-repos/) | 17 repos mapped with paths and descriptions |
| 13 | [Competitive](13-competitive/) | CRE tech landscape, 8 gaps nobody fills |
| 14 | [Business](14-business/) | Pricing tiers, monetization layers, engine architecture |
| 15 | [Operations](15-operations/) | Runbooks: daily ops, training, deployment |
| 16 | [Dev Tools](16-dev-tools/) | CLI reference, Supabase schema, Stripe, Discord, Wrangler |
| 17 | [Audits](17-audits/) | Market audits: CRE, medical, pharma, aviation, infrastructure, regulatory |
| 18 | [Blueprints](18-blueprints/) | SwarmCurator-9B blueprint, Last-Mile AI Appliances |

## The Deal Machine

The Swarm pipeline IS the Marcus & Millichap brokerage deal machine — encoded into AI infrastructure:

```
M&M DEAL LIFECYCLE                    SWARM PIPELINE
-----------------                    --------------
Make the dials                    ->  Signal Workers (11 sources, real-time)
Book the sits                     ->  SwarmCurator-2B classifies, routes
Do the proposals                  ->  SwarmCRE-35B underwriting + IC memos
Win the listing                   ->  Judge/Gate validates, seals
Go to market                      ->  Skills: market_report, comp_analyzer
Generate LOIs                     ->  Skills: bookmaker, lead_scorer
Best final, highest prob close    ->  SwarmCurator-27B strategic ranking
In escrow                         ->  deal_tracker skill, HCS Event topic
Due diligence                     ->  SwarmCRE-35B + research analysis
Hard deposit / contingencies      ->  Judge verification gate
Close                             ->  HCS seal (SHA256 + guarantee.json)
Steak dinner                      ->  Rinse and repeat
```
