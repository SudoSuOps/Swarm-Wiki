# Qwen 3.5 9B — Why It's the Perfect Micro-Domain Base

**Status**: SELECTED — base model for all tenant-specific specialist cooks
**Date**: 2026-04-07

## The Assessment

Qwen 3.5 9B is specifically built for micro-domain specialists. Not by accident — by architecture.

## 1. Gated Delta Networks (GDN) — Pattern Storage

75% of layers use GDN (linear attention, O(n) complexity). 25% use standard attention (every 4th layer).

A DG specialist sees the same lease structures, same cap rate patterns, same NNN terms over and over. GDN encodes these PATTERNS cheaply and retrieves them fast. Standard attention handles the REASONING — "should I price at 7.00 or 7.25?"

Pattern storage (GDN) + reasoning (attention) = specialist.

## 2. 9B Parameter Count — The Sweet Spot

```
Too small (2-4B):  can't hold enough domain knowledge
Too large (27-35B): expensive to cook, expensive to serve,
                     OVERTHINKS (Finding: 27B scored 0% honey)
9B:                enough capacity for one deep domain
                   serves on RTX 4500 32GB (23.5GB bf16)
                   fast enough for real-time queries (165 tok/s)
                   cheap enough to cook ($0.50 energy)

The DG King didn't need to know everything.
He needed to know ONE THING deeply.
9B is enough for one thing. 27B is overkill.
```

## 3. Native Tool Calling

Qwen 3.5 was trained with structured output capability. Agent-DG needs to:

- Generate JSON for BOV calculations
- Call PostGrid API for letters
- Query the DG graph for comps
- Output formatted OM templates

Tool calling is BUILT IN — not bolted on. The model can DO things, not just ANSWER things.

## 4. Think Mode Control

```
enable_thinking=True   → complex analysis (IC memo, deal structure)
enable_thinking=False  → fast operations (comp lookup, letter gen)

/no_think prefix in ollama disables reasoning blocks.
3-5x faster for simple tasks.

"What's the cap rate for a 10yr FL DG?"
→ no_think → instant answer → 0.3 seconds

"Should my 1031 client buy this DG or wait?"
→ think → chain of reasoning → 3 seconds → better answer
```

## 5. Context Window

262,144 tokens native. 1M via YaRN extension.

```
A full DG lease:              ~5,000 tokens
A comp deck with 5 trades:    ~3,000 tokens
An owner profile + entities:  ~2,000 tokens
A full deal package:          ~15,000 tokens

262K context = the model holds the ENTIRE deal in memory
while reasoning. No chunking. No retrieval needed.
Lease + comps + owner + entity chain — in one pass.
```

## 6. Vocabulary Size (248,320 tokens)

Massive vocab means CRE terms tokenize efficiently:

```
"triple-net"    = 1-2 tokens (not 4-5 in smaller vocab)
"cap rate"      = 1 token
"1031 exchange" = 2 tokens
"NOI"           = 1 token

Efficient tokenization = more content per context window.
More content = better reasoning on complex deals.
```

## 7. LoRA Receptivity

Qwen 3.5 was designed for fine-tuning:

```
TRAINING CONFIG:
  Precision:         bf16 LoRA only (no QLoRA — quant differences too high)
  Rank:              r=64 (captures domain patterns without overfitting)
  Epoch cap:         0.6 (prevents memorization)
  Packing:           True (6x speedup)
  AutoTokenizer:     bypass required for Qwen3.5 (known issue)
  Framework:         Unsloth FastLanguageModel + TRL SFTTrainer

COOK MATH:
  5,000 DG pairs × 3 epochs × 0.6 cap = 9,000 effective steps
  At ~45 pairs/step with packing = ~200 steps
  At 165 tok/s = ~10 hours on RTX PRO 6000
  Energy: $0.50 in electricity
  
  The model absorbs the DG wiki in one overnight cook.
```

## The Bottom Line

```
WHY QWEN 3.5 9B FOR EVERY MICRO-DOMAIN COOK:

  ✓ GDN for pattern storage (leases, cap rates, terms, comps)
  ✓ Attention for reasoning (deal analysis, pricing, strategy)
  ✓ 9B = one deep domain, not too big to overthink
  ✓ 23.5GB bf16 = serves on $2,750 RTX 4500 (broker's GPU)
  ✓ 165 tok/s = real-time answers on the phone with an owner
  ✓ Native tool calling = Agent-DG can act, not just answer
  ✓ Think mode toggle = fast for lookups, deep for analysis
  ✓ 262K context = entire deal in one pass
  ✓ LoRA receptive = $0.50 cook, 10 hours, proven patterns
  ✓ NOT 27B = no overthinking, no 0% honey, no wasted watts
```

## 9B vs 27B — The Finding Still Holds

```
27B (Haymitch):
  The consultant. Call for hard problems.
  60-96 seconds per verdict. Overthinks.
  0% honey in mining. 6.4x slower judging.
  $5 per complex query. Offline batch only.

9B (the DG King):
  The specialist. Grinds 200 dials a day.
  5-10 seconds per response. Decisive.
  24% honey rate. 165 tok/s throughput.
  $0.50 to cook. Runs on a $2,750 card.

Right-size the model. Right-size the silicon.
9B for the specialist. 27B for the strategist.
That was the Finding. That's still the rule.
```

---

*The DG King was a 9B. Decisive. Fast. Deep on one thing. That's the model for every micro-domain specialist cook.*
