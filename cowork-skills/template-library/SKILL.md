---
name: template-library
description: "Branded template library for consistent document output. Provides Wayne's brand CSS theme for WeasyPrint PDFs, PPTX reference template generator (5 palettes, 5 slide masters), and DOCX reference template generator. Use whenever creating branded documents, or when other skills need consistent styling. Trigger when the user mentions 'brand', 'template', 'branded', 'consistent look', 'company style', or when generating multiple documents that should look the same."
---

# Template Library

Provides branded templates and themes for consistent document output across all formats.

## Quick Reference

| Asset | File | Usage |
|-------|------|-------|
| **PDF theme** | `wayne_brand.css` | `<link>` or inline in HTML before WeasyPrint |
| **PPTX template** | `create_pptx_template.js` | Generate → use with `--reference` in Pandoc |
| **DOCX template** | `create_docx_template.py` | Generate → use with `--reference-doc` in Pandoc |

## Color Palettes

All three generators share 5 consistent palettes:

| Palette | Primary | Secondary | Best For |
|---------|---------|-----------|----------|
| **midnight** (default) | Navy `#1E2761` | Blue `#2B6CB0` | Professional, corporate |
| **forest** | Green `#2C5F2D` | Moss `#97BC62` | Nature, sustainability |
| **coral** | Navy `#2F3C7E` | Coral `#F96167` | Creative, energetic |
| **ocean** | Deep blue `#065A82` | Teal `#1C7293` | Technology, trust |
| **charcoal** | Charcoal `#36454F` | Off-white `#F2F2F2` | Minimal, modern |

## PDF Theme (WeasyPrint)

The CSS theme `wayne_brand.css` provides styled components:

- **Cover page**: `.cover`, `.cover h1`, `.subtitle`, `.bar`, `.meta`
- **KPI cards**: `.kpi-row`, `.kpi-card`, `.kpi-value`, `.kpi-label`, `.kpi-delta`
- **Tables**: Auto-styled with header colors, alternating rows
- **Callouts**: `.callout`, `.callout-success`, `.callout-warn`, `.callout-danger`
- **Badges**: `.badge-done`, `.badge-wip`, `.badge-blocked`, `.badge-new`
- **Layout**: `.two-col`, `.three-col`, `.section-break`, `.keep-together`
- **Page setup**: @page rules with page numbers, author header

### Usage

```html
<link rel="stylesheet" href="wayne_brand.css">
<!-- Or copy CSS inline into <style> tag -->
```

To change the palette, modify the CSS variables at the top of the file:

```css
:root {
    --brand-primary: #1E2761;
    --brand-secondary: #2B6CB0;
    /* etc. */
}
```

## PPTX Template

Generate a branded PowerPoint reference template:

```bash
node create_pptx_template.js output.pptx --palette midnight
```

Creates 5 slide masters: `TITLE_SLIDE`, `CONTENT_SLIDE`, `SECTION_BREAK`, `TWO_COLUMN`, `CLOSING_SLIDE`.

Use with Pandoc:
```bash
python html_to_pptx.py content.md output.pptx --reference wayne_brand_template.pptx
```

Use with PptxGenJS:
```javascript
let slide = pres.addSlide({ masterName: "CONTENT_SLIDE" });
slide.addText("Title", { placeholder: "title" });
```

## DOCX Template

Generate a branded Word reference template:

```bash
python create_docx_template.py output.docx --palette midnight
```

Configures styles: Title, Subtitle, Heading 1–4, Normal body text.

Use with Pandoc:
```bash
pandoc content.md -o output.docx --reference-doc=wayne_brand_template.docx
```

## Generating Templates for a Session

At the start of a session where you'll create multiple branded documents:

```bash
# Generate all three templates
node scripts/create_pptx_template.js /tmp/brand_template.pptx --palette midnight
python scripts/create_docx_template.py /tmp/brand_template.docx --palette midnight
# CSS is ready to use directly — just include it in your HTML
```

Then reference them throughout the session for consistent output.
