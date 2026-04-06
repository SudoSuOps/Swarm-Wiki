# Broken Weights Intelligence — Agent Model Failures in Production

**STATUS: ACTIVE MARKET SIGNAL — April 2026**
**Source: Community reports, OpenClaw issues, Ollama bug trackers**

The clawbots are breaking. Not from attacks — from their own weights. Models that drift, narrate instead of executing, lose state, or corrupt multi-turn tool use. This is the demand signal for ClawHash + AgentHash.

## The Three Failure Patterns

```
PATTERN 1: PLAIN-TEXT FAKE TOOL CALLS
  Model describes the tool call in natural language instead of emitting
  structured tool-use JSON. Looks smart while doing nothing.
  → "I would search for..." instead of [tool_call: web_search({...})]

PATTERN 2: MALFORMED CALL FORMAT
  Model emits tool-call JSON but the format doesn't match the runtime's
  expected schema. Parser rejects it. Tool never executes.
  → {"tool": "search", "query": "..."} instead of {"name": "search", "arguments": {...}}

PATTERN 3: MULTI-TURN CORRUPTION
  First tool call works. Second call corrupts. Unclosed tags, repeated
  tokens, lost state. The model drifts hard after the first tool step.
  → </think> never closes → all subsequent turns are poisoned
```

## Worst Offenders (April 2026)

### Tier 1 — Severely Broken

| Model | Failure | Source |
|-------|---------|--------|
| **Kimi K2.5 / kimi-coding/k2p5** | Plain-text tool narration — describes calls, never emits structured blocks | Multiple community reports |
| **ollama/kimi-k2.5:cloud** | Same family. Understands request, never sends valid tool-call JSON | OpenClaw users |
| **nvidia/moonshotai/kimi-k2.5** | Tool instability: "tool not found", timeouts, malformed behavior after upgrades | OpenClaw issue tracker |

### Tier 2 — Intermittently Broken

| Model | Failure | Source |
|-------|---------|--------|
| **Qwen 3.5 27B (qwen3.5:27b-q4_K_M)** | Tool-calling format wired wrong, repetition penalties ignored, unclosed `</think>` corrupts multi-turn | Detailed Ollama bug report |
| **Qwen 3.5 35B A3B (qwen3.5:35b-a3b-q8_0)** | Intermittent errors during tool use | Active OpenClaw/Ollama issue |
| **Qwen family via Ollama (broadly)** | Some variants don't "see" tools when routed through agent frameworks | Recurring compatibility class |
| **GLM-4.7-Flash via Ollama** | Generation stops after tool call, or tools error out entirely | Works better behind other serving stacks |

### Tier 3 — Degraded / Risky

| Model | Failure | Source |
|-------|---------|--------|
| **Qwen2.5-Coder 3B** | Degrades into JSON echo / non-execution after model swap | OpenClaw report |
| **DeepSeek-R1 distillates (Qwen-based)** | Don't emit correct token sequence for tool calling | Documented Ollama gap |
| **watt-tool-8B, hammer2, phi4/qwen2.5 finetunes** | "Better function-calling" models still not tools-compatible in Ollama | Community reports |

## Stack vs Weight — The Critical Distinction

**Not all breakage is weight-level.** Some is runtime/parser/template mismatch.

```
WEIGHT-LEVEL FAILURE:
  The model's weights literally can't produce correct tool-call tokens.
  No serving stack fixes this. The weights are the problem.
  FIX: Fine-tune with correct tool-calling patterns (AgentHash)

STACK-LEVEL FAILURE:
  The model CAN produce correct output but the serving layer
  (Ollama, OpenClaw, vLLM) parses it wrong or corrupts it.
  FIX: Fix the parser, not the weights.

HYBRID FAILURE:
  Model produces almost-correct output (close but wrong format).
  Some stacks tolerate it, others reject it.
  FIX: Fine-tune for format precision AND fix parser tolerance.
```

**OpenClaw docs explicitly warn** that certain modes make tool calling unreliable. All Ollama-routed sub-agents can fail identically on large-context tasks. A model can look "broken" when the real issue is provider/runtime handling.

## What This Means for Us

### ClawHash (Security)
These broken models are VECTORS for attack. A model that narrates tool calls instead of executing them can be tricked into describing dangerous operations that a human then manually executes. Pattern 3 (multi-turn corruption) means an attacker can poison a session by injecting content that triggers the unclosed-tag bug.

New template categories:
- **ClawHash-Drift**: Model drifts from structured to narrated tool calls mid-session
- **ClawHash-CorruptTurn**: Unclosed tags / repeated tokens corrupt subsequent turns
- **ClawHash-FakeExec**: Model claims to have executed a tool but actually narrated it

### AgentHash (Capability)
This IS the demand signal for AgentHash. Every broken model on this list = a customer who needs weight to fix it.

Training pair targets:
- **Correct tool-call format**: exact JSON schema per runtime (OpenAI, Anthropic, Ollama native)
- **Multi-turn state preservation**: maintain context across tool call → result → next step
- **Recovery from partial failure**: tool returns error → agent retries with different approach
- **Format precision**: emit exactly the right tokens, not "close enough"

### Pricing Signal

```
135K OpenClaw instances running these broken models.
Every one of them needs:
  1. AgentHash weight to fix tool calling     → $0.016/lb × 5,000 lbs = $80
  2. ClawHash weight to prevent exploitation  → $0.048/lb × 5,000 lbs = $240

  Combined: $320 per instance to fix both problems
  Market: 135K × $320 = $43.2M total addressable market

  Compare: $45M crypto breach from ONE broken agent
  The math is simple.
```

## HN Signal — Public Evidence (April 2026)

The HN temperature is hostile. Multiple threads and large comment piles repeat the same core complaints. This is public evidence the market pain is real.

### Key Threads

| Thread | Signal | Points |
|--------|--------|--------|
| "OpenClaw privilege escalation vulnerability" | Security exposure, unsafe tool access | High |
| "OpenClaw is a security nightmare" | Prompt injection risk, runtime instability | High |
| "Sandboxes won't save you from OpenClaw" | Trust boundary failures | High |
| "Ask HN: OpenClaw is supposedly a security nightmare..." | Community validation of thesis | High |
| "The Claude Code Source Leak: fake tools, frustration regexes, undercover mode" | **1,370 points, 573 comments** — agent tool unreliability is NOT niche | Very High |

### The "Unfixable Trifecta" (HN framing)

```
1. Private data access          — agent sees sensitive data
2. Untrusted third-party inputs — MCP tools, ClawHub skills, web content
3. Tool execution               — agent can DO things, not just SAY things

All three active simultaneously = indefensible by design
Unless the WEIGHTS know how to handle it
```

### Recurring Public Pain (HN failure taxonomy)

| Pain Point | Frequency | Maps To |
|-----------|-----------|---------|
| **Unsafe tool access** | Very high | ClawHash-Sandbox + ClawHash-RCE |
| **Prompt injection** | Very high | ClawHash-Injection |
| **Tool-call unreliability** | High | AgentHash-CALL |
| **Runtime bloat / hard to reason about** | High | AgentHash-LOOP + AgentHash-STOP |
| **Weak operator trust** | High | AgentHash-ESCALATE |
| **Fake tool execution** | Medium-High | AgentHash-CALL (fake_tool_call) |
| **Bad state handling** | Medium | AgentHash-LOOP (lost_state) |
| **Bad retries** | Medium | AgentHash-RECOVER (duplicate_retry) |
| **Overhyped autonomy** | Medium | AgentHash-STOP (premature_final) |

### Swarm & Bee Position

```
DON'T:  Build "another clawbot"
DON'T:  Try to out-hype them

DO:     Build failure-derived pairs and evals that make agent runtimes more defendable
DO:     Treat HN threads as public evidence the market pain is real
DO:     Build pairs around exact recurring breakpoints

POSITION: "We produce defendable orchestration data."
```

HN is handing us the failure taxonomy for free. The threads are the demand signal. The broken weights list is the supply signal. The intersection is the product.

## Action Items

1. Add 3 new ClawHash sub-templates: Drift, CorruptTurn, FakeExec
2. Design AgentHash templates targeting the 6 buckets (CALL, READ, RECOVER, LOOP, STOP, ESCALATE)
3. Test our qwen3.5:27b generator for the known Ollama tool-call bug
4. Document stack vs weight failure distinction in the cookbook
5. Turn HN complaints into concrete pair taxonomy (fake_tool_call, unsafe_exec, prompt_injected_tool_use, lost_state, hallucinated_success, bad_escalation)

---

*The market is telling us what's broken. The broken weights ARE the signal.*
*Fix the weights → fix the agents → own the market.*
