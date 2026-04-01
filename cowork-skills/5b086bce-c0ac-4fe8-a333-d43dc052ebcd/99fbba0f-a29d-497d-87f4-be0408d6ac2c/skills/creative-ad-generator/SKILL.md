---
name: creative-ad-generator
description: "Generate 40 brand-matched creative ad images from a client's website. Scrapes the site for brand colours, fonts, and design style (Brand DNA), then produces ready-to-use prompts for all 40 proven ad formats — headlines, testimonials, UGC, comparison ads, social proof, editorial, and more. Use this skill whenever someone wants to create ad creatives for a brand, generate social media ads, make Facebook/Instagram/TikTok ad images, or mentions 'ad creatives' + a website/brand. Also trigger when: the user has a client URL and wants ad images styled to their brand, wants to batch-generate ad variations, wants scroll-stopping social ads, or says things like 'make ads for this client', 'generate 40 ad creatives', 'ad campaign images'. Even casual requests like 'create some ads for their brand' or 'make social ads matching their site' should trigger this skill. This skill complements brand-product-photography — that one does product shots, this one does ad creatives."
---

# Creative Ad Generator — 40 Proven Ad Formats

Turn any client's website into a full set of 40 production-ready ad creative prompts. The workflow: research the brand's visual identity from their URL, then generate prompts for 40 battle-tested ad formats — each filled with the client's exact brand colours, typography, product details, and voice.

These 40 templates come from Adcrate / Alex Cooper and have all been proven to one-shot successfully with Nano Banana 2 via Higsfield.

This skill pairs with **brand-product-photography** — that handles clean product shots and lifestyle photography, this handles conversion-focused ad creatives.

## Workflow

### Step 0: Output Format

Ask the user:

> Where will you generate these images?
> 1. **Nano Banana Studio** — I'll give you a JSON array for Bulk Import
> 2. **Higsfield** — plain text prompts, one at a time
> 3. **Other** — tell me the tool and I'll adapt

Remember their choice for the session.

### Step 1: Collect Inputs

Gather from the user:

- **Client website URL** (required) — this is how we extract the brand identity
- **Product images** (optional but strongly recommended — dramatically improves output quality)
- **Product description** (required) — what the product is, key features, price point, target audience
- **Key selling points** — USPs, stats, testimonials, press mentions, offers
- **Which templates** — all 40, a specific batch, or ask you to recommend based on their product type

If the user gives you everything upfront, crack on. Don't ask questions you already have answers to.

### Step 2: Brand DNA Research

Run the Brand DNA research process. Load `references/brand-dna-prompt.md` for the full research prompt.

Four phases:
1. **External Research** — web search for brand guidelines, fonts, colours, packaging, design agency
2. **On-Site Analysis** — visit the URL and analyse voice, photography style, typography, colour application
3. **Competitive Context** — find 2-3 direct competitors, note visual differentiation
4. **Output** — compile into a structured Brand DNA document

The Brand DNA must include:
- Exact hex colour codes (e.g. `#2BBFFF`) — never vague colour names
- Font names where possible
- Photography direction (lighting, composition, mood)
- Brand voice characteristics (for any text/copy in the ads)
- An **Image Generation Prompt Modifier** — a 40-60 word paragraph prepended to every prompt

Present the Brand DNA to the user for review before generating prompts.

### Step 3: Template Selection

Load `references/templates.md` to access all 40 ad creative templates. Present them grouped by category:

**Core Ads (The Essentials)**
1. Headline — text rendering test, clean studio product shot
2. Offer/Promotion — split background, core offer presentation
3. Testimonials — real environment + text overlay
4. Features/Benefits Point-Out — educational diagram layout
5. Bullet-Points — split composition, product left, benefits right

**Social Proof & Trust**
6. Social Proof — member count + review card + press logos
7. Pull-Quote Review Card — emotional quote over truncated review
8. Verified Review Card — mimics review platform UI
9. Highlighted/Annotated Testimonial — highlighter pen on key phrases
10. Social Comment Screenshot + Product — Facebook comment style

**Comparison & Competition**
11. Us vs Them — side-by-side, photography quality gap
12. Us vs Them Color Split — vibrant brand vs dull competitor
13. Comparison Grid/Table — structured meme-format table

**UGC & Native Feel**
14. Before & After (UGC Native) — mirror selfie transformation
15. UGC + Viral Post Overlay — selfie with Reddit/Twitter screenshot
16. UGC Story Callout / Text Bubble — Instagram Story with highlighted bubbles
17. UGC Lifestyle + Product + Review Card — vertical split casual/branded
18. Native / Ugly Post-It Note — product photo with handwritten note

**Editorial & Authority**
19. Press/Editorial — Vogue back-page energy
20. Advertorial / Editorial Content Card — looks like a news post
21. Faux Press / News Article Screenshot — publication masthead style
22. Long-Form Manifesto / Letter Ad — copy-dominant, writing IS the ad

**Product Showcase**
23. Lifestyle Action + Product Colorway Array — action hero + product lineup
24. Stat Surround / Callout Radial (Product Hero) — stats orbiting product
25. Bundle Showcase + Benefit Bar — open box with benefit strip
26. Stat Surround / Callout Radial (Lifestyle Flatlay) — stats over flatlay
27. Hero Product Showcase + Stat Bar — exploded ingredients + stat bar
28. Feature Arrow Callout / Product Annotation — hand-drawn arrow style

**Bold Creative**
29. Negative Marketing (Bait & Switch) — fake bad review that's a rave
30. Bold Statement / Reaction Headline — provocative line + gradient
31. Curiosity Gap / Hook Quote Testimonial — bait-and-switch quote
32. Curiosity Gap + Scroll-Stopper Hook — no product, pure curiosity

**Data & Stats**
33. Stat Callout (Data-Driven Lifestyle) — stat IS the headline
34. Benefit Checklist Showcase — info-dense, product + checklist + CTA

**Conversion & Offers**
35. Hero Statement + Icon Benefit Bar — power statement + icons
36. Hero Statement + Icon Bar + Offer Burst — promo variant with discount badge
37. Flavor Story / "Tastes Like" — flavour visualization
38. Whiteboard Before/After + Product Hold — casual educational
39. Product + Comment Callout (Faux Social Proof) — studio shot + comment
40. Faux iPhone Notes / App Screenshot — disguised as Notes app

Let the user pick by number, category name, or ask for recommendations. When recommending, consider:
- **E-commerce / DTC brands**: Start with 1, 2, 4, 6, 7, 11, 24, 27 (core conversion set)
- **Supplement / health brands**: Add 3, 8, 14, 19, 30, 31, 33, 35 (trust + transformation)
- **Food / beverage**: Add 22, 25, 37, 40 (flavour + appetite appeal)
- **Tech / SaaS**: Focus on 1, 4, 5, 11, 13, 20, 23, 34 (features + comparison)
- **Beauty / skincare**: Add 3, 7, 14, 17, 19, 26, 32 (social proof + UGC)

The user can say "all 40", pick specific numbers, pick categories, or ask for a recommended batch.

### Step 4: Gather Ad-Specific Content

Before generating, collect the content that fills the templates. This varies by template but typically includes:

- **Headlines and copy** — the user's actual ad copy, or ask them to provide key messages and you'll write variations
- **Testimonials / reviews** — real customer quotes, star ratings, reviewer names
- **Stats and claims** — specific numbers (e.g. "900k+ customers", "20g protein")
- **Offers** — discount percentages, promo codes, free trial details
- **Competitor info** (for comparison ads) — category name for the competitor side
- **Press mentions** — publication names, pull quotes

If the user doesn't have all this ready, help them draft it. Write punchy ad copy that matches the brand voice from the Brand DNA.

### Step 5: Generate Prompts

For each selected template:

1. Load the template from `references/templates.md`
2. Fill in every `[PLACEHOLDER]` with brand-specific details from the Brand DNA and the ad content gathered in Step 4
3. Prepend the Image Generation Prompt Modifier from the Brand DNA
4. If the user attached product images, include: "Use the attached images as brand reference"
5. Set the aspect ratio per the template's recommendation
6. **Zero leftover placeholders** — every `[BRACKET]` must be replaced with real brand-specific content

**Output format depends on Step 0 choice:**

#### Nano Banana Studio (JSON array)

```json
[
  {"prompt": "Use the attached images as brand reference. [Brand modifier]. [Full prompt]", "ratio": "4:5"},
  {"prompt": "...", "ratio": "9:16"},
  {"prompt": "...", "ratio": "1:1"}
]
```

Rules:
- `prompt` is clean natural language (not nested JSON)
- `ratio` matches the template's recommended aspect ratio
- Default to `nb2` (omit `model` key). Add `"model": "pro"` for templates requiring precise text rendering (1, 2, 4, 5, 16, 34)
- Tell the user: *"Paste this into Nano Banana Studio -> Bulk Import"*

#### Higsfield (plain text)

Output each prompt as a numbered section with the template name and ratio noted.

### Step 6: Batch Strategy

For all 40, generate in batches of 10 to keep things manageable:
- **Batch 1** (templates 1-10): Core ads + social proof
- **Batch 2** (templates 11-20): Comparison + UGC + editorial
- **Batch 3** (templates 21-30): Showcase + bold creative
- **Batch 4** (templates 31-40): Data + conversion + native

After each batch, check with the user before continuing. They might want to adjust the brand modifier or copy direction based on early results.

### Step 7: Iterate

After generating, offer refinements:
- **Copy variants** — try different headlines, hooks, or testimonials in the same template
- **Colour adjustments** — tighten or loosen the brand colour restrictions
- **Format swaps** — switch a 1:1 to 9:16 for Stories, or 4:5 for feed
- **A/B versions** — generate two variations of the same template with different hooks
- **New templates** — if the user describes a format not in the 40, create a custom template following the same structure

## Tips for Better Results

- **Product images are essential.** Every template starts with "Use the attached images as brand reference" — provide 2-3 clear product photos.
- **Real testimonials convert better.** Even if AI-generated, make them specific (name, credential, timeframe, emotional detail).
- **Hex codes, not colour names.** "#2BBFFF" beats "bright blue" every time.
- **UGC templates should look ugly on purpose.** Don't over-polish templates 14, 15, 16, 17, 18, 29, 32 — the rawness IS the point.
- **Text rendering:** Nano Banana Pro handles text better than NB2. For text-heavy templates (1, 2, 22, 23), consider using `"model": "pro"`.

## Resources

### references/

- `brand-dna-prompt.md` — The full Master Brand Research prompt for Step 2. Shared with brand-product-photography.
- `templates.md` — All 40 ad creative templates with placeholders. The complete Adcrate template library.
