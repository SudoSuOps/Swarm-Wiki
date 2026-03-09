# Discord Integration

Two Discord systems: Signal Bridge (automated alerts) and SwarmBot (interactive slash commands).

## Signal Bridge

**File**: `swarmrouter/signal/integrations/discord_bridge.py`
**Channel**: `#swarm-signal`
**Webhook**: `DISCORD_WEBHOOK_URL` (env var in `signal/config.py`)

### What Gets Posted

Only P1-P3 priority signals. P4-P5 are filtered out.

### Rich Embed Format

Each signal posts as a color-coded embed:

| Domain | Color | Emoji |
|--------|-------|-------|
| AI | 0x7C3AED (purple) | robot |
| CRE | 0x059669 (green) | construction |
| Macro | 0xD97706 (amber) | chart |
| Pharma | 0xDC2626 (red) | pill |
| Aviation | 0x2563EB (blue) | airplane |
| General | 0x6B7280 (gray) | globe |

**Embed fields**: Domain, Priority (P1-P3), Confidence %, Source Worker, Signal Type, Body (300 char), Entities (up to 10), URL if available.

**Footer**: `SwarmSignal | YYYY-MM-DD HH:MM UTC`

### Bridge Methods

- `post_signal(signal)` -- Single signal to Discord
- `post_batch(signals)` -- Batch of signals, returns count posted
- `post_summary(stats)` -- Collection summary with worker counts

### Data Flow

```
Signal Workers (11 sources, tiered scheduling)
  -> Entity Scorer + Velocity Tracker
  -> Dedup Store (72-hour window)
  -> Discord Bridge (P1-P3 filter) -> #swarm-signal
```

## SwarmBot

**File**: `swarm-agents/swarmbot.js`
**Framework**: discord.js v14.25.1
**Guild ID**: 1464676140290412616

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `DISCORD_BOT_TOKEN` | Bot authentication |
| `DISCORD_CLIENT_ID` | 1474762559944130650 |
| `DISCORD_GUILD_ID` | 1464676140290412616 |
| `DISCORD_WEBHOOK_URL` | Custom notifications |

### Slash Commands (9)

| Command | Function |
|---------|----------|
| `/sample [specialty]` | Pull free medical QA pairs (10 random or filtered) |
| `/catalog` | Browse live inventory (391K+ pairs, 59 specialties, pricing) |
| `/search <query>` | Search SwarmNet listings |
| `/price <pairs> [specialty]` | Pricing calculator for custom data orders |
| `/hedera` | Live on-chain stats (HBAR balance, SFPAIR/SFMOD NFTs, HCS events) |
| `/status` | Training status, model releases, fleet health |
| `/rfp <company> <email> <need>` | Submit Request for Proposal |
| `/about` | Company info, pricing tiers, HuggingFace links |
| `/setup` | Admin: auto-create S&B Discord channels |

### Auto-Created Channels (via `/setup`)

1. `#lobby` -- Entry point
2. `#announcements` -- Major releases
3. `#sample-pairs` -- Free data sampling
4. `#live-catalog` -- Inventory
5. `#cook-status` -- Training updates
6. `#hedera-proofs` -- On-chain activity
7. `#rfp-desk` -- Proposals
8. `#support` -- Client support
9. `#general` -- Community

### Integrations

- **Live API**: Fetches from `https://swarmandbee.com/api/data/*` (sample, catalog, pricing)
- **Hedera Mirror Node**: Real-time mainnet queries (balance, NFT supply, HCS messages)
- **RFP**: Captures company/email/need -> POST to `/api/rfp` + logs to Discord
- **Welcome DM**: Auto-sends new members quick-start commands

### Branding Colors

| Name | Hex |
|------|-----|
| Gold | 0xB89B3C |
| Green | 0x5A9A6A |
| Blue | 0x4A90D9 |
| Discord Purple | 0x5865F2 |

## Webhook Queue (Inbound)

**File**: `swarmrouter/signal/workers/worker_webhook.py`
**Queue**: `signal/.state/webhook_queue/`

External sources (Zapier, n8n, manual) drop JSON files into the queue. Picked up on next signal collection cycle and posted via Discord Bridge if P1-P3.

```json
{
  "title": "...",
  "body": "...",
  "domain": "cre|pharma|ai|macro|aviation|general",
  "signal_type": "event|news|supply_chain|market_data",
  "priority": 1-5,
  "source": "manual_intelligence|zapier|n8n",
  "url": "...",
  "entities": [{"name": "...", "type": "company|technology|asset_class"}]
}
```
