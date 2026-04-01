#!/usr/bin/env python3
"""Convert CSV/TSV data into a visual PDF dashboard using WeasyPrint.

Reads a data file, auto-detects column types (currency, percentage, integers,
text), generates KPI cards for numeric columns, a styled data table, and
optional summary stats — all rendered as a branded PDF.

Usage:
    python csv_to_dashboard.py data.csv output.pdf
    python csv_to_dashboard.py data.csv output.pdf --title "Q1 Sales Report"
    python csv_to_dashboard.py data.tsv output.pdf --palette ocean --kpi Revenue,Profit,Growth
    python csv_to_dashboard.py data.csv output.pdf --no-kpi --no-stats
    python csv_to_dashboard.py data.csv output.html  # HTML only (no WeasyPrint needed)

Also works as a library:
    from csv_to_dashboard import DashboardBuilder
    db = DashboardBuilder(df, title="Monthly Report")
    db.generate_pdf("report.pdf")
"""

import argparse
import os
import sys
import datetime
import pandas as pd
import numpy as np
from pathlib import Path


# ── Color Palettes ──────────────────────────────────────────
PALETTES = {
    "midnight": {
        "primary": "#1E2761", "secondary": "#2B6CB0", "accent": "#38A169",
        "bg": "#FFFFFF", "bg_alt": "#F7FAFC", "border": "#E2E8F0",
        "text": "#2D3748", "muted": "#718096",
        "positive": "#38A169", "negative": "#E53E3E",
        "header_font": "Georgia, serif",
        "body_font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    "forest": {
        "primary": "#2C5F2D", "secondary": "#97BC62", "accent": "#38A169",
        "bg": "#FFFFFF", "bg_alt": "#F5F5F5", "border": "#D1D5DB",
        "text": "#1A202C", "muted": "#6B7280",
        "positive": "#38A169", "negative": "#E53E3E",
        "header_font": "Georgia, serif",
        "body_font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    "coral": {
        "primary": "#2F3C7E", "secondary": "#F96167", "accent": "#F9E795",
        "bg": "#FFFFFF", "bg_alt": "#FFF5F5", "border": "#E2E8F0",
        "text": "#2D3748", "muted": "#718096",
        "positive": "#38A169", "negative": "#E53E3E",
        "header_font": "Georgia, serif",
        "body_font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    "ocean": {
        "primary": "#065A82", "secondary": "#1C7293", "accent": "#21295C",
        "bg": "#FFFFFF", "bg_alt": "#EBF8FF", "border": "#CBD5E0",
        "text": "#1A202C", "muted": "#64748B",
        "positive": "#38A169", "negative": "#E53E3E",
        "header_font": "Georgia, serif",
        "body_font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    "charcoal": {
        "primary": "#36454F", "secondary": "#4A5568", "accent": "#212121",
        "bg": "#FFFFFF", "bg_alt": "#F2F2F2", "border": "#D1D5DB",
        "text": "#212121", "muted": "#6B7280",
        "positive": "#48BB78", "negative": "#FC8181",
        "header_font": "'Arial Black', sans-serif",
        "body_font": "Arial, sans-serif",
    },
}


def detect_column_types(df):
    """Auto-detect column types for formatting."""
    types = {}
    for col in df.columns:
        if df[col].dtype in ["float64", "float32"]:
            # Check if likely percentage (values between -1 and 1 or -100 and 100)
            non_null = df[col].dropna()
            if len(non_null) > 0:
                if non_null.abs().max() <= 1.0 and non_null.abs().min() >= 0:
                    types[col] = "pct_decimal"  # 0.15 → 15%
                elif non_null.abs().max() <= 100 and "%" in col.lower():
                    types[col] = "pct_whole"  # 15 → 15%
                else:
                    types[col] = "float"
            else:
                types[col] = "float"
        elif df[col].dtype in ["int64", "int32"]:
            # Check if likely currency
            if any(kw in col.lower() for kw in ["revenue", "sales", "cost", "profit",
                                                   "price", "amount", "budget", "spend",
                                                   "income", "expense", "total", "$"]):
                types[col] = "currency"
            else:
                types[col] = "int"
        else:
            types[col] = "text"
    return types


def format_value(val, col_type, compact=False):
    """Format a value based on detected column type."""
    if pd.isna(val):
        return "—"

    if col_type == "currency":
        if compact and abs(val) >= 1_000_000:
            return f"${val / 1_000_000:,.1f}M"
        elif compact and abs(val) >= 1_000:
            return f"${val / 1_000:,.0f}K"
        return f"${val:,.0f}"
    elif col_type == "pct_decimal":
        return f"{val * 100:.1f}%"
    elif col_type == "pct_whole":
        return f"{val:.1f}%"
    elif col_type == "float":
        if compact:
            if abs(val) >= 1_000_000:
                return f"{val / 1_000_000:,.1f}M"
            elif abs(val) >= 1_000:
                return f"{val / 1_000:,.0f}K"
        return f"{val:,.2f}"
    elif col_type == "int":
        if compact and abs(val) >= 1_000_000:
            return f"{val / 1_000_000:,.1f}M"
        elif compact and abs(val) >= 1_000:
            return f"{val / 1_000:,.0f}K"
        return f"{val:,}"
    return str(val)


def compute_delta(series):
    """Compute period-over-period change for KPI delta display."""
    non_null = series.dropna()
    if len(non_null) < 2:
        return None, None
    last = non_null.iloc[-1]
    prev = non_null.iloc[-2]
    if prev == 0:
        return None, None
    change_pct = ((last - prev) / abs(prev)) * 100
    direction = "up" if change_pct >= 0 else "down"
    return change_pct, direction


class DashboardBuilder:
    """Build a visual PDF dashboard from a pandas DataFrame."""

    def __init__(self, df, title="Data Dashboard", subtitle=None,
                 palette="midnight", kpi_cols=None, show_kpi=True,
                 show_stats=True, show_table=True, max_table_rows=50,
                 author="Wayne Pearce"):
        self.df = df
        self.title = title
        self.subtitle = subtitle or f"Generated {datetime.date.today().strftime('%B %d, %Y')}"
        self.p = PALETTES.get(palette, PALETTES["midnight"])
        self.col_types = detect_column_types(df)
        self.show_kpi = show_kpi
        self.show_stats = show_stats
        self.show_table = show_table
        self.max_table_rows = max_table_rows
        self.author = author

        # Auto-select KPI columns (numeric only, max 4)
        if kpi_cols:
            self.kpi_cols = [c for c in kpi_cols if c in df.columns]
        else:
            numeric_cols = [c for c in df.columns if self.col_types.get(c) not in ["text"]]
            self.kpi_cols = numeric_cols[:4]

    def _build_css(self):
        p = self.p
        return f"""
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: {p['body_font']};
            font-size: 10pt;
            line-height: 1.5;
            color: {p['text']};
            background: {p['bg']};
        }}
        @page {{
            size: letter;
            margin: 0.75in;
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 8pt;
                color: {p['muted']};
            }}
            @top-right {{
                content: "{self.author}";
                font-size: 7pt;
                font-style: italic;
                color: #a0aec0;
            }}
        }}
        @page :first {{
            @top-right {{ content: none; }}
        }}

        /* Header */
        .header {{
            border-bottom: 3px solid {p['secondary']};
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-family: {p['header_font']};
            font-size: 24pt;
            color: {p['primary']};
            margin-bottom: 2px;
        }}
        .header .subtitle {{
            font-size: 11pt;
            color: {p['muted']};
        }}

        /* KPI Cards */
        .kpi-row {{
            display: flex;
            gap: 14px;
            margin: 18px 0;
        }}
        .kpi-card {{
            flex: 1;
            background: {p['bg_alt']};
            border: 1px solid {p['border']};
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            page-break-inside: avoid;
        }}
        .kpi-card .value {{
            font-family: {p['header_font']};
            font-size: 24pt;
            font-weight: 700;
            color: {p['primary']};
        }}
        .kpi-card .label {{
            font-size: 8pt;
            color: {p['muted']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 2px;
        }}
        .kpi-card .delta {{
            font-size: 9pt;
            margin-top: 4px;
        }}
        .delta-up {{ color: {p['positive']}; }}
        .delta-down {{ color: {p['negative']}; }}

        /* Section headers */
        h2 {{
            font-family: {p['header_font']};
            font-size: 14pt;
            color: {p['primary']};
            border-bottom: 2px solid {p['secondary']};
            padding-bottom: 4px;
            margin-top: 24px;
            margin-bottom: 10px;
        }}

        /* Data table */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 9pt;
            margin: 10px 0;
        }}
        th {{
            background: {p['primary']};
            color: white;
            padding: 8px 10px;
            text-align: left;
            font-weight: 600;
            font-size: 8pt;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        td {{
            padding: 6px 10px;
            border-bottom: 1px solid {p['border']};
        }}
        tr:nth-child(even) td {{
            background: {p['bg_alt']};
        }}
        .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
        .negative {{ color: {p['negative']}; }}

        /* Stats summary */
        .stats-grid {{
            display: flex;
            gap: 14px;
            margin: 10px 0;
            flex-wrap: wrap;
        }}
        .stat-block {{
            flex: 1 1 0;
            min-width: 100px;
            max-width: 20%;
            background: {p['bg_alt']};
            border: 1px solid {p['border']};
            border-radius: 6px;
            padding: 10px 12px;
            page-break-inside: avoid;
        }}
        .stat-block .col-name {{
            font-size: 8pt;
            color: {p['muted']};
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 4px;
        }}
        .stat-block .stat-row {{
            display: flex;
            justify-content: space-between;
            font-size: 9pt;
            padding: 1px 0;
        }}
        .stat-label {{ color: {p['muted']}; }}
        .stat-value {{ font-weight: 600; }}

        .footer {{
            margin-top: 24px;
            padding-top: 8px;
            border-top: 1px solid {p['border']};
            font-size: 8pt;
            color: {p['muted']};
            text-align: center;
        }}
        .page-break {{ page-break-before: always; }}
        """

    def _build_kpi_html(self):
        if not self.show_kpi or not self.kpi_cols:
            return ""

        cards = []
        for col in self.kpi_cols:
            col_type = self.col_types.get(col, "float")
            series = self.df[col].dropna()
            if len(series) == 0:
                continue

            # Use last value as the KPI
            last_val = series.iloc[-1]
            formatted = format_value(last_val, col_type, compact=True)

            # Delta
            change_pct, direction = compute_delta(series)
            delta_html = ""
            if change_pct is not None:
                arrow = "&#9650;" if direction == "up" else "&#9660;"
                cls = "delta-up" if direction == "up" else "delta-down"
                delta_html = f'<div class="delta {cls}">{arrow} {abs(change_pct):.1f}%</div>'

            cards.append(f"""
            <div class="kpi-card">
                <div class="value">{formatted}</div>
                <div class="label">{col}</div>
                {delta_html}
            </div>""")

        if not cards:
            return ""

        return f'<div class="kpi-row">{"".join(cards)}</div>'

    def _build_table_html(self):
        if not self.show_table:
            return ""

        df = self.df.head(self.max_table_rows)
        rows_total = len(self.df)
        shown = len(df)

        header = "<tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>"

        body_rows = []
        for _, row in df.iterrows():
            cells = []
            for col in df.columns:
                val = row[col]
                col_type = self.col_types.get(col, "text")
                formatted = format_value(val, col_type)

                is_num = col_type not in ["text"]
                cls_parts = []
                if is_num:
                    cls_parts.append("num")
                if is_num and not pd.isna(val) and isinstance(val, (int, float)) and val < 0:
                    cls_parts.append("negative")

                cls = f' class="{" ".join(cls_parts)}"' if cls_parts else ""
                cells.append(f"<td{cls}>{formatted}</td>")

            body_rows.append("<tr>" + "".join(cells) + "</tr>")

        truncation = ""
        if shown < rows_total:
            truncation = f'<p style="font-size: 8pt; color: #718096; text-align: center;">Showing {shown} of {rows_total} rows</p>'

        return f"""
        <h2>Data</h2>
        <table>
            <thead>{header}</thead>
            <tbody>{"".join(body_rows)}</tbody>
        </table>
        {truncation}
        """

    def _build_stats_html(self):
        if not self.show_stats:
            return ""

        numeric_cols = [c for c in self.df.columns if self.col_types.get(c) not in ["text"]]
        if not numeric_cols:
            return ""

        blocks = []
        for col in numeric_cols[:6]:  # Max 6 stat blocks
            col_type = self.col_types.get(col, "float")
            series = self.df[col].dropna()
            if len(series) == 0:
                continue

            stats = {
                "Mean": format_value(series.mean(), col_type),
                "Median": format_value(series.median(), col_type),
                "Min": format_value(series.min(), col_type),
                "Max": format_value(series.max(), col_type),
                "Sum": format_value(series.sum(), col_type),
            }

            stat_rows = "".join(
                f'<div class="stat-row"><span class="stat-label">{k}</span>'
                f'<span class="stat-value">{v}</span></div>'
                for k, v in stats.items()
            )

            blocks.append(f"""
            <div class="stat-block">
                <div class="col-name">{col}</div>
                {stat_rows}
            </div>""")

        if not blocks:
            return ""

        return f'<h2>Summary Statistics</h2><div class="stats-grid">{"".join(blocks)}</div>'

    def build_html(self):
        """Generate complete HTML for the dashboard."""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>{self._build_css()}</style>
</head>
<body>
    <div class="header">
        <h1>{self.title}</h1>
        <div class="subtitle">{self.subtitle}</div>
    </div>

    {self._build_kpi_html()}
    {self._build_table_html()}
    {self._build_stats_html()}

    <div class="footer">{self.author} &bull; {self.subtitle}</div>
</body>
</html>"""

    def generate_pdf(self, output_path):
        """Render the dashboard as a PDF using WeasyPrint."""
        from weasyprint import HTML
        html_content = self.build_html()
        HTML(string=html_content).write_pdf(output_path)
        file_size = os.path.getsize(output_path)
        print(f"Dashboard PDF created: {output_path} ({file_size:,} bytes)")

    def generate_html(self, output_path):
        """Save the dashboard as an HTML file."""
        html_content = self.build_html()
        with open(output_path, "w") as f:
            f.write(html_content)
        file_size = os.path.getsize(output_path)
        print(f"Dashboard HTML created: {output_path} ({file_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Generate PDF dashboard from CSV/TSV data")
    parser.add_argument("input", help="Input CSV or TSV file")
    parser.add_argument("output", help="Output file (.pdf or .html)")
    parser.add_argument("--title", default=None, help="Dashboard title")
    parser.add_argument("--subtitle", default=None, help="Dashboard subtitle")
    parser.add_argument("--palette", default="midnight",
                        choices=list(PALETTES.keys()), help="Color palette")
    parser.add_argument("--kpi", default=None, help="Comma-separated KPI column names")
    parser.add_argument("--no-kpi", action="store_true", help="Hide KPI cards")
    parser.add_argument("--no-stats", action="store_true", help="Hide summary stats")
    parser.add_argument("--no-table", action="store_true", help="Hide data table")
    parser.add_argument("--max-rows", type=int, default=50, help="Max table rows (default: 50)")
    parser.add_argument("--author", default="Wayne Pearce", help="Author name")
    args = parser.parse_args()

    # Read data
    sep = "\t" if args.input.endswith((".tsv", ".tab")) else ","
    df = pd.read_csv(args.input, sep=sep)

    title = args.title or Path(args.input).stem.replace("_", " ").replace("-", " ").title()
    kpi_cols = args.kpi.split(",") if args.kpi else None

    builder = DashboardBuilder(
        df,
        title=title,
        subtitle=args.subtitle,
        palette=args.palette,
        kpi_cols=kpi_cols,
        show_kpi=not args.no_kpi,
        show_stats=not args.no_stats,
        show_table=not args.no_table,
        max_table_rows=args.max_rows,
        author=args.author,
    )

    ext = Path(args.output).suffix.lower()
    if ext == ".pdf":
        builder.generate_pdf(args.output)
    elif ext in [".html", ".htm"]:
        builder.generate_html(args.output)
    else:
        print(f"Unsupported format: {ext}. Use .pdf or .html", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
