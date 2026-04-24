# Orchestration Patterns

Five proven patterns for multi-agent systems. Each includes when to use it, a topology diagram, a real-world example, and guidance on agent design.

---

## 1. Sequential Pipeline

**One-liner:** Agents run in order, each transforming or enriching data for the next step.

**When to use:**
- Steps must happen in a fixed order
- Each step's output is the next step's input
- Early steps filter or classify, later steps do heavy work

**Topology:**
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Agent A  │────>│  Agent B  │────>│  Agent C  │
│  (filter) │     │ (process) │     │ (format)  │
└──────────┘     └──────────┘     └──────────┘
```

**Real example — Telegram Pipeline:**
```
triage-agent (haiku)  ──>  research-agent (haiku)  ──>  response-agent (haiku)
  Categorise message         Gather information          Draft reply
  Decide what's needed       Search codebase/web/vault   Match Wayne's voice
  Output: structured         Output: findings            Output: plain text
          triage result               (max 500 words)            reply
```

**Agent design guidance:**
- Earlier agents should be cheaper (haiku) — they filter and route
- Later agents can be more capable if they do the heavy lifting
- Each agent's output format must be explicitly defined so the next agent can parse it
- Tool sets should narrow through the pipeline — the final agent often needs the fewest tools

**Handoff mechanism:** Structured text blocks passed via the orchestrating prompt. Each agent returns a formatted result that the orchestrator includes in the next agent's prompt.

**Error handling:** If an early agent fails, the pipeline stops — no point running later steps. If a late agent fails, the orchestrator can retry it with the same input from the previous step.

**Strengths:** Simple to reason about, easy to debug (check each step's output), clear data flow.
**Limitations:** Slow for long pipelines (each step waits for the previous one), brittle if any step fails.

---

## 2. Parallel Fan-Out

**One-liner:** Multiple agents process the same input independently, then results are collected and combined.

**When to use:**
- You need multiple perspectives on the same input
- Tasks are independent — no agent needs another's output
- Speed matters — parallel is faster than sequential for independent work
- Evaluation, quality assurance, or multi-criteria analysis

**Topology:**
```
                 ┌──────────┐
            ┌───>│ Agent A   │───┐
            │    │ (aspect 1)│   │
┌────────┐  │    └──────────┘   │    ┌───────────┐
│  Input  │──┤                   ├───>│ Collector  │
└────────┘  │    ┌──────────┐   │    └───────────┘
            │    │ Agent B   │   │
            ├───>│ (aspect 2)│───┤
            │    └──────────┘   │
            │    ┌──────────┐   │
            └───>│ Agent C   │───┘
                 │ (aspect 3)│
                 └──────────┘
```

**Real example — Multi-Reviewer Code Review:**
```
                 ┌─────────────────────┐
            ┌───>│ security-reviewer    │───┐
            │    │ (opus) Read,Grep,Glob│   │
┌────────┐  │    └─────────────────────┘   │    ┌──────────────────┐
│ PR diff │──┤                              ├───>│ review-summariser │
└────────┘  │    ┌─────────────────────┐   │    │ (sonnet) Read     │
            ├───>│ performance-reviewer │───┤    └──────────────────┘
            │    │ (sonnet) Read,Grep  │   │
            │    └─────────────────────┘   │
            └───>┌─────────────────────┐   │
                 │ style-reviewer       │───┘
                 │ (haiku) Read,Grep   │
                 └─────────────────────┘
```

**Agent design guidance:**
- All fan-out agents must use the same output format so the collector can parse them uniformly
- Each agent should focus on a distinct aspect — if they overlap, you'll get redundant findings
- The collector/summariser is usually a separate agent that merges and deduplicates
- Fan-out agents can use different model tiers based on complexity of their aspect

**Handoff mechanism:** The orchestrator dispatches all fan-out agents with the same input, collects their outputs, and passes them to the collector agent.

**Error handling:** If one fan-out agent fails, the others can still complete. The collector should note which aspects are missing and flag gaps in coverage.

**Strengths:** Fast (parallel execution), independent failure, good for comprehensive analysis.
**Limitations:** All agents get the same context (no enrichment between them), collector must handle variable-quality inputs.

---

## 3. Baton-Passing Loop

**One-liner:** A single agent (or small team) iterates, writing state to a file as a "baton" for the next iteration.

**When to use:**
- Iterative refinement where the number of passes isn't known upfront
- Building something incrementally (pages of a site, chapters of a doc)
- Quality-gated loops — keep going until a standard is met
- Long-running generation that exceeds a single agent's capacity

**Topology:**
```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Agent    │────>│  State File  │────>│  Agent   │──> ...
│ (pass 1)  │     │ (the baton)  │     │ (pass 2) │
└──────────┘     └──────────────┘     └──────────┘
                        │
                  metadata.json
                  next-prompt.md
```

**Real example — Stitch Build Loop:**
```
Pass 1: Agent reads .stitch/next-prompt.md
  └─> Generates homepage
  └─> Writes new baton: "Build the About page next"
  └─> Updates .stitch/metadata.json

Pass 2: Agent reads .stitch/next-prompt.md
  └─> Generates About page
  └─> Writes new baton: "Build the Contact page next"
  └─> Updates metadata

(Continues until sitemap is complete)
```

**Agent design guidance:**
- The baton file must contain everything the next pass needs — no assumptions about prior context
- Include a termination condition (sitemap complete, quality score above threshold, max iterations)
- State files should be human-readable so you can debug by reading the baton
- The agent in each pass can be the same agent type or different specialists

**Handoff mechanism:** File-based state. The baton (e.g. `next-prompt.md`) contains the task for the next pass. Metadata (e.g. `metadata.json`) tracks overall progress and accumulated state.

**Error handling:** If a pass fails, the baton file still contains the task — you can retry the same pass. Include a pass counter to detect infinite loops.

**Strengths:** Handles unbounded iteration, persistent state survives crashes, human can inspect/modify the baton between passes.
**Limitations:** Sequential (one pass at a time), requires careful baton design, can loop forever without a termination condition.

---

## 4. Conditional Dispatch

**One-liner:** A classifier/router agent examines the input and dispatches to different specialist agents based on the classification.

**When to use:**
- Different input types need different processing
- A router can reliably classify the input
- Specialist agents are more effective than one generalist
- You want to avoid running unnecessary agents

**Topology:**
```
                         ┌──────────────┐
                    ┌───>│ Specialist A  │
                    │    └──────────────┘
┌──────────┐   ┌───┴───┐
│  Input    │──>│Router  │
└──────────┘   │(haiku) │
               └───┬───┘
                    │    ┌──────────────┐
                    ├───>│ Specialist B  │
                    │    └──────────────┘
                    │    ┌──────────────┐
                    └───>│ Specialist C  │
                         └──────────────┘
```

**Real example — Telegram Triage Short-Circuit:**
```
triage-agent classifies the message:
  ├─ greeting/casual → Short-circuit (reply directly, no other agents)
  ├─ question/task   → Full pipeline (research + response agents)
  └─ urgent          → Full pipeline with priority flag
```

**Agent design guidance:**
- The router MUST be fast and cheap (haiku) — it runs on every input
- Router needs only classification tools (Read, Grep) — no heavy processing
- Specialist agents can be more capable (sonnet/opus) since they only run when needed
- Define clear classification categories with no overlap
- Include a fallback/default route for unclassifiable inputs

**Handoff mechanism:** The router returns a classification result (category, confidence, routing decision). The orchestrator reads the result and dispatches the appropriate specialist.

**Error handling:** If the router can't classify, route to the most general specialist. If a specialist fails, the router's classification can be used to retry with a different specialist or escalate.

**Strengths:** Efficient (only runs needed agents), specialist agents are more focused, easy to add new routes.
**Limitations:** Router accuracy is critical — misclassification sends to wrong specialist, adding routes requires updating the router.

---

## 5. Hybrid

**One-liner:** Combines two or more patterns for complex workflows.

**When to use:**
- The workflow has both sequential AND parallel sections
- Some steps branch conditionally while others always run
- Real-world tasks rarely fit a single pure pattern

**Common combinations:**
- **Conditional + Sequential:** Route first, then run a pipeline for the selected path (Telegram pipeline does this)
- **Sequential + Parallel:** Process sequentially until a fan-out step, collect results, continue sequentially
- **Loop + Pipeline:** Each loop iteration runs a full pipeline internally

**Topology example — Conditional + Sequential + Parallel:**
```
┌────────┐   ┌────────┐
│ Router  │──>│ Path A │──> Sequential pipeline
│ (haiku) │   └────────┘
└────┬───┘
     │       ┌────────┐     ┌─────┐  ┌─────┐
     └──────>│ Path B │──>  │ B1  │  │ B2  │  ──> Collector
             └────────┘     └─────┘  └─────┘
                            (parallel fan-out)
```

**Design guidance:**
- Draw the topology first — if you can't draw it, you can't build it
- Keep the total agent count reasonable — every agent adds latency and cost
- Identify which sub-patterns apply to which sections
- The orchestration skill becomes more important for hybrids — it's the glue

**Error handling:** Each sub-pattern uses its own error handling. The orchestration skill must define what happens when one section fails — does the whole workflow stop, or can other sections continue?

---

## Pattern Selection Quick Reference

| Signal in the workflow | Recommended pattern |
|---|---|
| Steps must run in order, each feeding the next | Sequential Pipeline |
| Multiple independent evaluations of the same input | Parallel Fan-Out |
| Iterative refinement until a quality bar is met | Baton-Passing Loop |
| Different input types need different processing | Conditional Dispatch |
| Workflow has both sequential and parallel sections | Hybrid |
| Simple 2-step process | Might not need a pattern — just 2 agents |
