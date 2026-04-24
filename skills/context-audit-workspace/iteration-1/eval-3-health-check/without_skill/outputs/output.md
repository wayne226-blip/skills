# Context Health Check

**Model:** claude-sonnet-4-6
**Usage:** 82k / 1000k (8%)
**Free space:** 884k

---

## Breakdown

| Source | Tokens | % of used |
|---|---|---|
| System prompt | 16.8k | 20.5% |
| MCP tools | 18.7k | 22.8% |
| Skills | 9.8k | 12.0% |
| Memory files | 4.7k | 5.7% |
| Messages | 10k | 12.2% |
| Other | 21.9k | 26.7% |

---

## MCP Tools Detail (18.7k)

| Tool | Tokens |
|---|---|
| notebooklm | ~8k |
| playwright | ~4k |
| preview | ~3k |
| scheduled-tasks | ~1.6k |
| mcp-registry | ~0.7k |

---

## Skills Detail (9.8k)

| Skill | Tokens |
|---|---|
| anthropic-skills:xlsx-pro | 254 |
| anthropic-skills:docx-pro | 203 |
| anthropic-skills:xlsx | 241 |
| anthropic-skills:pptx-pro | 189 |
| anthropic-skills:pptx | 178 |
| anthropic-skills:docx | 202 |
| User: job-finder | 272 |
| User: notebooklm | 265 |

---

## Assessment

**Overall: Healthy.** At 8% usage you have plenty of headroom.

**Largest consumers:**
- MCP tools at 18.7k are the biggest single cost — notebooklm alone is 8k. If you're not using NotebookLM in this session, unloading it would save the most.
- System prompt at 16.8k is fixed overhead from CLAUDE.md + memory.
- Skills at 9.8k: the base/pro pairs (docx + docx-pro, xlsx + xlsx-pro, pptx + pptx-pro) are doubling up. If you're only using the Pro versions, the base versions are dead weight.

**No action needed right now** — 884k free is comfortable. Worth revisiting if context climbs past 50%.
