#!/usr/bin/env python
"""
Optimize an image for web / social (Open Graph) previews.

Resizes the image to a maximum width and compresses it so the output stays
under a target file size. Useful for making cover images that WhatsApp,
Twitter, etc. will actually fetch and render (they skip images that are too big).

Usage:
    python optimize_image.py <input> [--output PATH] [--max-width 1200]
                             [--max-kb 300] [--suffix -opt]

Examples:
    # Create an optimized copy next to the original (foo-opt.jpg)
    python optimize_image.py content/image/post/photo.png

    # Explicit output path and limits
    python optimize_image.py photo.png --output photo-small.jpg --max-width 1080 --max-kb 250
"""

import argparse
import os
import sys

from PIL import Image


def optimize(input_path, output_path, max_width, max_kb):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    img = Image.open(input_path)

    # Flatten transparency onto white so we can save as JPEG.
    if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        rgba = img.convert("RGBA")
        background.paste(rgba, mask=rgba.split()[-1])
        img = background
    else:
        img = img.convert("RGB")

    # Resize down to max_width, keeping aspect ratio.
    if img.width > max_width:
        new_height = round(img.height * max_width / img.width)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    target_bytes = max_kb * 1024

    # Step quality down until we hit the target size (or the floor).
    quality = 90
    while quality >= 30:
        img.save(output_path, format="JPEG", quality=quality, optimize=True)
        size = os.path.getsize(output_path)
        if size <= target_bytes:
            break
        quality -= 5

    return output_path, os.path.getsize(output_path), img.size


def build_output_path(input_path, suffix):
    root, _ = os.path.splitext(input_path)
    return f"{root}{suffix}.jpg"


def main():
    parser = argparse.ArgumentParser(description="Optimize an image for web / OG previews.")
    parser.add_argument("input", help="Path to the source image")
    parser.add_argument("--output", help="Output path (default: <input><suffix>.jpg)")
    parser.add_argument("--max-width", type=int, default=1200, help="Max width in pixels (default: 1200)")
    parser.add_argument("--max-kb", type=int, default=300, help="Target max size in KB (default: 300)")
    parser.add_argument("--suffix", default="-opt", help="Suffix for auto-named output (default: -opt)")
    args = parser.parse_args()

    output_path = args.output or build_output_path(args.input, args.suffix)

    out, size_bytes, dimensions = optimize(
        args.input, output_path, args.max_width, args.max_kb
    )

    original_size = os.path.getsize(args.input)
    print(f"Input:  {args.input} ({original_size / 1024:.0f} KB)")
    print(f"Output: {out} ({size_bytes / 1024:.0f} KB, {dimensions[0]}x{dimensions[1]})")


if __name__ == "__main__":
    sys.exit(main())
