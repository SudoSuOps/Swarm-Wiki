# Stripe Payment Integration

Payment processing for SwarmForge data packs, SwarmCurator subscriptions, and API access.

## Architecture

```
Customer → swarmandbee.ai checkout → Stripe Checkout Session
  → Webhook (checkout.session.completed) → Generate sk_swarm_ API key
  → Store in R2 (keys/api-keys.json)
  → Discord notification
  → Customer uses key on /api/data/pull (quota-enforced)
```

## Pricing Tiers

### SwarmForge Data Packs (One-Time)

| Tier | Pairs | Price | Mode |
|------|-------|-------|------|
| finetune | 1,000 | $99 | payment |
| pro | 50,000 | $499 | payment |
| custom | 100,000 | $999 | payment |
| enterprise | 250,000 | $1,995 | payment |

### SwarmCurator Subscriptions (Monthly)

| Tier | Pairs/mo | Price | Product |
|------|----------|-------|---------|
| curator | 20,000 | $20/mo | SwarmCurator single vertical |
| starter | 250,000 | $49/mo | Full access, 5 streams |
| pro | 50,000 | $299/mo | CRE Moat with API credits |

### Dataset Concierge (Enterprise)

| Tier | Pairs | Price |
|------|-------|-------|
| starter | 1,000 | $99 |
| professional | 10,000 | $499 |
| volume | 50,000 | $1,999 |
| enterprise | full vault | Custom LOI |
| monthly | unlimited | $4,999/mo |

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/data/checkout` | POST | Create Stripe checkout session (data packs) |
| `/api/data/subscribe` | POST | Create subscription checkout |
| `/api/data/activate` | GET | Activate API key after payment |
| `/api/data/webhook` | POST | Stripe webhook handler (REVENUE CRITICAL) |
| `/api/data/pull` | GET | Pull training pairs (API key gated, quota enforced) |
| `/api/data/catalog` | GET | Browse data catalog with specialty counts |
| `/api/data/count` | GET | Live pair counts per vertical/specialty |
| `/api/data/sample` | GET | Free sample pairs |
| `/api/data/order` | POST | CRE dataset cook orders from chat |

## API Key System

**Key format**: `sk_swarm_` + 48 hex characters

**Key record structure**:
```json
{
  "key": "sk_swarm_...",
  "email": "customer@example.com",
  "tier": "pro",
  "stripe_session": "cs_...",
  "stripe_customer_id": "cus_...",
  "stripe_subscription_id": "sub_...",
  "amount_paid": 2999,
  "currency": "usd",
  "quota": 50000,
  "pairs_pulled": 1234,
  "status": "active",
  "origin": "hq",
  "created_at": "ISO timestamp",
  "last_renewal": "ISO timestamp"
}
```

**Quota enforcement**: Checked on every `/api/data/pull`. Returns 403 when exhausted. Resets on subscription renewal.

## Webhook Events

| Event | Action |
|-------|--------|
| `checkout.session.completed` | Generate API key with tier-based quota |
| `invoice.paid` | Reset `pairs_pulled` counter (subscription renewal) |
| `customer.subscription.deleted` | Mark API key as cancelled |

Webhook uses HMAC-SHA256 signature verification. Idempotent operations prevent duplicate key generation. Discord notification on every activation/renewal/cancellation.

## Revenue Splits (Billing Ledger)

| Role | Split |
|------|-------|
| Specialist | 70% |
| Reasoning agent | 15% (if escalated) |
| Verifier | 10% (if verified) |
| Operator (S&B) | 5% platform fee |
| Broker | 10% commission (on sourced deals) |

Billing entries logged to Hedera HCS for audit trail. Can settle in HBAR/USDC.

## Storage

API keys stored in R2: `swarm-ops` bucket → `keys/api-keys.json`

## Stripe Configuration

No pre-created Product/Price IDs — line items created dynamically per checkout using `price_data` with inline `product_data`. Products/prices created on-the-fly.

**Redirect URLs**:
- Data pack success: `https://swarmandbee.com/data-success?session_id={ID}`
- Subscription success: `https://swarmandbee.ai/dashboard?checkout=success`
- Cancel: `https://swarmandbee.ai/curator#pricing`

## Environment Variables

| Variable | Location | Purpose |
|----------|----------|---------|
| `STRIPE_SECRET_KEY` | swarm-api-worker secrets | API authentication |
| `STRIPE_WEBHOOK_SECRET` | swarm-api-worker secrets | Webhook signature verification |
| `DISCORD_DATA_WEBHOOK_URL` | swarm-api-worker secrets | Activation notifications |

## Codebase Locations

| Component | Path |
|-----------|------|
| Checkout handler | `swarmrouter/swarm-api-worker/src/handlers/data/checkout.js` |
| Subscribe handler | `swarmrouter/swarm-api-worker/src/handlers/data/subscribe.js` |
| Webhook handler | `swarmrouter/swarm-api-worker/src/handlers/data/webhook.js` |
| Activate handler | `swarmrouter/swarm-api-worker/src/handlers/data/activate.js` |
| Pull handler (quota) | `swarmrouter/swarm-api-worker/src/handlers/data/pull.js` |
| Wrangler config | `swarmrouter/swarm-api-worker/wrangler.toml` |
| Billing ledger | `swarm-agents/ledger/billing.py` |
| Concierge tiers | `swarm-agents/workflows/dataset_concierge.py` |
