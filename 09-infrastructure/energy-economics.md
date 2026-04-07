# SwarmEnergy — Compute Economics

**Status**: LIVE at swarmandbee.ai/energy
**Principle**: Energy is evidence. Every deed has a cost-to-weigh in watts. Every pound has an energy cost. The weight costs energy. The energy proves the work.

## The Formula

```
COST TO MINT (per deed):
  Fleet power (W) × time per deed (s) ÷ 3,600 × $/kWh = cost/deed

PRICE PER POUND:
  Cost to mint × 20 = price per pound (20x margin)
  
PROOF OF WORK:
  GPU time + electricity → digital expertise
  Same economics as Bitcoin mining, same discipline
```

## Fleet Power Budget

Source: `swarm.yaml` → `infrastructure`

| Node | Hardware | Power Cap | Role |
|------|----------|-----------|------|
| GPU 0 | RTX PRO 6000 Blackwell 96GB | 300W | Training + Scale A (heavy) |
| GPU 1 | RTX PRO 6000 Blackwell 96GB | 250W | Scale A (standard) + Scale B (heavy) |
| GPU 2 | RTX PRO 4500 Blackwell 32GB | 150W | Scale A (standard) / deed writer |
| GPU 3 | RTX PRO 4500 Blackwell 32GB | 150W | Scale B (standard) |
| CPU | Xeon w9-3475X 36C/72T | ~200W | Orchestration |
| Whale | RTX 3090 24GB | idle | Disabled — no 7B scales |
| Edge | Zima N150 + T1000 | ~50W | Deed recorder + watchdog |
| Lite | Zima Celeron | ~15W | Web host (nginx + APIs) |
| NAS | Synology DS1525+ | ~80W | PostgreSQL + MinIO + IPFS |
| **Total fleet** | | **~1,195W** | |

## Cost Per Pound by Domain

Derived from real throughput measurements. Price = 20x cost to mint.

| Domain-Hash | RJ/hr | Watts/RJ | Cost/1K RJ | Price/lb |
|------------|-------|----------|-----------|---------|
| LegalHash | 683 | 0.88W | $0.08 | $0.0022 |
| GrantHash | 246 | 2.43W | $0.22 | $0.0061 |
| MedHash | 209 | 2.86W | $0.26 | $0.0072 |
| AviHash | ~200 | ~3.0W | ~$0.27 | $0.0075 |
| AgentHash | ~91 | ~6.6W | ~$0.59 | $0.016 |
| CREHash | 52 | 11.5W | $1.03 | $0.029 |
| ClawHash | ~31 | ~19.4W | ~$1.74 | $0.048 |

Why ClawHash is most expensive: adversarial pairs require two LLM calls per pair (red team attack + blue team defense) using 27B+ models. Double the compute, double the energy.

## The Energy Finding (glass-wall)

From `22-glass-wall/FINDING_ENERGY.md`:

```
CONFIG 1: 27B Judge (the coma)
  Total: 202W, 0.7 pairs/min, 247W per deed
  THE CHAIN WAS IN A COMA

CONFIG 2: 4× 9B Judges (the heartbeat)  
  Total: ~80W per judge, 5.1 pairs/min, 16W per deed
  15x more efficient. Right-size the silicon.
```

**Standing rule**: efficiency is king. Don't run 27B when 12B handles it. Don't run 96GB when 32GB fits. The smallest model that agrees with the largest 90%+ of the time is your scale.

## GPU Clock Tuning (MINER discipline)

Training is memory-bandwidth bound (cores at 32%, memory at 95%).

```
OPTIMAL CLOCK SETTINGS (training):
  Core:   Let it throttle (~990-1100 MHz) — cores are waiting on memory
  Memory: PUSH TO MAX (14,001 MHz on Blackwell GDDR7)
  Power:  Cap to 80% nominal (300W → 240W, 200W → 160W)
  
  Memory clock IS the hashrate
  Core clock is wasted watts
```

Domain-specific flight sheets per domain-hash algorithm. Different domains have different compute profiles — ClawHash (two 27B models) burns more than LegalHash (two 12B models).

## Energy Tracking

```bash
# Real-time snapshot
python3 ~/google-gemma-4-FTW/edge/energy_tracker.py

# JSON output
python3 ~/google-gemma-4-FTW/edge/energy_tracker.py --json

# Record to DB
DATABASE_URL="..." python3 ~/google-gemma-4-FTW/edge/energy_tracker.py --record

# API (from anywhere)
curl -s https://swarmandbee.ai/deed/api/energy
```

## Electricity Rate

Default: $0.10/kWh (configurable via `ELECTRICITY_RATE` env var)

At $0.10/kWh and 500W average fleet draw:
- $0.05/hour fleet cost
- $1.20/day
- $36/month
- $432/year

That powers 23,500+ deeds, 19,791 lbs weighed. The energy cost of the entire operation is less than a single month of Claude API access for one OpenClaw agent.

## The Commodity Parallel

```
Bitcoin:  SHA-256 hashes per joule → price per BTC
Swarm:    Pairs weighed per joule → price per pound

Both: GPU time + electricity → digital asset
Both: measurable cost of production → market price
Both: energy IS the proof of work

Difference: we produce intelligence, not hashes
```

---

*Energy is evidence. The weight costs watts. The watts prove the work. Price per pound.*
