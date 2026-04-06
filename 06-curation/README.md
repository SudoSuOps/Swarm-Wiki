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

## Prompt Genome System (BUILT — /data2/cook-domain-prompts/)

A complete genetic algorithm for prompt evolution. Every prompt is DNA.

### Genome Schema

Each prompt is decomposed into independently mutable parameters:

```json
{
  "persona": "senior analyst at a CRE intelligence platform",
  "credentials": "CCIM/MAI-credentialed",
  "domain_bias": "cre",
  "objective": "translates research into actionable market intelligence",
  "reasoning_style": ["mechanism", "causal_chain"],
  "numeric_density": 3,
  "named_entities": true,
  "tradeoff_analysis": true,
  "metrics_required": true,
  "arithmetic_explicit": false,
  "tone": "professional",
  "audience": "practitioners"
}
```

The **compiler** (`compile_prompt.py`) assembles genome JSON → system prompt string. Every parameter is a gene. Every gene is independently mutable.

### Mutation Axes

| Axis | What It Pushes | Genes Mutated |
|------|---------------|--------------|
| specificity | Named entities, tradeoff analysis | `named_entities=true`, `tradeoff_analysis=true` |
| reasoning | Causal chains, constraint analysis | `reasoning_style` expanded |
| numeric | Rates, ratios, show the math | `numeric_density` increased, `arithmetic_explicit=true` |
| persona | Professional credentials, experience | `credentials`, `experience_years` |

2 parents × 4 axes = 8 mutations per generation. **Crossover** breeds two parents into a child.

### Current Population

**Parents** (Generation 0):
- `quant_analyst` (hash: `00aeb3f5`) — avg 90.5, 1,012 pairs
- `cre_analyst` (hash: `9206000c`) — avg 90.0, 1,007 pairs

**Generation 1 Mutations** (8 variants):
- MUT_01 specificity_quant: **93.8** avg (exploring)
- MUT_05 numeric_quant: **93.4** avg (exploring)
- MUT_02-08: all outperforming parents (91-95 range)

### Fitness Function

`genome_fitness.py` joins local genome metadata with live telemetry from hive-ledger:
- Telemetry scores from `/api/telemetry/prompts`
- **Novelty scoring** prevents convergence — rewards prompts exploring different parts of space
- **Extinction rule**: avg < 85 after 200 pairs = removed from pool
- **Softmax allocation**: temperature-scaled weighting, 5% floor prevents starvation

### Files

| File | Location | Role |
|------|----------|------|
| `compile_prompt.py` | `/data2/cook-domain-prompts/` | Genome → system prompt compiler |
| `genome_fitness.py` | `/data2/cook-domain-prompts/` | Fitness + novelty + telemetry join |
| `genomes/base/` | `/data2/cook-domain-prompts/` | 2 parent genomes (JSON) |
| `genomes/mutations/gen_1/` | `/data2/cook-domain-prompts/` | 8 gen-1 mutations (JSON) |
| `genomes/schema.py` | `/data2/cook-domain-prompts/` | PromptGenome dataclass + compile + mutate + crossover |
| `genomes/novelty.py` | `/data2/cook-domain-prompts/` | Vector distance novelty scoring |

**Key finding**: "The prompt was the bottleneck, not the model." Confirmed by EXP-004 — one sentence change produced +9% specificity improvement. The genome system is the automated version of what APE did manually.

---

## Pair Generation Engine (BUILT — /data2/openalex/)

The cook scripts that turn raw sources into training pairs.

### cook_openalex.py — Main Engine

Turns academic papers into instruction/response training pairs:

```
OpenAlex JSONL → reconstruct abstract → generate instruction → 
LLM inference → quality gate → platinum JSONL
```

**Backends** (3 options):
- **vLLM** (local): SwarmCurator-9B or 27B on swarmrails GPUs
- **Together.ai** (cloud): Zero local GPU, 20 concurrent workers
- **Cloudflare Workers AI** (free): Free 30B model tier

**Multi-worker**: 4-20 concurrent workers depending on backend.

### The 5-Step Trajectory Template

The secret sauce. Every pair is generated with this reasoning scaffold:

```
1. IDENTIFY the core issue
2. CALCULATE key metrics — specific numbers, percentages, show the math
3. ANALYZE root causes — 'because', 'therefore', 'consequently'
4. EVALUATE risks — 'if X then Y', 'unless Z', 'assuming W'
5. RECOMMEND specific actions with clear rationale
```

**Why it works**: JellyScore counts trajectory keywords (5), causal keywords (3), conditional keywords (2), and quantitative markers (2). Max 12 → capped at 10 → divided by 10. The trajectory template guarantees all keyword categories are hit, producing 100% reasoning_depth scores.

### Domain Prompt Library

12 domain files in `/data2/cook-domain-prompts/domains/`:

| Domain | Persona | Key References |
|--------|---------|---------------|
| aviation | ATP pilot, A&P engineer, safety investigator | FAA/ICAO/EASA regs, ADs, service bulletins |
| cre | Senior CRE analyst | Cap rates, NOI, DSCR, FAR citations |
| medical | Pharma safety analyst | Drug interactions, dosing, FDA refs |
| legal_consumer | Consumer protection attorney | CFPB, FDCPA, state regs |
| finance | Capital markets analyst | Fixed income, derivatives, SEC filings |
| energy | Grid/renewables analyst | DOE, FERC, ISO/RTO refs |
| crypto | DeFi protocol analyst | Smart contracts, TVL, governance |
| economic | Macro economist | Fed, BLS, trade data |
| climate | Environmental scientist | EPA, IPCC, emissions data |
| software | Systems architect | Architecture patterns, security |
| ai | ML researcher | Model architectures, training methods |

Each domain prompt appends the universal `RJ_SYSTEM_SUFFIX` which includes the trajectory template.

### PropolisCollector — Failure Harvesting

Failures (propolis-tier pairs) are collected by `PropolisCollector` from `/data2/audit/hive/propolis.py` and fed into `cook_swarmjelly.py` — a specialized cook that turns failures into learning pairs. The failures teach the model what NOT to do.

### Additional Cook Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `cook_all.sh` | `/data2/openalex/` | Batch orchestrator for all domains |
| `cook_auditor.py` | `/data2/openalex/` | Quality audit on cooked pairs |
| `test_rj_prompts.py` | `/data2/openalex/` | A/B test prompt variants |
| `cook_swarmjelly.py` | `/data2/Swarm-Jelly/` | Failure → learning pair cook |
| `pair_cooker.py` | `/data2/swarm-radar/` | Signal → pair generation |
| `domain_prompts.py` | `/data2/swarm-radar/` | Signal-specific prompt library |
| `cook_dna_batch2.py` | `~/swarmwriter-nemotron70b/` | Nemotron 70B pair generation |

---

## Prompt Machine

Automated prompt evolution that closes the loop between cook output quality and prompt selection. See [prompt-machine.md](prompt-machine.md).

**Current state**: Genome system built, telemetry endpoints live, softmax allocation implemented in cook_openalex.py. EXP-004 (APE) confirmed the approach — one sentence change produced +9% specificity improvement. The genome system is the automated, continuous version of what APE did as a one-shot experiment.

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
