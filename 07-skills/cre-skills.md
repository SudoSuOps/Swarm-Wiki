# CRE Skills (19)

Commercial real estate skills deployed on router.swarmandbee.com. Each skill maps to a real step in how CRE deals get done -- sourced from decades of brokerage experience.

## Skill Inventory

| # | Skill Name | Description | Spec Path |
|---|-----------|-------------|-----------|
| 1 | `broker_senior` | Senior broker advisor -- deal strategy, client management, market positioning | `skills/cre/broker_senior/SKILL.md` |
| 2 | `broker_junior` | Junior broker assistant -- research, comps, cold outreach, listing prep | `skills/cre/broker_junior/SKILL.md` |
| 3 | `intelligence_query` | Natural language query against CRE intelligence objects | `skills/cre/intelligence_query/SKILL.md` |
| 4 | `bookmaker` | Deal pricing and probability estimation -- what will it trade at | `skills/cre/bookmaker/SKILL.md` |
| 5 | `deal_tracker` | Pipeline tracking -- LOI, escrow, due diligence, close milestones | `skills/cre/deal_tracker/SKILL.md` |
| 6 | `developer` | Development feasibility -- land use, entitlements, construction cost estimation | `skills/cre/developer/SKILL.md` |
| 7 | `signal_scraper` | Market signal extraction from public filings, news, and data feeds | `skills/cre/signal_scraper/SKILL.md` |
| 8 | `investor` | Investment analysis -- returns, risk-adjusted yields, hold/sell recommendations | `skills/cre/investor/SKILL.md` |
| 9 | `exchange_1031` | 1031 exchange advisory -- timeline, qualified intermediary, replacement property rules | `skills/cre/exchange_1031/SKILL.md` |
| 10 | `market_report` | Market report generation -- submarket stats, trends, comparable transactions | `skills/cre/market_report/SKILL.md` |
| 11 | `lead_scorer` | Lead scoring and qualification -- buyer/seller propensity, engagement signals | `skills/cre/lead_scorer/SKILL.md` |
| 12 | `email_composer` | CRE-specific email drafting -- cold outreach, follow-up, deal updates | `skills/cre/email_composer/SKILL.md` |
| 13 | `comp_analyzer` | Comparable sales analysis -- price/SF, cap rate, adjustment grids | `skills/cre/comp_analyzer/SKILL.md` |
| 14 | `rent_roll_analyzer` | Rent roll parsing and analysis -- occupancy, lease terms, rollover risk | `skills/cre/rent_roll_analyzer/SKILL.md` |
| 15 | `debt_analyzer` | Debt analysis -- loan terms, DSCR, debt yield, maturity risk | `skills/cre/debt_analyzer/SKILL.md` |
| 16 | `tax_assessor` | Property tax analysis -- assessed vs market value, appeal potential | `skills/cre/tax_assessor/SKILL.md` |
| 17 | `site_selector` | Site selection scoring -- location factors, labor, infrastructure, incentives | `skills/cre/site_selector/SKILL.md` |
| 18 | `portfolio_optimizer` | Portfolio-level optimization -- diversification, disposition candidates, rebalancing | `skills/cre/portfolio_optimizer/SKILL.md` |
| 19 | `news_digest` | CRE news aggregation and summarization -- market-moving events | `skills/cre/news_digest/SKILL.md` |

## Deal Lifecycle Mapping

These skills map directly to the brokerage deal machine:

```
Dials           → lead_scorer, email_composer
Sits            → broker_junior, intelligence_query
Proposals       → bookmaker, comp_analyzer, market_report
Win Listing     → broker_senior, deal_tracker
Go to Market    → signal_scraper, news_digest, investor
LOI             → debt_analyzer, rent_roll_analyzer
Escrow          → tax_assessor, exchange_1031
Due Diligence   → developer, site_selector
Close           → portfolio_optimizer, deal_tracker
```

## Usage

```bash
# Execute a skill
curl -X POST https://router.swarmandbee.com/skill/comp_analyzer \
  -H "Content-Type: application/json" \
  -d '{"property_address": "123 Industrial Blvd", "asset_type": "warehouse"}'

# Get skill spec
curl https://router.swarmandbee.com/skill/comp_analyzer/spec

# List all skills
curl https://router.swarmandbee.com/skills
```

## JS Module Structure

Each skill is implemented as a JS module in `worker/src/skills/`:

```javascript
// worker/src/skills/comp_analyzer.js
export async function handle(request, env) {
  const input = await request.json();
  // Skill logic -- may call edge AI, query R2, or run deterministic logic
  return new Response(JSON.stringify(result));
}
```

Skills can call the edge model (`@cf/qwen/qwen3-30b-a3b-fp8`), query R2 intelligence objects, hit the D1 database, or run pure deterministic logic -- whatever the task requires.
