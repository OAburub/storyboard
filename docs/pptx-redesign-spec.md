# PPTX Engine Visual Redesign Specification

## Mission
Transform the PPTX engine output from "educational template" quality to **McKinsey-level consulting-firm minimalism** — ultra-clean, white space-driven, structured grids, corporate serious.

## Problem Statement
The current engine output looks "cheap and not nice." Specific issues:
1. **Decorative corners** feel like clip-art, not professional design
2. **Too many colors/elements** — slides feel cluttered
3. **Typography is off** — font sizes, weights, spacing feel like a school project
4. **Interaction patterns** (quiz, drag-drop, click-reveal) need complete visual rethink
5. **Depth effects** (shadows, gradients) feel dated

## Target Style
**McKinsey-style**: Ultra-clean, minimal, lots of white space, navy/dark blue accent, very structured grids, "corporate serious"

## Design Principles (from interview)
1. **White space is the design** — let breathing room do the heavy lifting
2. **2-3 colors maximum** — research optimal palette for Arabic educational + consulting feel
3. **Typography carries the message** — Keep Tajawal font but fix sizing, weights, spacing
4. **No fake decorations** — remove or replace decorative corners with minimal alternatives
5. **Interactions should feel elegant** — redesign quiz, drag-drop, click-reveal, cards patterns
6. **Content clean, interactions refined** — all 13 slide types need visual audit

## End Users (Both must be impressed)
- **Instructional designers**: Import into Storyline 360, care about structure + clean import
- **University faculty/clients**: Professors and deans who review for approval, judge visual quality

## Scope
- **Modify existing engine** (not rewrite) — `engine/pptx_engine.py`
- **Fix layout first, add images back later** — get slides looking great without images
- **Research both** Anthropic's official PPTX skill AND consulting-firm design patterns

## Research Required

### 1. Anthropic Official PPTX Skill Analysis
- URL: https://github.com/anthropics/skills/tree/main/skills/pptx
- How do they structure PPTX generation?
- What design decisions do they make?
- How do they handle typography, spacing, colors?
- What can we learn from their approach?

### 2. Design Audit (3 perspectives)
**As Art Director**: Typography hierarchy, color harmony, visual rhythm, white space usage, grid consistency
**As Client** (university dean): Does this look professional? Would I approve this? Does it represent my institution well?
**As Designer**: Interaction affordances, visual consistency across slide types, alignment precision, detail polish

### 3. Engine Code Audit
- Trace each visual issue back to specific code in `pptx_engine.py`
- Identify hardcoded values that produce poor output
- Map all 13 slide types to their visual problems
- Identify quick wins vs deeper changes

## Current Engine Stats
- File: `engine/pptx_engine.py` (~3,163 lines)
- 13 slide types (title, objectives, content, section_divider, quiz, drag_drop, click_reveal, cards, two_column, closing, tabs, hotspot, sorting)
- Uses python-pptx library
- Tajawal font family (Regular, Bold, Medium)
- Color palette: #2D588C, #156082, #009688, #FF9800
- Layout cycling (A/B/C variants for content slides)
- OOXML shadows, corner radius, decorative corners on section dividers

## Specimen File for Audit
- `output/NJR01/U03/NJR01_U03_Interactive_Lecture.pptx` (19 slides, 6.4 MB)

## Deliverables
1. Research findings document with specific recommendations
2. Modified `engine/pptx_engine.py` with visual improvements
3. Before/after comparison (regenerated Unit 3 lecture)
