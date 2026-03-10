---
name: image-pipeline
description: "Bridge between AI-generated images and document pipelines. Inserts images (from Nano Banana, DALL-E, local files, or URLs) into PPTX, DOCX, or PDF (via HTML for WeasyPrint). Trigger when the user wants to add images to a document, create a presentation with photos, insert generated images into slides, or when combining Nano Banana output with document creation. Also trigger for 'image to slide', 'photo in document', 'add picture to presentation'."
---

# Image Pipeline

Insert AI-generated or local images into PPTX, DOCX, or PDF documents.

## Quick Reference

| Task | Command |
|------|---------|
| Image → PPTX slide | `python image_to_doc.py photo.png output.pptx` |
| Image → DOCX | `python image_to_doc.py photo.png output.docx --width 5` |
| Image → HTML (for PDF) | `python image_to_doc.py photo.png --html` |
| URL → PPTX | `python image_to_doc.py --url "https://..." output.pptx` |
| Multiple → grid | `python image_to_doc.py a.png b.png c.png d.png output.pptx --layout grid` |

## Usage

### Insert into PowerPoint

```bash
# Single image, centered
python scripts/image_to_doc.py hero.png output.pptx

# Positioned left with specific width
python scripts/image_to_doc.py hero.png output.pptx --position left --width 4

# Multiple images in a grid layout
python scripts/image_to_doc.py img1.png img2.png img3.png img4.png output.pptx --layout grid

# From URL
python scripts/image_to_doc.py --url "https://example.com/photo.jpg" output.pptx
```

### Insert into Word

```bash
python scripts/image_to_doc.py photo.png output.docx --width 5
```

### Generate HTML for PDF Pipeline

```bash
# Get an HTML img tag with base64-encoded image
python scripts/image_to_doc.py photo.png --html --html-width "80%"
```

Output:
```html
<img src="data:image/png;base64,..." style="width: 80%; display: block; margin: 1em auto;" alt="photo">
```

Paste this into your HTML template before running WeasyPrint.

## Library Usage

```python
from image_to_doc import image_to_base64, generate_html_tag, get_image_dimensions

# Get base64 for PptxGenJS
b64 = image_to_base64("photo.png")
# Returns: "image/png;base64,iVBORw0..."

# Get HTML tag for WeasyPrint
html = generate_html_tag(["photo.png", "chart.png"], width="45%")

# Get dimensions for layout calculations
w, h = get_image_dimensions("photo.png")
```

## Workflow: Nano Banana → Document

1. Generate image with Nano Banana prompting skill
2. Save the generated image locally
3. Use this pipeline to insert into your target document:

```bash
# Into a presentation
python scripts/image_to_doc.py generated_hero.png deck.pptx --position center

# Into a PDF report (get HTML, add to template)
python scripts/image_to_doc.py generated_hero.png --html >> report.html
```

## Options

| Flag | Description |
|------|-------------|
| `--url URL` | Download image from URL first |
| `--position` | `center`, `left`, `right` (PPTX only) |
| `--layout` | `single` or `grid` (PPTX with multiple images) |
| `--width N` | Width in inches (PPTX/DOCX) |
| `--html` | Output HTML img tag instead of file |
| `--html-width` | CSS width for HTML output (default: 100%) |
| `--template` | PPTX reference template |

## Dependencies

- `pip install Pillow` — image dimension detection
- `pip install python-docx` — DOCX insertion
- `npm install -g pptxgenjs` — PPTX insertion
