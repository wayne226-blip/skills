---
name: ad-creative
description: "Generate bulk ad image prompts for any brand using Nano Banana 2 or Higsfield. Takes a brand name + URL, researches the brand, then produces ready-to-use image prompts from a playbook of 40 proven ad formats. Use this skill whenever someone wants to create ad creatives, generate ad images, make social media ads, build a batch of ad prompts, or mentions 'ad creative' + any image generation tool. Also trigger when: the user has a brand/product and wants multiple ad variations, wants to create Facebook/Instagram/TikTok ad images, mentions 'Adcrate', 'Higsfield', or wants brand-specific image prompts at scale. Even if they just say 'make ads for [brand]' or 'I need ad images for my product' — this skill applies."
---

# Ad Creative Generator

Turn any brand into a batch of production-ready ad image prompts. Based on the Adcrate workflow: research the brand, pick ad formats from a 40-template playbook, and generate brand-specific prompts ready to paste into Nano Banana Studio or Higsfield.

## Workflow

### Step 0: Output Format

Before anything else, ask the user one question:

> Where will you generate these images?
> 1. **Nano Banana Studio** — I'll give you a JSON array to paste into Bulk Import
> 2. **Higsfield** — I'll give you plain text prompts, one at a time
> 3. **Other** — tell me the tool and I'll adapt

This determines the output format for Step 3. Don't ask again — remember their choice for the rest of the session.

### Step 1: Brand DNA

Collect two things from the user:

- **Brand name** (required)
- **Brand URL** (required — this is how we research the brand)
- **Product images** (optional — the user can attach images of the specific product they want ads for)

Then run the Brand DNA research process. Load `references/brand-dna-prompt.md` for the full research prompt — it has four phases:

1. **External Research** — web search for brand guidelines, fonts, colors, packaging, design agency, ad library
2. **On-Site Analysis** — visit the URL and analyse voice, photography style, typography, color application, layout, packaging
3. **Competitive Context** — find 2-3 direct competitors, note visual differentiation
4. **Output** — compile into a structured Brand DNA document

The Brand DNA document includes an **Image Generation Prompt Modifier** — a 50-75 word paragraph that gets prepended to every image prompt to match the brand's visual identity. This is the key output from this step.

**Critical: hex codes and specifics.** The Brand DNA must include exact hex color codes (e.g. `#2BBFFF`), not just color names. When generating prompts in Step 3, always use the hex codes from the Brand DNA — not vague descriptions like "deep teal" or "warm brown". Specificity is what makes AI-generated images match the real brand. Same applies to font names, product dimensions, and packaging details — the more precise, the better the output.

Present the Brand DNA to the user for review before moving on. They may want to adjust colors, tone, or positioning.

### Step 2: Template Selection

Load `references/templates.md` to access all 40 ad formats. Present them grouped by category:

**Social Proof & Reviews** (trust-building)
- 3. Testimonials
- 6. Social Proof
- 11. Pull-Quote Review Card
- 15. Social Comment Screenshot + Product
- 16. Curiosity Gap / Hook Quote Testimonial
- 17. Verified Review Card
- 19. Highlighted / Annotated Testimonial
- 24. Product + Comment Callout (Faux Social Proof)
- 29. UGC + Viral Post Overlay
- 38. UGC Lifestyle + Product + Review Card

**Product Showcase** (hero shots + features)
- 1. Headline
- 4. Features/Benefits Point-Out
- 5. Bullet-Points
- 12. Lifestyle Action + Product Colorway Array
- 13. Stat Surround / Callout Radial (Product Hero)
- 14. Bundle Showcase + Benefit Bar
- 18. Stat Surround / Callout Radial (Lifestyle Flatlay)
- 27. Benefit Checklist Showcase
- 28. Feature Arrow Callout / Product Annotation
- 30. Hero Statement + Icon Benefit Bar
- 35. Hero Product Showcase + Stat Bar

**Comparison & Competition** (us vs them)
- 7. Us vs Them
- 25. Us vs. Them Color Split
- 31. Comparison Grid / Table

**Lifestyle & UGC** (native-looking)
- 8. Before & After (UGC Native)
- 22. Flavor Story / "Tastes Like"
- 32. UGC Story Callout / Text Bubble Explainer
- 36. Whiteboard Before / After + Product Hold
- 40. Native / Ugly Post-It Note Style

**Bold Creative** (scroll-stoppers)
- 9. Negative Marketing (Bait & Switch)
- 21. Bold Statement / Reaction Headline
- 23. Long-Form Manifesto / Letter Ad
- 39. Curiosity Gap + Scroll-Stopper Hook

**Editorial & Press** (authority)
- 10. Press/Editorial
- 20. Advertorial / Editorial Content Card
- 33. Faux Press / News Articles Screenshot
- 34. Faux iPhone Notes / App Screenshot

**Promotional** (offers + CTAs)
- 2. Offer/Promotion
- 26. Stat Callout (Data-Driven Lifestyle)
- 37. Hero Statement + Icon Bar + Offer Burst (Promo)

Let the user pick by number, category, or ask you to recommend. When recommending, consider the brand type — e.g. food/supplement brands benefit from flavour stories and stat callouts, fashion brands from lifestyle + comparison, SaaS from editorial + bold statements.

The user can say "all 40", pick specific numbers, pick categories, or ask for a recommended set (typically 8-15 is a good batch).

### Step 3: Generate Prompts

For each selected template:

1. Load the template from `references/templates.md`
2. Fill in every `[PLACEHOLDER]` with brand-specific details from the Brand DNA document — use hex codes for all colors (e.g. `#2BBFFF` not "electric blue"), real font names, real product names, real stats from the brand's site
3. Prepend the Image Generation Prompt Modifier from the Brand DNA (keep it tight — 40-60 words max, focused on colors with hex codes, photography style, and mood)
4. If the user attached product images, reference them in the prompt ("Use the attached images as brand reference")
5. Set the aspect ratio based on the template's recommendation
6. Zero leftover placeholders — every `[BRACKET]` must be replaced with real brand-specific content. If you don't have the info, make a reasonable choice based on the Brand DNA rather than leaving a bracket

When recommending templates, briefly explain *why* each one suits this specific brand. For example: "Us vs Them (#7) — strong pick because Aloha already positions against conventional protein bars on their site" rather than just listing numbers.

**Output format depends on Step 0 choice:**

#### Nano Banana Studio (JSON array)

Output a single JSON array ready to paste into Bulk Import:

```json
[
  {"prompt": "Use the attached images as brand reference. Match the exact product colors... [full prompt]", "ratio": "4:5"},
  {"prompt": "...", "ratio": "1:1"},
  {"prompt": "...", "ratio": "9:16", "model": "pro"}
]
```

Rules:
- `prompt` is clean natural language (not nested JSON) — the Studio sends it directly to the API
- `ratio` matches the template's recommended aspect ratio
- Default to `nb2` (omit `model` key). Only add `"model": "pro"` for templates that need precise text rendering or very complex compositions (e.g. comparison grids, manifesto ads)
- Tell the user: *"Paste this into Nano Banana Studio → Bulk Import"*

#### Higsfield (plain text)

Output each prompt as a numbered section:

```
## 1. Headline Ad
[full prompt text]

## 7. Us vs Them
[full prompt text]
```

Tell the user to copy each prompt individually into Higsfield.

### Tips for Better Results

- **Product images matter.** Attaching 1-3 product images dramatically improves output quality. The prompts reference them with "Use the attached images as brand reference."
- **Aspect ratios:** 1:1 and 4:5 work for most feed ads. 9:16 for Stories/Reels. 16:9 for landscape/banner.
- **Model choice:** Use `nb2` for speed. Switch individual prompts to `pro` if text rendering or fine detail is critical.
- **Copy quality:** The templates include placeholder copy. The Brand DNA research gives Claude enough context to write decent copy, but the user should review and refine headlines for their specific campaign.

## Resources

### references/

- `brand-dna-prompt.md` — The full Master Brand Research prompt. Run this in Step 1 to generate the Brand DNA document.
- `templates.md` — All 40 ad format templates with placeholders. Load this in Steps 2-3.
