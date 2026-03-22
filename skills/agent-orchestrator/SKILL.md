---
name: agent-orchestrator
description: "Design and generate complete sub-agent teams for Claude Code. Takes a complex task, recommends an orchestration pattern (sequential pipeline, parallel fan-out, baton-passing loop, conditional dispatch, or hybrid), designs each agent's role/tools/model/handoffs, validates against anti-patterns, generates the actual agent .md files ready for ~/.claude/agents/, and optionally generates an orchestration skill to coordinate them. Use this skill whenever someone wants to build a multi-agent system, design an agent pipeline, create a team of agents, orchestrate sub-agents, break a task into cooperating agents, or says things like 'design agents for', 'build me a pipeline', 'agent team for', 'orchestrate this', 'multi-agent setup', 'break this into agents', 'I need agents that work together', 'create a team of specialists', 'pipeline for handling X'. Even if someone just describes a complex workflow and mentions wanting agents — this skill applies. Distinct from creating a single agent (which writes one agent file) — agent-orchestrator designs entire TEAMS with handoff contracts, topology maps, validation, and coordination logic."
---

# Agent Orchestrator

Design and generate complete sub-agent teams for Claude Code. Takes a complex task, selects the right orchestration pattern, designs each agent with explicit contracts, validates the design, and produces ready-to-deploy files.

**Two outputs:** agent .md files (ready for `~/.claude/agents/`) + optional orchestration skill (coordinates the team).

## Workflow

### Step 1: Intake

Collect from the user:

- **Task description** (required) — what complex task needs multiple agents? What's the end-to-end workflow?
- **Team size preference** (optional, default: auto) — small (2-3), medium (3-5), large (5+)
- **Trigger context** (optional) — how will this team be invoked? (manually, scheduled task, webhook/notification, another skill)
- **Constraints** (optional) — budget concerns (model costs), speed requirements, existing agents to integrate with

If the user describes the task upfront, proceed with sensible defaults. Don't interrogate — figure out what they need from what they said.

### Step 2: Task Decomposition

Before selecting a pattern, break the task apart:

1. **List the sub-tasks** — what distinct steps does this workflow require?
2. **Map dependencies** — which steps depend on others? Which can run in parallel?
3. **Identify decision points** — where does the workflow branch based on conditions?
4. **Trace the data flow** — what data does each step produce and consume?

Present the decomposition to the user as a numbered list. Use arrows to show dependencies:

```
1. Classify input  ──>  2a. Research (if needed)
                         2b. Skip research (if simple)
                   ──>  3. Draft output
                   ──>  4. Review output
```

Wait for the user to confirm the decomposition before moving on. They may want to merge steps, split them, or add missing ones.

### Step 3: Pattern Selection

Read `references/orchestration-patterns.md`. Based on the decomposition, recommend a pattern:

| Signal in the decomposition | Pattern |
|---|---|
| Steps must run in order, each feeding the next | **Sequential Pipeline** |
| Multiple independent evaluations of the same input | **Parallel Fan-Out** |
| Iterative refinement until a quality bar is met | **Baton-Passing Loop** |
| Different paths based on input classification | **Conditional Dispatch** |
| Workflow has both sequential and parallel sections | **Hybrid** |

Present the recommendation with:
- 2-3 sentence justification for why this pattern fits
- ASCII topology diagram showing the agent connections
- A simpler alternative if one exists ("You could also do this with just 2 agents if...")

### Step 4: Team Design Canvas

Read `references/team-design-canvas.md`. For each agent in the team, work through:

1. **Name** — kebab-case, descriptive of function (e.g. `content-classifier`, `quality-grader`)
2. **Role** — single responsibility, one sentence
3. **Input contract** — exactly what data this agent receives (format, fields)
4. **Output contract** — exactly what data this agent produces (format, fields)
5. **Tools** — minimal set needed (read `references/agent-template.md` for the tool selection guide)
6. **Model tier** — haiku (simple routing/classification), sonnet (reasoning/generation), opus (deep analysis/complex judgement)
7. **Handoff** — how output reaches the next agent

Present the full design as a formatted summary:

```
AGENT TEAM DESIGN
═══════════════════════════════════════

Team: [name]
Pattern: [pattern]
Agents: [count]

[ASCII topology diagram with model tiers and tools]

═══════════════════════════════════════
AGENT DETAILS
═══════════════════════════════════════

1. [agent-name] ([model])
   Role: [single sentence]
   Input: [from where, what format, what fields]
   Output: [to where, what format, what fields]
   Tools: [minimal list]

───────────────────────────────────────

2. [agent-name] ([model])
   [...]

═══════════════════════════════════════
```

Wait for user approval. They may want to merge agents, split responsibilities, change model tiers, or adjust the topology.

### Step 5: Validation

Read `references/anti-patterns.md`. Check the design against every anti-pattern:

- [ ] No agent has more than 6 tools (tool bloat)
- [ ] No two agents have overlapping responsibilities (role duplication)
- [ ] Every agent has a defined output contract (no dangling outputs)
- [ ] Every handoff specifies exact format and fields (no vague "pass the data")
- [ ] Routing/classification agents use haiku, not opus (model waste)
- [ ] Read-only agents don't have Write/Edit tools (tool excess)
- [ ] The team has error handling — what happens if an agent fails?
- [ ] No circular dependencies in the topology
- [ ] Total agent count is the minimum needed (no over-engineering)
- [ ] Every output has a consumer, every input has a producer

Report any violations and suggest fixes. Don't generate files until the design passes validation.

### Step 6: Check for Existing Agents

Before generating, check `~/.claude/agents/` for agents that already exist and could be reused or adapted. Common ones to watch for:

- `research-assistant` — web research
- `content-reviewer` — writing review
- `code-reviewer` — code quality analysis
- `devils-advocate` — critical analysis
- `vault-master` — Obsidian vault operations

If an existing agent covers part of the workflow, suggest reusing it rather than creating a duplicate. Note which existing agents to integrate and which new ones to create.

### Step 7: Generate Agent Files

Read `references/agent-template.md` for the exact format. For each new agent, generate a .md file with:

**Frontmatter:**
```yaml
---
name: [kebab-case-name]
description: "[What this agent does. Part of the [team-name] pipeline.]"
tools:
  - [minimal tool list]
model: [haiku/sonnet/opus — only if not haiku]
---
```

**Body structure:**
1. Role declaration — "You are a [function]. Your job is to [responsibility]."
2. Input section — what it receives, from where, in what format
3. Process section — numbered steps
4. Output format — exact template with ASCII separators and named fields
5. Rules section — guardrails, constraints, edge cases, British English

Save each file to the current working directory as `[agent-name].md`.

### Step 8: Generate Orchestration Skill (Optional)

Generate an orchestration skill if:
- The team has 3+ agents
- The pattern involves conditional dispatch or parallel fan-out
- The coordination logic is non-trivial

The skill follows the telegram-pipeline structure:

```markdown
---
name: [team-name]-pipeline
description: "[What the pipeline does. When to trigger it.]"
---

# [Team Name] Pipeline

[Brief description of what this pipeline does end-to-end.]

## Pipeline Flow

### Step 1: [First Agent]

Dispatch the **[agent-name]** with the input.

Agent(subagent_type="[agent-name]", prompt="[what to pass]")

Read the result. [Decision logic if conditional.]

### Step 2: [Second Agent]

[Continue the flow...]

## Error Handling

- If [agent] fails: [what to do]
- If [agent] returns incomplete data: [fallback]

## When to Short-Circuit

[Conditions where the pipeline can skip steps or exit early.]
```

Save to the current working directory as `[team-name]-pipeline/SKILL.md`.

### Step 9: Deliver

Present the complete package:

```
AGENT TEAM GENERATED
═══════════════════════════════════════

Team: [name]
Pattern: [pattern]
Agents: [count new] + [count reused existing]

Files created:
  [agent-name-1].md    — [role summary]
  [agent-name-2].md    — [role summary]
  [agent-name-3].md    — [role summary]
  [team]-pipeline/     — orchestration skill
    SKILL.md

To install:
  cp [agent-name-*.md] ~/.claude/agents/
  cp -r [team]-pipeline/ ~/.claude/skills/

Existing agents to integrate:
  [existing-agent]     — [how it fits]

═══════════════════════════════════════
```

Offer refinements — swap responsibilities, add/remove agents, change model tiers, adjust handoff formats, add error paths.

---

## Complexity Handling

### Simple teams (2-3 agents)

- Compress steps 2-5 into a single pass — design inline without the formal canvas
- Likely sequential pipeline or conditional dispatch
- Skip the orchestration skill — describe coordination in agent descriptions
- Generate and deliver in one go

### Medium teams (3-5 agents)

- Full canvas + validation
- Generate orchestration skill
- Present topology diagram
- Consider whether any existing agents can be reused

### Complex teams (5+ agents)

- Full canvas + validation + anti-pattern check
- Consider splitting into sub-teams (e.g. a "research team" and a "generation team")
- Generate orchestration skill with error handling and performance notes
- Suggest file-based state for baton-passing between sub-teams
- Recommend staging: build and test 2-3 core agents first, add the rest after

---

## Autonomous Teams

Some teams run without human involvement — triggered by schedules, hooks, or external events. When the user wants a fully autonomous agent team, the design needs extra considerations.

### What Makes a Team Autonomous

An autonomous team runs end-to-end without human input. This requires:

1. **A trigger mechanism** — how does the team start?
   - **Scheduled task** — cron-based via `~/.claude/scheduled-tasks/`. The task prompt dispatches the first agent
   - **Hook** — a Claude Code hook (Notification, PostToolUse, etc.) fires and launches the pipeline
   - **External event** — a webhook, Telegram message, or file change triggers a skill that dispatches agents
   - **Baton file** — the previous iteration left a `next-prompt.md` that the orchestrator picks up

2. **Self-contained decision logic** — every branch and decision must be handled by an agent, not deferred to the user. The triage agent pattern is key here: a cheap classifier (haiku) makes the routing decision, and specialist agents handle each path.

3. **Termination conditions** — the team must know when to stop:
   - Pipeline reaches the final step and delivers output
   - Loop hits a quality threshold or max iteration count
   - Classifier determines no action is needed (short-circuit)

4. **Error recovery** — what happens when an agent fails without a human to notice:
   - **Retry once** — transient failures (rate limits, timeouts)
   - **Degrade gracefully** — skip the failed step, note the gap in output
   - **Alert the user** — send a Telegram message or write to a log file
   - **Never loop forever** — always include a max-retry or max-iteration guard

5. **Output delivery** — how does the result reach the user?
   - Write to a file (vault, project directory)
   - Send via Telegram (`@Claudwozzabot`)
   - Create a draft (email, PR)
   - Update a status file that another process reads

### Autonomous Design Additions

When designing an autonomous team, add these to the canvas for each agent:

- **Timeout**: How long should this agent be allowed to run? (default: 120 seconds)
- **Max retries**: How many times to retry on failure? (default: 1)
- **Fallback output**: What does the agent return if it can't complete?
- **Logging**: Should the agent write its output to a log file for debugging?

And for the orchestration skill:

- **Trigger section**: How the pipeline starts (cron expression, hook event, or manual)
- **Circuit breaker**: Stop the pipeline if N consecutive runs fail
- **Notification on completion**: Send results via Telegram, write to vault, or log
- **State persistence**: For loops, where is state stored between iterations?

### Generating Autonomous Pipelines

When generating the orchestration skill for an autonomous team:

1. Include the trigger mechanism at the top of the skill (scheduled task config or hook definition)
2. Add a `## Monitoring` section describing how to check if the pipeline is running correctly
3. Add a `## Failure Modes` section listing what can go wrong and how each failure is handled
4. Include an iteration/run counter for loops to prevent infinite execution
5. End with output delivery — the result must go somewhere the user will see it

### Real Example: Telegram Pipeline (Fully Autonomous)

The telegram pipeline is the canonical autonomous team:
- **Trigger**: Notification hook fires on incoming Telegram message
- **Decision logic**: triage-agent classifies and routes (no human needed)
- **Conditional execution**: research-agent only runs if triage says needed
- **Output delivery**: reply sent directly via Telegram
- **Short-circuit**: greetings and casual messages get instant responses
- **Deduplication**: message_id tracking prevents double-processing
- **Error handling**: graceful fallback if any agent fails

---

## Resources

When you need detailed reference material during the workflow:

| Step | Load this reference |
|---|---|
| Pattern selection (Step 3) | `references/orchestration-patterns.md` — 5 patterns with diagrams, real examples, and guidance |
| Team design (Step 4) | `references/team-design-canvas.md` — structured per-agent design framework |
| Validation (Step 5) | `references/anti-patterns.md` — 10 common mistakes and how to fix them |
| File generation (Step 7) | `references/agent-template.md` — canonical agent format, model/tool guides |
