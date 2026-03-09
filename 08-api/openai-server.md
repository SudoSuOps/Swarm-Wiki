# OpenAI-Compatible Inference Gateway

Swarm's OpenAI-compatible server at `api.swarmandbee.ai`. Any OpenAI SDK client connects with one line change.

## Quick Start

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.swarmandbee.ai/v1",
    api_key="sk_swarm_..."
)

response = client.chat.completions.create(
    model="swarm/curator-27b",
    messages=[{"role": "user", "content": "Analyze cap rate compression in DFW industrial."}]
)
```

## Architecture

```
api.swarmandbee.ai (CF Worker)
         │
    cloudflared tunnel
         │
    FastAPI Gateway (swarmrails:4000)
      ├── swarmrails:8081 → SwarmCurator-9B (vLLM bf16, 165 tok/s x4)
      ├── swarmrails:8082 → SwarmCurator-27B (vLLM bf16, 88 tok/s x4)
      └── Together.ai Qwen-235B (fallback)
```

## Model Catalog

| Model ID | Params | VRAM | Vertical | Status |
|----------|--------|------|----------|--------|
| `swarm/curator-27b` | 27B Dense | 93GB bf16 | Strategy, quality gating | LIVE |
| `swarm/curator-9b` | 9B Dense | 23.5GB bf16 | Operations, signal analysis | LIVE |
| `swarm/pharma-35b` | 35B MoE (3B active) | 20GB Q4 | Pharmacology | DONE |
| `swarm/capital-markets-27b` | 27B Dense | 93GB bf16 | CMBS, debt, rate advisory | TRAINING |

All models based on Qwen3.5 with Gated Delta Networks. 262K context window. Trained on 1.16M verified pairs.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/models` | List available models |
| POST | `/v1/chat/completions` | Chat completion (streaming + non-streaming) |
| GET | `/health` | Backend health check |

## Authentication

API keys use format `sk_swarm_{tier}_{random}`.

```bash
curl https://api.swarmandbee.ai/v1/chat/completions \
  -H "Authorization: Bearer sk_swarm_full_abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "swarm/curator-9b",
    "messages": [{"role": "user", "content": "What is a DSCR?"}],
    "stream": false
  }'
```

## Streaming

Full SSE support — token-by-token streaming from vLLM passed through without buffering:

```bash
curl https://api.swarmandbee.ai/v1/chat/completions \
  -H "Authorization: Bearer sk_swarm_full_abc123" \
  -H "Content-Type: application/json" \
  -d '{"model": "swarm/curator-27b", "messages": [{"role": "user", "content": "Draft an IC memo for 50K SF cold storage in DFW."}], "stream": true}'
```

## Fallback Chain

1. **Primary**: Local vLLM on swarmrails (free, fastest)
2. **Fallback**: Together.ai Qwen-235B (paid, highest quality)

Fallback activates automatically when vLLM is unreachable (training, maintenance, GPU failure).

## Logging

Every request logged to JSONL at `/data2/swarm_api/logs/openai_gateway_YYYY-MM-DD.jsonl`.

Each record includes: model, messages, response, usage (tokens), latency, backend used, API key name. Training-ready for router v3.

## Deployment

**On swarmrails**:
```bash
cd ~/Desktop/swarmrouter
# Foreground
python3 -m openai_server.server --port 4000

# Daemon
./openai_server/start.sh --daemon
```

**Environment variables**:
| Var | Default | Purpose |
|-----|---------|---------|
| `VLLM_9B_URL` | `http://localhost:8081` | 9B backend |
| `VLLM_27B_URL` | `http://localhost:8082` | 27B backend |
| `TOGETHER_API_KEY` | (none) | Enables fallback |
| `SWARM_API_KEYS` | (none) | Comma-separated test keys |
| `SWARM_INTERNAL_KEY` | `sk_swarm_internal_dev` | Dev/internal key |
| `SWARM_LOG_DIR` | `/data2/swarm_api/logs` | Log directory |
| `SWARM_GATEWAY_PORT` | `4000` | Server port |

## Hedera Proof-of-Inference (Planned)

Each request will produce:
1. `SHA256(model + prompt_hash + response_hash + timestamp)`
2. Published to HCS Receipt topic (0.0.10291834)
3. `x-swarm-proof` response header with HCS transaction ID
4. Verifiable on Hedera mainnet

## Code

- Gateway: `swarmrouter/openai_server/server.py`
- Models: `swarmrouter/openai_server/models.py`
- Auth: `swarmrouter/openai_server/auth.py`
- Logging: `swarmrouter/openai_server/logging.py`
- Launch: `swarmrouter/openai_server/start.sh`
