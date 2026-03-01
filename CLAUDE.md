# Storyboard Generator

AI-powered system that transforms raw client course content into production-ready educational storyboard documents (DOCX/PPTX) for Arabic e-learning courses. PPTX output is designed for direct import into Storyline 360.

## Architecture

```
User provides raw content (PDF, DOCX, PPTX, images)
  → Main agent COORDINATES + GENERATES content directly (no subagents)
    → Engine scripts build formatted documents
      → Output: production-ready DOCX/PPTX files
```

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Unified Skill | `.claude/skills/storyboard-generator/` | All instructions, engine, references, assets |
| Engine Scripts | `.claude/skills/storyboard-generator/scripts/` | 10 Python modules (9,491 lines) |
| References | `.claude/skills/storyboard-generator/references/` | 14 reference docs (3,200+ lines) |
| Assets | `.claude/skills/storyboard-generator/assets/pptx_assets/` | Decorative slide elements (17 PNGs) |
| Coordinator | `.claude/commands/storyboard.md` | `/storyboard` entry point |
| Project Configs | `projects/[code]/config.json` | Per-project metadata and branding |

### PPTX Engine — Modular Architecture (6,419 lines)

The PPTX engine is split into 7 focused modules that compose via Python mixins:

```
scripts/
├── _pptx_core.py              (1,273 lines) — SlideEngine base class, constants, helpers, RTL, shadows
├── _pptx_depth.py               (365 lines) — Background depth layers, decorative elements, accent system
├── _pptx_structural.py          (763 lines) — Title, objectives, section divider, summary, closing
├── _pptx_visual_grammar.py    (1,684 lines) — 8 visual patterns (process flow, stats, timeline, etc.)
├── _pptx_interactions.py      (1,106 lines) — 6 interactions (quiz, drag-drop, scenario, etc.)
├── _pptx_svg_generator.py       (585 lines) — SVG generation via Gemini AI for complex diagrams
├── pptx_engine.py               (643 lines) — LectureBuilder composer (28 public add_* methods)
├── docx_engine.py             (2,335 lines) — 8 DOCX builders
├── image_gen.py                 (448 lines) — AI image generation via Gemini
└── rtl_helpers.py               (289 lines) — RTL XML workarounds
```

**Inheritance chain**: `LectureBuilder → StructuralMixin → InteractionsMixin → VisualGrammarMixin → DepthMixin → SlideEngine`

### How Document Generation Works

- Python builders construct DOCX/PPTX documents from scratch
- All formatting, RTL, fonts, colors handled automatically
- The agent produces CONTENT and calls engine builders via `python3 -c "..."`
- Portable imports: `_paths.py` auto-detects project root via git (works on any machine)
- For PPTX: agent acts as **art director** with a visual palette (see `references/principles.md`):
  - **Native PPTX shapes** — when the layout pattern IS the visual (stat cards, timelines)
  - When an image is needed, classify into **4 output types**: Photo (Freepik stock → AI raster) · Illustration (Freepik stock → Recraft → SVG) · Infographic (SVG → HTML+CSS) · Screen (HTML+CSS only). See `references/principles.md` → "The Visual Palette"
- Every PPTX slide has **Storyline blueprints** in speaker notes (layers, states, triggers, variables)

## Non-Negotiable Rules

1. **COORDINATOR + CONTENT PRODUCER** — The main agent orchestrates AND generates. No subagents needed.
2. **ONE AT A TIME** — Generate each storyboard type individually with user review between each.
3. **ENGINE BUILDS DOCUMENTS** — All documents built by scripts in the skill. Call builders via Bash.
4. **ARABIC RTL** — All content in Arabic, right-to-left. No tashkeel/diacritics needed.
5. **USER DECIDES** — AI suggests (activity types, content distribution), user approves before proceeding.
6. **VISUAL GRAMMAR** — For PPTX: never default to bullets. Choose the best visual pattern per concept.
7. **STORYLINE-READY** — Every PPTX slide must have named shapes and interaction blueprints in notes.
8. **LEARNER-FIRST VISUALS** — Classify each image need (Photo/Illustration/Infographic/Screen), follow priority order, judge output, iterate. Plan visuals BEFORE building.

## Workflow (Every Unit)

```
Phase 1: Content Analysis
  → Read all raw content files
  → Produce structured Arabic analysis
  → Present for user review

Phase 2: Learning Objectives
  → Generate Bloom's Taxonomy-aligned objectives
  → Call ObjectivesBuilder engine
  → Present for user review

Phase 3: Individual Storyboards (one at a time)
  → Read type-specific instructions from references/storyboard-types.md
  → For PPTX: also read pptx-composition-arc.md + visual-grammar.md + pptx-design-system.md
  → Generate content + call engine builder
  → Present for user review → next type after approval
```

### Suggested Storyboard Order
1. Learning Objectives (الأهداف التعليمية)
2. Learning Map / Infographic (خارطة التعلم)
3. Pre-Test (الاختبار القبلي)
4. Interactive Lecture (المحاضرة التفاعلية)
5. PDF Lecture (محاضرة PDF)
6. Motion Video (فيديو موشن)
7. Interactive Activities (الأنشطة التفاعلية)
8. Discussion (النقاش)
9. Assignment (الواجب)
10. Post-Test (الاختبار البعدي)
11. Summary (الملخص)
12. Course Exam (if applicable)

## 12 Storyboard Types

| # | Type | Engine Builder |
|---|------|----------------|
| 1 | فيديو موشن (Motion Video) | VideoBuilder (DOCX) |
| 2 | نشاط تفاعلي (Interactive Activity) | ActivityBuilder (DOCX) |
| 3 | محاضرة تفاعلية (Interactive Lecture) | LectureBuilder (PPTX) |
| 4 | محاضرة PDF (PDF Lecture) | LectureBuilder (PPTX) |
| 5 | إنفوجرافيك (Learning Map) | InfographicBuilder (DOCX) |
| 6 | اختبار قبلي (Pre-Test) | TestBuilder (DOCX) |
| 7 | اختبار بعدي (Post-Test) | TestBuilder (DOCX) |
| 8 | نقاش (Discussion) | DiscussionBuilder (DOCX) |
| 9 | واجب (Assignment) | AssignmentBuilder (DOCX) |
| 10 | اختبار المقرر (Course Exam) | TestBuilder (DOCX) |
| 11 | أهداف تعليمية (Learning Objectives) | ObjectivesBuilder (DOCX) |
| 12 | ملخص (Summary) | SummaryBuilder (DOCX) |

## PPTX Slide Methods (28 total)

| Category | Methods | Count |
|----------|---------|-------|
| Structural | title, objectives, section_divider, summary, closing | 5 |
| Content | content_slide, content_with_cards, two_column | 3 |
| Visual Grammar | process_flow, stat_cards, quote_highlight, timeline, comparison, icon_grid, cycle_diagram, concept_visual | 8 |
| Interactions | quiz, drag_drop, click_reveal, slider, dropdown, scenario | 6 |
| Depth | depth_wash, depth_accent, decorative_corner, progress_dots, header_bar, section_banner | 6 |

## Skill Reference Files (14 docs)

Navigate by what you're doing:

| Stage | Reference | Purpose |
|-------|-----------|---------|
| **Foundation** | `principles.md` | **Single source of truth** — design philosophy, visual palette, rules |
| **Composing** | `composition-examples.md` | 3 creative composition examples with agent reasoning (Anthropic "Tool Use Examples" pattern) |
| **Analyzing** | `storyboard-types.md` | Per-type domain knowledge, rules, quality standards |
| **Analyzing** | `educational-standards.md` | Bloom's Taxonomy, QM alignment, Gagne's Nine Events, NELC, growth mindset feedback |
| **Designing** | `pptx-composition-arc.md` | Pre-build planning, narrative arc, motivation arc, pacing, engagement design, art direction |
| **Designing** | `visual-grammar.md` | 8 visual patterns + selection guide |
| **Designing** | `pptx-design-system.md` | Art direction, typography, colors, depth |
| **Building** | `pptx-builder.md` | Full PPTX API (28 methods across all modules) |
| **Building** | `docx-builders.md` | DOCX builder API (8 builders) |
| **Building** | `storyline-blueprint.md` | Storyline 360 interaction specs |
| **Building** | `image-gen.md` | AI image generation API + density guidelines |
| **Building** | `recraft-gen.md` | Recraft MCP illustration generation — vector/raster with style consistency |
| **Reviewing** | `quality-checklist.md` | Pre-delivery quality gates |
| **Debugging** | `common-issues.md` | Known problems, fixes, anti-patterns |
| **Debugging** | `rtl-arabic-patterns.md` | RTL-specific issues and workarounds |
| **Debugging** | `engine-internals.md` | Module architecture, how things work internally |

## Project Setup

When starting a new project, collect:
- Project code (e.g., `NJR01`)
- Project name, client name, institution
- Client logo + header image file paths
- Designer name
- Unit count and names

Save to: `projects/[project-code]/config.json`

## File Naming Convention

```
[PROJECT_CODE]_U[UNIT_NUMBER]_[Element_Type]
```

## Output Location

```
output/[project-code]/U[XX]/
```

## Content Input
- User shares **file paths** — read them directly using Read tool
- Content can be: .pptx, .docx, .pdf, images, .txt
- Each content share = one complete unit

## Branding
- Per-project branding (different logos, headers per client)
- Stored in `projects/[project-code]/branding/`
