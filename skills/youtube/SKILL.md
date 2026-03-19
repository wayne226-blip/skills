---
name: youtube
description: "Complete YouTube channel analyser and SEO audit tool. Analyses recent videos, runs a full SEO audit (titles, descriptions, tags, thumbnails, AI search readiness, playlists, Shorts, engagement), identifies content saturation, tracks growth trajectory, benchmarks against competitors, and suggests next videos with projected impact estimates. Supports 3 modes (taster/standard/full) and optional flags (html/email/calendar/shorts/vs). Use this skill whenever the user wants to analyse a YouTube channel, audit YouTube SEO, compare channels, generate a content calendar, or find SEO opportunities for YouTube creators. Usage: /youtube [channel-url] [mode] [flags]"
argument-hint: "[youtube URL or @handle] [taster|standard|full] [html|email|calendar|shorts|vs URL]"
allowed-tools: Bash, WebSearch, Write, mcp__claude_ai_Gmail__gmail_create_draft
---

# YouTube Channel Analyser + Full SEO Audit

A comprehensive YouTube channel analysis and SEO audit tool covering 60+ ranking factors for 2026.

---

## Step 1: Parse Arguments

Parse the arguments to determine the channel URL, mode, and flags.

**Mode** (pick one — default is `standard`):
- `taster` — free lead-gen version: shows problems but withholds fixes
- `standard` — solid audit with actionable recommendations
- `full` — complete 60-factor premium audit

**Flags** (can combine):
- `html` — save the report as a styled HTML file
- `email` — auto-draft a Gmail to the channel owner with the report
- `calendar` — append a 30-day content calendar
- `shorts` — Shorts-only deep analysis (replaces standard flow)
- `vs [url]` — head-to-head channel comparison (replaces standard flow)

If no URL is given, use: `https://www.youtube.com/@aireallyreal`

Examples:
- `/youtube https://www.youtube.com/@channel` → standard mode
- `/youtube https://www.youtube.com/@channel taster` → taster mode
- `/youtube https://www.youtube.com/@channel full html email` → full audit + HTML + email
- `/youtube https://www.youtube.com/@channel vs https://www.youtube.com/@other` → comparison

---

## Step 2: Fetch Data (time-scaled, two-pass)

The amount of data scales by mode to ensure meaningful analysis windows regardless of upload frequency.

| Mode | Long-form window | Shorts window | Deep metadata on |
|------|-----------------|---------------|------------------|
| taster | Last 2 weeks | skip | Top 10 by views |
| standard | Last 30 days | Last 30 days | Top 20 + bottom 10 + 5 most recent |
| full | Last 90 days | Last 60 days | Top 20 + bottom 10 + 5 most recent |
| shorts | skip | Last 60 days | Top 20 + bottom 10 + 5 most recent |
| vs | Last 30 days each | Last 30 days each | Top 15 per channel |

### Pass 1 — Fast scan

Get ALL videos in the time window (title, views, duration, URL only). Calculate the `--dateafter` value from today's date.

```bash
yt-dlp --flat-playlist --dateafter [YYYYMMDD] --print "%(title)s|||%(view_count)s|||%(duration_string)s|||%(webpage_url)s" "[CHANNEL_URL]/videos" 2>/dev/null
```

If that returns nothing, try without `/videos`. If still nothing: "No public videos found on this channel yet."

### Pass 2 — Deep metadata

Only fetch individually for the selected subset (top by views + bottom + most recent). This keeps things fast while getting descriptions, tags, captions, likes, and dates where they matter.

```bash
yt-dlp --print "%(title)s|||%(view_count)s|||%(duration_string)s|||%(webpage_url)s|||%(upload_date)s|||%(like_count)s|||%(description)s|||%(tags)s|||%(subtitles)s|||%(automatic_captions)s" --skip-download "[VIDEO_URL]" 2>/dev/null
```

### Channel metadata

```bash
yt-dlp --print "%(channel)s|||%(channel_follower_count)s|||%(channel_url)s" --playlist-end 1 "[CHANNEL_URL]/videos" 2>/dev/null
```

### Playlists (standard + full only)

```bash
yt-dlp --flat-playlist --print "%(playlist_title)s|||%(webpage_url)s" "[CHANNEL_URL]/playlists" 2>/dev/null
```

### Shorts (standard + full, or shorts flag)

Fetch from the Shorts tab with the same date filter:
```bash
yt-dlp --flat-playlist --dateafter [YYYYMMDD] --print "%(title)s|||%(view_count)s|||%(duration_string)s|||%(webpage_url)s" "[CHANNEL_URL]/shorts" 2>/dev/null
```

---

## Step 3: Parse & Calculate

For every video:
- Split on `|||`, convert views/likes to integers (treat NA as 0)
- Parse upload_date (YYYYMMDD) → calculate days since upload
- **Views/day**: `views / max(days_since_upload, 1)`
- **Engagement rate**: `(likes / views) * 100`
- **Views/minute**: `views / duration_in_minutes`
- Group by primary topic/brand (topic clustering)
- Extract hashtags from descriptions
- Detect chapters/timestamps in descriptions
- Flag caption/subtitle availability
- Separate Shorts from long-form
- Sort by views descending

---

## Step 4: Channel Overview

Display a snapshot table:

| Metric | Value |
|--------|-------|
| Channel | [name] ([N] subscribers) |
| Videos analysed | [N] long-form, [N] Shorts |
| Date range | [earliest date] – [latest date] |
| Average views | [N] |
| Median views | [N] |
| Avg engagement rate | [N]% |
| Upload frequency | every [N] days (~[N]/day) |
| Top video | [title] ([N] views) |
| Most engaging | [title] ([N]% engagement) |

For standard and full modes, also use WebSearch to look up the channel's niche CPM range and include:
| Estimated niche CPM | $[N]–$[N] |

---

## Step 5: Channel Page SEO Audit

*Standard + full modes only.*

Evaluate the channel's page-level SEO:
- **About section**: Do the first 150 characters contain niche keywords? (This shows in search results)
- **Channel keywords**: Are they set and relevant?
- **Channel trailer**: Does one exist?
- **Banner**: Does it communicate the value prop and upload schedule?
- **Links**: Social links, website present?

Score: /5. Provide specific fixes for anything scoring below 3.

---

## Step 6: Topical Authority Score

Count unique topics across all videos. Calculate what % fall within the primary niche.

- **Specialist** (>80% one niche): Strong authority signal. YouTube's algorithm rewards this — niche channels grow 3.7x faster.
- **Focused** (60-80%): Good but could tighten.
- **Scattered** (<60%): Fragmented authority. Flag this as a problem.

---

## Step 7: Key Insights

Produce 5-7 specific, data-driven observations. Be specific — use actual numbers. Never write generic statements like "engaging content performs well."

Analyse ALL of the following:

**Performance tiers:**
- Hit (>2x median), Solid (1x-2x median), Underperformer (<0.5x median)
- List titles in each tier

**Topic analysis:**
- Which keywords/topics appear in top performers vs bottom?
- Average views across all videos vs top 5 — how skewed?

**Duration analysis:**
- Long-form vs short-form performance
- Views/minute — which lengths are most efficient?
- Outliers — massively over or underperforming

**Title patterns:**
- Title length: top 5 avg vs bottom 5 avg
- Power words: "NEW", "INSANE", "FREE", "DESTROYS", numbers
- Emoji impact: avg views with vs without
- Question vs statement

**Momentum:**
- Views/day of 5 most recent vs 5 oldest — growing, stable, or declining?
- Any recent videos gaining traction fast?

---

## Step 8: Content Saturation & Cannibalisation

*Standard + full modes only.*

Group all videos by primary topic/tool. For each topic with 3+ videos:
- Count of videos
- Average views
- View trend from first to last upload (ascending = growing interest, descending = saturated)
- **Same-day upload collision**: Flag videos on the same topic uploaded within hours — they split the same subscribers' feed slots

| Topic/Tool | # Videos | Avg Views | Trend (1st → Last) | Status |
|------------|----------|-----------|---------------------|--------|
| [topic] | [N] | [N] | [views] → [views] ↑/↓ | SATURATED / WATCH / GROWING |

- **Saturation score**: 1-5 (1 = diverse, 5 = heavily repetitive)
- **Cannibalisation warnings**: Specific pairs/groups competing
- **Advice**: For each saturated topic: retire / reduce frequency / double down (with reasoning)

In taster mode: Show the saturation score and topic groupings but withhold the retire/reduce/double-down advice.

---

## Step 8b: Content Format Analysis

*Full mode only.*

Categorise each video by FORMAT: News/Update, Tutorial, Comparison, Review, Reaction, Walkthrough, Listicle.

| Format | # Videos | Avg Views | Best Performer |
|--------|----------|-----------|----------------|
| News/Update | [N] | [N] | [title] |
| Tutorial | [N] | [N] | [title] |

- Which format performs best?
- Recommend a format mix (e.g. "80% news, 10% comparisons, 10% tutorials")
- Flag formats that consistently underperform

---

## Step 8c: Growth Trajectory & Timeline

*Standard + full modes only.*

Using the full time-window dataset, calculate weekly trends:

| Week | Period | Videos | Avg Views | Best Video |
|------|--------|--------|-----------|------------|
| 1 | [dates] | [N] | [N] | [title] ([N]) |

- Categorise: **Growing** / **Plateaued** / **Declining** / **Volatile**
- Weekly upload count trend
- Views per upload over time — getting more or less efficient?
- **Topic lifecycle**: When did each topic start? Peak? Decline?
- For full mode (90 days): detect seasonal patterns

---

## Step 9: Upload Strategy

*Standard + full modes only.*

- Current pace (videos/day or /week)
- Correlate volume with per-video performance
- Best performing day (if data spans multiple days)
- Volume vs quality trade-off calculation
- Note: research shows 1-2 great videos/week with strong retention outperforms daily posting with weak retention
- **Seasonal CPM**: Q4 spike (Oct-Dec), Q1 dip (Jan-Mar) — time high-value content for Q4
- Audience fatigue indicator
- **Recommended pace** with reasoning

In taster mode: Show the headline problem (e.g. "Publishing 12 videos/day may be cannibalising your views") but NOT the recommended pace.

---

## Step 10: Title SEO

*Standard + full modes only.*

For each of the top 10 videos:
- **Keyword positioning**: Primary keyword in first 3-5 words? (YouTube weights first 40 chars most)
- **Title length**: Optimal 50-70 chars. Flag <30 or >70 (truncated)
- **Search intent match**: Does it match what someone would type into YouTube search?
- **CTR appeal**: Score 1-5

| Video | Length | Primary Keyword | Position | Intent | CTR | Rewrite |
|-------|--------|-----------------|----------|--------|-----|---------|

Only suggest rewrites for CTR ≤3 or positioning issues.

---

## Step 11: Description SEO

*Standard + full modes only.*

For each top 10 video:
- **First 150 chars**: Contains keyword + hook? (This shows in search results)
- **Keyword density**: Natural usage?
- **Links**: Social, website, related videos?
- **Timestamps/chapters**: Present? (11% more watch time, enables Google rich results)
- **CTA**: Clear call to action?
- **Length**: <200 chars is a missed opportunity. Ideal: 200-500 words
- **Hashtags**: 2-3 focused + branded hashtags for cross-linking?

| Video | First 150 | Keywords | Timestamps | Links | CTA | Length | Score /10 |

**Recommended Description Template** for future videos:
Include: keyword-rich first 2 sentences, timestamp placeholder, CTA section, social/link section, 3-5 relevant hashtags.

---

## Step 12: Tag Analysis

*Standard + full modes only.*

For each top 10 video:
- **Number of tags** (YouTube allows up to 500 chars)
- **Relevance**: Do tags match the topic?
- **Mix**: 2-3 broad + 5-10 specific long-tail
- **Missing**: Obvious tags that should be there
- **Branded tags**: Consistent use of channel name tag for cross-linking?

Note: Tags mainly help with misspellings and related searches in 2026.

| Video | # Tags | Broad | Specific | Missing |

**Recommended Tag Template** for the channel's niche.

---

## Step 13: Thumbnail Audit

*Standard + full modes only.*

Can't scrape thumbnails via yt-dlp. Instead, use WebSearch to check the channel's thumbnail style and provide a 2026 best practices assessment:

- Max 4 words of text
- High contrast, readable on mobile (70%+ watch time is mobile)
- Expressive face visible
- Clean, high-contrast realism (red arrows/shocked faces are outdated in 2026)
- Consistent branding but not identical (identical thumbnails reduce CTR in suggested feeds)
- Mention YouTube's built-in A/B thumbnail testing feature

Provide specific recommendations.

---

## Step 14: Google AI Search Readiness

*Standard + full modes only.*

29.5% of Google AI Overviews cite YouTube — it's the #1 cited domain. Videos without chapters + captions are invisible to AI search.

For each top 10 video, check:
- Chapters/timestamps present? (rich results eligibility)
- Captions/transcript available? (AI engines parse transcripts for discovery)
- Structured description with keyword in first 150 chars? (featured snippet eligibility)

| Video | Chapters | Captions | Description | AI-Ready /3 |

Template for making future videos AI-search ready.

In taster mode: Mention how many videos are missing chapters/captions as an SEO problem, but don't provide the fix.

---

## Step 15: Captions & Localisation

*Full mode only.*

For each deep-metadata video, check:
- Auto-generated captions?
- Manual/uploaded captions (SRT)?
- Multi-language subtitles?

Impact: subtitled videos boost watch time 12-15%, 80% of viewers more likely to finish.

Recommend which languages to add based on likely audience geography. Flag videos with NO captions.

---

## Step 16: Playlist Strategy

*Standard + full modes only.*

Using the playlists fetched in Step 2:
- How many playlists exist? (Channels with 5+ organised playlists get 22% more session views)
- Are top-performing videos in playlists?
- Flag orphaned videos (not in any playlist)
- Playlist title keyword optimisation
- Recommend playlist groupings based on topic clusters from Step 8

Playlists boost session watch time — one of YouTube's strongest ranking signals.

---

## Step 17: Shorts Strategy

*Full mode, or when `shorts` flag is set.*

Using Shorts data from Step 2:
- Separate views/engagement analysis for Shorts
- Shorts algorithm signals: swipe-away rate, completion rate, replay rate (can't measure from outside but advise on optimisation)
- **Cross-promotion audit**:
  - Do Shorts preview/link to long-form content?
  - Are Shorts in playlists alongside related long-form?
  - Is the channel using Shorts for discovery → long-form for depth?
- Hashtag usage (up to 30 for Shorts vs 2-3 for long-form)
- Audio/trending sound usage
- Recommendations for the Shorts ↔ long-form funnel

---

## Step 18: Session Watch Time & Engagement

*Full mode only.*

Best-practice recommendations:
- **End screens**: 2 elements ("Best video" + "Subscribe") in last 5-20 seconds
- **Info cards**: 3-5 cards pointing to pillar playlists (30-70% more session watch time)
- **Pinned comments**: 40-60% more replies
- **Reply rate**: Responding to comments boosts engagement signals
- **Community tab**: Polls, updates, behind-the-scenes
- **CTA placement**: Verbal CTA at engagement peak, not just at the end

---

## Step 19: Video Structure Scoring

*Full mode only.*

For each deep-metadata video, estimate content quality signals:
- **Hook** (first 8 seconds — if viewer stays, YouTube dramatically increases recommendations)
- **Chapter structure** — clear sections?
- **Pattern breaks** — advised every 2-3 minutes for retention
- **Duration sweet spot** — based on channel data, which length range gets best views/minute?

Score /3 per video. Note: retention > raw watch time in 2026.

---

## Step 19b: Collaboration & Mention Detection

*Full mode only.*

Scan descriptions and titles for mentions of other creators/channels. Check for tags/links to other channels.

Videos featuring other creators get algorithmic boosts from cross-audience exposure. Flag if the channel is doing zero collaborations — it's a missed growth lever.

Recommend collaboration opportunities based on niche overlap.

---

## Step 20: Keyword Opportunities

*Standard + full modes.*

Use WebSearch to research YouTube search terms for the channel's niche:
- Search for "[niche] youtube 2026" to find trending queries
- Search for "youtube autocomplete [main topics]"

Also mine YouTube's own autocomplete:
```bash
yt-dlp "ytsearch10:[niche keyword]" --flat-playlist --print "%(title)s" 2>/dev/null
```

Identify 10-15 high-opportunity keywords:

| Keyword / Topic | Est. Demand | Competition | Already Covered? | Opportunity |

---

## Step 21: Competitor Benchmarking

*Standard + full modes.*

Use WebSearch to find 2-3 similar channels. For each:
- Channel name, subscriber count, recent avg views
- Topics/keywords they rank for that this channel doesn't
- Title/description pattern differences
- Content gaps this channel could fill

---

## Step 22: Trending Topics & Gaps

*Standard + full modes.*

Use WebSearch to find what's trending in the niche RIGHT NOW:
- Search for "trending [niche] 2026", "[niche] news this week"
- Compare against channel's recent coverage
- Flag missed opportunities ranked by urgency

| Trending Topic | Why It's Hot | Channel Coverage | Opportunity |

---

## Step 23: CPM/Revenue Optimisation

*Full mode only.*

Use WebSearch for the channel's niche CPM/RPM rates:
- High or low-value niche?
- Could content pivots target higher-CPM topics?
- Seasonal timing (Q4 > Q1)
- Ad-friendly content check (avoid demonetisation triggers)

---

## Step 23b: Embed & Backlink Audit

*Full mode only.*

Use WebSearch for "[channel name] youtube embed" and "[top video title]" to check external presence.

- Are any videos embedded on blogs/sites?
- External embeds give a ranking boost
- Recommend embedding strategy: own blog, guest posts, Reddit, Quora, forums
- Suggest which top videos to promote off-platform

---

## Step 23c: Re-optimisation Opportunities

*Full mode only.*

Cross-reference top-performing videos (high views) with weak metadata (poor descriptions, missing tags, no chapters, no captions). These are LOW EFFORT, HIGH IMPACT fixes.

| Video | Views | Missing | Action | Expected Impact |

Prioritise: videos with >2x median views but description score <5/10 or missing chapters/captions.

---

## Step 23d: Audience Overlap Detection

*Full mode only.*

Based on topic clusters, identify if the channel serves multiple distinct audiences (e.g. "AI tools" vs "SEO" vs "coding").

Fragmented audiences break YouTube's "watch multiple videos" signal. Recommend whether to consolidate or consider separate channels.

---

## Step 24: SEO Quick Wins

Prioritised list of actionable improvements. Each must reference specific videos or data.

- **Taster**: Skip this section entirely
- **Standard**: Top 10 quick wins
- **Full**: Top 20 quick wins

| Priority | Action | Impact | Effort | Details |

Draw actions from ALL sections: titles, descriptions, tags, thumbnails, AI readiness, playlists, Shorts, engagement, saturation, captions, embeds, re-optimisation, format mix, collaborations, audience overlap.

---

## Step 24b: Projected Impact Estimates

Calculate estimated uplift for each recommendation using the channel's own data + industry benchmarks. Use conservative ranges and label confidence levels.

**Calculation methods:**
- **Topic shift**: (high-performing topic avg - channel avg) × videos/week
- **Volume reduction**: Compare avg views at different posting rates from the channel's own data
- **Add chapters**: +11% watch time (YouTube published data) → estimated +5-10% more views
- **Add captions**: +12-15% watch time → estimated +200-500 views/video
- **Playlist organisation**: +22% session views (YouTube data)
- **Fix descriptions**: +5-15% search traffic per video
- **Title rewrites**: +10-20% views on rewritten videos

| Action | Estimated Uplift | Confidence | Based On |
|--------|-----------------|------------|----------|
| [action] | [range] | HIGH/MED | [channel data / industry benchmark / YouTube data] |

**Total projected monthly uplift:**
- Current: avg views × videos/month
- Projected: if all recommendations implemented
- Present as: "Implementing these changes could increase monthly views from ~X to ~Y (+Z%)"

**Mode-specific display:**
- **Taster**: Headline only — "You're potentially leaving ~X views/month on the table" + "Get the full audit to see the breakdown"
- **Standard**: Summary table + total
- **Full**: Per-action breakdown + summary + monthly projection

---

## Step 25: Next Video Suggestions

5 specific video ideas based on top performer patterns + keyword opportunities + trending topics.

Each includes:
- **Title**
- **Why it should work** (which pattern + keyword + trend it targets)
- **Suggested tags**
- **Description hook** (first 2 sentences)
- **Thumbnail direction** (4 words max text suggestion)
- **Target playlist**
- **Timing** (publish NOW if trending, or schedule)
- **Estimated CPM potential** (full mode only)

In taster mode: Skip this section entirely.

---

## Step 26: Channel Comparison (`vs` flag)

Only when `vs` flag is set. Replaces the standard flow.

Fetch 30 videos from EACH channel (last 30 days). Run the analysis for both.

Side-by-side comparison:

| Metric | Channel A | Channel B | Winner |
|--------|-----------|-----------|--------|

Compare: subscribers, avg views, median views, engagement rate, upload frequency, topical authority, saturation score, title SEO avg, description SEO avg.

- Topic overlap: what both cover, where they diverge
- What each does better that the other should steal
- Content gaps neither covers
- "If you're Channel A, here's how to beat Channel B" summary

---

## Step 27: 30-Day Content Calendar (`calendar` flag)

Only when `calendar` flag is set.

Based on keyword opportunities, trending topics, optimal upload frequency, seasonal CPM, and format mix.

| Day | Date | Title | Format | Target Keyword | Playlist | Priority |
|-----|------|-------|--------|----------------|----------|----------|

Include:
- Upload days vs rest days (based on recommended frequency)
- Format mix matching top-performer patterns
- Seasonal awareness (frontload high-CPM topics if approaching Q4)
- 1-2 experiment slots for testing new topics
- Shorts schedule alongside long-form
- Notes per video: why this title, thumbnail direction

---

## Step 28: Viral Potential Scoring

*Standard + full modes.*

Score each video 1-10:
- Trending topic? (+3)
- Engagement rate >2x channel avg? (+2)
- Strong views/day trajectory? (+2)
- "FREE" or high-CTR power word? (+1)
- Major brand name (Google, Nvidia, OpenAI)? (+1)
- Under 10 mins (shareable)? (+1)

Flag 7+ as "still has legs — promote externally". Flag 3- as "dead on arrival — learn why."

---

## Step 29: Risk Flags

*Full mode only.*

- **Demonetisation risk**: Scan for ad-unfriendly content in titles/descriptions
- **Copyright risk**: Flag heavy use of other creators' content without attribution
- **Community guidelines**: Misleading clickbait that could trigger review
- **Repetitive content penalty**: If saturation score is 4-5, warn about reduced recommendations

---

## Step 30: HTML Report (`html` flag)

Only when `html` flag is set.

Generate a styled HTML file saved to the working directory:
- Filename: `youtube-audit-[channel-name]-[date].html`
- Professional layout with colour-coded sections (green/amber/red for tiers and scores)
- Tables with alternating row colours
- Collapsible sections for longer audits
- Print-friendly CSS
- Footer: "Analysis by Wayne Pearce — AI & Automation Consultant"

Use the Write tool to save the file.

---

## Step 31: Auto-Email Draft (`email` flag)

Only when `email` flag is set.

1. WebSearch for the channel owner's email ("[channel name] email contact")
2. Draft a Gmail using `mcp__claude_ai_Gmail__gmail_create_draft`
3. Format depends on mode:
   - **Taster**: Concise email with key findings + projected impact headline + teaser of full audit
   - **Standard/Full**: Email with summary + key findings inline
4. Subject: "YouTube Channel Analysis: [X] Quick Wins for [Channel Name]"
5. Tone: Helpful outreach, not salesy. "I ran an analysis... thought you'd find this useful"
6. **Always include** the projected impact headline (e.g. "Based on your channel data, implementing the top 5 fixes alone could add an estimated 30,000-50,000 views/month")
7. End with a soft CTA
8. Return the Gmail draft URL

---

## Step 32: Output

Format the full report. Only include sections relevant to the selected mode. Only include bonus features when their flag is set.

### Taster output includes:
1. Channel Overview table
2. Top 10 Videos table (views, views/day, engagement, duration, date, link)
3. Performance Tiers (with video names)
4. 3-5 Key Insights with specific numbers
5. Content Saturation Score (topic groupings shown, but NO advice)
6. Upload Strategy headline (problem shown, but NO recommended pace)
7. 3 SEO Problems Identified — name the problem with data, DON'T give the fix
8. Projected Impact headline only ("You're potentially leaving ~X views/month on the table")
9. Teaser box:

```
---
### Want the full audit?
The complete SEO audit covers 60+ ranking factors including:
- Title rewrites for underperforming videos
- Custom description template for your niche
- Tag strategy with recommended tag sets
- Thumbnail review against 2026 best practices
- Google AI Search readiness check
- Playlist strategy to boost session watch time
- Shorts cross-promotion audit
- 20 prioritised quick wins ranked by impact vs effort
- 5 data-backed next video ideas with tags, descriptions, and thumbnail direction
- Competitor gap analysis
- Trending opportunities you're missing right now
- 30-day content calendar
- Projected impact estimates for every recommendation

Contact Wayne Pearce — AI & Automation Consultant
---
```

### Standard output includes:
Everything from taster (with fixes and advice unlocked) + SEO audit sections (Steps 10-14, 16, 20-22) + Quick Wins (10) + Impact estimates (summary) + Next Video suggestions + Viral scoring

### Full output includes:
Everything. All steps, all tables, all templates, all recommendations.

### Top 10 Videos table (all modes):

| # | Title | Views | Views/Day | Engagement | Duration | Uploaded | Link |
|---|-------|-------|-----------|------------|----------|----------|------|

Full mode adds: AI-Ready Score, Viral Score columns.

### Footer (all modes):
*Fetched [N] videos · [N] Shorts · Analysed [date] · Mode: [taster/standard/full]*
