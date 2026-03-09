# Middleware Chain

The curator fleet processes signals through 7 ordered middlewares defined in `curator/middleware.py`. The chain is inspired by DeerFlow (ByteDance) but stripped of LangGraph, frontend, and LLM memory dependencies.

## Chain Order

```
1. SignalIngestion -> 2. Classification(2B) -> 3. Analysis(9B) -> 4. Strategy(27B) -> 5. QualityGate -> 6. StateUpdate -> 7. Dispatch
```

## Middleware Details

### 1. SignalIngestion
Ingests raw signals into FleetState. Normalizes input format, assigns tracking IDs, and validates that the signal has minimum required fields (source, content, timestamp).

### 2. Classification (2B)
Routes and categorizes signals via SwarmCurator-2B:
- Vertical assignment (CRE, Medical, Aviation, Drone, Signal)
- Task type classification within the vertical
- Priority assessment (P1/P2/P3)

**Fallback**: Rule-based classification using keyword matching and source heuristics. Runs when no 2B endpoint is available.

### 3. Analysis (9B)
Detailed signal analysis via SwarmCurator-9B:
- Entity extraction and enrichment
- Market context assessment
- Complexity scoring for task difficulty assignment
- Cook order parameter generation (asset type, market, analysis type)

**Fallback**: Template-based analysis using classification output and known entity databases.

### 4. Strategy (27B)
Strategic decisions via SwarmCurator-27B:
- Cross-vertical correlation (e.g., a Fed rate signal affects both CRE and medical facility financing)
- Priority escalation or de-escalation based on portfolio context
- Resource allocation (which factory pipeline, which GPU)
- Quality threshold adjustment based on current dataset gaps

**Fallback**: Static priority rules and default resource allocation.

### 5. QualityGate
6 deterministic quality checks -- no LLM calls. Same gates used by the dataset factory:
- json_valid, output_length, degenerate, dedup, concept_present, numeric_verify

See [quality-gates.md](../04-datasets/quality-gates.md) for gate details.

### 6. StateUpdate
Updates FleetState with processing results:
- State transitions: `Pending -> Cooking -> Ready -> Published`
- Logs decision chain to `.state/fleet_runs.jsonl` for future RL training
- Updates metrics (throughput, pass rates, error counts)

### 7. Dispatch
Emits outputs:
- Cook orders to the factory pipeline
- Published results to R2 buckets
- Alerts to Discord via webhook
- HCS seals for provenance

## FleetState and FleetContext

Two objects flow through the chain:

- **FleetState**: Mutable state of the current processing batch. Contains signals, classifications, analysis results, quality verdicts, and final outputs. Transitions through Pending/Cooking/Ready/Published.
- **FleetContext**: Immutable configuration. Holds LLM endpoints, R2 credentials, quality thresholds, and vertical configs.

## Performance

The chain runs in under 5ms when using algorithmic fallbacks (zero GPUs). With full LLM endpoints, latency depends on model inference time but the chain itself adds negligible overhead.

## Decision Logging

Every run appends a record to `.state/fleet_runs.jsonl` containing the full decision chain: which middleware ran LLM vs. fallback, classification results, quality gate pass/fail, and final disposition. This log is designed to be training data for future RL-based fleet optimization.
