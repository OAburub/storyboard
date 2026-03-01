# Visual Grammar — Pattern Selection Guide

How to choose the right visual representation for each concept. The agent reads this before designing any content slide.

## Core Principle

**Never default to bullets.** For every concept, ask: "What RELATIONSHIP does this content express?" Then pick the visual pattern that matches that relationship.

## Relationship-to-Visual Mapping

Use this decision table. Find the content relationship in the left column, then use the corresponding visual pattern.

| Content Relationship | Visual Pattern | SVG Visualization? | When to Use |
|---|---|---|---|
| Steps in order | Process Flow | Consider (if metaphor helps) | Procedures, workflows, sequential instructions |
| Events over time | Timeline | Consider (if milestones need visual context) | Historical events, project phases, development stages |
| Two+ options compared | Comparison Layout | Consider (if comparing systems) | Pros/cons, before/after, feature comparison |
| Parts of a whole | Icon Grid or SVG Visual | Yes (layers, structures) | Organizational structures, classification systems — use icon_grid for flat groups, SVG for layered/nested structures |
| Repeating cycle | Cycle Diagram | Yes (always) | Plan-Do-Check-Act, seasons, feedback loops |
| Narrowing stages | Funnel | Yes (visual funnel) | Sales pipeline, filtering process, selection criteria |
| Key numbers | Stat Cards | No (numbers are the visual) | KPIs, survey results, performance metrics |
| Central idea + branches | Concept Map | Yes (connected nodes) | How ideas relate, cause-and-effect, mind maps |
| Abstract concept | Visual Metaphor (SVG) | Yes (always) | Any idea that benefits from creative illustration |
| Grouped items | Icon Grid | Consider (if items form a system) | Features, tools, team roles, categories |
| Notable quote/insight | Quote Highlight | No (text is the visual) | Expert quotes, key takeaways, surprising facts |
| Contrasting ideas | Two Column | Consider (if visual contrast helps) | Theory vs practice, old vs new, myth vs reality |
| Simple list (last resort) | Card Layout | No | When content truly is a list — use cards, NOT bullets |

## Pattern Specifications

### 1. Process Flow (تدفق العملية)

**Best for**: 3-7 sequential steps
**Structure**: Connected shapes flowing right-to-left (RTL)
**Elements per step**: Number + Label + Optional description
**Visual treatment**:
- Each step is a rounded card with accent-colored top bar
- Steps connected by arrows (← for RTL)
- Active/current step highlighted with primary color
- Shadow on cards for depth

**Data format for engine**:
```python
add_concept_visual(
    title="مراحل إدارة المشروع",
    visual_type="process_flow",
    steps=[
        {"num": 1, "label": "التخطيط", "desc": "تحديد الأهداف والموارد"},
        {"num": 2, "label": "التنفيذ", "desc": "تطبيق الخطة"},
        {"num": 3, "label": "المراقبة", "desc": "متابعة التقدم"},
        {"num": 4, "label": "الإغلاق", "desc": "تقييم النتائج"},
    ]
)
```

### 2. Timeline (الجدول الزمني)

**Best for**: 4-8 events/milestones
**Structure**: Horizontal line with points above/below (alternating)
**Elements per point**: Date/label + Title + Brief description
**Visual treatment**:
- Central horizontal line with circular milestone markers
- Alternating above/below placement for visual rhythm
- Done markers (filled) vs pending (outline)
- Color-coded by phase or status

**Data format**:
```python
add_concept_visual(
    title="تطور الذكاء الاصطناعي",
    visual_type="timeline",
    milestones=[
        {"year": "1956", "title": "مؤتمر دارتموث", "desc": "ولادة المصطلح", "status": "done"},
        {"year": "1997", "title": "ديب بلو", "desc": "هزيمة بطل الشطرنج", "status": "done"},
        {"year": "2024", "title": "النماذج اللغوية", "desc": "ثورة الذكاء التوليدي", "status": "active"},
    ]
)
```

### 3. Comparison Layout (مقارنة)

**Best for**: 2-3 options with 3-6 comparison criteria
**Structure**: Side-by-side columns (right column first for RTL)
**Visual treatment**:
- Each option in its own card with distinct header color
- Shared criteria rows for easy scanning
- Checkmarks/crosses or color coding for quick comparison
- Optional "winner" highlight

**Data format**:
```python
add_concept_visual(
    title="التعلم التقليدي مقابل التعلم الإلكتروني",
    visual_type="comparison",
    columns=[
        {"title": "التعلم التقليدي", "color": "neutral", "items": ["حضوري", "وقت محدد", "تفاعل مباشر"]},
        {"title": "التعلم الإلكتروني", "color": "primary", "items": ["عن بُعد", "مرن", "تفاعل رقمي"]},
    ]
)
```

### 4. Hierarchy / Layers (الهرمية)

**Best for**: 2-4 levels of depth, organizational structures, classification systems
**Implementation**: Use **SVG concept visualization** (`use_svg=True` on any pattern method) — no dedicated hierarchy method exists. Describe the hierarchy structure in the SVG concept description.
**Alternative**: For flat groupings (4-9 items), use `add_icon_grid()` instead.
**Visual treatment**:
- Nested cards with decreasing opacity (dark → medium → light)
- Connecting lines between levels
- Root node largest, children progressively smaller

### 5. Cycle Diagram (دورة)

**Best for**: 3-6 repeating stages
**Structure**: Circular arrangement with directional arrows
**Visual treatment**:
- Stages positioned in a circle
- Curved arrows connecting each stage to the next
- Each stage gets a distinct accent color
- Central label (optional) naming the cycle

### 6. Funnel (القمع)

**Best for**: 3-5 narrowing stages
**Structure**: Stacked bars of decreasing width
**Visual treatment**:
- Widest bar at top, narrowest at bottom
- Each level a different shade (light → dark)
- Numbers/percentages on each level
- Arrow indicators between levels

### 7. Stat Cards (بطاقات إحصائية)

**Best for**: 2-4 key numbers
**Structure**: Horizontal row of cards
**Elements per card**: Big number + Label + Optional trend indicator
**Visual treatment**:
- Each card has colored accent bar on top
- Numbers in ExtraBold, 48-72pt
- Trend arrows (up/down) with semantic colors (green=positive, red=negative)
- Subtle shadow on cards

**Data format**:
```python
add_concept_visual(
    title="نتائج الاستطلاع",
    visual_type="stat_cards",
    stats=[
        {"number": "92%", "label": "رضا المتعلمين", "trend": "up"},
        {"number": "4.7", "label": "متوسط التقييم", "trend": "up"},
        {"number": "15 دقيقة", "label": "متوسط وقت الإكمال", "trend": "down"},
    ]
)
```

### 8. Concept Map (خريطة مفاهيم)

**Best for**: 1 central idea with 3-6 connected sub-concepts
**Structure**: Central node with radiating branches
**Visual treatment**:
- Large central circle with primary concept
- Connecting lines to smaller satellite nodes
- Different colors per branch
- Optional secondary connections between satellites

### 9. Visual Metaphor — SVG (استعارة بصرية)

**Best for**: Infographics (1st priority) and Illustrations of abstract concepts (3rd priority after Freepik and Recraft)
**Structure**: Custom SVG generated by Gemini AI
**SVG is a primary tool for infographics and concept metaphors.** Ask: "Would seeing this as a picture help the learner understand faster?"

**When to use SVG** (broadly — not just as a last resort):
- The concept can be made tangible through a visual metaphor
- A diagram would show relationships that text alone can't convey
- The learner would benefit from "seeing" the concept, not just reading about it
- The slide would have more impact with a meaningful visualization

**Examples of SVG concept visualizations**:
- "5 pillars of digital literacy" → Building with 5 labeled pillars
- "Data flows through a pipeline" → Visual pipeline with transformation stages
- "Innovation ecosystem" → Connected growing elements in a garden
- "Security layers" → Concentric shields, each layer labeled
- "Technology stack" → Stacked layers (hardware → OS → middleware → app)
- "Learning journey" → Winding path with milestone markers
- "Digital transformation" → Before/after visual showing analog → digital shift
- "AI decision tree" → Branching paths with decision nodes
- "Cloud architecture" → Cloud shape with connected service boxes
- "Agile methodology" → Sprint cycle with connected phases

**Can combine with AI images**: An SVG diagram on one side + an AI-generated contextual image on the other.

**Keep labels short**: SVG text is rasterized to PNG. Use 1-3 word Arabic labels inside SVG. Long explanatory text should be in native PPTX shapes alongside the visual.

### 10. Icon Grid (شبكة أيقونات)

**Best for**: 4-9 related items (features, categories, tools)
**Structure**: 2x2, 2x3, or 3x3 grid of icon-label pairs
**Visual treatment**:
- Each cell: icon/emoji + label + 1-line description
- Consistent card styling across all cells
- Subtle grid lines or card borders
- Color accent rotation across cells

### 11. Quote Highlight (اقتباس بارز)

**Best for**: Expert quotes, key insights, surprising statistics
**Structure**: Large featured text with attribution
**Visual treatment**:
- Quote in large, distinctive typography
- Accent bar or decorative quotation marks
- Author/source in smaller text below
- Minimal supporting elements — let the quote breathe

### 12. Two Column (عمودان)

**Best for**: Contrasting two perspectives, before/after, theory/practice
**Structure**: Two equal columns side by side
**Visual treatment**:
- Right column (first in RTL) for primary/new concept
- Left column for secondary/old concept
- Distinct colors per column (primary vs neutral)
- Shared title spanning both columns

### 13. Card Layout (بطاقات)

**Best for**: When content truly IS a list — but present as cards, not bullets
**Structure**: 2-4 cards in a row or stacked
**Visual treatment**:
- Each card: colored accent bar + title + description
- Shadow for depth
- Consistent sizing
- Color rotation across cards

**Use this as the MINIMUM visual treatment. Never use raw bullets.**

## Selection Process

When designing a slide, follow this process:

1. **Read the concept** — what information is being presented?
2. **Identify the relationship** — is it sequential? Comparative? Hierarchical?
3. **Match to pattern** — use the relationship-to-visual table above
4. **Consider visualization** — would an SVG concept diagram make this idea tangible? If a visual metaphor, architecture diagram, or relationship map would help the learner "see" the concept, plan SVG (use_svg=True). Check the "SVG Visualization?" column in the table above.
5. **Consider illustration** — would a real-world AI image add context? If the concept benefits from a contextual scene or illustration, plan an image_prompt.
6. **Consider the narrative** — where are we in the 5-act arc? Does this slide need a "wow" moment?
7. **Check pacing** — avoid 3+ dense pattern slides in a row (insert a breathing slide)
8. **Apply brand** — use the project's design system colors/fonts

## Pacing Rules

For detailed pacing rules (3-4 slide rule, breathing rule, variety rule, section rule, cognitive load), see `pptx-composition-arc.md` Part 5.

---

## SVG Prompt Engineering Patterns

Source: Practical guide tested in early 2026.

### Key Keywords That Improve Output Quality
- "buttery smooth", "cinematic", "minimal", "isometric", "pastel"
- "ease-in-out timing", "infinite loop", "smooth easing"
- Always specify viewBox (e.g., "viewBox 0 0 500 300")
- Mention `<animate>`, `<animateTransform>`, or `CSS @keyframes inside <style>`
- "clean code, no groups/transform hell, logical layer order"
- "Output only the <svg>...</svg> code" (prevents markdown wrapping)

### Three Proven Prompt Patterns

**Pattern A — Simple & Reliable**
```
Generate a complete, standalone animated SVG (no HTML wrapper needed) that shows:
[DESCRIPTION].
Use <animate> and <animateTransform> elements.
viewBox="0 0 500 300", modern flat style, pastel colors, infinite loop, smooth easing.
Output only the <svg>…</svg> code.
```

**Pattern B — Cinematic / Detailed**
```
Create a beautiful looping SVG animation:
[MULTI-STEP DESCRIPTION with timing per step].
Use only paths, lines, ellipses and circles.
viewBox 0 0 400 500, [color scheme], very smooth animations with ease-in-out timing, repeat indefinite.
Include <style> with CSS animations if it gives better control.
Give clean, well-commented SVG code.
```

**Pattern C — Isometric / 3D-ish**
```
One-shot prompt: generate an isometric SVG animation
[SCENE DESCRIPTION with motion path].
[Color scheme], flat minimal style with soft shadows.
Smooth 5-7 second loop, use animateMotion along path + scale/rotate transforms.
viewBox 0 0 600 400, infinite repeat, buttery smooth easing.
```

### Iteration Pattern
After first SVG, paste code back and say:
"Make these changes: [specific changes]. Keep everything else almost identical. Output the full updated <svg> code."

### Application Examples

**Simple educational diagrams** (process flows, icon grids) → Pattern A:
```
SVG Concept: "5 connected pipeline chambers flowing right-to-left, each labeled with a stage name, modern flat style, pastel primary/secondary tints"
```

**Rich concept metaphors** (pillars, ecosystems, layered systems) → Pattern B:
```
SVG Concept: "A building with 5 labeled pillars supporting a roof. First the foundation draws in (2s), then pillars rise sequentially (1s each), then roof settles on top (2s). Minimal flat style, primary blue pillars, accent gold roof."
```

**Architectural/3D-feel visuals** (tech stacks, cloud architecture) → Pattern C:
```
SVG Concept: "Isometric layered stack — hardware at bottom, OS middle, application top. Each layer slides in from left with soft shadow. Pastel blue-green scheme, flat minimal with depth."
```

### Engine Integration
These quality keywords are built into `scripts/_pptx_svg_generator.py`. All 8 pattern-specific prompt builders benefit from the common_style keywords: "minimal flat style", "clean code logical layer order", "soft pastel tints", "generous white space", "buttery smooth easing".
