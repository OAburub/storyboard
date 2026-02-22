#!/usr/bin/env python3
"""Test Gemini SVG generation — tries multiple models."""

import os
os.environ["GEMINI_API_KEY"] = "AIzaSyDNpJzwtR62rXRqJs0RCyfF6ldpE3fZ0kY"

from google import genai
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# First, list available models to find the right one
print("=== Listing available models ===")
for m in client.models.list():
    if "flash" in m.name.lower() or "pro" in m.name.lower():
        print(f"  {m.name}")

print("\n=== Testing SVG generation ===")

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

# Try models in order of preference
models_to_try = [
    "gemini-2.5-flash-preview-04-17",
    "gemini-2.5-pro-preview-05-06",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]

svg_code = None
used_model = None

for model_name in models_to_try:
    print(f"\nTrying model: {model_name} ...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        raw = response.text
        print(f"  Got response ({len(raw)} chars)")

        # Extract SVG from response (strip markdown fences if present)
        if "```" in raw:
            parts = raw.split("```")
            for part in parts[1:]:
                if part.strip().startswith("svg") or part.strip().startswith("xml") or part.strip().startswith("<svg"):
                    svg_code = part.strip()
                    if svg_code.startswith("svg") or svg_code.startswith("xml"):
                        svg_code = svg_code.split("\n", 1)[1]
                    break
            if not svg_code:
                # Try the second part directly
                svg_code = parts[1].strip()
                if svg_code.startswith("svg") or svg_code.startswith("xml"):
                    svg_code = svg_code.split("\n", 1)[1]
        elif "<svg" in raw:
            # Raw SVG without fences
            start = raw.index("<svg")
            svg_code = raw[start:]

        if svg_code and "<svg" in svg_code:
            used_model = model_name
            print(f"  SUCCESS! Got valid SVG ({len(svg_code)} chars)")
            break
        else:
            print(f"  No valid SVG found in response")
            svg_code = None
    except Exception as e:
        print(f"  Error: {e}")

if svg_code:
    # Save SVG
    os.makedirs("/Users/qusaiabushanap/dev/storyboard/output/TEST/slides", exist_ok=True)
    out_path = "/Users/qusaiabushanap/dev/storyboard/output/TEST/slides/test_process_flow.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    print(f"\n=== SVG saved to {out_path} ===")
    print(f"Model used: {used_model}")
    print(f"SVG size: {len(svg_code)} chars")

    # Check SVG quality indicators
    has_gradient = "linearGradient" in svg_code or "radialGradient" in svg_code
    has_shadow = "filter" in svg_code or "feDropShadow" in svg_code or "feGaussianBlur" in svg_code
    has_arabic = "التحليل" in svg_code
    has_rounded = "rx=" in svg_code

    print(f"\nQuality check:")
    print(f"  Gradients: {'YES' if has_gradient else 'NO'}")
    print(f"  Shadows: {'YES' if has_shadow else 'NO'}")
    print(f"  Arabic text: {'YES' if has_arabic else 'NO'}")
    print(f"  Rounded corners: {'YES' if has_rounded else 'NO'}")
else:
    print("\n=== FAILED: No model produced valid SVG ===")
