---
name: linkedin-article
description: "Create a complete LinkedIn article with AI-generated images. Writes the article in Markdown with frontmatter, generates professional illustrations via the Gemini API, and produces an HTML preview — all saved to a project folder. Use this skill whenever Wayne wants to write a LinkedIn article, create long-form LinkedIn content, publish an article on LinkedIn, or says things like 'write an article for LinkedIn', 'LinkedIn article about X', 'long-form post for LinkedIn', 'create an article with images'. Also trigger when Wayne says 'linkedin-article' or asks to create any article-length content destined for LinkedIn, even if he doesn't explicitly say 'article' — if the content is longer than a standard post and involves LinkedIn, this skill applies."
---

# LinkedIn Article Generator

Create a complete LinkedIn article with AI-generated images, written in Wayne's voice.

## Output Structure

```
~/Claude/Projects/linkedin-articles/[slug]/
├── article.md          — Source article with YAML frontmatter
├── article.html        — Styled HTML preview (for copy-paste into LinkedIn)
├── generate_images.py  — Reusable image generation script
└── images/
    ├── hero.png        — Cover image (uploaded as LinkedIn article cover)
    ├── section-1.png   — First section illustration
    ├── section-2.png   — Second section illustration
    └── cta.png         — Call-to-action image (optional)
```

## Workflow

### Step 1: Gather Requirements

Ask Wayne these questions one at a time using AskUserQuestion:

1. **Topic** — What is the article about?
2. **Angle** — What's the key message or hook? (e.g., "why SMBs need AI now", "what I learned building X", "the real cost of Y")
3. **Image count** — How many images? Default: 3-4 (hero + 2-3 section images)
4. **Image style** — Clean & professional (default), warm & approachable, bold & editorial, or photo-realistic

### Step 2: Write the Article

Create `article.md` with YAML frontmatter and Markdown body:

```markdown
---
title: "Article Title Here"
description: "1-2 sentence summary for LinkedIn SEO and social preview"
cover_image: images/hero.png
author: Wayne Pearce
---

# Article Title Here

![Hero](images/hero.png)

[Article body...]
```

**Wayne's voice rules:**
- Direct, plain English, short sentences
- No hype, no buzzwords, no corporate speak
- Contractions are fine ("don't", "it's", "you're")
- Short paragraphs (2-3 sentences max — LinkedIn readers scan on mobile)
- Explain things like you're talking to a mate who's smart but not technical
- Under 1,200 words. Ideally 800-1,000

**Article structure that works on LinkedIn:**
1. Hero image placeholder
2. Opening hook — grab attention in 2-3 sentences (a question, a bold statement, or a relatable scenario)
3. Section image
4. 2-3 key points with subheadings — the meat of the article
5. Section image (before/after, transformation, or visual break)
6. The pivot — connect the points to what Wayne does (calibre.ai) without being salesy
7. CTA image (optional)
8. Soft close — invite conversation, not a hard sell
9. Byline: *Wayne Pearce is the founder of calibre.ai, helping small businesses get set up with AI that actually works.*

### Step 3: Generate Images

Run the bundled script: `scripts/generate_images.py`

Or create a project-specific version. The script:
- Reads `GEMINI_API_KEY` from environment (check `~/.claude/.env` or `~/.zshrc` if not set)
- Calls `gemini-3.1-flash-image-preview` (NB2 model) via the Gemini API
- Appends aspect ratio hint to each prompt: "Generate as a wide 16:9 aspect ratio image."
- Decodes base64 response, saves PNGs to `images/`
- Uses `ssl._create_unverified_context()` for macOS SSL compatibility

**API details:**
```
Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={API_KEY}
Method: POST
Body: {"contents": [{"parts": [{"text": "prompt"}]}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
Response: candidates[0].content.parts[] — find the part with inlineData.data (base64)
```

**Image prompt guidelines:**
- Always include: "No text, no words, no letters anywhere in the image."
- Always include: "Generate as a wide 16:9 aspect ratio image."
- Default style: "Modern flat illustration, clean professional style, blue and white colour palette, subtle gradients"
- Keep prompts under 100 words — shorter prompts generate faster and time out less
- If an image times out, retry with a simplified prompt

### Step 4: Generate HTML Preview

Create `article.html` — a clean, styled HTML page:
- Max-width 720px, centered
- System font stack (-apple-system, etc.)
- Line-height 1.7, good paragraph spacing
- Images full-width with border-radius
- Byline styled with top border and italic

This preview serves two purposes:
1. Wayne can review the full article with images before publishing
2. He can select-all and copy the formatted text into LinkedIn's editor (formatting carries over as rich text)

### Step 5: Publishing Guide

Tell Wayne:
1. Open `article.html` in browser to preview
2. On LinkedIn: go to "Write article"
3. Upload `hero.png` as the cover image
4. Copy text from HTML preview (Cmd+A, Cmd+C) and paste into the editor body
5. Insert remaining images manually at the right positions using the image button in LinkedIn's toolbar
6. Add the title and description from the frontmatter

## Regenerating Images

If Wayne wants to redo any images, he can either:
- Run `python3 generate_images.py` from the article folder to regenerate all
- Ask Claude to regenerate specific ones with adjusted prompts

## Slug Convention

Convert the article title to a URL-friendly slug:
- "Why Small Businesses Need AI Now" → `why-smbs-need-ai`
- Keep it short — 4-6 words max
