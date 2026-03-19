---
name: web-slides
description: "Create beautiful presentation slides as single-file HTML with Tailwind CSS, then optionally export to PPTX. Generates a standalone HTML presentation with full-viewport slides (1920x1080), each designed using Tailwind utility classes and Google Fonts. Can screenshot each slide via Playwright and assemble into a .pptx file where slides are full-bleed images. Use when someone wants to create slides, a presentation, a deck, a pitch deck using web technologies, or says 'make me slides', 'presentation about', 'slide deck for', 'web slides', 'HTML slides', 'beautiful slides'. Distinct from pptx-pro (which works with existing .pptx files and native PowerPoint elements) -- web-slides designs slides as HTML first for pixel-perfect visuals, then optionally converts to PPTX as images."
---

# Web Slides

Create stunning presentations using HTML, Tailwind CSS, and Google Fonts. Optionally export to PPTX.

**Pipeline:** Content -> HTML slides -> (optional) PNG screenshots -> (optional) .pptx assembly

**Two output modes:**
- **HTML presentation** -- standalone file, open in browser, present with arrow keys
- **PPTX export** -- each slide screenshotted and assembled into .pptx (image-based, not editable text)

---

## Workflow

### Step 1: Intake

Collect from the user:

- **Topic / content** (required) -- what the presentation is about. Can be markdown, bullet points, structured data, or natural language
- **Slide count** (optional, default: 8-12)
- **Theme** (optional, default: recommend based on topic) -- pick from built-in themes or describe custom
- **Output format** (optional, default: HTML only):
  - `html` -- standalone HTML presentation
  - `pptx` -- HTML + screenshots + PPTX assembly
  - `both` -- all outputs
  - `png` -- HTML + individual slide PNGs
- **Audience** (optional) -- helps tailor design density and language

If the user provides content upfront, proceed with sensible defaults. Don't interrogate.

### Step 2: Theme Selection

Load `references/themes.md`. Either use the user's choice or recommend one based on the topic.

Each theme provides:
- 4-5 hex colours (primary, secondary, accent, background, text)
- Google Fonts pairing (heading + body)
- Tailwind config extension snippet

Present the theme briefly -- name + colour swatches described. Move on unless the user objects.

### Step 3: Plan the Deck

For each slide, plan:
- **Layout** from `references/slide-layouts.md` (title, two-column, stats, quote, etc.)
- **Content** -- headline, body text, supporting elements
- **Visual approach** -- which theme colours, gradients, decorative elements

Present the outline as a numbered list:
```
1. Title Slide -- "Your Headline Here" (gradient bg, centred)
2. Two Column -- Problem statement left, solution right
3. Stats -- 3 key numbers with labels
...
```

Wait for user approval before building. They may want to reorder, add, or remove slides.

### Step 4: Generate HTML

Build a single HTML file with all slides. Use the Write tool to create the file, then Edit to add slides incrementally (2-3 slides per edit to avoid output token limits).

**HTML structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{PRESENTATION_TITLE}</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={HEADING_FONT_URL}&family={BODY_FONT_URL}&display=swap" rel="stylesheet">
  <style type="text/tailwindcss">
    @theme {
      --color-primary: {PRIMARY_HEX};
      --color-secondary: {SECONDARY_HEX};
      --color-accent: {ACCENT_HEX};
      --color-surface: {SURFACE_HEX};
      --font-heading: '{HEADING_FONT}', sans-serif;
      --font-body: '{BODY_FONT}', sans-serif;
    }
  </style>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .slide {
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      position: relative;
      flex-shrink: 0;
    }
    /* Screenshot mode: all slides stacked vertically */
    body.screenshot-mode .slide { display: flex; }
    /* Presentation mode: one slide at a time */
    body.present-mode .slide { display: none; position: fixed; top: 0; left: 0; }
    body.present-mode .slide.active { display: flex; }
    /* Scale to fit viewport in presentation mode */
    body.present-mode {
      overflow: hidden;
      background: #000;
    }
    #slide-counter {
      position: fixed;
      bottom: 20px;
      right: 30px;
      color: rgba(255,255,255,0.5);
      font-family: system-ui;
      font-size: 14px;
      z-index: 1000;
      display: none;
    }
    body.present-mode #slide-counter { display: block; }
  </style>
</head>
<body class="screenshot-mode">

  <!-- SLIDES GO HERE -->

  <div id="slide-counter"></div>

  <script>
    // Minimal slideshow engine
    const slides = document.querySelectorAll('.slide');
    let current = 0;
    const counter = document.getElementById('slide-counter');

    function showSlide(n) {
      current = Math.max(0, Math.min(n, slides.length - 1));
      slides.forEach((s, i) => s.classList.toggle('active', i === current));
      counter.textContent = `${current + 1} / ${slides.length}`;
      // Scale slide to fit viewport
      const scaleX = window.innerWidth / 1920;
      const scaleY = window.innerHeight / 1080;
      const scale = Math.min(scaleX, scaleY);
      slides[current].style.transform = `scale(${scale})`;
      slides[current].style.transformOrigin = 'top left';
      slides[current].style.left = `${(window.innerWidth - 1920 * scale) / 2}px`;
      slides[current].style.top = `${(window.innerHeight - 1080 * scale) / 2}px`;
    }

    function enterPresent() {
      document.body.classList.remove('screenshot-mode');
      document.body.classList.add('present-mode');
      showSlide(current);
    }

    function exitPresent() {
      document.body.classList.remove('present-mode');
      document.body.classList.add('screenshot-mode');
      slides.forEach(s => {
        s.style.transform = '';
        s.style.left = '';
        s.style.top = '';
        s.classList.remove('active');
      });
    }

    document.addEventListener('keydown', (e) => {
      if (!document.body.classList.contains('present-mode')) {
        if (e.key === 'f' || e.key === 'F') enterPresent();
        return;
      }
      switch(e.key) {
        case 'ArrowRight': case 'ArrowDown': case ' ':
          e.preventDefault(); showSlide(current + 1); break;
        case 'ArrowLeft': case 'ArrowUp':
          e.preventDefault(); showSlide(current - 1); break;
        case 'Home': showSlide(0); break;
        case 'End': showSlide(slides.length - 1); break;
        case 'Escape': case 'f': case 'F':
          exitPresent(); break;
      }
    });

    window.addEventListener('resize', () => {
      if (document.body.classList.contains('present-mode')) showSlide(current);
    });
  </script>
</body>
</html>
```

**Critical rules for slide HTML:**
- Every slide is `<section class="slide" data-slide="N">` with exactly 1920x1080 dimensions
- Use Tailwind utility classes exclusively for styling (flex, grid, gradients, shadows, rounded corners, padding, text sizes)
- Use theme colours via `text-primary`, `bg-accent`, etc.
- Use `font-heading` for headlines, `font-body` for body text
- Decorative elements: CSS gradients (`bg-linear-to-br` NOT `bg-gradient-to-br` — renamed in v4), Tailwind-styled divs as shapes, SVG icons inline
- No external images unless the user provides URLs
- Text sizes should be LARGE -- this is a presentation, not a webpage. Headings: `text-6xl` to `text-8xl`. Body: `text-2xl` to `text-3xl`
- Generous whitespace -- use `p-16`, `p-20`, `gap-12`, etc.

### Step 5: Screenshot & Export (Optional)

If the user wants PNGs or PPTX:

**Screenshot all slides:**
```bash
cd ~/.claude/skills/web-slides/references && uv run python render_slides.py /absolute/path/to/slides.html /absolute/path/to/output-dir/
```

This creates `slide-01.png`, `slide-02.png`, etc. at 1920x1080.

**Assemble PPTX (if requested):**
```bash
python3 ~/.claude/skills/web-slides/references/assemble_pptx.py /absolute/path/to/output-dir/ /absolute/path/to/slides.pptx
```

### Step 6: QA & Iterate

Open the HTML in the browser (use preview tools if available, or tell the user to open it).

Check:
- All slides render correctly at 1920x1080
- Fonts load (Google Fonts)
- Text is readable at presentation scale
- Colour theme is consistent
- If PNGs were generated, verify no rendering artifacts

Offer refinements:
- Swap layouts on individual slides
- Adjust theme colours or fonts
- Add/remove/reorder slides
- Re-export if changes were made

---

## Design Principles

1. **Generous scale** -- presentations are viewed from a distance. Oversized text, huge padding, bold colours
2. **One idea per slide** -- don't cram. If content is dense, split across slides
3. **Visual variety** -- alternate layouts. Don't use the same layout twice in a row
4. **Consistent theme** -- every slide uses the same colour palette and font pairing
5. **Clean hierarchy** -- headline dominates, supporting text is clearly secondary
6. **Subtle decoration** -- gradients, shapes, accent bars. Not clip art or stock photos
