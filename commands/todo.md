---
name: todo
description: Convert a spec into a phased, numbered todo list. Run after /spec or when Wayne has a spec.md and wants actionable tasks broken out.
argument-hint: "[optional: path to spec file]"
allowed-tools: Read, Write, Glob
---

# Todo Generator

Convert a spec into a clear, phased todo list that Wayne can work through task by task.

## Finding the spec

1. If an argument was passed, read that file.
2. Otherwise, look for `./spec.md` in the current directory.
3. If neither exists, ask Wayne to paste the spec or run `/spec` first.

## How to break it down

Read the spec and produce tasks in phases. Think about what must happen before each other thing — don't list tasks in random order.

### Phase 1: Setup
Foundation work — project structure, dependencies, API keys, config files, base scaffolding.

### Phase 2: Core Features
The key features listed in the spec, one task per feature. Break complex features into sub-tasks if needed.

### Phase 3: Test & Polish
Manual testing against the "Done looks like" criteria, error handling, edge cases, UX cleanup.

### Phase 4: Ship (if applicable)
Deploy, publish, or hand off. Only include if relevant to the spec.

## Output format

```
# Todo: [Project Name]
**Generated from:** spec.md
**Date:** [today]

### Phase 1: Setup
- [ ] 1. [specific actionable task]
- [ ] 2. [specific actionable task]

### Phase 2: Core Features
- [ ] 3. [specific actionable task]
- [ ] 4. [specific actionable task]
- [ ] 5. [specific actionable task]

### Phase 3: Test & Polish
- [ ] 6. [test against success criteria from spec]
- [ ] 7. [handle edge cases]

### Phase 4: Ship
- [ ] 8. [deploy / publish step]
```

## Rules for good tasks

- Each task should be doable in one sitting (1–3 hours max)
- Tasks should be specific — not "build the UI", but "create the HTML form with fields for name, email, and message"
- Reference the tech stack from the spec when describing tasks
- The first task should always be something Wayne can start immediately

## After generating

Save the todo list as `./todo.md`.

Tell Wayne: "Start with task 1: [first task description]."
