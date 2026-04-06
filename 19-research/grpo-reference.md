# GRPO Reference — Group Relative Policy Optimization

**Source**: Grok technical deep-dive on DeepSeek GRPO + OpenClaw-RL adaptation
**Status**: REFERENCE — Year 3 implementation
**Paper**: DeepSeekMath 2024

## One-Paragraph Summary

GRPO is a critic-free variant of PPO for LLM post-training. Instead of training a separate value model (expensive, unstable at LLM scale), it samples a group of responses per prompt and uses intra-group relative rewards as the baseline. 30-50% lower memory, simpler training, better stability on binary rewards. OpenClaw-RL adapts it to online Binary RL where every live conversation turn becomes a training signal via PRM (Process Reward Model) scoring.

## Key Insight for Swarm & Bee

```
STANDARD GRPO:  Sample G responses → score all → relative advantage
OPENCLAW-RL:    Live conversation → PRM scores each turn → binary reward
                +1 (good), -1 (bad), 0 (neutral)
                No group sampling needed — every real turn = data

OUR TRIBUNAL:   Live conversation → dual-scale weighs each turn → 5-dim weight
                More granular than binary (+1/-1)
                More rigorous than single PRM (two independent scales)
                Provenance chain (Merkle → Hedera)
```

The tribunal is a BETTER PRM. Five dimensions > binary. Two scales > one judge. Provenance > trust-me.

## OpenClaw-RL GRPO Hyperparameters

```
eps_clip:       0.2
eps_clip_high:  0.28 (asymmetric — encourages exploration)
kl_loss_coef:   0.02
entropy_coef:   0 (disabled)
normalize_advantages: False (binary rewards, no normalization)
last_turn_mask: True (no next-state feedback for final turn)
```

Asymmetric clipping (0.2 / 0.28) is critical for agent tasks — allows more exploration than standard PPO. Fixes hallucinated success and loops by giving the model room to try different approaches.

## How GRPO Fixes Each Failure

| Failure | Signal | Reward |
|---------|--------|--------|
| Tool-call failure | PRM: "said done but tool returned error" | -1 |
| Loops | PRM: "user re-prompted after 'checking'" | -1 |
| Hallucinated success | PRM: "claimed complete, next-state shows incomplete" | -1 |
| Bad recovery | PRM: "user corrected after wrong retry" | -1 |
| Lost state | PRM: "asked same question that was already answered" | -1 |
| Correct tool call | PRM: "tool executed, result used correctly" | +1 |
| Clean recovery | PRM: "different approach after failure" | +1 |
| Honest escalation | PRM: "said 'I'm stuck' when actually stuck" | +1 |

## When We Build This

```
NOT NOW.

SEQUENCE:
  1. ✅ ClawHash calibration (100 pairs — cooking now)
  2.    AgentHash first experiment (6 buckets × 100 tasks)
  3.    Weight Shop sales (prove market)
  4.    Enterprise cook service (prove delivery)
  5. →  GRPO integration (tribunal as PRM, continuous RL)

Prerequisites:
  - Tribunal API exposed publicly
  - At least 48x GPU fleet for parallel rollout + training
  - 3+ enterprise clients generating live conversation data
  - Proven before/after metrics from SFT (Tier 1+2)

Don't build the RL loop before proving the weight sells.
Don't build the reward model before proving the tribunal works on ClawHash.
```

## Slime GRPO Launch Flags (for future reference)

```bash
--advantage-estimator grpo
--n-samples-per-prompt 4
--normalize-advantages        # or disable for binary RL
--eps-clip 0.2
--use-kl-loss --kl-loss-coef 0.02
--entropy-coef 0
```

---

*GRPO is the math. The tribunal is the signal. The deed is the receipt.*
*Year 3: every conversation makes the agent smarter, provably.*
