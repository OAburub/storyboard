# Engine Internals — Module Architecture Reference

Technical reference for debugging, extending, and understanding the PPTX engine. This is the map of the codebase.

## File Map

```
.claude/skills/storyboard-generator/scripts/
├── _paths.py                  (76 lines)   — Path auto-detection (git + file walk + cwd)
├── rtl_helpers.py             (290 lines)  — RTL workarounds for python-pptx and python-docx
├── _pptx_core.py              (1273 lines) — SlideEngine base class, constants, all helpers
├── _pptx_depth.py             (366 lines)  — Visual depth (washes, accents, corners, dots)
├── _pptx_structural.py        (763 lines)  — Structural slides (title, objectives, divider, summary, closing)
├── _pptx_visual_grammar.py    (1409 lines) — 8 visual patterns (process_flow, stat_cards, etc.)
├── _pptx_svg_generator.py     (~300 lines) — SVG generation via Gemini AI
├── pptx_engine.py             (1418 lines) — LectureBuilder composer (public API)
├── docx_engine.py             (~2500 lines)— 8 DOCX builders
└── image_gen.py               (~300 lines) — AI image generation via Gemini 3 Pro Image
```

## Mixin Inheritance Diagram

The LectureBuilder class composes all PPTX modules via Python's MRO (Method Resolution Order):

```
LectureBuilder
    ├── StructuralMixin      (title, objectives, section_divider, summary, closing)
    ├── VisualGrammarMixin   (process_flow, stat_cards, quote, timeline, comparison,
    │                         icon_grid, cycle_diagram, concept_visual)
    ├── DepthMixin           (depth_wash, depth_accent, decorative_corner, progress_dots,
    │                         header_bar, section_banner)
    └── SlideEngine          (base class: __init__, save, finalize, all _private helpers)
```

MRO resolution order: `LectureBuilder → StructuralMixin → VisualGrammarMixin → DepthMixin → SlideEngine`

Mixins come BEFORE SlideEngine so they can override or extend base behavior. All mixins use `self` to access SlideEngine's private helpers without importing it (avoids circular imports).

## Key Methods in SlideEngine (_pptx_core.py)

### Initialization
- `__init__()` — Opens template PPTX, deletes example slides, stores project metadata
- `save(filepath)` — Calls `finalize()` then writes the .pptx file
- `finalize()` — Applies any post-processing (slide numbering, etc.)

### Slide Creation
- `_add_slide_with_layout(layout_index)` — Adds a blank slide with a specific layout
- `_add_content_slide_with_layout()` — Adds a slide using the content layout (with background)

### Shape Helpers
- `_add_shape(slide, shape_type, left, top, width, height, fill_color, border_color, corner_radius, name)` — Universal shape creation with optional shadow
- `_add_arabic_textbox(slide, left, top, width, height, text, font_name, font_size, bold, color, alignment, name)` — RTL textbox with full font setup
- `_add_image(slide, image_path, left, top, max_width, max_height, name)` — Image with aspect ratio preservation via PIL
- `_add_notes(slide, text)` — Sets speaker notes

### Font and RTL
- `_set_run_font(run, font_name, size, bold, color)` — Sets all font properties including CS font
- `_set_rtl(paragraph)` — Shortcut for `pptx_set_paragraph_rtl()`

### Layout Helpers
- `_add_header_bar(slide, title, subtitle, color)` — Top title bar (slides 2+)
- `_add_section_banner(slide, title, wide)` — Section banner PNG with text overlay
- `_add_decorative_corner(slide, position, color, size)` — Two lines + dot corner decoration
- `_set_slide_title_for_toc(slide, title)` — Hidden off-screen textbox for Storyline sidebar
- `_add_shadow(shape)` — OOXML shadow via `effectLst > outerShdw`

### Color System
- `_get_accent_color(index)` — Returns next color from ACCENT_CYCLE (5 colors, wraps around)

## How to Add a New Visual Pattern

Step-by-step guide for adding a new pattern to the engine:

### 1. Define the method in `_pptx_visual_grammar.py`

```python
class VisualGrammarMixin:

    def add_new_pattern(self, title, data, notes="", image_prompt=None):
        """Add a [pattern name] slide showing [description]."""

        # 1. Increment slide count
        self.slide_count += 1

        # 2. Create the slide
        slide = self._add_content_slide_with_layout()

        # 3. Set TOC title for Storyline
        self._set_slide_title_for_toc(slide, title)

        # 4. Add header bar and section banner
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title)

        # 5. Add depth wash (background layer)
        self.add_depth_wash(slide, style="corner_oval")

        # 6. Render pattern-specific shapes
        # ... your pattern layout code here ...

        # 7. Add speaker notes
        if notes:
            self._add_notes(slide, notes)

        # 8. Optional: generate and add image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(slide, img_path, ...)
```

### 2. Add to the concept_visual dispatcher

The `add_concept_visual()` method routes `visual_type` strings to specific pattern methods:

```python
def add_concept_visual(self, title, visual_type, notes="", image_prompt=None, **kwargs):
    dispatch = {
        "process_flow": self.add_process_flow,
        "stat_cards": self.add_stat_cards,
        "new_pattern": self.add_new_pattern,  # Add here
        # ...
    }
```

### 3. Document in visual-grammar.md

Add the pattern to the Relationship-to-Visual Mapping table and create a full specification section.

## How Depth Layers Work

Every content slide can have three visual depth layers:

```
Layer 1 (Background): add_depth_wash()
  ├── "corner_oval"     — Large oval in top-right, very light blue-gray (#F0F4F8)
  ├── "radial_glow"     — Centered oval, warm light tone (#F5F0EB)
  └── "gradient_strip"  — Thin horizontal bar at bottom (#E8EEF4)

Layer 2 (Content): Main shapes — cards, textboxes, diagrams
  └── Shadows applied via _add_shadow() → OOXML effectLst

Layer 3 (Emphasis): add_depth_accent(), add_decorative_corner()
  ├── Accent bars: Thin colored strips (0.3cm) along slide edges
  └── Decorative corners: Two lines + dot at top-right or bottom-left
```

Washes are added FIRST (sent to back via z-order). Content shapes are added on top. Emphasis elements are added last (front of z-order).

## Color Rotation Algorithm

The 5-color accent cycle prevents visual monotony across repeated elements:

```python
ACCENT_CYCLE = [PRIMARY_BLUE, ACCENT1_BLUE, TEAL, ACCENT_ORANGE, PRIMARY_BLUE_LIGHT]
#               #2D588C       #156082        #009688  #FF9800       #4A7AAE

# Usage: each call to _get_accent_color() returns the next color
color = self._get_accent_color()  # Returns ACCENT_CYCLE[self._accent_index % 5]
self._accent_index += 1           # Advances for next call

# Or get a specific index:
color = self._get_accent_color(index=2)  # Returns TEAL
```

Cards, process steps, stat bars, and icon grid cells each get the next color in the cycle.

## Content Layout Variants

Content slides cycle through 3 layout variants for visual variety:

```
Variant 0 (A): Card layout
  - Content in a rounded rectangle card with shadow
  - Default for slides with images

Variant 1 (B): Accent stripe
  - Thin colored stripe on the left side via _add_accent_stripe()
  - Content offset slightly from the stripe

Variant 2 (C): Numbered points
  - Each bullet becomes a numbered row with colored circle badge
  - Via _add_numbered_points()
```

The variant cycles: `self._content_layout_cycle % 3`, advancing by 1 each content slide.

## SVG Generator Pipeline

```
Agent calls add_process_flow() (or other pattern method)
  → Method checks if SVG is appropriate (auto for cycle_diagram, 6+ step process_flow)
  → _try_svg_visual() called
    → Imports _pptx_svg_generator.generate_slide_svg()
    → Sends prompt to Gemini AI (tries 3.1 Pro → 3.0 Pro → 2.5 Flash)
    → Gemini returns SVG string
    → SVG extracted from response and saved to output/[PROJECT]/U[XX]/slides/
    → cairosvg converts SVG to PNG (1280x720, matching slide dimensions)
    → PNG embedded on slide via _add_image() as full-slide background
    → SVG file path appended to speaker notes for Storyline developer
  → If SVG fails: falls back to native shape-based rendering
```

## Image Generation Pipeline

```
Agent provides image_prompt parameter
  → _generate_image_for_slide(prompt, context_type) called
  → image_gen.py:generate_storyboard_image() invoked
    → Loads visual direction from config.json (style, palette, negativeRules)
    → Builds enhanced prompt with cultural rules and visual direction
    → Calls Gemini 3 Pro Image API
    → Saves result to output/[PROJECT]/U[XX]/images/ (cached by topic_key)
    → Returns file path
  → If API fails: returns {"action": "ask_user"} for graceful fallback
  → Image embedded via _add_image() with aspect ratio preservation
```

## Template Loading

```python
# In SlideEngine.__init__():
# 1. Open template PPTX file (gets layouts, backgrounds, logos)
self.prs = Presentation(template_path)

# 2. Delete ALL example slides (keep only layouts)
while len(self.prs.slides) > 0:
    sld_id = self.prs.slides._sldIdLst[0]
    rId = sld_id.get('{...relationships}id')
    self.prs.part.drop_rel(rId)           # Remove relationship
    self.prs.slides._sldIdLst.remove(sld_id)  # Remove ID entry

# 3. If template not found: create blank presentation
self.prs = Presentation()
self.prs.slide_width = 12192000   # 16:9 widescreen
self.prs.slide_height = 6858000
```

## Constants Quick Reference

All design tokens are defined in `_pptx_core.py`:

| Constant | Value | Purpose |
|---|---|---|
| `SLIDE_WIDTH` | 12192000 EMU | 16:9 widescreen width |
| `SLIDE_HEIGHT` | 6858000 EMU | 16:9 widescreen height |
| `PRIMARY_BLUE` | #2D588C | Headings, primary elements |
| `ACCENT1_BLUE` | #156082 | Theme accent, button fills |
| `BODY_TEXT` | #333333 | Body text color |
| `TEAL` | #009688 | Accent bars, definitions |
| `ACCENT_ORANGE` | #FF9800 | Cards, examples |
| `WHITE` | #FFFFFF | Button text, light backgrounds |
| `CONTENT_CARD_BG` | #F5F7FA | Light gray card backgrounds |
| `FONT_EXTRABOLD` | "Tajawal ExtraBold" | Titles (weight 800) |
| `FONT_MEDIUM` | "Tajawal Medium" | Card titles (weight 500) |
| `FONT_REGULAR` | "Tajawal" | Body text (weight 400) |
| `FONT_FALLBACK` | "Sakkal Majalla" | Fallback for DOCX |
| `TEXT_MARGIN_LR` | 0.25cm | Left/right text padding |
| `TEXT_MARGIN_TB` | 0.13cm | Top/bottom text padding |

## Path Auto-Detection (_paths.py)

The engine works on any machine without hardcoded paths:

```
Strategy 1: git rev-parse --show-toplevel (works in any git subdirectory)
Strategy 2: Walk up from _paths.py → scripts/ → storyboard-generator/ → skills/ → .claude/ → PROJECT_ROOT
Strategy 3: Fall back to current working directory
```

Exported paths:
- `PROJECT_ROOT` — where CLAUDE.md, projects/, output/ live
- `SCRIPTS_DIR` — the scripts/ directory (where engine .py files live)
- `SKILL_DIR` — the storyboard-generator/ directory
- `ASSETS_DIR` — the assets/pptx_assets/ directory (17 PNG files)
- `REFERENCES_DIR` — the references/ directory
- `PROJECTS_DIR` — the projects/ directory (per-project configs)
- `OUTPUT_DIR` — the output/ directory
