---
name: update-files
description: >
  Scan the current project and update CLAUDE.md, handoff.md, and related
  documentation to reflect the current state. Fixes stale skill counts,
  bundle statuses, file trees, and command/skill tables. Use after adding
  or removing skills, agents, commands, or changing project structure.
---

# Update Project Files

Scan the current project directory and update all documentation files to reflect reality. This is a housekeeping command — it reads the actual filesystem and fixes any docs that have drifted.

## What to Update

### 1. Project CLAUDE.md

Read `./CLAUDE.md` in the current working directory. Then scan the actual project structure and update:

**Bundle status table:**
- Count skills per bundle: `ls bundles/*/skills/*/SKILL.md` — each directory = one skill
- Count agents per bundle: `ls bundles/*/agents/*.md`
- Count commands per bundle: `ls bundles/*/commands/*.md`
- Update the Skills column with accurate counts (e.g. "8/8 skills complete")
- List skill names in the Status column if they've changed
- Don't change bundle Status text (DONE, READY TO SHIP, etc.) unless the user says to

**Project structure tree:**
- Scan `bundles/` for actual directories and update the tree
- Include bundles that exist on disk but aren't in the tree yet
- Don't remove bundles from the tree that exist in the tree but not on disk — they may be planned

**Commands and skills tables (if present):**
- Cross-reference against actual files in the project's `commands/` and `skills/` directories
- Add any that are on disk but not in the table
- Flag any that are in the table but not on disk

### 2. Global CLAUDE.md (~/Claude/CLAUDE.md)

If the current project is listed in the global CLAUDE.md's Projects table:
- Update the Status column to match the project CLAUDE.md
- Update the Stack column if it's changed

If commands or skills were added to `~/.claude/commands/` or `~/.claude/skills/` during this session:
- Add them to the relevant table in the global CLAUDE.md

### 3. Handoff (./handoff.md)

If `./handoff.md` exists:
- Don't overwrite it — that's for the `/handoff` command
- But flag if it looks stale (last modified date more than a week ago): "handoff.md may be stale — last updated [date]. Run /handoff to refresh?"

### 4. Bundle CLAUDE.md Files

For each bundle that has a `CLAUDE.md`:
- Check the skills table matches actual `skills/*/SKILL.md` files
- Check the file locations table mentions all directories that exist on disk
- Check the agents table matches actual `agents/*.md` files
- Check the commands table matches actual `commands/*.md` files
- Add missing entries, flag entries that reference files that don't exist

### 5. Shared Conventions

For each bundle that has `shared-conventions.md`:
- Don't modify content — these are carefully written
- But flag if a skill references shared-conventions.md but the file doesn't exist

## How to Do It

1. **Scan first, then show the diff.** Don't just make changes — show Wayne what you found and what you'll update.
2. **Group changes by file.** "In CLAUDE.md: updating bundle 2 skill count from 7 to 8, adding test-assistant to project tree."
3. **Ask before writing** if you're unsure about any change. Most updates are obvious (skill counts, missing table entries) and can just be done.
4. **Log what you changed** at the end: brief list of files modified and what changed in each.

## What NOT to Do

- Don't change bundle pricing
- Don't change bundle Status labels (DONE, READY TO SHIP, etc.) without Wayne saying so
- Don't rewrite prose sections — only update structured data (tables, trees, lists)
- Don't touch README.md files — those are buyer-facing and separate
- Don't create CLAUDE.md for bundles that don't have one yet (that's a separate task)
- Don't modify skill SKILL.md files — this command only updates documentation

## Output

After running, summarise:

```
Updated files:
- ./CLAUDE.md — [what changed]
- ~/Claude/CLAUDE.md — [what changed]
- bundles/test-assistant/CLAUDE.md — [what changed]
- ...

Flagged:
- bundles/tradesperson-assistant has no CLAUDE.md (needs writing)
- handoff.md is 12 days old — run /handoff to refresh?
```
