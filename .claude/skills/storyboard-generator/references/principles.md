# Design Principles — Single Source of Truth

All other reference files REFERENCE this document for philosophy and principles. If you need to change a principle, change it HERE and the entire system updates.

## Core Philosophy: Learner-First Visual Design

The agent is an **art director**, not a template filler. Every visual choice serves the LEARNER. For each slide, ask: **"What visual would make this concept click fastest for the learner?"**

## The 3-Tool Visual Palette

Choose based on what helps the learner UNDERSTAND, not what's easiest to build:

| Tool | When to Use | NOT For |
|------|-------------|---------|
| **Native PPTX shapes** | When the layout pattern itself IS the visual (stat cards show numbers, timelines show progression, comparisons show differences) | Don't use just because it's the default |
| **SVG concept visualization** (via Gemini, `use_svg=True`) | When a visual metaphor, diagram, or architecture makes an abstract concept tangible. SVG is a PRIMARY visualization tool. | Don't use for text-heavy content (Arabic text rendering issues) |
| **AI-generated images** (via Nano Banana / Gemini, `image_prompt`) | When a contextual illustration adds real-world meaning. Each image should help the learner visualize the concept. | Don't use as decoration. No generic stock-photo descriptions. |

Any slide can **combine tools**: SVG diagram + AI image when both add value.

## SVG Philosophy

SVG is NOT a last resort for "complex diagrams." It is a **primary visualization tool** for making concepts tangible:
- "5 pillars of X" → Building with labeled pillars
- "Security layers" → Concentric shields
- "Innovation ecosystem" → Connected growing elements
- "Technology stack" → Stacked layers
- "Data pipeline" → Flow through transformation stages

**Ask**: "Would seeing this concept as a picture help the learner understand faster?" If yes → SVG.

**Limitation**: Keep Arabic labels short (1-3 words) inside SVG. Long text should be in native PPTX shapes alongside the SVG visual.

## Visual Composition Plan

REQUIRED before building any PPTX lecture. The agent must:
1. Create a slide-by-slide visual plan (pattern + SVG? + image? per slide)
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
