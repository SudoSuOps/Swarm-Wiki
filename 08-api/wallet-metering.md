# Wallet & Metering

API metering for api.router.swarmandbee.com. Free tier uses router.swarmandbee.com (no key required).

## API Key Format

- Prefix: `sb_live_`
- Storage: SHA-256 hashed in D1 (plaintext never stored)
- Header: `Authorization: Bearer sb_live_xxxxx`

Example:
```
sb_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

## Credit Costs

| Operation | Credits | Description |
|-----------|---------|-------------|
| `cook` | 1 | Generate an intelligence object |
| `skill` | 2 | Execute any skill |
| `query` | 0.5 | Search/query operations |

## D1 Tables

### wallets

| Column | Type | Description |
|--------|------|-------------|
| wallet_id | TEXT PRIMARY KEY | Unique wallet identifier |
| api_key_hash | TEXT | SHA-256 hash of the API key |
| credits | REAL | Current credit balance |
| created_at | TEXT | ISO 8601 creation timestamp |
| updated_at | TEXT | ISO 8601 last update timestamp |

### usage_log

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| wallet_id | TEXT | Foreign key to wallets |
| operation | TEXT | Operation type (cook, skill, query) |
| credits_used | REAL | Credits consumed |
| endpoint | TEXT | Full endpoint path |
| timestamp | TEXT | ISO 8601 timestamp |
| metadata | TEXT | JSON string with request details |

### topup_log

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| wallet_id | TEXT | Foreign key to wallets |
| credits_added | REAL | Credits added |
| source | TEXT | Payment source or admin grant |
| timestamp | TEXT | ISO 8601 timestamp |

## Metering Flow

1. Request arrives at api.router.swarmandbee.com with `Authorization: Bearer sb_live_xxxxx`
2. Worker hashes the key with SHA-256
3. Looks up wallet by `api_key_hash` in D1 `wallets` table
4. Checks `credits >= cost` for the requested operation
5. If insufficient: returns 402 with `{"error": "insufficient credits", "balance": N}`
6. If sufficient: deducts credits, logs to `usage_log`, processes request
7. Response includes `X-Credits-Remaining` header

## Rate Limiting

Rate limits are enforced per API key:

| Tier | Requests/min | Concurrent |
|------|-------------|------------|
| Free (router.swarmandbee.com) | 60 | 5 |
| Metered (api.router.swarmandbee.com) | 300 | 20 |

## Usage Stats

```bash
# Check wallet balance (via Supabase RPC)
curl -X POST https://gizwfmgowyfadmvjjitb.supabase.co/rest/v1/rpc/get_balance \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -d '{"p_wallet_id": "wallet_123"}'
```

The D1 `usage_log` table stores every metered API call and is queryable via the `/events/stats/db` endpoint for aggregate reporting.
