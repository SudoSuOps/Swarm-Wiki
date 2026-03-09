# Mainnet Deployment

## HCS Topics (Immutable Audit Trails)

| Topic ID | Name | Purpose |
|----------|------|---------|
| 0.0.10291833 | Block | Genesis block records |
| 0.0.10291834 | Receipt | Transaction receipts |
| 0.0.10291836 | Event | Market events, signal timestamps |
| 0.0.10291838 | PoE | Proof of Execution |
| 0.0.10294205 | Escrow | Escrow state transitions |

## HTS Tokens (Tokenized Asset Classes)

| Token ID | Name | Asset Class |
|----------|------|-------------|
| 0.0.10291839 | Block | Genesis blocks |
| 0.0.10291840 | Pair | Training pairs |
| 0.0.10291842 | Model | Model artifacts |
| 0.0.10291843 | Deed | Intelligence Object deeds |
| 0.0.10291844 | Dataset | Dataset collections |

## Accounts

| Account | Type | Purpose |
|---------|------|---------|
| 0.0.10291542 | ED25519 | HNS owner (swarmandbee.hbar) |
| 0.0.10291827 | ECDSA | Mainnet operator |
| 0.0.10298834 | — | CRE Broker Agent (dedicated) |

### Testnet

| Account | Type | Balance |
|---------|------|---------|
| 0.0.7974929 | ECDSA | 879 HBAR |
| 0.0.7974075 | ED25519 | 1,000 HBAR |

## Fee Schedule

| Operation | USD | Notes |
|-----------|-----|-------|
| ConsensusCreateTopic | $0.01 | One-time per topic |
| ConsensusSubmitMessage | $0.0008 | Was $0.0001, 8x increase Jan 2026 |
| TokenCreate (HTS) | $1.00 | One-time per token type |
| TokenTransfer | $0.001 | Per transfer |
| CryptoTransfer (HBAR) | $0.0001 | Cheapest operation |
| ContractCreate | $1.00 | Smart contract deploy |

- Fees are USD-denominated, converted to HBAR at tx time
- Fixed pricing (not gas-based) — no congestion surcharges
- HCS 1,024-byte message limit — need chunking for large payloads
- Our guarantee publishes: ~$0.0008 each, 11.7 HBAR covers 14,600+ publishes

## Hedera Platform Context (2026-03)

- Governing Council: Google, IBM, Dell, FedEx, Deutsche Telekom, LG, Repsol
- DeFi TVL: $208M+, Agent Economy: $470M+ GDP
- Cross-chain: Axelar bridge to 60+ chains
- Open source: Project Hiero under Linux Foundation Decentralized Trust
- HashSphere: private Hedera for regulated enterprise
