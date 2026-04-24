#!/usr/bin/env python3
"""
Generate images for a LinkedIn article using the Gemini API.
Uses GEMINI_API_KEY from environment.
Standard library only — no pip installs needed.

Usage:
    python3 generate_images.py --output ./images "prompt 1" "prompt 2" "prompt 3"

Or import and use programmatically:
    from generate_images import generate_image
    image_bytes = generate_image("A clean professional illustration...")
"""

import urllib.request
import urllib.error
import json
import base64
import os
import ssl
import sys
import argparse
from pathlib import Path


API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3.1-flash-image-preview"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def generate_image(prompt: str, api_key: str = None) -> bytes:
    """Call Gemini API and return raw image bytes."""
    key = api_key or API_KEY
    if not key:
        raise ValueError("GEMINI_API_KEY not set")

    url = f"{ENDPOINT}?key={key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    # macOS Python SSL workaround — system certs often missing for urllib
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, timeout=180, context=ctx) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise ValueError(f"HTTP {e.code}: {error_body}")

    data = json.loads(raw.decode("utf-8"))

    # Find the image part in the response
    parts = data["candidates"][0]["content"]["parts"]
    for part in parts:
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])

    raise ValueError("No image found in API response")


def main():
    parser = argparse.ArgumentParser(description="Generate images via Gemini API")
    parser.add_argument("prompts", nargs="*", help="Image prompts")
    parser.add_argument("--output", "-o", default="./images", help="Output directory")
    parser.add_argument("--names", "-n", nargs="*", help="Output filenames (without extension)")
    args = parser.parse_args()

    if not API_KEY:
        print("Error: GEMINI_API_KEY not set in environment")
        sys.exit(1)

    if not args.prompts:
        print("Error: No prompts provided")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    names = args.names or [f"image-{i}" for i in range(1, len(args.prompts) + 1)]

    for i, (prompt, name) in enumerate(zip(args.prompts, names), 1):
        filename = f"{name}.png"
        print(f"[{i}/{len(args.prompts)}] Generating {filename}...")

        try:
            image_bytes = generate_image(prompt)
            output_path = output_dir / filename
            output_path.write_bytes(image_bytes)
            size_kb = len(image_bytes) / 1024
            print(f"  Saved: {output_path} ({size_kb:.0f} KB)")
        except Exception as e:
            print(f"  Error generating {filename}: {e}")
            continue

    print(f"\nDone! Images saved to: {output_dir}")


if __name__ == "__main__":
    main()
