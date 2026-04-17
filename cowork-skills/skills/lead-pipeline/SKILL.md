---
name: lead-pipeline
description: "Set up an automated lead generation and outreach pipeline using Vibe Prospecting and Gmail. Creates 4 scheduled tasks: weekly lead finder, outreach email writer, outreach sender (Gmail drafts), and daily reply checker. Use this skill whenever Wayne says 'set up a lead pipeline', 'lead pipeline for [niche]', 'find leads for [niche]', 'outreach pipeline', 'prospecting pipeline', 'set up prospecting for', 'build me a lead funnel', 'create a lead workflow', or any variation of wanting to find leads, write outreach, and track replies for a target audience. Also trigger when Wayne says 'find me leads' or 'get leads for' even if he doesn't mention a full pipeline — the skill will ask if he wants the full pipeline or just a one-off search."
---

# Lead Pipeline Builder

This skill creates a complete automated outreach pipeline: find leads → write personalised emails → create Gmail drafts → check for replies. All CSVs are saved to `Co-Work/Leads/` so everything stays in one place.

## Step 1: Gather Target Info

Before creating anything, you need to understand who Wayne wants to reach. Ask these questions (but skip any he's already answered in the conversation):

1. **Who's the target?** — Industry, company size, job titles, geography
2. **How many leads per week?** — Default is 50 if he doesn't specify
3. **What's the pitch?** — What product/service is he selling? What's the value prop? (Currently SalesNote AI, but this could change)
4. **Pipeline name** — A short slug for the task names, e.g. "uk-saas-founders" becomes `uk-saas-founders-lead-finder`, `uk-saas-founders-outreach-writer`, etc. Suggest one based on the target and let Wayne confirm.

If Wayne says something like "find leads for UK dentists" — you already have most of what you need. Fill in sensible defaults and confirm before creating.

## Step 2: Map Filters to Vibe Prospecting

Translate Wayne's target description into Vibe Prospecting filters. The main filters available are:

| Filter | What it does | Needs autocomplete? |
|---|---|---|
| `company_country_code` | Country (ISO Alpha-2, e.g. "GB", "US") | No |
| `company_region_country_code` | Region (ISO 3166-2, e.g. "US-CA") | No |
| `company_size` | Employee count range ("1-10", "11-50", "51-200", etc.) | No |
| `company_revenue` | Annual revenue range ("1M-5M", "500M-1B") | No |
| `linkedin_category` | Industry category | Yes — use autocomplete |
| `naics_category` | NAICS code | Yes — use autocomplete |
| `job_title` | Specific titles | Yes — use autocomplete |
| `job_level` | Seniority ("c-suite", "director", "manager", etc.) | No |
| `job_department` | Department ("engineering", "sales", etc.) | No |
| `has_email` | Only prospects with emails | No (set to true) |
| `business_intent_topics` | Companies showing buying intent | Yes — use autocomplete |
| `company_tech_stack_tech` | Tech they use | Yes — use autocomplete |

**Always set `has_email: true`** — leads without emails are useless for outreach.

When a filter needs autocomplete, note it in the task prompt so the scheduled task knows to call autocomplete first. Don't hardcode autocomplete values — they can change. Instead, tell the task to autocomplete at runtime.

### Choosing Between job_level and job_title

This matters a lot for lead quality. The wrong choice means you find the wrong people.

- **Use `job_level`** (e.g. "c-suite", "director", "vice president") when targeting large companies (200+ employees) where people have standardised corporate titles. Combine with `job_department` if needed (e.g. job_level "director" + job_department "engineering").

- **Use `job_title` with autocomplete** when targeting small businesses (1-50 employees) or specific professions. Small business owners rarely have "c-suite" in their title — they're "Owner", "Founder", "Managing Director", "Principal", "Practice Owner", etc. For professions like dentists, lawyers, accountants, the title is often role-specific ("Principal Dentist", "Senior Partner", "Practice Manager").

- **Rule of thumb:** If company_size is "1-10" or "11-50", prefer `job_title` autocomplete over `job_level`. The autocomplete will surface real titles people actually use in that industry.

- **Never use both** `job_level` and `job_title` together — pick one.

### Choosing Between city_region and company_region_country_code

- **Use `city_region` with autocomplete** when Wayne names a specific city (e.g. "London", "Sydney", "New York"). This is more precise than region codes and works well for city-level targeting. Always autocomplete it — don't guess the value.

- **Use `company_region_country_code`** (ISO 3166-2, e.g. "US-CA", "GB-ENG") when targeting a state, province, or broad region rather than a specific city.

- **Use `company_country_code`** when the whole country is the target with no city/region specified.

- **Never combine** `city_region` with `company_region_country_code` — pick the most specific one that matches what Wayne asked for.

### Timezone Awareness

Wayne's scheduled tasks run in his local timezone (London, GMT/BST). If the target audience is in a significantly different timezone, flag it:

- Targets in the Americas, Asia-Pacific, or Australia will have business hours that don't align with London morning schedules
- This doesn't affect lead finding (Vibe Prospecting doesn't care about time), but it matters for the outreach sender — Gmail drafts created at 10am London might get sent at odd hours in the target's timezone
- If the timezone gap is large (6+ hours), mention it to Wayne and suggest he adjust the outreach-sender schedule, or just review and send drafts manually at an appropriate time
- Include a note in the outreach-sender task prompt reminding Wayne to check timezone alignment before enabling it

## Step 3: Create the 4 Scheduled Tasks

Use the `create_scheduled_task` tool to create each one. The naming convention is `{slug}-lead-finder`, `{slug}-outreach-writer`, `{slug}-outreach-sender`, `{slug}-reply-checker`.

### Task 1: Lead Finder (Monday 8am)

**Purpose:** Find leads using Vibe Prospecting and save CSV to Co-Work/Leads/.

**Prompt template:**
```
Find {count} {target description} leads with emails using Vibe Prospecting, then save the CSV.

## Steps

1. Use Vibe Prospecting autocomplete for any filters that need it: {list filters needing autocomplete, including job_title if targeting small businesses or specific professions}
2. Use fetch-entities with entity_type "prospects" and these filters:
   {list all filters with values}
   - has_email: true
   - number_of_results: {count}
3. Enrich prospects with enrich-prospects-contacts (email)
4. Show a sample preview with cost estimate
5. Export to CSV using export-to-csv with dataset_name "{slug}_leads"
6. After export, download the CSV from the export URL and save it to the workspace folder at `/sessions/*/mnt/Claude/Co-Work/Leads/` with filename `{slug}-leads-YYYY-MM-DD.csv`
7. Present the file link

## Notes
- Exclude previously exported leads using exclude_key "prospects"
- If fewer than {count} results, broaden filters (try removing company_size first, then broaden industry categories)
- Always save the final CSV to Co-Work/Leads/
- For small businesses (1-50 employees): use job_title autocomplete to find real titles like "Owner", "Founder", "Managing Director" — don't rely on job_level "c-suite" as small biz owners rarely use that title
- For specific professions (dentists, lawyers, etc.): autocomplete job_title for role-specific titles like "Principal Dentist", "Senior Partner"
```

**Cron:** `0 8 * * 1` (Monday 8am)

### Task 2: Outreach Writer (Monday 9am)

**Purpose:** Read the latest leads CSV and write personalised outreach emails.

**Prompt template:**
```
Write personalised outreach emails from the latest lead export CSV in Co-Work/Leads/.

## Steps

1. Find the latest leads CSV — look in `/sessions/*/mnt/Claude/Co-Work/Leads/` for the most recent `{slug}-leads-*.csv`
2. Read the CSV to get prospect names, emails, companies, job titles
3. Write personalised outreach emails for each lead:
   - Subject line: Short, personal, no spam words, under 50 chars
   - Opening: Reference their company or role specifically
   - Body: Brief value prop about {product/service} — {value prop summary}. Under 150 words.
   - CTA: Soft ask, not pushy
   - Tone: Friendly, direct, human. No corporate jargon.
4. Save output as CSV to `/sessions/*/mnt/Claude/Co-Work/Leads/{slug}-outreach-YYYY-MM-DD.csv` with columns: name, email, company, job_title, subject, body
5. Present the file link

## Notes
- Each email should feel individually written
- Reference the prospect's industry, company size, or role
- No attachments or links in first email
```

**Cron:** `0 9 * * 1` (Monday 9am)

### Task 3: Outreach Sender (Monday 10am)

**Purpose:** Create Gmail drafts from the outreach CSV so Wayne can review and send.

**Prompt template:**
```
Create Gmail drafts from the latest outreach CSV in Co-Work/Leads/.

## Steps

1. Find the latest outreach CSV — look in `/sessions/*/mnt/Claude/Co-Work/Leads/` for the most recent `{slug}-outreach-*.csv`
2. Read it to get name, email, company, subject, body for each prospect
3. For each prospect, use gmail_create_draft to create an email draft:
   - to: their email
   - subject: from the CSV
   - body: from the CSV, formatted as plain text
4. After creating all drafts, summarise: total drafts created, any failures
5. Save a log to `/sessions/*/mnt/Claude/Co-Work/Leads/{slug}-drafts-YYYY-MM-DD.csv` with columns: name, email, subject, draft_id, status

## Notes
- Create drafts, never send directly — Wayne reviews and sends manually
- If a draft fails, log the error and continue with the rest
- Report any failures prominently
- TIMEZONE CHECK: These leads are in {target country}. If that's not in the UK timezone, Wayne should review and send drafts at a time that lands in the recipient's business hours (typically 8-10am their local time). Don't auto-send at London morning time if the audience is in a different timezone.
```

**Cron:** `0 10 * * 1` (Monday 10am)
**Start disabled** — Wayne should enable this once he's comfortable with the outreach quality. Also flag timezone alignment if targeting outside UK.

### Task 4: Reply Checker (Tue-Fri 9am)

**Purpose:** Check Gmail for replies to outreach emails and classify them.

**Prompt template:**
```
Check Gmail inbox for replies to outreach emails and classify them. Save results to Co-Work/Leads/.

## Steps

1. Find the latest outreach CSV — look in `/sessions/*/mnt/Claude/Co-Work/Leads/` for the most recent `{slug}-outreach-*.csv`
2. Search Gmail for replies from the email addresses in the CSV:
   - `from:{email}` for each prospect
   - Also search `is:unread`
   - Look back 7 days
3. Classify each reply:
   - **Interested** — wants to chat, asks questions, positive signal
   - **Not interested** — polite decline
   - **Out of office** — auto-reply
   - **Bounce** — delivery failure
   - **Question** — asks for more info
4. Save to `/sessions/*/mnt/Claude/Co-Work/Leads/{slug}-replies-YYYY-MM-DD.csv` with columns: name, email, company, category, reply_snippet, received_date
5. Summary: total replies, breakdown by category, highlight any "Interested" leads

## Notes
- Only check replies from prospects in the most recent outreach CSV
- If no replies, save empty CSV and report "No replies yet"
- Flag "Interested" replies prominently — hot leads
- Don't reply to any emails — just classify and report
```

**Cron:** `0 9 * * 2-5` (Tue-Fri 9am)

## Step 4: Create the Leads Folder

Before creating any tasks, ensure the output folder exists:

```bash
mkdir -p /sessions/*/mnt/Claude/Co-Work/Leads
```

## Step 5: Confirm and Summarise

After creating all 4 tasks, show Wayne a summary table:

| Time | Task | What it does | Enabled |
|---|---|---|---|
| Mon 8am | {slug}-lead-finder | Finds {count} leads, saves CSV | Yes |
| Mon 9am | {slug}-outreach-writer | Writes personalised emails | Yes |
| Mon 10am | {slug}-outreach-sender | Creates Gmail drafts | No (enable when ready) |
| Tue-Fri 9am | {slug}-reply-checker | Classifies replies | Yes |

All CSVs go to `Co-Work/Leads/`.

## One-Off Lead Search

If Wayne just wants leads without the full pipeline (e.g. "find me 20 SaaS founders in New York"), do a single Vibe Prospecting search and save the CSV to `Co-Work/Leads/`. Don't create scheduled tasks. Ask if he wants the full pipeline after delivering the results.

## Multiple Pipelines

Wayne might want pipelines for different niches running in parallel. That's fine — each gets its own slug and task names. The CSVs all go to the same `Co-Work/Leads/` folder but are distinguished by the slug prefix in the filename.

If Wayne asks to "list my pipelines" or "what pipelines do I have", use `list_scheduled_tasks` and group by slug prefix.
