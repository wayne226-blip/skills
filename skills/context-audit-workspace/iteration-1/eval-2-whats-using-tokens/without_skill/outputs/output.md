Based on the context data, here's what's eating your tokens:

**MCP tools are the biggest drain — 53.6k tokens.** That's 60% of your used context. Zapier is the main culprit. You've got ~90+ Zapier tools loaded, and each tool definition takes up space just by existing in the context, even if you never use them.

**System prompt — 16.8k.** Your CLAUDE.md files, memory, and instructions load every session. That's fixed overhead.

**Skills — 10.7k.** You've got duplicates: `linkedin-post` and `prompt-guide` appear twice each — once as User skills and once as Plugin (anthropic-skills) versions. That's wasted space.

**Memory — 4.7k.** MEMORY.md loading each time. Reasonable but worth keeping trimmed.

**Messages — 1.8k.** Low, so it's not conversation history causing the weight.

**Quick wins:**

1. Disconnect Zapier MCP or reduce the tools it exposes — 90+ tools is the main problem
2. Remove the duplicate skills (you have User + Plugin versions of the same skills)
3. Keep MEMORY.md pruned — stale entries add up

You're at 89.5k / 1000k (9%) so you're not in danger, but Zapier MCP alone is using more context than everything else combined.
