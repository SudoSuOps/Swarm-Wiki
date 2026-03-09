# Skills Discovery

The skills discovery system (`curator/skills.py`) scans for SKILL.md files and makes them available to the curator fleet for LLM context injection. This lets models know what skills exist and how to invoke them.

## 28 Skills

Bootstrapped from the JavaScript skill modules in `worker/src/skills/`. Split across two verticals:

### CRE Skills (19)

| Skill | Description |
|-------|-------------|
| broker_senior | Senior broker analysis and deal strategy |
| broker_junior | Junior broker support tasks |
| intelligence_query | Query Intelligence Objects for market data |
| bookmaker | Deal pricing and valuation |
| deal_tracker | Pipeline and deal status tracking |
| developer | Development feasibility analysis |
| signal_scraper | CRE signal collection and parsing |
| investor | Investment analysis and recommendation |
| exchange_1031 | 1031 exchange structuring and compliance |
| market_report | Market report generation |
| lead_scorer | Lead qualification and scoring |
| email_composer | Professional CRE email drafting |
| comp_analyzer | Comparable sales analysis |
| rent_roll_analyzer | Rent roll parsing and analysis |
| debt_analyzer | Debt structure analysis and refinancing |
| tax_assessor | Property tax assessment and appeal |
| site_selector | Site selection criteria matching |
| portfolio_optimizer | Portfolio-level optimization |
| news_digest | CRE news summarization |

### Medical Skills (9)

| Skill | Description |
|-------|-------------|
| drug_interaction | Drug-drug interaction checking |
| med_reconciliation | Medication list reconciliation |
| dose_calculator | Weight/renal/hepatic dose adjustment |
| anticoag_advisor | Anticoagulation therapy management |
| allergy_check | Allergy and cross-reactivity verification |
| pgx_advisor | Pharmacogenomics-guided prescribing |
| adverse_event | Adverse event detection and reporting |
| pregnancy_safety | Pregnancy/lactation medication safety |
| med_safety | General medication safety assessment |

## SKILL.md Format

Each skill is defined by a SKILL.md file with YAML frontmatter and a markdown body:

```markdown
---
name: comp_analyzer
version: 1.0
vertical: cre
description: Comparable sales analysis for industrial properties
role: analyst
model: swarmcurator-9b
---

## Purpose
Analyze comparable sales to support property valuation...

## Inputs
- Property address or parcel ID
- Asset type and square footage
- Target date range for comps

## Output Format
Structured comp grid with adjustments...
```

The frontmatter provides machine-readable metadata. The markdown body provides the detailed spec that gets injected into LLM context.

## Discovery Functions

### discover_skills()
Scans the `skills/` directory tree for all SKILL.md files. Returns a list of parsed skill objects with frontmatter metadata and body content. Used at fleet startup to populate the available skills registry.

### skills_prompt_section(vertical="cre")
Generates an `<available_skills>` XML block for LLM context injection. Filters by vertical and formats each skill with its name, description, and key parameters. The output is designed to be appended to system prompts so models know what skills they can invoke.

Example output:
```xml
<available_skills vertical="cre">
  <skill name="comp_analyzer" version="1.0">
    Comparable sales analysis for industrial properties
  </skill>
  <skill name="debt_analyzer" version="1.0">
    Debt structure analysis and refinancing
  </skill>
  ...
</available_skills>
```

## CLI

```bash
python3 -m curator skills                          # List all 28 skills
python3 -m curator skills --vertical cre           # List CRE skills only
python3 -m curator skills --vertical medical       # List medical skills only
python3 -m curator skills --bootstrap              # Re-scan and rebuild skill registry
python3 -m curator skills --prompt-section          # Output the XML prompt section
```

## Integration with Middleware

The Strategy middleware (step 4 in the chain) uses `skills_prompt_section()` to inform SwarmCurator-27B about available skills. This allows the 27B model to generate cook orders that reference specific skills, producing training pairs that teach downstream models how to use the skill system.
