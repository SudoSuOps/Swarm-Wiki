# The Swarm Cookbook — 8 Verified Recipes

**Status**: LIVE at swarmandbee.ai/cookbook
**Source of truth**: This doc + the HTML page. Keep synced.

Every recipe is a flight sheet for a cook. Ingredients (weight by the pound), oven settings (GPU + power), bake time, verified result.

---

## Recipe 1: MASTER WRITER — Grant & Business Specialist

| Setting | Value |
|---------|-------|
| Base model | Gemma 4 31B-it |
| Weight | 35,957 lbs Class A GrantHash |
| Personas | 37 expert (grant writer, SBA specialist, 501(c)(3) attorney, pitch deck strategist) |
| Method | QLoRA r=64, alpha=32, 4-bit NF4 |
| Epochs | 3 |
| Learning rate | 1e-5 |
| Max length | 4096 tokens |
| GPU | RTX PRO 6000 Blackwell 96GB |
| Power | 300W cap (memory-bound, core throttles to ~1000 MHz) |
| Memory clock | MAX (14,001 MHz on Blackwell) — THIS is the hashrate |
| VRAM used | ~33 GB (4-bit quantized + gradients) |
| Bake time | 37 hours, 3,204 steps |
| Energy | $1.71 total ($0.10/kWh) |

**Verified result (April 5, 2026):**
- eval_loss: 0.7534 → 0.5158 (31.5% improvement)
- Convergence: step 2,880 (last 324 steps gained 0.0001)
- Output: wrote $4.2M DOE GRIP grant application, CRE net lease business plan, its own OM case study
- Live: swarmandbee.ai/writer

---

## Recipe 2: OWN YOUR AGENT — Sovereign, Secure, No API Dependency

**EMERGENCY — Anthropic cut off OpenClaw April 4, 2026**

The problem: Claude subscription went from $20/month → $2,250/month (112x). Plus 9 CVEs, 135K exposed instances, $45M stolen.

| Setting | Value |
|---------|-------|
| Base model | Qwen 3.5 27B (best agent reasoning, native tool calling) |
| Weight | 5,000 lbs Class A ClawHash ($9.99/lb) |
| Sub-algorithms | Injection defense, tool poison detection, RCE prevention, sandbox patterns, audit logging |
| Method | QLoRA r=64, 3 epochs, lr=5e-6 |
| GPU | RTX PRO 4500 Blackwell 32GB ($2,750) |
| Power | 150W (efficiency mode) |
| Bake time | ~12 hours to cook, runs forever after |
| Inference cost | ~$2/day. That's it. Forever. |

**The math:**
- Claude API: $2,250/month ongoing, dependent on Anthropic
- Own Your Agent: $49,950 (weight) + $2,750 (GPU) = $52,700 one-time
- Break-even: 23 days
- Year 2+: $27,000/year saved

---

## Recipe 3: AGENT RELIABILITY — Fix Your AI Agent

**2026 market signal — highest demand**

Pick your ingredient based on what's broken:

| Sub-algorithm | Fixes |
|--------------|-------|
| AgentHash-ToolUse | Wrong API, wrong params, misreads response |
| AgentHash-Structure | JSON breaks, schema violations, format drift |
| SecurityHash | Prompt injection, data leaks, auth bypass |
| AgentHash-MultiStep | Reasoning falls apart at step 4+ |
| AgentHash-Recovery | One error kills the chain |
| AgentHash-Eval | Can't tell if it worked |

| Setting | Value |
|---------|-------|
| Base model | Qwen 3.5 27B or Gemma 4 31B |
| Weight | 5,000 lbs Class A AgentHash ($5.99/lb) |
| Method | QLoRA r=64, 3 epochs, lr=5e-6 |
| Bake time | ~12 hours (complex multi-turn format) |
| Total cost | $29,950 ingredients + $0.50 energy |

---

## Recipe 4: MEDICAL SPECIALIST — Clinical Domain Expert

| Setting | Value |
|---------|-------|
| Base model | Gemma 4 31B-it or Qwen 3.5 27B |
| Weight | 5,000 lbs Class A MedHash ($4.99/lb) |
| Specialties | Drug interactions, dosing, reconciliation, surgical eval, clinical guidance |
| Method | QLoRA r=64, 3 epochs, lr=1e-5 |
| GPU | RTX 6000 96GB (bf16) or RTX 4500 32GB (Q4) |
| Power | 250-300W |
| Bake time | ~10 hours |
| Energy | ~$0.50 |

**Expected:** +20% medical expertise relocation. Board-certified-level clinical responses.

Shelf life warning: medical regulations change. Buy 5,000 lbs now, micro-cook 750 lbs weekly virgin jelly to stay current.

---

## Recipe 5: CRE DEAL ANALYST — Commercial Real Estate Underwriting

| Setting | Value |
|---------|-------|
| Base model | Gemma 4 31B-it |
| Weight | 5,000 lbs Class A CREHash ($9.99/lb) |
| Specialties | NOI, cap rates, DSCR, debt coverage, pro forma, tenant analysis |
| Method | QLoRA r=64, 3 epochs, lr=1e-5 |
| Bake time | ~10 hours |

---

## Recipe 6: LEGAL COMPLIANCE — Credit Repair & Regulatory Expert

| Setting | Value |
|---------|-------|
| Base model | Qwen 3.5 27B or Gemma 4 31B |
| Weight | 5,000 lbs Class A LegalHash ($0.99/lb) |
| Specialties | FCRA, FDCPA, consumer protection, dispute methodology, regulatory citations |
| Method | QLoRA r=64, 3 epochs, lr=1e-5 |

Note: dispute_letters domain is OFF LIMITS (standing rule). Legal compliance training only.

---

## Recipe 7: WEEKLY MICRO-COOK — Keep Your Model Fresh

Virgin jelly — yesterday's data is the brothel.

| Setting | Value |
|---------|-------|
| Frequency | Weekly |
| Weight | 750 lbs fresh Class A per week |
| Source | Live signal (HN, X, industry feeds, new regulations) |
| Method | LoRA merge on existing base (not full retrain) |
| Bake time | ~2 hours per micro-cook |
| Pricing | FUTURES: 20% discount on weekly subscription |

The lifecycle: Conversation → Idea → Signal → Virgin Jelly → Weighed → Cooked → Deployed → Conversation.

---

## Recipe 8: BOARD MEMBER — Strategic Advisor (Internal)

| Setting | Value |
|---------|-------|
| Base model | Qwen 3.5 27B |
| Weight | 500 lbs WikiHash (internal, not priced) |
| Source | Glass-wall doctrine, wiki sections, company identity |
| Method | QLoRA r=64, 3 epochs |
| Purpose | Board-level strategic advice trained on Swarm & Bee doctrine |

Internal recipe — not for sale. The model that knows the company.

---

## Standing Rules for All Cooks

1. **Cook clean** — shut everything else down during a cook. No compromised infills.
2. **Don't overbake** — check the toothpick (eval_loss). When delta < 0.001, stop.
3. **Don't overbuy** — models absorb ~5,000 lbs per cook. Buy, cook, measure, come back.
4. **Permit before build** — no cook without a reviewed flight sheet.
5. **Efficiency is king** — memory clock MAX, core clock let it throttle. Watts per deed.
6. **Never cook dispute_letters** — standing rule, no exceptions.

---

*Intelligence by the pound. Buy the ingredients. Follow the recipe. Serve on your own hardware.*
