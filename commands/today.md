Generate my daily to-do list for today.

## Steps

1. Read `Tasks/index.md` to understand the task system
2. Scan all `.md` files in `Tasks/` and read their YAML front matter
3. Read `Personal/routines.md` for today's schedule context
4. Read `Personal/goals.md` for current priorities
5. Check what day of the week it is

## Output

Produce a focused daily briefing in this format:

### Today — [Day, Date]

**Top priorities** (max 3 — the most important things to move forward today)
- [ ] ...

**Other tasks** (anything else with status: todo or in-progress, sorted by priority)
- [ ] ...

**Blocked** (anything with status: blocked — flag why if the file says)
- ...

**Completed recently** (anything marked done in the last 7 days — quick wins to feel good about)
- ...

**Schedule notes** (based on routines.md — any relevant context for today)
- ...

## Rules

- Only include tasks with status `todo` or `in-progress` in the active lists
- High priority tasks always go in Top priorities
- If there are more than 3 high-priority tasks, flag that as a warning — too many priorities means no priorities
- Keep it short and scannable — no paragraphs
- If a task has a due date that's today or overdue, mark it with (OVERDUE) or (DUE TODAY)
- If Tasks/ is empty or has no actionable items, say so and suggest adding some
