# DOCX Builders API Reference

Complete API documentation for all 8 DOCX builders in `engine/docx_engine.py`.

## Common Constructor (All Builders)

```python
import sys
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))

builder = AnyBuilder(
    project_code="DSAI",
    unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران",
    designer="أحمد",
)
```

## Common Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_element_name(name)` | `name: str` | Element name (e.g. "الاختبار القبلي") |
| `set_element_code(code)` | `code: str` | Element code (e.g. "DSAI_U01_Pre_Test"). Auto-generated if not called. |
| `set_date(date_str)` | `date_str: str` | Date string (default: today). Format: "YYYY-MM-DD" |
| `build()` | none | Build complete document. Call AFTER setting all content. |
| `save(output_path)` | `output_path: str` | Save to disk. Creates parent directories automatically. |

**Execution order**: Constructor -> set_element_name/code -> content methods -> build() -> save()

Run via Bash: `python3 -c "..."` with the full script.

---

## Group A: ObjectivesBuilder, SummaryBuilder, InfographicBuilder

These three share an identical infographic-style content table.

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_screen_description(value)` | `value: str` | Screen/infographic visual description (row 1) |
| `set_content_text(value)` | `value: str` | Main content text (row 2) |
| `set_image_sources(value)` | `value: str` | Image sources/credits (row 3) |
| `set_detailed_description(value)` | `value: str` | Detailed screen description (row 4) |
| `set_image(image_path, image_prompt)` | `image_path: str`, `image_prompt: str` | Set hero image. Use `image_prompt` for AI generation, or `image_path` for existing file. Priority: image_path > image_prompt |

### ObjectivesBuilder

Used for: Learning Objectives (الأهداف التعليمية)

```python
from docx_engine import ObjectivesBuilder

builder = ObjectivesBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("الأهداف التعليمية")
builder.set_element_code("DSAI_U01_MLO")
builder.set_screen_description("وصف شاشة الأهداف التعليمية")
builder.set_content_text(
    "1. أن يُعرّف المتعلم مفهوم التقنية الناشئة\n"
    "2. أن يُحدد المتعلم فوائد التقنية الرقمية\n"
)
builder.set_image_sources("أيقونات الأهداف التعليمية")
builder.set_detailed_description("")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Learning_Objectives.docx")
```

### SummaryBuilder

Used for: Unit Summary (الملخص)

```python
from docx_engine import SummaryBuilder

builder = SummaryBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("ملخص الوحدة")
builder.set_element_code("DSAI_U01_Summary")
builder.set_screen_description("شاشة توضيحية للملخص")
builder.set_content_text("ملخص المحتوى التعليمي...")
builder.set_image_sources("")
builder.set_detailed_description("")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Summary.docx")
```

### InfographicBuilder

Used for: Learning Map / Infographic (خارطة التعلم)

```python
from docx_engine import InfographicBuilder

builder = InfographicBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("خارطة التعلم")
builder.set_element_code("DSAI_U01_Learning_Map")
builder.set_screen_description("الإرشادات التعليمية...")
builder.set_content_text("خطوات التعلم في هذه الوحدة...")
builder.set_image_sources("أيقونة اختبار\nأيقونة محتوى")
builder.set_detailed_description("")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Learning_Map.docx")
```

---

## Group B: DiscussionBuilder, AssignmentBuilder

These two share a card-style content table.

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_screen_description(value)` | `value: str` | Screen description (row 1) |
| `set_content_text(value)` | `value: str` | Main content text (row 2) |
| `set_instructions(value)` | `value: str` | Instructions/guidelines (row 3) |
| `set_related_objectives(value)` | `value: str` | Related learning objectives (row 4) |
| `set_image(image_path, image_prompt)` | `image_path: str`, `image_prompt: str` | Set hero image. Use `image_prompt` for AI generation, or `image_path` for existing file. Priority: image_path > image_prompt |

### DiscussionBuilder

Used for: Discussion (النقاش)

```python
from docx_engine import DiscussionBuilder

builder = DiscussionBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("نقاش الوحدة الأولى")
builder.set_element_code("DSAI_U01_Discussion")
builder.set_screen_description("شاشة توضيحية تعرض سؤال النقاش")
builder.set_content_text("ناقش مع زملائك: كيف يمكن...")
builder.set_instructions("احترم آراء الجميع وشارك بآراء مدعمة...")
builder.set_related_objectives("1. أن يُحلل المتعلم تأثير التقنية...")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Discussion.docx")
```

### AssignmentBuilder

Used for: Assignment (الواجب)

```python
from docx_engine import AssignmentBuilder

builder = AssignmentBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("واجب الوحدة الأولى")
builder.set_element_code("DSAI_U01_Assignment")
builder.set_screen_description("شاشة توضيحية تعرض الواجب")
builder.set_content_text("اكتب مقالة من 500 كلمة...")
builder.set_instructions("صيغة التسليم: ملف Word\nالموعد النهائي: نهاية الأسبوع")
builder.set_related_objectives("1. أن يُطبق المتعلم مفاهيم التقنية...")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Assignment.docx")
```

---

## TestBuilder

Used for: Pre-Test, Post-Test, Course Exam

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_test_info(description, instructions)` | `description: str, instructions: str` | Test description and instructions |
| `set_image(image_path, image_prompt)` | `image_path: str`, `image_prompt: str` | Set hero image. Use `image_prompt` for AI generation, or `image_path` for existing file. Priority: image_path > image_prompt |
| `add_question(question_text, choices, correct_answer, image_description)` | See below | Add one question. Call multiple times. |

**add_question parameters:**
- `question_text: str` -- The question in Arabic
- `choices: str` -- Newline-separated: `"أ) ...\nب) ...\nج) ...\nد) ..."`
- `correct_answer: str` -- Correct answer letter (e.g. "ب")
- `image_description: str` -- Image description (use "" if none)

```python
from docx_engine import TestBuilder

builder = TestBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("الاختبار القبلي")
builder.set_element_code("DSAI_U01_Pre_Test")
builder.set_test_info(
    description="الاختبار القبلي للوحدة الأولى",
    instructions="المحاولات المتاحة: محاولة واحدة"
)
builder.add_question(
    question_text="ما هو الذكاء الاصطناعي؟",
    choices="أ) برنامج حاسوبي\nب) فرع من علوم الحاسب\nج) لغة برمجة\nد) نظام تشغيل",
    correct_answer="ب",
    image_description=""
)
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Pre_Test.docx")
```

---

## ActivityBuilder

Used for: Interactive Activity (نشاط تفاعلي). Each activity has one or more scenes.

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `add_scene(...)` | See below | Add a scene. Call multiple times for multi-scene activities. |

**add_scene parameters:**
- `title: str` -- Scene title (e.g. "المشهد الأول")
- `description: str` -- Scene description
- `elements: str` -- Scene elements content
- `image_desc: str` -- Image descriptions (default: "-")
- `motion_desc: str` -- Motion graphic description (default: "-")
- `sound_effects: str` -- Sound effects (default: "-")
- `on_screen_text: str` -- Text shown on screen (includes feedback)
- `steps: str` -- Activity steps
- `correct_answer: str` -- Correct answer text
- `buttons: str` -- Buttons after attempts (default: 'زر "مراجعة المحتوى"\nزر "أعد المحاولة"')
- `image_path: str` -- Path to existing image file (optional)
- `image_prompt: str` -- AI image generation prompt (English, optional). Used if no image_path

```python
from docx_engine import ActivityBuilder

builder = ActivityBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("النشاط التفاعلي 1.1")
builder.set_element_code("DSAI_U01_Activity1.1")
builder.add_scene(
    title="المشهد الأول",
    description="في هذا المشهد يظهر للطالب سؤال...",
    elements="يظهر السؤال مع أربعة خيارات...",
    image_desc="صورة توضيحية للمفهوم",
    motion_desc="-",
    sound_effects="-",
    on_screen_text="السؤال: ...\nالتغذية الراجعة: ...",
    steps="على الطالب اختيار الإجابة الصحيحة. عدد المحاولات: 2",
    correct_answer="ب) فرع من علوم الحاسب",
    buttons='زر "مراجعة المحتوى"\nزر "أعد المحاولة"',
)
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Activity1.1.docx")
```

---

## VideoBuilder

Used for: Motion Video (فيديو موشن). Has a 6-row metadata table. Each video has scenes with narration segments.

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `add_scene(...)` | See below | Add a scene with narration segments. Call multiple times. |

**add_scene parameters:**
- `title: str` -- Scene title (e.g. "مشهد العنوان")
- `screen_description: str` -- Visual description for the scene
- `sound_effects: str` -- Special sound effects
- `narration_segments: list[dict]` -- List of dicts, each with:
  - `"narration"` -- The narrated/read text
  - `"on_screen_text"` -- Text shown on screen
  - `"scene_description"` -- Detailed scene description with sync timing
  - `"image_links"` -- Image source links/descriptions
- `image_path: str` -- Path to existing image file (optional)
- `image_prompt: str` -- AI image generation prompt (English, optional). Used if no image_path

```python
from docx_engine import VideoBuilder

builder = VideoBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("فيديو موشن الوحدة 1")
builder.set_element_code("DSAI_U01_Video")
builder.add_scene(
    title="مشهد العنوان",
    screen_description="يظهر العنوان الرئيسي مع شعار الجامعة",
    sound_effects="موسيقى هادئة",
    narration_segments=[
        {
            "narration": "مرحبا بكم في الوحدة الأولى...",
            "on_screen_text": "المهارات الرقمية",
            "scene_description": "بالتزامن مع النص يظهر العنوان...",
            "image_links": "logo.png",
        },
    ]
)
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Video.docx")
```
