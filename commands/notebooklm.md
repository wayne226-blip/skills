---
name: notebooklm
description: NotebookLM workflows — create notebooks, add sources, generate podcasts/audio overviews, query content, run research. Usage: /notebooklm [action] [topic or URL]
argument-hint: "[action: new|podcast|research|query|list] [topic or URL]"
allowed-tools: All
---

# NotebookLM Command

Parse the argument to determine what Wayne wants, then execute the right workflow.

## Argument Parsing

Split `$ARGUMENTS` into `action` (first word) and `rest` (everything after). If no argument is given, show the menu below.

### Actions

| Argument | What to do |
|----------|-----------|
| `new [title]` | Create a new notebook with that title |
| `podcast [notebook-name or ID]` | Generate an audio deep-dive for that notebook |
| `research [topic]` | Create a notebook, run web research on topic, import top sources |
| `query [notebook-name] [question]` | Query a specific notebook |
| `list` | List all notebooks with source counts |
| `add [url or text]` | Add a source to the most recently used notebook |
| *(no argument)* | Show the menu below |

---

## No argument: show menu

If no argument given, list existing notebooks and offer options:

```
## Your NotebookLM Notebooks

[list notebooks with titles and source counts]

### What do you want to do?
- `/notebooklm new [title]` — create a new notebook
- `/notebooklm podcast [notebook name]` — generate an audio podcast
- `/notebooklm research [topic]` — research a topic and build a notebook
- `/notebooklm query [notebook] [question]` — ask a question about a notebook
- `/notebooklm list` — see all notebooks
```

---

## Workflow: `new`

1. Call `mcp__notebooklm__notebook_create` with the provided title
2. Confirm creation and show the notebook ID
3. Ask: "Want to add sources or run research on a topic?"

---

## Workflow: `podcast`

1. Call `mcp__notebooklm__notebook_list` to find the matching notebook by name (fuzzy match is fine)
2. Call `mcp__notebooklm__studio_create` with:
   - `artifact_type: "audio"`
   - `audio_format: "deep_dive"`
   - `confirm: true`
3. Poll `mcp__notebooklm__studio_status` every 15 seconds until `status: "completed"`
4. Show the URL and offer to download

---

## Workflow: `research`

1. Create a notebook: `mcp__notebooklm__notebook_create` — title = the topic
2. Start research: `mcp__notebooklm__research_start` with:
   - `query`: the topic
   - `source: "web"`
   - `mode: "fast"`
   - `notebook_id`: the new notebook's ID
3. Poll `mcp__notebooklm__research_status` until complete
4. Import top sources: `mcp__notebooklm__research_import`
5. Show what was imported
6. Ask: "Want me to generate a podcast or query the sources?"

---

## Workflow: `query`

1. Find the notebook using `mcp__notebooklm__notebook_list` (fuzzy match on name)
2. Call `mcp__notebooklm__notebook_query` with the question
3. Show the answer

---

## Workflow: `list`

Call `mcp__notebooklm__notebook_list` and display as a table:

```
| # | Title | Sources | Last Updated |
|---|-------|---------|-------------|
| 1 | ...   | N       | ...          |
```

---

## Workflow: `add`

1. Check `mcp__notebooklm__notebook_list` — use the most recently updated notebook
2. If a URL: `source_type: "url"`; if text: `source_type: "text"`
3. Call `mcp__notebooklm__source_add` with `wait: true`
4. Confirm the source was added
