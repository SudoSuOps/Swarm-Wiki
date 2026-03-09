# Hedera Ecosystem

Swarm & Bee's trust and provenance layer. Hedera Hashgraph provides immutable audit trails (HCS) and tokenized asset classes (HTS) for the entire intelligence pipeline.

## Mainnet Resources

| Resource | IDs | Purpose |
|----------|-----|---------|
| HNS | swarmandbee.hbar | Hedera Name Service |
| Operator | 0.0.10291827 (ECDSA) | Mainnet operations |
| 5 HCS Topics | Block .10291833, Receipt .10291834, Event .10291836, PoE .10291838, Escrow .10294205 | Immutable audit trails |
| 5 HTS Tokens | Block .10291839, Pair .10291840, Model .10291842, Deed .10291843, Dataset .10291844 | Tokenized asset classes |
| 8 Agents | med, health, aviation, cre, compute, appliance, broker, capital | On-chain identities |
| CRE Broker | 0.0.10298834 | Dedicated account + topics |
| AI Studio Agent | d78a1a60-0e72-11f1-9576-fb6407340b5d | PASETO v4 token |

## Sections

- [Mainnet Deployment](mainnet.md) — HCS topics, HTS tokens, operator accounts
- [Agents](agents.md) — 8 registered agents with account IDs
- [Bridge](bridge.md) — Merkle tree to HCS publish to guarantee.json
- [Tokenization](tokenization.md) — ATS, ERC-1400, RedSwan, HIP-991
