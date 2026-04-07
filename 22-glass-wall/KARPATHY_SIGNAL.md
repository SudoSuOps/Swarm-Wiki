# Karpathy Signal — The Idea File

> *"I think there is room here for an incredible new product instead of a hacky collection of scripts."*
> — Andrej Karpathy, April 2026 (12M views)

> *"This is an idea file. Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you."*
> — Andrej Karpathy, [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

---

## The Pattern He Described

Karpathy's LLM Wiki pattern has three layers:

1. **Raw Sources** — your curated collection of source documents. Immutable. Source of truth.
2. **The Wiki** — LLM-generated markdown files. Summaries, entity pages, synthesis. The LLM writes it, you read it.
3. **The Schema** — a configuration file that tells the LLM how the wiki is structured. You and the LLM co-evolve this over time.

Operations: **Ingest** (process new sources, update 10-15 pages per source), **Query** (ask questions, file good answers back into the wiki), **Lint** (health-check for contradictions, stale claims, orphan pages).

The key insight: *"The wiki is a persistent, compounding artifact. The knowledge is compiled once and then kept current, not re-derived on every query."*

---

## What We Built

| Karpathy's Pattern | Swarm & Bee Implementation |
|--------------------|-----------------------------|
| **Raw sources** | 1.5M pairs in PostgreSQL + 2.5M on NAS + 30K medical images |
| **The wiki** | Swarm-Wiki (19 sections, 80+ pages) + deeds table (20,000+ scored pairs) |
| **The schema** | `scoring_prompt.py` + `CLAUDE.md` + flight sheets + per-dimension CoT rubric |
| **Ingest** | Tribunal runner scores pairs 24/7 → deed recorder files deeds → Merkle batches seal |
| **Query** | swarmandbee.ai/deed (search any deed) + swarmandbee.ai/grant (prompt the model) |
| **Lint** | Swarm-Inspector (8 integrity layers) + research-ops (paper → experiment → production) |
| **Index** | `index.md` in wiki + GitNexus (5,033 nodes across 8 repos) |
| **Log** | deed ledger (CSV) + Hedera HCS anchors (immutable, timestamped) |
| **Compounding** | The flywheel: tribunal → RJ pairs → train model → better pairs → higher yield |

---

## The Deeper Alignment

Karpathy says: *"The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."*

We automated the bookkeeping. The tribunal scores 24/7. The deed recorder files automatically. The Merkle trees seal every 50 deeds. The watchdog checks 14 systems every 5 minutes. The energy tracker monitors watts per deed. The session reporter summarizes daily findings. None of this requires human intervention.

Karpathy says: *"The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."*

That's the glass wall. The founder curates the thesis, directs the architecture, asks the questions that matter. The swarm does everything else — scores, records, anchors, reports, deploys.

Karpathy says: *"Good answers can be filed back into the wiki as new pages. This way your explorations compound."*

That's the research-ops pipeline. Paper → signal → plan → implement → test → eval → ship. Experiment #1 (position bias) filed back as a finding. Experiment #3 (per-dimension CoT) shipped to production. The wiki gets smarter as we operate, exactly as he described.

Karpathy says: *"The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free."*

That's glass-wall (20 docs) + Swarm-Wiki (80+ pages). Both on GitHub. Both version-controlled. Both indexed by GitNexus (5,033 nodes, 10,599 edges). Every change tracked, every commit signed.

---

## Where We Go Further

Karpathy describes a knowledge base. We describe an **asset factory**.

His wiki accumulates knowledge. Our hive accumulates **deeded, scored, anchored, sellable inventory**.

The difference:

| | Karpathy Wiki | Swarm & Bee |
|---|---------------|-------------|
| Output | Markdown pages | Title deeds (scored, anchored, sellable) |
| Value | Knowledge compounds | Inventory compounds + revenue |
| Trust | "I wrote this" | Dual-judge scored, blockchain-anchored, 5 proofs |
| Monetization | Not addressed | Shop ($29-$199), Proof of Location, OM |
| Infrastructure | Obsidian + LLM | 2x RTX 6000 + 100x RTX 3090 + 48x RTX 4500 + Hedera mainnet |
| Maintenance | LLM does bookkeeping | Tribunal runs 24/7, zero human intervention |

He built the pattern. We built the product.

---

## The Idea File Concept

Karpathy's gist IS the product. Not the code. The idea.

> *"In this era of LLM agents, there is less of a point/need of sharing the specific code/app, you just share the idea, then the other person's agent customizes & builds it for your specific needs."*

This glass-wall repo IS an idea file. Twenty documents describing the vision, the doctrine, the architecture, the findings. No code. Just ideas. The code lives in 8 repos indexed by GitNexus. The ideas live here.

The code changes daily. The ideas compound forever.

---

## The Grass Roots Build

No VC funding. No corporate backing. No team of 50 engineers.

One founder. One thesis. LLM agents building the infrastructure. Glass walls showing the work.

- The founder brings 30 years of CRE closing discipline
- The agents bring 24/7 automated scoring, recording, anchoring
- The protocol brings trust: dual judges, Merkle proofs, Hedera timestamps
- The market brings demand: 12M people watched Karpathy say "there's room here"

The idea file is planted. The swarm builds it. The glass wall shows it. Nature takes care of the rest.

---

*"The part he couldn't solve was who does the maintenance. The LLM handles that."*
— Karpathy, on Vannevar Bush's Memex (1945)

*The part the market couldn't solve was who validates the data. The tribunal handles that.*
— Swarm & Bee, on AI training data (2026)

---

*Source: [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — April 2026, 12M+ views*

*Validate the Validator. Prove the Location.*
