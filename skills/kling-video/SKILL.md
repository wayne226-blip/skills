---
name: kling-video
description: Write Kling 3.0 image-to-video prompts and configure UI options for hero reels, content-creator wedge content, and motion tests. Use when the user asks for a "kling prompt", "kling video", "i2v", "image to video", wants to animate a still, or is testing motion mechanics on a creator persona. Also triggers when discussing reel production for Wren Rivers, content-creator wedge motion, or any pre-launch motion validation. Defaults to image-to-video on a single source still; for text-to-video or multi-shot narratives, adapt the structure but follow the same prompt rules.
---

## What You're Doing

Kling 3.0 is the current Kling model (released Q1 2026). It accepts a source image (i2v) and a text prompt, plus structured UI chips for camera framing, motion intensity, and identity binding. The output is a 5-15 second video clip at up to 4K (paid tier).

Kling 3.0 is **fundamentally different** from older Kling versions in that:
- It treats the source image as an **anchor** — describe how the scene EVOLVES, not what's already in it
- It rewards **cinematic intent** over visual description
- It penalises **scene re-description** (you'll get warped output if you fight the source image)
- It supports **multi-shot narratives** via `Shot 1: / Cut to:` syntax
- It has explicit **identity binding** ("Bind elements to enhance consistency") for character LoRA-style face hold

---

## The Prompt Formula

**Camera Movement + Subject Action + Vibe/Lighting + (optional) Time/Audio**

20-50 words total. Anything longer dilutes the signal; shorter starves the model.

### What to include

1. **Camera Movement** — explicit, cinematic. "Static medium shot, no camera movement" / "slow dolly push toward subject" / "handheld whip-pan to the left" / "shoulder-cam drift". Generic "moves" is wasted tokens.
2. **Subject Action** — the EVOLUTION from the source still. Use strong active verbs. Sequence multiple actions if needed: "She breathes once, eyes blink softly, then mouth corner lifts."
3. **Hand anchoring** — never let hands move freely in air. Always tie to an object or surface. "Fingers grip the cup", "hands rest on knees", "left hand braces against the doorframe".
4. **Vibe/Lighting reinforcement** — only if you want to fight the source's default. Kling defaults to commercial-polish; "candid handheld iPhone, ambient daylight only, no studio lighting, no commercial polish" is the standard anti-glamour clause.
5. **Background hold** (optional) — "background completely still" if you want a locked plate.

### What NOT to include

- **Don't re-describe what's already in the image.** The image carries setting, wardrobe, lighting, identity. Re-describing causes warping.
- **Don't use generic motion verbs** — "moves", "goes", "does". Always specific cinematographic language.
- **Don't put POV/hooks in the prompt** — it's not a TikTok caption, it's a director's instruction.
- **Don't pile on adjectives** — Kling 3.0 picks up nuance from precise verbs, not stacked adjectives.

---

## UI Configuration (Kling 3.0 web app)

Source upload + prompt is half the work. The structured UI chips matter:

| UI Element | Purpose | Default for typical creator wedge |
|---|---|---|
| **Image upload (left)** | The anchor still | Always 9:16 (1080x1920) for IG reels — crop the source first |
| **Add end frame (right)** | Optional second image for a directed transition | Leave blank unless doing a deliberate before/after |
| **Bind elements to enhance consistency** | Locks character/object identity across all frames | **ON** for any creator content where face must stay the same |
| **Camera shot chip** (Close-up / Medium / Long / Low Angle / etc.) | Forces a framing transformation OR maintains current framing | Pick the one that **matches the source framing** to keep it static. Picking a different one forces a zoom/pan during the clip |
| **Profile shot / Front view chip** | Forces angle change during clip | Match the source angle. Don't pick a different one unless you want the camera to rotate |
| **Multi-Shot toggle** | Enables `Shot 1: / Cut to:` syntax for editorial cuts | OFF for single-clip creator content. ON only for narrative reels with deliberate cuts |
| **Mode (Standard / Pro)** | Quality/credit tradeoff | Standard for testing + daily content, Pro for hero/launch-day reels |
| **Duration (5s / 10s / 15s)** | Length | 10s for hero wedge content (algo bias), 5s for B-roll. 15s only if test-validated |
| **Motion intensity (0.1-1.0)** | How aggressive the motion is | 0.2-0.3 for breath/blink/static-pose tests, 0.5-0.7 for active flows, 0.8+ rarely (sport/action only) |

### The framing rule (most-missed)

The camera shot chip **isn't** describing the source — it's describing what Kling should DO during the clip. If your source is a medium shot and you pick "Close-up", Kling will zoom in over the 10s. To keep framing static, **pick the chip that matches the source**.

**Validated 26 Apr 2026 (Wren v4 step 500 test):** picking "Close-up" on a medium-shot source produced an aggressive zoom-in, and combined with default motion intensity made the whole clip feel "too much" even though the underlying motion description was minimal. **Always match the chip to the source unless cinematic motion is intended.**

### The motion intensity rule

Default motion intensity in Kling 3.0 is around 0.5 — that's tuned for "average" content with talking + walking + gestures. For micro-motion (breath, blink, head tilt), 0.5 over-amplifies everything: chest pumps unnaturally, head sways too fast, hair moves like there's wind.

**Calibration table:**

| Test goal | Motion intensity |
|---|---|
| Static portrait with breath/blink only | 0.1-0.2 |
| Reformer flow / pour / sit-to-stand | 0.3-0.4 |
| Walking, casual gesture, hair drift | 0.5 (default) |
| Active sport, dance, vigorous motion | 0.7-0.9 |
| Anything ≥0.8 | rare, test first |

**Rule of thumb:** if the prompt is "barely-there X" or "subtle Y", motion intensity must be ≤0.3. Otherwise the model interprets the verb correctly but the slider amplifies it past natural.

### The activewear / exposed-torso rule

When the source has the model in a **sports bra, swimwear, or any garment that exposes the ribcage / midriff**, breath instructions become dangerous. Even at intensity 0.2, "barely-there breath" produces visible ribcage flex which reads as unnatural — humans don't show breath that obviously through skin.

**Rule:** with exposed-torso sources, drop breath from the prompt entirely AND add an explicit negative: "Torso completely still, no breathing visible." Motion lives only in the face (blink, smile, head tilt) and hands.

Validated 26 Apr 2026 (Wren v4 attempt 2): medium-shot framing + intensity 0.2 + "barely-there breath" still produced visible ribcage motion in a sports-bra source. Fix moved to attempt 3 by killing breath entirely.

This rule does **not** apply to fully-clothed sources — t-shirt / sweater / dress / oversized hoodie sources can carry breath at 0.2 because the garment dampens the visible motion.

### Source rendering for Kling (per `project_social_output_floor_2048.md`)

Source rendering is single-stage now — Z-Image Turbo at 2048x2560 native renders in ~8-12s on a 5070 Ti. No need for a separate "cheap iteration" path; iteration source = production source.

| Use | Source render |
|---|---|
| **Standard Kling test / daily wedge** | Z-Image Turbo native 2048x2560 + character LoRA @ 1.15, 8 steps, shift 3.0, dpmpp_sde+beta. Crop centre 9:16 → 1440x2560. ~8-12s on 5070 Ti. |
| **Hero / launch reel** | Same as above, then optional Ultimate SD Upscale 2x → 4096x5120 (Turbo kernel, 8 steps, denoise 0.25, LoRA 1.15). Crop 9:16 → 2880x5120. ~75-110s total. |

**Don't use SeedVR2** — dropped 25 Apr 2026 per `project_social_output_floor_2048.md` (painterly skin at zoom). Don't add it to the source pipeline.

**Don't render iteration source at 1024 + LANCZOS crop** — that's what we did pre-25-Apr and the cross-eye + skin artifact failure mode hit hard. The 2K native render at ~10s/shot makes the "cheap iteration" path obsolete.

Validated 26 Apr 2026 (Wren v4 — 4 attempts on a cheap 1024 source surfaced source-quality issues that masked prompt iteration signal). Lesson: render at production quality from attempt 1.

### The "static-but-alive" trick

When you've killed breath (per the activewear rule) and the result reads as **a still photo with eyes open**, you need to add life signals that don't touch the torso. Two safe additions:

1. **Smile evolution** — "her smile grows from small to genuinely warm across the clip." Kling's most reliable face-only motion. Reads as "real moment captured" instantly. Always add this when face is the subject and breath is forbidden.
2. **Hair drift** — "her hair drifts gently in the airflow / breeze". Low compute, no anatomy risk, adds the "alive" signal. Pair with a plausible airflow source (open window, fan, breeze) so it doesn't read as defying physics.

Validated 26 Apr 2026 (Wren v4 attempt 3): static medium shot + intensity 0.2 + breath-killed produced a clip that Wayne read as "static." Attempt 4 adds smile-evolution + hair drift to fix without re-introducing torso motion.

**Avoid as life signals (bring back the ribcage problem):**
- Shoulder shifts
- Posture redistribution
- Anything described as "settling" or "relaxing into" — Kling interprets these as torso animation

### Source quality IS result quality

Kling cannot fix defects in the source image — it animates whatever it's given. Common source defects that Kling preserves:

- **Cross-eyes / boss-eyes** — frame-1 eye drift carries through the entire clip. Caused by skipping FaceDetailer in the source render.
- **Skin artifacts / noise / compression bands** — Kling animates every pixel including noise. Caused by using Turbo render (distilled, fewer steps = less skin texture convergence) instead of Base, or by soft-upscaling artifacts up. Fix: Z-Image Base at 30 steps + FaceUp post-chain.
- **Soft / low-res** — fake-upscale (LANCZOS, basic ESRGAN) produces a video that reads soft. Kling can't sharpen its anchor. Fix: render at 2048 native via Z-Image Turbo (~10s on 5070 Ti), then optional Ultimate SD 2x → 4K for hero work. Do NOT use SeedVR2 (deprecated 25 Apr).
- **Plastic skin / airbrushed** — the artifact stays animated. Fix: Portra grade or skin-detailer LoRA at low strength in the source render.
- **Anatomy errors** (extra fingers, weird proportions) — preserved.

**Rule:** budget quality investment in the source render, never in Kling prompt tweaks. Per memory `project_social_output_floor_2048.md` (25 Apr 2026 — supersedes the older 23 Apr RECIPES.md):

**Default Kling source (creator wedge content):**
1. **Z-Image Turbo NATIVE at 2048x2560** + character LoRA at 1.15 (cross-base drift)
2. Sampler dpmpp_sde + beta, cfg 0 (Turbo ignores), **8 steps, shift 3.0** (NOT 16 / 2.0 — those were tested and reverted 21 Apr per `feedback_zimage_turbo_sharpness.md`)
3. NO upscale stage — Turbo renders 2K cleanly in one pass (~8-12s on 5070 Ti)
4. Crop centre 9:16 from 2048x2560 → 1440x2560 → upload to Kling

**Hero/launch-reel source (when extra detail is worth it):**
1. Same Turbo 2048x2560 native render
2. Then Ultimate SD Upscale 2x to 4096x5120 (Turbo kernel, euler+simple, cfg 1.0, 8 steps, denoise 0.25, LoRA 1.15, ESRGAN 4x_NMKD-Siax_200k, tile 1024, seam fix Half Tile + Intersections)
3. Crop 9:16 → 2880x5120 → resize to upload size

**Cover/promo (highest fidelity, slowest):**
1. Z-Image Base at 2048x2560 + LoRA at 1.0 (shift=7, res_2s+beta, cfg 5.5, 30 steps)
2. Ultimate SD Upscale 2x to 4K
3. + FaceUp face-only pass for skin/eye detail
4. Cinematic grade

**SeedVR2 is NOT in the stack** — dropped 25 Apr 2026 (painterly/plastic skin at zoom across all variants tested). Don't add it.

**Validated 26 Apr 2026** (Wren v4 attempts 1-4): no Kling prompt formula compensated for a source rendered as raw 1024 Turbo + soft LANCZOS crop. The 2048 native render is the floor for creator content; cover lane is only needed for hero work where the extra 4K detail earns its time.

---

## Identity Binding for Creator Content

When working with a character LoRA-rendered source (e.g. content creator persona):

1. **Bind elements: ON** — non-negotiable. Without it, face drifts within 3-5s.
2. **Source still must be a clear, well-lit face** — Kling can only bind what it can see. Side-profile or shadow sources produce weak binds.
3. **Don't change wardrobe in the prompt** — the source carries it. Mentioning a different outfit will cause garment warping.
4. **For multi-shot creator narratives** — upload the SAME source as anchor for each shot, even if you describe different scenes. Identity drifts more between shots than within them.

---

## Motion Mechanics — what Kling 3.0 does well vs badly

### Reliable (use freely)
- Breath, blink, micro-smile, slow head tilt
- Hand-to-object actions (gripping, lifting, pouring)
- Slow camera dolly toward/away from a static subject
- Hair drift in implied breeze (low amplitude)
- Steam, water surface ripples, fabric drift
- Walking with consistent stride (mid-distance shots)

### Unreliable (test before committing)
- Eye contact change (looking away → back)
- Multi-person interaction (faces stay clean ~5s, then drift)
- Fast motion (running, jumping, spinning)
- Hand gestures in empty space (always anchor)
- Leg motion when face is dominant in frame (anatomy contention)

### Don't even try
- Talking / lip-sync (text-to-speech-driven mouth shape)
- Swimming, dancing, complex sport motion
- Anything where the subject leaves the frame
- Multi-person with overlapping bodies

---

## The Eye-Coherence Canary

Per Wayne's pipeline rules: **eyes break first** in any AI motion model. Anatomy compute is hardest on faces. Whatever generator you're using, eyes are the gating criterion.

For any new Kling test on a creator face:
1. First test = breath/blink only on a face-prominent source. If eyes drift in 10s, don't ship 10s — drop to 5s or kill the source-face-prominent strategy.
2. Eyes drifting means hair-colour/skin-tone are also drifting, you just don't notice them as fast.
3. Pro tier sometimes holds eyes better than Standard — worth re-testing borderline Standard fails on Pro before giving up.

---

## Pricing & Credit Management (Q2 2026)

Kling subscription tiers (web only — API is a separate billing track, do NOT assume web credits cover API):

| Tier | $/mo | Credits | Use case |
|---|---|---|---|
| Standard | $7.99 | ~660 cr | Hobbyist / testing only |
| Standard one-month special | $27.99 | 3000 cr | **Wayne's current plan** — production volume |
| Pro | varies | varies | Hero/launch-day shots, post-test only |

Cost per render at Standard:
- 5s = 60 cr (~$0.56 at $27.99/3000)
- 10s = 120 cr (~$1.12)
- 15s = 180 cr (~$1.68)

Run an A/B of 3-5 versions per hero shot if budget allows; pick the best take. With 3000 cr/mo this allows 25 × 10s reels OR 16 × 15s.

---

## Prompt Templates

### Static face micro-motion (lowest-amplitude / safest test)
```
Static medium shot, no camera movement. She holds her gaze with a soft small smile, blinks once gently, head tilts a fraction to one side. Barely-there breath. Hands stay [resting on knees / on the counter / holding the cup]. Background completely still. Candid handheld iPhone feel, ambient daylight only, no commercial polish.
```
Pair with: motion intensity **0.2**, camera shot chip **matches source** (no zoom).

### Visible breath (use only when chest is the subject)
```
Static medium shot, no camera movement. She breathes once — chest rises and falls slowly. Eyes hold steady. Hands stay [anchor]. Background still. Candid handheld iPhone, ambient daylight only.
```
Pair with: motion intensity **0.3**. Avoid for portrait close-up framings where chest exits frame mid-clip.

### Slow flow (reformer / pilates / pour)
```
Static medium shot, no camera movement. She [executes the specific flow — e.g. "lowers her legs from the straps slowly toward the carriage"]. Hands grip the [object — e.g. "straps with steady tension"]. Hair drifts a fraction with the motion. Background still. Candid handheld iPhone, ambient daylight, no commercial polish.
```

### Dolly-in hero shot (cinematic)
```
Slow dolly push toward subject, ~10% closer over the clip. She holds her gaze with a small relaxed smile, breathes once, blinks softly. Hands [anchor]. Light shifts subtly with the camera move. Cinematic 35mm feel, natural daylight.
```

### Hands-and-object close-up (Wan-eligible content)
```
Static close-up on the hands, no camera movement. Her fingers [specific action — e.g. "wrap a bamboo whisk around the lip of a ceramic bowl, then sweep it through the matcha three times"]. Steam rises faintly. Background blurred. Candid iPhone close-up, ambient daylight.
```

### Multi-shot narrative (only with Multi-Shot ON)
```
Shot 1: [framing + action + lighting]. Cut to Shot 2: [framing + action + lighting]. Cut to Shot 3: [framing + action + lighting].
```

---

## Wayne-Specific Defaults

When working in the Wren Rivers workspace or any content-creator workspace:

- **Aspect:** 9:16 (1080x1920) source. Match output aspect to source. Always crop source to 9:16 BEFORE upload.
- **Wedge length:** 10s (locked per CLAUDE.md). Only drop to 5s if a 10s test fails the eye-coherence criterion.
- **Aesthetic clause:** always include "candid handheld iPhone feel, ambient daylight only, no commercial polish" or equivalent — Kling defaults to commercial-glossy and the wedge needs casual.
- **Bind elements:** always ON for creator content.
- **Mode:** Standard for tests + daily reels. Pro reserved for launch day if Standard's quality is borderline.
- **Hand anchoring:** if the source has visible hands, name where they go. If not in frame, omit hand instruction.

---

## Pre-Fire Checklist

Before clicking Generate, confirm:

- [ ] Source is 9:16 (1080x1920 or close)
- [ ] Source crop preserves the face / focal subject in centre
- [ ] Bind elements: ON (for creator content)
- [ ] Camera shot chip matches source framing (unless intentional motion)
- [ ] Multi-Shot OFF (unless deliberately scripting cuts)
- [ ] Prompt is 20-50 words
- [ ] Hands are anchored to a named object/surface
- [ ] No re-description of source content
- [ ] Anti-commercial language included
- [ ] Duration matches the wedge spec (10s default for hero)
- [ ] Mode = Standard for tests, Pro for launch hero

---

## Verdict Template (for motion tests)

After every Kling test, score the result on these criteria:

1. **Eye coherence** — anatomically correct across full clip, no drift / squint / asymmetry
2. **Identity hold** — same person from first to last frame
3. **Motion realism** — natural human, not animated
4. **Aesthetic match** — candid vs commercial-glossy
5. **Background coherence** — no warping
6. **Anatomy stability** — hands, limbs, body don't morph
7. **No artefacts** — no flicker, no AI smear

Pass = 7/7. Eye drift only = drop to 5s wedge. Multiple fails = re-render source or switch generator.

Save the verdict to `motion-tests/<date>/README.md` and write a memory entry if a new pattern emerges (`feedback_kling_<topic>.md`).
