# PPTX Design System — Art Direction

Design principles and visual standards for the PPTX engine. This document GUIDES the agent's design decisions — it sets the quality bar, not a rigid template.

## Design Philosophy

We are designing an **educational interactive experience**, not a corporate presentation.

- The PPTX is a **milestone for client review** and an **input for Storyline 360**
- Every slide should look like a senior educational designer + graphic designer created it
- The learner's attention and comprehension come first
- Visual richness serves learning — decoration without purpose is clutter
- The agent should think: "How would a learner best UNDERSTAND this concept?"

## Slide Dimensions

- 16:9 widescreen: 13.333" x 7.5" (12192000 x 6858000 EMU)
- Target story size for Storyline: 1280 x 720 px
- Safe margins: 5% from each edge (no content in the outer frame)

## 3-Zone Layout

Every slide divides into three zones:

```
┌──────────────────────────────────────┐
│  HEADER ZONE (10%)                   │ ← Section tag, progress, branding
│──────────────────────────────────────│
│                                      │
│  CONTENT ZONE (78%)                  │ ← Main content, visuals, interactions
│                                      │
│                                      │
│──────────────────────────────────────│
│  FOOTER ZONE (12%)                   │ ← Takeaway, source, navigation hint
└──────────────────────────────────────┘
```

- **Header**: Section name badge + optional progress dots. Light background.
- **Content**: All main content. Use the full width creatively.
- **Footer**: Optional takeaway box, source attribution. Subtle.

## Typography

### Font Family: Tajawal (Arabic-optimized)

| Role | Weight | Size | Use |
|---|---|---|---|
| Slide title | ExtraBold (800) | 28-32pt | One per slide, always RTL |
| Section tag | Bold (700) | 12-14pt | Category label in header zone |
| Body text | Regular (400) | 16-18pt | Descriptions, explanations |
| Card title | Bold (700) | 18-20pt | Within cards, stat labels |
| Big number | ExtraBold (800) | 48-72pt | Hero stats, key figures |
| Caption | Regular (400) | 11-12pt | Source attribution, footnotes |
| Button text | Bold (700) | 14-16pt | Interactive elements |

### Typography Rules

1. **Aggressive weight contrast**: Title weight 800 vs body weight 400. Never use similar weights adjacent.
2. **Line spacing**: 1.3x for body text >= 18pt, 1.4x for bullets, 1.1x for big numbers
3. **Max line length**: ~60 characters per line for readability
4. **RTL always**: Every text element must have `rtl='1'` and right-alignment
5. **No ALL CAPS** for Arabic — it doesn't apply. Use weight for emphasis instead.
6. **Complex Script font**: Always set `font.cs_name` separately (RTL causes `font.name` to be ignored)

## Color System

### Brand Colors (from project config)

The engine reads colors from `projects/[code]/config.json → designSystem.colors`. Defaults:

| Token | Default | Usage |
|---|---|---|
| `primary` | #2D588C | Headers, primary buttons, section dividers |
| `secondary` | #4A90D9 | Active states, links, secondary elements |
| `accent` | #F5A623 | Highlights, attention points, key numbers |
| `success` | #27AE60 | Correct answers, positive trends, completion |
| `warning` | #F39C12 | Caution states, in-progress indicators |
| `error` | #E74C3C | Wrong answers, negative trends, alerts |
| `neutral` | #7F8C8D | Inactive states, secondary text, borders |
| `surface` | #F8F9FA | Card backgrounds, content areas |
| `background` | #FFFFFF | Slide background |
| `text_primary` | #2C3E50 | Main body text |
| `text_secondary` | #7F8C8D | Captions, secondary text |

### 5-Color Accent Rotation

To prevent visual monotony, cycle through 5 accent colors for repeated elements (process steps, cards, stat bars):

```
Cycle: primary → secondary → accent → success → warning
```

Each new card/step/element gets the next color in the cycle. This creates visual variety while maintaining harmony.

### Color Usage Rules

1. **Maximum 3 colors per slide** (excluding text and backgrounds)
2. **Primary color** for the most important element on each slide
3. **Accent color** for ONE highlight per slide (not everything)
4. **Neutral** for supporting elements that shouldn't compete for attention
5. **Semantic colors** are fixed: success=green, error=red, warning=amber — never override

## 3-Layer Depth System

Every slide has visual depth through three layers:

### Layer 1: Background (Subtle)
- Light wash or very faint geometric shape at 93-97% brightness
- Example: Pale oval in top-right corner at 5% opacity
- Purpose: Prevents "flat white page" feeling
- Implementation: `_add_depth_layer()` helper function

### Layer 2: Content (Primary)
- Cards, text boxes, diagrams — the main content
- Cards have subtle shadows: `outerShdw blurRad="50800" dist="25400"`
- Corner radius on cards: 8-12pt (0.04-0.06 ratio)
- Content sits clearly ABOVE the background

### Layer 3: Emphasis (Foreground)
- Accent bars, highlight borders, active indicators
- These elements draw the eye to the most important content
- Used sparingly — maximum 1-2 emphasis elements per slide

### Shadow Specifications

| Element | Shadow | Blur | Distance | Opacity |
|---|---|---|---|---|
| Content card | Yes | 50800 EMU | 25400 EMU | 15% |
| Stat card | Yes | 38100 EMU | 19050 EMU | 12% |
| Button/tab | Yes | 25400 EMU | 12700 EMU | 10% |
| Background shape | No shadow | — | — | — |

## Visual Tokens

Consistent spacing and sizing across all slides:

| Token | Value | Use |
|---|---|---|
| `spacing_tight` | 8pt (0.11") | Within card padding |
| `spacing_element` | 16pt (0.22") | Between elements in a group |
| `spacing_section` | 32pt (0.44") | Between sections on a slide |
| `spacing_zone` | 48pt (0.67") | Between header/content/footer zones |
| `radius_small` | 4pt | Badges, tags, small elements |
| `radius_medium` | 8pt | Cards, buttons |
| `radius_large` | 12pt | Feature cards, large containers |
| `border_thin` | 0.5pt | Subtle dividers |
| `border_accent` | 3pt | Accent bars on card tops |

## Slide Variety Rules

1. **Never repeat the same layout** on 2 consecutive slides
2. **Visual grammar first**: Choose the pattern that best represents the content (see visual-grammar.md)
3. **Breathing slides**: After 2-3 dense information slides, insert a lighter slide (quote, reflection, visual-only)
4. **Section dividers**: Every 4-6 slides, insert a section divider with progress indicator
5. **Narrative pacing**: Hook → Build → Insight → Practice → Summary (not linear content dump)

## Decorative Elements

### Section Dividers
- Full-bleed primary color background
- Section title in white ExtraBold
- Progress dots showing position in lecture (filled = completed)
- Optional decorative corner images from assets/

### Accent Bars
- 3pt colored bar on top of cards
- Color from the 5-color rotation cycle
- Signals "this is a distinct content block"

### Progress Indicators
- Small dots in header zone showing lecture progress
- Filled dot = current section, outline = upcoming
- Helps learner understand where they are in the journey

## What NOT to Do

1. **No bullet slides** as the default — use card layout minimum, visual patterns preferred
2. **No centered paragraph text** — always right-aligned for RTL
3. **No placeholder images** — use actual images sourced by output type priority (Photo/Illustration/Infographic/Screen)
4. **No dense text slides** — if more than 6 lines of body text, split into 2 slides or use cards
5. **No identical consecutive slides** — vary the visual pattern
6. **No floating text without containers** — put text in cards, badges, or defined zones
7. **No page numbers** — Storyline player handles navigation

## Brand Theming Integration

The engine reads brand parameters from `config.json` but the agent has FREEDOM to:
- Choose complementary shades of the brand colors
- Pick which visual pattern best represents each concept
- Design the narrative arc and pacing
- Create visual metaphors and diagrams
- Add breathing slides for pacing

The brand system CONSTRAINS:
- Which font family to use (but agent controls weights and sizes)
- The primary/secondary color palette (but agent controls usage and accents)
- Logo placement (header zone, title slide)
- General style direction (modern-minimal, bold-vibrant, etc.)
