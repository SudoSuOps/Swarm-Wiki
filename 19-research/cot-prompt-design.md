# Chain-of-Thought & Prompt Design — Scoring Prompt Optimization

Papers covering CoT reasoning, automatic prompt optimization, and structured output design. These directly inform improving our `scoring_prompt.py` and tribunal methodology.

## TOP 15 — Ranked by Relevance to Tribunal Scoring

### 1. Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **Date**: 2022-03-21 | **Link**: https://arxiv.org/abs/2203.11171
- **Why**: Foundational self-consistency paper — sample multiple reasoning paths, take majority. Validates our two-judge architecture and suggests sampling N>2 chains per judge for even stronger agreement signals.
- **Action**: Consider sampling 3 CoT chains per judge, majority vote on the score.

### 2. Chain of Thought Prompting Elicits Reasoning in Large Language Models
- **Date**: 2022-01-28 | **Link**: https://arxiv.org/abs/2201.11903
- **Why**: The foundational CoT paper. Our scoring prompt already asks judges for reasoning before numeric score — this paper established why that works. CoT dramatically improves multi-step reasoning (like evaluating 5 quality dimensions).
- **Action**: Our scoring prompt already follows this pattern. Validates current design.

### 3. Large Language Models Are Human-Level Prompt Engineers (APE)
- **Date**: 2022-11-03 | **Link**: https://arxiv.org/abs/2211.01910 | **GitHub**: keirp/automatic_prompt_engineer
- **Why**: Automatic Prompt Engineer — generates candidate prompts, evaluates them, iteratively improves. Could auto-tune our 5-dimension scoring prompt against a calibration set of human-labeled ground truth.
- **Action**: After cook finishes, use APE to optimize scoring_prompt.py. Generate variants, score calibration set, select prompt that maximizes inter-judge agreement.

### 4. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Date**: 2023-06-09 | **Link**: https://arxiv.org/abs/2306.05685
- **Why**: DIRECTLY studies LLMs-as-judges. Analyzes position bias, verbosity bias, self-enhancement bias, and limited reasoning in LLM judges. Critical for understanding failure modes in our tribunal.
- **Action**: MUST READ. Test for position bias by swapping Q&A order between Judge A and Judge B. Check if our scores correlate with response length (verbosity bias).

### 5. Chain-of-Verification Reduces Hallucination in Large Language Models (CoVe)
- **Date**: 2023-09-20 | **Link**: https://arxiv.org/abs/2309.11495
- **Why**: After initial response, model plans verification questions, answers independently, revises. Directly applicable to our 2-pass validation — first pass scores, second pass verifies with explicit questions per dimension.
- **Action**: Structure 2nd pass as verification questions: "Does the score for accuracy match the reasoning?" per dimension.

### 6. Self-Refine: Iterative Refinement with Self-Feedback
- **Date**: 2023-03-30 | **Link**: https://arxiv.org/abs/2303.17651
- **Why**: Iterative self-refinement where LLM generates, critiques, refines. Shows when self-refinement helps (structured tasks with clear criteria — like rubric scoring) and when it fails.
- **Action**: Our 2-pass is effective. A 3rd pass may add noise more than signal for structured scoring.

### 7. Automatic Prompt Augmentation and Selection with Chain-of-Thought from Labeled Data
- **Date**: 2023-02-24 | **Link**: https://arxiv.org/abs/2302.12822 | **GitHub**: shizhediao/automate-cot
- **Why**: Automates CoT prompt construction from labeled data. Given thousands of scored Royal Jelly pairs with ground truth, this can automatically generate optimal CoT exemplars for our scoring prompt.
- **Action**: Use our 10K+ scored deeds as labeled data to auto-generate few-shot exemplars for the scoring prompt.

### 8. ChatEval: Multi-Agent Debate for Evaluation
- **Date**: 2023-08-14 | **Link**: https://arxiv.org/abs/2308.07201
- **Why**: Multi-agent debate for evaluation. Shows structured disagreement resolution produces more reliable evaluations than simple averaging.
- **Action**: When judges diverge > 0.15 drift, implement a debate round rather than averaging or flagging.

### 9. Shepherd: A Critic for Language Model Generation
- **Date**: 2023-08-08 | **Link**: https://arxiv.org/abs/2308.04592 | **GitHub**: facebookresearch/shepherd
- **Why**: Dedicated critic model with multi-dimensional feedback. Approach to structured, dimension-wise critique aligns with our 5-dimension rubric.
- **Action**: Our fine-tuned Gemma 4 31B could become a dedicated scoring model (Judge C) rather than relying on general-purpose base models.

### 10. REFINER: Reasoning Feedback on Intermediate Representations
- **Date**: 2023-04-04 | **Link**: https://arxiv.org/abs/2304.01904 | **GitHub**: debjitpaul/refiner
- **Why**: Separate critic provides structured feedback on intermediate reasoning steps. The critic identifies WHY a score is wrong.
- **Action**: Could add to tribunal: when judges disagree, a refiner explains the disagreement source.

### 11. Revisiting OPRO: The Limitations of Small-Scale LLMs as Optimizers
- **Date**: 2024-05-16 | **Link**: https://arxiv.org/abs/2405.10276
- **Why**: When LLM-based prompt optimization works and fails for SMALLER models. Since our judges are 12b and 7b, this paper's findings on optimization limitations at that scale are directly relevant.
- **Action**: APE-style optimization may need a larger model (31B after cook) to optimize prompts for the smaller judges.

### 12. CoT for Evaluating Students' Formative Assessment Responses in Science
- **Date**: 2024-03-21 | **Link**: arxiv.org (education domain)
- **Why**: CoT prompting for rubric-based scoring of student responses — structurally identical to our domain-pair scoring. Shows how to decompose evaluation into dimension-specific CoT chains.
- **Action**: Consider explicit per-dimension CoT rather than holistic scoring.

### 13. Automatic Chain of Thought Prompting in Large Language Models (Auto-CoT)
- **Date**: 2022-10-07 | **Link**: https://arxiv.org/abs/2210.03493 | **GitHub**: amazon-science/auto-cot
- **Why**: Automates the creation of CoT demonstrations by clustering questions and sampling diverse examples. Removes manual effort from CoT prompt design.
- **Action**: Use Auto-CoT to generate diverse scoring exemplars across domains automatically.

### 14. Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- **Date**: 2023-05-17 | **Link**: https://arxiv.org/abs/2305.10601 | **GitHub**: princeton-nlp/tree-of-thought-llm
- **Why**: Extends CoT to explore multiple reasoning branches. For complex scoring decisions (borderline pairs at 0.74-0.76), exploring multiple reasoning trees before committing to a score could improve classification accuracy.
- **Action**: For borderline tier decisions, ToT could replace simple 2-pass validation.

### 15. Complexity-Based Prompting for Multi-Step Reasoning
- **Date**: 2022-10-05 | **Link**: https://arxiv.org/abs/2210.00720
- **Why**: Shows that more complex reasoning chains (more steps) improve performance on harder tasks. Suggests our scoring prompt should encourage longer reasoning for difficult domain pairs.
- **Action**: Add to scoring prompt: "For complex domain pairs, reason through each dimension step by step before scoring."

---

## Key Takeaways for Swarm

1. **Our scoring prompt design is sound** — CoT reasoning before numeric output is the validated pattern (papers 1, 2). Our existing design follows this.
2. **Automatic optimization is the next level** — APE (paper 3) and Auto-CoT (paper 13) can auto-tune our scoring prompt using our 10K+ labeled deeds as ground truth. This is a high-ROI project.
3. **Position bias is a real risk** — MT-Bench paper (4) shows LLM judges exhibit position bias. We should test if swapping Q&A order between judges changes scores.
4. **Debate > averaging for disagreements** — ChatEval (8) shows multi-agent debate resolves disagreements better than averaging. When drift > 0.15, a debate pass could be more effective than flagging.
5. **Per-dimension CoT is stronger** — Papers 12, 15 suggest scoring each dimension with its own reasoning chain rather than holistic evaluation. Could improve granularity.

---

## Priority Action Items

| # | Action | Paper | Effort | Impact |
|---|--------|-------|--------|--------|
| 1 | Test position bias (swap Q&A order) | MT-Bench (#4) | Low | High |
| 2 | Auto-generate scoring exemplars from deeds | Auto-CoT (#7, #13) | Medium | High |
| 3 | APE-optimize scoring_prompt.py | APE (#3) | Medium | High |
| 4 | Debate pass for high-drift pairs | ChatEval (#8) | Medium | Medium |
| 5 | Per-dimension CoT scoring | #12, #15 | Low | Medium |

---

*Source: [EgoAlpha/prompt-in-context-learning](https://github.com/EgoAlpha/prompt-in-context-learning) — ChainofThoughtList.md, PromptDesignList.md, AutomaticPromptList.md, InContextLearningList.md*
