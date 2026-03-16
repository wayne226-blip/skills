---
name: claude-code-onboarding
description: >
  Generate a complete Claude Code / Cowork AI Brain for a small business client.
  Takes discovery call intake data and produces a full output package saved to
  /client-brains/[name]/: 6 core brain files (CLAUDE.md, BRAND.md, BUSINESS.md,
  ME.md, PLAN.md, TASKS.md), custom skills with SKILL.md files, specialist agents,
  slash commands, Cowork Global Instructions, Quick Start Guide, Service Agreement,
  and QA validation report with assumptions log. Supports 7 industry verticals
  (estate agents, accountants, recruitment, solicitors, retailers, tradespeople,
  coaches) with pre-loaded defaults for terminology, compliance, and tone.
  Enforces package limits: Starter (2 skills), Business (5 skills, 2 agents,
  3 commands), Pro (10 skills, unlimited). Use this skill whenever Wayne says
  "onboard a client", "build a brain for [business]", "client onboarding",
  "set up claude code for", "new client brain", "cowork onboarding",
  "install a brain", "run the onboarding skill", "generate their full Claude Code
  setup", or provides discovery call data with a business name and package tier.
  Do NOT use for claude.ai Project setup (that is claude-ai-onboarding), for
  writing individual content (emails, posts, proposals), or for creating a single
  CLAUDE.md/agent/skill outside of a full client onboarding.
---

# Claude Code / Cowork Onboarding

You are building a complete AI Brain for a small business client. This is the full install — Claude Code context files, custom skills, agents, commands, and Cowork Global Instructions. Everything the client needs to start using AI in their business.

Read all reference files in `references/` before starting:
- `industry-defaults.md` — 7 business verticals with terminology, tone, compliance, typical skills/agents/commands
- `brain-file-templates.md` — templates for the 6 core brain files
- `skill-templates.md` — templates for the 12 available client skills

---

## Step 1: Intake

Collect the client's details. Support two input modes:

**Paste mode** — Wayne pastes or types the answers directly into the chat.
**File mode** — Wayne points at a filled-in Discovery Questionnaire .docx (attempt to read it; if it fails, ask Wayne to paste the contents).

### Data points to collect (24 total):

1. Business name (full + trading name if different)
2. Business type (from the 7 supported verticals — or "Other")
3. Owner name
4. Owner role/title
5. Location
6. What the business does (2-3 sentences)
7. What makes them different (differentiator)
8. Typical customer description
9. Brand personality — 3 words that describe them
10. Brand personality — 3 words that do NOT describe them
11. Brand colours (hex codes if available)
12. Fonts (if they have brand fonts)
13. Tone (formal to casual — where do they sit?)
14. Words/phrases to always use
15. Words/phrases to never use
16. Email sign-off
17. Top 3-5 pain points (ranked)
18. Selected skills (from the 12 available — see `references/skill-templates.md`)
19. Package selected (Starter / Business / Pro)
20. Current business goals
21. Tech comfort level
22. Device (Mac / Windows / iPad)
23. Any writing samples or docs provided
24. Whether they want Cowork, Claude Code, or both

**If data is incomplete:** Fill gaps with industry defaults from `references/industry-defaults.md`. Do NOT interrogate Wayne — work with what you have and note assumptions in the QA report.

**Package skill limits:**
- Starter (£497): 2 skills, no agents, no commands
- Business (£997): 5 skills, 2 agents, 3 commands
- Pro (£1,997): 10 skills, unlimited agents, unlimited commands

---

## Step 2: Business Type Routing

Read `references/industry-defaults.md` and match the client to one of 7 verticals:

1. Estate Agents / Letting Agencies
2. Accountants / Financial Services
3. Recruitment Agencies
4. Solicitors / Legal Practices
5. Retailers (Online / High Street)
6. Tradespeople / Contractors
7. Coaches / Consultants / Freelancers

If the client doesn't fit a vertical, use "Other" — skip industry-specific defaults and rely entirely on the client's own data.

Load the matching vertical's:
- **Terminology** — industry-specific words to use correctly
- **Compliance** — regulations and disclaimers
- **Default tone** — starting point if not specified
- **Typical skills** — recommended skills for this vertical
- **Typical agents** — recommended agents for this vertical
- **Typical commands** — recommended commands for this vertical
- **Banned phrases** — words/phrases to avoid
- **Key features** — special considerations

Client-specific data ALWAYS overrides industry defaults.

---

## Step 3: Generate Core Brain Files

Read `references/brain-file-templates.md` and generate all 6 files, filling every `{{PLACEHOLDER}}` with client data merged with industry defaults.

### Files generated:

1. **CLAUDE.md** — Master system prompt. The brain's rulebook. Contains session pattern, communication rules, file references, compliance notes. This is the most important file — it tells Claude how to behave.

2. **BRAND.md** — Brand identity. Colours, fonts, tone, writing rules, phrases to use/avoid, email sign-off. Skills and agents read this for voice consistency.

3. **BUSINESS.md** — Business context. What they do, services, customers, competitors, goals, industry terminology. Provides the knowledge layer.

4. **ME.md** — Owner profile. Working style, tech comfort, communication preferences. Helps Claude adapt to the user.

5. **PLAN.md** — Current goals and priorities. Seeded from questionnaire, updated by the client over time.

6. **TASKS.md** — Active task list. Blank template with correct structure, ready for use.

---

## Step 4: Generate Skills

Read `references/skill-templates.md`. For each skill selected during the call, generate a complete skill folder.

### Available skills (12 total):

| Category | Skill | Good for |
|---|---|---|
| Communication | Email Writer | All client types |
| Communication | Customer Reply Handler | Retailers, tradespeople, estate agents |
| Communication | Internal Comms Writer | Businesses with staff |
| Sales | Proposal / Quote Writer | Coaches, solicitors, tradespeople |
| Sales | Follow-Up Sequence Writer | Recruitment, coaches, estate agents |
| Sales | Job Advert Writer | Recruitment agencies |
| Content | Social Media Post Writer | All client types |
| Content | Newsletter Writer | Retailers, accountants, coaches |
| Content | Blog / Long-Form Writer | Coaches, solicitors, accountants |
| Admin | Meeting Notes Summariser | All client types |
| Admin | Report Writer | Accountants, solicitors |
| Admin | Document Summariser | All client types |

### For each skill:

1. Create a folder: `/skills/[skill-name]/`
2. Generate `SKILL.md` using the template from `references/skill-templates.md`
3. Replace ALL `{{PLACEHOLDER}}` values with client data
4. Add industry-specific rules from Step 2
5. Ensure the skill reads from BRAND.md for voice consistency
6. Write a description that names the unique output structure (critical for recall)

### Skill linking:
Some skills need to reference other files:
- All skills should read BRAND.md for tone
- Email Writer needs the sign-off from BRAND.md
- Proposal Writer needs services/pricing from BUSINESS.md
- Social Media Writer needs brand colours from BRAND.md
- Blog Writer needs expertise areas from BUSINESS.md

Add these cross-references as explicit instructions in each skill.

---

## Step 5: Generate Agents

Agents are specialist sub-agents that handle specific domains. They live in the client's `~/.claude/agents/` folder (for Claude Code) or are configured in Cowork.

### Agent format (Claude Code):

```markdown
---
name: [agent-name]
model: sonnet
---

# [Agent Name]

[Agent description and instructions]

## Rules
- Read BRAND.md for tone before writing anything
- Read BUSINESS.md for context
- [Industry-specific rules]
- British English only

## What You Handle
[List of tasks this agent covers]

## What You Don't Handle
[Redirect to other agents or main chat]
```

### Generate agents based on:

1. **Industry defaults** — each vertical has typical agents (see `references/industry-defaults.md`)
2. **Client pain points** — if their top pain point is customer comms, prioritise a Customer Comms Agent
3. **Package limits** — Starter: 0 agents, Business: 2, Pro: unlimited

### Common agent patterns:

| Agent | Purpose | Good for |
|---|---|---|
| Client Communications | All outward-facing client/customer emails | All verticals |
| Marketing / Content | Social posts, newsletters, blog content | All verticals |
| Sales | Proposals, follow-ups, lead responses | Coaches, recruitment, estate agents |
| Compliance / Legal | Client care letters, disclaimers, regulatory language | Solicitors, accountants |
| Internal | Team updates, meeting notes, reports | Businesses with staff |

### Agent rules:
- Every agent MUST read BRAND.md before producing any output
- Agents should have clear boundaries — what they handle vs what they don't
- Use `model: sonnet` for speed (most client tasks don't need Opus)
- Name agents clearly: `client-comms`, `marketing`, `sales`, etc.

---

## Step 6: Generate Commands

Commands are slash commands that live in the client's `~/.claude/commands/` folder. They provide quick shortcuts for common tasks.

### Command format:

```markdown
---
name: [command-name]
description: [What this command does]
---

[Full prompt that runs when the command is invoked]
```

### Generate commands based on:

1. **Industry defaults** — each vertical has typical commands (see `references/industry-defaults.md`)
2. **Client's most frequent tasks** — mapped from pain points
3. **Package limits** — Starter: 0 commands, Business: 3, Pro: unlimited

### Common command patterns:

| Command | What it does | Example usage |
|---|---|---|
| `/email` | Draft an email using brand voice | `/email follow up with Sarah about the quote` |
| `/social` | Write a social media post | `/social new listing at 14 Elm Road` |
| `/review-reply` | Respond to a customer review | `/review-reply [paste review]` |
| `/proposal` | Draft a proposal or quote | `/proposal kitchen refit for the Johnsons` |
| `/followup` | Write a follow-up email | `/followup haven't heard from Acme Ltd` |
| `/meeting-notes` | Summarise meeting notes | `/meeting-notes [paste notes]` |
| `/blog` | Write a blog post | `/blog 3 mistakes with pricing strategy` |

### Command rules:
- Commands should reference BRAND.md for voice
- Keep command names short (one word ideally)
- Include `$ARGUMENTS` to accept input
- Each command should produce a complete, ready-to-use output

### Command template:

```markdown
---
name: [command-name]
description: [One-line description]
---

You are writing a [type of content] for {{BUSINESS_NAME}}.

Read BRAND.md for tone and voice rules before writing.
Read BUSINESS.md for context about the business.

The user wants: $ARGUMENTS

[Specific instructions for this command type]

Output a complete, ready-to-use [type of content]. British English only.
```

---

## Step 7: Generate Cowork Global Instructions

Generate the text block to paste into the client's Cowork desktop app settings (Settings > Global Instructions).

### Format:

```
Business: {{BUSINESS_NAME}}
Owner: {{OWNER_NAME}}
Role: {{OWNER_ROLE}}

Brand Voice: {{TONE_SUMMARY_ONE_SENTENCE}}

Key Rules:
- British English always
- Sign off emails with: {{EMAIL_SIGNOFF}}
- Always use: {{WORDS_ALWAYS}}
- Never use: {{WORDS_NEVER}}
- {{INDUSTRY_COMPLIANCE_ONE_LINER}}

Services: {{SERVICES_SUMMARY}}

Customers: {{CUSTOMER_SUMMARY}}

Top Priority: {{TOP_PRIORITY}}
```

Save as `cowork-global-instructions.txt` in the `/config/` folder.

---

## Step 8: Generate Client Docs

### Quick Start Guide

Generate a client-facing guide based on `references/setup-guide-template.md` (from the claude-ai-onboarding skill — adapt for Claude Code/Cowork):

- What's been installed (list all brain files, skills, agents, commands)
- How to use it daily (start a session, ask for help, use commands)
- Weekly rhythm (Monday: task list, Friday: update tasks, Monthly: update PLAN.md)
- Tips for best results
- If something doesn't sound right (troubleshooting)
- What's Next — Phase 2 seeds (new skills, inbox connection, document search, content repurposing)
- Support contact and check-in date

Save as `quick-start-guide.md` in `/docs/`.

### Service Agreement Summary

Generate a summary of what was agreed:
- Package and price
- Skills installed (list)
- Agents installed (list)
- Commands installed (list)
- Support period
- Check-in call date

Save as `service-summary.md` in `/docs/`.

---

## Step 9: QA Validation

Run these checks automatically and save results as `qa-report.md`:

### Must pass:
- [ ] Business name is consistent across ALL generated files
- [ ] BRAND.md tone matches CLAUDE.md communication rules
- [ ] Every selected skill has a folder with SKILL.md
- [ ] Every agent file exists and references BRAND.md
- [ ] Every command file exists and references BRAND.md
- [ ] Cowork Global Instructions match core files
- [ ] No `{{PLACEHOLDER}}` or `[PLACEHOLDER]` values remain in any file
- [ ] British English throughout
- [ ] Quick Start Guide lists match actual skills/agents/commands generated

### Should pass:
- [ ] Industry terminology correct for selected vertical
- [ ] Brand personality "yes" and "no" words don't overlap
- [ ] Skill count matches package limit
- [ ] Agent count matches package limit
- [ ] Command count matches package limit

### Assumptions log:
List every data point that was:
- Filled from industry defaults
- Left blank or marked "not specified" because the client didn't provide it
- Inferred from context rather than explicitly stated

This is critical — if the client didn't provide brand colours, fonts, a logo, writing samples, or any other data point, it MUST appear in the assumptions log even if you left the field blank rather than guessing. The assumptions log is how Wayne knows what to follow up on before handover.

Format:
```
ASSUMED: [field] = [value] (industry default for [vertical])
MISSING: [field] — not provided by client, left as [what you put instead]
INFERRED: [field] = [value] (based on [what you inferred from])
```

---

## Step 10: Generate Install Script

Generate install scripts that the client runs on their own machine to set everything up. Wayne sends them the package folder (e.g. via AirDrop, USB, zip, or Google Drive) and they run one command.

### How the client runs it:

**Mac/Linux:**
1. Wayne sends the client the package folder (zipped or via AirDrop/Drive)
2. Client unzips it to their Desktop or Downloads
3. Client opens Terminal (Cmd+Space → type "Terminal")
4. Client types: `bash ~/Downloads/[folder-name]/install.sh`
5. Done — everything is in the right place

**Windows:**
1. Wayne sends the client the package folder (zipped or via Drive/email)
2. Client unzips it
3. Client double-clicks `install.bat`
4. Done — everything is in the right place

### Script requirements:
- Must work on both Mac and Windows (generate TWO scripts: `install.sh` for Mac/Linux and `install.bat` for Windows)
- **Pre-flight check:** Verify Claude Code is installed (`command -v claude` on Mac, `where claude` on Windows). If not found, print clear install instructions (link to claude.ai/download) and exit
- **Pre-flight check:** Verify `~/.claude/` directory exists. If not, create it
- Accept an optional argument for the project folder path (default: `~/Documents/[client-slug]-ai` on Mac, `%USERPROFILE%\Documents\[client-slug]-ai` on Windows)
- Use `SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"` so it works from any location (bash version)
- Copy the 6 brain files to the project folder
- Copy skills to `~/.claude/skills/` (preserving folder structure)
- Copy agents to `~/.claude/agents/`
- Copy commands to `~/.claude/commands/`
- Print progress for each step with counts
- Print a summary at the end with paths and "how to start" instructions
- Remind Cowork users to paste `cowork-global-instructions.txt` into Settings manually
- Use `set -e` to stop on errors (bash version)
- Make the bash script executable (`chmod +x`)

### Template:

```bash
#!/bin/bash
# ─────────────────────────────────────────────────
# {{BUSINESS_NAME}} — Claude Code Brain Install
# Run this on the client's Mac to set everything up
# Usage: bash install.sh [project-folder]
# Example: bash install.sh ~/Documents/{{CLIENT_SLUG}}-ai
# ─────────────────────────────────────────────────

set -e

PROJECT_DIR="${1:-$HOME/Documents/{{CLIENT_SLUG}}-ai}"

echo ""
echo "══════════════════════════════════════════════"
echo "  {{BUSINESS_NAME}} — AI Brain Install"
echo "══════════════════════════════════════════════"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Pre-flight: Check Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "ERROR: Claude Code is not installed."
    echo ""
    echo "Install it first:"
    echo "  1. Go to https://claude.ai/download"
    echo "  2. Download and install Claude Code"
    echo "  3. Run 'claude' once to complete setup"
    echo "  4. Then run this script again"
    echo ""
    exit 1
fi

# Pre-flight: Ensure .claude directory exists
mkdir -p "$HOME/.claude"

echo "Claude Code found. Starting install..."
echo ""

# Step 1: Create project folder
echo "[1/5] Creating project folder: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"

# Step 2: Copy brain files
echo "[2/5] Installing brain files"
for file in CLAUDE.md BRAND.md BUSINESS.md ME.md PLAN.md TASKS.md; do
    cp "$SCRIPT_DIR/$file" "$PROJECT_DIR/$file"
done

# Step 3: Install skills
echo "[3/5] Installing skills to ~/.claude/skills/"
mkdir -p "$HOME/.claude/skills"
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$HOME/.claude/skills/$skill_name"
    cp "$skill_dir"SKILL.md "$HOME/.claude/skills/$skill_name/SKILL.md"
    echo "       + $skill_name"
done

# Step 4: Install agents
echo "[4/5] Installing agents to ~/.claude/agents/"
mkdir -p "$HOME/.claude/agents"
for agent_file in "$SCRIPT_DIR"/agents/*.md; do
    agent_name=$(basename "$agent_file")
    cp "$agent_file" "$HOME/.claude/agents/$agent_name"
    echo "       + ${agent_name%.md}"
done

# Step 5: Install commands
echo "[5/5] Installing commands to ~/.claude/commands/"
mkdir -p "$HOME/.claude/commands"
for cmd_file in "$SCRIPT_DIR"/commands/*.md; do
    cmd_name=$(basename "$cmd_file")
    cp "$cmd_file" "$HOME/.claude/commands/$cmd_name"
    echo "       + /${cmd_name%.md}"
done

echo ""
echo "══════════════════════════════════════════════"
echo "  Install complete!"
echo "══════════════════════════════════════════════"
echo ""
echo "  Cowork users: paste config/cowork-global-instructions.txt"
echo "  into Settings > Global Instructions"
echo ""
echo "══════════════════════════════════════════════"
echo ""
read -p "Launch Claude Code now? (y/n) " answer
if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    cd "$PROJECT_DIR" && claude
fi
```

### Windows template (`install.bat`):

```batch
@echo off
REM ─────────────────────────────────────────────────
REM {{BUSINESS_NAME}} — Claude Code Brain Install
REM Run this on the client's PC to set everything up
REM Usage: install.bat [project-folder]
REM Example: install.bat "%USERPROFILE%\Documents\{{CLIENT_SLUG}}-ai"
REM ─────────────────────────────────────────────────

setlocal enabledelayedexpansion

if "%~1"=="" (
    set "PROJECT_DIR=%USERPROFILE%\Documents\{{CLIENT_SLUG}}-ai"
) else (
    set "PROJECT_DIR=%~1"
)

echo.
echo ══════════════════════════════════════════════
echo   {{BUSINESS_NAME}} — AI Brain Install
echo ══════════════════════════════════════════════
echo.

REM Pre-flight: Check Claude Code is installed
where claude >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Claude Code is not installed.
    echo.
    echo Install it first:
    echo   1. Go to https://claude.ai/download
    echo   2. Download and install Claude Code
    echo   3. Run 'claude' once to complete setup
    echo   4. Then run this script again
    echo.
    pause
    exit /b 1
)

REM Pre-flight: Ensure .claude directory exists
if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"

echo Claude Code found. Starting install...
echo.

set "SCRIPT_DIR=%~dp0"

REM Step 1: Create project folder
echo [1/5] Creating project folder: %PROJECT_DIR%
if not exist "%PROJECT_DIR%" mkdir "%PROJECT_DIR%"

REM Step 2: Copy brain files
echo [2/5] Installing brain files
for %%f in (CLAUDE.md BRAND.md BUSINESS.md ME.md PLAN.md TASKS.md) do (
    copy /Y "%SCRIPT_DIR%%%f" "%PROJECT_DIR%\%%f" >nul
)

REM Step 3: Install skills
echo [3/5] Installing skills to %USERPROFILE%\.claude\skills\
for /D %%d in ("%SCRIPT_DIR%skills\*") do (
    set "skill_name=%%~nxd"
    if not exist "%USERPROFILE%\.claude\skills\!skill_name!" mkdir "%USERPROFILE%\.claude\skills\!skill_name!"
    copy /Y "%%d\SKILL.md" "%USERPROFILE%\.claude\skills\!skill_name!\SKILL.md" >nul
    echo        + !skill_name!
)

REM Step 4: Install agents
echo [4/5] Installing agents to %USERPROFILE%\.claude\agents\
if not exist "%USERPROFILE%\.claude\agents" mkdir "%USERPROFILE%\.claude\agents"
for %%f in ("%SCRIPT_DIR%agents\*.md") do (
    copy /Y "%%f" "%USERPROFILE%\.claude\agents\%%~nxf" >nul
    echo        + %%~nf
)

REM Step 5: Install commands
echo [5/5] Installing commands to %USERPROFILE%\.claude\commands\
if not exist "%USERPROFILE%\.claude\commands" mkdir "%USERPROFILE%\.claude\commands"
for %%f in ("%SCRIPT_DIR%commands\*.md") do (
    copy /Y "%%f" "%USERPROFILE%\.claude\commands\%%~nxf" >nul
    echo        + /%%~nf
)

echo.
echo ══════════════════════════════════════════════
echo   Install complete!
echo ══════════════════════════════════════════════
echo.
echo   Cowork users: paste config\cowork-global-instructions.txt
echo   into Settings ^> Global Instructions
echo.
echo ══════════════════════════════════════════════
echo.
set /p "answer=Launch Claude Code now? (y/n) "
if /i "%answer%"=="y" (
    cd /d "%PROJECT_DIR%" && claude
) else (
    pause
)
```

Replace all `{{BUSINESS_NAME}}` and `{{CLIENT_SLUG}}` placeholders with actual values. Make the bash script executable with `chmod +x install.sh`. Both scripts go in the package root.

### README.md

Also generate a `README.md` in the package root. This is the first thing the client (or a new Claude session) sees when opening the folder. It should explain what's in the package and how to install it.

Template:

```markdown
# {{BUSINESS_NAME}} — AI Brain

Your custom AI assistant, built with Claude Code.

## What's Inside

| File | Purpose |
|---|---|
| CLAUDE.md | How Claude behaves for your business |
| BRAND.md | Your brand voice, tone, colours |
| BUSINESS.md | What your business does, services, customers |
| ME.md | Your working style and preferences |
| PLAN.md | Current goals and priorities |
| TASKS.md | Active task list |

### Skills ({{SKILL_COUNT}})
{{SKILL_LIST — one bullet per skill with one-line description}}

### Agents ({{AGENT_COUNT}})
{{AGENT_LIST — one bullet per agent with one-line description}}

### Commands ({{COMMAND_COUNT}})
{{COMMAND_LIST — one bullet per command with example usage}}

## How to Install

### Prerequisites
1. Install Claude Code from https://claude.ai/download
2. Run `claude` once to complete initial setup

### Mac / Linux
```
bash install.sh
```

### Windows
Double-click `install.bat` or run it from Command Prompt.

### Cowork Desktop App
Paste the contents of `config/cowork-global-instructions.txt` into Settings > Global Instructions.

## How to Use

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to your project folder: `cd ~/Documents/{{CLIENT_SLUG}}-ai`
3. Type `claude` and press Enter
4. Start chatting — Claude already knows your business

### Try these commands:
{{COMMAND_EXAMPLES — 2-3 example slash commands with descriptions}}

## Weekly Rhythm
- **Monday:** Review TASKS.md, plan the week
- **Friday:** Update TASKS.md with progress
- **Monthly:** Review and update PLAN.md

## Support
Built by Wayne Pearce. If something doesn't sound right or you need changes, get in touch.

Package: {{PACKAGE_TIER}}
Installed: {{DATE}}
```

Replace all `{{PLACEHOLDER}}` values with actual client data.

---

## Step 11: Package

Create the complete folder structure:

```
/Users/wayne/Claude/client-brains/[client-business-name-slugified]/
  CLAUDE.md
  BRAND.md
  BUSINESS.md
  ME.md
  PLAN.md
  TASKS.md
  README.md               ← What's inside + how to install
  install.sh              ← Mac/Linux install script
  install.bat             ← Windows install script
  /skills/
    /email-writer/
      SKILL.md
    /social-media-writer/
      SKILL.md
    [etc — one folder per selected skill]
  /agents/
    client-comms.md
    marketing.md
    [etc — one file per agent]
  /commands/
    email.md
    social.md
    [etc — one file per command]
  /config/
    cowork-global-instructions.txt
  /docs/
    quick-start-guide.md
    service-summary.md
  qa-report.md
```

Use lowercase-kebab-case for the folder name (e.g., `smiths-estate-agents`, `bright-coaching`).

After saving, show Wayne:
1. A summary of everything generated (files, skills, agents, commands)
2. The QA report highlights (any failures or assumptions)
3. Package tier confirmation (Starter/Business/Pro)
4. Remind him to review before installing on the client's machine
5. Note any skills that need linking to external services (Gmail, Google Drive, etc.) — these will need additional setup during install
