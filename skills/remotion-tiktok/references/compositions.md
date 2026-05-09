# Remotion Composition Reference

Full source patterns for the two TikTok composition types.

---

## BlakeHartleyHook — Key Pattern

```tsx
// Duration: 60 (hook) + lines.length * 50 (body) + 70 (CTA)
export function blakeHartleyDuration(lineCount: number) {
  return 60 + lineCount * 50 + 70;
}

// Body lines animate in one at a time
// Each line uses localFrame = frame - (i * LINE_HOLD)
// Lines with quotes or CTAs get ICE colour accent
// Cover image fades out after hook scene (frames 40-70)
```

**Registration in Root.tsx:**
```tsx
<Composition
  id="BlakePost1-Example"
  component={BlakeHartleyHook}
  schema={BlakeHartleyHookSchema}
  durationInFrames={blakeHartleyDuration(5)}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{
    hookLine: "Hook line here — big and punchy",
    lines: [
      "Line one slides in",
      "Line two follows",
      "Line three",
      '"Quoted line gets ice blue colour"',
      "Final line before CTA",
    ],
    ctaLine: "Link in bio. Free. 18+",
    showCover: true,
  }}
/>
```

---

## BlakeMontage — Key Pattern

```tsx
// Duration: SLIDE_DURATION * slideCount + 90 (CTA card)
// SLIDE_DURATION = 120 frames (4 seconds)
// Ken Burns: scale interpolates 1.0 → 1.08 over durationInFrames
// Quote text fades up after FADE_DURATION (20 frames)
// Cross-fade between slides over FADE_DURATION frames
```

**Registration in Root.tsx:**
```tsx
<Composition
  id="BlakeMontage"
  component={BlakeMontage}
  durationInFrames={120 * 3 + 90}  // 3 slides + CTA
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{}}
/>
```

**Slide sequence in BlakeMontage.tsx:**
```tsx
<Series>
  <Series.Sequence durationInFrames={SLIDE_DURATION}>
    <Slide image="image1.png" quote="Quote for slide 1" />
  </Series.Sequence>
  <Series.Sequence durationInFrames={SLIDE_DURATION}>
    <Slide image="image2.png" quote="Quote for slide 2" />
  </Series.Sequence>
  <Series.Sequence durationInFrames={SLIDE_DURATION}>
    <Slide image="image3.png" quote="Quote for slide 3" isLast />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <CtaCard />
  </Series.Sequence>
</Series>
```

---

## Text Positioning Rules

**CRITICAL — TikTok UI covers bottom ~300-400px:**

```tsx
// Quotes: position in top 60% — use paddingTop, not bottom alignment
style={{ paddingTop: 300, justifyContent: "flex-start" }}

// CTA buttons: bottom padding minimum 400px (not 180px)
style={{ paddingBottom: 400 }}

// Pen name badge: top 80px padding — always safe
style={{ padding: "80px 60px 0" }}
```

---

## Colours by Pen Name

```
Blake Hartley:  ICE=#4FC3F7  DARK=#0A0A0C  MUTED=#9A9AA0
Luca Marchetti: Use Ferrari red + dark — TBD
Sable Voss:     Deep crimson + near-black — TBD
Dotty Pemberton: Warm cream + forest green — TBD
```

---

## Common Issues

**Image not showing:** Check file is in `public/` and referenced as `staticFile('filename.png')` not a path

**Text too low:** TikTok covers bottom — move all text to top 60%, increase paddingBottom on CTAs to 400px+

**Video too dark:** Reduce overlay opacity from 0.85 to 0.65 on the gradient

**Ken Burns not visible:** Check interpolation range — 1.0 to 1.08 minimum, can go to 1.12 for more movement

**TypeScript error on durationInFrames:** Must be an integer — use `Math.round()` if calculating dynamically
