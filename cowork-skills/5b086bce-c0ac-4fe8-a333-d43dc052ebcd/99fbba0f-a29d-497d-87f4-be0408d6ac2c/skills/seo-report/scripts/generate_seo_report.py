#!/usr/bin/env python3
"""
SEO Report Generator
Generates a branded HTML report from structured SEO audit data,
then optionally converts to PDF via WeasyPrint.

Usage:
    python generate_seo_report.py data.json output.pdf
    python generate_seo_report.py data.json output.html  # HTML only
    python generate_seo_report.py --from-json '{"domain":"example.com",...}' output.pdf
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
REFS_DIR = SKILL_DIR / "references"


def load_css():
    """Load and combine brand CSS + SEO-specific CSS."""
    css_parts = []

    # Try to load wayne_brand.css from pdf-pro
    brand_paths = [
        Path("/sessions") / "blissful-laughing-clarke" / "mnt" / ".skills" / "skills" / "pdf-pro" / "scripts" / "wayne_brand.css",
        SCRIPT_DIR / "wayne_brand.css",
    ]
    for p in brand_paths:
        if p.exists():
            css_parts.append(p.read_text())
            break

    # Load SEO-specific styles
    seo_css = REFS_DIR / "seo_report_styles.css"
    if seo_css.exists():
        css_parts.append(seo_css.read_text())

    return "\n".join(css_parts)


def score_class(score):
    """Return CSS class for a numeric score (0-100)."""
    if score >= 90: return "score-a"
    if score >= 80: return "score-b"
    if score >= 70: return "score-c"
    if score >= 60: return "score-d"
    return "score-f"


def score_grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


def severity_badge(level):
    level_lower = level.lower()
    return f'<span class="severity severity-{level_lower}">{level}</span>'


def status_badge(status):
    s = status.lower()
    if s == "pass": return '<span class="status-pass">Pass</span>'
    if s == "fail": return '<span class="status-fail">Fail</span>'
    return '<span class="status-warn">Warning</span>'


def intent_badge(intent):
    mapping = {
        "informational": "info",
        "navigational": "nav",
        "commercial": "comm",
        "transactional": "trans",
    }
    cls = mapping.get(intent.lower(), "info")
    return f'<span class="intent intent-{cls}">{intent}</span>'


def opp_badge(level):
    cls = level.lower()
    return f'<span class="opp opp-{cls}">{level}</span>'


def diff_badge(level):
    mapping = {"easy": "easy", "moderate": "moderate", "hard": "hard"}
    cls = mapping.get(level.lower(), "moderate")
    return f'<span class="diff diff-{cls}">{level}</span>'


def progress_bar(score):
    if score >= 80: color = "green"
    elif score >= 70: color = "blue"
    elif score >= 60: color = "yellow"
    elif score >= 50: color = "orange"
    else: color = "red"
    return f'''<div class="progress-bar"><div class="progress-fill progress-{color}" style="width: {score}%;"></div></div>'''


def generate_html(data):
    """Generate the full HTML report from structured data."""
    css = load_css()
    domain = data.get("domain", "Unknown")
    date = data.get("date", datetime.now().strftime("%B %d, %Y"))
    scores = data.get("scores", {})
    overall = scores.get("overall", 0)
    executive_summary = data.get("executive_summary", "")
    top_priorities = data.get("top_priorities", [])
    keywords = data.get("keywords", [])
    onpage_issues = data.get("onpage_issues", [])
    content_gaps = data.get("content_gaps", [])
    technical_checks = data.get("technical_checks", [])
    backlink_data = data.get("backlink_data", {})
    eeat_data = data.get("eeat_data", {})
    competitor_data = data.get("competitor_comparison", [])
    quick_wins = data.get("quick_wins", [])
    strategic = data.get("strategic_investments", [])

    # --- Build HTML sections ---

    # Cover
    cover = f'''
    <div class="cover">
        <h1>SEO Audit Report</h1>
        <p class="subtitle">{domain}</p>
        <div class="bar"></div>
        <p class="meta">{date}</p>
        <p class="meta">Prepared by Wayne Pearce</p>
    </div>
    '''

    # Executive Summary + Score Cards
    score_cards = '<div class="score-row">'
    for label, key in [("Overall", "overall"), ("On-Page", "onpage"), ("Technical", "technical"), ("Content", "content"), ("Backlinks", "backlinks")]:
        s = scores.get(key, 0)
        score_cards += f'''
        <div class="score-card">
            <div class="score-circle {score_class(s)}">{s}</div>
            <div class="score-label">{label}</div>
        </div>'''
    score_cards += '</div>'

    priorities_html = ""
    if top_priorities:
        items = "<br>".join(f"{i+1}. {p}" for i, p in enumerate(top_priorities))
        priorities_html = f'<div class="callout"><strong>Top Priorities:</strong><br>{items}</div>'

    exec_section = f'''
    <h2>Executive Summary</h2>
    {score_cards}
    <p>{executive_summary}</p>
    {priorities_html}
    '''

    # Sub-score detail bars
    sub_scores_html = '<div class="two-col" style="margin-top: 1em;">'
    for label, key in [("On-Page SEO", "onpage"), ("Technical SEO", "technical"), ("Content Quality", "content"), ("Backlink Profile", "backlinks"), ("E-E-A-T Signals", "eeat")]:
        s = scores.get(key, 0)
        sub_scores_html += f'''
        <div style="margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 9pt;">
                <span>{label}</span><span class="bold">{s}/100</span>
            </div>
            {progress_bar(s)}
        </div>'''
    sub_scores_html += '</div>'

    # Keywords table
    kw_rows = ""
    for kw in keywords:
        kw_rows += f'''<tr>
            <td>{kw.get("keyword", "")}</td>
            <td>{diff_badge(kw.get("difficulty", "Moderate"))}</td>
            <td>{opp_badge(kw.get("opportunity", "Medium"))}</td>
            <td>{kw.get("volume", "—")}</td>
            <td>{intent_badge(kw.get("intent", "Informational"))}</td>
            <td>{kw.get("content_type", "")}</td>
        </tr>'''
    kw_section = f'''
    <h2 class="section-break">Keyword Opportunities</h2>
    <table>
        <tr><th>Keyword</th><th>Difficulty</th><th>Opportunity</th><th>Volume</th><th>Intent</th><th>Content Type</th></tr>
        {kw_rows}
    </table>
    ''' if keywords else ""

    # On-Page Issues table
    op_rows = ""
    for issue in onpage_issues:
        op_rows += f'''<tr>
            <td>{issue.get("page", "")}</td>
            <td>{issue.get("issue", "")}</td>
            <td>{severity_badge(issue.get("severity", "Medium"))}</td>
            <td>{issue.get("fix", "")}</td>
        </tr>'''
    op_section = f'''
    <h2 class="section-break">On-Page SEO Issues</h2>
    <table>
        <tr><th>Page</th><th>Issue</th><th>Severity</th><th>Recommended Fix</th></tr>
        {op_rows}
    </table>
    ''' if onpage_issues else ""

    # Content Gaps
    gap_cards = ""
    for gap in content_gaps:
        gap_cards += f'''
        <div class="gap-card">
            <h4>{gap.get("topic", "")}</h4>
            <p style="font-size: 10pt;">{gap.get("why", "")}</p>
            <div class="gap-meta">
                <span>Format: <strong>{gap.get("format", "Blog post")}</strong></span>
                <span>Priority: {opp_badge(gap.get("priority", "Medium"))}</span>
                <span>Effort: <strong>{gap.get("effort", "Moderate")}</strong></span>
            </div>
        </div>'''
    gap_section = f'''
    <h2 class="section-break">Content Gap Analysis</h2>
    {gap_cards}
    ''' if content_gaps else ""

    # Technical Checklist
    tc_rows = ""
    for check in technical_checks:
        tc_rows += f'''<tr>
            <td>{check.get("check", "")}</td>
            <td>{status_badge(check.get("status", "Warning"))}</td>
            <td>{check.get("details", "")}</td>
        </tr>'''
    tc_section = f'''
    <h2 class="section-break">Technical SEO Checklist</h2>
    <table>
        <tr><th>Check</th><th>Status</th><th>Details</th></tr>
        {tc_rows}
    </table>
    ''' if technical_checks else ""

    # Backlink section
    bl_section = ""
    if backlink_data:
        bl_summary = backlink_data.get("summary", "")
        bl_opps = backlink_data.get("opportunities", [])
        opps_html = ""
        for o in bl_opps:
            opps_html += f'''<div class="gap-card">
                <h4>{o.get("strategy", "")}</h4>
                <p style="font-size: 10pt;">{o.get("description", "")}</p>
            </div>'''
        bl_section = f'''
        <h2 class="section-break">Backlink Profile &amp; Opportunities</h2>
        <p>{bl_summary}</p>
        {opps_html}
        '''

    # E-E-A-T section
    eeat_section = ""
    if eeat_data:
        eeat_items = eeat_data.get("signals", [])
        eeat_rows = ""
        for item in eeat_items:
            eeat_rows += f'''<tr>
                <td>{item.get("signal", "")}</td>
                <td>{status_badge(item.get("status", "Warning"))}</td>
                <td>{item.get("recommendation", "")}</td>
            </tr>'''
        eeat_section = f'''
        <h2 class="section-break">E-E-A-T Assessment</h2>
        <p>{eeat_data.get("summary", "")}</p>
        <table>
            <tr><th>Signal</th><th>Status</th><th>Recommendation</th></tr>
            {eeat_rows}
        </table>
        '''

    # Competitor Comparison
    comp_section = ""
    if competitor_data:
        comp_headers = competitor_data.get("headers", [])
        comp_rows_data = competitor_data.get("rows", [])
        th_html = "".join(f"<th>{h}</th>" for h in comp_headers)
        comp_rows_html = ""
        for row in comp_rows_data:
            cells = "".join(f"<td>{c}</td>" for c in row)
            comp_rows_html += f"<tr>{cells}</tr>"
        comp_section = f'''
        <h2 class="section-break">Competitor Comparison</h2>
        <table>
            <tr>{th_html}</tr>
            {comp_rows_html}
        </table>
        '''

    # Action Plan
    qw_html = ""
    for i, action in enumerate(quick_wins):
        qw_html += f'''
        <div class="action-row">
            <div class="action-number">{i+1}</div>
            <div class="action-content">
                <h4>{action.get("action", "")}</h4>
                <p style="font-size: 10pt; margin: 0;">{action.get("description", "")}</p>
                <div class="action-impact">Impact: <strong>{action.get("impact", "Medium")}</strong> &bull; Effort: <strong>{action.get("effort", "1-2 hours")}</strong></div>
            </div>
        </div>'''

    si_html = ""
    for i, action in enumerate(strategic):
        si_html += f'''
        <div class="action-row">
            <div class="action-number">{i+1}</div>
            <div class="action-content">
                <h4>{action.get("action", "")}</h4>
                <p style="font-size: 10pt; margin: 0;">{action.get("description", "")}</p>
                <div class="action-impact">Impact: <strong>{action.get("impact", "Medium")}</strong> &bull; Effort: <strong>{action.get("effort", "Multi-day")}</strong></div>
            </div>
        </div>'''

    action_section = f'''
    <h2 class="section-break">Prioritized Action Plan</h2>
    <h3>Quick Wins (This Week)</h3>
    {qw_html}
    <h3 style="margin-top: 1.5em;">Strategic Investments (This Quarter)</h3>
    {si_html}
    ''' if (quick_wins or strategic) else ""

    # Disclaimer
    disclaimer = '''
    <div class="disclaimer">
        <strong>Disclaimer:</strong> This audit is based on publicly observable data and web search results.
        Search volume and keyword difficulty estimates are directional indicators, not exact measurements.
        For precise data, verify findings with dedicated SEO tools (Ahrefs, Semrush, Google Search Console).
    </div>
    '''

    # Assemble full HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SEO Audit Report — {domain}</title>
    <style>
{css}
    </style>
</head>
<body>
{cover}
{exec_section}
{sub_scores_html}
{kw_section}
{op_section}
{gap_section}
{tc_section}
{bl_section}
{eeat_section}
{comp_section}
{action_section}
{disclaimer}
</body>
</html>'''

    return html


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate SEO audit report")
    parser.add_argument("input", nargs="?", help="JSON data file path")
    parser.add_argument("output", help="Output file (.pdf or .html)")
    parser.add_argument("--from-json", help="JSON string instead of file")
    parser.add_argument("--size", default="letter", help="Page size (letter, a4)")
    args = parser.parse_args()

    if args.from_json:
        data = json.loads(args.from_json)
    elif args.input:
        with open(args.input) as f:
            data = json.load(f)
    else:
        parser.error("Provide either a JSON file or --from-json")

    html = generate_html(data)
    output = Path(args.output)

    if output.suffix.lower() == ".html":
        output.write_text(html)
        print(f"HTML report saved to {output}")
    else:
        # Save HTML first, then convert to PDF
        html_path = output.with_suffix(".html")
        html_path.write_text(html)

        # Try WeasyPrint via pdf-pro's script
        pdf_script = Path("/sessions/blissful-laughing-clarke/mnt/.skills/skills/pdf-pro/scripts/html_to_pdf.py")
        if pdf_script.exists():
            os.system(f'python "{pdf_script}" "{html_path}" "{output}" --size {args.size}')
        else:
            # Direct WeasyPrint
            try:
                from weasyprint import HTML
                HTML(filename=str(html_path)).write_pdf(str(output))
                print(f"PDF report saved to {output}")
            except ImportError:
                print(f"WeasyPrint not available. HTML saved to {html_path}")
                print("Install with: pip install weasyprint --break-system-packages")


if __name__ == "__main__":
    main()
