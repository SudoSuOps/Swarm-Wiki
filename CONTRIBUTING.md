# Contributing to SwarmWiki

## File Naming

- Lowercase with hyphens: `training-patterns.md`, `cre-skills.md`
- Each section directory has a `README.md` as index page

## Cross-References

Use relative paths:
```markdown
See [SwarmCurator-27B](../02-models/swarmcurator-27b.md)
See [Quality Gates](../04-datasets/quality-gates.md)
```

## Adding a New Model

1. Create `02-models/model-name.md`
2. Update the fleet roster table in `02-models/README.md`
3. Add training script reference in `03-scripts/train-scripts.md`
4. Add dataset reference in `04-datasets/README.md`
5. Update `README.md` dashboard count

## Updating Pair Counts

1. Update the R2 bucket table in `04-datasets/r2-buckets.md`
2. Update the grand total in `04-datasets/README.md`
3. Update the dashboard in root `README.md`
4. Add "Last updated: YYYY-MM-DD" to changed tables

## Adding a New Skill

1. Add to the appropriate skills table in `07-skills/`
2. Update the count in root `README.md` dashboard
3. Add SKILL.md spec in the repo's `skills/` directory

## Volatile Data

Mark frequently-changing numbers with timestamps:
```markdown
*Last updated: 2026-03-09*
```

Volatile items: pair counts, model status, GPU assignments, loss values.

## No Secrets

Never include actual API keys, passwords, or private keys. Reference patterns:
- "Together.ai key in `.env`"
- "sudo password stored separately"
- "Hedera keys in hedera-swarmfoundry/.env"
