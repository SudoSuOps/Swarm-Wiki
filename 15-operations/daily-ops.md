# Daily Operations

## Health Checks

```bash
# GPU status
ssh swarmrails "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,power.draw --format=csv,noheader"

# vLLM servers
curl -s swarmrails:8081/health  # 9B model
curl -s swarmrails:8082/health  # 27B model

# API health
curl -s https://router.swarmandbee.com/health

# Signal status
python3 -m signal status
```

## Monitor Active Training

```bash
# Check running processes
ssh swarmrails "ps aux | grep python3 | grep -v grep"

# Tail training log
ssh swarmrails "tail -20 /data2/swarmcapitalmarkets/train_full.log"

# GPU power/memory
ssh swarmrails "nvidia-smi"
```

## Signal Pipeline

```bash
# Check signal daemon
ssh zima-edge-1 "systemctl status swarmsignal"

# Manual collect
python3 -m signal collect --dry-run
python3 -m signal collect

# Run daemon (tiered: 15min/1hr/6hr)
python3 -m signal run
```

## Cook Status

```bash
# Check active cooks
TOGETHER_KEY=... python3 -m data.cre_capital_cook --status

# Check R2 bucket sizes
# (use Cloudflare dashboard or wrangler r2 commands)
```

## Key Paths on swarmrails

| Path | Content |
|------|---------|
| /data2/swarmcurator-9b-p2/merged/ | SwarmCurator-9B merged model |
| /data2/swarmcurator-27b/merged/ | SwarmCurator-27B merged model |
| /data2/swarmcapitalmarkets/ | Capital markets training data + scripts |
| /data2/swarmpharma-35b/ | SwarmPharma-35B model |
| /data2/swarm-qwen27b/ | Training layout (scripts, configs, logs) |
