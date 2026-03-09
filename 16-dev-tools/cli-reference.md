# CLI Reference

Complete command reference for all Swarm & Bee CLI tools.

## Curator Pipeline (`python3 -m curator`)

```bash
# Plan cook orders (signal-directed)
python3 -m curator plan --vertical cre --signal /data2/swarmsignal/

# Execute a cook order
python3 -m curator run order.yaml --dry-run

# Direct cook for a vertical
python3 -m curator cook cre --target 5000 --stream underwriting

# Format raw output into training records
python3 -m curator assemble output.jsonl --vertical cre --eval-pct 0.05

# Run gates + dedup
python3 -m curator validate output.jsonl --vertical cre --cross-batch

# Push to R2
python3 -m curator publish platinum.jsonl --vertical cre --prefix pairs/

# Show pair inventory
python3 -m curator inventory --vertical cre

# Quality report
python3 -m curator report --gate-breakdown --input output.jsonl

# Show delta since last run
python3 -m curator delta

# Run fleet middleware chain (27B+9B+2B)
python3 -m curator fleet --dry-run --head URL --ops URL --worker URL

# Discover and manage skills
python3 -m curator skills --vertical cre --bootstrap --prompt-section
```

## Signal Engine (`python3 -m signal`)

```bash
# One-shot collection
python3 -m signal collect --workers rss,hn,arxiv --dry-run

# Daemon mode (tiered: 15min/1hr/6hr)
python3 -m signal run

# Engine status
python3 -m signal status

# Aggregate stats
python3 -m signal stats

# Topic velocity / acceleration
python3 -m signal velocity --topic office-distress --limit 20

# Drop a human-curated signal
python3 -m signal drop \
  --title "NVIDIA $4B photonics" \
  --domain cre \
  --priority 2 \
  --url https://example.com \
  --type industry_development

# Edge node status
python3 -m signal edge-status
```

## Data Factory (`python3 -m data.factory`)

```bash
# Run 6 code gates on JSONL
python3 -m data.factory gate input.jsonl --domain cre

# Cook via Together.ai two-tier pipeline
python3 -m data.factory cook input.jsonl --domain cre --workers 10

# Promote gold → platinum (rewrite + CoVe)
python3 -m data.factory promote gold.jsonl --domain medical --workers 25

# Push to R2 with sharding + manifest
python3 -m data.factory push platinum.jsonl --bucket sb-cre --prefix pairs/

# Factory dashboard
python3 -m data.factory health --json

# Industrial audit scoreboard
python3 -m data.factory audit --scoreboard --full

# Pipeline status
python3 -m data.factory status --cook-id UUID

# Cook proposals
python3 -m data.factory propose create --domain cre --stream energy --target 10000
python3 -m data.factory propose list --status draft
python3 -m data.factory propose show <id>
python3 -m data.factory propose submit <id>
python3 -m data.factory propose approve <id>
python3 -m data.factory propose scan
```

## Capital Markets Cook (`python3 -m data`)

```bash
# 8-stream cook (debt_maturity, cmbs_distress, rate_advisory, equity_advisory,
#   valuation_advisory, deal_origination, macro_causality, deal_graph)
TOGETHER_API_KEY=... python3 -m data.cre_capital_cook --stream all --workers 50

# Reasoning Path Augmentation (5 personas, 235B)
TOGETHER_API_KEY=... python3 -m data.cook_rpa --workers 100

# 109 hand-crafted prompts x 3 response variants
TOGETHER_API_KEY=... python3 -m data.cook_golden_pairs

# Platinum mutation engine
TOGETHER_API_KEY=... python3 -m data.cook_platinum_mutations

# 5-pool blend + rebalance + eval holdout
python3 -m data.assemble_final --dry-run
```

## Vault Engine (`python -m cli.reconcile`)

```bash
# Local NAS reconciliation
python -m cli.reconcile --nas-path /path --output ./vault

# R2 + NAS reconciliation
python -m cli.reconcile --r2-bucket sb-cre --r2-bucket sb-medical --nas-path /path

# Full fleet scan
python -m cli.reconcile --scan-rigs --output ./vault

# With fuzzy dedup + sync back
python -m cli.reconcile --fuzzy --sync-back --output ./vault --verbose
```

## Hedera SwarmFoundry (`node index.js`)

```bash
node index.js init                      # Create HCS topics + HTS tokens
node index.js seal <block>              # Seal block → HCS + HFS + HTS
node index.js migrate --full-run        # Migrate from Base/ETH
node index.js verify <fp|chain>         # Verify pair or chain
node index.js status                    # SwarmChain/PoPChain counts
node index.js inventory                 # Consolidate all sources
node index.js foundry <pdf>             # PDF → pair generation
node index.js agent <task>              # Agent commands
node index.js train-model               # Generate training config
node index.js generate-om [name] [fmt]  # Offering Memorandum
node index.js generate-deed [num] [fmt] # Certificate of Pair
```

## Swarm Agents (`npm run`)

```bash
npm run broker           # CRE broker agent
npm run dial             # Dialer (--blast mode)
npm run dial:pitch       # Pitch dialer
npm run brief            # Brief agent
npm run outreach         # Outreach agent
npm run outreach:linkedin # LinkedIn outreach
npm run bot              # SwarmBot
npm run bot:register     # Register bot on Hedera
```

## Cloudflare Workers

```bash
# SwarmRouter edge worker
cd worker && npx wrangler deploy    # Production
cd worker && npx wrangler dev       # Local dev
cd worker && npx wrangler tail      # Live logs

# Swarm API worker
cd swarm-api-worker && npm run deploy
cd swarm-api-worker && npm run tail
```

## Training Scripts (Direct Execution)

```bash
# Cook pairs
TOGETHER_API_KEY=... python3 data/cook_swarmcurator_9b.py --stream all --workers 50 --assemble
TOGETHER_API_KEY=... python3 data/cook_swarmcurator_27b.py --stream all --workers 50

# Train models
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=0 python3 data/train_swarmcurator_9b.py
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=1 python3 data/train_swarmcurator_27b_v1.py
```
