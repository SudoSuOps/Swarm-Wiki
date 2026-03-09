# SwarmCurator-27B

The strategic head of the curator fleet. Makes high-level decisions about what to cook, how to rank competing signals, and when output quality is sufficient for promotion. Deployed on Blackwell.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen3.5-27B Dense |
| Architecture | 64 layers, 5120 hidden dim, all 27B parameters active |
| Attention | GDN (75%) + Standard (25%), block pattern: 3 GDN + 1 Attn |
| Vocabulary | 248,320 tokens |
| Context | 262K native, 1M via YaRN |
| Training method | bf16 LoRA r=64 alpha=32 |
| Training pairs | 62,525 train / 500 eval |
| Steps | 1,000 of 1,171 (early stopped) |
| Train loss | 0.4766 |
| Eval loss | 0.680 |
| Training time | 14.38 hours on RTX PRO 6000 Blackwell |
| Merged checkpoint | swarmrails:/data2/swarmcurator-27b/merged/ (52GB, 11 shards) |

## Training Data Assembly

Three-phase assembly ensuring diversity across operational domains:

| Phase | Pairs | Content |
|-------|-------|---------|
| Methodology | 27,700 | How to analyze signals, evaluate quality, structure reasoning |
| Operations | 19,900 | Factory pipeline operations, cook decisions, gate interpretations |
| Strategic | 18,125 | Market-level analysis, cross-signal correlation, fleet coordination |
| **Total** | **62,525 train + 500 eval** | |

System prompt diversity enforced: 30+ unique system prompts, no single prompt exceeds 10% of the training set. 26+ task types prevent template memorization.

## Loss Curve

Clean convergence with no instability:
- Start: ~2.1
- Step 200: ~0.9
- Step 400: ~0.6
- Step 600: ~0.52
- Step 800: ~0.49
- Step 1,000: 0.4766 (early stopped, eval loss plateaued at 0.680)

No signs of overfitting. Eval loss tracked train loss with expected generalization gap.

## Quantized Formats

| Format | Size | Use Case |
|--------|------|----------|
| Q4_K_M GGUF | 16GB | Local testing, backup inference |
| Q8_0 GGUF | 27GB | High-quality offline inference |
| F16 GGUF | 51GB | When vLLM is unavailable |
| bf16 (vLLM) | 52GB | Production serving |

## Deployment

**Production**: vLLM 0.17.0 on swarmrails port 8082, GPU1 (RTX PRO 6000 Blackwell, 96GB VRAM).

```
Model name: swarmcurator-27b
Endpoint: http://swarmrails:8082/v1/chat/completions
Throughput: 88 tok/s at 4 concurrent requests
VRAM usage: ~93GB bf16
```

Launch script: `/tmp/start_vllm_27b.sh`

Required flags:
```
--skip-mm-profiling
--enforce-eager
--limit-mm-per-prompt '{"image": 0}'
```

Required config fix: Copy `vision_config` from base Qwen3.5 model into merged config.json. The `out_hidden_size` field must match the text model's hidden_size. This is an Unsloth merge artifact -- the merge bakes in VL (vision-language) weights from the base model even though we only fine-tuned text.

## Sampling Parameters

Two operational modes:

### Structured Evaluation Mode
For gate decisions, quality scoring, and classification tasks where consistency matters.

```json
{
  "temperature": 0.7,
  "top_p": 0.8,
  "top_k": 20,
  "presence_penalty": 1.5,
  "max_tokens": 4096
}
```

### Deep Analysis Mode
For strategic ranking, cross-signal correlation, and open-ended market analysis.

```json
{
  "temperature": 1.0,
  "top_p": 0.95,
  "max_tokens": 8192
}
```

## Think Mode Behavior

Qwen3.5 has think mode ON by default for 9B+ models. There is no soft-switch. Key behaviors:

1. **Short system prompts cause loops.** With minimal context, the model enters think-loops where it reasons in circles. Always provide substantial system prompts (200+ tokens).
2. **Long system prompts produce focused output.** The more context you give, the more directed the reasoning becomes. This is why SKILL.md specs are injected into the system prompt.
3. **Disable with `enable_thinking: false`** when you need deterministic, non-reasoning output (e.g., JSON classification).
4. **Set `max_tokens` to 4096+.** Think mode generates internal reasoning tokens before the visible response. With low token limits, the model spends all its budget thinking and produces truncated output.
5. **Never use `do_sample=False`.** Greedy decoding breaks Qwen3.5 think mode. Always sample.
6. **Use `presence_penalty=1.5`** to prevent repetitive reasoning chains in structured eval mode.

## Role in Fleet

SwarmCurator-27B sits at the top of the curator middleware chain (stage 4 of 7: Strategy). It receives analyzed signals from the 9B and makes strategic decisions:

- Should we cook new training pairs for this signal category?
- How should competing signals be ranked for attention?
- Is the current output quality sufficient, or do we need a targeted cook run?
- What market reports should be generated from this signal cluster?

When the 27B is offline, the middleware falls back to algorithmic heuristics (signal heat scoring, frequency-based ranking). The fleet operates without any GPU; it just operates better with one.
