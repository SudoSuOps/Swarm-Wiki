# API Gateway Architecture

The two Cloudflare Workers — SwarmRouter and swarm-api — are the public gateway to the entire Swarm & Bee compute network. Models, datasets, agents, skills, and edge appliances all plug into them.

## Two Workers, Two Missions

| Worker | Domain | Endpoints | Mission |
|--------|--------|-----------|---------|
| **SwarmRouter** | `router.swarmandbee.com` | 69 | Intelligence engine — skills, events, memory, state experts, IOs |
| **swarm-api** | `api.swarmandbee.com` | 14 | Commerce + medical inference — Stripe, data pull, SwarmMed |

They share Supabase (13 tables, pgvector), R2 (8 active buckets, 1.16M pairs), and Cloudflare AI bindings. But they serve fundamentally different roles.

## SwarmRouter: The Intelligence Engine

**Code**: `swarmrouter/worker/src/index.js` (~2000 lines)

69 endpoints organized into 7 groups:

| Group | Endpoints | Key Capabilities |
|-------|-----------|------------------|
| Skills | 7 | Execute 28 composable skills (19 CRE + 9 medical), SKILL.md specs, testing |
| Intelligence Objects | 6 | PIO CRUD, search, feed, `/cook` endpoint for on-demand generation |
| Events | 5 | 22 event types across 5 categories, entity extraction, timeline |
| Memory | 2 | Semantic search (BGE-Base 768-dim pgvector), context retrieval |
| Router | 3 | Routing decisions, health, stats |
| State Experts | 1 | 50 state-specific CRE expert personas with market-heat weighting |
| Wallet/Metering | 4+ | `sb_live_` API keys, credit tiers, usage tracking |

### Skill Execution Flow

```
User request → /skill/{name}
  → registry.js resolves skill module
  → SKILL.md spec injected into system prompt
  → CF AI (Qwen3-30B-A3B) generates response
  → Validator checks output schema
  → Response returned (cost: ~$0.00004/call)
```

28 skills are composable — a single user query can chain `intelligence_query` → `comp_analyzer` → `debt_analyzer` → `email_composer`.

### State Expert System

`worker/src/states.js` (599 lines) defines 50 state-specific CRE expert personas. Each state expert knows local market dynamics, regulatory environment, and key metrics. Market heat weighting adjusts response confidence based on current signal velocity.

### Event Machine

22 event types across 5 categories (deal, supply, ownership, macro, tenant). EDGAR pump feeds 15 REIT tickers. Events stored in Supabase + R2 with entity extraction and resolution. Timeline queries let you track any entity's event history.

## swarm-api: Commerce + Medical Inference

**Code**: `swarm-api-worker/src/index.js` + `src/handlers/`

14 endpoints in 4 groups:

| Group | Endpoints | Key Capabilities |
|-------|-----------|------------------|
| Contact/Forms | 3 | Contact form, LOI submission, RFP submission |
| Medical | 2 | SwarmMed inference with PHI/emergency guards, Together.ai fallback |
| Commerce | 5 | Stripe checkout/subscribe/webhook, data pull with quota enforcement |
| Catalog | 4 | Dataset catalog, count, sample, cook orders |

### Stripe Integration

```
Checkout flow:
  POST /api/checkout → dynamic Stripe session (no pre-created Products)
  → success_url callback → sk_swarm_ API key generated
  → key stored in R2 (swarm-ops bucket)
  → HMAC webhook verification on payment events

Tiers:
  SwarmCurator  $20/mo  — 20K pairs, 1 vertical
  Full Access   $49/mo  — 250K pairs, 5 streams
  Enterprise    Custom  — Dedicated models, API
  Per-IO        $0.0002 — Per Intelligence Object
```

### SwarmMed Inference

Medical queries get special handling:
- PHI detection guard (refuses to process identifiable patient data)
- Emergency keyword detection (redirects to 911/poison control)
- Primary: CF AI Qwen3-30B → Fallback: Together.ai Qwen-235B
- Response includes confidence score + disclaimer

### Data Commerce

`POST /api/data/pull` enforces quota from `sk_swarm_` API key. Pulls from R2 buckets with filtering by vertical, specialty, difficulty tier. Rate-limited per key tier.

## The Inference Gap: Why Workers Don't Call Self-Hosted Models

**Critical architectural fact**: Neither CF Worker directly calls swarmrails or whale. The Workers use only Cloudflare AI bindings.

```
CF Worker Layer (edge)         GPU Fleet (on-prem)
─────────────────────         ─────────────────────
CF AI: Qwen3-30B-A3B          vLLM: SwarmCurator-9B  (:8081)
CF AI: Llama-3.2-3B           vLLM: SwarmCurator-27B (:8082)
CF AI: BGE-Base embeddings     Ollama: BeeMini Router (:8080)
                               Together.ai: Qwen-235B (serverless)

          ↑ no direct connection ↑

The bridge: Python Curator Middleware
─────────────────────────────────────
curator/middleware.py → OpenAI-compatible /v1/chat/completions
  SignalIngestion → Classification(2B) → Analysis(9B) → Strategy(27B)
  → QualityGate → StateUpdate → Dispatch
```

This is intentional:
1. **CF Workers can't make arbitrary outbound HTTP** to private IPs
2. **Latency**: Edge → home server round-trip would negate edge benefits
3. **Separation of concerns**: Workers handle public API surface; Python curator handles internal intelligence pipeline

The Python curator fleet (`curator/middleware.py`) is the only code that talks to vLLM directly. It uses the standard OpenAI-compatible API at `swarmrails:8081` and `swarmrails:8082`.

## Four-Layer Inference Topology

```
Layer 1: Edge (Cloudflare AI)
  ├── @cf/qwen/qwen3-30b-a3b-fp8     — Primary edge model (skills, IOs, events)
  ├── @cf/meta/llama-3.2-3b-instruct  — Fallback / lightweight tasks
  └── @cf/baai/bge-base-en-v1.5       — Embeddings (768-dim, cosine)
  Cost: ~$0.00004/call, <100ms latency

Layer 2: Orchestration (Python Curator)
  ├── 7-middleware chain (SignalIngestion → Dispatch)
  ├── Calls vLLM via OpenAI-compatible API
  ├── Calls Together.ai for heavyweight tasks
  └── Decision logging → .state/fleet_runs.jsonl
  Cost: $0/call (self-hosted), network only

Layer 3: GPU Fleet (On-Prem vLLM)
  ├── SwarmCurator-9B bf16   — GPU 0 (RTX PRO 4500, 32GB) — 165 tok/s x4
  ├── SwarmCurator-27B bf16  — GPU 1 (RTX PRO 6000, 96GB) — 88 tok/s x4
  ├── Router Proxy           — Ollama BeeMini (:8080)
  └── whale RTX 3090         — BeeMini GGUF (:8081)
  Cost: electricity only, ~1,740 pairs/hr combined

Layer 4: Serverless (Together.ai)
  ├── Qwen3-Next-80B-A3B     — Fast generation (cook pipeline)
  └── Qwen3-235B-A22B        — Quality rewrites, RPA
  Cost: ~$0.005/pair, used for cook/train not inference
```

## Data Flow: Signal to Sealed Intelligence Object

```
Signal Worker (edge)
  → Supabase events table + R2
  → Python Curator ingests (middleware chain)
  → vLLM generates training pairs (9B/27B)
  → 6 deterministic gates validate
  → 27B subjective quality review
  → R2 bucket (sb-cre, sb-medical, etc.)
  → Factory assembles train JSONL
  → Unsloth trains next model generation
  → vLLM deploys updated model
  → Better signals → better data → loop

Public API serves the results:
  SwarmRouter → /search, /feed, /cook, /skill/*
  swarm-api → /api/data/pull (paid), /api/med/* (SwarmMed)
```

## What "Gateway to the Compute Network" Means

The two Workers are the **public surface** of a much deeper system:

| Resource | Access Path |
|----------|-------------|
| **28 AI Skills** | `POST router.swarmandbee.com/skill/{name}` |
| **1.16M Training Pairs** | `POST api.swarmandbee.com/api/data/pull` (paid) |
| **50-State CRE Intelligence** | `POST router.swarmandbee.com/state-expert` |
| **22 Event Types** | `GET router.swarmandbee.com/events/query` |
| **Semantic Memory** | `POST router.swarmandbee.com/memory/search` |
| **Medical Inference** | `POST api.swarmandbee.com/api/med/query` |
| **Hedera Provenance** | Via guarantee.json links in IO metadata |
| **Dataset Samples** | `GET api.swarmandbee.com/api/data/sample` |
| **Cook Orders** | `POST api.swarmandbee.com/api/data/cook` |

Every model trained, every pair cooked, every signal detected, every skill built — it all becomes accessible through these two Workers. They're not just API endpoints. They're the storefront for the entire AI refinery.

## Future: Bridging the Gap

The inference gap (Workers can't call self-hosted models) will close with:
1. **Cloudflare Tunnel** (cloudflared on swarmrails) — expose vLLM endpoints to Workers via tunnel
2. **SwarmScaler** (`api.swarmandbee.ai` — in development) — dedicated inference gateway with load balancing across GPU fleet
3. **DGX Spark** — when deployed, the 9B/27B models move to always-on inference appliance, freeing Blackwell GPUs for training

When bridged, a single API call to `router.swarmandbee.com` will be able to:
- Use CF AI for fast edge inference (current)
- Fall through to self-hosted 9B/27B for deeper analysis (future)
- Escalate to Together.ai 235B for maximum quality (future)

This creates a **cost cascade**: free edge → cheap self-hosted → expensive serverless, automatically routing based on query complexity.
