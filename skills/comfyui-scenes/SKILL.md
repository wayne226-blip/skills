---
name: comfyui-scenes
description: Generate explicit multi-person scenes via ComfyUI — prompt engineering, anatomy fixes, pose templates for MF/FF/MM/MFF/MMF/FFF/group compositions
triggers:
  - multi person scene
  - multi-person
  - threesome
  - group scene
  - couple scene
  - boy girl
  - girl girl
  - boy boy
  - two women
  - two men
  - man and woman
  - mf scene
  - ff scene
  - mm scene
  - mff scene
  - mmf scene
  - fff scene
  - orgy
  - generate scene
  - comfyui scene
  - filth scene
  - sexy scene
---

# ComfyUI Multi-Person Scene Generator

Generate explicit multi-person images via The Engine. This skill handles the hard part — keeping multiple bodies distinct and anatomically correct.

**Prerequisites:** ComfyUI must be running. See `nsfw-generator` skill for setup.

---

## Quick Generate

```bash
cd ~/calibre-hq/comfyui-engine

# MF — SD1.5 (fast iteration)
python3 generate.py --preset maitland-ward --prompt "PROMPT" --output ./output/mf-scene.png

# MF — SDXL (higher quality)
python3 generate.py --preset maitland-ward-xl --prompt "PROMPT" --output ./output/mf-scene-xl.png

# FF — SD1.5
python3 generate.py --preset maitland-ward --prompt "PROMPT" --output ./output/ff-scene.png

# MM — use SDXL (less MM training data in epiCRealism)
python3 generate.py --preset maitland-ward-xl --prompt "PROMPT" --output ./output/mm-scene-xl.png

# MFF / MMF / FFF — always SDXL for 3+ people
python3 generate.py --preset maitland-ward-xl --prompt "PROMPT" --negative "MULTI_PERSON_NEGATIVES" --output ./output/group-xl.png

# Group (4+) — SDXL, landscape orientation
python3 generate.py --preset maitland-ward-xl --size 1216x832 --prompt "PROMPT" --negative "MULTI_PERSON_NEGATIVES" --output ./output/group-wide.png
```

**Batch mode:**
```bash
python3 generate.py --batch batch_jobs/couples-variety.json
python3 generate.py --batch batch_jobs/threesome-pack.json
```

---

## Genre Prompt Guide

**Always read before building scene prompts:**
`~/calibre-hq/authors/vivienne-cole/prompt-guide.md`

Contains tested templates for all 41 Vivienne Cole content categories including couples, multi-person, and genre-specific scenes.

---

## Why Multi-Person Fails (and How to Fix It)

SD models learn from millions of single-person images. Prompting for multiple people makes the latent space blend them — merged torsos, extra limbs, faces on wrong bodies. Four techniques fix this:

### 1. Spatial Anchoring

Tell the model WHERE each person is. Without this, it guesses and merges.

```
blonde woman on the left, dark-haired man on the right, facing each other
```

Keywords: `on the left`, `on the right`, `behind`, `in front`, `in the foreground`, `in the background`, `above`, `below`, `between`

### 2. Contrast Anchoring

Make characters visually distinct so the model has hooks to keep them separate. The more different they look, the less merging.

**Strong contrast markers:**
- Hair colour (blonde vs brunette vs redhead)
- Skin tone (fair vs olive vs dark)
- Build (petite vs curvy, muscular vs lean)
- Hair length (long vs short)

**Weak/useless:** eye colour, personality, emotion — the model can't reliably separate on these

### 3. Bracket Isolation

Describe each person as a complete unit BEFORE describing their interaction:

```
[blonde woman, 25, long wavy hair, blue eyes, petite, fair skin], [dark-haired man, 30, athletic build, tan skin], passionate embrace on silk sheets, warm bedroom lighting
```

This forces cross-attention to treat them as separate entities rather than one blended concept.

### 4. BREAK Keyword

Splits the prompt into separate 77-token chunks processed independently by CLIP. Prevents attribute bleeding between characters.

```
woman, red hair, blue dress BREAK man, black hair, suit BREAK bedroom, warm lighting
```

Each section before BREAK is encoded separately, so "red hair" won't tint the man's features. Combine with spatial anchoring for best results.

**Best results: use all four together.**

---

## Recommended Settings

| Scene Type | Preset | Size | CFG | Steps | Notes |
|---|---|---|---|---|---|
| MF (iterate) | vivienne-cole | 512x768 | 5.0 | 32 | Fast, good enough for exploring |
| MF (keeper) | vivienne-cole-xl | 832x1216 | 5.5 | 35 | Final quality |
| FF | vivienne-cole | 512x768 | 5.0 | 32 | Use strong visual contrast + BREAK |
| FF (keeper) | vivienne-cole-xl | 832x1216 | 5.5 | 35 | |
| MM | vivienne-cole-xl | 832x1216 | 5.5 | 35 | SDXL preferred — less MM data in SD1.5 |
| MFF | vivienne-cole-xl | 1024x1536 | 6.0 | 38 | SDXL only, use BREAK between each person |
| MMF | vivienne-cole-xl | 1024x1536 | 6.0-6.5 | 40 | Most prone to torso merging |
| FFF | vivienne-cole-xl | 1024x1536 | 6.5 | 40 | Highest confusion risk — max contrast + BREAK |
| Group (4+) | vivienne-cole-xl | 1216x832 | 6.0 | 40 | Landscape, accept lower accuracy |

**CFG notes:** EpiCRealism oversaturates above 7. Use 5.0 for SD1.5, 5.5-6.5 for SDXL multi-person. Use DPM++ SDE Karras sampler for best skin detail.

---

## Multi-Person Negative Prompt

The standard maitland-ward negative handles single-person anatomy. For multi-person, extend it:

**SD1.5 full negative:**
```
cartoon, anime, illustration, deformed, low quality, bad anatomy, extra fingers, blurry, watermark, merged bodies, fused limbs, extra arms, extra legs, extra heads, shared torso, conjoined, three arms, wrong number of limbs, floating limbs, disconnected body parts, multiple faces on one body, mismatched anatomy, body horror, extra people, too many people
```

**SDXL full negative (add these):**
```
cartoon, anime, illustration, deformed, low quality, bad anatomy, extra fingers, blurry, watermark, merged bodies, fused limbs, extra arms, extra legs, extra heads, shared torso, conjoined, three arms, wrong number of limbs, floating limbs, disconnected body parts, multiple faces on one body, mismatched anatomy, distorted proportions, incorrect anatomy, asymmetrical bodies
```

Pass via `--negative "..."` to override the preset default.

---

## Scene Type Templates

### MF (Man + Woman)

Easiest composition — most training data exists for this pairing.

**Prompt structure:**
```
[WOMAN_DESC], [MAN_DESC], POSE, SETTING, LIGHTING
```

Put the focal character first — epiCRealism skews female-forward so woman-first prompts tend to produce better results.

**Examples:**
```
[beautiful blonde woman, mid 20s, long wavy hair, blue eyes, slim athletic body, fair skin], [tall dark-haired man, early 30s, muscular build, tan skin], passionate embrace on white silk sheets, luxury bedroom, warm golden lamp light, intimate
```
```
[curvy brunette woman, late 20s, shoulder-length hair, brown eyes, olive skin], [lean man, stubble, hazel eyes, medium build], woman pressed against tiled wall, steamy shower, water streaming down bodies, soft diffused lighting
```
```
[petite redhead woman, green eyes, pale freckled skin, naked], [athletic dark-skinned man, close-cropped hair], woman on top, riding position, hotel room, city lights through floor-to-ceiling windows, cinematic lighting
```

### FF (Woman + Woman)

Tricky because identical anatomy type. Maximise visual contrast between the two.

**Prompt structure:**
```
[WOMAN_A_DESC — distinct features], [WOMAN_B_DESC — contrasting features], POSE, SETTING, LIGHTING
```

**Examples:**
```
[blonde woman, petite, fair skin, long straight hair], [brunette woman, curvy, olive skin, short curly hair], kissing passionately, tangled together on velvet couch, candlelight, romantic
```
```
[tall athletic woman, dark skin, close-cropped hair], [petite pale redhead, long wavy hair, freckles], in shower together, wet skin, steam, one pressing other against glass, soft warm lighting
```
```
[asian woman, long black hair, slim], [blonde woman, curvy, tanned], lying together in bed nude, one kissing other's neck, morning sunlight through white curtains, tender intimate
```

### MM (Man + Man)

Less MM training data in epiCRealism. Use SDXL for better results.

**Prompt structure:**
```
[MAN_A_DESC — distinct build], [MAN_B_DESC — contrasting build], POSE, SETTING, LIGHTING
```

Explicitly differentiate physiques — two "muscular men" will merge. Use height, build, and hair contrast.

**Examples:**
```
[muscular man, dark skin, shaved head, broad shoulders], [lean man, fair skin, brown wavy hair, slim build], standing embrace, one behind the other, dramatic side lighting, studio photography
```
```
[tall bearded man, 30s, rugged, brown skin], [younger man, clean-shaven, athletic, pale skin], in bed together, tender intimate moment, one lying on other's chest, morning light, white sheets
```

### MFF (Man + Two Women)

SDXL only. Spatial layout is critical — describe positions explicitly.

**Prompt structure:**
```
[WOMAN_A on left/behind], [MAN in center], [WOMAN_B on right/in front], POSE, SETTING
```

**Examples:**
```
[blonde woman on far left, petite, fair skin], [dark-haired man in center, athletic, tan], [brunette woman on right, curvy, olive skin], passionate threesome on large bed, man kissing blonde while brunette kisses his neck, warm lamp light, luxury bedroom
```
```
[redhead woman behind man, arms around his chest], [man standing, muscular], [dark-skinned woman kneeling in front], dramatic studio lighting, black background, artistic
```

### MMF (Two Men + Woman)

Most prone to torso merging. Use strongest anatomy negatives and highest CFG (6.5-7.0).

**Prompt structure:**
```
[WOMAN as focal anchor — describe first], [MAN_A position relative to her], [MAN_B position relative to her]
```

**Examples:**
```
[brunette woman in center, curvy, olive skin], [muscular man behind her, dark skin, shaved head], [lean man facing her, fair skin, brown hair], passionate threesome, satin sheets, warm golden lighting
```
```
[petite blonde woman between two men], [tall dark-haired man on left], [athletic bearded man on right], tangled together in bed, intimate and tender, soft warm lamp light
```

### FFF (Three Women)

Highest body-confusion risk — identical anatomy type x3. Requires maximum contrast on ALL markers.

**Rules:**
- All three MUST have different hair colour
- All three MUST have different skin tone or build
- Use vertical separation: kneeling/standing/lying
- CFG 7.0, steps 40

**Example:**
```
[blonde woman, petite, fair skin, standing], [brunette woman, curvy, olive skin, kneeling], [dark-skinned woman, athletic, short hair, lying on bed], passionate threesome, luxury penthouse, warm dramatic lighting, silk sheets
```

### Group (4+)

SDXL only. Landscape orientation (1216x832). Accept lower anatomical precision.

**Counterintuitive tip:** For 4+ people, describe the GROUP rather than itemising each person. The model handles "group of four nude people" better than four separate descriptions fighting for attention.

**Example:**
```
four attractive people on large bed, two men two women, passionate group embrace, tangled limbs, luxury bedroom, warm golden lighting, silk and velvet textures, intimate, erotic photography
```

---

## Character Blocks (Mix and Match)

Compact ~15-token descriptions. Drop these into any template.

**Women:**
```
blonde woman, late 20s, long wavy hair, blue eyes, athletic build, fair skin
brunette woman, early 30s, shoulder-length dark hair, brown eyes, curvy build, olive skin
redhead woman, mid 20s, short curly red hair, green eyes, petite build, pale freckled skin
asian woman, late 20s, long straight black hair, slim build, light skin
dark-skinned woman, mid 20s, natural curly hair, athletic build, rich dark skin
```

**Men:**
```
dark-haired man, early 30s, athletic build, tan skin, short hair
muscular man, late 20s, dark skin, shaved head, broad shoulders
lean man, mid 30s, brown wavy hair, hazel eyes, fair skin, stubble
tall man, 30s, dark hair, bearded, rugged, medium brown skin
```

**Do NOT include** personality, emotion, or narrative in character blocks — save that for the scene description. Token budget matters for multi-person prompts.

---

## Setting Templates

Each includes lighting keywords — critical for multi-person because dramatic lighting helps the model separate bodies spatially.

```
luxury penthouse bedroom, silk sheets, warm lamp light, floor-to-ceiling windows, city night skyline
```
```
marble bathroom, steam, soft diffused light, wet skin, warm water, glass shower
```
```
private pool at night, fairy lights, warm underwater glow, tropical foliage, steam rising
```
```
professional photography studio, clean white background, dramatic Rembrandt lighting, artistic
```
```
dark hotel room, single lamp, heavy curtains, amber light, tangled shadows, intimate
```
```
outdoor hot tub, night time, fairy lights, steam, champagne on edge, intimate
```

**Rule:** Simpler settings work on SD1.5. Complex environments (tropical pool, penthouse skyline) benefit from SDXL's higher resolution and attention capacity.

---

## Pose Templates (Easiest to Hardest)

Ordered by failure rate — start with the easiest, move down when you've found a good seed.

### MF Poses
1. `standing embrace, facing each other, his arms around her waist, her hands on his chest` — lowest failure rate
2. `woman sitting on man's lap, both facing camera`
3. `woman lying on bed, man above her, both facing viewer`
4. `woman pressed against wall, man facing her, her leg raised around his hip`
5. `man behind woman, both standing, his hands on her hips` — moderate difficulty
6. `woman on top, riding position, man lying on bed` — harder, use SDXL
7. `doggy style, man behind woman, side profile view` — hardest for SD1.5, SDXL recommended

### FF Poses
1. `standing embrace, facing each other, kissing` — easiest
2. `one woman lying, other above her, both facing viewer`
3. `spooning in bed, taller behind shorter`
4. `sitting face to face, legs intertwined`

### MM Poses
1. `standing embrace, one behind the other, arms wrapped around` — easiest
2. `kissing, facing each other, one against wall`
3. `one lying on other's chest in bed, relaxed`

### 3-Person Layouts
1. **Triangle:** `woman A kneeling foreground, man standing behind, woman B standing to right` — most stable
2. **Linear (bed):** `three people in a row, left to right with described interactions`
3. **Sandwich:** `woman in center, one person behind, one in front` — moderate difficulty
4. **Stacked:** `one person lying, one above, third alongside` — harder

---

## Seed Iteration Workflow

Multi-person anatomy is partly luck. Use this workflow to find winners efficiently:

1. **Explore:** Run with random seed (`--seed -1`) at SD1.5 to find compositions where bodies are correctly distinct. Expect ~30-50% usable at 2-person, ~15-25% at 3-person.

2. **Lock the seed:** When you find good anatomy, note the seed (printed after generation).

3. **Upscale quality:** Rerun with that seed at SDXL:
   ```bash
   python3 generate.py --preset maitland-ward-xl --seed 12345 --prompt "SAME PROMPT" --output ./output/refined.png
   ```

4. **Important:** Seed + CFG + steps + dimensions = a set. Changing any of these changes the output. If moving from SD1.5 to SDXL, the seed won't reproduce exactly — but good seeds tend to stay good.

---

## Triage Guide

When a generation fails, diagnose before regenerating:

| Problem | Fix |
|---|---|
| Extra limb visible | New seed, same settings — structural issue |
| Faces merged | Add `conjoined faces, merged faces` to negative, retry |
| Bodies blurring together | Increase CFG by 0.5, add more spatial keywords |
| One person missing | Move their description earlier in prompt, try bracket isolation |
| Wrong number of people | Add `extra people, too many people` or `only two people` to prompt/negative |
| Good anatomy but low quality | Keeper seed — rerun at SDXL with more steps |
| Good quality but wrong pose | Keep seed, adjust pose description, keep CFG/steps same |

**When to give up on a prompt:** If 5+ seeds all produce the same anatomical failure, the prompt structure is the problem. Restructure using bracket isolation and stronger spatial anchoring before trying more seeds.

---

## Performance (M1 Pro 16GB)

| Preset | Size | People | Time | Use For |
|---|---|---|---|---|
| maitland-ward | 512x768 | 2 | ~55s | Fast MF/FF iteration |
| maitland-ward | 512x768 | 3 | ~55s | Seed exploration only |
| maitland-ward-xl | 832x1216 | 2 | ~2.5 min | MF/FF/MM keepers |
| maitland-ward-xl | 1024x1536 | 2 | ~4 min | Maximum quality 2-person |
| maitland-ward-xl | 1024x1536 | 3 | ~4.5 min | MFF/MMF/FFF |
| maitland-ward-xl | 1216x832 | 4+ | ~4 min | Landscape group |

**VRAM note:** SDXL at 1024x1536 pushes 16GB hard. If generation stalls before starting (not just slow), ComfyUI is paging. Close other apps or drop to 832x1216.

---

## Output Locations

- Interactive: `~/calibre-hq/comfyui-engine/output/`
- Batches: specified in batch JSON `output_dir`
- Save keepers to `~/calibre-hq/image-library/` immediately
