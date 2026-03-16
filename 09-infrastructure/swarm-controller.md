# Swarm Controller

Central orchestration daemon running on swarmrails (Xeon w9-3475X). Monitors all compute nodes, dispatches cook orders, and auto-triggers downstream pipeline stages.

## Overview

| Field | Value |
|-------|-------|
| Host | swarmrails (localhost) |
| Port | 9000 |
| Database | SQLite at `/data2/swarm-controller/swarm.db` |
| Code | `/data2/swarm-controller/` |
| Service | `swarm-controller.service` (systemd) |
| Dashboard | `http://localhost:9000/` (auto-refresh 15s) |

## Node Registry

The controller health-checks 9 nodes every 30 seconds:

| Node | Host | Port | Model | GPU | Capabilities |
|------|------|------|-------|-----|-------------|
| gpu0 | localhost | 8081 | nemotron-nano-fp4 | RTX PRO 4500 (32GB) | cook |
| gpu1 | localhost | 8083 | nemotron-nano | RTX PRO 6000 (96GB) | cook |
| cpu | localhost | 8085 | swarmjelly-4b-q4_k_m | None (AMX CPU) | jelly, gate, finalize |
| jetson | 192.168.0.79 | 8085 | qwen35-4b-q4_k_m | Orin Nano (8GB) | cook-edge |
| openrouter | openrouter.ai | 443 | fleet | None (cloud) | cook-cloud |
| whale | 192.168.0.99 | 8081 | qwen35-4b | RTX 3090 (24GB) | cook, jelly, gate |
| whale-cpu | 192.168.0.99 | 8085 | swarmjelly-4b-q4_k_m | None | jelly, gate, finalize |
| bee | 192.168.0.70 | 9000 | infra | None (N150 CPU) | finalize, audit, staging, signal |
| nas | 192.168.0.102 | 5000 | storage | None | storage, model-vault |

Health checks hit each node's `health_endpoint` (e.g., `/v1/models` for vLLM, `/health` for llama-server, `/minio/health/live` for MinIO, `/` for NAS DSM).

## Pipeline DAG

The controller orchestrates 5 pipeline stages, auto-triggering downstream when upstream completes:

```
cook_complete(order_id)
  -> finalize_batch.py --input {cook_output_dir}
  -> status = "finalizing"

finalize_complete(order_id, batch_id)
  -> push_batch.py --batch {batch_dir}
  -> status = "pushing"

push_complete(order_id, merkle_root)
  -> event: "batch_anchored"
  -> status = "done"
```

SwarmJelly runs independently on a 15-minute timer, processing propolis failures into royal_jelly training pairs.

## REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Aggregated swarm status (nodes, active cooks, total pairs, uptime) |
| GET | `/api/nodes` | All nodes with health, GPU util, last_seen |
| GET | `/api/cooks` | Active and recent cook orders |
| GET | `/api/cooks/{id}` | Full cook detail + metrics timeline |
| GET | `/api/events` | Last 200 events (filterable by type) |
| GET | `/api/metrics/{node}` | Time-series metrics for a node |
| POST | `/api/cook` | Submit new cook order |
| POST | `/api/metrics` | Ingest checkpoint metrics from cook scripts |
| GET | `/` | HTML dashboard (server-rendered, 15s auto-refresh) |

## Cook Order Schema

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | e.g., "COOK-AVN-20260316" |
| domain | TEXT | aviation, legal_consumer, cre, etc. |
| backend | TEXT | nemotron, fleet, 4b |
| workers | INT | Concurrency level |
| target | INT | Pair count target (0 = all) |
| status | TEXT | pending -> cooking -> gating -> finalizing -> pushed -> done |
| pairs_done | INT | Progress counter |

## Metrics

Cook scripts POST checkpoint metrics to `/api/metrics`. The controller also samples `nvidia-smi` every 30 seconds for GPU utilization tracking.

Tracked metrics: `pairs_cooked`, `tok_per_s`, `gpu_util`, `gate_pass_rate`.

## Cook Scripts

| Domain | Script | Location |
|--------|--------|----------|
| aviation | cook_openalex.py | `/data2/openalex/cook_openalex.py` |
| legal_consumer | cook_creditsniper.py | `/data2/creditsniper/cook_creditsniper.py` |
| signal | cook_signal_orders.py | `~/Desktop/swarmrouter/data/cook_signal_orders.py` |

## Systemd

```ini
[Unit]
Description=Swarm Controller — Central Orchestration Daemon
After=network.target

[Service]
Type=simple
User=swarm
WorkingDirectory=/data2/swarm-controller
ExecStart=/usr/bin/python3 -u controller.py
Restart=always
RestartSec=10
Nice=10
CPUWeight=50
MemoryMax=2G

[Install]
WantedBy=multi-user.target
```

## Integration

The controller wraps existing scripts via `subprocess.Popen` — it does not replace them. Each cook script runs as its own process; the controller monitors liveness and progress.

| Script | How Controller Uses It |
|--------|----------------------|
| cook_openalex.py | Subprocess dispatch, progress monitoring |
| cook_creditsniper.py | Subprocess dispatch, progress monitoring |
| finalize_batch.py | Auto-triggered on cook completion |
| push_batch.py | Auto-triggered on finalize completion |
| pipeline_swarmjelly.py | Monitors state.json (existing systemd timer) |
