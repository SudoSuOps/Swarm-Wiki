# Developer Tools & CLI

All CLI entry points, package management, environment setup, and development workflows.

## CLI Entry Points

| CLI | Entry | Purpose |
|-----|-------|---------|
| `python3 -m curator` | `curator/cli.py` | Pipeline orchestration (plan, cook, assemble, validate, publish, fleet, skills) |
| `python3 -m signal` | `signal/cli.py` | Signal ingestion (collect, run, status, velocity, drop, edge-status) |
| `python3 -m data.factory` | `data/factory/cli.py` | Quality gates, cooking, promotion, R2 push, factory dashboard |
| `python -m cli.reconcile` | `swarm-vault-engine/` | Dataset reconciliation, dedup, Merkle trees, R2 sync |
| `npx wrangler deploy` | `worker/wrangler.toml` | Deploy Cloudflare Workers (edge API) |
| `node index.js` | `hedera-swarmfoundry/` | Hedera: seal, migrate, verify, inventory, agents |

## Package Management

### Python (uv)

```bash
# Lightweight install (API, CLI, dev tools)
uv sync

# Full ML stack (GPU rigs only)
uv sync --group train
```

| Tool | Version | Notes |
|------|---------|-------|
| uv | 0.10.6 | Installed on local + whale + swarmrails |
| Python | 3.13 (local), 3.12.3 (whale), 3.11+ (swarmrails) | PEP 668 — always use venv |

### Node.js (npm)

```bash
cd worker && npm install          # Edge worker
cd swarm-api-worker && npm install  # API worker
cd hedera-swarmfoundry && npm install  # Hedera
cd swarm-agents && npm install    # Agent suite
```

Node 18+ required.

## Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `TOGETHER_API_KEY` | swarmrails, whale | Cook pipeline API calls |
| `CUDA_DEVICE_ORDER=PCI_BUS_ID` | swarmrails | Consistent GPU numbering |
| `CUDA_VISIBLE_DEVICES` | swarmrails | Target specific GPU for training |
| `SUPABASE_SERVICE_ROLE_KEY` | swarmrails, whale | Server-side Supabase admin |
| `STRIPE_SECRET_KEY` | swarm-api-worker | Payment processing |
| `STRIPE_WEBHOOK_SECRET` | swarm-api-worker | Webhook signature verification |
| `CLOUDFLARE_ACCOUNT_ID` | local | Wrangler deploys |
| `CF_API_TOKEN` | local | R2 operations |
| `PINATA_JWT` | hedera-swarmfoundry | IPFS pinning |

## Section Index

- [CLI Reference](cli-reference.md) -- All commands with usage examples
- [Supabase Schema](supabase-schema.md) -- 13 tables, 10 RPCs, pgvector
- [Stripe Integration](stripe-integration.md) -- Payments, subscriptions, webhooks, quotas
- [Wrangler & Workers](wrangler-workers.md) -- Cloudflare Worker deployment
