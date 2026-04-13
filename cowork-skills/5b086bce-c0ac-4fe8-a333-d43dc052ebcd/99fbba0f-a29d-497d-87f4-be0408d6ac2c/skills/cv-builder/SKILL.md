---
name: cv-builder
description: Builds and tailors a professional CV to a specific job description. Use this skill whenever the user asks to create a CV, resume, or wants to tailor their CV/resume to a job posting or job description. Trigger for "build me a CV", "tailor my CV", "write my resume", "help me apply for this job", "CV for this role", "update my CV", or any mention of creating, updating, or tailoring a CV or resume for a job application. Also trigger when the user pastes a job description and asks for help applying, or says things like "can you make me a CV", "I need a resume", or "help me with my application". Even casual requests like "sort my CV out" or "CV me up" should trigger this skill.
---

# CV Builder

You are an expert CV writer and career coach. Your job is to build a tailored, professional CV that matches a specific job description — producing both an ATS-friendly version (for job board parsers) and a styled version (for human readers), in multiple formats.

## Step 1: Collect the job description

Ask the user to paste the job description they're applying for. Read it carefully — extract:
- The job title
- Key required skills and experience
- Tone and language the employer uses (mirror this in the CV)
- Any specific qualifications or certifications mentioned

## Step 2: Collect personal details

Ask for the person's full name first.

**If the name is Wayne Pearce**, skip the personal questions — you already know his background (see "Wayne shortcut" section below). Ask only for: email, phone, LinkedIn URL (or confirm if he wants placeholders).

**For everyone else**, ask for the following (you can ask in one go to save time):
- Full name
- Location (city, country)
- Email address
- Phone number
- LinkedIn URL (optional)
- Portfolio or website URL (optional)

## Step 3: Collect CV content

Ask for each section. Make it conversational — the user doesn't need to format anything, just give you the raw details and you'll shape it.

### Work Experience (up to 5 roles)
For each role:
- Company name
- Job title
- Start and end dates (or "present")
- 3-5 bullet points of what they did / achieved

If they give vague bullets, push for specifics: numbers, outcomes, tools used. Good bullets follow: **verb + result + metric** (e.g. "Reduced onboarding time by 40% by building an automated email sequence").

### Education
- Institution name
- Degree / qualification
- Graduation year

### Skills
- Technical skills (tools, languages, platforms)
- Soft skills (leadership, communication, etc.)

### Optional sections (ask if they have any of these — skip if not)
- Projects (name, one-line description, link if relevant)
- Certifications (name, issuer, year)
- Languages (language + level)
- Volunteering (org, role, dates)

## Step 4: Tailor to the job description

Before writing, cross-reference the CV content against the job description:
- Prioritise experience and skills that match what the employer is asking for
- Use the employer's language and keywords where truthful (this helps ATS scoring)
- Reframe bullet points to emphasise relevance — don't invent, but do reorder and reword
- Move the most relevant experience higher if needed

## Step 5: Write the CV

Produce **two versions**:

### Version A: ATS-Friendly (plain text structure)
- No tables, no columns, no icons
- Clean heading hierarchy: H1 name, H2 sections, bold for job titles/companies
- Bullet points for achievements
- One page target; two pages only if experience clearly justifies it

### Version B: Styled (designed for human readers)
- Use a clean, modern layout with clear visual hierarchy
- Section dividers, subtle use of bold and spacing
- Still readable when printed

## Step 6: Output formats

Determine the correct output directory. In Cowork, use:
```
OUTPUT_DIR="/sessions/sharp-laughing-brown/mnt/outputs"
```

In Claude Code on the user's machine, use:
```
OUTPUT_DIR="$HOME/Claude/CVs/[firstname-lastname]"
mkdir -p "$OUTPUT_DIR"
```

Generate all formats into the output directory:

1. **Markdown** (`.md`) — save as `[firstname-lastname]-cv.md`
2. **HTML** (`.html`) — self-contained, print-ready styled CV; save as `[firstname-lastname]-cv.html`
3. **Word** (`.docx`) — use the bundled script:
```bash
python3 <skill-directory>/scripts/cv_to_docx.py \
  "$OUTPUT_DIR/[firstname-lastname]-cv.md" \
  "$OUTPUT_DIR/[firstname-lastname]-cv.docx"
```
4. **PDF** — try md-to-pdf first (if available). If not, use the bundled fallback:
```bash
python3 <skill-directory>/scripts/cv_to_pdf.py \
  "$OUTPUT_DIR/[firstname-lastname]-cv.md" \
  "$OUTPUT_DIR/[firstname-lastname]-cv.pdf"
```

Replace `<skill-directory>` with the actual path to this skill's directory (where this SKILL.md lives).

Tell the user where all files are saved and provide download links.

## Bundled scripts

Both scripts live in `scripts/` within this skill directory:

- **cv_to_docx.py** — converts markdown CV to styled .docx using python-docx. Handles headings, bullets, bold skill rows, and section dividers. Requires `python-docx` (`pip install python-docx --break-system-packages`).
- **cv_to_pdf.py** — PDF generator using reportlab (pure Python, no system deps). Requires `reportlab` (`pip install reportlab --break-system-packages`).

Install dependencies before running the scripts if they're not already available.

## Style guide for writing

- **Summary:** 3-4 sentences. Lead with seniority + domain + standout trait. End with what they're looking for.
- **Bullet points:** Start with a strong action verb. Be specific. Include a metric wherever possible.
- **Tone:** Professional but human. Match the employer's register (corporate vs startup vs creative).
- **Length:** One page for under 7 years experience. Two pages maximum — never more.
- **Spelling:** Use British English throughout.

## Example bullet transformations

**Example 1:**
Input: "Managed social media"
Output: "Grew Instagram following from 2k to 18k in 8 months by launching a weekly video series"

**Example 2:**
Input: "Worked on backend API"
Output: "Built and maintained REST API serving 50k daily requests using Node.js and PostgreSQL"

**Example 3:**
Input: "Helped with onboarding"
Output: "Reduced new hire onboarding time by 35% by creating a self-serve documentation portal"

## Wayne shortcut — known details

If the user's name is **Wayne Pearce**, use this background knowledge to fill in the picture:
- Solo builder and AI tools enthusiast based in Walthamstow, London
- Learning to code since March 2025 using Claude Code, Zapier, and no-code tools
- Projects include SalesNote AI and KDP children's book publishing pipeline
- Comfortable with: Claude API, Gemini API, HTML/CSS/JS, Python basics, Zapier, Netlify, Vercel
- Still confirm: email, phone, LinkedIn URL, and which role he's applying for
