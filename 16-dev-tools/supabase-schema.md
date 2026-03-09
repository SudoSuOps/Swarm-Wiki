# Supabase Database Schema

**Project URL**: `https://gizwfmgowyfadmvjjitb.supabase.co`

## Tables (13)

### Event Machine (5 tables)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `events` | 22 event types (deal, supply, ownership, macro, tenant) | `id` UUID, `object_id`, `event_type`, `category`, `source`, `ticker`, `state`, `market`, `confidence`, `priority`, `price`, `cap_rate`, `sf`, `data_json`, `processed`, `created_at` |
| `entities` | Named entities (REITs, properties, investors, tenants, brokers) | `id` UUID, `entity_type`, `name`, `normalized_name`, `ticker`, `state`, `address`, `metadata_json`, `event_count`, `last_seen`, `created_at` |
| `event_entities` | Junction table (many-to-many event-entity with roles) | `event_id` FK, `entity_id` FK, `role`, `created_at` |
| `market_snapshots` | Market state at point in time | `id` UUID, `state`, `market`, `asset_type`, `vacancy_rate`, `avg_cap_rate`, `avg_rent_psf`, `deal_count`, `snapshot_json`, `period`, `created_at` |
| `memory_index` | pgvector embeddings (768-dim BGE-Base-1.5) for semantic search | `id` UUID, `object_id`, `object_type`, `r2_key`, `summary`, `state`, `asset_type`, `embedding` vector(768), `created_at` |

### Factory Pipeline (5 tables)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `cooked_pairs` | Training pairs from factory | `id` serial, `cook_name`, `cook_run_id`, `domain`, `pair_data` JSON, `fingerprint` MD5, `specialty`, `tier`, `vertical`, `r2_synced` bool, `created_at` |
| `cook_runs` | Cook job metadata | `id` UUID, `name`, `domain`, `cook_type`, `status` (running/completed/failed/cancelled), `gen_model`, `gen_model_provider`, `pass_model`, `output_count`, `pass_count`, `r2_verified`, `started_at`, `completed_at`, `notes`, `created_at` |
| `dataset_versions` | Finalized dataset snapshots | `id` UUID, `name`, `domain`, `record_count`, `r2_bucket`, `r2_prefix`, `notes`, `created_at` |
| `training_runs` | Model fine-tuning jobs | `id` UUID, `model_name`, `base_model`, `status`, `current_step`, `total_steps`, `loss_curve` JSON array, `final_loss`, `started_at`, `completed_at`, `created_at` |

### Project Management (3 tables)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `projects` | Master project registry | `id` serial, `project_id` TEXT UNIQUE (e.g. `PRJ-001-SWARMROUTER`), `project_name`, `status`, `phase`, `description`, `phases` JSONB, `deliverables` JSONB, `model_lineup` JSONB, `infrastructure` JSONB, `created_at` |
| `build_phases` | Phase tracking within projects | `id` serial, `project_id` FK, `phase_id` TEXT UNIQUE, `phase_name`, `phase_number`, `status`, `build_id` FK, `acceptance_results` JSONB, `created_at` |
| `model_builds` | Sealed, versioned training datasets | `id` serial, `build_id` TEXT UNIQUE, `model_name`, `version`, `sealed_at`, `train_pairs`, `eval_pairs`, `sha256_train`, `sha256_eval`, `manifest` JSONB, `domain_dist`, `model_dist`, `status`, `r2_bucket`, `r2_prefix`, `created_at` |

## RPC Functions (10)

| RPC | Purpose | Auth |
|-----|---------|------|
| `match_memory` | Semantic vector search (cosine similarity) | Anon |
| `get_event_stats` | Summary stats on events table | Anon |
| `get_memory_stats` | Summary stats on memory_index | Anon |
| `get_feedback_stats` | Summary stats on feedback | Anon |
| `get_router_stats` | Summary stats on router decisions | Anon |
| `update_training_progress` | Update training_runs with step/loss | SECURITY DEFINER |
| `get_factory_dashboard` | Summary of cook_runs + training_runs + datasets | SECURITY DEFINER |
| `exec_sql` | Execute arbitrary SQL (used by log_cook.py) | Service Role only |

### match_memory Parameters

```sql
query_embedding  JSON vector (768-dim)
match_threshold  float (cosine similarity cutoff)
match_count      int (max results)
```

Returns: `{id, similarity, object_id, object_type, state, asset_type, summary, r2_key}`

## Row-Level Security

| Tables | Policy |
|--------|--------|
| `model_builds`, `projects`, `build_phases` | SECURITY DEFINER — service_role only |
| `events`, `entities`, `memory_index` | Public read (no explicit RLS) |
| `cooked_pairs`, `cook_runs`, `training_runs` | Public read for analytics |

## Indexes

| Table | Index |
|-------|-------|
| `model_builds` | `idx_model_builds_model_name(model_name)`, `idx_model_builds_status(status)` |
| `projects` | `idx_projects_status(status)` |
| `build_phases` | `idx_build_phases_project(project_id)`, `idx_build_phases_status(status)` |
| `memory_index` | pgvector HNSW (768-dim cosine) on `embedding` column |

## Data Flow

### Training Pair Pipeline

```
R2 bucket (sb-medical, sb-cre, etc.)
  ↓ backfill_r2_to_supabase.py
cooked_pairs table (inserts every 100 pairs, R2 shards every 500)
  → dedup_cooked_pairs.py (cleanup by question hash)
  → factory.cook.py (logs to cook_runs)
  → dataset_versions (finalized snapshots)
```

### Training Run Monitoring

```
Training log (swarmrails/whale)
  ↓ train_monitor.py (SSH fetch, parse loss)
  ↓ update_training_progress RPC (SECURITY DEFINER)
training_runs table (step, loss_curve updates)
```

### Event Machine

```
External sources (EDGAR, RSS)
  → worker/src/event_machine.js
  → events table (insertEvent)
  → Entity extraction → entities table (upsertEntity)
  → event_entities junction
  → memory.js: embedAndStore → memory_index (pgvector)
```

## Codebase Locations

| Component | Path |
|-----------|------|
| Worker DB layer | `swarmrouter/worker/src/db.js` |
| Worker memory/pgvector | `swarmrouter/worker/src/memory.js` |
| Worker Supabase client | `swarmrouter/worker/src/supabase.js` |
| Backfill R2→Supabase | `swarmrouter/data/factory/backfill_r2_to_supabase.py` |
| Dedup pairs | `swarmrouter/data/factory/dedup_cooked_pairs.py` |
| SafeStore 3-tier | `swarmrouter/data/factory/safestore.py` |
| Training monitor | `swarmrouter/data/factory/train_monitor.py` |
| Cook logger | `swarmrouter/data/log_cook.py` |
| Migrations | `swarmrouter/data/router_v3/migrations/` |
| Config | `swarmrouter/data/factory/config.py` |
| swarmandbee.com SSR | `swarmandbee.com/src/lib/supabase/{server,client}.ts` |
