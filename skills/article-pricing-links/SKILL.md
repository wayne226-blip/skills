---
name: article-pricing-links
description: >
  Create articles with pricing tables, comparison grids, and affiliate/product links.
  Use this skill whenever the user wants to write a pricing article, product comparison,
  buyer's guide, "best of" list, or any content that combines written copy with prices
  and links. Also trigger when the user mentions: creating affiliate content, writing
  product roundups, building pricing pages, generating comparison articles, adding
  buy-now links, or assembling deal/offer posts. Even if they just say "write an article
  about X with prices" or "compare these products with links" — this skill applies.
---

# Article Pricing Links Generator

Create well-structured articles that combine editorial content with pricing information and product/affiliate links. Ideal for product roundups, buyer's guides, comparison articles, and pricing pages.

## Workflow

### Step 1 — Understand the Brief

Collect from the user:

- **Topic / niche** (required) — what products or services are being covered?
- **Article type** (required) — pick one:
  1. **Product Roundup** — "10 Best [X] in 2026"
  2. **Comparison Article** — "[Product A] vs [Product B]"
  3. **Buyer's Guide** — "How to Choose the Right [X]"
  4. **Pricing Page** — standalone pricing breakdown for a single product/service
  5. **Deal/Offer Post** — time-sensitive promotions with links
- **Products / services** — names, URLs, prices (user may provide or ask you to research)
- **Link format** — plain URLs, affiliate links, or placeholder `[LINK]` tokens?
- **Tone** — professional, casual, enthusiastic, neutral (default: professional but approachable)
- **Word count target** — default 1,200–1,800 words

If the user gives you a topic but skips the rest, use sensible defaults and proceed.

### Step 2 — Research (if needed)

If the user hasn't provided product details, research using web search:

1. Search for current pricing on each product/service
2. Find official product pages for accurate links
3. Note key features, pros/cons for comparison
4. Check for any current deals or promotions

Always verify prices are current. State the date prices were checked in the article.

### Step 3 — Write the Article

Load `references/templates.md` for the structural template matching the chosen article type.

Every article must include:

#### Title
Clear, specific, SEO-friendly. Include the year if relevant.

**Examples:**
- "10 Best Project Management Tools in 2026 (With Pricing)"
- "Notion vs Obsidian: Features, Pricing & Which to Pick"
- "The Complete Guide to Email Marketing Pricing (2026)"

#### Introduction (100–150 words)
Hook the reader. State what the article covers and why it matters. No fluff.

#### Product/Service Sections
For each product or pricing tier covered:

- **Name** — linked to the product page or affiliate URL
- **Price** — clearly displayed (monthly/annual, per-user, free tier if applicable)
- **Key features** — 3–5 bullet points, not a feature dump
- **Best for** — one sentence on ideal user/use case
- **Pros/Cons** — 2–3 of each, honest and specific

#### Pricing Comparison Table
A markdown table summarising all options at a glance:

```markdown
| Product | Free Tier | Starter | Pro | Enterprise |
|---------|-----------|---------|-----|------------|
| [Tool A](URL) | Yes | $9/mo | $29/mo | Custom |
| [Tool B](URL) | No | $12/mo | $35/mo | $99/mo |
```

Include the table early — readers scan for it. Put it after the introduction or after the first product section.

#### Verdict / Recommendation
2–3 paragraphs. Give a clear recommendation based on use case:
- "Best overall: [X]"
- "Best value: [Y]"
- "Best for teams: [Z]"

Don't be wishy-washy. Pick winners and explain why.

#### Links Section
At the bottom, a clean list of all product links:

```markdown
## Quick Links

- [Product A — Official Site](URL)
- [Product B — Official Site](URL)
- [Product C — Official Site](URL)
```

### Step 4 — Format and Polish

Before delivering:

1. All prices are clearly formatted (£/$, monthly vs annual, per-user noted)
2. All links are working markdown links (or `[LINK]` placeholders if requested)
3. Pricing table is accurate and aligned
4. No broken markdown formatting
5. Word count is within target range
6. Disclosure line included if affiliate links are used:
   > *This article contains affiliate links. We may earn a commission at no extra cost to you.*

### Writing Guidelines

**Do:**
- Lead with value — what does the reader get from this article?
- Use specific numbers — "$29/mo for up to 5 users" not "affordable pricing"
- Compare like-for-like — same tier, same billing cycle
- Update pricing dates — "Prices checked March 2026"
- Keep paragraphs short — 2–4 sentences max

**Don't:**
- Use hype language — "incredible value", "game-changing", "must-have"
- Hide pricing behind vague language — if you know the price, state it
- Overload with features — pick the ones that matter for the target reader
- Write a wall of text — use headers, bullets, and tables to break it up

## Output Format

Deliver the article as clean markdown, ready to publish. If the user wants it saved to a file, use this naming convention:

```
YYYY-MM-DD-[slug].md
```

Example: `2026-03-19-best-email-marketing-tools-pricing.md`

## Resources

### references/
- `templates.md` — Structural templates for each article type (roundup, comparison, buyer's guide, pricing page, deal post)
