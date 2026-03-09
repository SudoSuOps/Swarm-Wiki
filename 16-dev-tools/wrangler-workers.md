# Cloudflare Workers & Wrangler

## Workers

### SwarmRouter Edge Worker

| Property | Value |
|----------|-------|
| Path | `swarmrouter/worker/` |
| Main | `src/index.js` |
| Account | `6abec5e82728df0610a98be9364918e4` |
| Routes | `router.swarmandbee.com/*`, `api.router.swarmandbee.com/*`, `router.swarmandbee.ai/*`, `api.router.swarmandbee.ai/*` |

**Bindings**:
- AI: Qwen3-30B-A3B-FP8 (primary), Llama-3.2-3B (fallback)
- R2: INTELLIGENCE, MEDICAL, AVIATION, CRE, CORE
- D1: swarm-intelligence-db
- Vectorize: swarm-memory (768-dim cosine BGE-Base)

**Deploy**:
```bash
cd worker
npx wrangler deploy
npx wrangler tail    # Live logs
npx wrangler dev     # Local development
```

### Swarm API Worker

| Property | Value |
|----------|-------|
| Path | `swarmrouter/swarm-api-worker/` |
| Main | `src/index.js` |
| Routes | `api.swarmandbee.com/*`, `swarmandbee.com/api/*`, `api.swarmandbee.ai/*`, `swarmandbee.ai/api/*` |

**Bindings**:
- R2: OPS_BUCKET, MEDICAL_BUCKET, AVIATION_BUCKET, CRE_BUCKET, CORE_BUCKET
- Supabase: `gizwfmgowyfadmvjjitb.supabase.co`
- Stripe: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET

**Secrets** (set via `wrangler secret put`):
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `SUPABASE_SERVICE_ROLE_KEY`
- `DISCORD_DATA_WEBHOOK_URL`

**Deploy**:
```bash
cd swarm-api-worker
npm run deploy
npm run tail
```

## Wrangler Configuration

Use `npx wrangler` (not global install). Set `CLOUDFLARE_ACCOUNT_ID` env var.

```bash
# Deploy
npx wrangler deploy

# Local dev
npx wrangler dev

# Tail production logs
npx wrangler tail

# Set secrets
npx wrangler secret put STRIPE_SECRET_KEY

# List R2 buckets
npx wrangler r2 bucket list
```

No `--remote` flag needed in newer wrangler versions.

## R2 Bucket Bindings

| Binding | Bucket | Worker |
|---------|--------|--------|
| INTELLIGENCE | sb-intelligence | edge |
| MEDICAL / MEDICAL_BUCKET | sb-medical | both |
| AVIATION / AVIATION_BUCKET | sb-aviation | both |
| CRE / CRE_BUCKET | sb-cre | both |
| CORE / CORE_BUCKET | sb-core | both |
| OPS_BUCKET | swarm-ops | API |
