# MAGIC Model — The AI CRE Firm

**Origin**: Donovan Mackey, 30 years CRE, $8B closed on the Marcus & Millichap platform
**Specialization**: Single Tenant Net Lease (STNL)
**Status**: PROVEN (human) — BLUEPRINT (agents)

## The Model

MAGIC simplified the entire CRE brokerage lifecycle into five clear phases:

```
M — MEETINGS      Book the sits. 200 dials/day. The bullpen grinding.
A — APPRAISALS    Value the asset. Comp analysis. BOV. Present the proposal.
G — GRIND         Win the listing. Go to market. Email blast the book.
I — INK           Got a deal. LOI signed. PSA executed. In contract.
C — CLOSE         Close escrow. Deed recorded. FEE earned. Steak dinner.
```

**Result**: $8B in closed transactions. Very clear focus. The model works.

## The Bullpen

10 junior brokers. 200 dials per day each. 2,000 touches per day total. The grind is the engine. The senior broker closes. The bullpen fills the pipeline.

```
BEFORE (human bullpen):
  10 junior brokers × 200 dials = 2,000 touches/day
  Cost: 10 salaries + office + phones + training
  Output: meetings booked, proposals baked, listings won

AFTER (agent bullpen):
  10 SwarmCRE agents × unlimited capacity = always grinding
  Cost: GPU time + weight (CREHash at $0.029/lb)
  Output: same pipeline, automated
  
  The brokers are agents. The dials are API calls.
  The proposals are generated. The comps are instant.
  The only human is the senior broker who closes.
```

## STNL Specialization

Single Tenant Net Lease — the domain algorithm. Like ClawHash for security or MedHash for medical, STNL is the CRE sub-algorithm:

- Dollar General, Walgreens, Starbucks — credit tenants
- Triple net — tenant pays taxes, insurance, maintenance
- Cap rates, NOI, lease term remaining, tenant credit rating
- The math is clean. The data is structured. Perfect for AI.

## Mapping MAGIC to SwarmOS

| MAGIC | CRE Broker | SwarmOS Equivalent |
|-------|-----------|-------------------|
| M — Meetings | Cold calls, door knocks, referrals | Signal workers, lead scoring, contact API |
| A — Appraisals | Pull comps, drive the property, BOV | SwarmCRE-35B comp analysis, automated BOV |
| G — Grind | Win the listing, go to market, blast the book | Generated proposals, email blast, listing distribution |
| I — Ink | LOI signed, PSA executed, in contract | Auto-generated LOI/PSA from stock templates, e-signature |
| C — Close | Close escrow, deed recorded, commission earned | Deal Machine, closing statement, Hedera anchor, FEE |

## Why This Matters

The CRE brokerage model hasn't changed in 40 years. The same 200 dials. The same bullpen. The same grind. The only thing that changed is who's in the bullpen.

```
1985: Junior brokers with phones and a Rolodex
2005: Junior brokers with phones and a CRM
2025: Junior brokers with phones and a laptop
2026: Agents with 643K weighed CRE pairs and a $0.029/lb pipeline

The model is the same. The workforce changed.
MAGIC stays. The bullpen evolves.
```

## FEE — The Why

MAGIC is how. FEE is why.

```
MAGIC → FEE

F — FINALITY       Hedera anchored. Permanent. Can't be undone.
                   The deed is recorded. The deal is closed. Done.

E — ECONOMICS      Price per pound. Cost to mint. 20x margin.
                   The math works. The steak dinner is earned.

E — EQUITY         You OWN the weight. Sovereign. No subscription.
                   Runs on your GPU. Can never be cut off. Yours.
```

In CRE, the FEE is the commission check. The steak dinner. You did the work, you earned it.

In AI, the FEE is the same thing:
- **Finality** — the pair is weighed, deeded, Merkle batched, Hedera anchored. Permanent.
- **Economics** — the cost to mint is measurable, the price per pound is transparent, the margin is real.
- **Equity** — the buyer owns the weight. Not renting tokens. Not subscribing to an API. Owning an asset.

```
The broker doesn't work for free.
The GPU doesn't run for free.
The MAGIC produces the FEE.

Cook the MAGIC → earn the FEE.
Mine the weight → collect the steak dinner.

MAGIC + FEE = the complete model.
The process and the proof it worked.
```

## Agent-DG: The MAGIC Skill

The product. Agent-DG running the MAGIC playbook as a Claude Code skill.

### Commands

```
/magic dg                          # run full MAGIC cycle on Dollar General
/magic dg --mine                   # M — find DG owners likely to sell
/magic dg --appraise 123-main-st   # A — BOV on a specific DG property
/magic dg --grind                  # G — generate outreach for P1 leads
/magic dg --ink deal-001           # I — generate LOI/PSA for a deal
/magic dg --close deal-001         # C — closing statement, deed, FEE

/magic walgreens                   # same MAGIC, different tenant
/magic starbucks                   # same MAGIC, different tenant
```

### What Each Step Does

```
/magic dg --mine
  Query county assessor APIs for DG properties in target MSAs
  Cross-reference owner holding period (>5yr = likely seller)
  Check lease expiration dates (within 3yr = decision point)
  Score and rank by likelihood to sell
  → P1_leads.csv (owner, address, NOI, cap rate, hold period)

/magic dg --appraise [address]
  Pull DG comps (same state, last 12 months, similar lease term)
  Calculate: NOI ÷ market cap rate = indicated value
  Generate: 1-sheet OM (4 panels, folded in half)
  Generate: listing proposal (5-page booklet)
  → BOV.pdf + OM.pdf + proposal.pdf (stock templates, auto-populated)

/magic dg --grind
  For each P1 lead, generate personalized email from BOV data:
  "Mr. Jones — I just listed a new DG in Florida. 10yr with bumps,
   corner lot, on a light, 7 cap. Send me the deal?"
  Blast the book of business
  → outreach_batch.csv ready for email send

/magic dg --ink [deal-id]
  Generate LOI from deal terms (1 page, stock template)
  Generate PSA from stock template
  → LOI.pdf + PSA.pdf ready for signature
  The ink is on the paper. In contract.

/magic dg --close [deal-id]
  Closing statement (actual vs estimated)
  Deed recorded → Hedera anchored → permanent
  Commission calculated → FEE earned
  → closing_statement.pdf + steak dinner
```

### Model Stack

```
SwarmCRE-35B      — underwriting, BOV, comp analysis
masterwriter:31b  — OM copy, proposal narrative, email personalization
SwarmCurator-9B   — operations, lead scoring, pipeline management
gemma3:12b        — tribunal validation on all analysis (no hallucinated cap rates)
```

### Comp Deeds — The Appraisal Stack

Every DG trade in the country gets a comp deed. Same format as the OM. Same 1 sheet folded in half. Same 4 panels. Universal.

```
COMP DEED (1 sheet, folded in half):
  COVER:          Photo + address + SOLD + price + cap rate + date
  INSIDE LEFT:    Lease summary (tenant, term remaining, bumps, NNN expenses)
  INSIDE RIGHT:   Sale details (buyer, seller, $/SF, cap rate, NOI, hold period)
  BACK:           Map + nearby comps + market cap rate trend line

  Every DG trade → comp deed filed
  Agent-DG maintains 500+ comp deeds in the library
  Updated weekly from public records + CoStar/Crexi feeds
```

When an owner asks "what's my DG worth?":

```
  Agent-DG pulls 5 comp deeds from same state, similar lease term
  Hands them over like a stack of playing cards
  The owner sees REAL trades, not opinions
  
  "Mr. Jones, here are the last 5 Dollar Generals that sold
   in Georgia. 5.5 to 6.25 caps. Yours is worth $1.25M.
   Here's the comps."
   
  The comp deed IS the appraisal.
  No 50-page report. No "let me get back to you."
  5 cards on the table. The math speaks.
```

The comp deed format:
- Same dimensions as the OM (1 sheet folded)
- Same design language (cover, left, right, back)
- Stock template — auto-populated from trade data
- Agent-DG generates them in 2 seconds from the database
- Tribunal-verified — no hallucinated cap rates, no fake comps

```
AGENT-DG COMP LIBRARY:
  /magic dg --comps GA              # all DG comps in Georgia
  /magic dg --comps FL --last 6mo   # Florida, last 6 months
  /magic dg --comps --near 30301    # within 50 miles of zip code
  /magic dg --comp-deck 123-main    # 5 best comps for a specific property
                                    # → comp_deck.pdf (5 sheets, ready to hand out)
```

### Stock Templates (1 sheet, 1 page, zero friction)

```
OM:        1 sheet folded in half → 4 panels (cover, left, right, back)
LOI:       1 page (price, terms, closing date, contingencies, sign here)
Proposal:  5-page booklet (cover, valuation, marketing plan, track record, contact)
Email:     3 sentences (new listing, the numbers, "send me the deal?")

All stock. Change the address and the numbers. Print.
The agent that generates fastest lists first.
```

### The Flywheel

```
Agent-DG lists a DG
  → auto-blasts the database (personalized, with BOV attached)
  → tracks opens, replies, interest
  → routes 1031 buyers to the listing
  → 3 owners see the trade and want to sell theirs
  → Agent-DG already has their BOV ready (pre-generated)
  → next listing → flywheel spins

Every listing creates the next listing.
The inventory IS the marketing.
The machine feeds itself.
MAGIC → FEE → MAGIC → FEE → MAGIC → FEE
```

---

*$8B closed with human MAGIC. The next $8B closes with agent MAGIC. Same model. Different workforce. The weight is the training. The FEE is the proof.*
