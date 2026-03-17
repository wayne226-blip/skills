---
name: photo-director
description: "Plan and execute a complete product photography shoot for any brand. Acts as an AI photography director — researches the brand, analyses the product, selects the right shot types from a 25-template library, plans lighting/angles/props/contexts with a narrative arc, and outputs both a creative brief document AND a Nano Banana Studio bulk import JSON array. Use this skill when someone wants product photography planned for a brand, wants a photo shoot planned, wants product images for e-commerce or social media, or says things like 'plan a shoot', 'product photos for [brand]', 'photography director', 'shoot plan', 'product photography', 'photo shoot for', 'brand photography'. Distinct from ad-creative (which generates AD format images like testimonials, comparison grids, and social proof cards) — photo-director generates actual PRODUCT PHOTOGRAPHY (hero shots, lifestyle scenes, flat lays, e-commerce listings). Distinct from nano-banana-prompting (which helps craft individual prompts one at a time) — photo-director plans an entire SHOOT as a cohesive set with narrative arc."
---

# Photo Director

Plan a complete product photography shoot like a professional photographer. Research the brand, analyse the product, select the right shots, and generate everything in one go.

**Two outputs:** a creative brief (markdown doc) + a Nano Banana Studio bulk import JSON array.

## Workflow

### Step 1: Intake

Collect from the user:

- **Product name + description** (required) — what is it, what does it look like, key features
- **Brand URL** (required) — this is how we research the brand
- **Product images** (optional, recommended) — attaching 1-3 product images dramatically improves prompt quality
- **Intended use** (optional, default: all-purpose):
  - **E-commerce** — marketplace listings, product pages
  - **Social media** — Instagram, TikTok, Facebook
  - **Catalogue / lookbook** — brand website, print materials
  - **All-purpose** — a versatile set covering all channels
- **Shot count** (optional, default: standard):
  - **Small** — 6-8 focused shots
  - **Standard** — 10-12 shots (recommended)
  - **Comprehensive** — 15-20 shots for a complete library

If the user gives product + brand URL upfront, proceed with defaults — don't interrogate. Only ask about intended use and shot count if it's unclear or if they want something specific.

### Step 2: Brand DNA

Load `references/brand-dna-prompt.md` and run the 4-phase brand research:

1. **External Research** — web search for brand guidelines, fonts, colours, packaging, design agency, ad library
2. **On-Site Analysis** — visit the URL and analyse voice, photography style, typography, colour application, layout, packaging
3. **Competitive Context** — find 2-3 direct competitors, note visual differentiation
4. **Output** — compile into a structured Brand DNA document

**Critical:** The Brand DNA must include:
- Exact hex colour codes (e.g. `#2BBFFF`), not just colour names
- Real font names
- An **Image Generation Prompt Modifier** — a 50-75 word paragraph to prepend to every image prompt

Present the Brand DNA to the user for review before moving on. They may want to adjust colours, tone, or positioning.

### Step 3: Director's Brief

This is where the skill earns its name. Load `references/director-prompt.md` and think like a photography director.

**Analyse the product:**
- Physical properties: shape, size, texture, reflectivity, transparency
- Key visual features: logo placement, distinctive shape, unique detail
- Photography challenges: reflective surfaces, small size, dark colours

**Consider the brand:**
- Photography style from Brand DNA
- Premium vs accessible positioning
- Existing imagery patterns

**Select shots using the narrative arc:**
1. **Opening** (1-2 shots) — hero/first impression shots
2. **Exploration** (2-4 shots) — detail/feature/ingredient shots
3. **Desire** (3-5 shots) — lifestyle/context shots that build emotional connection
4. **Conversion** (2-3 shots) — e-commerce/comparison shots that drive purchase

For each shot, explain:
- Why it was chosen for THIS product and brand
- Specific creative choices (surface, props, lighting, angle)
- How it fits the overall narrative

**Present the Creative Brief** for user review before generating prompts:

```markdown
# [Brand] Product Photography — Creative Brief

## Shoot Overview
[2-3 sentences: product, brand, visual strategy]

## Shot List

### 1. [Template Name] (Template #X)
**Purpose:** [What this shot communicates — 1 sentence]
**Key choices:** [Specific surface, props, lighting direction, camera angle]
**Brand fit:** [How this connects to the Brand DNA — 1 sentence]
**Ratio:** [aspect ratio] | **Model:** [nb2 or pro]

### 2. ...
[repeat for each shot]

## Narrative Arc
[1-2 sentences on how the shots flow as a set]
```

Wait for user approval. They may want to swap shots, add seasonal context, or adjust the mood.

### Step 4: Generate Prompts

For each approved shot:

1. Load the matching template from `references/templates.md`
2. Fill ALL `[PLACEHOLDERS]` with brand-specific details from the Brand DNA — use hex codes for colours, real font names, real product details
3. Prepend the **Image Generation Prompt Modifier** from the Brand DNA (keep it tight — 50-75 words max)
4. Apply JSON prompting principles from `references/json-prompting-guide.md`:
   - Always include ColorRestriction thinking (use hex codes from Brand DNA)
   - Match camera settings to the shot type (see the guide's reference table)
   - Use Pro model only for detail/macro, text-heavy, or multi-angle grid shots
5. If the user attached product images, include "Use the attached images as brand reference" at the start

**Zero leftover placeholders** — every `[BRACKET]` must be replaced with real brand-specific content. If you don't have the info, make a reasonable choice based on the Brand DNA.

### Step 5: Output

Produce two deliverables:

**1. Creative Brief (markdown file)**

Save as `[brand]-photo-shoot-brief.md` in the current working directory. This is the document you'd hand to a real photographer — it explains the thinking behind each shot.

**2. JSON Array (code block)**

Ready to paste into Nano Banana Studio's Bulk Import:

```json
[
  {"prompt": "[Image Generation Prompt Modifier]. [Full prompt text]...", "ratio": "1:1"},
  {"prompt": "[Image Generation Prompt Modifier]. [Full prompt text]...", "ratio": "4:5"},
  {"prompt": "[Image Generation Prompt Modifier]. [Full prompt text]...", "ratio": "4:5", "model": "pro"}
]
```

**Rules:**
- `prompt` is clean natural language (not nested JSON) — Nano Banana Studio sends it directly to the API
- `ratio` matches each template's recommended aspect ratio
- Default to NB2 (omit `model` key). Only add `"model": "pro"` for templates that need precise text rendering, macro detail, or complex multi-angle compositions
- Tell the user: *"Paste this into Nano Banana Studio → Bulk Import"*

### Step 6: Iterate

After delivering the outputs, offer specific refinements:

- **Swap shots:** Replace individual shots with alternatives from the template library
- **Adjust mood:** Shift the overall feel (warmer, cooler, more dramatic, softer)
- **Add seasonal:** Include season-specific shots for a campaign
- **Regenerate individual prompts:** Different props, surfaces, angles, or lighting
- **Scale up/down:** Add more shots or trim to a tighter set
- **Switch channels:** Re-optimise the set for a different channel (e.g. pivot from e-commerce to social)

## Resources

### references/

- `brand-dna-prompt.md` — Master Brand Research prompt. Run this in Step 2 to generate the Brand DNA document.
- `templates.md` — All 25 product photography templates with placeholders. Load this in Steps 3-4.
- `director-prompt.md` — Photography director reasoning framework. Load this in Step 3 to guide shot selection and narrative arc planning.
- `json-prompting-guide.md` — Condensed product photography prompting reference. Use in Step 4 for camera settings, model selection, and prompt structure.
