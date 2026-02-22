#!/usr/bin/env python3
"""Test gemini-3.1-pro-preview for SVG generation — both static and animated."""

import sys
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard/.claude/skills/storyboard-generator/scripts')

from _pptx_svg_generator import generate_slide_svg

COLORS = {
    "primary": "#2D588C",
    "secondary": "#4A90D9",
    "accent": "#F5A623",
}

STEPS = [
    {"num": 1, "label": "التحليل", "desc": "تحديد الاحتياجات والأهداف"},
    {"num": 2, "label": "التصميم", "desc": "تصميم المحتوى والأنشطة"},
    {"num": 3, "label": "التطوير", "desc": "إنتاج المواد التعليمية"},
    {"num": 4, "label": "التقييم", "desc": "قياس فعالية التعلم"},
]

OUT_DIR = "/Users/qusaiabushanap/dev/storyboard/output/TEST/slides"

# Test 1: Static SVG (for PPTX embedding)
print("=" * 60, flush=True)
print("Test 1: Static SVG (gemini-3.1-pro-preview)", flush=True)
print("=" * 60, flush=True)

result_static = generate_slide_svg(
    pattern_type="process_flow",
    data=STEPS,
    colors=COLORS,
    title="مراحل التصميم التعليمي",
    output_path=f"{OUT_DIR}/test_31pro_static.svg",
    animated=False,
)
print(f"Static result: {result_static}", flush=True)

# Test 2: Animated SVG (with CSS @keyframes)
print("\n" + "=" * 60, flush=True)
print("Test 2: Animated SVG (gemini-3.1-pro-preview)", flush=True)
print("=" * 60, flush=True)

result_animated = generate_slide_svg(
    pattern_type="process_flow",
    data=STEPS,
    colors=COLORS,
    title="مراحل التصميم التعليمي",
    output_path=f"{OUT_DIR}/test_31pro_animated.svg",
    animated=True,
)
print(f"Animated result: {result_animated}", flush=True)

# Check animated SVG has @keyframes
if result_animated:
    with open(result_animated, "r") as f:
        content = f.read()
    has_keyframes = "@keyframes" in content
    has_style = "<style" in content
    has_animation = "animation" in content
    print(f"\nAnimation check:", flush=True)
    print(f"  Has <style> tag: {has_style}", flush=True)
    print(f"  Has @keyframes: {has_keyframes}", flush=True)
    print(f"  Has animation property: {has_animation}", flush=True)

print("\nDone!", flush=True)
