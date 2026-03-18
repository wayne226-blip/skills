# Claude Code Onboarding Skill — Tasks

Current score: 8.5/10. These tasks close the gaps to 10/10.

---

## Priority 1 — High Impact

- [ ] **Add version tracking** — Add a `VERSION` file to each package (e.g. `1.0.0`) and a `version` field in CLAUDE.md. Install script should print the version. Update script can compare versions to show what changed.
- [ ] **Add update/upgrade path** — New Step 12: "Update Existing Client". Reads current installed brain, diffs against new package, copies only changed files. Lets Wayne add a skill 3 months later without regenerating everything.
- [ ] **Add uninstall script** — `uninstall.sh` + `uninstall.bat` that cleanly removes all installed skills, agents, commands, and brain files. Should list what it will delete and ask for confirmation before acting.

## Priority 2 — Quality

- [ ] **Build eval set for autoresearch** — Create 5-8 eval prompts in `~/Claude/autoresearch/eval-sets/claude-code-onboarding/` so the skill description can be optimised overnight. Need trigger phrases + expected outputs.
- [ ] **Add Cowork skill generation** — Currently only generates Claude Code skills (`~/.claude/skills/`). Add option to also output Cowork-format skills for `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/`.

## Priority 3 — Nice to Have

- [ ] **Add backup before install** — Install script should back up any existing `~/.claude/skills/`, agents, commands before overwriting, so nothing gets lost if client already has their own setup.
- [ ] **Add dry-run mode** — `bash install.sh --dry-run` shows what would be copied without actually doing it. Useful for Wayne to demo to clients.
- [ ] **Add changelog generation** — When updating a client brain, auto-generate a `CHANGELOG.md` showing what changed between versions.

## Add-On — Scheduled Tasks (upsell for Business/Pro clients)

- [ ] **Weekly content calendar task** — Scheduled task that runs every Monday morning, reads PLAN.md + TASKS.md, and generates a week's worth of content ideas (social posts, emails, blog topics) based on the client's current goals. Outputs to a `content-calendar.md` in their project folder. Could be offered as a Business/Pro add-on.
- [ ] **Monthly brain health check task** — Scheduled task that runs 1st of each month, checks if PLAN.md and TASKS.md are stale (not updated in 2+ weeks), reviews if brand voice has drifted in recent outputs, and sends Wayne a summary so he can proactively reach out to the client. Good retention tool.

---

Last updated: 2026-03-16
