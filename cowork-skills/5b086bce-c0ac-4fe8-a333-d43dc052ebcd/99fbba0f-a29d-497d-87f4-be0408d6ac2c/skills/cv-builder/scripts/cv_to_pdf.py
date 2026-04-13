#!/usr/bin/env python3
"""Convert a CV markdown file to PDF using reportlab."""
import sys
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def md_to_pdf(input_md, output_pdf):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=16*mm,
        bottomMargin=16*mm,
    )

    styles = getSampleStyleSheet()
    accent = colors.HexColor("#1a1a2e")

    name_style = ParagraphStyle("Name", fontSize=22, textColor=accent,
                                spaceAfter=2, fontName="Helvetica-Bold", alignment=TA_CENTER)
    contact_style = ParagraphStyle("Contact", fontSize=9, textColor=colors.HexColor("#555555"),
                                   spaceAfter=6, alignment=TA_CENTER)
    h2_style = ParagraphStyle("H2", fontSize=11, textColor=accent, spaceBefore=10,
                               spaceAfter=3, fontName="Helvetica-Bold")
    job_title_style = ParagraphStyle("JobTitle", fontSize=10, spaceBefore=6,
                                     spaceAfter=1, fontName="Helvetica-Bold")
    meta_style = ParagraphStyle("Meta", fontSize=9, textColor=colors.HexColor("#666666"),
                                spaceAfter=2, fontName="Helvetica-Oblique")
    body_style = ParagraphStyle("Body", fontSize=9.5, spaceAfter=3, leading=14)
    bullet_style = ParagraphStyle("Bullet", fontSize=9.5, spaceAfter=2,
                                  leftIndent=12, leading=13, bulletIndent=0)

    story = []

    with open(input_md, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # H1 = name
        if line.startswith("# ") and not line.startswith("## "):
            story.append(Paragraph(line[2:], name_style))
            i += 1
            continue

        # H2 = section heading
        if line.startswith("## "):
            story.append(HRFlowable(width="100%", thickness=0.5,
                                    color=colors.HexColor("#cccccc"), spaceAfter=2))
            story.append(Paragraph(line[3:].upper(), h2_style))
            i += 1
            continue

        # H3 = job title / institution
        if line.startswith("### "):
            story.append(Paragraph(line[4:], job_title_style))
            i += 1
            continue

        # Bullet points
        if line.startswith("- "):
            text = line[2:]
            # bold any **text**
            text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
            story.append(Paragraph(f"• {text}", bullet_style))
            i += 1
            continue

        # Bold line (e.g. **Company — Role** | dates)
        if line.startswith("**") or ("|" in line and "---" not in line and line.strip()):
            text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            story.append(Paragraph(text, meta_style))
            i += 1
            continue

        # Horizontal rule
        if line.startswith("---"):
            story.append(Spacer(1, 3))
            i += 1
            continue

        # Empty line
        if not line.strip():
            story.append(Spacer(1, 3))
            i += 1
            continue

        # Plain text
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
        story.append(Paragraph(text, body_style))
        i += 1

    doc.build(story)
    print(f"PDF saved: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 cv_to_pdf.py input.md output.pdf")
        sys.exit(1)
    md_to_pdf(sys.argv[1], sys.argv[2])
