# Networking

## Node Addresses

| Node | IP | SSH | Ports |
|------|----|-----|-------|
| swarmrails | local | `ssh swarmrails` | 8081 (9B vLLM), 8082 (27B vLLM), 8080 (router proxy) |
| whale | 192.168.0.99 | `ssh whale` | 8081 (BeeMini GGUF) |
| signal-edge-01 | 192.168.1.95 | `ssh sigedge@192.168.1.95` | -- |
| zima-edge-1 | 192.168.0.70 | `ssh dev@192.168.0.70` | 9000/9001 (MinIO), 81 (Nginx Proxy Manager) |

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
| `sigedge` | sigedge | 192.168.1.95 | SSH key (password: mack) |
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
| vLLM (9B) | 8081 | SwarmCurator-9B bf16, GPU 0 |
| vLLM (27B) | 8082 | SwarmCurator-27B bf16, GPU 1 |
| FastAPI router proxy | 8080 | Wraps Ollama swarmrouter-v2, logs decisions |

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
| Supabase | gizwfmgowyfadmvjjitb.supabase.co | Auth DB (18 tables, 10 RPCs) |
| DigitalOcean | -- | Account created, pending provisioning |
| Together.ai | api.together.xyz | API inference (keys in swarm-agents/.env) |
