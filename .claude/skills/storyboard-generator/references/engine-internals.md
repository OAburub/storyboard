# Engine Internals — Module Architecture Reference

Technical reference for debugging, extending, and understanding the PPTX engine.

## File Map

```
.claude/skills/storyboard-generator/scripts/
├── _paths.py                  — Path auto-detection (git + file walk + cwd)
├── rtl_helpers.py             — RTL workarounds for python-pptx and python-docx
├── _pptx_core.py              — SlideEngine base class, constants, all helpers
├── _pptx_depth.py             — Visual depth (washes, accents, corners, dots)
├── _pptx_structural.py        — Structural slides (title, objectives, divider, summary, closing)
├── _pptx_visual_grammar.py    — 8 visual patterns (process_flow, stat_cards, etc.)
├── _pptx_interactions.py      — 6 interaction types (quiz, drag-drop, scenario, etc.)
├── _pptx_svg_generator.py     — SVG generation via Gemini AI
├── pptx_engine.py             — LectureBuilder composer (public API)
├── docx_engine.py             — 8 DOCX builders
├── image_gen.py               — AI image generation via Gemini
└── screenshot_gen.py          — HTML→PNG via Playwright
```

## Mixin Inheritance

```
LectureBuilder
    ├── StructuralMixin      (title, objectives, section_divider, summary, closing)
    ├── InteractionsMixin    (quiz, drag_drop, click_reveal, slider, dropdown, scenario)
    ├── VisualGrammarMixin   (process_flow, stat_cards, quote, timeline, comparison,
    │                         icon_grid, cycle_diagram, concept_visual)
    ├── DepthMixin           (depth_wash, depth_accent, decorative_corner, progress_dots,
    │                         header_bar, section_banner)
    └── SlideEngine          (base class: __init__, save, finalize, all _private helpers)
```

MRO: `LectureBuilder → StructuralMixin → InteractionsMixin → VisualGrammarMixin → DepthMixin → SlideEngine`

All mixins use `self` to access SlideEngine helpers without importing it (avoids circular imports).

## Key SlideEngine Methods (_pptx_core.py)

### Initialization & Save
- `__init__()` — Opens template PPTX, deletes example slides, stores project metadata
- `save(filepath)` — Calls `finalize()` then writes the .pptx file
- `finalize()` — Post-processing (slide numbering, etc.)

### Shape Helpers
- `_add_shape(slide, shape_type, left, top, width, height, fill_color, border_color, corner_radius, name)` — Universal shape creation with optional shadow
- `_add_arabic_textbox(slide, left, top, width, height, text, font_name, font_size, bold, color, alignment, name)` — RTL textbox with full font setup
- `_add_image(slide, image_path, left, top, max_width, max_height, name)` — Image with aspect ratio preservation via PIL
- `_add_notes(slide, text)` — Sets speaker notes

### Font and RTL
- `_set_run_font(run, font_name, size, bold, color)` — Sets all font properties including CS font
- `_set_rtl(paragraph)` — Shortcut for `pptx_set_paragraph_rtl()`

### Layout Helpers
- `_add_header_bar(slide, title, subtitle, color)` — Top title bar
- `_add_section_banner(slide, title, wide)` — Section banner PNG with text overlay
- `_add_decorative_corner(slide, position, color, size)` — Two lines + dot corner decoration
- `_set_slide_title_for_toc(slide, title)` — Hidden off-screen textbox for Storyline sidebar
- `_add_shadow(shape)` — OOXML shadow via `effectLst > outerShdw`

### Color System
- `_get_accent_color(index)` — Returns next color from ACCENT_CYCLE (5 colors, wraps around)

## How to Add a New Visual Pattern

1. Define method in `_pptx_visual_grammar.py` class `VisualGrammarMixin`
2. Increment `self.slide_count`, create slide via `self._add_content_slide_with_layout()`
3. Set TOC title, header bar, section banner, depth wash
4. Render pattern-specific shapes
5. Add speaker notes, optional image
6. Add to `add_concept_visual()` dispatcher's `dispatch` dict
7. Document in `visual-grammar.md`

## Depth Layers

Every content slide has three visual depth layers:

| Layer | Method | Purpose |
|-------|--------|---------|
| 1. Background | `add_depth_wash()` | Large subtle shapes: `corner_oval`, `radial_glow`, `gradient_strip` |
| 2. Content | Main shapes | Cards, textboxes, diagrams — shadows via `_add_shadow()` |
| 3. Emphasis | `add_depth_accent()`, `add_decorative_corner()` | Thin colored accent bars, corner decorations |

Washes added FIRST (back z-order), content on top, emphasis last (front).

## Color Rotation

5-color accent cycle prevents visual monotony:

```python
ACCENT_CYCLE = [PRIMARY_BLUE, ACCENT1_BLUE, TEAL, ACCENT_ORANGE, PRIMARY_BLUE_LIGHT]
#               #2D588C       #156082        #009688  #FF9800       #4A7AAE
```

Each `_get_accent_color()` call returns the next color and advances the index.

## Content Layout Variants

Content slides cycle through 3 variants: **A** (card with shadow), **B** (accent stripe), **C** (numbered points). Cycles via `self._content_layout_cycle % 3`.

## SVG Generator Pipeline

```
Pattern method → _try_svg_visual() → Gemini AI generates SVG string
  → SVG saved to output/[PROJECT]/U[XX]/slides/
  → cairosvg converts SVG → PNG (1280x720)
  → PNG embedded on slide via _add_image()
  → SVG path appended to speaker notes
  → Falls back to native shapes on failure
```

## Image Generation Pipeline

```
image_prompt parameter → _generate_image_for_slide()
  → image_gen.py loads visual direction from config.json
  → Calls Gemini API with enhanced prompt + cultural rules
  → Cached by topic_key in output/[PROJECT]/U[XX]/images/
  → Returns file path or {"action": "ask_user"} on failure
```

## Constants (from _pptx_core.py)

| Constant | Value | Purpose |
|---|---|---|
| `SLIDE_WIDTH/HEIGHT` | 12192000 / 6858000 EMU | 16:9 widescreen |
| `PRIMARY_BLUE` | #2D588C | Headings, primary elements |
| `ACCENT1_BLUE` | #156082 | Theme accent, button fills |
| `BODY_TEXT` | #333333 | Body text color |
| `TEAL` | #009688 | Accent bars, definitions |
| `ACCENT_ORANGE` | #FF9800 | Cards, examples |
| `FONT_EXTRABOLD` | "Tajawal ExtraBold" | Titles (weight 800) |
| `FONT_MEDIUM` | "Tajawal Medium" | Card titles (weight 500) |
| `FONT_REGULAR` | "Tajawal" | Body text (weight 400) |
| `FONT_FALLBACK` | "Sakkal Majalla" | Fallback for DOCX |

## Path Auto-Detection (_paths.py)

Exports: `PROJECT_ROOT`, `SCRIPTS_DIR`, `SKILL_DIR`, `ASSETS_DIR`, `REFERENCES_DIR`, `PROJECTS_DIR`, `OUTPUT_DIR`. Detection: git rev-parse → file walk → cwd fallback.
