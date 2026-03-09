# Tokenization

## Asset Tokenization Studio (ATS)

Open-source toolkit for tokenized securities on Hedera. Apache 2.0.

### Architecture

- **ERC-1400** standard (+ ERC-1410, 1594, 1643, 1644)
- Factory Contract: deploys bonds/equities via `deployBond`, `deployEquity`
- Resolver Contract: routes operations to logic modules
- Proxy Contract: diamond proxy pattern, upgradeable
- 2 smart contracts per tokenization
- Audited by A&D Forensics
- Web UI: https://tokenization-studio.hedera.com

### Compliance Modules

| Module | Function |
|--------|----------|
| Access Control | Role-based (Minter, Controller) |
| Control List | Whitelist/blocklist for KYC/AML |
| Supply Cap | Max token supply enforcement |
| Pause | Freeze all transfers (audit/security) |
| Lock | Address/token freeze (vesting, escrow) |
| Snapshots | Balance capture (dividends, voting, audits) |

### Regulatory: SEC Reg D (506-b, 506-c), Regulation S, external KYC, optional ERC-3643

## RedSwan CRE — The Precedent

RedSwan (CEO: Ed Nwokedi, ex-Cushman & Wakefield) is THE CRE tokenization case study on Hedera.

| Metric | Value |
|--------|-------|
| Tokenized assets | $5B+ |
| Target (36 months) | $25B |
| Investors | 13,000 |
| Active funds | 3 (USA, Africa, GCC) |
| Min investment | $1,000 |
| Token standard | HTS native (KYC/AML built-in) |

### Swarm vs RedSwan

- **RedSwan** = tokenize the ASSET (property ownership fractions)
- **Swarm** = tokenize the INTELLIGENCE (underwriting, analysis, deal data)
- Not competing — complementary. RedSwan needs underwriting models -> SwarmCRE-35B

## HIP-991: Revenue-Generating Topics

- Permissionless fixed-fee system for topic message submissions
- Topic operators can set custom fees for message submission
- **Swarm opportunity**: Charge per intelligence object publish, per signal timestamp
- Status: On testnet v0.59, heading to mainnet

## EQTY Labs — Verifiable AI Compute

- Hardware-attested AI computation proofs (NVIDIA Blackwell TEE-I/O)
- SLSA Level 3 certification
- Every AI computation logged to HCS
- **Swarm opportunity**: Our Blackwell training runs could get on-chain attestation. Model provenance from silicon to seal.

## Revenue Opportunities

1. **IO API**: Charge per Intelligence Object via wallet metering (already built)
2. **HIP-991 Fees**: Custom fees on HCS topics for signal/seal reads
3. **Deed Tokens**: Mint HTS Deed tokens for verified CRE intelligence
4. **Compute Attestation**: EQTY-style proofs for training runs
5. **Agent Economy**: 8 registered agents transacting HBAR for services
