# Nano Banana Prompting Guide

Complete reference for JSON-structured image generation prompts. Use this when constructing prompts — find the right template for the user's need and adapt it.

## Table of Contents

1. [JSON Templates by Use Case](#1-json-templates-by-use-case)
2. [Technique Details](#2-technique-details)
3. [Enumerated Field Values](#3-enumerated-field-values)
4. [API Code Samples](#4-api-code-samples)
5. [Common Patterns & Tips](#5-common-patterns--tips)

---

## 1. JSON Templates by Use Case

### Product Photography

Clean, commercial-quality product images.

```json
{
  "label": "product-hero-shot",
  "tags": ["product-photography", "minimalist"],
  "Style": ["studio-product-photography", "clean-minimal"],
  "Subject": [
    "modern wireless headphones, matte black finish",
    "premium build quality, soft ear cushions visible"
  ],
  "MadeOutOf": ["brushed aluminum", "memory foam", "soft-touch plastic"],
  "Arrangement": "product resting at 30-degree angle on reflective surface",
  "Background": "clean white gradient, subtle shadow",
  "ColorRestriction": ["monochrome palette", "black product on white", "no color accents"],
  "Lighting": "soft diffused studio lighting, subtle rim light from behind",
  "Camera": {
    "type": "medium format digital",
    "lens": "85mm macro",
    "aperture": "f/5.6",
    "flash": "off, continuous studio lights"
  },
  "OutputStyle": "commercial product photography, magazine quality",
  "Mood": "premium, sophisticated"
}
```

**Key choices for product shots:**
- Camera: medium format or DSLR, 85-100mm macro lens, f/5.6-f/11 for sharpness
- Lighting: soft, diffused, rim light for edge definition
- Background: infinite white curve or solid gradient
- ColorRestriction: keep it tight — let the product be the color focus

### Portrait Photography

People-focused images with controlled depth of field.

```json
{
  "label": "environmental-portrait",
  "tags": ["portrait", "natural-light"],
  "Style": ["editorial-portrait", "magazine-feature"],
  "Subject": [
    "woman in her 30s, confident expression",
    "dark curly hair, warm skin tone",
    "looking slightly off-camera, gentle smile"
  ],
  "MadeOutOf": [
    "navy wool blazer, gold buttons",
    "white cotton shirt, open collar",
    "small gold hoop earrings"
  ],
  "Arrangement": "seated in leather armchair, leaning slightly forward",
  "Background": "modern office with floor-to-ceiling windows, city skyline soft in background",
  "RoomObjects": ["potted monstera plant", "stack of hardcover books", "ceramic coffee mug"],
  "ColorRestriction": ["warm neutral tones", "navy and gold accents", "no bright colors"],
  "Lighting": "large window light from the left, soft fill from right, warm color temperature",
  "Camera": {
    "type": "mirrorless full-frame",
    "lens": "85mm",
    "aperture": "f/1.8",
    "iso": "200",
    "flash": "off"
  },
  "OutputStyle": "editorial photography, natural skin tones, minimal retouching",
  "Mood": "confident, approachable, professional"
}
```

**Key choices for portraits:**
- Camera: 85mm lens is the portrait sweet spot, f/1.4-2.8 for bokeh
- Subject: break traits into separate lines — face, hair, expression, gaze direction
- Lighting: directional with fill for flattering shadows
- Always specify skin tone rendering in OutputStyle

### Cinematic Scene

Film-quality atmospheric images.

```json
{
  "label": "noir-detective",
  "tags": ["film-noir", "cinematic", "moody"],
  "Style": ["film-noir", "1940s-cinema"],
  "Subject": ["detective in trench coat, fedora casting shadow over eyes"],
  "MadeOutOf": ["worn leather trench coat", "felt fedora", "polished shoes"],
  "Arrangement": "standing under streetlight, cigarette smoke curling upward",
  "Background": "rain-slicked cobblestone alley, dim neon signs in distance",
  "ColorRestriction": ["desaturated palette", "high contrast black and white", "single warm accent from streetlight"],
  "Lighting": "harsh overhead streetlight, deep shadows, rim light from neon",
  "Camera": {
    "type": "film camera",
    "lens": "50mm",
    "aperture": "f/2.0",
    "grain": "heavy film grain"
  },
  "OutputStyle": "cinematic still, film noir aesthetic",
  "Mood": "mysterious, tense, atmospheric"
}
```

### Illustration / Stylized Art

Non-photorealistic images with specific art direction.

```json
{
  "label": "isometric-city",
  "tags": ["isometric-3d", "miniature"],
  "Style": ["isometric-3d", "miniature-tilt-shift"],
  "Subject": ["city block with shops, park, and apartments"],
  "Arrangement": "45-degree top-down isometric view, all buildings visible",
  "Background": "soft solid color, clean edge",
  "ColorRestriction": ["pastel palette", "soft warm tones", "no harsh shadows"],
  "Lighting": "soft diffused overhead, gentle shadows for depth",
  "Camera": {
    "type": "orthographic",
    "lens": "isometric projection"
  },
  "OutputStyle": "3D cartoon miniature, soft PBR textures, lifelike lighting",
  "Mood": "cheerful, inviting, playful"
}
```

### Text-Heavy (Poster / Magazine Cover)

Images that need legible text rendered correctly.

```json
{
  "label": "magazine-cover",
  "tags": ["editorial", "typography"],
  "Style": ["high-fashion-editorial", "Vogue-inspired"],
  "Subject": [
    "fashion model, dramatic pose, looking at camera",
    "bold red lipstick, slicked-back hair"
  ],
  "MadeOutOf": [
    "structured black evening gown",
    "statement diamond necklace"
  ],
  "Arrangement": "full body standing pose, slightly turned, one hand on hip",
  "Background": "solid deep burgundy",
  "Text": {
    "headline": "THE NEW BOLD",
    "subhead": "Fall Fashion Preview 2026",
    "placement": "headline large at top, subhead smaller below"
  },
  "ColorRestriction": ["red, black, burgundy only", "gold accents for jewelry", "white text"],
  "Lighting": "dramatic studio lighting, strong key light from above-right",
  "Camera": {
    "type": "medium format",
    "lens": "70mm",
    "aperture": "f/8"
  },
  "OutputStyle": "high-end magazine cover, sharp and polished",
  "Mood": "powerful, glamorous, editorial"
}
```

**Text rendering tips:**
- Always put exact text in quotes within the JSON
- Use a `Text` block to specify content and placement
- Nano Banana Pro has the best text rendering; Nano Banana 2 is very good
- Keep text short — longer phrases are more likely to have errors
- Specify font style (serif, sans-serif, handwritten) if it matters

### Educational / Infographic

Diagrams, explanations, and educational visuals.

```json
{
  "label": "water-cycle-diagram",
  "tags": ["educational", "infographic", "science"],
  "Style": ["clean-infographic", "textbook-illustration"],
  "Subject": ["the water cycle: evaporation, condensation, precipitation, collection"],
  "Arrangement": "circular flow diagram with labeled stages, arrows connecting each stage",
  "Background": "light blue gradient, clean and uncluttered",
  "Text": {
    "labels": ["Evaporation", "Condensation", "Precipitation", "Collection"],
    "placement": "each label next to its corresponding stage"
  },
  "ColorRestriction": ["blues and whites for water", "warm yellows for sun/heat", "green for ground"],
  "Lighting": "flat, even illumination, no dramatic shadows",
  "OutputStyle": "clean vector-style infographic, modern textbook quality",
  "Mood": "educational, clear, accessible"
}
```

---

## 2. Technique Details

### Photography Terms (Vibe Library)

Anchor the aesthetic to a specific era or camera style by including relevant terms:

**Era presets:**
- **1970s film**: Kodachrome colors, warm cast, soft focus, slight vignette
- **1990s disposable camera**: flash-washed faces, red-eye, slight blur, oversaturated
- **2000s digital**: slightly flat colors, auto-flash, point-and-shoot framing
- **Modern DSLR**: sharp, clean, precise exposure, professional grade
- **Polaroid**: square frame, washed-out colors, soft edges, white border

**Film stock references:**
- Kodak Portra 400 — warm skin tones, soft pastels
- Fuji Superia — cool greens, vivid colors
- Ilford HP5 — classic black and white, medium grain
- CineStill 800T — tungsten-balanced, halation around highlights

Include these in the `tags` or `Style` array to anchor the aesthetic.

### Physical Object Framing

Describe the image as a real physical object rather than a digital image:
- "A vintage travel poster printed on thick matte paper"
- "A glossy magazine cover on a newsstand"
- "A worn Polaroid photo found in a shoebox"

This gives the model a concrete reference point and naturally includes details like texture, wear, lighting on the object surface, and framing.

### Perspective Framing

Use a specific viewpoint as a creative device:
- "How a cat would see the living room — low angle, fish-eye distortion, warm afternoon light"
- "A drone's view of the city — straight down, geometric patterns, tiny people"
- "Through the eyes of a child — everything oversized, magical, saturated colors"

### Image Transformation

When editing an existing image, describe what changes to make. Keep unchanged elements implicit:

```json
{
  "label": "background-swap",
  "Style": ["maintain original style"],
  "Subject": ["keep the original subject exactly as-is"],
  "Background": "replace with sunset beach, golden hour, calm ocean",
  "Lighting": "adjust to match golden hour — warm directional light from left"
}
```

Send the reference image alongside this JSON. The model will preserve the subject and apply the changes.

### Multi-Panel Output

Request multiple views in a single image:

```json
{
  "label": "character-sheet",
  "Style": ["character-design-sheet"],
  "Subject": ["fantasy warrior, scarred face, braided hair"],
  "Arrangement": "2x2 grid: front view, side profile, back view, action pose",
  "Background": "neutral gray for each panel",
  "ColorRestriction": ["consistent palette across all panels"]
}
```

### Character Consistency

For generating the same character across multiple images:

1. Use a `consistency_id` field with a unique identifier
2. Be extremely specific in `Subject` — the more detail, the more consistent
3. Keep the same `Subject` and `MadeOutOf` blocks across prompts, changing only Arrangement, Background, etc.

```json
{
  "consistency_id": "detective-blake-001",
  "Subject": [
    "male detective, mid-40s, sharp jawline, graying temples",
    "deep-set hazel eyes, permanent five-o'clock shadow",
    "tall, lean build, slightly weathered face"
  ]
}
```

### Reference Role Assignment

When the user provides multiple reference images, assign a specific role to each:

```json
{
  "reference_images": [
    {"image": "photo1.jpg", "role": "face and identity", "strength": 0.85},
    {"image": "photo2.jpg", "role": "clothing style only"},
    {"image": "photo3.jpg", "role": "background and environment"}
  ]
}
```

### Negative Prompts

Specify what to exclude. Add as a separate key:

```json
{
  "NegativePrompt": [
    "no watermarks or text overlays",
    "no extra fingers or distorted hands",
    "avoid oversaturation"
  ]
}
```

### Aspect Ratio & Resolution

**Supported aspect ratios (both models):** 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9, 5:4, 4:5

**Nano Banana 2 exclusive:** 4:1, 1:4, 8:1, 1:8 (great for banners and social media headers)

**Resolution (Nano Banana 2):** 512px, 1K (default), 2K, 4K

Include in a `meta` block:
```json
{
  "meta": {
    "aspect_ratio": "16:9",
    "resolution": "2K"
  }
}
```

---

## 3. Enumerated Field Values

Quick reference for valid values in each field:

| Field | Values |
|-------|--------|
| `aspect_ratio` | 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9, 5:4, 4:5, 4:1*, 1:4*, 8:1*, 1:8* |
| `aperture` | f/1.4, f/2.0, f/2.8, f/4.0, f/5.6, f/8.0, f/11, f/16 |
| `focal_length` | 14mm (ultra-wide), 24mm (wide), 35mm (standard), 50mm (normal), 85mm (portrait), 135mm (telephoto), 200mm+ (super tele) |
| `shutter_speed` | 1/500s, 1/250s, 1/125s, 1/60s, 1/30s, 1/15s |
| `lighting.type` | natural, studio, dramatic, soft, rim, backlit, ambient |
| `lighting.direction` | front, side, back, top, bottom, three-quarter |
| `color_temperature` | warm, neutral, cool, daylight (5500K), tungsten (3200K), fluorescent |
| `framing` | close_up, medium_shot, full_shot, long_shot, extreme_long_shot |
| `perspective` | eye_level, high_angle, low_angle, dutch_angle, bird_eye, worm_eye |
| `depth_of_field` | shallow (f/1.4-2.8), medium (f/4-5.6), deep (f/8-16) |
| `quality/style` | ultra_photorealistic, raw, anime, 3d_render, oil_painting, sketch, pixel_art, vector_illustration, watercolor |
| `resolution`* | 512px, 1K, 2K, 4K |

*Nano Banana 2 only

---

## 4. API Code Samples

### Python (Google Gemini SDK)

```python
import json
from google import genai
from google.genai import types

client = genai.Client()

json_prompt = {
    "label": "hero-shot",
    "Style": ["product-photography"],
    "Subject": ["sleek smartwatch on wrist"],
    "Background": "clean white",
    "Lighting": "soft studio",
    "Camera": {"lens": "100mm macro", "aperture": "f/8"},
    "OutputStyle": "commercial quality",
    "Mood": "premium"
}

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",  # or "gemini-3-pro-image-preview" for Pro
    contents=[json.dumps(json_prompt)],
    config=types.GenerateContentConfig(
        image_size="2K"  # Nano Banana 2 only: 512px, 1K, 2K, 4K
    ),
)

for part in response.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        part.as_image().save("output.png")
```

### JavaScript (Google GenAI SDK)

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});

const jsonPrompt = {
  label: "hero-shot",
  Style: ["product-photography"],
  Subject: ["sleek smartwatch on wrist"],
  Background: "clean white",
  Lighting: "soft studio",
  Camera: { lens: "100mm macro", aperture: "f/8" },
  OutputStyle: "commercial quality",
  Mood: "premium"
};

const response = await ai.models.generateContent({
  model: "gemini-3.1-flash-image-preview",
  contents: JSON.stringify(jsonPrompt),
});

for (const part of response.candidates[0].content.parts) {
  if (part.text) console.log(part.text);
  else if (part.inlineData) {
    fs.writeFileSync("output.png", Buffer.from(part.inlineData.data, "base64"));
  }
}
```

### Image Editing (Python)

```python
from PIL import Image

# Load reference image
ref_image = Image.open("reference.jpg")

edit_prompt = {
    "label": "background-swap",
    "Subject": ["keep original subject exactly as-is"],
    "Background": "sunset beach, golden hour, calm ocean",
    "Lighting": "warm directional light matching golden hour"
}

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        types.Part.from_image(ref_image),
        json.dumps(edit_prompt)
    ],
)
```

---

## 5. Common Patterns & Tips

### Prevent Concept Bleeding
The #1 reason to use JSON. Put each visual concept in its own key. Never describe the subject's clothing in the Background field, or the lighting in the Subject field.

### ColorRestriction Is Your Best Friend
Always include this key. Without it, the model defaults to a broad, often garish palette. Even a simple `["warm neutral tones", "minimal accent colors"]` makes a big difference.

### Start Simple, Add Detail
Begin with Subject, Background, Lighting, and Mood. Add Camera, MadeOutOf, ColorRestriction only if the initial results need more control. Over-specifying can constrain the model too much.

### Iterating on Results
JSON's biggest practical advantage is iteration. If the colors are wrong, change only ColorRestriction. If the mood is off, adjust Lighting and Mood. If the composition is weird, change Arrangement. You never have to rewrite the whole prompt.

### Text in Images
- Put exact text in quotes: `"the sign reads 'GRAND OPENING'"`
- Keep text short — single words or short phrases render best
- Use the `Text` block for explicit placement control
- Nano Banana Pro has the best text rendering; use it for text-heavy images

### Consistency Across Multiple Images
- Use the same `consistency_id` across prompts
- Keep Subject and MadeOutOf identical
- Only change Arrangement, Background, Lighting between images
- The more specific the Subject description, the more consistent the results
