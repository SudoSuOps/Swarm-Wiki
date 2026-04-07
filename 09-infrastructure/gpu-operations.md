# GPU Operations — Blackwell Clock Tuning & Power Management

Power management, clock optimization, and the MINER discipline: tune GPUs like a mining rig for maximum work-per-watt.

## Fleet (April 2026)

| GPU | Card | VRAM | Architecture | Max Power | Max Core | Max Mem | Bandwidth | Role |
|-----|------|------|-------------|-----------|----------|---------|-----------|------|
| GPU0 | RTX PRO 6000 Blackwell | 96GB GDDR7 | sm_120 | 600W | 3,090 MHz | 14,001 MHz | 1,792 GB/s | Training (cook) |
| GPU1 | RTX PRO 6000 Blackwell | 96GB GDDR7 | sm_120 | 600W | 3,090 MHz | 14,001 MHz | 1,792 GB/s | Scale A (inference) |
| GPU0 | RTX PRO 6000 Blackwell | 96GB GDDR7 | sm_120 | 600W | 3,090 MHz | 14,001 MHz | 1,792 GB/s | Scale B (inference) |
| Fleet (48x) | RTX PRO 4500 Blackwell | 32GB GDDR7 | sm_120 | 200W | 2,617 MHz | ~14,001 MHz | 896 GB/s | Expansion (Blackwell) |
| Fleet (100x) | RTX 3090 | 24GB GDDR6X | sm_86 | 350W | 1,695 MHz | 9,751 MHz | 936 GB/s | Expansion (Ampere) |

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

### RTX PRO 4500 Blackwell — The Fleet Card (48 incoming)

```
╔══════════════════════════════════════════════════════════════════╗
║           RTX PRO 4500 BLACKWELL — CLOCK CHART                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  GPU:         GB203 (Blackwell, sm_120, same arch as 6000)       ║
║  CUDA Cores:  10,496 (82 SMs)                                   ║
║  Tensor:      328 (5th gen) — FP4/FP8/INT8/BF16                 ║
║  VRAM:        32GB GDDR7 — ECC — 256-bit                        ║
║  Bandwidth:   896 GB/s                                           ║
║                                                                  ║
║  CORE CLOCK (Graphics)                                           ║
║  ├─ Base:      1,590 MHz                                         ║
║  ├─ Boost:     2,617 MHz                                         ║
║  ├─ Inference:  1,200 - 1,600 MHz  ← sweet spot (7B-12B models) ║
║  └─ Idle:       ~210 MHz                                         ║
║                                                                  ║
║  MEMORY CLOCK (GDDR7)                                            ║
║  └─ Maximum:  ~14,001 MHz  ← same GDDR7 tech as 6000            ║
║                                                                  ║
║  POWER LIMIT                                                     ║
║  ├─ Minimum:     ~100W (est, verify with nvidia-smi)             ║
║  ├─ Inference:    120 - 150W  ← sweet spot for 7B-12B scoring    ║
║  ├─ Default:      200W (TDP workstation)                         ║
║  └─ Server Ed:    165W (single-slot, max density)                ║
║                                                                  ║
║  FLEET ECONOMICS (48 cards)                                      ║
║  ├─ Total VRAM:   1,536 GB (1.5 TB)                             ║
║  ├─ Total Power:  9,600W max / ~6,000W tuned                    ║
║  ├─ Total Cost:   $132,000 (48 × $2,750)                        ║
║  ├─ $/GB VRAM:    $85.94                                         ║
║  ├─ Cores/Watt:   52.5 (vs 23.3 on 6000 at 600W)               ║
║  └─ Use case:     1 model per card, inference fleet              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why the 4500 is the perfect fleet card:**

| Metric | RTX PRO 6000 | RTX PRO 4500 | 4500 Advantage |
|--------|-------------|-------------|----------------|
| VRAM | 96GB | 32GB | Right-sized for 7B-12B inference |
| TDP | 400W (default) | 200W | 2x more efficient by design |
| CUDA Cores | 24,576 | 10,496 | Still 10K+ cores for inference |
| Bandwidth | 1,792 GB/s | 896 GB/s | Sufficient for single-model serving |
| Price | ~$7,500 | ~$2,750 | 2.7x cheaper |
| Cores/Watt | 23.3 (at 600W) | 52.5 (at 200W) | 2.25x more cores per watt |
| Form factor | Dual-slot | Dual-slot (or single-slot server) | Density option |
| Architecture | sm_120 | sm_120 | Same Blackwell, same software |

**Fleet deployment pattern:** Each 4500 runs one model (gemma3:12b quantized = ~8GB, qwen2.5:32b quantized = ~20GB). At 150W per card, 48 cards = 7.2 kW running 48 independent scales. That's 48 parallel scoring threads. At 380 pairs/hr per scale pair, 24 parallel tribunal pairs = **9,120 pairs/hr**. The 163-day wall becomes **7 days**.

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
║       RTX 3090 — CLOCK CHART (WHALE)                  ║
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

## Xeon w9-3475X Sapphire Rapids — CPU Mining Profile

The CPU is a compute node. Same tuning discipline. Same economics.

```
╔══════════════════════════════════════════════════════════════════╗
║           XEON w9-3475X SAPPHIRE RAPIDS                          ║
╠══════════════════════════════════════════════════════════════════╣
║  Cores/Threads: 36C / 72T                                        ║
║  Base / Turbo:  2,200 MHz / 4,800 MHz                            ║
║  Cache:         L2: 72 MiB (2MB/core) | L3: 82.5 MiB            ║
║  TDP:           300W (MTP: 360W)                                 ║
║  Memory:        256GB DDR5-4800 ECC, 8 channels, 307 GB/s       ║
║  NUMA:          1 node (all local)                               ║
║  AMX:           INT8: 2,048 ops/cycle | BF16: 1,024 ops/cycle   ║
║  Socket:        LGA-4677                                         ║
╚══════════════════════════════════════════════════════════════════╝
```

### Current State — Problems Found

| Setting | Current | Optimal | Impact |
|---------|---------|---------|--------|
| CPU Governor | **powersave** | performance | Cores idle at 800 MHz instead of 4.8 GHz |
| HugePages | **0 configured** | 16GB of 1GB pages | 5-50% inference boost (like RandomX) |
| AMX utilization | Unknown | Verify ollama uses AMX | 8x throughput if INT8 via AMX vs AVX-512 |

### The RandomX Parallel

Both RandomX mining and AI inference are **memory-bandwidth bound on CPU**. Same tuning applies:

- **CPU Governor → performance** (mandatory, same as mining rigs)
- **Enable Huge Pages** (RandomX miners get 1-50% boost, AI inference similar)
- **All 8 DDR5 channels populated** (half the channels = half the bandwidth)
- **RAM speed matters** (DDR5-4800 = 307 GB/s ceiling, every MHz counts)
- **L3 cache is the fast lane** (82.5 MB = model weights stay hot)

### Immediate Tuning Commands

```bash
# 1. Switch governor to performance (instant, no risk)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# 2. Enable 1GB huge pages (AI inference + mining boost)
echo 16 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# 3. Verify DDR5 channel population (should be 8x 32GB)
sudo dmidecode -t memory | grep -E "Size:|Locator:|Speed:"

# 4. Check AMX usage
cat /proc/cpuinfo | grep amx

# 5. Monitor power
sudo turbostat --interval 1 --num_iterations 3 --show PkgWatt,CorWatt,Avg_MHz 2>/dev/null
```

### Expected Gains

| Tuning | Estimated Improvement | Risk |
|--------|----------------------|------|
| Governor → performance | +20-40% tok/s | None |
| Enable huge pages | +5-20% tok/s | None (reversible) |
| Verify AMX active | +100-700% if currently AVX-512 | None (diagnostic) |
| **Combined** | **+30-60% inference throughput** | **Zero risk** |

Current: ~200 tok/s on gemma3:4b. After tuning: potentially 300-400 tok/s. Same CPU, same power draw, just not running in powersave mode with zero huge pages.

## RTX 3090 / 3090 Ti — The Fleet Workhorses (100+ cards)

Former mining cards. We tuned these for ETH. Same knowledge, new workload.

```
╔══════════════════════════════════════════════════════════════════╗
║              RTX 3090                 RTX 3090 Ti                ║
╠══════════════════════════════════════════════════════════════════╣
║  GPU        GA102 (sm_86)           GA102 full (sm_86)          ║
║  Cores      10,496 CUDA             10,752 CUDA                 ║
║  Tensor     328 (3rd gen)           336 (3rd gen)               ║
║  VRAM       24GB GDDR6X 384-bit    24GB GDDR6X 384-bit         ║
║  Bandwidth  936 GB/s               1,008 GB/s (+7.7%)          ║
║  Base       1,395 MHz              1,560 MHz                    ║
║  Boost      1,695 MHz              1,860 MHz                    ║
║  TDP        350W                   450W                         ║
║  Power Min  ~100W                  ~100W                        ║
║  Mem Clock  9,751 MHz (19.5Gbps)   10,752 MHz (21 Gbps)        ║
║  PCIe       Gen 4 x16             Gen 4 x16                    ║
║  NVLink     Yes (2-way)           No                           ║
║  Price(used) $600-800              $800-1,000                   ║
╚══════════════════════════════════════════════════════════════════╝
```

### Mining DNA → AI Inference

| Setting | ETH Mining (proven) | AI Inference (7B) | AI Inference (12B) |
|---------|-------------------|-------------------|-------------------|
| Core | -400 MHz offset | Lock 1,200 MHz | Lock 1,400 MHz |
| Memory | +1,100 MHz | Auto (9,501 MHz) | Auto (9,501 MHz) |
| Power | 290W (77%) | 150W (43%) | 200W (57%) |
| Workload | Memory-bound (DAG) | Memory-bound (KV cache) | Memory-bound (weights) |
| Output | 121 MH/s | ~200 tok/s | ~80 tok/s |

### Fleet Economics (100 × RTX 3090)

| Metric | Value |
|--------|-------|
| Total VRAM | 2,400 GB (2.4 TB) |
| Total Power (max) | 35,000W |
| Total Power (tuned 150W each) | 15,000W |
| Cards per model | 1 card = 1× 7B quantized |
| Judge pairs | 50 parallel tribunals |
| Throughput | 50 × 380 = **19,000 pairs/hr** |
| **163-day wall** | **→ 3.3 days** |
| Monthly power cost (at $0.10/kWh) | $1,080 |

### 3090 Inference Flight Sheets

```
SCALE 12B (gemma3:12b):    Core 1,400 MHz | Mem auto | Power 200W | ~80 tok/s
SCALE 32B (qwen2.5:32b):  Core 1,400 MHz | Mem auto | Power 250W | ~50 tok/s
IDLE / STANDBY:            Core 210 MHz   | Mem auto | Power 100W
```

### Fleet Recommendation

Buy 3090s over 3090 Ti for fleet builds. The Ti's 7.7% bandwidth advantage doesn't justify the price premium or higher idle power. The 3090 at 150W is the sweet spot for inference fleet density.

### GDDR6X Thermal Note

3090's GDDR6X backside VRAM runs 90-110°C under sustained load. For fleet:
- Thermal pad replacement on VRAM (drops 10-20°C)
- Power limit 150W keeps VRAM < 95°C
- Monitor: `nvidia-smi -q -d TEMPERATURE`

---

## Rigel Mining Patterns Applied to AI

Borrowed from [rigelminer/rigel](https://github.com/rigelminer/rigel) — crypto mining solved GPU optimization before AI did.

| Rigel Feature | AI Equivalent | Implementation |
|--------------|---------------|----------------|
| `--lock-cclock/mclock` | Lock clocks for stability | `nvidia-smi -lgc 1000,1000 -lmc 14001` |
| `--dag-reset-mclock` | Reset mem OC before model load | Reset → load model → reapply OC |
| `--dual-mode a12:h92` | Tribunal + experiment on 1 GPU | Priority scheduling via ollama |
| `--temp-limit tc[60-70]` | Thermal hysteresis | Throttle at 85°C, resume at 78°C |
| `--kernel 2` (energy efficient) | Attention implementation | eager / flash_attn2 / SDPA |
| `--power-avg 10` | Smooth power readings | 10-second averaging window |
| `--pl` per device | Per-GPU power limits | `nvidia-smi -i N -pl X` |

### Autotune Protocol

```
1. Set power to 60% TDP, memory to max
2. Start core at 50% of max
3. Benchmark 5 min, record throughput
4. Increase core +100 MHz, repeat
5. Stop when throughput plateaus = memory-bound ceiling
6. Sweep power limits to find the knee
7. Lock final settings to flight sheet
```

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
