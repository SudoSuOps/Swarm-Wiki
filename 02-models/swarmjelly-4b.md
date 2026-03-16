# SwarmJelly-4B

Self-healing model that converts propolis-tier failures into royal_jelly training pairs.

## Overview

| Field | Value |
|-------|-------|
| Base | Qwen3.5-4B |
| Status | DEPLOYED |
| Training Data | 5,000 propolis->RJ repair cells |
| Format | Q4_K_M GGUF |
| Location | swarmrails:8085 (CPU, AMX+mlock) |
| Throughput | 1,083 tok/s prompt processing |

## Architecture

SwarmJelly is a closed-loop self-improvement system:

```
propolis pairs (score < 70)
    |
    v
SwarmJelly-4B infers improved response
    |
    v
RJ quality gate (mechanism + tradeoff + density)
    |
    v
Pass -> stamp as royal_jelly, push to ledger
Fail -> log failure mode, retry with adjusted params
```

## Pipeline

`pipeline_swarmjelly.py` implements the 5-stage loop:

1. **propolis** -- Pull lowest-scoring pairs from D1
2. **infer** -- SwarmJelly generates improved response
3. **vet** -- 3-gate RJ quality check
4. **stamp** -- HiveCell stamping with full provenance
5. **push** -- Push to hive-ledger as new batch

## Deployment

Running on swarmrails CPU via llama-server:

```bash
llama-server \
  -m swarmjelly-4b-q4_k_m.gguf \
  --host 0.0.0.0 --port 8085 \
  -c 4096 --mlock
```

The Xeon 3475's AMX (Advanced Matrix Extensions) accelerates BF16/INT8 matrix ops, achieving 1,083 tok/s on prompt processing -- fast enough for batch inference without GPU.

## Training

Trained on 5,000 cells derived from propolis failures. Each cell contains the original failed pair, the failure analysis, and a corrected response that passes RJ quality gates. The model learns to recognize and repair common failure modes:

- Missing causal reasoning chains
- Absent domain-specific terminology
- Lack of quantitative evidence
- Generic filler instead of specific analysis

## Systemd Units

Written for deployment on swarmrails rig:
- `swarmjelly-server.service` -- llama-server process
- `swarmjelly-pipeline.service` -- continuous pipeline loop

Install: `scp + sudo bash install.sh` on swarmrails.
