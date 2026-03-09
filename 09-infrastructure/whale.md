# whale

Secondary training and evaluation rig.

## Hardware

| Component | Spec |
|-----------|------|
| CPU | AMD Ryzen 9 5900X 12C/24T |
| RAM | 64GB DDR4 |
| Storage | Samsung 990 EVO 1TB |
| GPU | RTX 3090 (24GB, Gen4 x16, 65.4 TFLOPS FP16) |
| NIC | Intel X540-AT2 10G (dual-port, not cabled yet) |
| Mobo | B550 Tomahawk |

## Benchmarks

- FP16: 65.4 TFLOPS (92% theoretical)
- H2D: 13.0 GB/s
- RAM STREAM copy: 36.6 GB/s

## Software

- Python 3.12.3
- Unsloth 2026.2.1
- uv 0.10.6

## Models

- SwarmCurator-2B merged at `~/swarmcurator-2b/merged/`
- BeeMini GGUF on port 8081

## Access

```bash
ssh whale  # swarm@192.168.0.99, key auth
```
