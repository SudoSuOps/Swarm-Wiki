# SwarmCurator-9B

The operational workhorse of the curator fleet. Handles detailed signal analysis, pair generation oversight, and quality assessment. Fast enough for real-time inference, smart enough for nuanced analysis.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-9B |
| Architecture | GDN (75%) + Standard attention (25%) |
| Vocabulary | 248,320 tokens |
| Context | 262K native, 1M via YaRN |
| Training method | bf16 LoRA r=64 alpha=32 |
| Training pairs | 46,000 |
| Steps | 414 |
| Train loss | 0.707 |
| Training hardware | Blackwell GPUs on swarmrails |
| Merged checkpoint | swarmrails:/data2/swarmcurator-9b-p2/merged/ |

## Training Data Assembly

Two-phase training to build operational capability on top of methodological foundations:

| Phase | Pairs | Content |
|-------|-------|---------|
| Phase 1: Methodology | 30,000 | Signal analysis patterns, quality evaluation criteria, reasoning structures |
| Phase 2: Operations | 20,000 | Factory pipeline tasks, cook oversight, gate interpretation, fleet coordination |

Total effective training set after deduplication and quality filtering: 46,000 pairs.

## Deployment

**Production**: vLLM 0.17.0 on swarmrails port 8081, GPU0 (RTX PRO 4500 Blackwell, 32GB VRAM).

```
Model name: swarmcurator-9b
Endpoint: http://swarmrails:8081/v1/chat/completions
Throughput: 165 tok/s at 4 concurrent requests
VRAM usage: ~23.5GB bf16
```

The 9B runs on the smaller Blackwell GPU (32GB) and delivers nearly 2x the throughput of the 27B. This makes it the right choice for any task that needs speed over depth -- signal analysis, quality scoring, pair review.

Launch script: `/tmp/start_vllm_9b.sh`

Same required flags and vision_config fix as the 27B (see [swarmcurator-27b.md](swarmcurator-27b.md)).

## Performance Context

Qwen3.5-9B punches well above its weight class:

- MMLU-Pro: 82.5 (beats Qwen3-30B at 80.9)
- GPQA: 81.7 (beats Qwen3-30B at 73.4)
- LongBench: 55.2 (beats Qwen3-30B at 44.8)

These are base model benchmarks. After fine-tuning on curator-specific tasks, the 9B handles operational analysis at quality levels that would have required a 30B+ model in the previous generation.

## Role in Fleet

SwarmCurator-9B sits at stage 3 of the curator middleware chain (Analysis). It receives classified signals from the 2B and performs detailed analysis:

- What does this market event mean in context?
- How does it relate to signals seen in the past 30 days?
- What is the quality level of generated pairs in this domain?
- Are there data gaps that need targeted cook runs?

The 9B handles the bulk of inference volume. The 27B only gets called for strategic decisions that require deeper reasoning. Most signals never need to escalate past the 9B.

## Concurrent Performance

At 4 concurrent workers via vLLM:
- 165 tok/s combined throughput
- 3.6x improvement over sequential inference
- ~1,740 pairs/hr combined with the 27B (both GPUs working)

The cook pipeline supports `--vllm --workers 4` for concurrent pair generation against the 9B endpoint.
