# SwarmResearch-32B

General-purpose research model. Built on the previous-generation Qwen2.5 architecture before the move to Qwen3.5. Still operational for open-ended investigation tasks that do not fit neatly into a vertical skill.

## Specifications

| Field | Value |
|-------|-------|
| Base model | Qwen/Qwen2.5-32B |
| Architecture | Dense transformer, standard attention throughout |
| Generation | Gen 1 (pre-GDN, pre-248K vocab) |
| Training method | bf16 LoRA |
| Training pairs | 35,500 |
| Steps | 2,220 |
| Train loss | 0.635 |
| Checkpoint | swarmrails:/data2/swarm-research-32b/ |

## Training Data

35,500 pairs across general research domains. Unlike the vertical models (CRE, Medical, Aviation), SwarmResearch was trained to handle open-ended queries: multi-step reasoning, cross-domain analysis, literature synthesis, and investigative workflows.

## Evaluation

SwarmResearch-32B has the most comprehensive eval suite of any Swarm model:

### Standard Eval (300 prompts)
Located at `swarmrails:/data2/swarmresearch32_eval/`

10 categories with 30 prompts each:
- Factual recall
- Multi-step reasoning
- Cross-domain analysis
- Numerical computation
- Structured output generation
- Long-form synthesis
- Instruction following
- Edge case handling
- Ambiguity resolution
- Meta-cognitive tasks

### Deep Eval (100 prompts)
Located at `swarmrails:/data2/swarmresearch32_deep_eval/`

9 categories requiring multi-step reasoning chains:
- Complex causal analysis
- Adversarial prompts
- Conflicting evidence resolution
- Long-context comprehension
- Multi-constraint optimization
- Implicit reasoning
- Domain transfer
- Self-correction
- Compositional tasks

## Status

DONE. The model is trained and available but has been functionally superseded by SwarmCurator-27B for most tasks. The 27B on Qwen3.5 architecture (GDN + 262K context) outperforms the 32B on Qwen2.5 in nearly every category, at lower VRAM cost due to the GDN efficiency gains.

SwarmResearch-32B remains useful for:
- Baseline comparison against newer models
- Tasks requiring the older Qwen2.5 tokenizer behavior
- Eval development (the 300+100 prompt suite was built for this model and transferred to eval newer models)

## Legacy Note

This was the first Swarm model to demonstrate that domain-specific fine-tuning on curated pairs could meaningfully outperform base model prompting. The eval suite built for SwarmResearch became the template for all subsequent model evaluations.
