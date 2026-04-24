## Context Audit

**Session:** claude-sonnet-4-6 | 89.5k used / 1000k (9% used) | 877.5k free

### Breakdown
| Category | Tokens | % of session |
|---|---|---|
| MCP tools | 53.6k | 59.9% |
| Skills | 10.7k | 12.0% |
| Memory files | 4.7k | 5.3% |
| System (fixed) | 16.8k | 18.8% |
| Messages | 1.8k | 2.0% |

---

### Waste Found

**MCP tools are the main culprit — 60% of your context.**

- **Duplicate:** `linkedin-post` (User 184 tokens) + `anthropic-skills:linkedin-post` (Plugin 188 tokens) — ~184 tokens wasted loading both
- **Duplicate:** `prompt-guide` (User 242 tokens) + `anthropic-skills:prompt-guide` (Plugin 246 tokens) — ~242 tokens wasted loading both
- **Base+Pro:** `anthropic-skills:pdf` (115 tokens) loaded alongside `anthropic-skills:pdf-pro` (125 tokens) — base is dead weight, ~115 tokens wasted
- **Oversized MCP:** Zapier is loading ~96 tools at 53.6k tokens every session. Only 6 tools are named in the breakdown — gmail, google_docs, google_sheets, microsoft_outlook, plus send/draft variants. That's 90+ tools you're paying for in context but almost certainly not using in most sessions.
- **Likely unused Zapier tools:** Google Docs (`google_docs_get_document_content` — 217 tokens), Google Sheets (`google_sheets_create_spreadsheet` — 391 tokens), and Microsoft Outlook (`microsoft_outlook_send_email` — 471 tokens) are loading even when you're only doing Gmail work.

---

### Recommendations
| Priority | Action | Est. saving |
|---|---|---|
| 1 | Disable Zapier MCP in Settings → MCP (or narrow it to Gmail-only tools) — re-enable for Docs/Sheets sessions | ~53.6k tokens/session |
| 2 | Delete `~/.claude/skills/prompt-guide/` — Plugin version (`anthropic-skills:prompt-guide`) is larger and does the same job | ~242 tokens |
| 3 | Delete `~/.claude/skills/linkedin-post/` (if it exists as a User skill) — Plugin version is equivalent | ~184 tokens |
| 4 | Remove `anthropic-skills:pdf` from Plugin skills — `pdf-pro` is a superset, base adds nothing | ~115 tokens |

---

### Quick Wins
Things to do right now, biggest impact first:

- **Disable Zapier MCP** in Settings → MCP — this single change saves 53.6k tokens per session. That's 60% of your current context load gone. Only turn it on when you actually need Zapier automations. Saves ~53.6k.
- **Delete `~/.claude/skills/prompt-guide/`** — the Plugin version (anthropic-skills:prompt-guide at 246 tokens) is slightly larger and loads anyway. Your User copy is redundant. Saves ~242 tokens.
- **Delete `~/.claude/skills/linkedin-post/`** — same situation, Plugin version wins. Saves ~184 tokens.
- **Remove `anthropic-skills:pdf`** via Plugin skill settings — you have pdf-pro, the base version is dead weight. Saves ~115 tokens.

Total recoverable: **~54.1k tokens** — dropping your session from 89.5k to ~35k used at startup.

---

### Fixed Overhead (can't be reduced)
- System prompt + tools: ~16.8k (this is fixed — CLAUDE.md, memory files, built-in tools)
- Autocompact buffer: ~33k
- Messages: grow through the session, nothing to do at startup
