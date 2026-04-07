# Micro-Domain Thesis — 10,000x the Addressable Market

**Status**: ACTIVE — proving with SwarmDG-9B (Dollar General first)
**Date**: 2026-04-07
**Origin**: masterwriter eval (+0.002 on broad cook) → DG King principle → this

## The Shift

```
OLD: 7 broad domains (CRE, medical, legal, grants, aviation, security, agents)
     35,957 pairs → broad cook → +0.002 delta → dust
     Expensive. Hard to sell. Impossible to prove ROI.

NEW: Thousands of micro-domains
     5,000 pairs → narrow cook → +0.08 delta → relocation
     $150 to produce. Easy to sell. Obvious ROI.
```

Not 7 domains. Thousands.

## The Math

```
CRE ALONE HAS 100+ MICRO-DOMAINS:
  Dollar General    Walgreens       Starbucks       Tractor Supply
  AutoZone          O'Reilly        Dollar Tree     CVS
  7-Eleven          McDonald's      Chick-fil-A     Popeyes
  Wawa              QuikTrip        Tire Kingdom    Jiffy Lube
  Advance Auto      Family Dollar   Chase Bank      Bank of America
  Aldi              Lidl            Five Below      TJ Maxx
  Sherwin-Williams  Chipotle        Panera          Sonic
  ...each one is a micro-domain

MEDICAL HAS 85+ MICRO-DOMAINS:
  Not "medical." Cardiology. Dermatology. Oncology.
  Orthopedic surgery. Pediatric endocrinology.
  Drug interactions for SSRIs specifically.
  Each specialty = a micro-domain.

LEGAL HAS 50+ MICRO-DOMAINS:
  Not "legal." FCRA disputes. FDCPA violations.
  Patent prosecution. Maritime injury. HOA law.
  Each practice area = a micro-domain.

TOTAL ADDRESSABLE MICRO-DOMAINS: 1,000+ conservatively
```

## Why Micro-Domains Win

```
BROAD COOK (35,957 pairs across 7 sub-domains):
  Each sub-domain gets ~5,100 pairs
  Model learns a little about everything
  Can't outperform base on any specific topic
  Delta: +0.002 → INVESTIGATE → doesn't ship
  
MICRO-DOMAIN COOK (5,000 pairs on ONE tenant):
  All 5,000 pairs deepen ONE topic
  Model becomes the undisputed specialist
  Base model CANNOT know this trade knowledge
  Delta: +0.08 expected → SHIP
  
  Same total pairs. Different distribution.
  Broad = thin everywhere. Narrow = deep somewhere.
  The DG King closed 60 deals. The generalist closed 6.
```

## Why The Base Model Can't Compete

The base model is strong at REASONING. It is not strong at KNOWING.

```
BASE MODEL KNOWS:
  "Dollar General is a discount retail chain"
  Generic. Wikipedia. Any human with Google knows this.

BASE MODEL DOES NOT KNOW:
  CG Buchalter built 800 DGs over 25 years
  FL DG trades 25-50 bps tighter than national average
  Standard lease: 15yr NNN, 10% bumps, 6x5yr options
  $110K base rent → $235K at Option 6 = $7.17M total rent
  Colby Capital is preferred developer in 6 states
  75-100 bps premium new construction vs existing
  1031 exchange buyers are 30-35% of deal flow
  Spirit Realty owns 400+ DGs and is a portfolio seller

  NONE of this is in pre-training. This is TRADE KNOWLEDGE.
  The wiki IS the weight. The cook transfers the weight.
  The delta should be OBVIOUS — not +0.002. More like +0.08.
```

## The Product

One tenant → one wiki → one model → one specialist.

```
PRODUCT LINE:
  SwarmDG-9B         $150    Dollar General specialist
  SwarmWAG-9B        $150    Walgreens specialist
  SwarmTSCO-9B       $150    Tractor Supply specialist
  SwarmAutoZone-9B   $150    AutoZone specialist
  SwarmDollarTree-9B $150    Dollar Tree specialist
  ... (100+ tenant types in CRE alone)

COST TO PRODUCE:
  Wiki research:     $0     (public data — EDGAR, OSM, DOR, Sunbiz)
  Pair generation:   $145   (5K lbs domain-specific weight)
  Training:          $0.50  (10 hours GPU time)
  TOTAL:             ~$150 per model

PRICE TO BUYER:
  One-time:          $150/model
  Subscription:      $49/month (includes weekly virgin jelly updates)
  
BUYER ROI:
  1 closed DG deal = $45K commission
  SwarmDG-9B cost = $150
  ROI: 300x on first deal
```

## The Scale

```
PER TENANT TYPE:
  100 tenant types × $150/model = $15,000 to cook full library
  
REVENUE (conservative):
  10,000 CRE brokers in the US
  × 1% adoption = 100 subscribers
  × $49/month = $4,900/month
  × 12 months = $58,800/year
  FROM ONE TENANT TYPE

  Scale to 20 tenant types:
  20 × $58,800 = $1.17M/year

  Scale to 100 tenant types:
  100 × $58,800 = $5.88M/year

COST TO OPERATE:
  100 models × $150/cook = $15,000 one-time
  Weekly virgin jelly (100 models × $3/week) = $15,600/year
  GPU inference: ~$730/year
  TOTAL: ~$31,000/year operating cost

MARGIN: ($5.88M - $31K) / $5.88M = 99.5%

AND: each broker's deals generate market data
     → feeds back into the wiki
     → improves the next cook
     → makes the model better
     → attracts more brokers
     
THE FLYWHEEL FEEDS ITSELF.
```

## Beyond CRE

```
MEDICAL (85+ specialties):
  SwarmCardiology-9B      $150    knows every cardiac drug interaction
  SwarmDermatology-9B     $150    knows every skin condition protocol
  SwarmOncology-9B        $150    knows every chemotherapy regimen
  ...buyer: specialist physicians, medical groups

LEGAL (50+ practice areas):
  SwarmFCRA-9B            $150    knows every credit dispute pathway
  SwarmPatent-9B          $150    knows every patent prosecution tactic
  SwarmMaritime-9B        $150    knows every Jones Act case
  ...buyer: solo practitioners, small firms

AVIATION (30+ specialties):
  SwarmASRS-9B            $150    knows every incident pattern
  SwarmPart135-9B         $150    knows every charter regulation
  ...buyer: safety officers, compliance teams

TOTAL ADDRESSABLE:
  1,000+ micro-domains × $58,800/year each = $58.8M/year at 1% adoption
  At 5% adoption: $294M/year
  
  From $150 cooks. On $0.50 of electricity. 99.5% margin.
```

## The Proof

SwarmDG-9B is the first test.

```
STEP 1: DG-WIKI-GRAPH (DONE — 16 docs, 2,700+ lines)
STEP 2: Generate 5,000 DG-specific pairs from wiki
STEP 3: Weigh on tribunal (dual-scale)
STEP 4: Cook on Qwen 3.5 9B (QLoRA, 10 hours)
STEP 5: Eval: base vs SwarmDG-9B on 40 DG questions
STEP 6: Delta > +0.05 → thesis PROVEN → scale to 100 tenants
        Delta < +0.03 → thesis KILLED → back to broad cooks

IF PROVEN:
  Cook 10 more tenant models in month 1
  Launch swarmandbee.ai/models → $150/model store
  Weekly virgin jelly subscription → $49/month
  First $1M year within 12 months of proof
```

## Standing Rules

1. **One tenant per model.** Never mix DG and Walgreens.
2. **Wiki first, pairs second.** Intelligence before ingredients.
3. **5,000 pairs is the sweet spot.** Maximum relocation per pound.
4. **$150 is the price point.** 300x ROI. No-brainer.
5. **Eval on what you cooked.** DG model = DG questions. Not generic CRE.
6. **The delta must be obvious.** +0.002 = dust. +0.05 minimum to ship.
7. **The flywheel feeds itself.** Broker deals → market data → wiki → better model.

---

*The masterwriter cooked broad and moved +0.002. Dust.*
*The DG King specialized and closed 60 deals. MAGIC.*
*Not 7 domains. Thousands. Each one a $150 cook with a $45K ROI.*
*That's not a dataset business. That's an intelligence refinery.*
*Prove it with DG. Scale to thousands. The weight IS the product.*
