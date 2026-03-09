# Products In Development

## Active Products

### SwarmScaler (api.swarmandbee.ai)

**Status**: IN DEVELOPMENT

API scaling layer at `api.swarmandbee.ai`. Manages fleet scaling, load balancing, and metered access to SwarmCurator inference endpoints.

### SwarmCRE App Store (swarmandbee.ai/app-store)

**Status**: IN DEVELOPMENT

Voice + text app store for CRE brokers. Desktop appliance + mobile app. On-device inference (4B phone, 9B desktop).

**Vision** (Phase 5 — "The Deal Machine in Every Broker's Pocket"):
```
"Hey Swarm, pull comps for 50K SF cold storage in DFW"
  -> comp_analyzer skill -> 3 comps with $/SF, cap rates
  -> underwriting_calc -> NOI, DSCR, LTV
  -> ic_memo skill -> full IC memorandum
  -> email_composer -> send to team
  -> HCS seal -> timestamped intelligence object
```

**Tiers**: Free (5 queries/day), Pro ($20-49/mo), Enterprise (dedicated 35B)

### SwarmMed

**Status**: IN DEVELOPMENT (data live)

Medical AI product. 434,882 verified medical training pairs across 92 specialties. 8-step SwarmCurator pipeline. CoVe verification by 235B model. Platinum-tier quality.

**Product page**: `swarmbeeai-factory/swarmmed.html`

### SwarmPharma

**Status**: IN DEVELOPMENT (model trained)

Pharmacology-focused AI. SwarmPharma-35B trained (25.6K pairs, 2,402 steps, loss 0.337). 16 task types, 5-step trajectory. Drug interactions, DDI prediction, clinical pharmacology.

**Model**: `swarmrails:/data2/swarmpharma-35b/`
**Product page**: `swarmbeeai-factory/swarmpharma.html`

### SwarmAviation

**Status**: IN DEVELOPMENT (data live)

Aviation AI. 45,222 verified pairs, 50+ specialties. Safety compliance, flight ops, pilot training, MRO, ATC. CoVe-promoted platinum-tier quality.

**Product page**: `swarmbeeai-factory/swarmaviation.html`

## Hardware Products (Roadmap)

From `swarm-bee/LASTMILE_BLUEPRINT.md`:

| Product | Hardware | VRAM | Power | Price | Models |
|---------|----------|------|-------|-------|--------|
| BeeMini | Jetson Orin Nano Super | 8GB | 10W | $249 | 4B |
| BeePro | Jetson Orin NX | 16GB | 40W | $599 | 9B multi-agent |
| BeeRack | RTX PRO 6000 Blackwell | 96GB | 350W | $3,500/mo | 14B-32B |

Offline-first, always-on, DIN-rail mount. Data never leaves device. FDA 21 CFR Part 11, HIPAA, ITAR compliant.

## Model Exploration

### OpenRouter

**Status**: EXPLORING — audit needed

OpenRouter (`openrouter.ai`) being evaluated as alternative/supplementary LLM API provider alongside Together.ai. No integration code exists yet. Audit required for:
- Model availability (Qwen3.5, Llama, etc.)
- Pricing comparison vs Together.ai
- Rate limits and throughput for cook pipelines
- OpenAI-compatible API format

### Current LLM Providers

| Provider | Usage | Models |
|----------|-------|--------|
| Together.ai | Primary cook pipeline | Llama-3.3-70B-Turbo (gen), Qwen3-235B (pass/RPA) |
| Cloudflare AI | Edge inference | Qwen3-30B-A3B-FP8, Llama-3.2-3B |
| Self-hosted vLLM | Production inference | SwarmCurator-9B, SwarmCurator-27B |
| Ollama | Local dev + router | BeeMini, swarmrouter-v2 |

## Product Pages

All at `~/Desktop/swarmbeeai-factory/`:

| File | Product |
|------|---------|
| `index.html` | Main site |
| `swarmmed.html` | SwarmMed |
| `swarmpharma.html` | SwarmPharma |
| `swarmaviation.html` | SwarmAviation |
| `swarmcapitalmarkets.html` | Capital Markets |
| `curator.html` | SwarmCurator |
| `hedera.html` | Hedera |
| `pricing.html` | Pricing |
