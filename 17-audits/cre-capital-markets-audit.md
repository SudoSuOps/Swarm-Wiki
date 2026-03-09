# CRE & Capital Markets Audit

## Market Moment (2026)

- CBRE/JLL/CWK stocks dropped 12-14% Feb 2026 on AI disruption fears — biggest since COVID
- $16.7B deployed into proptech in 2025 (67.9% YoY increase)
- AI-focused proptech share: 20% (2024) -> 30-50% (2025)
- 75% of US brokerages use AI daily
- RE AI market $222B -> $989B by 2029
- McKinsey: AI could generate $110-180B in value for real estate

## Top 10 CRE Tech Competitors

| # | Company | What | Revenue/Valuation | Fine-tuned Models? | API? |
|---|---------|------|-------------------|---:|------|
| 1 | CoStar | Data monopoly (6M properties, 11M comps, 2.4T fields) | $3.2B revenue | NO | NO |
| 2 | VTS | Leasing & asset mgmt (12B+ sqft) | $1.88B | NO | NO |
| 3 | Blooma | AI lending underwriting ($12B analyzed) | $15M Series A | NO | PARTIAL |
| 4 | Cactus | AI deal underwriting (92% less data entry) | Growing fast | NO | NO |
| 5 | Dealpath | Institutional deal management | $200-400/user/mo | NO | NO |
| 6 | Buildout | Broker marketing & CRM | -- | NO | NO |
| 7 | Prophia | AI lease abstraction ($20/doc) | -- | NO | NO |
| 8 | RedSwan | CRE tokenization ($4B+ on Hedera) | 13K investors | NO | PARTIAL |
| 9 | CRED iQ | CMBS/loan data & analytics | -- | NO | YES |
| 10 | Trepp | Structured finance data (since 1979) | -- | NO | YES |

**None have fine-tuned CRE models. None have LLM-as-Judge. None are API-first intelligence.**

## Big Brokerage Internal AI

| Firm | AI Initiative | Status |
|------|--------------|--------|
| CBRE | "Ellis" research AI, Nexus FM platform, AI playground (20K sites) | Cloud-only, back-office |
| JLL | Proprietary LLM (2023), "JLL Serve", dozens of products | Internal only |
| M&M | AI for underwriting prep, market intel, marketing copy | Early stage |
| Cushman & Wakefield | AI-powered market analytics | Cloud-only |

All: cloud-only, proprietary, back-office focus, not for independent brokers.

## 8 Gaps Nobody Fills

1. **On-device CRE AI** — all competitors are cloud-only
2. **Voice-first broker tools** — field brokers need hands-free
3. **Independent broker tools** — big firms hoard internally
4. **AI + tokenization combined** — nobody does both
5. **Signal-driven deal origination** — reactive, not proactive
6. **Offline field capability** — dead zones exist
7. **Verifiable AI output** — no on-chain provenance anywhere
8. **Capital markets Intelligence Objects** — actionable, not just data

## CRE Dataset Moat

| Asset | Count | Competitor Equivalent |
|-------|-------|----------------------|
| Verified CRE training pairs | 643,382 | None (CoStar has raw data, not training pairs) |
| CRE task types | 8 | None |
| Asset types covered | 9 | CoStar: all, but not training-ready |
| Live CRE skills | 19 | Cactus: ~5, Blooma: ~3 |
| Capital markets pairs | 45,039 (training NOW) | None |
| Capital markets cook streams | 8 | None |

## Capital Markets Engine (7-Layer Architecture)

| Layer | Function |
|-------|----------|
| 1. Input | Raw deal data, market feeds, EDGAR filings |
| 2. Normalization | Standardize formats, extract entities |
| 3. Feature Engineering | Calculate ratios (DSCR, LTV, cap rates) |
| 4. Retrieval | Similar deals, market comps, precedent transactions |
| 5. Reasoning | SwarmCapitalMarkets-27B analysis + scenario modeling |
| 6. Decision | Risk scoring, recommendation generation |
| 7. Output | Intelligence Objects (verified, structured, HCS-sealed) |

### 4 Product Modes

| Mode | Purpose |
|------|---------|
| Deal Screen | Quick Go/No-Go on incoming deals |
| Credit Memo | Full underwriting package for IC presentation |
| Scenario Lab | Stress testing (rate shocks, vacancy, cap rate expansion) |
| Distress Mode | CMBS special servicing, maturity wall analysis |

## Capital Markets Cook Pipeline (8 Streams)

| Stream | Task Types | Target |
|--------|-----------|--------|
| debt_maturity | Maturity analysis, refinancing scenarios | 5,000 |
| cmbs_distress | Special servicing, workout strategies | 5,000 |
| rate_advisory | Interest rate scenarios, hedging | 5,000 |
| equity_advisory | Cap rate analysis, value-add strategies | 5,000 |
| valuation_advisory | DCF, comparable sales, income approach | 5,000 |
| deal_origination | Deal screening, pipeline management | 5,000 |
| macro_causality | Fed policy impact, economic indicators | 5,000 |
| deal_graph | Multi-party deal structure, entity relationships | 5,000 |

## SwarmCapitalMarkets-27B

| Property | Value |
|----------|-------|
| Base | Qwen3.5-27B Dense |
| Status | TRAINING (step ~20/844, ~29.5h total) |
| Training pairs | 45,039 |
| Eval pairs | 500 |
| GPU | swarmrails GPU 1 (RTX PRO 6000, 96GB) |
| Hyperparams | bf16 LoRA r=64, batch 2, grad_accum 16, lr 2e-5 |

## Deal Machine Mapping

The Swarm pipeline IS the M&M brokerage deal machine:

| M&M Lifecycle | Swarm Pipeline |
|--------------|----------------|
| Make the dials | Signal Workers (11 sources) |
| Book the sits | SwarmCurator-2B classifies, routes |
| Do the proposals | SwarmCRE-35B underwriting + IC memos |
| Win the listing | Judge/Gate validates, seals |
| Go to market | Skills: market_report, comp_analyzer |
| Generate LOIs | Skills: bookmaker, lead_scorer |
| Best final | SwarmCurator-27B strategic ranking |
| In escrow | deal_tracker skill, HCS Event topic |
| Due diligence | SwarmCRE-35B + research analysis |
| Hard deposit | Judge verification gate |
| Close | HCS seal (SHA256 + guarantee.json) |

## Revenue Model

| Model | Benchmark | Application |
|-------|-----------|-------------|
| API usage-based | Together.ai, OpenAI | SwarmSkills API per-call |
| Subscription | CoStar ($10K-100K/yr) | Intelligence Objects access |
| Outcome-based | Harvey (per-matter) | Per-deal underwriting |
| Model licensing | HuggingFace Pro | On-prem deployment |
| Data marketplace | Scale AI | CRE Intelligence Objects |

**Key insight**: Price against analyst labor ($80K-120K/year), not IT budget. 40% time savings = $30K-50K/year per firm.
