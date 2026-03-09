# EntityScorer

The EntityScorer (`signal/scorer.py`) assigns confidence scores and priority levels to every signal. It combines source reliability, entity extraction, temporal freshness, and cross-source corroboration into a single confidence value.

## Confidence Formula

```
Confidence = source_weight(0.40) + entity_richness(0.25) + freshness(0.20) + cross_source(0.15)
```

### Component Weights

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| source_weight | 0.40 | Reliability of the signal source (EDGAR > RSS > Reddit) |
| entity_richness | 0.25 | Number and quality of extracted entities (tickers, companies, dollar amounts) |
| freshness | 0.20 | Temporal recency -- decays over hours/days |
| cross_source | 0.15 | Same entity/event appearing in multiple independent sources |

## Named Entity Recognition

The scorer runs NER on every signal to extract structured entities. Extraction feeds both the entity_richness score and the downstream Event Machine.

### Known Entity Databases

| Database | Count | Examples |
|----------|-------|---------|
| REIT_TICKERS | 23 | PLD, DLR, AMT, SPG, O, VICI |
| AI_COMPANIES | 31 | NVIDIA, OpenAI, Anthropic, Google DeepMind |
| CRE_FIRMS | 19 | CBRE, JLL, Cushman & Wakefield, Marcus & Millichap |

### Regex Patterns

| Pattern | Target | Example Match |
|---------|--------|--------------|
| TICKER_PATTERN | Stock tickers | $PLD, NVDA |
| MONEY_PATTERN | Dollar amounts | $1.2B, $450M, $12,500,000 |
| PERCENTAGE_PATTERN | Rates and percentages | 6.5%, 125bps |

## Confidence Refinement

After initial scoring, the EntityScorer applies refinement rules:

- Signals matching known REIT tickers get a source_weight boost (EDGAR-quality data about a tracked entity)
- Signals with both a ticker and a dollar amount get an entity_richness boost (likely a deal announcement)
- Signals from multiple sources within a 2-hour window get cross_source amplification

## Priority Classification

The final confidence score maps to priority levels:

| Priority | Criteria | Action |
|----------|----------|--------|
| P1 | High confidence + accelerating velocity | Immediate: cook orders, Discord alert, HCS seal |
| P2 | Moderate confidence or stable velocity | Batch processing queue |
| P3 | Low confidence or decelerating | Archive for trend analysis only |

Priority classification uses both the EntityScorer confidence and the VelocityTracker acceleration (see [velocity.md](velocity.md)).
