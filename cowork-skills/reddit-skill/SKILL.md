---
name: reddit-skill
description: >
  Use this skill whenever the user wants to search Reddit, browse subreddits, read post comments, or research what people are saying about a topic on Reddit. Trigger on any mention of "Reddit", "subreddit", "r/", posts, threads, or upvotes. Also trigger when the user wants to research a topic and understand public opinion, community discussion, or trending conversations — even if they don't say "Reddit" explicitly. Use this skill for tasks like: "what does Reddit think about X", "find me the top posts in r/investing", "summarise the comments on this Reddit thread", "research what people say about Y", or "pull posts from r/technology this week". If the user wants data from Reddit in any form, use this skill.
---

# Reddit Skill

This skill lets you search Reddit, browse subreddits, fetch post comments, and research topics — all using the free Reddit API. It covers four core workflows: searching posts, fetching subreddit feeds, reading comment threads, and producing research summaries.

## Setup: Reddit API Credentials

The Reddit API uses OAuth2. Users need a free Reddit app to get credentials.

**If the user hasn't set up API credentials yet**, walk them through this before running any code:

1. Log into Reddit and go to: https://www.reddit.com/prefs/apps
2. Click **"create another app..."** at the bottom
3. Fill in:
   - **Name**: anything (e.g. "MyClaudeApp")
   - **Type**: select **script**
   - **Redirect URI**: `http://localhost:8080`
4. Click **"create app"**
5. Note down:
   - **client_id**: the short string shown just below the app name
   - **client_secret**: the longer string labeled "secret"

These two values plus a user agent string are all the script needs. No login required for read-only access.

## How to interact with the Reddit API

Use Python with the `requests` library (no PRAW needed — keeps it lightweight). The Reddit API uses app-only OAuth for public read-only access.

### Authentication (app-only OAuth)

```python
import requests

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
USER_AGENT = "ClaudeRedditSkill/1.0"

def get_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": USER_AGENT}
    r = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth, data=data, headers=headers
    )
    return r.json()["access_token"]

def reddit_headers(token):
    return {"Authorization": f"bearer {token}", "User-Agent": USER_AGENT}
```

### Key API endpoints

| Task | Endpoint |
|------|----------|
| Search all of Reddit | `GET https://oauth.reddit.com/search?q={query}&sort=relevance&limit=25` |
| Search within a subreddit | `GET https://oauth.reddit.com/r/{sub}/search?q={query}&restrict_sr=1&limit=25` |
| Subreddit feed (hot/new/top) | `GET https://oauth.reddit.com/r/{sub}/{sort}?limit=25&t={timeframe}` |
| Post comments | `GET https://oauth.reddit.com/r/{sub}/comments/{post_id}` |
| Subreddit info | `GET https://oauth.reddit.com/r/{sub}/about` |

**Timeframe options** (`t` param): `hour`, `day`, `week`, `month`, `year`, `all`

**Sort options**: `hot`, `new`, `top`, `rising`, `relevance` (for search), `confidence` (for comments)

### Parsing post data

Each post in the response lives under `data.children[].data`. Key fields:

```python
post = item["data"]
title     = post["title"]
score     = post["score"]          # upvotes minus downvotes
url       = post["url"]
permalink = "https://reddit.com" + post["permalink"]
selftext  = post["selftext"]       # body text (empty for link posts)
num_comments = post["num_comments"]
subreddit = post["subreddit"]
created   = post["created_utc"]    # Unix timestamp
```

## Workflow 1: Search Reddit Posts

When the user wants to find posts matching a keyword or phrase:

1. Authenticate and run a search query
2. Return the top results with title, subreddit, score, comment count, and link
3. If the user specified a subreddit, restrict the search to it (`restrict_sr=1`)
4. Sort by relevance by default; offer `top` or `new` as alternatives

**Good output format:**
```
**[Post Title](https://reddit.com/r/sub/permalink)**
r/subreddit · ⬆ 1,234 · 56 comments

Short summary of the post content if available...
```

## Workflow 2: Fetch Subreddit Feed

When the user wants to browse a subreddit (e.g. "show me top posts from r/investing this week"):

1. Determine sort (`hot`, `new`, `top`) and timeframe (`day`, `week`, `month`, etc.)
2. Default to `hot` if not specified
3. Fetch and display posts with title, score, comment count, and link
4. Optionally include a brief description of what each post is about

## Workflow 3: Get Comments on a Post

When the user shares a Reddit URL or asks about a specific post's discussion:

1. Extract the post ID from the URL (the alphanumeric string after `/comments/`)
2. Fetch the post and its top-level comments
3. Sort by `confidence` (best) by default
4. Present the post summary first, then the top comments
5. For long threads, fetch the top 10–15 comments and summarise the overall sentiment

**Parsing comments:** Comments live in the second element of the response array (`response[1]["data"]["children"]`). Each comment's text is in `data.body`. Skip `"kind": "more"` items (these are "load more" placeholders).

## Workflow 4: Research & Summarise a Topic

When the user wants to understand what Reddit thinks about something (e.g. "what does Reddit say about standing desks?"):

1. Run a broad search across Reddit for the topic
2. Also fetch from 1–2 relevant subreddits if identifiable (e.g. "standing desks" → r/standingdesk, r/WorkSetups)
3. Pull top comments from the highest-scoring posts
4. Synthesise a summary: common opinions, recurring themes, notable advice or warnings
5. Include links to the most relevant threads so the user can dive deeper

**Good structure for a research summary:**
- **What people generally think** (2–3 sentences)
- **Common themes** (key points that come up repeatedly)
- **Noteworthy perspectives** (minority views, expert comments, cautionary tales)
- **Recommended threads** (top 3 links with brief descriptions)

## Error handling

- **401 Unauthorized**: credentials are wrong — ask the user to double-check their client_id and secret
- **403 Forbidden**: the subreddit may be private or quarantined — let the user know
- **404**: subreddit or post doesn't exist
- **429 Too Many Requests**: rate limited — wait a moment and retry once, then inform the user
- **Empty results**: tell the user and suggest a broader search term or different subreddit

## Rate limits

The free Reddit API allows approximately 100 requests per minute. For most tasks this is more than enough. If doing a large research summary (searching + fetching comments from multiple posts), batch requests efficiently and avoid fetching more data than needed.

## Tips for good output

- Always include clickable links back to Reddit — users often want to read the original
- Show upvote scores — they signal community consensus
- When summarising comments, attribute interesting quotes with the commenter's username (e.g. `u/username said: "..."`)
- For research tasks, be clear about recency — note if posts are from this week vs. last year
- If the user's query is ambiguous (e.g. "python" could mean the language or the snake), note the ambiguity and ask or pick the most likely interpretation
