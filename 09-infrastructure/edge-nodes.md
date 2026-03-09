# Edge Nodes

## signal-edge-01 (Jetson Orin Nano 8GB)

| Field | Value |
|-------|-------|
| IP | 192.168.1.95 |
| User | sigedge/mack (SSH key auth) |
| OS | JetPack 6.2 (R36.4.7) |
| CUDA | 12.6 |
| llama.cpp | Built for sm_87 |
| Model | SwarmSignal-2B Q4_K_M (1.2GB) |
| Inference | CPU-only (Super firmware needed for GPU mode) |

## zima-edge-1 (Intel N150)

| Field | Value |
|-------|-------|
| IP | 192.168.0.70 |
| User | dev/mack |
| CPU | Intel N150 4C/4T, 3.6GHz, AVX2+AVX-VNNI |
| RAM | 14GB LPDDR5 |
| Storage | 931GB + 466GB SSDs |

### Services

| Service | Port | Details |
|---------|------|---------|
| swarmsignal.service | — | systemd, 15min cycles, enabled |
| Discord bridge | — | P1-P3 signals to #swarm-signal |
| BitNet b1.58-2B | — | 19.7 tok/s CPU |
| MinIO | 9000/9001 | Object storage |
| Nginx Proxy Manager | 81 | Reverse proxy |
| cloudflared | — | Cloudflare tunnel |

SwarmSignal Python venv at `/data/swarmsignal/venv/`
