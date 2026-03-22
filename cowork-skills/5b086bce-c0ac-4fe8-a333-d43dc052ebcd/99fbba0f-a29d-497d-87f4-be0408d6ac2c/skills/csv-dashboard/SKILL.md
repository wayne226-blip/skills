---
name: csv-dashboard
description: "Auto-generate visual PDF dashboards from CSV/TSV data files. Drop a CSV, get a branded report with KPI cards, styled data table, and summary statistics. Uses WeasyPrint for PDF rendering. Trigger when the user says 'dashboard from data', 'CSV to report', 'data to PDF', 'visualize this CSV', 'make a report from this spreadsheet', 'turn this data into a dashboard', or when they upload a CSV/TSV and want a visual summary."
---

# CSV → Dashboard

Convert any CSV or TSV file into a polished PDF dashboard with KPI cards, styled tables, and summary statistics.

## Quick Reference

```bash
# Basic — auto-detects everything
python scripts/csv_to_dashboard.py data.csv report.pdf

# With custom title and palette
python scripts/csv_to_dashboard.py sales.csv sales_report.pdf --title "Q1 Sales Report" --palette ocean

# Specify KPI columns
python scripts/csv_to_dashboard.py data.csv report.pdf --kpi Revenue,Profit,Growth

# HTML output (no WeasyPrint needed)
python scripts/csv_to_dashboard.py data.csv report.html

# Minimal — table only
python scripts/csv_to_dashboard.py data.csv report.pdf --no-kpi --no-stats
```

## What It Auto-Detects

The pipeline automatically analyzes your data columns:

| Pattern | Detected As | Formatting |
|---------|-------------|------------|
| Column named "Revenue", "Sales", "Cost", etc. | Currency | `$1,234` or `$1.2M` |
| Float values 0–1 | Percentage (decimal) | `15.0%` |
| Column with "%" in name | Percentage (whole) | `15.0%` |
| Integer columns | Number | `1,234` or `1.2K` |
| Everything else | Text | As-is |

## KPI Cards

By default, the top 4 numeric columns become KPI cards showing:
- **Last value** from the column (most recent row)
- **Period-over-period delta** comparing last two rows (▲/▼ with percentage)

Override with `--kpi Revenue,Profit,Growth` to pick specific columns.

## Color Palettes

| Palette | Look |
|---------|------|
| `midnight` (default) | Navy headers, blue accents |
| `forest` | Green headers, moss accents |
| `coral` | Navy + coral accents |
| `ocean` | Deep blue + teal |
| `charcoal` | Dark gray, minimal |

## Library Usage

```python
import pandas as pd
from csv_to_dashboard import DashboardBuilder

df = pd.read_csv("sales.csv")

builder = DashboardBuilder(
    df,
    title="Q1 Sales Report",
    subtitle="January – March 2026",
    palette="ocean",
    kpi_cols=["Revenue", "Profit", "Growth"],
    show_kpi=True,
    show_stats=True,
    show_table=True,
    max_table_rows=50,
)

builder.generate_pdf("q1_report.pdf")
# Or HTML:
builder.generate_html("q1_report.html")
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | Filename | Dashboard title |
| `--subtitle` | Today's date | Subtitle text |
| `--palette` | `midnight` | Color palette |
| `--kpi` | Auto (top 4 numeric) | Comma-separated KPI columns |
| `--no-kpi` | Show | Hide KPI cards |
| `--no-stats` | Show | Hide summary statistics |
| `--no-table` | Show | Hide data table |
| `--max-rows` | 50 | Max rows in table |
| `--author` | Wayne Pearce | Author in footer/header |

## Dependencies

- `pip install pandas weasyprint` — core pipeline
- `pip install numpy` — statistics
