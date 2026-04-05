# MINER × Energy — Clock Settings Analysis

The energy tracker now captures GPU clock data alongside power metrics. This page documents baseline clock profiles for analysis and optimization.

## Live Data Source

```bash
# Local (reads nvidia-smi directly)
python3 /home/swarm/google-gemma-4-FTW/edge/energy_tracker.py

# JSON (for programmatic use)
python3 /home/swarm/google-gemma-4-FTW/edge/energy_tracker.py --json

# API (from anywhere)
curl -s https://swarmandbee.ai/deed/api/energy
```

## Baseline Clock Profile — Gemma 4 31B Cook (April 2026)

Captured during production training. This is the untuned baseline to improve on.

### GPU0 — Training (QLoRA, 300W power cap)

| Metric | Value | % of Max | Notes |
|--------|-------|----------|-------|
| Core Clock | 990 MHz | 32.0% | Power-throttled, cores waiting on memory |
| Core Max | 3,090 MHz | — | Available but unused (power budget) |
| Memory Clock | 13,365 MHz | 95.5% | Near max, THIS is the bottleneck |
| Memory Max | 14,001 MHz | — | 636 MHz headroom |
| Power Draw | 300W | 50% of 600W | SW Power Cap active |
| GPU Util | 99% | — | Looks busy, but cores are stalling |
| Memory Util | 43-44% | — | Memory bandwidth is the constraint |
| Temperature | 80-85°C | — | Well under 90°C limit |
| Throttle | ⚠ SW Power Cap | — | Active for 53+ hours continuous |
| Step Rate | ~64s/step | — | 5.33 Wh/step |

**Analysis:** Core running at 32% capacity. Memory at 95.5%. The 300W power budget is being burned on core clocks that do nothing useful — the cores are idle-waiting on memory transfers. Memory has 636 MHz of untapped bandwidth.

### GPU1 — Tribunal Judge A (gemma3:12b inference, 300W cap)

| Metric | Value | % of Max | Notes |
|--------|-------|----------|-------|
| Core Clock | 1,612 MHz | 52.2% | Higher than training (prefill compute) |
| Memory Clock | 13,365 MHz | 95.5% | Same as GPU0 |
| Power Draw | 300W | 50% of 600W | SW Power Cap active |
| GPU Util | 87% | — | Mixed compute+memory workload |
| Memory Util | 50% | — | More memory-bound than training |
| Temperature | 69°C | — | Cool, has thermal headroom |
| Throttle | ⚠ SW Power Cap | — | Active |

**Analysis:** Inference is more balanced (52% core vs 32% for training). Legal/grants pairs are long → more KV cache → more memory pressure (50% mem util). Core could be lower for long-pair domains, higher for short-pair domains.

## Next Cook — Experiment Plan

When the current cook finishes (checkpoint 2,880 decision), the next cook starts with tuned clocks:

### Phase 1: Baseline (first 320 steps)
```
Core: auto | Memory: auto | Power: 300W
Measure: steps/sec, temperature, actual clocks
```

### Phase 2: Memory Max (steps 320-640)
```
Core: auto | Memory: 14,001 MHz (locked max) | Power: 300W
Measure: steps/sec delta, temperature change
```

### Phase 3: Core Lock + Memory Max (steps 640-960)
```
Core: 1,000 MHz (locked) | Memory: 14,001 MHz | Power: 250W
Measure: steps/sec, power savings, temperature
```

### Phase 4: Sweet Spot Search (steps 960+)
```
Iterate: find the power limit where steps/sec stops improving
Chart: power (W) vs steps/sec vs temperature
```

### What We're Looking For

```
steps/sec
    ^
    |     ╭──────────── plateau (memory-bound ceiling)
    |    ╱
    |   ╱
    |  ╱   ← sweet spot is where curve flattens
    | ╱
    |╱
    └─────────────────> power (W)
    150  200  250  300  350  400
```

The sweet spot is where the curve flattens — more power stops buying more speed. That's the optimal power limit. Everything above it is waste.

## Domain-Specific Clock Analysis

Grants pairs (long) push memory harder than CRE pairs (short). The optimal clock profile depends on what you're cooking or scoring:

| Domain | Avg Pair Size | Memory Pressure | Optimal Core | Optimal Memory |
|--------|--------------|-----------------|-------------|---------------|
| Grants | 10K+ chars | HIGH (large KV) | 1,000-1,200 MHz | 14,001 MHz |
| Legal | 8K+ chars | HIGH | 1,000-1,200 MHz | 14,001 MHz |
| Medical | 6K chars | MEDIUM | 1,200-1,500 MHz | 14,001 MHz |
| CRE | 3-5K chars | LOWER | 1,500-1,800 MHz | 13,365 MHz |
| Aviation | 3-5K chars | LOWER | 1,500-1,800 MHz | 13,365 MHz |

## Blackwell Fleet — Complete Clock Reference

### RTX PRO 6000 Blackwell (96GB GDDR7)

| Parameter | Min | Max | Training | Inference (long) | Inference (short) | Idle |
|-----------|-----|-----|----------|-----------------|------------------|------|
| Core | 180 MHz | 3,090 MHz | 1,000 MHz | 1,200 MHz | 1,800 MHz | 210 MHz |
| Memory | — | 14,001 MHz | 14,001 MHz | 14,001 MHz | 13,365 MHz | auto |
| Power | 150W | 600W | 250W | 200W | 275W | 150W |
| Temp target | — | 90°C | < 85°C | < 80°C | < 82°C | — |

### RTX PRO 4500 Blackwell (32GB GDDR7)

| Parameter | Min | Max | Inference (7B) | Inference (12B) | Idle |
|-----------|-----|-----|---------------|----------------|------|
| Core | ~180 MHz | 2,617 MHz | 1,200 MHz | 1,400 MHz | 210 MHz |
| Memory | — | ~14,001 MHz | 14,001 MHz | 14,001 MHz | auto |
| Power | ~100W | 200W | 120W | 150W | 100W |
| Temp target | — | 85°C | < 75°C | < 80°C | — |

### RTX 3090 (24GB GDDR6X)

| Parameter | Min | Max | Inference (7B) | Inference (12B) | Idle |
|-----------|-----|-----|---------------|----------------|------|
| Core | ~210 MHz | 1,695 MHz | 1,200 MHz | 1,400 MHz | 210 MHz |
| Memory | — | 9,751 MHz | auto | auto | auto |
| Power | ~100W | 350W | 150W | 200W | 100W |
| Temp target | — | 93°C | < 85°C | < 85°C | — |
| VRAM target | — | 110°C | < 95°C | < 100°C | — |

### Xeon w9-3475X (CPU)

| Parameter | Min | Max | AI Inference | Mining (RandomX) | Idle |
|-----------|-----|-----|-------------|-----------------|------|
| Core | 800 MHz | 4,800 MHz | 4,800 MHz (turbo) | 4,800 MHz | 800 MHz |
| Governor | — | — | performance | performance | powersave |
| DDR5 | — | 4,800 MT/s | 4,800 MT/s | 4,800 MT/s | auto |
| Huge Pages | 0 | 256GB | 16GB (1GB pages) | 16GB (1GB pages) | 0 |
| TDP | — | 360W (MTP) | 300W | 300W | ~100W |

---

*Updated: 2026-04-05 — Baseline captured during Gemma 4 31B cook (step 2,655/3,204)*
