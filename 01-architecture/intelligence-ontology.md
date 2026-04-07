# Intelligence Ontology — The Operating Map of the Refinery

**Status**: ACTIVE — evolving with every graph rebuild
**Date**: 2026-04-07

## What This Is

This is not just a wiki graph. It is the machine-readable operational memory of Swarm & Bee.

Most companies have docs, code, scripts, buckets, APIs, databases. But they do not have a graph that explains how those things produce intelligence.

Swarm & Bee is building a **graph-native refinery**. The graph IS the map of how raw inputs become intelligence objects.

## What It Enables

```
TODAY:
  ✓ Dependency tracing        — what breaks if we change X?
  ✓ Build impact analysis     — which services touch this concept?
  ✓ Missing documentation     — where are the gaps in the graph?

NEXT:
  → Code-to-concept search    — "what code implements the tribunal?"
  → Training lineage          — "what pairs trained this model?"
  → Architecture QA           — "does this change violate doctrine?"
  → Automated onboarding      — "explain Swarm & Bee to a new dev"
  → Agent navigation          — "Agent-DG, find the owner of this DG"

FUTURE:
  → Self-healing graph        — new code commits auto-update the graph
  → Cross-repo connections    — Swarm Wiki + DG Wiki + code repos = one graph
  → Live operational state    — graph reflects what's running, not just what's documented
```

## Node Types (Semantic Ontology)

Replace flat `type: document` with meaningful types:

| Type | Description | Examples |
|------|------------|---------|
| `concept` | Abstract idea or principle | Proof of Weight, Glass Wall, Train Narrow Win Deep |
| `system` | Running service or platform | SwarmChain, Tribunal Runner, Signal Pipeline |
| `dataset` | Collection of training data | CRE 643K pairs, ClawHash 1,577 pairs |
| `script` | Executable code | generate_clawhash.py, train_swarmatlas_9b.py |
| `model` | Trained AI model | SwarmDG-9B, SwarmAtlas-27B, masterwriter:31b |
| `agent` | Autonomous AI agent | Agent-DG, deed-recorder, tribunal-runner |
| `api` | API endpoint or service | Pool API, Deed API, Shop API |
| `storage` | Data store | PostgreSQL, MinIO, R2 Buckets, IPFS |
| `schema` | Data structure definition | 17-field parcel schema, PIO schema |
| `workflow` | Multi-step process | MAGIC pipeline, 5-layer finality, build-to-suit |
| `source` | External data source | FL DOR, Sunbiz, OpenCorporates, EDGAR |
| `document` | Written documentation | glass-wall doctrine, OM template |
| `hardware` | Physical infrastructure | RTX PRO 6000, Jetson, NAS |
| `person` | Named individual | Donovan Mackey, Satoshi Nakamoto |
| `company` | Business entity | Dollar General Corp, Spirit Realty, Swarm & Bee LLC |
| `metric` | Measurable value | 6.70% cap rate, 0.85 RJ threshold, 1.20x DSCR |
| `experiment` | Research experiment | EXP-003 Per-Dimension CoT, DG Baseline Eval |
| `doctrine` | Standing rule or principle | Train Narrow Win Deep, Permit Before Build |

## Relationship Verbs

Don't just connect nodes. Tell me HOW they connect:

```
PRODUCTION RELATIONSHIPS:
  Intelligence Object  ←stored_in→     R2 Buckets
  Intelligence Object  ←indexed_by→    BGE-Base Embeddings
  Intelligence Object  ←served_by→     swarm-api Worker
  Intelligence Object  ←structured_by→ PIO Schema
  cook_swarmcurator.py ←produces→      Intelligence Object
  EDGAR Pump           ←feeds→         Intelligence Object

TRAINING RELATIONSHIPS:
  DG Wiki              ←generates→     DG Training Pairs
  DG Training Pairs    ←weighed_by→    Tribunal (dual-scale)
  Tribunal             ←produces→      Deed (weight certificate)
  Deed                 ←trains→        SwarmDG-9B
  SwarmDG-9B           ←powers→        Agent-DG

DEPENDENCY RELATIONSHIPS:
  Tribunal Runner      ←reads_from→    swarm.yaml (config)
  Tribunal Runner      ←requires→      Scale A + Scale B (12B+ models)
  Deed Recorder        ←depends_on→    Tribunal Runner (scored pairs)
  Hedera Anchor        ←depends_on→    Deed Recorder (Merkle batches)

VALIDATION RELATIONSHIPS:
  Baseline Eval        ←proves→        Knowledge Gap (0/15)
  Knowledge Gap        ←defines_target→ SwarmDG-9B (80%+ target)
  Train Narrow Win Deep ←governs→      All micro-domain cooks
```

## Community Names (Semantic Labels)

Replace `Community N` with meaningful names:

| ID | Semantic Name | Key Nodes |
|----|--------------|-----------|
| 0 | Core Intelligence Architecture | SwarmLedger, Title Deed, 5-Layer Finality |
| 1 | Data Refinery Stack | Prompt Machine, Middleware Chain, Quality Gates |
| 2 | Training Pipeline | LoRA Config, Training Patterns, Unsloth |
| 3 | Model Fleet | SwarmAtlas, SwarmCurator, SwarmDG, SwarmJelly |
| 4 | Delivery / API Layer | Pool API, Shop API, Deed API, SwarmRouter |
| 5 | Market Intelligence | Cap Rates, Comps, Buyer Profiles, Competitors |
| 6 | Storage + Embeddings | R2 Buckets, MinIO, PostgreSQL, BGE-Base |
| 7 | Swarm Runtime | Tribunal Runner, Deed Recorder, Watchdog |
| 8 | Signal Pipeline | 11 Workers, EntityScorer, VelocityTracker |
| 9 | Blockchain / Finality | Hedera HCS, Merkle Trees, ENS Domains |
| 10 | Research / Experiments | EXP-001 through EXP-004, Baseline Eval |
| 11 | Glass Wall Doctrine | Proof of Weight, Train Narrow, MAGIC |
| 12 | DG Domain Intelligence | DG Wiki, Agent-DG, DG Ownership Graph |

## Node Summary Text

Every node gets a 1-2 line definition:

```
Intelligence Object
  Canonical internal unit of structured Swarm intelligence, linking
  schema, storage, embeddings, event flow, and cook/train outputs.

Tribunal (Dual-Scale)
  Two independent base models weigh each pair on 5 dimensions.
  Consensus weight determines the deed. The tribunal is a SCALE.

MAGIC Model
  Meetings-Appraisals-Grind-Ink-Close. The CRE operating model
  proven at $8B. Same process, human or agent workforce.

Train Narrow Win Deep
  Doctrine: build micro-domain intelligence, not broad domain models.
  General knowledge creates competence. Specific knowledge creates edge.

SwarmDG-9B
  Dollar General STNL specialist model. Target: 80%+ on DG trade
  knowledge (baseline: 0/15 on both base and Atlas-9B).
```

## The Deeper Product Insight

```
WHAT MOST COMPANIES HAVE:
  docs + code + scripts + buckets + APIs + databases
  Disconnected. No map. No relationships. No intelligence flow.

WHAT SWARM & BEE IS BUILDING:
  A graph that explains HOW those things produce intelligence.
  
  Raw signal → scored pairs → deeds → models → agents → deals → signal
  Every step is a node. Every connection is an edge.
  The graph IS the refinery map.

THIS IS NOT A WIKI.
THIS IS THE OPERATING MAP OF AN INTELLIGENCE REFINERY.
```

## Implementation Path

```
PHASE 1 (current): Flat ontology with graphify
  type: document for everything
  Community N labels
  Basic node inspector
  
PHASE 2 (next): Semantic ontology
  18 node types (concept, system, model, agent, etc.)
  Relationship verbs on every edge
  Community semantic names
  1-2 line node summaries
  
PHASE 3 (future): Live operational graph
  Auto-update from git commits
  Code-to-concept mapping
  Training lineage tracking
  Cross-repo connections (Swarm Wiki + DG Wiki + code)
  Agent-navigable (Agent-DG queries the graph directly)
```

---

*The graph is not a visualization. It's the operating map of the intelligence refinery. Every node is a component. Every edge is a relationship. Every community is a functional cluster. The map IS the product.*
