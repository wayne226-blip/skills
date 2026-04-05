---
name: easter-comp
description: "Transform a photo of people into Easter-themed AI art for competitions. Takes a source photo, analyses the people in it, then generates multiple Easter-styled versions across different art styles (Renaissance, Pixar, vintage card, fantasy, pop art, royal portrait). Uses Gemini edit_image to preserve likenesses and generate_image for creative reimaginings. Use when someone says 'Easter photo', 'Easter competition', 'Easter picture', 'make this Easter', 'Easter art from photo', or wants to transform a group photo into festive Easter artwork."
---

# Easter Photo Competition

Transform a photo of real people into competition-winning Easter AI art. Generates multiple style variations so you can pick the best one.

## Workflow

### Step 1: Get the Photo

Ask for the photo path if not provided. Accept any image format (PNG, JPEG, WebP, HEIC).

### Step 2: Analyse the Source Photo

Use `gemini_describe_image` to understand the photo before transforming it:

```
Question: "Describe every person in this photo in detail — their approximate age, hair colour and style, skin tone, facial expression, body position, what they're wearing, and their relative positions to each other. Also describe the background/setting. Be very specific — I need enough detail to recreate these people in a different artistic style."
```

Save this description — it's the foundation for all the generate_image prompts.

### Step 3: Choose Styles

Ask the user which styles they want, or default to all six. The styles are:

| Style | Description | Best Tool |
|---|---|---|
| **Renaissance Easter** | Old Masters oil painting. Golden light, flowing robes, Easter lilies, halos, classical composition | edit_image |
| **Pixar Easter** | 3D animated characters in a pastel Easter world. Big expressive eyes, Easter egg hunt scene, warm lighting | edit_image |
| **Vintage Easter Card** | 1950s greeting card illustration. Soft pastels, decorative border, spring flowers, retro charm | edit_image |
| **Easter Fantasy** | Photorealistic but magical. Giant decorated eggs, enchanted garden, golden hour light, butterflies, spring blossoms | edit_image |
| **Pop Art Easter** | Warhol/Lichtenstein style. Bold flat colours, Ben-Day dots, comic outlines, Easter eggs and bunnies as pop motifs | edit_image |
| **Easter Royalty** | Regal group portrait. Elaborate Easter-themed crowns, velvet robes in pastel colours, ornate throne room with egg motifs | edit_image |

### Step 4: Generate the Images

**For each style, use `gemini_edit_image` first** — this preserves the actual people from the photo:

#### Renaissance Easter
```
Instruction: "Transform this photo into a Renaissance oil painting in the style of Raphael. The people should be wearing flowing classical robes in gold and cream. Surround them with Easter lilies, spring flowers, and soft golden divine light. Add a pastoral Italian landscape background with rolling hills. Oil painting texture, rich warm palette, classical composition."
Model: gemini-2.5-flash-image
```

#### Pixar Easter
```
Instruction: "Transform these people into Pixar-style 3D animated characters. Give them big expressive eyes and slightly exaggerated features. Place them in a colourful pastel Easter egg hunt scene with giant decorated eggs, spring flowers, baby chicks, and a bright blue sky. Warm, cheerful Pixar lighting. 3D rendered look."
Model: gemini-2.5-flash-image
```

#### Vintage Easter Card
```
Instruction: "Transform this photo into a 1950s vintage Easter greeting card illustration. Soft pastel watercolour style. Add a decorative scalloped border with spring flowers. Include Easter eggs, baby rabbits, and spring daffodils around the people. Retro mid-century illustration style with gentle colours — mint green, baby pink, lavender, butter yellow."
Model: gemini-2.5-flash-image
```

#### Easter Fantasy
```
Instruction: "Transform this photo into a magical Easter fantasy scene. Keep the people photorealistic but place them in an enchanted spring garden with giant ornately decorated Easter eggs (some cracked open revealing golden light), luminous butterflies, cherry blossoms falling, a carpet of wildflowers, and warm golden hour lighting. Magical sparkles and soft lens flare. Dreamy, ethereal atmosphere."
Model: gemini-2.5-flash-image
```

#### Pop Art Easter
```
Instruction: "Transform this photo into bold Pop Art in the style of Andy Warhol and Roy Lichtenstein. Flat bold colours — hot pink, electric blue, bright yellow, lime green. Add Ben-Day dots pattern. Bold black comic-book outlines around the people. Fill the background with pop art Easter eggs, stylised bunnies, and graphic spring flowers. High contrast, punchy, eye-catching."
Model: gemini-2.5-flash-image
```

#### Easter Royalty
```
Instruction: "Transform these people into Easter royalty. Dress them in elaborate regal robes in pastel Easter colours — lavender, mint, gold, rose. Give them ornate crowns decorated with jewelled Easter eggs and spring flowers. Place them in an opulent throne room with marble columns, velvet drapes, and a mosaic floor with Easter egg patterns. Dramatic portrait lighting. Regal and majestic."
Model: gemini-2.5-flash-image
```

### Step 5: Try generate_image for the best style

Once the user picks their favourite style from the edits, also create a `gemini_generate_image` version using the detailed person descriptions from Step 2. This gives a more dramatic artistic interpretation — sometimes it wins, sometimes the edit wins. Generate both and let the user choose.

Build the prompt by combining:
- The detailed person descriptions from Step 2
- The style instructions from the chosen preset
- Aspect ratio: `3:2` for landscape group shots, `2:3` for portrait
- Model: `gemini-3-pro-image-preview` for maximum quality on the final version

### Step 6: Save and Display

Save all images to `~/Claude/gemini-output/easter-comp/` with clear filenames:
- `easter-renaissance.png`
- `easter-pixar.png`
- `easter-vintage-card.png`
- `easter-fantasy.png`
- `easter-pop-art.png`
- `easter-royalty.png`
- `easter-final-generate.png`

**Read every output image** with the Read tool so the user can see them inline.

Report: "Here are all 6 styles. Which one wins the competition?"

## Tips for Winning

- **edit_image preserves faces** — if likeness matters, this is the safer bet
- **generate_image goes bigger** — if you want maximum "wow factor" and don't mind approximate likenesses, generate from the description
- **Pro model for finals** — use `gemini-3-pro-image-preview` for the final competition entry, it handles complex scenes and text better
- If a style doesn't land, tweak the instruction and re-run just that one
- Easter = pastels, eggs, bunnies, chicks, lilies, spring flowers, golden light. Layer these in for maximum Easter energy

## Quick Run

If the user just says "do it" or "run them all":
1. Analyse the photo
2. Run all 6 edit_image styles
3. Display all results
4. Ask which to polish with generate_image + pro model
