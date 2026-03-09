# Repository Map

18 repos across the Swarm & Bee ecosystem. All on `~/Desktop/`.

## Core Platform

| Repo | Path | Description |
|------|------|-------------|
| swarmrouter | ~/Desktop/swarmrouter/ | Core platform: signal pipeline, curator fleet, data factory, worker API, skills framework, 28 skills |
| swarm-capital-markets | ~/Desktop/swarm-capital-markets/ | CRE capital markets intelligence engine: 8-stream cook, 7 skills, training scripts, 180-prompt eval |
| swarm-agents | ~/Desktop/swarm-agents/ | Agent framework: broker, reasoning, router, specialist, verifier agents |

## Blockchain & Infrastructure

| Repo | Path | Description |
|------|------|-------------|
| hedera-swarmfoundry | ~/Desktop/hedera-swarmfoundry/ | Hedera mainnet ops: minting, escrow, deeds, agents, PoE bridge |
| intelligence-objects | ~/Desktop/intelligence-objects/ | Intelligence Object pipeline + PIO examples |

## Websites

| Repo | Path | Description |
|------|------|-------------|
| swarmbeeai-factory | ~/Desktop/swarmbeeai-factory/ | swarmandbee.ai (Cloudflare Pages, 7 pages) |
| swarm-bee | ~/Desktop/swarm-bee/ | swarmandbee.com main site |

## Training & Inference

| Repo | Path | Description |
|------|------|-------------|
| **swarm-qwen-27B-Gold-Standard-Build-LLM** | ~/Desktop/swarm-qwen-27B-Gold-Standard-Build-LLM/ | **Gold standard Qwen3.5 training playbook** — 27B/9B/2B templates, proven manifests, deploy scripts, quality gates. THE source of truth for all builds. |
| **swarm-inference-gateway** | ~/Desktop/swarm-inference-gateway/ | **OpenAI-compatible API server** — routes to vLLM fleet, API key auth, SSE streaming, JSONL logging, Together.ai fallback. The front door to `api.swarmandbee.ai`. |
| swarm-vllm | ~/Desktop/swarm-vllm/ | vLLM 0.17.0 deployment configs, launch scripts, vision_config fixes, benchmark scripts |
| swarm_router_train | ~/Desktop/swarm_router_train/ | BeeMini router v2 training (60K pairs, serve_router.py) |
| swarm-capital-markets | ~/Desktop/swarm-capital-markets/ | Capital markets intelligence: 8-stream cook, 7 skills, training, 180-prompt eval |

## Eval

| Repo | Path | Description |
|------|------|-------------|
| swarmresearch32_eval | ~/Desktop/swarmresearch32_eval/ | Research model eval (300 prompts, 10 categories) |
| swarmresearch32_deep_eval | ~/Desktop/swarmresearch32_deep_eval/ | Deep eval (100 prompts, 9 categories, 4 tiers) |

## Tools & Utilities

| Repo | Path | Description |
|------|------|-------------|
| dataset-entropy | ~/Desktop/dataset-entropy/ | Zero-dependency dataset diversity measurement tool |
| swarm_roi | ~/Desktop/swarm_roi/ | ROI Objects pipeline, platinum pair conversion |
| swarm-vault-engine | ~/Desktop/swarm-vault-engine/ | Vault pipeline + model storage |
| swarm-wiki | ~/Desktop/swarm-wiki/ | This wiki — single source of truth |

## GitHub & HuggingFace

- **GitHub Org**: swarm-bee-github
- **HuggingFace Org**: https://huggingface.co/SwarmandBee

## Which Code Lives Where

| Capability | Primary Repo | Secondary |
|------------|-------------|-----------|
| Signal workers (11) | swarmrouter/signal/ | — |
| Curator fleet | swarmrouter/curator/ | — |
| Data factory (10 stages) | swarmrouter/data/factory/ | — |
| Cook scripts | swarmrouter/data/ | swarm-capital-markets/data/ |
| Skills (28 CRE+Med) | swarmrouter/skills/ | swarmrouter/worker/src/skills/ |
| Skills (7 capital markets) | swarm-capital-markets/skills/ | — |
| Worker API (40+ endpoints) | swarmrouter/worker/ | — |
| Training scripts | swarmrouter/data/ | swarm-capital-markets/train/ |
| Inference gateway | swarm-inference-gateway/ | swarm-vllm/ |
| Eval suites | swarmresearch32_eval/ | swarm-capital-markets/eval/ |
| Hedera bridge | swarmrouter/data/factory/ | hedera-swarmfoundry/ |
| Websites | swarmbeeai-factory/ | swarm-bee/ |
