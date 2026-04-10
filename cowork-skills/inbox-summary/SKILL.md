---
name: inbox-summary
description: >
  Quick inbox summary showing unread/recent emails — count, senders, subjects, and urgency.
  Works across both Gmail and Outlook. Use this skill whenever Wayne says "check my email",
  "what's in my inbox", "any new emails", "inbox summary", "email summary", "what emails
  do I have", "anything new in email", "check emails", "email check", "show me my emails",
  "unread emails", or any variation of wanting a quick overview of recent email activity.
  Also triggers on "how many emails", "who's emailed me", "any urgent emails", or just
  "emails" when the intent is clearly to see what's come in. Even casual mentions like
  "anything I need to look at in email" should trigger this skill.
---

# Inbox Summary

Provide Wayne with a quick, scannable overview of his recent emails across Gmail and Outlook.

## Step 1 — Fetch emails from both accounts

Run these in parallel:

### Gmail
Use `gmail_find_email` to search for recent unread emails:
- Search for unread emails: query `is:unread`
- Then search for recent emails from today: query `newer_than:1d`
- Limit to 20 results max

### Outlook
Use `microsoft_outlook_find_emails` to search for recent emails:
- Search for unread emails
- Then search for recent emails from today
- Limit to 20 results max

## Step 2 — Compile the summary

Present a clean, scannable summary grouped by account. Use this format:

Start with a one-line status: e.g. "You've got 5 unread in Gmail and 3 in Outlook."

Then for each account, list the emails briefly:

**Gmail** (X unread)
- [Sender] — Subject line (time received if available)
- Flag anything that looks urgent or time-sensitive

**Outlook** (X unread)
- [Sender] — Subject line (time received if available)
- Flag anything that looks urgent or time-sensitive

## Step 3 — Highlight what needs attention

At the end, add a brief "Needs attention" section if any emails look:
- Time-sensitive (meeting invites, deadlines mentioned in subject)
- From important/recurring contacts
- Flagged as high importance
- Reply-needed (RE: threads, questions in subject)

If nothing stands out, just say "Nothing urgent — you're clear."

## Rules
- Keep it concise — this is a quick glance, not a deep dive
- British English spelling
- No emojis
- Don't read full email bodies unless Wayne asks — just subjects and senders
- If either account returns no results, say so briefly rather than skipping it
