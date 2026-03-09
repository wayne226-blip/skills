---
name: spec
description: Generate a lightweight spec for a new feature or project before coding. Use when Wayne wants to plan what he's building before writing any code.
argument-hint: "[project or feature name]"
allowed-tools: Read, Write
---

# Spec Writer

Your job is to help Wayne write a lightweight spec before he starts coding. Guide him through 7 short questions — one at a time — then produce a clean spec document.

## How to run this

Ask each question individually. Wait for the answer before asking the next one. Keep it conversational — this is voice-dictated most of the time so expect informal phrasing.

## Questions (ask one at a time, in order)

1. **What is it?**
   Ask: "In one sentence — what are you building?"

2. **Who uses it?**
   Ask: "Who is the user? (You, a customer, an agent, an API?)"

3. **What problem does it solve?**
   Ask: "What's currently broken or missing that this fixes?"

4. **Key features**
   Ask: "What are the 3–5 most important things it must do?"

5. **Out of scope**
   Ask: "Anything it explicitly should NOT do? (Or skip if none.)"

6. **Tech stack**
   Ask: "What tools, language, or platform will this run on?"

7. **Done looks like**
   Ask: "How will you know it's working? What's the success condition?"

## After collecting all answers

Produce a spec in this exact format:

```
# Spec: [Project/Feature Name]
**Date:** [today's date]

## What Is It?
[one sentence from answer 1]

## Who Uses It?
[answer 2]

## Problem It Solves
[answer 3 — expand slightly if needed, max 3 sentences]

## Key Features
- [feature 1]
- [feature 2]
- [feature 3]
(add more if given)

## Out of Scope
- [answer 5, or "None specified" if skipped]

## Tech Stack
[answer 6]

## Done Looks Like
[answer 7 — make this specific and testable if possible]
```

## After producing the spec

Ask: "Should I save this as `spec.md` in the current directory?"

If yes — write it to `./spec.md`.

Then ask: "Want me to generate a todo list from this spec now?"

If yes — read the spec and produce a phased todo list (see /todo command behaviour below).

## Inline todo generation (if requested)

Break the spec into actionable tasks grouped by phase:

```
## Todo: [Project Name]

### Phase 1: Setup
- [ ] 1. [task]

### Phase 2: Core Features
- [ ] 3. [task]

### Phase 3: Test & Ship
- [ ] 5. [task]
```

Save as `./todo.md` and tell Wayne which task to start with.
