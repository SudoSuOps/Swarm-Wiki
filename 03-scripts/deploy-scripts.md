# Deploy Scripts

Deployment pipeline: Merge (Unsloth) -> Quantize (llama.cpp) -> Serve (vLLM or llama-server).

## Step 1: Merge LoRA Adapters

After training, merge LoRA adapters into a full-weight model using Unsloth's `save_pretrained_merged()`.

```python
model.save_pretrained_merged("merged_16bit")
```

This produces a standard HuggingFace model directory with merged bf16 weights. The merge scripts live on swarmrails at `/data2/swarm-qwen27b/run_merge.sh`.

### Qwen3.5 Config Fix (Required)

After merging, the output `config.json` is missing `vision_config` fields that vLLM expects. You must copy `vision_config` from the base Qwen3.5 model into the merged model's `config.json`.

**Critical**: `out_hidden_size` in the vision config must match the text model's `hidden_size`. If they do not match, vLLM will crash on startup with a dimension mismatch error.

```bash
# Example: copy vision_config from base model
python3 -c "
import json
base = json.load(open('/path/to/base/qwen3.5/config.json'))
merged = json.load(open('/path/to/merged/config.json'))
merged['vision_config'] = base['vision_config']
json.dump(merged, open('/path/to/merged/config.json', 'w'), indent=2)
"
```

## Step 2: Quantize (Optional -- for GGUF Deployment)

Quantize merged models using llama.cpp's `llama-quantize` for edge deployment or CPU inference.

```bash
# Convert HF model to GGUF
python3 /home/swarm/llama.cpp/convert_hf_to_gguf.py /path/to/merged --outfile model-f16.gguf

# Quantize to Q4_K_M (recommended for edge)
/home/swarm/llama.cpp/llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M

# Other quantization levels
/home/swarm/llama.cpp/llama-quantize model-f16.gguf model-q8_0.gguf Q8_0
/home/swarm/llama.cpp/llama-quantize model-f16.gguf model-f16.gguf F16
```

**Note**: llama.cpp on swarmrails is currently built for sm_86 only. It needs a rebuild for sm_120 (Blackwell) to use GPU acceleration. CPU quantization still works.

## Step 3: Serve via vLLM (Primary)

vLLM 0.17.0 is the primary inference server on swarmrails. PyTorch CUDA 12.8 with native sm_86 + sm_120 support.

### Launch Command

```bash
vllm serve /path/to/merged \
  --language-model-only \
  --skip-mm-profiling \
  --enforce-eager \
  --limit-mm-per-prompt '{"image": 0}' \
  --port 808N
```

### Required Flags for Qwen3.5

| Flag | Why |
|------|-----|
| `--language-model-only` | Skips vision encoder loading |
| `--skip-mm-profiling` | Avoids multimodal memory profiling crash |
| `--enforce-eager` | Prevents CUDA graph issues on Blackwell |
| `--limit-mm-per-prompt '{"image": 0}'` | Disables image input processing |

### Current Deployments

| Model | Port | GPU | VRAM | Throughput |
|-------|------|-----|------|------------|
| SwarmCurator-9B (bf16) | 8081 | GPU 0 (RTX PRO 4500) | 23.5GB | 165 tok/s (4 concurrent) |
| SwarmCurator-27B (bf16) | 8082 | GPU 1 (RTX PRO 6000) | 93GB | 88 tok/s (4 concurrent) |

Combined throughput: ~1,740 pairs/hr with `--workers 4` concurrent generation.

### Launch Scripts on swarmrails

```
/data2/swarm-qwen27b/run_merge.sh   -- Merge LoRA adapters
/data2/swarm-qwen27b/run_serve.sh   -- Start vLLM server
/data2/swarm-qwen27b/run_infer.sh   -- Quick inference smoke test
/tmp/start_vllm_9b.sh               -- Launch 9B on :8081
/tmp/start_vllm_27b.sh              -- Launch 27B on :8082
```

## GPU Power Management

Set power limits before long inference or training runs to prevent thermal throttling.

```bash
# RTX PRO 6000 Blackwell (96GB) -- GPU 1
sudo nvidia-smi -i 1 -pl 350

# RTX PRO 4500 Blackwell (32GB) -- GPU 0
sudo nvidia-smi -i 0 -pl 200
```

Always use `CUDA_DEVICE_ORDER=PCI_BUS_ID` on swarmrails for consistent GPU numbering.

## Alternative: llama-server (Legacy)

llama-server via llama.cpp was the previous inference backend. It has been replaced by vLLM for production use because:

- Limited to sm_86 (no Blackwell GPU acceleration)
- Sequential inference only (no concurrent batching)
- No OpenAI-compatible API out of the box

Still useful for quick GGUF testing on whale or edge nodes:

```bash
/home/swarm/llama.cpp/llama-server \
  -m model-q4_k_m.gguf \
  --port 8081 \
  --ctx-size 32768 \
  --n-gpu-layers 99
```

## GGUF Inventory

| Model | Quant | Size | Location |
|-------|-------|------|----------|
| SwarmPharma-35B | Q4_K_M | 20GB | swarmrails |
| BeeMini (Router v2) | Q4_K_M | 1.8GB | whale:8081 |
| SwarmSignal-2B | Q4_K_M | 1.2GB | signal-edge-01 |
| BitNet b1.58-2B | GGUF | 1.2GB | zima-edge-1 |
