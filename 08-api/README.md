# API Surface

The Swarm API runs as a monolithic Cloudflare Worker at two domains:

| Domain | Tier | Auth |
|--------|------|------|
| `router.swarmandbee.com` | Free | None |
| `api.router.swarmandbee.com` | Metered | `sb_live_` API key |

## Architecture

- **Worker**: `worker/src/index.js` -- single Cloudflare Worker handling all routes
- **Edge AI**: `@cf/qwen/qwen3-30b-a3b-fp8` (primary), `@cf/meta/llama-3.2-3b-instruct` (fallback)
- **Embeddings**: `@cf/baai/bge-base-en-v1.5` (768-dim, cosine similarity)
- **Database**: D1 `swarm-intelligence-db` (10 tables, see [Event Machine](event-machine.md))
- **Vector Store**: Vectorize `swarm-memory` (768 dims, cosine, BGE-Base)
- **Object Storage**: R2 buckets (see below)
- **Auth DB**: Supabase `gizwfmgowyfadmvjjitb.supabase.co` (18 tables, 10 RPCs)

## R2 Buckets

| Bucket | Contents | Objects |
|--------|----------|---------|
| `sb-intelligence` | Intelligence objects (PIOs) | Variable |
| `sb-medical` | Medical training pairs | ~432K |
| `sb-aviation` | Aviation training pairs | ~45K |
| `sb-cre` | CRE training pairs | ~643K |
| `sb-core` | Cross-vertical core pairs | ~31K |
| `sb-drone` | Drone/UAV pairs | ~6.8K |
| `sb-judge` | Judge training data | Variable |
| `sb-judge-traces` | Agent trace data | Variable |
| `sb-models` | Model artifacts | Variable |

## Endpoint Groups

| Group | Count | Description |
|-------|-------|-------------|
| [Intelligence Objects](intelligence-objects.md) | 6 | PIO CRUD, search, feed, cook |
| [Skills](../07-skills/README.md) | 7 | Skill execution, listing, specs, testing |
| [Events](event-machine.md) | 5 | Event query, stats, entities, timeline |
| [Memory](endpoints.md) | 2 | Semantic search, context retrieval |
| [Router](endpoints.md) | 3 | Route decisions, health, stats |
| [State Experts](endpoints.md) | 1 | 50 state-specific CRE experts |
| [Wallet/Metering](wallet-metering.md) | 4+ | Key management, credits, usage |

Total: 40+ endpoints.

## Deploy

```bash
cd worker && npx wrangler deploy
```

Cloudflare Account: `6abec5e82728df0610a98be9364918e4`

## Section Index

- [Endpoints](endpoints.md) -- Full endpoint reference
- [Wallet & Metering](wallet-metering.md) -- API key format, credit costs
- [Event Machine](event-machine.md) -- 22 event types, D1 schema, EDGAR pump
- [Intelligence Objects](intelligence-objects.md) -- PIO format, sources, state experts
