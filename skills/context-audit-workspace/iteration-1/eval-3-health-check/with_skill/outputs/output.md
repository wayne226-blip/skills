## Context Audit

**Session:** claude-sonnet-4-6 | 82k used / 1000k (8%) | 884k free

### Breakdown
| Category | Tokens | % of session |
|---|---|---|
| MCP tools | 18.7k | 23% |
| Skills | 9.8k | 12% |
| Memory files | 4.7k | 6% |
| System (fixed) | 16.8k | 20% |
| Messages | 10k | 12% |

### Waste Found

- **Base+Pro:** `anthropic-skills:docx` (202 tokens) loaded alongside `anthropic-skills:docx-pro` (203 tokens) — base is dead weight (~202 tokens wasted)
- **Base+Pro:** `anthropic-skills:xlsx` (241 tokens) loaded alongside `anthropic-skills:xlsx-pro` (254 tokens) — base is dead weight (~241 tokens wasted)
- **Base+Pro:** `anthropic-skills:pptx` (178 tokens) loaded alongside `anthropic-skills:pptx-pro` (189 tokens) — base is dead weight (~178 tokens wasted)
- **Heavy MCP:** `notebooklm` MCP — ~8k tokens at startup. If this session isn't doing NotebookLM work, that's 8k loaded for nothing. Enable on-demand instead.
- **Specialised MCPs:** `playwright` (~4k) and `preview` (~3k) — both browser/preview tools. Only one is likely needed per session. If you're not doing browser automation or preview work right now, both are pure overhead.

**Total recoverable waste: ~7.6k tokens** (621 from base skill duplicates + ~7k from on-demand MCP candidates)

### Recommendations
| Priority | Action | Est. saving |
|---|---|---|
| 1 | Disable `notebooklm` MCP in Settings → MCP — enable only for NotebookLM sessions | ~8k tokens/session |
| 2 | Disable `playwright` MCP in Settings → MCP — enable only when doing browser automation | ~4k tokens/session |
| 3 | Disable `preview` MCP in Settings → MCP — enable only when using Claude Preview | ~3k tokens/session |
| 4 | Remove base `anthropic-skills:docx` Plugin skill — `docx-pro` is a superset | ~202 tokens |
| 5 | Remove base `anthropic-skills:xlsx` Plugin skill — `xlsx-pro` is a superset | ~241 tokens |
| 6 | Remove base `anthropic-skills:pptx` Plugin skill — `pptx-pro` is a superset | ~178 tokens |

### Quick Wins
Things to do right now, biggest impact first:

- **Turn off `notebooklm` MCP** in Settings → MCP (only enable for NotebookLM sessions) — saves ~8k per session
- **Turn off `playwright` MCP** in Settings → MCP (only enable for browser automation sessions) — saves ~4k per session
- **Turn off `preview` MCP** in Settings → MCP (only enable when using Preview) — saves ~3k per session
- **Remove base Plugin skills** (docx, xlsx, pptx) — the pro versions load the same capabilities. Remove in Cowork/Plugin skill settings — saves ~621 tokens

### Fixed Overhead (can't be reduced)
- System prompt: ~5.8k
- System tools: ~11k
- Autocompact buffer: ~33k

### Summary
Session is healthy at 8% usage — plenty of headroom. No User/Plugin skill duplicates detected in this session. The main opportunity is MCP management: notebooklm, playwright, and preview together cost ~15k tokens every session whether you use them or not. Moving those to on-demand would cut startup overhead by ~80% of the MCP category. The three base/pro Plugin pairs are a quick clean-up for ~621 tokens.
