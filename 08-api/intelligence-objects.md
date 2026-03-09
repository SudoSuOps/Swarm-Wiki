# Intelligence Objects

Intelligence Objects are the correct term for finalized, verified, structured CRE data. Not datasets. Intelligence Objects.

SwarmRouter is the API Object Machine -- it processes raw public records into Intelligence Objects.

## Object ID Prefixes

| Prefix | Type | Description |
|--------|------|-------------|
| `pio_` | Infrastructure Object | Primary intelligence object (property, deal, market) |
| `evt_` | Event | Market event (see [Event Machine](event-machine.md)) |
| `mem_` | Memory Vector | Embedded memory for RAG retrieval |

## R2 Storage Paths

| Path Pattern | Contents |
|--------------|----------|
| `pio/{id}` | Intelligence objects |
| `pio/skills/{name}/{id}` | Skill execution outputs |
| `events/{id}` | Event payloads |

## Data Sources

Intelligence Objects are assembled from multiple public and commercial data sources:

| Source | Data Type | Access |
|--------|-----------|--------|
| SEC EDGAR | REIT 10-K/10-Q filings, material events | Free API |
| County Assessor/Recorder | Property ownership, tax records, deed transfers | County-specific APIs |
| ATTOM API | Property data, tax assessments, AVM, deed history | Commercial ($500/mo) |
| CompStak | Lease comps, sale comps (verified by brokers) | Commercial |
| Regrid | Parcel data, zoning, boundaries | Commercial |

## 50 State Area Experts

Each state has a dedicated CRE expert accessible via `POST /cook/{STATE}`. State experts include:

- **Tax rates**: Property tax rates, assessment ratios, millage rates
- **Market heat**: Hot/warm/cool/cold classification per submarket
- **Population data**: Growth rates, migration trends, employment stats
- **Regulatory context**: Zoning frameworks, entitlement processes, environmental requirements
- **Submarket definitions**: Named submarkets with geographic boundaries

Example:
```bash
# Cook with Texas expert
curl -X POST https://api.router.swarmandbee.com/cook/TX \
  -H "Authorization: Bearer sb_live_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"address": "4500 Frisco St, Dallas, TX 75201", "asset_type": "industrial"}'
```

## Object Lifecycle

```
Raw Input (EDGAR, assessor, API)
  → Normalize (field mapping, unit conversion)
  → Enrich (cross-reference sources, fill gaps)
  → Validate (deterministic gates: schema, bounds, consistency)
  → Embed (BGE-Base → 768-dim vector)
  → Seal (optional HCS hash for provenance)
  → Store (R2 object + D1 metadata + Vectorize embedding)
```

## Intelligence Object Schema

A typical PIO contains:

```json
{
  "id": "pio_abc123def456",
  "type": "property",
  "asset_class": "industrial",
  "asset_type": "cold_storage",
  "address": {
    "street": "4500 Frisco St",
    "city": "Dallas",
    "state": "TX",
    "zip": "75201",
    "county": "Dallas",
    "submarket": "North Dallas"
  },
  "metrics": {
    "sf": 125000,
    "acres": 8.2,
    "year_built": 2019,
    "clear_height": 36,
    "occupancy": 0.95,
    "noi": 1850000,
    "cap_rate": 0.055,
    "price_psf": 245
  },
  "ownership": {
    "entity": "Prologis Inc",
    "entity_id": "ent_prologis_001",
    "acquired": "2021-03-15",
    "acquisition_price": 28500000
  },
  "events": ["evt_001", "evt_002"],
  "sources": ["edgar", "attom", "county_assessor"],
  "created_at": "2026-03-01T12:00:00Z",
  "updated_at": "2026-03-09T08:30:00Z",
  "hcs_seal": "0.0.10291838:1234567890"
}
```

## The Product Vision

Intelligence Objects are the product -- the new CoStar, but API-first and agent-native. No human breaks in the pipeline. Raw public records go in, verified structured intelligence comes out. Every object is:

1. **Multi-sourced**: Cross-referenced across 3+ data providers
2. **Verified**: Passed through deterministic quality gates
3. **Embedded**: Searchable via semantic similarity
4. **Provenance-tracked**: Optional Hedera HCS seal for immutable audit trail
5. **Agent-consumable**: JSON-native, schema-validated, ready for LLM context injection
