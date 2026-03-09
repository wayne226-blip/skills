# Push

Push all repos to GitHub.

## Instructions

Run a GitHub push for Wayne's three repos. For each repo, stage any changes, commit with today's date, and push. Skip silently if nothing has changed.

### Repos

1. `/Users/wayne/Claude/Projects/SALES NOTE AI/`
2. `/Users/wayne/Claude/Projects/KDP-Super-Swarm-Book-Creator/`
3. Skills repo at `/tmp/skills-repo` (remote: `https://github.com/wayne226-blip/skills.git` — auth token is stored in the `daily-github-push` scheduled task SKILL.md)

### Skills repo steps
- Pull latest from remote first
- Copy fresh files:
  - `~/.claude/agents/*.md` → `agents/`
  - `~/.claude/commands/*.md` → `commands/`
  - `~/.claude/skills/*/SKILL.md` → `skills/*/SKILL.md` (skip `*-workspace` dirs)
- Then commit and push any changes

### All repos
- Commit message: `Daily backup — [TODAY'S DATE]`
- Use Bash tool for all git operations
- Report a table: Repo | Result (pushed N files / no changes)
