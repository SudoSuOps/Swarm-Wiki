# Tribunal-Hash Mining Pool API

2miners pattern applied to AI training data mining. Same API shape. Same economics. New asset class.

**Live**: `swarmandbee.ai/pool/api/`
**Source**: `/home/swarm/google-gemma-4-FTW/edge/pool_api.py`
**Port**: 9094 on swarmrails, proxied through nginx

## Endpoints

| Endpoint | 2miners Equivalent | Returns |
|----------|-------------------|---------|
| `GET /pool/api/stats` | `/stats` | Pool hashrate, miners, blocks, algorithms, energy |
| `GET /pool/api/blocks` | `/blocks` | Merkle batches (candidates/immature/matured) |
| `GET /pool/api/miners` | `/miners` | Active GPUs with power/temp/clocks/role |
| `GET /pool/api/payments` | `/payments` | Block reward pool from deed sales |
| `GET /pool/api/accounts/{gpu_id}` | `/accounts/{walletid}` | Per-GPU miner stats |
| `GET /pool/api/accounts/{gpu_id}/shares/{range}` | `/accounts/{walletid}/shares/{range}` | RJ/Honey/Propolis counts (5m/30m/6h) |

## Data Model Mapping

### 2miners → Tribunal-Hash

| Crypto Mining | AI Mining |
|--------------|-----------|
| Coin (ETC, KAS) | Algorithm (MedHash, CREHash) |
| Wallet ID | GPU ID (gpu0, gpu1, whale) |
| Worker | Judge instance (gemma3:12b, qwen2.5:7b) |
| Hashrate | Deeds scored per hour |
| Block | Merkle batch (50 deeds) |
| Block reward | Revenue from deed package sales |
| Valid share | Royal Jelly deed (score >= 0.75) |
| Stale share | Honey deed (0.50-0.74) |
| Invalid share | Propolis deed (< 0.50) |
| Difficulty | 100 - RJ yield % |
| Mining pool | Tribunal fleet (swarmrails + whale + edge) |
| Nonce | Score (0.00-1.00) |

### Algorithm Registry

| Algorithm | Domain | Difficulty | RJ Yield | Cost/1000 RJ |
|-----------|--------|-----------|----------|-------------|
| GrantHash | grants | 1.8 | 98.2% | $0.16 |
| LegalHash | legal | 1.9 | 98.1% | $0.08 |
| MedHash | medical | 14.7 | 85.3% | $0.26 |
| CREHash | cre | 53.9 | 46.1% | $1.03 |
| AvionHash | aviation | TBD | TBD | TBD |
| WikiHash | self_healing | TBD | TBD | TBD |

### Block Maturity (Merkle Batch Lifecycle)

| 2miners Status | Tribunal-Hash | Meaning |
|---------------|---------------|---------|
| candidate | Pending | < 50 deeds, batch not sealed |
| immature | Sealed | 50 deeds, Merkle root computed, not anchored |
| matured | Anchored | Merkle root submitted to Hedera HCS, immutable |

### Reward Distribution

When a deed package sells ($29-$199):

| Recipient | Share | Role |
|-----------|-------|------|
| Judge A GPU | 40% | Primary scorer |
| Judge B GPU | 30% | Cross-validator |
| Deed Recorder | 10% | Filing + Merkle |
| Infrastructure | 20% | NAS, networking, Hedera |

## Response Examples

### GET /pool/api/stats

```json
{
  "hashrate": 112,
  "hashrateUnit": "deeds/hr",
  "minersTotal": 3,
  "stats": {
    "totalDeeds": 23402,
    "totalBatches": 467,
    "lastBlockFound": 1775478528,
    "roundShares": 48
  },
  "algorithms": {
    "GrantHash": {"totalDeeds": 12336, "rjYield": 98.2, "difficulty": 1.8},
    "MedHash":   {"totalDeeds": 5038,  "rjYield": 85.3, "difficulty": 14.7},
    "CREHash":   {"totalDeeds": 1015,  "rjYield": 46.1, "difficulty": 53.9}
  },
  "fleet": {
    "totalWatts": 504.7,
    "costPerHour": 0.0505,
    "costPerDeed": 0.000045
  }
}
```

### GET /pool/api/miners

```json
{
  "miners": {
    "gpu0": {"name": "RTX PRO 6000 Blackwell", "power_w": 25, "role": "training", "offline": true},
    "gpu1": {"name": "RTX PRO 6000 Blackwell", "power_w": 150, "role": "judge_a", "core_mhz": 667, "mem_mhz": 13365},
    "whale": {"name": "RTX 3090", "role": "judge_b", "deeds_scored": 23410}
  },
  "minersTotal": 3
}
```

### GET /pool/api/blocks

```json
{
  "candidates": [{"pendingDeeds": 48, "targetSize": 50}],
  "immature": [{"id": "batch-7a8b9c...", "merkle_root": "abc123...", "leaf_count": 50, "status": "immature"}],
  "matured": [{"id": "batch-...", "hedera_topic": "0.0.10291838", "hedera_sequence": 721, "status": "matured"}]
}
```

### GET /pool/api/payments

```json
{
  "payments": [
    {"algorithm": "GrantHash", "rjDeeds": 12116, "packages": 12, "value_usd": 348},
    {"algorithm": "MedHash",   "rjDeeds": 4295,  "packages": 4,  "value_usd": 116}
  ],
  "totalValue": 580,
  "rewardModel": {"judgeA_pct": 40, "judgeB_pct": 30, "recorder_pct": 10, "infrastructure_pct": 20}
}
```

## Connection to Mining Concepts

### Satoshi Parallel

| Bitcoin | Tribunal-Hash |
|---------|--------------|
| CPU time + electricity → digital gold | GPU time + electricity → digital expertise |
| SHA-256 hashing → find nonce | Dual-judge scoring → find quality |
| Block = valid transactions | Block = 50 valid deeds |
| Merkle tree of transactions | Merkle tree of deeds (same algorithm) |
| Proof-of-Work | Proof-of-Location |
| 21M cap (scarcity) | RJ yield % (domain-specific scarcity) |

### Energy Economics

```
Pool power:      ~500W (gpu1 150W + whale 200W + edge 50W + cpu 100W)
Hashrate:        112 deeds/hr
Energy/deed:     4.46 Wh
Cost/deed:       $0.000446
Revenue/deed:    $0.029 (at $29/1000)
Margin:          98.5%
```

## Infrastructure

```
swarmandbee.ai/pool/api/ → nginx proxy → 192.168.0.91:9094
                                          ↓
                                    pool_api.py
                                    ├── PostgreSQL (deeds, batches, anchors)
                                    ├── nvidia-smi (live GPU stats)
                                    └── energy calculations
```

## Future: Fleet Expansion

When 100x RTX 3090 fleet comes online:

```
Current:   3 miners  |  112 deeds/hr  |  500W
Expanded:  53 miners | 19,000 deeds/hr | 15,000W
           50 judge pairs scoring in parallel
           163-day wall → 3.3 days
```

---

*2miners runs mining pools for crypto. We run mining pools for AI training data. Same API. Same economics. New asset class.*

*Mine the Location.*
