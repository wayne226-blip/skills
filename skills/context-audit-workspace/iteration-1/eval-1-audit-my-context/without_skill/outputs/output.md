Here's the audit:

**Context breakdown — 75.5k total (8% of limit)**

| Component | Tokens | % of total | Notes |
|---|---|---|---|
| Messages | 25.6k | 34% | Conversation history |
| MCP tools | 18.7k | 25% | Loaded tool definitions |
| System tools | 11k | 15% | Built-in Claude Code tools |
| Skills | 10.7k | 14% | User + Plugin skill descriptions |
| System prompt | 5.8k | 8% | CLAUDE.md files |
| Memory files | 4.7k | 6% | MEMORY.md |
| Free space buffer | 33k | — | Autocompact headroom |

---

**What's worth looking at**

**Skills (10.7k) — obvious duplication**

You have three skills that exist in both User and Plugin form:

| Skill | User | Plugin | Combined waste |
|---|---|---|---|
| notebooklm | 265 | 180 | 445 tokens loading twice |
| job-finder | 272 | 229 | 501 tokens loading twice |
| cv-builder | 99 | 177 | 276 tokens loading twice |

That's ~1.2k tokens loading duplicated skills every session. You noted in memory you removed cv-builder, download-video, and prompt-guide from User skills on 2026-03-18 — but the data here still shows cv-builder at 99 tokens on the User side. Worth confirming that removal actually took effect.

The base vs pro pairs (pdf/pdf-pro, docx/docx-pro, pptx/pptx-pro, xlsx/xlsx-pro) are also all loading simultaneously. If you always use the Pro versions, the base ones are dead weight — ~860 tokens combined.

**MCP tools (18.7k) — likely the biggest opportunity**

18.7k is a lot for tool definitions. The sample `/context` output from your message shows 18 MCP tools loaded. Without seeing the full list it's hard to pinpoint, but common culprits are:

- MCP servers connected but never used in most sessions (Playwright, Gmail, NotebookLM, etc.)
- Each MCP server loads its full tool schema regardless of whether you use it

If you only use Gmail occasionally, having it loaded every session costs tokens for nothing. Same for Playwright — useful when you need a browser, dead weight otherwise.

**Memory (4.7k) — reasonable but growing**

MEMORY.md is 4.7k and growing as entries accumulate. Not a problem now, but worth an occasional prune. Stale entries (like autoresearch status from weeks ago) add up.

---

**Quick wins**

1. Confirm User-side cv-builder, download-video, prompt-guide are actually removed — the data suggests cv-builder may still be loading
2. Remove base skill versions (pdf, docx, pptx, xlsx) if you only use Pro
3. Audit which MCP servers you actually use weekly vs occasionally — disable the occasional ones and connect them on-demand

**Bottom line:** You're only at 8% context so nothing is urgent, but skills duplication and always-on MCP tools are the cleanest things to tighten up.
