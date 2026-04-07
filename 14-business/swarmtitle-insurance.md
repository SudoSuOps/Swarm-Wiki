# SwarmTitle — Title Insurance for AI Training Data

**Status**: LIVE at swarmandbee.ai/title
**Principle**: In CRE, every property has a title search, an inspection, and insurance. AI training data should work the same way.

## The CRE Parallel

| Real Estate | SwarmTitle |
|-------------|-----------|
| Title search | Provenance check — where did this pair come from? |
| Property inspection | Dual-scale tribunal — two independent base models weigh the pair |
| Appraisal | Weight classification — Royal Jelly, Honey, or Propolis |
| Title commitment | Flight sheet — all settings frozen, permit issued |
| Closing statement | Actual vs estimated — honest accounting |
| Title insurance | SwarmTitle — the guarantee that the deed is valid |
| Recording | Hedera HCS — permanent, public, immutable |

## Independence — Separation of Concerns

SwarmTitle is the independent certifier. It does NOT:
- Generate pairs (that's the cook)
- Run the tribunal (that's the scales)
- Write deeds (that's the deed writer)
- Anchor to blockchain (that's the recorder)

It DOES:
- Verify the scales are base models (unmodified)
- Verify the flight sheet hash matches execution
- Verify the Merkle proof is valid
- Verify the Hedera anchor exists
- Verify all 5 finality layers are populated
- Issue the title insurance certificate

The certifier is separate from production. Same principle as a title company being independent from the buyer, seller, and lender.

## Eight Integrity Layers (Swarm-Inspector)

| Layer | What's Checked | Fail = |
|-------|---------------|--------|
| 1. Deed | Does the deed record exist with all required fields? | VOID |
| 2. Scale | Were both scales base models from approved list? | VOID |
| 3. Permit | Was a flight sheet approved before execution? | VOID |
| 4. Weight | Does the weight classification match the consensus weight? | RECLASSIFY |
| 5. Merkle | Does the Merkle proof validate against the batch root? | VOID |
| 6. Anchor | Does the Hedera topic contain the Merkle root? | UNANCHORED |
| 7. Storage | Is the deed in MinIO + IPFS + PostgreSQL? | INCOMPLETE |
| 8. Protocol | Were all standing rules followed (2-pass, drift, etc.)? | FLAGGED |

## Title Premium

The title premium is included in the price per pound. It covers:
- Independent verification of every deed in the batch
- Swarm-Inspector 8-layer audit
- Certificate of authenticity
- Permanent on-chain record of the insurance

Not a separate charge. Built into the cost to mint. The insurance IS the product.

## Registered Scales

Scales are registered on Hedera at deployment. The registration proves:
- Model identity (name, version, parameter count)
- Hardware assignment (GPU, VRAM, architecture)
- Base model verification (unmodified from published state)
- Registration sequence number (immutable on-chain)

| Scale | Model | Hardware | Hedera Seq |
|-------|-------|----------|-----------|
| Scale A | gemma3:12b | RTX PRO 4500 Blackwell 32GB | 715 |
| Scale B | qwen2.5:32b | RTX PRO 6000 Blackwell 96GB | 716 |

Source: `swarm.yaml` → `scales`

## Five Proofs Per Deed

Every deed carries five proofs. Without them it's a JSONL file. With them it's an insured asset.

| Proof | What It Proves |
|-------|---------------|
| 1. Origin | Which model generated it, on what hardware, with what strategy |
| 2. Quality | Deterministic weight from two independent scales — not opinion |
| 3. Process | Full lineage: tried, failed, survived. The journey is the proof. |
| 4. Economics | Energy cost, price per pound. The weight costs watts. |
| 5. Trust | Hedera HCS anchor, Merkle root. Permanent, public, verifiable. |

## Certification Process

```
1. SCOPE        Client defines domain, volume, quality requirements
2. CALIBRATION  50 pairs weighed — real metrics, real cost
3. PERMIT       Flight sheet frozen, SHA256 hash, client approval
4. PRODUCTION   Tribunal runs under permit — gate reports at 25/50/75/100%
5. INSPECTION   Swarm-Inspector validates all 8 layers
6. CLOSING      Actual vs estimated — honest accounting
7. DELIVERY     ZIP: pairs + deeds + OM + quality report + closing + insurance cert
```

## Model Agnostic

The buyer selects the base model. The protocol certifies the weight. SwarmTitle doesn't care if you cook on Gemma, Qwen, Llama, or Mistral — the certification process is the same. The scales weigh. The inspector validates. The deed records. The blockchain anchors.

## On-Chain Infrastructure

| Resource | Address | Purpose |
|----------|---------|---------|
| POE Topic | 0.0.10291838 | Merkle root finality — the moment of truth |
| Block Topic | 0.0.10291833 | Tribunal batch records |
| Receipt Topic | 0.0.10291834 | Deed issuance confirmations |
| Event Topic | 0.0.10291836 | Scale registrations |
| Operator | 0.0.10291827 | Mainnet signing authority |
| ENS | swarmdeed.eth | Permanent deed registry URL |
| ENS | swarmtitle.eth | Permanent title insurance URL |

---

*Every property has a title search. Every AI dataset should too.*
*SwarmTitle: the independent certifier. The insurance IS the product.*
