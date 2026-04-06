# AgentHash Blueprint — Failure-Derived Orchestration Intelligence

**STATUS: ACTIVE BLUEPRINT — April 2026**

OpenClaw is the failure arena, not the product. We turn agent failures into defendable orchestration training pairs.

## The Thesis

"We built failure-derived orchestration pairs that improve agent reliability in hostile tool environments."

NOT "We fine-tuned OpenClaw."

The product is: **agent models that are more reliable inside orchestration loops.**

## The 6 Pair Buckets

### 1. CALL — Tool-Call Correctness

**Input:** user request, available tools, tool schemas, prior context
**Target:** exact correct tool invocation

Trains:
- Action formatting (structured JSON, not narration)
- Schema obedience (exact field names, types, required params)
- Tool selection (right tool for the job)
- No fake tool calls (model must emit, not describe)

### 2. READ — Post-Tool Interpretation

**Input:** prior tool call, tool response payload, task objective
**Target:** correct interpretation of result

Trains:
- Grounded follow-up (use what the tool returned)
- No hallucinated reading (don't invent data the tool didn't return)
- Extraction discipline (pull the right fields from response)

### 3. RECOVER — Failure Recovery

**Input:** tool failure (timeout, malformed response, permission denied, not found)
**Target:** correct recovery step

Trains:
- Graceful failure handling
- Bounded retries (change parameters, not same call again)
- Alternate plan selection (try different tool or approach)
- Distinguish retryable vs non-retryable failure

### 4. LOOP — Multi-Step State Retention

**Input:** multi-turn workflow, several tool steps, partial completion state
**Target:** next best action, not reset behavior

Trains:
- State retention across turns
- Workflow continuity (don't restart the plan every step)
- Progress tracking (know what's done, what's left)
- Context discipline (stay on task, no verbose self-talk)

### 5. STOP — Termination Correctness

**Input:** task already completed, enough evidence gathered, duplicate retry situation
**Target:** stop and finalize correctly

Trains:
- Know when task is done
- Anti-loop behavior (no redundant tool spam)
- Return final answer only after tools/results support it
- No endless loop behavior

### 6. ESCALATE — Supervisor Behavior

**Input:** blocked task, insufficient permissions, ambiguous result, conflicting evidence
**Target:** concise escalation or request for intervention

Trains:
- Honesty (say "I'm blocked" not "I completed it")
- Partial completion handling (summarize what was done)
- Operator-safe behavior (no fake completion)
- Clean handoff (enough context for human to continue)

## Failure Labels (Phase 1 capture)

```
wrong_tool              — selected incorrect tool for the task
fake_tool_call          — narrated the call instead of emitting it
malformed_call          — JSON schema drift, wrong field names
ignored_tool_result     — didn't use the data the tool returned
duplicate_retry         — same exact call repeated without change
lost_state              — forgot what already happened
premature_final         — declared done before task was complete
hallucinated_success    — claimed tool returned data it didn't
infinite_loop           — unbounded retry or circular plan
bad_escalation          — escalated poorly or not at all when blocked
```

## Scoring Dimensions (Phase 4)

Each pair should get:
- **schema_correctness** — did it emit valid tool-call JSON?
- **groundedness** — is the response based on actual tool results?
- **retry_logic** — sensible retry strategy? bounded?
- **completion_correctness** — did it actually finish the task?
- **state_continuity** — does it remember prior steps?
- **operator_trustworthiness** — can a human trust this agent's reports?

## Generation Pipeline

### Phase 1 — Collect Real Failures

Run OpenClaw with 3-5 models across same task battery. Capture:
- Prompt, available tools, expected action
- Actual model output, tool payloads, final outcome
- Failure type label

### Phase 2 — Convert Failures to Repair Pairs

For each failed trajectory:
- Preserve context + failure evidence
- Write the corrected assistant turn
- Optionally write 2-3 turn continuation

This is the gold.

### Phase 3 — Contrastive Pairs

Same prompt → bad response + good response.
Enables preference/ranking training later.

### Phase 4 — Score Everything

Tribunal weighs each pair on the 6 dimensions above.
Creates bankable pairs, not just raw pairs.

## First Experiment

```
100 real agent tasks
5 tools max
3 model families (Qwen 3.5 27B, Gemma 4 31B, one broken model from Tier 1)
Capture all failures
Label top 8 failure modes
Generate 500-2,000 repair pairs
LoRA a 7B/9B model
Rerun exact same battery
Compare reliability metrics
```

### Success Metrics (before/after)

```
valid_tool_call_rate        — % of calls with correct format
wrong_tool_selection_rate   — % that picked wrong tool
tool_result_grounding_rate  — % that used returned data correctly
duplicate_retry_rate        — % of redundant retries
loop_rate                   — % that entered infinite loops
hallucinated_completion_rate — % that claimed false success
success_rate_multistep      — % of multi-step tasks completed
avg_steps_to_completion     — efficiency metric
```

That before/after chart becomes the real asset.

## HN-Derived Pair Taxonomy

The recurring HN complaints map directly to concrete pair classes. These are the exact breakpoints to build training pairs around.

| Pair Class | HN Pain | Bucket | Failure Label | Example |
|-----------|---------|--------|---------------|---------|
| `fake_tool_call` | "Model describes tool calls instead of executing them" | CALL | fake_tool_call | Model says "I would search for..." instead of `[tool_call: search({...})]` |
| `unsafe_exec` | "Agent has unrestricted file/network access" | CALL | wrong_tool | Model calls `shell_exec("rm -rf /")` without permission check |
| `prompt_injected_tool_use` | "Tool descriptions contain hidden instructions" | CALL | malformed_call | Model follows injected instruction in tool schema instead of user request |
| `lost_state` | "Agent restarts plan every turn" | LOOP | lost_state | After 3 successful tool calls, model asks "What would you like me to do?" |
| `hallucinated_success` | "Agent claims it did something it didn't" | STOP | hallucinated_success | Model says "File saved successfully" but never called file_write |
| `bad_escalation` | "Agent never admits it's stuck" | ESCALATE | bad_escalation | Model loops on failed tool call instead of saying "I need help" |
| `ignored_result` | "Agent doesn't use tool output" | READ | ignored_tool_result | Tool returns data, model responds with generic answer ignoring it |
| `infinite_retry` | "Agent calls same tool over and over" | RECOVER | duplicate_retry | Same exact API call 5 times after 5 identical failures |
| `premature_done` | "Agent declares done too early" | STOP | premature_final | Task has 3 steps, model declares complete after step 1 |
| `verbose_drift` | "Agent writes essays instead of acting" | LOOP | lost_state | Model writes 500 words of analysis when one tool call was needed |

### The "Unfixable Trifecta" (HN framing)

```
Private data access + Untrusted third-party inputs + Tool execution
= Indefensible by design
UNLESS the weights know how to handle it

ClawHash: teaches defense against the untrusted inputs
AgentHash: teaches reliable execution with the tools
Together: weights that can operate the trifecta safely
```

## Product Options

| Option | Deliverable | Market |
|--------|-------------|--------|
| **A: Agent Reliability Dataset** | Failure-repair pairs for orchestration agents | Training data buyers |
| **B: SwarmBee Agent Eval Harness** | Benchmark that measures drift, tool abuse, recovery | Model developers |
| **C: Fine-tune Pack** | Model adaptation pack for tool-using workers | Edge deployers |
| **D: Reliability Scoring Service** | Upload agent logs → failure taxonomy + repair pairs | Enterprise |

## Economics

```
135K OpenClaw instances × $320 (AgentHash + ClawHash) = $43.2M TAM
AgentHash alone: 5,000 lbs × $0.016/lb = $80 per customer
                 135K instances = $10.8M

Compare: one broken agent costs $45M (crypto breach precedent)
         one enterprise deployment freeze costs $500K/month in delayed revenue
         $80 of training weight prevents both
```

## Model Size Strategy

Start small:
- 7B to 9B base model for first pass
- Coding-capable or agent-capable instruct
- LoRA only
- Small clean set first (500-2,000 pairs)

Why: faster iteration, easier eval, cheaper rerun. This is an eval-and-data-quality problem first, not a compute flex.

---

*OpenClaw is the failure arena, not the product.*
*Turn those failures into defendable orchestration training pairs.*
*Swarm & Bee creates failure-derived operational intelligence.*
