#!/usr/bin/env python3
"""Test gemini-2.5-flash for SVG generation quality."""

import os
os.environ["GEMINI_API_KEY"] = "AIzaSyDNpJzwtR62rXRqJs0RCyfF6ldpE3fZ0kY"

from google import genai
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = """Generate a self-contained SVG (viewBox="0 0 1280 720") showing a professional 4-step process flow for educational content.

Requirements:
- Steps flow RIGHT to LEFT (Arabic RTL direction)
- Steps: 1-التحليل (Analysis), 2-التصميم (Design), 3-التنفيذ (Implementation), 4-الاختبار (Testing)
- Each step is a rounded rectangle card with gradient fill from #2D588C to #4A90D9
- Cards connected by curved arrows pointing left
- White text on cards, Tajawal font family
- Step number in a circle above each card
- Subtle drop shadows on cards
- Background: light gradient from #F8F9FA to #EEF2F7
- Modern, premium, clean design — like a top design agency made it
- NO animation tags — static SVG only
- Return ONLY the raw SVG code, nothing else"""

print("Trying gemini-2.5-flash...", flush=True)
try:
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    raw = response.text
    print(f"Response: {len(raw)} chars", flush=True)

    svg_code = None

    if "```" in raw:
        parts = raw.split("```")
        for part in parts[1:]:
            stripped = part.strip()
            if "<svg" in stripped:
                svg_code = stripped
                # Remove language tag if present
                first_line = svg_code.split("\n", 1)[0].strip().lower()
                if first_line in ("svg", "xml", "html"):
                    svg_code = svg_code.split("\n", 1)[1]
                break
    elif "<svg" in raw:
        start = raw.index("<svg")
        svg_code = raw[start:]

    if svg_code and "<svg" in svg_code:
        out = "/Users/qusaiabushanap/dev/storyboard/output/TEST/slides/test_25flash.svg"
        with open(out, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"Saved: {out} ({len(svg_code)} chars)", flush=True)

        has_gradient = "linearGradient" in svg_code or "radialGradient" in svg_code
        has_shadow = "filter" in svg_code or "feGaussianBlur" in svg_code
        has_arabic = "التحليل" in svg_code
        has_rounded = "rx=" in svg_code
        print(f"Gradients: {has_gradient}, Shadows: {has_shadow}, Arabic: {has_arabic}, Rounded: {has_rounded}", flush=True)
    else:
        print("No valid SVG found in response", flush=True)
        print(f"First 500 chars: {raw[:500]}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
