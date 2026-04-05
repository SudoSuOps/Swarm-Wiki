# SwarmWiki

Single source of truth for all Swarm & Bee IP. Defendable AI Training Data Infrastructure.

**Founded by Donovan Mackey** — 30-year CRE broker, $8B in closed transactions. Licensed Florida real estate brokerage. Jupiter, FL. The same discipline that makes a $50M office tower bankable — title search, independent appraisal, title insurance, closing statement — now applied to AI training data.

**Core thesis**: We don't sell datasets. We sell **Proof of Location** — measurable, reproducible relocation of AI models from generic to specialist capability. The deed proves origin. The title insures quality. The Proof of Location proves outcome.

## Live Systems

| System | URL | Status |
|--------|-----|--------|
| Main Site | [swarmandbee.ai](https://swarmandbee.ai) | LIVE — 12 routes |
| Tribunal Arena | [swarmandbee.ai/chain](https://swarmandbee.ai/chain/) | LIVE — real-time hex grid |
| Deed Office | [swarmandbee.ai/deed](https://swarmandbee.ai/deed/) | LIVE — 8,400+ deeds searchable |
| Dataset Shop | [swarmandbee.ai/shop](https://swarmandbee.ai/shop/) | LIVE — Stripe, 10 domains |
| GEO Scanner | [swarmandbee.ai/geo](https://swarmandbee.ai/geo/) | LIVE — LLM-powered, 3 seconds |
| Provenance Graph | [swarmandbee.ai/graph](https://swarmandbee.ai/graph/) | LIVE — 512 nodes |
| Fleet Status | [swarmandbee.ai/status](https://swarmandbee.ai/status/) | LIVE — 14/14 checks |
| Title Insurance | [swarmandbee.ai/title](https://swarmandbee.ai/title/) | LIVE — closing statement |
| Custom Builder | [swarmandbee.ai/builder](https://swarmandbee.ai/builder/) | LIVE — 6-phase client process |
| About / Manifesto | [swarmandbee.ai/about](https://swarmandbee.ai/about/) | LIVE — full thesis |
| Offering Memorandum | [swarmandbee.ai/om](https://swarmandbee.ai/om/) | LIVE — Bloomberg-style template |
| Blog | [swarmandbee.ai/blog](https://swarmandbee.ai/blog/) | LIVE — news feed |
| Hedera Anchors | [hashscan.io](https://hashscan.io/#/mainnet/topic/0.0.10291838) | MAINNET — topic 0.0.10291838 |

## Dashboard (updated 2026-04-04)

| Metric | Value | Details |
|--------|-------|---------|
| Pairs in PostgreSQL | 1,495,857 | Across 10 registered domains |
| Deeds Filed | 8,400+ | Dual-judge scored, Merkle-anchored |
| Royal Jelly | 5,200+ | Score >= 0.75, production-grade |
| Merkle Batches | 167+ | 50 deeds per SHA256 tree |
| Domains Selling | 2 | Medical + Grants (Master Writer) |
| Domains in Tribunal | 4 | CRE, Aviation, Self-Healing, Legal |
| Domains Coming Soon | 4 | Finance, Imaging, Blockchain, Research |
| Tribunal Rate | 777 pairs/hr | 24/7 autonomous, Judge A + Judge B |
| Permanent Services | 7 | tribunal-runner, deed-recorder, watchdog, 3 APIs, chain |
| GPU Fleet | 128x RTX 6000 + 48x RTX 4500 | 13.5 TB total VRAM |
| Active Cook | Gemma 4 31B | 75% complete, eval_loss 0.5194 |
| Website Routes | 12 | All returning 200, all SEO tagged |
| ENS Domains | 14 | swarmgeo.eth (newest) + 13 others |
| Claude Code Skills | 5 | /inventory, /cook-monitor, /deploy, /geo-report, /tribunal-status |

## Architecture (April 2026)

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  swarmandbee.ai → 12 routes, Stripe shop, GEO scanner      │
│  Cloudflare Tunnel → Zima Lite (.173) → nginx + 3 APIs     │
├─────────────────────────────────────────────────────────────┤
│                    TRIBUNAL LAYER                            │
│  tribunal-runner (24/7, systemd, swarmrails)                │
│  Judge A: gemma3:12b (RTX PRO 6000, GPU1)                  │
│  Judge B: qwen2.5:7b (RTX 3090, whale rig)                 │
│  Protocol: 2-pass, drift ≤ 0.15, deterministic             │
├─────────────────────────────────────────────────────────────┤
│                    RECORDING LAYER                           │
│  deed-recorder (zima-edge, 24/7, 50W)                      │
│  scored → deeds table → Merkle batches (every 50)          │
│  NAS filing: /mnt/swarm/datasets/{domain}/deeds/           │
│  CSV ledger export: hourly                                  │
├─────────────────────────────────────────────────────────────┤
│                    FINALITY LAYER                            │
│  L1: PostgreSQL (NAS .102:5433)                             │
│  L2: Merkle trees (SHA256, batches of 50)                   │
│  L3: NAS archive (/mnt/swarm/swarmdeed-finality/)          │
│  L4: Hedera HCS mainnet (topic 0.0.10291838)               │
│  L5: ENS domains (14 registered)                            │
├─────────────────────────────────────────────────────────────┤
│                    MONITORING LAYER                          │
│  swarm-watchdog (zima-edge, 14 checks, every 5min)         │
│  Resend email alerts on failure                             │
│  swarmandbee.ai/status/ (auto-refresh 30s)                 │
└─────────────────────────────────────────────────────────────┘
```

## The Proof of Location Framework

**We don't sell data. We sell relocation.**

| Concept | CRE Analogy | Swarm & Bee |
|---------|-------------|-------------|
| The Asset | Building | AI training pairs |
| The Location | Neighborhood | Model capability space |
| The Deed | Title deed | Dual-judge scored deed certificate |
| The Title | Title insurance | Score guarantee ±0.15 |
| The Appraisal | Independent valuation | Tribunal (2 base model judges) |
| The Relocation | Moving to a better location | Fine-tuning on Royal Jelly |
| The Proof | Comparable sales | Proof of Location benchmark (before/after delta) |
| The Flight Sheet | Relocation plan | Hardware + cost + timeline + client approval |

### Three Location Classes

| Class | Tier | Score | Outcome |
|-------|------|-------|---------|
| Class A | Royal Jelly | >= 0.75 | Prime location. Specialist responses. Irreplaceable. |
| Class B | Honey | 0.50-0.74 | Decent area. Adequate. Replaceable. |
| Class C | Propolis | < 0.50 | Bad neighborhood. Hallucinations. No tenants. |

## Fleet

| Machine | Hardware | Role | SSH |
|---------|----------|------|-----|
| swarmrails | 2x RTX PRO 6000 96GB + Xeon w9-3475X 72T 256GB | Training + Judge A + Chain API + GEO | localhost |
| whale (.99) | RTX 3090 24GB | Judge B (qwen2.5:7b) | key-only |
| zima-edge (.230) | Intel N150 + T1000 4GB | Deed recorder + watchdog | key-only |
| zima-lite (.173) | Celeron N3450 8GB | Web host + 3 APIs | password |
| zima-swarm (.112) | Intel N150 16GB | Docker + Tailscale | key-only |
| jetson (.79) | Orin Nano 8GB | Edge inference (gemma3:4b) | password |
| NAS (.102) | Synology DS1525+ | PostgreSQL + 3 NFS shares | password |

## Data Warehouse

| Domain | Pairs in DB | On Disk (NAS) | Deeds | Shop Status |
|--------|-------------|---------------|-------|-------------|
| medical | 417,136 | 796,846 | 5,038 | AVAILABLE |
| grants | 35,271 | 80,132 | 1,378+ | AVAILABLE (Master Writer) |
| cre | 810,097 | 810,097 | 0 | In tribunal queue |
| self_healing | 186,875 | 186,876 | 0 | In tribunal queue |
| aviation | 41,477 | 51,475 | 0 | In tribunal queue |
| legal | 5,001 | 79,910 | 0 | Coming soon |
| finance | 0 | 28,682 | 0 | Coming soon |
| imaging | 0 | 25,058 images | 0 | Coming soon (multimodal) |
| blockchain | 0 | TBD | 0 | Coming soon |
| research | 0 | 750,000+ (OpenAlex) | 0 | Coming soon |

**Total**: 1.5M in PostgreSQL, 2.5M+ on disk, 30K+ medical images

## Sections

| # | Section | What's Inside |
|---|---------|---------------|
| 01 | [Architecture](01-architecture/) | 5-layer stack, data flow, sovereign compute, glossary |
| 02 | [Models](02-models/) | Fleet roster, 12+ model specs, Gemma 4 31B cook, training patterns |
| 03 | [Scripts](03-scripts/) | Cook, train, deploy, eval scripts |
| 04 | [Datasets](04-datasets/) | Factory protocol, quality gates, Royal Jelly Protocol, schemas |
| 05 | [Signal](05-signal/) | SwarmSignal v2 (planned), lead gen, edge deployment |
| 06 | [Curation](06-curation/) | Tribunal methodology, prompt machine, domain verticals |
| 07 | [Skills](07-skills/) | Domain skills, Claude Code skills (/inventory, /cook-monitor, etc.) |
| 08 | [API](08-api/) | deed-api, shop-api, geo-api, chain-api, endpoints |
| 09 | [Infrastructure](09-infrastructure/) | GPU fleet, networking, NAS, edge nodes, systemd services |
| 10 | [Hedera](10-hedera/) | Mainnet anchoring, topic 0.0.10291838, 5-layer finality |
| 11 | [swarmbee.ai](11-swarmbee-ai/) | 12 routes, Stripe shop, GEO scanner, arena, OM template |
| 12 | [Repos](12-repos/) | GitHub repos mapped |
| 13 | [Competitive](13-competitive/) | Market landscape, Karpathy signal (12M views) |
| 14 | [Business](14-business/) | Proof of Location, pricing, packages, distribution plan |
| 15 | [Operations](15-operations/) | Daily ops, tribunal runner, deed recorder, watchdog |
| 16 | [Dev Tools](16-dev-tools/) | CLI reference, Stripe, Discord, Claude Code skills |
| 17 | [Audits](17-audits/) | Code audit (Phase 1+2), domain audits, 206 tests pass |
| 18 | [Blueprints](18-blueprints/) | SwarmSignal v2, arena vision, Proof of Location protocol |
| 19 | [Research](19-research/) | 50 papers: LLM-as-judge, agents, CoT, RAG, knowledge graphs (EgoAlpha) |

## Karpathy Connection (April 2026, 12M views)

> "I think there is room here for an incredible new product instead of a hacky collection of scripts."

This wiki follows Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
- **Raw Sources** → 2.5M pairs on NAS + PostgreSQL
- **The Wiki** → This repo (80+ pages) + deeds table (8,400+ deeds)
- **The Schema** → scoring_prompt.py + flight sheets + CLAUDE.md

The market wants **outcome infrastructure**. Not tools, not dashboards — systems that compound model capability over time. That's what location does in CRE. That's what Royal Jelly does in AI.

## Links

- Website: [swarmandbee.ai](https://swarmandbee.ai)
- Twitter/X: [@swarmandbee](https://x.com/swarmandbee)
- GitHub: [SudoSuOps](https://github.com/SudoSuOps)
- Hedera: [topic 0.0.10291838](https://hashscan.io/#/mainnet/topic/0.0.10291838)
- ENS: swarmchain.eth, swarmdeed.eth, swarmgraph.eth, swarmgeo.eth + 10 more

---

*Validate the Validator. Prove the Location.*

*Last updated: 2026-04-04*

---

## The Doctrine — Glass Wall

The [glass-wall](https://github.com/SudoSuOps/glass-wall) repo is the philosophical foundation — 19 documents covering the vision, the biology, the arena, the doctrine. The glass-wall is the WHY. This wiki is the HOW.

| Document | What It Covers |
|----------|---------------|
| [GENESIS.md](https://github.com/SudoSuOps/glass-wall/blob/main/GENESIS.md) | The first titled AI data pair — block 8f42666ef87c |
| [DOCTRINE.md](https://github.com/SudoSuOps/glass-wall/blob/main/DOCTRINE.md) | Six roles, one tribunal — Scout, Router, Filter, Repair, Critic, Katniss |
| [HIVE.md](https://github.com/SudoSuOps/glass-wall/blob/main/HIVE.md) | Biology = architecture = product. 50-bee hive on Xeon. |
| [ARENA.md](https://github.com/SudoSuOps/glass-wall/blob/main/ARENA.md) | Convergence through elimination. The tributes. The games. |
| [SWARMOS.md](https://github.com/SudoSuOps/glass-wall/blob/main/SWARMOS.md) | HiveOS for AI mining — flight sheets, power tuning, hashrate |
| [SWARMEVAL.md](https://github.com/SudoSuOps/glass-wall/blob/main/SWARMEVAL.md) | Combat evaluation — drop your model in the chain |
| [PRESSURE_TO_TRUTH.md](https://github.com/SudoSuOps/glass-wall/blob/main/PRESSURE_TO_TRUTH.md) | The thesis under pressure |
| [SPECTATORS.md](https://github.com/SudoSuOps/glass-wall/blob/main/SPECTATORS.md) | The audience — who watches the glass wall |
