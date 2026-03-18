# Skill Templates

Templates for the 12 client skills. Each skill is generated as a standalone SKILL.md file in the client's `/skills/[skill-name]/` folder.

All skills share this frontmatter format:

```yaml
---
name: [skill-name]
description: >
  [What it does]. [Unique output structure]. [Trigger phrases].
---
```

---

## Communication Skills

### Email Writer

```markdown
---
name: email-writer
description: >
  Write professional emails in {{BUSINESS_NAME}}'s brand voice. Produces
  a ready-to-send email with subject line, body, and sign-off. Triggers:
  "write an email", "draft a reply", "email to", "respond to this email".
---

# Email Writer

Write emails for {{BUSINESS_NAME}} using the brand voice from BRAND.md.

## Rules
- Always read BRAND.md before writing
- Use the email sign-off: {{EMAIL_SIGNOFF}}
- British English only
- {{TONE_DESCRIPTION}}
- {{INDUSTRY_COMPLIANCE_NOTES}}

## Output Format
1. **Subject line** — clear, concise
2. **Body** — appropriate length for context (short for follow-ups, longer for introductions)
3. **Sign-off** — always {{EMAIL_SIGNOFF}}

## When writing:
- Match formality to the recipient
- {{AUDIENCE_NOTES}}
- Keep it concise — no waffle
- Include a clear call to action where appropriate
```

### Customer Reply Handler

```markdown
---
name: customer-reply-handler
description: >
  Handle customer queries, complaints, and reviews in {{BUSINESS_NAME}}'s
  brand voice. Produces a professional, empathetic response. Triggers:
  "respond to this review", "handle this complaint", "reply to this customer",
  "customer query".
---

# Customer Reply Handler

Respond to customer messages, reviews, and complaints for {{BUSINESS_NAME}}.

## Rules
- Always read BRAND.md for tone
- Empathetic but professional
- Acknowledge the issue before solving it
- Never be defensive
- {{INDUSTRY_COMPLIANCE_NOTES}}

## For complaints:
1. Thank them for reaching out
2. Acknowledge the issue
3. Explain what you'll do / have done
4. Offer next steps
5. Sign off warmly

## For positive reviews:
1. Thank them genuinely (not generically)
2. Reference something specific they mentioned
3. Invite them back / to recommend
```

### Internal Comms Writer

```markdown
---
name: internal-comms-writer
description: >
  Write internal team communications for {{BUSINESS_NAME}}. Produces team
  updates, announcements, and memos in a clear, direct style. Triggers:
  "write a team update", "announce this internally", "draft an internal memo",
  "staff announcement".
---

# Internal Comms Writer

Write internal communications for {{BUSINESS_NAME}}'s team.

## Rules
- More casual than external comms, but still professional
- Clear, actionable, no corporate waffle
- Lead with the key information
- British English

## Output Format
- **Subject/title** — what this is about
- **Key message** — 1-2 sentences
- **Detail** — what people need to know
- **Action required** — what to do next (if anything)
```

---

## Sales Skills

### Proposal / Quote Writer

```markdown
---
name: proposal-writer
description: >
  Write proposals and quotes for {{BUSINESS_NAME}} in brand voice. Produces
  a structured proposal with scope, pricing, and next steps. Triggers:
  "write a proposal", "draft a quote", "put together a proposal for",
  "scope of work for".
---

# Proposal / Quote Writer

Write proposals and quotes for {{BUSINESS_NAME}}.

## Rules
- Read BRAND.md for tone and BUSINESS.md for services/pricing
- Professional, confident, clear
- Focus on value to the client, not just features
- {{INDUSTRY_COMPLIANCE_NOTES}}

## Structure
1. **Introduction** — who we are, reference to their need
2. **Understanding** — what they told us they need (shows we listened)
3. **Our Approach** — how we'll deliver
4. **Scope** — what's included (and what's not)
5. **Investment** — pricing, payment terms
6. **Timeline** — when they can expect delivery
7. **Next Steps** — how to proceed
```

### Follow-Up Sequence Writer

```markdown
---
name: follow-up-writer
description: >
  Write follow-up email sequences for {{BUSINESS_NAME}}. Produces a series
  of 2-4 follow-up emails spaced over time. Triggers: "write a follow-up",
  "chase this lead", "follow-up sequence", "they haven't replied".
---

# Follow-Up Sequence Writer

Write follow-up email sequences for {{BUSINESS_NAME}}.

## Rules
- Read BRAND.md for tone
- Never pushy — helpful and value-adding
- Each follow-up adds something new (don't just repeat)
- {{INDUSTRY_COMPLIANCE_NOTES}}

## Sequence Pattern
1. **Day 1-2**: Friendly check-in, reference original conversation
2. **Day 5-7**: Add value — share something useful related to their need
3. **Day 14**: Final follow-up — keep door open, no pressure
4. **(Optional) Day 30**: Reconnect with new angle or update
```

### Job Advert Writer

```markdown
---
name: job-advert-writer
description: >
  Write job adverts for {{BUSINESS_NAME}}. Produces inclusive, engaging job
  listings with clear requirements and benefits. Triggers: "write a job ad",
  "hiring for", "job listing for", "we're recruiting".
---

# Job Advert Writer

Write job adverts for {{BUSINESS_NAME}}.

## Rules
- Read BRAND.md for employer brand voice
- Inclusive language — no age, gender, ethnicity bias
- Clear on requirements vs nice-to-haves
- Lead with what makes the role/company attractive
- British English, salary in GBP

## Structure
1. **Headline** — role title + key selling point
2. **About us** — 2-3 sentences on the company
3. **The role** — what they'll be doing day-to-day
4. **What we're looking for** — requirements (essential vs desirable)
5. **What we offer** — benefits, salary, culture
6. **How to apply** — clear next steps
```

---

## Content Skills

### Social Media Post Writer

```markdown
---
name: social-media-writer
description: >
  Write social media posts for {{BUSINESS_NAME}} across platforms. Produces
  platform-appropriate posts with hashtag suggestions. Triggers: "write a post
  for Instagram", "LinkedIn post", "Facebook post", "social media post about",
  "draft a tweet".
---

# Social Media Post Writer

Write social media posts for {{BUSINESS_NAME}}.

## Rules
- Read BRAND.md for tone and visual identity
- Adapt format to platform (LinkedIn = longer/professional, Instagram = visual/casual, Facebook = community/conversational)
- British English
- {{INDUSTRY_COMPLIANCE_NOTES}}

## Per Platform
- **LinkedIn**: Professional, thought-leadership, 150-300 words, use line breaks, no hashtag overload (3-5 max)
- **Instagram**: Casual, visual-first, include caption + hashtag suggestions (10-15), mention if image needed
- **Facebook**: Conversational, community-focused, encourage comments, shorter than LinkedIn
- **X/Twitter**: Punchy, under 280 chars, optional thread format for longer content
```

### Newsletter Writer

```markdown
---
name: newsletter-writer
description: >
  Write newsletter content for {{BUSINESS_NAME}}. Produces structured email
  newsletter with sections, subject line, and preview text. Triggers: "write
  this week's newsletter", "draft an email campaign", "newsletter about",
  "email blast".
---

# Newsletter Writer

Write newsletters for {{BUSINESS_NAME}}.

## Rules
- Read BRAND.md for tone
- Scannable — use headers, short paragraphs, bullet points
- One clear CTA per newsletter
- Subject line + preview text included
- British English

## Structure
1. **Subject line** + **preview text**
2. **Opening** — hook or timely reference
3. **Main content** — 2-3 sections with clear headers
4. **CTA** — one clear action
5. **Sign-off** — personal, warm
```

### Blog / Long-Form Writer

```markdown
---
name: blog-writer
description: >
  Write blog posts and long-form content for {{BUSINESS_NAME}}. Produces
  SEO-aware articles with headers, meta description, and structured content.
  Triggers: "write a blog post about", "draft an article", "long-form content
  on", "write a guide about".
---

# Blog / Long-Form Writer

Write blog posts and long-form content for {{BUSINESS_NAME}}.

## Rules
- Read BRAND.md for tone, BUSINESS.md for expertise areas
- SEO-aware: include target keywords naturally, use H2/H3 headers
- Authoritative but accessible
- British English
- {{INDUSTRY_COMPLIANCE_NOTES}}

## Output Format
1. **Title** — engaging, keyword-rich
2. **Meta description** — under 160 characters
3. **Introduction** — hook + what they'll learn
4. **Body** — structured with H2/H3 headers, short paragraphs
5. **Conclusion** — summary + CTA
6. **Suggested internal links** — if applicable
```

---

## Admin Skills

### Meeting Notes Summariser

```markdown
---
name: meeting-summariser
description: >
  Summarise meeting notes into structured action points for {{BUSINESS_NAME}}.
  Produces summary with decisions, actions, and owners. Triggers: "summarise
  these notes", "write up this meeting", "meeting summary", "what was decided".
---

# Meeting Notes Summariser

Summarise meeting notes for {{BUSINESS_NAME}}.

## Rules
- Extract key decisions, actions, and owners
- Keep it concise — no padding
- Use bullet points
- British English

## Output Format
1. **Meeting** — date, attendees, purpose
2. **Key Decisions** — what was agreed
3. **Action Items** — who does what by when
4. **Notes** — anything else worth recording
```

### Report Writer

```markdown
---
name: report-writer
description: >
  Write reports and summaries for {{BUSINESS_NAME}}. Produces structured
  reports with clear sections and recommendations. Triggers: "write a weekly
  report", "produce a summary", "draft a report on", "monthly report".
---

# Report Writer

Write reports for {{BUSINESS_NAME}}.

## Rules
- Read BUSINESS.md for context
- Professional, data-driven where possible
- Clear structure with executive summary
- British English
- {{INDUSTRY_COMPLIANCE_NOTES}}

## Output Format
1. **Title and period**
2. **Executive summary** — 2-3 sentences
3. **Key metrics / highlights**
4. **Detail sections** — as needed
5. **Recommendations / next steps**
```

### Document Summariser

```markdown
---
name: document-summariser
description: >
  Summarise documents into concise key points for {{BUSINESS_NAME}}. Produces
  a structured summary with highlights and action items. Triggers: "summarise
  this document", "what are the key points", "TL;DR this", "break this down".
---

# Document Summariser

Summarise documents for {{BUSINESS_NAME}}.

## Rules
- Preserve key facts and figures
- Highlight anything that requires action
- Keep summaries under 500 words unless asked for more
- British English

## Output Format
1. **Document** — title, source, date
2. **Key Points** — bullet list of main findings/messages
3. **Action Required** — anything that needs a response or decision
4. **Full Summary** — 2-3 paragraph overview (if needed)
```
