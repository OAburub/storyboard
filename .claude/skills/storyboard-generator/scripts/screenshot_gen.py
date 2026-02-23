#!/usr/bin/env python3
"""
screenshot_gen.py — HTML → PNG via Playwright (Chromium)

Usage:
    python screenshot_gen.py <html_path> <output_path> [width] [height] [wait_ms]

Args:
    html_path   : Path to HTML file
    output_path : Where to save PNG
    width       : Viewport width  (default: 1280)
    height      : Viewport height (default: 720)
    wait_ms     : Wait before capture in ms (default: 500; use 1500 if Google Fonts)

Output:
    Prints output_path on success.
    Prints "ERROR: <message>" and exits 1 on failure.
    Prints "CACHED: <path>" and exits 0 if PNG already exists (skip regeneration).
"""

import sys
import os
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("ERROR: Usage: screenshot_gen.py <html_path> <output_path> [width] [height] [wait_ms]")
        sys.exit(1)

    html_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 720
    wait_ms = int(sys.argv[5]) if len(sys.argv) > 5 else 500

    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}")
        sys.exit(1)

    # Cache: if PNG exists, skip
    if output_path.exists():
        print(f"CACHED: {output_path}")
        sys.exit(0)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(html_path.as_uri())
            if wait_ms > 0:
                page.wait_for_timeout(wait_ms)
            page.screenshot(path=str(output_path))
            browser.close()
        print(str(output_path))
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
