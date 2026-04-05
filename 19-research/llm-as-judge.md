# LLM-as-Judge & Dual-Judge Systems

These papers directly validate and inform our dual-judge tribunal architecture where two independent base models (gemma3:12b + qwen2.5:7b) score AI training pairs.

## TIER 1 — Directly Applicable to Tribunal

### 1. ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate
- **Authors**: Chi-Min Chan, Weize Chen, Yusheng Su, Jianxuan Yu, Wei Xue, et al.
- **Date**: 2023-08-14
- **Link**: https://arxiv.org/abs/2308.07201
- **Why it matters**: Closest match to our system. Uses multiple LLM agents in a debate framework to improve evaluation quality — directly parallel to our dual-judge tribunal where gemma3:12b and qwen2.5:7b independently score and their agreement determines finality.
- **Swarm application**: Validates dual-judge architecture. Could inform a "debate pass" when judges disagree beyond drift threshold.

### 2. LM vs LM: Detecting Factual Errors via Cross Examination
- **Authors**: Roi Cohen, May Hamri, Mor Geva, A. Globerson
- **Date**: 2023-05-22
- **Link**: https://arxiv.org/abs/2305.13281
- **Why it matters**: One LLM cross-examines another to detect factual errors. This is the adversarial version of our dual-judge model — two models checking each other's work to surface quality issues.
- **Swarm application**: Could add a cross-examination pass for flagged pairs (high disagreement).

### 3. Examining the Inter-Consistency of Large Language Models: An In-depth Analysis via Debate
- **Authors**: Kai Xiong, Xiao Ding, Yixin Cao, Ting Liu, Bing Qin
- **Date**: 2023-05-19
- **Link**: https://arxiv.org/abs/2305.11595
- **Why it matters**: Studies inter-model agreement/disagreement — the exact metric our tribunal uses when gemma3 and qwen2.5 score the same pair. Directly informs how to interpret judge concordance.
- **Swarm application**: Research backing for our drift threshold (0.15). May suggest better agreement metrics.

### 4. Shepherd: A Critic for Language Model Generation
- **Authors**: Tianlu Wang, Ping Yu, Xiaoqing Tan, Sean O'Brien, Ramakanth Pasunuru, et al.
- **Date**: 2023-08-08
- **Link**: https://arxiv.org/abs/2308.04592
- **Why it matters**: A dedicated critic model that evaluates LLM outputs with structured feedback. Validates the architecture of using separate models as quality judges rather than self-evaluation.
- **Swarm application**: Our judges ARE critic models. This paper validates the design of separating generation from evaluation.

### 5. GPTEval: NLG Evaluation using GPT-4 with Better Human Alignment
- **Authors**: Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, et al.
- **Date**: 2023-03-29
- **Link**: https://arxiv.org/abs/2303.16634
- **Why it matters**: Establishes methodology for LLM-as-judge evaluation with chain-of-thought scoring and human alignment metrics. Provides the evaluation framework our scoring prompt design builds on.
- **Swarm application**: Direct precedent for our scoring prompt structure (score + reasoning).

### 6. Evaluating LLMs at Detecting Errors in LLM Responses
- **Authors**: Ryo Kamoi, Sarkar Snigdha Sarathi Das, Renze Lou, et al.
- **Date**: 2024-04-04
- **Link**: https://arxiv.org/abs/2404.03602
- **Why it matters**: Directly measures how well LLMs can detect errors in other LLMs' outputs — the core capability our judges need. Shows where LLM judges succeed and fail.
- **Swarm application**: Identifies blind spots in LLM judges. Informs which domains may need human spot-checks.

### 7. Training Verifiers to Solve Math Word Problems (OpenAI)
- **Authors**: Karl Cobbe, V. Kosaraju, Mohammad Bavarian, Jacob Hilton, Reiichiro Nakano, et al.
- **Date**: 2021-10-27
- **Link**: https://arxiv.org/abs/2110.14168
- **Why it matters**: The foundational paper on training separate verifier models to judge solution quality. OpenAI's original work that proved dedicated verifiers outperform generators at quality assessment — the thesis behind our entire tribunal.
- **Swarm application**: Academic foundation for "the validator is separate from the generator."

### 8. AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback
- **Authors**: Yann Dubois, Xuechen Li, Rohan Taori, Tianyi Zhang, Ishaan Gulrajani, et al.
- **Date**: 2023-05-22
- **Link**: https://arxiv.org/abs/2305.14387
- **Why it matters**: Simulates human feedback with LLM judges for RLHF training. Directly relevant to using LLM judges as proxies for human quality assessment in training data scoring.
- **Swarm application**: Validates using base model judges as proxy for human quality assessment.

### 9. FActScore: Fine-grained Atomic Evaluation of Factual Precision
- **Authors**: Sewon Min, Kalpesh Krishna, Xinxi Lyu, M. Lewis, Wen-tau Yih, et al.
- **Date**: 2023-05-23
- **Link**: https://arxiv.org/abs/2305.14251
- **Why it matters**: Decomposes text into atomic claims and scores each one — a granular scoring methodology our tribunal could adopt for more defensible deed-level quality scores.
- **Swarm application**: Future enhancement: atomic-level scoring per deed for more granular quality proofs.

### 10. Self-Consistency for Open-Ended Generations
- **Authors**: Siddhartha Jain, Xiaofei Ma, Anoop Deoras, Bing Xiang
- **Date**: 2023-07-11
- **Link**: https://arxiv.org/abs/2307.06857
- **Why it matters**: Extends self-consistency to open-ended generation by measuring agreement across multiple samples. Directly applicable to understanding when our two judges should converge vs. diverge.
- **Swarm application**: Informs our 2-pass validation logic and when to trust/reject dual-judge scores.

---

## Key Takeaways for Swarm

1. **Our dual-judge architecture is academically validated** — ChatEval, LM-vs-LM, and Inter-Consistency all study the same pattern we implemented.
2. **Separate verifiers > self-evaluation** — The Shepherd and OpenAI Verifier papers prove that dedicated critic models outperform self-evaluation. Our tribunal uses base models as judges, not the generator judging itself.
3. **Drift threshold has research backing** — Inter-Consistency studies show that inter-model agreement is a reliable quality signal. Our 0.15 drift threshold is a reasonable boundary.
4. **Atomic scoring is the next level** — FActScore's approach of decomposing into atomic claims could make our deeds even more defensible.
5. **Constitutional approach works** — Our `scoring_prompt.py` is essentially a constitution (Anthropic's Constitutional AI). The scoring dimensions (accuracy, completeness, clarity, relevance, domain expertise) serve as principles that guide judge behavior.

---

*Source: [EgoAlpha/prompt-in-context-learning](https://github.com/EgoAlpha/prompt-in-context-learning) — EvaluationReliabilityList.md, AgentList.md*
