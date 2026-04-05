# Knowledge Graphs & RAG — Graph Construction, Retrieval, Provenance

Papers covering knowledge graph construction, graph-augmented retrieval, and provenance systems. These inform SwarmGraph (provenance graph) and GitNexus (code knowledge graph).

## TOP 15 — Ranked by Relevance to SwarmGraph

### 1. Chain of Knowledge: A Framework for Grounding LLMs with Structured Knowledge Bases
- **Date**: 2023-05-22 | **Link**: https://arxiv.org/abs/2305.13269
- **Why**: Directly addresses grounding LLMs with structured KBs — the core pattern SwarmGraph needs for connecting scored pairs, judges, and provenance chains into a queryable structure.

### 2. Decoupling Knowledge from Memorization: Retrieval-augmented Prompt Learning (PromptKG)
- **Date**: 2022-05-29 | **Link**: https://arxiv.org/abs/2205.14704 | **GitHub**: zjunlp/promptkg (662 stars)
- **Why**: Explicitly about retrieval-augmented prompting over knowledge graphs. The PromptKG framework is the closest architectural analog to what SwarmGraph + GitNexus does: structured KG retrieval feeding into prompt construction.

### 3. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG — the original)
- **Date**: 2020-05-22 | **Link**: https://arxiv.org/abs/2005.11401 | **Citations**: 551
- **Why**: The foundational RAG paper. Defines the retrieve-then-generate paradigm that underpins how SwarmGraph should serve provenance context to judges and downstream consumers.

### 4. Relation Extraction as Open-book Examination: Retrieval-enhanced Prompt Tuning
- **Date**: 2022-05-04 | **Link**: https://doi.org/10.1145/3477495.3531746 | **Venue**: SIGIR
- **Why**: Relation extraction is the core operation in building provenance graphs — extracting judge-to-pair, pair-to-domain, pair-to-Merkle-batch edges.

### 5. Unveiling LLMs: The Evolution of Latent Representations in a Temporal Knowledge Graph
- **Date**: 2024-04-04 | **Link**: https://arxiv.org/abs/2404.03623
- **Why**: Temporal KGs are directly relevant to SwarmGraph's time-ordered provenance model — epochs, scoring timestamps, Merkle batch sealing times.

### 6. RAG Survey: Retrieval-Augmented Generation for AI-Generated Content
- **Date**: 2024-02-29 | **Link**: https://arxiv.org/abs/2402.19473 | **GitHub**: hymie122/rag-survey (893 stars)
- **Why**: Comprehensive RAG survey covering structured-knowledge-augmented generation patterns. Essential reference for designing SwarmGraph's retrieval interface.

### 7. GraphPrompt: Unifying Pre-Training and Downstream Tasks for Graph Neural Networks
- **Date**: 2023-02-16 | **Link**: https://arxiv.org/abs/2302.08043
- **Why**: Directly relevant to SwarmGraph's node/edge representation. Unifies graph pre-training with downstream tasks through prompting.

### 8. KnowledGPT: Enhancing LLMs with Retrieval and Storage Access on Knowledge Bases
- **Date**: 2023-08-17 | **Link**: https://arxiv.org/abs/2308.11761
- **Why**: Combines LLM generation with structured KB retrieval and storage — exactly the read/write pattern SwarmGraph needs when deed recorder writes and judges read.

### 9. Demonstrate-Search-Predict (DSP/DSPy)
- **Date**: 2022-12-28 | **Link**: https://arxiv.org/abs/2212.14024 | **GitHub**: stanfordnlp/dsp (14K stars)
- **Why**: Composable pipeline pattern: demonstrate, search, predict. Maps to SwarmGraph workflow: demonstrate quality with exemplar deeds, search provenance graph, predict/score new pairs.

### 10. Representing Text for Joint Embedding of Text and Knowledge Bases
- **Date**: 2015 | **Link**: https://doi.org/10.18653/v1/D15-1174 | **Citations**: 551 | **Venue**: EMNLP
- **Why**: Foundational work on jointly embedding text and KBs. For SwarmGraph, where scored Q&A text coexists with graph edges, joint embedding bridges semantic retrieval and graph traversal.

### 11. Untangle the KNOT: Interweaving Conflicting Knowledge and Reasoning
- **Date**: 2024-04-04 | **Link**: https://arxiv.org/abs/2404.03577
- **Why**: Addresses conflicting knowledge in LLMs — directly relevant to dual-judge disagreement. How to interweave conflicting KGs informs dispute resolution in scoring.

### 12. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- **Date**: 2023-10-17 | **Link**: https://arxiv.org/abs/2310.11511 | **GitHub**: AkariAsai/self-rag (1,600 stars)
- **Why**: Self-RAG's retrieve-generate-critique loop mirrors SwarmProtocol's score-validate-seal cycle.

### 13. Knowledgeable Prompt-tuning: Incorporating Knowledge into Prompt Verbalizer
- **Date**: 2021-08-04 | **Link**: https://arxiv.org/abs/2108.02035 | **Venue**: ACL
- **Why**: Shows how to inject external knowledge into prompt verbalizers. Enables domain-specific knowledge injection (medical ontologies, grant taxonomies) into scoring prompts.

### 14. REALM: Retrieval-Augmented Language Model Pre-Training
- **Date**: 2020-02-10 | **Link**: https://arxiv.org/abs/2002.08909 | **Citations**: 542
- **Why**: Pioneered pre-training with a differentiable retriever — architectural foundation for systems that learn what to retrieve.

### 15. ARES: Automated Evaluation Framework for RAG Systems
- **Date**: 2023-11-16 | **Link**: https://arxiv.org/abs/2311.09476 | **GitHub**: stanford-futuredata/ares (371 stars)
- **Why**: Automated evaluation of RAG across context relevance, answer faithfulness, and answer relevance — the same axes Swarm-Inspector validates.

---

## Key Takeaways for Swarm

1. **PromptKG is our closest academic cousin** — ZJU NLP's work on retrieval-augmented prompting over knowledge graphs is architecturally what SwarmGraph + GitNexus does.
2. **DSPy/DSP is the composable pattern** — 14K stars, Stanford NLP. Our pipeline (demonstrate quality → search provenance → predict scores) is exactly their framework.
3. **Temporal KGs for provenance** — SwarmGraph is fundamentally a temporal knowledge graph. Epochs, timestamps, sealing order all matter.
4. **Joint embeddings bridge text and structure** — Our scored pairs (text) + graph edges (structure) need joint representation for effective retrieval.
5. **Note**: KnowledgeAugmentedPromptList.md and RetrievalAugmentedGenerationList.md are byte-for-byte identical files in the source repo.

---

*Source: [EgoAlpha/prompt-in-context-learning](https://github.com/EgoAlpha/prompt-in-context-learning) — PromptKnowledgeGraphList.md, RetrievalAugmentedGenerationList.md*
