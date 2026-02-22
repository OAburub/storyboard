#!/usr/bin/env python3
"""
Test all SVG visual patterns using the _pptx_svg_generator module.
Generates SVG+PNG for each pattern and creates a combined PPTX.
"""

import sys
import os
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard/.claude/skills/storyboard-generator/scripts')

from _pptx_svg_generator import generate_slide_svg
from _pptx_core import SlideEngine, SLIDE_WIDTH, SLIDE_HEIGHT

# Colors matching the engine's design palette
COLORS = {
    "primary": "#2D588C",
    "secondary": "#4A90D9",
    "accent": "#F5A623",
}

OUTPUT_DIR = "/Users/qusaiabushanap/dev/storyboard/output/TEST/slides"

# Define test data for each pattern
PATTERNS = {
    "process_flow": {
        "title": "مراحل التصميم التعليمي",
        "data": [
            {"num": 1, "label": "التحليل", "desc": "تحديد الاحتياجات والأهداف"},
            {"num": 2, "label": "التصميم", "desc": "تصميم المحتوى والأنشطة"},
            {"num": 3, "label": "التطوير", "desc": "إنتاج المواد التعليمية"},
            {"num": 4, "label": "التقييم", "desc": "قياس فعالية التعلم"},
        ],
    },
    "stat_cards": {
        "title": "مؤشرات الأداء الرئيسية",
        "data": [
            {"number": "92%", "label": "نسبة الرضا", "trend": "up", "desc": "ارتفاع مقارنة بالعام السابق"},
            {"number": "4.7", "label": "متوسط التقييم", "trend": "up"},
            {"number": "15 دقيقة", "label": "وقت الإكمال", "trend": "down", "desc": "تحسن ملحوظ"},
        ],
    },
    "timeline": {
        "title": "مراحل تطور الذكاء الاصطناعي",
        "data": [
            {"year": "1956", "title": "مؤتمر دارتموث", "desc": "ولادة المصطلح", "status": "done"},
            {"year": "1997", "title": "ديب بلو", "desc": "هزيمة بطل الشطرنج", "status": "done"},
            {"year": "2012", "title": "التعلم العميق", "desc": "ثورة الشبكات العصبية", "status": "done"},
            {"year": "2024", "title": "النماذج الكبيرة", "desc": "عصر الذكاء التوليدي", "status": "active"},
        ],
    },
    "comparison": {
        "title": "مقارنة بين التعلم التقليدي والرقمي",
        "data": [
            {
                "title": "التعلم التقليدي",
                "items": ["حضور فيزيائي", "تفاعل مباشر", "جدول ثابت", "تكلفة أعلى"],
            },
            {
                "title": "التعلم الرقمي",
                "items": ["مرونة في الوقت", "محتوى تفاعلي", "تكلفة أقل", "وصول أوسع"],
                "highlight": True,
            },
        ],
    },
    "icon_grid": {
        "title": "مهارات القرن الحادي والعشرين",
        "data": [
            {"icon": "circle", "label": "التفكير النقدي", "desc": "تحليل وتقييم المعلومات"},
            {"icon": "hexagon", "label": "الإبداع", "desc": "إنتاج أفكار جديدة"},
            {"icon": "diamond", "label": "التعاون", "desc": "العمل ضمن فريق"},
            {"icon": "triangle", "label": "التواصل", "desc": "إيصال الأفكار بفعالية"},
            {"icon": "square", "label": "التكنولوجيا", "desc": "استخدام الأدوات الرقمية"},
            {"icon": "pentagon", "label": "القيادة", "desc": "توجيه وإلهام الآخرين"},
        ],
    },
    "cycle": {
        "title": "دورة التعلم المستمر",
        "data": {
            "center_label": "التعلم المستمر",
            "stages": [
                {"label": "التخطيط", "desc": "تحديد الأهداف"},
                {"label": "التنفيذ", "desc": "تطبيق المعرفة"},
                {"label": "المراجعة", "desc": "تقييم النتائج"},
                {"label": "التحسين", "desc": "تعديل الأساليب"},
            ],
        },
    },
    "quote": {
        "title": "حكمة تعليمية",
        "data": {
            "quote": "التعليم ليس ملء دلو، بل إشعال نار",
            "attribution": "ويليام بتلر ييتس",
        },
    },
}

# Generate SVGs for all patterns
print("=" * 60)
print("Testing all SVG visual patterns")
print("=" * 60)

results = {}
for pattern_name, pattern_data in PATTERNS.items():
    print(f"\n--- {pattern_name} ---", flush=True)
    svg_output = os.path.join(OUTPUT_DIR, f"pattern_{pattern_name}.svg")

    result = generate_slide_svg(
        pattern_type=pattern_name,
        data=pattern_data["data"],
        colors=COLORS,
        title=pattern_data["title"],
        output_path=svg_output,
    )

    if result:
        file_size = os.path.getsize(result)
        print(f"  SUCCESS: {result} ({file_size:,} bytes)", flush=True)
        results[pattern_name] = result
    else:
        print(f"  FAILED: No output generated", flush=True)
        results[pattern_name] = None

# Create combined PPTX with all successful patterns
print("\n" + "=" * 60)
print("Creating combined PPTX...")
print("=" * 60, flush=True)

engine = SlideEngine(
    project_code="TEST",
    unit_number=1,
    unit_name="SVG Test",
    institution="Test University",
)

for pattern_name, png_path in results.items():
    if png_path and os.path.exists(png_path):
        slide = engine._add_content_slide_with_layout()
        engine._set_slide_title_for_toc(slide, pattern_name)
        slide.shapes.add_picture(
            png_path, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT
        )
        engine._add_notes(slide, f"SVG Pattern: {pattern_name}\nFile: {png_path}")

out_pptx = "/Users/qusaiabushanap/dev/storyboard/output/TEST/test_svg_hybrid.pptx"
engine.save(out_pptx)
print(f"\nPPTX saved: {out_pptx}", flush=True)

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
successful = sum(1 for v in results.values() if v is not None)
total = len(results)
print(f"Patterns generated: {successful}/{total}")
for name, path in results.items():
    status = "OK" if path else "FAILED"
    print(f"  {name}: {status}")
print(flush=True)
