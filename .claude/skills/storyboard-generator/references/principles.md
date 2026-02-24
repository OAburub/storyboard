# Design Principles — Single Source of Truth

All other reference files REFERENCE this document for philosophy and principles. If you need to change a principle, change it HERE and the entire system updates.

## Core Philosophy: Learner-First Visual Design

The agent is an **art director**, not a template filler. Every visual choice serves the LEARNER. For each slide, ask: **"What visual would make this concept click fastest for the learner?"**

## The 3-Tool Visual Palette

Choose based on what helps the learner UNDERSTAND, not what's easiest to build:

| Tool | When to Use | NOT For |
|------|-------------|---------|
| **Native PPTX shapes** | When the layout pattern itself IS the visual (stat cards show numbers, timelines show progression, comparisons show differences) | Don't use just because it's the default |
| **AI-generated images** (via Nano Banana / Gemini, `image_prompt`) | When a photorealistic or styled illustration adds real-world meaning — a scenario photo, a textural background, a stylized scene. | Don't use when you need precise control over layout or labeled diagrams |
| **HTML+CSS Screenshot** (via Playwright, `image_path`) | For ANY custom visual where you control the output: concept diagrams, infographics, process flows, activity illustrations, question visuals, video scenes (شاشة توضيحية), data visualizations, UI screens, or anything that benefits from precise design. Write HTML → run screenshot script → embed PNG. Lazy-load `references/screenshot-gen.md` when needed. | Don't use for photorealistic images (use AI image) |

Any slide can **combine tools**: an HTML diagram + AI image when both add value.

## HTML+CSS Philosophy

HTML+CSS is the primary tool for custom visual design. It is NOT limited to software UI — use it whenever you want to create something precise and designed:
- "5 pillars of X" → Styled cards arranged as pillars
- "Security layers" → Nested styled divs with labels
- "Step-by-step process" → Numbered flow with arrows
- "Activity instructions" → Visual representation of how the activity works
- "Video scene" → What the learner sees on screen at that moment
- "Data comparison" → Side-by-side styled panels

**Ask**: "Do I need precise control over this visual?" If yes → HTML+CSS Screenshot.

**Key advantage over SVG**: Full CSS layout, real Arabic text rendering (with Tajawal font), reliable RTL, and no text-in-SVG limitations. Inline SVG can still be embedded inside HTML when vector shapes are needed.

## Visual Composition Plan

REQUIRED before building any PPTX lecture. The agent must:
1. Create a slide-by-slide visual plan (pattern + HTML visual? + AI image? per slide)
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
