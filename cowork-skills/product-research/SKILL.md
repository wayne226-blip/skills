---
name: product-research
description: "Research any product and produce a beautiful branded PDF report with product images, specs, pricing, pros/cons, competitor comparison, YouTube review links, and a buying recommendation. Handles physical goods, software, SaaS, gadgets, tools, appliances — anything someone might buy. Trigger whenever the user says 'research this product', 'product research', 'compare products', 'should I buy X', 'review X for me', 'what's the best X', 'find me a good X', 'product report on X', 'deep dive on X product', or any variation of wanting to investigate a product before purchasing. Also trigger when the user pastes a product URL and asks for analysis, mentions wanting a buying guide, or asks to compare alternatives. Even casual requests like 'tell me about the Sony WH-1000XM5' or 'is Notion worth it' should trigger this skill if the user seems to want a thorough answer rather than a one-liner."
---

# Product Research — Detailed Report with Images

Research any product thoroughly and deliver a professional, image-rich PDF report using WeasyPrint. The report covers everything a buyer needs: overview, features, pricing, pros/cons, competitor comparison, YouTube reviews, and a clear recommendation.

## Inputs

Gather from the user before starting:

1. **Product name or URL** — what they want researched (required)
2. **Report depth** — ask the user which they prefer:
   - **Quick summary** — 2-3 page overview with key specs, price, verdict, and one competitor
   - **Deep dive** (recommended default) — full report: detailed features, pricing breakdown, 3+ competitors compared, YouTube reviews, pros/cons analysis, buying recommendation
   - **Comparison focus** — less about one product, more about comparing 3-5 alternatives head-to-head
3. **Budget or context** (optional) — helps tailor the recommendation
4. **Specific questions** (optional) — anything particular they want answered

If the user just says "research X" without specifying depth, ask them which depth they'd like.

## Important Defaults

- **Currency: UK pounds (£).** All prices throughout the report must use £ (GBP). Search for UK pricing specifically — add "UK price" or "price UK" to searches. If only USD is available, convert to GBP and note "(approx. converted)".
- **Cover image:** The cover page MUST include a product image. Download the main product hero image during Step 3 and embed it on the cover with `class="cover-img"`. If the download fails, use the `cover-img-placeholder` div.

## Process

### Step 1: Web Research

Use web search extensively. For each product, search for:

- `{product name} review 2025 2026` — recent reviews
- `{product name} specs features` — technical details
- `{product name} price UK` — current UK pricing in GBP
- `{product name} pros cons` — balanced assessment
- `{product name} vs` — discover main competitors
- `{product name} alternatives` — find alternatives
- `site:youtube.com "{product name}" review` — **CRITICAL: search YouTube directly to get actual youtube.com URLs**
- `{product name} reddit` — real user opinions

Run at least 6-8 searches to get a well-rounded picture. Don't rely on a single source.

### Step 2: Collect YouTube Review URLs

**This is a dedicated step — do not skip it.**

1. Search specifically for `site:youtube.com "{product name}" review`
2. From the search results, extract the actual `youtube.com/watch?v=...` URLs
3. You need at least 3 YouTube URLs for a deep dive, 1-2 for a quick summary
4. Record: video title, channel name, and the full YouTube URL
5. If `site:youtube.com` search doesn't return enough, also try `{product name} youtube review` and look for youtube.com links in the results
6. **Every YouTube reference in the final report MUST be a clickable hyperlink** using `<a href="https://youtube.com/watch?v=...">Video Title</a>` format

### Step 3: Download Product Images

Product images make the report vastly more useful. Use this approach:

**Method 1 — Download with curl (preferred):**
```bash
# Find image URLs from official product pages or retailers during web research
# Then download them:
curl -L -o /tmp/product_images/product_main.jpg \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "IMAGE_URL_HERE"
```

**Method 2 — Python urllib fallback:**
```python
import urllib.request
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ..."})
with urllib.request.urlopen(req, timeout=10) as resp:
    with open(output_path, "wb") as f:
        f.write(resp.read())
```

**Method 3 — Use the helper script:**
```bash
python /sessions/dazzling-eager-euler/product-research/scripts/download_images.py "IMAGE_URL" /tmp/product_images/product.jpg
```

**IMPORTANT IMAGE RULES:**
- Create `/tmp/product_images/` directory first: `mkdir -p /tmp/product_images`
- Try at least 3 different image URLs per product if the first ones fail
- Look for image URLs on official product pages, Amazon, Best Buy, etc.
- If ALL image downloads fail, use a styled placeholder div instead — never leave blank space
- Aim for 1-2 images per product (main product + competitors)

**Embedding images in HTML:**
```python
import sys
sys.path.insert(0, "/sessions/dazzling-eager-euler/mnt/.skills/skills/pdf-pro/scripts")
from image_helpers import generate_img_tag

# This creates a base64 <img> tag that embeds directly in the HTML
tag = generate_img_tag("/tmp/product_images/product.jpg", width="60%", css_class="product-img")
```

**If an image cannot be downloaded, use this SMALL inline placeholder (80x80px):**
```html
<div class="image-placeholder">
    <div class="placeholder-icon">📦</div>
    <div class="placeholder-text">Name</div>
</div>
<p>Description text flows right next to the placeholder because it uses float:left...</p>
```
**NEVER make placeholders larger than 80x80px. They should float left with text beside them, not sit centred on their own line.**

### Step 4: Structure the Report

Organize research into sections based on report depth:

#### For Quick Summary (STRICT: 2-3 pages max):
Keep it tight. No cover page for quick summaries. Include ONLY:
- Product name + one hero image (or placeholder)
- 5-row key specs table
- Price (one line)
- 3 pros, 3 cons (brief — one line each)
- One main competitor (brief comparison, not a full table)
- 2-sentence verdict
- 1-2 YouTube review links

**Do NOT add sections beyond this for quick summaries. No feature deep dives, no user sentiment analysis, no extensive competitor tables.**

#### For Deep Dive:
- **Cover Page** — product name, date, researched for Wayne Pearce
- **At a Glance** — KPI cards (price, rating, value score, best for) + one-sentence bottom line
- **Product Overview** — what it is, who it's for, with hero image
- **Key Specifications** — detailed spec table
- **Features Deep Dive** — 4-6 most important features
- **Pricing & Value** — tiers, price-per-value assessment
- **Pros & Cons** — honest, balanced list
- **User Sentiment** — what real users say
- **YouTube Reviews** — 3-5 video reviews with clickable links
- **Competitor Comparison** — side-by-side table of 3-4 alternatives
- **Recommendation** — clear, opinionated verdict with "Best For / Not For"

#### For Comparison Focus:
- Brief intro to the product category
- Comparison matrix (specs, pricing, features)
- Individual product summaries (shorter)
- Winner by category
- YouTube reviews for each contender

### Step 5: Build the HTML Report

Generate the report using WeasyPrint HTML-to-PDF.

**CRITICAL LAYOUT RULES — READ CAREFULLY:**

1. **ZERO forced page breaks except after the cover page.** The ONLY `page-break` in the entire document is `.cover { page-break-after: always; }`. No other element gets `page-break-before` or `page-break-after`. Not the competitor section, not any `<h2>`, nothing.

2. **Do NOT use `page-break-inside: avoid` on ANY container larger than 150px tall.** This is the #1 cause of white space — WeasyPrint pushes the entire block to the next page, leaving a half-page gap. Specifically:
   - **NEVER** put `page-break-inside: avoid` on: `.product-hero`, `.two-col` (pros/cons), the competitor table, `.yt-card` containers, any `<div>` wrapping multiple elements
   - **OK to use** `page-break-inside: avoid` on: individual `.kpi-card` (small), individual table `<tr>` rows, `.verdict-box` (small)

3. **Reduce all `<h2>` top margins to 0.8em.** Do NOT use 1.5em or larger margins on headings — it creates visual gaps.

4. **Placeholder images must be SMALL: 80x80px max.** Never 200x200. They should be inline next to text, not centred on their own taking up page space.

5. **All URLs must be clickable hyperlinks.** Every URL — YouTube, product pages, retailer links — must use `<a href="URL">Display Text</a>`. Never bare text URLs.

6. **Content must flow continuously.** Every section starts immediately after the previous one with only a heading + thin top margin. No blank half-pages anywhere.

7. **Write enough content to fill pages.** Each feature in the deep dive needs 3-4 lines minimum. User sentiment needs 4 paragraphs (positive, complaints, reliability, long-term). Include 7-8 pros AND 7-8 cons for deep dive. Add a "Key differentiator" paragraph to the overview. Include 3-4 pricing tiers. This prevents short sections that leave half-page gaps.

8. **Use CSS columns for Pros & Cons.** Use `<div class="pros-cons">` with `columns: 2` layout, NOT flexbox `.two-col`. This packs pros and cons side-by-side much more tightly.

9. **Use compact page margins.** Set `@page { margin: 0.65in 0.7in 0.8in 0.7in; }` — NOT 0.85in. The tighter margins are essential for fitting content.

10. **Use 10.5pt body font and 1.45 line-height.** These are smaller than the brand theme defaults but essential for avoiding white space in reports with this much structured content.

#### HTML Template:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        /* === PASTE wayne_brand.css CONTENT HERE === */
        /* Read from: /sessions/dazzling-eager-euler/mnt/.skills/skills/pdf-pro/scripts/wayne_brand.css */
        /* THEN OVERRIDE the following body/page/heading rules to keep layout tight: */

        /* === CRITICAL OVERRIDES FOR COMPACT LAYOUT === */
        body {
            font-size: 10.5pt;   /* slightly smaller than brand default */
            line-height: 1.45;   /* tighter than brand default 1.6 */
        }

        @page {
            size: letter;
            margin: 0.65in 0.7in 0.8in 0.7in;  /* tighter margins = more content per page */
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-family: var(--font-body);
                font-size: 8pt;
                color: var(--brand-text-muted);
            }
            @top-right {
                content: "Wayne Pearce";
                font-family: var(--font-body);
                font-size: 7pt;
                font-style: italic;
                color: #a0aec0;
            }
        }
        @page :first { @bottom-center { content: none; } @top-right { content: none; } }

        /* TIGHT heading margins — prevents gaps between sections */
        h2 { margin-top: 0.6em !important; margin-bottom: 0.3em !important; font-size: 15pt; }
        h3 { margin-top: 0.5em !important; margin-bottom: 0.2em !important; font-size: 12pt; }
        p { margin-bottom: 0.4em; }

        /* Tables — compact 9.5pt font */
        table { font-size: 9.5pt; margin: 0.3em 0; }
        th { padding: 6px 8px; font-size: 9pt; }
        td { padding: 5px 8px; }

        /* KPI cards — compact */
        .kpi-row { gap: 10px; margin: 0.3em 0; }
        .kpi-card { padding: 10px 6px; }
        .kpi-value { font-size: 20pt; }
        .kpi-label { font-size: 8pt; }

        /* Callout — compact */
        .callout { padding: 8px 12px; margin: 0.3em 0; font-size: 10pt; }

        /* === PRODUCT-RESEARCH SPECIFIC CSS === */

        /* Cover image — centred product hero on first page */
        .cover-img {
            max-width: 260px;
            max-height: 260px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
            margin: 24px auto 20px auto;
            display: block;
            object-fit: contain;
        }
        .cover-img-placeholder {
            width: 200px;
            height: 200px;
            background: var(--brand-bg-alt);
            border: 2px dashed var(--brand-border);
            border-radius: 10px;
            margin: 24px auto 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60pt;
            color: var(--brand-text-muted);
        }

        /* Product image styling */
        .product-img {
            border-radius: 6px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            max-width: 180px;
            float: left;
            margin: 0 16px 8px 0;
        }

        /* Image placeholder — SMALL (60x60) with float:left */
        .image-placeholder {
            width: 60px;
            height: 60px;
            background: var(--brand-bg-alt);
            border: 1px dashed var(--brand-border);
            border-radius: 6px;
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            float: left;
            margin: 0 10px 6px 0;
        }
        .placeholder-icon { font-size: 20px; }
        .placeholder-text { font-size: 7pt; color: var(--brand-text-muted); }

        /* Pros/cons — CSS COLUMNS layout (compact, no gaps) */
        .pros-cons {
            columns: 2;
            column-gap: 20px;
            margin: 0.3em 0;
        }
        .pros-cons .col-half {
            break-inside: avoid;
            margin-bottom: 0.3em;
        }
        .pro-item { color: #38A169; margin-bottom: 0.3em; font-size: 10pt; }
        .pro-item::before { content: "\2713  "; font-weight: 700; }
        .con-item { color: #E53E3E; margin-bottom: 0.3em; font-size: 10pt; }
        .con-item::before { content: "\2717  "; font-weight: 700; }

        /* YouTube review card — ultra compact */
        .yt-card {
            background: var(--brand-bg-alt);
            border: 1px solid var(--brand-border);
            border-radius: 6px;
            padding: 5px 10px;
            margin-bottom: 4px;
        }
        .yt-card .yt-title { font-weight: 600; color: var(--brand-primary); font-size: 10pt; }
        .yt-card .yt-title a { color: var(--brand-secondary); text-decoration: none; }
        .yt-card .yt-channel { font-size: 8.5pt; color: var(--brand-text-muted); }
        .yt-card .yt-link { font-size: 8.5pt; color: var(--brand-secondary); word-break: break-all; }
        .yt-card .yt-link a { color: var(--brand-secondary); text-decoration: underline; }

        /* Verdict box — small, keeps page-break-inside: avoid */
        .verdict-box {
            background: linear-gradient(135deg, #EBF8FF 0%, #F0FFF4 100%);
            border: 2px solid var(--brand-secondary);
            border-radius: 8px;
            padding: 10px 16px;
            margin: 0.4em 0;
            text-align: center;
            page-break-inside: avoid;
        }
        .verdict-box .verdict-label { font-size: 8pt; text-transform: uppercase; color: var(--brand-text-muted); letter-spacing: 1px; }
        .verdict-box .verdict-text { font-family: var(--font-heading); font-size: 14pt; color: var(--brand-primary); margin-top: 2px; }

        /* Lists — compact */
        ul { margin: 0.2em 0 0.3em 1.5em; }
        li { margin-bottom: 0.2em; font-size: 10pt; }

        /* Report footer */
        .report-footer {
            margin-top: 1em;
            padding-top: 0.5em;
            border-top: 1px solid var(--brand-border);
            color: var(--brand-text-muted);
            font-size: 8.5pt;
        }

        /* NUCLEAR: no page breaks except after cover */
        h2, h3, h4, div, section, table { page-break-before: auto !important; }
    </style>
</head>
<body>

    <!-- COVER PAGE (deep dive only — skip for quick summary) -->
    <div class="cover">
        <h1>Product Research Report</h1>
        <p class="subtitle">{Product Name}</p>
        <div class="bar"></div>
        <!-- EMBED cover product image here using base64 img tag with class="cover-img" -->
        <!-- e.g.: <img class="cover-img" src="data:image/jpeg;base64,..." alt="Product Name"> -->
        <!-- OR if image download failed, use this placeholder: -->
        <div class="cover-img-placeholder" style="flex-direction: column; gap: 8px;">
            <div style="font-size: 48pt; color: var(--brand-secondary);">&#128230;</div>
            <div style="font-size: 10pt; color: var(--brand-text-muted);">Product Image</div>
        </div>
        <p class="meta">{date}</p>
        <p class="meta">Researched for Wayne Pearce</p>
    </div>

    <!-- AT A GLANCE with KPI Cards -->
    <h2>At a Glance</h2>
    <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-value">£XXX</div><div class="kpi-label">Price</div></div>
        <div class="kpi-card"><div class="kpi-value">X.X/5</div><div class="kpi-label">Rating</div></div>
        <div class="kpi-card"><div class="kpi-value">X/10</div><div class="kpi-label">Value Score</div></div>
        <div class="kpi-card"><div class="kpi-value">{Who}</div><div class="kpi-label">Best For</div></div>
    </div>
    <div class="callout">
        <strong>Bottom Line:</strong> One-sentence verdict here.
    </div>

    <!-- PRODUCT OVERVIEW with small float:left image -->
    <h2>Product Overview</h2>
    <!-- EMBED product image here using base64 img tag from image_helpers.py with class="product-img" -->
    <!-- OR if image download failed, use this small placeholder: -->
    <div class="image-placeholder">
        <div class="placeholder-icon">📦</div>
        <div class="placeholder-text">Product</div>
    </div>
    <p>Overview text flows right beside the image/placeholder...</p>
    <p><strong>Who it's for:</strong> Target audience description.</p>
    <p><strong>Key differentiator:</strong> What sets this product apart from competitors.</p>

    <!-- KEY SPECS TABLE -->
    <h2>Key Specifications</h2>
    <table>
        <tr><th>Specification</th><th>Details</th></tr>
        <!-- 10-12 rows for deep dive, 5 rows for quick summary -->
    </table>

    <!-- FEATURES — no page break, flows immediately -->
    <h2>Features Deep Dive</h2>
    <h3>Feature Name</h3>
    <p>Feature description with enough detail to fill 3-4 lines...</p>
    <!-- Include 5-6 features for deep dive. Write 3-4 lines per feature minimum. -->

    <!-- PRICING — no page break, flows immediately -->
    <h2>Pricing &amp; Value</h2>
    <table>
        <tr><th>Price Point</th><th>Where to Buy</th><th>Value Assessment</th></tr>
        <!-- 3-4 pricing tiers -->
    </table>
    <p><strong>Value Assessment:</strong> Detailed paragraph about value proposition...</p>

    <!-- PROS & CONS — CSS columns layout (compact) -->
    <h2>Pros &amp; Cons</h2>
    <div class="pros-cons">
        <div class="col-half">
            <h3 style="color: #38A169; margin-bottom: 0.3em;">Pros</h3>
            <div class="pro-item">Pro with detail (not just keywords)</div>
            <!-- 7-8 pros for deep dive -->
        </div>
        <div class="col-half">
            <h3 style="color: #E53E3E; margin-bottom: 0.3em;">Cons</h3>
            <div class="con-item">Con with detail (not just keywords)</div>
            <!-- 7-8 cons for deep dive -->
        </div>
    </div>

    <!-- USER SENTIMENT — no page break -->
    <h2>What Users Say</h2>
    <p><strong>Positive feedback:</strong> 3-4 lines of real user praise...</p>
    <p><strong>Common complaints:</strong> 3-4 lines of genuine criticism...</p>
    <p><strong>Build quality/reliability:</strong> 2-3 lines...</p>
    <p><strong>Long-term ownership:</strong> 2-3 lines about 12+ month experience...</p>

    <!-- YOUTUBE REVIEWS — MUST use <a href> tags -->
    <h2>YouTube Reviews</h2>
    <div class="yt-card">
        <div class="yt-title"><a href="https://youtube.com/watch?v=XXXXX">Video Title Here</a></div>
        <div class="yt-channel">Channel Name</div>
        <div class="yt-link"><a href="https://youtube.com/watch?v=XXXXX">youtube.com/watch?v=XXXXX</a></div>
    </div>
    <!-- 3-4 yt-cards for deep dive -->

    <!-- COMPETITOR COMPARISON — NO forced page break -->
    <h2>Competitor Comparison</h2>
    <p>Brief intro sentence about the competitive landscape.</p>
    <table>
        <tr><th>Feature</th><th>Product 1</th><th>Product 2</th><th>Product 3</th><th>Product 4</th></tr>
        <!-- 8-9 comparison rows including: Price, key features, ratings, best for -->
    </table>
    <h3>Competitor Summary</h3>
    <p><strong>Competitor 1:</strong> 2-3 sentence comparison...</p>
    <p><strong>Competitor 2:</strong> 2-3 sentence comparison...</p>
    <p><strong>Competitor 3:</strong> 2-3 sentence comparison...</p>

    <!-- RECOMMENDATION — no page break -->
    <h2>Recommendation</h2>
    <div class="verdict-box">
        <div class="verdict-label">Our Verdict</div>
        <div class="verdict-text">Clear recommendation text here</div>
    </div>
    <h3>Best For</h3>
    <ul><li>Target audience with detail</li><!-- 4-5 items --></ul>
    <h3>Not Ideal For</h3>
    <ul><li>Who should avoid with reason</li><!-- 4-5 items --></ul>
    <h3>Final Thoughts</h3>
    <p>2-paragraph wrap-up with actionable buying advice...</p>

    <p class="report-footer">
        <strong>Report Date:</strong> {date} | <strong>Depth:</strong> {depth} | <strong>Pricing Valid:</strong> As of {month year} | <strong>Sources:</strong> {source list}
    </p>

</body>
</html>
```

### Step 6: Generate PDF and Deliver

1. Write the complete HTML to `/tmp/product_report.html`
2. Install WeasyPrint if needed: `pip install weasyprint --break-system-packages`
3. Convert to PDF:
   ```bash
   python /sessions/dazzling-eager-euler/mnt/.skills/skills/pdf-pro/scripts/html_to_pdf.py /tmp/product_report.html /tmp/product_report.pdf
   ```
4. Copy the PDF to the workspace folder:
   ```bash
   cp /tmp/product_report.pdf /sessions/dazzling-eager-euler/mnt/Claude/{product-name}-research-report.pdf
   ```
5. Provide the user a download link

### Step 7: Follow-Up

After delivering the report, offer:
- "Want me to research any of the competitors in more detail?"
- "Should I create a comparison spreadsheet you can edit?"
- "Want me to find the best place to buy?"

## Handling Different Product Types

**Physical products** (gadgets, tools, appliances):
- Emphasize specs table, build quality, warranty, where to buy
- Include dimensions, weight, materials

**Software / SaaS**:
- Emphasize pricing tiers, feature comparison at each tier, integrations
- Include free tier / trial info, ease of setup, learning curve
- Replace physical specs with platform support

**Services** (subscriptions, platforms):
- Emphasize value proposition, customer support quality
- Include user reviews more heavily

## Important Notes

- The PDF is the primary deliverable — always produce it
- Be honest and balanced — include genuine cons
- **All YouTube links MUST be actual youtube.com/watch URLs wrapped in `<a href>` tags**
- **All URLs in the report must be clickable `<a href>` hyperlinks — never plain text URLs**
- Prices should note the date checked
- If a product is very new and lacks reviews, say so
- Cross-reference claims across multiple sources
- **Do NOT use `.section-break` or `page-break-before: always` on ANY section — only the cover page gets `page-break-after: always`**
- **Use `.pros-cons` with CSS columns for Pros & Cons — NOT `.two-col` with flexbox**
- **Quick summary MUST be 2-3 pages. If it's longer, you've included too much content. Cut ruthlessly.**
- If image downloads fail, use placeholder divs — never leave blank space in the layout
