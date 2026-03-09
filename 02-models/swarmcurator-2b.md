# SwarmCurator-2B / SwarmSignal-2B

The edge classifier. Runs on devices with no GPU and 8-14GB of RAM. Triages incoming signals into priority tiers and classifies them by vertical and task type. Deployed as both SwarmCurator-2B (curator fleet role) and SwarmSignal-2B (edge signal processing role) -- same model, different deployment contexts.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-2B |
| Architecture | GDN (75%) + Standard attention (25%) |
| Vocabulary | 248,320 tokens |
| Context | 262K native |
| Training method | bf16 LoRA r=32 alpha=16 |
| Training pairs | 9,400 |
| Steps | 224 |
| Train loss | 0.880 |
| Training hardware | whale RTX 3090 24GB |
| Merged checkpoint | whale:~/swarmcurator-2b/merged/ |

## Quantized Formats

| Format | Size | Deployment |
|--------|------|------------|
| Q4_K_M GGUF | ~1.2GB | Jetson Orin Nano, zima-edge-1 |
| bf16 merged | ~4GB | whale (full precision) |

## Edge Deployments

### signal-edge-01 (Jetson Orin Nano 8GB)
- IP: 192.168.1.95
- User: sigedge/mack
- Runtime: llama.cpp (CUDA sm_87 built, but CPU-only inference -- Super firmware needed for GPU mode)
- Model: SwarmSignal-2B-v1 Q4_K_M (1.2GB)
- JetPack 6.2 (R36.4.7), CUDA 12.6

### zima-edge-1 (Intel N150)
- IP: 192.168.0.70
- User: dev/mack
- Runtime: Python venv at /data/swarmsignal/venv/
- Service: systemd `swarmsignal.service` (enabled, 15-minute cycles)
- Discord bridge: Posts P1-P3 signals to #swarm-signal channel via webhook
- Also runs BitNet b1.58-2B-4T (microsoft/BitNet GGUF, 1.2GB, 19.7 tok/s on CPU)

## Role in Fleet

SwarmCurator-2B is stage 2 of the curator middleware chain (Classification). It receives raw signals from the ingestion stage and makes fast triage decisions:

- **Priority**: P1 (act now), P2 (watch), P3 (background), or noise (discard)
- **Vertical**: CRE, Medical, Aviation, Capital Markets, or General
- **Task type**: What kind of event is this? (Lease expiration, EDGAR filing, rate change, etc.)

Classification must be fast and cheap because it runs on every signal, every 15 minutes, across all 11 workers. The 2B handles this in milliseconds on CPU. Only signals classified as P1-P3 escalate to the 9B for detailed analysis.

When the 2B is offline, the middleware falls back to keyword-based classification rules. These are coarser but functional -- the fleet never stops processing.

## Training Data

9,400 pairs focused on classification accuracy:
- Signal priority assignment (P1/P2/P3/noise) with reasoning
- Vertical classification with confidence scores
- Task type identification from raw event text
- Edge cases: ambiguous signals that could be multiple verticals, signals with incomplete data

Smaller training set than the 9B/27B because the task is narrower. The 2B does not need to analyze or strategize -- it needs to sort quickly and accurately.
