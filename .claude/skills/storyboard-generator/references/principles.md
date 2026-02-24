# Design Principles — Single Source of Truth

All other reference files REFERENCE this document for philosophy and principles. If you need to change a principle, change it HERE and the entire system updates.

## Core Philosophy: Learner-First Visual Design

The agent is an **art director**, not a template filler. Every visual choice serves the LEARNER. For each slide, ask: **"What visual would make this concept click fastest for the learner?"**

## The Visual Palette

**Native PPTX shapes** — when the layout pattern itself IS the visual (stat cards, timelines, comparisons). The slide structure carries the meaning.

**When you need a generated image, you have 3 options:**

| Option | When to Use | NOT For |
|--------|-------------|---------|
| **SVG concept visualization** (via Gemini, `use_svg=True`) | When a visual metaphor or architecture diagram makes an abstract concept tangible: pillars, shields, ecosystems, tech stacks, data flows | Text-heavy content (Arabic text in SVG has rendering limits) |
| **AI-generated images** (`image_prompt`) | When a photorealistic or stylized illustration adds real-world meaning — a scenario scene, a textural background, a styled illustration | Diagrams, labeled layouts, or anything needing precise structure |
| **HTML+CSS Screenshot** (`image_path`, via Playwright) | For ANY custom visual where you design the output: diagrams, infographics, process flows, activity illustrations, question visuals, video scenes (شاشة توضيحية), data visualizations, UI screens. Not restricted to software — use it whenever HTML gives you better control. Lazy-load `references/screenshot-gen.md` when needed. | Photorealistic images (use AI image instead) |

Any slide can **combine**: SVG concept + AI background image, HTML diagram + AI illustration, etc.

## SVG Philosophy

SVG is NOT a last resort for "complex diagrams." It is a **primary visualization tool** for making concepts tangible:
- "5 pillars of X" → Building with labeled pillars
- "Security layers" → Concentric shields
- "Innovation ecosystem" → Connected growing elements
- "Technology stack" → Stacked layers
- "Data pipeline" → Flow through transformation stages

**Ask**: "Would seeing this concept as a picture help the learner understand faster?" If yes → SVG (or HTML if you need richer layout/text).

**Limitation**: Keep Arabic labels short (1-3 words) inside SVG. Long Arabic text should be in native PPTX shapes alongside the SVG, or use HTML+CSS instead.

## HTML+CSS Philosophy

HTML+CSS is NOT limited to software UI mockups. Use it whenever you want a designed visual with full layout control:
- Precise multi-column layouts with Arabic text
- Styled diagrams with real font rendering
- Activity illustrations (what a drag-and-drop looks like)
- Video scenes / شاشة توضيحية
- Any visual where SVG's text limitations would be a problem

Inline SVG can still be embedded inside HTML when you need vector shapes within a richer layout.

## Visual Composition Plan

REQUIRED before building any PPTX lecture. The agent must:
1. Create a slide-by-slide visual plan (pattern + which image option? per slide)
2. Present the plan to the user for review
3. Wait for approval BEFORE building

See `references/pptx-composition-arc.md` → "Planning Phase" for the template.
See `references/composition-examples.md` for creative thinking examples.

## 8 Non-Negotiable Rules

1. **COORDINATOR + CONTENT PRODUCER** — Main agent orchestrates AND generates. No subagents.
2. **ONE AT A TIME** — Generate each storyboard type with user review between each.
3. **ENGINE BUILDS DOCUMENTS** — All documents built by scripts. Call via `python3 -c "..."`.
4. **ARABIC RTL** — All content in Arabic, right-to-left. No tashkeel/diacritics.
5. **USER DECIDES** — AI suggests, user approves before proceeding.
6. **VISUAL GRAMMAR** — Never default to bullets. Choose the best visual pattern per concept.
7. **STORYLINE-READY** — Every PPTX slide must have named shapes and blueprint in speaker notes.
8. **LEARNER-FIRST VISUALS** — Choose whatever visual tool best helps the learner understand. Plan visuals BEFORE building.

## OOXML Visual Effects (Engine Internals)

The engine applies these effects internally for professional polish. The agent does NOT call these directly — they are applied automatically by the builder methods or via `use_svg=True`:

- `_apply_gradient_fill(shape, color1, color2, angle)` — Linear gradients on accent bars, card backgrounds
- `_apply_glow(shape, color, radius_pt, alpha)` — Colored halo on interactive badges, buttons
- `_apply_soft_edge(shape, radius_pt)` — Soft blending on decorative elements, card edges
- `_add_shadow_to_shape(shape)` — Drop shadows on content cards, buttons

These are PRIVATE methods (prefix `_`). The agent controls visuals through the public API (`add_process_flow`, `add_stat_cards`, etc.) and the `use_svg=True` parameter.
