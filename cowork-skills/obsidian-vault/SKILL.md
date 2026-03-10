---
name: obsidian-vault
description: >
  Knows where Wayne's Obsidian vault is located and helps with any tasks
  involving it — reading notes, searching for content, creating new notes,
  organising files, or working with the vault in any way. Use this skill
  whenever the user mentions Obsidian, their vault, their notes, or asks
  to find, read, create, or edit any note or markdown file in their
  knowledge base. Trigger even for casual mentions like "check my notes on X",
  "add this to my vault", "what do I have on Y in Obsidian", or "open my
  Obsidian folder". ALWAYS trigger immediately when the user types /vault
  at the start of their message — this is a direct command shortcut for
  this skill.
---

# Obsidian Vault

## Vault location

Wayne's Obsidian vault is at:

```
/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza
```

This is the root of the vault. All notes and folders live inside here.

## /vault command

When Wayne types `/vault` followed by anything (e.g. `/vault show my AI notes`, `/vault add a new note about X`, `/vault search for Y`), treat it as a direct instruction to work with the Obsidian vault. Parse everything after `/vault` as the task to perform.

Examples:
- `/vault list all notes` → list all `.md` files in the vault
- `/vault find notes about Python` → search vault contents for "Python"
- `/vault create a note called Meeting Notes` → create a new note
- `/vault show my latest note` → find and read the most recently modified note

## Working with the vault

When Wayne asks about notes or the vault, you have access to the filesystem.
Here's how to help effectively:

- **Finding notes**: Use `find` or `ls` to search by filename, or `grep` to search note contents
- **Reading notes**: Use the `Read` tool with the full path to the file
- **Creating notes**: Use the `Write` tool to create new `.md` files inside the vault
- **Editing notes**: Use the `Edit` tool to modify existing notes
- **Listing contents**: Use `ls` via Bash to browse folders

## Helpful patterns

**Search by keyword across all notes:**
```bash
grep -r "keyword" "/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza" --include="*.md" -l
```

**List all notes in the vault:**
```bash
find "/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza" -name "*.md" | sort
```

**Find a note by approximate name:**
```bash
find "/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza" -iname "*keyword*"
```

**Find most recently modified notes:**
```bash
find "/Users/wayne/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza" -name "*.md" -printf "%T@ %p\n" | sort -rn | head -10
```

## Tips

- Obsidian notes are plain markdown (`.md`) files — read and write them directly
- Internal links look like `[[Note Name]]` — these are just references to other files in the vault
- If Wayne asks to "add to" or "update" a note, always read it first so you don't overwrite content accidentally
- If creating a new note, place it in a sensible subfolder if the vault has an existing folder structure — check with `ls` first
