# Edge Nodes

Two edge devices for signal processing and lightweight inference at the network boundary.

## signal-edge-01 (Jetson Orin Nano 8GB)

NVIDIA Jetson for edge AI inference. Currently CPU-only due to firmware limitation.

| Field | Value |
|-------|-------|
| IP | 192.168.1.95 |
| User | sigedge (password: mack, SSH key auth) |
| Hostname | signal-edge-01 |
| OS | JetPack 6.2 (R36.4.7) |
| SoC | Orin Nano, 8GB shared memory |
| CUDA | 12.6 |
| GPU Arch | sm_87 |

### Software

| Component | Status |
|-----------|--------|
| llama.cpp | Built for sm_87 (CUDA) |
| SwarmSignal-2B | Q4_K_M (1.2GB), deployed |
| Inference | CPU-only (Super firmware needed for GPU mode) |

### Firmware Note

The Orin Nano ships with standard firmware that does not enable GPU compute for llama.cpp. The "Super" firmware update is required to unlock GPU-accelerated inference. Until then, the 2B model runs on CPU only, which is adequate for the signal classification workload.

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
