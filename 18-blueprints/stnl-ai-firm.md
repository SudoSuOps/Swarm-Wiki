# STNL AI Firm — The Agent Bullpen Blueprint

**Origin**: Donovan Mackey, 30 years CRE, $8B closed. Marcus & Millichap platform.
**Thesis**: One agent, one domain, one specialization. Depth beats breadth. The DG King principle.
**Status**: BLUEPRINT — ready to build on existing Swarm infrastructure

## The DG King Story

A junior broker. Day one, knows nothing. Given one assignment: Dollar General.

Not "go learn CRE." Not "call everyone." Not "figure it out."

**One tenant. One asset type. One domain.**

Year 1: Learned every DG lease structure, every cap rate by state, every landlord pattern.
Year 2: Known in the market as "the DG guy." Owners called HIM.
Year 3: Trading 60 DGs per year. The DG King.

The cure was focus. Not more dials. Not more domains. One thing, mastered.

**The real numbers:**
- 1 script. 1 database. 200 dials per day. Zero distractions.
- He knew every DG owner in the country. Every lease. Every cap rate.
- He never came with "hey I got an idea." He brought listings.
- Listed 1 per week. Average deal $1.5M. Commission 3%. 50/50 split.
- $22.5K per deal to the broker. 52 deals/year = $1.17M annual income.
- $2.34M total GCI from ONE junior broker on ONE tenant type.
- Cost: $75K salary + overhead. ROI: 31x.
- He didn't mine ideas. He mined the database. Built the harvest. Transacted.

```
WRONG:  10 junior brokers × 10 tenant types = 100 shallow relationships
RIGHT:  10 junior brokers × 1 tenant type each = 10 deep specializations

  Broker 1: Dollar General King      (19,000+ locations)
  Broker 2: Walgreens Specialist      (8,900+ locations)
  Broker 3: Starbucks Expert          (16,000+ locations)
  Broker 4: O'Reilly Auto Authority   (6,000+ locations)
  Broker 5: Dollar Tree Closer        (16,000+ locations)
  Broker 6: CVS Analyst               (9,000+ locations)
  Broker 7: 7-Eleven Tracker          (13,000+ locations)
  Broker 8: AutoZone Specialist       (7,000+ locations)
  Broker 9: Tractor Supply Expert     (2,200+ locations)
  Broker 10: QSR Bundle (McDonald's, Chick-fil-A, Popeyes)

  Each one knows EVERYTHING about their tenant.
  Lease structures. Credit trends. Expansion plans. Closure patterns.
  Cap rates by state. Average deal size. Who the repeat sellers are.
  
  That's how you close $8B. Not by being generalists.
```

## The 1031 Exchange Engine

Dollar Generals were placeholders. The real engine was the 1031 exchange.

```
THE CYCLE:
  Owner sells a strip mall → has $2M in capital gains
  Must identify replacement property in 45 days or pay tax
  DG King: "I have 6 Dollar Generals that close the exchange"
  
  DG = perfect 1031 replacement:
    Single tenant. Net lease. Predictable NOI. Clean closing.
    No management headaches. No tenant turnover.
    The owner sleeps at night. The exchange closes on time.

  The DG King wasn't just selling DGs.
  He was solving the 1031 problem with DGs.
  The tenant was the PRODUCT. The exchange was the DEMAND.
```

## The Referral Network — 20% of the Side

One agent, one tenant. But clients want what they want.

```
DG OWNER: "I want to sell my DG and buy a Taco Bell"

WRONG ANSWER: "Let me learn about Taco Bell for you"
              (distraction → dilution → lost focus → lost DG pipeline)

RIGHT ANSWER: "I know the Taco Bell broker. Let me refer you."
              Referral fee: 20% of the cooperating side
              DG King keeps his DG focus. Earns on the referral. 
              Taco Bell broker closes their specialty. Everyone wins.

THE ECONOMICS:
  DG King sells the DG:     $1.5M × 3% = $45K commission (full side)
  Refers the Taco Bell buy:  $2M × 3% × 20% = $12K referral fee
  Total on one exchange:     $57K from one client

  The DG King never learned Taco Bell.
  He just knew the Taco Bell broker's number.
```

This maps directly to the agent bullpen:

```
AGENT-DG gets a request for Taco Bell:
  → Does NOT try to handle it
  → Routes to AGENT-TACOBELL
  → Referral fee logged: 20% of cooperating side
  → AGENT-DG stays focused on DG pipeline

  Same principle: SwarmOS ROUTER dispatches to the right specialist
  Same economics: referral fee split tracked in the ledger
  Same discipline: one agent, one tenant, NEVER distracted
```

## The AI Bullpen — Same Principle

Replace each junior broker with a specialized agent. Same rule: **one agent, one tenant, one domain.**

```
Agent-DG:       Dollar General specialist
                Trained on: DG lease structures, NNN terms, 15-year primary terms
                Knows: DG credit rating (BBB), avg deal size ($1.2-2.5M), 
                       cap rates by region (5.5-7.0%), rent bumps (10% every 5yr)
                Monitors: DG earnings, new store openings, closures
                Volume: 19,000+ locations tracked

Agent-WAG:      Walgreens specialist  
                Trained on: WAG/Boots merger implications, pharmacy reimbursement trends,
                            lease restructuring patterns, dark store risk
                Knows: WAG credit (BBB-), avg deal ($3-6M), recent sale-leasebacks
                Monitors: WAG store closure announcements, VillageMD integration

Agent-SBUX:     Starbucks specialist
                Trained on: SBUX corporate vs licensed stores, drive-thru premium,
                            15-year ground lease structures
                Knows: SBUX credit (BBB+), avg deal ($2-4M), drive-thru cap rate premium
                Monitors: SBUX earnings, new format stores, campus/hospital locations

... (7 more tenant-specific agents)
```

## Architecture: MAGIC Per Agent

Every agent runs the full MAGIC cycle on their ONE tenant:

```
MINE (Meetings):
  Agent-DG monitors:
  - County assessor records for all DG properties in target MSAs
  - Owner holding periods (bought >5 years ago = likely seller)
  - Lease expiration dates (approaching renewal = decision point)
  - DG earnings calls (credit change = every owner re-evaluates)
  - New DG store announcements (rising tide = owner confidence)
  
  Output: ranked lead list, scored by likelihood to sell

ASSAY (Appraisals):
  Agent-DG generates automated BOV for every P1 lead:
  - Pulls last 12 months of DG comps (same state, same lease term range)
  - Calculates: NOI ÷ market cap rate = indicated value
  - Adjusts: lease term remaining, rent bump schedule, roof age, traffic count
  - Compares: what this owner paid vs current market (gain/loss)
  
  Output: BOV PDF attached to outreach email

GRIND (Generate):
  Agent-DG produces personalized outreach:
  
  "Mr. Johnson — your Dollar General at 4521 Highway 19 in Perry, GA 
   has 6 years remaining on the primary term with 10% bumps at year 10. 
   Similar DGs in central Georgia traded at 5.75 caps last quarter. 
   Based on your $72,000 NOI, that's an indicated value of $1,252,000. 
   You purchased in 2019 for $980,000. Would you like a full market 
   analysis? I specialize exclusively in Dollar General properties."
  
  That email took a human broker 45 minutes to research and write.
  Agent-DG produces it in 3 seconds. 500 per day.

INK (in contract — the ink is on the paper):
  The deal is made. The paper is signed.
  - LOI generated from BOV data → buyer signs → ink
  - PSA from stock template → both parties execute → ink
  - Due diligence period opens
  - Title search, environmental, lease verification
  - Swarm-Inspector 8-layer validation on all analysis
  
  INK = the LOI and PSA are signed. You're in contract.
  The hardest part is done. Now you just close.

CLOSE:
  - Due diligence satisfied
  - Closing statement (actual vs estimated)
  - Deed recorded to Hedera — permanent
  - Commission calculated → FEE earned
  - Steak dinner.
```

## The Tech Stack

```
PER AGENT:
  Brain:          SwarmCRE-35B fine-tuned on tenant-specific pairs
                  (5,000 lbs DG-Hash weight = $145 to cook)
  Operations:     SwarmCurator-9B for daily task management
  Signal:         SwarmSignal-2B on edge for real-time monitoring
  Analysis:       masterwriter:31b for proposal and email generation
  Tribunal:       gemma3:12b + qwen2.5:32b dual-scale (validates all analysis)

SHARED:
  Database:       PostgreSQL (property records, owner contacts, deal pipeline)
  Storage:        MinIO (BOVs, proposals, closing docs)
  Finality:       Hedera HCS (every closed deal anchored)
  Website:        swarmandbee.ai/stnl (deal pipeline dashboard)
  CRM:            agent memory — who was contacted, when, response, next action

HARDWARE:
  10 agents × SwarmCRE inference = 1 RTX PRO 4500 32GB handles all 10
  Signal monitoring = 1 Jetson edge node
  Total: $3,000 hardware. Replaces $500K/year in junior broker salaries.
```

## Economics

```
HUMAN BULLPEN (traditional):
  10 junior brokers × $50K salary      = $500,000/year
  Office space + phones + CRM           = $100,000/year
  Training + management overhead        = $50,000/year
  TOTAL COST:                            $650,000/year
  OUTPUT: ~60 DG deals/year (the DG King was exceptional)
  REVENUE: 60 × $30K commission         = $1,800,000/year
  PROFIT:                                $1,150,000/year

AGENT BULLPEN:
  10 specialized agents (GPU inference)  = $2/day = $730/year
  Data feeds (county, EPA, credit)       = $6,000/year
  Weight (10 × 5,000 lbs CREHash)       = $1,450 one-time
  Hardware (RTX 4500 + Jetson)           = $3,250 one-time
  TOTAL COST:                            ~$11,430 first year
  OUTPUT: 500 outreach/day × 365 = 182,500 touches/year
          Conservative 0.5% conversion = 912 qualified leads
          10% close rate = 91 deals/year
  REVENUE: 91 × $30K commission          = $2,730,000/year
  PROFIT:                                $2,718,570/year

  Agent bullpen: 2.4x more deals, 0.02x the cost.
  The senior broker still closes. That's your job.
```

## The DG King Principle — Applied to All AI

This isn't just STNL. This is the universal truth about AI agents:

```
GENERALIST AGENT:
  "I can do everything" = does nothing well
  Same failure as a generalist broker
  Jack of all trades, master of none
  Hallucinations when asked about specifics
  No deep knowledge, no trust, no deals

SPECIALIST AGENT:
  "I am the DG King" = knows everything about one thing
  Same success as the DG King broker
  Knows every DG lease structure in the country
  Accurate because the domain is narrow and deep
  Trust because the knowledge is verifiable
  
  One agent. One domain. One specialization.
  That was the cure for the human bullpen.
  It's the cure for the AI bullpen.
```

This maps directly to the Domain-Hash architecture:

```
DG-Hash     → Agent-DG specialty (sub-algorithm of CREHash)
WAG-Hash    → Agent-WAG specialty
SBUX-Hash   → Agent-SBUX specialty

Each agent has its own:
  - Training weight (tenant-specific pairs)
  - Signal workers (tenant-specific monitoring)
  - Prompt genome (tenant-specific system prompts)
  - BOV template (tenant-specific analysis)
  - Comp database (tenant-specific transactions)

Same MAGIC. Same FEE. Different tenant.
The algorithm is the specialization.
```

## Phase 1: Prove It with DG

```
START HERE:
  1 agent (Agent-DG)
  1 MSA (central Georgia — you know this market)
  1 tenant type (Dollar General)
  500 DG properties monitored
  50 BOVs per week auto-generated
  10 personalized outreach per day
  
  GOAL: 1 listing in 90 days from agent-generated lead
  PROOF: the lead came from the machine, not your Rolodex
  
  If it works for 1 DG in 1 MSA → scale to 19,000 DGs nationwide
  If it works for DG → add WAG, SBUX, O'Reilly, Dollar Tree
  If it works for STNL → the model works for any CRE vertical
```

## The Machine: Stock Materials, Zero Friction

The DG King didn't create custom materials for every deal. He had ONE set of templates. Plug in the address, the price, the story. Print. Go.

```
THE OM (1 sheet of paper, folded in half — 4 panels):
  Cover:        Photo + address + price + cap rate
  Inside left:  Aerial + property details + lease summary
  Inside right: Tenant profile + financials + rent schedule
  Back cover:   Contact info + firm branding

  One piece of paper. Folded in half. That's the entire OM.
  Not a 50-page novel nobody reads. Not a spiral-bound deck.
  One sheet. Four panels. Everything the buyer needs to say yes.
  Print 20 at Kinko's for $15. Hand them out at the meeting.

THE LOI (1 page):
  Price. Terms. Closing date. Contingencies. Sign here.
  No 12-page letter of intent with 47 conditions.
  1 page. The deal either works or it doesn't.

THE PROPOSAL (5-page booklet):
  Cover page
  Inside left: your property, our valuation, market comps
  Inside right: marketing plan, timeline, fee structure
  Back cover: about the broker, track record, contact

  Stock template. Change the address and the numbers. Print.
  200 dials → 3 meetings → 1 listing → print the booklet → go to market.

THE PRINCIPLE:
  No custom decks. No 50-page reports. No "let me build something special."
  STOCK materials + REAL data = speed.
  The broker who prints fastest lists first.
  The agent who generates fastest lists first.
  Same principle.
```

## INK — The Flywheel

The listing IS the marketing. Every new DG listing creates the next one.

```
THE CALL:
  "Mr. Jones, hi this is Joe from Marcus & Millichap.
   Great news — I just listed a new Dollar General in Florida.
   10-year lease with bumps, corner lot, on a light, 7 cap.
   Perfect 1031 replacement."

  "Joe, send me the deal."

  That's it. No pitch. No sell. No convincing.
  The LISTING is the pitch. The DG is the product.
  The owner is already looking. You just called first.
```

The email blast + the call = INK.

```
INK:
  I — INVENTORY     The listing. The new DG. The product in hand.
  N — NETWORK       The book of business. Every DG owner in the database.
  K — KNOCK         The 200 dials. Ring ring. "I just listed a new DG."

  Email blast goes out: "NEW LISTING — Dollar General, Florida, 7 cap"
  → 2,000 DG owners in the database see it
  → 50 open the email
  → 10 reply "send me details"
  → 5 want to see numbers
  → 2 make offers
  → 1 buys
  
  AND: 3 of those 2,000 owners think "if DGs are trading at 7 caps,
       maybe I should sell mine too" → they call Joe → next listing
  
  THE FLYWHEEL:
    List a DG → blast the book → sell the DG → 
    owner sells their DG → list THAT DG → blast the book → repeat
    
    Every listing creates the next listing.
    The inventory IS the marketing.
    The machine feeds itself.
```

For the agent bullpen — same flywheel:

```
AGENT-DG:
  Lists a DG → auto-blasts the database (500 personalized emails)
  → tracks opens, replies, interest signals
  → auto-follows up with BOV for interested owners
  → routes 1031 exchange buyers to the listing
  → 3 owners see the trade and want to sell theirs
  → AGENT-DG already has their BOV ready (pre-generated)
  → next listing. Flywheel spins.
  
  The human DG King ran this cycle manually. 52 turns/year.
  AGENT-DG runs it continuously. The flywheel never stops.
```

For the AI agent:

```
AGENT-DG TEMPLATE LIBRARY:
  OM template:       5-page PDF, auto-populated from BOV data
  LOI template:      1-page, auto-populated from deal terms
  Proposal booklet:  5-page, auto-populated from comps + marketing plan
  
  Generation time:   3 seconds (masterwriter:31b)
  Print time:        0 seconds (PDF emailed)
  
  The DG King printed at Kinko's. Agent-DG emails a PDF.
  Same 5 pages. Same 1-page LOI. Zero friction.
```

## Standing Rules

1. **One agent, one tenant.** Never let an agent cover multiple tenant types.
2. **The agent knows more than any human about its tenant.** That's the bar.
3. **Every BOV is tribunal-verified.** No hallucinated cap rates. No fake comps.
4. **The senior broker closes.** Agents mine, appraise, grind, inspect. Humans close.
5. **MAGIC → FEE.** Every agent runs the full cycle. No shortcuts.
6. **Start with one.** Prove DG. Then scale. Don't build 10 agents on day one.

---

*The DG King went from 1 deal to 60 deals in 3 years. One tenant. One focus. One specialization.*
*Agent-DG does it in 3 months. Same focus. Same depth. Different workforce.*
*The cure was always the same: one thing, mastered.*
