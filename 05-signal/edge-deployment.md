# Edge Deployment

Signal collection runs on two dedicated edge nodes in addition to the main swarmrails infrastructure. These nodes provide always-on, low-power signal ingestion close to the network edge.

## signal-edge-01 (Jetson Orin Nano)

| Spec | Value |
|------|-------|
| Hardware | NVIDIA Jetson Orin Nano 8GB |
| IP | 192.168.0.79 |
| User | sigedge (password: mack) |
| Hostname | signal-edge-01 |
| OS | JetPack 6.2 (R36.4.7) |
| CUDA | 12.6 |
| Inference | llama.cpp built for sm_87 (Orin GPU arch) |
| Model | SwarmSignal-2B-v1 Q4_K_M (1.2GB) |
| SSH | Key auth configured |

### Current Status

- **CPU-only inference**: The GPU requires a Super firmware update to enable GPU-mode inference. Running SwarmSignal-2B on CPU in the meantime.
- **llama.cpp**: Built with CUDA sm_87 target, ready for GPU mode once firmware is updated.
- **Role**: Lightweight signal classification and scoring at the edge. Feeds results back to the main signal engine.

## zima-edge-1 (Intel N150)

| Spec | Value |
|------|-------|
| Hardware | Intel N150 (4C/4T, 3.6GHz, AVX2 + AVX-VNNI) |
| RAM | 14GB LPDDR5 |
| Storage | 931GB + 466GB SSDs |
| IP | 192.168.0.70 |
| User | dev (password: mack) |

### Deployed Services

| Service | Details |
|---------|---------|
| SwarmSignal | systemd `swarmsignal.service` (enabled, 15min cycles), Python venv at `/data/swarmsignal/venv/` |
| Discord bridge | Posts P1-P3 signals to `#swarm-signal` channel via webhook |
| BitNet b1.58-2B-4T | Microsoft BitNet GGUF (1.2GB), built bitnet.cpp, 19.7 tok/s on N150 CPU |
| MinIO | Object storage on ports 9000 (API) / 9001 (console) |
| Nginx Proxy Manager | Port 81, reverse proxy for local services |
| cloudflared | Cloudflare tunnel for external access |
| swarm-witness | Witness service for signal verification |

### SwarmSignal Service

The `swarmsignal.service` systemd unit runs the signal collection loop:
- **Cycle**: Every 15 minutes
- **Venv**: `/data/swarmsignal/venv/`
- **Outputs**: Scored signals pushed to Discord webhook and main signal engine
- **Status**: Enabled and running (auto-starts on boot)

## Edge vs. Central

| Concern | Edge Nodes | swarmrails |
|---------|-----------|------------|
| Availability | Always-on, low power | Primary compute, may be busy with training |
| Model size | 2B (Q4_K_M, 1.2GB) | 9B/27B (bf16, full precision) |
| Role | Signal collection + lightweight classification | Full analysis + strategy + factory |
| Network | Local LAN | LAN + Cloudflare tunnel |

Edge nodes ensure signal collection continues even when swarmrails is occupied with GPU-heavy training or inference workloads.
