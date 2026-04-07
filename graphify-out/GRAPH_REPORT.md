# Graph Report - /home/swarm/Swarm-Wiki  (2026-04-07)

## Corpus Check
- 178 files · ~132,610 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 431 nodes · 487 edges · 51 communities detected
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `SwarmLedger 5-Layer Finality Pipeline (23,500+ deeds, 477 batches)` - 10 edges
2. `SwarmConfig — Central Config Loader` - 8 edges
3. `Prompt Machine — Automated Prompt Evolution` - 8 edges
4. `7-Middleware Chain (SignalIngestion→Classification→Analysis→Strategy→QualityGate→StateUpdate→Dispatch)` - 8 edges
5. `Broken Weights Intelligence — Agent Model Failures (April 2026)` - 8 edges
6. `Title Deed` - 8 edges
7. `Algorithm Registry` - 8 edges
8. `Reliability & Calibration Research (LLM score defensibility)` - 7 edges
9. `Agent Orchestration Research Papers (Tier 2)` - 7 edges
10. `ClawHash` - 7 edges

## Surprising Connections (you probably didn't know these)
- `SwarmConfig — Central Config Loader` --references--> `Tribunal Layer (Scale A + Scale B, 24/7 autonomous)`  [INFERRED]
  00-config/swarm_config.py → README.md
- `Tribunal Parameters (drift_threshold, temperature, batch_size)` --conceptually_related_to--> `Tribunal Layer (Scale A + Scale B, 24/7 autonomous)`  [INFERRED]
  00-config/swarm_config.py → README.md
- `Decision Logging (.state/fleet_runs.jsonl for RL training)` --semantically_similar_to--> `GRPO — Binary RL (tool-call accuracy, completion correctness)`  [INFERRED] [semantically similar]
  06-curation/middleware.md → 19-research/slime-framework-reference.md
- `5-Step Trajectory Template (IDENTIFY→CALCULATE→ANALYZE→EVALUATE→RECOMMEND)` --semantically_similar_to--> `Paper: Constitutional AI — Harmlessness from AI Feedback (Bai et al., 2022)`  [INFERRED] [semantically similar]
  06-curation/README.md → 19-research/reliability-calibration.md
- `PropolisCollector (failure harvesting → cook_swarmjelly.py)` --semantically_similar_to--> `Broken Weights Intelligence — Agent Model Failures (April 2026)`  [INFERRED] [semantically similar]
  06-curation/README.md → 19-research/broken-weights-intelligence.md

## Hyperedges (group relationships)
- **Tribunal → Deed → Merkle → Hedera Finality Chain** — tribunal_layer, recording_layer, merkle_py, finality_layer4_hedera, swarmledger_finality [EXTRACTED 0.95]
- **Prompt Evolution Closed Loop (Cook → Telemetry → Softmax → Mutation → Extinction)** — pair_generation_engine, hive_ledger, softmax_allocation, prompt_mutations, extinction_rule, prompt_machine [EXTRACTED 0.95]
- **7-Middleware Orchestration Flow (Signal → Classification → Strategy → Dispatch)** — middleware_chain, orchestrator, planner, assembler, publisher, velocity_tracker [INFERRED 0.85]
- **Research Ops Experiment Pipeline** — exp001_position_bias, exp002_fewshot, exp003_cot, exp004_ape, scoring_prompt, specificity_gap, researchops_changelog [INFERRED 1.00]
- **ClawHash Security Convergence** — clawhash, openclaw, cve_2026_25253, nemoclaw, anthropic_kill_switch, unfixable_trifecta, clawhash_6_subalgorithms [INFERRED 1.00]
- **Infrastructure Compute Stack** — swarmrails, whale, nas, swarm_controller, blackwell_rtx6000, blackwell_rtx4500, rtx3090, miner_discipline, flight_sheets, energy_economics [INFERRED 1.00]
- **Swarm Model Training + Deployment Pipeline** —  [INFERRED 1.00]
- **SwarmTitle Deed Provenance Chain** —  [INFERRED 1.00]
- **Edge Node Infrastructure** —  [INFERRED 1.00]
- **Full Transaction Lifecycle** — PSA, JudgeCalibrationCert, ClosingStatement, PostClosingWarranty, SwarmTitle, HederaHCS, MerkleTree [INFERRED 1.00]
- **Quality Production Stack** — RedBlueTribunal, FlightSheetEpoch1, CalibrationDoctrine, VirginJellyPipeline, SwarmCurator9B, FiveProvenanceProofs [INFERRED 0.90]
- **Go-To-Market Stack** — EnterpriseCookbookPricing, RelocationEconomics, OfferingMemorandum_Internal, ProofOfLocation, OM_CRE, OM_Medical, BusinessModelREADME, CapitalMarketsEngine [INFERRED 0.90]
- **Tribunal Processing Pipeline** — scout_bee, router_bee, filter_bee, repair_bee, critic_bee, katniss, deed, merkle_tree, hedera_anchor [INFERRED 1.00]
- **Mining Economics Framework** — algorithm_registry, weights_hash, mining_matrix, flight_sheet, proof_of_weight, weight_classes, rwa_deed, spot_futures [INFERRED 1.00]
- **Trust and Verification Stack** — glass_wall, spectators, challengeable_transparency, five_trust_layers, five_proofs, hedera_anchor, behavioral_eval, swarm_eval [INFERRED 1.00]
- **Signal-to-Cook Feedback Loop** — signal_pipeline, entity_scorer, velocity_tracker, curator_bridge, factory_protocol [INFERRED 1.00]
- **OpenClaw Market Signal to Products** — openclaw_anthropic_ban, hn_signal_report_april_2026, x_signal_openclaw_april_2026, grok_finetune_playbook, grok_lora_hyperparams, agenthash_failure_categories [INFERRED 1.00]
- **Audit and Compliance Stack** — dataset_curation_audit, factory_protocol_audit, regulatory_audit, eu_ai_act, six_gate_pipeline, cove_2stage, safestore_3tier [INFERRED 0.90]
- **Factory Production Pipeline** — factory_protocol, quality_gates, cove_promotion, safestore, r2_buckets, hcs_seal [INFERRED 1.00]
- **Skills Deployment Stack** — swarm_skills_framework, skill_spec_format, curator_skills_py, swarm_router_worker, cloudflare_workers [INFERRED 1.00]
- **Swarm Inference Platform** — openai_inference_gateway, swarmcurator_27b, swarmcurator_9b, wallet_metering, cloudflare_workers [INFERRED 1.00]
- **Intelligence Object Lifecycle** — n1, n7, n19, n27, n33, n36 [INFERRED 1.00]
- **Curator Fleet Training Loop** — n9, n14, n15, n16, n18, n38 [INFERRED 1.00]
- **Pool API Mining Economics** — n5, n29, n30, n33, n42 [INFERRED 1.00]
- **Bitcoin PoW Analog in Swarm** — n17, n31, n33, n24, n19 [INFERRED 0.90]
- **Algorithm Registry Production Stack** — n1, n12, n35, n36, n32, n34 [INFERRED 1.00]
- **ClawHash + AgentHash Adversarial Pair Ecosystem** — n9, n10, n38, n33, n14 [INFERRED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (42): Intelligence Object, cook_swarmcurator_9b.py, cook_swarmcurator_27b.py, cook_swarmcurator_ops.py, make_swarmcre.py, Train Scripts, SwarmCurator-9B, SwarmCurator-27B (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (29): AI Studio Agent (PASETO v4, d78a1a60...), Bitcoin Merkle Tree Parallel (same algorithm, new asset class), Proof-of-Work → Proof-of-Location Mapping, CRE Broker Agent (0.0.10298834, dedicated topics), Deed Lifecycle (queued→scored→deeded→batched→anchored), Dual-Judge Tribunal as Honesty Mechanism (collusion architecturally impossible), 13 ENS Domains (swarmdeed.eth, swarmchain.eth, etc.), Layer 1: PostgreSQL (hot queries, mutable) (+21 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (26): Assembler (builds messages array, injects skills context), BaseVertical ABC (plugin architecture for verticals), Paper: CoALA — Cognitive Architectures for Language Agents (Sumers et al., 2023), 19 CRE Skills (broker_senior, comp_analyzer, debt_analyzer, etc.), Decision Logging (.state/fleet_runs.jsonl for RL training), DeerFlow (ByteDance) — Middleware Chain Inspiration, FleetContext (immutable configuration), FleetState (mutable processing batch state) (+18 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (25): Agent Orchestration Research Papers (Tier 2), Paper: AgentVerse — Multi-Agent Collaboration (Chen et al., 2023), Paper: AutoGen — Multi-Agent Conversation (Wu et al., 2023), Paper: Constitutional AI — Harmlessness from AI Feedback (Bai et al., 2022), Paper: Dynamic LLM-Agent Network (Liu et al., 2023), EgoAlpha/prompt-in-context-learning (source repo for research papers), Paper: GPTSwarm — Language Agents as Optimizable Graphs (Zhuge et al., 2024), Paper: Just Ask for Calibration (Tian et al., 2023) (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (25): SwarmAtlas Reasoning Tiers, Key Finding: Base 4B = Fine-Tuned 9B, BeeMini Router v2, CoVe (Chain of Verification), Swarm Model Fleet Topology, Gold Standard Build Specification, Memphis IC Validation Test, Nemotron Nano (Cook Fleet) (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (25): Behavioral Evaluation, Data Warehouse (1.5M+ pairs, 10 domains), Title Deed, Discovery Document, Edge Deployment, Eval Protocol — Standing Rules, Finding: Five Coordinates, Five Proofs of Defendability (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (24): AgentHash Demand Signal ($43.2M TAM, 135K instances × $320), Broken Weights Intelligence — Agent Model Failures (April 2026), ClawHash New Templates (Drift, CorruptTurn, FakeExec), Curation README — Production Pipeline + Blueprint, Extinction Rule (avg < 85 + 200 pairs → removed), Failure Pattern 2: Malformed Call Format, Failure Pattern 3: Multi-Turn Corruption (unclosed tags), Failure Pattern 1: Plain-Text Fake Tool Calls (+16 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (24): Business Model Overview, Calibration — Evaluate the Evaluators, Capital Markets Intelligence Engine, ClawForge Meta-Agent, Closing Statement, Enterprise Cookbook Two-Tier Business Model, Five Provenance Proofs, Flight Sheet — Epoch 1 Validation (+16 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (17): AgentHash, AgentHash 6 Pair Buckets, AgentHash Failure Traces, Algorithm Registry, Anthropic ToS Kill Switch, AvionHash, ClawHash, ClawHash 6 Sub-Algorithms (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (17): Capital Markets Skills (7), Cloudflare Workers, CRE Skills (19), curator/skills.py, Letter Sender Skill, Medical Skills (9), R2 Buckets, SafeStore (+9 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (16): Curator Bridge (curator_bridge.py), Discord Bridge (discord_bridge.py), EntityScorer, Event Bridge (event_bridge.py), Hedera Signal Bridge (hedera_bridge.py), Memory Bridge (memory_bridge.py), NER Entity Databases, Planner (VelocityTracker heat-map → cook orders) (+8 more)

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (14): BaseWorker ABC, HN Signal Report April 2026, OpenClaw Anthropic Ban, arXiv Worker (worker_arxiv.py), CRE News Worker (worker_cre_news.py), EDGAR Worker (worker_edgar.py), FRED Worker (worker_fred.py), GitHub Worker (worker_gh.py) (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.16
Nodes (14): CoVe 2-Stage Verification, CoVe Promotion, Dataset Curation Audit, Factory Protocol (factory_protocol.py), Factory Protocol Audit, HCS Seal, MASTER_PLATINUM, numeric_verify Gate (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (13): Aviation Audit, CreditSniper, Dataset Pair Schema, EU AI Act, Hippocratic AI, Medical & Pharma Audit, Pharma 5-Step Trajectory, Regulatory Audit (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.2
Nodes (12): GRPO, GRPO — Binary RL (tool-call accuracy, completion correctness), Living Weight — Continuous RL Improvement ($2K/month), OPD — On-Policy Distillation (recovery logic, state management), OpenClaw-RL, 3 Product Layers (Weight → Cook → RL-as-a-Service), OpenClaw-RL Architecture — Continuous Agent Self-Improvement, Slime 4-Component Architecture (SGLang Server + Rollout + PRM Judge + Megatron Trainer) (+4 more)

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (11): ASRS Aviation Cook, RTX PRO 4500 Blackwell, RTX PRO 6000 Blackwell, Energy Economics, Domain-Specific Flight Sheets, MINER Discipline, NAS (DS1525+), RTX 3090 (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.2
Nodes (10): bee-finalize-watcher, cloudflared tunnel, Five Proofs Per Deed, MinIO (zima-edge-1), Offering Memorandum — Aviation Domain, Offering Memorandum — Grants Domain, Proof of Location Case Study — Master Writer, swarm-witness (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (10): Critic Bee, Filter Bee, Finding: 27B Not Production Grade, Katniss, Repair Bee, Router Bee, Scout Bee, SwarmRefinery 3-Shift Operation (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (9): Challengeable Transparency, Finding: Energy Efficiency, Five Trust Layers, Flight Sheet, Glass-Wall, Glass-Wall Browser Layout, Permit Protocol, Spectators (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (6): APE (Large LLMs Are Human-Level Prompt Engineers), EXP-002: Few-Shot Exemplars, EXP-003: Per-Dimension CoT, EXP-004: APE Prompt Optimization, scoring_prompt.py, Specificity Quality Gap

### Community 20 - "Community 20"
Cohesion: 0.4
Nodes (6): Competitive Landscape 13, CoStar, CRE Capital Markets Audit, CRE Dataset Moat, RedSwan, SwarmCapitalMarkets-27B

### Community 21 - "Community 21"
Cohesion: 0.47
Nodes (6): Builder Permit Process, Deployment Runbook, OpenAI Inference Gateway, SwarmCurator-27B, SwarmCurator-9B, Training Runbook

### Community 22 - "Community 22"
Cohesion: 0.4
Nodes (5): DSPy/DSP, ARES (RAG Evaluation), PromptKG, Self-RAG, SwarmGraph

### Community 23 - "Community 23"
Cohesion: 0.67
Nodes (4): LOI Flight Sheet Template, SwarmTitle Certification Process, SwarmTitle Insurance, Title Commitment Template

### Community 24 - "Community 24"
Cohesion: 0.5
Nodes (4): Docling MCP, Data Lifecycle, SPOT vs FUTURES Pricing, Virgin Jelly

### Community 25 - "Community 25"
Cohesion: 0.5
Nodes (4): AgentHash Failure Categories, Grok Fine-Tune Playbook, Grok LoRA Hyperparameters, X Signal OpenClaw April 2026

### Community 26 - "Community 26"
Cohesion: 0.67
Nodes (3): Offering Memorandum — Internal (Proof of Location), Proof of Location Protocol, Relocation Economics

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (2): EXP-001: Position Bias, MT-Bench

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (2): ChatEval, LLM-as-Judge Research

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (2): Convergence Efficiency, Pressure to Truth

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (2): Mining Matrix, Weights-Hash

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (2): Infrastructure & GPU Audit, Qwen3.5 Architecture

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (2): swarmandbee.ai Website, SwarmScaler

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): swarmandbee.ai — 12+ Route Website

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Swarm Fleet Hardware (swarmrails, whale, zima-edge, NAS)

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Model Addition Workflow (CONTRIBUTING.md)

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Pair Count Update Protocol

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Hedera Mainnet Accounts (operator 0.0.10291827, HNS 0.0.10291542)

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): Hedera Fee Schedule ($0.0008/ConsensusSubmitMessage)

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Process Reward Model (PRM)

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): GitNexus

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): RAG (Lewis et al. 2020)

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): ResearchOps Changelog

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (1): AgentHash Failure Labels

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): CoT & Prompt Design Research

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): GRPO Hyperparameters

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Convergence Ladder

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): SwarmCRE App Store

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): Hardware Products (BeeMini/BeePro/BeeRack)

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): MASTER_GOLD

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (1): Repository Map (19 repos)

## Knowledge Gaps
- **117 isolated node(s):** `swarm.yaml — Single Source of Truth Config File`, `Tribunal Scale Configuration (Scale A / Scale B models)`, `Domain-Hash Pricing Config (price_per_lb, rj_per_hour)`, `Red/Blue Team Model Config`, `Deed Writer Model Config` (+112 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 27`** (2 nodes): `EXP-001: Position Bias`, `MT-Bench`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `ChatEval`, `LLM-as-Judge Research`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `Convergence Efficiency`, `Pressure to Truth`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `Mining Matrix`, `Weights-Hash`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `Infrastructure & GPU Audit`, `Qwen3.5 Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `swarmandbee.ai Website`, `SwarmScaler`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `swarmandbee.ai — 12+ Route Website`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Swarm Fleet Hardware (swarmrails, whale, zima-edge, NAS)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Model Addition Workflow (CONTRIBUTING.md)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `Pair Count Update Protocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `Hedera Mainnet Accounts (operator 0.0.10291827, HNS 0.0.10291542)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `Hedera Fee Schedule ($0.0008/ConsensusSubmitMessage)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Process Reward Model (PRM)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `GitNexus`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `RAG (Lewis et al. 2020)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `ResearchOps Changelog`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `AgentHash Failure Labels`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `CoT & Prompt Design Research`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `GRPO Hyperparameters`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Convergence Ladder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `SwarmCRE App Store`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `Hardware Products (BeeMini/BeePro/BeeRack)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `MASTER_GOLD`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `Repository Map (19 repos)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Curator Orchestrator (state machine: Pending→Cooking→Ready→Published)` connect `Community 2` to `Community 10`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `Planner (VelocityTracker heat-map → cook orders)` connect `Community 10` to `Community 2`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **What connects `swarm.yaml — Single Source of Truth Config File`, `Tribunal Scale Configuration (Scale A / Scale B models)`, `Domain-Hash Pricing Config (price_per_lb, rj_per_hour)` to the rest of the system?**
  _117 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._