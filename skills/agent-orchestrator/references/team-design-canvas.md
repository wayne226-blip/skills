# Team Design Canvas

A structured framework for designing each agent in a multi-agent team. Fill this in before generating any files — thinking through contracts upfront prevents the most common integration failures.

---

## Team Overview

Fill this in first:

```
TEAM DESIGN CANVAS
═══════════════════════════════════════

Task: [What the team does end-to-end, one sentence]
Pattern: [Sequential Pipeline / Parallel Fan-Out / Baton-Passing Loop / Conditional Dispatch / Hybrid]
Trigger: [How the team is invoked — manually, scheduled, webhook, skill, etc.]
Agent count: [N]

═══════════════════════════════════════
```

---

## Per-Agent Canvas

Fill in one of these for each agent:

```
───────────────────────────────────────
AGENT: [kebab-case-name]
───────────────────────────────────────
Responsibility: [One sentence — what is this agent's single job?]
Model: [haiku / sonnet / opus] — [one-line justification]
Tools: [Minimal list — justify each tool]

Input contract:
  From: [which agent or external trigger sends data to this agent]
  Format: [structured text / JSON / file path / plain text]
  Fields:
    - [field_name]: [type] — [description]
    - [field_name]: [type] — [description]

Output contract:
  To: [which agent(s) receive this output]
  Format: [structured text / JSON / file path / plain text]
  Fields:
    - [field_name]: [type] — [description]
    - [field_name]: [type] — [description]

Error handling:
  On failure: [retry / skip / degrade / report]
  Fallback: [what the orchestrator does if this agent can't complete]

Notes: [Any special considerations — performance, cost, edge cases]

# Additional fields for autonomous teams:
Timeout: [max seconds this agent should run, default 120]
Max retries: [how many times to retry on failure, default 1]
Fallback output: [what to return if the agent can't complete]
───────────────────────────────────────
```

---

## Team Health Checklist

After filling in all agents, verify:

**Contracts match:**
- [ ] Every output contract has a matching input contract on the receiving agent
- [ ] Field names and types are consistent across the handoff
- [ ] No agent expects data that no other agent produces

**Tools are minimal:**
- [ ] No tool appears that isn't needed for the agent's stated responsibility
- [ ] Read-only agents don't have Write/Edit
- [ ] Routing agents don't have WebSearch/WebFetch

**Models are justified:**
- [ ] Simple tasks use haiku (routing, classification, formatting)
- [ ] Complex reasoning uses sonnet or opus
- [ ] No agent uses opus without a clear reason

**Errors are handled:**
- [ ] Every agent has a defined failure behaviour
- [ ] The orchestrator knows what to do if any agent fails
- [ ] There's no scenario where a failure silently drops data

**No redundancy:**
- [ ] No two agents have overlapping responsibilities
- [ ] The team is the minimum size needed for the task
- [ ] Every agent earns its place — remove any that don't

---

## Topology Diagram

Draw the agent connections using this format:

```
┌──────────────┐     ┌──────────────┐
│  agent-name  │────>│  agent-name  │
│  [model]     │     │  [model]     │
│  Tools: X, Y │     │  Tools: Y, Z │
└──────────────┘     └──────────────┘
```

Use `────>` for sequential flow, split arrows for fan-out, and `─ ─ >` (dashed) for conditional/optional paths.
