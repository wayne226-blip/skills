Create a new task file in `Tasks/`.

The user will describe the task in plain English after the command: $ARGUMENTS

## Steps

1. Parse what the user said into a task title and details
2. Ask the user for priority (high/medium/low) and area (work/personal/writing/kdp/salesnote) — if obvious from context, just pick it
3. Create a new `.md` file in `Tasks/` using this format:

```
---
title: [task title]
status: todo
priority: [high|medium|low]
area: [area]
created: [today's date YYYY-MM-DD]
due: [if mentioned, otherwise blank]
---

# [Task title]

## What
[Details from user input]

## Notes

```

4. Confirm the task was created with the filename and key details
