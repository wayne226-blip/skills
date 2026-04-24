# Agent Template

The canonical format for Claude Code agent files. Every generated agent must follow this structure exactly.

---

## File Format

Agent files are markdown with YAML frontmatter. They live in `~/.claude/agents/` and are named `[agent-name].md` using kebab-case.

## Frontmatter Schema

```yaml
---
name: kebab-case-name          # Required. Lowercase with hyphens
description: "Detailed text"   # Required. When/why to use this agent, with trigger examples
tools:                         # Required. Minimal set needed for this agent's job
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  # MCP tools: mcp__[server]__[tool_name]
model: sonnet                  # Optional. opus / sonnet / haiku
color: blue                    # Optional. Visual indicator in UI
memory: user                   # Optional. user / feedback / project / reference
---
```

### Description Writing Guide

The description is the primary mechanism Claude uses to decide when to invoke this agent. Make it specific and include trigger phrases:

**Good:**
```
"Drafts Telegram replies using triage context and research findings. Matches Wayne's communication style. Part of the Telegram multi-agent pipeline."
```

**Better (for standalone agents):**
```
"Use this agent when you need to conduct comprehensive code reviews focusing on code quality, security vulnerabilities, and best practices. Specifically: [examples with user/assistant/commentary format]"
```

For agents that are part of a team (dispatched by an orchestration skill), keep descriptions short and factual — the skill handles the triggering logic.

---

## Body Structure

### Role Declaration (first line after frontmatter)

Always start with a clear role statement:

```markdown
You are a [role description]. Your job is to [primary responsibility].
```

Or for Wayne's personal agents:

```markdown
You are Wayne's [function]. You [core responsibility].
```

### Standard Sections

**Input** — What this agent receives and in what format:

```markdown
## Input

You will receive:
- The original [input type]
- [Context from previous agent] ([what fields to expect])
```

**Process** — Numbered steps the agent follows:

```markdown
## Process

1. [First step]
2. [Second step]
3. [Third step]
```

**Output Format** — Exact template for the agent's output. Use ASCII separators for structure:

```markdown
## Output Format

Return your analysis as structured text:

TITLE IN CAPS
─────────────────
Field 1: [value]
Field 2: [value]
Summary: [1-sentence description]

## Details
[Expanded content]

## Gaps
[What's missing or uncertain]
```

For top-level section dividers, use double lines:
```
═══════════════════════════════════════
MAJOR SECTION
═══════════════════════════════════════
```

For sub-sections, use single lines:
```
───────────────────────────────────────
Sub-section
───────────────────────────────────────
```

**Rules** — Guardrails, constraints, what NOT to do. Always the final section:

```markdown
## Rules

- [Most important constraint]
- [Speed/quality trade-off guidance]
- [Edge case handling]
- [What to do when uncertain]
- British English throughout
```

---

## Model Tier Guide

| Tier | Cost | Speed | Use for |
|------|------|-------|---------|
| **haiku** | Cheapest | Fastest | Routing, classification, triage, simple transformations, formatting. Any agent where speed matters more than depth |
| **sonnet** | Mid | Mid | Reasoning, generation, summarisation, moderate analysis, drafting. Default choice when unsure |
| **opus** | Most expensive | Slowest | Deep analysis, complex judgement, nuanced writing, security review, code review. Use when quality is critical |

**Rule of thumb:** Start with haiku. Move up only if the agent's output quality noticeably suffers.

---

## Tool Selection Guide

Choose the minimum set of tools needed for the agent's specific job.

| Agent role | Typical tools |
|---|---|
| Router / classifier / triage | Read, Grep, Glob |
| Researcher (codebase) | Read, Grep, Glob |
| Researcher (web) | Read, Grep, Glob, WebSearch, WebFetch |
| Builder / generator | Read, Write, Edit, Bash |
| Reviewer / grader (read-only) | Read, Grep, Glob |
| Formatter / drafter | Read (maybe Write if saving output) |
| Coordinator / orchestrator | Read, Bash, Glob |
| MCP-dependent agent | Specific mcp__[server]__[tool] entries |

**Anti-pattern:** Giving an agent tools it doesn't use. A review agent should not have Write/Edit. A router should not have WebSearch. Fewer tools = more focused behaviour.

---

## Conventions

- **British English** throughout all agent files
- **Kebab-case** for agent names (e.g. `content-classifier`, `quality-grader`)
- **Concise rules** — each rule is one line, no paragraphs
- **Output under 500 words** for agents in a pipeline (keeps context manageable for the next agent)
- **No hardcoded paths** to user data — use descriptions like "the standard Obsidian vault location" or pass paths via the prompt
