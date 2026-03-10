---
name: nano-banana-prompting
description: "Craft optimized prompts for Nano Banana Pro and Nano Banana 2 (Gemini image generation) using JSON-structured prompting. Use this skill whenever a user wants help writing, improving, or structuring an image generation prompt — whether they say 'prompt', 'image gen', 'Gemini', 'nano banana', or just describe an image they want to create with AI. Trigger especially when users mention: generating product photos, character consistency across images, color bleeding problems, wanting a specific camera/film aesthetic, JSON prompting, structured prompts, or creating illustrations for a project (children's books, posters, social media). Even if the user doesn't explicitly mention 'nano banana' or 'Gemini' — if they're asking for help writing a prompt that will be used for AI image generation, this skill applies."
---

# Nano Banana Prompting

Craft high-quality, structured prompts for Nano Banana Pro and Nano Banana 2 (Gemini image generation). The core technique is **JSON-structured prompting** — organizing image descriptions into distinct key-value pairs that the model processes independently, producing more consistent, controllable results than freeform text.

## Why JSON Prompts?

Natural language prompts are fine for quick exploration, but they have a fundamental problem: adjectives bleed across concepts. "A woman in a red dress standing in a blue-lit cyberpunk alley" often results in the red tinting the alley or the blue creeping into the dress. JSON solves this by giving each visual element its own isolated key — the model treats them as separate instructions.

JSON prompts also enable:
- **Iterability** — change one key (e.g., Background) without touching anything else
- **Consistency** — same character across multiple images with <3% variation
- **Speed** — structured input processes faster than the model parsing freeform text

## Workflow

### Step 1: Understand What They Want

Ask 2-3 focused questions using `AskUserQuestion`. The goal is to identify:

1. **What kind of image?** (photo, illustration, product shot, poster, diagram, etc.)
2. **What's the subject?** (person, object, scene, concept)
3. **Any special needs?** (text in image, specific era/style, reference images provided, multiple panels)

Keep it quick — get enough to pick a template, then refine in the prompt itself. Don't interrogate them with 10 questions before producing anything.

If the user already provided a detailed description, skip questions and go straight to building the JSON prompt.

### Step 2: Build the JSON Prompt

Construct a JSON prompt using the community-standard structure. Load `references/guide.md` for the full template library and technique details.

#### The Core JSON Structure

Every prompt starts from this skeleton:

```json
{
  "label": "descriptive-name",
  "tags": ["style-anchor-1", "style-anchor-2"],
  "Style": ["style-descriptor"],
  "Subject": ["trait line 1", "trait line 2"],
  "MadeOutOf": ["material/clothing 1", "material/clothing 2"],
  "Arrangement": "pose and spatial placement",
  "Background": "environment description",
  "ColorRestriction": ["palette constraint 1", "contrast instruction"],
  "Lighting": "source, direction, and quality",
  "Camera": {
    "type": "camera type",
    "lens": "focal length",
    "aperture": "f-stop",
    "flash": "flash setting"
  },
  "OutputStyle": "rendering style",
  "Mood": "emotional tone"
}
```

**Key principles when filling this out:**

- **Subject**: Break traits into separate array items, not one long sentence. Each item = one visual concept the model processes independently.
- **ColorRestriction**: This is the single most impactful key for visual coherence. Always include it. Without it, the model tends to produce garish, inconsistent palettes.
- **Camera**: Specify settings like a real photographer would — aperture, focal length, and lens type dramatically affect the look. Shallow depth of field (f/1.4-2.8) for portraits, deeper (f/8-16) for products and landscapes.
- **MadeOutOf**: Prevents generic "plastic-looking" textures. Be specific about materials.
- **Lighting**: Describe source, direction, AND quality. "Soft diffused window light from the left" is much better than just "natural lighting."

Not every key is needed for every prompt. A simple scene might only need Style, Subject, Background, Lighting, and Mood. The guide has specific templates for different use cases — load it to match the right template to the user's needs.

### Step 3: Select Techniques

Based on what the user wants, apply relevant techniques from `references/guide.md`:

| User Need | Technique |
|-----------|-----------|
| Photo-realistic image | Photography Terms — camera settings, film stocks, lens choices |
| Specific era look (90s film, Polaroid, etc.) | Vibe Library — era-specific presets and aesthetic anchors |
| Magazine cover / poster with text | Physical Object Framing — describe it as a real printed thing |
| "How X would see Y" / conceptual | Perspective Framing — use viewpoint as creative lens |
| Diagram or infographic | Educational Imagery — labels, arrows, structured layout |
| Edit an existing image | Image Transformation — describe changes to reference |
| Multiple views in one image | Multi-Panel Output — grid/collage layout instructions |
| Same character across images | Character Consistency — consistency_id + trait anchoring |
| Multiple reference images | Reference Role Assignment — assign purpose to each image |
| Exclude unwanted elements | Negative Prompts — specify what NOT to include |
| Specific dimensions | Aspect Ratio control — native ratios for each model |

### Step 4: Present the Prompt

Show the user the complete JSON prompt with:

1. **The prompt itself** — formatted and ready to paste
2. **A brief note on why you chose this structure** — which techniques you applied and why
3. **One or two variations to try** — e.g., "swap the Camera aperture to f/1.4 for more bokeh" or "change Background for a different vibe"

Present the JSON in a clean code block. If the user wants it for API use, wrap it in the appropriate code (Python, JavaScript, or cURL) — see the API reference section in the guide.

### Step 5: Iterate and Refine

If the user wants changes, modify only the relevant keys. This is one of JSON prompting's biggest strengths — surgical edits without rewriting the whole prompt.

Common refinements:
- **Too busy/chaotic** → Tighten ColorRestriction, simplify Background
- **Wrong mood** → Adjust Lighting and Mood keys
- **Character looks different** → Add consistency_id, be more specific in Subject
- **Text not rendering well** → Use explicit quotes: `"the sign reads 'OPEN 24/7'"`

### Step 6: Hand Off to Generation

When the prompt is ready, recommend using the **nano-banana** skill to actually generate the image:

> "Your prompt is ready! Want me to generate the image now using the nano-banana skill?"

If the user agrees, invoke the `nano-banana` skill with the crafted prompt.

## Model Differences

| Feature | Nano Banana Pro | Nano Banana 2 |
|---------|----------------|---------------|
| Model ID | `gemini-3-pro-image-preview` | `gemini-3.1-flash-image-preview` |
| Speed | Slower (Pro-tier) | Fast (Flash-tier) |
| Cost | Higher | ~30-50% less |
| Max resolution | 1K, 2K, 4K | 512px, 1K, 2K, 4K |
| Exclusive aspect ratios | — | 4:1, 1:4, 8:1, 1:8 |
| Text rendering | Best in class | Very good |
| Thinking | Advanced | Configurable levels |
| Search grounding | Yes | Yes |

**When to recommend which:**
- **Nano Banana Pro**: Complex scenes, precise text rendering, maximum quality
- **Nano Banana 2**: Fast iteration, cost-sensitive workflows, banner/infographic formats (exclusive aspect ratios)

## Resources

### references/

- `guide.md` — Complete reference with JSON templates for every use case (product photography, portraits, scenes, illustrations, etc.), technique details with examples, API code samples, and enumerated field values. Load this when constructing prompts.
