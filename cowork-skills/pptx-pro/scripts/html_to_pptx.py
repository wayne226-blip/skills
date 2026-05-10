#!/usr/bin/env python3
"""Convert HTML or Markdown to PPTX using Pandoc.

Each H1 or H2 heading creates a new slide. Content under each heading
becomes the slide body. Pandoc handles tables, lists, links, images,
and code blocks automatically.

Usage:
    python html_to_pptx.py input.html output.pptx
    python html_to_pptx.py input.md output.pptx
    python html_to_pptx.py --from-string "# Slide 1\n\nBullet points" output.pptx
    python html_to_pptx.py input.md output.pptx --reference template.pptx
"""

import sys
import argparse
import os
import subprocess
import shutil


def detect_format(filename):
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
    }
    return format_map.get(ext, "html")


def main():
    parser = argparse.ArgumentParser(
        description="Convert HTML/Markdown to PPTX using Pandoc"
    )
    parser.add_argument("input", nargs="?", help="Input file (HTML, Markdown, etc.)")
    parser.add_argument("output", help="Output PPTX file")
    parser.add_argument(
        "--from-string", help="HTML/Markdown string to convert (instead of file)"
    )
    parser.add_argument(
        "--from-format",
        help="Force input format: html, markdown, gfm, rst, org, latex",
    )
    parser.add_argument(
        "--reference",
        help="Reference PPTX template for styles (fonts, colors, layouts)",
    )
    parser.add_argument(
        "--slide-level",
        type=int,
        default=2,
        help="Heading level that creates new slides (default: 2, meaning H1 and H2 create slides)",
    )
    parser.add_argument(
        "--highlight-style",
        default="tango",
        help="Code highlighting style: tango, pygments, espresso, etc.",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Make lists display incrementally (one bullet at a time)",
    )
    args = parser.parse_args()

    if not args.from_string and not args.input:
        parser.error("Either provide an input file or use --from-string")

    if not shutil.which("pandoc"):
        print("Error: pandoc is not installed", file=sys.stderr)
        sys.exit(1)

    # Build pandoc command
    cmd = ["pandoc"]

    # Input format
    input_format = args.from_format or (
        "html" if args.from_string else detect_format(args.input)
    )
    cmd.extend(["-f", input_format])

    # Output
    cmd.extend(["-t", "pptx", "-o", args.output])

    # Reference template
    if args.reference:
        cmd.extend(["--reference-doc", args.reference])

    # Slide level
    cmd.extend(["--slide-level", str(args.slide_level)])

    # Code highlighting
    if args.highlight_style:
        cmd.extend(["--highlight-style", args.highlight_style])

    # Incremental lists
    if args.incremental:
        cmd.append("--incremental")

    # Standalone
    cmd.append("-s")

    # Input file (if not from string)
    if not args.from_string:
        cmd.append(args.input)

    try:
        result = subprocess.run(
            cmd,
            input=args.from_string if args.from_string else None,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        print("Error: pandoc timed out after 60 seconds", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(f"Error: pandoc failed\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(args.output)
    print(f"PPTX created: {args.output} ({file_size:,} bytes)")


if __name__ == "__main__":
    main()
