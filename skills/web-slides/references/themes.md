# Built-in Themes (Tailwind v4)

Each theme provides colours, Google Fonts, and a Tailwind v4 `@theme` snippet.

**CDN:** `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>`

Theme colours go in `<style type="text/tailwindcss">@theme { ... }</style>`.

**v4 gradient note:** Use `bg-linear-to-br` (NOT `bg-gradient-to-br` — renamed in v4).

---

## Midnight

Dark corporate. Confident, modern, authoritative.

| Role | Hex | Use |
|------|-----|-----|
| primary | #1E2761 | Headlines, key elements |
| secondary | #CADCFC | Body text on dark backgrounds |
| accent | #408EC6 | CTAs, highlights, accent bars |
| surface | #0F1B3D | Slide backgrounds |
| text | #F0F4FF | General text |

**Fonts:** Inter (heading + body)

```html
<style type="text/tailwindcss">
  @theme {
    --color-primary: #1E2761;
    --color-secondary: #CADCFC;
    --color-accent: #408EC6;
    --color-surface: #0F1B3D;
    --color-text: #F0F4FF;
    --font-heading: 'Inter', sans-serif;
    --font-body: 'Inter', sans-serif;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

---

## Forest

Natural, earthy, trustworthy. Great for sustainability, health, education.

| Role | Hex | Use |
|------|-----|-----|
| primary | #2C5F2D | Headlines, key elements |
| secondary | #97BC62 | Supporting text, accents |
| accent | #F5F5F5 | Cards, callout backgrounds |
| surface | #1A3A1C | Slide backgrounds |
| text | #EAEFE8 | General text |

**Fonts:** Playfair Display (heading), Source Sans 3 (body)

```html
<style type="text/tailwindcss">
  @theme {
    --color-primary: #2C5F2D;
    --color-secondary: #97BC62;
    --color-accent: #F5F5F5;
    --color-surface: #1A3A1C;
    --color-text: #EAEFE8;
    --font-heading: 'Playfair Display', serif;
    --font-body: 'Source Sans 3', sans-serif;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Coral

Bold, energetic, attention-grabbing. Great for startups, creative pitches, marketing.

| Role | Hex | Use |
|------|-----|-----|
| primary | #F96167 | Headlines, key elements |
| secondary | #F9E795 | Supporting accents, highlights |
| accent | #2F3C7E | Contrast elements, dark text |
| surface | #FFFFFF | Slide backgrounds |
| text | #1A1A2E | General text |

**Fonts:** Poppins (heading), Inter (body)

```html
<style type="text/tailwindcss">
  @theme {
    --color-primary: #F96167;
    --color-secondary: #F9E795;
    --color-accent: #2F3C7E;
    --color-surface: #FFFFFF;
    --color-text: #1A1A2E;
    --font-heading: 'Poppins', sans-serif;
    --font-body: 'Inter', sans-serif;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Charcoal

Clean, minimal, professional. Works for any corporate or technical content.

| Role | Hex | Use |
|------|-----|-----|
| primary | #36454F | Headlines, key elements |
| secondary | #7A8B99 | Supporting text, subtle elements |
| accent | #E8491D | CTAs, highlights, data callouts |
| surface | #FFFFFF | Slide backgrounds |
| text | #212121 | General text |

**Fonts:** DM Sans (heading), Inter (body)

```html
<style type="text/tailwindcss">
  @theme {
    --color-primary: #36454F;
    --color-secondary: #7A8B99;
    --color-accent: #E8491D;
    --color-surface: #FFFFFF;
    --color-text: #212121;
    --font-heading: 'DM Sans', sans-serif;
    --font-body: 'Inter', sans-serif;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Galaxy

Dark, creative, expressive. Great for tech, design, creative agencies.

| Role | Hex | Use |
|------|-----|-----|
| primary | #A490C2 | Headlines, key elements |
| secondary | #E6E6FA | Body text, supporting elements |
| accent | #7B5EA7 | CTAs, gradients, highlights |
| surface | #1A1128 | Slide backgrounds |
| text | #E8E0F0 | General text |

**Fonts:** Space Grotesk (heading), Inter (body)

```html
<style type="text/tailwindcss">
  @theme {
    --color-primary: #A490C2;
    --color-secondary: #E6E6FA;
    --color-accent: #7B5EA7;
    --color-surface: #1A1128;
    --color-text: #E8E0F0;
    --font-heading: 'Space Grotesk', sans-serif;
    --font-body: 'Inter', sans-serif;
  }
</style>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```
