#!/usr/bin/env python3
"""
Convert HTML or Markdown to DOCX using Pandoc.

Much faster than building DOCX programmatically with docx-js when you already
have content as HTML or Markdown. Supports style templates via --reference.

Usage:
    python html_to_docx.py input.html output.docx
    python html_to_docx.py input.md output.docx
    python html_to_docx.py --from-string "<h1>Hello</h1>" output.docx
    python html_to_docx.py input.html output.docx --reference template.docx

Options:
    --from-string HTML      Pass HTML/Markdown as a string instead of a file
    --from-format FORMAT    Input format: html, markdown, gfm (default: auto-detect)
    --reference FILE        Reference DOCX for styles/formatting (template)
    --toc                   Include table of contents
    --toc-depth N           TOC depth (default: 3)
    --highlight-style STYLE Code highlighting: pygments, tango, espresso, etc.
"""

import sys
import argparse
import os
import subprocess
import shutil


def detect_format(filename):
    """Auto-detect input format from extension."""
    ext = os.path.splitext(filename)[1].lower()
    format_map = {
        ".html": "html",
        ".htm": "html",
        ".md": "markdown",
        ".markdown": "markdown",
        ".txt": "markdown",
        ".rst": "rst",
        ".org": "org",
        ".tex": "latex",
        ".epub": "epub",
    }
    return format_map.get(ext, "html")


def main():
    parser = argparse.ArgumentParser(description="Convert HTML/Markdown to DOCX")
    parser.add_argument("input", nargs="?", help="Input file (HTML, Markdown, etc.)")
    parser.add_argument("output", help="Output DOCX file")
    parser.add_argument("--from-string", help="HTML/Markdown string to convert")
    parser.add_argument("--from-format", help="Input format (default: auto-detect)")
    parser.add_argument("--reference", help="Reference DOCX template for styles")
    parser.add_argument("--toc", action="store_true", help="Include table of contents")
    parser.add_argument("--toc-depth", type=int, default=3, help="TOC depth (default: 3)")
    parser.add_argument(
        "--highlight-style",
        default="tango",
        help="Code highlight style (default: tango)",
    )

    args = parser.parse_args()

    if not args.from_string and not args.input:
        parser.error("Either provide an input file or use --from-string")

    if not shutil.which("pandoc"):
        print("Error: pandoc is not installed", file=sys.stderr)
        sys.exit(1)

    cmd = ["pandoc"]

    if args.from_string:
        input_format = args.from_format or "html"
    else:
        input_format = args.from_format or detect_format(args.input)

    cmd.extend(["-f", input_format])
    cmd.extend(["-t", "docx"])
    cmd.extend(["-o", args.output])

    if args.reference:
        cmd.extend(["--reference-doc", args.reference])

    if args.toc:
        cmd.append("--toc")
        cmd.extend(["--toc-depth", str(args.toc_depth)])

    if args.highlight_style:
        cmd.extend(["--highlight-style", args.highlight_style])

    cmd.append("-s")

    if not args.from_string:
        cmd.append(args.input)

    if args.from_string:
        result = subprocess.run(
            cmd, input=args.from_string, capture_output=True, text=True, timeout=60
        )
    else:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        print(f"Error: pandoc failed\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if result.stderr:
        print(f"Warnings: {result.stderr}", file=sys.stderr)

    file_size = os.path.getsize(args.output)
    print(f"DOCX created: {args.output} ({file_size:,} bytes)")


if __name__ == "__main__":
    main()
