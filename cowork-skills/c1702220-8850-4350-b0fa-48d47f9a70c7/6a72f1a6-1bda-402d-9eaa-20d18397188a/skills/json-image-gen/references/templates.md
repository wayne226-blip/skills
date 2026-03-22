# Template Categories & Reference Data

## Template 1: Product Photography

Best for: E-commerce hero shots, marketing materials, product catalogs.

```json
{
  "label": "product-hero-shot",
  "aspect_ratio": "4:5",
  "tags": ["product-photography", "minimalist"],
  "Style": ["studio-product-photography", "clean-minimal"],
  "Subject": [
    "modern wireless headphones, matte black finish",
    "premium build quality, soft ear cushions visible"
  ],
  "MadeOutOf": ["brushed aluminum", "memory foam", "soft-touch plastic"],
  "Arrangement": "headphones resting at 30-degree angle on reflective surface",
  "Background": "clean white gradient, subtle shadow",
  "ColorRestriction": ["monochrome palette", "black product on white", "no color accents"],
  "Lighting": "soft diffused studio lighting from above and slightly left, subtle rim light from behind for edge separation, no harsh shadows",
  "Camera": {
    "type": "medium format digital",
    "lens": "85mm macro",
    "aperture": "f/5.6",
    "iso": 100,
    "grain": "none"
  },
  "OutputStyle": "commercial product photography, magazine quality",
  "Mood": "premium, sophisticated"
}
```

Key characteristics: Clean backgrounds, studio lighting consolidated in the Lighting key, sharp focus throughout (f/5.6-f/8), macro or medium telephoto lens, monochrome or brand-matched palettes. Always include aspect_ratio — 1:1 or 4:5 for e-commerce, 16:9 for hero banners.

---

## Template 2: Portraits

Best for: Character art, headshots, editorial portraits, social media avatars.

```json
{
  "label": "editorial-portrait",
  "aspect_ratio": "3:2",
  "tags": ["portrait", "editorial"],
  "Style": ["editorial-portrait", "fashion-magazine"],
  "Subject": [
    "young woman, early 20s, fair skin",
    "long dark hair, loose braids",
    "eyes looking directly into camera, subtle confident expression"
  ],
  "MadeOutOf": [
    "white cotton camisole",
    "gold pendant necklace"
  ],
  "Arrangement": "shoulders slightly turned, face toward camera",
  "Background": "soft blurred warm-toned interior",
  "Accessories": ["thin gold bracelet"],
  "ColorRestriction": [
    "warm tungsten tones",
    "white outfit for contrast",
    "gold accents only"
  ],
  "Lighting": "strong direct on-camera flash creating hard shadows, warm tungsten ambient fill, overall high-contrast look",
  "Camera": {
    "type": "digital rangefinder",
    "lens": "85mm",
    "aperture": "f/1.8",
    "iso": 400,
    "grain": "subtle film grain"
  },
  "OutputStyle": "editorial fashion photography",
  "Mood": "confident, intimate"
}
```

Key characteristics: Shallow depth of field (f/1.4-f/2.0), 85mm portrait lens, all lighting described in the Lighting key (including flash), subject-focused composition, warm or dramatic color palettes.

---

## Template 3: Landscapes & Scenes

Best for: Environment art, travel imagery, establishing shots, wallpapers.

```json
{
  "label": "mountain-golden-hour",
  "aspect_ratio": "16:9",
  "tags": ["landscape", "nature", "golden-hour"],
  "Style": ["landscape-photography", "national-geographic"],
  "Subject": [
    "dramatic mountain range with snow-capped peaks",
    "alpine meadow with wildflowers in foreground"
  ],
  "Arrangement": "wide panoramic view, leading lines from meadow to peaks",
  "Background": "golden hour sky with wispy clouds, warm to cool gradient",
  "SceneElements": ["small hiking trail winding through meadow", "distant eagle silhouette"],
  "ColorRestriction": [
    "golden hour warm palette",
    "cool blue shadows on mountains",
    "green and gold foreground"
  ],
  "Lighting": "low-angle golden hour sunlight from left, long dramatic shadows, warm direct light on peaks with cool shadow fill in valleys",
  "Camera": {
    "type": "full-frame DSLR",
    "lens": "24mm wide-angle",
    "aperture": "f/11",
    "iso": 100,
    "grain": "none"
  },
  "OutputStyle": "professional landscape photography, ultra sharp",
  "Mood": "awe-inspiring, serene"
}
```

Key characteristics: Wide-angle lenses (16-35mm), deep depth of field (f/8-f/16), natural lighting, strong color palettes tied to time of day, foreground-to-background compositional flow. 16:9 or 21:9 for desktop/banner, 9:16 for phone wallpapers.

---

## Template 4: Interiors & Environmental Scenes

Best for: Coffee shops, restaurants, living rooms, offices, cozy spaces, architectural interiors, real estate imagery, lifestyle blog photography.

This template fills the gap between landscapes (outdoor) and product photography (single object). Use it whenever the subject is a space or environment that people inhabit — the "feel" of the room is the subject, not just the objects in it.

```json
{
  "label": "cozy-coffee-shop",
  "aspect_ratio": "3:2",
  "tags": ["interior", "lifestyle", "warm-tones"],
  "Style": ["interior-photography", "lifestyle-editorial"],
  "Subject": [
    "interior of a small independent coffee shop",
    "exposed brick walls, reclaimed wood counter, hand-written chalkboard menu",
    "a few patrons in soft focus at background tables"
  ],
  "MadeOutOf": [
    "reclaimed wood surfaces",
    "exposed red brick",
    "warm leather seating",
    "matte ceramic dishware"
  ],
  "Arrangement": "shot from a seated perspective at a corner table, depth through the room toward the front windows",
  "Background": "large front windows letting in soft daylight, street visible but blurred beyond",
  "SceneElements": [
    "steaming latte with art on nearby table",
    "potted monstera on windowsill",
    "hanging Edison bulbs overhead",
    "espresso machine gleaming on counter"
  ],
  "ColorRestriction": [
    "warm earthy palette: browns, creams, amber, terracotta",
    "no cool tones except window daylight",
    "soft golden highlights from overhead bulbs"
  ],
  "Lighting": "soft natural window light from the front-left as primary source, warm Edison bulb ambient fill from above, gentle shadows under tables and seating",
  "Camera": {
    "type": "mirrorless full-frame",
    "lens": "35mm",
    "aperture": "f/2.8",
    "iso": 400,
    "grain": "subtle film grain"
  },
  "OutputStyle": "lifestyle blog photography, warm and inviting, editorial quality",
  "Mood": "cozy, intimate, welcoming"
}
```

Key characteristics:
- **Lens choice matters a lot here.** 24-35mm for environmental shots that show the whole space. 50mm for a more natural "I'm sitting here" perspective. Avoid longer lenses — they compress the room and lose the sense of space.
- **Depth of field is moderate** (f/2.0-f/4.0). You want some background softness to create atmosphere but enough sharpness to show the environment. Too shallow and it looks like a portrait with a room behind it.
- **Lighting is almost always mixed.** Interiors combine natural light (windows) with artificial sources (lamps, overhead fixtures, candles). Describe both in the Lighting key.
- **SceneElements carry a lot of weight.** The props and details are what make a space feel real and lived-in — the stack of books, the steam rising from a cup, the plant on the shelf. Be generous with this key for interiors.
- **MadeOutOf describes the space's materiality.** Wood, brick, concrete, tile, fabric — these textures define the character of an interior.

---

## Template 5: Illustrations & Stylized Art

Best for: Concept art, book covers, game art, stylized social content, anime, watercolor.

```json
{
  "label": "isometric-city-block",
  "aspect_ratio": "1:1",
  "tags": ["isometric-3d", "miniature-tilt-shift"],
  "Style": ["isometric-3d", "miniature-tilt-shift"],
  "Subject": ["city block with shops, park, and apartments"],
  "Arrangement": "45-degree top-down isometric view, all buildings visible",
  "Background": "soft solid color, clean edge",
  "SceneElements": ["tiny cars on street", "park bench with figure", "streetlights"],
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

Key characteristics: Use the Camera block to describe the *rendering perspective*, not photographic settings. Common approaches:
- **Isometric:** `"type": "orthographic"`, `"lens": "isometric projection"`
- **Anime/hand-painted:** `"type": "illustrated"` or `"hand-painted"`, `"lens": "low angle looking upward"` or whatever the scene calls for
- **Flat/graphic design:** `"type": "flat-graphic"`, `"lens": "straight-on flat perspective"`
- **3D rendered:** `"type": "3D-rendered"`, `"lens": "wide establishing shot"` or similar

Skip `aperture`, `iso`, and `grain` for non-photographic styles unless you want a deliberate hybrid look. The `OutputStyle` key carries more weight here than in photographic templates — it's where you specify the rendering target (watercolor, cel-shaded, pixel art, vector, etc.).

---

## Template 6: UI & Mockups

Best for: App screenshots, device mockups, website previews, dashboard designs.

```json
{
  "label": "app-mockup-iphone",
  "aspect_ratio": "4:5",
  "tags": ["ui-design", "mockup", "minimal"],
  "Style": ["device-mockup", "tech-product-photography"],
  "Subject": [
    "modern smartphone showing a fitness tracking app interface",
    "clean UI with graphs, activity rings, and daily stats"
  ],
  "MadeOutOf": ["glass front", "titanium frame"],
  "Arrangement": "phone slightly angled, floating with soft shadow beneath",
  "Background": "clean gradient, light gray to white",
  "ColorRestriction": [
    "neutral background",
    "UI colors: blue primary, green for positive metrics",
    "minimal accent colors"
  ],
  "Lighting": "even soft studio lighting from above, no harsh reflections on screen, subtle gradient on device frame",
  "Camera": {
    "type": "medium format",
    "lens": "65mm",
    "aperture": "f/5.6",
    "iso": 100,
    "grain": "none"
  },
  "OutputStyle": "tech product photography, Apple-style presentation",
  "Mood": "clean, modern, aspirational"
}
```

Key characteristics: Clean minimal backgrounds, even lighting to avoid screen glare, medium depth of field, focus on readability of UI elements, tech-oriented color palettes.

---

## Template 7: Text-Heavy Designs

Best for: Posters, magazine covers, social media graphics, greeting cards, signage.

Nano Banana 2 has strong text rendering. For best results, put exact text in quotes within the Subject or a dedicated key.

```json
{
  "label": "event-poster",
  "aspect_ratio": "2:3",
  "tags": ["typography", "poster-design", "bold"],
  "Style": ["graphic-design", "modern-typography"],
  "Subject": [
    "event poster for a summer music festival",
    "the headline reads 'WAVELENGTH FEST 2026'",
    "subtext reads 'June 15-17 • Riverside Park • Live Music & Art'"
  ],
  "Arrangement": "headline centered upper third, subtext centered below, imagery fills background",
  "Background": "abstract gradient of sunset colors, flowing wave shapes",
  "ColorRestriction": [
    "sunset gradient: coral to deep purple",
    "white text for maximum readability",
    "no more than 3 colors total"
  ],
  "Lighting": "ambient glow from the gradient, no directional light needed",
  "Camera": {
    "type": "flat-graphic",
    "lens": "straight-on flat perspective"
  },
  "OutputStyle": "bold graphic design poster, print quality",
  "Mood": "energetic, festive, inviting"
}
```

Key characteristics: Exact text in quotes, flat/graphic Camera settings, strong color contrast for readability, composition focused on text hierarchy, simple backgrounds that don't compete with text.

---

## Extended Technical Schema

For users who need fine-grained control over generation parameters:

```json
{
  "meta": {
    "aspect_ratio": "16:9",
    "quality": "ultra_photorealistic",
    "seed": 42,
    "steps": 40,
    "guidance_scale": 7.5
  },
  "subject": [
    {
      "id": "hero",
      "type": "person",
      "description": "tall, muscular, scar on left eye",
      "input_image": {
        "path": "./reference.jpg",
        "usage_type": "face_id",
        "strength": 0.85
      }
    }
  ],
  "scene": {
    "background": "neon-lit cyberpunk street",
    "time_of_day": "night",
    "weather": "rain"
  },
  "camera": {
    "type": "DSLR",
    "model": "Canon EOS R5",
    "lens": {
      "focal_length": 35,
      "aperture": 2.0
    },
    "settings": {
      "shutter_speed": "1/250",
      "iso": 100,
      "exposure_compensation": 0.0
    }
  },
  "lighting": {
    "setup": "three-point lighting",
    "main_light": {
      "type": "softbox",
      "position": "45 degrees",
      "intensity": "high"
    },
    "fill_light": {
      "type": "reflector",
      "position": "opposite",
      "intensity": "medium"
    },
    "color_temperature": "5500K"
  },
  "rendering": {
    "engine": "raytracing",
    "samples": 64,
    "denoising": {
      "enabled": true,
      "strength": 0.5
    }
  },
  "post_processing": {
    "retouching": "minimal",
    "sharpening": "medium",
    "color_grading": "neutral"
  }
}
```

---

## Enumerated Fields Reference

Use these accepted values when filling in JSON prompts:

| Field | Accepted Values |
|-------|----------------|
| `aspect_ratio` | 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3, 21:9, 5:4, 4:5, 4:1, 1:4, 8:1, 1:8 |
| `aperture` | f/1.4, f/2.0, f/2.8, f/4.0, f/5.6, f/8.0, f/11, f/16 |
| `focal_length` | wide (16-24mm), normal (35-50mm), portrait (85mm), telephoto (100mm+) |
| `shutter_speed` | 1/500s, 1/250s, 1/125s, 1/60s, 1/30s, 1/15s |
| `lighting.type` | natural, studio, dramatic, soft, rim, backlit, ambient |
| `lighting.direction` | front, side, back, top, bottom, three-quarter |
| `lighting.color_temperature` | warm, neutral, cool, daylight (5500K), tungsten (3200K), fluorescent |
| `framing` | close_up, medium_shot, full_shot, long_shot, extreme_long_shot |
| `perspective` | eye_level, high_angle, low_angle, dutch_angle, bird_eye, worm_eye |
| `depth_of_field` | shallow (f/1.4-f/2.0), medium (f/2.8-f/5.6), deep (f/8-f/16) |
| `quality` | ultra_photorealistic, standard, raw, anime_v6, 3d_render_octane, oil_painting, sketch, pixel_art, vector_illustration |
| `resolution` | 512px, 1K (default), 2K, 4K |

### Nano Banana 2 Exclusive Features
- Aspect ratios 4:1, 1:4, 8:1, 1:8 (banners, infographics)
- Web search grounding for real-world accuracy
- Configurable thinking levels for complex scenes
- Resolution up to 4K

### Model Selection Guide
| Need | Recommended Model |
|------|------------------|
| Fast iteration, high volume | Nano Banana 2 (`gemini-3.1-flash-image-preview`) |
| Maximum text rendering quality | Nano Banana Pro (`gemini-3-pro-image-preview`) |
| Complex multi-element scenes | Nano Banana Pro with advanced thinking |
| Cost-sensitive production | Nano Banana 2 (30-50% cheaper than Pro) |
