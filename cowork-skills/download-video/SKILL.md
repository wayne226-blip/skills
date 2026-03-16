---
name: download-video
description: >
  Download videos and audio from any URL using yt-dlp. Supports 1,872+ sites including YouTube, TikTok, Instagram, Twitch, Vimeo, and more. Defaults to best quality up to 4K. Use this skill whenever the user wants to download, grab, save, or rip a video or audio clip from a URL. Also triggers for: "download this video", "grab this clip", "save this video", "get the audio from this", "download-video [url]", "rip audio", "save that YouTube video", or any message containing a video/audio URL with download intent. Even casual requests like "can you grab that for me" with a URL should trigger this skill. If the user pastes a video URL and seems to want the file locally, use this skill.
---

# download-video

Download videos and audio from any URL using yt-dlp. This skill teaches you the exact flags, decision logic, and error handling to make downloads work reliably first time.

## Dependencies

Two tools are required:

- **yt-dlp** — the download engine. Install with `pip3 install yt-dlp` if missing.
- **ffmpeg** — needed for merging video+audio streams and audio extraction. Expected at `~/.local/bin/ffmpeg`. If missing, suggest downloading a static binary from evermeet.cx to `~/.local/bin/`.

Before your first download in a session, verify both are available:

```bash
which yt-dlp && ~/.local/bin/ffmpeg -version 2>/dev/null | head -1
```

If either is missing, tell the user and suggest the install command. Don't attempt a download without them.

## Save Location

Default: `~/Downloads/Media/`

Create it if it doesn't exist:

```bash
mkdir -p ~/Downloads/Media/
```

If the user specifies a different location (e.g. "save to Desktop"), adjust the `-o` path accordingly.

## Default Video Download Command

This is your starting point for every video download. Adjust flags based on user options (see below), but always start here:

```bash
yt-dlp \
  --ffmpeg-location ~/.local/bin/ \
  --no-playlist \
  --merge-output-format mp4 \
  --no-warnings \
  --print after_move:filepath \
  -f "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best" \
  -o "~/Downloads/Media/%(title)s.%(ext)s" \
  "[URL]"
```

Key flags explained:

- `--ffmpeg-location ~/.local/bin/` — tells yt-dlp where to find ffmpeg
- `--no-playlist` — downloads only the single video, not a full playlist (unless user asks)
- `--merge-output-format mp4` — ensures the final file is MP4
- `--no-warnings` — keeps output clean
- `--print after_move:filepath` — prints the final saved file path (this is how you know where the file ended up)
- `-f "bestvideo[height<=2160]..."` — picks best quality up to 4K with sensible fallbacks

## Quality Options

The default format string targets 4K (2160p) and falls back gracefully. When the user requests a specific quality, swap the height value:

- **720p**: `-f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best"`
- **1080p**: `-f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best"`
- **4K** (default): `-f "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best"`

## Audio-Only Mode

When the user wants just the audio ("just the audio", "mp3 only", "extract audio", "rip the audio"), use completely different flags. This is important — do NOT include `--merge-output-format` or the `-f` format string in audio-only mode:

```bash
yt-dlp \
  --ffmpeg-location ~/.local/bin/ \
  --no-playlist \
  --no-warnings \
  --print after_move:filepath \
  -x --audio-format m4a \
  -o "~/Downloads/Media/%(title)s.%(ext)s" \
  "[URL]"
```

Use `m4a` by default. If the user specifically asks for MP3, swap to `--audio-format mp3`.

## Playlist Downloads

By default, `--no-playlist` is always on. When the user explicitly asks to download a playlist:

1. **Check the size first** — don't blindly download hundreds of videos:
   ```bash
   yt-dlp --flat-playlist --print "%(playlist_count)s" "[URL]"
   ```
2. If more than 10 videos, tell the user the count and ask them to confirm before proceeding.
3. Once confirmed, remove `--no-playlist` from the command and run the full download.

This safeguard exists because playlists can be enormous. The user might not realise they're about to download 500 videos.

## Subtitles

When the user asks for subtitles ("with subtitles", "include subs", "get captions"), add:

```
--write-subs --embed-subs --sub-lang en
```

## Info/Preview Mode

If the user just wants to know what a video is without downloading ("what is this video?", "what's this?"), use:

```bash
yt-dlp --print "%(title)s - %(duration_string)s" "[URL]"
```

This is quick and doesn't download anything.

## Workflow

For every download request, follow these steps:

1. **Parse the request** — identify the URL and any options (quality, audio-only, save location, playlist, subtitles).
2. **Create the save directory** — `mkdir -p ~/Downloads/Media/` (or custom path).
3. **Build the command** — start with the default flags, then:
   - Audio-only? Swap to `-x --audio-format` flags, drop `--merge-output-format` and `-f`.
   - Custom quality? Adjust the height in `-f`.
   - Custom location? Adjust `-o`.
   - Playlist? Run the safeguard check first, then remove `--no-playlist`.
   - Subtitles? Add the subtitle flags.
4. **Run yt-dlp** — use `--print after_move:filepath` to capture the final file path.
5. **Verify** — run `ls -lh` on the output file to confirm it exists and get the file size.
6. **Report** — tell the user: filename, file size, save location, and resolution/quality (if video).

Keep the output minimal. Don't dump raw yt-dlp progress to the user — just report the result. If the download fails, show the error for diagnosis.

## Error Handling

| Error | How to detect | What to do |
|---|---|---|
| Unsupported site | "Unsupported URL" in output | Tell user the site isn't supported by yt-dlp |
| Geo-blocked | "not available in your country" | Explain the restriction |
| Private/login required | "Private video" or login prompt | Tell user it requires authentication. Suggest `--cookies-from-browser safari` if they have access |
| Rate limited | HTTP 429 / "Too Many Requests" | Wait and retry, or suggest `--cookies-from-browser safari` |
| ffmpeg missing | "ffmpeg not found" | Suggest downloading static binary from evermeet.cx to `~/.local/bin/` |
| yt-dlp not installed | command not found | Suggest `pip3 install yt-dlp` |
| Network failure | timeout or connection error | Suggest retrying, check connection |
| Special chars in filename | file not found after download | Rely on `--print after_move:filepath` for the actual saved path rather than guessing |
