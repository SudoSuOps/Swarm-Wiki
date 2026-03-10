# SwarmAtlas-27B

CRE capital markets intelligence model. The production evolution of SwarmCapitalMarkets-27B. Covers IC memos, waterfall distributions, stress testing, debt analysis, equity structuring, and kill/defend decisions. Deployed on Blackwell, API-accessible at `api.swarmandbee.ai`.

## Lineage

SwarmCapitalMarkets-27B was the training name. Once it hit production with verified IC memo output quality, it was renamed **SwarmAtlas-27B** — the public-facing CRE intelligence engine.

Same weights. Same checkpoint. New identity for the product layer.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-27B Dense |
| Architecture | 64 layers, 5120 hidden dim, all 27B parameters active |
| Attention | GDN (75%) + Standard (25%), block pattern: 3 GDN + 1 Attn |
| Vocabulary | 248,320 tokens |
| Context | 16,384 (serving) / 262K native |
| Training method | bf16 LoRA r=64 alpha=32 |
| Training pairs | 45,039 train / 500 eval |
| Steps | 844 (full run, 0.6 epoch) |
| Train loss | 0.4186 |
| Eval loss | 0.2238 (final checkpoint) |
| Training time | 29.32 hours on RTX PRO 6000 Blackwell |
| Config source | SwarmCurator-27B-v1 Gold Standard |
| Merged checkpoint | swarmrails:/data2/swarmcapitalmarkets/merged/ |

## Loss Curve

Clean convergence, beating the Curator-27B reference build (0.477):

| Step | Train Loss | Eval Loss | Epoch |
|------|-----------|-----------|-------|
| 10 | 1.051 | — | 0.007 |
| 50 | 0.742 | — | 0.071 |
| 100 | 0.598 | — | 0.114 |
| 150 | 0.525 | — | 0.135 |
| 200 | 0.522 | 0.533 | 0.142 |
| 400 | ~0.47 | 0.269 | 0.284 |
| 600 | ~0.29 | 0.227 | 0.426 |
| 800 | ~0.27 | 0.224 | 0.568 |
| 844 | 0.266 | — | 0.600 |

**Aggregate train_loss: 0.4186** (SFTTrainer reports running average across all steps).

Final eval loss 0.2238 shows strong generalization — no overfitting. The model learned the domain deeply while maintaining flexibility on unseen prompts.

## Training Data Assembly

5-pool assembly with intentional diversity weighting:

| Pool | Share | Pairs | Content |
|------|-------|-------|---------|
| Diversified | 60% | ~27,000 | Broad capital markets: CMBS, rate advisory, equity structuring, valuation |
| RPA (Risk-Parity Augmented) | 25% | ~11,200 | Risk-weighted scenarios, stress tests, tail events |
| Macro + Graph | 8% | ~3,600 | Macroeconomic causality chains, deal relationship graphs |
| Golden | 4% | ~1,800 | Hand-verified exemplars from production signals |
| Mutations | 3% | ~1,400 | Deliberately perturbed scenarios to test robustness |

### 8 Cook Streams

| Stream | Content |
|--------|---------|
| debt_maturity | Loan maturity analysis, refinancing risk, prepayment scenarios |
| cmbs_distress | CMBS loan watchlist, special servicing, workout analysis |
| rate_advisory | Interest rate hedging, swap analysis, rate lock recommendations |
| equity_advisory | Equity raise structuring, LP/GP splits, promote waterfalls |
| valuation_advisory | DCF, direct cap, sales comparison across asset classes |
| deal_origination | Deal sourcing, relationship mapping, pipeline management |
| macro_causality | Fed policy impact chains, yield curve analysis, recession indicators |
| deal_graph | Multi-party deal structures, entity relationships, capital stack mapping |

## Reasoning Tiers

Atlas operates across four reasoning complexity tiers, tested via the Memphis IC scenario (312-unit Class B multifamily, distressed debt fund structure):

| Tier | Capability | Example |
|------|-----------|---------|
| **Bronze** | NOI calculation, cap rate derivation | Stabilized NOI from rent roll + expenses → cap rate |
| **Silver** | Rent roll analysis, occupancy modeling | Vacancy drag, loss-to-lease, concession burn-off |
| **Gold** | Waterfall distribution, refi analysis, capital stack | LP/GP splits, promote hurdles, exit proceeds allocation |
| **Platinum** | Stress testing, IC recommendation, kill/defend | Multi-scenario comparison, structural flaw identification |

### Memphis IC Validation (Production Test)

Full IC memo stress test — 312-unit Class B Memphis MF, $14.2M basis, 80% LTC bridge at 8.35%, 36-month hold, value-add thesis:

- **12/12 math calculations correct** (zero errors)
- **Model independently identified the deal-killing structural flaw**: At realistic 5.75% exit cap, leverage compression (80% LTC in → 65% LTV out) combined with 8.35% bridge carry makes the deal structurally dead. LP doesn't clear 8% pref.
- **Added 5% soft cost buffer** not explicitly in the prompt — institutional underwriting standard the model learned from training data
- **Verdict: NUKED** — correct kill decision with full quantitative justification
- **Output: 10,220 tokens**, finish_reason: stop (complete formatted output)

## Deployment

**Production**: vLLM 0.17.0 on swarmrails port 8082, GPU1 (RTX PRO 6000 Blackwell, 96GB VRAM).

```
Model name:     swarm-atlas-27b
vLLM endpoint:  http://swarmrails:8082/v1/chat/completions
Public API:     https://api.swarmandbee.ai/v1/chat/completions
Gateway model:  swarm/atlas-27b
Throughput:     88 tok/s at 4 concurrent requests
VRAM usage:     ~93GB bf16
Context:        16,384 tokens (max_model_len)
Max sequences:  4 concurrent
```

### Inference Tunnel Chain

```
Client
  → api.swarmandbee.ai (Cloudflare Worker, openai.js)
    → inference.swarmandbee.ai (Cloudflare Tunnel)
      → swarmrails:4000 (Python FastAPI gateway)
        → swarmrails:8082 (vLLM, swarm-atlas-27b)
```

### Auth

Two key types accepted:
- `sk_swarm_*` — pass-through (internal/legacy keys, no metering)
- `sb_live_*` — wallet-metered keys (Supabase credit check, 5 credits/call)

### Launch Script

`/tmp/start_atlas_16k.sh` on swarmrails:

```bash
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 \
python -m vllm.entrypoints.openai.api_server \
  --model /data2/swarmcapitalmarkets/merged \
  --served-model-name swarm-atlas-27b \
  --host 0.0.0.0 --port 8082 \
  --dtype bfloat16 \
  --max-model-len 16384 \
  --max-num-seqs 4 \
  --gpu-memory-utilization 0.92 \
  --enforce-eager \
  --skip-mm-profiling \
  --limit-mm-per-prompt '{"image": 0}'
```

Required config fix: Copy `vision_config` from base Qwen3.5 model into merged config.json (`out_hidden_size` must match text hidden_size). Unsloth merge artifact.

## Think Mode Behavior

Qwen3.5 has think mode ON by default. Atlas produces "Thinking Process:" reasoning chains before formatted output. Key implications:

1. **IC memos need 16K context**: Thinking traces consume 6-8K tokens before the formatted output begins. With max_tokens < 10K, output gets truncated.
2. **max_tokens: 12000** is the sweet spot for full IC memos with waterfall tables and stress test comparisons.
3. **Short prompts still work**: Simple questions (cap rate definitions, single calculations) complete fine at 150-500 tokens.
4. **Cannot be disabled via prompt engineering**: "No thinking" in system prompt doesn't work. The CoT is baked into training data, not controlled by chat template.
5. **`enable_thinking: false`** in extra_body also doesn't suppress it for this model.

## Sampling Parameters

### IC Memo / Deep Analysis Mode
For waterfall distributions, stress tests, multi-section IC memos:

```json
{
  "temperature": 1.0,
  "top_p": 0.95,
  "max_tokens": 12000
}
```

### Quick Analysis Mode
For single calculations, market snapshots, quick opinions:

```json
{
  "temperature": 0.7,
  "top_p": 0.8,
  "max_tokens": 2000
}
```

## Product Page

Live at [swarmandbee.ai/capital](https://swarmandbee.ai/capital). Dark terminal aesthetic with gold accents. Shows:

- Model specifications and training badges
- Four reasoning tier visualization (Bronze → Platinum)
- Live Memphis IC proof (12 metrics from the stress test)
- NUKED verdict callout
- Example prompts
- Waitlist signup

## Relationship to Fleet

Atlas replaces SwarmCurator-27B on port 8082. It serves the same architectural role (strategic layer, Blackwell GPU1) but is specialized for capital markets intelligence rather than general curation.

The Python gateway (`/data2/swarm-vllm/openai_server/models.py`) maps both `swarm/atlas-27b` and `swarm/curator-27b` to port 8082 — backward compatibility for any existing integrations.

```
Strategic Layer:  SwarmAtlas-27B (Blackwell 96GB) ← YOU ARE HERE
Operational:      SwarmCurator-9B (RTX PRO 4500 32GB)
Edge:             SwarmCurator-2B / SwarmSignal-2B
Router:           BeeMini v2 (GGUF)
```
