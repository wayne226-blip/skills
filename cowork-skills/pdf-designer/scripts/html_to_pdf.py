#!/usr/bin/env python3
"""
Convert HTML to high-quality PDF using WeasyPrint.

Supports full CSS3 including @page rules, flexbox, web fonts,
headers/footers, page numbers, and multi-column layouts.

Usage:
    python html_to_pdf.py input.html output.pdf
    python html_to_pdf.py input.html output.pdf --base-url ./assets/
    python html_to_pdf.py --from-string "<h1>Hello</h1>" output.pdf

Options:
    --base-url DIR      Base URL for resolving relative paths (images, CSS, fonts)
    --from-string HTML  Pass HTML as a string instead of a file
    --css FILE          Additional CSS stylesheet to apply
    --landscape         Use landscape orientation (overrides @page in HTML)
    --size SIZE         Paper size: letter, a4, legal (default: letter)
    --margin MARGIN     Page margin e.g. "1in" or "2cm" (default: 1in)
"""

import sys
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Convert HTML to PDF using WeasyPrint")
    parser.add_argument("input", nargs="?", help="Input HTML file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--base-url", help="Base URL for resolving relative paths")
    parser.add_argument("--from-string", help="HTML string to convert (instead of file)")
    parser.add_argument("--css", action="append", help="Additional CSS file(s) to apply")
    parser.add_argument("--landscape", action="store_true", help="Use landscape orientation")
    parser.add_argument(
        "--size",
        default="letter",
        choices=["letter", "a4", "legal"],
        help="Paper size (default: letter)",
    )
    parser.add_argument("--margin", default="1in", help="Page margin (default: 1in)")

    args = parser.parse_args()

    if not args.from_string and not args.input:
        parser.error("Either provide an input HTML file or use --from-string")

    from weasyprint import HTML, CSS

    size_map = {
        "letter": "8.5in 11in",
        "a4": "210mm 297mm",
        "legal": "8.5in 14in",
    }
    size_str = size_map[args.size]
    if args.landscape:
        parts = size_str.split()
        size_str = f"{parts[1]} {parts[0]}"

    override_css = CSS(
        string=f"""
        @page {{
            size: {size_str};
            margin: {args.margin};
        }}
    """
    )

    stylesheets = [override_css]
    if args.css:
        for css_file in args.css:
            stylesheets.append(CSS(filename=css_file))

    if args.from_string:
        base_url = args.base_url or os.getcwd()
        doc = HTML(string=args.from_string, base_url=base_url)
    else:
        base_url = args.base_url or os.path.dirname(os.path.abspath(args.input))
        doc = HTML(filename=args.input, base_url=base_url)

    doc.write_pdf(args.output, stylesheets=stylesheets)

    file_size = os.path.getsize(args.output)
    print(f"PDF created: {args.output} ({file_size:,} bytes)")


if __name__ == "__main__":
    main()
