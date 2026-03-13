---
name: skillpoint
description: Creates visually bold, colourful, professionally styled PowerPoint presentations (.pptx files) specialising in books, journals, KDP pitches, and publishing concepts. Use this skill whenever Wayne says "create slides for", "make slides about", "build a deck for", "presentation on", or any variation of wanting a PowerPoint about a book, journal, KDP idea, children's book series, publishing pitch, or any topic. Also trigger when Wayne says things like "slides for my book idea", "pitch deck for [title]", "deck about [topic]", or "can you make a presentation about X". Always use this skill rather than answering casually — it produces a proper styled .pptx file every time.
---

# SkillPoint

You are building a visually striking PowerPoint presentation for Wayne. Wayne's #1 complaint is that decks look plain and boring. Your job is to produce something that looks like a professional designer made it — rich colours, bold layouts, visual variety slide to slide.

**Do NOT use Pandoc or the pptx-pro html_to_pptx path.** That produces plain output. Instead, write a Python script using python-pptx directly so you have full control over every visual element.

## Output location

Save the final .pptx to `/sessions/keen-upbeat-clarke/mnt/outputs/<topic-name>.pptx`

---

## Step 1 — Choose a colour palette

Pick one of these palettes based on the topic mood, or invent one that fits:

| Palette | Primary | Accent | Background | Text |
|---|---|---|---|---|
| **Navy Gold** (premium) | #1B2A4A | #C9A84C | #F5F0E8 | #1B2A4A |
| **Coral Modern** (warm) | #E8593A | #2C2C2C | #FDF6F0 | #2C2C2C |
| **Forest Fresh** (natural) | #2D6A4F | #F4C542 | #F9F7F0 | #2D6A4F |
| **Purple Creative** (imaginative) | #5B2D8E | #E8A838 | #FAF5FF | #2C1A3E |
| **Slate Teal** (modern clean) | #1F3A4A | #2ABFBF | #F0F7F7 | #1F3A4A |

For journaling/KDP topics: Navy Gold or Purple Creative work beautifully.

---

## Step 2 — Plan the slides

7–9 slides. Each slide has ONE job. For a book/journal KDP pitch:

1. **Hero** — big bold title, tagline, full colour background
2. **Book Mockup** — realistic layered book cover simulation (see Book Mockup Slide section below)
3. **The Big Idea** — one sentence concept, large type
4. **Who It's For** — audience description, maybe 3 short bullet points max
5. **Why It Works** — 2–3 compelling reasons, visual icons or bold numbers
6. **What's Inside** — section/chapter overview, clean grid or list
7. **The Opportunity** — market angle, KDP potential, series possibilities
8. **Next Steps / CTA** — clear action, contact, or what happens next

For general topic decks, skip the Book Mockup slide and adapt the rest freely.

---

## Step 3 — Build with python-pptx (full visual control)

Write a Python script. Here is the exact visual recipe to follow:

### Slide types to alternate between:

**TYPE A — Full colour hero slide** (use for slide 1, section breaks, CTA)
```
- Entire background filled with PRIMARY colour
- Title: white, bold, 44–52pt, centred, positioned upper-centre
- Subtitle/tagline: white or ACCENT colour, 22–26pt, centred below title
- Optional: thin ACCENT colour horizontal bar (height 0.08 inches) near bottom
```

**TYPE B — Split layout slide** (use for concept, opportunity, next steps)
```
- Left 40% of slide: PRIMARY colour solid fill rectangle
- Right 60%: white/light background
- Heading on left panel: white, bold, 28–34pt
- Body content on right panel: dark text, 18–22pt, short punchy lines
- Optional accent line or small coloured rectangle as visual anchor
```

**TYPE C — Clean content slide** (use for lists, what's inside, who it's for)
```
- White or very light background (use the palette's Background colour)
- Bold heading bar at top: PRIMARY colour rectangle full width, height 1.0–1.2 inches
- Heading text in bar: white, bold, 30–36pt
- Content below: dark text, 18–20pt, max 5 short bullet points
- Left accent strip: thin PRIMARY colour rectangle on far left edge (0.1 inches wide, full height)
```

**TYPE D — Big statement slide** (use for "The Big Idea", key stats)
```
- Light background
- One large statement: PRIMARY colour text, bold, 36–44pt, centred
- Small supporting line below: grey, 18pt
- Optional: large ACCENT colour circle or rectangle as background shape behind text
```

### Python-pptx implementation notes:
- Widescreen slides: `prs.slide_width = Inches(13.33)`, `prs.slide_height = Inches(7.5)`
- Solid background fill: use `slide.background.fill.solid()` then set `fore_color.rgb`
- Add rectangles: `slide.shapes.add_shape(MSO_SHAPE_TYPE.RECTANGLE, left, top, width, height)`
- Set fill: `shape.fill.solid()`, `shape.fill.fore_color.rgb = RGBColor(...)`
- Remove border: `shape.line.fill.background()`
- Text boxes: `slide.shapes.add_textbox(left, top, width, height)`
- Bold + font size: `run.font.bold = True`, `run.font.size = Pt(44)`
- Font colour: `run.font.color.rgb = RGBColor(255, 255, 255)`
- Use `from pptx.util import Inches, Pt`, `from pptx.dml.color import RGBColor`, `from pptx.enum.text import PP_ALIGN`

---

## Step 4 — Content quality

- Titles: punchy, 4–7 words max
- Body text: short sentences, never full paragraphs on a slide
- Use bold numbers or short stats where possible ("3 reasons", "10 prompts per section")
- Each slide should feel like it could stand alone as a poster

---

## Step 5 — Verify and present

After saving, confirm the file exists with `os.path.getsize()` and share a `computer://` download link with Wayne.

---

## Book Mockup Slide (for KDP/journal/book pitches)

This is a signature slide that makes a book pitch deck look instantly professional. Build it entirely with python-pptx shapes — no images needed.

The goal is to simulate a physical book sitting on a surface, using layered rectangles to create depth and shadow.

### How to build the book mockup with python-pptx:

```
Slide background: dark (use PRIMARY colour or very dark grey #1A1A2E)

Layer 1 — Book shadow (bottom-most, slightly offset right and down):
  - Rectangle, slightly larger than the book
  - Fill: very dark grey #111111, no border
  - Position: book position + 0.15" right, + 0.15" down

Layer 2 — Book spine (left edge of book):
  - Thin tall rectangle (~0.35" wide, full book height)
  - Fill: darker shade of PRIMARY colour
  - Positioned at left edge of book

Layer 3 — Book cover (main face):
  - Large rectangle (~4.5" wide x 6" tall), centred slightly right of middle
  - Fill: your chosen ACCENT or a rich complementary colour
  - No border

Layer 4 — Cover title text box (on top of cover rectangle):
  - Book title: white, bold, 28–34pt, centred on cover
  - Subtitle or author: white or light gold, 16–18pt, below title

Layer 5 — Top edge highlight (page stack illusion):
  - Very thin rectangle (~0.08" tall) at top of book
  - Fill: light cream/white #F5F0E8 — simulates page edges

Layer 6 — Right edge highlight:
  - Very thin rectangle (~0.08" wide) on right side of book
  - Fill: same cream — simulates page edges on right side

Layer 7 — Accent bar or decorative element on cover:
  - Small ACCENT colour rectangle near bottom of cover (like a publisher band)
  - Optional: small text "KDP Edition" or series name in 12pt
```

Position the whole book assembly left-of-centre, and add a bold text callout on the right side:
- Big title of the book in PRIMARY colour, 36–44pt
- One line tagline below it
- Small "Available on Amazon KDP" badge (just a small rounded rectangle with text)

This creates a slide that looks like a product showcase — far more impressive than a plain title slide.
