# JSON Prompting Guide — Product Photography

Condensed reference for writing product photography prompts using JSON-structured prompting principles. Based on the Nano Banana Prompting guide, focused on what matters for product shots.

---

## Core JSON Structure

Each visual concept gets its own key to prevent "concept bleeding" — adjectives from one concept leaking into another:

```json
{
  "Style": ["studio-product-photography", "clean-minimal"],
  "Subject": ["product description, shape, colour, materials"],
  "MadeOutOf": ["specific materials visible in the shot"],
  "Arrangement": "how the product is positioned in frame",
  "Background": "what's behind/around the product",
  "ColorRestriction": ["brand palette constraints with hex codes"],
  "Lighting": "light type, direction, quality",
  "Camera": {
    "type": "camera type",
    "lens": "focal length",
    "aperture": "f-stop",
    "flash": "flash setting"
  },
  "OutputStyle": "overall rendering quality",
  "Mood": "emotional tone"
}
```

---

## ColorRestriction — The Most Important Key

Always include this for product photography. Without it, the model defaults to broad, often garish palettes. Use hex codes from the Brand DNA.

Good: `["warm neutrals only", "brand teal #008080 as accent", "no bright reds or oranges"]`
Bad: `["nice colours"]`

---

## Camera Settings Reference for Product Photography

| Shot Type | Lens | Aperture | Why |
|-----------|------|----------|-----|
| Hero / Clean | 85-100mm macro | f/5.6-f/8 | Edge-to-edge sharpness, slight compression |
| Detail / Macro | 100mm macro | f/2.8 | Razor-thin focal plane, creamy bokeh |
| Lifestyle / Environment | 35-50mm | f/2.0-f/2.8 | Product sharp, background soft |
| Flat Lay / Overhead | 35mm | f/5.6 | Even focus across the surface |
| Full Product Range | 100mm | f/8 | All products equally sharp |
| Action / Motion | 85mm | f/2.0 | Fast shutter, shallow depth |
| E-Commerce / White BG | 100mm macro | f/11 | Maximum depth of field |
| UGC / Phone-style | 28mm equivalent | f/1.8 | Phone-camera look, wide and close |

---

## When to Use Pro vs NB2

| Use Case | Model | Why |
|----------|-------|-----|
| Text rendering (infographics, labels) | Pro | Best text accuracy |
| Macro / detail / texture | Pro | Higher precision for fine detail |
| Complex compositions (grids, multi-product) | Pro | Better spatial reasoning |
| Lifestyle / environment | NB2 | Faster, cheaper, quality is excellent |
| Hero shots | NB2 | Speed for iteration, upgrade to Pro for final |
| Social / UGC aesthetic | NB2 | The slight imperfection fits the aesthetic |
| Seasonal / mood | NB2 | Atmosphere doesn't need pixel precision |

**Default to NB2** (omit the `model` key in the JSON array). Only specify `"model": "pro"` when the shot genuinely needs it — detail shots, text-heavy layouts, or multi-angle grids.

---

## Aspect Ratios for Product Photography

| Ratio | Use |
|-------|-----|
| 1:1 | Instagram feed, product listings, hero shots |
| 4:5 | Instagram feed (max height), portrait product shots, in-use |
| 16:9 | Website banners, landscape environments, product lineups |
| 9:16 | Stories, Reels, vertical social |
| 4:3 | General purpose, slightly wider than 1:1 |

---

## Output Format for Nano Banana Studio

The bulk import expects a JSON array where each `prompt` is **natural language text**, not nested JSON:

```json
[
  {"prompt": "Image Generation Prompt Modifier. Full natural language prompt here...", "ratio": "1:1"},
  {"prompt": "Image Generation Prompt Modifier. Full natural language prompt here...", "ratio": "4:5", "model": "pro"}
]
```

**Rules:**
- `prompt` is clean text — the JSON prompting structure informs HOW you write it, but the output is plain English
- Prepend the Image Generation Prompt Modifier from the Brand DNA to every prompt
- `ratio` matches the template's recommended aspect ratio
- Omit `model` for NB2 (default). Only add `"model": "pro"` when needed
- Zero leftover `[PLACEHOLDERS]` — every bracket must be filled with real brand-specific content

---

## Tips

1. **Prevent concept bleeding:** Don't describe lighting in the Subject. Don't mention the product in the Background. Keep concepts separated.
2. **ColorRestriction is your best friend:** Always include it. Even `["warm neutral tones", "minimal accent colours"]` makes a big difference.
3. **Start simple, add detail:** Begin with Subject, Background, Lighting, Mood. Add Camera, MadeOutOf, ColorRestriction only if initial results need more control.
4. **Iterating:** JSON's biggest advantage. If colours are wrong, change only ColorRestriction. If mood is off, adjust Lighting and Mood. Never rewrite the whole prompt.
5. **Hex codes everywhere:** Use `#2BBFFF` not "electric blue". The model responds to specificity.
