---
name: email-digest
description: >
  Daily email digest summarising what came in, what needs replies, and what's pending across
  Gmail and Outlook. Designed to run as a scheduled daily summary or on-demand. Use this skill
  whenever Wayne says "email digest", "daily digest", "daily email summary", "morning email
  briefing", "email briefing", "catch me up on email", "what did I miss in email",
  "email roundup", "summarise my emails", "summarize my emails", "end of day email summary",
  "email recap", or any variation of wanting a comprehensive summary of email activity.
  Also triggers on "morning briefing" or "daily briefing" when email context is clear,
  "what came in today", "what emails came in", or "email report". This skill goes deeper
  than inbox-summary — it reads email bodies and provides actual summaries of content,
  not just subject lines.
---

# Email Digest

Produce a comprehensive daily digest of Wayne's email activity across Gmail and Outlook. This goes deeper than the inbox-summary skill — it reads email content and provides actual summaries.

## Step 1 — Fetch emails from both accounts

Run these in parallel:

### Gmail
Use `gmail_find_email` to pull emails:
- Search: `newer_than:1d` (up to 30 results)
- Also search: `is:unread` (up to 20 results)
- Deduplicate

### Outlook
Use `microsoft_outlook_find_emails`:
- Search for emails from the last 24 hours (up to 30 results)
- Also search for unread emails (up to 20 results)
- Deduplicate

## Step 2 — Read and summarise key emails

For emails that look substantive (not automated notifications or marketing), read the email body to get the actual content. Skip reading bodies for obvious low-value emails like marketing, social notifications, and automated alerts.

For each substantive email, create a brief summary:
- Who it's from
- What it's about (2-3 sentences max)
- Whether it needs a reply or action
- Any deadlines or time-sensitive info mentioned

## Step 3 — Compile the digest

Structure the digest as a proper briefing document:

**Email Digest — [Today's Date]**

**Overview**: X new emails across Gmail and Outlook. Y need replies. Z are FYI.

**Needs Reply**
For each email needing a reply:
- **From**: [Sender] via [Gmail/Outlook]
- **Subject**: [Subject line]
- **Summary**: [2-3 sentence summary of content]
- **Action**: [What Wayne needs to do — reply, decide, approve, etc.]

**Key Updates** (important but no reply needed)
For each:
- **From**: [Sender] via [Gmail/Outlook]
- **Subject**: [Subject line]
- **Summary**: [1-2 sentence summary]

**Other** (newsletters, notifications, low-priority)
Brief grouped list — no need to summarise each one individually:
- X newsletters/marketing emails
- X automated notifications
- X social media updates
- List any that might be worth a look

**Pending Threads**
Any ongoing email threads where Wayne is waiting for a response:
- [Thread subject] — last sent [date], waiting on [person]

## Step 4 — Closing recommendation

End with a brief "Start here" recommendation:
- Which email to tackle first and why
- Rough time estimate if there's a lot to get through
- Flag anything that's been sitting unread for more than 2 days

## Rules
- British English spelling
- No emojis
- Read email bodies for substantive emails — this skill is meant to save Wayne from opening each one
- Group similar low-value emails rather than listing each one
- When run as a scheduled task, keep the output self-contained — it should make sense without any prior context
- If either account has no emails in the period, note it briefly
