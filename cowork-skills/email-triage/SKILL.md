---
name: email-triage
description: >
  Categorise and prioritise emails across Gmail and Outlook. Sorts emails into action-needed,
  FYI, and low-priority buckets with clear next steps. Use this skill whenever Wayne says
  "triage my email", "triage my inbox", "prioritise my emails", "sort my emails",
  "categorise my inbox", "what needs a reply", "which emails need action", "email priorities",
  "organise my inbox", "what should I respond to", "inbox triage", "email triage", or any
  variation of wanting emails sorted by importance or action required. Also triggers on
  "help me deal with my inbox", "inbox zero", "clear my inbox", "what can I ignore",
  "which emails matter", or "go through my emails". Even casual requests like "my inbox is
  a mess, help" should trigger this skill.
---

# Email Triage

Sort Wayne's emails across Gmail and Outlook into clear priority buckets so he knows exactly what to act on, what to skim, and what to skip.

## Step 1 — Fetch emails from both accounts

Run these in parallel:

### Gmail
Use `gmail_find_email` to pull recent emails:
- First search: `is:unread` (up to 25 results)
- Second search: `newer_than:2d` (up to 25 results)
- Deduplicate by subject/sender

### Outlook
Use `microsoft_outlook_find_emails` to pull recent emails:
- Search for unread emails (up to 25 results)
- Search for emails from the last 2 days (up to 25 results)
- Deduplicate by subject/sender

## Step 2 — Read subjects and metadata

For each email, note:
- Sender name and address
- Subject line
- Whether it's unread
- Whether it's flagged/starred
- Whether it's part of a thread (RE:, FW:)
- Time received
- Any importance markers

## Step 3 — Categorise into buckets

Sort every email into one of these categories:

### Action Required
Emails that need Wayne to do something — reply, make a decision, complete a task, attend something. These go first.

Signals: direct questions, requests, meeting invites, deadlines, "please", "can you", "need your", action verbs in subject.

### Waiting / Follow-up
Emails where Wayne is waiting on someone else, or threads he's already replied to that have new activity.

Signals: RE: threads where Wayne was last to reply, automated confirmations, "we'll get back to you".

### FYI / Read Later
Informational emails worth knowing about but no action needed right now.

Signals: newsletters, team updates, CC'd emails, announcements, reports, digests.

### Low Priority / Skip
Promotional emails, automated notifications, marketing, anything Wayne can safely ignore.

Signals: unsubscribe links, "noreply@", promotional language, social media notifications.

## Step 4 — Present the triage

Format the output clearly:

Start with a one-line summary: e.g. "Triaged 18 emails — 4 need action, 3 FYI, rest is noise."

Then list each bucket with the emails in it:

**Action Required** (X emails)
For each: [Account: Gmail/Outlook] [Sender] — Subject — *Brief note on what's needed*

**Waiting / Follow-up** (X emails)
For each: [Account] [Sender] — Subject — *What you're waiting on*

**FYI / Read Later** (X emails)
For each: [Account] [Sender] — Subject

**Low Priority / Skip** (X emails)
For each: [Account] [Sender] — Subject

## Step 5 — Suggest next steps

End with a brief recommendation:
- "I'd start with [sender]'s email about [topic] — looks time-sensitive."
- If there are emails that could be archived/deleted, mention it
- If Wayne asks, offer to draft replies to any action-required emails

## Rules
- Keep descriptions brief — one line per email max
- British English spelling
- No emojis
- Don't read full email bodies by default — use subjects and metadata to categorise
- If Wayne asks to dig into a specific email, then read the full body
- If either account has no emails, note it briefly
