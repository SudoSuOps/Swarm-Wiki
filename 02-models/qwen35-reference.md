# Qwen3.5 Architecture Reference

Complete architecture reference for the Qwen3.5 model family, which serves as the base for all current-generation Swarm models. Audited 2026-03-07.

## Gated Delta Networks (GDN)

The defining feature of Qwen3.5. 75% of transformer layers use GDN (linear attention, O(n) complexity) instead of standard attention (O(n^2)). Layers alternate in blocks:

```
Block pattern: [GDN] [GDN] [GDN] [Standard Attention]
                 75%                    25%
```

GDN layers handle the bulk of context processing at linear cost. Standard attention layers (every 4th) provide the full-context reasoning capability. This hybrid design is what enables 262K native context without the quadratic memory blowup.

## Model Size Table

| Model | Total Params | Active Params | Layers | Hidden Dim | Experts | Active Experts |
|-------|-------------|---------------|--------|------------|---------|----------------|
| Qwen3.5-397B-A17B | 397B | 17B | 94 | 6400 | 256 | 8+1 |
| Qwen3.5-122B-A10B | 122B | 10B | 80 | 4096 | 256 | 8+1 |
| **Qwen3.5-35B-A3B** | 35B | 3B | 64 | 2560 | 256 | 8+1 |
| **Qwen3.5-27B** | 27B | 27B | 64 | 5120 | -- | Dense |
| **Qwen3.5-9B** | 9B | 9B | 48 | 3584 | -- | Dense |
| Qwen3.5-4B | 4B | 4B | 36 | 2560 | -- | Dense |
| **Qwen3.5-2B** | 2B | 2B | 28 | 1536 | -- | Dense |
| Qwen3.5-0.8B | 0.8B | 0.8B | 24 | 1024 | -- | Dense |

**Bold = models used as Swarm fleet bases**

MoE models (35B, 122B, 397B): 256 total experts, 8 routed + 1 shared active per token, 512 expert intermediate dim.

Dense models (0.8B through 27B): All parameters active on every token.

## Attention Configuration

### GDN Layers (75% of blocks)

| Model | V Heads | QK Heads | Head Dim |
|-------|---------|----------|----------|
| 35B-A3B | 32 | 16 | 128 |
| 27B | 48 | 16 | 128 |
| 9B | 32 | 16 | 128 |
| 4B | 20 | 20 | 128 |
| 2B | 12 | 12 | 128 |

### Standard Attention Layers (25% of blocks)

| Model | Q Heads | KV Heads | Head Dim | RoPE |
|-------|---------|----------|----------|------|
| 35B-A3B | 16 | 2 | 256 | Yes |
| 27B | 24 | 4 | 256 | Yes |
| 9B | 16 | 4 | 256 | Yes |
| 4B | 20 | 4 | 128 | Yes |
| 2B | 12 | 4 | 128 | Yes |

Standard attention layers use grouped-query attention (GQA) with fewer KV heads than Q heads. GDN layers use separate V and QK head counts.

## 35B-A3B MoE Details

- 256 total experts, 8 routed + 1 shared = 9 active per token
- Expert intermediate dim: 512
- Total 35B params, only 3B active -- extreme sparsity
- Used by: SwarmPharma-35B, SwarmCRE-35B

## Tokenizer

- **Vocabulary**: 248,320 tokens (63% larger than Qwen3's 151,936)
- **Special tokens**: `<|im_start|>` (248045), `<|im_end|>` (248046), `<|endoftext|>` (248044), `</think>` (248069)
- **EOS**: `<|im_end|>`
- **Byte-level fallback**: Handles any UTF-8 input without UNK tokens
- **Impact**: Larger vocabulary means more efficient encoding (fewer tokens per input) but larger embedding table in memory

## Context Length

- **Native**: 262,144 tokens (262K) -- all sizes from 0.8B through 397B
- **Extended**: up to 1,010,000 tokens via YaRN (Yet another RoPE extensioN)
- **Minimum recommended**: 128K to preserve thinking capabilities

## Think Mode

Think mode is ON by default for 9B+ models. Smaller models (0.8B, 2B, 4B) default to non-thinking.

| Model | Default Mode | Think Available |
|-------|-------------|-----------------|
| 397B-A17B | Thinking | Yes |
| 122B-A10B | Thinking | Yes |
| 35B-A3B | Thinking | Yes |
| 27B | Thinking | Yes |
| 9B | Thinking | Yes |
| 4B | Non-thinking | No |
| 2B | Non-thinking | No |
| 0.8B | Non-thinking | No |

There is no soft-switch (unlike Qwen3 which allowed toggling via system prompt).

### Controlling Think Mode

- **Disable**: Set `enable_thinking=False` in the generation config or chat template
- **Enable** (default for 9B+): Model generates internal `<think>...</think>` reasoning before the visible response
- **Token budget**: Think tokens count against `max_tokens`. Set 4096+ to avoid truncation.
- **GGUF**: `reasoning_content` field separates think from content
- **SFT**: Training data without think tokens works fine -- SFT overrides base behavior

### Behavioral Notes

- Short system prompts cause reasoning loops (model thinks in circles with insufficient context)
- Long, detailed system prompts produce focused reasoning
- Greedy decoding (`do_sample=False`) breaks think mode entirely -- always sample
- `presence_penalty=1.5` helps prevent repetitive reasoning chains
- Think mode reasoning appears in `reasoning_content` field (some frameworks) or inline `<think>` tags

## Sampling Parameters

Four recommended configurations:

| Mode | temp | top_p | top_k | presence_penalty | Use Case |
|------|------|-------|-------|-----------------|----------|
| Think -- general | 1.0 | 0.95 | 20 | 1.5 | Open-ended analysis, strategic reasoning |
| Think -- coding | 0.6 | 0.95 | 20 | 0.0 | Code generation, structured output |
| Instruct -- general | 0.7 | 0.8 | 20 | 1.5 | Classification, evaluation, scoring |
| Instruct -- reasoning | 1.0 | 1.0 | 40 | 2.0 | Multi-step reasoning without think tokens |

**CRITICAL**: Never use `do_sample=False` (greedy decoding breaks thinking entirely).

## VRAM Requirements

| Model | bf16 | Q8_0 | Q4_K_M | Training (LoRA r=64) |
|-------|------|------|--------|---------------------|
| 0.8B | 1.6GB | 0.8GB | 0.5GB | 8GB |
| 2B | 4GB | 2GB | 1.2GB | 8GB |
| 4B | 8GB | 4GB | 2.5GB | 16GB |
| 9B | 19GB | 9GB | 5.5GB | 24GB |
| 27B | 54GB | 27GB | 16GB | 96GB |
| 35B-A3B | 67GB | 35GB | 20GB | 96GB |
| 122B-A10B | 244GB | 122GB | 72GB | Unreachable |

## Framework Support

| Framework | Dense (0.8B-27B) | MoE (35B-A3B) | Notes |
|-----------|-------------------|----------------|-------|
| transformers | Yes | Yes | |
| vLLM | Yes | Yes | Requires --skip-mm-profiling --enforce-eager |
| SGLang | Yes | Yes | |
| llama.cpp | Yes | Yes | |
| Ollama | Yes | **NO** | Does not support 35B MoE as of March 2026 |
| Unsloth | Yes | Yes | bf16 LoRA only, AutoTokenizer bypass required |

### Unsloth Training Notes

- **AutoTokenizer bypass**: Qwen3.5 triggers a VL (vision-language) model dispatch in AutoTokenizer. Must bypass by loading the tokenizer directly.
- **packing=True**: Required for efficient training. 6x speedup over unpacked.
- **No QLoRA**: Qwen3.5 architecture has "higher than normal quantization differences." bf16 LoRA only.
- **LoRA targets**: Must cover BOTH GDN projections (75% of layers) AND standard attention projections (25%). Missing either set means most of the model is untrainable.
- **train_on_responses_only**: Consider for reasoning models -- masks instruction tokens so the model only learns to generate responses, not to repeat prompts.

### vLLM Deployment Notes

- Unsloth merge bakes VL weights into the checkpoint. Must copy `vision_config` from base model into merged config.json, with `out_hidden_size` matching text hidden_size.
- Required flags: `--skip-mm-profiling --enforce-eager --limit-mm-per-prompt '{"image": 0}'`

## Known Weaknesses

Based on testing across the Swarm fleet:

1. **Short system prompts cause infinite reasoning loops.** Fix: use long, structured system prompts (SKILL.md injection).
2. **Tool calling broken in Ollama.** Use vLLM or SGLang instead.
3. **Greedy decoding breaks thinking entirely.** Always sample.
4. **35B-A3B MoE: 64x slowdown at 100K context** without optimization (Flash attention, KV cache quantization).
5. **GGUF template bugs** in some Unsloth quants -- test before deploying.
6. **Coding reliability**: Occasionally generates syntactically valid but logically wrong code in complex multi-file scenarios.

## Open Issues

| # | Issue | Impact on Swarm |
|---|-------|-----------------|
| #48 | KV-cache breaks when thinking disabled | May affect llama-server deployments using enable_thinking=False |
| #33 | Undertrained long tokens cause semantic collapse | Long CRE/Pharma documents near context boundary |
| #26 | Missing reasoning_content in tool calling | Agent/skill routing with think mode active |
| #65 | MTP fine-tune not supported yet | Cannot leverage multi-token prediction in LoRA training |

## Benchmarks (Base Models)

| Benchmark | 9B | 27B | 35B-A3B |
|-----------|-----|------|---------|
| MMLU-Pro | 82.5 | -- | 85.3 |
| GPQA Diamond | 81.7 | 85.8 | 84.2 |
| IFEval | 91.5 | -- | 91.9 |
| SWE-Bench Verified | -- | -- | 69.2 |
| SWE-Bench Hard | -- | -- | 37.8 |
| LongBench | 55.2 | -- | -- |

The 9B is the standout -- it beats Qwen3-30B on MMLU-Pro (82.5 vs 80.9), GPQA (81.7 vs 73.4), and LongBench (55.2 vs 44.8). This is the GDN architecture paying dividends: a 9B model with linear attention outperforms a 30B model with standard attention.
