---
name: vivienne-fire
description: Fires Vivienne Cole NSFW image renders via the locked Z-Image Turbo production stack on Wayne's PC ComfyUI. Use whenever Wayne asks for Vivienne Cole content, Vivienne Gumroad pack images, NSFW renders for the explicit-content lane, or any of the 43 genres in vivienne-cole's prompt-guide.md. Composes the workflow JSON from persona + genre + register inputs, applies the locked recipe (model + sampler + LoRA stack + anti-glamour negative wall), enqueues to the PC ComfyUI MCP, pulls results to local. Defaults to seedy/anti-glamour register unless explicitly told otherwise. NEVER use other models for Vivienne content — Z-Image Turbo is locked primary at top of stack.
---

# vivienne-fire

Fires Vivienne Cole NSFW renders on the locked Z-Image Turbo production stack. Validated end-to-end 6 May 2026 across the full difficulty range (solo / topless / public / hardcore / multi-person / consent-framed / period / fetish / explicit). Read the full locked recipe at `feedback_vivienne_zimage_locked_stack.md` before deviating.

## When to use

User says any of:
- "Render Vivienne X"
- "Fire a [genre] for Vivienne / for the Gumroad lane"
- "Make me [N] images of [persona] doing [scene]"
- Names any of the 43 genres in `authors/vivienne-cole/prompt-guide.md`
- Names any persona from the Vivienne roster (Sharon, Tracey, Maxine, Chelsea, Paige, Demi, Lacey, Amber, Leah, Vivienne)

Don't use for: Wren / Mila / Skye / Saskia / Helen / brand-safe creators (different stacks).

## The locked recipe (Z-Image Turbo — PRIMARY)

```json
{
  "1":  {"class_type": "UNETLoader", "inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}},
  "2":  {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "qwen_image"}},
  "3":  {"class_type": "VAELoader", "inputs": {"vae_name": "z_image_ae.safetensors"}},
  "5":  {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 2}},
  "20": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["5", 0], "lora_name": "skin_texture_zib_v1_1.safetensors", "strength_model": 0.5}},
  "21": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["20", 0], "lora_name": "NSFW_master_ZIT_000008766.safetensors", "strength_model": 0.5}},
  "30": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": "<POSITIVE>"}},
  "31": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": "<NEGATIVE>"}},
  "40": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1024, "height": 1280, "batch_size": 1}},
  "50": {"class_type": "KSampler", "inputs": {"model": ["21", 0], "positive": ["30", 0], "negative": ["31", 0], "latent_image": ["40", 0], "seed": <SEED>, "steps": 9, "cfg": 1, "sampler_name": "dpmpp_sde", "scheduler": "beta", "denoise": 1}},
  "55": {"class_type": "VAEDecode", "inputs": {"samples": ["50", 0], "vae": ["3", 0]}},
  "80": {"class_type": "SaveImage", "inputs": {"images": ["55", 0], "filename_prefix": "<PREFIX>"}}
}
```

PC ComfyUI endpoint: `http://100.107.67.79:8000/` (Tailscale-routed). Use `mcp__comfyui__enqueue_workflow` to submit, `mcp__comfyui__get_job_status` or curl history to poll, curl `/view` to pull rendered file to local.

## NSFW LoRA strength guide (lane → strength of node 21)

| Lane | NSFW_master_ZIT | Notes |
|---|---|---|
| Topless / softcore / suggestive | 0.4 | Add `nipplediffusion_zimage_v1` @ 0.3-0.4 if anatomy detail wanted |
| Soft-explicit / "naughty teaser" / public-explicit | 0.5-0.6 | |
| Multi-person + soft (couples MF, FF, group) | 0.5-0.6 | |
| Multi-person + explicit | 0.7 | |
| Hardcore (anal pose / facial / squirting / spread / fully exposed) | **0.85** | Drop contradictory garment tokens, lead anatomy clause |

For MILF personas (Sharon, Tracey, Maxine), add `MisterMR_Willow_Milf_Zimageturbo.safetensors` @ 0.6 as an additional LoRA chained after node 21.

For lingerie/fetish/seedy lanes specifically, push `skin_texture_zib_v1_1` (node 20) from 0.5 → 0.75. The body archetype lock fights hardest in this lane.

## Prompt structure (locked)

**Subject + action first → Setting → Details → Lighting → Atmosphere → Mood + Style + Film stock at end.**

```
[curvy white woman early 30s, long red wavy hair greasy at roots, freckled fair skin
with visible pores blemishes stretch marks asymmetric breasts, full natural heavy
breasts with gravity, soft belly with stretch marks, mole, knowing tired smile, real
working-class British woman, NOT glamour-model NOT page-three NOT instagram-model,
slag-energy not glamour, fully naked], <ACTION + POSE single-arm phrasing>, <SEEDY
SETTING with specific working-class British details>, <LIGHTING with camera-direction>,
candid working-class real, gritty British documentary photograph, shot on 35mm film
Kodak Tri-X 400 with heavy grain
```

### Hard rules

1. **NEVER use the word "topless"** — overloaded token; use anatomy clauses instead ("bare chest with full natural breasts visible")
2. **Lead with what's ON / what's exposed**, not what's off
3. **Anchor garment geometry** — "elastic gusset visible between her thighs", "waistband stretched across her bottom", "knickers riding up between her cheeks"
4. **Single-arm pose phrasing** — "right hand resting on the table", NOT "both elbows resting"
5. **Adult-anchor mandatory for under-25 personas** — "fully grown adult woman, fully developed mature adult anatomy, just turned eighteen and legally adult"
6. **Multi-person preamble** — "Two distinct people:" or "Three distinct people:", describe each with separable identities, single-arm-per-subject, anchor body contact specifically
7. **Setting determines body register** — premium/luxury settings pull glamour body; **default to bedsit/grim/seedy British working-class for any explicit lane** unless brief explicitly demands premium
8. **Garment-cut rule** — for upskirt/anal "rucked up / pulled down" scenarios, choose **loose flowing** (wrap-dress, sundress, pleated mini, floral midi). Tight-tailored (leather mini, pencil skirt) holds intact and refuses to ruck. For hardcore "pulled down to thigh" — **drop the contradictory garment token entirely**, use "completely naked from the waist down"
9. **"slag-energy not glamour"** tag in positive — works as register signal to the model
10. **Front-load wardrobe + anatomy in first 30 words** — Z-Image has shorter attention budget than Klein

## Standard anti-glamour negative (locked)

```
low quality, worst quality, blurry, deformed, bad anatomy, bad hands, extra fingers,
fused fingers, extra arms, extra limbs, multiple arms, watermark, text, logo, cartoon,
3d render, illustration, painting, glamour model, page three, page-three, perfect smooth
skin, perfect symmetric breasts, narrow waist, photoshopped, magazine cover, editorial,
fashion shoot, premium boudoir, luxury, polished, hd, 4k, ultra detailed, sharp focus,
beauty filter, flawless, retouched, airbrushed, perfectly clean, immaculate,
instagram-model, model-perfect, glossy skin, plastic skin, smooth doll skin,
professional studio lighting, magazine quality
```

Add per-scene:
- **Multi-person:** `three arms, four arms, extra heads, conjoined bodies, fused limbs, four people, multiple bodies, additional people`
- **Solo explicit:** `multiple people, additional people, second face`
- **Rough/dominant:** `victim, fearful, distressed, crying, scared expression, frightened`
- **Topless / bare-chest:** `dress, mini dress, full dress, t-shirt, tank top, crop top, bra, fabric on chest, clothing on chest, covered chest, censored, modesty bra`
- **Hardcore-explicit:** `skirt, mini skirt, leather skirt, dress, fully clothed, intact clothing on lower body, knickers pulled up, thong pulled up, jeans, trousers, leggings`
- **Adult-anchor for under-25:** `child, teen, teenager, underage, schoolgirl, juvenile, immature body, undeveloped body, flat chest`
- **Lingerie / fetish:** all the glamour-wall above

## Roster (10 personas, locked 6 May 2026)

**MILF tier (45-55):** Sharon (52, bleached blonde, pub MILF), Tracey (48, black bob with blonde streaks, suburban naughty mum), Maxine (56, silver pixie, country-club cougar)

**22-year-old tier:** Chelsea (Essex club slag, platinum extensions), Paige (Geordie auburn, student), Demi (alt-goth, black + red underlights, septum)

**18-year-old tier (adult-anchor mandatory):** Lacey (just-18, white-blonde), Amber (fresh-faced, strawberry-blonde), Leah (festival/rave, black space-buns)

**Ringleader:** Vivienne (28, brunette British exhibitionist)

Each has identity blocks ready to drop into the `[character_block]` of any prompt — extracted from the session memory file.

## Output convention

Files go to `~/calibre-hq/authors/vivienne-cole/output/raw/{batch_name}/` per the existing batch-system convention. Filename prefix in the SaveImage node should match the batch name. **Do NOT use `output/chroma-tests/`** — that was the test-run dump from 6 May; production goes to `output/raw/`.

For test/iteration runs that aren't part of a named batch, use `output/raw/_test/{date}/`.

## Batch JSON format (existing system)

Vivienne's `batch_jobs/{name}.json` files use this format:
```json
{
  "name": "<batch-name>",
  "preset": "vivienne-cole",
  "output_dir": "/Users/wayne/calibre-hq/authors/vivienne-cole/output/raw/<batch-name>/",
  "jobs": [
    {"prompt": "[character_block], <action>, <setting>, <lighting>", "filename": "<name>-01.png", "negative": "..."}
  ]
}
```

When rendering a full batch, iterate through `jobs[]` and submit each via the locked workflow with the prompt + filename + per-job negative (or fall back to the standard anti-glamour negative if `negative` is empty).

## What this skill does NOT do

- **Generate prompts from thin air** — the user must specify the genre/scene/register, OR point to a batch_jobs JSON file. The skill applies the locked recipe, doesn't invent the creative direction.
- **Use any other model** — Z-Image Turbo is locked at top of stack. If a render legitimately needs Chroma (atmospheric/cinematic) or Klein 9B (soft private portrait), call those out explicitly and ask the user to confirm before deviating.
- **Train LoRAs or PuLID** — separate workflow. PuLID + Z-Image is on the to-do for character consistency across the catalogue but not yet validated.
- **Apply Flux LoRAs** — they silently corrupt the Z-Image UNET. Z-Image-specific LoRAs only.

## Stack assignments (full)

| Lane | Model | Recipe |
|---|---|---|
| **PRIMARY — explicit, topless, hardcore, multi-person, public, private, fetish** | **Z-Image Turbo** | this skill |
| Atmospheric / cinematic / moody hero shot | Chroma1-HD pure base | 24 steps, CFG 3.5, dpmpp_2m+simple, no LoRAs, DualCLIPLoader (clip_l + t5xxl, type flux), VAE ae.safetensors |
| Soft / portrait / cover / character keystone in private setting | Klein 9B distilled | 4 steps, CFG 1.0, euler+simple, ModelSamplingFlux 1.15, single CLIPLoader (qwen_3_8b, type flux2), VAE flux2-vae |
| ~~Klein 4B base/distilled~~ | DROPPED | slower, no quality advantage |
| ~~Flux dev / Krea~~ | DROPPED | non-commercial license + worse quality |

## Verification

After every render, before declaring done:
1. Pull the file to local via curl `/view` endpoint
2. Read the image
3. Check: register correct (seedy not glamour), body archetype real-women not IG-model, prompted anatomy/garments rendered as asked, no extra-limb artefacts, single-arm pose held
4. If any check fails — diagnose against the rules above (most common: setting too premium, garment too tight-tailored, "topless" word leaked into prompt, NSFW LoRA strength too low for lane)
