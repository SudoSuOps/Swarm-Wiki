# NAS (Synology DS1525+)

Central storage backbone for the swarm. Hosts model vault and shared data via NFS.

## Hardware

| Field | Value |
|-------|-------|
| Model | Synology DS1525+ |
| IP | 192.168.0.102 |
| CPU | AMD Ryzen V1500B (Zen, 4C/8T, 2.2 GHz) |
| RAM | 8 GB ECC DDR4 |
| Storage | 2x WD Red Plus 2TB (RAID 1) -- 1.8 TB usable, ~1.1 TB free |
| Network | Gigabit Ethernet (bonded) |
| OS | DSM 7.x |
| DSM Web | http://192.168.0.102:5000 |

## Access

```bash
ssh admin@192.168.0.102   # password: Jupiter1023$
```

DSM web UI at http://192.168.0.102:5000.

## NFS Shares

The primary share `/volume1/swarm` is mounted on all compute nodes:

| Node | Mount Point | Method |
|------|-------------|--------|
| swarmrails (Xeon) | `/mnt/swarm` | fstab (nfs defaults,soft,timeo=150,retrans=3) |
| whale (192.168.0.99) | `/mnt/swarm` | fstab |
| bee (192.168.0.70) | `/mnt/swarm` | fstab |

## Model Vault

Large model checkpoints stored at `/volume1/swarm/models/`:

| Directory | Model | Size |
|-----------|-------|------|
| `swarmcre-35b/` | SwarmCRE 35B v1 | 67 GB |
| `swarmcre-35b-v2/` | SwarmCRE 35B v2 | ~67 GB |
| `swarmpharma-35b-v1/` | SwarmPharma 35B v1 | 87 GB |
| `swarmrouter-3b-v1/` | SwarmRouter 3B v1 | ~6 GB |

These are cold-stored checkpoints. Active inference models live on local NVMe on each compute node for speed.

## Controller Integration

Registered as `nas` node in swarm-controller with capabilities `["storage", "model-vault"]`. Health-checked via DSM web UI on port 5000.
