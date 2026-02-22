# PPTX LectureBuilder API Reference

Complete API for the modular PPTX engine. LectureBuilder composes 5 modules:
- `_pptx_core.py` — SlideEngine base class, constants, helpers
- `_pptx_depth.py` — Visual depth (washes, accents, corners)
- `_pptx_structural.py` — Structural slides (title, objectives, divider, summary, closing)
- `_pptx_visual_grammar.py` — 8 visual patterns (process flow, stats, timeline, etc.)
- `_pptx_interactions.py` — 6 interaction types (quiz, drag-drop, scenario, etc.)

## Constructor

```python
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DSAI",
    unit_number=1,
    unit_name="المهارات الرقمية",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
    designer="أحمد",  # optional
)
```

## Structural Slides (5 methods — from _pptx_structural.py)

### add_title_slide(title, subtitle, start_button_text)
Opening slide. Sets `builder.lecture_title` used on all subsequent slides.
- `title: str` — Main lecture title
- `subtitle: str` — Subtitle (default: "")
- `start_button_text: str` — Button text (default: "ابدأ المحاضرة")

### add_objectives_slide(objectives)
Numbered objectives with colored background rows.
- `objectives: list[str]` — Objective strings (3-5 recommended)

### add_section_divider(section_title, section_subtitle, section_number, total_sections, image_path, image_prompt)
Full-color section transition with decorative corners and optional progress dots.
- `section_title: str` — Main title
- `section_subtitle: str` — Optional subtitle
- `section_number: int` — Current section (enables progress dots)
- `total_sections: int` — Total sections
- `image_path/image_prompt: str` — Optional background illustration

### add_summary_slide(summary_items)
Recap slide with blue text.
- `summary_items: list` — Strings OR dicts: `{"title": "...", "text": "..."}`

### add_closing_slide(next_steps, image_prompt)
End slide with decorative corners and next steps.
- `next_steps: list[str]` — Action items for students
- `image_prompt: str` — Optional decorative image

## Content Slides (3 methods — from pptx_engine.py)

### add_content_slide(title, bullets, paragraphs, image_placeholder, image_path, image_prompt, notes)
Main workhorse slide. **Auto-cycles 3 layout variants** (A: card, B: accent stripe, C: numbered points).
- `title: str` — Section title
- `bullets: list[str]` — Bullet points (use this OR paragraphs)
- `paragraphs: list[str]` — Paragraph text (use this OR bullets)
- `image_path/image_prompt: str` — Optional illustration. Priority: image_path > image_prompt
- `notes: str` — Speaker notes / Storyline instructions

### add_content_with_cards(title, cards, notes)
2-4 concept cards with optional images.
- `cards: list[dict]` — `{"title": "...", "body": "...", "color": RGBColor, "image": "path", "image_prompt": "..."}`

### add_two_column_slide(title, right_title, right_points, left_title, left_points, notes, right_image, left_image, right_image_prompt, left_image_prompt)
Side-by-side comparison (RTL: right column first).

## Visual Grammar (8 methods — from _pptx_visual_grammar.py)

All visual grammar methods accept `use_svg=False`. When True, uses SVG generation instead of native shapes. Default: native PPTX shapes (better for text-heavy educational content).

### add_process_flow(title, steps, notes, image_prompt, use_svg)
Connected RTL boxes with arrows. Steps flow right-to-left.
- `steps: list[dict]` — `{"num": 1, "label": "...", "desc": "..."}` (3-7 steps)
- Auto-splits into 2 rows when > 4 steps
- SVG auto-selected when 6+ steps

### add_stat_cards(title, stats, notes, image_prompt, use_svg)
Big numbers in card frames — great for hooks and key insights.
- `stats: list[dict]` — `{"number": "85%", "label": "...", "desc": "...", "trend": "up/down"}` (2-4 cards)

### add_quote_highlight(title, quote, attribution, notes)
Breathing slide — large quote text with decorative marks. Generous whitespace.
- `quote: str` — Quote text (24-28pt)
- `attribution: str` — Source attribution

### add_timeline(title, milestones, notes, image_prompt, use_svg)
Horizontal timeline with alternating above/below markers.
- `milestones: list[dict]` — `{"year": "2020", "title": "...", "desc": "...", "status": "done/active/pending"}`

### add_comparison(title, columns, notes, image_prompt, use_svg)
2-3 side-by-side columns with colored headers.
- `columns: list[dict]` — `{"title": "...", "items": [...], "highlight": True/False}`

### add_icon_grid(title, items, notes, image_prompt, use_svg)
2x2, 3x2, or 3x3 grid of concept cards.
- `items: list[dict]` — `{"icon": "circle/hexagon/diamond", "label": "...", "desc": "..."}`

### add_cycle_diagram(title, stages, center_label, notes, image_prompt, use_svg)
Circular arrangement with connecting arrows.
- `stages: list[dict]` — `{"label": "...", "desc": "..."}` (3-6 stages)
- SVG auto-selected (circular layout benefits from SVG)

### add_concept_visual(title, visual_type, data, notes, image_prompt, use_svg)
Dispatcher — routes to the right pattern by `visual_type` string.
- `visual_type: str` — "process_flow", "stat_cards", "timeline", "comparison", "icon_grid", "cycle", "quote"

## Interaction Slides (6 methods — from _pptx_interactions.py)

### add_quiz_slide(question, options, correct_index, quiz_number, total_quizzes, image_path, image_prompt)
MCQ quiz with Arabic letter badges (أ ب ج د). Correct answer in notes.
- `options: list[str]` — 2-4 answer options
- `correct_index: int` — Zero-based correct answer index

### add_drag_drop_slide(question, items, correct_order, quiz_number)
Drag-and-drop classification with grip indicators and drop zones.
- `items: list[str]` — Draggable items
- `correct_order: list[str]` — Correct classification per item

### add_click_reveal_slide(title, instruction, reveal_items, notes)
Click-to-reveal with tabs (<=4 items) or vertical list (5+ items).
- `reveal_items: list[dict]` — `{"label": "...", "description": "..."}`

### add_scenario_slide(title, situation, choices, correct_index, notes)
**NEW** — Branching scenario with situation card and decision buttons.
- `situation: str` — Scenario description text
- `choices: list[str]` — 2-3 decision options
- `correct_index: int` — Zero-based correct choice
- Storyline blueprint in notes: layers per choice outcome, trigger setup

### add_slider_slide(title, items, notes)
Slider/scroll interaction with numbered step badges.
- `items: list` — Dicts `{"number": "1", "text": "..."}` or plain strings

### add_dropdown_slide(title, instruction, items, notes)
Dropdown matching activity.
- `items: list[dict]` — `{"text": "...", "correct": "..."}`

## Save

```python
builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```

`save()` auto-calls `finalize()` which adds click actions to buttons.

## SVG vs Native PPTX Decision

| Pattern | Default | Why |
|---------|---------|-----|
| process_flow (<=5) | Native PPTX | Text-heavy, editable Arabic |
| process_flow (6+) | SVG | Multi-row layout complex with shapes |
| stat_cards | Native PPTX | Numbers + text = native excels |
| quote_highlight | Native PPTX | Text IS the visual |
| timeline | Native PPTX | Milestones are text-heavy |
| comparison | Native PPTX | Column text needs proper RTL |
| icon_grid | Native PPTX | Labels need wrapping |
| cycle_diagram | SVG | Circular layout with curved arrows |

Override with `use_svg=True` on any method to force SVG generation.

## OOXML Visual Effects

Native PPTX slides are enhanced with OOXML XML effects:
- **Gradient fills** on cards and accent bars (not just solid colors)
- **Glow effects** on key elements (number badges, active milestones)
- **Soft edges** on decorative elements (quote marks, depth shapes)
- **Real shadows** via `effectLst > outerShdw` (not fake offset rectangles)

These use direct lxml XML manipulation — same technique as the shadow system.

## Storyline 360 Compatibility

- **TOC Titles**: Hidden off-screen title on every slide for Storyline sidebar
- **Shape Names**: Convention: `btn_*`, `opt_*`, `txt_*`, `bg_*`, `icon_*`, `num_*`
- **Import Instructions**: Title slide notes contain import steps, fonts, QA checklist
- **Story Size**: 1280x720 pixels
- **Speaker Notes**: Every interaction slide has full Storyline blueprint (layers, states, triggers, variables)

## Full Example

```python
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
)

# --- Structural ---
builder.add_title_slide(title="المحاضرة الأولى:", subtitle="المهارات الرقمية")
builder.add_objectives_slide(objectives=[
    "تعريف ماهي التقنية الناشئة.",
    "التعرف إلى فوائد التقنيات الرقميّة.",
])

# --- Content with visual variety ---
builder.add_content_slide(
    title="المقدمة",
    bullets=["أصبحت التقنية الرقمية جزءاً من حياتنا"],
    image_prompt="flat vector of digital technology in daily life",
)

builder.add_stat_cards(title="أرقام مهمة", stats=[
    {"number": "4.9B", "label": "مستخدم إنترنت", "trend": "up"},
    {"number": "85%", "label": "يستخدمون الهواتف", "trend": "up"},
])

builder.add_section_divider(
    section_title="المحور الثاني", section_subtitle="فوائد التقنية",
    section_number=2, total_sections=4,
)

builder.add_process_flow(title="مراحل التحول الرقمي", steps=[
    {"num": 1, "label": "التخطيط", "desc": "وضع الاستراتيجية"},
    {"num": 2, "label": "التنفيذ", "desc": "بناء الحلول"},
    {"num": 3, "label": "التقييم", "desc": "قياس الأثر"},
])

builder.add_quote_highlight(
    title="رؤية 2030",
    quote="التحول الرقمي ركيزة أساسية لمستقبل المملكة",
    attribution="رؤية المملكة العربية السعودية 2030",
)

builder.add_comparison(title="مقارنة", columns=[
    {"title": "الفوائد", "items": ["تسريع الوصول", "خفض التكاليف"]},
    {"title": "التحديات", "items": ["الأمن السيبراني", "الخصوصية"]},
])

# --- Interactions ---
builder.add_quiz_slide(
    question="أي العبارات تعبر عن التقنية الناشئة؟",
    options=["تقنية قديمة", "تقنية في مراحلها الأولى", "تقنية مكلفة"],
    correct_index=1,
)

builder.add_scenario_slide(
    title="سيناريو تطبيقي",
    situation="أنت مدير تقنية المعلومات في شركة ناشئة. طلب منك الرئيس التنفيذي تقليل التكاليف بنسبة 30%.",
    choices=["إلغاء جميع المشاريع التقنية", "التحول إلى الحوسبة السحابية", "تقليل عدد الموظفين"],
    correct_index=1,
)

builder.add_click_reveal_slide(
    title="تأثير التقنية على القطاعات",
    instruction="انقر لاكتشاف المزيد",
    reveal_items=[
        {"label": "التعليم", "description": "أثرت التقنية على أساليب التعلم"},
        {"label": "الصحة", "description": "الطب عن بعد والسجلات الإلكترونية"},
        {"label": "التجارة", "description": "التجارة الإلكترونية والدفع الرقمي"},
    ],
)

# --- Closing ---
builder.add_summary_slide(["التقنيات الناشئة في مراحلها الأولى", "التحول الرقمي يتطلب تخطيط"])
builder.add_closing_slide(next_steps=["مراجعة المحاضرة", "حل النشاط التفاعلي"])

builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```
