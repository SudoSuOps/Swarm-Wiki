# Factory Protocol Audit (22 Integrated Audits)

The factory protocol (`data/factory_protocol.py`, 1,884 lines) integrates 22 industrial audits into a 10-stage production pipeline.

## 10-Stage Pipeline

```
1. SOURCES    -> Raw data (public records, EDGAR, RSS)
2. GENERATE   -> Deterministic (CRE) or LLM-based (Medical/Pharma/Aviation)
3. GATE       -> 6 deterministic quality gates
4. VERIFY     -> CoVe 2-stage (rewrite + 235B verify)
5. DEDUP      -> MD5 fingerprint (per-run + global)
6. SHARD      -> R2 shards (500 pairs each, SHA256 manifest)
7. STORE      -> SafeStore 3-tier (local JSONL + R2 + Supabase)
8. ASSEMBLE   -> Multi-phase blend (difficulty balance, pool weighting)
9. TRAIN      -> Unsloth bf16 LoRA (packing=True, 0.6 epoch)
10. DEPLOY    -> Merge -> vLLM serve (or GGUF quantize)
```

## Production Yields

| Domain | Pairs | Yield | Method |
|--------|-------|-------|--------|
| CRE | 643,382 | 99.2% | Deterministic generation |
| Medical | 432,196 | 77.9% | CoVe verification |
| Aviation | 45,222 | 76.1% | CoVe verification |
| Pharma | 28,624 | ~80% | Trajectory + CoVe |
| Drone | 6,755 | ~75% | CoVe verification |
| **Total** | **1,158,902** | -- | -- |

Total API spend: ~$510

## 22 Integrated Audits

| # | Audit | Key Finding |
|---|-------|-------------|
| 1 | Factory Pipeline | 10-stage, 73-93% yield by domain |
| 2 | Production Yields | 1.16M pairs, $510 total spend |
| 3 | Known Failure Modes | 8 patterns (template memorization, eval overhead, think mode) |
| 4 | Frontier Model Weaknesses | 5 models audited for systematic failures |
| 5 | Claude Code Mistakes | 7 failures documented (packing, AutoTokenizer, QLoRA) |
| 6 | Swarm & Bee Mistakes | 8 strategic errors (CRE v1, judge overkill, 2-prompt training) |
| 7 | Human Trial & Error | Founder arc: M&M → AI → first model → scaling |
| 8 | HuggingFace Slop | Audit of low-quality datasets on HF |
| 9 | Clawbot Ecosystem | 52% of web is AI-generated content |
| 10 | Reverse Engineering | Distillation as competitive weapon |
| 11 | DeepSeek | 14.8T tokens, GRPO algorithm analysis |
| 12 | Common Sense | All LLMs fail basic reasoning tests |
| 13 | Winning Systems | NeMo, FineWeb, LIMA, Phi analysis |
| 14 | Red Teaming | 7-layer quality defense stack |
| 15 | Indie Dev Playbook | Solo/small team AI development patterns |
| 16 | GitHub / Open Source | Open source strategy audit |
| 17 | Linux Cluster | Security audit (4/10 — needs improvement) |
| 18 | Data Sovereignty Economics | $15.8K CapEx, 112-day breakeven vs cloud |
| 19 | Unsloth AI | 2x training speed, memory optimization |
| 20 | Qwen Family | 36T tokens, Apache 2.0, GDN architecture |
| 21 | Quantum Computing | Zero ML relevance for 15+ years |
| 22 | Inference Engineering | RTX PRO 6000 1.63x faster than H100 |

## 6 Deterministic Quality Gates

From `factory/gates.py`:

| Gate | Check |
|------|-------|
| 1. JSON validity | Instant parse check |
| 2. Output length | JSON >= 20 chars, text >= 50 chars |
| 3. Numeric verification | Gold targets within tolerance ($1, +/-0.01%) |
| 4. Concept presence | Minimum 2 domain terms |
| 5. Deduplication | MD5 fingerprint |
| 6. Degenerate detection | Repetition pattern `(.{40,})\1{2,}` |

## CoVe 2-Stage Promotion

| Stage | Model | Purpose |
|-------|-------|---------|
| 1 | Llama-3.3-70B-Turbo | Rewrite (improve quality) |
| 2 | Qwen3-235B | Verify (5-criterion scoring) |

**Pass threshold**: total >= 20/25, all criteria >= 3, accuracy >= 4

**Criteria**: accuracy, completeness, structure, relevance, sft_quality

## 8 Known Failure Modes

1. Template memorization (CRE v1: 78K pairs, 2 system prompts)
2. Eval overhead (3,291 samples without packing = 13h eval)
3. Think mode in training (adds `<think>` token, must disable)
4. QLoRA on Qwen3.5 (does not work, use bf16 LoRA)
5. Batch padding waste (variable-length prompts create massive left-pad)
6. Greedy decoding (do_sample=False breaks Qwen3.5 thinking)
7. AutoTokenizer VL dispatch bug (loads vision tokenizer for text)
8. Single judge (no ensembling, systematic bias risk)

## SafeStore 3-Tier Architecture

| Tier | Storage | Recovery |
|------|---------|----------|
| 1 | Local JSONL | Instant |
| 2 | R2 shards (500 pairs each) | Minutes |
| 3 | Supabase (cooked_pairs table) | Database query |

**Guarantee**: Never lose a pair. Every pair exists in at least 2 tiers before pipeline advances.

## Generated Reports

| Output | Format | Location |
|--------|--------|----------|
| Industrial Audit Report | .docx | `swarmrouter/data/audit_output/Industrial_Audit_Report.docx` |
| Industrial Audit Economics | .xlsx | `swarmrouter/data/audit_output/Industrial_Audit_Economics.xlsx` |
| Excel sheets | 7 | Audit Summary, Economics, R2 Inventory, Inference Costs, Compute Ladder, Models, Linux Scorecard |
