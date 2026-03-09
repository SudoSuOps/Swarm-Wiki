# api.swarmandbee.ai — The Operating System of Sovereign AI Compute

## The Architecture

```
                    api.swarmandbee.ai
                         │
            ┌────────────┴────────────┐
            │                         │
       Auth Layer               Swarm Router
            │                         │
            │                ┌────────┴────────┐
            │                │                 │
         Billing        vLLM Inference     Pair Factory
            │                │                 │
            │                │                 │
         SwarmLedger     GPU Clusters      Dataset Vault
            │                │                 │
            └─────── Edge Nodes / Agents ──────┘
```

One domain. Six control planes. Everything behind one auth layer.

## What It Controls

### 1. Models

Every trained model in the fleet is accessible through the API. Not just inference — the full lifecycle.

| Capability | What It Does |
|------------|-------------|
| **Inference** | Route queries to the right model (2B/9B/27B/35B) based on complexity |
| **Model Registry** | Track every model version, training run, merge, quantization |
| **Deployment** | Push models to GPU clusters, edge nodes, or serverless |
| **Evaluation** | Run eval suites against any model, compare generations |

Current fleet behind the API:
- SwarmCurator-27B (96GB Blackwell, 88 tok/s x4)
- SwarmCurator-9B (32GB Blackwell, 165 tok/s x4)
- SwarmCurator-2B (edge/mobile)
- SwarmPharma-35B (pharma vertical)
- SwarmCapitalMarkets-27B (training now — step 282/844)
- SwarmCRE-35B (next build)
- BeeMini Router (1.8GB, routing decisions)
- CF AI edge models (Qwen3-30B, Llama-3B — zero-cost inference)

### 2. Datasets

1.16M verified training pairs across 5 verticals. The API controls access, sampling, cooking, and commerce.

| Vertical | Pairs | Bucket |
|----------|-------|--------|
| CRE | 643K | sb-cre |
| Medical | 432K | sb-medical |
| Aviation | 45K | sb-aviation |
| Core | 31K | sb-core |
| Drone | 6.8K | sb-drone |

API operations:
- `GET /catalog` — browse available datasets by vertical/specialty/tier
- `GET /sample` — preview pairs before purchasing
- `POST /pull` — download pairs (quota-enforced per API key tier)
- `POST /cook` — order custom pair generation (async, billed per pair)
- `GET /count` — real-time inventory across all buckets

Every pair traceable back to its source signal, cook script, quality gate results, and (optionally) Hedera hash.

### 3. Nodes

The physical compute infrastructure — GPU clusters, edge devices, serverless providers — all managed through one control plane.

```
GPU Cluster (swarmrails)
├── GPU 0: RTX PRO 4500 Blackwell (32GB) — inference or training
├── GPU 1: RTX PRO 6000 Blackwell (96GB) — inference or training
└── 128GB combined VRAM, Xeon w9-3475X 36C/72T, 256GB DDR5

Remote Node (whale)
├── RTX 3090 (24GB) — inference or cooking
├── Intel X540-AT2 10G NIC (pending cable)
└── Ryzen 9 5900X, 64GB DDR4

Edge Nodes
├── signal-edge-01: Jetson Orin Nano 8GB — signal classification
├── zima-edge-1: Intel N150 — signal + MinIO + tunnel
└── BeeMini/BeePro/BeeRack (hardware product line)

Serverless
├── Together.ai: Qwen-80B (gen), Qwen-235B (pass/RPA)
└── Cloudflare AI: Qwen3-30B, Llama-3B, BGE-Base embeddings
```

The API knows what's running where, what's available, and routes accordingly. When GPU 1 is training SwarmCapitalMarkets-27B, inference routes to GPU 0 or serverless. When training finishes, the new model deploys and the API starts routing to it.

### 4. Agents

8 registered Hedera agents with on-chain identities. Each agent has capabilities, an account ID, and can operate autonomously.

| Agent | Account | Capabilities |
|-------|---------|-------------|
| swarm-med | Registered | Medical intelligence, drug interactions |
| swarm-health | Registered | Health data processing |
| swarm-aviation | Registered | Aviation compliance, MRO |
| swarm-cre | Registered | CRE underwriting, deal analysis |
| swarm-compute | Registered | GPU orchestration, job scheduling |
| swarm-appliance | Registered | Edge device management |
| swarm-broker | 0.0.10298834 | CRE brokerage deal machine |
| swarm-capital | Registered | Capital markets analysis |

The API is the agent bus. Agents register, authenticate, receive tasks, report results, and get paid — all through `api.swarmandbee.ai`.

### 5. Billing

Three revenue streams, one billing layer.

| Stream | Mechanism | Price Points |
|--------|-----------|-------------|
| **Subscriptions** | Stripe recurring | $20/mo (Curator), $49/mo (Full Access), Enterprise |
| **Per-IO metering** | `sb_live_` API keys + credit wallet | $0.0002/Intelligence Object |
| **Data commerce** | Quota-enforced pull + cook orders | Per-pair pricing by tier |

API key format: `sk_swarm_{tier}_{random}` — stored in R2, quota tracked in Supabase, usage logged per-call.

The billing layer doesn't just charge — it enforces. Every API call checks:
1. Valid key exists
2. Quota not exhausted
3. Tier permits the requested operation
4. Usage logged for invoicing

### 6. Compute Proofs (SwarmLedger)

This is where sovereign AI compute becomes provable.

```
Training run completes
  → Merkle tree of training pairs (merkle.py)
  → SHA-256 root hash
  → HCS publish to PoE topic (0.0.10291838)
  → guarantee.json with on-chain provenance
  → HTS token minted (Dataset 0.0.10291844)

Inference request served
  → Response + model version + timestamp
  → Hash to HCS Receipt topic (0.0.10291834)
  → Verifiable proof that THIS model produced THIS output at THIS time

Intelligence Object created
  → Full provenance chain: signal → cook → gate → promote → seal
  → HCS Event topic (0.0.10291836)
  → Immutable audit trail
```

Every model, every dataset, every inference — provable on Hedera mainnet. This is not theoretical. The bridge is built (`merkle.py` → `hedera_bridge.py` → `guarantee.py`). The topics exist. The tokens exist.

## Why This Is Different

The market has:
- **Model APIs** (OpenAI, Anthropic, Together) — inference only, no data, no provenance
- **Dataset platforms** (HuggingFace, Scale) — data only, no inference, no billing
- **Compute marketplaces** (Lambda, CoreWeave) — raw GPUs, no intelligence
- **Blockchain AI** (Bittensor, Render) — tokens first, models second

Nobody has all six under one roof:

```
Models + Datasets + Nodes + Agents + Billing + Compute Proofs
                         =
        Sovereign AI Compute Operating System
```

**Sovereign** because: you control your models (trained on your data), your data (verified by your gates), your compute (your GPUs), your proofs (your Hedera topics). No vendor lock-in. No data leaving the network unless you sell it.

## The Convergence

Today these are separate systems:
- `router.swarmandbee.com` — 69 endpoints (intelligence engine)
- `api.swarmandbee.com` — 14 endpoints (commerce + medical)
- Python curator middleware — bridges to GPU fleet
- Hedera bridge — provenance layer

Tomorrow they converge into `api.swarmandbee.ai`:

```
api.swarmandbee.ai
├── /v1/inference/*      — Model routing + execution
├── /v1/data/*           — Dataset catalog, pull, cook, sample
├── /v1/skills/*         — 28+ composable AI skills
├── /v1/events/*         — Market intelligence event stream
├── /v1/memory/*         — Semantic search + context
├── /v1/agents/*         — Agent registration, tasks, results
├── /v1/nodes/*          — Cluster status, job scheduling
├── /v1/billing/*        — Keys, credits, usage, invoices
├── /v1/ledger/*         — Hedera proofs, guarantees, tokens
└── /v1/health           — System-wide health + metrics
```

One API. One auth. One billing. Full stack.

## Proof-of-Compute Alignment

The Hedera integration isn't a marketing feature — it's the core differentiator.

| Traditional AI API | api.swarmandbee.ai |
|---|---|
| "Trust us, it's GPT-4" | Verifiable model hash on HCS |
| "We trained on internet data" | Every training pair traced to source signal |
| No provenance | SHA-256 merkle root on mainnet |
| Opaque pricing | Per-IO metering with on-chain receipts |
| Vendor-locked | Sovereign: your models, your data, your GPUs |

When a customer pulls 10K CRE training pairs:
1. API authenticates + checks quota
2. Pairs delivered from R2
3. Merkle root of delivered pairs published to HCS
4. Customer gets `guarantee.json` — cryptographic proof of exactly what was delivered
5. HTS Dataset token tracks the transaction

This is Proof-of-Compute. Not proof that compute happened somewhere. Proof that THIS compute, on THESE pairs, produced THIS result, verified by THESE gates, at THIS time.

## Implementation Path

| Phase | Scope | Dependencies |
|-------|-------|-------------|
| **Now** | Two workers + Python curator + Hedera bridge | All operational |
| **Next** | Cloudflare Tunnel (swarmrails → CF) | cloudflared config |
| **Then** | Unified `api.swarmandbee.ai` worker | Merge router + api workers |
| **After** | Agent bus + node management | Agent SDK + fleet orchestrator |
| **Target** | Full sovereign compute OS | All 6 control planes unified |

The infrastructure exists. The models are trained. The data is verified. The proofs are on mainnet. What remains is convergence — collapsing the separate systems into one API surface that makes the whole network accessible through a single domain.
