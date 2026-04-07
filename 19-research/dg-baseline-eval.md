# Baseline Eval — SwarmAtlas-27B on DG Trade Knowledge

**Date**: 2026-04-07
**Model**: SwarmAtlas-27B (Qwen 3.5 27B Dense, fine-tuned on 45K CRE pairs)
**General CRE score**: 94% PLATINUM (180 prompts, 11 domains)
**DG Trade Knowledge score**: 1 PARTIAL out of 15 = 7%

## The Thesis Proven

The smartest CRE model we've ever built — 94% PLATINUM on general commercial real estate — scored 7% on Dollar General trade knowledge. The base model is SMART but IGNORANT.

This is the moat. This is what SwarmDG-9B will fill.

## Scorecard

| # | Knowledge Point | Ground Truth (DG Wiki) | Atlas 27B Said | Verdict |
|---|----------------|----------------------|---------------|---------|
| 1 | CG Buchalter store count | 800 DGs over 25 years | Confused developers with landlords | **FAIL** |
| 2 | Colby Capital states | Preferred in 6 states | Didn't know | **FAIL** |
| 3 | Standard DG lease term | 15yr NNN initial | Said 5yr initial | **FAIL** |
| 4 | Rent bumps | 10% every 5yr, 6×5yr options | Got bumps right, wrong term structure | **PARTIAL** |
| 5 | $110K → total rent | $7.17M over 45 years | $7.4M (wrong — based on 5yr initial) | **FAIL** |
| 6 | FL DG spread vs national | 25-50 bps tighter | Said 100-125 bps WIDER (backwards) | **FAIL** |
| 7 | DG cap rate | ~6.70% | Said 4.5-5.5% or 5.75-6.50% | **FAIL** |
| 8 | AutoZone cap rate | ~5.34% | Said 5.25-6.00% or 5.5-6.5% | **FAIL** |
| 9 | AZO vs DG spread | ~136 bps tighter | Said 50 bps, confused direction | **FAIL** |
| 10 | 1031 buyer % of deal flow | 30-35% | Didn't know | **FAIL** |
| 11 | Spirit Realty 400+ DGs | Spirit Realty, portfolio seller | Went in circles — Blackstone, Cerberus | **FAIL** |
| 12 | pOpshelf failure | Cannibalization / shop-in-shop ended | Generic guess, no specifics | **FAIL** |
| 13 | FL DOR OWN_ADDR | Free parcel lookup for CI | Didn't know | **FAIL** |
| 14 | 10K pop profitability | DG profitable under 10K population | Didn't know | **FAIL** |
| 15 | New construction premium | 75-100 bps over existing | Didn't know specific spread | **FAIL** |

**Result: 1 partial / 15 = 7%**

## Head-to-Head: Atlas-9B vs Base Qwen 3.5 9B

Both models scored IDENTICALLY on DG trade knowledge — proving the 45K CRE pairs added zero DG-specific knowledge:

| Trade Knowledge | Ground Truth | Atlas-9B (45K CRE pairs) | Base Qwen 3.5 9B (no training) |
|----------------|-------------|-------------------------|-------------------------------|
| CG Buchalter (800 DGs) | 800 stores, 25 yrs | Didn't know | Didn't know |
| Colby Capital (6 states) | Preferred developer | Didn't know | Didn't know |
| DG Lease — initial term | 15yr NNN | Said 5yr | Said 10yr |
| Rent bumps / options | 10%/5yr, 6x5yr options | Partial (got bumps) | Partial (got bumps) |
| $110K → total rent | $7.17M over 45yr | $7.4M (wrong term) | Wrong (wrong term) |
| FL DG spread | 25-50 bps tighter | Said WIDER | Said wider/discount |
| DG cap rate | ~6.70% | Said 4.5-6.5% | Said 6.0-7.5% |
| AZO cap rate | ~5.34% | Said 5.25-6.0% | Said 7.5-9.0% |
| AZO vs DG spread direction | AZO tighter than DG | Confused | Inverted (said AZO wider) |
| 1031 = 30-35% of flow | 30-35% | Didn't know | Didn't know |
| Spirit Realty (400+ DGs) | Spirit Realty | Guessed Blackstone | Guessed Blackstone |
| pOpshelf cannibalization | Shop-in-shop failed | Generic | Generic |
| FL DOR OWN_ADDR | Free parcel lookup | Didn't know | Didn't know |
| 10K pop threshold | Profitable under 10K | Didn't know | Didn't know |
| New construction premium | 75-100 bps | Didn't know | Said 100-200 bps |

**Both models: 0 correct, 1 partial, 14 wrong. IDENTICAL on DG trade knowledge.**

The fine-tune added zero DG trade knowledge — because it wasn't in the 45K training pairs. The cook works (94% PLATINUM on CRE mechanics). The ingredients determine the outcome.

## Additional Failures

- Leaked entire thinking process as plain text on every response
- Fabricated plausible-sounding but WRONG numbers (classic hallucination)
- Got FL pricing direction completely inverted (said wider, reality is tighter)
- Named wrong REIT owners (Blackstone, Cerberus — neither owns DG portfolios)

## What This Means

```
GENERAL CRE KNOWLEDGE (180 prompts):
  SwarmAtlas-27B:  94% PLATINUM
  The model knows CRE mechanics COLD.
  NOI calculations. Cap rate derivations. DSCR analysis. 12/12 math verified.
  
DG TRADE KNOWLEDGE (15 prompts):
  SwarmAtlas-27B:  7% (1 partial / 15)
  The model knows NOTHING about Dollar General specifically.
  Wrong lease terms. Wrong cap rates. Wrong state pricing. Wrong owners.
  
  NOT BECAUSE IT'S DUMB — because the knowledge doesn't exist
  in any base model's training data.
  
  This knowledge lives in:
    - The DG wiki (19 docs, 3,000+ lines)
    - Broker heads (30 years of trade experience)
    - Boulder Group reports (proprietary research)
    - NET Lease Advisor data (industry benchmarks)
    
  NONE of this is in pre-training. ALL of it is in our wiki.
```

## The Ship Criteria for SwarmDG-9B

```
BASELINE (proven today):
  Atlas 27B on DG trade knowledge: 7% (1/15)
  
SHIP THRESHOLD:
  SwarmDG-9B on DG trade knowledge: 80%+ (12/15)
  
  The delta: 7% → 80% = +73 percentage points
  
  NOT +0.002 like the masterwriter eval.
  +73 PERCENTAGE POINTS. Obvious. Undeniable. Defensible.
  
  If the model can correctly answer:
    "What's the standard DG lease term?" → 15yr NNN
    "What cap rate for a FL DG?" → 6.40-6.50% (25-50 bps tighter)
    "Who builds DGs in 15 states?" → CG Buchalter, 800 units, 25yr partnership
    "Who owns the most DGs?" → Spirit Realty, 400+
    "What's the new construction premium?" → 75-100 bps
    
  THEN THE THESIS IS PROVEN.
  THEN WE SCALE TO 100 TENANTS.
  THEN WE SHIP THE PRODUCT.
```

## Why This Can't Be Replicated

```
NO COMPETITOR CAN:
  1. Build this wiki (requires 30 years of CRE trade knowledge)
  2. Source this data (requires EDGAR + DOR + Sunbiz + broker OMs)
  3. Cook this model (requires the wiki pairs + tribunal verification)
  4. Prove this delta (requires the baseline eval we just ran)
  
  The wiki IS the moat.
  The trade knowledge IS the weight.
  The eval IS the proof.
  
  94% PLATINUM on general CRE means NOTHING for DG.
  7% on DG trade knowledge means EVERYTHING for the product.
  
  SwarmDG-9B fills the 93% gap.
  That gap is the business.
```

---

*SwarmAtlas-27B: 94% PLATINUM on CRE, 7% on Dollar General.*
*The smartest CRE model we've built doesn't know a DG lease is 15 years.*
*That's the moat. That's the gap. That's the product.*
*Cook the wiki. Fill the gap. Ship SwarmDG-9B.*
