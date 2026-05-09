"""General-purpose photo editing CLI powered by Pillow.

Usage:
    cd ~/.claude/skills/photo-edit/scripts
    uv run python photo_edit.py <command> [options] <files...>

First-time setup:
    cd ~/.claude/skills/photo-edit/scripts
    uv sync

Commands:
    resize      Resize images (preserving aspect ratio)
    crop        Crop to dimensions or aspect ratio
    rotate      Rotate or flip images
    adjust      Adjust brightness, contrast, saturation, sharpness
    convert     Convert between formats (PNG, JPEG, WebP)
    watermark   Add text or image watermark
    composite   Layer one image on top of another
    info        Print image metadata
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFont
except ImportError:
    print("ERROR: Pillow not installed.", file=sys.stderr)
    print("Run: cd ~/.claude/skills/photo-edit/scripts && uv sync", file=sys.stderr)
    sys.exit(1)


def resolve_output(input_path: Path, output_dir: str | None, suffix: str | None) -> Path:
    """Determine output path for a processed image."""
    parent = input_path.parent
    out_dir = Path(output_dir) if output_dir else parent / "edited"
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = input_path.stem
    ext = input_path.suffix
    if suffix:
        return out_dir / f"{stem}_{suffix}{ext}"
    return out_dir / f"{stem}{ext}"


def copy_exif(src: Image.Image, dst: Image.Image) -> Image.Image:
    """Copy EXIF data from source to destination if available."""
    exif = src.info.get("exif")
    if exif:
        dst.info["exif"] = exif
    return dst


def ensure_rgb(img: Image.Image) -> Image.Image:
    """Convert RGBA to RGB with white background (needed for JPEG)."""
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        return background
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def save_image(img: Image.Image, output_path: Path, quality: int | None, original: Image.Image | None = None) -> None:
    """Save image with format-appropriate settings."""
    fmt = output_path.suffix.lower().lstrip(".")
    fmt_map = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WebP"}
    pil_fmt = fmt_map.get(fmt, fmt.upper())

    kwargs: dict = {}
    if original:
        exif = original.info.get("exif")
        if exif and pil_fmt in ("JPEG", "WebP"):
            kwargs["exif"] = exif

    if pil_fmt == "JPEG":
        img = ensure_rgb(img)
        kwargs["quality"] = quality or 85
    elif pil_fmt == "WebP":
        kwargs["quality"] = quality or 85
    elif pil_fmt == "PNG":
        if quality:
            kwargs["compress_level"] = min(9, max(0, quality // 11))

    img.save(output_path, pil_fmt, **kwargs)


def process_files(args, handler) -> None:
    """Process each input file through a handler function."""
    files = [Path(f) for f in args.files]
    count = 0
    for f in files:
        if not f.exists():
            print(f"SKIP: {f} (not found)", file=sys.stderr)
            continue
        try:
            img = Image.open(f)
            result = handler(img, args)
            if result is not None:
                out = resolve_output(f, getattr(args, "output_dir", None), getattr(args, "suffix", None))
                save_image(result, out, getattr(args, "quality", None), original=img)
                print(f"  {f.name} -> {out}")
                count += 1
        except Exception as e:
            print(f"ERROR: {f.name}: {e}", file=sys.stderr)
    if count:
        print(f"\n{count} file(s) processed.")


# ── Resize ──────────────────────────────────────────

def cmd_resize(args) -> None:
    def handler(img: Image.Image, args) -> Image.Image:
        w, h = img.size
        if args.percent:
            factor = args.percent / 100
            new_w, new_h = int(w * factor), int(h * factor)
        elif args.max_dim:
            ratio = args.max_dim / max(w, h)
            new_w, new_h = int(w * ratio), int(h * ratio)
        elif args.width and args.height:
            new_w, new_h = args.width, args.height
        elif args.width:
            ratio = args.width / w
            new_w, new_h = args.width, int(h * ratio)
        elif args.height:
            ratio = args.height / h
            new_w, new_h = int(w * ratio), args.height
        else:
            print("ERROR: Specify --width, --height, --percent, or --max-dim", file=sys.stderr)
            sys.exit(1)
        return img.resize((new_w, new_h), Image.LANCZOS)

    print(f"Resizing...")
    process_files(args, handler)


# ── Crop ────────────────────────────────────────────

def cmd_crop(args) -> None:
    def handler(img: Image.Image, args) -> Image.Image:
        w, h = img.size
        if args.aspect:
            aw, ah = map(int, args.aspect.split(":"))
            target_ratio = aw / ah
            current_ratio = w / h
            if current_ratio > target_ratio:
                new_w = int(h * target_ratio)
                new_h = h
            else:
                new_w = w
                new_h = int(w / target_ratio)
        elif args.width and args.height:
            new_w, new_h = min(args.width, w), min(args.height, h)
        else:
            print("ERROR: Specify --width/--height or --aspect", file=sys.stderr)
            sys.exit(1)

        gravity = getattr(args, "gravity", "center")
        if gravity == "center":
            left = (w - new_w) // 2
            top = (h - new_h) // 2
        elif gravity == "top":
            left = (w - new_w) // 2
            top = 0
        elif gravity == "bottom":
            left = (w - new_w) // 2
            top = h - new_h
        elif gravity == "left":
            left = 0
            top = (h - new_h) // 2
        elif gravity == "right":
            left = w - new_w
            top = (h - new_h) // 2
        else:
            left = (w - new_w) // 2
            top = (h - new_h) // 2

        return img.crop((left, top, left + new_w, top + new_h))

    print(f"Cropping...")
    process_files(args, handler)


# ── Rotate ──────────────────────────────────────────

def cmd_rotate(args) -> None:
    def handler(img: Image.Image, args) -> Image.Image:
        if args.flip_h:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if args.flip_v:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if args.degrees:
            img = img.rotate(args.degrees, expand=True, resample=Image.LANCZOS)
        return img

    print(f"Rotating...")
    process_files(args, handler)


# ── Adjust ──────────────────────────────────────────

def cmd_adjust(args) -> None:
    def handler(img: Image.Image, args) -> Image.Image:
        if args.brightness and args.brightness != 1.0:
            img = ImageEnhance.Brightness(img).enhance(args.brightness)
        if args.contrast and args.contrast != 1.0:
            img = ImageEnhance.Contrast(img).enhance(args.contrast)
        if args.saturation and args.saturation != 1.0:
            img = ImageEnhance.Color(img).enhance(args.saturation)
        if args.sharpness and args.sharpness != 1.0:
            img = ImageEnhance.Sharpness(img).enhance(args.sharpness)
        return img

    print(f"Adjusting...")
    process_files(args, handler)


# ── Convert ─────────────────────────────────────────

def cmd_convert(args) -> None:
    def handler(img: Image.Image, args) -> Image.Image:
        return img

    # Override output extension
    original_resolve = resolve_output.__code__
    target_fmt = args.format.lower()
    ext_map = {"jpeg": ".jpg", "jpg": ".jpg", "png": ".png", "webp": ".webp"}
    target_ext = ext_map.get(target_fmt, f".{target_fmt}")

    files = [Path(f) for f in args.files]
    count = 0
    for f in files:
        if not f.exists():
            print(f"SKIP: {f} (not found)", file=sys.stderr)
            continue
        try:
            img = Image.open(f)
            out_dir = Path(args.output_dir) if args.output_dir else f.parent / "edited"
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = f.stem
            if args.suffix:
                out = out_dir / f"{stem}_{args.suffix}{target_ext}"
            else:
                out = out_dir / f"{stem}{target_ext}"
            save_image(img, out, args.quality, original=img)
            print(f"  {f.name} -> {out}")
            count += 1
        except Exception as e:
            print(f"ERROR: {f.name}: {e}", file=sys.stderr)
    if count:
        print(f"\n{count} file(s) converted to {target_fmt.upper()}.")


# ── Watermark ───────────────────────────────────────

def cmd_watermark(args) -> None:
    def handler(img: Image.Image, args) -> Image.Image:
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        if args.text:
            font_size = args.size or max(20, img.size[0] // 20)
            try:
                if args.font:
                    font = ImageFont.truetype(args.font, font_size)
                else:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), args.text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            pos = _watermark_position(img.size, (tw, th), args.position or "bottom-right")
            alpha = int(255 * (args.opacity if args.opacity is not None else 0.5))
            color = (255, 255, 255, alpha)
            draw.text(pos, args.text, font=font, fill=color)

        elif args.image:
            wm = Image.open(args.image).convert("RGBA")
            if args.size:
                ratio = args.size / max(wm.size)
                wm = wm.resize((int(wm.size[0] * ratio), int(wm.size[1] * ratio)), Image.LANCZOS)
            if args.opacity is not None and args.opacity < 1.0:
                alpha_channel = wm.split()[3]
                alpha_channel = alpha_channel.point(lambda p: int(p * args.opacity))
                wm.putalpha(alpha_channel)
            pos = _watermark_position(img.size, wm.size, args.position or "bottom-right")
            overlay.paste(wm, pos)
        else:
            print("ERROR: Specify --text or --image for watermark", file=sys.stderr)
            sys.exit(1)

        return Image.alpha_composite(img, overlay)

    print(f"Watermarking...")
    process_files(args, handler)


def _watermark_position(img_size: tuple, wm_size: tuple, position: str) -> tuple:
    """Calculate watermark position with 20px margin."""
    w, h = img_size
    ww, wh = wm_size
    margin = 20
    positions = {
        "top-left": (margin, margin),
        "top-right": (w - ww - margin, margin),
        "bottom-left": (margin, h - wh - margin),
        "bottom-right": (w - ww - margin, h - wh - margin),
        "center": ((w - ww) // 2, (h - wh) // 2),
    }
    return positions.get(position, positions["bottom-right"])


# ── Composite ───────────────────────────────────────

def cmd_composite(args) -> None:
    base = Image.open(args.files[0]).convert("RGBA")
    overlay_img = Image.open(args.overlay).convert("RGBA")

    if args.opacity is not None and args.opacity < 1.0:
        alpha_channel = overlay_img.split()[3]
        alpha_channel = alpha_channel.point(lambda p: int(p * args.opacity))
        overlay_img.putalpha(alpha_channel)

    x, y = 0, 0
    if args.position:
        parts = args.position.split(",")
        if len(parts) == 2:
            x, y = int(parts[0]), int(parts[1])

    result = base.copy()
    result.paste(overlay_img, (x, y), overlay_img)

    out = resolve_output(Path(args.files[0]), args.output_dir, args.suffix)
    save_image(result, out, args.quality, original=base)
    print(f"  {args.files[0]} + {args.overlay} -> {out}")


# ── Info ────────────────────────────────────────────

def cmd_info(args) -> None:
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"SKIP: {f} (not found)", file=sys.stderr)
            continue
        img = Image.open(p)
        size_kb = p.stat().st_size / 1024
        print(f"\n{p.name}")
        print(f"  Dimensions:  {img.size[0]} x {img.size[1]}")
        print(f"  Format:      {img.format}")
        print(f"  Mode:        {img.mode}")
        print(f"  File size:   {size_kb:.1f} KB")
        exif = img.getexif()
        if exif:
            print(f"  EXIF fields: {len(exif)}")


# ── CLI ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photo_edit",
        description="General-purpose photo editing CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Common args helper
    def add_common(p):
        p.add_argument("files", nargs="+", help="Input image file(s)")
        p.add_argument("--output-dir", "-o", help="Output directory (default: edited/)")
        p.add_argument("--suffix", "-s", help="Append suffix to output filename")
        p.add_argument("--quality", "-q", type=int, help="Output quality (1-100)")

    # resize
    p = sub.add_parser("resize", help="Resize images")
    add_common(p)
    p.add_argument("--width", "-W", type=int, help="Target width in pixels")
    p.add_argument("--height", "-H", type=int, help="Target height in pixels")
    p.add_argument("--percent", "-p", type=float, help="Scale by percentage (e.g. 50)")
    p.add_argument("--max-dim", type=int, help="Max dimension (longest side)")
    p.set_defaults(func=cmd_resize)

    # crop
    p = sub.add_parser("crop", help="Crop images")
    add_common(p)
    p.add_argument("--width", "-W", type=int, help="Crop width")
    p.add_argument("--height", "-H", type=int, help="Crop height")
    p.add_argument("--aspect", help="Aspect ratio (e.g. 16:9)")
    p.add_argument("--gravity", default="center", choices=["center", "top", "bottom", "left", "right"])
    p.set_defaults(func=cmd_crop)

    # rotate
    p = sub.add_parser("rotate", help="Rotate or flip images")
    add_common(p)
    p.add_argument("--degrees", "-d", type=float, help="Rotation angle (counter-clockwise)")
    p.add_argument("--flip-h", action="store_true", help="Flip horizontally")
    p.add_argument("--flip-v", action="store_true", help="Flip vertically")
    p.set_defaults(func=cmd_rotate)

    # adjust
    p = sub.add_parser("adjust", help="Adjust brightness, contrast, saturation, sharpness")
    add_common(p)
    p.add_argument("--brightness", "-b", type=float, help="Brightness multiplier (1.0 = unchanged)")
    p.add_argument("--contrast", "-c", type=float, help="Contrast multiplier")
    p.add_argument("--saturation", type=float, help="Saturation multiplier")
    p.add_argument("--sharpness", type=float, help="Sharpness multiplier")
    p.set_defaults(func=cmd_adjust)

    # convert
    p = sub.add_parser("convert", help="Convert image format")
    add_common(p)
    p.add_argument("--format", "-f", required=True, choices=["jpeg", "jpg", "png", "webp"], help="Target format")
    p.set_defaults(func=cmd_convert)

    # watermark
    p = sub.add_parser("watermark", help="Add text or image watermark")
    add_common(p)
    p.add_argument("--text", "-t", help="Watermark text")
    p.add_argument("--image", "-i", help="Watermark image path")
    p.add_argument("--position", choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"], default="bottom-right")
    p.add_argument("--opacity", type=float, help="Watermark opacity (0.0-1.0)")
    p.add_argument("--size", type=int, help="Font size (text) or max dimension (image)")
    p.add_argument("--font", help="Path to .ttf/.otf font file")
    p.set_defaults(func=cmd_watermark)

    # composite
    p = sub.add_parser("composite", help="Layer one image on another")
    add_common(p)
    p.add_argument("--overlay", required=True, help="Overlay image path")
    p.add_argument("--position", help="Position as x,y (e.g. 100,50)")
    p.add_argument("--opacity", type=float, help="Overlay opacity (0.0-1.0)")
    p.set_defaults(func=cmd_composite)

    # info
    p = sub.add_parser("info", help="Print image metadata")
    p.add_argument("files", nargs="+", help="Input image file(s)")
    p.set_defaults(func=cmd_info)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
