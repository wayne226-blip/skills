---
name: parallel-research
description: >
  Deep-dive research on any broad topic by automatically splitting it into 10 focused
  subtopics and researching each one simultaneously with a dedicated agent. Use this
  skill whenever the user asks for comprehensive research, wants to thoroughly explore
  a subject from multiple angles, or needs broad coverage of a topic quickly. Trigger
  on phrases like "research [topic]", "find out everything about", "give me a deep
  dive on", "I need comprehensive research on", "explore all aspects of", or any time
  the user wants to cover a topic exhaustively rather than superficially. Also trigger
  when the user explicitly mentions using multiple agents, parallel research, or wants
  ten agents. Even when a user just says "research X for me" — use this skill.
---

# Parallel Research Skill

This skill gives any broad topic thorough, multi-angle coverage by splitting it into
10 focused subtopics and researching each one simultaneously with a dedicated agent.
The result is a fast, comprehensive set of summaries that together cover the full
landscape of a subject.

---

## Step 1: Decompose the topic into 10 subtopics

Before spawning any agents, think carefully about how to divide the user's topic.
The goal is 10 subtopics that:

- Are **distinct and non-overlapping** — each one is its own angle, not a repeat
- Are **specific enough** to be researched independently in a focused way
- **Together give comprehensive coverage** of the whole subject
- **Balance breadth and depth** — not so narrow they're trivial, not so broad they're vague

**Example** — for the topic "electric vehicles":
1. Battery technology and energy density
2. Charging infrastructure and grid demand
3. Market leaders and competitive landscape
4. Government policy, incentives and regulation
5. Consumer adoption trends and barriers
6. Environmental impact vs. fossil fuels (lifecycle analysis)
7. Total cost of ownership vs. ICE vehicles
8. Autonomous driving integration
9. Supply chain and raw materials (lithium, cobalt, nickel)
10. Future outlook and next-generation technology

**Present the 10 proposed subtopics to the user** and ask them to confirm or suggest
changes before spawning the agents. Keep this quick — a simple numbered list and
"Does this look good, or would you like to adjust any?" is enough. Don't over-explain.

---

## Step 2: Spawn 10 agents in parallel

Once the subtopics are confirmed, launch **all 10 agents in a single message** using
10 simultaneous Task tool calls. Every agent must start at the same time — do not
wait for one to finish before launching the next. Parallel execution is what makes
this skill fast.

Use this prompt template for each agent (fill in the bracketed fields):

```
You are a focused research agent. Research the subtopic below and produce a
thorough, well-structured summary.

**Main topic**: [user's original topic]
**Your subtopic**: [specific subtopic N]

Instructions:
- Use web search to find current, accurate, and reliable information
- Write 3–5 paragraphs covering the key facts, trends, data points, and insights
- Include specific statistics, examples, or named sources where available
- Note any significant debates, open questions, or areas of uncertainty
- Start your response with the subtopic as a heading (e.g., ## Battery Technology)
- Write only your research summary — no preamble, no meta-commentary
```

Set `subagent_type: "general-purpose"` for each agent so it has web search access.

---

## Step 3: Collect and present the results

Once all 10 agents have returned, present their summaries to the user in order,
using each subtopic as a heading. Keep the outputs as the agents wrote them —
do not merge, rewrite, or condense unless the user asks.

If any agent failed or returned a thin result, flag it clearly and offer to re-run
that subtopic.

End with a brief note: "All 10 subtopics are above — let me know if you'd like me
to go deeper on any of them, combine them into a single report, or export to a file."

---

## Tips for good subtopic design

The quality of the research depends heavily on how well the topic is split. A few
things that help:

- **Avoid chronological splits** ("history of X", "future of X") — they tend to
  overlap badly. Use thematic angles instead.
- **Think about who cares** — policy, business, technology, environment, consumers
  are usually distinct enough angles for most topics.
- **Adjust for topic size** — for very narrow topics, it's better to have 10 highly
  specific angles than 10 vague ones. For very broad topics, use high-level
  categories that each have their own depth.
