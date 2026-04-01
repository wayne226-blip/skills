---
name: email-tone-rewriter
description: Rewrites draft emails in multiple tones — direct, warm, formal, and assertive — to help the user pick the version that fits their situation. Use this skill whenever the user pastes or describes an email and wants it rewritten, improved, or adjusted in tone. Trigger on phrases like "rewrite this email", "make this email more professional", "soften this message", "make this more direct", "help me say this differently", "how should I word this email", or any time the user shares email text and wants tonal or stylistic alternatives. Also trigger when the user wants to send a tricky, sensitive, or high-stakes message and isn't sure how to phrase it — even if they don't explicitly say "tone". If there's an email in the conversation and the user wants help with it, use this skill.
---

# Email Tone Rewriter

## Purpose
Take a draft email (or rough idea) and produce multiple polished rewrites in different tones, so the user can choose the version that best fits their situation and relationship with the recipient.

---

## When to use this skill
- User pastes a draft email and wants improvements or alternatives
- User describes what they want to say and asks for help wording it
- User says "make this more X" (professional, warm, firm, friendly, etc.)
- User has a tricky/sensitive message and isn't sure how to phrase it
- User wants to see different options before sending

---

## Workflow

### Step 1: Understand the context
Before rewriting, quickly extract or infer:
- **What's the email about?** (what's the core ask/message)
- **Who is the recipient?** (boss, colleague, client, vendor, stranger?)
- **What's the relationship?** (close, formal, strained, new?)
- **What outcome does the user want?** (action, acknowledgement, resolution?)

If the email is ambiguous or context is missing, ask ONE clarifying question. Otherwise, proceed directly.

### Step 2: Produce four rewrites

Always generate all four tone variants unless the user specifies otherwise. Use the `message_compose_v1` tool to present the variants cleanly.

**The four tones:**

#### 🎯 Direct
- Gets to the point immediately
- No filler phrases ("I hope this email finds you well", "Just wanted to check in")
- Short sentences, clear ask up front
- Confident but not rude
- Best for: busy recipients, internal comms, follow-ups

#### 🤝 Warm
- Opens with a personal or friendly touch
- Collaborative language ("I'd love to", "Would you be open to", "Happy to help")
- Softens asks and avoids anything that could feel demanding
- Maintains a positive, relationship-first tone
- Best for: building rapport, sensitive situations, new relationships

#### 📋 Formal
- Professional register throughout
- Full sentences, no contractions
- Polite but impersonal ("Please find", "I would appreciate", "Kindly")
- Appropriate for legal, HR, exec-level, or external business correspondence
- Best for: official matters, unfamiliar recipients, high-stakes situations

#### 💪 Assertive
- Confident, clear, and firm without being aggressive
- States needs/expectations plainly ("I need", "This requires", "Please confirm by")
- Doesn't hedge or over-apologise
- Still respectful, but leaves no doubt about what is expected
- Best for: escalations, when previous messages were ignored, setting boundaries

### Step 3: Add a brief guide
After the four variants, include a short 2–3 line note that tells the user:
- Which tone might work best given their situation (if you can infer it)
- Any nuance worth flagging (e.g., "the assertive version may feel strong if your relationship is new")

---

## Quality Rules

- **Preserve the core message** — never change what the email is actually asking for
- **Match the length to the tone** — Direct = short; Formal = can be longer; Warm = medium
- **Keep subject lines sharp** — one clear line, no vague subjects like "Follow-up"
- **Don't add fluff** — avoid filler openers like "I hope you're well" unless it genuinely fits the warm version
- **Don't remove critical info** — if the original has a deadline, amount, or specific ask, keep it in all versions
- **Read between the lines** — if the original email sounds frustrated or passive-aggressive, acknowledge it internally and produce cleaner versions that achieve the same goal professionally

---

## Example

**User input:**
> "Hey can you rewrite this? 'Hi John, just following up again on the invoice from last month, I've sent a few emails already and haven't heard back, it would be great if you could pay it soon, thanks'"

**Expected output:** Four clean variants using `message_compose_v1` — Direct (short, firm ask with deadline), Warm (collegial, assumes positive intent), Formal (professional language, references prior communications), Assertive (states what's needed and by when, mentions next steps if unpaid).

---

## Notes
- If the user only wants one or two specific tones, produce only those
- If the user provides context like "my boss" or "a difficult client", lean into that when selecting which tone to highlight in the guide
- If the draft email is actually good already, say so and offer minor polish rather than full rewrites
