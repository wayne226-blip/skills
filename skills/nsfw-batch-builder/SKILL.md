---
name: nsfw-batch-builder
description: Build themed NSFW image batches for Gumroad/Patreon products
triggers:
  - nsfw batch
  - build a set
  - image pack
  - gumroad set
  - pinup set
  - boudoir set
  - content pack
---

# NSFW Batch Builder

Create themed image packs for sale on Gumroad, Patreon, or use as fiction cover assets. Generates batch JSON files for the ComfyUI engine, then runs them.

## Workflow

1. **Pick a theme** — boudoir, fantasy, pin-up, seasonal, genre-specific
2. **Define the character(s)** — hair, eyes, body type, distinguishing features
3. **Generate 15-30 variations** — different poses, outfits, settings, lighting
4. **Curate** — review outputs, regenerate duds with different seeds
5. **Package** — organise into a product folder for upload

## Product Templates

### Boudoir Set (Gumroad, £4.99-9.99)
15-20 images of a single character model in bedroom/luxury settings.
Variations: lingerie, silk robe, nude artistic, shower, morning light.

### Fantasy Pin-Up Set (Gumroad, £3.99-7.99)
15-20 images with fantasy/cosplay themes.
Variations: elven queen, dark sorceress, warrior priestess, fairy, vampire.

### Seasonal Set (Gumroad, £2.99-4.99)
10-15 images tied to a holiday/season.
Variations: Christmas lingerie, Halloween witch, Valentine's boudoir, summer beach.

### Romance Cover Pack (for pen names, internal use)
10-20 potential cover backgrounds for fiction books.
Dark romance, paranormal, sports romance, historical.

### Character Consistency Set (Patreon tier reward)
20-30 images of the SAME character across different scenarios.
Use same seed base + face description for consistency.

## Building a Batch

Create the batch JSON at `~/calibre-hq/comfyui-engine/batch_jobs/`:

```json
{
  "name": "valentines-boudoir-2026",
  "preset": "maitland-ward",
  "output_dir": "~/calibre-hq/comfyui-engine/output/valentines-set/",
  "jobs": [
    {
      "prompt": "CHARACTER_DESC, red silk lingerie, rose petals on bed, candlelight",
      "filename": "valentines-01-silk.png"
    }
  ]
}
```

Run: `python3 generate.py --batch batch_jobs/valentines-boudoir-2026.json`

## Character Consistency

For sets featuring the same character, use a consistent character block at the start of every prompt:

```
"beautiful blonde woman, age 25, bright blue eyes, long wavy hair, athletic build, light skin, small nose"
```

Then vary only the scene/outfit/pose after this block.

## Pricing Guide (Gumroad)

| Product | Images | Price | Notes |
|---|---|---|---|
| Mini pack | 5-10 | £1.99-2.99 | Taster/loss leader |
| Standard set | 15-20 | £4.99-7.99 | Core product |
| Premium collection | 25-40 | £9.99-14.99 | Multiple themes |
| Monthly subscription | 20-30/mo | £4.99/mo | Patreon model |

## File Organisation

```
~/calibre-hq/comfyui-engine/
  output/
    {set-name}/           # Raw generations
  products/
    {product-name}/       # Curated, ready to upload
      preview/            # Watermarked previews for listing
      full/               # Full resolution for buyers
      listing.md          # Gumroad description
```
