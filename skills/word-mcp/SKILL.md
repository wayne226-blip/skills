---
name: word-mcp
description: "Create, edit, format, and export Microsoft Word documents using the Word MCP extension (By Anthropic). Use this skill whenever the user wants to work with .docx files — creating reports, letters, CVs, proposals, formatted documents, or editing existing Word files. Also use when the user asks to export a document to PDF via Word. Triggers on: 'create a Word doc', 'write a report', 'format this document', 'make a letter', 'export to PDF', 'edit the docx', 'open my document', or any task involving .docx files."
---

# Word MCP Skill

This skill drives Microsoft Word on the user's Mac through the Word (By Anthropic) MCP extension. Unlike script-based approaches (python-docx), these tools control the actual Word application, giving you native formatting, styles, and reliable PDF export.

## Available Tools

### Read-only
| Tool | Purpose |
|------|---------|
| `open_document` | Open an existing .docx file in Word |
| `get_document_text` | Read the text content of the open document |

### Write
| Tool | Purpose |
|------|---------|
| `create_document` | Create a new blank Word document |
| `insert_text` | Add text at a position in the document |
| `replace_text` | Find and replace text in the document |
| `format_text` | Apply formatting (bold, italic, font size, colour, headings, etc.) |
| `save_document` | Save the document to a file path |
| `close_document` | Close the document in Word |
| `export_pdf` | Export the current document as PDF |

## Core Workflow

Every Word task follows this pattern:

```
create_document / open_document
  -> insert_text (build content)
  -> format_text (style it)
  -> save_document (write to disk)
  -> export_pdf (optional)
  -> close_document
```

Always save before exporting to PDF. Always close when done.

## Workflow Patterns

### Creating a new document from scratch

1. `create_document` — opens a new blank doc in Word
2. `insert_text` — add title, headings, body text, bullet points. Build the full content first before formatting
3. `format_text` — apply heading styles, bold, font sizes, colours after content is in place
4. `save_document` — save to the user's desired path (default to `~/Documents/` if no path given)
5. `export_pdf` — if the user wants a PDF version
6. `close_document` — clean up

### Editing an existing document

1. `open_document` — open the .docx file
2. `get_document_text` — read current content to understand what's there
3. `replace_text` / `insert_text` — make changes
4. `format_text` — adjust formatting if needed
5. `save_document` — save changes
6. `close_document`

### Quick PDF export

1. `open_document` — open the .docx
2. `export_pdf` — export to PDF (saves alongside the .docx by default, or to a specified path)
3. `close_document`

## Best Practices

- **Content first, formatting second.** Insert all text before applying formatting. This avoids formatting being overwritten or misapplied as content shifts.
- **Be specific with file paths.** Use absolute paths like `/Users/wayne/Documents/report.docx`. If the user gives a relative path or filename only, save to `~/Documents/`.
- **Confirm the save location.** Before saving, tell the user where the file will be saved.
- **Build structure with headings.** Use `format_text` to apply Heading 1, Heading 2 styles — this gives the document proper structure that shows up in Word's navigation pane and PDF bookmarks.
- **Close when done.** Always call `close_document` at the end to avoid leaving orphan windows in Word.

## Common Use Cases

### Report / Proposal
- Title (Heading 1, bold, larger font)
- Executive Summary section
- Body sections with Heading 2
- Bullet points for key findings
- Save as .docx + export PDF

### Letter / Email Draft
- Date, recipient address
- Salutation, body paragraphs
- Sign-off, sender name
- Formal formatting (12pt, Times New Roman or similar)

### CV / Resume
- Name as title (bold, larger font)
- Contact details
- Sections: Summary, Experience, Education, Skills
- Consistent heading styles
- Export to PDF for sending

### Meeting Notes / Minutes
- Meeting title, date, attendees
- Agenda items as headings
- Action items as bullet points
- Save to shared location

## Error Handling

- If Word is not open, `create_document` or `open_document` will launch it — allow a moment for startup.
- If a file path doesn't exist, create the directory first or save to `~/Documents/`.
- If `export_pdf` fails, ensure the document has been saved first with `save_document`.
