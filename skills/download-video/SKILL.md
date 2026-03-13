---
name: download-video
description: >
  Downloads video or audio from any URL (YouTube, TikTok, Instagram, Vimeo, and
  1,800+ other sites) using yt-dlp. Use this skill whenever the user asks to
  download, grab, or save a video or audio clip from a URL. The skill produces a
  downloaded media file at ~/Downloads/Media/ (or a user-specified location) in
  the best available quality up to 4K, with options for audio-only extraction,
  specific quality, playlists, and subtitles. Without this skill, Claude guesses
  at yt-dlp flags and often gets merging, format selection, or playlist handling
  wrong.
---

# Download Video Skill

Download video or audio from any URL using yt-dlp. Supports 1,800+ sites.

## Dependencies

- **yt-dlp** — if missing: `pip3 install yt-dlp`
- **ffmpeg** — static binary at `~/.local/bin/ffmpeg`. If missing: download from `https://evermeet.cx/ffmpeg/getrelease/zip`, unzip to `~/.local/bin/`

## Step-by-Step Workflow

### 1. Parse the request

Identify from the user's message:
- **URL** — the video/page URL
- **Mode** — video (default) or audio-only ("just the audio", "mp3", "audio only")
- **Quality** — 4K default, or specific ("720p", "1080p")
- **Location** — `~/Downloads/Media/` default, or custom ("save to Desktop", "put it in ~/Projects/")
- **Playlist** — only if user explicitly says "playlist", "all videos", "whole playlist"
- **Subtitles** — only if user says "with subtitles", "with subs"
- **Info only** — only if user says "what is this video?", "how long is this?"

### 2. Create output directory

```bash
mkdir -p ~/Downloads/Media
```

Or the custom directory if the user specified one.

### 3. Build and run the yt-dlp command

#### Video download (default)

```bash
yt-dlp \
  --ffmpeg-location ~/.local/bin/ \
  --no-playlist \
  --merge-output-format mp4 \
  --no-warnings \
  -f "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best" \
  -o "~/Downloads/Media/%(title)s.%(ext)s" \
  "[URL]"
```

#### Specific quality (e.g. 720p, 1080p)

Replace `2160` with the requested height:

```bash
-f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best"
```

#### Audio only

Do NOT include `--merge-output-format` or `-f` format string. Use:

```bash
yt-dlp \
  --ffmpeg-location ~/.local/bin/ \
  --no-playlist \
  --no-warnings \
  -x --audio-format m4a \
  -o "~/Downloads/Media/%(title)s.%(ext)s" \
  "[URL]"
```

Use `--audio-format mp3` if the user specifically asks for MP3.

#### Subtitles

Add these flags to the video command:

```bash
--write-subs --embed-subs --sub-lang en
```

#### Info/preview only (no download)

```bash
yt-dlp \
  --no-playlist \
  --no-warnings \
  --print "%(title)s | %(duration_string)s" \
  "[URL]"
```

Report the title and duration. Do not attempt to show file size (it is often unavailable).

#### Playlist download

**Safeguard first** — check how many videos:

```bash
yt-dlp --flat-playlist --print "%(playlist_count)s" "[URL]" 2>/dev/null | head -1
```

- If 10 or fewer: proceed automatically
- If more than 10: tell the user the count and ask to confirm before downloading
- Only after confirmation, run without `--no-playlist`:

```bash
yt-dlp \
  --ffmpeg-location ~/.local/bin/ \
  --merge-output-format mp4 \
  --no-warnings \
  -f "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best" \
  -o "~/Downloads/Media/%(title)s.%(ext)s" \
  "[URL]"
```

### 4. Verify and report

After download completes, verify the file:

```bash
ls -lh "[filepath]"
```

Report to the user:
- **Filename**
- **File size**
- **Save location** (full path)
- **Resolution** (if video download)

## Error Handling

| Error | What to look for | What to do |
|---|---|---|
| Unsupported site | "Unsupported URL" | Tell user the site isn't supported by yt-dlp |
| Geo-blocked | "not available in your country" | Explain the geo-restriction |
| Private/login required | "Private video", "Sign in" | Suggest `--cookies-from-browser safari` for sites where user is logged in |
| Rate limited | HTTP 429, "Too Many Requests" | Wait a moment and retry. If persistent, suggest `--cookies-from-browser safari` |
| ffmpeg missing | "ffmpeg not found", merger errors | Tell user to download ffmpeg: `curl -L "https://evermeet.cx/ffmpeg/getrelease/zip" -o /tmp/ffmpeg.zip && unzip -o /tmp/ffmpeg.zip -d ~/.local/bin/` |
| yt-dlp missing | "command not found" | `pip3 install yt-dlp` |
| Network failure | timeout, connection refused | Suggest retrying or checking connection |
| File not found after download | ls fails | The filename may have special characters. Re-check with `ls ~/Downloads/Media/` to find actual file |

## Key Rules

- **Always use `--ffmpeg-location ~/.local/bin/`** — ffmpeg is not in the system PATH
- **Always use `--no-playlist`** unless the user explicitly asks for a playlist
- **Never use `--merge-output-format` with audio-only mode** — it conflicts with `-x`
- **Never dump raw yt-dlp progress output** to the user — just report the result
- **Always verify the file exists** after download before reporting success
- **Default to 4K** (height<=2160) — falls back to best available if 4K isn't offered
- **Set timeout to 300000ms** (5 minutes) on the Bash command for large downloads
