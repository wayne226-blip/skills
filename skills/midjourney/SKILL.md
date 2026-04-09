---
name: midjourney
description: Generate optimised Midjourney prompts for any image — character portraits, book covers, marketing assets, product shots, scenes, couples. Use this skill whenever the user asks for a "midjourney prompt", "mj prompt", "midjourney pic", wants an image described for use in Midjourney, or needs a detailed image prompt for any purpose. Also triggers when working on book covers, character art, romance novel images, or marketing visuals where Midjourney is the likely generation tool. When in a fiction workspace, pull character details from the character bible before writing the prompt — never invent physical details that are already documented.
---

## What You're Doing

Midjourney prompts have a specific structure that produces reliably good results. Translate the request — whether "a midjourney pic of our couple" or "a dark moody cover for my thriller" — into a prompt that will actually work well.

**Read source files first.** If there's a character bible, cover brief, or world bible relevant to the request, read it before writing. Don't invent physical details that are already documented.

---

## Prompt Structure

Build prompts in this order — MJ weights earlier tokens more heavily, so subject comes first and technical parameters come last:

1. **Subject** — who/what, specific physical details (height, build, hair, eyes, distinguishing marks)
2. **Action/Pose** — what they're doing, spatial relationship between figures
3. **Setting** — location, environmental context
4. **Lighting & mood** — atmosphere, colour palette, emotional tone
5. **Style/medium** — photorealistic, cel-shaded, oil painting, anime, etc.
6. **Technical specs** — camera, lens, settings (photorealistic only)
7. **Parameters** — `--ar`, `--style`, `--v`, `--no`

---

## Style Modes

### Photorealistic
- Include camera + lens: `Shot on Sony A7R V, 85mm f/1.4, shallow depth of field`
- Use `--style raw` — suppresses MJ's default illustrative treatment
- Use `--v 7`
- Lighting descriptor helps: `cinematic lighting`, `golden hour`, `studio lighting with rim light`

### Illustrated / cel-shaded / anime
- Name the style explicitly: `flat cel-shaded illustration, anime-influenced, romcom energy`
- No camera specs needed
- Use `--v 7`
- Can add: `clean linework`, `pastel palette`, `dynamic pose`

### Dark / cinematic
- `cinematic lighting, dramatic shadows, moody atmosphere`
- `--style raw` or `--style cinematic` depending on desired output
- Film grain adds grit: `subtle film grain`

### Painterly / concept art
- `digital painting, high detail, concept art style, artstation quality`

---

## Parameters Reference

| Parameter | Use |
|---|---|
| `--ar 2:3` | Portrait / book cover |
| `--ar 3:2` | Landscape / wide scene |
| `--ar 1:1` | Social / square crop |
| `--style raw` | Photorealism — suppresses MJ's illustrative defaults |
| `--v 7` | Default — best current model |
| `--no text, words, letters` | When text keeps rendering in the image |
| `--no watermark, logo` | Clean image output |
| `--q 2` | Higher quality render (slower) |

---

## MJ-Specific Craft Notes

**Physical details over personality:** MJ renders anatomy, not psychology. "Sharp jaw, dark brown hair slightly too long" works. "Brooding and intense" doesn't render. Translate personality into posture and expression: "jaw set, looking down at her without smiling."

**Multiple figures:** Anchor spatial relationships explicitly — "standing face to face", "her hand on his chest", "he looks down at her." Without spatial anchors MJ drifts. Height difference matters: "she comes to his shoulder."

**Distinguishing marks:** Name them by location in the subject section, not as an afterthought. "Small beauty mark mole below her left ear" renders reliably when called out clearly.

**Ethnicity / skin tone:** Be explicit when it matters for accuracy. "Chinese-American woman, warm medium skin tone, black hair" is more reliable than leaving it to MJ's inference.

**Text in images:** MJ generates text badly. Add `--no text, words, letters` whenever text in the image is unwanted. For book covers, generate image clean and add title/author in Canva.

**Clothing details:** Specific beats generic. "Blue college hockey jersey, number 19, lace-up collar, white sleeve stripes" beats "blue jersey."

---

## Output Format

Always output:
1. The full prompt — ready to paste directly into Midjourney, no editing needed
2. 2-3 brief notes on key choices (why that style flag, how any tricky element was handled)

If the request is for a book cover image, add: "Generate clean with no text — add title/author in Canva over the top."

---

## Example: Romance Novel Couple (Photorealistic)

**Request:** Photo-realistic couple shot, college hockey romance, no text overlay, mole below her left ear

```
Photorealistic close-up of a young couple in a hockey arena, cinematic lighting. Man: 6'1", lean athletic build, dark brown hair slightly too long falling across his forehead, sharp jaw, grey-green eyes, wearing blue college hockey jersey number 19 with "CALLOWAY" across the chest, wrist taped in black. Woman: 5'5", Chinese-American, warm medium skin tone, black hair in high ponytail, warm brown eyes, small beauty mark mole below her left ear, wearing dark navy athletic staff polo with a lanyard ID badge, her hand resting on his chest touching his jersey number, looking up at him. He looks down at her, jaw set, intense and restrained. Ice rink visible behind them, arena lights casting warm glow, shallow background. Intimate tension-filled romance novel composition. Shot on Sony A7R V, 85mm f/1.4, shallow depth of field --ar 2:3 --style raw --v 7 --no text, words, letters
```

**Notes:**
- `--style raw` prevents MJ rendering it as illustrated despite the anime-adjacent subject
- 85mm f/1.4 gives editorial portrait framing with bokeh background matching the cover composition
- Mole called out in subject section so it's not missed

---

## Example: Book Cover (Illustrated Style)

**Request:** Illustrated cover for a college hockey romance, pastel, romcom energy

```
Flat cel-shaded illustration of a young couple at an ice rink, pastel blue and white palette, romcom energy. Tall dark-haired man in blue hockey jersey number 19 looking down with a reluctant almost-smile. Shorter woman in navy athletic polo looking up at him, one hand on his chest, ponytail. Warm arena lighting from behind. Dynamic poses, clean linework, soft shading, illustration style similar to contemporary YA romance covers --ar 2:3 --v 7 --no text, watermark
```

**Notes:**
- No camera specs for illustrated — they'd push toward photorealism
- `romcom energy` is a style direction MJ understands surprisingly well
- Generate clean, add title text in Canva
