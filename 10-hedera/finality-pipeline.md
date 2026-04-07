# SwarmLedger — 5-Layer Finality Pipeline

**Status**: PRODUCTION — 23,500+ deeds filed, 477 Merkle batches sealed
**Principle**: A deed without finality is a JSONL file. With finality, it's a defendable asset.

## The 5 Layers

Every deed passes through 5 layers of finality. All 5 must be populated before a deed is considered final. The Swarm Inspector validates this.

```
LAYER 1: PostgreSQL (hot queries — mutable)
   │  deed record written to deeds table
   │  queryable, searchable, API-accessible
   │  swarmandbee.ai/deed/ reads from here
   ▼
LAYER 2: MinIO (versioned archive — immutable bucket)
   │  deed JSONL written to swarmdeed-finality bucket on NAS
   │  versioned — no overwrite, no delete
   │  local backup, fast retrieval
   ▼
LAYER 3: IPFS (public — CID-addressable)
   │  deed batch pinned to IPFS
   │  content-addressed — CID = hash of content
   │  anyone with the CID can retrieve and verify
   ▼
LAYER 4: Hedera HCS (consensus timestamp — immutable)
   │  Merkle root submitted to HCS topic 0.0.10291838
   │  aBFT consensus — publicly verifiable, permanent
   │  timestamp proves existence at that moment
   ▼
LAYER 5: ENS (permanent URL)
      swarmdeed.eth resolves to IPFS content
      human-readable, blockchain-permanent
      the address of the deed registry
```

## Deed Lifecycle

```
1. Pair enters bin (status: queued)
2. Tribunal weighs pair (status: scored → weighed)
   Scale A + Scale B, 2-pass, drift < 0.15
3. Deed recorder files deed (status: deeded)
   Weight, classification, scale reasoning, sealed timestamp
4. Batch of 50 deeds → Merkle tree
   SHA256 leaves, binary tree, root computed
5. Merkle root → Hedera HCS (topic 0.0.10291838)
   Consensus timestamp = finality
6. Batch → MinIO (swarmdeed-finality bucket)
7. Batch → IPFS (public pin)
8. Status: anchored — FINAL, permanent, verifiable
```

## Hedera Topics

| Topic | ID | Purpose |
|-------|----|---------|
| Block | 0.0.10291833 | Tribunal batch records |
| Receipt | 0.0.10291834 | Deed issuance confirmations |
| Event | 0.0.10291836 | Scale registrations (seq 715-721) |
| POE | 0.0.10291838 | Merkle root anchors — FINALITY |

Operator: 0.0.10291827 (mainnet)

## Merkle Tree Structure

- Leaves: SHA256 hash of each deed record
- Batch size: 50 deeds per tree
- Tree: binary Merkle tree
- Root: single SHA256 hash anchored to Hedera
- Proof: any leaf can prove membership via Merkle path

```
                    ROOT (anchored to Hedera)
                   /                          \
              H(AB)                            H(CD)
             /      \                        /      \
         H(A)      H(B)                  H(C)      H(D)
          |          |                    |          |
        deed_1    deed_2              deed_3      deed_4
```

## Verification Chain

Anyone can verify a deed:

```bash
# 1. Look up the deed
curl -s "https://swarmandbee.ai/deed/api/lookup?id=SB-2026-0406-00847"

# 2. Verify the Merkle proof
# Response includes: merkle_root, merkle_leaf_idx, merkle_path
# Recompute: hash the deed → walk the path → compare to root

# 3. Verify the Hedera anchor
# Response includes: hedera_topic, hedera_sequence
# Look up on hashscan.io — consensus timestamp proves existence

# 4. Verify the scales were base models
# Response includes: scale_a (model + version), scale_b (model + version)
# Download the same base model. Run the same pair. Compare weights.
```

This is the "validate the validator" protocol. Every step is reproducible.

## ENS Domains

13 ENS domains on IPFS:

| Domain | Purpose |
|--------|---------|
| swarmdeed.eth | Deed registry — permanent URL |
| swarmgraph.eth | Provenance graph |
| swarmchain.eth | Block explorer |
| swarmprotocol.eth | Protocol spec |
| swarmtitle.eth | Title insurance |
| swarmshop.eth | Weight shop |
| swarmbuilder.eth | Custom cook |
| defendable.eth | Thesis |
| swarmos.eth | Operating system |
| swarmdev.eth | Developer tools |
| swarmledger.eth | Ledger |
| swarmepoch.eth | Epoch records |
| swarmenergy.eth | Energy dashboard |

## Infrastructure

| Component | Location | Role |
|-----------|----------|------|
| deed_recorder.py | Zima Edge (.230) | Files deeds, builds Merkle trees, polls every 30s |
| hedera_anchor.js | swarmrails | Submits Merkle roots to HCS mainnet |
| export_ledger.py | swarmrails | Exports full ledger for audit |
| MinIO | NAS (.102:9000) | swarmdeed-finality bucket, versioned |
| IPFS | NAS (.102) | Public pins, CID-addressable |
| PostgreSQL | NAS (.102:5433) | deeds + batches + anchors tables |

## Standing Rules

1. **All 5 layers** must be populated before a deed is final
2. **Merkle roots are immutable** — once anchored, the batch is sealed
3. **Hedera is the clock** — consensus timestamp is the moment of truth
4. **No backdating** — timestamp manipulation is a permit violation
5. **Inspector validates** — Swarm-Inspector checks all 5 layers on every audit

---

*PostgreSQL for speed. MinIO for backup. IPFS for access. Hedera for proof. ENS for permanence.*
*Five layers. One truth. Every deed.*
