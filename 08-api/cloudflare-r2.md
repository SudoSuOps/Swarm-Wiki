# Cloudflare R2 Buckets

**Account ID**: `6abec5e82728df0610a98be9364918e4`

## Active Buckets (8)

| Bucket | Binding (Router) | Binding (API) | Contents | Pairs |
|--------|------------------|---------------|----------|-------|
| `sb-intelligence` | `INTELLIGENCE` | -- | Intelligence Objects (PIOs), address lookups | Variable |
| `sb-medical` | `MEDICAL` | `MEDICAL_BUCKET` | Medical training pairs (92 specialties) | ~432K |
| `sb-aviation` | `AVIATION` | `AVIATION_BUCKET` | Aviation training pairs (157 specialties) | ~45K |
| `sb-cre` | `CRE` | `CRE_BUCKET` | CRE training pairs (9 asset types, 8 task types) | ~643K |
| `sb-core` | `CORE` | `CORE_BUCKET` | Cross-vertical core (legal, medicine) | ~31K |
| `sb-drone` | -- | -- | Drone/UAV pairs (176 specialties) | ~6.8K |
| `sb-signal` | -- | -- | Daily signal archives (JSONL.gz) | Daily |
| `swarm-ops` | -- | `OPS_BUCKET` | API keys, configs, operations | Variable |

**Grand total**: 1,158,902+ training pairs across all verticals.

## Legacy/Archive Buckets (8)

| Bucket | Contents | Status |
|--------|----------|--------|
| `sb-judge` | Judge training data | ARCHIVED (franchise killed 2026-03-06) |
| `sb-judge-traces` | Agent trace data | ARCHIVED |
| `sb-models` | Model artifacts | ACTIVE |
| `block-0` | Genesis NFTs (303 objects) | LEGACY |
| `swarm-apedia-vault` | Legacy storage (8.72K objects) | LEGACY |
| `swarm-vault` | Multi-vertical legacy | LEGACY |
| `swarm-scripts` | Training scripts archive (23 objects) | LEGACY |
| `9b-block-0-phase2` | Judge phase 2 assembly | ARCHIVED |

## R2 Path Patterns

### Intelligence Objects (PIO)
```
pio/{object_id}                    # Main objects
pio/by-addr/{normalized_address}   # Address index
pio/skills/{name}/{id}             # Skill outputs
pio/events/{type}/{object_id}      # Event storage
```

### Signal Archives
```
signals/YYYY/MM/DD/bin_YYYY-MM-DD.jsonl.gz   # Daily compressed
```

### Training Pairs
```
pairs/shard_XXXX.jsonl             # 500-pair shards
metadata/manifest.json             # SHA256 checksums
metadata/specialties.json          # Specialty index
```

## Access Patterns

### JavaScript (Workers — R2 Binding API)
```javascript
// Put object
await env.CRE.put(key, jsonString);

// Get object
const obj = await env.CRE.get(key);
const data = await obj.json();

// List objects
const list = await env.CRE.list({ prefix: "pairs/", limit: 100 });
```

### Python (Factory — rclone/boto3)
```python
# Config in data/factory/config.py
R2_BUCKETS = {
    "cre": "sb-cre",
    "medical": "sb-medical",
    "aviation": "sb-aviation",
    "core": "sb-core",
    "drone": "sb-drone",
    "intelligence": "sb-intelligence",
}
```

Signal pipeline uses `rclone copyto` for daily archives to `sb-signal`.

## CreditSniper R2

Separate R2 bucket for credit dispute products:

| Bucket | Binding | Contents |
|--------|---------|----------|
| `creditsniper-vault` | `CREDIT_VAULT` | Product zip files (5 tiers) |

Products stored at `products/` prefix:
- `Credit_Sample_Pack.zip` — 5 platinum credit law QA pairs
- `Dispute_Letter_Pack.zip` — Dispute letter templates
- `Full_Credit_Vault.zip` — Complete credit dispute intelligence

## Cost Structure (API Credits)

| Operation | Credits | Description |
|-----------|---------|-------------|
| Cook (inference + R2) | 1 | Generate + store Intelligence Object |
| Skill execution (AI + R2) | 2 | Run skill + store output |
| Query (DB read) | 0.5 | Read from Supabase |
| Memory search (embed + pgvector) | 1 | Semantic similarity search |
| Event processing | 1 | Ingest + store event |
