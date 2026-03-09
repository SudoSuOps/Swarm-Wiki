# Signal Integrations

Six bridges in `signal/integrations/` route scored signals to downstream systems. Every signal passes through the EntityScorer and VelocityTracker before reaching any bridge.

## Bridge Inventory

### 1. event_bridge.py -- Event Machine
Pushes structured events to the CRE Event Machine:
- **Destination**: D1 database (`swarm-intelligence-db`) + Cloudflare Vectorize index (`swarm-memory`)
- **Format**: 22 event types across 5 categories (deal, supply, ownership, macro, tenant)
- **Entity resolution**: Extracted entities are linked to canonical records in the `entities` table
- **Vectorize**: 768-dimension BGE-Base embeddings for semantic search via `/memory/search`

### 2. memory_bridge.py -- Semantic Memory
Pushes signals to pgvector semantic memory:
- **Embeddings**: 768-dimension BGE-Base
- **Purpose**: Long-term semantic retrieval for agent context. Signals become retrievable by meaning, not just keywords.
- **Distinct from event_bridge**: Event bridge stores structured events in D1. Memory bridge stores unstructured signal content in pgvector for broader semantic search.

### 3. curator_bridge.py -- Cook Orders
Writes JSONL cook orders for the curator planner:
- **Output**: Cook order files consumed by `curator/planner.py`
- **Content**: Topic, vertical, priority, suggested task types, market_heat score
- **Trigger**: P1 and P2 signals generate cook orders. P3 signals are archived only.
- **Effect**: Accelerating real-world topics automatically produce training data via the factory pipeline.

### 4. r2_archive.py -- Daily Archive
Archives all signals to R2 buckets:
- **Frequency**: Daily batch push
- **Format**: JSONL with full signal metadata (source, timestamp, entities, scores)
- **Purpose**: Complete signal history for retroactive analysis and model training

### 5. discord_bridge.py -- Discord Alerts
Posts P1-P3 signals to the `#swarm-signal` Discord channel:
- **Method**: Webhook POST
- **Format**: Formatted embed with source, entities, confidence score, and priority level
- **Deployed on**: zima-edge-1 (runs as part of the swarmsignal.service systemd unit)
- **Filtering**: All priority levels are posted, with P1 getting prominent formatting

### 6. hedera_bridge.py -- HCS Seal
Publishes signal hashes to Hedera Consensus Service for immutable timestamping:
- **Topic**: HCS Event topic `0.0.10291836` (mainnet)
- **Payload**: SHA-256 hash of the signal content
- **Purpose**: Provenance -- proves a signal existed at a specific time. Enables downstream verification that intelligence objects trace back to real signals.
- **Integration**: Uses same bridge infrastructure as the factory publish step (`data/factory/hedera_bridge.py`)

## Bridge Execution

All bridges run after scoring. The SignalEngine dispatches to bridges in parallel -- a slow R2 upload does not block the Discord alert or cook order generation.

Bridges are fault-tolerant: if one bridge fails (e.g., R2 timeout), the signal is still delivered to all other bridges. Failed bridge deliveries are logged and retried on the next cycle.
