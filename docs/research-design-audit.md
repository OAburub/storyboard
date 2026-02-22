# PPTX Engine Design Audit

## Executive Summary

After a thorough code review of `engine/pptx_engine.py` (3,561 lines, 13 slide types), five critical findings emerge:

1. **Color Palette Overload**: 25+ named color constants create a fragmented visual identity. A McKinsey deck uses 3 colors maximum. The engine uses PRIMARY_BLUE, ACCENT1_BLUE, TEAL, ACCENT_GREEN, ACCENT_RED, ACCENT_ORANGE, LIGHT_BLUE_BG, DARK_BG, WARM_GRAY, PRIMARY_BLUE_LIGHT, PRIMARY_BLUE_DARK, TEAL_LIGHT — all competing for attention.

2. **Decorative Noise Over Substance**: Section dividers pile up 6+ shapes (background rectangle, depth strip, accent bar, two corner decorations with dots, decorative line, progress dots). Each element individually is fine, but stacked together they create visual clutter that screams "PowerPoint template" not "consulting firm."

3. **Inconsistent Typography Scale**: The type hierarchy is flat. Headers at Pt(24), body at Pt(18-20), labels at Pt(16-18) — the jumps are too small. There is no clear visual distinction between H1/H2/Body/Caption. Everything looks the same weight.

4. **Card-mania**: Almost every slide wraps content in a CONTENT_CARD_BG (#F5F7FA) rounded rectangle with shadows and borders. Content slides, summary slides, quiz options, drag-drop items, click-reveal rows, two-column layouts — all cards. This removes white space and makes everything feel enclosed and heavy.

5. **Hardcoded Spacing Chaos**: Margin and padding values are ad-hoc across every method. Content starts at Cm(5) on some slides, Cm(5.5) on others, Cm(4.5) on others. Banner positions drift. There is no grid system.

---

## 1. Art Director Audit

### 1.1 Typography Hierarchy — WEAK

**Problem**: The font size scale creates almost no visual hierarchy.

| Element | Current Size | Notes |
|---------|-------------|-------|
| Title slide institution | Pt(24) | Same as lecture title |
| Title slide title | Pt(24) | Same as institution — no hierarchy |
| Title slide subtitle | Pt(20) | Close to title — no clear step-down |
| Section divider title | Pt(40) | Only place with real drama |
| Header bar (lecture name) | Pt(18) | Fine for a persistent element |
| Section banner text | Pt(18-20) | Same as body text — invisible hierarchy |
| Content body/bullets | Pt(18-20) | Identical to section titles |
| Quiz question | Pt(24) | Fine |
| Card titles | Pt(20) | Same as body text |
| Card body | Pt(18) | Identical to card title perceived weight |
| Summary items | Pt(20) | Same as everything else |
| Button text | Pt(20-22) | Appropriate |
| Closing "thank you" | Pt(36) | Good scale jump |

**Code locations**:
- Line 364: Institution name — `Pt(24)`
- Line 387: Title — `Pt(24)` (same as institution = no hierarchy)
- Line 397: Subtitle — `Pt(20)` (barely different from Pt(18) body)
- Line 509: Objective intro — `Pt(18)` (same as bullets)
- Line 594: Objective text — `Pt(18)` (same as intro)
- Line 747: Bullet list — `Pt(20)`
- Line 929-930: Card title — `Pt(20)`, card body — `Pt(18)` (2pt difference is invisible)

**Recommendation**: Establish a proper type scale with meaningful jumps:
- H1 (slide title): Pt(32-36)
- H2 (section/card title): Pt(24)
- Body: Pt(18)
- Caption/label: Pt(14)
- The minimum 1.5x ratio between levels creates real hierarchy

### 1.2 Color Harmony — TOO MANY COLORS

**Problem**: 25+ named colors create visual noise.

**Colors defined (lines 82-117)**:
```
PRIMARY_BLUE (#2D588C)
ACCENT1_BLUE (#156082)
BODY_TEXT (#333333)
SUBTITLE_TEXT (#262626)
LINK_BLUE (#2E6CEC)
WHITE (#FFFFFF)
DARK_BG (#1A1A2E)
BUTTON_BORDER (#082836)
NOTES_YELLOW (#FFFF00)
TEAL (#009688)
ACCENT_GREEN (#4CAF50)
ACCENT_RED (#F44336)
ACCENT_ORANGE (#FF9800)
LIGHT_BLUE_BG (#E3F2FD)
CONTENT_CARD_BG (#F5F7FA)
CONTENT_CARD_BORDER (#E0E5EC)
CARD_LIGHT_BG (#FAFBFC)
OPTION_ALT_BG (#F0F4F8)
DIVIDER_BG (#2D588C)
BULLET_MARKER_COLOR (#2D588C)
SHADOW_COLOR (#E0E0E0)
PRIMARY_BLUE_LIGHT (#4A7AAE)
PRIMARY_BLUE_DARK (#1E3D63)
TEAL_LIGHT (#4DB5B3)
WARM_GRAY (#6B6B6B)
ACCENT_DEFINITION (#009688)
ACCENT_EXAMPLE (#FF9800)
HEADER_BAR_BLUE (#2D588C)
```

Many are duplicates or near-duplicates:
- `PRIMARY_BLUE`, `DIVIDER_BG`, `BULLET_MARKER_COLOR`, `HEADER_BAR_BLUE` are all #2D588C
- `TEAL` and `ACCENT_DEFINITION` are both #009688
- `ACCENT_ORANGE` and `ACCENT_EXAMPLE` are both #FF9800
- `CONTENT_CARD_BG` (#F5F7FA), `CARD_LIGHT_BG` (#FAFBFC), `OPTION_ALT_BG` (#F0F4F8) — three barely distinguishable grays

**Active palette in a typical content slide**: PRIMARY_BLUE (header, banner text, bullets), BODY_TEXT (body), CONTENT_CARD_BG (card fill), CONTENT_CARD_BORDER (card border), plus shadow. That is 5 visual elements minimum. A McKinsey slide uses 2: dark text + one accent.

**Recommendation**: Reduce to 5 total colors:
- Primary: #2D588C (headings, accents)
- Text: #333333 (body)
- Subtle: #F5F7FA (backgrounds when needed)
- White: #FFFFFF
- Feedback only: Green/Red (quiz slides only, never decorative)

### 1.3 Visual Rhythm — INCONSISTENT

**Problem**: Vertical spacing is ad-hoc across slide types.

Content top positions across different slides:
- Content slide body: `Cm(5)` (line 702)
- Card content area: `Cm(5.5)` (line 855)
- Quiz question: `Cm(5)` (line 1228)
- Quiz options: `Cm(7.5)` (line 1245)
- Drag-drop question: `Cm(5)` (line 1414)
- Drag-drop items: `Cm(8.5)` (line 1449)
- Click-reveal instruction: `Cm(4.5)` (line 2258)
- Click-reveal tabs: `Cm(7)` (line 2354)
- Dropdown instruction: `Cm(4.5)` (line 2515)
- Dropdown rows: `Cm(7)` (line 2530)
- Summary body: `Cm(4.5)` (line 1871)
- Slider items: `Cm(5)` (line 2149)

These should align to a consistent vertical grid so the eye knows where to find content on every slide.

**Recommendation**: Establish a vertical grid:
- Header zone: 0 - Cm(2)
- Banner zone: Cm(2) - Cm(4)
- Content zone starts: Cm(5) always
- Footer zone: Cm(17) - Cm(19.05)

### 1.4 White Space — INSUFFICIENT

**Problem**: Content cards eat into margins and leave no breathing room.

The content card (lines 725-737) extends:
- Left: `content_left - Cm(0.5)` = Cm(2.5)
- Right: content_left + content_width + Cm(1) = Cm(32) (nearly edge-to-edge on a 33.87cm slide)
- Top: `content_top - Cm(0.3)` = Cm(4.7)
- Bottom: content_top + content_height + Cm(0.6) = Cm(17.1) (almost touching bottom)

The card fills approximately 85% of the slide area. McKinsey slides typically keep 30-40% white space.

**Recommendation**:
- Remove cards entirely from content slides — let text breathe on the white background
- If cards must exist, add minimum 3cm margins on all sides
- Reserve cards only for truly distinct grouped content (comparison columns, option cards)

### 1.5 Grid Consistency — NO GRID SYSTEM

**Problem**: Every slide positions elements independently using hardcoded values.

Left margin values used across the codebase:
- `Cm(2)`, `Cm(2.5)`, `Cm(3)`, `Cm(4)`, `Cm(5)`, `Cm(6)`, `Cm(7)`, `Cm(9)`, `Cm(10)`, `Cm(13)`

There is no consistent column grid. Every method defines its own "content area" dimensions.

**Recommendation**: Define a grid system as constants:
```python
GRID_LEFT_MARGIN = Cm(3)       # Consistent left margin
GRID_RIGHT_MARGIN = Cm(3)      # Consistent right margin
GRID_CONTENT_LEFT = Cm(3)      # Content always starts here
GRID_CONTENT_WIDTH = Cm(27.87) # 33.87 - 3 - 3
GRID_CONTENT_TOP = Cm(5)       # Below banner, always same
GRID_CONTENT_BOTTOM = Cm(17)   # Above footer zone
```

### 1.6 Visual Weight — TOO HEAVY

**Problem**: Multiple elements compete for attention on every slide.

On a typical content slide, the visual weight distribution includes:
1. Template layout background image (from the PPTX template)
2. Header bar text ("Lecture Title") — Pt(18) ExtraBold
3. Section banner PNG image — full-width decorative element
4. Banner text — Pt(18-20) ExtraBold on top of the banner image
5. Content card — rounded rectangle with fill, border, AND shadow
6. Bullet markers — filled circles in PRIMARY_BLUE
7. Body text — Pt(20)

That is 7 competing visual layers. The eye has nowhere to rest.

Elements with excessive visual weight:
- Cards: fill + border + shadow = 3 simultaneous treatments (lines 725-738)
- Section dividers: bg rect + depth strip + accent bar + 2 corners with dots + line + progress dots = 7+ elements (lines 1020-1141)
- Quiz options: card bg + border + shadow + badge circle = 4 treatments per option (lines 1256-1291)
- Two-column: each column has card bg + border + shadow + accent bar = 4 treatments x 2 = 8 elements (lines 1677-1795)

**Recommendation**: Pick ONE treatment per element:
- Cards: background fill ONLY, no border, no shadow
- Or: subtle shadow ONLY, no border, no fill
- Never: fill + border + shadow together

---

## 2. Client Audit (University Dean Perspective)

### 2.1 Professionalism — MIXED

**Positive**:
- Font choice (Tajawal) is modern and clean
- RTL handling is technically correct
- Shape naming for Storyline is professional
- Speaker notes structure is thorough

**Negative**:
- Decorative corners on section dividers feel like clip-art, not institutional
- Progress dots feel like a website pagination, not a presentation
- Multiple shades of blue (PRIMARY_BLUE, ACCENT1_BLUE, PRIMARY_BLUE_LIGHT) create confusion about what is the "brand blue"
- TEAL and ORANGE accent colors on cards (line 850: `default_colors = [PRIMARY_BLUE, ACCENT1_BLUE, TEAL, CARD_DARK2, AMBER, PRIMARY_BLUE]`) feel like a children's educational app, not university-level content

### 2.2 First Impression — "TEMPLATE"

When a dean opens this file, the first slide they see is the title slide. It has:
- Institution name in PRIMARY_BLUE centered text (fine)
- Lecture title in PRIMARY_BLUE below (fine)
- A button labeled "Start the lecture" with ACCENT1_BLUE fill and BUTTON_BORDER border
- A play icon PNG next to the button
- A hand cursor icon below the button

The play icon and hand cursor are the problem. They make this look like a YouTube tutorial, not a university presentation. The button itself with its border treatment looks like a web button circa 2015.

**Code locations**:
- Lines 430-451: Play icon and hand cursor placement
- Lines 402-427: Button with ACCENT1_BLUE fill + BUTTON_BORDER

### 2.3 Content Readability — GOOD (with reservations)

Arabic text is technically readable at Pt(18-20). However:
- The 1.3x line spacing (line 2900) for body text is tight for Arabic. Arabic needs 1.5-1.6x minimum for comfortable reading, especially on screen.
- Bullet markers at Pt(16) (line 3548) are smaller than body text at Pt(20) — this creates inconsistent visual weight in the same line
- The blue bullet markers (BULLET_MARKER_COLOR) compete with the body text for attention instead of being subtle guides

### 2.4 Brand Alignment — MISALIGNED

The current design says "tech startup template" not "established university." Specific issues:
- Rounded corners everywhere (corner_radius 0.04-0.08) feel playful
- TEAL, ORANGE, AMBER accents feel consumer-tech
- Shadow effects on cards feel like Material Design web components
- Progress dots feel like a mobile app wizard

A university wants to project: authority, tradition, rigor, seriousness. The current design projects: modern, tech-forward, casual, friendly.

### 2.5 Comparison to Commercial E-learning — BELOW AVERAGE

Commercial Arabic e-learning from companies like Edraak, Rwaq, or Noon Academy uses:
- Flat design (no shadows)
- Maximum 2 colors per slide
- Full-bleed images
- Generous white space
- Clean sans-serif fonts at large sizes
- Minimal decorative elements

The current engine output tries to do too much on every slide.

---

## 3. Designer Audit

### 3.1 Interaction Affordances — ADEQUATE

**Quiz slide** (lines 1143-1355):
- Option cards with letter badges (A, B, C, D) are clear
- "Check answer" button is identifiable
- But: alternating card backgrounds (line 1255: `CONTENT_CARD_BG if i % 2 == 0 else WHITE`) add visual noise. All options should look identical until the learner interacts.

**Drag-drop** (lines 1357-1580):
- Grip indicator (line 1499: hamburger icon `\u2630`) is too subtle at Pt(14)
- Dashed borders on drop zones (line 1531) are good affordance
- "Drag here" hint text (line 1540) is clear
- But: drag items have shadows AND borders — overly heavy for draggable elements

**Click-reveal** (lines 2199-2453):
- Horizontal tabs for 4 or fewer items: first tab is active (PRIMARY_BLUE), rest are lighter (PRIMARY_BLUE_LIGHT) — good affordance but the color difference is subtle
- Vertical list for 5+ items: number badges work as click targets
- Description area with accent bar (line 2401-2411) is a nice touch

### 3.2 Visual Consistency — INCONSISTENT

Cross-slide inconsistencies:

| Property | Content Slide | Quiz Slide | Cards Slide | Two-Column | Summary |
|----------|---------------|------------|-------------|------------|---------|
| Card bg | #F5F7FA | #F5F7FA or #FFF (alternating) | #FAFBFC | #FFFFFF | #F5F7FA |
| Card border | #E0E5EC | #E0E5EC | per-card color | #E0E5EC | #E0E5EC |
| Card radius | 0.04 | 0.06 | implicit | 0.04 | implicit |
| Shadow blur | 4pt | 3pt | 6pt (default) | 4pt | none |
| Shadow opacity | 15% | 12% | 25% (default) | 12% | none |

Three different shadow configurations, three different corner radii, three different background colors. This breaks the "same family" feeling.

**Code locations for inconsistency**:
- Content card shadow: line 738 — `blur_pt=4, opacity_pct=15`
- Quiz option shadow: line 1269 — `blur_pt=3, opacity_pct=12`
- Card slide shadow: line 882 — default (blur_pt=6, opacity_pct=25)
- Two-column shadow: line 1690 — `blur_pt=4, opacity_pct=12`
- Summary: no shadow at all (line 1857-1868)

### 3.3 Alignment Precision — MOSTLY GOOD

The code uses precise EMU values extracted from the template, so alignment against the template background is accurate. However:

- Accent stripe (line 3322): `left=Cm(31)` with `width=Cm(1.2)` = extends to Cm(32.2), which is within the 33.87cm slide width but leaves an asymmetric gap compared to the left margin
- Closing slide content card (line 1964-1973): margin of Cm(3) on all sides, but the decorative corner starts at `SLIDE_WIDTH - Cm(3)` — so the card and corner share the exact same edge, which looks unintentional

### 3.4 Detail Polish — NEEDS WORK

**Corner radius inconsistency**:
- Content cards: 0.04 (line 736)
- Quiz options: 0.06 (line 1268)
- Click-reveal tabs: 0.08 (line 2375)
- Closing slide card: default (none specified, line 1967)
- Section divider bg: default (none specified, line 1023)
- Summary card: default (none specified, line 1859)

All should be the same radius for consistency. Three different radii across slide types breaks family resemblance.

**Border width inconsistency**:
- Content card border: Pt(1) (line 734)
- Quiz option border: Pt(0.5) (line 1265)
- Card slide card border: Pt(2) (line 878)
- Two-column card border: Pt(1) (line 1685)
- Drag item border: Pt(1.5) (line 1475)
- Drop zone border: Pt(1.5) (line 1528)
- Button border: Pt(1.5) (line 411)
- Dropdown border: no width specified (line 2573)

Five different border widths across the system.

**Shadow inconsistency** (already covered in 3.2):
- Default: blur=6, dist=3, dir=2700000, opacity=25% (line 3035)
- Content cards: blur=4, opacity=15% (line 738)
- Quiz: blur=3, opacity=12% (line 1269)
- Two-column: blur=4, opacity=12% (line 1690)

### 3.5 Color Coding System — UNCLEAR

There is no clear semantic color system:
- PRIMARY_BLUE is used for: headings, bullets, badges, accent bars, column titles, card accents, step numbers, buttons, tab fills — it means everything, therefore nothing
- TEAL appears as: accent bars, definitions — but also as a card color alongside AMBER and NAVY
- The card `default_colors` array (line 850) cycles through 6 colors including TEAL and AMBER, creating rainbow cards that break the blue-based palette

**Recommendation**: Establish semantic color roles:
- Brand/Primary: ONE blue, used for headings and primary interactive elements
- Interactive: A slightly different shade for buttons and click targets
- Neutral: Gray scale for backgrounds and borders
- Feedback: Green (correct) and Red (incorrect) — used ONLY for quiz feedback, never decorative

---

## 4. Code Traceability

### Issue 1: Excessive Color Constants
- **Location**: Lines 82-117 (color definitions)
- **Root cause**: Colors were added incrementally as features were built, without design system governance
- **Fix**: Reduce to 6 semantic constants, alias duplicates

### Issue 2: No Grid System
- **Location**: Every public method has independent left/top/width/height values
- **Root cause**: Each slide type was built independently, copying values from the template rather than abstracting a grid
- **Fix**: Add grid constants at the top of the file, reference them in all methods

### Issue 3: Card-on-Everything Pattern
- **Location**: Lines 725-737 (content), 1256-1268 (quiz), 1677-1756 (two-column), 1857-1868 (summary)
- **Root cause**: Cards were introduced to "look professional" but applied universally
- **Fix**: Remove cards from content slides and summary. Keep ONLY for grouped items (card layout, quiz options, column containers)

### Issue 4: Decorative Corner Overkill
- **Location**: Lines 3076-3157 (`_add_decorative_corner`)
- **Root cause**: Attempt to replicate a "design template" look with code-drawn shapes
- **Fix**: Remove decorative corners entirely. They add no information and look amateur. Replace with a single thin accent line if any decoration is needed.

### Issue 5: Section Divider Overloaded
- **Location**: Lines 1010-1141 (`add_section_divider`)
- **Root cause**: Multiple decorative elements stacked without restraint
- **Fix**: Simplify to: colored background + title + subtitle + optional progress indicator. Remove: depth strip, accent bar, decorative corners.

### Issue 6: Inconsistent Shadow Parameters
- **Location**: Lines 738, 882, 1269, 1479, 1690 (various shadow calls)
- **Root cause**: Shadow parameters were tuned per-slide without a design standard
- **Fix**: Define ONE shadow profile: `SHADOW_DEFAULT = {"blur_pt": 4, "opacity_pct": 15}`. Use everywhere.

### Issue 7: Inconsistent Corner Radius
- **Location**: Lines 736, 1268, 2375, and many shapes without explicit radius
- **Root cause**: Different corner radius values assigned per feature without standardization
- **Fix**: Define ONE radius: `CORNER_RADIUS = 0.04`. Use everywhere.

### Issue 8: Inconsistent Border Width
- **Location**: Lines 411, 734, 878, 1265, 1475, 1528, 2573
- **Root cause**: Border widths set ad-hoc per element
- **Fix**: Define TWO profiles: `BORDER_THIN = Pt(1)` (cards, containers) and `BORDER_MEDIUM = Pt(1.5)` (buttons, interactive elements)

### Issue 9: Flat Typography Hierarchy
- **Location**: Lines 364, 387, 397 (title slide), 509/594 (objectives), 747 (body), 929/939 (cards)
- **Root cause**: Font sizes cluster between Pt(18-24) with no clear hierarchy
- **Fix**: Establish scale: H1=Pt(32), H2=Pt(24), Body=Pt(18), Caption=Pt(14)

### Issue 10: Tight Line Spacing for Arabic
- **Location**: Line 2900 (`p.line_spacing = 1.3` default for >= Pt(18))
- **Root cause**: 1.3x was chosen for compact layouts, but Arabic script needs more vertical room
- **Fix**: Increase to 1.5x minimum for body text, 1.6x for bullets (line 3558 has 1.4x, which is closer but still tight)

---

## 5. Priority Matrix

### Quick Wins (1-2 lines each, immediate visual improvement)

| # | Change | Lines to Edit | Impact |
|---|--------|---------------|--------|
| 1 | Unify corner_radius to 0.04 everywhere | 1268, 2375, plus add to ~5 shapes missing it | Medium |
| 2 | Unify shadow params to blur=4, opacity=15 | 882, 1269, 1690 | Medium |
| 3 | Unify border width to Pt(1) for containers | 878, 1265, 1475, 1528 | Low |
| 4 | Increase line spacing to 1.5 for body | 2900, 3558 | Medium |
| 5 | Remove alternating quiz option backgrounds | 1255 | Low |
| 6 | Remove bullet marker color — use WARM_GRAY instead of PRIMARY_BLUE | 3548 | Medium |
| 7 | Remove duplicate color constants (alias them) | 104-117 | Low |

### Medium Changes (10-30 lines, significant improvement)

| # | Change | Methods Affected | Impact |
|---|--------|-----------------|--------|
| 8 | Remove content card from `add_content_slide` | Lines 725-764 | High |
| 9 | Remove content card from `add_summary_slide` | Lines 1857-1868 | Medium |
| 10 | Simplify section divider (remove depth strip, accent bar, corners) | Lines 1031-1069 | High |
| 11 | Remove decorative corners from closing slide | Line 1976 | Medium |
| 12 | Define grid constants and apply to all methods | New constants + all methods | High |
| 13 | Remove play icon and hand cursor from title slide | Lines 430-451 | Medium |
| 14 | Establish typography scale (H1=32, H2=24, Body=18) | All methods | High |

### Deep Changes (50+ lines, architectural improvement)

| # | Change | Effort | Impact |
|---|--------|--------|--------|
| 15 | Remove layout variant cycling (A/B/C) from content slides — use one clean layout | Lines 699-782 | High |
| 16 | Replace `_add_decorative_corner` with minimal accent lines or remove entirely | Lines 3076-3157 | Medium |
| 17 | Reduce card color palette to monochrome + one accent in `add_content_with_cards` | Lines 848-850 | High |
| 18 | Create a design token system (single source of truth for all visual properties) | New architecture | Very High |

### Recommended Implementation Order

**Phase 1 — Immediate cleanup** (Quick Wins 1-7): Standardize the inconsistencies. This alone will make the output feel more polished even if the design direction doesn't change.

**Phase 2 — Remove visual noise** (Medium 8-14): Strip away the cards, corners, and decorative elements that make slides feel heavy. This is where the biggest visual improvement happens.

**Phase 3 — Establish design system** (Deep 15-18): Unify the entire engine around a grid, type scale, and design token system. This prevents future drift.

---

## Appendix: Slide Type Inventory

| # | Method | Lines | Key Visual Issues |
|---|--------|-------|-------------------|
| 1 | `add_title_slide` | 306-454 | Play/hand icons feel cheap; button border treatment dated |
| 2 | `add_objectives_slide` | 456-599 | PNG row backgrounds + target icons = template clip-art feel |
| 3 | `add_content_slide` | 601-786 | Card wrapping + 3 variants (A/B/C cycling) = inconsistent |
| 4 | `add_content_with_cards` | 788-960 | Rainbow card colors (5 different colors cycling) |
| 5 | `add_section_divider` | 962-1141 | 7+ visual elements stacked = visual clutter |
| 6 | `add_quiz_slide` | 1143-1355 | Alternating option BGs, different shadow params |
| 7 | `add_drag_drop_slide` | 1357-1580 | Grip icon too subtle, heavy card treatment on drag items |
| 8 | `add_two_column_slide` | 1582-1810 | Dual card treatment with accent bars = 8 decorative elements |
| 9 | `add_summary_slide` | 1812-1912 | Unnecessary card wrapping |
| 10 | `add_closing_slide` | 1914-2079 | Blue full-bleed + white card + decorative corner = competing layers |
| 11 | `add_slider_slide` | 2081-2197 | Cleanest slide type — number badges + text, minimal decoration |
| 12 | `add_click_reveal_slide` | 2199-2453 | Two different layouts (horizontal/vertical) = inconsistent |
| 13 | `add_dropdown_slide` | 2455-2591 | Cleanest interaction — simple rows with dropdown indicator |
