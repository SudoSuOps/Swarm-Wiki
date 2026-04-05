# Agent Orchestration — Multi-Agent Coordination Patterns

Papers covering multi-agent systems, role specialization, and pipeline orchestration. These inform SwarmOS → SwarmChain → SwarmTribunal → SwarmDeed coordination.

## TIER 2 — Agent Architecture Patterns

### 11. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- **Authors**: Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, et al.
- **Date**: 2023-08-16
- **Link**: https://arxiv.org/abs/2308.08155
- **GitHub**: 28K+ stars
- **Why it matters**: The definitive multi-agent conversation framework. Provides the orchestration pattern for coordinating multiple LLM agents — directly applicable to our SwarmOS epoch orchestration layer.
- **Swarm application**: Pattern reference for tribunal_runner.py coordinating Judge A, Judge B, deed recorder, and Merkle builder.

### 12. AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors
- **Authors**: Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, et al.
- **Date**: 2023-08
- **Link**: https://arxiv.org/abs/2308.10848
- **Why it matters**: Studies emergent behaviors when multiple agents collaborate — including how agent team composition affects task quality. Relevant to understanding how our two judges interact.
- **Swarm application**: Research on judge pair dynamics. Different model families (Gemma vs Qwen) may produce different emergent scoring patterns.

### 13. Dynamic LLM-Agent Network: An LLM-agent Collaboration Framework with Agent Team Optimization
- **Authors**: Zijun Liu, Yanzhe Zhang, Peng Li, Yang Liu, Diyi Yang
- **Date**: 2023-10-03
- **Link**: https://arxiv.org/abs/2310.02170
- **Why it matters**: Optimizes agent team composition dynamically. Could inform future tribunal designs where judge models are selected based on domain expertise rather than being fixed.
- **Swarm application**: Future: domain-specific judge selection. Medical pairs might benefit from different judge pairs than grants or aviation.

### 14. Cognitive Architectures for Language Agents (CoALA)
- **Authors**: T. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths
- **Date**: 2023-09-05
- **Link**: https://arxiv.org/abs/2309.02427
- **Why it matters**: Provides a unified architectural framework for building language agents with memory, action, and decision modules — the blueprint for how SwarmOS orchestrates tribunal + deed + Merkle flows.
- **Swarm application**: Our architecture already mirrors CoALA: SwarmKeeper = memory, SwarmTribunal = action, SwarmOS = decision/orchestration.

### 15. MetaGPT: Meta Programming for Multi-Agent Collaborative Framework
- **Authors**: Sirui Hong, Xiawu Zheng, Jonathan P. Chen, Yuheng Cheng, Ceyao Zhang, et al.
- **Date**: 2023-08-01
- **Link**: https://arxiv.org/abs/2308.00352
- **Why it matters**: Assigns specialized roles to different agents in a structured workflow with standardized outputs. Mirrors our architecture where Judge A, Judge B, deed recorder, and Merkle builder each have distinct roles.
- **Swarm application**: Validates our role separation: judges score, writer deeds, builder batches, anchor finalizes.

### 16. Language Agents as Optimizable Graphs (GPTSwarm)
- **Authors**: Mingchen Zhuge, Wenyi Wang, Louis Kirsch, et al.
- **Date**: 2024-02-26
- **Link**: https://arxiv.org/abs/2402.16823
- **Why it matters**: Models agent pipelines as computational graphs that can be optimized. Our tribunal → deed → Merkle → anchor pipeline could be modeled and optimized as such a graph.
- **Swarm application**: The entire SwarmProtocol pipeline is a directed acyclic graph. This paper provides the framework for optimizing it end-to-end.

---

## Key Takeaways for Swarm

1. **Role specialization beats generalists** — MetaGPT and AutoGen both show that agents with specialized roles outperform single-agent architectures. Our separated Judge A / Judge B / Deed Writer / Recorder validates this.
2. **Pipeline = graph = optimizable** — GPTSwarm's insight: if your pipeline is a graph, you can optimize it. Our pairs → bin → judges → deeds → Merkle → anchor is exactly such a graph.
3. **Dynamic team composition is the next level** — Currently our judges are fixed (gemma3:12b + qwen2.5:7b). Research suggests domain-specific judge selection could improve quality.
4. **Emergent behaviors matter** — AgentVerse shows that multi-agent systems develop emergent patterns. Our RJ yield differences across domains (97.8% legal vs 85.3% medical) may partially reflect judge pair dynamics, not just source quality.

---

*Source: [EgoAlpha/prompt-in-context-learning](https://github.com/EgoAlpha/prompt-in-context-learning) — AgentList.md*
