# Signal Pipeline

The signal layer is the bottom of the Swarm stack. It continuously ingests, scores, and routes real-world signals into the curation and data factory layers.

## Architecture

```
11 Workers -> EntityScorer -> VelocityTracker -> 6 Integration Bridges
```

## Core Components

| Component | File | Role |
|-----------|------|------|
| SignalEngine | `signal/engine.py` | Top-level orchestrator. Runs workers on schedule, feeds scorer and velocity tracker, dispatches to bridges. |
| Workers | `signal/workers/` | 11 source-specific collectors (see [workers.md](workers.md)) |
| EntityScorer | `signal/scorer.py` | 4-weight confidence scoring + NER (see [scorer.md](scorer.md)) |
| VelocityTracker | `signal/velocity.py` | 7-day sliding window for trend detection (see [velocity.md](velocity.md)) |
| Integrations | `signal/integrations/` | 6 output bridges (see [integrations.md](integrations.md)) |

## Worker Lifecycle

Every worker follows the BaseWorker ABC contract:

1. **Fetch** -- Pull raw data from source (RSS, API, scrape)
2. **Normalize** -- Convert to standard signal schema
3. **Dedup** -- MD5 fingerprint against seen signals
4. **Score** -- EntityScorer assigns confidence + priority
5. **Emit** -- Signal enters VelocityTracker + integration bridges

## Scheduling Tiers

| Tier | Interval | Workers |
|------|----------|---------|
| FAST | 15 minutes | Hacker News, Reddit, CRE News, Webhook |
| MEDIUM | 1 hour | RSS, arXiv, EDGAR, GitHub, Trending |
| SLOW | 6 hours | FRED (Federal Reserve economic data) |

## Priority Levels

Signals are classified into three priority levels based on confidence score and velocity:

- **P1** -- High confidence + accelerating velocity. Immediate action: cook orders, Discord alerts, HCS seal.
- **P2** -- Moderate confidence or stable velocity. Queued for batch processing.
- **P3** -- Tracking only. Archived for trend analysis, no immediate action.

## CLI

```bash
python3 -m signal collect     # Run all workers once
python3 -m signal run          # Start daemon (scheduled collection)
python3 -m signal status       # Show worker health and last run times
```

## Edge Deployment

Signal collection runs on two edge nodes in addition to the main infrastructure. See [edge-deployment.md](edge-deployment.md) for hardware and service details.

## Related

- [workers.md](workers.md) -- All 11 signal workers
- [scorer.md](scorer.md) -- Confidence scoring formula
- [velocity.md](velocity.md) -- Trend detection and acceleration
- [integrations.md](integrations.md) -- 6 output bridges
- [edge-deployment.md](edge-deployment.md) -- Jetson and Zima edge nodes
