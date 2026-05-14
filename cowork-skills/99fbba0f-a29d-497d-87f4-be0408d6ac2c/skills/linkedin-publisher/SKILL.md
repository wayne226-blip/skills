---
name: linkedin-publisher
description: >
  Writes and publishes LinkedIn posts in one flow. Use this skill whenever Wayne
  asks to "post to LinkedIn", "publish on LinkedIn", "put this on LinkedIn",
  "share this on LinkedIn", or any variation of wanting content published to his
  LinkedIn profile. Also triggers when he says "post this", "publish this" after
  writing a LinkedIn post, or "linkedin-publisher". Combines Wayne's voice and
  post-writing style with semi-automated publishing via the browser. If Wayne
  just wants to write a post without publishing, use the linkedin-post skill
  instead — this skill is for when he wants the post to actually go live.
---

# LinkedIn Publisher

Writes a LinkedIn post in Wayne's voice and opens it in his browser ready to publish. This is a two-phase skill: **write** then **publish**.

## Phase 1 — Write the Post

Follow the exact same writing process as the linkedin-post skill. Wayne's voice rules apply here identically:

### Determine the topic

Check $ARGUMENTS:
- If it contains a topic or text to post -> use that
- If the user has already written a post in this conversation -> use that
- If $ARGUMENTS is empty -> ask: "What's the post about?"

If the user provides an already-written post (e.g. "post this to LinkedIn: [text]"), skip writing and go straight to Phase 2.

### Wayne's Voice — The Non-Negotiables

Wayne's writing is direct, plain, and real. It sounds like a person, not a brand.

**Always:**
- Short sentences. Fragments are fine.
- Contractions: "don't" not "do not", "it's" not "it is"
- Own uncertainty honestly
- One idea per paragraph. White space matters.

**Never:**
- Hype words: game-changing, revolutionary, seamless, powerful, leverage, utilise, cutting-edge
- Performative openers: "Excited to share"
- Corporate signposting: "In this post I will..."
- Hashtag spam: 3 max, specific only
- Starting with a question

### Post Structure

**HOOK (line 1-2)** — Earns the click before "...see more"
**BODY (3-7 short paragraphs)** — Real examples, real numbers. No padding.
**LANDING (2-3 lines)** — A real insight or specific question.
**HASHTAGS** — 3 max. Specific (#buildinpublic, #AItools, #solobuilder).

### Write Two Versions

- **Version A** — Results/numbers hook (lead with a concrete metric or timeframe)
- **Version B** — Counterintuitive or honest-admission hook

Present both to Wayne. Ask which one to publish (or if he wants edits first).

## Phase 2 — Publish

Once Wayne picks a version (or provides/approves the text):

### Step 1: Save the post

Save to `/Users/wayne/Claude/linkedin-posts/` using the format `YYYY-MM-DD-[slug].md` (same as linkedin-post skill). Create the folder if needed.

### Step 2: Copy to clipboard and open LinkedIn

Run the publishing script:

```bash
python3 SKILL_DIR/scripts/publish.py --text "THE_POST_TEXT"
```

Replace `SKILL_DIR` with the actual path to this skill's directory. The script:
1. Copies the post text to the macOS clipboard
2. Opens LinkedIn's share dialog in the default browser

### Step 3: Tell Wayne what to do

After running the script, tell him:

> Post copied to your clipboard and LinkedIn is opening. Just:
> 1. Click in the post text area
> 2. Cmd+V to paste
> 3. Hit Post
>
> Saved to: `/Users/wayne/Claude/linkedin-posts/[filename].md`

That's it. Three clicks and it's live.

## Important Notes

- This skill deliberately uses a semi-automated approach rather than full browser automation. LinkedIn actively detects and restricts accounts that use Selenium/Playwright. The clipboard + open browser method is reliable and won't risk Wayne's account.
- If Wayne asks for full automation, explain the account restriction risk and recommend sticking with the clipboard approach.
- If Wayne has already written a post with the linkedin-post skill in this session, offer to publish that rather than rewriting.
