---
name: notebooklm
description: >
  Use this skill for ANY interaction with NotebookLM — creating notebooks, adding sources (URLs, YouTube, text, files, Google Drive), generating audio/video/podcast overviews, querying notebook content, running deep research, managing sources, exporting artifacts, and sharing notebooks. ALWAYS trigger when Wayne mentions NotebookLM explicitly, or when he asks to: make a podcast or audio overview from a notebook, generate flashcards/quiz/study guide/mind map/briefing doc from sources, add something to a notebook, build a notebook about a topic, query what's in a notebook, list his notebooks, do deep research and save it in NotebookLM, or "notebooklm it". Also trigger for phrases like "put this in a notebook", "save it in notebooklm", "what's in my [X] notebook", "make a podcast from my [X] notebook", or "summarise my notebooklm sources". Do NOT trigger for: general web search/summarise URL requests with no notebook mentioned, scheduling tasks, Obsidian vault lookups, YouTube channel analysis, or PDF/file tasks unrelated to NotebookLM.
---

# NotebookLM Skill

You have full access to the `mcp__notebooklm__*` tools. Use them to handle any NotebookLM workflow Wayne asks for.

---

## Quick Reference: MCP Tools

| Tool | What it does |
|------|-------------|
| `notebook_list` | List all notebooks |
| `notebook_get` | Get a notebook + its sources |
| `notebook_create` | Create a new notebook |
| `notebook_rename` | Rename a notebook |
| `notebook_delete` | Delete a notebook (requires confirm=True) |
| `notebook_describe` | Get AI summary + suggested topics |
| `notebook_query` | Ask AI a question about existing sources |
| `source_add` | Add URL, text, file, or Drive doc as a source |
| `source_list_drive` | List sources with Drive freshness |
| `source_delete` | Delete a source |
| `source_describe` | Get AI summary of a source |
| `source_get_content` | Get raw text of a source |
| `studio_create` | Generate audio, video, report, flashcards, quiz, mind map, etc. |
| `studio_status` | Check generation status + get URLs |
| `studio_delete` | Delete a studio artifact |
| `research_start` | Start web or Drive research |
| `research_status` | Poll research progress |
| `research_import` | Import discovered sources |
| `download_artifact` | Download audio, report, slides, etc. to a file |
| `export_artifact` | Export report/table to Google Docs/Sheets |
| `notebook_share_public` | Enable/disable public link |
| `notebook_share_invite` | Invite collaborators by email |
| `note` | Create, list, update, or delete notes in a notebook |

---

## Workflows

### Creating a notebook and adding sources

1. Call `notebook_create` with a descriptive title
2. Call `source_add` for each source:
   - `source_type: "url"` for web pages or YouTube videos
   - `source_type: "text"` for pasted text content
   - `source_type: "file"` for local PDFs or audio files
   - `source_type: "drive"` for Google Docs/Slides/Sheets
   - Pass `wait: true` so we wait for processing before moving on
3. Confirm what was added and show the notebook ID for future reference

**Tip:** For multiple URLs, use `urls: [...]` in a single `source_add` call rather than one call per URL.

### Generating audio overview (podcast)

1. Find or create the notebook (use `notebook_list` if unsure)
2. Call `studio_create` with:
   - `artifact_type: "audio"`
   - `audio_format: "deep_dive"` (default — conversational deep dive)
   - `audio_format: "brief"` if Wayne wants a shorter version
   - `confirm: true`
3. Poll `studio_status` until status is `completed`
4. Show Wayne the URL or offer to download with `download_artifact`

### Generating other studio artifacts

Same pattern as audio — call `studio_create` with the right `artifact_type`:

| Wayne says | artifact_type | Notes |
|-----------|---------------|-------|
| "make a podcast" / "audio overview" | `audio` | `audio_format`: deep_dive, brief, critique, debate |
| "make a video" | `video` | `video_format`: explainer, brief |
| "make a study guide" | `report` | `report_format`: "Study Guide" |
| "make a briefing doc" | `report` | `report_format`: "Briefing Doc" |
| "make a blog post" | `report` | `report_format`: "Blog Post" |
| "make flashcards" | `flashcards` | `difficulty`: easy/medium/hard |
| "make a quiz" | `quiz` | `question_count`: N, `difficulty`: easy/medium/hard |
| "make a mind map" | `mind_map` | — |
| "make slides" / "slide deck" | `slide_deck` | `slide_format`: detailed_deck or presenter_slides |
| "make an infographic" | `infographic` | — |

### Querying a notebook

Use `notebook_query` to ask questions about the sources already in a notebook. This is for asking AI about **existing sources** — not for web search. Provide a `notebook_id` and a clear question.

### Running research

Use `research_start` to find new sources from the web or Google Drive:
1. Call `research_start` with `query`, `source: "web"`, and `mode: "fast"` (or `"deep"` for thorough research)
2. Call `research_status` to poll until complete
3. Review the sources returned and call `research_import` to add chosen ones to the notebook

### Downloading artifacts

Use `download_artifact` with:
- `artifact_type`: audio, video, report, mind_map, slide_deck, infographic, data_table, quiz, flashcards
- `output_path`: where to save the file
- Omit `artifact_id` to get the latest artifact of that type

---

## Decision guide

- **"Make a notebook about X"** → create notebook, run `research_start` with `mode: "fast"`, import top sources, then ask if Wayne wants any studio artifacts
- **"Add this URL to NotebookLM"** → `notebook_list` to find the right notebook (or create one), then `source_add`
- **"Make a podcast from X"** → create notebook if needed, add source X, then `studio_create` with `artifact_type: "audio"`
- **"Query my notebook about X"** → `notebook_list` to find the right one, then `notebook_query`
- **"Summarise my sources"** → `notebook_describe` for a quick AI summary
- **"Download the audio"** → `studio_status` to get the artifact ID, then `download_artifact`

---

## Style notes

- Always confirm notebook creation and source addition with a brief summary (title, number of sources added, notebook ID)
- When studio generation is kicked off, tell Wayne it's running and poll until done rather than leaving him hanging
- If a notebook already exists for the topic, use it — don't create duplicates. Use `notebook_list` to check first
- Store notebook IDs in the response so Wayne can refer back to them
- Offer next steps after each workflow (e.g. after creating a notebook: "Want me to generate an audio overview or query the sources?")
