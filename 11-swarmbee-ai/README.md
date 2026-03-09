# swarmbee.ai — Web Properties

## Live Sites

| Site | URL | Platform |
|------|-----|----------|
| swarmandbee.ai | https://swarmandbee.ai | Cloudflare Pages |
| Router API | https://router.swarmandbee.com | Cloudflare Workers |
| Metered API | https://api.router.swarmandbee.com | Cloudflare Workers |

## swarmandbee.ai Pages (7)

Built with Cloudflare Pages. Marketing + product showcase.

| Page | Content |
|------|---------|
| Signal | SwarmSignal market intelligence |
| Curator | SwarmCurator fleet — $20/mo and $49/mo tiers |
| Morey | Strategic research platform |
| SwarmCare | Medical AI vertical |
| Hedera | Zero-trust provenance (purple #8B5CF6 theme) |
| Dashboard | Intelligence dashboard |
| SwarmMed | Medical AI product page |

## Pricing (Stripe Integration)

| Tier | Price | Features |
|------|-------|----------|
| SwarmCurator | $20/mo | 20K pairs, 1 vertical, Hedera guarantee |
| Full Access | $49/mo | 250K pairs, 5 streams |
| Enterprise | Custom | Dedicated models, API, support |
| Per-IO API | $0.0002 | Per Intelligence Object (edge model cost) |

Stripe tiers: `curator` ($20), `starter` ($49)

## Section Index

- [Products In Development](products-in-development.md) -- SwarmScaler, App Store, SwarmMed, SwarmPharma, SwarmAviation, OpenRouter
- [CreditSniper](creditsniper.md) -- Litigation-grade credit dispute intelligence (creditsniper.xyz)

## Cloudflare Workers

- Deploy: `cd worker && npx wrangler deploy --remote`
- Tail logs: `cd worker && npx wrangler tail --remote`
- Account: 6abec5e82728df0610a98be9364918e4
- Worker code: `worker/src/index.js` (monolithic router, 40+ endpoints)
- R2 bindings: sb-intelligence, sb-medical, sb-aviation, sb-cre, sb-core, sb-drone
- D1 database: swarm-intelligence-db
- Vectorize: swarm-memory (768-dim, cosine, BGE-Base)
