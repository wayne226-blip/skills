---
name: lora-trainer
description: >
  End-to-end character LoRA training pipeline for Z-Image via ai-toolkit (Ostris).
  Locks the v4-validated workflow: Gemini Pro Edit dataset gen anchored to a keystone,
  Ostris-format captions (trigger + what-changes-only, no face descriptors),
  yaml spec (rank 16, 3000 steps, 1024 res, EMA on, adapter v2), WMI-detached launch
  that survives SSH drops, sample prompts in production format so identity convergence
  is visible mid-training. For content creators and book characters. Triggers on:
  "train a LoRA for [character]", "build [creator] LoRA", "/lora-train [name]",
  or after persona-anatomy is set up and the creator has no LoRA yet.
version: 2.0.0
metadata:
  author: calibre.ai
  category: image-pipeline
  platforms:
    - claude-code
---

# LoRA Trainer Skill — Z-Image / ai-toolkit (v2)

## Purpose

Train a face-locked Z-Image LoRA for any character (content creator or book character) using the validated 26 Apr 2026 pipeline. One workflow, multiple SCP-and-fire steps, one detached training run.

## When to Use

- New content creator needs a face-locked Z-Image LoRA (before first production render)
- Book character needs consistent cover art at 4K
- Retraining a v1/v2/v3 LoRA where identity didn't lock
- Cross-character LoRA work for any project on this machine

## What This Replaced (legacy reference)

This is v2 of the skill. **v1 used SDXL + OneTrainer + Gemini-anchor → 40 free-renders.** Deprecated 23 Apr 2026 when Z-Image became the locked model stack. Don't use OneTrainer / SDXL paths from old runbooks. If a memory file or doc references rank 64 / text encoder training / 5-hour training time / OneTrainer GUI, it's pre-23-Apr legacy.

## How "Z-Image De-Turbo" relates to our setup

The Ostris GUI now exposes **"Z-Image De-Turbo (De-Distilled)"** as a first-class model picker option. Functionally equivalent to what we already do via `arch: zimage` + `training_adapter_path: zimage_turbo_training_adapter_v2.safetensors`. The training adapter "de-distills" Z-Image Turbo during training so the LoRA learns the subject without breaking Turbo's distillation; at inference, removing the adapter leaves the new LoRA on top of distilled Turbo at distilled speeds.

Either path produces compatible LoRAs. We stick with the explicit yaml-based approach because it's reproducible and version-controlled.

## Hardware tier — VRAM-dependent settings (confirmed 26 Apr 2026 research)

| VRAM | Transformer | Text Encoder | low_vram | Notes |
|---|---|---|---|---|
| 24GB+ (RTX 4090 / 5090) | BF16 (no quant) | BF16 (no quant) | false | Full quality, fast |
| **16GB (5070 Ti — Wayne's box)** | **float8** | **float8** | **true** | **Our locked setting** |
| 12GB | float8 | float8 | true | Quantize both, may need lower res |

Set in the yaml under `model.qtype: qfloat8` + `model.low_vram: true` for the 16GB case.

## Knowledge sources — ALWAYS READ FIRST

In order:
1. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_lora_sample_prompts_use_persona.md` — sample prompt format (must use production format, NOT bare trigger)
2. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_persona_prefix_poisons_zimage_lora.md` — face descriptors must be stripped from inference prompts (carries through to caption rules)
3. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_two_identity_blocks_lora.md` — rich block for dataset gen, minimal block for inference
4. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_gemini_edit_dataset_for_lora.md` — Gemini Pro Edit dataset gen recipe (beats pure Z-base t2i)
5. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_detached_training_pattern.md` — WMI launcher + log mirror
6. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_adapter_v2_safe_in_comfyui.md` — Ostris adapter v2 is safe via ComfyUI
7. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_lora_dataset_95_face_match.md` — cull rule (face features 95% match, everything else varies)
8. `~/.claude/projects/-Users-wayne-calibre-hq/memory/feedback_lora_dataset_strip_makeup.md` — neutral face in dataset, glam at inference

## Prerequisites

Before running:

1. **Character keystone exists** — single locked face image, validated against same-seed montage + skin-stress test. If no keystone: build one via Z-Image Base candidate sweep + optional Gemini Pro Edit refinement.
2. **Two identity blocks defined in `custom_creators.json`:**
   - `identity` — minimal (~40 words, body + jewellery + posture, NO face/hair/skin tokens)
   - `identity_full_with_face` — rich (400-1000 chars, all face descriptors) — kept for PuLID-anchor mode only
3. **Tailscale SSH to PC** is live: `ssh wauzz@100.107.67.79 "echo ok"` (NOT the legacy `-p 2222 127.0.0.1` tunnel)
4. **PC has free VRAM** — close ComfyUI on PC during training (`Stop-Process -Id <comfy-pid>` if needed)
5. **GPU is idle** — training will hold ~14GB VRAM for ~2.5-4 hours

If any check fails, surface clearly and stop.

---

## Phase 1 — Lock the keystone

Generate or refine a single face that becomes the LoRA's identity anchor.

### Option A — Z-Image Base candidate sweep (preferred)

Render 20-50 candidates via Z-Image Base + rich identity block, sweep seeds, pick the one that:
- Reads as the locked persona on first glance
- Holds same-seed montage (same face on +1, +2, +3 seeds)
- Survives skin-stress test (close-up zoom shows real skin texture, no airbrush)

### Option B — Gemini Pro Edit refinement

If Z-Image Base candidates are close but missing a specific feature, use `gemini-3-pro-image-preview` to refine:
- Anchored to the best Z-Image candidate
- Edit prompt: "same woman, but [specific feature change]"
- Per `feedback_gemini_edit_dataset_for_lora.md` this is the validated path for AI personas

Save keystone to: `content-creators/<creator>/lora-training-v[N]/<creator>_v[N]_keystone.png`

**CONFIRM WITH WAYNE** before proceeding. Bad keystone = bad LoRA. The 30 min spent on keystone selection is the cheapest QA in the entire pipeline.

---

## Phase 2 — Generate dataset (Gemini Pro Edit anchored)

**Validated method:** `gemini-3-pro-image-preview` anchored to the locked keystone produces a face-consistent training dataset. Beats pure Z-Image t2i for AI persona LoRAs (no face drift across seeds).

### Dataset spec

| Shot type | Count | Notes |
|---|---|---|
| Head + shoulders front | 4-6 | Different expressions: neutral, soft smile, eyes closed, laughing |
| Three-quarter | 4-6 | Left + right, soft expression variation |
| Profile | 2-4 | Left + right |
| Upper body | 8-10 | Different outfits + light direction |
| Full body | 10-15 | Different settings, poses, framings |
| Detail | 2-4 | Hands, feet, hair detail |

Total target: **30-50 images**. More is not always better — quality > quantity. Cull aggressively in Phase 3.

### Gemini prompt pattern

```
Same woman as the reference image, [specific scene + framing + light + outfit], natural skin texture, no airbrushing
```

### Anti-patterns

- **No baked makeup** — neutral face in dataset, glam at inference (per `feedback_lora_dataset_strip_makeup.md`)
- **No named eyelashes** — they render painted-on after upscale (per `feedback_no_named_lashes.md`)
- **No "clear smooth skin" / "perfect"** — strips realism
- **No multi-person scenes** — face attribution gets confused

Save all to: `content-creators/<creator>/lora-training-v[N]/dataset-gemini/`

---

## Phase 3 — Cull + caption

### Cull rule (per `feedback_lora_dataset_95_face_match.md`)

Keep an image only if it passes the **"clearly the same woman"** test:

| Feature | Match level | Action if drifts |
|---|---|---|
| Face structure / bones | 95%+ | DROP |
| Eye shape + colour | 95%+ | DROP |
| Skin tone | 95%+ | DROP |
| Hair colour | 95%+ | DROP |
| Body frame | 95%+ | DROP |
| Expression | should vary | KEEP |
| Pose | should vary | KEEP |
| Outfit | should vary | KEEP |
| Lighting | should vary | KEEP |
| Background | should vary | KEEP |
| Framing | should vary | KEEP |

Aggressive cull: 50 candidates → 30 keepers is a healthy ratio.

### Caption format (Ostris convention)

For each kept image, write a `.txt` file with matching name. Format:

```
<trigger>, <what changes for THIS shot>
```

**Examples (Wren v4):**
```
<wren1>, cream cotton tank top, side profile facing camera left, head and shoulders, plain white studio backdrop, soft studio lighting

<wren1>, oversized white tee, leaning on pale wood kitchen counter holding a small ceramic matcha bowl, eyes lowered, soft warm morning window light from camera left

<wren1>, cream linen blouse and faded blue jeans, leaning over a wooden trestle table, golden-hour light through awnings
```

### What captions MUST NOT contain

- **Face/hair/skin descriptors** (per `feedback_persona_prefix_poisons_zimage_lora.md`) — those tokens corrupt Z-Image latent space when applied at inference
- **The literal name** ("Wren", "Wren Rivers") — risks the LoRA learning name-as-token vs face
- **Eyelash references** — see `feedback_no_named_lashes.md`
- **Filler words** — keep tight, ~20-50 tokens per caption

### What captions SHOULD contain

- Trigger word at start, always (or `[trigger]` placeholder if `trigger_word` is set in yaml — auto-replaced at training time)
- Outfit / wardrobe (because that varies per shot)
- Pose / framing / camera angle (because that varies)
- Lighting direction / quality (because that varies)
- Setting / background (because that varies)

### Caption attribute rule (from 2026 research)

The principle: **caption what VARIES, not what's CONSTANT.** The model learns "this varies → not part of identity" and "everything else stays → part of identity (the locked face)."

| Attribute | Caption it? | Why |
|---|---|---|
| Hair colour (single colour across dataset) | NO | Constant — would over-attribute. Face wins via absence. |
| Hair style (varies — up / down / wet / dry) | YES — describe the style only ("low bun", "wet from the surf") | Variable per shot |
| Eye colour | NO | Constant. Causes inference latent corruption (per `feedback_persona_prefix_poisons_zimage_lora.md`) |
| Skin tone | NO | Constant. Same poisoning risk. |
| Face shape / cheekbones / lips | NEVER | These are the LoRA's job; describing = teaching that they vary |
| Outfit | YES | Varies per shot |
| Lighting direction | YES | Varies per shot |
| Setting | YES | Varies per shot |
| Pose / framing | YES | Varies per shot |

Rule of thumb: if you imagine training on a dataset where ALL hair was the same colour and ALL outfits were the same, then captioning the hair colour overweights it as a "characteristic that needs describing" → at inference you get hair locked in even harder + face less locked. Don't.

---

## Phase 4 — SCP dataset to PC

```bash
# From Mac
scp -r ~/calibre-hq/content-creators/<creator>/lora-training-v[N]/dataset-gemini/ \
  wauzz@100.107.67.79:C:/Users/wauzz/ai-toolkit/datasets/<creator>_v[N]/

# Then check for .DS_Store and remove
ssh wauzz@100.107.67.79 'powershell -c "Get-ChildItem C:\Users\wauzz\ai-toolkit\datasets\<creator>_v[N] -Filter .DS_Store | Remove-Item"'

# Verify count: should equal (image count * 2) — one .png + one .txt per dataset image
ssh wauzz@100.107.67.79 'dir C:\Users\wauzz\ai-toolkit\datasets\<creator>_v[N] | findstr "File(s)"'
```

---

## Phase 5 — Write the yaml

### Locked spec (validated on Wren v4 26 Apr 2026)

| Field | Value | Why |
|---|---|---|
| `arch` | `zimage` | Z-Image base model |
| `training_adapter_path` | `zimage_turbo_training_adapter_v2.safetensors` | Adapter v2 safe in our ComfyUI path per `feedback_adapter_v2_safe_in_comfyui.md` |
| `quantize` | `true`, `qtype: qfloat8` | Fits 1024 res in 16GB |
| `low_vram` | `true` | Required for 1024 res + rank 16 in 16GB |
| `network.linear` | `16` | Rank — increase to 32 only if rank 16 fails identity hold |
| `network.linear_alpha` | `16` | Match rank |
| `train.steps` | `3000` | Step count for character LoRA |
| `train.lr` | `0.0001` | 1e-4 |
| `train.optimizer` | `adamw8bit` | |
| `train.dtype` | `bf16` | |
| `train.ema_config.use_ema` | `true` | Smooths late-training noise per Skye + Wren v4 lock |
| `train.ema_config.ema_decay` | `0.99` | |
| `train.gradient_checkpointing` | `true` | |
| `train.noise_scheduler` | `flowmatch` | |
| `dataset.resolution` | `[1024]` | Native Z-Image training res |
| `dataset.caption_dropout_rate` | `0.05` | |
| `dataset.shuffle_tokens` | `false` | |
| `dataset.cache_latents_to_disk` | `true` | First run caches; resumes are instant |
| `save.dtype` | `float16` | |
| `save.save_every` | `500` | Checkpoint cadence |
| `save.max_step_saves_to_keep` | `6` | Keep last 6 step-saves |
| `sample.sampler` | `flowmatch` | |
| `sample.sample_every` | `250` | Mid-training visibility |
| `sample.disable_sampling` | `false` | Enable mid-training samples |
| `sample.skip_first_sample` | `true` | Skip step-0 sample (no info) |
| `sample.guidance_scale` | `4.5` | Base-style sampling for samples (28 steps cfg 4.5). NOT Turbo-style 8 steps cfg 0 — that's the most common ai-toolkit Z-Image misconfiguration per 2026 research. |
| `sample.sample_steps` | `28` | |
| `sample.width` / `height` | `768` / `1024` | |

### Time Step Bias rule (Ostris-confirmed Mar 2026)

Per Ostris's own Z-Image Turbo training video — set `train.timestep_bias` based on what you're training:

| Training type | timestep_bias | Why |
|---|---|---|
| **Character LoRA (face/identity)** | `balanced` (default) | Need to learn at all noise levels — face features fire across the whole denoising trajectory |
| **Style LoRA (aesthetic transformation)** | **`high_noise_first`** | Style affects the early high-noise steps where composition is built. High-noise bias forces the LoRA to learn during the "what does this image start as" phase |

For Wren and any character LoRA: leave at default balanced. For a hypothetical "candid iPhone aesthetic" style LoRA: switch to high noise. Ostris himself swaps mid-run for style work in his demo (~step 2250 he flipped from balanced → high noise to fix the children's drawings convergence). You can change this between runs but mid-run requires kill+restart.

### Differential Guidance — advanced (Ostris-built feature)

Ostris built this directly into ai-toolkit (advanced section in GUI). Solves the "training averages out" problem where a LoRA never quite hits the keystone, just asymptotically closer.

**How it works:** Like CFG but for training. Computes the difference between current knowledge and target, amplifies it, adds it back. Each step overshoots the target slightly, then corrects on the next step. Net result: LoRA actually hits the target rather than approaching it.

**When to use:**
- Style LoRAs where the visual change is drastic (Ostris used it for his children's drawings demo at guidance_scale 3)
- Characters where the keystone is hard to bind (face nuance not converging by step 1500)
- Any training where you'd otherwise crank LR (which explodes the model — 2e-4 confirmed broken by Ostris)

**When NOT to use:**
- First training run on a new character — start standard, only add diff guidance if convergence stalls
- Very small datasets (under 15 images) — already over-fit risk

**Settings:**
- `train.diff_guidance.use_diff_guidance: true`
- `train.diff_guidance.guidance_scale: 3.0` (Ostris's demo value — start here)

**Caveat (direct quote from Ostris):** "It may not even function the way I think it does, but it does seem to work." Experimental — A/B against a standard run before committing to it as default.

### Caption philosophy — character vs style (Ostris-confirmed)

Two distinct caption rules depending on what you're training:

**Character LoRA (Wren, future creators):** caption what VARIES per shot, never the constant identity. Detailed rules in the "Caption attribute rule" section above.

**Style LoRA (e.g. "candid iPhone aesthetic" applied universally):** **don't caption the style itself**. Ostris's children's drawings example — every caption is a description of the IMAGE CONTENT (e.g. "a bear, a pig, a green balloon, an owl wearing suspenders") with NO mention of "children's drawing" or "crayon sketch" or "amateur art". The model learns "this is just how a bear is rendered now" because every image of a bear in the dataset looks like that style.

The principle is the same as our character rule, just inverted: caption what VARIES (the subject matter), don't caption what's CONSTANT (the style itself).

**Trigger word for style LoRAs:** Optional. Ostris doesn't use one for his children's drawings demo — "you apply the LoRA and this is just how it works." For character LoRAs we always use a trigger because we want the option to apply the character only on certain renders. For style LoRAs that are always-on, no trigger is fine.

### Trigger word

Use bracket pattern: `<creatorname>` or `<creatorname1>`. Examples: `<wren1>`, `<honey1>`, `<marlowe1>`. Single-token, collision-free with English vocab.

### Sample prompts — USE PRODUCTION FORMAT (critical)

**Per `feedback_lora_sample_prompts_use_persona.md` — bare-trigger samples give zero identity-convergence signal mid-training.** Use the production format:

```yaml
sample:
  prompts:
    - "{stripped_persona}, <trigger>, on a pilates reformer, cream tank, black leggings, studio daylight"
    - "{stripped_persona}, <trigger>, kitchen counter holding matcha, oversized tee, soft morning window light"
    - "{stripped_persona}, <trigger>, walking the beach with surfboard, black wetsuit, overcast"
    - "{stripped_persona}, <trigger>, head and shoulders portrait, cream backdrop, soft window light"
```

Replace `{stripped_persona}` with the character's actual minimal identity block from `custom_creators.json`. Same format `fire_v[N]_validation.py` uses.

This way step-250 / 500 / 750 / etc. samples actually show identity converging toward the keystone. Without this, you get garbage signal until step 2000+.

### Save the yaml

`tools/flux-pipeline/lora-training-workflows/<creator>_v[N]_zimage.yaml`

SCP to PC config dir:
```bash
scp <creator>_v[N]_zimage.yaml wauzz@100.107.67.79:C:/Users/wauzz/ai-toolkit/config/
```

---

## Phase 6 — Launch detached (WMI pattern)

**CRITICAL:** Don't use `ssh wauzz@PC "python run.py ..."` — SSH drops kill the python. Use the WMI launcher per `feedback_detached_training_pattern.md`.

### Setup launcher .bat (one-time per character)

```bat
@echo off
cd /d C:\Users\wauzz\ai-toolkit
call venv\Scripts\activate.bat
python run.py config/<creator>_v[N]_zimage.yaml > C:\Users\wauzz\ai-toolkit\output\<creator>_v[N]_zimage\detached.log 2>&1
```

**No `python -u`, no `PYTHONUNBUFFERED=1`** — costs 2.5x speed via synchronous flushes. Default block-buffering is fine.

SCP to PC: `C:\Users\wauzz\ai-toolkit\run_<creator>_v[N].bat`

### Launcher .ps1

```powershell
$result = ([wmiclass]'Win32_Process').Create('cmd /c C:\Users\wauzz\ai-toolkit\run_<creator>_v[N].bat', 'C:\Users\wauzz\ai-toolkit')
Write-Host "ProcessId: $($result.ProcessId)  ReturnValue: $($result.ReturnValue)"
```

SCP and fire:
```bash
ssh wauzz@100.107.67.79 'powershell -ExecutionPolicy Bypass -File C:\Users\wauzz\ai-toolkit\launch_detached.ps1'
```

### Mirror PC log to local for Studio visibility

```bash
nohup bash -c "ssh wauzz@100.107.67.79 'powershell -c \"Get-Content C:\Users\wauzz\ai-toolkit\output\<creator>_v[N]_zimage\detached.log -Wait\"' > /tmp/studio-training/<creator>_v[N]_zimage.log" > /tmp/log-mirror.log 2>&1 &
disown
```

Studio's `/api/training/ostris?job=<creator>_v[N]_zimage` reads from this local mirror.

### Power management

```bash
# Quiet bedroom mode (slightly slower, less heat / fan):
ssh wauzz@100.107.67.79 "nvidia-smi -pl 250"

# Stock (default 285W, full speed):
ssh wauzz@100.107.67.79 "nvidia-smi -pl 285"
```

---

## Phase 7 — Monitor training

### What to expect

- Step rate: ~4.3-4.7s/step on 5070 Ti at stock 285W, rank 16, res 1024
- Total wall time: ~3h 30min for 3000 steps (~75min if you can train at 512 res)
- Sample renders fire every 250 steps (4 samples per fire = ~30s pause)
- Checkpoint saves every 500 steps (~10 sec each, 85MB rank-16 file)

### Check status via Studio

`http://localhost:5050/next/train` — engine toggle to "Ostris", job dropdown to `<creator>_v[N]_zimage`. Shows current step, loss, sec/step, ETA, checkpoints saved, latest sample renders.

### Identity convergence trajectory (expected with production-format samples)

| Step | Expected sample state |
|---|---|
| 250 | Gender locked, body type locked, generic-looking face |
| 500 | Face structure starting to bind toward keystone |
| 1000 | Face clearly the right "type", hair colour may still be wrong |
| 1500 | Hair colour binding, full keystone match emerging |
| 2000 | Identity locked, mostly indistinguishable from keystone |
| 3000 | Final — should be production-grade |

If by step 1500 the face still reads as a generic Asian male in portraits or generic anything, training has failed — kill, investigate dataset/captions/persona block, restart.

### NEVER run inference on the same GPU during training

Per `feedback_detached_training_pattern.md` — VRAM thrashing tanks step rate ~5x. Don't run validation renders / Comfy queue jobs while training is active. Suspending training doesn't release CUDA memory; only kill does. Wait for completion or pause via kill + resume from latest checkpoint.

---

## Phase 8 — Score-test post-training

When the final `<creator>_v[N]_zimage.safetensors` lands (no `_<step>` suffix):

```bash
# Copy to ComfyUI loras dir
ssh wauzz@100.107.67.79 'copy "C:\Users\wauzz\ai-toolkit\output\<creator>_v[N]_zimage\<creator>_v[N]_zimage.safetensors" "C:\Users\wauzz\Documents\ComfyUI\models\loras\trained\"'

# Restart ComfyUI to register new LoRA (only needed for first deployment)
# Reset GPU power
ssh wauzz@100.107.67.79 "nvidia-smi -pl 285"

# Fire score-test (10 prompts × Base@1.00 + Turbo@1.15 = 20 renders)
cd content-creators/<creator>/lora-training-v[N]/score-test
python3 fire_v[N]_score_test.py <variant>
```

The `fire_v[N]_score_test.py` script template is at `content-creators/wren-rivers/lora-training-v4/score-test/fire_v4_score_test.py` — copy + adapt for new character.

### Pass criteria

For each of the 10 prompts × 2 backends (20 renders):

1. Identity holds across all 10 prompts (clearly same woman)
2. Scene types render correctly (no overfit to a single scene type like fitness)
3. Eyes natural, no painted-on lashes
4. Hair colour / eye colour / skin tone match keystone
5. Cross-backend consistency (Base @ 1.00 and Turbo @ 1.15 both produce keystone-true)

---

## Phase 9 — Deploy to production

If score-test passes:

1. Lock LoRA name in `tools/flux-pipeline/studio/config/custom_creators.json`:
   ```json
   "<creator>": {
     "lora_name": "trained\\<creator>_v[N]_zimage.safetensors",
     "lora_strength_base": 1.00,
     "lora_strength_turbo": 1.15,
     ...
   }
   ```
2. Update persona.md to reference v[N] LoRA
3. Archive previous version in `_archive/<creator>-v[N-1]/`
4. Test 5 production renders via Studio's Single Render or character-image-gen skill
5. If all pass — character is production-ready

---

## Phase 10 — Update memory + skill

- Append to `pipeline/image-pipeline-knowledge.md` learning loop
- If a new pattern emerged (e.g. specific failure mode + fix), write a new `feedback_*.md` memory file
- If a global rule shifted (e.g. rank should now default to 32), update this skill + RECIPES.md

---

## Cost & timing summary

| Phase | Active time | Wall time |
|---|---|---|
| Keystone lock (incl. confirm) | 30 min | 30 min |
| Dataset gen via Gemini | 5 min | 30-60 min (Gemini quota dependent) |
| Cull + caption | 30 min | 30 min |
| SCP + yaml | 5 min | 10 min |
| WMI launch | 5 min | 5 min |
| **Training** | 0 min (background) | **3h 30min** |
| Score-test | 5 min | 10 min |
| Deploy | 10 min | 10 min |
| **TOTAL** | **~90 min active** | **~5-6 hrs wall clock** |

---

## Speed optimisation experiments (for v5+ characters)

The default 3h 30min training time is appropriate for **5070 Ti at 1024 res with adapter v2 + qfloat8 + low_vram + rank 16 + 3000 steps + EMA**. That's the production-grade lock for Wren v4.

If you want to halve training time on future characters, here are the levers ranked by quality cost:

### Tier 1 — Try first (low quality risk)

**Drop steps to 2000.** Saves ~70 min per run with no significant quality cost. Validated on Skye Mercer v1 (2000 steps, shipped successfully). Ostris's pipeline routinely hits identity at 2000. Adjust `train.steps: 2000` in the yaml. Track if identity converges as fast — if step-1500 sample shows full keystone match, 2000 is enough.

**Status: queue this as the v5 / next-character experiment.** A/B against the 3000-step baseline once.

### Tier 2 — Consider (small quality cost)

**Drop res to 768.** Saves ~30% time (~70 min). Smaller than 512 so less face detail loss. Reasonable for Turbo creator content. Less ideal for cover work where 1024 face nuance matters. Adjust `dataset.resolution: [768]`.

**Drop EMA.** Saves ~5% time. Quality cost: slightly less smooth late-training noise. Marginal — only worth if combining with other levers.

### Tier 3 — Don't (real quality cost)

**Drop res to 512.** Saves ~50% time but cost is high — face nuance bakes in noticeably less. Avoid unless time-critical and you've already proven 768 works for that character.

**Drop rank to 8.** Saves ~5-10%. Quality cost: less face capacity, which exactly defeats the point of training a character LoRA. Skip.

### Tier 4 — Hardware solution

**Buy a 5090 (32GB).** Halves time + removes qfloat8 quantization tax = ~2x speedup overall = ~1h 45min per character at full quality. Best long-term ROI if running multiple characters. ~£2k investment.

### Recommended progression

1. Wren v4 ships with 3000 steps (current run, don't touch)
2. **Next character: try 2000 steps as Tier 1 experiment.** If identity converges as well, lock 2000 as new default.
3. If 2000 works AND time still matters: try 768 res as Tier 2 experiment.
4. If still need more speed: 5090 hardware upgrade.

### ComfyUI output → input directory bridge (pipeline gotcha)

When chaining renders (e.g. stage 1 native render → stage 2 Ultimate SD upscale of stage 1's output), **the LoadImage node reads from `ComfyUI/input/` only** — NOT from `output/` where stage 1 saved. Without an explicit copy, stage 2 returns HTTP 400 silently for every prompt.

Fix: any multi-stage pipeline must copy stage-N outputs to input/ before stage-N+1 fires:

```bash
ssh wauzz@PC 'powershell -c "Get-ChildItem C:\Users\wauzz\Documents\ComfyUI\output\<pattern>*.png | Copy-Item -Destination C:\Users\wauzz\Documents\ComfyUI\input\ -Force"'
```

Reference implementation in `content-creators/wren-rivers/lora-training-v4/score-test/fire_v4_candid_upscale.py` `copy_outputs_to_input()`. Costs ~2s + transfer, idempotent (Force overwrites).

Validated 26 Apr 2026 (Wren v4 candid pipeline) — first-run failure: 10 prompts × HTTP 400 = silent total fail. Second-run success: pre-flight copy fixed it.

### What NOT to optimise on speed

- The detached training pattern (WMI launcher) — already optimal, costs zero quality
- The sample prompts in production format — saves debugging time massively, costs nothing
- The Gemini-anchored dataset — quality lever, do NOT downgrade to bare Z-base t2i for speed
- The keystone lock confirmation — saves catastrophic failure cost

---

## Failure modes to avoid (validated 26 Apr 2026)

- **Don't use bare-trigger sample prompts in yaml** — gives zero identity signal mid-training (forces validation pass post-training and you can't tell if training is failing until it's done). Always production format.
- **Don't put face descriptors in captions OR persona block** — Z-Image latent space corruption; default Asian face on Turbo.
- **Don't use the same identity block for dataset gen and inference** — rich for dataset, minimal for inference. See `feedback_two_identity_blocks_lora.md`.
- **Don't tie python to SSH session** — use WMI launcher. SSH drops will kill it.
- **Don't use `python -u` to make logs flush** — costs 2.5x speed. Use default buffering + log mirror.
- **Don't run inference during training** — VRAM thrashing.
- **Don't suspend the training process to free GPU temporarily** — CUDA memory stays allocated, no help. Kill + resume from latest checkpoint instead.
- **Don't skip the keystone lock confirmation** — bad keystone = bad LoRA, all downstream work wasted.
- **Don't put name tokens in prompts** ("Wren", "Wren Rivers") — risks LoRA learning name-as-token vs face.

## Rollout priority (current characters)

1. **Wren Rivers v4** — Gemini dataset, 26 Apr 2026 — IN FLIGHT
2. Wren Rivers v4 — zbase dataset (A/B comparison) — DEFERRED unless Gemini fails
3. Marlowe Vance v1 — Klein 9B (different model, separate skill)
4. Future content creators per content-creators/roster.md

## Integration with other skills

- **Before:** persona-anatomy must have set up the persona profile + custom_creators.json entries
- **During:** uses `gemini-toolkit` for Gemini Pro Edit dataset gen
- **After:** `character-image-gen` and `flux-creator-pipeline` use the trained LoRA
- **Cross-ref:** `kling-video` skill for using the LoRA's renders as Kling sources
- **Production stack:** `tools/flux-pipeline/RECIPES.md` for the lane recipes that use the LoRA
