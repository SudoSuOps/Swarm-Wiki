# Signal Workers

11 workers collect signals from diverse sources. All implement the BaseWorker ABC with the fetch/normalize/dedup/score/emit lifecycle.

## Worker Inventory

| Worker | Source | Schedule | Description |
|--------|--------|----------|-------------|
| worker_rss.py | RSS feeds | MEDIUM (1hr) | Configurable feed list covering CRE publications, tech news, and vertical-specific sources |
| worker_arxiv.py | arXiv papers | MEDIUM (1hr) | Monitors cs.AI, cs.LG, q-fin, and other relevant categories for new papers |
| worker_hn.py | Hacker News | FAST (15min) | Top and new stories via HN API. High signal for AI/infrastructure trends |
| worker_reddit.py | Reddit | FAST (15min) | Monitors subreddits relevant to CRE, AI, finance, and aviation |
| worker_fred.py | Federal Reserve (FRED) | SLOW (6hr) | Economic indicators: interest rates, employment, CPI, housing starts. Slow-moving but high-impact signals |
| worker_edgar.py | SEC EDGAR filings | MEDIUM (1hr) | Tracks 15 REIT tickers for 10-K, 10-Q, 8-K filings. 34 events pumped live to date |
| worker_gh.py | GitHub trending | MEDIUM (1hr) | Trending repositories in AI/ML, infrastructure, and related topics |
| worker_trending.py | Composite trending | MEDIUM (1hr) | Aggregates cross-source trend signals into composite trending scores |
| worker_cre_news.py | CRE industry news | FAST (15min) | CRE-specific news sources: deal announcements, market reports, regulatory changes |
| worker_webhook.py | Webhook ingest | Event-driven | HTTP endpoint for external systems to push signals. No polling schedule. |
| worker_human.py | Manual input | On-demand | Discord commands and API calls for human-submitted signals. Bypasses scheduling. |

## EDGAR Worker Detail

The EDGAR worker is the most structured signal source. It tracks 15 REIT tickers and extracts structured events from SEC filings:

- Filing types: 10-K (annual), 10-Q (quarterly), 8-K (material events)
- Event extraction: Acquisition announcements, disposition alerts, lease expirations, debt maturity, dividend changes
- 34 events pumped live to the Event Machine (D1 database)

## Worker Configuration

Workers are configured via the signal engine. Each worker defines:
- `source_name`: Unique identifier
- `schedule`: FAST, MEDIUM, or SLOW
- `fetch()`: Source-specific data retrieval
- `normalize(raw_data)`: Convert to standard signal schema
- `dedup_key(signal)`: MD5 fingerprint field selection

## CLI

```bash
python3 -m signal collect              # Run all workers once
python3 -m signal collect --worker hn  # Run single worker
python3 -m signal status               # Show last run times and health
```
