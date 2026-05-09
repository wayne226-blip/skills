# Multi-Agent Anti-Patterns

Common mistakes when designing agent teams. Check every design against this list before generating files.

---

| # | Anti-Pattern | What It Looks Like | Why It's a Problem | Fix |
|---|---|---|---|---|
| 1 | **Tool Bloat** | Agent has 8+ tools, most unused in practice | Extra tools widen the agent's action space, making it more likely to wander off-task. Also increases the system prompt size | Strip to the minimum set needed for this agent's specific job. If in doubt, remove the tool and see if the agent still works |
| 2 | **Role Overlap** | Two agents both "analyse and summarise" the same thing | Duplicate work, conflicting outputs, wasted tokens | Split responsibilities cleanly — one analyses, the other summarises. Single responsibility per agent |
| 3 | **Missing Handoff** | Agent produces output but there's no defined format for the next agent to consume | The receiving agent has to guess what it's getting, leading to fragile parsing and inconsistent behaviour | Define an explicit output contract with named fields and a structured template |
| 4 | **Vague Output** | Output spec says "pass the relevant information" | "Relevant" is subjective — the agent will include too much or too little, and the next agent can't reliably extract what it needs | Specify exact fields: "Return: category, urgency, summary, research_needed" with types and examples |
| 5 | **Model Waste** | Using opus for a simple router/classifier that just picks a category | Opus is 10x+ the cost and slower. For classification tasks, haiku is equally accurate and much faster | Use haiku for routing and classification. Reserve opus for tasks that demonstrably need deep reasoning |
| 6 | **Tool Excess** | A read-only review agent has Write and Edit tools | The agent might write files it shouldn't, or the extra tools create decision paralysis about whether to read or edit | Remove tools the agent doesn't need. A reviewer reads; a builder writes. Keep the roles clean |
| 7 | **Circular Dependencies** | Agent A needs Agent B's output, which needs Agent A's output | Deadlock — neither agent can start. Or infinite loop if they keep calling each other | Redesign the topology. Usually means a missing third agent that produces the shared dependency, or a loop needs a termination condition |
| 8 | **God Agent** | One agent has 5+ responsibilities and does everything | Too much complexity in one agent leads to unfocused output, longer prompts, and harder debugging | If an agent has more than 2-3 distinct responsibilities, split it into focused specialists |
| 9 | **No Error Path** | Pipeline assumes every agent always succeeds | In practice, agents fail (bad input, rate limits, hallucination). Without a fallback, the whole pipeline silently breaks | Define what happens when each agent fails: retry, skip with degraded output, or report the failure clearly |
| 10 | **Over-Engineering** | 6 agents for a task that needs 2 | Every agent adds latency, cost, and complexity. Small teams are easier to debug, faster to run, and cheaper | Start with the minimum viable team. Add agents only when you can point to a specific limitation that requires it |
| 11 | **Runaway Loop** | Autonomous baton-passing loop with no max iteration count | Without a termination condition, a loop can run forever burning tokens and producing garbage. This is the #1 autonomous team failure mode | Always include: max_iterations guard, quality threshold check, and a "circuit breaker" that stops after N consecutive failures |
| 12 | **Silent Failure** | Autonomous pipeline fails but nobody notices | Without a human watching, a failed pipeline just... stops. The user never gets their output and doesn't know why | Every autonomous team needs an alerting mechanism: Telegram notification, log file write, or status file that a monitoring task checks |

---

## Quick Validation Checklist

Run through this for every agent in the design:

- [ ] Does this agent have a single, clear responsibility?
- [ ] Are all its tools actually used in its process?
- [ ] Is the model tier justified? (Could haiku handle this?)
- [ ] Is the output format explicitly defined with named fields?
- [ ] Does the output format match what the receiving agent expects as input?
- [ ] Is there a defined behaviour when this agent fails?
- [ ] Does this agent's responsibility overlap with any other agent?

And for the team as a whole:

- [ ] Can you draw the topology clearly? (If not, simplify)
- [ ] Is the total agent count the minimum needed?
- [ ] Are there any circular dependencies?
- [ ] Does every output have a consumer? (No dangling outputs)
- [ ] Does every input have a producer? (No missing dependencies)
