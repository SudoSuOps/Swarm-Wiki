# Cloudflare Workers

**Account ID**: `6abec5e82728df0610a98be9364918e4`

## Deployed Workers (2)

### 1. swarm-router (Edge Intelligence)

| Property | Value |
|----------|-------|
| Config | `swarmrouter/worker/wrangler.toml` |
| Main | `src/index.js` |
| Compat date | 2024-09-25 |

**Routes**:
- `router.swarmandbee.com/*`
- `api.router.swarmandbee.com/*`
- `router.swarmandbee.ai/*`
- `api.router.swarmandbee.ai/*`

**Bindings**:

| Type | Binding | Resource |
|------|---------|----------|
| AI | `AI` | `swarm-gateway` — DeepSeek-R1-32B (edge), Llama-3.2-3B (fallback) |
| R2 | `INTELLIGENCE` | `sb-intelligence` |
| R2 | `MEDICAL` | `sb-medical` |
| R2 | `AVIATION` | `sb-aviation` |
| R2 | `CRE` | `sb-cre` |
| R2 | `CORE` | `sb-core` |

**Endpoints** (40+):
- `/pio/*` — Intelligence Object CRUD, search, feed
- `/cook/*` — Edge inference (batch, EDGAR, market)
- `/skill/*` — 28 skills (19 CRE + 9 medical)
- `/events/*` — Event machine (22 types)
- `/entities/*` — Entity management, timeline
- `/memory/*` — Semantic search (pgvector)
- `/wallet/*` — Credit metering
- `/router/*` — Decision logging

**Backend**: Supabase PostgreSQL (10 tables + pgvector 768-dim)

### 2. swarm-api (Data Commerce)

| Property | Value |
|----------|-------|
| Config | `swarmrouter/swarm-api-worker/wrangler.toml` |
| Main | `src/index.js` |
| Compat date | 2024-09-25 |

**Routes**:
- `api.swarmandbee.com/*`
- `swarmandbee.com/api/*`
- `api.swarmandbee.ai/*`
- `swarmandbee.ai/api/*`

**Bindings**:

| Type | Binding | Resource |
|------|---------|----------|
| R2 | `OPS_BUCKET` | `swarm-ops` |
| R2 | `MEDICAL_BUCKET` | `sb-medical` |
| R2 | `AVIATION_BUCKET` | `sb-aviation` |
| R2 | `CRE_BUCKET` | `sb-cre` |
| R2 | `CORE_BUCKET` | `sb-core` |

**Secrets** (via `wrangler secret put`):
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `DISCORD_WEBHOOK_URL`
- `DISCORD_DATA_WEBHOOK_URL`
- `TOGETHER_API_KEY`

**Endpoints**:
- `POST /api/contact` — Contact form (-> Rocket.Chat)
- `POST /api/loi` — Letter of Intent builder
- `POST /api/rfp` — RFP submission
- `POST /api/ask-med` — Medical inference
- `POST /api/data/checkout` — Stripe checkout
- `POST /api/data/subscribe` — Stripe subscription
- `POST /api/data/webhook` — Stripe webhooks
- `GET /api/data/catalog` — Browse data catalog
- `GET /api/data/count` — Live pair counts
- `GET /api/data/sample` — Free samples
- `GET /api/data/pull` — API key gated downloads
- `GET /api/health` — Health check

### 3. CreditSniper (Pages Functions)

| Property | Value |
|----------|-------|
| Config | `creditsniper-xyz/wrangler.toml` |
| Platform | Cloudflare Pages |
| Domain | `creditsniper.xyz` |

**R2 Binding**: `CREDIT_VAULT` -> `creditsniper-vault`

**Functions**:
- `POST /api/contact` — Contact form -> Rocket.Chat webhook
- `GET /api/download` — Stripe session verification + R2 zip delivery

## Deploy Commands

```bash
# Deploy router worker
cd swarmrouter/worker && npx wrangler deploy

# Deploy API worker
cd swarmrouter/swarm-api-worker && npx wrangler deploy

# Tail logs
npx wrangler tail

# Set secrets
npx wrangler secret put STRIPE_SECRET_KEY
```

## Database (Supabase — replaces D1)

**Project**: `gizwfmgowyfadmvjjitb.supabase.co`

| Resource | Details |
|----------|---------|
| PostgreSQL | 10 tables (events, entities, memory_index, wallets, etc.) |
| pgvector | 768-dim cosine (BGE-Base-EN-v1.5 embeddings) |
| RPCs | 10 functions (match_memory, get_event_stats, etc.) |
| Auth | Anon key (read) + Service Role (write) |

Note: D1 and Vectorize are NOT in current stack — migrated to Supabase.
