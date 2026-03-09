# BeeMini Router v2

Request router. Takes an incoming query and decides which skill or model should handle it. Runs at 1.8GB quantized, fast enough for real-time routing on minimal hardware.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen2.5-3B |
| Architecture | Dense transformer (Gen 1, standard attention) |
| Training method | QLoRA |
| Training pairs | 60,000 |
| Steps | 693 |
| Train loss | 0.026 |
| GGUF | swarmrouter-v2-q4_k_m.gguf (1.8GB) |
| Deployment | whale:8081 via llama-server |

## Why the Loss is 0.026

The extremely low training loss is not a bug. Router classification is a constrained output task -- the model outputs a structured JSON object with a fixed schema: target skill name, confidence score, and routing rationale. With 60K examples covering all 28 skills and their edge cases, the mapping becomes highly deterministic. There is essentially one correct answer for each input pattern.

## Training Data

60,000 routing examples covering:
- All 28 skills (19 CRE + 9 medical)
- Ambiguous queries that could route to multiple skills
- Off-domain queries that should route to a fallback
- Multi-skill queries that need decomposition
- Adversarial queries designed to trick the router

Training set: `/home/swarm/Desktop/swarmrouter/data/swarmrouter_train_60k.jsonl`

## Routing Architecture

### Confidence Scoring

The router proxy (FastAPI on swarmrails:8080) wraps the BeeMini model and adds confidence scoring:

```
Confidence = json_valid(0.30) + schema_complete(0.25) + enum_valid(0.25) + logprob_score(0.20)
```

| Component | Weight | What it checks |
|-----------|--------|---------------|
| json_valid | 0.30 | Is the output valid JSON? |
| schema_complete | 0.25 | Are all required fields present? |
| enum_valid | 0.25 | Is the target skill in the allowed set? |
| logprob_score | 0.20 | Model confidence from log probabilities |

Promotable threshold: confidence >= 0.80. Routing decisions below this threshold get logged for review but still execute (with a warning flag).

### Decision Logging

Every routing decision logs to JSONL at `swarmrails:/data2/swarm_router_train/logs/router_decisions_YYYY-MM-DD.jsonl`.

Each record includes:
- Full `messages` array (training-ready for v3)
- Confidence breakdown by component
- Selected skill and rationale
- Latency

These logs serve dual purpose: operational monitoring and training data for the next router version.

### Router Proxy

```
Code: /home/swarm/Desktop/swarm_router_train/serve_router.py
Endpoints:
  POST /route     -- route a query
  GET  /health    -- health check
  GET  /stats     -- routing statistics
```

Start command:
```bash
ssh swarmrails "cd /data2/swarm_router_train && nohup python3 serve_router.py --port 8080 > logs/serve_router.log 2>&1 &"
```

## Live Deployment

BeeMini Router v2 runs on the Cloudflare Worker at router.swarmandbee.com. The worker handles:

- `POST /skill/{name}` -- execute a skill
- `GET /skills` -- list available skills
- `GET /skill/{name}/spec` -- get SKILL.md spec for a skill
- `/mock`, `/test`, `/eval`, `/fail` -- testing endpoints

Edge model for skill calls: Qwen3-30B-A3B at ~$0.00004 per skill call.

## Router Logging in D1

Routing decisions also log to the D1 database (swarm-intelligence-db, table: router_decisions). The `/router/stats` and `/router/decisions` endpoints expose this data for analysis.

## v3 Plans

Router v3 will train on the accumulated decision logs from v2 production traffic. The logs include the full message arrays, meaning v3 training data comes from real-world queries rather than synthetic generation. This should improve handling of ambiguous and multi-skill queries.
