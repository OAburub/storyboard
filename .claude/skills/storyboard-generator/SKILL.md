---
name: storyboard-generator
description: Generates production-ready DOCX/PPTX storyboard documents for Arabic e-learning courses. 12 types including interactive lectures, tests, activities, videos, discussions, assignments, summaries, objectives, and infographics. Creates Storyline 360-ready PPTX with visual grammar design, named shapes, and interaction blueprints. Use when user says /storyboard, mentions storyboard generation, e-learning course documents, interactive lectures, or Arabic educational content.
---

# Storyboard Generator

Transforms raw course content into production-ready educational storyboard documents (DOCX/PPTX) for Arabic e-learning courses. PPTX output is designed for direct import into Storyline 360.

## Philosophy: Agent as Art Director (Learner-First)

You are not a template filler. You are an **art director** who makes creative design decisions for every slide. For EACH slide, ask: **"What visual would make this concept click fastest for the learner?"**

**Native PPTX shapes** — when the layout pattern itself IS the visual (stat cards, timelines, comparisons, icon grids). This is for PPTX slide design, not for images placed into slides.

**When you need an image** (placed into PPTX or DOCX), classify it into one of 4 output types, then follow the priority order:

| Output Type | Priority Order |
|-------------|---------------|
| **Photo** (real-world scenes, people, objects) | Freepik stock → AI raster (Gemini) |
| **Illustration** (drawings, icons, visual metaphors) | Freepik stock → Recraft vector (MCP) → Native SVG (Gemini) |
| **Infographic** (data viz, process diagrams, concept maps) | Native SVG (Gemini) → HTML+CSS (Playwright) |
| **Screen** (UI mockups, شاشة توضيحية, activity previews, motion scenes) | HTML+CSS only |

Images are **directions for the graphics team** — they may use them directly, modify SVGs, find stock alternatives, or use them as visual guides. Always provide file paths/URLs. HTML+CSS is an organizational tool, not a drawing tool. Screens and infographics can contain other output types (photos, illustrations) sourced by their own priority order.

Think about **composition, whitespace, focal points, and pacing** — not just "which pattern to use."

**Non-Negotiable Rules** → See CLAUDE.md

## Workflow

### Phase 0: Project Setup (if no config exists)
Collect: project code, name, client, institution, logo path, header path, designer, unit count/names.
Save to: `projects/[code]/config.json`

### Phase 1: Content Analysis
- Read ALL provided content files
- Produce structured Arabic analysis: topics, structure, concepts, terms, media, gaps, distribution
- **Assign Bloom's level to each topic** (read `educational-standards.md` Section 1)
- **Create draft alignment map**: objective → content → activity → assessment (Section 3)
- **Identify "Why This Matters" hooks** for each section (Section 7)
- **Plan Motivation Arc** (read `references/pptx-composition-arc.md` → Part 4 "Pre-Build Design Questions"):
  - What should the learner FEEL? (target aesthetics)
  - What's the learner's current motivation level?
  - Where are the information gaps that create curiosity?
  - Where is the culminating challenge (Triumph moment)?
- Suggest activity types and test concepts
- Present for user review. Wait for approval.

### Phase 2: Learning Objectives
- Generate 4-8 Bloom's Taxonomy-aligned objectives using **measurable verbs only** (read `educational-standards.md` Section 1)
- Format: "أن + الفعل (من تصنيف بلوم) + المتعلم + المحتوى + المعيار"
- **Verify alignment map**: every objective has matching content + activity + assessment
- **Check Bloom's distribution**: not all at Remember level — include Apply/Analyze
- Call ObjectivesBuilder engine
- Present for user review. Wait for approval.

### Phase 3: Individual Storyboards (one at a time, in suggested order)
For each requested type:
1. Read type-specific instructions from `references/storyboard-types.md`
2. For PPTX lectures: also read design references + `educational-standards.md` Gagne's Nine Events (Section 2)
3. For PPTX lectures: also read `references/pptx-composition-arc.md` (Parts 1-5: planning, arcs, pacing, engagement)
4. For tests: read `educational-standards.md` Bloom's-question mapping + feedback library (Sections 5, 8)
5. **For PPTX lectures: Create Visual Composition Plan BEFORE building**
   - Read `references/pptx-composition-arc.md` → Part 1 "Pre-Build Planning" section
   - Create slide-by-slide plan: visual pattern + SVG concept + AI image prompt per slide
   - **Map each slide to Motivation Arc phase** (Hook/Ignite/Struggle/Triumph/Launch)
   - **Verify the 3-4 slide rule:** no more than 3-4 content slides without an interaction
   - Present the visual plan to the user for review
   - Wait for approval. THEN build.
   - Take your time with this step. Quality is more important than speed.
5. Generate content and call the appropriate engine builder (use `use_svg=True` for SVG-planned slides)
6. **Run content type distribution check** (Section 6): variety, interactions, no passive-only sections
7. Present output for user review
8. Wait for approval before next type

**Suggested order**: Objectives → Learning Map → Pre-Test → Interactive Lecture → PDF Lecture → Video → Activities → Discussion → Assignment → Post-Test → Summary

## Engine Quick Reference

### Import Bootstrap (portable — works on any machine)
```python
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
```

### DOCX Builders (8 types)
```python
from docx_engine import (
    TestBuilder, ActivityBuilder, VideoBuilder,
    ObjectivesBuilder, SummaryBuilder, InfographicBuilder,
    DiscussionBuilder, AssignmentBuilder,
)
```

### PPTX Builder
```python
from pptx_engine import LectureBuilder  # Interactive & PDF lectures
```

**28 slide methods** organized by purpose:
- **Structural** (5): title, objectives, section_divider, summary, closing
- **Content** (3): content_slide, content_with_cards, two_column
- **Visual Grammar** (8): process_flow, stat_cards, quote_highlight, timeline, comparison, icon_grid, cycle_diagram, concept_visual
- **Interactions** (6): quiz, drag_drop, click_reveal, slider, dropdown, scenario
- **Depth** (5): depth_wash, depth_accent, decorative_corner, progress_dots, header_bar, section_banner

## Image Generation

Classify each image need into an output type, then follow its priority order. See `references/image-gen.md` for the full decision framework and API details.

| Output Type | Priority Order | Reference |
|-------------|---------------|-----------|
| **Photo** | Freepik stock → AI raster (Gemini) | `image-gen.md` |
| **Illustration** | Freepik stock → Recraft (MCP) → SVG (Gemini) | `image-gen.md`, `recraft-gen.md` |
| **Infographic** | SVG (Gemini) → HTML+CSS (Playwright) | `image-gen.md`, `screenshot-gen.md` |
| **Screen** | HTML+CSS only | `screenshot-gen.md` |

All builders support `image_path` and `image_prompt` parameters. Priority: `image_path` > `image_prompt`. Always provide file paths/URLs for the graphics team.

## Navigation — Read What You Need

### Foundation (read once, always applies):
→ `references/principles.md` — **Single source of truth** for design philosophy, visual palette, non-negotiable rules. All other docs reference this.

### When analyzing content (Phase 1):
→ `references/storyboard-types.md` — per-type domain knowledge, rules, quality standards
→ `references/educational-standards.md` — **Bloom's Taxonomy, QM alignment, Gagne's Nine Events, NELC standards** (read Sections 1-4 + Section 9 Backward Design)

### When generating objectives (Phase 2):
→ `references/educational-standards.md` — Bloom's verb table (Arabic + English), objective formula, alignment map template

### When designing a PPTX lecture:
→ `references/pptx-composition-arc.md` — **Pre-build planning, narrative arc, motivation arc, pacing, engagement design, SDT, information gap techniques**
→ `references/visual-grammar.md` — 8 visual patterns + selection guide
→ `references/pptx-design-system.md` — art direction, typography, colors, depth
→ `references/storyline-blueprint.md` — Storyline 360 interaction specs
→ `references/educational-standards.md` — Gagne's Nine Events → slide mapping (Section 2)

### When composing a PPTX lecture (creative thinking):
→ `references/composition-examples.md` — 3 complete examples of creative visual composition with agent reasoning
→ `references/visual-grammar.md` → "SVG Prompt Engineering Patterns" section — prompt patterns for writing better concept descriptions

### When building slides:
→ `references/pptx-builder.md` — full API for all 28 slide methods
→ `references/image-gen.md` — image generation API + density guidelines
→ `references/recraft-gen.md` — Recraft MCP illustration generation (vector/raster with style consistency) — lazy-load only when using Recraft
→ `references/docx-builders.md` — DOCX builder API (8 builders)

### When generating tests/quizzes:
→ `references/educational-standards.md` — Bloom's → question type mapping, factual accuracy rule, growth mindset feedback library (Sections 5, 8)

### When reviewing quality:
→ `references/quality-checklist.md` — pre-delivery quality gates

### When generating شاشة توضيحية (UI mockup / demo screen) — lazy-load only when needed:
→ `references/screenshot-gen.md` — HTML → PNG via Playwright: template, CLI, viewport sizes, design rules

### When debugging:
→ `references/common-issues.md` — known problems, fixes, anti-patterns
→ `references/rtl-arabic-patterns.md` — RTL-specific issues and workarounds
→ `references/engine-internals.md` — module architecture, how things work internally
