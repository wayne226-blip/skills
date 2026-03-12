# CLAUDE.md

## Repository Overview

This is a **Claude Code skills, agents, and commands library** — a collection of reusable AI configurations organized into three categories: skills (complex workflows with supporting scripts/resources), agents (specialized AI personas), and commands (lightweight slash-command workflows). The repository is actively maintained as a personal configuration backup.

## Directory Structure

```
skills/                         # Repository root
├── agents/                     # 8 agent configuration files (.md)
├── commands/                   # 17 command definitions (.md)
├── cowork-skills/              # 30 extended skill directories
│   ├── docx/, docx-pro/        #   Word document generation
│   ├── pptx/, pptx-pro/        #   PowerPoint creation
│   ├── pdf/, pdf-pro/           #   PDF generation
│   ├── xlsx/, xlsx-pro/         #   Excel spreadsheet creation
│   ├── canvas-design/           #   Canvas drawing (100+ fonts)
│   ├── csv-dashboard/           #   CSV to dashboard conversion
│   ├── mcp-builder/             #   MCP skill builder
│   ├── skill-creator/           #   Meta-skill for creating skills
│   └── ...                      #   (and 21 more)
├── skills/                     # 6 core/stable skill directories
│   ├── cv-builder/
│   ├── excalidraw-diagram/
│   ├── handoff/
│   ├── notebooklm/
│   ├── playwright-cli/
│   └── prompt-guide/           #   Includes evals/evals.json
├── *-SKILL.md                  # 3 standalone skill definitions
├── index.md                    # Repository index and navigation
├── skill.md                    # Framework documentation
└── readme                      # Minimal readme
```

## Key Conventions

### File Naming

| Type | Location | Naming |
|------|----------|--------|
| Skill (directory) | `skills/` or `cowork-skills/` | `{name}/SKILL.md` |
| Skill (standalone) | Root | `{name}-SKILL.md` |
| Agent | `agents/` | `{name}.md` |
| Command | `commands/` | `{name}.md` |
| Scripts | Inside skill dirs | `scripts/{purpose}.py` |

### YAML Frontmatter (Required on All Definitions)

Every skill, agent, and command uses YAML frontmatter:

```yaml
---
name: skill-name
description: >
  Use this skill when [trigger conditions].
  Trigger on phrases like "[example phrases]".
  [Description of what it does]
---
```

**Agents** additionally include: `tools:` (list), `model:` (claude model tier)
**Commands** additionally include: `argument-hint:`, `allowed-tools:` (list)

### Skill Structure Pattern

A directory-based skill typically contains:
- `SKILL.md` — Main definition with workflow steps, rules, and examples
- `scripts/` — Python implementation files (e.g., `csv_to_dashboard.py`)
- Supporting resources (fonts, schemas, templates, reference docs)

### Description Conventions

Skill/agent descriptions should include:
- **Trigger conditions**: "Use this skill when..." or "Trigger on phrases like..."
- **Examples with commentary**: Real-world usage scenarios
- **Step-by-step workflows**: Numbered procedures
- **Quality rules**: Constraints and edge case handling

## Common Dependencies

Python libraries used across skills (documented inline, no central requirements file):
- `python-docx` — Word documents
- `reportlab`, `weasyprint` — PDF generation
- `pandas` — Data processing
- `requests` — API calls
- External tools: Pandoc (document conversion)

## No Build System

- No `package.json`, `requirements.txt`, `Makefile`, or CI/CD pipelines
- Dependencies are documented within individual `SKILL.md` files
- No test runner — the only evals are in `skills/prompt-guide/evals/evals.json`

## Development Workflow

1. **Adding a new skill**: Create a directory under `skills/` or `cowork-skills/` with a `SKILL.md` file. Follow the frontmatter and description conventions above. Add supporting `scripts/` as needed.
2. **Adding a new agent**: Create a `.md` file in `agents/` with name, description, tools, and model in frontmatter.
3. **Adding a new command**: Create a `.md` file in `commands/` with name, description, and allowed-tools in frontmatter.
4. **Updating the index**: After adding new items, update `index.md` to include links.

## Key Reference Files

- `skill.md` — Framework documentation explaining what skills are and how to design them
- `index.md` — Full table of contents with links to all agents, commands, and skills
- `json-image-gen-templates.md` — Template reference for the image generation skill
