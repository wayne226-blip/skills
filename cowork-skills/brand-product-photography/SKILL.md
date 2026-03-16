---
name: brand-product-photography
description: "Generate brand-matched product photography prompts from a client's website. Scrapes the site for brand colours, fonts, and design style, then produces Nano Banana JSON prompts for studio product shots and lifestyle/contextual photography — all in the client's exact visual identity. Use this skill whenever someone wants to create product photos that match a brand, generate branded product photography, make e-commerce images in a client's style, or mentions 'product photography' + a website/brand. Also trigger when: the user has a client URL and wants product images styled to their brand, wants to create Amazon/Shopify listing photos in brand colours, wants lifestyle product shots for social media, or says things like 'match this brand's look for product shots'. Even casual requests like 'shoot product photos in their style' or 'make product images for this client' should trigger this skill."
---

# Brand Product Photography Generator

Turn any client's website into a set of production-ready product photography prompts. The workflow: research the brand's visual identity from their URL, then generate Nano Banana JSON prompts for studio and lifestyle product photography that matches their exact colours, typography, and design aesthetic.

This skill complements the **ad-creative** skill. Where ad-creative generates 40 ad format variations, this skill focuses specifically on high-quality product photography — the kind you'd use for e-commerce listings, catalogues, social media hero shots, and brand lookbooks.

## Workflow

### Step 0: Output Format

Ask the user one question:

> Where will you generate these images?
> 1. **Nano Banana Studio** — I'll give you a JSON array for Bulk Import
> 2. **Higsfield** — plain text prompts, one at a time
> 3. **Other** — tell me the tool and I'll adapt

Remember their choice for the rest of the session.

### Step 1: Collect Inputs

Gather from the user:

- **Client website URL** (required) — this is how we extract the brand identity
- **Product images** (optional but recommended — dramatically improves output)
- **Product description** (optional — what the product is, key features, materials, dimensions)
- **Shot list preferences** (optional — ask if they want studio shots, lifestyle, or both)

If the user gives you a URL and product info upfront, crack on — don't ask unnecessary questions.

### Step 2: Brand DNA Research

Run the Brand DNA research process. Load `references/brand-dna-prompt.md` for the full research prompt. This has four phases:

1. **External Research** — web search for brand guidelines, fonts, colours, packaging, design agency
2. **On-Site Analysis** — visit the URL and analyse voice, photography style, typography, colour application, layout
3. **Competitive Context** — find 2-3 direct competitors, note visual differentiation
4. **Output** — compile into a structured Brand DNA document

The Brand DNA must include:
- Exact hex colour codes (e.g. `#2BBFFF`), not vague colour names
- Font names where possible
- Photography direction (lighting, composition, mood)
- An **Image Generation Prompt Modifier** — a 40-60 word paragraph prepended to every prompt

Present the Brand DNA to the user for review before generating prompts. They may want to tweak colours or mood.

### Step 3: Template Selection

Load `references/templates.md` to access all product photography templates. Present them grouped by category:

**Studio Product Shots** (clean, commercial)
- 1. Hero Product Shot — clean background, single product, magazine quality
- 2. Product Array / Colour Range — multiple variants or colours displayed together
- 3. Ingredient Explosion — product surrounded by ingredients or components
- 4. Packaging Detail — close-up on label, texture, materials
- 5. Product in Use — hands holding/using the product, studio setting
- 6. Scale Shot — product next to everyday object for size reference
- 7. Unboxing / Packaging System — box open, contents visible, premium feel

**Lifestyle / Contextual** (real-world settings)
- 8. Flat Lay — overhead arrangement with props on styled surface
- 9. Environment Shot — product in its natural habitat (kitchen, bathroom, desk, gym)
- 10. Morning Routine — product as part of a daily ritual scene
- 11. Social Moment — product in a social/sharing context
- 12. Seasonal / Mood — product styled for a specific season or vibe
- 13. In-Action / Motion — product being actively used, dynamic feel
- 14. Styled Vignette — curated corner/scene with product as focal point

**E-Commerce Ready** (listing-optimised)
- 15. White Background Hero — Amazon/Shopify standard, pure white, sharp
- 16. Infographic Layout — product with callout annotations pointing to features
- 17. Comparison Shot — your product vs generic alternative, side by side
- 18. Bundle / Set Display — multiple products arranged as a collection

**Brand Storytelling** (editorial feel)
- 19. Texture & Material Close-Up — macro detail shot, premium feel
- 20. Behind the Scenes — raw/making-of aesthetic, authenticity play

Let the user pick by number, category, or ask you to recommend. When recommending, consider the product type — e.g. food/drink benefits from ingredient explosions and flat lays, tech from hero shots and in-action, beauty from texture close-ups and routines.

The user can say "all 20", pick specific numbers, pick categories, or ask for a recommended set (typically 6-10 is a solid product photography batch).

### Step 4: Generate Prompts

For each selected template:

1. Load the template from `references/templates.md`
2. Fill in every `[PLACEHOLDER]` with brand-specific details from the Brand DNA — use hex codes for all colours, real font names, real product details
3. Prepend the Image Generation Prompt Modifier from the Brand DNA
4. If the user attached product images, reference them: "Use the attached images as brand reference"
5. Set the aspect ratio based on the template's recommendation
6. Zero leftover placeholders — every `[BRACKET]` must be replaced with real brand-specific content

When recommending templates, briefly explain *why* each suits this specific product and brand.

**Output format depends on Step 0 choice:**

#### Nano Banana Studio (JSON array)

```json
[
  {"prompt": "Use the attached images as brand reference. [Brand modifier]. [Full prompt]", "ratio": "1:1"},
  {"prompt": "...", "ratio": "4:5"},
  {"prompt": "...", "ratio": "16:9", "model": "pro"}
]
```

Rules:
- `prompt` is clean natural language (not nested JSON)
- `ratio` matches the template's recommended aspect ratio
- Default to `nb2` (omit `model` key). Add `"model": "pro"` only for templates needing precise detail (macro shots, infographic layouts)
- Tell the user: *"Paste this into Nano Banana Studio -> Bulk Import"*

#### Higsfield (plain text)

Output each prompt as a numbered section with the template name.

### Step 5: Iterate

After the first batch, offer refinements:

- **Swap backgrounds** — try a different surface or environment
- **Adjust lighting** — warmer, cooler, more dramatic, softer
- **Change angles** — overhead, eye-level, low angle, 3/4 view
- **Add/remove props** — more lifestyle context or cleaner isolation
- **Colour correction** — if brand colours aren't coming through strong enough, tighten the ColorRestriction

The JSON structure makes surgical edits easy — change one key without rewriting the whole prompt.

## Tips for Better Results

- **Product images are king.** Attaching 1-3 product images dramatically improves output. Always reference them in prompts.
- **Hex codes, not colour names.** "Deep teal" is ambiguous. `#008080` is not.
- **Aspect ratios:** 1:1 for social/e-commerce, 4:5 for Instagram feed, 16:9 for banners/hero images, 9:16 for Stories
- **Model choice:** Use `nb2` for speed. Switch to `pro` for macro/detail shots and infographic layouts where precision matters.
- **Surface and props** matter as much as the product. A premium product on a scratched table looks cheap. Match surface materials to the brand's positioning.

## Resources

### references/

- `brand-dna-prompt.md` — The full Master Brand Research prompt. Run this in Step 2 to generate the Brand DNA document. Shared with the ad-creative skill.
- `templates.md` — All 20 product photography templates with placeholders. Load this in Steps 3-4.
