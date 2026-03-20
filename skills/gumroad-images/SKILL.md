---
name: gumroad-images
description: "Generate Gumroad product covers, thumbnails, and profile banners using Nano Banana. Outputs a ready-to-paste Nano Banana Studio bulk import JSON array with correct Gumroad dimensions and centre-safe composition for thumbnail cropping. Use this skill whenever the user mentions Gumroad images, Gumroad covers, Gumroad banners, Gumroad thumbnails, product listing images for Gumroad, digital product covers, or wants to create visuals for selling digital products on Gumroad. Also use when someone says 'make my Gumroad look good', 'product page images', 'listing graphics', or 'cover art for my [ebook/course/template]'."
---

# Gumroad Images

Generate eye-catching product covers, thumbnails, and profile banners for Gumroad digital products. Outputs Nano Banana Studio bulk import JSON arrays ready to paste.

## Gumroad Image Specs

These dimensions are non-negotiable — Gumroad's display system depends on them:

| Image Type | Pixels | Ratio | Notes |
|---|---|---|---|
| **Product cover** | 1280 x 720 | `16:9` | Main product image. Gumroad auto-crops the centre into a 600x600 square for the thumbnail |
| **Profile banner** | 1600 x 400 | `4:1` | Brand banner above your profile. Very wide — needs panoramic composition |
| **Social card** | 1:1 square | `1:1` | For sharing on social, email headers, promotional use |

**Thumbnail cropping rule:** Gumroad crops ~280px off each side of a 16:9 cover to make the square thumbnail. Every cover prompt MUST place key visual elements in the centre third of the frame. Edges are expendable — use them for ambient colour, gradients, or bleed.

**Up to 8 cover images** per product — use multiple covers to show different angles of value (hero, features, preview, lifestyle, etc.).

## Workflow

### Step 1: Gather Details

Collect from the user:

- **Product name** (required)
- **Product type** (required) — ebook, course, template pack, code, preset, guide, toolkit, etc.
- **Target audience** (required) — who buys this and what's their world like
- **Key benefit** (required) — the one-line transformation or result
- **Brand colours** (optional) — hex codes preferred. If none provided, suggest a vibrant, high-contrast palette that fits the product's vibe
- **Image set** (optional, default: standard):
  - **Single cover** — 1 hero cover image
  - **Standard** — 3-4 covers + banner (recommended)
  - **Full set** — up to 8 covers + banner + social card

If the user gives enough context upfront, proceed with sensible defaults — don't interrogate. Only ask if something critical is missing.

### Step 2: Choose Visual Approach

Pick templates from the library below based on the product type and audience. Think about what will make someone stop scrolling and click.

**Selection principles:**
- Lead with the strongest visual — the hero concept or mockup screen becomes Cover 1 (the thumbnail)
- Vary the remaining covers to show different facets of value
- Every cover must work as a standalone image AND as a centre-cropped square thumbnail
- Match the visual style to the audience (corporate = clean/minimal, creative = bold/expressive, technical = structured/precise)

### Step 3: Generate Prompts

For each selected template:

1. Fill in all product-specific details — no generic placeholders
2. Apply brand colours as hex codes (e.g. `bold electric blue #2B7FFF accents`)
3. Compose centrally — main subject and visual weight in the middle third
4. Use bold, saturated, high-contrast palettes — small thumbnails need visual punch
5. Describe the scene as clean natural language — Nano Banana sends this directly to Gemini

**Critical rules:**
- **No text in images.** Do not describe any text, titles, headings, or words in the prompt. AI-generated text looks terrible. Generate the visual/background only — Wayne overlays text separately in Canva or HTML
- **No nested JSON.** The `prompt` value is a plain string of natural language
- **Centre composition.** Every cover prompt must describe the key subject as centrally placed, centred in frame, or positioned at the visual centre
- **Bold colours.** Use specific hex codes and high-contrast combinations. Muted palettes disappear in Gumroad's browse grid

**Model selection:**
- Default to NB2 (omit `model` key) — better for bold, stylised, eye-catching visuals
- Use `"model": "pro"` only for: realistic mockup screens, complex multi-element scenes, or macro detail shots

### Step 4: Output

Produce one deliverable — a JSON array ready to paste into Nano Banana Studio's Bulk Import:

```json
[
  {"prompt": "Centrally composed [description]...", "ratio": "16:9"},
  {"prompt": "Centrally composed [description]...", "ratio": "16:9"},
  {"prompt": "Wide panoramic [description]...", "ratio": "4:1"},
  {"prompt": "Square composition [description]...", "ratio": "1:1"}
]
```

After the JSON, add a reminder:

> **Thumbnail check:** After generating, check each cover works as a square by imagining the left and right edges cropped off. The centre should still tell the story.
>
> **Text overlay:** Add your product title and any text in Canva, Figma, or an HTML tool — don't rely on AI-generated text.
>
> Paste the JSON above into **Nano Banana Studio → Bulk Import**.

### Step 5: Iterate

Offer specific refinements:
- **Swap a template** — replace one cover with a different visual approach
- **Adjust colours** — shift the palette warmer, cooler, or to match updated branding
- **Add more covers** — fill remaining slots (up to 8 total)
- **Regenerate one** — different angle, mood, or composition for a specific cover
- **Create matching social cards** — 1:1 versions optimised for sharing

## Template Library

### 1. Hero Concept
**Purpose:** Abstract visual representing the product's core benefit — the "feeling" of what it delivers.
**Best for:** Courses, guides, methods, frameworks.
**Ratio:** 16:9
**Prompt pattern:** Bold abstract visual centred in frame. [Visual metaphor for the product's transformation]. Vibrant [brand colour] palette with high contrast. Clean, modern aesthetic. Professional digital product feel. Centrally composed with visual weight in the middle third.

### 2. Mockup Screen
**Purpose:** Show the product in use on a device — makes digital products feel tangible.
**Best for:** Templates, code, apps, dashboards, design assets.
**Ratio:** 16:9 | **Model:** pro
**Prompt pattern:** Modern laptop or tablet centred on a clean desk, screen displaying [description of what the product looks like in use]. Soft ambient lighting from the left. Shallow depth of field, screen sharp, background softly blurred. [Brand colour] accent elements. Minimal props. Shot with 85mm lens, f/2.8. Centrally composed.

### 3. Lifestyle Scene
**Purpose:** Show a person in the target audience's world, benefiting from the product.
**Best for:** Courses, coaching programs, productivity tools.
**Ratio:** 16:9
**Prompt pattern:** [Target audience person] in [their natural environment], looking [emotion that reflects the product's benefit]. Warm, aspirational lighting. [Brand colours] subtly present in the environment. The person is centred in frame, occupying the middle third. Modern, clean setting. Natural, editorial photography style.

### 4. Tool Preview
**Purpose:** Visual preview of what's inside — a bird's-eye look at the resources.
**Best for:** Template packs, toolkits, resource libraries, design assets.
**Ratio:** 16:9
**Prompt pattern:** Overhead flat lay of [visual representation of the product contents] arranged neatly on a [surface colour] surface. Items centrally arranged with even spacing. [Brand colour] accent elements. Clean, organised, satisfying layout. Soft even lighting from above. Shot from directly overhead. Professional product photography.

### 5. Before/After
**Purpose:** Visualise the transformation the product enables.
**Best for:** Any product with a clear before/after story.
**Ratio:** 16:9
**Prompt pattern:** Split composition — left side shows [visual metaphor for the "before" state], right side shows [visual metaphor for the "after" state]. Clear visual contrast between the two halves. [Brand colour] dominates the "after" side. Both sides centred within their half. Clean dividing line. Bold, high-contrast palette.

### 6. Process Visual
**Purpose:** Visual metaphor for the journey, method, or system the product teaches.
**Best for:** Courses, frameworks, methodologies, step-by-step guides.
**Ratio:** 16:9
**Prompt pattern:** Abstract visual representation of [the process/journey] — [visual metaphor like ascending steps, connecting nodes, unfolding path, building blocks]. Bold [brand colour] palette with gradient progression. Clean, modern, geometric aesthetic. Main visual element centred in frame. Professional, premium feel.

### 7. Results/Proof
**Purpose:** Suggest outcomes, success, achievement — social proof energy.
**Best for:** Courses, coaching, business tools, anything with measurable results.
**Ratio:** 16:9
**Prompt pattern:** [Visual metaphor for success/achievement in the product's domain] — [e.g. upward graphs, celebratory moment, finished project, full calendar]. Bright, optimistic lighting. [Brand colour] as the dominant accent. Subject centred with strong visual weight in the middle. Clean background with subtle depth.

### 8. Bold Background
**Purpose:** Clean, striking background designed specifically for text overlay — no competing elements.
**Best for:** Any product. Great as a secondary cover or social card base.
**Ratio:** 16:9 (also works at 1:1)
**Prompt pattern:** Abstract gradient background blending [brand colour 1] and [brand colour 2]. Smooth, flowing shapes with subtle texture. No objects, no people, no text. Bold, vibrant, high-contrast. Visual interest concentrated in the centre with colours fading softer toward the edges. Modern, premium, digital aesthetic.

### 9. Profile Banner
**Purpose:** Wide brand banner for the top of a Gumroad profile page.
**Ratio:** 4:1
**Prompt pattern:** Ultra-wide panoramic composition. [Brand-relevant abstract or environmental scene]. [Brand colours] as the dominant palette. Visual elements concentrated in the centre third — the left and right edges should fade to simpler colour/gradient since they may be partially hidden on narrow screens. Smooth, professional, modern. No text or words. Clean and bold.
