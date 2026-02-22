# RTL Arabic Patterns — Deep Reference

Complete reference for handling Arabic right-to-left text in python-pptx and python-docx. Every code pattern the engine uses, with explanations.

## Why RTL is Hard

Neither python-pptx nor python-docx has complete built-in RTL support. Both require direct XML manipulation for:
- Paragraph direction (`rtl='1'`)
- Complex Script font assignment (`cs` font slot)
- Table direction (`bidiVisual`)
- Text alignment (right-aligned by default for Arabic)

The engine's `rtl_helpers.py` module provides all the workaround functions.

## python-pptx RTL Patterns

### Setting Paragraph Direction

Every paragraph containing Arabic text must have RTL direction set at the XML level:

```python
from rtl_helpers import pptx_set_paragraph_rtl

p = text_frame.paragraphs[0]
run = p.add_run()
run.text = "مرحبا بالعالم"
pptx_set_paragraph_rtl(p)  # Sets pPr rtl='1'
```

What this does internally:
```python
pPr = paragraph._p.get_or_add_pPr()
pPr.set('rtl', '1')
```

### Setting LTR for Numbers

Even in an Arabic presentation, slide numbers and some labels should be LTR:

```python
from rtl_helpers import pptx_set_paragraph_ltr

p_number = text_frame.paragraphs[0]
run = p_number.add_run()
run.text = "3 / 25"
pptx_set_paragraph_ltr(p_number)  # Sets pPr rtl='0'
```

### Font Assignment for Arabic

The critical workaround: `font.name` only sets the "latin" font. Arabic text requires the "cs" (Complex Script) font set via XML.

```python
from rtl_helpers import pptx_set_run_font_arabic

run = p.add_run()
run.text = "النص العربي"
run.font.size = Pt(18)
run.font.bold = True
pptx_set_run_font_arabic(run, "Tajawal ExtraBold")
```

This sets three font slots in the XML:
- `<a:cs typeface="Tajawal ExtraBold"/>` — what Arabic text actually uses
- `<a:latin typeface="Tajawal ExtraBold"/>` — for mixed English characters
- `<a:ea typeface="Tajawal ExtraBold"/>` — for completeness

It also sets `lang="ar-JO"` for proper Arabic text shaping.

### The Engine's Helper

The engine's `_set_run_font()` wraps all of this:

```python
# Inside SlideEngine methods:
self._set_run_font(run, FONT_EXTRABOLD, Pt(24), bold=False, color=PRIMARY_BLUE)
# Internally calls pptx_set_run_font_arabic + sets size, bold, color
```

### Text Alignment

```python
from pptx.enum.text import PP_ALIGN

# Body text — always right-aligned for RTL
p.alignment = PP_ALIGN.RIGHT

# Titles — centered (both Arabic and English)
p.alignment = PP_ALIGN.CENTER

# Numbers/LTR — left-aligned
p.alignment = PP_ALIGN.LEFT
```

## python-docx RTL Patterns

### Paragraph RTL

DOCX uses a different XML namespace (`w:`) and a different element (`w:bidi`):

```python
from rtl_helpers import docx_set_paragraph_rtl

paragraph = document.add_paragraph("النص العربي")
docx_set_paragraph_rtl(paragraph)
```

Internally creates `<w:bidi/>` in the paragraph properties, placed in the correct schema position using `insert_element_before()`.

### Run RTL

Individual runs need `<w:rtl/>` to trigger Complex Script font selection:

```python
from rtl_helpers import docx_set_run_rtl

run = paragraph.add_run("النص")
run.font.cs_name = "Sakkal Majalla"  # python-docx supports cs_name directly
docx_set_run_rtl(run)  # Appends <w:rtl/> to rPr
```

### Table Direction

Tables must be set to RTL so the first column appears on the right:

```python
from rtl_helpers import docx_set_table_rtl

table = document.add_table(rows=3, cols=4)
docx_set_table_rtl(table)
# Sets WD_TABLE_DIRECTION.RTL + autofit = False
```

This also disables autofit so explicit column widths are respected.

### Cell Shading

Background colors on table cells require creating a NEW XML element each time:

```python
from rtl_helpers import docx_set_cell_shading

# CRITICAL: Each call creates a new element — never reuse
docx_set_cell_shading(table.cell(0, 0), "31849B")  # Teal header
docx_set_cell_shading(table.cell(1, 0), "DBE5F1")  # Light blue
```

### Cell Borders

python-docx has no border API. Use XML manipulation:

```python
from rtl_helpers import docx_set_cell_borders

docx_set_cell_borders(cell,
    top={"sz": 4, "val": "single", "color": "000000"},
    bottom={"sz": 4, "val": "single", "color": "000000"},
    start={"sz": 4, "val": "single", "color": "000000"},
    end={"sz": 4, "val": "single", "color": "000000"},
)
```

## XML Element Reuse Prohibition

This is the most common bug source. In lxml, XML elements have a single parent. Appending an element to a new parent **removes it from the old parent**.

```python
# WRONG — element moves from cell_1 to cell_2
shading = parse_xml('<w:shd w:fill="31849B"/>')
cell_1_tcPr.append(shading)  # OK
cell_2_tcPr.append(shading)  # Moves from cell_1!

# CORRECT — new element each time
cell_1_tcPr.append(parse_xml('<w:shd w:fill="31849B"/>'))
cell_2_tcPr.append(parse_xml('<w:shd w:fill="31849B"/>'))
```

This applies to ALL XML elements: shading, borders, paragraph properties, run properties, shadows.

## Process Flows: Right-to-Left

In RTL layouts, sequential content flows from right to left:

```
Step 1 (rightmost) ←── Step 2 ←── Step 3 ←── Step 4 (leftmost)
```

The engine positions step 1 at the right edge and works leftward:

```python
# Rightmost step = step 1 (highest x position)
for i, step in enumerate(steps):
    step_left = total_width - (i + 1) * (step_width + gap)
    # Arrows point left: ←
```

Arrow markers point left to indicate the reading direction.

## Line Spacing for Arabic

Arabic text requires more generous line spacing than Latin text for readability:

```python
from pptx.util import Pt

# Body text (>= 18pt): 1.3x line spacing
p.line_spacing = Pt(18 * 1.3)  # Or use Emu-based calculation

# Bullet lists: 1.4x line spacing
p.line_spacing = Pt(16 * 1.4)

# Big numbers (stat cards): 1.1x
p.line_spacing = Pt(48 * 1.1)
```

## Content Rules for Arabic

1. **No tashkeel/diacritics** — storyboard content uses plain Arabic without vowel marks
2. **No ALL CAPS** — Arabic has no uppercase/lowercase distinction. Use font weight for emphasis instead (ExtraBold vs Regular)
3. **Right alignment** for all body text. Center only for titles and buttons
4. **Font family**: Tajawal for PPTX, Sakkal Majalla for DOCX
5. **Mixed text**: When Arabic and English appear together, the RTL base direction handles bidi algorithm automatically. Numbers within Arabic text flow correctly

## Quick Reference Table

| Operation | python-pptx | python-docx |
|---|---|---|
| Set paragraph RTL | `pPr.set('rtl', '1')` | `<w:bidi/>` via `insert_element_before` |
| Set run RTL | Not needed (paragraph-level) | `<w:rtl/>` via `rPr.append()` |
| Set CS font | `<a:cs typeface="..."/>` via XML | `run.font.cs_name = "..."` (native API) |
| Table RTL | N/A (use shapes instead) | `WD_TABLE_DIRECTION.RTL` + `autofit=False` |
| Cell shading | `_add_shape()` with fill_color | `<w:shd w:fill="..."/>` (new element each time) |
| Text alignment | `PP_ALIGN.RIGHT` | `WD_ALIGN_PARAGRAPH.RIGHT` |
| Slide/page direction | Set on each paragraph | Set on each paragraph |
