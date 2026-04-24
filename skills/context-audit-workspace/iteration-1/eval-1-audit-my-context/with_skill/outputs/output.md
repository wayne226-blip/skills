## Context Audit

**Session:** claude-sonnet-4-6 | 75.5k used / 1000k (8% used) | 888.5k free

### Breakdown
| Category | Tokens | % of session |
|---|---|---|
| MCP tools | 18.7k | 25% |
| Skills | 10.7k | 14% |
| Memory files | 4.7k | 6% |
| System (fixed) | 16.8k | 22% |
| Messages | 25.6k | 34% |

---

### Waste Found

**Duplicates — same skill loaded twice (User + Plugin):**

- **Duplicate:** `notebooklm` (User 265 tokens) + `anthropic-skills:notebooklm` (Plugin 180 tokens) — ~265 tokens wasted (User version is larger and loads on top of the Plugin copy)
- **Duplicate:** `job-finder` (User 272 tokens) + `anthropic-skills:job-finder` (Plugin 229 tokens) — ~272 tokens wasted
- **Duplicate:** `cv-builder` (User 99 tokens) + `anthropic-skills:cv-builder` (Plugin 177 tokens) — ~99 tokens wasted (Plugin version is larger/more complete here)

**Base + Pro pairs — base version is dead weight when Pro is loaded:**

- **Base+Pro:** `pdf` (115 tokens) loaded alongside `pdf-pro` (125 tokens) — base is dead weight, ~115 tokens wasted
- **Base+Pro:** `docx` (202 tokens) loaded alongside `docx-pro` (203 tokens) — ~202 tokens wasted
- **Base+Pro:** `pptx` (178 tokens) loaded alongside `pptx-pro` (189 tokens) — ~178 tokens wasted
- **Base+Pro:** `xlsx` (241 tokens) loaded alongside `xlsx-pro` (254 tokens) — ~241 tokens wasted

**Total estimated waste from skills alone: ~1,372 tokens**

**MCP tools — 18.7k at startup:**

The MCP layer is the single biggest discretionary cost at 18.7k tokens (25% of session). Without a per-server breakdown it's hard to pinpoint exact culprits, but 18.7k across 18.7k of definitions suggests multiple large integrations are loading whether or not they're used in a given session. Common culprits are Google Workspace connectors (Gmail, Drive, Docs, Sheets) and Zapier — these can each run to 5–10k tokens of tool definitions.

---

### Recommendations
| Priority | Action | Est. saving |
|---|---|---|
| 1 | Remove `~/.claude/skills/notebooklm/` (User version) — Plugin version is loaded and does the same job | ~265 tokens/session |
| 2 | Remove `~/.claude/skills/job-finder/` (User version) — Plugin version covers it | ~272 tokens/session |
| 3 | Keep `~/.claude/skills/cv-builder/` or the Plugin version — remove whichever is the older/weaker copy (Plugin at 177 is larger, so remove User at 99 tokens) | ~99 tokens/session |
| 4 | Disable base `pdf` Plugin skill — `pdf-pro` is a superset | ~115 tokens/session |
| 5 | Disable base `docx` Plugin skill — `docx-pro` is a superset | ~202 tokens/session |
| 6 | Disable base `pptx` Plugin skill — `pptx-pro` is a superset | ~178 tokens/session |
| 7 | Disable base `xlsx` Plugin skill — `xlsx-pro` is a superset | ~241 tokens/session |
| 8 | Audit MCP servers in Settings → MCP — disable any Google Workspace or Zapier connectors you don't use in every session; only enable them when you need them | Potentially 5–15k tokens/session |

---

### Quick Wins

Things to do right now, biggest impact first:

- **Audit MCP servers** in Settings → MCP — this is your biggest lever. 18.7k tokens is loading every session regardless of whether you touch Gmail, Drive, or Sheets. Disable anything you don't use daily. Re-enable on demand. Potential saving: 5–15k tokens.
- **Delete `~/.claude/skills/job-finder/`** — the Plugin version (`anthropic-skills:job-finder`) is loaded and does the job. Saves ~272 tokens every session.
- **Delete `~/.claude/skills/notebooklm/`** — Plugin version handles it. Saves ~265 tokens every session.
- **Delete `~/.claude/skills/cv-builder/`** (the User copy, 99 tokens) — Plugin version at 177 tokens is more complete.
- **Disable base Plugin skills** (`pdf`, `docx`, `pptx`, `xlsx`) in the Cowork/Plugin skill manager — the Pro versions already include everything. Combined saving: ~736 tokens/session.

---

### Fixed Overhead (cannot be reduced)
- System prompt: ~5.8k
- System tools: ~11k
- Autocompact buffer: ~33k

These are baked into every session — don't try to shrink them.

---

### Summary

Your setup is healthy overall at only 8% context used — no crisis here. But you're carrying ~1.4k tokens of pure duplicate/redundant skill weight every session, and the MCP layer at 18.7k is the real opportunity. If you only do one thing: open Settings → MCP and disable anything you don't use in every single session. The skill cleanup is easy and worth doing, but MCP is where the real savings are.
