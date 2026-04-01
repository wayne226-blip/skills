---
name: gemini-toolkit
description: Use the Gemini MCP tools for image generation, image editing, vision/image description, video understanding, video compression, cheap text generation, text-to-speech, and embeddings. Trigger this skill whenever the user asks to generate an image, create a picture, edit a photo, describe or analyse an image or video, understand a video, compress a video, convert text to speech, read something aloud, generate embeddings, or mentions "Gemini" in the context of any of these tasks. Also trigger when the user says "make me an image", "draw", "picture of", "what's in this image", "describe this photo", "what's in this video", "analyse this video", "compress this video", "read this out", "speak this", "TTS", or asks for cheap/fast text generation via Gemini rather than Claude. Even casual requests like "get me an image of a blue dog", "what does this picture show", or "what happens in this video" should trigger this skill.
---

# Gemini Toolkit

Guide for using the Gemini MCP server — 9 tools that give you image generation, image editing, vision, video understanding, video compression, cheap text, TTS, and embeddings through Google's Gemini API.

The MCP tools are prefixed `mcp__gemini__`. This skill tells you when to use each one and how to get the best results.

**API reference:** https://ai.google.dev/gemini-api/docs

---

## Tool Selection

Pick the right tool based on what the user needs:

| User wants... | Tool | Key thing to know |
|---|---|---|
| Generate an image from a description | `gemini_generate_image` | Default model is fast and free. Specify aspect_ratio for non-square. |
| Edit/modify an existing image | `gemini_edit_image` | Pass the image file path + natural language instruction. |
| Describe, analyse, or ask about an image | `gemini_describe_image` | Accepts local file paths AND URLs. Use the `question` param for specific queries. Supports OCR, object detection, visual Q&A. |
| Analyse or ask about a video | `gemini_describe_video` | Accepts local video files AND YouTube URLs. Supports timestamp clipping. |
| Compress a video file | `gemini_compress_video` | Uses ffmpeg. Targets a file size (default 20MB). Useful before uploading large videos. |
| Quick/cheap text generation | `gemini_text` | Uses Gemini's cheapest model. Good for tasks where Claude itself is overkill or when you need a second opinion. |
| Convert text to audio | `gemini_tts` | Returns a .wav file. 8 voice options. Max ~5000 chars per call. |
| Generate embeddings for search/similarity | `gemini_embed` | Returns a vector. Useful for building search indexes or measuring text similarity. |
| Check what models are available | `gemini_list_models` | Useful when a model 404s — names change as Google updates previews. |

---

## Available Models (March 2026)

Models are grouped by generation. Newer isn't always better — pick based on the task.

### Image Generation Models
| Model | Use case |
|---|---|
| `gemini-2.5-flash-image` | **MCP default.** Fast, free tier, good enough for most things. |
| `gemini-3.1-flash-image-preview` | Latest fast model. Higher quality than 2.5, supports resolutions up to 4K. |
| `gemini-3-pro-image-preview` | Best quality. Advanced reasoning, better text rendering, complex scenes. Use when quality matters more than speed. |

### Vision / Multimodal Models
| Model | Use case |
|---|---|
| `gemini-2.5-flash` | **MCP default for vision.** Fast multimodal — handles images, audio, video, documents. |
| `gemini-3-flash-preview` | Latest. Better at fine detail, object detection, segmentation. |
| `gemini-3.1-pro-preview` | Most intelligent. Use for complex visual reasoning tasks. |

### Text Models
| Model | Use case |
|---|---|
| `gemini-2.5-flash-lite` | **MCP default.** Cheapest and fastest. Good for simple tasks. |
| `gemini-2.5-flash` | Mid-tier. Better reasoning than lite. |
| `gemini-2.5-pro` | Most capable 2.5 model. Complex tasks. |

### Other Models
| Model | Use case |
|---|---|
| `gemini-2.5-flash-preview-tts` | Text-to-speech. 8 voices. |
| `gemini-embedding-2-preview` | Text embeddings for search/similarity. |

**Tip:** Model names change as Google updates previews. If you get a 404, run `gemini_list_models` to find the current name.

---

## After Every Image Generation or Edit

This is important — always do both of these steps:

1. **Read the output file** using the Read tool so the user can actually see the image inline in the conversation. The MCP tool returns a file path, not the image itself.
2. **Tell the user the file path** so they know where it's saved.

If you skip step 1, the user just sees a path string and has to go find the file manually. That's a bad experience.

---

## Image Generation Tips

### Aspect Ratios

The API supports these aspect ratios (pass via the `aspect_ratio` parameter):

| Ratio | Good for |
|---|---|
| **1:1** | Default. Profile pics, icons, square social posts |
| **16:9** | Landscapes, desktop wallpapers, YouTube thumbnails |
| **9:16** | Phone wallpapers, Instagram stories, TikTok |
| **3:2** / **2:3** | Standard photo ratios (landscape/portrait) |
| **4:3** / **3:4** | Classic screen ratios |
| **4:5** / **5:4** | Instagram portrait/landscape posts |
| **21:9** | Ultra-wide, cinematic |
| **4:1** / **1:4** | Banners (horizontal/vertical) |
| **8:1** / **1:8** | Extreme banners / tall strips |

### Model Choice
- **`gemini-2.5-flash-image`** (MCP default) — Fast, free tier, good enough for most things
- **`gemini-3.1-flash-image-preview`** — Latest fast model. Better quality, supports image resolutions (512, 1K, 2K, 4K) and thinking levels
- **`gemini-3-pro-image-preview`** — Best quality. Better text rendering in images, better at complex scenes. Use when the user wants quality over speed, or when the default produces something that's not quite right

### Advanced Features (API-level, not all in MCP tool yet)
- **Image resolution:** `512`, `1K`, `2K`, `4K` — available via API `image_size` param on 3.x models. Not yet exposed in MCP tool; pass via model param workaround or request MCP server update.
- **Reference images:** Up to 14 images can be passed as style/subject references (10 objects + 4 characters on 3.1 Flash). Useful for brand consistency.
- **Thinking levels:** `minimal` (default, fastest) or `high` (better quality, slower). Controls how much the model reasons before generating.
- **Multi-turn refinement:** The API supports iterative refinement through conversation — generate, then ask for changes in follow-up turns.
- **Grounding with Google Search:** 3.x models can access real-time web data to generate imagery based on current events, weather, etc.

### Prompt Quality
The Gemini image models respond well to detail. If the user gives a vague prompt like "a dog", consider whether to ask for more detail or just go with it. For professional or specific use cases, more detail helps: lighting, style, mood, setting, camera angle.

Don't over-prompt for casual requests though — "a blue dog" doesn't need "a blue dog, photorealistic, 8K, cinematic lighting, rule of thirds."

**Key tip from Google:** "Describe the scene, don't just list keywords" — natural language descriptions produce better results than keyword-stuffed prompts.

---

## Image Editing Tips

The edit tool works by passing an existing image plus a natural language instruction. It's conversational — describe what you want changed as if you're talking to a human editor:

- "Make the sky sunset orange"
- "Remove the person on the left"
- "Change the blue car to red"
- "Add a hat to the dog"
- "Make it look like a watercolour painting"

The instruction should describe the change, not the final result. "Make the background blue" works better than "An image with a blue background."

All generated images include a SynthID watermark (invisible digital watermark from Google).

---

## Vision / Image Description

This tool analyses images — it doesn't generate them. Use it when the user wants to know what's in an image, extract text from a photo, or ask questions about visual content.

### Capabilities

The vision model (multimodal) can do:
- **Image captioning** — describe what's in an image
- **Visual Q&A** — answer specific questions about image content
- **OCR** — extract text from photos, documents, screenshots
- **Object detection** — identify items and return bounding box coordinates (0-1000 normalised scale)
- **Image classification** — categorise images
- **Segmentation** — extract contour masks for specific objects (Gemini 2.5+ models)
- **Document processing** — handle text-heavy images, scanned docs, multi-page PDFs

### Question Parameter

The `question` parameter defaults to "Describe this image in detail" but you should customise it based on what the user actually wants:
- "What text is visible in this image?" — for OCR
- "How many people are in this photo?" — for counting
- "What brand is the laptop?" — for identification
- "Is this image suitable for a professional website?" — for assessment
- "Identify all objects and return their bounding box coordinates" — for detection
- "What damage is visible in this photo?" — for inspection/assessment

### Supported Image Formats
PNG, JPEG, WEBP, HEIC, HEIF

### Technical Details
- Accepts URLs as well as local file paths
- Up to 3,600 images per request (API limit)
- Token cost: 258 tokens for images <= 384px; larger images tiled into 768x768 sections
- **Best practice:** When combining a single image with a text prompt, place the text prompt *after* the image in the contents array (the MCP tool handles this automatically)
- For fine text recognition, higher `media_resolution` improves accuracy (API-level setting)

### Model Choice for Vision
- **`gemini-2.5-flash`** (MCP default) — Fast, handles most vision tasks well
- **`gemini-3-flash-preview`** — Better at fine detail, object detection with bounding boxes, segmentation masks
- **`gemini-3.1-pro-preview`** — Most capable for complex visual reasoning

---

## Video Understanding

Analyse videos — describe content, answer questions about specific moments, transcribe speech. Works with local files and YouTube URLs.

### What It Can Do
- **Describe and summarise** video content (visual + audio)
- **Answer questions** about what happens at specific timestamps
- **Extract information** from visual frames and audio tracks
- **Process YouTube URLs directly** — no need to download first (public videos only)

### Parameters
- **`video_source`** — Local file path OR YouTube URL
- **`question`** — What to ask (e.g. "What happens at 01:30?" or "Summarise this video")
- **`model`** — Default `gemini-2.5-flash`. Use `gemini-3-flash-preview` for better detail
- **`start_offset`** / **`end_offset`** — Optional timestamp clipping in seconds (e.g. "60" for 1 min in). Saves tokens on long videos by only analysing a section

### Supported Formats
MP4, MPEG, MOV, AVI, FLV, WebM, WMV, 3GPP

### Technical Details
- Videos under 20MB are sent inline; larger files are uploaded via the Gemini Files API automatically
- YouTube URLs go directly — no download needed
- Token cost: ~300 tokens/second at default resolution (258 tokens/frame at 1 FPS + 32 tokens/second audio)
- A 1-minute video costs ~18,000 tokens
- Videos up to 1 hour work with 1M context models; up to 3 hours at low resolution
- YouTube free tier: 8 hours/day; paid: unlimited

### Tips
- Use `start_offset`/`end_offset` to analyse just the relevant section of a long video
- For fast-action content, the default 1 FPS sampling may miss details
- Place the question *after* the video in your prompt for best results (the MCP tool handles this)

---

## Video Compression

Compress videos using ffmpeg before uploading or sharing. Useful when a video exceeds the 20MB inline limit.

### Parameters
- **`video_path`** — Path to the video file
- **`target_mb`** — Target file size in MB (default: 20, matching the Gemini inline limit)
- **`output_filename`** / **`output_dir`** — Optional custom output location

The tool calculates the optimal bitrate based on video duration, uses H.264 encoding with AAC audio. Shows original vs compressed size with percentage reduction.

**Requires:** ffmpeg (installed at `/Users/wayne/.local/bin/ffmpeg`)

---

## Audio Understanding

**Note:** The MCP server currently handles audio *output* (TTS) but not audio *input* (understanding). The Gemini API supports audio understanding — this section documents the API capabilities for reference. An audio understanding tool could be added to the MCP server in future.

### What the API Can Do
- **Transcription & translation** — speech-to-text with automatic language detection
- **Emotion detection** — identify speaker emotions (happy, sad, angry, neutral)
- **Non-speech analysis** — recognise sounds like birdsong, sirens, music, appliances
- **Timestamped references** — use MM:SS format to query specific audio segments
- **Structured output** — get JSON responses with segmented transcripts

### Technical Details
- 32 tokens per second of audio; 1 minute = 1,920 tokens
- Maximum 9.5 hours of combined audio per prompt
- Audio downsampled to 16 Kbps; multi-channel converted to mono
- Supported formats: WAV, MP3, AIFF, AAC, OGG Vorbis, FLAC
- Does NOT support real-time transcription (use Live API or Google Cloud Speech-to-Text for that)

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

### Parameters
- **`system_instruction`** — Set up Gemini with specific behaviour for a task
- **`temperature`** — Controls creativity (0.0 = deterministic, 2.0 = very creative). **Important:** For Gemini 3.x models, Google strongly recommends keeping temperature at the default 1.0. Lower values on 3.x models can cause unexpected behaviour like looping or degraded output.
- **`max_tokens`** — Default 2048. Increase for longer outputs.

### Thinking Mode (Gemini 3.x)
Gemini 3 models support a thinking/reasoning mode with configurable levels (low, medium, high). This affects cost, latency, and quality. The MCP tool doesn't expose this directly yet — would need a server update to add a `thinking_level` parameter.

### Alternative Models
Pass a different model via the `model` parameter:
- `gemini-2.5-flash` — Better reasoning than lite, still cheap
- `gemini-2.5-pro` — Most capable, higher cost
- `gemini-3-flash-preview` — Latest, with thinking mode support

---

## Output Location

All generated files (images, audio) are saved to `~/Claude/gemini-output/` by default. Files are named with a timestamp and a slug from the prompt, e.g. `2026-03-23_14-30-45_blue-dog-sitting-in.png`.

You can override the output directory per-call with the `output_dir` parameter if the user wants files saved somewhere specific (e.g., a project folder).

---

## Error Handling

Common issues and what to do:

- **Model 404**: Gemini preview model names change frequently. Run `gemini_list_models` to find the current name and retry with the correct model.
- **Rate limit**: Free tier has limits. Tell the user and suggest waiting a moment or switching to a different model.
- **No image generated**: Sometimes the model returns text instead of an image (e.g., if the prompt triggers safety filters). Share the text response with the user and suggest rephrasing.
- **API key missing**: The error message tells the user exactly where to add it (`~/.claude/settings.json` under `mcpServers.gemini.env`). Pass it along.
- **Safety filter**: If content is blocked, the model returns a text explanation. Don't retry with the same prompt — help the user rephrase.
- **Image too large**: For vision, inline data has a 20MB total request limit. For larger files, suggest resizing first or note that the Files API (not yet in MCP) handles larger uploads.
- **Temperature looping**: If text output from Gemini 3.x models loops or degrades, check if temperature was set below 1.0. Reset to 1.0.
