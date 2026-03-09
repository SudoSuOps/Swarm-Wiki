# Glossary

Definitions for terms used throughout the Swarm ecosystem.

---

**Intelligence Object** -- A finalized, verified, structured piece of CRE (or vertical-specific) data that has passed all quality gates. This is the correct term for what Swarm produces. Not a dataset. Not a document. An Intelligence Object. It has provenance, a quality score, and optionally an HCS seal.

**PIO (Platinum Intelligence Object)** -- An Intelligence Object that has passed all six deterministic gates plus CoVe verification. The highest quality tier. PIOs are eligible for HCS sealing and promotion to production training sets.

**Pair** -- A single instruction-response training example in JSONL format. Contains a system prompt, user instruction, and assistant response. The atomic unit of training data in the Swarm factory.

**Vertical** -- A domain-specific application layer. Current verticals: CRE (commercial real estate), Medical/Pharma, Aviation, Capital Markets. Each vertical has its own training data, models, skills, and evaluation criteria.

**Cook** -- The process of generating new training pairs from raw data or signals. A cook order specifies the vertical, task type, number of pairs, and source data. "Cooking" is running the factory pipeline to produce pairs.

**Gate** -- A deterministic quality check applied to generated pairs before promotion. Six gates run in sequence: JSON validity (0.30 weight), schema completeness (0.25), enum validation (0.25), verdict match, score MAE, and confidence threshold (>= 0.80 to pass). Gates are code, not models.

**Promote** -- Moving a pair from generated status to verified status after passing all gates and CoVe review. Promoted pairs enter the training pool. Failed pairs are logged with reasons.

**Trajectory** -- An enhanced training pair that includes intermediate reasoning steps, not just the final answer. Trajectory pairs teach models how to think through a problem, not just what to output. Used in pharma (28,624 trajectory-enhanced pairs across 16 task types).

**SafeStore** -- Secure storage for sensitive intelligence objects. Encrypted at rest, access-controlled, audit-logged.

**HCS Seal** -- A SHA-256 hash of an intelligence object published to a Hedera Consensus Service topic on mainnet. The seal proves that a specific piece of data existed in a specific state at a specific time. Produces a guarantee.json file containing the Merkle root, hash, HCS transaction ID, and timestamp.

**Guarantee** -- The guarantee.json file produced by an HCS seal. Contains the complete provenance chain: what data was sealed, when, by which agent, with what hash, and the on-chain transaction ID. This is the trust anchor for any intelligence object.

**SKILL.md** -- A specification file for a Swarm skill. YAML frontmatter (name, version, vertical, description, role) plus a markdown body describing the skill's behavior, inputs, outputs, and constraints. LLM-injectable via `skills_prompt_section()`. 28 skills defined across CRE and medical verticals.

**Fleet** -- The collection of deployed models operating as a coordinated system. The curator fleet (2B/9B/27B) handles signal classification, analysis, and strategic decisions. The vertical fleet (35B MoE models) handles domain-specific tasks. Fleet topology: edge (2B) -> inference (9B) -> strategic (27B) -> specialist (35B).

**Middleware** -- The 7-stage processing chain in the curator fleet: SignalIngestion, Classification, Analysis, Strategy, QualityGate, StateUpdate, Dispatch. Each stage has an LLM endpoint and an algorithmic fallback.

**Sandbox** -- An isolated execution environment for running generated code or agent actions. Two providers: Local (development) and Remote SSH (swarmrails/whale for production). Alibaba OpenSandbox evaluated for future multi-tenant isolation.

**Signal** -- A market event detected by one of the 11 signal workers. Signals are scored by EntityScorer, tracked by VelocityTracker, and prioritized P1 through P3 (or filtered as noise). Signals are the raw input that drives the entire pipeline.

**Curator** -- The AI system that converts signals into training data. The curator fleet (three model tiers) classifies, analyzes, and makes strategic decisions about what to cook, how much, and at what quality level. AI observing AI.

**Deal Machine** -- The mapping between a traditional CRE brokerage deal lifecycle (Dials through Close) and the Swarm pipeline. Every component in Swarm corresponds to a real step in how commercial real estate deals get done. See [deal-machine.md](deal-machine.md).

**GDN (Gated Delta Network)** -- The linear attention mechanism used in 75% of Qwen3.5 transformer layers. GDN layers run in O(n) time versus O(n^2) for standard attention. The architecture alternates in blocks of 3 GDN layers + 1 standard attention layer. This is what makes Qwen3.5 efficient at long contexts (262K native, 1M via YaRN).

**Cook Order** -- A specification sent from the Curator Planner to the Factory, defining what pairs to generate. Includes vertical, task type, target count, source data references, and quality constraints.

**CoVe (Chain of Verification)** -- The multi-step verification process applied to generated pairs. Pairs pass through deterministic gates first, then receive a quality classification (platinum, gold, or fail) with per-criterion scores for accuracy, completeness, structure, relevance, and SFT quality.

**EntityScorer** -- A component in the signal pipeline that assigns relevance scores to detected entities based on profile data, market context, and historical signal patterns.

**VelocityTracker** -- A component that detects acceleration in entity signal frequency. An entity appearing 3 times in a week is treated differently than 3 times in a year. Velocity is a key input to signal prioritization.

**vLLM** -- The inference serving framework used for production model deployment on swarmrails. Version 0.17.0 with PyTorch CUDA 12.8, supporting both sm_86 and sm_120 (Blackwell) architectures.

**Unsloth** -- The training framework used for all Swarm model fine-tuning. Provides FastLanguageModel wrapper around HuggingFace transformers with optimized LoRA training, packing support, and efficient memory management.

**LoRA (Low-Rank Adaptation)** -- The fine-tuning method used for all Swarm models. Adds small trainable adapter layers to a frozen base model. Standard configuration: r=64, alpha=32 for 9B/27B models; r=32 for 2B. bf16 only (no QLoRA) for Qwen3.5 architecture.
