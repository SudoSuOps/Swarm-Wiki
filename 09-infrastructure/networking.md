# Networking

## Node Addresses

| Node | IP | SSH | Ports |
|------|----|-----|-------|
| swarmrails | local | `ssh swarmrails` | 8081 (9B), 8082 (27B) |
| whale | 192.168.0.99 | `ssh whale` | 8081 (BeeMini) |
| signal-edge-01 | 192.168.1.95 | `ssh sigedge@192.168.1.95` | — |
| zima-edge-1 | 192.168.0.70 | `ssh dev@192.168.0.70` | 9000 (MinIO), 81 (NPM) |

## 10G NICs

- swarmrails: Intel X710 10G (active)
- whale: Intel X540-AT2 10G dual-port (not cabled yet)

## Cloudflare

- Account: 6abec5e82728df0610a98be9364918e4
- API: router.swarmandbee.com (free tier)
- Metered API: api.router.swarmandbee.com
- Deploy: `cd worker && npx wrangler deploy --remote`
- Logs: `cd worker && npx wrangler tail --remote`

## SSH Key Auth

All nodes use SSH key authentication. No password SSH.
