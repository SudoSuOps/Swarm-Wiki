# Nemotron Nano (Cook Fleet)

NVIDIA's Nemotron Nano 30B MoE model deployed as the primary cook engine on swarmrails. Replaces base Qwen3.5-4B for higher-quality pair generation with instruction-following capability built in.

## Variants

| Variant | GPU | Port | Quantization | VRAM | Status |
|---------|-----|------|-------------|------|--------|
| nemotron-nano | RTX PRO 6000 (96GB) | 8083 | FP8 | ~60 GB | ACTIVE -- aviation cook |
| nemotron-nano-fp4 | RTX PRO 4500 (32GB) | 8081 | FP4 | ~28 GB | STANDBY -- SwarmJelly using GPU 0 |

## Architecture

| Property | Value |
|----------|-------|
| Base | NVIDIA Nemotron Nano |
| Parameters | ~30B total (MoE) |
| Active Params | ~8B per token |
| Serving | vLLM 0.17.0 |
| Health Endpoint | `/v1/models` |
| Context | 4096 (cook default) |

## Cook Performance

| Metric | FP8 (GPU 1) | FP4 (GPU 0) |
|--------|-------------|-------------|
| Throughput | ~0.8 pairs/s | ~0.4 pairs/s |
| Workers | 20 | 8 |
| Quality | Honey-tier (RJ-aligned prompts) | Honey-tier |

### Key Finding: Single-GPU Superiority

Dual-GPU round-robin (FP8 + FP4) caused a 39% failure rate due to FP4 timeouts dragging down the pool. Single-GPU FP8 on the RTX 6000 runs clean at 0.8/s with zero failures. The RTX 4500 is better utilized for SwarmJelly GPU inference or standalone cooks.

## Cook Integration

The Nemotron fleet uses `cook-domain-prompts` for RJ-aligned prompt generation:

```python
# cook_openalex.py endpoint config (single GPU mode)
VLLM_NEMOTRON = "http://localhost:8083/v1/chat/completions"
MODEL_NEMOTRON = "nemotron-nano"
```

Prompts are domain-specific (15 domains), SHA-256 hashed for telemetry, with the Prompt Machine managing softmax allocation across 10 mutations per domain.

## Controller Registration

Registered as `gpu0` (FP4, :8081) and `gpu1` (FP8, :8083) in swarm-controller config.py with capability `["cook"]`.

## vs. Base Qwen3.5-4B

| | Nemotron Nano (FP8) | Qwen3.5-4B Base |
|--|-------------------|-----------------|
| Params active | ~8B | 4B |
| Instruction following | Native | Requires prompt engineering |
| Quality | Honey-tier | Honey-tier (with RJ prompts) |
| Speed | 0.8 pairs/s (20 workers) | 0.4 pairs/s (8 workers) |
| VRAM | 60 GB (FP8) | 8 GB (Q4_K_M) |

Both achieve Honey-tier quality with RJ-aligned prompts. Nemotron's advantage is throughput -- the larger model handles more concurrent workers without quality degradation.
