# Datasets

Grand total: **1,158,902+ training pairs** across 5 verticals.

| Vertical | Bucket | Pairs | Specialties |
|----------|--------|-------|-------------|
| CRE | sb-cre | 643,382 | 10 |
| Medical | sb-medical | 432,196 | 85 |
| Aviation | sb-aviation | 45,222 | 157 |
| Core | sb-core | 31,347 | 3 |
| Drone | sb-drone | 6,755 | 176 |

All data lives in Cloudflare R2 buckets with local master copies on disk.

## Local Master Files

| File | Path | Pairs |
|------|------|-------|
| MASTER_PLATINUM | `/home/swarm/swarmbin/MASTER_PLATINUM.jsonl` | 406,181 |
| MASTER_GOLD | `/home/swarm/swarmbin/MASTER_GOLD.jsonl` | 385,626 |

PLATINUM is the highest-quality tier -- every pair has passed deterministic gates and CoVe promotion. GOLD is one tier below (passed gates, not yet CoVe-promoted or scored below threshold).

## How Data Gets Made

1. **Factory** generates raw pairs via skeleton + LLM enrichment (see [factory-protocol.md](factory-protocol.md))
2. **Quality gates** reject malformed or degenerate output (see [quality-gates.md](quality-gates.md))
3. **CoVe promotion** rewrites and scores survivors (see [factory-protocol.md](factory-protocol.md))
4. **SafeStore** persists every pair across three tiers so nothing is ever lost (see [safestore.md](safestore.md))
5. **R2 publish** pushes finalized shards to per-vertical buckets (see [r2-buckets.md](r2-buckets.md))

## Pair Format

All pairs use the OpenAI messages schema. See [schemas.md](schemas.md) for field definitions, label taxonomies, and numeric conventions.

## Related

- [r2-buckets.md](r2-buckets.md) -- Per-bucket inventory and details
- [factory-protocol.md](factory-protocol.md) -- 10-stage production pipeline
- [quality-gates.md](quality-gates.md) -- 6 deterministic gates + CoVe thresholds
- [schemas.md](schemas.md) -- Pair format, labels, and conventions
- [safestore.md](safestore.md) -- Three-tier persistence architecture
