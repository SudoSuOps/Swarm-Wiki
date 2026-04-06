# Curation

Pair generation, scoring, and quality control. Two systems: what's running (production tribunal) and what's next (full curator fleet).

## Production System (LIVE — April 2026)

The tribunal scores pairs 24/7. Simple, reliable, battle-tested.

```
PRODUCTION PIPELINE:
  Pairs (PostgreSQL) → Bin (queue) → Tribunal Runner → Deed Recorder → Merkle Batcher
                                         ↓
                              Judge A (gemma3:12b, GPU1)
                              Judge B (qwen2.5:7b, whale)
                              Per-dimension CoT scoring
                              Drift threshold: 0.15
```

### What's Running

| Component | Implementation | Location |
|-----------|---------------|----------|
| Scoring engine | `tribunal_runner.py` | swarmrails (systemd) |
| Judge A | gemma3:12b via ollama | GPU1 (RTX PRO 6000) |
| Judge B | qwen2.5:7b via ollama | whale (RTX 3090) |
| Deed recorder | `deed_recorder.py` | zima-edge (systemd) |
| Merkle batcher | Every 50 deeds | zima-edge |
| Scoring prompt | Per-dimension CoT + APE-optimized rubric anchors | `scoring_prompt.py` |
| Watchdog | 14 checks every 5 min | zima-edge (systemd) |

### Scoring Prompt (shipped EXP-003 + EXP-004)

5 dimensions, independently scored, per-dimension reasoning:

| Dimension | Corpus Average | What It Measures |
|-----------|---------------|-----------------|
| accuracy | 0.930 | Factual correctness |
| completeness | 0.899 | Fully addresses the query |
| specificity | 0.790 | Concrete details, numbers, named entities |
| structure | 0.938 | Organization and clarity |
| domain_expertise | 0.940 | Real domain knowledge |

APE-optimized (EXP-004): negative exemplar + rubric anchors. "0.5 means generic." Specificity +9% stricter, spread +48% wider.

### Domain Rotation

| Domain | Pairs in DB | Deeds Filed | Status |
|--------|------------|-------------|--------|
| legal | 5,001 | scoring now | ACTIVE |
| grants | 35,271 | 8,500+ | AVAILABLE |
| aviation | 41,477 | 0 | In queue |
| self_healing | 186,875 | 0 | In queue |
| medical | 417,136 | 5,038 | Round 1 done |
| cre | 810,097 | 0 | In queue |
| finance | registered | 0 | Coming soon |
| imaging | registered | 0 | Coming soon (multimodal) |
| blockchain | registered | 0 | Coming soon |
| research | registered | 0 | Coming soon |

### Rate & Economics

- Throughput: 380 pairs/hr (legal, long pairs) to 777 pairs/hr (grants, medium)
- Cost per deed: $0.000078
- Pairs per kWh: 1,285
- Fleet power: ~1,080W sustained

---

## Blueprint: Full Curator Fleet (NEXT BUILD)

The wiki originally described a 3-tier orchestrated fleet. This is the target architecture, informed by what we learned in production.

### Three-Tier Model Hierarchy

| Tier | Model | Role | Status |
|------|-------|------|--------|
| Strategy | Board Member (Qwen 3.5 27B, fine-tuned on wiki doctrine) | Strategic decisions, cross-domain correlation | BUILDING — 500 pairs generating |
| Judges | Domain-specific fine-tuned models | Per-domain scoring with qualified expertise | PLANNED |
| Workers | gemma3:4b, small quantized models | Classification, routing, triage | AVAILABLE (Xeon + Jetson) |

### Planned Upgrades

**Domain-Specific Judges** (from virgin jelly insight):
- Medical judge: trained on medical Royal Jelly pairs
- CRE judge: trained on CRE Royal Jelly pairs
- Grants judge: trained on grants Royal Jelly pairs
- Each judge is a specialist appraiser, not a generalist

**Prompt Machine v2** (from EXP-004 learnings):
- Automated APE: softmax-weighted prompt variants run continuously
- Extinction rule: prompts scoring below threshold auto-removed
- Mutation axes: specificity, reasoning, numeric density, persona
- Telemetry: per-prompt performance tracked via deed metadata

**Virgin Jelly Pipeline** (from micro-cook architecture):
- Weekly fresh signal capture from live sources
- 750 pairs/week scored and micro-cooked
- Continual LoRA: model compounds knowledge weekly
- Hedera timestamps prove data freshness

**Signal-Driven Orchestration** (from original wiki design):
- VelocityTracker detects hot topics (e.g., CRE debt maturity wall)
- Planner generates cook orders based on market heat
- Assembler builds pairs from live signal + domain templates
- Validator runs 6 deterministic quality gates before tribunal

### 7-Middleware Chain (target architecture)

```
SignalIngestion → Classification(Worker) → Analysis(Judge) → Strategy(Board Member)
    → QualityGate → StateUpdate → Dispatch
```

Each middleware has an algorithmic fallback. Chain runs in <5ms without LLMs. Full LLM mode adds domain intelligence at each step.

---

## Prompt Machine

Automated prompt evolution that discovers which system prompts produce highest-scoring pairs. See [prompt-machine.md](prompt-machine.md).

**Key finding**: "The prompt was the bottleneck, not the model." Confirmed by EXP-004 — one sentence change produced +9% specificity improvement.

**Production state**: Manual APE (research-ops pipeline). Target: automated softmax allocation with continuous mutation.

---

## Verticals (CRE Founding Vertical)

See [verticals.md](verticals.md) for the BaseVertical ABC and vertical configuration.

### CRE Task Types (validated against 810K pair inventory)

| Task Type | Description | Pairs |
|-----------|-------------|-------|
| underwriting_calc | NOI, cap rate, DSCR, IRR | HIGH |
| ic_memo | Investment Committee memoranda | HIGH |
| lease_abstract | Extract lease terms to JSON | MEDIUM |
| t12 | Trailing 12-month normalization | MEDIUM |
| rent_roll | Tenant analysis, escalations | MEDIUM |
| market_comp | Comparable sales/lease analysis | MEDIUM |
| debt_maturity | Loan maturity analysis, refi risk | LOW (virgin jelly target) |
| risk_triage | Environmental, zoning, title | LOW |
| cost_segregation | Depreciation, bonus, tax strategy | LOW |

### Missing CRE Topics (virgin jelly targets for 2026)

- CMBS special servicing / workout procedures
- $1.5T debt maturity wall (2024-2026 refinancing crisis)
- Office-to-residential conversion
- Bank failure / FDIC receivership process
- Florida insurance crisis (Citizens, wind mitigation)
- Climate risk pricing (flood zones, sea level)
- Sale-leaseback structuring
- Mezzanine / preferred equity capital stack
- AI-powered property valuation methodology

---

## Research Ops Integration

Scoring improvements flow from the research pipeline:

| Experiment | Result | Impact on Curation |
|-----------|--------|-------------------|
| EXP-001: Position bias | NO ACTION | Confirmed current order is fine |
| EXP-002: Few-shot | NO ACTION | Single-domain exemplars hurt cross-domain |
| EXP-003: Per-dim CoT | SHIPPED | 10 data points per deed, 5 location coordinates |
| EXP-004: APE optimization | SHIPPED | Specificity +9%, spread +48%, 1 sentence change |

Next experiments: debate pass for high-drift pairs (#5), STaR bootstrap Judge C (#7), domain-specific judges (#8).

---

## Related

- [prompt-machine.md](prompt-machine.md) — Prompt evolution, mutations, softmax allocation
- [middleware.md](middleware.md) — 7-middleware chain details (target architecture)
- [orchestrator.md](orchestrator.md) — State machine, planner, assembler, validator, publisher (target)
- [verticals.md](verticals.md) — Vertical configuration and BaseVertical ABC
- [skills-discovery.md](skills-discovery.md) — SKILL.md format and discovery system
- [../18-blueprints/virgin-jelly-pipeline.md](../18-blueprints/virgin-jelly-pipeline.md) — Micro-cook weekly cadence
- [../19-research/CHANGELOG.md](../19-research/CHANGELOG.md) — Experiment results and shipped improvements
