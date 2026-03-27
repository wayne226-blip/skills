# Refresh Publishing Command Centre Dashboard

Refresh the Publishing Command Centre dashboard with current data from all author workspaces.

## Steps

1. **Read all source files** — gather current status from every author workspace:

   **Tom Hadley (non-fiction):**
   - `~/Claude/Projects/calibre-bundles/bundles/persona-design-book/TASKS.md`
   - `~/Claude/Projects/calibre-bundles/bundles/persona-design-book/series-plan.md`
   - Count files in each `books/*/chapters/`, `books/*/diagrams/`, `books/*/manuscripts/`, `books/*/covers/`, `books/*/marketing/` directory

   **Lady Elara (dark romantasy):**
   - `~/Claude/Projects/calibre-bundles/bundles/lady-elara/seasons/status.md`
   - `~/Claude/Projects/calibre-bundles/bundles/lady-elara/marketing/` (check what marketing assets exist)

   **Maren Wolfe (dark paranormal romance):**
   - `~/authors/maren-wolfe/TASKS.md`
   - `~/authors/maren-wolfe/seasons/status.md`

   **Sable Voss (dark academia romance):**
   - `~/authors/sable-voss/TASKS.md`
   - `~/authors/sable-voss/seasons/status.md`

   **Dotty Pemberton (cozy mystery):**
   - `~/authors/dotty-pemberton/TASKS.md`

2. **Determine pipeline status** for each book by checking what files exist:
   - `chapters/` has files → write stage is complete or in-progress
   - `diagrams/` has files → diagrams stage is complete or in-progress
   - `manuscripts/` has .docx → compile is complete
   - `covers/` has final image → cover is complete
   - `marketing/` has files → marketing is complete or in-progress
   - TASKS.md says "PUBLISHED" or status.md says "PUBLISHED" → publish is complete

3. **Update the dashboard** — edit the `PUBLISHING_DATA` JS object between the `// === DATA START ===` and `// === DATA END ===` markers in:
   `~/Claude/Projects/calibre-bundles/bundles/persona-design-book/dashboard.html`

   Update:
   - `meta.lastUpdated` to today's date
   - `meta.nextAction` to the most urgent unfinished task
   - All book pipeline stages, word counts, chapter counts, diagram counts
   - Any new books or seasons that have been added
   - TikTok video status if any have been posted
   - Author status changes (e.g., if Dotty Pemberton starts writing, change status from 'early' to 'active')

4. **Report what changed** — tell Wayne what was updated.

## Rules
- Don't change any rendering code — only update the data block
- Keep the data structure exactly the same (same field names, same format)
- Use actual file counts, not estimates
- Set today's date for `lastUpdated`
- If a new pen name workspace appears in `~/authors/`, add it to the authors array
