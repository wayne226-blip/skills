#!/usr/bin/env python3
"""
LinkedIn Publisher — copies post text to clipboard and opens LinkedIn share dialog.

Usage:
    python3 publish.py --text "Your LinkedIn post text here"
    python3 publish.py --file /path/to/post.txt

Semi-automated approach: copies to clipboard, opens browser.
User pastes and clicks Post. This avoids LinkedIn's automation detection
which can restrict or ban accounts.
"""

import argparse
import subprocess
import sys
import urllib.parse
import webbrowser


def copy_to_clipboard(text: str) -> bool:
    """Copy text to macOS clipboard using pbcopy."""
    try:
        process = subprocess.Popen(
            ["pbcopy"],
            stdin=subprocess.PIPE,
            env={"LANG": "en_US.UTF-8"}
        )
        process.communicate(text.encode("utf-8"))
        return process.returncode == 0
    except FileNotFoundError:
        # Not on macOS — try xclip as fallback (Linux)
        try:
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"],
                stdin=subprocess.PIPE
            )
            process.communicate(text.encode("utf-8"))
            return process.returncode == 0
        except FileNotFoundError:
            return False


def open_linkedin_share(text: str = "") -> None:
    """Open LinkedIn's share dialog in the default browser.

    Uses the LinkedIn share URL which pre-fills are limited,
    so we rely on clipboard paste instead.
    """
    # LinkedIn's share page — user can paste from clipboard
    url = "https://www.linkedin.com/feed/?shareActive=true"
    webbrowser.open(url)


def main():
    parser = argparse.ArgumentParser(description="Publish a post to LinkedIn")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="The post text to publish")
    group.add_argument("--file", type=str, help="Path to a file containing the post text")

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text

    if not text:
        print("Error: No text provided", file=sys.stderr)
        sys.exit(1)

    # Strip hashtags onto their own line if they're inline
    # (LinkedIn renders them better on a separate line)

    # Copy to clipboard
    if copy_to_clipboard(text):
        print("Post copied to clipboard.")
    else:
        print("Warning: Could not copy to clipboard. Text below for manual copy:", file=sys.stderr)
        print("---")
        print(text)
        print("---")

    # Open LinkedIn
    open_linkedin_share(text)
    print("LinkedIn share dialog opening in browser.")
    print("\nNext steps:")
    print("  1. Click in the post text area")
    print("  2. Cmd+V (or Ctrl+V) to paste")
    print("  3. Hit Post")


if __name__ == "__main__":
    main()
