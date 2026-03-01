# Design Principles — Single Source of Truth

All other reference files REFERENCE this document for philosophy and principles. If you need to change a principle, change it HERE and the entire system updates.

## Core Philosophy: Learner-First Visual Design

The agent is an **art director**, not a template filler. Every visual choice serves the LEARNER. For each slide, ask: **"What visual would make this concept click fastest for the learner?"**

## The Visual Palette

**Native PPTX shapes** — when the layout pattern itself IS the visual (stat cards, timelines, comparisons). The slide structure carries the meaning. This is for PPTX slide design, not for images placed into slides.

**When you need an image** (placed into PPTX or DOCX), classify it into one of 4 output types, then follow the priority order for that type:

### Output Type 1: Photo

Real-world photographs — people, objects, scenes, environments, textures.

| Priority | Method | When |
|----------|--------|------|
| 1st | **Freepik stock search** | Always try first. Easier for the graphics team to find alternatives for stock photos than to regenerate AI images. |
| 2nd | **AI raster image** (Gemini) | Only if no suitable stock photo exists. |

### Output Type 2: Illustration

Drawings — icons, characters, conceptual art, visual metaphors, decorative elements. Anything that is "drawn" rather than photographed.

| Priority | Method | When |
|----------|--------|------|
| 1st | **Freepik stock search** | Try first for common illustration needs. |
| 2nd | **Recraft vector** (MCP) | When stock doesn't match, or you need style consistency across many illustrations. Lazy-load `references/recraft-gen.md`. |
| 3rd | **Native SVG** (Gemini) | For abstract concept metaphors — pillars, shields, ecosystems, tech stacks, data flows. Lazy-load `references/image-gen.md`. |

### Output Type 3: Infographic

Data visualizations, structured information layouts, process diagrams, comparison charts, concept maps — anything that organizes information visually.

| Priority | Method | When |
|----------|--------|------|
| 1st | **Native SVG** (Gemini) | Best for structured visual layouts — flows, hierarchies, cycles, layered diagrams. |
| 2nd | **HTML+CSS** (Playwright) | When you need richer text rendering, multi-column layouts, or precise Arabic text control. Lazy-load `references/screenshot-gen.md`. |

Infographics may **contain illustrations** within them. If so, source the illustration using the Illustration priority order above, then embed it in the SVG or HTML.

### Output Type 4: Screen

UI mockups, شاشة توضيحية, activity previews, motion graphics scenes, software interfaces — any visual that represents "what the learner sees on a screen."

| Priority | Method | When |
|----------|--------|------|
| Only | **HTML+CSS** (Playwright) | Always. HTML+CSS is the only method for screens. Lazy-load `references/screenshot-gen.md`. |

Screens may **contain other output types** within them. A screen showing a photo uses Photo instructions to source the photo, then embeds it in the HTML. A screen with an illustration follows Illustration instructions, etc.

**For projects with many screens**: consider building a reusable HTML template and a script to fill it, ensuring visual consistency across all screens in the project.

### Combining Outputs

Any image can combine output types. An infographic (SVG) containing illustrations (Freepik/Recraft). A screen (HTML+CSS) containing photos (Freepik/Gemini) and illustrations. Think in layers: the **outer container** determines the primary method, inner elements follow their own type's priority.

### Judgment and Iteration

These are priority orders, not rigid rules. Choose the method you see fit for each specific image. Judge your output honestly — if it doesn't match your art direction vision, try a different method or regenerate. The images are **directions for the graphics team**, who may use them directly, modify SVGs, find stock alternatives, or use them as visual guides.

### File Tracking

Always provide the file path or URL for every fetched/generated image. Point out relative locations to make it easy for the instructional designer and graphic designer to find them.

## SVG Philosophy

SVG is NOT a last resort for "complex diagrams." It is a **primary visualization tool** for:
- **Infographics** — structured information, process flows, hierarchies, cycles, comparisons
- **Concept metaphors** — "5 pillars" as pillars, "security layers" as shields, "data pipeline" as flow stages

**Limitation**: Keep Arabic labels short (1-3 words) inside SVG. Long Arabic text should be in native PPTX shapes alongside the SVG, or use HTML+CSS (Infographic type, 2nd priority) instead.

## HTML+CSS Philosophy

HTML+CSS is an **organizational tool**, not a drawing tool. Use it to arrange and structure content — text, images, shapes, embedded SVGs — with precise layout control. Never use it to "draw" illustrations (use Illustration type methods for that).

Use cases:
- **Screens** (Output Type 4) — UI mockups, activity previews, motion graphics scenes, شاشة توضيحية
- **Infographics** (Output Type 3, 2nd priority) — when SVG's text limitations are a problem
- Precise multi-column layouts with Arabic text
- Any visual needing embedded images sourced from other methods

Inline SVG can be embedded inside HTML when you need vector shapes within a richer layout.

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
