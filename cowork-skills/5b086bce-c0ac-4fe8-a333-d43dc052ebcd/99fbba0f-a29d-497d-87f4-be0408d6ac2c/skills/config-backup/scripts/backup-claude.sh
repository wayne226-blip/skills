#!/bin/bash
# ============================================
# Claude Code + Cowork Backup Script
# Works in BOTH Cowork VM and native Mac Terminal
# Generates a README.md with contents + timestamp
# ============================================

# --- DETECT ENVIRONMENT ---
if [[ -d "/sessions" ]] && ls -d /sessions/*/mnt &>/dev/null; then
  MODE="cowork"
  SESSION_DIR=$(ls -d /sessions/*/mnt 2>/dev/null | head -1)
  SESSION_DIR="${SESSION_DIR%/mnt}"
  MNT="$SESSION_DIR/mnt"
  echo "Running in Cowork VM"
else
  MODE="terminal"
  echo "Running on Mac (Terminal)"
fi

# --- SET UP PATHS BASED ON ENVIRONMENT ---
if [ "$MODE" = "cowork" ]; then
  WORKSPACE="$MNT/Claude"
  WORKSPACE_CLAUDE_DIR="$MNT/Claude/.claude"
  HOME_CLAUDE_DIR="$MNT/.claude"
  SKILLS_DIR="$MNT/.skills/skills"
  BACKUP_ROOT="$SESSION_DIR/Library/Mobile Documents/com~apple~CloudDocs/Claude-Backups"
else
  WORKSPACE="$HOME/Claude"
  WORKSPACE_CLAUDE_DIR="$HOME/Claude/.claude"
  HOME_CLAUDE_DIR="$HOME/.claude"
  SKILLS_DIR=""
  BACKUP_ROOT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Claude-Backups"
fi

DATE=$(date +%Y-%m-%d_%H%M)
HUMAN_DATE=$(date "+%A %d %B %Y at %H:%M")
BACKUP_DIR="$BACKUP_ROOT/$DATE"
mkdir -p "$BACKUP_DIR"

echo "Backing up to: $BACKUP_DIR"
echo "================================"

# Track what we back up for the README
FOUND=0
README_TABLE="$BACKUP_DIR/.readme_rows.tmp"
: > "$README_TABLE"

add_item() {
  # $1 = category, $2 = description, $3 = file/folder name in backup
  echo "| $1 | $2 | \`$3\` |" >> "$README_TABLE"
  FOUND=$((FOUND+1))
}

# --- CLAUDE CODE (home-level .claude) ---
if [ -d "$HOME_CLAUDE_DIR/commands" ]; then
  cp -r "$HOME_CLAUDE_DIR/commands" "$BACKUP_DIR/claude-code-commands"
  echo "✓ Claude Code commands"
  CMD_COUNT=$(find "$HOME_CLAUDE_DIR/commands" -type f 2>/dev/null | wc -l | tr -d ' ')
  add_item "Claude Code" "Slash commands ($CMD_COUNT files)" "claude-code-commands/"
else
  echo "- No Claude Code commands found"
fi

if [ -d "$HOME_CLAUDE_DIR/agents" ]; then
  cp -r "$HOME_CLAUDE_DIR/agents" "$BACKUP_DIR/claude-code-agents"
  echo "✓ Claude Code agents"
  AGENT_COUNT=$(find "$HOME_CLAUDE_DIR/agents" -type f 2>/dev/null | wc -l | tr -d ' ')
  add_item "Claude Code" "Agents ($AGENT_COUNT files)" "claude-code-agents/"
else
  echo "- No Claude Code agents found"
fi

if [ -f "$HOME_CLAUDE_DIR/settings.json" ]; then
  cp "$HOME_CLAUDE_DIR/settings.json" "$BACKUP_DIR/claude-code-settings.json"
  echo "✓ Claude Code settings.json"
  add_item "Claude Code" "Global settings" "claude-code-settings.json"
fi

if [ -f "$HOME_CLAUDE_DIR/settings.local.json" ]; then
  cp "$HOME_CLAUDE_DIR/settings.local.json" "$BACKUP_DIR/claude-code-settings-local.json"
  echo "✓ Claude Code settings.local.json"
  add_item "Claude Code" "Local settings" "claude-code-settings-local.json"
fi

# --- WORKSPACE-LEVEL .claude (inside ~/Claude/.claude) ---
if [ -d "$WORKSPACE_CLAUDE_DIR" ] && [ "$WORKSPACE_CLAUDE_DIR" != "$HOME_CLAUDE_DIR" ]; then
  if [ -f "$WORKSPACE_CLAUDE_DIR/settings.local.json" ]; then
    cp "$WORKSPACE_CLAUDE_DIR/settings.local.json" "$BACKUP_DIR/workspace-settings-local.json"
    echo "✓ Workspace .claude/settings.local.json"
    add_item "Workspace Config" "Workspace settings.local.json" "workspace-settings-local.json"
  fi
  if [ -f "$WORKSPACE_CLAUDE_DIR/launch.json" ]; then
    cp "$WORKSPACE_CLAUDE_DIR/launch.json" "$BACKUP_DIR/workspace-launch.json"
    echo "✓ Workspace .claude/launch.json"
    add_item "Workspace Config" "Workspace launch.json" "workspace-launch.json"
  fi
fi

# --- COWORK / PERSONAL SKILLS ---
SKILLS_BACKED_UP=false
if [ -n "$SKILLS_DIR" ] && [ -d "$SKILLS_DIR" ]; then
  cp -r "$SKILLS_DIR" "$BACKUP_DIR/cowork-skills"
  SKILLS_BACKED_UP=true
  SKILL_COUNT=$(find "$SKILLS_DIR" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  SKILL_LIST=$(find "$SKILLS_DIR" -maxdepth 1 -mindepth 1 -type d -exec basename {} \; 2>/dev/null | sort | tr '\n' ', ' | sed 's/,$//')
  echo "✓ Cowork skills ($SKILL_COUNT skills)"
  add_item "Cowork Skills" "$SKILL_COUNT skills: $SKILL_LIST" "cowork-skills/"
else
  # Fallback: native Mac path
  SKILLS_PLUGIN_BASE="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
  if [ -d "$SKILLS_PLUGIN_BASE" ]; then
    FOUND_SKILLS=$(find "$SKILLS_PLUGIN_BASE" -maxdepth 3 -type d -name "skills" 2>/dev/null | head -1)
    if [ -n "$FOUND_SKILLS" ] && [ -d "$FOUND_SKILLS" ]; then
      cp -r "$FOUND_SKILLS" "$BACKUP_DIR/cowork-skills"
      SKILLS_BACKED_UP=true
      SKILL_COUNT=$(find "$FOUND_SKILLS" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
      SKILL_LIST=$(find "$FOUND_SKILLS" -maxdepth 1 -mindepth 1 -type d -exec basename {} \; 2>/dev/null | sort | tr '\n' ', ' | sed 's/,$//')
      echo "✓ Cowork skills ($SKILL_COUNT skills)"
      add_item "Cowork Skills" "$SKILL_COUNT skills: $SKILL_LIST" "cowork-skills/"
    fi
  fi
fi

if [ "$SKILLS_BACKED_UP" = false ]; then
  echo "- No Cowork skills folder found"
fi

# --- WORKSPACE FILES ---
if [ -f "$WORKSPACE/CLAUDE.md" ]; then
  cp "$WORKSPACE/CLAUDE.md" "$BACKUP_DIR/workspace-CLAUDE.md"
  echo "✓ Workspace CLAUDE.md"
  add_item "Workspace" "CLAUDE.md (main config)" "workspace-CLAUDE.md"
fi

if [ -f "$WORKSPACE/ME.md" ]; then
  cp "$WORKSPACE/ME.md" "$BACKUP_DIR/workspace-ME.md"
  echo "✓ Workspace ME.md"
  add_item "Workspace" "ME.md (personal context)" "workspace-ME.md"
fi

# --- PROJECT CLAUDE.md FILES ---
if [ -d "$WORKSPACE/Projects" ]; then
  PROJECT_FILES=$(find "$WORKSPACE/Projects" -name "CLAUDE.md" -type f 2>/dev/null)
  if [ -n "$PROJECT_FILES" ]; then
    mkdir -p "$BACKUP_DIR/project-configs"
    echo "$PROJECT_FILES" | while read f; do
      REL=$(echo "$f" | sed "s|$WORKSPACE/Projects/||" | tr '/' '_')
      cp "$f" "$BACKUP_DIR/project-configs/$REL"
    done
    PROJECT_COUNT=$(echo "$PROJECT_FILES" | wc -l | tr -d ' ')
    PROJECT_NAMES=$(echo "$PROJECT_FILES" | sed "s|$WORKSPACE/Projects/||" | sed 's|/CLAUDE.md||' | tr '\n' ', ' | sed 's/,$//')
    echo "✓ Project CLAUDE.md files ($PROJECT_COUNT projects)"
    add_item "Projects" "$PROJECT_COUNT project configs: $PROJECT_NAMES" "project-configs/"
  fi
fi

# --- SPEC FILES ---
if [ -d "$WORKSPACE/spec" ]; then
  cp -r "$WORKSPACE/spec" "$BACKUP_DIR/specs"
  SPEC_COUNT=$(find "$WORKSPACE/spec" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "✓ Spec files ($SPEC_COUNT files)"
  add_item "Specs" "$SPEC_COUNT spec files" "specs/"
fi

# --- GENERATE README.md ---
README="$BACKUP_DIR/README.md"
{
  echo "# Claude Backup"
  echo ""
  echo "**Date:** $HUMAN_DATE"
  echo "**Environment:** $MODE"
  echo "**Status:** Successful ($FOUND items backed up)"
  echo ""
  echo "---"
  echo ""
  echo "## Contents"
  echo ""
  echo "| Category | What | Backup File |"
  echo "|----------|------|-------------|"
  cat "$README_TABLE"

  echo ""
  echo "---"
  echo ""
  echo "## How to restore"
  echo ""
  echo "Copy any file back to its original location:"
  echo ""
  echo "- \`workspace-CLAUDE.md\` → \`~/Claude/CLAUDE.md\`"
  echo "- \`workspace-ME.md\` → \`~/Claude/ME.md\`"
  echo "- \`workspace-settings-local.json\` → \`~/Claude/.claude/settings.local.json\`"
  echo "- \`claude-code-commands/\` → \`~/.claude/commands/\`"
  echo "- \`claude-code-agents/\` → \`~/.claude/agents/\`"
  echo "- \`claude-code-settings.json\` → \`~/.claude/settings.json\`"
  echo "- \`project-configs/\` → individual \`CLAUDE.md\` files in \`~/Claude/Projects/\`"
  echo "- \`specs/\` → \`~/Claude/spec/\`"
  echo ""

  if [ "$MODE" = "cowork" ]; then
    echo "## Notes"
    echo ""
    echo "- \`~/.claude/commands\` and \`~/.claude/agents\` are not accessible from Cowork."
    echo "- Run this script in Terminal to back those up too."
    echo ""
  fi

  echo "---"
  echo "*Generated by backup-claude.sh*"
} > "$README"

# Clean up temp file
rm -f "$README_TABLE"

echo "================================"

if [ "$FOUND" -eq 0 ]; then
  echo "⚠️  Nothing was backed up."
  rm -f "$README"
  rmdir "$BACKUP_DIR" 2>/dev/null
else
  echo "Done! $FOUND items backed up to: $BACKUP_DIR"
  echo "README.md generated with full contents list."
  echo ""
  echo "Contents:"
  ls -1 "$BACKUP_DIR"
fi

if [ "$MODE" = "cowork" ]; then
  echo ""
  echo "Note: ~/.claude/commands and ~/.claude/agents aren't accessible"
  echo "from Cowork. To back those up too, run this script in Terminal."
fi
