---
name: linkedin-post
description: >
  Writes high-performing LinkedIn posts in Wayne Pearce's tone of voice. Use this
  skill whenever Wayne asks to write, draft, create, or generate a LinkedIn post —
  even if he just says "write a LinkedIn post about X", "make a post about X",
  "draft something for LinkedIn", or "LinkedIn post on [topic]". Also triggers when
  Wayne mentions pulling topics from Reddit, scraping a subreddit, or says things
  like "pull trending topics from r/entrepreneur" or "scrape reddit for post ideas".
  Always produces two versions: one with a results/numbers hook, one with a
  counterintuitive or honest-admission hook. Each post follows Wayne's voice —
  direct, plain, short sentences, contractions, no hype — under 300 words, 3 max hashtags.
---

# LinkedIn Post Generator

## Step 1 — Determine the topic source

Check $ARGUMENTS:

- If it mentions a subreddit (e.g. `r/entrepreneur`, `reddit`, `subreddit`) → run the **Reddit Topic Discovery** flow below
- If it contains a direct topic → skip to **Writing the Post**
- If $ARGUMENTS is empty → ask: "What's the post about? Or give me a subreddit to pull trending topics from (default: r/entrepreneur)"

---

## Reddit Topic Discovery

Use this when the user wants to pull trending topics from Reddit.

### 1. Fetch the data

Run this command, replacing SUBREDDIT with the name (default: `entrepreneur`).
For multiple subreddits, join with `+` (e.g. `entrepreneur+startups`):

```bash
curl -s \
  -H "User-Agent: WaynePearceLinkedIn/1.0" \
  "https://www.reddit.com/r/SUBREDDIT/hot.json?limit=25"
```

### 2. Parse and format as JSON

After fetching, extract the top posts with this Python snippet:

```bash
python3 - <<'EOF'
import json, sys

raw = sys.stdin.read()
data = json.loads(raw)
posts = data['data']['children']

results = []
for post in posts:
    p = post['data']
    if p.get('stickied'):
        continue
    results.append({
        "rank": len(results) + 1,
        "title": p['title'],
        "score": p['score'],
        "comments": p['num_comments'],
        "flair": p.get('link_flair_text') or '',
        "url": "https://reddit.com" + p['permalink']
    })
    if len(results) >= 10:
        break

print(json.dumps(results, indent=2))
EOF
```

Pipe them together:
```bash
curl -s -H "User-Agent: WaynePearceLinkedIn/1.0" \
  "https://www.reddit.com/r/SUBREDDIT/hot.json?limit=25" | python3 -c "
import json, sys
data = json.load(sys.stdin)
posts = data['data']['children']
results = []
for post in posts:
    p = post['data']
    if p.get('stickied'): continue
    results.append({'rank': len(results)+1, 'title': p['title'], 'score': p['score'], 'comments': p['num_comments'], 'flair': p.get('link_flair_text') or ''})
    if len(results) >= 10: break
print(json.dumps(results, indent=2))
"
```

### 3. Present the topics

Display the results as a clean numbered list:

```
Trending topics from r/SUBREDDIT:

1. [title] — score: X | comments: Y
2. [title] — score: X | comments: Y
...
```

Then ask: **"Which topic do you want to turn into a LinkedIn post? Pick a number or describe it."**

### 4. Once the user picks a topic

Use the Reddit post title and any relevant context as the subject.
Interpret it through Wayne's lens — what's the angle that connects this topic
to his experience as a solo builder, AI builder, or KDP publisher?

Don't just regurgitate the Reddit topic. Extract the underlying idea and
make it Wayne's own take on it.

Then continue to **Writing the Post** below.

---

## Writing the Post

Write two LinkedIn posts for Wayne on the chosen topic.

### Wayne's Voice — The Non-Negotiables

Wayne's writing is direct, plain, and real. It sounds like a person, not a brand.

**Always:**
- Short sentences. Fragments are fine. Get in. Say the thing. Get out.
- Contractions: "don't" not "do not", "it's" not "it is"
- Own uncertainty honestly — say "I don't know yet" rather than faking authority
- One idea per paragraph. White space is not wasted space.
- Say the thing clearly the first time. Don't repeat for emphasis.

**Never:**
- Hype words: game-changing, revolutionary, seamless, powerful, leverage, utilise, cutting-edge
- Performative openers: "I've been heads-down building furiously", "Excited to share"
- Corporate signposting: "In this post I will...", "To summarise the above..."
- Generic closers: "What do you think?" as the only ending
- Hashtag spam: 3 max, only specific and relevant ones
- Starting with a question

### Post Structure

**LINE 1–2 (THE HOOK)** — Shows before "...see more". Must earn the click.

**BODY (3–7 short paragraphs)** — Deliver on the hook. Real examples, real numbers.
No padding. Cut anything that doesn't add value.

**LANDING (2–3 lines)** — A real insight or a specific question. The last line sticks.

**HASHTAGS** — 3 max. Specific (#buildinpublic, #AItools, #solobuilder).
Never generic (#success, #mindset, #entrepreneur).

### Version A — Results / Numbers Hook

Lead with a concrete outcome, metric, or timeframe.

Examples:
- "I published 4 children's books in 6 weeks. Here's the actual process."
- "3 hours. That's how long it took to go from idea to published PDF."

### Version B — Counterintuitive or Honest Admission Hook

Open with something that challenges an assumption, or admits something real.

Examples:
- "Most people build with AI to move faster. That's not why I do it."
- "I started learning to code 6 months ago. I still can't explain recursion."

### Output Format

```
---
VERSION A — [brief hook description]
---

[post text with line breaks as it would appear on LinkedIn]

[hashtags]

---
VERSION B — [brief hook description]
---

[post text with line breaks as it would appear on LinkedIn]

[hashtags]
```

### Before You Finalise

- Does line 1 make someone want to read line 2?
- Does every paragraph earn its place?
- Does it sound like a person in Walthamstow, not a LinkedIn influencer?
- No hype words snuck in?
- Under 300 words each?

---

## Save Output — Always Required

After writing the posts, **always** save them to a markdown file. Do this automatically — no need to ask.

### File location

```
/Users/wayne/Claude/linkedin-posts/
```

Create the folder if it doesn't exist.

### Filename format

```
YYYY-MM-DD-[slug].md
```

Where `[slug]` is 2–4 words from the topic, lowercase, hyphenated.

Example: `2026-03-08-claude-vs-chatgpt.md`

### File contents

Use this template exactly:

```markdown
# LinkedIn Post — [Topic]

Date: YYYY-MM-DD

---

## Version A — [brief hook description]

[full post text, line breaks preserved]

[hashtags]

---

## Version B — [brief hook description]

[full post text, line breaks preserved]

[hashtags]
```

### After saving

Tell Wayne the file path so he can find it:

> Saved to: `/Users/wayne/Claude/linkedin-posts/YYYY-MM-DD-[slug].md`

---

## Repurpose for Other Platforms

After presenting the LinkedIn posts, ask:

> **Want me to repurpose this for other platforms?** (X, Bluesky, Threads — or all)

If yes, take the **chosen LinkedIn version** (A or B) and adapt it for the requested platforms.

### Platform Rules

**X / Twitter:**
- 280 chars per tweet. If the post needs more, create a thread (max 5 tweets).
- Thread format: number each tweet (1/5, 2/5, etc.)
- First tweet must hook — it's the only one most people see
- No hashtags in the thread body. 1-2 hashtags on the final tweet only
- Cut any padding ruthlessly. X rewards density

**Bluesky:**
- 300 chars per post. Use a thread if needed (max 4 posts)
- More conversational than X — slightly looser tone is fine
- No hashtags (Bluesky doesn't use them meaningfully yet)
- Can include a link in the last post if relevant

**Threads:**
- 500 chars per post
- Single post preferred — threads are less common here
- Slightly more casual than LinkedIn, same directness
- 1-2 hashtags max, only if genuinely relevant
- Works well for hot takes and short observations

### Voice — Same Rules Apply

Wayne's voice doesn't change across platforms. Same directness, same contractions, same no-hype rule. The only thing that changes is length and structure.

### Output Format

```
---
X / TWITTER — [thread or single tweet]
---

[tweet text, numbered if thread]

---
BLUESKY — [thread or single post]
---

[post text]

---
THREADS
---

[post text]

[hashtags if any]
```

### Save Repurposed Versions

Append the repurposed versions to the **same file** that was already saved for the LinkedIn post. Add them under a new heading:

```markdown
---

## Repurposed Versions

### X / Twitter
[content]

### Bluesky
[content]

### Threads
[content]
```
