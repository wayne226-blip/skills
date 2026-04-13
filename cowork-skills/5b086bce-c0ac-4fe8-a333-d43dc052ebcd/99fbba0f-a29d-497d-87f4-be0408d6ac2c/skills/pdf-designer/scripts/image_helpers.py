#!/usr/bin/env python3
"""Image helper utilities for embedding images in WeasyPrint HTML.

Usage (library):
    from image_helpers import image_to_base64_uri, generate_img_tag

    uri = image_to_base64_uri("photo.png")
    tag = generate_img_tag("photo.png", width="80%", css_class="hero")

Usage (CLI):
    python image_helpers.py photo.png                    # prints data URI
    python image_helpers.py photo.png --html             # prints <img> tag
    python image_helpers.py photo.png --html --width 60% # with custom width
"""

import argparse
import base64
import os
import sys
from pathlib import Path


def image_to_base64_uri(image_path):
    """Convert an image file to a base64 data URI string."""
    ext = Path(image_path).suffix.lower()
    mime_map = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp",
    }
    mime = mime_map.get(ext, "image/png")
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def generate_img_tag(image_path, width="100%", css_class=""):
    """Generate an HTML <img> tag with base64-embedded image data."""
    uri = image_to_base64_uri(image_path)
    cls = f' class="{css_class}"' if css_class else ''
    alt = Path(image_path).stem
    return (
        f'<img src="{uri}"{cls} '
        f'style="width: {width}; display: block; margin: 1em auto;" '
        f'alt="{alt}">'
    )


def generate_img_tags(image_paths, width="100%", css_class=""):
    """Generate HTML img tags for multiple images."""
    return "\n".join(generate_img_tag(p, width, css_class) for p in image_paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image embedding helpers for WeasyPrint")
    parser.add_argument("image", help="Image file path")
    parser.add_argument("--html", action="store_true", help="Output full <img> tag")
    parser.add_argument("--width", default="100%", help="CSS width (default: 100%%)")
    parser.add_argument("--css-class", default="", help="CSS class to add")
    args = parser.parse_args()
    if not os.path.exists(args.image):
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)
    if args.html:
        print(generate_img_tag(args.image, width=args.width, css_class=args.css_class))
    else:
        print(image_to_base64_uri(args.image))
