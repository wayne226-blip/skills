---
name: obsidian-vault
description: >
  The Vault Master — manages Wayne's Obsidian vault. Handles reading, searching,
  creating and editing notes, syncing project statuses from CLAUDE.md, running
  vault health checks, and maintaining the Vault Index. Use this skill whenever
  the user mentions Obsidian, their vault, their notes, or asks to find, read,
  create, or edit any note or markdown file in their knowledge base. Trigger even
  for casual mentions like "check my notes on X", "add this to my vault",
  "what do I have on Y in Obsidian", "open my Obsidian folder", "sync the vault",
  "vault health", or "update the vault". ALWAYS trigger immediately when the user
  types /vault at the start of their message — this is a direct command shortcut
  for this skill. Also trigger when the user says "update the vault", "sync the
  vault", "vault needs updating", "give the vault a once over", or any variation
  of wanting vault maintenance done.
---

# Vault Master

> The Vault Master keeps Wayne's Obsidian vault in sync with reality.

## Vault Location

Wayne's Obsidian vault is at:

```
/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza
```

In Cowork sessions, this will be mounted — check for it at paths like:

```
/sessions/*/mnt/Documents/wauzza
```

If the vault folder isn't mounted yet, use `request_cowork_directory` to ask the user to mount it. The host path is `/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents`.

---

## /vault Command

When Wayne types `/vault` followed by anything, treat everything after `/vault` as the task. Examples:

- `/vault list all notes` → list `.md` files
- `/vault find notes about Python` → search note contents
- `/vault create a note called Meeting Notes` → create a new note
- `/vault show my latest note` → most recently modified note
- `/vault sync` → run a full vault sync
- `/vault health` → run a vault health check

---

## Core Capabilities

### 1. Find and Read Notes

Wayne will often ask things like "what do I have on X" or "find my notes about Y". Search strategies:

```bash
VAULT="<mounted-vault-path>"

# Search by keyword across all notes
grep -rl "keyword" "$VAULT" --include="*.md"

# Find by approximate filename
find "$VAULT" -iname "*keyword*"

# Most recently modified notes
find "$VAULT" -name "*.md" -not -path '*/.obsidian*' \
  -exec stat --format="%Y %n" {} \; | sort -rn | head -10
```

Use the `Read` tool for full note contents. Always quote paths — folder names have spaces (e.g. `Learning AI`, `Apple Notes`).

### 2. Create and Edit Notes

**Creating:** Use the `Write` tool. Place notes in the right folder based on content:

| Content type | Folder |
|---|---|
| Quick capture, unsorted | `Inbox/` |
| Daily journal | `Daily/` (format: `YYYY-MM-DD.md`) |
| About Wayne, goals, routines | `Personal/` |
| Brand, marketing, stack | `Work/` |
| Project notes | `Projects/` or `Projects/KDP/` |
| Tasks and to-dos | `Tasks/` |
| AI learning notes | `Learning AI/` |
| NotebookLM study notes | `NotebookLM/` |
| Reference material, guides | `Reference/` |
| Research reports | `Research/` |
| Written drafts | `Writing/` |

**Editing:** Always `Read` the note first so you don't overwrite existing content. Use `Edit` for targeted changes.

**Internal links:** Use `[[Note Name]]` syntax — these are just references to other files in the vault. Preserve them when editing.

### 3. Vault Sync

Trigger: "sync the vault", "update the vault", "vault needs updating"

This compares the source of truth (Wayne's `CLAUDE.md` and project files) against what's in the vault, and updates anything that's drifted.

**Steps:**

1. Read Wayne's main `CLAUDE.md` (in the Claude folder, not the vault copy) for current project statuses, book pipeline, commands list
2. Compare against these vault notes:
   - `Projects/Projects.md` — project list and statuses
   - `Projects/KDP/KDP Book Status.md` — per-book pipeline progress
   - `Reference/Claude Skills & Tools Reference.md` — commands and agents
3. List every proposed change and show Wayne before writing anything
4. Only apply updates after Wayne confirms
5. Set `Last updated:` to today's date on every changed note
6. After structural changes, offer to update `Vault Index.md` (file counts, note listings, date)

### 4. Vault Health Check

Trigger: "vault health", "check the vault", "give it a once over"

Run diagnostics and report findings — don't fix anything without asking.

**Checks to run:**

1. Total note count and notes per folder
2. 10 most recently modified notes
3. Empty folders (might be fine, might need tidying)
4. Vault Index accuracy — do the file counts and note listings match reality?
5. Broken `[[internal links]]` — links pointing to notes that don't exist
6. Orphaned notes — notes that exist but aren't linked from any index
7. Stale notes — notes with `Last updated:` dates more than 30 days old

Report findings clearly. Suggest fixes but wait for confirmation.

### 5. Vault Index Updates

The `Vault Index.md` is the master index of the vault. After any structural change (new note, moved note, deleted note, folder change):

1. Update file counts in the Structure Overview table
2. Add or remove note links in the appropriate section
3. Update the `Last updated:` date

Always offer to do this after making changes — don't do it silently.

---

## Rules — Always Follow These

These rules exist because Wayne's vault contains personal data and an archive of imported notes that shouldn't be touched by automated processes.

1. **Never delete vault content** unless Wayne explicitly asks
2. **Never touch the IPTV folder** (`Reference/IPTV/`) — it's a personal reference, not part of project syncing
3. **Never touch the Apple Notes archive** (`Archive/Apple Notes/`) — these are imported legacy notes, leave them alone
4. **Always show proposed changes before writing** — list every edit and wait for confirmation
5. **Suggest new notes** rather than creating them without asking
6. **Preserve Obsidian syntax** — keep `[[internal links]]`, callout blocks (`> [!type]`), frontmatter, and checkbox formatting intact
7. **Quote paths properly** — vault folders have spaces in their names

---

## Vault Structure Reference

```
wauzza/
├── Inbox/              — Quick capture
├── Daily/              — Daily notes (YYYY-MM-DD.md)
├── Personal/           — About Wayne, goals, CV
├── Work/               — Brand, marketing, stack
├── Projects/           — Active projects
│   ├── KDP/            — KDP book pipeline
│   └── SalesNote/      — SalesNote AI
├── Tasks/              — Action items
├── Learning AI/        — AI learning journey
├── NotebookLM/         — Study notes from notebooks
├── Reference/          — Guides, tools, clippings
│   └── IPTV/           — DO NOT TOUCH
├── Research/           — Research reports
├── Writing/            — Drafts
├── Templates/          — Note templates
├── Tags/               — Tag index pages
├── Archive/            — DO NOT TOUCH (~265 Apple Notes)
├── _attachments/       — PDFs, images
├── CLAUDE.md           — Vault-level Claude instructions
├── Vault Master.md     — Agent description note
└── Vault Index.md      — Master index of all notes
```

---

## Tips

- Wayne uses voice-to-text, so expect typos in requests — figure out what he means rather than asking for clarification
- Obsidian notes are plain `.md` files — read and write them directly with standard tools
- Callout blocks use `> [!type] Title` followed by `> content` — preserve this formatting
- If you need the vault mounted and it isn't, use `request_cowork_directory` to ask
- When creating task notes, use the checkbox format: `- [ ] Task` and `- [x] Done`
