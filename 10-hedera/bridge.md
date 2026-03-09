# Hedera Bridge

Three-file architecture for provenance sealing: Merkle tree construction, HCS publication, guarantee generation.

## Pipeline

```
Training Pairs -> Merkle Tree -> SHA-256 Root Hash -> HCS Publish -> guarantee.json
```

## Components

### 1. merkle.py (`data/factory/merkle.py`)

Builds a Merkle tree from training pairs:
- Input: JSONL file of pairs
- Process: SHA-256 hash each pair, build binary tree
- Output: Merkle root hash + tree structure

### 2. hedera_bridge.py (`data/factory/hedera_bridge.py`)

Publishes the Merkle root to HCS:
- Takes Merkle root hash + metadata
- Publishes to PoE topic (0.0.10291838)
- Returns transaction ID + consensus timestamp
- Cost: $0.0008 per publish

### 3. guarantee.py (`data/factory/guarantee.py`)

Generates the provenance guarantee document:
- Combines: Merkle root, HCS transaction ID, consensus timestamp, dataset metadata
- Output: `guarantee.json` with full on-chain provenance
- Verifiable: Anyone can check the HCS topic for the published hash

## Cost Analysis

- ~$0.0008 per HCS message
- 11.7 HBAR covers 14,600+ publishes
- ~100 signals/day = $0.08/day = $2.40/month for signal timestamping

## Signal Timestamping

For P1-P3 market signals:
1. Hash each signal with SHA-256
2. Publish hash to Event topic (0.0.10291836)
3. Full signal stays in R2 — only hash goes on-chain (1,024-byte limit)
4. Proves when we detected a market signal (no backdating)
