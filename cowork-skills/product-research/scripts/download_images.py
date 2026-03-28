#!/usr/bin/env python3
"""Download product images from URLs for embedding in research reports.

Usage:
    python download_images.py "https://example.com/image.jpg" /tmp/product_images/product.jpg
    python download_images.py "URL1" "URL2" "URL3" --output-dir /tmp/product_images/
    python download_images.py --search "Sony WH-1000XM5" --output-dir /tmp/product_images/

The script handles:
- Following redirects
- Setting proper User-Agent headers (some sites block default Python UA)
- Timeout handling (10s default)
- Creating output directories automatically
- Skipping already-downloaded files
- Returning the path of successfully downloaded images
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def download_image(url, output_path, timeout=10):
    """Download a single image from a URL.

    Returns the output path on success, None on failure.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip if already downloaded
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"Already exists: {output_path}")
        return str(output_path)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")

            # Validate it's actually an image
            if not any(t in content_type for t in ["image/", "octet-stream", "binary"]):
                # Some servers don't set content-type properly for images,
                # so check file extension as fallback
                ext = output_path.suffix.lower()
                if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"):
                    print(f"Skipped (not an image): {url} — Content-Type: {content_type}", file=sys.stderr)
                    return None

            data = response.read()

            # Basic sanity check — images should be at least a few hundred bytes
            if len(data) < 200:
                print(f"Skipped (too small, likely error page): {url} — {len(data)} bytes", file=sys.stderr)
                return None

            with open(output_path, "wb") as f:
                f.write(data)

            print(f"Downloaded: {output_path} ({len(data):,} bytes)")
            return str(output_path)

    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for {url}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL error for {url}: {e.reason}", file=sys.stderr)
        return None
    except TimeoutError:
        print(f"Timeout downloading {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return None


def download_multiple(urls, output_dir, prefix="product"):
    """Download multiple images, naming them sequentially.

    Returns list of successfully downloaded file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for i, url in enumerate(urls):
        # Try to preserve the original extension
        url_path = url.split("?")[0]  # strip query params
        ext = Path(url_path).suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
            ext = ".jpg"  # default to jpg

        output_path = output_dir / f"{prefix}_{i+1}{ext}"
        result = download_image(url, output_path)
        if result:
            downloaded.append(result)

    return downloaded


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download product images for research reports")
    parser.add_argument("urls", nargs="*", help="Image URL(s) to download")
    parser.add_argument("--output-dir", "-o", default="/tmp/product_images", help="Output directory")
    parser.add_argument("--prefix", "-p", default="product", help="Filename prefix (default: product)")
    parser.add_argument("--timeout", "-t", type=int, default=10, help="Download timeout in seconds")
    args = parser.parse_args()

    if not args.urls:
        print("Usage: python download_images.py URL [URL ...] [--output-dir DIR]", file=sys.stderr)
        sys.exit(1)

    # If single URL with a second positional arg, treat second as output path
    if len(args.urls) == 2 and not args.urls[1].startswith("http"):
        result = download_image(args.urls[0], args.urls[1], timeout=args.timeout)
        sys.exit(0 if result else 1)

    # Multiple URLs
    downloaded = download_multiple(args.urls, args.output_dir, prefix=args.prefix)
    print(f"\nDownloaded {len(downloaded)}/{len(args.urls)} images")
    for path in downloaded:
        print(f"  {path}")
