---
name: pdf-designer
description: Design-focused PDF creation with professional themes. Use this skill whenever creating a new PDF that needs to look good — reports, proposals, audits, dashboards, case studies, branded documents, or any PDF where visual quality matters. This skill provides 5 distinct visual themes (executive, modern, creative, corporate, dark) and design guidance that transforms generic PDFs into polished, professional documents. Trigger on any PDF creation task, especially when the user mentions "report", "proposal", "audit", "dashboard", "branded", "professional", or wants a PDF that doesn't look like a default template. Also use when the user says "make it look good", "better design", "not so generic", or expresses dissatisfaction with how a PDF looks. This skill complements pdf-pro — pdf-pro handles the mechanics (merge, split, extract, forms), this skill handles the aesthetics.
---

# PDF Designer

This skill transforms generic-looking PDFs into polished, professional documents. It provides 5 visual themes and design principles that make the difference between "looks like a robot made it" and "looks like a designer made it."

## How It Works

Every PDF you create follows this pipeline:
1. Pick a theme (or let the content guide you)
2. Write HTML using the theme's CSS classes
3. Convert to PDF with WeasyPrint

The themes handle all the visual heavy lifting — typography, colours, spacing, cover pages, cards, tables — so you can focus on the content.

## Setup

WeasyPrint needs to be installed once per session:
```bash
pip install weasyprint --break-system-packages
```

## Choosing a Theme

Each theme has a distinct personality. Pick based on who's reading the document and what impression you want to make.

| Theme | Personality | Best For |
|-------|------------|----------|
| **executive** | Sophisticated, authoritative. Dark navy + gold. Serif headings. | Proposals, board packs, client reports, pitch decks |
| **modern** | Clean, minimal. Monochrome + indigo accent. Bold sans-serif. | Tech reports, SaaS docs, project updates, internal docs |
| **creative** | Bold, energetic. Purple-to-pink gradient. Vibrant. | Marketing reports, brand decks, case studies, social media audits |
| **corporate** | Professional, trustworthy. Blue-grey, no surprises. | Audits, compliance docs, formal reports, financial summaries |
| **dark** | Sleek, high-contrast. Dark background, neon accents. | Analytics dashboards, dev docs, portfolio pieces, tech presentations |

If the user doesn't specify a theme, choose based on context:
- Business/client-facing → **executive**
- Technical/internal → **modern**
- Marketing/creative → **creative**
- Formal/compliance → **corporate**
- Data-heavy/analytics → **dark** or **modern**

## Using a Theme

Read the theme CSS from `themes/[name].css` and inline it in the HTML:

```python
import os
skill_dir = os.path.dirname(os.path.abspath(__file__))  # adjust path as needed

# Read the theme
with open(os.path.join(skill_dir, "themes", "modern.css")) as f:
    theme_css = f.read()

# Build the HTML
html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>{theme_css}</style>
</head>
<body>
    <!-- Cover page -->
    <div class="cover">
        <div class="eyebrow">Project Report</div>
        <h1>The Title Goes Here</h1>
        <div class="subtitle">A subtitle with more context</div>
        <div class="bar"></div>
        <div class="meta">
            Prepared by Wayne Pearce<br>
            March 2026
        </div>
    </div>

    <!-- Content starts here -->
    <h2>Section Heading</h2>
    <p>Your content...</p>
</body>
</html>"""
```

Then convert:
```bash
python scripts/html_to_pdf.py input.html output.pdf --size a4
```

## Design Principles

These principles are what separate a good PDF from a generic one. They apply regardless of which theme you use.

### Typography Creates Hierarchy

The eye needs to know where to look. Every theme uses a clear size/weight ladder:
- **Cover title**: 32-40pt, heaviest weight — the first thing anyone sees
- **Section headings (h2)**: 15-16pt with a coloured underline — they signal "new topic"
- **Subsection headings (h3)**: 12pt in the accent colour — secondary landmarks
- **Body text**: 10.5pt with generous line-height (1.6-1.7) — comfortable to read
- **Captions and labels**: 7.5-8pt, muted colour, often uppercase — metadata that stays out of the way

The gap between heading sizes matters. If h2 and h3 look too similar, the document feels flat.

### White Space Is Not Wasted Space

The most common mistake in generated PDFs is cramming too much onto each page. Generous margins (0.85-1in), spacing between sections (margin-top on headings), and padding inside cards/callouts all contribute to a document that breathes. It's better to use an extra page than to compress everything.

### Colour Should Have a Job

Every colour in the theme exists for a reason:
- **Primary** (headings, emphasis) — draws the eye to structure
- **Secondary/accent** (subheadings, links, borders) — adds visual interest without competing
- **Muted** (captions, metadata, page numbers) — present but doesn't distract
- **Semantic** (green=good, red=bad, amber=warning) — instant meaning

Don't add random colours. If you need to highlight something, use a `.callout` box or a `.badge`.

### Cover Pages Set the Tone

Every PDF of more than 2 pages should have a cover page. The cover page uses `page-break-after: always` so it stands alone. It should include:
- A title (obviously)
- A subtitle or one-line description
- The author/date
- Optionally a category label (`.eyebrow` class)

The cover uses the theme's most distinctive styling — the executive theme uses a dark background, the creative theme uses a gradient, the modern theme uses oversized bold type.

### Tables Should Be Scannable

Tables are where most PDFs fall apart visually. The themes handle this with:
- Dark header row with uppercase labels — clearly separates headers from data
- Alternating row backgrounds — makes it easy to track across wide tables
- Consistent padding — nothing feels cramped
- Small font size (9.5pt) — fits more data without looking cluttered

For tables with many columns, consider landscape orientation (`--landscape` flag).

### KPI Cards Tell the Story

When you have 3-5 key metrics, put them in `.kpi-row` with `.kpi-card` elements. Each card shows:
- `.kpi-value` — the big number (26-28pt)
- `.kpi-label` — what the number means (tiny uppercase)
- `.kpi-delta` — change from last period (coloured green/red)

These work in every theme and immediately give the reader the headlines before they dive into detail.

## HTML Component Reference

All themes share the same CSS class names, so you can swap themes without changing your HTML structure.

### Cover Page
```html
<div class="cover">
    <div class="eyebrow">Category Label</div>
    <h1>Document Title</h1>
    <div class="subtitle">Subtitle or tagline</div>
    <div class="bar"></div>
    <div class="meta">
        Author Name<br>
        Date
    </div>
</div>
```

### KPI Cards
```html
<div class="kpi-row keep-together">
    <div class="kpi-card">
        <div class="kpi-value">£42K</div>
        <div class="kpi-label">Revenue</div>
        <div class="kpi-delta green">+18% MoM</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">94%</div>
        <div class="kpi-label">Uptime</div>
        <div class="kpi-delta red">-2%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">1,204</div>
        <div class="kpi-label">Users</div>
        <div class="kpi-delta green">+340</div>
    </div>
</div>
```

### Callout Boxes
```html
<div class="callout">
    <strong>Key Insight:</strong> Your main point here.
</div>
<div class="callout callout-success">
    <strong>Result:</strong> Something good happened.
</div>
<div class="callout callout-warn">
    <strong>Note:</strong> Something to watch out for.
</div>
<div class="callout callout-danger">
    <strong>Warning:</strong> Something critical.
</div>
```

### Two/Three Column Layout
```html
<div class="two-col">
    <div>
        <h3>Left Side</h3>
        <p>Content for the left column.</p>
    </div>
    <div>
        <h3>Right Side</h3>
        <p>Content for the right column.</p>
    </div>
</div>
```

### Status Badges
```html
<span class="badge badge-done">Complete</span>
<span class="badge badge-wip">In Progress</span>
<span class="badge badge-blocked">Blocked</span>
<span class="badge badge-new">New</span>
```

### Section Breaks and Keep-Together
```html
<!-- Force a new page before this section -->
<h2 class="section-break">New Section</h2>

<!-- Prevent this block from being split across pages -->
<div class="keep-together">
    <h3>Important Block</h3>
    <p>This stays on one page.</p>
</div>
```

### Theme-Specific Components

Some themes have unique components that match their personality:

**Executive** — `.exec-summary` (dark box for executive summary):
```html
<div class="exec-summary">
    <h3>Executive Summary</h3>
    <p>The key points in a visually distinct box.</p>
</div>
```

**Modern** — `.highlight` (dark accent box):
```html
<div class="highlight">
    <h3>Key Finding</h3>
    <p>Stands out from the rest of the content.</p>
</div>
```

**Creative** — `.gradient-box` (gradient accent box):
```html
<div class="gradient-box">
    <h3>Spotlight</h3>
    <p>Eye-catching section for important content.</p>
</div>
```

**Dark** — `.glow-box` (bordered accent box):
```html
<div class="glow-box">
    <h3>Highlighted Data</h3>
    <p>Draws attention with a subtle border glow.</p>
</div>
```

## Conversion

Use the bundled `scripts/html_to_pdf.py`:

```bash
# Standard A4
python scripts/html_to_pdf.py report.html report.pdf --size a4

# Landscape for wide tables
python scripts/html_to_pdf.py report.html report.pdf --size a4 --landscape

# Custom margins
python scripts/html_to_pdf.py report.html report.pdf --margin 0.75in
```

To preview before finalising (useful for catching layout issues):
```bash
pdftoppm -jpeg -r 150 output.pdf preview
```

## Embedding Images

Use `scripts/image_helpers.py` to embed images as base64 so they render in the PDF:
```python
from image_helpers import generate_img_tag
tag = generate_img_tag("chart.png", width="80%")
# Insert `tag` into your HTML string
```

## Quick Start Checklist

When creating a new PDF:
1. Pick a theme based on audience and content type
2. Read the theme CSS from `themes/[name].css`
3. Build your HTML with a cover page, sections, and the component classes
4. Inline the CSS in a `<style>` tag
5. Convert with `scripts/html_to_pdf.py`
6. Preview with `pdftoppm` and adjust if needed
7. Save the final PDF to the workspace folder
