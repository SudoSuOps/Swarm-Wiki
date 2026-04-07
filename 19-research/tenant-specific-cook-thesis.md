# Tenant-Specific Cook Thesis — The DG King Principle Applied to Model Training

**Status**: HYPOTHESIS — informed by masterwriter eval results + DG King operational data
**Date**: 2026-04-07

## The Problem

MasterWriter Gold Eval v4 result: **INVESTIGATE**

```
Base (gemma4:31b Q4):     0.9016
MasterWriter (tuned):     0.9032
Delta:                   +0.0016

Domain (Tier 1):         +0.0019 (below +0.03 ship threshold)
General (Tier 3):        +0.0020 (no regression — good)
Specificity:             +0.0042 (improved — but not enough)
Domain expertise:        +0.0062 (improved — but not enough)
```

The cook moved the model, but barely. 35,957 pairs across 37 personas across a BROAD domain (grants, SBA, 501c3, SBIR, finance, workforce dev). The weight was spread too thin. Like a junior broker trying to cover 10 tenant types.

## The DG King Lesson

```
BROAD BROKER (10 tenants):
  Knows a little about everything
  Can't out-detail anyone on anything
  Closes 6 deals/year — average
  
DG KING (1 tenant):
  Knows EVERYTHING about Dollar General
  Every lease structure, every cap rate, every owner
  Closes 60 deals/year — exceptional
  
  The cure: depth over breadth. One tenant, mastered.
```

## The Hypothesis: Tenant-Specific Cooks

Instead of cooking a "grants specialist" or a "CRE analyst," cook a **Dollar General specialist**.

```
BROAD COOK (what we did — masterwriter):
  35,957 pairs across:
    - 37 expert personas
    - SBA 7(a) lending
    - SBIR/STTR
    - 501(c)(3) formation
    - DOE GRIP
    - Workforce development
    - Business formation
    - Finance
  
  RESULT: +0.002 delta. Too broad. Model learned a little about everything.
  
TENANT-SPECIFIC COOK (what we should do — SwarmDG):
  5,000 pairs ALL about Dollar General:
    - DG lease structures (15yr NNN, bumps, options, NNN responsibility)
    - DG cap rate trends (6.70% new, 7.50% existing, state variations)
    - DG site selection (rural fortress, 20K population, co-tenancy)
    - DG preferred developers (Colby Capital, CG Buchalter, build-to-suit)
    - DG comp analysis (recent trades, price/sqft, buyer profiles)
    - DG 1031 exchange mechanics (FL tax-free, 45-day clock)
    - DG owner identification (tax roll → Sunbiz → entity resolution)
    - DG valuation (NOI ÷ cap rate, lease term adjustment, comp deck)
    - DG proposals and OMs (1-sheet format, 4 panels, stock template)
    - DG buyer profiles (1031 exchangers, DSTs, REITs, HNW)
  
  EXPECTED: +0.05 to +0.10 delta on DG-specific questions
  WHY: 5,000 pairs focused on ONE topic = maximum relocation per pound
```

## The Math

```
BROAD COOK:
  35,957 pairs ÷ 7 sub-domains = ~5,100 pairs per sub-domain
  Each sub-domain is shallow — not enough depth to RELOCATE
  Model improved generically but can't outperform base on specifics
  
TENANT-SPECIFIC COOK:
  5,000 pairs ÷ 1 tenant = 5,000 pairs on Dollar General
  Every pair deepens ONE domain — maximum depth per pair
  Model becomes the UNDISPUTED DG expert
  
  Same total weight. Different distribution.
  Broad = thin everywhere. Narrow = deep somewhere.
  
  The DG King didn't know more than other brokers.
  He knew more about ONE THING than all of them.
```

## The Product Line

One tenant → one wiki → one model → one specialist.

```
SwarmDG-9B         — DG-WIKI-GRAPH → 5K pairs → Qwen 3.5 9B cook
SwarmWAG-9B        — WAG-WIKI-GRAPH → 5K pairs → Qwen 3.5 9B cook  
SwarmTSCO-9B       — TSCO-WIKI-GRAPH → 5K pairs → Qwen 3.5 9B cook
SwarmAutoZone-9B   — AZO-WIKI-GRAPH → 5K pairs → Qwen 3.5 9B cook
SwarmDollarTree-9B — DLTR-WIKI-GRAPH → 5K pairs → Qwen 3.5 9B cook

COST PER MODEL:
  Wiki research:  $0 (public data — EDGAR, OSM, DOR, Sunbiz)
  Pair generation: $145 (5K lbs CREHash weight)
  Training:        $0.50 (10 hours GPU time)
  TOTAL:           ~$150 per tenant-specific model

PRICE TO JUNIOR BROKER:
  $150 per model OR $49/month subscription with weekly virgin jelly updates
  
  1 closed DG deal = $45K commission
  SwarmDG-9B cost = $150
  ROI: 300x on first deal
```

## The Eval Design (SwarmDG-9B)

Don't repeat the masterwriter mistake. Eval on EXACTLY what we trained on.

```
60 DG-SPECIFIC QUESTIONS:
  Tier 1 (40 questions — domain-matched):
    DG lease structure questions (8)
    DG cap rate / valuation questions (8)
    DG site selection questions (8)
    DG comp analysis questions (8)  
    DG owner identification / outreach questions (8)
  
  Tier 2 (10 questions — adjacent STNL):
    Walgreens lease comparison (3)
    Tractor Supply site selection (3)
    1031 exchange mechanics for NNN (4)
  
  Tier 3 (10 questions — general):
    General CRE math (5)
    General writing / analysis (5)

SHIP CRITERIA:
  Tier 1 delta > +0.05 (DG-specific improvement must be SIGNIFICANT)
  Tier 3 delta > -0.03 (minimal general regression)
  
  Base gemma4 or qwen3.5 CANNOT know DG lease bump schedules.
  Base CANNOT know that CG Buchalter built 800 DGs over 25 years.
  Base CANNOT know that FL DG trades 25-50 bps tighter than national.
  
  SwarmDG-9B MUST know all of this. That's the proof of location.
  The delta should be OBVIOUS — not +0.002. More like +0.08.
```

## Why This Changes the Business Model

```
OLD MODEL:
  Cook broad domain models (grants, medical, CRE, legal)
  Sell by the pound ($0.029/lb CREHash)
  Customer: enterprises and model builders
  
NEW MODEL (additional):
  Cook tenant-specific specialist models
  Sell the MODEL directly ($150/model or $49/month)
  Customer: individual brokers and small teams
  
  The wiki IS the training data.
  The model IS the product.
  The broker IS the customer.
  
  MAGIC: They use the model to run MAGIC on their tenant.
  FEE: They earn commissions. We earn subscriptions.
  INK: Their deals generate more market data → feeds the wiki → improves the model.
  
  The flywheel: wiki → model → broker → deals → market data → wiki
```

## Standing Rules for Tenant-Specific Cooks

1. **One tenant per model.** Never mix DG and Walgreens in the same cook.
2. **Wiki first, pairs second.** Build the intelligence wiki BEFORE generating pairs.
3. **Eval on what you cooked.** DG model eval = DG questions. Not generic CRE.
4. **The delta must be obvious.** +0.002 is a failed cook. +0.05 minimum to ship.
5. **5,000 pairs is the sweet spot.** First 5K = maximum relocation. After that, diminishing returns.
6. **$150 per model is the price point.** ROI = 300x on first deal. No-brainer for a broker.
7. **Weekly virgin jelly.** Keep the model fresh — new comps, new trades, market shifts.

---

*The masterwriter cooked broad and moved +0.002.*
*The DG King specialized and closed 60 deals.*
*Same principle. Different workforce. Cook narrow. Cook deep. Cook one tenant.*
*That's the cure.*
