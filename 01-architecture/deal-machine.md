# The Deal Machine

The Swarm pipeline is the brokerage deal machine. Not a metaphor -- literally the same lifecycle that closes commercial real estate deals, automated end to end.

This architecture comes from Donovan Mackey, founder of Swarm & Bee. 30-year CRE broker. Senior Managing Director at Marcus & Millichap, where he led the national industrial team and closed $8B in sales across industrial STNL, cold storage, supply chain logistics, and economic development. M&M was a machine for closing deals. Swarm is that machine encoded as AI.

## The Mapping

Every step in a real brokerage deal maps to a component in the Swarm stack:

| # | Brokerage Step | Swarm Component | What Happens |
|---|----------------|-----------------|--------------|
| 1 | **Dials** | Signal Workers (11 sources) | Prospecting. Workers scrape EDGAR, county records, lease databases, construction permits, news feeds. Every 15 minutes, the system is making dials -- reaching out to data sources looking for opportunity. |
| 2 | **Sits** | SwarmCurator-2B classifies | First meeting. The 2B edge model triages incoming signals: is this worth pursuing? P1 (act now), P2 (watch), P3 (background), or noise. Fast, cheap, runs on a $200 device. |
| 3 | **Proposals** | SwarmCRE-35B underwriting + IC memos | Pitch the deal. The vertical model generates underwriting calculations, investment committee memos, lease abstractions, and market comparables. This is the work product that wins business. |
| 4 | **Win Listing** | Judge/Gate validates, HCS seals | Got the listing. Deterministic gates verify the numbers (JSON valid, schema complete, calculations correct). If it passes, it gets sealed to Hedera with a SHA-256 hash. The intelligence object is now an asset. |
| 5 | **Go to Market** | Skills: market_report, comp_analyzer | Market the property. Skills generate market reports, pull comparable sales, analyze rent rolls, score leads. The listing is active and producing intelligence. |
| 6 | **LOIs** | Skills: bookmaker, lead_scorer | Letters of intent. The bookmaker skill structures offers, the lead scorer ranks buyers by likelihood to close. Multiple offers get compared systematically. |
| 7 | **Best & Final** | SwarmCurator-27B strategic ranking | Select the winner. The 27B model does deep strategic analysis -- comparing offers not just on price but on certainty of close, timeline, contingencies, buyer track record. |
| 8 | **Escrow** | deal_tracker skill, HCS Event topic | Open escrow. The deal tracker skill monitors milestones. Every state change publishes to the HCS Event topic on Hedera -- immutable audit trail. |
| 9 | **Due Diligence** | SwarmCRE-35B + research models | Inspect the deal. The vertical model cross-references environmental reports, title searches, zoning compliance, tenant creditworthiness. SwarmResearch-32B handles open-ended investigation. |
| 10 | **Hard Deposit** | Judge verification gate | Money goes hard. Final verification pass. Every number, every assumption, every calculation gets re-validated through the deterministic gate chain. If something changed since the LOI, the gate catches it. |
| 11 | **Close** | HCS seal (SHA-256 + guarantee.json) | Record the deal. The final intelligence object gets its guarantee.json: Merkle root of all data, SHA-256 hash, HCS transaction ID, timestamp. Immutable proof that this deal happened, with this data, at this time. |

## Why This Matters

Most AI companies build from theory. Swarm builds from decades of deal-making experience.

Every model exists because there is a real step in the deal lifecycle that needs it. Every skill exists because a broker actually does that task by hand today. Every gate exists because bad data kills deals, and in CRE, a killed deal is real money lost.

The intelligence feedback loop maps directly to how a brokerage gets better over time: more deals closed means more market knowledge, which means better proposals, which means more listings won. Swarm automates that flywheel.

## The Numbers

- 11 signal workers (the dials)
- 28 skills (19 CRE + 9 medical)
- 6 deterministic gates (the quality floor)
- 1.15M+ training pairs across all verticals
- 5 HCS topics on Hedera mainnet (Block, Receipt, Event, PoE, Escrow)
- 5 HTS tokens on Hedera mainnet (Block, Pair, Model, Deed, Dataset)

This is not a demo. This is infrastructure for the next generation of commercial real estate intelligence.
