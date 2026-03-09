Mark a task as done.

The user will say which task after the command: $ARGUMENTS

## Steps

1. Scan all `.md` files in `Tasks/` and read their YAML front matter
2. Find the task that best matches what the user described (fuzzy match on title)
3. Update the YAML front matter: set `status: done` and add `completed: [today's date]`
4. Confirm which task was marked done
5. If no match found, list the current tasks and ask which one they meant
