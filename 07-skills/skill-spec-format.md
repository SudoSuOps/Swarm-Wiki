# SKILL.md Spec Format

Every skill is defined by a `SKILL.md` file that combines YAML frontmatter with a markdown body. This format is designed to be both human-readable documentation and machine-parseable LLM context.

## Format

```markdown
---
name: skill_name
version: "1.0"
vertical: cre | medical | capital_markets
description: One-line description of what the skill does
role: Analyst role name (e.g., "Senior CRE Broker", "Clinical Pharmacist")
model: edge-30b
---

# Skill Title

## Process
Step-by-step description of how the skill operates.

## Examples
Input/output examples showing expected behavior.

## Constraints
Hard rules the skill must follow (e.g., regulatory, mathematical, safety).

## Output Format
Description of the structured output schema.
```

## Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Snake_case skill identifier, unique within vertical |
| `version` | Yes | string | Semver version (quoted to prevent YAML number parsing) |
| `vertical` | Yes | enum | `cre`, `medical`, or `capital_markets` |
| `description` | Yes | string | One-line human-readable description |
| `role` | Yes | string | The analyst persona the LLM should adopt |
| `model` | No | string | Target model tier (default: `edge-30b`) |

## Discovery: curator/skills.py

The Python skill discovery system scans the repository for `SKILL.md` files and makes them available programmatically.

### discover_skills()

Walks the `skills/` directory tree, finds all `SKILL.md` files, parses YAML frontmatter, and returns a list of skill metadata dictionaries.

```python
from curator.skills import discover_skills

skills = discover_skills()
# Returns: [
#   {"name": "comp_analyzer", "vertical": "cre", "version": "1.0", ...},
#   {"name": "drug_interaction", "vertical": "medical", "version": "1.0", ...},
#   ...
# ]
```

### skills_prompt_section(vertical)

Generates a formatted text block for injection into LLM system prompts. This gives the model awareness of available skills and their capabilities.

```python
from curator.skills import skills_prompt_section

# Get CRE skills context for LLM
cre_context = skills_prompt_section(vertical="cre")
# Returns formatted markdown listing all 19 CRE skills with descriptions

# Get medical skills context
med_context = skills_prompt_section(vertical="medical")
```

The output is designed to be concatenated directly into a system prompt:

```python
system_prompt = f"""You are a CRE intelligence analyst.

{skills_prompt_section(vertical="cre")}

Use the above skills when appropriate to answer the user's question.
"""
```

## Directory Structure

```
skills/
  cre/
    broker_senior/
      SKILL.md
    broker_junior/
      SKILL.md
    comp_analyzer/
      SKILL.md
    ...
  medical/
    drug_interaction/
      SKILL.md
    dose_calculator/
      SKILL.md
    ...
  capital_markets/      (in swarm-capital-markets repo)
    deal_packet/
      SKILL.md
      schema.json
    underwrite/
      SKILL.md
      schema.json
      validator.js
    ...
```

## Authoring Guidelines

1. **name** must be unique within its vertical and match the directory name
2. **description** should be actionable -- start with a verb (e.g., "Calculate", "Analyze", "Generate")
3. **role** should describe the human expert this skill emulates
4. **Process** section should list concrete steps, not vague descriptions
5. **Constraints** section must include any hard rules (regulatory limits, mathematical bounds, safety guardrails)
6. **Examples** should include at least one happy path and one edge case
7. Keep the total SKILL.md under 2,000 tokens -- it gets injected into LLM context windows

## JS Implementation Pairing

Each `SKILL.md` has a corresponding JS implementation in `worker/src/skills/`. The JS module handles HTTP routing, input parsing, model invocation, and response formatting. The SKILL.md provides the LLM with domain knowledge and behavioral constraints.

```
SKILL.md     → What the skill knows and how it should behave
*.js         → How the skill is invoked and what it returns
schema.json  → Input/output validation contract
validator.js → Runtime constraint enforcement
```
