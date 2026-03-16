# Edge Nodes

Two edge devices for signal processing and lightweight inference at the network boundary.

## signal-edge-01 (Jetson Orin Nano 8GB)

NVIDIA Jetson running as an edge cook node. Full GPU offload enabled, producing ~12 pairs/hr.

| Field | Value |
|-------|-------|
| IP | 192.168.0.79 |
| User | sigedge (password: mack, SSH key auth) |
| Hostname | signal-edge-01 |
| OS | JetPack 6.2 (R36.4.7) |
| SoC | Orin Nano, 8GB shared memory |
| CUDA | 12.6 |
| GPU Arch | sm_87 |
| Power Mode | MAXN (jetson_clocks enabled) |
| Throughput | ~7.8 tok/s GPU, ~12 pairs/hr |

### Software

| Component | Status |
|-----------|--------|
| llama.cpp | Built for sm_87 (CUDA), full GPU offload |
| Qwen3.5-4B base | Q4_K_M GGUF, cooking aviation pairs |
| jetson_cook.py | Custom cook script with thinking mode disabled |
| Cook output | ~/swarm/cook/cooked_shard_2k.jsonl |

### Cook Setup

```bash
# llama-server with full GPU offload, reduced context to fit 8GB
llama-server -m qwen35-4b-base-q4_k_m.gguf \
  --host 0.0.0.0 --port 8085 \
  -ngl 99 -c 2048

# Cook script (nohup, screen not installed)
nohup python3 jetson_cook.py --input shard_2k.jsonl --domain aviation &
```

### Key Configuration

- **Thinking mode disabled**: Base Qwen3.5-4B consumes all tokens in `<think>` tags. Fix: `"chat_template_kwargs": {"enable_thinking": false}` in cook script payload.
- **Context reduced to 2048**: Full 4096 causes CUDA OOM on 8GB shared memory. 2048 fits with full GPU offload.
- **Power mode MAXN**: Set with `sudo nvpmodel -m 0 && sudo jetson_clocks` for maximum throughput.
- **Desktop environment removed**: Freed ~500MB RAM for inference.

## zima-edge-1 / Bee Node (Intel N150)

Always-on Intel mini PC serving as the swarm's infrastructure node — finalize pipeline, audit archive, staging, signal ingestion, and S3-compatible object storage. Registered as `bee` in swarm-controller.

| Field | Value |
|-------|-------|
| IP | 192.168.0.70 |
| User | dev (password: mack) |
| Hostname | zima-edge-1 |
| CPU | Intel N150 4C/4T, 3.6GHz, 6W TDP, AVX2 + AVX-VNNI |
| RAM | 16 GB DDR5 |
| Storage | 915 GB NVMe (851 GB free) + 458 GB /data (430 GB free) |
| Network | 10G fiber + NAS mount at /mnt/swarm |
| GPU | None (CPU only -- too weak for inference, perfect for always-on services) |
| OS | Ubuntu 25.04, kernel 6.17.0, Python 3.13 |

### Active Services

| Service | Port | Details |
|---------|------|---------|
| bee-finalize-watcher | -- | Auto-finalize cooked pairs from /data/swarm-staging/{domain}/ |
| swarmsignal | -- | Python RSS/feed ingestion, 29K sources/day, 169 MB RAM |
| MinIO | 9000/9001 | S3 buckets: grind-output, platinum-cache, swarm-aero, training-staging |
| swarm-witness | 8420 | Rust binary, SwarmOS identity/attestation daemon |
| cloudflared | -- | CF tunnel cf6a905e -> chat.swarmandbee.com:3000 |
| Nginx Proxy Manager | 80/443 | Reverse proxy (Docker) |

### Data Directories

| Path | Purpose |
|------|---------|
| `/data/swarm-finalize/` | finalize_batch.py + watcher daemon |
| `/data/swarm-staging/{domain}/` | Incoming cooked JSONL from cook nodes |
| `/data/swarm-audit/` | Archived finalized batches |
| `/data/swarmsignal/` | Signal ingestion engine |
| `/data/platinum/` | CoVe verify, MRI gold |
| `/data/minio/data/` | 4 S3 buckets |

### Finalize Pipeline

The `bee-finalize-watcher` monitors `/data/swarm-staging/{domain}/` for new cooked JSONL files. When detected:
1. Runs `finalize_batch.py` -- stamps HiveCells, scores RJ tiers
2. Pushes to hive-ledger API (Cloudflare Workers + D1 + Hedera)
3. Uploads to R2 (sb-honey-verified bucket)
4. Archives to `/data/swarm-audit/`

### Controller Integration

Registered as `bee` node in swarm-controller. Health-checked via MinIO `/minio/health/live` on port 9000. Capabilities: `["finalize", "audit", "staging", "signal"]`.

### Access

```bash
ssh dev@192.168.0.70  # password: mack (needs sshpass from remote)
```
