# Reliability & Calibration — Making LLM Scores Defensible

Papers addressing the fundamental question: can LLM scores be trusted? These inform how to make our Royal Jelly threshold boundaries (0.75 / 0.50) and drift threshold (0.15) scientifically defensible.

## TIER 3 — Reliability Infrastructure

### 17. Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores
- **Authors**: Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, et al.
- **Date**: 2023-05-24
- **Link**: https://arxiv.org/abs/2305.14975
- **Why it matters**: Methods for getting calibrated confidence scores from LLMs. Directly applicable to making our judges output reliable numerical quality scores rather than arbitrary numbers.
- **Swarm application**: Can we calibrate gemma3:12b and qwen2.5:7b so their 0.85 actually means the same thing? This paper shows how.

### 18. Prompting GPT-3 To Be Reliable
- **Authors**: Chenglei Si, Zhe Gan, Zhengyuan Yang, et al.
- **Date**: 2022-10-17
- **Link**: https://arxiv.org/abs/2210.09150
- **Why it matters**: Systematically studies LLM reliability across multiple dimensions including consistency, calibration, and faithfulness. Provides the reliability framework our tribunal scoring needs to be defensible.
- **Swarm application**: Reliability dimensions map directly to our 5 proofs: consistency = judge agreement, calibration = score distribution, faithfulness = reasoning quality.

### 19. Constitutional AI: Harmlessness from AI Feedback
- **Authors**: Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, et al.
- **Date**: 2022-12-15
- **Link**: https://arxiv.org/abs/2212.08073
- **Why it matters**: AI models evaluating AI outputs using principles/constitutions. Our `scoring_prompt.py` is essentially a constitution that guides judge behavior — this paper validates that approach.
- **Swarm application**: Our scoring prompt IS a constitution. The 5 scoring dimensions (accuracy, completeness, clarity, relevance, domain expertise) are constitutional principles.

### 20. Solving Math Word Problems with Process- and Outcome-Based Feedback
- **Authors**: J. Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, et al.
- **Date**: 2022-11-25
- **Link**: https://arxiv.org/abs/2211.14275
- **Why it matters**: Compares process-based vs outcome-based verification for quality scoring. Our 2-pass validation (initial score + verification pass) mirrors this process-based approach, and this paper shows why it produces more reliable results.
- **Swarm application**: Academic justification for our 2-pass tribunal validation. Process-based verification catches errors that outcome-based misses.

---

## Key Takeaways for Swarm

1. **Calibration is solvable** — Our judges can be calibrated so their scores are meaningful and consistent. This makes the Royal Jelly threshold scientifically defensible.
2. **Constitutional scoring works** — Our scoring prompt is a constitution. Anthropic's own research validates this pattern for evaluation.
3. **Process > outcome** — Our 2-pass validation is process-based verification. The OpenAI paper proves this is more reliable than single-pass scoring.
4. **Reliability is multi-dimensional** — Consistency (do judges agree?), calibration (are scores meaningful?), and faithfulness (does reasoning match score?) are all measurable. We already track the first two via drift threshold and score distribution.

---

*Source: [EgoAlpha/prompt-in-context-learning](https://github.com/EgoAlpha/prompt-in-context-learning) — EvaluationReliabilityList.md*
