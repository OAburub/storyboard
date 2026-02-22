# Research: Anthropic's Official PPTX Skill

Source: https://github.com/anthropics/skills/tree/main/skills/pptx

## Summary of Their Approach

Anthropic's PPTX skill takes a **dual-strategy** approach to presentation generation:

1. **Template-Based Editing** (editing.md) — When an existing PPTX template is available, they unpack it to raw XML, manipulate the XML directly, then repack. This preserves all original design (masters, layouts, themes, media) while replacing content.

2. **From-Scratch Creation** (pptxgenjs.md) — When building presentations without a template, they use **PptxGenJS** (a Node.js library), NOT python-pptx. Every element is positioned absolutely with explicit coordinates in inches.

They do NOT use python-pptx for creation. This is the most important finding.

---

## Key Architecture Decisions

### 1. Two Completely Separate Workflows

| Workflow | Tool | When to Use |
|----------|------|-------------|
| Edit existing | Raw XML (unpack/edit/pack) | Template provided by client |
| Create new | PptxGenJS (Node.js) | No template, build from scratch |

They explicitly avoid using python-pptx for creating new presentations.

### 2. XML-Level Manipulation for Templates

Their editing workflow:
1. `unpack.py` — Extract PPTX (it's a ZIP), pretty-print all XML
2. Visual analysis via `thumbnail.py` — Creates a JPEG grid of slide thumbnails
3. Structural changes (duplicate/delete/reorder slides) via `add_slide.py`
4. Content replacement via Claude's Edit tool (direct XML manipulation)
5. Cleanup via `clean.py` — Remove orphaned files
6. Repack via `pack.py` — Validate, condense XML, ZIP back up

Key insight: They use the **Edit tool** (not Python scripts) for content replacement. Each slide is a separate XML file, so subagents can edit slides in parallel.

### 3. PptxGenJS for From-Scratch (Not python-pptx)

Their creation guide uses PptxGenJS with:
- Absolute positioning in inches (x, y, w, h)
- Shape layering for visual depth (background shapes + text overlays)
- Built-in shadow support (type, blur, offset, angle, opacity)
- Icon rendering via react-icons -> SVG -> sharp -> PNG -> base64
- Chart styling with custom colors, muted grid lines, clean backgrounds

### 4. Quality Assurance Pipeline

- `thumbnail.py` for layout analysis
- `soffice.py` for PDF/image conversion (visual QA)
- Schema validators (`validators/`) for XML correctness
- `markitdown` for text extraction and grep-based checks
- Smart quote handling via entity escaping

---

## Design Standards (From SKILL.md)

### Typography
| Element | Size | Notes |
|---------|------|-------|
| Titles | 36-44pt | Bold, paired header font (Georgia, Arial Black, Impact) |
| Body text | 14-16pt | Clean body font (paired with header) |
| Character spacing | Explicit `charSpacing: 6` for emphasis | Not `letterSpacing` (silently ignored) |

### Color Strategy
- **60-70% dominant color** with supporting accent tones
- **10 named palettes** provided as examples (Midnight Executive, Cherry Bold, etc.)
- Topic-specific palette selection, not one-size-fits-all
- Muted axis labels (#64748B) for charts
- Subtle grid lines (#E2E8F0, 0.5pt) for charts

### Layout Standards
| Parameter | Value |
|-----------|-------|
| Slide size | 10" x 5.625" (LAYOUT_16x9) |
| Margins | 0.5" on all sides |
| Element spacing | 0.3-0.5" between blocks |
| Text box margin | Set to 0 when aligning with shapes |

### Layout Variety (Critical Emphasis)
Their editing.md explicitly warns against monotonous presentations. They mandate variety:
- Multi-column layouts (2-col, 3-col)
- Image + text combinations
- Full-bleed images with text overlay
- Quote/callout slides
- Section dividers
- Stat/number callouts
- Icon grids / icon + text rows

> "Monotonous presentations are a common failure mode. Don't default to basic title + bullet slides."

### Shadow Standards (PptxGenJS)
```javascript
shadow: {
  type: "outer",
  color: "000000",
  blur: 6,
  offset: 2,
  angle: 135,
  opacity: 0.15
}
```
- Never use negative offset values (corrupts file)
- Never encode opacity in hex color string (corrupts file)
- Use `angle: 270` for upward shadows (footer bars)
- Always create fresh shadow objects (PptxGenJS mutates objects in-place)

---

## Common Pitfalls They Document

### Critical Corruption Bugs
1. Never use "#" prefix with hex colors
2. Never use 8-char hex colors (opacity in color string)
3. Never reuse option objects across PptxGenJS calls (mutation)
4. Never use negative shadow offset values
5. Don't pair ROUNDED_RECTANGLE with rectangular accent overlays

### Content Formatting
1. Never use unicode bullets ("*") — use proper `bullet: true`
2. Multi-item content MUST use separate `<a:p>` elements, never concatenate
3. Bold all headers, subheadings, and inline labels
4. Use `xml:space="preserve"` for whitespace-sensitive text
5. Avoid `lineSpacing` with bullets — use `paraSpaceAfter` instead
6. Use `breakLine: true` between array text items

### Template Adaptation
1. When source has fewer items than template: remove excess elements entirely
2. When replacing with longer text: test for overflow
3. Template slots != source items (delete unused slots, don't just clear text)

---

## Tooling Scripts Analysis

### `thumbnail.py`
- Creates JPEG grid of slide thumbnails with XML filenames as labels
- Uses LibreOffice (soffice) for PDF conversion + pdftoppm for images
- 300px thumbnail width, 3 columns default, max 6
- Handles hidden slides with diagonal-line placeholders
- Key insight: visual analysis before editing prevents layout mistakes

### `add_slide.py`
- Duplicates slides or creates from layout templates
- Auto-handles Content_Types.xml, relationship IDs, notes references
- Removes notes slide references when duplicating (prevents orphans)
- Prints `<p:sldId>` element for manual placement in presentation.xml

### `clean.py`
- Iterative cleanup: loops until no more orphans found
- Removes: orphaned slides, trash directory, orphaned rels, unreferenced media/embeddings/charts/diagrams/themes/notes
- Updates Content_Types.xml after cleanup
- Uses defusedxml.minidom (not ElementTree — avoids namespace corruption)

### `pack.py`
- Condenses XML (removes whitespace nodes and comments)
- Preserves text nodes (skips tags ending with `:t`)
- Schema validation with auto-repair
- Separate validators for DOCX (schema + redlining) and PPTX (schema only)

### `soffice.py`
- LibreOffice wrapper with sandbox compatibility
- Compiles a C shim library to intercept AF_UNIX socket calls in sandboxed environments
- Enables document conversion (PPTX -> PDF -> images) in restricted environments

---

## Comparison with Our Current Engine

| Aspect | Anthropic Skill | Our Engine |
|--------|----------------|------------|
| **Library** | PptxGenJS (Node.js) for creation; raw XML for editing | python-pptx for everything |
| **Units** | Inches (human-readable) | EMU (machine-oriented, hard to read) |
| **Template approach** | Unpack -> XML edit -> repack | Open template, delete slides, add new |
| **RTL/Arabic** | Not addressed | Extensive RTL handling |
| **Shadow creation** | Native PptxGenJS API | Manual OOXML XML injection |
| **Design philosophy** | "Every slide needs visual elements" | Content-focused with decorative shapes |
| **Layout variety** | Explicitly mandated, warned against monotony | 3 auto-cycling variants (A/B/C) |
| **Color palettes** | 10 named palettes, 60-70% dominant | Single fixed palette per project |
| **Typography** | Font pairing (header + body), explicit sizes | Single font family (Tajawal), consistent sizes |
| **Quality assurance** | Visual thumbnails + PDF conversion + schema validation | No automated QA pipeline |
| **Font sizes** | 36-44pt titles, 14-16pt body | Various (28pt titles, 18-22pt body) |
| **Margins** | 0.5" consistent | Variable (0.24" to 0.69" depending on element) |
| **Icon system** | react-icons -> SVG -> PNG -> base64 | No icon system |
| **Chart styling** | Custom colors, muted grids, clean backgrounds | No chart support |

---

## Actionable Recommendations for Our Engine

### HIGH Priority

#### 1. Adopt Consistent Margins and Spacing
Our engine has inconsistent margins (CONTENT_LEFT varies, padding is ad-hoc). Anthropic standardizes on 0.5" margins and 0.3-0.5" spacing between blocks.

**Action**: Define a consistent spacing system:
- `MARGIN = 0.5"` (all sides)
- `BLOCK_GAP = 0.4"` between major elements
- `INNER_PAD = 0.3"` inside cards/containers

#### 2. Increase Font Size Range
Our title fonts (28pt) are smaller than Anthropic's recommendation (36-44pt). Our body text (18pt) is close to their 14-16pt but our content is in Arabic which typically needs slightly larger sizes.

**Action**: Consider bumping titles to 32-36pt range for more visual hierarchy.

#### 3. Mandate Layout Variety
Anthropic explicitly warns that monotonous slides are a "common failure mode." While we have 3 auto-cycling variants, we should:
- Increase to 5+ layout variants
- Add full-bleed image layouts
- Add stat/number callout layouts
- Add icon grid layouts
- Add quote/highlight layouts

#### 4. Add Visual QA Pipeline
Anthropic has thumbnail generation + PDF conversion + schema validation. We have none.

**Action**: Add a `qa.py` script that:
- Converts PPTX to PDF via LibreOffice
- Generates thumbnail grid for quick visual review
- Checks for text overflow / missing content

### MEDIUM Priority

#### 5. Adopt Named Color Palettes
Instead of a single fixed palette, define 3-5 named palettes per project. The 60-70% dominant color principle is important — one color should lead.

#### 6. Consider Font Pairing
Anthropic recommends pairing a distinctive header font with a clean body font. Our Tajawal family already has weight variants (ExtraBold, Medium, Regular) that serve this purpose, but we could explore pairing with a second Arabic font for headers.

#### 7. Improve Shadow Consistency
Our engine uses raw OOXML for shadows. The values could be standardized:
- Cards: blur=6pt, offset=2pt, opacity=15%, angle=135
- Hover/active: blur=10pt, offset=4pt, opacity=20%
- Footer bars: angle=270 (upward shadow)

#### 8. Add Icon System
Anthropic uses react-icons for clean, scalable icons. For Arabic educational content, we could:
- Use a curated set of educational icons (stored as PNG in assets)
- Auto-place icons on content cards, section dividers, objectives slides
- Define icon catalog in project config

### LOW Priority (Future)

#### 9. Consider PptxGenJS for Non-Template Slides
PptxGenJS has cleaner APIs for shadows, rounded rectangles, and image sizing. However, switching would require:
- Node.js runtime dependency
- Rewriting 3,163 lines of Python
- Losing our RTL helper infrastructure

**Verdict**: Not worth switching. python-pptx with our RTL helpers works. But we should adopt their design standards.

#### 10. Add Schema Validation
Their `pack.py` runs PPTX schema validation with auto-repair. We could add a lightweight validation step to catch XML errors before the user opens the file.

---

## Key Takeaways

1. **Design quality comes from standards, not tools.** PptxGenJS vs python-pptx matters less than consistent margins, proper font sizes, layout variety, and color discipline.

2. **Layout variety is critical.** Monotonous slides are their most-warned-against failure mode. Our 3-variant cycle is a good start but needs expansion.

3. **Visual QA is essential.** They never ship a presentation without visual inspection. We should add thumbnail generation.

4. **Spacing consistency matters.** Standardize margins and gaps across all slide types. Currently our spacing varies too much between slide types.

5. **Their XML-level editing approach is powerful** but only relevant when working with existing templates. For our "template-as-code" approach (building from scratch), the design principles matter more than the tooling.

6. **60-70% dominant color rule** is a simple but effective design principle we should adopt. One color leads, others support.
