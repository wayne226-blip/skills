---
name: youtube
description: Fetch a YouTube channel's recent videos, show top 10 by views, generate key insights and next video suggestions. Usage: /youtube [channel-url]
argument-hint: "[youtube channel URL or @handle]"
allowed-tools: Bash
---

# YouTube Channel Analyser

Analyse a YouTube channel's recent performance and suggest next video ideas.

## Step 1: Get the channel URL

If an argument was passed, use that as the channel URL.
If no argument was given, use: `https://www.youtube.com/@aireallyreal`

## Step 2: Fetch the data

Run this command to fetch the 20 most recent videos:

```bash
yt-dlp --flat-playlist --print "%(title)s|||%(view_count)s|||%(duration_string)s|||%(webpage_url)s" --playlist-end 20 "[CHANNEL_URL]/videos" 2>/dev/null
```

If that returns nothing or errors (channel has no /videos tab), try without `/videos`:
```bash
yt-dlp --flat-playlist --print "%(title)s|||%(view_count)s|||%(duration_string)s|||%(webpage_url)s" --playlist-end 20 "[CHANNEL_URL]" 2>/dev/null
```

Each line is formatted as: `title|||view_count|||duration|||url`

If 0 videos are returned, tell the user: "No public videos found on this channel yet."

## Step 3: Parse and sort

- Split each line on `|||` to get title, views, duration, url
- Convert view counts to integers
- Sort by view count descending
- Take the top 10

## Step 4: Generate Key Insights

Analyse the full 20-video dataset (not just top 10) and produce 3–5 specific, data-driven observations. Examples of what to look for:

- Which title keywords or topics appear in top performers vs low performers
- Average view count across all 20 vs top 5
- Whether long-form or short-form performs better (compare duration vs views)
- Any outlier videos — massively over or underperforming
- Posting recency vs view count (if newer videos are catching up fast)

Be specific. Use actual numbers. Do NOT write generic statements like "engaging content performs well."

## Step 5: Generate Your Next Video suggestions

Based on patterns in the top 5 performers, suggest 3–5 specific video title ideas that:
- Follow the same title style/format as top performers
- Target similar topics or keywords
- Are realistic for the channel's apparent niche

## Step 6: Output

Format the result exactly like this:

---

## Key Insights
- [specific insight with numbers]
- [specific insight with numbers]
- [specific insight with numbers]

## Your Next Video
Suggested titles based on top performers:
1. [title suggestion]
2. [title suggestion]
3. [title suggestion]

---

## Top 10 Videos by Views

| # | Title | Views | Duration | Link |
|---|-------|-------|----------|------|
| 1 | [title] | [views formatted with commas] | [duration] | [Watch](url) |
| 2 | ... | ... | ... | ... |

---
*Fetched [N] videos · Analysed [date]*
