# Swarm Skills Framework

35 total skills across three verticals, deployed on router.swarmandbee.com as a Cloudflare Worker.

## Skill Counts

| Vertical | Count | Location |
|----------|-------|----------|
| CRE | 19 | `worker/src/skills/` + `skills/cre/` |
| Medical | 9 | `worker/src/skills/` + `skills/medical/` |
| Capital Markets | 7 | `swarm-capital-markets` repo |
| **Total** | **35** | |

## Skill Anatomy

Each skill consists of:

| File | Purpose |
|------|---------|
| `SKILL.md` | Spec file -- YAML frontmatter + markdown body, LLM-injectable |
| `*.js` | JavaScript implementation (Cloudflare Worker) |
| `validator.js` | Input/output validation (optional) |
| `schema.json` | JSON Schema for inputs and outputs (optional) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/skill/{name}` | POST | Execute a skill |
| `/skills` | GET | List all available skills |
| `/skill/{name}/spec` | GET | Return the SKILL.md spec |
| `/skill/{name}/mock` | GET | Return mock output for testing |
| `/skill/{name}/test` | GET | Run built-in test suite |
| `/skill/{name}/eval` | GET | Run evaluation against reference outputs |
| `/skill/{name}/fail` | GET | Return example failure modes |

## Edge Model

- **Primary**: `@cf/qwen/qwen3-30b-a3b-fp8` (Cloudflare Workers AI)
- **Fallback**: `@cf/meta/llama-3.2-3b-instruct`
- **Cost**: ~$0.00004 per skill call

## Skill Discovery (Python)

The `curator/skills.py` module provides programmatic skill discovery:

```python
from curator.skills import discover_skills, skills_prompt_section

# List all skills
skills = discover_skills()

# Generate LLM context for CRE skills
prompt = skills_prompt_section(vertical="cre")
```

`discover_skills()` scans the repository for `SKILL.md` files and parses their YAML frontmatter. `skills_prompt_section()` renders a formatted block suitable for injection into LLM system prompts.

## Section Index

- [CRE Skills](cre-skills.md) -- 19 commercial real estate skills
- [Medical Skills](medical-skills.md) -- 9 pharmaceutical/clinical skills
- [Capital Markets Skills](capital-markets-skills.md) -- 7 debt/equity transaction skills
- [Skill Spec Format](skill-spec-format.md) -- SKILL.md authoring guide
