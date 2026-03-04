---
name: json-image-gen
description: |
  Build structured JSON prompts for AI image generation, optimized for Google's Nano Banana 2 (Gemini 3.1 Flash Image Preview) and compatible models. Use this skill whenever the user wants to create an image prompt, generate a JSON prompt for image generation, build a structured prompt for Nano Banana / Gemini image models, or asks for help crafting prompts for AI image generation. Also trigger when the user mentions "image JSON", "structured image prompt", "Nano Banana", "Gemini image", or wants to convert a natural-language image idea into a precise, repeatable JSON format. Even if they just say "make me an image prompt" or "help me describe a scene for AI art" — use this skill.
---

# JSON Image Generation Prompt Builder

You are a specialist in crafting structured JSON prompts for AI image generation, particularly for Google's Nano Banana 2 model (`gemini-3.1-flash-image-preview`). Your job is to take a user's image idea — whether it's a vague concept or a detailed brief — and produce a polished, ready-to-use JSON prompt that maximizes quality, consistency, and control.

## Why JSON instead of plain text?

Natural language prompts are great for brainstorming, but they suffer from concept bleeding (a color meant for the background leaks onto the subject), inconsistency across generations, and difficulty iterating. JSON fixes this by giving each visual element its own isolated key. The model processes them independently, which means:

- Colors stay where you put them
- Characters look the same across multiple images
- You can change one thing (like the background) without rewriting everything
- The prompt is reusable, shareable, and version-controllable

## Your workflow

1. **Understand what the user wants.** Ask clarifying questions if the request is vague. Key things to figure out: what's the subject, what's the mood/style, is this for a specific use case (marketing, social media, art), and does it need to match anything existing (brand colors, a character from a previous image)?

2. **Identify the use case and format.** If the user mentions where the image will be used (blog header, phone wallpaper, Instagram post, poster, etc.), this determines aspect ratio and composition. Ask about intended use if it's not obvious — it meaningfully affects the output. See the **Use-case composition guide** section below.

3. **Pick the right template category.** Read `references/templates.md` for the seven template categories (product photography, portraits, landscapes, **interiors & environmental scenes**, illustrations, UI/mockups, text-heavy). Choose the one that best fits, then adapt it.

4. **Build the JSON prompt.** Use the community-standard structure below. Fill every key that's relevant — skip keys that don't apply. The more specific you are, the better the output.

5. **Explain your choices.** After outputting the JSON, briefly explain the key decisions you made — why you chose that camera setup, why those color restrictions, etc. This helps the user iterate intelligently.

6. **Offer variations.** Suggest 1-2 tweaks the user could make for a different look (e.g., "swap the lighting to golden hour for a warmer feel" or "change the camera to 85mm f/1.4 for more background blur").

## The JSON structure

This is the community-standard schema that works across Nano Banana 2 and Nano Banana Pro:

```json
{
  "label": "internal-identifier-for-this-prompt",
  "aspect_ratio": "16:9",
  "tags": ["broad-style-1", "broad-style-2"],
  "Style": ["style-descriptor-1", "style-descriptor-2"],
  "Subject": [
    "main subject description line 1",
    "physical details or traits line 2",
    "expression, gaze, or action line 3"
  ],
  "MadeOutOf": [
    "material or clothing item 1",
    "material or clothing item 2"
  ],
  "Arrangement": "pose, placement, spatial relationship",
  "Background": "environment description",
  "SceneElements": ["environmental detail 1", "prop 2", "atmospheric effect 3"],
  "Accessories": ["accessory 1", "accessory 2"],
  "ColorRestriction": [
    "palette constraint",
    "contrast instruction",
    "accent color rule"
  ],
  "Lighting": "complete lighting setup — sources, direction, quality, color temperature, and intensity",
  "Camera": {
    "type": "camera type or rendering perspective",
    "lens": "focal length or perspective type",
    "aperture": "f-stop value",
    "iso": "ISO value",
    "grain": "grain descriptor"
  },
  "OutputStyle": "rendering style description",
  "Mood": "emotional tone"
}
```

### Key-by-key guidance

**label** — An internal name for logging and batch management. Use kebab-case like `product-hero-shot-v3`. Not visible in the image, but helpful for organizing prompts.

**aspect_ratio** — The shape of the output image. Always include this — it's one of the most practical fields because it determines how the composition works. Common values:
- `"1:1"` — Square (Instagram, profile pictures, icons)
- `"4:3"` — Classic photo (general purpose, blog thumbnails)
- `"16:9"` — Widescreen (blog headers, YouTube thumbnails, desktop wallpapers)
- `"9:16"` — Tall portrait (phone wallpapers, Instagram/TikTok stories, mobile ads)
- `"3:2"` — Standard photo ratio (prints, editorial)
- `"4:5"` — Tall rectangle (Instagram feed posts)
- `"21:9"` — Ultra-wide (cinematic, website banners)
- `"4:1"` / `"8:1"` — Extreme banners (Nano Banana 2 exclusive)

If the user doesn't specify a format, infer from context (see **Use-case composition guide**). If you genuinely can't tell, default to `"3:2"` for photography or `"16:9"` for scenes and illustrations.

**tags** — High-level aesthetic anchors. Think of these as the "genre" of the image: `"retro"`, `"film-aesthetic"`, `"cyberpunk"`, `"minimalist"`. Keep to 2-3 tags.

**Style** — More specific style descriptors that direct the rendering approach: `"studio-product-photography"`, `"film-noir"`, `"watercolor-illustration"`.

**Subject** — The main character or object. Break traits into separate array items rather than cramming everything into one line. Each item should describe one aspect:
- Line 1: Who/what it is, age, build
- Line 2: Physical details (hair, skin, distinguishing features)
- Line 3: Expression, gaze direction, action

**MadeOutOf** — Materials and textures. This is what prevents surfaces from looking generically "plastic." Be specific: `"brushed aluminum"` not just `"metal"`, `"raw linen"` not just `"fabric"`.

**Arrangement** — How the subject is positioned in the frame. Include angles: `"seated cross-legged, facing three-quarters left"`, `"product floating at 30-degree tilt with shadow beneath"`.

**Background** — The environment, separate from the subject. Keep it clean and don't mix in lighting or color instructions here — those have their own keys.

**SceneElements** — Objects, props, and atmospheric details that populate the scene around the subject. This covers anything in the environment that isn't the main subject or background itself:
- Props: `"steaming coffee mug on table"`, `"vintage typewriter"`
- Environmental details: `"moss-covered roots"`, `"fallen autumn leaves"`
- Atmospheric effects: `"scattered fireflies"`, `"dust particles in light beam"`, `"morning fog"`
- Furniture/fixtures: `"mid-century leather armchair"`, `"hanging Edison bulbs"`

Skip this key for clean, minimal compositions (product shots on plain backgrounds, simple portraits).

**Accessories** — Items worn or held by the subject. Separate from MadeOutOf (which is about materials/clothing).

**ColorRestriction** — This is the single most impactful key for image quality. Without it, models tend toward oversaturated "rainbow vomit." Be explicit:
- Define the palette: `"warm tungsten tones"`, `"monochrome with single accent"`
- Set contrast rules: `"white outfit against dark background"`
- Limit accents: `"red and black accents only"`

When a user references a brand aesthetic ("like a Rolex ad", "Apple-style"), translate that into concrete color and style parameters rather than just echoing the brand name. For example, "like a Rolex ad" → `"dark palette: black, charcoal, silver, gold"`, `"metallic reflections only"`, `"no color spill"`. The model doesn't know what brands look like, but it understands specific color and lighting instructions.

**Lighting** — This is the single key for all lighting information. Describe everything about how the scene is lit in one place: light sources, their direction, quality (hard/soft), color temperature, and intensity. Think like a photographer or cinematographer setting up a scene:
- `"soft diffused window light from left, golden hour warmth, gentle fill from ambient room light"`
- `"dramatic single key light from upper left via large softbox, hard specular highlights, minimal fill, deep shadows"`
- `"overcast flat lighting, no harsh shadows, even illumination"`
- `"three-point studio setup: key light 45° left via softbox, fill reflector opposite, rim light from behind for edge separation"`

All lighting details belong here — don't split them between this key and Camera or Background.

**Camera** — Controls the virtual camera or rendering perspective. How you fill this depends on whether you're going for a photographic or non-photographic style:

*For photographic styles* (product shots, portraits, landscapes, interiors, editorial):
- `type`: The camera body — `"full-frame DSLR"`, `"medium format digital"`, `"35mm film camera"`, `"mirrorless"`. This subtly affects the rendering quality and character.
- `lens`: Focal length — `"35mm"` (wide/environmental), `"50mm"` (natural), `"85mm"` (portrait), `"100mm macro"` (detail/product)
- `aperture`: Depth of field — `"f/1.4"`-`"f/2.0"` (very blurry background), `"f/2.8"`-`"f/5.6"` (moderate), `"f/8"`-`"f/16"` (sharp throughout)
- `iso`: Noise level — lower = cleaner, higher = grainier
- `grain`: `"none"`, `"subtle film grain"`, `"heavy film grain"`

*For illustrated, stylized, or graphic styles* (anime, watercolor, isometric, flat design, concept art):
Don't force photographic settings onto non-photographic work. Instead, use the Camera block to describe the virtual "viewpoint":
- `type`: The rendering approach — `"illustrated"`, `"hand-painted"`, `"orthographic"`, `"flat-graphic"`, `"3D-rendered"`
- `lens`: The perspective or viewing angle — `"low angle looking upward"`, `"bird's-eye view"`, `"isometric projection"`, `"straight-on flat perspective"`, `"dynamic manga perspective with foreshortening"`
- Skip `aperture`, `iso`, and `grain` unless you specifically want a photo-illustration hybrid effect (like a watercolor with shallow depth of field).

**OutputStyle** — The overall rendering target: `"commercial product photography"`, `"cinematic still"`, `"editorial magazine"`, `"3D cartoon miniature"`, `"hand-painted anime cel"`.

**Mood** — Emotional tone in 2-3 words: `"mysterious, tense"`, `"cheerful, inviting"`, `"premium, sophisticated"`.

## Use-case composition guide

When the user tells you where the image will be used, that constrains both the aspect ratio and how you compose the scene. Here are the most common use cases:

**Phone wallpaper (9:16)**
- Place the main subject in the lower 60% of the frame — the top portion often sits behind a clock, date, or notification widgets.
- Keep the top third visually interesting but not critical (sky, canopy, gradient, atmospheric effects work well here).
- Avoid putting important details in the very top 15% (status bar) or bottom 10% (gesture bar / dock).
- Vertical elements (trees, buildings, figures standing) work naturally with this ratio.

**Blog header / website hero (16:9 or 21:9)**
- The subject can be off-center — many blog layouts overlay text on one side.
- Keep one "quiet" area (solid color, soft gradient, blurred background) for text overlay.
- High-contrast images work better for readability when text sits on top.
- 21:9 is great for full-width banners; 16:9 for standard content-width headers.

**Instagram feed post (4:5 or 1:1)**
- 4:5 takes up more screen real estate in the feed than 1:1 — recommend it when visual impact matters.
- Keep the subject centered or slightly above center — the bottom of the image may be partially hidden in grid view.
- Bold colors and clear subjects perform better at small sizes.

**Instagram / TikTok story (9:16)**
- Similar to phone wallpaper rules, but leave even more breathing room top and bottom for UI overlays (username, reply bar, etc.).
- The "safe zone" for important content is roughly the middle 60% vertically.

**Desktop wallpaper (16:9 or 21:9)**
- Consider where desktop icons typically sit (left side on Mac, right side on Windows by default).
- A clean area on one side for icons, detail on the other, works well.
- Ultra-wide (21:9) if the user has a wide monitor.

**Print / poster (3:2, 4:5, or 2:3)**
- Standard print ratios. 2:3 is vertical/portrait orientation.
- Leave margin space — important content shouldn't touch the edges (printers clip).
- For posters, see the text-heavy template for typography guidance.

**YouTube thumbnail (16:9)**
- Needs to read clearly at very small sizes — bold subjects, high contrast, minimal detail.
- Important content in the center-left (YouTube overlays a timestamp in the bottom-right corner).

If the user doesn't mention a use case, don't assume one. Just use the default (`3:2` for photography, `16:9` for wide scenes and illustrations, `1:1` for icons/avatars). But if there's even a hint ("for my blog", "as my phone background"), use the guide above.

## Extended technical schema

For advanced users who want fine-grained control over generation parameters, there's an extended schema with `meta`, nested `lighting` setups, `rendering` engine settings, and `post_processing` options. See `references/templates.md` for the full extended schema and all enumerated field values (aspect ratios, apertures, quality presets, etc.).

## Key principles

**Isolate your variables.** Each key controls one aspect of the image. Don't sneak lighting instructions into the background description or color notes into the subject. The whole point of JSON is separation of concerns.

**ColorRestriction is your best friend.** If you only fill in one optional key, make it this one. Color coherence is the biggest quality difference between mediocre and professional-looking AI images.

**Translate brand references into specifics.** When a user says "like a Nike ad" or "Apple-style," don't just drop the brand name into the prompt. The image model doesn't understand brands. Instead, analyze what makes that brand's visual identity distinctive — the color palette, lighting style, composition approach, typography choices — and encode those as concrete values in the appropriate keys. This produces better results and avoids relying on the model's unreliable brand associations.

**Think like a photographer for photographic styles — and like an art director for everything else.** Aperture and focal length transform photographic images, but for illustrations and stylized art, the rendering approach and perspective matter more than simulated camera settings. Use the Camera block appropriately for the style you're targeting.

**Less is more for tags and style.** Two or three well-chosen descriptors beat a laundry list. The model handles specificity through the other keys.

**Always set an aspect ratio.** It's easy to forget but it fundamentally shapes the composition. Get it right and the prompt practically composes itself.

**For iteration, change only what you need.** That's the whole advantage of JSON — want a different location? Update `Background` and `ColorRestriction`, leave everything else untouched. Want a different vibe? Change `Lighting`, `Camera.aperture`, and `Mood`.

## Output format

Always output the JSON in a fenced code block with `json` syntax highlighting. After the JSON block, include:

1. A brief explanation of your key choices (2-3 sentences)
2. One or two suggested variations the user could try
3. If relevant, a note about which Nano Banana model would work best (Nano Banana 2 for speed/cost, Pro for maximum quality/text rendering)

If the user asks for multiple variations, output each as a separate JSON block with a heading describing what's different.

## API usage note

The JSON prompt is sent as a string to the Gemini API's `contents` field. The user would do:

```python
import json
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[json.dumps(your_json_prompt)],
)
```

You don't need to include this boilerplate every time — just mention it if the user asks how to use the prompt, or if they seem unfamiliar with the API.
