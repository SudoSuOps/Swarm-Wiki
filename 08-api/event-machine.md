# CRE Event Machine

22 event types across 5 categories, stored in D1 with automatic entity extraction and vector embedding.

## Event Categories and Types

### Deal Events
| Type | Description |
|------|-------------|
| `just_listed` | Property newly listed for sale |
| `just_sold` | Transaction closed |
| `under_contract` | LOI accepted, in escrow |
| `refinanced` | Existing debt refinanced |
| `distressed` | Asset in distress (default, foreclosure risk) |

### Supply Events
| Type | Description |
|------|-------------|
| `new_construction` | New development or ground-up construction |
| `vacancy_trend` | Significant vacancy rate change in submarket |
| `market_shift` | Broad market condition change |

### Ownership Events
| Type | Description |
|------|-------------|
| `acquisition` | Entity acquired property or portfolio |
| `foreclosure` | Lender-initiated foreclosure |
| `bankruptcy` | Owner/operator filed bankruptcy |

### Macro Events
| Type | Description |
|------|-------------|
| `rate_change` | Interest rate change (Fed, SOFR, Treasury) |
| `fed_policy` | Federal Reserve policy announcement |
| `economic_data` | Economic indicator release (jobs, GDP, CPI) |

### Tenant Events
| Type | Description |
|------|-------------|
| `lease_signed` | New lease executed |
| `lease_ended` | Lease expiration or early termination |
| `default` | Tenant default on lease obligations |

## D1 Database: swarm-intelligence-db

10 tables:

| Table | Purpose |
|-------|---------|
| `events` | All event records with type, category, payload, timestamps |
| `entities` | Resolved entities (companies, properties, people) |
| `event_entities` | Many-to-many join between events and entities |
| `memory_index` | Vector memory references for RAG |
| `market_snapshots` | Point-in-time market condition snapshots |
| `wallets` | API key wallets and credit balances |
| `usage_log` | Metered API usage records |
| `topup_log` | Credit top-up history |
| `feedback` | User feedback on API responses |
| `router_decisions` | Logged routing decisions for training data |

## Vectorize Index: swarm-memory

| Property | Value |
|----------|-------|
| Name | `swarm-memory` |
| Dimensions | 768 |
| Metric | Cosine similarity |
| Embedding model | `@cf/baai/bge-base-en-v1.5` (BGE-Base) |

Every event is automatically embedded via `embedAndStore()` when ingested. This enables semantic search over the event corpus through `/memory/search`.

## Entity Extraction and Resolution

When an event is ingested:

1. The edge model extracts entity mentions (companies, properties, addresses, people)
2. Entities are resolved against the `entities` table (fuzzy matching on name + location)
3. New entities are created if no match found
4. `event_entities` join records link the event to all resolved entities
5. Entity timelines are queryable via `/entities/{id}/timeline`

## EDGAR Pump

The `edgar_pump.py` script ingests SEC EDGAR filings from 15 REIT tickers and converts them into structured events.

| Property | Value |
|----------|-------|
| Script | `edgar_pump.py` |
| Tickers | 15 REITs |
| Events pumped | 34 (live as of launch) |
| Filing types | 10-K, 10-Q |
| Output | Events in D1 + R2 + Vectorize |

The pump parses EDGAR XML/HTML filings, extracts material events (acquisitions, dispositions, lease activity, debt changes), and publishes them through the standard event ingestion pipeline.

## API Endpoints

```bash
# Query events by type and date range
curl "https://router.swarmandbee.com/events/query?type=just_sold&days=30"

# Database statistics
curl "https://router.swarmandbee.com/events/stats/db"

# List entities
curl "https://router.swarmandbee.com/entities"

# Entity timeline
curl "https://router.swarmandbee.com/entities/ent_abc123/timeline"

# Semantic memory search
curl -X POST https://router.swarmandbee.com/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Prologis acquisition activity 2025"}'

# Contextual memory retrieval (RAG)
curl "https://router.swarmandbee.com/memory/context?q=industrial+vacancy+phoenix"
```

## Event Ingestion Flow

```
Source (EDGAR, signal, manual)
  → Parse & normalize
  → Entity extraction (edge AI)
  → Entity resolution (D1 lookup)
  → Store event (D1 events table)
  → Link entities (D1 event_entities)
  → Embed text (BGE-Base → Vectorize)
  → Store object (R2)
```
