---
name: parse-pdfs
description: >
  Parse PDFs (and other documents) in the Obsidian vault into Markdown for RAG
  indexing. Use when Wayne says "parse pdfs", "convert pdfs", "index my pdfs",
  "update library", "parse documents", or drops new PDFs into the vault and
  wants them searchable via Copilot. Also use when he says /parse-pdfs.
---

# Parse PDFs

Convert PDFs and other documents in the Obsidian vault into clean Markdown files with front matter, saved to `Library/`. Copilot then indexes them for RAG search.

## Dependencies

- **docling** -- if missing: `pip3 install docling`

## Vault Paths

- **Vault root:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza`
- **Output folder:** `Library/` (inside vault root)
- **Skip:** `.trash/`, `Library/` (already parsed), `copilot/`

## Step-by-Step Workflow

### 1. Find PDFs to parse

Scan the vault for `.pdf` files. Skip:
- Files in `.trash/`
- Files that already have a matching `.md` in `Library/`

Report what was found: "Found 3 new PDFs to parse"

### 2. Parse each PDF

Run this Python script (adapt paths as needed):

```python
from docling.document_converter import DocumentConverter
from pathlib import Path
from datetime import datetime

VAULT = Path("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/wauzza").expanduser()
OUTPUT = VAULT / "Library"
OUTPUT.mkdir(exist_ok=True)

converter = DocumentConverter()

# pdf_path = the PDF to convert
result = converter.convert(str(pdf_path))
markdown = result.document.export_to_markdown()

front_matter = f"""---
title: "{pdf_path.stem}"
source: "{pdf_path.relative_to(VAULT)}"
type: parsed-document
tags:
  - parsed
  - pdf
date: {datetime.now().strftime('%Y-%m-%d')}
---

"""

output_path = OUTPUT / f"{pdf_path.stem}.md"
output_path.write_text(front_matter + markdown, encoding="utf-8")
```

### 3. Update Vault Index

Add any new files to the Library section of `Vault Index.md`.

### 4. Remind Wayne

Tell Wayne to **restart Obsidian** (or reload) so Copilot re-indexes the new files. The auto-index-on-startup setting handles the rest.

## Copilot Config

If Copilot embedding model is wrong, fix it in `.obsidian/plugins/copilot/data.json`:
- `embeddingModelKey` should be `gemini-embedding-001|google`
- `indexVaultToVectorStore` should be `ON STARTUP`
- `enableSemanticSearchV3` should be `true`

## What Docling Supports

PDF, DOCX, PPTX, HTML, images, Markdown, AsciiDoc, CSV, XLSX. Same script works -- just point it at the file.

## Common Issues

| Problem | Fix |
|---|---|
| Docling not installed | `pip3 install docling` |
| Tables garbled | Docling handles most tables well -- check the PDF isn't image-only |
| Images not described | Docling extracts text only. For image descriptions, send to a vision model separately |
| Copilot not indexing | Check `indexVaultToVectorStore: "ON STARTUP"` in copilot data.json, then restart Obsidian |
| Wrong embedding model | Set `embeddingModelKey` to `gemini-embedding-001\|google` |
