---
name: wtf
description: "Interpret vague or voice-dictated instructions by creating a team of 3 interpretation agents (pragmatist, strategist, creative), each reading workspace context through a different lens. Agents interpret independently, then review each other's readings and refine. Presents the final interpretations and executes the one Wayne picks. Use when Wayne gives an ambiguous instruction like 'do the thing', 'sort out the stuff', 'continue from where we left off', 'fix that problem', or any instruction where it's unclear what specific action to take. Also triggered by 'wtf', 'what do I mean', 'figure it out', 'you know what I mean', 'work it out'."
---

# WTF — What's The Focus

Creates a team of 3 interpreter agents who independently read a vague instruction, then challenge and refine each other's interpretations before presenting options.

## Step 1: Capture the Vague Instruction

The user's message (or the text after `/wtf`) is the vague instruction. Save it exactly as received — typos and all.

## Step 2: Gather Workspace Context

Read the following files. Skip any that don't exist — not every workspace has all of them.

| File | What it tells the agents |
|---|---|
| `./CLAUDE.md` | What this project is, what skills/agents exist, how the workspace works |
| `./TASKS.md` | What's active, what's done, what's next |
| `./handoff.md` | What was happening last session — the most recent context |
| `./ME.md` | Who the user is in this workspace |

Then run these commands:

```bash
git log --oneline -10 2>/dev/null || echo "Not a git repo"
```

```bash
ls .claude/skills/ 2>/dev/null || echo "No local skills"
```

```bash
ls .claude/agents/ 2>/dev/null || echo "No local agents"
```

Compile everything into a WORKSPACE SNAPSHOT block:

```
WORKSPACE SNAPSHOT
==================
Project: [first meaningful line from CLAUDE.md, or directory name]
Directory: [current working directory]

Active tasks:
[relevant lines from TASKS.md, or "No TASKS.md found"]

Last session:
[key context from handoff.md, or "No handoff found"]

Available skills: [comma-separated list from .claude/skills/]
Available agents: [comma-separated list from .claude/agents/]

Recent git activity:
[git log output]
==================
```

Keep the snapshot concise — no more than 40 lines. Summarise long sections.

## Step 3: Create the Interpreter Team

Create the team:

```
TeamCreate(team_name="wtf-interpreters", description="Interpreting vague instruction: [first 50 chars of instruction]")
```

## Step 4: Spawn 3 Interpreters

Launch ALL THREE teammates in a SINGLE message (3 Agent tool calls). They must run in parallel.

Each teammate gets the same workspace snapshot and vague instruction but has a different interpretation lens. All use `team_name="wtf-interpreters"`.

```
Agent(
  subagent_type="wtf-pragmatist",
  model="haiku",
  team_name="wtf-interpreters",
  name="pragmatist",
  prompt="""
You are the PRAGMATIST interpreter on the wtf-interpreters team.

PHASE 1: Interpret independently. Read the workspace snapshot and the vague instruction below. Produce your INTERPRETATION block and send it to the team lead using SendMessage.

VAGUE INSTRUCTION
─────────────────
[paste the exact vague instruction]
─────────────────

[paste the full WORKSPACE SNAPSHOT block]

Follow your agent instructions. Send your INTERPRETATION block to the team lead, then go idle and wait. You will receive Phase 2 instructions with the other interpreters' readings.
""")
```

```
Agent(
  subagent_type="wtf-strategist",
  model="haiku",
  team_name="wtf-interpreters",
  name="strategist",
  prompt="""
You are the STRATEGIST interpreter on the wtf-interpreters team.

PHASE 1: Interpret independently. Read the workspace snapshot and the vague instruction below. Produce your INTERPRETATION block and send it to the team lead using SendMessage.

VAGUE INSTRUCTION
─────────────────
[paste the exact vague instruction]
─────────────────

[paste the full WORKSPACE SNAPSHOT block]

Follow your agent instructions. Send your INTERPRETATION block to the team lead, then go idle and wait. You will receive Phase 2 instructions with the other interpreters' readings.
""")
```

```
Agent(
  subagent_type="wtf-creative",
  model="haiku",
  team_name="wtf-interpreters",
  name="creative",
  prompt="""
You are the CREATIVE interpreter on the wtf-interpreters team.

PHASE 1: Interpret independently. Read the workspace snapshot and the vague instruction below. Produce your INTERPRETATION block and send it to the team lead using SendMessage.

VAGUE INSTRUCTION
─────────────────
[paste the exact vague instruction]
─────────────────

[paste the full WORKSPACE SNAPSHOT block]

Follow your agent instructions. Send your INTERPRETATION block to the team lead, then go idle and wait. You will receive Phase 2 instructions with the other interpreters' readings.
""")
```

## Step 5: Collect Phase 1 Interpretations

Wait for all 3 teammates to send their INTERPRETATION blocks. Messages arrive automatically — don't poll.

Once all 3 are in, check for early convergence:
- If all three propose the same action (same skill/agent AND same target), skip to Step 7 — no need for peer review.

## Step 6: Peer Review (Phase 2)

Send each interpreter the other two agents' readings. They can refine their own interpretation or challenge the others.

Send all 3 messages in a SINGLE message (3 SendMessage calls):

```
SendMessage(
  to="pragmatist",
  message="""PHASE 2: Peer review. Here are the other two interpretations. Review them, then send back your FINAL INTERPRETATION — either your original (if you still stand by it) or a refined version. You may also flag if you think another interpreter got it right.

STRATEGIST said:
[paste strategist's interpretation]

CREATIVE said:
[paste creative's interpretation]

Send your FINAL INTERPRETATION block to the team lead.""",
  summary="Phase 2: review other interpretations"
)
```

```
SendMessage(
  to="strategist",
  message="""PHASE 2: Peer review. Here are the other two interpretations. Review them, then send back your FINAL INTERPRETATION — either your original (if you still stand by it) or a refined version. You may also flag if you think another interpreter got it right.

PRAGMATIST said:
[paste pragmatist's interpretation]

CREATIVE said:
[paste creative's interpretation]

Send your FINAL INTERPRETATION block to the team lead.""",
  summary="Phase 2: review other interpretations"
)
```

```
SendMessage(
  to="creative",
  message="""PHASE 2: Peer review. Here are the other two interpretations. Review them, then send back your FINAL INTERPRETATION — either your original (if you still stand by it) or a refined version. You may also flag if you think another interpreter got it right.

PRAGMATIST said:
[paste pragmatist's interpretation]

STRATEGIST said:
[paste strategist's interpretation]

Send your FINAL INTERPRETATION block to the team lead.""",
  summary="Phase 2: review other interpretations"
)
```

Wait for all 3 final interpretations to come back.

## Step 7: Check Convergence

After Phase 2, check again: did the peer review cause convergence?

**If all 3 now agree on the same action:**

```
All 3 readings agree (after peer review):
> [the converged interpretation]
> Execute with: [skill/agent name]

Executing now.
```

Shutdown the team and go to Step 9.

**If 2 of 3 agree and the third defers ("I think [other agent] got it right"):**

Present the majority interpretation with a note:

```
2 of 3 agree:
> [the majority interpretation]
> Execute with: [skill/agent name]

Executing now.
```

Shutdown the team and go to Step 9.

## Step 8: Present Options

If the interpretations still differ after peer review, present them:

```
3 WAYS I READ THAT
========================================

1. PRAGMATIST [confidence]
   [What I think you mean — 1 sentence]
   Execute with: [skill/agent/main conversation]

2. STRATEGIST [confidence]
   [What I think you mean — 1 sentence]
   Execute with: [skill/agent/main conversation]

3. CREATIVE [confidence]
   [What I think you mean — 1 sentence]
   Execute with: [skill/agent/main conversation]

========================================
Pick 1, 2, or 3 — or tell me what you actually meant.
```

Wait for Wayne's response.

**If Wayne picks a number (1, 2, or 3):** Shutdown the team, go to Step 9.
**If Wayne picks a number with a modification** ("2 but for chapter 6"): Incorporate the modification, shutdown, go to Step 9.
**If Wayne says "none" or gives a new instruction:** Shutdown the team. Treat his response as the real instruction and act on it directly. Do NOT re-run wtf.

## Step 9: Shutdown Team and Execute

First, shutdown all teammates:

```
SendMessage(to="*", message={"type": "shutdown_request", "reason": "Interpretation complete"})
```

Then take the selected interpretation and act on it:

| The interpretation says "Execute with..." | What you do |
|---|---|
| A skill name (e.g. `chapter-writer`) | Proceed as if Wayne had given the specific action as a direct instruction. The skill will trigger naturally through the conversation. |
| An agent name (e.g. `research-assistant`) | Dispatch that agent with the specific action text as the prompt |
| "main conversation" | Just act on the specific action text directly — no skill or agent dispatch needed |

## Rules

- **Never re-run wtf recursively.** If Wayne's response to the options is still vague, ask ONE direct question and then act.
- **Don't over-explain the process.** Wayne doesn't need to know about phases or peer review. Just show the options.
- **Voice input is expected.** The vague instruction will have typos, shorthand, incomplete sentences. Parse what you can.
- **Only reference real skills/agents.** Each agent's prompt includes the workspace snapshot with the exact list of available skills and agents. Never invent tools that don't exist.
- **Always shutdown the team.** Whether the interpretation succeeds or fails, send the shutdown broadcast before proceeding.

## Error Handling

| Failure | Recovery |
|---|---|
| One agent fails Phase 1 | Continue with the 2 that worked. Skip Phase 2 for the missing agent. |
| All agents fail Phase 1 | Shutdown team. Fall back to asking Wayne one direct clarifying question. |
| One agent fails Phase 2 | Use their Phase 1 interpretation as their final answer. |
| No CLAUDE.md or TASKS.md | Agents still work — they'll base interpretation on git log and directory structure. |
| Not a git repo | Agents still work — they'll base interpretation on whatever context files exist. |
