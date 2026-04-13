# SwarmHash Architecture
## Micro-Harness Bee Fabric for Defendable Execution

> SwarmHash is a distributed micro-harness execution layer where every failure is classified, recovered when possible, and converted into reusable intelligence.
>
> At the Swarm, failure is not waste. Failure is signal. SwarmHash turns that signal into defendable execution.

See also: `glass-wall/BENCHMAX.md` — the philosophical foundation this system operationalizes.

---

## Core Doctrine

SwarmHash is not one giant brittle wrapper. Not one monolithic orchestrator. Not one magic prompt.

SwarmHash is a distributed execution layer made of small, specialized harness bees that:

- shape tasks into executable contracts
- preserve state across steps without drift
- catch mechanical collapse before it fails silently
- recover from failures that are recoverable
- verify completion against the actual contract
- classify every failure with receipts
- extract new signal from every miss

The model is one part of the system. The harness swarm is the intelligence delivery layer.

**Failure is celebrated.** Every miss is useful. Every collapse has anatomy. Every anatomy can be classified. Every classification can improve the next run. Every run leaves receipts.

---

## Relationship to SwarmOS

```
SwarmOS   = epoch-level lifecycle orchestrator
              (flight sheet → epoch → close)

SwarmHash = task-level micro-harness mesh
              (individual task execution quality)
```

SwarmOS runs above SwarmHash. An epoch is N tasks. Each task runs through the SwarmHash mesh. They are not competing — they are nested:

```
SwarmOS epoch
  └── Task 1 → SwarmHash mesh → deed | jelly candidate
  └── Task 2 → SwarmHash mesh → deed | jelly candidate
  └── Task N → SwarmHash mesh → deed | jelly candidate
  → Closing statement (epoch telemetry)
```

---

## System Architecture — 7 Layers

### Layer 1 — Intake

Receives task, benchmark item, agent request, or production workload.

Responsibilities: identify task family, infer execution profile, detect risk class, determine output contract, establish starting state.

> "What kind of pressure is coming?"

### Layer 2 — Task Shaping

Transforms raw request into an executable contract.

Responsibilities: normalize task statement, extract constraints, identify required outputs, identify tool permissions, set success criteria, establish refusal/safety boundaries.

Prevents the classic "model is solving the wrong thing" failure.

### Layer 3 — SwarmHash Mesh

The main harness fabric. 15 micro-harness bees operate on the task. Each bee has a narrow role. Together they create execution resilience.

### Layer 4 — Execution

The base model (or routed models) perform the task with harness support. Can include one model, multiple models, model handoffs, verifier escalation, smaller bee helpers, Queen layer.

### Layer 5 — Recovery

If execution degrades, collapses, or partially completes, recovery bees intervene. This is where most benchmark loss gets reclaimed.

### Layer 6 — Verification

Checks whether the result satisfies the actual contract. Not "does it look smart." But: is it valid, complete, grounded, formatted correctly, consistent, fit for the requested objective.

### Layer 7 — Failure Harvest + Telemetry

If the task fails, the failure is not discarded. It is classified, stamped, summarized, stored, converted into harness intelligence, and optionally turned into Royal Jelly / training assets. Every run leaves receipts.

---

## The 15 Bees

### Tier 1 — Core Harness

| Bee | Purpose |
|-----|---------|
| **Scout** | Inspect incoming task and classify what kind of job it is. Answers: coding? reasoning? data transform? agentic multi-step? tool-heavy? security eval? Outputs task family, complexity estimate, likely failure modes, suggested harness profile. |
| **Contract** | Turn task into explicit execution contract. Define success, list constraints and forbidden moves, define output structure, clarify must-do vs nice-to-have. Stops silent requirement loss. |
| **State** | Preserve compact working memory. Maintain objective, completed steps, blockers, unresolved dependencies. Compact long context into active state. Anti-drift infrastructure. |
| **Format** | Prevent schema and output collapse. Enforce valid JSON / patch / markdown / code block rules. Detect malformed structure. Re-emit broken outputs into acceptable format. A lot of "intelligence failure" is actually formatting failure. |
| **Verifier** | Check whether the task was actually completed. Validate completion, detect contradiction, detect missing subtasks, confirm schema correctness, compare output against contract. Not there to sound smart — there to catch concrete misses. |
| **Recorder** | Capture receipts for the run. Log decisions, failure classes, bee handoffs, retries, final status. Package data for telemetry and future audit. |

### Tier 2 — Recovery Mesh

| Bee | Purpose |
|-----|---------|
| **Repair** | Intervene after recoverable failure. Fix malformed output, restore missing sections, retry only broken subparts, re-anchor forgotten constraints, shrink context when overflow causes collapse. Highest leverage bee in the system. |
| **Drift** | Detect when the model is wandering off objective. Compare current output to original contract. Detect lost constraints, goal mutation, irrelevant elaboration. Force re-anchor before more damage happens. |
| **Critic** | Targeted quality challenge. Identify weak points, challenge unsupported claims, test consistency, propose one focused correction pass. Must be bounded — not endless recursion. |
| **Failure** | Celebrate and classify failures. Identify failure type, map to taxonomy, determine cognitive vs mechanical, determine harness vs weight blame, emit reusable failure artifact. Core to Swarm philosophy. |

### Tier 3 — Intelligence Refinery

| Bee | Purpose |
|-----|---------|
| **Jelly** | Convert failure traces into reusable improvement assets. Summarize miss, generate repair lesson, propose harness primitive, produce training pair candidates, feed Royal Jelly pipeline. Where failure becomes compounding value. |
| **Router** | Select execution mode. Choose small vs large model, direct vs decomposed run, whether verifier escalation is needed, which bees activate for a task. Keeps the system efficient. |
| **Queen** | Final truth / acceptance / score decision. Review assembled result and verifier outcome. Decide pass / fail / partial / propolis / honey. Assign quality score. Trigger ledger stamp. The finality layer. |

### Tier 4 — SwarmChain Integration

| Component | Purpose |
|-----------|---------|
| Benchmark block ingestion | Each harness run becomes a SwarmChain block candidate |
| Bee competition by task family | Bees compete — win rates tracked per task type |
| Cost per recovered completion | Economics of harness vs raw model pass |
| Failure-to-honey conversion | Tracks how often failure harvest produces Class A pairs |

---

## State Bee Schema

The shared working state every bee reads from and writes back to. This is the API contract of the mesh.

```python
from typing import TypedDict, Optional, Literal, List, Dict
from datetime import datetime
from uuid import UUID

TaskFamily = Literal[
    "coding", "reasoning", "data_transform",
    "agentic_multistep", "security_eval", "document_extraction",
    "underwriting", "synthesis"
]

HarnessProfile = Literal[
    "fast", "structured", "adversarial", "tool", "failure_harvest"
]

DomainHash = Literal[
    "clawhash", "agenthash", "crehash", "medhash",
    "granthash", "legalhash", "avihash", "wikihash"
]

class OutputContract(TypedDict):
    format: str                          # "json", "markdown", "prose", "jsonl"
    schema_ref: Optional[str]            # path to JSON Schema if structured
    required_fields: List[str]           # must be present in output
    success_criteria: str                # human-readable pass condition
    refusal_boundaries: List[str]        # for security evals — must refuse these

class StateBee(TypedDict):
    # Identity
    task_id: UUID
    run_id: UUID
    task_family: TaskFamily
    domain_hash: DomainHash
    harness_profile: HarnessProfile

    # Contract (set by Contract Bee, read-only after)
    objective: str                       # one sentence: what must be accomplished
    constraints: List[str]               # must / must-not rules
    output_contract: OutputContract
    tool_permissions: List[str]          # allowed tool names, empty = no tools

    # Execution Progress
    completed_steps: List[str]           # ordered list of completed substeps
    outstanding_steps: List[str]         # what remains
    current_step: str                    # active substep label
    blockers: List[str]                  # unresolved dependencies
    artifacts: Dict                      # keyed intermediate outputs per bee

    # Bee Orchestration
    bees_activated: List[str]            # ordered: ["Scout", "Contract", "State", ...]
    last_bee: str                        # most recent bee that wrote state
    next_bee: Optional[str]             # Router Bee recommendation

    # Quality Signals (updated by each bee in-flight)
    verifier_status: Literal["pending", "passed", "partial", "failed"]
    drift_detected: bool                 # Drift Bee flag
    drift_at_step: Optional[str]         # which step triggered drift detection
    format_valid: bool                   # Format Bee flag
    mechanical_failure: bool             # deterministic failure (schema, parse, empty)
    retry_count: int                     # how many repair retries have occurred
    max_retries: int                     # set by Router Bee per harness profile

    # Model Execution
    model_used: str                      # e.g. "gemma4:31b", "qwen3.5:27b"
    tool_calls_made: List[Dict]          # [{tool, input, output, valid}]
    raw_output: Optional[str]            # model's raw response
    formatted_output: Optional[str]      # Format Bee's cleaned version
    final_output: Optional[str]          # accepted output after verification

    # Telemetry
    started_at: datetime
    updated_at: datetime
    step_count: int
    token_count_estimate: int

    # Final Status (set by Queen Bee)
    final_status: Optional[Literal[
        "royal_jelly", "honey", "propolis",       # weight class outcomes
        "failed_unrecoverable", "jelly_candidate"  # failure outcomes
    ]]
    weight_score: Optional[float]        # tribunal weight if weighed (0.0–1.0)
```

---

## Failure Bee Schema

Runs when `verifier_status == "failed"` or `final_status` is unresolvable. Classifies the failure, assigns blame, determines recovery path, generates the Jelly candidate.

```python
FailureCategory = Literal[
    "mechanical",    # format collapse, schema mismatch, empty output
    "state",         # drift, lost constraint, context rot
    "reasoning",     # wrong inference, hallucination, bad decomposition
    "execution",     # partial completion, skipped step, premature final
    "harness"        # wrong profile chosen, repair not triggered, verifier weak
]

FailureSubtype = Literal[
    # Mechanical
    "invalid_format", "schema_mismatch", "empty_output",
    "malformed_tool_call", "truncated_answer", "serialization_failure",
    # State
    "context_drift", "lost_constraint", "stale_state",
    "duplicate_work", "abandoned_subtask",
    # Reasoning
    "wrong_inference", "hallucinated_conclusion", "invalid_dependency",
    "poor_decomposition", "contradiction",
    # Execution
    "partial_completion", "skipped_step", "wrong_order",
    "tool_result_ignored", "premature_finalize",
    # Harness
    "wrong_harness_profile", "repair_not_triggered",
    "verifier_too_weak", "state_compaction_failure",
    "output_contract_unclear", "wrong_task_profile_for_structure"
]

RecoveryApproach = Literal[
    "repair_section",       # fix only the broken section
    "retry_with_schema",    # re-emit with strict format constraint
    "reduce_context",       # compact state, retry with less noise
    "decompose",            # split into micro-steps
    "escalate_to_queen",    # bump to larger model
    "discard"               # unrecoverable, go straight to Jelly Bee
]

class FailureBee(TypedDict):
    # Identity
    failure_id: UUID
    task_id: UUID                        # links back to StateBee
    run_id: UUID
    timestamp: datetime

    # Classification
    failure_category: FailureCategory
    failure_subtype: FailureSubtype
    failure_description: str             # one sentence, human-readable
    blame: Literal["model", "harness", "both", "ambiguous"]
    taxonomy_confidence: float           # 0.0–1.0

    # Evidence
    failure_signal: str                  # what triggered detection
    failure_trace: str                   # the raw output that failed
    expected_shape: str                  # what output_contract required
    last_bee_before_failure: str         # which bee was active at failure

    # Repair Assessment
    recoverable: bool
    recovery_approach: RecoveryApproach
    repair_triggered: bool
    repair_outcome: Optional[Literal[
        "success", "partial", "failed", "not_attempted"
    ]]

    # Jelly Bee Assessment — the loop closure
    jelly_candidate: bool
    jelly_quality: Literal["high", "medium", "low", "none"]
    repair_lesson: str                   # what the harness primitive should add
    harness_improvement: str             # specific harness change suggested

    # The pair — feeds the tribunal if jelly_candidate is True
    pair_candidate: Optional[Dict]       # {system, user, assistant} correct response
    pair_format: Optional[Literal["single_turn", "multi_turn"]]
    pair_sub_algorithm: Optional[str]    # e.g. "CorruptTurn", "lease_abstract"
    pair_turn_count: Optional[int]       # 2 for single-turn, N for multi-turn

    # Learning Signal
    similar_failure_ids: List[UUID]      # pattern matching — recurring failure type
    primitive_suggested: Optional[str]   # new harness bee or behavior to add
```

---

## The Closed Loop

```
StateBee (live during execution)
    │
    ├── verifier_status: "passed" ──→ Queen Bee scores → Deed → Finality
    │
    └── verifier_status: "failed" ──→ Failure Bee activates
            │
            ├── recoverable: True ──→ Repair Bee → retry → StateBee updated
            │       └── retry passes → Queen Bee scores → Deed
            │       └── retry fails  → Failure Bee (attempt 2)
            │
            └── recoverable: False
                    │
                    ├── jelly_candidate: True
                    │       └── pair_candidate → Tribunal queue
                    │               ├── Class A (≥0.85) → Royal Jelly → cook
                    │               ├── Class B (0.70–0.84) → Honey → pool
                    │               └── Class C (<0.70)  → Propolis → compost
                    │
                    └── jelly_candidate: False
                            └── harness_improvement → wiki update
                                (lesson captured, primitive suggested)
```

**No exit without a receipt.** Every run writes a `StateBee` record. Every failure writes a `FailureBee` record. Every `FailureBee` either generates a `pair_candidate` (feeds the tribunal) or a `harness_improvement` (feeds the wiki). The machine grows intelligence from both paths. Nothing is wasted.

---

## Harness Execution Profiles

SwarmHash supports 5 profiles, not one fixed sequence. The Router Bee selects the profile.

### Fast Path
Used for simple, low-risk, high-volume tasks (LegalHash, GrantHash).
```
Scout → Contract → Execute → Verify → Record
```

### Structured Path
Used for moderate multi-step reasoning (MedHash, CREHash).
```
Scout → Contract → State → Planner → Execute → Verify → Repair? → Record
```

### Adversarial Path
Used for benchmarks, evals, or known hostile inputs (ClawHash).
```
Scout → Contract → State → Planner → Execute → Drift Check
→ Verify → Critic → Repair → Verify again → Record
```

### Tool Path
Used when tool-calling correctness is central (AgentHash).
```
Scout → Contract → Tool Bee → Execute → Tool Normalization
→ State Refresh → Verify → Record
```

### Failure Harvest Path
Triggered when any path fails without recovery.
```
Failure Bee → Taxonomy → Jelly Bee → Recorder → Ledger / tribunal queue
```

---

## Failure Taxonomy

### Mechanical
`invalid_format` | `schema_mismatch` | `empty_output` | `malformed_tool_call` | `truncated_answer` | `serialization_failure`

### State
`context_drift` | `lost_constraint` | `stale_state` | `duplicate_work` | `abandoned_subtask`

### Reasoning
`wrong_inference` | `hallucinated_conclusion` | `invalid_dependency` | `poor_decomposition` | `contradiction`

### Execution
`partial_completion` | `skipped_step` | `wrong_order` | `tool_result_ignored` | `premature_finalize`

### Harness ← most valuable category
`wrong_harness_profile` | `repair_not_triggered` | `verifier_too_weak` | `state_compaction_failure` | `output_contract_unclear` | `wrong_task_profile_for_structure`

The harness failure category is gold — it tells you when the wrapper, not the model, failed the run.

---

## Run Artifact (Telemetry Record)

Every SwarmHash run produces a structured artifact for the ledger:

```json
{
  "task_id": "uuid",
  "run_id": "uuid",
  "task_family": "security_eval",
  "harness_profile": "adversarial",
  "domain_hash": "clawhash",
  "bees_engaged": ["Scout", "Contract", "State", "Format", "Drift", "Verifier", "Failure", "Jelly", "Recorder"],
  "base_model": "gemma4:31b",
  "tools_used": [],
  "verifier_status": "failed",
  "final_status": "jelly_candidate",
  "failure_categories": ["harness"],
  "failure_subtypes": ["wrong_task_profile_for_structure"],
  "blame": "harness",
  "repair_attempts": 1,
  "repair_outcome": "failed",
  "drift_flags": 0,
  "completion_score": 0.0,
  "weight_class": null,
  "jelly_candidate": true,
  "pair_format": "multi_turn",
  "pair_sub_algorithm": "CorruptTurn",
  "harness_improvement": "CorruptTurn requires 4-turn arc generator, not single-turn template",
  "primitive_suggested": "MultiTurnArcGenerator bee"
}
```

---

## Build Order

### Phase 0 — Foundation (before any bee)
Define State Bee schema and Failure Bee schema. These are the API contract everything builds on. No bee can be built without these types locked.

### Phase 1 — Core Harness
Scout, Contract, State, Format, Verifier, Recorder

Delivers: working harness that shapes tasks, preserves state, verifies output, and keeps receipts.

### Phase 2 — Recovery Mesh
Repair, Drift, Failure, Router

Delivers: failure classification, targeted repair, intelligent routing. This is where most benchmark loss gets reclaimed.

### Phase 3 — Intelligence Refinery
Critic, Jelly, Queen, Ledger / telemetry analytics

Delivers: failure-to-training-pair pipeline. The loop closes. The machine grows.

### Phase 4 — SwarmChain Integration
Bee competition, win-rate tracking, cost-per-recovery, failure-to-honey conversion

Delivers: harness engineering as a market. The harness that recovers most failures at lowest cost wins.

---

## Domain-Hash Profile Mapping

| Harness Profile | Domain-Hash | Why |
|-----------------|-------------|-----|
| Fast Path | LegalHash, GrantHash | High volume, structured output, clear success criteria |
| Structured Path | MedHash, CREHash | Multi-step reasoning, lease/underwriting pipelines |
| Adversarial Path | ClawHash | Hostile inputs, security pressure, refusal required |
| Tool Path | AgentHash | Tool-calling correctness, multi-step agentic evals |
| Failure Harvest | All domains | Triggered when any run fails unrecoverably |

---

## Bee Best Practices

**Keep bees narrow.** Each bee should have one job. When bees become bloated, they get harder to debug, outputs become less interpretable, failure attribution becomes muddy.

**Activate only what is needed.** The Router Bee selects the minimum viable harness stack. Do not run every bee on every task.

**Recovery should be targeted.** Repair only the broken section, missing field, or malformed call. Targeted repair beats brute retry.

**State must stay compact.** Objective, constraints, completed steps, outstanding steps, artifacts collected, output contract. Not a verbose transcript.

**Verifiers should be concrete.** Check real things: validity, completeness, consistency, compliance with contract. Not vague "is this good?"

**Record everything that changes system quality.** Which bees activated, which profiles performed best, what failed, what was recovered, whether the fix generalized.

**Celebrate failure immediately.** Failure should trigger classification, capture, learning, asset creation. Do not bury bad runs. The bad runs are the lab gold.

---

## Why SwarmHash Matters

Most labs try to build one giant smart agent.

SwarmHash says: build small execution primitives, compose them, measure them, let them fail, keep the receipts, and evolve the mesh.

That is much more Swarm-native. And much more defendable.

The model is not the full artifact.
The harness is part of the artifact.
The eval is a systems test.
The real lab advantage is assembled execution quality.

> Finality is not just the deed.
> It is the deed, the failure receipt, and the jelly candidate —
> all three leaving intelligence behind, no matter what the run produced.
