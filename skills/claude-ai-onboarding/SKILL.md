---
name: claude-ai-onboarding
description: >
  Generate a complete claude.ai Project setup package for a small business client
  who uses the claude.ai web app (Pro or Teams), NOT Claude Code or Cowork. Takes
  discovery call intake data and produces output saved to /client-brains/[name]/:
  project-instructions.md (under 8,000 chars for the Project Instructions field),
  /knowledge/ folder with brand-summary.md and use-case templates to upload as
  Project Knowledge, setup-guide.md (client-facing how-to with tailored example
  prompts), and qa-report.md with assumptions log. Optionally generates multiple
  Projects split by use case (e.g., Email Brain, Social Media Brain, Sales Brain).
  Supports 7 industry verticals (estate agents, accountants, recruitment, solicitors,
  retailers, tradespeople, coaches/consultants) with pre-loaded terminology, compliance,
  and tone defaults. Use this skill whenever Wayne says "set up a claude.ai project
  for", "create project instructions for", "onboard a client onto claude.ai",
  "claude.ai brain", "project setup for [business]", "web app brain", "project
  instructions for a client", or provides discovery call data for a client who uses
  the claude.ai web app. Do NOT use for Claude Code or Cowork installs (that is
  claude-code-onboarding), for writing individual content (emails, posts, proposals),
  or for setting up your own claude.ai Project for personal use.
---

# Claude.ai Project Onboarding

You are setting up a claude.ai Project for a small business client. This is for clients who use the claude.ai web app (Pro or Teams) — NOT Claude Code or Cowork. The output is Project Instructions text + Knowledge files they paste/upload into claude.ai.

---

## Step 1: Intake

Collect the client's details. Support two input modes:

**Paste mode** — Wayne pastes or types the answers directly into the chat.
**File mode** — Wayne points at a filled-in questionnaire .docx (attempt to read it; if it fails, ask Wayne to paste the contents).

### Data points to collect (24 total):

1. Business name (full + trading name if different)
2. Business type (from the 7 supported verticals — or "Other")
3. Owner name
4. Owner role/title
5. Location
6. What the business does (2-3 sentences)
7. What makes them different (differentiator)
8. Typical customer description
9. Brand personality — 3 words that describe them
10. Brand personality — 3 words that do NOT describe them
11. Brand colours (hex codes if available)
12. Fonts (if they have brand fonts)
13. Tone (formal to casual — where do they sit?)
14. Words/phrases to always use
15. Words/phrases to never use
16. Email sign-off
17. Top 3-5 pain points (ranked)
18. What they'll use Claude for (mapped from pain points)
19. Package selected (if applicable)
20. Current business goals
21. Tech comfort level
22. Device (Mac/Windows/iPad)
23. Any writing samples or docs provided
24. Whether they want one combined Project or multiple split by use case

**If data is incomplete:** Fill gaps with industry defaults from `references/industry-defaults.md`. Do NOT interrogate Wayne — work with what you have and note assumptions in the QA report.

---

## Step 2: Business Type Routing

Read `references/industry-defaults.md` and match the client to one of 7 verticals:

1. Estate Agents / Letting Agencies
2. Accountants / Financial Services
3. Recruitment Agencies
4. Solicitors / Legal Practices
5. Retailers (Online / High Street)
6. Tradespeople / Contractors
7. Coaches / Consultants / Freelancers

If the client doesn't fit a vertical, use "Other" — skip industry-specific defaults and rely entirely on the client's own data.

Load the matching vertical's defaults:
- **Terminology** — industry-specific words to use correctly
- **Compliance** — regulations and disclaimers to be aware of
- **Default tone** — starting point if client hasn't specified
- **Typical use cases** — what they'll likely use Claude for
- **Banned phrases** — words/phrases to avoid in their industry
- **Key features** — special considerations (dual audience, seasonal awareness, etc.)
- **Example prompts** — industry-specific prompts for the setup guide

Client-specific data ALWAYS overrides industry defaults.

---

## Step 3: Generate Project Instructions

Read `references/project-instructions-template.md` and fill every `{{PLACEHOLDER}}` with client data merged with industry defaults.

### Single Project mode (default):
Generate one `project-instructions.md` with all 8 sections:
- Who You Are
- Brand Voice
- Communication Rules
- Our Customers
- Our Services
- Industry Rules
- Goals and Priorities
- Output Preferences

### Multi-Project mode (if client wants split):
Generate separate instruction files, each focused on a specific use case. Common splits:

| Project Name | Focus | Key Instructions |
|---|---|---|
| [Business] — Emails | Email writing | Email-specific tone, sign-off, common templates |
| [Business] — Social Media | Social posts | Platform-specific rules, hashtag style, post length |
| [Business] — Sales | Proposals, quotes, follow-ups | Sales tone, pricing rules, CTA style |
| [Business] — Content | Blog, newsletter, long-form | Content voice, SEO awareness, thought leadership |
| [Business] — Admin | Meeting notes, reports, summaries | Internal tone, concise format, action-focused |

Each split Project gets the core brand/business sections (Who You Are, Brand Voice, Communication Rules) PLUS use-case-specific instructions. This means some content is duplicated across Projects — that's intentional, each Project must be self-contained.

**File naming for multi-Project:**
```
project-instructions-emails.md
project-instructions-social-media.md
project-instructions-sales.md
[etc.]
```

### Character limit:
claude.ai Project Instructions has a ~10,000 character limit. Keep each set of instructions under **8,000 characters** to leave room for future additions. If it exceeds 8,000 characters, trim Output Preferences and Industry Rules first — the brand voice and communication rules are more important.

---

## Step 4: Generate Knowledge Files

Create a `/knowledge/` folder with files to upload as Project Knowledge.

### Always generate:
- **brand-summary.md** — condensed brand reference:
  - Business name and tagline
  - Brand colours (with hex codes)
  - Fonts
  - Core messaging pillars (3-5 key messages)
  - Tone of voice summary (1-2 sentences)
  - Example phrases that sound like them

### Generate based on pain points and use cases:
- **email-templates.md** — if they'll use Claude for emails: 2-3 template structures for their most common email types
- **social-media-guide.md** — if they'll use Claude for social: platform preferences, post structure, hashtag rules
- **sales-templates.md** — if they'll use Claude for proposals/quotes: standard structure, pricing presentation rules

### Client-provided docs:
Note in the setup guide which of the client's own documents should also be uploaded as Project Knowledge:
- Writing samples
- Brand guidelines PDF
- Existing templates
- Product/service descriptions

---

## Step 5: Generate Setup Guide

Read `references/setup-guide-template.md` and populate with:

- Client's business name (replace all `{{BUSINESS_NAME}}` placeholders)
- `{{KNOWLEDGE_FILE_LIST}}` — bullet list of every file to upload, with brief description of each
- `{{EXAMPLE_PROMPTS}}` — 3-5 example prompts tailored to their industry and pain points (pull from industry defaults + customise with their specific business context)
- `{{SUPPORT_EMAIL}}` — Wayne's support email
- `{{CHECKIN_DATE}}` — agreed check-in date (or "To be confirmed")
- `{{SUPPORT_PERIOD}}` — based on package (Starter: 1 month, Business: 3 months, Pro: 6 months, or as agreed)

### For multi-Project setups:
Adapt the setup guide to explain multiple Projects:
- How to create each one
- Which instruction file to paste into which Project
- Which knowledge files to upload to which Project (some shared, some specific)
- When to use which Project

Save as `setup-guide.md`.

---

## Step 6: QA Validation

Run these checks automatically and save results as `qa-report.md`:

### Must pass:
- [ ] Business name is consistent across ALL generated files
- [ ] No `{{PLACEHOLDER}}` or `[PLACEHOLDER]` values remain in any output file
- [ ] British English throughout — flag any -ize spellings, "color", "center", etc.
- [ ] Email sign-off appears correctly in project instructions
- [ ] Every file referenced in the setup guide actually exists in the output folder

### Should pass:
- [ ] Tone rules don't contradict (e.g., "casual" tone + "formal" language)
- [ ] Industry terminology is correct for the selected vertical
- [ ] Each project-instructions file is under 8,000 characters (report exact count)
- [ ] Brand personality "yes" and "no" words don't overlap
- [ ] Example prompts are relevant to the client's industry and pain points

### Assumptions log:
List every data point that was:
- Filled from industry defaults
- Left blank or marked "not specified" because the client didn't provide it
- Inferred from context rather than explicitly stated

This is critical — if the client didn't provide brand colours, fonts, a logo, writing samples, or any other data point, it MUST appear in the assumptions log even if you left the field blank rather than guessing. The assumptions log is how Wayne knows what to follow up on before handover.

Format:
```
ASSUMED: [field] = [value] (industry default for [vertical])
MISSING: [field] — not provided by client, left as [what you put instead]
INFERRED: [field] = [value] (based on [what you inferred from])
```

---

## Output

Save everything to:

```
/Users/wayne/Claude/client-brains/[client-business-name-slugified]/
  project-instructions.md          (or multiple if multi-Project)
  setup-guide.md
  qa-report.md
  /knowledge/
    brand-summary.md
    [any generated templates]
```

Use lowercase-kebab-case for the folder name (e.g., `smiths-estate-agents`, `bright-coaching`).

After saving, show Wayne:
1. A summary of what was generated
2. The QA report highlights (any failures or assumptions)
3. The character count of each project-instructions file
4. Remind him to review before sending to the client
