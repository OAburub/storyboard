# RTL Arabic Patterns — Deep Reference

Complete reference for handling Arabic right-to-left text in python-pptx and python-docx. All workarounds are in `rtl_helpers.py`.

## Why RTL is Hard

Neither python-pptx nor python-docx has complete built-in RTL support. Both require direct XML manipulation for paragraph direction, Complex Script font assignment, table direction, and text alignment.

## python-pptx RTL Patterns

### Paragraph Direction
Every paragraph with Arabic text needs RTL set at XML level:
```python
from rtl_helpers import pptx_set_paragraph_rtl, pptx_set_paragraph_ltr
pptx_set_paragraph_rtl(p)   # Sets pPr rtl='1' — for Arabic text
pptx_set_paragraph_ltr(p)   # Sets pPr rtl='0' — for slide numbers, LTR labels
```

### Font Assignment for Arabic
**Critical**: `font.name` only sets the "latin" font. Arabic uses the "cs" (Complex Script) slot:
```python
from rtl_helpers import pptx_set_run_font_arabic
pptx_set_run_font_arabic(run, "Tajawal ExtraBold")
# Sets cs, latin, ea font slots + lang="ar-JO"
```

Or use the engine's wrapper: `self._set_run_font(run, FONT_EXTRABOLD, Pt(24), bold=False, color=PRIMARY_BLUE)`

### Text Alignment
```python
from pptx.enum.text import PP_ALIGN
p.alignment = PP_ALIGN.RIGHT   # Body text — always right-aligned for RTL
p.alignment = PP_ALIGN.CENTER  # Titles only
p.alignment = PP_ALIGN.LEFT    # Numbers/LTR only
```

## python-docx RTL Patterns

### Paragraph & Run RTL
```python
from rtl_helpers import docx_set_paragraph_rtl, docx_set_run_rtl
docx_set_paragraph_rtl(paragraph)  # Creates <w:bidi/> in paragraph properties
docx_set_run_rtl(run)              # Appends <w:rtl/> to rPr
run.font.cs_name = "Sakkal Majalla"  # python-docx supports cs_name directly
```

### Table Direction
```python
from rtl_helpers import docx_set_table_rtl
docx_set_table_rtl(table)  # Sets WD_TABLE_DIRECTION.RTL + autofit = False
```

### Cell Shading & Borders
```python
from rtl_helpers import docx_set_cell_shading, docx_set_cell_borders
docx_set_cell_shading(table.cell(0, 0), "31849B")  # CRITICAL: creates new element each call
docx_set_cell_borders(cell, top={"sz": 4, "val": "single", "color": "000000"}, ...)
```

## XML Element Reuse Prohibition

In lxml, appending an element to a new parent **removes it from the old parent**. Create a new element every time. See `common-issues.md` "Shapes Reused Across Slides" for examples.

## Process Flows: Right-to-Left

Sequential content flows right-to-left: Step 1 (rightmost) ←── Step 2 ←── Step 3 (leftmost). Arrow markers point left.

## Line Spacing for Arabic

```python
# Body text (>= 18pt): 1.3x | Bullet lists: 1.4x | Big numbers: 1.1x
```

## Content Rules for Arabic

1. **No tashkeel/diacritics** — plain Arabic without vowel marks
2. **No ALL CAPS** — use font weight for emphasis (ExtraBold vs Regular)
3. **Right alignment** for body text. Center only for titles and buttons
4. **Fonts**: Tajawal for PPTX, Sakkal Majalla for DOCX
5. **Mixed text**: RTL base direction handles bidi algorithm automatically

## Quick Reference Table

| Operation | python-pptx | python-docx |
|---|---|---|
| Set paragraph RTL | `pPr.set('rtl', '1')` | `<w:bidi/>` via `insert_element_before` |
| Set run RTL | Not needed (paragraph-level) | `<w:rtl/>` via `rPr.append()` |
| Set CS font | `<a:cs typeface="..."/>` via XML | `run.font.cs_name = "..."` (native API) |
| Table RTL | N/A (use shapes instead) | `WD_TABLE_DIRECTION.RTL` + `autofit=False` |
| Cell shading | `_add_shape()` with fill_color | `<w:shd w:fill="..."/>` (new element each time) |
| Text alignment | `PP_ALIGN.RIGHT` | `WD_ALIGN_PARAGRAPH.RIGHT` |
