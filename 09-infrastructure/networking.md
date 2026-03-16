# Networking

## Node Addresses

| Node | IP | SSH | Ports |
|------|----|-----|-------|
| swarmrails | local | `ssh swarmrails` | 8081 (Nemotron FP4 vLLM), 8083 (Nemotron FP8 vLLM), 8085 (SwarmJelly), 9000 (controller) |
| whale | 192.168.0.99 | `ssh whale` (pw: mack) | 8081 (4B vLLM), 8085 (SwarmJelly CPU) |
| signal-edge-01 | 192.168.0.79 | `ssh sigedge@192.168.0.79` | 8085 (llama-server) |
| zima-edge-1 (bee) | 192.168.0.70 | `ssh dev@192.168.0.70` (pw: mack) | 9000/9001 (MinIO), 81 (Nginx), 8420 (swarm-witness) |
| nas (DS1525+) | 192.168.0.102 | `ssh admin@192.168.0.102` | 5000 (DSM web) |

## 10G NICs

| Node | NIC | Status |
|------|-----|--------|
| swarmrails | Intel X710 10G | Active |
| whale | Intel X540-AT2 10G (dual-port, Gen2 x4) | Not cabled yet |

The X540-AT2 on whale is installed in the x4 slot (freed by removing the second 3090). Once cabled, it enables 10G transfers between swarmrails and whale for model/data movement.

## SSH Key Auth

All nodes use SSH key authentication. No password SSH access.

| Alias | User | Host | Key |
|-------|------|------|-----|
| `swarmrails` | swarm | local | SSH key |
| `whale` | swarm | 192.168.0.99 | SSH key |
| `sigedge` | sigedge | 192.168.0.79 | SSH key (password: mack) |
| `zima` | dev | 192.168.0.70 | SSH key (password: mack) |

## Cloudflare

| Property | Value |
|----------|-------|
| Account ID | `6abec5e82728df0610a98be9364918e4` |
| Free API | `router.swarmandbee.com` |
| Metered API | `api.router.swarmandbee.com` |
| Worker | `worker/src/index.js` |
| Deploy | `cd worker && npx wrangler deploy` |
| Logs | `cd worker && npx wrangler tail` |

Use `npx wrangler` with `CLOUDFLARE_ACCOUNT_ID` env var (no `--remote` flag in newer wrangler versions).

## zima-edge-1 Services

| Service | Port | Protocol | Description |
|---------|------|----------|-------------|
| MinIO | 9000 | HTTP | S3-compatible object storage API |
| MinIO Console | 9001 | HTTP | MinIO web UI |
| Nginx Proxy Manager | 81 | HTTP | Reverse proxy management UI |
| cloudflared | -- | -- | Cloudflare tunnel (outbound only) |
| swarmsignal.service | -- | -- | systemd service, 15min signal cycles |
| swarm-witness | -- | -- | Witness service |

## swarmrails Services

| Service | Port | Description |
|---------|------|-------------|
| vLLM (Nemotron FP4) | 8081 | Nemotron Nano FP4, GPU 0 (standby -- SwarmJelly using GPU) |
| vLLM (Nemotron FP8) | 8083 | Nemotron Nano FP8, GPU 1 (active aviation cook) |
| llama-server (SwarmJelly) | 8085 | SwarmJelly-4B BF16, GPU 0 (or CPU AMX fallback) |
| Swarm Controller | 9000 | Central orchestration daemon, HTML dashboard |

### Router Proxy (swarmrails:8080)

FastAPI proxy wrapping the Ollama swarmrouter-v2 model. Logs every routing decision to JSONL for training data collection.

- Code: `/home/swarm/Desktop/swarm_router_train/serve_router.py`
- Logs: `/data2/swarm_router_train/logs/router_decisions_YYYY-MM-DD.jsonl`
- Start: `ssh swarmrails "cd /data2/swarm_router_train && nohup python3 serve_router.py --port 8080 > logs/serve_router.log 2>&1 &"`

Each log record includes the full `messages` array (training-ready for v3 router). Promotable threshold: confidence >= 0.80.

## External Services

| Service | URL | Purpose |
|---------|-----|---------|
| GitHub Org | github.com/swarm-bee-github | Source repos |
| HuggingFace Org | huggingface.co/SwarmandBee | Model hosting |
| Supabase | gizwfmgowyfadmvjjitb.supabase.co | PostgreSQL + pgvector (13 tables, 10 RPCs) |
| DigitalOcean | -- | Account created, provisioning for CreditSniper/CreditCase |
| Together.ai | api.together.xyz | API inference (keys in swarm-agents/.env) |
| Rocket.Chat | chat.swarmandbee.com | Team chat, CreditSniper contact webhook |
| PostGrid | api.postgrid.com | Physical mail API (letter_sender skill) |

## Cloud Domains

| Domain | Platform | Service |
|--------|----------|---------|
| `router.swarmandbee.com` | Cloudflare Workers | SwarmRouter edge API (40+ endpoints) |
| `api.swarmandbee.com` | Cloudflare Workers | Data commerce API (Stripe, catalog) |
| `swarmandbee.ai` | Cloudflare Pages | Marketing site |
| `creditsniper.xyz` | Cloudflare Pages | Credit dispute intelligence |
| `chat.swarmandbee.com` | Rocket.Chat | Team communications |
