# API Endpoints

Full endpoint reference for router.swarmandbee.com and api.router.swarmandbee.com.

## Intelligence Objects

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/pio/{id}` | Retrieve a single intelligence object by ID | Free |
| GET | `/pio/search` | Search intelligence objects by query, asset type, location | Free |
| GET | `/pio/feed` | Paginated feed of recent intelligence objects | Free |
| POST | `/cook` | Generate a new intelligence object from raw inputs | Metered |
| POST | `/cook/batch` | Batch cook multiple objects | Metered |
| POST | `/cook/edgar` | Cook intelligence objects from SEC EDGAR filings | Metered |

## Skills

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/skill/{name}` | Execute a skill with JSON input | Metered |
| GET | `/skills` | List all available skills with metadata | Free |
| GET | `/skill/{name}/spec` | Return the SKILL.md spec for a skill | Free |
| GET | `/skill/{name}/mock` | Return mock output (no model call) | Free |
| GET | `/skill/{name}/test` | Run built-in test suite for a skill | Free |
| GET | `/skill/{name}/eval` | Run evaluation against reference outputs | Free |
| GET | `/skill/{name}/fail` | Return example failure modes | Free |

## Events

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/events/query` | Query events by type, category, date range, entity | Free |
| GET | `/events/stats/db` | D1 database statistics (event counts, entity counts) | Free |
| GET | `/entities` | List known entities with event counts | Free |
| GET | `/entities/{id}/timeline` | Event timeline for a specific entity | Free |
| POST | `/events` | Submit a new event (internal use) | Metered |

## Memory (Vectorize)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/memory/search` | Semantic search over embedded memory vectors | Free |
| GET | `/memory/context` | Retrieve contextual memory for a query (RAG) | Free |

## Router

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/route` | Route a query to the appropriate skill/model | Metered |
| GET | `/health` | Health check (returns 200 if alive) | Free |
| GET | `/stats` | Router decision statistics | Free |

## State Experts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/cook/{STATE}` | Cook with a state-specific CRE expert (50 states) | Metered |

Each state expert includes:
- State-specific tax rates and assessment methods
- Market heat tier classification (hot/warm/cool/cold)
- Population and economic data
- Local regulatory considerations
- Submarket boundaries and naming conventions

Example: `POST /cook/TX` invokes the Texas CRE expert.

## Router Logging (swarmrails:8080)

The FastAPI proxy on swarmrails wraps the Ollama swarmrouter-v2 model and logs every decision.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/route` | Route a query (logs to JSONL) |
| GET | `/health` | Health check |
| GET | `/stats` | Routing statistics |

Log path: `/data2/swarm_router_train/logs/router_decisions_YYYY-MM-DD.jsonl`

Each log record includes the full `messages` array (training-ready for v3 router). Confidence formula:

| Component | Weight |
|-----------|--------|
| JSON validity | 0.30 |
| Schema completeness | 0.25 |
| Enum validity | 0.25 |
| Logprob score | 0.20 |

Promotable threshold: confidence >= 0.80

## Common Request Pattern

```bash
# Skill execution
curl -X POST https://api.router.swarmandbee.com/skill/comp_analyzer \
  -H "Authorization: Bearer sb_live_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"property_address": "123 Industrial Blvd", "asset_type": "warehouse"}'

# Intelligence object search
curl "https://router.swarmandbee.com/pio/search?q=cold+storage+dallas&type=industrial"

# Event query
curl "https://router.swarmandbee.com/events/query?type=just_sold&days=30"

# Memory search
curl -X POST https://router.swarmandbee.com/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "industrial vacancy trends in Phoenix"}'
```

## Error Responses

All endpoints return consistent error JSON:

```json
{
  "error": "description of what went wrong",
  "code": 400,
  "detail": "optional additional context"
}
```

| Code | Meaning |
|------|---------|
| 400 | Bad request (missing/invalid parameters) |
| 401 | Missing or invalid API key |
| 402 | Insufficient credits |
| 404 | Resource not found |
| 429 | Rate limited |
| 500 | Internal server error |
