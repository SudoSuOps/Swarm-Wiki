# GPU Operations — Blackwell Clock Tuning & Power Management

Power management, clock optimization, and the MINER discipline: tune GPUs like a mining rig for maximum work-per-watt.

## Fleet (April 2026)

| GPU | Card | VRAM | Architecture | Max Power | Max Core | Max Mem | Role |
|-----|------|------|-------------|-----------|----------|---------|------|
| GPU0 | RTX PRO 6000 Blackwell | 96GB GDDR7 | sm_120 | 600W | 3,090 MHz | 14,001 MHz | Training (cook) |
| GPU1 | RTX PRO 6000 Blackwell | 96GB GDDR7 | sm_120 | 600W | 3,090 MHz | 14,001 MHz | Judge A (inference) |
| Whale | RTX 3090 | 24GB GDDR6X | sm_86 | 350W | 1,860 MHz | 9,751 MHz | Judge B (inference) |

## MINER — The Mining Discipline Applied to AI

The same clock tuning that crypto miners use to maximize hashrate-per-watt applies to AI training and inference. Different workloads have different optimal clock profiles — just like different mining algorithms.

### Blackwell RTX PRO 6000 — Full Clock Chart

```
╔══════════════════════════════════════════════════════════════════╗
║           RTX PRO 6000 BLACKWELL — CLOCK CHART                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  CORE CLOCK (Graphics)                                           ║
║  ├─ Minimum:     180 MHz                                         ║
║  ├─ Idle:        210 MHz                                         ║
║  ├─ Training:  1,000 - 1,300 MHz  ← sweet spot (memory-bound)   ║
║  ├─ Inference: 1,200 - 1,800 MHz  ← sweet spot (mixed)          ║
║  ├─ Boost:     2,610 MHz (auto)                                  ║
║  └─ Maximum:   3,090 MHz (all-out)                               ║
║                                                                  ║
║  MEMORY CLOCK (GDDR7)                                            ║
║  ├─ Idle:       auto                                             ║
║  └─ Maximum:  14,001 MHz  ← ALWAYS push to max for AI workloads ║
║                                                                  ║
║  POWER LIMIT                                                     ║
║  ├─ Minimum:     150W (standby/idle)                             ║
║  ├─ Training:    250 - 300W  ← current cook at 300W              ║
║  ├─ Inference:   200 - 300W  ← depends on throughput target      ║
║  ├─ Default:     400W (TDP)                                      ║
║  └─ Maximum:     600W (absolute max)                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Why Training is Memory-Bound (The ETH Mining Parallel)

| | ETH Mining | QLoRA Training |
|---|-----------|---------------|
| Bottleneck | DAG file in VRAM | Weight matrices in VRAM |
| Core usage | Low — hashing is simple | Low — cores wait on memory transfers |
| Memory usage | HIGH — DAG must fit and stream | HIGH — 32GB+ weight matrices moving |
| Optimal core | Lower = less power, same hashrate | Lower = less power, same steps/sec |
| Optimal memory | MAX = more bandwidth = more hashrate | MAX = more bandwidth = faster steps |
| Power saved | On core (doing nothing useful) | On core (idle-waiting on memory) |

**Real data from GPU0 during Gemma 4 31B cook:**
```
Core clock:   1,312 MHz / 3,090 MHz max (42% — power throttled, but cores are WAITING)
Memory clock: 13,365 MHz / 14,001 MHz max (95% — this is the bottleneck)
GPU util:     99%  (looks busy, but cores are stalling on memory)
Memory util:  39%  (memory bandwidth is the constraint)
Throttle:     SW Power Cap ACTIVE for 53+ hours straight
Temperature:  80-84°C (well under 90°C thermal limit)
```

The GPU is burning watts running cores at 1,312 MHz that spend most of their time waiting for memory. Lower the core, push memory to max, save power or go faster.

### Flight Sheets — Domain-Specific GPU Profiles

```
┌─────────────────────────────────────────────────────────────┐
│  FLIGHT SHEET: TRAINING (QLoRA Fine-Tuning)                 │
│  Workload: Memory-bandwidth bound                           │
│  Core:     1,000 - 1,200 MHz (locked low)                   │
│  Memory:   14,001 MHz (locked max)                          │
│  Power:    250 - 300W                                       │
│  Target:   < 5.0 Wh/step                                   │
│  Rationale: Cores wait on memory. Save power on core.       │
├─────────────────────────────────────────────────────────────┤
│  FLIGHT SHEET: INFERENCE — LONG PAIRS (grants, legal, med)  │
│  Workload: Memory-bound (large KV cache, long decode)       │
│  Core:     1,200 - 1,500 MHz                                │
│  Memory:   14,001 MHz (locked max)                          │
│  Power:    200 - 250W                                       │
│  Target:   > 400 pairs/hr                                   │
│  Rationale: Long pairs = big KV cache = memory bandwidth    │
├─────────────────────────────────────────────────────────────┤
│  FLIGHT SHEET: INFERENCE — SHORT PAIRS (CRE, aviation)      │
│  Workload: Compute-bound (fast prefill, short decode)       │
│  Core:     1,800 - 2,100 MHz                                │
│  Memory:   14,001 MHz                                       │
│  Power:    250 - 300W                                       │
│  Target:   > 800 pairs/hr                                   │
│  Rationale: Short pairs = more compute per token ratio      │
├─────────────────────────────────────────────────────────────┤
│  FLIGHT SHEET: IDLE / STANDBY                               │
│  Core:     210 MHz (minimum)                                │
│  Memory:   auto                                             │
│  Power:    150W (minimum)                                   │
│  Apply:    Between domains, waiting for work, overnight      │
└─────────────────────────────────────────────────────────────┘
```

### Experiment Matrix

| Profile | Power | Core Lock | Mem Lock | Workload | Expected Outcome |
|---------|-------|-----------|----------|----------|-----------------|
| BASELINE | 300W | auto (1312) | auto (13365) | Training | 64s/step, 300W, 5.33 Wh/step |
| MEM-MAX | 300W | 1200 MHz | 14001 MHz | Training | Same speed, lower temp |
| EFFICIENT | 250W | 1000 MHz | 14001 MHz | Training | ~66s/step, 250W, 4.58 Wh/step |
| POWER-UP | 350W | auto | 14001 MHz | Training | ~58s/step, 350W |
| FULL-SEND | 400W | auto | 14001 MHz | Training | ~52s/step, 400W |
| INF-BALANCED | 250W | 1500 MHz | 14001 MHz | Inference | Sweet spot for tribunal |
| INF-EFFICIENT | 200W | 1200 MHz | 14001 MHz | Inference | Max pairs/watt |
| INF-THROUGHPUT | 300W | 2100 MHz | 14001 MHz | Inference | Max pairs/hr |

### Commands

```bash
# Check current state
nvidia-smi --query-gpu=index,clocks.gr,clocks.mem,power.draw,power.limit,temperature.gpu,utilization.gpu,utilization.memory --format=csv,noheader

# Check throttle reasons
nvidia-smi -q -d PERFORMANCE | grep -A 8 "Clocks Event Reasons"

# Set power limit
sudo nvidia-smi -i 0 -pl 250          # GPU0 to 250W
sudo nvidia-smi -i 1 -pl 200          # GPU1 to 200W

# Lock clocks
sudo nvidia-smi -i 0 -lgc 1000,1200   # Core: 1000-1200 MHz
sudo nvidia-smi -i 0 -lmc 14001       # Memory: max

# Reset to auto
sudo nvidia-smi -i 0 -rgc             # Reset core
sudo nvidia-smi -i 0 -rmc             # Reset memory

# Persistence mode (survives sleep)
sudo nvidia-smi -pm 1

# Full status (energy tracker)
python3 /home/swarm/google-gemma-4-FTW/edge/energy_tracker.py
```

### Whale RTX 3090 — Clock Chart

```
╔══════════════════════════════════════════════════════╗
║       RTX 3090 — CLOCK CHART (JUDGE B)               ║
╠══════════════════════════════════════════════════════╣
║  Core:    210 - 1,860 MHz (inference: 1,200 MHz)     ║
║  Memory:  up to 9,751 MHz                            ║
║  Power:   100W - 350W (currently capped at 150W)     ║
║  GDDR6X:  memory-bound for 7B inference              ║
║  SSH:     ssh swarm@192.168.0.99                      ║
╚══════════════════════════════════════════════════════╝
```

### Benefits of Clock Tuning

| Benefit | How | Impact |
|---------|-----|--------|
| **Reduce energy cost** | Lower core clock on memory-bound workloads | 15-25% power savings |
| **Extend GPU lifespan** | Lower temps = less thermal cycling = longer life | Years of additional service |
| **Boost throughput** | Push memory to max on bandwidth-bound workloads | 3-8% speed improvement |
| **Domain optimization** | Different clock profiles for different pair lengths | Better pairs/watt per domain |
| **Better models** | Stable temps = more consistent gradient computation | Potentially better convergence |
| **Marketing** | "We tune our GPUs like miners tune their rigs" | Differentiation story |

### The Discovery

> GPU cores at 42% of max clock, power-throttled for 53 hours straight, while memory runs at 95% of max. The cores are burning watts doing nothing — waiting on memory. This is ETH mining all over again: the hashrate is in the memory, not the cores. Lower the core, push the memory, save the watts.

This is not theoretical. This is measured on production hardware under real training load. The experiment matrix above will quantify the exact savings.

---

## CUDA Device Ordering

Always set on swarmrails for consistent GPU numbering:

```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
```

| CUDA Index | GPU | VRAM | PCI Bus |
|------------|-----|------|---------|
| 0 | RTX PRO 6000 Blackwell | 96GB | 16:00.0 |
| 1 | RTX PRO 6000 Blackwell | 96GB | AC:00.0 |

## Blackwell sm_120 Compatibility

Pre-built CUDA acceleration packages need rebuilds for sm_120:

| Package | Status |
|---------|--------|
| flash_attn | undefined symbol — does not load |
| causal_conv1d | no kernel for sm_120 |
| flash-linear-attention | falls back to torch |

All training works with eager attention fallback. vLLM with `--enforce-eager` handles inference correctly.

## Monitoring

```bash
# Real-time GPU utilization
watch -n 1 nvidia-smi

# Structured query (full)
nvidia-smi --query-gpu=index,name,clocks.gr,clocks.mem,power.draw,power.limit,temperature.gpu,pstate,utilization.gpu,utilization.memory --format=csv,noheader

# Energy economics
python3 /home/swarm/google-gemma-4-FTW/edge/energy_tracker.py

# Throttle analysis
nvidia-smi -q -d PERFORMANCE | grep -A 15 "Clocks Event Reasons"
```
