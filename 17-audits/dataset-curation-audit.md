# Dataset Curation Audit

**Date**: 2026-03-06
**Overall Grade**: B+
**Source**: `~/Desktop/DATASET_CURATION_AUDIT_2026-03-06.md`

## Executive Summary

Swarm & Bee operates a 1,158,902-pair dataset factory across 5 verticals with a mature, production-proven curation pipeline.

## Grades

| Dimension | Grade |
|-----------|-------|
| Data Quality Gates | A |
| Deduplication | B- |
| Contamination Prevention | A- |
| Provenance & Versioning | B |
| Schema Consistency | A- |
| Scale & Coverage | B+ |
| Market Positioning | A |
| Regulatory Readiness | C+ |

## Quality Gates (Grade: A)

**6-Gate Deterministic Pipeline** (`factory/gates.py`):
1. JSON validity
2. Output length (JSON >= 20, text >= 50 chars)
3. Numeric verification (gold targets within tolerance)
4. Concept presence (minimum 2 domain terms)
5. Deduplication (MD5 fingerprint)
6. Degenerate detection (repetition patterns)

**CoVe 2-Stage**: Rewrite (Llama-3.3-70B) + Verify (Qwen3-235B, 5 criteria, threshold 20/25)

**Yields**: CRE 99.2%, Medical 77.9%, Aviation 76.1%

### Industry Comparison

| Practice | Industry Standard | Swarm Status |
|----------|------------------|--------------|
| LLM-as-Judge | 85% human agreement | CoVe + Llama 4 Maverick — ON PAR |
| Multi-criterion scoring | 3-7 dimensions | 5 dimensions — ON PAR |
| Chain-of-thought judging | Required | CoVe verdicts include reasoning — ON PAR |
| Pairwise evaluation | Reduces position bias | NOT IMPLEMENTED |
| Judge ensemble | 2-3 judges | Single judge per stage — GAP |
| Human audit sampling | 5-10% random | No systematic review — GAP |

## Deduplication (Grade: B-)

**Current**: MD5 of normalized question text only.

**Missing**:
- MinHash LSH (near-duplicate detection)
- Semantic dedup (SemHash, Model2Vec)
- Cross-vertical dedup
- N-gram overlap

**Impact**: Estimated 3-8% paraphrased duplicates in synthetic data. CRE template generation = highest near-duplicate risk.

## Contamination Prevention (Grade: A-)

**Strong**: Seed-based separation (train=42, eval=99999), hash-verified, deal ID isolation.

**Missing**: Dynamic benchmarks, embedding similarity (KDS), cross-vertical contamination check, formally sealed eval vaults.

## Provenance (Grade: B)

**Have**: SHA256 checksums, Supabase tables (cook_runs, dataset_versions), frozen model snapshots.

**Missing**: DVC/lakeFS, transformation lineage, license compliance tracking, W&B/MLflow (WANDB_MODE=disabled).

## Schema (Grade: A-)

Core schema standardized with Pydantic (14 models). CRE uses `messages` format, Medical/Aviation use `question/answer` — format gap requires conversion in assemblers.

## Market Positioning (Grade: A)

Only player building fine-tuned CRE models + LLM-as-Judge quality gate. 643K verified CRE pairs is the largest known CRE-specific dataset.

## Vertical AI Market

| Metric | Value |
|--------|-------|
| Global Vertical AI Market (2024) | $12.9B |
| Projected (2034) | $115.4B (24.5% CAGR) |
| AI Datasets Market (2025) | $1.64B |
| AI Datasets Market (2034) | $11.79B (32.9% CAGR) |
| Enterprises planning AI spend increase | 92% |

**Key insight**: Vertical AI competes for labor budgets (13% US GDP), not IT budgets. 10x larger than legacy SaaS.

## Entropy & Start-Phrase Diversity

### Data Assembly Rules

| Rule | Threshold | Purpose |
|------|-----------|---------|
| System prompt diversity | 30+ unique prompts | Prevent template memorization (v1 failure: 2 prompts) |
| Max single prompt share | 10% | No prompt dominance |
| Task type diversity | 26+ unique types | Force generalizable reasoning |
| Start-phrase entropy | < 4% top-1 5-token prefix | Prevent repetitive response openings |
| Difficulty balance | Bronze 20%, Silver 20%, Gold 15%, High 30%, Platinum 15% | Stretch beyond recall without overwhelming |

### The v1 Lesson

SwarmCRE-35B v1: 78K pairs with only 2 system prompts. Model memorized templates, not tasks. Perfect on in-distribution, collapsed on everything else. Fix: 30+ prompts, 26+ task types, < 4% start-phrase concentration.

## Dataset Growth Priorities

| Vertical | Current | Target (6mo) | Priority |
|----------|---------|--------------|----------|
| CRE | 643K | 1M+ | P0 |
| Medical | 432K | 500K | P1 |
| Pharma | 29K | 100K | P1 |
| Aviation | 45K | 150K | P2 |
| Drone | 7K | 50K | P3 |
| Legal | 0 | 50K | CONSIDER |
| Financial | 0 | 50K | CONSIDER |

## Signal-Driven Curation

The signal pipeline feeds directly into dataset curation:

```
Signal Workers (11 sources, tiered 15min/1hr/6hr)
  -> EntityScorer (confidence = w_freq*freq + w_rec*recency + w_src*source + w_sent*sentiment)
  -> Velocity Tracker (7-day SQLite momentum)
  -> Curator Plan (signal -> cook orders)
  -> Cook Pipeline (Together.ai generation)
  -> Quality Gates (6 deterministic + CoVe)
  -> R2 Storage (SafeStore 3-tier)
```

The key insight: signals tell the curator WHAT to cook. Market-moving events (NVIDIA investments, Fed policy, data center deals) generate immediate cook orders for relevant training pairs. This is proactive dataset construction, not static dataset collection.
