---
name: gemini-toolkit
description: Use the Gemini MCP tools for image generation, image editing, vision/image description, cheap text generation, text-to-speech, and embeddings. Trigger this skill whenever the user asks to generate an image, create a picture, edit a photo, describe or analyse an image, convert text to speech, read something aloud, generate embeddings, or mentions "Gemini" in the context of any of these tasks. Also trigger when the user says "make me an image", "draw", "picture of", "what's in this image", "describe this photo", "read this out", "speak this", "TTS", or asks for cheap/fast text generation via Gemini rather than Claude. Even casual requests like "get me an image of a blue dog" or "what does this picture show" should trigger this skill.
---

# Gemini Toolkit

Guide for using the Gemini MCP server — 7 tools that give you image generation, image editing, vision, cheap text, TTS, and embeddings through Google's Gemini API.

The MCP tools are prefixed `mcp__gemini__`. This skill tells you when to use each one and how to get the best results.

---

## Tool Selection

Pick the right tool based on what the user needs:

| User wants... | Tool | Key thing to know |
|---|---|---|
| Generate an image from a description | `gemini_generate_image` | Default model is fast and free. Specify aspect_ratio for non-square. |
| Edit/modify an existing image | `gemini_edit_image` | Pass the image file path + natural language instruction. |
| Describe, analyse, or ask about an image | `gemini_describe_image` | Accepts local file paths AND URLs. Use the `question` param for specific queries. |
| Quick/cheap text generation | `gemini_text` | Uses Gemini's cheapest model. Good for tasks where Claude itself is overkill or when you need a second opinion. |
| Convert text to audio | `gemini_tts` | Returns a .wav file. 8 voice options. Max ~5000 chars per call. |
| Generate embeddings for search/similarity | `gemini_embed` | Returns a vector. Useful for building search indexes or measuring text similarity. |
| Check what models are available | `gemini_list_models` | Useful when a model 404s — names change as Google updates previews. |

---

## After Every Image Generation or Edit

This is important — always do both of these steps:

1. **Read the output file** using the Read tool so the user can actually see the image inline in the conversation. The MCP tool returns a file path, not the image itself.
2. **Tell the user the file path** so they know where it's saved.

If you skip step 1, the user just sees a path string and has to go find the file manually. That's a bad experience.

---

## Image Generation Tips

### Aspect Ratios
Match the aspect ratio to the content:
- **1:1** — Default. Good for profile pictures, icons, square social posts
- **16:9** — Landscapes, desktop wallpapers, YouTube thumbnails
- **9:16** — Phone wallpapers, Instagram stories, TikTok
- **3:2** / **4:3** — Standard photo ratios
- **4:5** — Instagram portrait posts

### Model Choice
- **`gemini-2.5-flash-image`** (default) — Fast, free tier, good enough for most things
- **`gemini-3-pro-image-preview`** — Higher quality, better text rendering in images, better at complex scenes. Use when the user wants quality over speed, or when the default produces something that's not quite right.

### Prompt Quality
The Gemini image models respond well to detail. If the user gives a vague prompt like "a dog", consider whether to ask for more detail or just go with it. For professional or specific use cases, more detail helps: lighting, style, mood, setting, camera angle.

Don't over-prompt for casual requests though — "a blue dog" doesn't need "a blue dog, photorealistic, 8K, cinematic lighting, rule of thirds."

---

## Image Editing Tips

The edit tool works by passing an existing image plus a natural language instruction. It's conversational — describe what you want changed as if you're talking to a human editor:

- "Make the sky sunset orange"
- "Remove the person on the left"
- "Change the blue car to red"
- "Add a hat to the dog"
- "Make it look like a watercolour painting"

The instruction should describe the change, not the final result. "Make the background blue" works better than "An image with a blue background."

---

## Vision / Image Description

This tool analyses images — it doesn't generate them. Use it when the user wants to know what's in an image, extract text from a photo, or ask questions about visual content.

The `question` parameter defaults to "Describe this image in detail" but you should customise it based on what the user actually wants:
- "What text is visible in this image?" — for OCR
- "How many people are in this photo?" — for counting
- "What brand is the laptop?" — for identification
- "Is this image suitable for a professional website?" — for assessment

Accepts URLs as well as local file paths — useful when the user pastes an image link.

---

## Text-to-Speech

Voices available (the `voice_name` parameter):

| Voice | Character |
|---|---|
| **Kore** (default) | Clear, neutral female |
| **Puck** | Friendly, approachable male |
| **Charon** | Deep, authoritative male |
| **Fenrir** | Strong, energetic |
| **Aoede** | Warm, melodic female |
| **Leda** | Soft, gentle female |
| **Orus** | Clear, professional male |
| **Zephyr** | Light, airy |

If the user doesn't specify a voice, use Kore (the default). If they ask for a male voice, suggest Puck or Orus. For something dramatic, suggest Charon.

Text is limited to ~5000 characters per call. For longer text, you'll need to split it into chunks and make multiple calls.

Output is always a .wav file. Let the user know this — if they need MP3 they'll need to convert it.

---

## Cheap Text Generation

The `gemini_text` tool calls Gemini's cheapest model (`gemini-2.5-flash-lite`). Use it when:

- The user explicitly asks to use Gemini for text
- You need a second AI opinion on something
- The task is simple and using Claude feels like overkill (e.g., generating test data, simple translations)
- You want to compare Claude's answer with Gemini's

Don't default to this for normal tasks — Claude is the primary assistant. This is a utility tool for specific situations.

The `system_instruction` parameter is useful for setting up Gemini with specific behaviour for a task. The `temperature` parameter controls creativity (0.0 = deterministic, 2.0 = very creative).

---

## Output Location

All generated files (images, audio) are saved to `~/Claude/gemini-output/` by default. Files are named with a timestamp and a slug from the prompt, e.g. `2026-03-23_14-30-45_blue-dog-sitting-in.png`.

You can override the output directory per-call with the `output_dir` parameter if the user wants files saved somewhere specific (e.g., a project folder).

---

## Error Handling

Common issues and what to do:

- **Model 404**: Gemini preview model names change. Run `gemini_list_models` to find the current name and retry with the correct model.
- **Rate limit**: Free tier has limits (~500 images/day, 15 text requests/minute). Tell the user and suggest waiting a moment.
- **No image generated**: Sometimes the model returns text instead of an image (e.g., if the prompt triggers safety filters). Share the text response with the user and suggest rephrasing.
- **API key missing**: The error message tells the user exactly where to add it. Pass it along.
