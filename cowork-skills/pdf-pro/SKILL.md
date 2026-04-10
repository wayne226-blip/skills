---
name: pdf-pro
description: UPGRADED PDF skill with WeasyPrint. Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.

## Quick Reference — Choosing the Right Tool

| Task | Best Tool | Why |
|------|-----------|-----|
| **Create new PDFs** (reports, proposals, letters) | **WeasyPrint** (`scripts/html_to_pdf.py`) | Full CSS3, flexbox, page numbers, headers/footers — professional output |
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Simple generated PDFs (labels, barcodes) | ReportLab | Good for programmatic, data-driven elements |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see FORMS.md) | See FORMS.md |

---

## Creating New PDFs (Recommended: WeasyPrint HTML-to-PDF)

The best way to create professional-looking PDFs is to write styled HTML and convert it with WeasyPrint. This gives you full CSS3 support — flexbox layouts, `@page` rules for page numbers and headers/footers, web fonts, multi-column layouts, and cover pages. The results are dramatically better than ReportLab for any document a human will read.

### Setup

WeasyPrint needs to be installed once per session:
```bash
pip install weasyprint --break-system-packages
```

### Basic Usage

```bash
# From an HTML file
python scripts/html_to_pdf.py report.html report.pdf

# From an HTML string
python scripts/html_to_pdf.py --from-string "<h1>Hello</h1><p>Content here.</p>" output.pdf

# With options
python scripts/html_to_pdf.py input.html output.pdf --size a4
python scripts/html_to_pdf.py input.html output.pdf --landscape
python scripts/html_to_pdf.py input.html output.pdf --margin 0.75in
python scripts/html_to_pdf.py input.html output.pdf --css extra-styles.css
```

### Recommended Workflow

1. Write content as a single HTML file with inline `<style>` block
2. Run `python scripts/html_to_pdf.py input.html output.pdf`
3. Preview: `pdftoppm -jpeg -r 150 output.pdf preview` then view the images
4. Iterate on the HTML/CSS until it looks right

### HTML Template Patterns

These CSS patterns work in WeasyPrint and produce professional results.

**Page numbers and headers/footers** — use `@page` rules with named areas:
```css
@page {
    size: letter;
    margin: 1in;
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #718096;
    }
    @top-right {
        content: "Confidential";
        font-size: 8pt;
        font-style: italic;
        color: #a0aec0;
    }
}

/* Suppress header/footer on first (cover) page */
@page :first {
    @top-right { content: none; }
    @bottom-center { content: none; }
}
```

**Cover page** — centered content with a page break after:
```html
<div style="text-align: center; padding-top: 3in; page-break-after: always;">
    <h1 style="font-size: 28pt; color: #1a365d;">Report Title</h1>
    <p style="font-size: 14pt; color: #2b6cb0;">Subtitle</p>
    <p style="font-size: 10pt; color: #718096;">March 2026</p>
</div>
```

**Section breaks** — force new page before a section:
```css
.section-break { page-break-before: always; }
.keep-together { page-break-inside: avoid; }
```

**KPI/metric cards** — use flexbox:
```html
<div style="display: flex; gap: 16px; margin: 1em 0;">
    <div style="flex: 1; background: #f7fafc; border: 1px solid #e2e8f0;
                border-radius: 8px; padding: 16px; text-align: center;">
        <div style="font-size: 24pt; font-weight: 700; color: #1a365d;">$4.2M</div>
        <div style="font-size: 9pt; color: #718096; text-transform: uppercase;">Revenue</div>
        <div style="font-size: 10pt; color: #38a169;">+18% YoY</div>
    </div>
    <!-- more cards... -->
</div>
```

**Two-column layout**:
```html
<div style="display: flex; gap: 24px;">
    <div style="flex: 1;">Left column</div>
    <div style="flex: 1;">Right column</div>
</div>
```

**Styled tables** — standard HTML tables with CSS:
```html
<style>
    table { width: 100%; border-collapse: collapse; font-size: 10pt; }
    th { background: #1a365d; color: white; padding: 10px 12px; text-align: left; }
    td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) td { background: #f7fafc; }
</style>
```

**Callout/highlight box**:
```html
<div style="background: #ebf8ff; border-left: 4px solid #2b6cb0;
            padding: 16px 20px; margin: 1em 0; border-radius: 0 6px 6px 0;">
    <strong style="color: #1a365d;">Key Takeaway:</strong> Your insight here.
</div>
```

### Full Example HTML Structure

A well-structured PDF document typically looks like this:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Document Title</title>
    <style>
        body { font-family: -apple-system, sans-serif; font-size: 11pt; line-height: 1.6; color: #2d3748; }
        @page { size: letter; margin: 1in;
            @bottom-center { content: "Page " counter(page) " of " counter(pages); font-size: 9pt; color: #718096; }
        }
        @page :first { @bottom-center { content: none; } }
        h2 { color: #1a365d; border-bottom: 2px solid #2b6cb0; padding-bottom: 0.3em; }
        h3 { color: #2b6cb0; }
        /* ... more styles ... */
    </style>
</head>
<body>
    <!-- Cover page -->
    <div style="text-align: center; padding-top: 3in; page-break-after: always;">
        <h1>Title</h1>
    </div>

    <!-- Content sections -->
    <h2>Section 1</h2>
    <p>Content...</p>

    <h2 style="page-break-before: always;">Section 2</h2>
    <p>More content...</p>
</body>
</html>
```

---

## Reading and Extracting from PDFs

### Quick Start
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

text = ""
for page in reader.pages:
    text += page.extract_text()
```

### pdfplumber — Text and Table Extraction

```python
import pdfplumber

# Extract text with layout
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

# Extract tables
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

### Advanced Table Extraction to Excel
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

---

## Manipulating Existing PDFs

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()
page = reader.pages[0]
page.rotate(90)
writer.add_page(page)
with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### Add Watermark
```python
watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Password Protection
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

---

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
pdftotext input.pdf output.txt              # Extract text
pdftotext -layout input.pdf output.txt      # Preserve layout
pdftotext -f 1 -l 5 input.pdf output.txt   # Pages 1-5
```

### qpdf
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf  # Merge
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf            # Split
qpdf input.pdf output.pdf --rotate=+90:1                 # Rotate page 1
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf  # Decrypt
```

### Extract Images
```bash
pdfimages -j input.pdf output_prefix
```

### OCR Scanned PDFs
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"
```

---

## ReportLab — Programmatic PDF Creation (Legacy)

ReportLab is still useful for simple programmatic PDFs like labels, barcodes, or data-driven documents where you're iterating over rows. For anything a human will read (reports, proposals, letters), prefer the WeasyPrint HTML approach above — it's faster to write and produces much better-looking output.

### Basic ReportLab Usage
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter
c.drawString(100, height - 100, "Hello World!")
c.line(100, height - 140, 400, height - 140)
c.save()
```

**IMPORTANT**: Never use Unicode subscript/superscript characters in ReportLab PDFs. Use `<sub>` and `<super>` tags in Paragraph objects instead.

---

## Brand Theme (wayne_brand.css)

A drop-in CSS theme at `scripts/wayne_brand.css` provides Wayne's branded styling for any WeasyPrint PDF. It includes pre-built components — cover pages, KPI cards, tables, callouts, badges, and two/three-column layouts — all with consistent typography and colors.

### Using the Brand Theme

Include it in your HTML:
```html
<link rel="stylesheet" href="scripts/wayne_brand.css">
```

Or read and inline it:
```python
with open("scripts/wayne_brand.css") as f:
    css = f.read()
html = f"<style>{css}</style><div class='cover'><h1>Report Title</h1>...</div>"
```

### Available CSS Classes

| Class | Purpose |
|-------|---------|
| `.cover`, `.cover h1`, `.subtitle`, `.bar`, `.meta` | Cover page |
| `.kpi-row`, `.kpi-card`, `.kpi-value`, `.kpi-label`, `.kpi-delta` | KPI metric cards |
| `.callout`, `.callout-success`, `.callout-warn`, `.callout-danger` | Callout boxes |
| `.badge-done`, `.badge-wip`, `.badge-blocked`, `.badge-new` | Status badges |
| `.two-col`, `.three-col` | Column layouts |
| `.section-break`, `.keep-together` | Page break control |

To rebrand, edit the CSS variables at the top of `wayne_brand.css`:
```css
:root {
    --brand-primary: #1E2761;
    --brand-secondary: #2B6CB0;
    /* etc. */
}
```

---

## Embedding Images in PDFs

Use `scripts/image_helpers.py` to embed local images into HTML for WeasyPrint rendering.

```bash
# Get an HTML <img> tag with base64-encoded image
python scripts/image_helpers.py photo.png --html --width 80%

# Get just the data URI
python scripts/image_helpers.py photo.png
```

Library usage:
```python
from image_helpers import image_to_base64_uri, generate_img_tag, generate_img_tags

# Single image
tag = generate_img_tag("chart.png", width="60%", css_class="chart")

# Multiple images
tags = generate_img_tags(["img1.png", "img2.png"], width="45%")
```

Insert the returned HTML into your template before running WeasyPrint.

---

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- If you need to fill out a PDF form, follow the instructions in FORMS.md
- For troubleshooting guides, see REFERENCE.md
