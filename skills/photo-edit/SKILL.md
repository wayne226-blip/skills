---
name: photo-edit
description: "Edit, transform, and batch-process existing photos and images. Handles resize, crop, rotate, flip, brightness/contrast/saturation/sharpness adjustments, format conversion (PNG/JPEG/WebP), text and image watermarks, and compositing. Uses a reusable Pillow-based CLI tool for common operations and writes custom Pillow scripts for anything unusual. Use when someone says 'edit photo', 'resize image', 'crop', 'convert to JPEG', 'add watermark', 'adjust brightness', 'make this smaller', 'batch resize', 'compress images', 'change format', 'flip', 'rotate', or any image manipulation task on existing files. Distinct from photo-director (which PLANS photography shoots and generates AI image prompts) and ad-creative (which generates AD format image prompts). photo-edit works on files that already exist on disk."
---

# Photo Edit

Edit, transform, and batch-process existing images using a Pillow-based CLI tool.

**This skill edits existing files.** For generating new images from scratch, use photo-director or ad-creative instead.

## Setup

First-time only:

```bash
cd ~/.claude/skills/photo-edit/scripts && uv sync
```

## Workflow

1. **Identify the task** — what does the user want done, and to which files?
2. **Choose the tool** — use `photo_edit.py` for standard operations (see Command Reference below). For anything it doesn't cover, write a custom Pillow script.
3. **Confirm** — before running, tell the user what you're about to do and where output will go.
4. **Run** — execute via `cd ~/.claude/skills/photo-edit/scripts && uv run python photo_edit.py <command> [options] <files>`
5. **Report** — show what was processed and where outputs landed.

## Output Convention

All output goes to an `edited/` subdirectory next to the input files. Originals are never modified. Override with `--output-dir <path>`.

## Command Reference

All commands accept: `--output-dir`/`-o`, `--suffix`/`-s`, `--quality`/`-q`, plus one or more input files.

### resize
Resize preserving aspect ratio.
```
photo_edit.py resize --width 800 photo.jpg
photo_edit.py resize --height 600 *.png
photo_edit.py resize --percent 50 large.jpg
photo_edit.py resize --max-dim 1200 photo.jpg
```

### crop
Crop to dimensions or aspect ratio.
```
photo_edit.py crop --width 800 --height 600 photo.jpg
photo_edit.py crop --aspect 16:9 photo.jpg
photo_edit.py crop --aspect 1:1 --gravity top photo.jpg
```
Gravity options: `center` (default), `top`, `bottom`, `left`, `right`.

### rotate
Rotate or flip.
```
photo_edit.py rotate --degrees 90 photo.jpg
photo_edit.py rotate --flip-h photo.jpg
photo_edit.py rotate --flip-v photo.jpg
```

### adjust
Brightness, contrast, saturation, sharpness. Values are multipliers (1.0 = no change).
```
photo_edit.py adjust --brightness 1.3 --contrast 1.1 photo.jpg
photo_edit.py adjust --saturation 0.5 photo.jpg          # desaturate
photo_edit.py adjust --sharpness 2.0 blurry.jpg
```

### convert
Change image format.
```
photo_edit.py convert --format webp *.jpg
photo_edit.py convert --format jpeg --quality 80 screenshot.png
```

### watermark
Add text or image overlay.
```
photo_edit.py watermark --text "DRAFT" --opacity 0.3 photo.jpg
photo_edit.py watermark --text "Wayne Pearce" --position bottom-right --size 36 photo.jpg
photo_edit.py watermark --image logo.png --opacity 0.5 --position top-left photo.jpg
```
Positions: `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`.

### composite
Layer one image on another.
```
photo_edit.py composite --overlay badge.png --position 100,50 --opacity 0.8 background.jpg
```

### info
Print image metadata (no output file created).
```
photo_edit.py info photo.jpg
photo_edit.py info *.png
```

## When to Write Custom Pillow Code Instead

Use `photo_edit.py` for the commands above. Write a custom Python script for:
- Complex multi-step pipelines (e.g. resize + crop + watermark in specific sequence with conditional logic)
- Filters not covered (blur, emboss, edge detection, colour channel manipulation)
- Drawing shapes, lines, or complex text layouts
- Batch operations with per-file logic (e.g. different crops for landscape vs portrait)
- Anything involving pixel-level manipulation

When writing custom scripts, use `uv run` with an inline script dependency:
```bash
uv run --with Pillow python my_script.py
```
