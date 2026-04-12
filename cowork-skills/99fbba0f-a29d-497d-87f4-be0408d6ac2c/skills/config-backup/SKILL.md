---
name: config-backup
description: >
  Backs up Claude Code and Cowork configuration to iCloud. Covers slash commands, agents, settings, Cowork skills, CLAUDE.md, ME.md, project configs, and spec files. Each backup generates a README.md with date, status, and full contents list. Trigger when Wayne says "back up", "backup", "save my config", "backup my stuff", "backup claude", or asks to back up his Claude Code or Cowork setup. Also trigger if he asks what's been backed up or wants to restore from a backup.
---

# Backup Claude Skill

Runs a backup of Wayne's Claude Code and Cowork configuration files to iCloud Drive.

## What gets backed up

| What | Source |
|------|--------|
| Claude Code slash commands | `~/.claude/commands/` |
| Claude Code agents | `~/.claude/agents/` |
| Claude Code settings | `~/.claude/settings.json` + `settings.local.json` |
| Workspace .claude config | `~/Claude/.claude/settings.local.json` + `launch.json` |
| Cowork installed skills | All skills from the mounted skills directory |
| Workspace CLAUDE.md | `~/Claude/CLAUDE.md` |
| Workspace ME.md | `~/Claude/ME.md` |
| Project CLAUDE.md files | `~/Claude/Projects/**/CLAUDE.md` |
| Spec files | `~/Claude/spec/` |

## Where backups go

`iCloud Drive/Claude-Backups/<timestamp>/`

Each run creates a new timestamped folder so nothing gets overwritten. Every backup includes a `README.md` with the date, status, and a full table of what was backed up.

## How to run

**From Cowork:** Find and run the bundled script dynamically:

```bash
SCRIPT=$(find /sessions -path "*/config-backup/scripts/backup-claude.sh" 2>/dev/null | head -1)
bash "$SCRIPT"
```

**From Terminal:** Wayne has a copy in his workspace:

```bash
bash ~/Claude/scripts/backup-claude.sh
```

The script auto-detects whether it's running in Cowork or Terminal and adjusts paths accordingly.

**In Cowork:** Backs up everything accessible via mounted folders. Commands and agents from `~/.claude/` aren't reachable — the script notes this and suggests running in Terminal for a full backup.

**In Terminal:** Backs up everything including `~/.claude/commands` and `~/.claude/agents`.

The script prints a checklist of what it found and backed up, and generates a README.md inside the backup folder. Share the output with Wayne so he can see what was captured.

## If Wayne asks what's been backed up

List the contents of the backup directory:

```bash
ls -lt ~/Library/Mobile\ Documents/com~apple~CloudDocs/Claude-Backups/
```

Show the most recent backup and read its README.md for a summary.

## If Wayne asks to restore

Backups are plain copies of the original files. To restore, copy files back from the backup folder to their original locations. The README.md in each backup lists where each file should go. Walk Wayne through which files he wants to restore — don't blindly overwrite current configs without confirming.
