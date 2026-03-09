---
name: handoff
description:
  Create a structured session handoff document for continuity across sessions.
  Use when ending a work session, switching contexts, or before a break.
  Captures decisions, progress, file changes, and next steps so a future session
  can pick up exactly where you left off. Especially useful mid-KDP pipeline run.
---

# Session Handoff Skill

Create a structured document that enables seamless continuity across Claude sessions —
particularly useful when pausing mid-pipeline on a KDP book or any multi-step project.

## When to Use

- Ending a work session
- Pausing mid-KDP pipeline run (e.g. between agents)
- Before switching to a different project
- When context is about to reset and you want to preserve state

## Handoff Process

### Step 1: Assess Session State

Quickly assess:

1. **What project?** (which book slug, or which project folder)
2. **What pipeline stage are we at?** (which agent last ran, what's next)
3. **How far along?** (just started, mid-way, almost done)

### Step 2: Ask What Matters

Ask the user:

> "I'll create a handoff doc. Anything specific to capture — decisions made, blockers, things you'll forget?"

### Step 3: Generate Handoff Document

Save the handoff as `handoff.md` in the current project folder (or `~/Claude/handoff.md` if no project context), then display it.

```markdown
# Session Handoff: [Brief Description]

**Date:** [YYYY-MM-DD]
**Project:** [project name / book slug]
**Session Duration:** [approximate]

## Current State

**Task:** [What we're working on]
**Pipeline Stage:** [last agent completed → next agent to run]
**Progress:** [percentage or milestone]

## What We Did This Session

[2–3 sentence summary]

## Decisions Made

- **[Decision]** — [Rationale]

## Files Changed

- `path/to/file` — [what and why]

## Key Context to Remember

[Important background, constraints, current book character names, illustration style,
anything that would take time to re-establish]

## Open Questions / Blockers

- [ ] [Issue or question needing resolution]

## Next Steps

1. [ ] [First thing to do next session]
2. [ ] [Second thing]
3. [ ] [Third thing]

## Files to Review on Resume

- `path/to/file` — [why it matters]
```

After saving, tell the user:
> "Handoff saved. Next session, open this file or paste it in and say 'resume from handoff' to pick up where we left off."
