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

## zima-edge-1 (Intel N150)

Always-on Intel mini PC running signal processing, Discord bridge, and edge services.

| Field | Value |
|-------|-------|
| IP | 192.168.0.70 |
| User | dev (password: mack) |
| CPU | Intel N150 4C/4T, 3.6GHz, AVX2 + AVX-VNNI |
| RAM | 14GB LPDDR5 |
| Storage | 931GB + 466GB SSDs |
| GPU | None (CPU only) |

### Services

| Service | Port | Details |
|---------|------|---------|
| swarmsignal.service | -- | systemd, enabled, 15min signal collection cycles |
| Discord bridge | -- | Posts P1-P3 signals to #swarm-signal channel via webhook |
| BitNet b1.58-2B-4T | -- | Microsoft BitNet GGUF (1.2GB), 19.7 tok/s on N150 CPU |
| MinIO | 9000/9001 | S3-compatible object storage + web console |
| Nginx Proxy Manager | 81 | Reverse proxy management |
| cloudflared | -- | Cloudflare tunnel (outbound) |
| swarm-witness | -- | Witness/attestation service |

### SwarmSignal Pipeline

- Python venv: `/data/swarmsignal/venv/`
- Service: `swarmsignal.service` (systemd, enabled at boot)
- Cycle: Every 15 minutes, collects signals, classifies priority (P1-P3), posts to Discord
- Discord webhook: Posts to #swarm-signal channel with priority-based formatting

### BitNet

Microsoft's BitNet b1.58-2B-4T model running via `bitnet.cpp` (separate from llama.cpp). 1-bit weights achieve 19.7 tok/s on the N150's CPU with AVX-VNNI acceleration. Used for experimental edge inference testing.

### Access

```bash
ssh dev@192.168.0.70  # password: mack
```
