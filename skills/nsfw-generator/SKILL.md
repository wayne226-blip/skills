---
name: nsfw-generator
description: Generate NSFW images via local ComfyUI — no filters, no API costs, fully private
triggers:
  - generate nsfw
  - generate image
  - comfyui generate
  - make me an image
  - filthy image
  - dirty image
  - boudoir
  - pinup
  - nsfw batch
---

# NSFW Image Generator

Generate images locally via ComfyUI with zero content restrictions. Supports both clean (kids/non-fiction) and NSFW (fiction pen names, pinup, adult content) modes.

## Prerequisites

ComfyUI must be running. If not:
```bash
open -a ComfyUI
```
Wait 5 seconds, then proceed.

## Quick Generate (Single Image)

```bash
cd ~/calibre-hq/comfyui-engine

# NSFW with pen name preset (applies style automatically)
python3 generate.py --preset maitland-ward --prompt "YOUR PROMPT" --output ./output/filename.png

# NSFW with specific preset
python3 generate.py --preset lady-elara --prompt "YOUR PROMPT" --output ./output/filename.png
python3 generate.py --preset sable-voss --prompt "YOUR PROMPT" --output ./output/filename.png

# Clean mode for kids content
python3 generate.py --preset puzzling-penny --prompt "YOUR PROMPT" --output ./output/filename.png

# Raw prompt (no style prefix/suffix added)
python3 generate.py --preset maitland-ward --raw-prompt --prompt "EXACT PROMPT" --output ./output/filename.png
```

## Available Presets

| Preset | Mode | Checkpoint | Style |
|---|---|---|---|
| maitland-ward | NSFW | epiCRealism | Erotic photography, boudoir, glamour |
| lady-elara | NSFW | epiCRealism | Regency dark romance, candlelit, gold/navy |
| sable-voss | NSFW | epiCRealism | Dark academia, gothic university, oxblood/gold |
| maren-wolfe | NSFW | epiCRealism | Dark paranormal, gothic forest, blood red/black |
| blake-hartley | NSFW | epiCRealism | Sports romance, ice hockey, cinematic |
| puzzling-penny | Clean | DreamShaper | Children's illustration, cute, bright |
| tom-hadley | Clean | DreamShaper | Professional, corporate, clean |

## Batch Generate

Create a JSON file in `~/calibre-hq/comfyui-engine/batch_jobs/`:

```json
{
  "name": "batch-name",
  "preset": "maitland-ward",
  "output_dir": "/path/to/output/",
  "jobs": [
    {"prompt": "description here", "filename": "output-name.png"},
    {"prompt": "another one", "filename": "another.png"}
  ]
}
```

Run it:
```bash
python3 generate.py --batch batch_jobs/your-batch.json
```

## Sizing

- Default: 512x768 (portrait, good for covers/pinups)
- Square: `--size 512x512` (good for spots, avatars)
- Landscape: `--size 768x512` (good for banners, scenes)
- SD 1.5 native resolution — upscale for print quality

## Performance on M1 Pro 16GB

- 512x512: ~35 seconds
- 512x768: ~50 seconds
- 20-image batch: ~17 minutes
- 60-image batch: ~50 minutes

## Prompt Guide

**Always read the full genre prompt guide before writing prompts:**
`~/calibre-hq/authors/vivienne-cole/prompt-guide.md`

Contains tested templates for all 41 Vivienne Cole content categories.

**Prompt structure formula:**
`[Character: age, hair, body, skin] + [Clothing/state] + [Pose/action] + [Setting] + [Lighting] + [Camera angle] + [Mood]`

**EpiCRealism-specific rules:**
- CFG is set to 5.0 (not 7) — the model oversaturates above 7
- Sampler is DPM++ SDE Karras — best for skin detail with this model
- Do NOT use "masterpiece", "best quality", "8k" — EpiCRealism ignores these, they waste tokens
- DO use camera terms: `85mm lens`, `DSLR`, `shallow depth of field`, `Kodachrome`
- Use `(feature:1.2-1.3)` weights for emphasis — never above 1.5
- For mature characters: always include physical markers `(crow's feet, laugh lines, natural aging:1.3)` — not just "age 50"
- For multi-person: use BREAK between characters and `(N distinct people:1.3)`
- Keep prompts under 75 tokens — overloading degrades output

**Negative prompt is pre-loaded per preset.** Override with `--negative "your negatives"`.

**Seed for reproducibility:** Use `--seed 12345` to recreate a specific image. Seed is printed after each generation.

## Output Locations

- Interactive: `~/calibre-hq/comfyui-engine/output/`
- Batches: specified in batch JSON `output_dir`
- ComfyUI also saves to: `~/Documents/ComfyUI/output/`

## Sales Channels (from research)

| Platform | Content Level | Notes |
|---|---|---|
| Gumroad | Adult OK | Age gates, no marketplace search, drive own traffic |
| Patreon | Adult OK | Tiered subscriptions, recurring revenue |
| Substack | Adult OK | Maitland Ward already live at maitward.substack.com |
| KDP | Erotica OK | Covers must meet guidelines (no full nudity on cover) |
| Etsy | CLEAN ONLY | Never mix adult content — will get shop banned |
