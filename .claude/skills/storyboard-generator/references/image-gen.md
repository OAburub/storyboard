# Image Generation API Reference

## Method 3: HTML+CSS Screenshot (Any Custom Visual)

For any visual requiring precise design control — diagrams, infographics, process flows, activity illustrations, video scenes (شاشة توضيحية), question visuals, UI screens, and more — **lazy-load `references/screenshot-gen.md`** for the full workflow. In brief:

```bash
# 1. Write HTML to: output/{PROJECT}/U{XX}/screenshots/{name}.html
# 2. Run:
python3 .claude/skills/storyboard-generator/scripts/screenshot_gen.py \
  output/{PROJECT}/U{XX}/screenshots/{name}.html \
  output/{PROJECT}/U{XX}/screenshots/{name}.png
# 3. Pass PNG path as image_path= to any builder method
```

Caching built-in: if PNG exists, script prints `CACHED: path` and skips. Read `references/screenshot-gen.md` only when you need the HTML template or design rules.

---

## Methods 1–3: AI Image Generation via Nano Banana Pro (Gemini 3 Pro)

## Main Function: `generate_storyboard_image()`

```python
import sys
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from image_gen import generate_storyboard_image

result = generate_storyboard_image(
    prompt="flat vector illustration of digital innovation concept",
    project_code="NJR01",
    unit_number=2,
    image_type="content",    # content, card, section, two_column, closing, quiz, hero, scene, step, inline
    topic_key="digital_innovation",  # For caching -- reuses if exists
)

if result["success"]:
    image_path = result["path"]  # Absolute path to generated image
    was_cached = result["cached"]  # True if reused from cache
else:
    error = result["error"]
    # result["action"] == "ask_user" -- stop and ask user what to do
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | str | Yes | Description of the image to generate (in English) |
| `project_code` | str | Yes | Project identifier (e.g. "NJR01") |
| `unit_number` | int | Yes | Unit number (e.g. 2) |
| `image_type` | str | No | Type for aspect ratio lookup: `content`, `card`, `section`, `two_column`, `closing`, `quiz`, `hero`, `scene`, `step`, `inline`. Default: `"content"` |
| `topic_key` | str | No | Cache key (e.g. "design_thinking"). Reuses existing image if found |
| `output_name` | str | No | Custom filename without extension. Defaults to topic_key or timestamp |
| `aspect_ratio` | str | No | Override aspect ratio (e.g. "16:9"). If None, uses config defaults |
| `resolution` | str | No | Override resolution ("1K", "2K", "4K"). Default from config or "2K" |

## Visual Direction (from config.json)

Loaded automatically from `projects/{code}/config.json` -> `visualDirection`:
- `promptPrefix`: Prepended to every prompt
- `promptSuffix`: Style descriptors appended
- `negativeRules`: Cultural/style rules enforced as "IMPORTANT: ..." instructions
- `defaultAspectRatios`: Per image_type aspect ratios
- `defaultResolution`: Default resolution (default: "2K")

## PPTX Usage (via `image_prompt` parameter)

All 6 image-supporting slide methods accept `image_prompt`. The engine calls `generate_storyboard_image()` internally when `image_prompt` is provided and no `image_path` exists.

```python
# Content slide with generated image
builder.add_content_slide(title="...", bullets=[...], image_prompt="flat vector of cloud computing concept")

# Section divider with background illustration
builder.add_section_divider(title="...", image_prompt="abstract digital network pattern")

# Quiz slide with illustration
builder.add_quiz_slide(question="...", options=[...], correct_index=0, image_prompt="AI concept diagram")

# Cards with per-card images
builder.add_content_with_cards(title="...", cards=[
    {"title": "...", "body": "...", "image_prompt": "IoT devices icon"},
    {"title": "...", "body": "...", "image_prompt": "AI brain icon"},
])

# Two-column with images per column
builder.add_two_column_slide(title="...",
    right_title="...", right_points=[...], right_image_prompt="benefits illustration",
    left_title="...", left_points=[...], left_image_prompt="challenges illustration",
)

# Closing slide with decorative image
builder.add_closing_slide(next_steps=[...], image_prompt="graduation celebration")
```

**Priority**: `image_path` > `image_prompt` (existing file path always wins).

## DOCX Usage (via `set_image()` or per-scene `image_prompt`)

### Group A: ObjectivesBuilder, SummaryBuilder, InfographicBuilder

```python
builder.set_image(image_prompt="flat vector of learning objectives concept")
```

### Group B: DiscussionBuilder, AssignmentBuilder

```python
builder.set_image(image_prompt="collaborative discussion illustration")
```

### TestBuilder

```python
builder.set_image(image_prompt="assessment and evaluation concept")
```

### ActivityBuilder (per-scene)

```python
builder.add_scene(
    title="...", description="...", elements="...",
    image_prompt="interactive drag-and-drop activity illustration",
)
```

### VideoBuilder (per-scene)

```python
builder.add_scene(
    title="...", screen_description="...", sound_effects="...",
    narration_segments=[...],
    image_prompt="motion graphics scene of digital transformation",
)
```

## Image Density Guidelines

| Storyboard Type | Images | Strategy |
|-----------------|--------|----------|
| Interactive Lecture (PPTX) | 8-12 | Most slides get images |
| PDF Lecture (PPTX) | 8-12 | Most slides get images |
| Motion Video (DOCX) | 6-8 | One per scene |
| Interactive Activity (DOCX) | 3-5 | One per interaction step |
| Discussion (DOCX) | 1 | Hero image only |
| Assignment (DOCX) | 1 | Hero image only |
| Pre/Post Test (DOCX) | 1-2 | Hero + optional per question |
| Summary (DOCX) | 2-3 | Per topic section |
| Infographic (DOCX) | 2-3 | Per learning milestone |
| Objectives (DOCX) | 1 | Hero image only |

## Caching

- Images cached by `topic_key` in `output/{PROJECT}/U{XX}/images/`
- Same `topic_key` across different storyboards reuses the image
- Video scene images are unique (use different topic_keys per scene)

## Error Handling

When image generation fails, the agent should STOP and ask the user:
1. Retry with modified prompt?
2. Skip this image?
3. Provide your own image path?

## Cultural Rules (Auto-enforced)

Read from `config.json` -> `visualDirection.negativeRules`. Typical rules:
- No human faces or facial features
- No female characters
- No Arabic text inside images
- No photorealistic style
- No gradients or shadows
