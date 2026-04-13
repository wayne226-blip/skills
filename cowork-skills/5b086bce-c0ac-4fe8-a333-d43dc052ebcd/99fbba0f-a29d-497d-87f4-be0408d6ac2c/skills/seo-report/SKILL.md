---
name: seo-report
description: "Comprehensive SEO audit that produces a beautiful branded PDF report. Covers keyword research, on-page analysis, content gaps, technical SEO, backlink opportunities, E-E-A-T signals, local SEO, competitor comparison, and a prioritized action plan — all rendered as a professional PDF with KPI score cards, color-coded severity tables, and executive summary. Trigger whenever the user says 'SEO report', 'SEO audit', 'analyze this site for SEO', 'keyword research for', 'check my SEO', 'site audit', 'how does my site rank', 'what SEO issues does my site have', 'run an SEO check', or any mention of wanting to analyze a website's search engine performance. Also trigger when they paste a URL and ask about its SEO health, rankings, or search visibility."
---

# SEO Report — Full Audit with PDF Output

Generate a comprehensive SEO audit for any website or domain and deliver the results as a beautifully formatted, branded PDF report using WeasyPrint.

## What Makes This Different

Most SEO audit tools dump text into chat. This skill produces a **professional PDF report** with:
- Cover page with the domain name and audit date
- KPI score cards (Overall Score, On-Page, Technical, Content, Backlinks)
- Color-coded severity tables (Critical/High/Medium/Low)
- Keyword opportunity tables with intent classification
- Content gap recommendations with effort estimates
- Technical checklist with Pass/Fail/Warning badges
- Competitor comparison matrix
- Prioritized action plan split into Quick Wins and Strategic Investments

The PDF uses Wayne's brand theme (wayne_brand.css) for consistent styling.

## Inputs

Gather from the user before starting. If not provided, ask:

1. **URL or domain** — the site to audit (or a topic/keyword for keyword-only mode)
2. **Audit scope** — one of:
   - **Full audit** (default) — everything below
   - **Keyword research only** — keyword opportunities for a topic/domain
   - **Technical audit only** — crawlability, speed, structured data
   - **Content audit only** — content gaps, thin content, freshness
   - **Competitor comparison** — head-to-head against specific competitors
3. **Target keywords** (optional) — keywords they're already targeting
4. **Competitors** (optional) — specific domains to compare against. If not provided, identify 2-3 likely competitors via web search.

## Process

### Step 1: Gather Data

Use web search to research the target site. For each section below, search for relevant information about the domain.

Search queries to run:
- `site:{domain}` — check indexed pages
- `{domain} SEO` — find existing audits or mentions
- `{target keywords} site:{domain}` — check keyword targeting
- `{domain} vs {competitor}` — competitive intelligence
- `{target keywords}` — check SERP landscape
- `{domain} reviews` or `{domain} about` — E-E-A-T signals

### Step 2: Analyze (All Sections)

Run through each section, collecting findings into structured data that will feed the PDF template.

#### 2A. Overall SEO Health Score

Calculate a score out of 100 based on weighted factors:
- On-Page SEO: 25 points
- Technical SEO: 25 points
- Content Quality: 20 points
- Backlink Profile: 15 points
- E-E-A-T Signals: 15 points

Each factor gets a sub-score. The overall score determines the grade:
- 90-100: A (Excellent)
- 80-89: B (Good)
- 70-79: C (Needs Work)
- 60-69: D (Significant Issues)
- Below 60: F (Critical Problems)

#### 2B. Keyword Research

For each keyword opportunity, assess:
- **Primary keywords** — high-intent terms directly tied to the business
- **Secondary keywords** — supporting terms and variations
- **Long-tail opportunities** — specific, lower-competition phrases
- **Question-based keywords** — "how to", "what is" queries matching People Also Ask
- **Search volume signals** — relative demand (High/Medium/Low)
- **Keyword difficulty** — how competitive (Easy/Moderate/Hard)
- **Intent classification** — Informational, Navigational, Commercial, Transactional
- **Opportunity score** — combined assessment (High/Medium/Low)

Provide 15-25 keyword opportunities sorted by opportunity score.

#### 2C. On-Page SEO Audit

For each key page (homepage, top landing pages, blog posts), evaluate:
- Title tags — present, unique, 50-60 chars, includes target keyword
- Meta descriptions — present, compelling, 150-160 chars, has CTA
- H1 tags — exactly one per page, includes primary keyword
- H2/H3 structure — logical hierarchy, uses secondary keywords
- Keyword usage — primary keyword in first 100 words, natural density
- Internal linking — related pages linked, no orphans, descriptive anchors
- Image alt text — all images have descriptive alt attributes
- URL structure — clean, readable, includes keywords
- Content length — sufficient depth for the topic
- Readability — grade level appropriate for audience

#### 2D. Content Gap Analysis

Identify what's missing:
- **Competitor topic coverage** — topics competitors rank for that this site doesn't
- **Content freshness** — pages not updated in 12+ months
- **Thin content** — pages with insufficient depth (<300 words for informational)
- **Missing content types** — formats competitors use (guides, comparisons, glossaries, tools)
- **Funnel gaps** — missing content at awareness, consideration, or decision stages
- **Topic cluster opportunities** — pillar pages with supporting content potential

#### 2E. Technical SEO

Evaluate infrastructure:
- Page speed indicators (large images, render-blocking scripts, redirects)
- Mobile-friendliness (responsive, tap targets, viewport)
- Structured data opportunities (FAQ, HowTo, Product, Article, Breadcrumb schema)
- Crawlability (robots.txt, XML sitemap, canonicals, noindex usage)
- Broken links (internal 404s, redirect chains)
- HTTPS and security
- Core Web Vitals signals (LCP, INP, CLS)
- Indexation (pages that should/shouldn't be indexed, duplicate content)

#### 2F. Backlink Profile & Link Building

Assess the site's link profile:
- **Domain authority signals** — relative site strength
- **Referring domains** — diversity and quality
- **Toxic link indicators** — spammy or low-quality links
- **Link-worthy content audit** — what content attracts links
- **Link building opportunities** — guest posting, broken link building, resource pages, HARO
- **Competitor backlink gaps** — who links to competitors but not to this site

#### 2G. E-E-A-T Signals

Evaluate Experience, Expertise, Authoritativeness, Trustworthiness:
- Author bios and credentials on content pages
- About page quality and depth
- Contact information accessibility
- Customer reviews and testimonials
- Industry certifications or awards
- External citations and mentions
- Content sourcing and citations within articles
- Site age and history

#### 2H. Local SEO (if applicable)

If the business has a physical location or serves local customers:
- Google Business Profile optimization
- NAP consistency (Name, Address, Phone across directories)
- Local citations (directory listings)
- Local keyword targeting
- Review management
- Local schema markup

#### 2I. Competitor Comparison

For each competitor, compare:
- Keyword overlap and gaps
- Domain authority signals
- Content depth and publishing frequency
- Backlink profile comparison
- SERP feature ownership (featured snippets, PAA, image packs)
- Technical advantages (speed, mobile, structured data)

### Step 3: Generate the PDF Report

After collecting all findings, generate the PDF using this workflow:

1. **Build the HTML report** using the template structure below
2. **Use WeasyPrint** to convert HTML to PDF via the pdf-pro skill's `scripts/html_to_pdf.py`
3. **Use the brand CSS** from `wayne_brand.css` for consistent styling
4. **Save to the workspace** folder so the user gets a downloadable file

#### PDF Report Structure

The HTML report should follow this structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        /* Include wayne_brand.css variables and base styles */
        /* Plus SEO-specific styles from references/seo_report_styles.css */
    </style>
</head>
<body>

    <!-- COVER PAGE -->
    <div class="cover">
        <h1>SEO Audit Report</h1>
        <p class="subtitle">{domain}</p>
        <div class="bar"></div>
        <p class="meta">{date}</p>
        <p class="meta">Prepared by Wayne Pearce</p>
    </div>

    <!-- EXECUTIVE SUMMARY with KPI Score Cards -->
    <h2>Executive Summary</h2>
    <div class="kpi-row">
        <!-- Overall Score, On-Page, Technical, Content, Backlinks -->
    </div>
    <p>3-5 sentence summary...</p>
    <div class="callout">
        <strong>Top 3 Priorities:</strong> ...
    </div>

    <!-- KEYWORD OPPORTUNITIES TABLE -->
    <h2 class="section-break">Keyword Opportunities</h2>
    <table><!-- keyword data --></table>

    <!-- ON-PAGE ISSUES TABLE -->
    <h2 class="section-break">On-Page SEO Issues</h2>
    <table><!-- issues with severity badges --></table>

    <!-- CONTENT GAPS -->
    <h2 class="section-break">Content Gap Analysis</h2>
    <!-- Gap cards with priority and effort -->

    <!-- TECHNICAL CHECKLIST -->
    <h2 class="section-break">Technical SEO Checklist</h2>
    <table><!-- Pass/Fail/Warning rows --></table>

    <!-- BACKLINK PROFILE -->
    <h2 class="section-break">Backlink Profile & Opportunities</h2>

    <!-- E-E-A-T ASSESSMENT -->
    <h2 class="section-break">E-E-A-T Assessment</h2>

    <!-- COMPETITOR COMPARISON -->
    <h2 class="section-break">Competitor Comparison</h2>
    <table><!-- comparison matrix --></table>

    <!-- ACTION PLAN -->
    <h2 class="section-break">Prioritized Action Plan</h2>
    <h3>Quick Wins (This Week)</h3>
    <table><!-- actions --></table>
    <h3>Strategic Investments (This Quarter)</h3>
    <table><!-- actions --></table>

</body>
</html>
```

#### SEO-Specific CSS Classes

In addition to the wayne_brand.css classes, use these for SEO-specific elements:

```css
/* Score circle */
.score-circle {
    width: 80px; height: 80px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 24pt; font-weight: 700; color: white;
    margin: 0 auto 8px;
}
.score-a { background: #38A169; }
.score-b { background: #2B6CB0; }
.score-c { background: #D69E2E; }
.score-d { background: #DD6B20; }
.score-f { background: #E53E3E; }

/* Severity badges */
.severity-critical { background: #FED7D7; color: #742A2A; padding: 2px 8px; border-radius: 10px; font-size: 8pt; font-weight: 600; }
.severity-high { background: #FEEBC8; color: #744210; padding: 2px 8px; border-radius: 10px; font-size: 8pt; font-weight: 600; }
.severity-medium { background: #FEFCBF; color: #744210; padding: 2px 8px; border-radius: 10px; font-size: 8pt; font-weight: 600; }
.severity-low { background: #C6F6D5; color: #22543D; padding: 2px 8px; border-radius: 10px; font-size: 8pt; font-weight: 600; }

/* Status indicators */
.status-pass { color: #38A169; font-weight: 600; }
.status-fail { color: #E53E3E; font-weight: 600; }
.status-warn { color: #D69E2E; font-weight: 600; }

/* Intent badges */
.intent-info { background: #BEE3F8; color: #2A4365; }
.intent-nav { background: #E9D8FD; color: #44337A; }
.intent-comm { background: #FEFCBF; color: #744210; }
.intent-trans { background: #C6F6D5; color: #22543D; }
```

### Step 4: Generate and Deliver

1. Write the complete HTML to a temp file
2. Install WeasyPrint if needed: `pip install weasyprint --break-system-packages`
3. Convert to PDF using: `python {pdf-pro-scripts}/html_to_pdf.py report.html report.pdf`
4. Copy the PDF to the workspace folder
5. Provide the user a download link

If WeasyPrint is not available, fall back to delivering the HTML report directly (it will still look good in a browser).

### Step 5: Follow-Up

After presenting the report, offer:
- "Want me to draft content briefs for the top keyword opportunities?"
- "Should I create optimized title tags and meta descriptions for your key pages?"
- "Want a content calendar based on the gap analysis?"
- "Should I generate schema markup (JSON-LD) for your pages?"
- "Want me to dive deeper into any section?"
- "Should I run this same analysis for a different domain?"

## Important Notes

- The PDF report is the primary deliverable — always produce it unless the user specifically asks for text-only output
- Use web search extensively to gather real data about the site
- Be honest about limitations — without direct access to tools like Ahrefs or Search Console, some metrics are estimated based on observable signals
- Include a disclaimer in the report noting that volume/difficulty estimates are directional and recommending verification with dedicated SEO tools
- The report should be actionable — every finding should have a specific recommended fix
