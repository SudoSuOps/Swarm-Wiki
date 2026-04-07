# Custom Cook — Builder & Permit Process

**Status**: LIVE at swarmandbee.ai/builder
**Principle**: No permit, no build. Every setting frozen before execution. Hidden settings are a liability.

## The Process

Your domain, our scale. Bespoke weight by the pound.

```
1. SCOPE & PLAN       → client defines domain, pair count, system prompts
2. CALIBRATION         → 50 pairs weighed through full tribunal, cost validated
3. PERMIT ISSUED       → client approves flight sheet, all settings frozen
4. COOK                → tribunal runs under permit, gate reports at 25/50/75/100%
5. CLOSING STATEMENT   → actual vs estimated: throughput, cost, quality, time
6. DELIVERY            → ZIP: 5 formats, deed certs, OM, quality report, closing statement
```

8 client notifications. 4 gate inspections. 2 approval gates. Zero black boxes.

## The Flight Sheet

The architectural plan for every cook. Like blueprints submitted to the city — every detail specified, reviewed, and approved before a single pair is weighed.

| Section | What's Specified |
|---------|-----------------|
| Job Specification | Domain, pair count, source file, batch size |
| Scale Assignment | Scale A model, Scale B model, protocol (2-pass), drift threshold |
| Hardware Assignment | Which GPUs, which nodes, power caps, network |
| Weighing Parameters | Temperature, max tokens, prompt version (SHA256 hashed), classification thresholds |
| Economics | Domain-hash, price per pound, energy estimate, ETA, estimated RJ yield |

All values from `swarm.yaml` (single source of truth).

## Permit Process — Four Gates

| Gate | What Happens | Who |
|------|-------------|-----|
| 1. Draft | Operator fills out flight sheet | Operator |
| 2. Review | Every field inspected. Scales verified as base. Settings validated. | Reviewer |
| 3. Freeze | All settings locked. SHA256 hash computed. No changes after freeze. | System |
| 4. Execute | Tribunal runs under permit. Permit ID stamped on every deed. | Automated |

## What Gets Frozen

Once the permit is issued, these are immutable:

| Parameter | Why It's Frozen |
|-----------|----------------|
| Scale models | Can't swap scales mid-run |
| Temperature | Affects output determinism |
| Max tokens | Prevents weight truncation |
| Weighing prompt | Same prompt, same evaluation criteria (SHA256 hashed) |
| Drift threshold | Controls quality gate |
| Classification | RJ/Honey/Propolis thresholds immutable |
| Hardware | Which GPUs, which nodes — silicon assignment locked |
| Batch size | Affects throughput timing |
| Power caps | Affects thermal and timing |

## Permit Violations — Auto Rejection

- Running tribunal without an approved permit → all deeds **VOID**
- Changing settings after freeze → permit **REVOKED**, run terminated
- Using fine-tuned model as scale → permit **DENIED** at review
- Single scale instead of dual → permit **DENIED**
- Skipping 2-pass validation → permit **DENIED**
- Drift threshold above 0.20 → permit **DENIED**
- Flight sheet hash mismatch at execution → run **HALTED**, audit triggered

## Client Timeline

### Phase 1: Scope & Plan
Client notified. Flight sheet drafted with domain, pair count, system prompts, price per pound quoted.

### Phase 2: Calibration
50 pairs weighed through full tribunal. Real latency, real power draw, real RJ rate measured. Cost per pound validated. Report sent to client.

### Phase 3: Permit Issued
**Nothing runs without this.** Client reviews flight sheet + calibration, approves the plan. All settings frozen. SHA256 hash computed. Go/no-go gate.

### Phase 4: Cook — Gate Inspections
Tribunal runs under permit. At each 25% gate:
- Pairs weighed, tier breakdown, quality metrics
- Cost vs estimate
- Client can inspect any pair at swarmandbee.ai/deed/ in real time

### Phase 5: Closing Statement
Actual vs estimated: throughput, cost per pound, quality, time. Every variance explained with specific numbers. Honest accounting.

### Phase 6: Delivery
ZIP package: 5 formats, deed certificates, offering memorandum, quality report, closing statement. Client owns a defendable, deeded, blockchain-anchored asset. Priced by the pound.

## Traceability

Every deed traces to its permit:

```
DEED    SB-2026-0406-00847
  ↓ issued under
PERMIT  PRM-2026-0406-001
  ↓ weighed by
SCALES  gemma3:12b (base) + qwen2.5:32b (base)
  ↓ on
HARDWARE  swarmrails-gpu2 + swarmrails-gpu0
  ↓ with
SETTINGS  temp=0.1, max_tokens=512, drift≤0.15 (FROZEN)
  ↓ verified by
SWARMTITLE  permit on file, settings match, scales base
  ↓ anchored to
HEDERA  0.0.10291838 — PERMANENT
```

## CRE Closing Parallel

The process mirrors commercial real estate closing:

| CRE Document | Swarm Equivalent |
|-------------|------------------|
| Letter of Intent | Flight Sheet (scope + terms) |
| Purchase Agreement | Permit (frozen settings + approval) |
| Title Commitment | Calibration Report (50-pair validation) |
| Closing Statement | Closing Statement (actual vs estimated) |
| Warranty Deed | Title Deed (weight certificate) |
| Title Insurance | SwarmTitle (inspector validates all 5 layers) |

---

*No permit, no build. Every setting frozen. Every deed traceable. Price per pound.*
