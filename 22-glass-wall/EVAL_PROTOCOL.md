# Eval Protocol — Standing Rules

These rules are non-negotiable. Every eval follows them. No exceptions.

---

## 1. Clean Room

Every eval starts from zero. Cold GPUs, nothing loaded, no background noise.

```
PRE-FLIGHT:
  1. Stop ALL services (tribunal, recorder, ollama models)
  2. Verify BOTH GPUs at idle (< 50W, < 500 MiB)
  3. Power limits set to target
  4. No other processes on the box
  5. Cold start — models load from disk, not VRAM cache
```

If the environment is contaminated, the eval doesn't run. You don't measure with dirty instruments.

---

## 2. Save the Deposition

Every run is on the record. Save EVERYTHING.

```
MUST SAVE:
  - Full question (system prompt + query)
  - Full raw response from each model (min 2000 chars)
  - Judge score + per-dimension breakdown
  - Judge reasoning
  - Timing per response
  - Peak power per response
  - GPU telemetry snapshots
```

Scores without responses are verdicts without depositions. You can't appeal. You can't rescore with a different judge. You can't audit. The deposition IS the evidence.

**File naming**: `proof_of_location_results_YYYYMMDD_HHMMSS.json` — versioned, never overwrite.

---

## 3. Judge Qualification

The judge must be qualified for the domain and weight class it evaluates.

```
HIERARCHY:
  1. Domain-specialist model (trained on the domain)
  2. Purpose-built evaluator (Nemotron 70B)
  3. Large generalist (70B+)
  4. Small generalist (12B) — ONLY for pairs below its weight class

RULE: A 12B model CANNOT judge 31B+ output.
      A generalist CANNOT judge specialist output in isolation.
      A math model CANNOT judge creative writing.
```

A hung jury is worse than no verdict. Match the jury to the case.

---

## 4. Apples to Apples

Both models under evaluation must run at the same precision, on the same class of hardware, with the same constraints.

```
REQUIRED:
  - Same quantization (both bf16, or both Q4 — never mixed)
  - Same context length
  - Same temperature
  - Same max_tokens
  - Same hardware class per model
```

You trained at bf16, you eval at bf16. You deploy at Q4, you benchmark at Q4. Never cross the streams.

---

## 5. Domain Match

The eval questions must match the training data domains.

```
VALID:   Trained on grants → eval on grants (Proof of Location)
BONUS:   Trained on grants → eval on medical (transfer learning test)
INVALID: Trained on grants → claim "general improvement" from mixed eval
```

Report each domain separately. The grants number is the Proof of Location. The medical number is a transfer test. Never combine them into one headline.

---

## 6. Energy is Evidence

Record power consumption throughout the eval. Energy tells you what kind of machine you have.

```
Ferrari: Spikes to 500W+, high peak, fast bursts
Ford:    Steady 300W, consistent throughput, reliable
Both:    Documented. Neither is wrong — they serve different markets.
```

---

## 7. Live Monitoring

Every eval should be observable in real-time. The process IS the product.

```
REQUIRED:
  - Live GPU telemetry (power, temp, util, clocks)
  - Live progress (current question, scores as they come in)
  - Live dimension breakdown (running averages)
```

If you can't watch it, you can't trust it.

---

*The glass wall applies to our own process, not just the product. These rules are public.*
