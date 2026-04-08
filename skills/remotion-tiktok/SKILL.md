---
name: remotion-tiktok
description: This skill should be used when the user asks to "make a TikTok video", "create a Remotion video", "render a TikTok", "do a montage video", "make a hook video", "build a TikTok for [pen name]", "do us a video", or wants to create short-form video content for romance pen names using Remotion. Covers both text hook videos and image montage videos for BookTok marketing.
---

# Remotion TikTok Video Builder

Build and render TikTok video assets using Remotion for romance pen name marketing. Two video types: text hook videos (line-by-line reveal on dark background) and image montages (Ken Burns slideshow with quote overlays).

---

## Project Location

Remotion project lives at `~/Claude/Remotion/demo/`:

```
~/Claude/Remotion/demo/
├── src/
│   ├── Root.tsx              ← register all compositions here
│   ├── BlakeHartleyHook.tsx  ← text hook template
│   ├── BlakeMontage.tsx      ← image montage template
│   └── index.ts
└── public/                   ← images go here before rendering
```

Output: `~/Desktop/[pen-name]-tiktok-videos/`

---

## TikTok Format

- **Resolution:** 1080x1920 (9:16 portrait)
- **FPS:** 30
- **Audio:** None — user adds trending sound in TikTok app
- **Critical:** Keep all text in the **top 60% of frame** — TikTok UI (likes, comments, share, caption) covers the bottom 300-400px

---

## Video Type 1: Text Hook (BlakeHartleyHook)

Line-by-line text reveal on dark background with optional cover image. Good for quote posts, POV hooks, direct CTAs.

**Props:**
```tsx
{
  hookLine: string,    // Big hook — displays alone for 2 seconds
  lines: string[],    // Body lines — each animates in and stays
  ctaLine: string,    // Final CTA button
  showCover: boolean  // true = cover image fades in behind hook
}
```

**Duration formula:** `60 + (lines.length × 50) + 70` frames

**To create a new text video:**
1. Add a new `<Composition>` block in `Root.tsx` with a unique `id`
2. Use `BlakeHartleyHook` as the component
3. Pass the hook, lines, and CTA as `defaultProps`
4. Set `durationInFrames` using `blakeHartleyDuration(lines.length)`

---

## Video Type 2: Image Montage (BlakeMontage)

Sequence of illustrated images with Ken Burns zoom and quote text overlays. Ends on a CTA card. Good for story moment posts and character reveals.

**Slide format:** `{ image: 'filename.png', quote: 'overlay text', isLast?: boolean }`

**Duration:** `(SLIDE_DURATION × slideCount) + 90` frames (each slide = 120 frames / 4 seconds)

**Ken Burns:** Scale 1.0 → 1.08 over slide duration — always include for algorithm reach

**To create a new montage:**
1. Generate images with Gemini (`mcp__gemini__gemini_generate_image`, aspect_ratio: `2:3`)
2. Copy images to `~/Claude/Remotion/demo/public/`
3. Create a new composition file (copy BlakeMontage.tsx pattern)
4. Register in Root.tsx
5. Render

---

## Colours

| Pen Name | Accent | Background |
|---|---|---|
| Blake Hartley | `#4FC3F7` (ice blue) | `#0A0A0C` |
| New pen name | Match their brand colours | `#0A0A0C` default |

---

## Image Pipeline

```bash
# 1. Generate with Gemini — always 2:3 aspect ratio for TikTok/Pinterest
# Style: "Illustrated cel-shaded, anime-influenced, pastel tones, 2:3 vertical"
# Save to Desktop/[pen-name]-pins/

# 2. Copy to Remotion public folder
cp ~/Desktop/[pen-name]-pins/image.png ~/Claude/Remotion/demo/public/image.png

# 3. Reference in composition as: staticFile('image.png')
```

Cover image source: `authors/[pen-name]/marketing/newsletter/deploy/cover.png`

---

## Render Commands

```bash
cd ~/Claude/Remotion/demo

# Single composition
npx remotion render src/index.ts [CompositionId] ~/Desktop/[pen-name]-tiktok-videos/[name].mp4

# Check available compositions
npx remotion compositions src/index.ts
```

---

## Posting Strategy

- **Max 2 videos per day**, 4-5 hours apart
- **Morning UK** (8-9am) hits US overnight feeds — best slot
- **Add trending audio** in TikTok app after upload — never bake audio into render
- **Key metric:** Saves (favourites) — better signal than likes, indicates warm leads
- **Comments beat likes** for algorithm — design hooks that spark Jake vs Ethan debates

**Conversion benchmarks:**
- 1,000 views → 10-20 clicks → 2-5 signups
- 10,000 views → 100-200 clicks → 20-50 signups
- Need one video to hit 5-10k before meaningful signups

---

## New Pen Name Setup

1. Create `[PenName]Hook.tsx` — copy BlakeHartleyHook, update colours and font
2. Create `[PenName]Montage.tsx` — copy BlakeMontage, update colours
3. Register both in `Root.tsx`
4. Copy cover image to `public/`
5. Create output folder: `~/Desktop/[pen-name]-tiktok-videos/`

---

## Additional Resources

- **`references/compositions.md`** — Full source for BlakeHartleyHook and BlakeMontage compositions
- **`references/posting-guide.md`** — TikTok posting strategy, captions, hashtags, timing
