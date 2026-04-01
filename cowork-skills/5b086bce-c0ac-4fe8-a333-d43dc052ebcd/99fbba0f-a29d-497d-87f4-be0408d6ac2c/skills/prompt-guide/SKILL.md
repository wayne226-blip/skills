---
name: prompt-guide
description: >
  Transforms any Claude prompt using Anthropic's official best practices. ALWAYS use
  this skill — do not answer informally — when the user: asks you to write, improve,
  fix, or review any prompt or system prompt; asks "what would the system prompt look
  like?"; asks how to get Claude to do something specific; pastes a prompt and asks
  what you think or why it isn't working; mentions their prompt gives inconsistent
  results or output that's too long/short/wrong format; asks whether to use XML tags,
  role definitions, or examples in prompts. The skill produces a structured three-part
  response that Claude does not produce naturally on its own: (1) Diagnosis — specific
  problems identified; (2) Improved Prompt — rewritten with role, XML structure,
  output constraints, and a worked example; (3) What Changed — reasoning for every
  decision. This structured output is the whole point. Always run this skill rather
  than answering the prompt question casually.
---

# Prompt Guide Skill

Transform rough, vague, or unstructured prompts into well-engineered Claude prompts.
Apply Anthropic's best practices and return a refined version with a brief explanation
of what changed and why.

## Core Best Practices (your checklist)

Work through these when analysing any prompt:

1. **Role** — Does it open with a clear role in the system prompt? ("You are a...")
2. **Clarity** — Are instructions specific and direct? Does it say what TO do, not just what to avoid?
3. **Context / motivation** — Are the reasons behind instructions explained, not just the rules?
4. **Structure** — Are mixed inputs (context, instructions, data, examples) separated with XML tags?
5. **Context placement** — Is long background content placed BEFORE the query/task?
6. **Examples** — For any prompt that generates written output — emails, messages, support replies, summaries, reports, creative tasks — always include a worked `<example>` block with a realistic input → output pair. Examples are the single most powerful quality lever after role definition: they show the model exactly what "good" looks like, which is far more precise than describing it in words. When in doubt, add one.
7. **Output format** — Is the desired format stated explicitly (prose, JSON, length, markdown use)?
8. **Tool use** (agentic prompts only) — Is there a `<tool_use>` block with parallel/sequential guidance?
9. **Safety** (agentic prompts only) — Is there a `<safety>` block covering reversible vs. risky actions?

Not every prompt needs all nine. Use judgement — a simple one-turn prompt doesn't need a safety block.

## Output Structure

Always produce exactly three sections:

### 1. Diagnosis
2–4 bullet points identifying what's weak or missing in the original prompt.
Be specific — "no role defined" is better than "unclear".

### 2. Improved Prompt
The full rewritten prompt in a fenced code block (so it's easy to copy).
Use XML tags to separate sections. Use `{{PLACEHOLDER}}` style for any variable content
the user will fill in.

### 3. What Changed
A short bulleted list explaining each significant change and *why* it helps.
Keep this concise — one line per change. Focus on the reasoning, not just the label.

## Key Patterns

**Positive over negative**
- Instead of: "Don't use bullet points"
- Use: "Write your response as flowing prose paragraphs."

**Context before query**
Place `<context>` blocks above `<instructions>` and the actual `<input>`.
For long documents, this can improve response quality by up to 30%.

**XML structure for complex prompts**
Use `<system>`, `<context>`, `<instructions>`, `<examples>`, `<input>` as needed.
For very simple prompts (one-turn, no variable content), plain prose is fine — don't over-engineer.

**Examples pattern**

Use whenever the prompt involves any kind of writing, tone, format, or style:
emails, support replies, summaries, reports, creative content, structured data generation.

```xml
<examples>
  <example>
    <input>User's input here</input>
    <output>Expected output here</output>
  </example>
</examples>
```

Write the example content yourself — make it realistic and representative of what
a good response looks like. A placeholder that says "your output here" is useless;
a concrete example is the whole point.

**Role line**
```
You are a [specific role] specialising in [domain].
```

**Agentic tool_use block**
```xml
<tool_use>
Where multiple tool calls have no dependencies, make them in parallel.
For dependent calls, run them sequentially. Never guess missing parameters.
</tool_use>
```

**Agentic safety block**
```xml
<safety>
Prefer reversible, local actions (reading files, running tests).
For destructive or externally visible actions (deleting files, pushing code, sending messages),
confirm with the user first.
</safety>
```

## Tone

Be direct and practical. Wayne is learning — a brief explanation of *why* each change
matters is more useful than just showing the finished product. But don't lecture.
One clear sentence per change is enough.

If the original prompt is already solid, say so and explain why — don't invent problems to fix.
