# Master Brand Research Prompt

Use this prompt to research a brand and produce a Brand DNA document. Replace the two input variables, then follow all four phases.

Credit: Will Sartorius (original concept), adapted by Adcrate.

---

## Input Variables

- **Target Brand Name:** [BRAND NAME]
- **Target URL:** [URL]

## Role

Act as a Senior Brand Strategist conducting a full reverse-engineering of the target brand's visual and verbal identity.

## Objective

Create a comprehensive Brand DNA document that will be used to write highly specific AI image generation prompts. Every detail matters because the output will be fed into an image model that needs exact specifications.

---

## Phase 1: External Research

Use web search to find the source of truth for this brand:

1. **Design credits:** Search for "who designed [Brand] branding", "[Brand] design agency case study", "[Brand] rebrand"
2. **Public brand assets:** Search for "[Brand] brand guidelines pdf", "[Brand] press kit", "[Brand] media kit", "[Brand] style guide"
3. **Typography:** Search for "[Brand] font", "[Brand] typeface", "what font does [Brand] use"
4. **Colors:** Search for "[Brand] brand colors", "[Brand] hex codes", "[Brand] color palette"
5. **Packaging:** Search for "[Brand] packaging design", "[Brand] unboxing", "[Brand] product photography"
6. **Advertising:** Search "[Brand]" in Meta Ad Library (facebook.com/ads/library) for current ad creative styles
7. **Press and positioning:** Search for "[Brand] brand story", "[Brand] founding story", "[Brand] mission"

## Phase 2: On-Site Analysis

Visit the Target URL and analyse:

1. **Voice and Tone:** Read hero copy, About page, and product descriptions. Give 5 distinct adjectives.
2. **Photography Style:** Describe lighting, color grading, composition, and subject matter.
3. **Typography on site:** Headline weight, body weight, letter-spacing, distinctive treatments.
4. **Color application:** Primary vs accent usage. Background colors. CTA color.
5. **Layout density:** Airy or dense? Grid-based or organic?
6. **Packaging details:** Physical appearance (materials, colors, shape, label placement, textures, translucency, matte vs gloss).

## Phase 3: Competitive Context

Search for 2-3 direct competitors and note visual differentiation.

## Phase 4: Output

Combine into this format:

```
BRAND DNA DOCUMENT
==================

BRAND OVERVIEW
Name / Tagline / Design Agency / Voice Adjectives [5] / Positioning / Competitive Differentiation

VISUAL SYSTEM
Primary Font [exact name] / Secondary Font [exact name] / Primary Color [name + hex, e.g. "Electric Blue #2BBFFF"] / Secondary Color [name + hex] / Accent Color [name + hex] / Background Colors [with hex] / CTA Color and Style [with hex]

PHOTOGRAPHY DIRECTION
Lighting / Color Grading / Composition / Subject Matter / Props and Surfaces / Mood

PRODUCT DETAILS
Physical Description / Label-Logo Placement / Distinctive Features / Packaging System

AD CREATIVE STYLE
Typical formats / Text overlay style / Photo vs illustration / UGC usage / Offer presentation

IMAGE GENERATION PROMPT MODIFIER
Write a single 40-60 word paragraph to prepend to any image prompt to match this brand's visual identity. Must include: hex color codes (e.g. #2BBFFF), font names, photography style (lighting + composition), and mood. Use hex codes, not color names. This paragraph gets prepended to every prompt so keep it tight and specific.
```
