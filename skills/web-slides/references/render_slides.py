"""Render HTML slides to individual PNGs using Playwright + headless Chromium.

Usage:
    cd ~/.claude/skills/web-slides/references
    uv run python render_slides.py <slides.html> <output-dir/>

First-time setup:
    cd ~/.claude/skills/web-slides/references
    uv sync
    uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def render_slides(
    html_path: Path,
    output_dir: Path,
    scale: int = 1,
) -> list[Path]:
    """Render each .slide section in an HTML file to a PNG. Returns list of output paths."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.", file=sys.stderr)
        print("Run: cd ~/.claude/skills/web-slides/references && uv sync && uv run playwright install chromium", file=sys.stderr)
        sys.exit(1)

    if not html_path.exists():
        print(f"ERROR: File not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    file_url = html_path.resolve().as_uri()
    outputs: list[Path] = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                print("ERROR: Chromium not installed for Playwright.", file=sys.stderr)
                print("Run: cd ~/.claude/skills/web-slides/references && uv run playwright install chromium", file=sys.stderr)
                sys.exit(1)
            raise

        # Use 1920x1080 viewport — matches our slide dimensions
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=scale,
        )

        page.goto(file_url)

        # Wait for Tailwind CDN to compile styles + Google Fonts to load
        # Tailwind Play CDN compiles on DOMContentLoaded, but we give it extra time
        page.wait_for_load_state("networkidle")

        # Wait for fonts to be ready
        try:
            page.evaluate("() => document.fonts.ready")
        except Exception:
            pass  # Fonts API might not be available, that's fine

        # Small extra wait for Tailwind JIT compilation
        time.sleep(1)

        # Find all slide sections
        slides = page.query_selector_all(".slide")
        if not slides:
            print("ERROR: No .slide elements found in the HTML file.", file=sys.stderr)
            browser.close()
            sys.exit(1)

        print(f"Found {len(slides)} slides. Screenshotting...")

        for i, slide in enumerate(slides):
            filename = f"slide-{i + 1:02d}.png"
            out_path = output_dir / filename

            # Scroll the slide into view and screenshot it
            slide.scroll_into_view_if_needed()
            time.sleep(0.3)  # Brief pause for any CSS transitions to settle
            slide.screenshot(path=str(out_path))

            print(f"  {filename} -> {out_path}")
            outputs.append(out_path)

        browser.close()

    print(f"\nDone. {len(outputs)} slides saved to {output_dir}")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Render HTML slides to individual PNGs")
    parser.add_argument("input", type=Path, help="Path to slides HTML file")
    parser.add_argument("output_dir", type=Path, help="Directory to save slide PNGs")
    parser.add_argument("--scale", "-s", type=int, default=1, help="Device scale factor (default: 1)")
    args = parser.parse_args()

    render_slides(args.input, args.output_dir, args.scale)


if __name__ == "__main__":
    main()
