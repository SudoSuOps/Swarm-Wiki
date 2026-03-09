# Orchestrator

The orchestrator (`curator/orchestrator.py`) manages the state machine and coordinates the planner, assembler, validator, and publisher components that surround the middleware chain.

## State Machine

Every signal/cook order moves through four states:

```
Pending -> Cooking -> Ready -> Published
```

| State | Meaning |
|-------|---------|
| Pending | Signal ingested, awaiting classification and analysis |
| Cooking | Factory is generating pairs from the cook order |
| Ready | Pairs generated and validated, awaiting publish |
| Published | Pushed to R2, Supabase, and/or HCS. Terminal state. |

State transitions are logged to `.state/fleet_runs.jsonl` with timestamps, enabling throughput analysis and bottleneck detection.

## Planner

`curator/planner.py`

The planner reads signal heat from the VelocityTracker and generates prioritized cook orders.

**Input**: VelocityTracker heat_map() -- per-topic velocity, direction, and acceleration.

**Logic**:
- Accelerating topics get higher `market_heat` scores
- Higher market_heat = earlier scheduling in the cook queue
- Topics with existing dataset gaps (low pair count for a vertical/task type) get a boost
- Decelerating topics are deprioritized but not dropped

**Output**: Ordered list of cook orders, each specifying vertical, task type, asset type, market, target pair count, and priority.

## Assembler

`curator/assembler.py`

The assembler builds the messages array (system/user/assistant) for each training pair. It applies:

- Vertical-specific system prompts from `curator/verticals.yaml`
- Task-type-specific user prompt templates
- Skills context injection via `skills_prompt_section()` when the task involves skill execution
- Trajectory formatting for multi-step reasoning pairs

## Validator

`curator/validator.py`

Three-layer validation runs on every assembled pair:

1. **Schema validation** -- Messages array structure, required fields, role sequence (system/user/assistant)
2. **Logic validation** -- Internal consistency checks (e.g., NOI calculation matches stated cap rate and value)
3. **Domain-specific validation** -- Vertical-aware checks (e.g., CRE pairs must have valid asset_type, medical pairs must reference real drug names)

Pairs that fail any layer are rejected with the failure reason logged.

## Publisher

`curator/publisher.py`

Publishes validated pairs to their destinations:

- **R2**: Per-vertical bucket upload as JSONL shards with manifest files
- **Supabase**: Streaming insert for queryable access
- **HCS**: Merkle tree root hash published to Hedera for provenance seal

The publisher generates manifest files for each R2 upload containing shard names, pair counts, and checksums. This enables downstream consumers to verify shard integrity without downloading full files.

## Orchestrator Loop

The orchestrator runs a continuous loop:

```
1. Planner generates cook orders from signal heat
2. Cook orders enter Pending state
3. Middleware chain processes: Classification -> Analysis -> Strategy -> QualityGate
4. Approved orders transition to Cooking, factory generates pairs
5. Assembler formats pairs, Validator checks quality
6. Passing pairs transition to Ready
7. Publisher pushes to R2/Supabase/HCS
8. Pairs transition to Published
9. Loop back to step 1
```

In `--dry-run` mode, the orchestrator runs steps 1-3 and logs what would happen without generating pairs or publishing.
