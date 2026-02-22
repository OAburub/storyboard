# Common Issues — Troubleshooting Guide

Known problems, their root causes, and fixes. Check here first when something looks wrong.

## Issue: Overlapping Text

**Symptom**: Text from one shape bleeds into or overlaps another shape on the slide.

**Root cause**: Modifying placeholder shapes from the template layout instead of creating new textboxes.

**Fix**: Never modify placeholder shapes. Always create new shapes with `slide.shapes.add_textbox()` or `self._add_shape()`. Placeholders have hidden anchoring behavior that causes overlap when you change their content.

## Issue: Font Not Rendering Arabic Correctly

**Symptom**: Arabic text appears in a default system font (Arial, Calibri) instead of Tajawal.

**Root cause**: python-pptx's `font.name` only sets the "latin" font slot. Arabic text uses the "cs" (Complex Script) font slot, which must be set separately via XML.

**Fix**: Always use `pptx_set_run_font_arabic(run, font_name)` from `rtl_helpers.py`. This sets all three font slots (cs, latin, ea):

```python
# WRONG — font.name is ignored for Arabic
run.font.name = "Tajawal ExtraBold"

# CORRECT — sets cs_font via XML
from rtl_helpers import pptx_set_run_font_arabic
pptx_set_run_font_arabic(run, "Tajawal ExtraBold")
```

Or use the engine's `_set_run_font()` helper which calls this internally.

## Issue: Shapes Reused Across Slides Disappear

**Symptom**: A shape appears on the last slide where it was used but vanishes from earlier slides.

**Root cause**: XML elements in lxml get **MOVED**, not copied, when appended to a new parent. If you store an element reference and add it to another slide, it is removed from the first.

**Fix**: Create a new XML element for every shape on every slide. Never reuse element references across slides or cells.

```python
# WRONG — reusing the same element
shading = parse_xml('<w:shd .../>')
cell_1.append(shading)  # Works
cell_2.append(shading)  # Moves from cell_1 to cell_2!

# CORRECT — create a new element each time
cell_1.append(parse_xml('<w:shd .../>'))
cell_2.append(parse_xml('<w:shd .../>'))
```

## Issue: Table Layout Broken

**Symptom**: Table columns are wrong width, or Word/PowerPoint auto-resizes columns.

**Root cause**: By default, both python-docx and python-pptx use autofit, which recalculates column widths based on content.

**Fix**: Set `autofit = False` and provide explicit cell widths:

```python
table.autofit = False
for row in table.rows:
    for i, cell in enumerate(row.cells):
        cell.width = explicit_widths[i]
```

## Issue: Image Stretched or Distorted

**Symptom**: An image appears squashed or stretched on the slide.

**Root cause**: Setting both width and height explicitly without respecting the original aspect ratio.

**Fix**: Use the engine's `_add_image()` method which reads the image dimensions with PIL and calculates the correct aspect ratio:

```python
# CORRECT — _add_image preserves aspect ratio
self._add_image(slide, image_path,
    left=Cm(2), top=Cm(5),
    max_width=Cm(9), max_height=Cm(9),
    name="img_content")
```

The method scales the image to fit within the bounding box while preserving its original proportions.

## Issue: SVG Text Looks Wrong in PPTX

**Symptom**: Arabic text in SVG-generated visuals has wrong font, wrong character shaping, or missing ligatures.

**Root cause**: SVGs are rasterized to PNG via cairosvg before embedding in PPTX. Cairo's font engine may not have the Tajawal font installed or may substitute a different Arabic font with different metrics.

**Fix**:
1. Ensure Tajawal font is installed system-wide (not just in the user font directory)
2. For text-heavy content, use native PPTX shapes instead of SVG
3. Reserve SVG for diagrams where the visual layout matters more than text rendering

## Issue: Shadow Not Appearing

**Symptom**: Cards and shapes have no visible shadow despite shadow code being present.

**Root cause**: python-pptx's built-in shadow API is limited. The engine uses direct OOXML XML manipulation for shadows via `effectLst > outerShdw`.

**Fix**: Use the engine's `_add_shadow()` helper which writes the correct OOXML XML:

```python
# The engine writes this XML to the shape's spPr element:
# <a:effectLst>
#   <a:outerShdw blurRad="50800" dist="25400" dir="5400000" algn="tl" rotWithShape="0">
#     <a:srgbClr val="000000"><a:alpha val="15000"/></a:srgbClr>
#   </a:outerShdw>
# </a:effectLst>
```

Never use python-pptx's `.shadow` property — it does not produce visible results.

## Issue: Bullet Markers Missing

**Symptom**: Bullet points appear as plain text with no bullet marker.

**Root cause**: Arabic RTL paragraphs need explicit XML for bullet markers. The default bullet rendering in python-pptx does not work reliably with RTL text.

**Fix**: The engine creates bullet markers manually as small colored circles (`OVAL` shapes) positioned to the right of each bullet text (RTL layout). This gives consistent visual results across all PowerPoint versions.

## Issue: Slide Looks Empty in Storyline

**Symptom**: After importing PPTX into Storyline 360, the slide panel shows "Untitled Slide" or the slide appears to have no content in the sidebar.

**Root cause**: Missing hidden TOC title. Storyline reads a special off-screen textbox named `title` to populate its sidebar navigation.

**Fix**: Every slide must have a hidden off-screen textbox:

```python
self._set_slide_title_for_toc(slide, "Arabic slide title here")
```

This creates a textbox at x=-2" (off-screen) named `title` containing the Arabic title.

## Issue: File Opens with Repair Prompt

**Symptom**: PowerPoint shows "We found a problem with some content" and offers to repair the file.

**Root cause**: Usually caused by invalid XML — duplicate relationship IDs, malformed elements, or elements in wrong positions.

**Fix**:
1. Never reuse XML elements (they get moved, not copied)
2. Ensure all slide layouts reference valid relationship IDs
3. Delete template slides properly using `drop_rel()` (the engine handles this in `__init__`)

---

## Anti-Patterns

These are common mistakes to avoid:

### Using bullets as default for every slide
**Instead**: Use visual grammar patterns. Every concept has a relationship (sequential, comparative, hierarchical) that maps to a visual pattern. Bullets are the LAST resort, and even then, use card layout, not raw bullets.

### Centering Arabic text
**Instead**: Body text should be right-aligned (`PP_ALIGN.RIGHT`). Only titles and buttons use center alignment. Centered Arabic body text looks amateur.

### Same layout on consecutive slides
**Instead**: Alternate between text-heavy (content, comparison) and visual (process_flow, stat_cards) patterns. Consecutive identical layouts feel monotonous.

### Putting too much text on one slide
**Instead**: If a slide has more than 6 lines of body text, split into 2 slides. Dense text walls are unreadable in e-learning. Each slide should present ONE concept.

### Using emojis as icons
**Instead**: Use geometric shapes (ovals, rounded rectangles with numbers) or generated images. Emojis render inconsistently across platforms and look unprofessional in Storyline.

### All-SVG with long Arabic text
**Instead**: SVG is a PRIMARY visualization tool for concept diagrams and metaphors (see `references/principles.md`). BUT keep Arabic labels inside SVG short (1-3 words). Long explanatory text must use native PPTX shapes alongside the SVG visual, because SVG text is rasterized to PNG and Arabic font rendering may be inconsistent.

### Template-fill approach for DOCX/PPTX
**Instead**: Build documents from scratch using the engine builders. Template-fill causes overlapping text, broken RTL, and unresolvable formatting conflicts.

### Reusing `_add_shape()` return values across slides
**Instead**: Each call to `_add_shape()` creates a new shape on a specific slide. Shape objects belong to their slide and cannot be moved or reused.
