# Slide Composition — Art Direction Guide

How to compose a full interactive lecture. This is NOT a template — it is a thinking framework for the agent acting as art director.

## Planning Phase (REQUIRED before building any PPTX lecture)

Before building ANY slide, create a Visual Composition Plan. Take your time with this step. Quality is more important than speed. Present the plan to the user for approval BEFORE calling any engine builder.

### Step 1: Map Content to Slides

List every topic from the content analysis. For each topic, decide:
- How many slides does this topic need? (1 concept = 1 slide)
- Where does it sit in the 5-act narrative arc? (Hook / Build / Insight / Practice / Summary)
- What type of slide? (structural, content, interaction, breathing)

### Step 2: Visual Composition Table

For EACH slide, fill in this table. This is the heart of the visual plan:

```
| # | Title (Arabic) | Act | Pattern | SVG Concept? | AI Image? | Image Prompt | Why This Visual |
|---|----------------|-----|---------|--------------|-----------|--------------|-----------------|
| 1 | عنوان المحاضرة | Hook | title | No | Yes (hero) | "digital innovation campus scene" | Sets visual tone |
| 2 | الأهداف التعليمية | Hook | objectives | No | No | — | Standard structural |
| 3 | 92% من المؤسسات... | Hook | stat_cards | No | No | — | Numbers ARE the visual |
| 4 | الركائز الخمس | Build | icon_grid | Yes: "5 pillars as building" | No | — | Metaphor makes it memorable |
| 5 | مراحل التصميم | Build | process_flow | Yes: "pipeline with stages" | No | — | Flow visualization |
| 6 | تطبيق عملي | Build | two_column | No | Yes | "student applying design thinking" | Real-world context |
| 7 | — | Build | quote_highlight | No | No | — | Breathing slide |
| 8 | طبقات الأمان | Build | content | Yes: "layered shields" | No | — | Abstract concept → tangible |
| 9 | اختبر فهمك | Practice | quiz | No | Yes | "thinking student at computer" | Visual stimulus |
| 10 | رتّب الخطوات | Practice | drag_drop | No | No | — | Interaction IS the visual |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

### Step 3: Visual Tool Palette — Learner-First Decisions

For EACH content slide, ask these three questions in order:

**Question 1: "Would a concept visualization make this idea tangible?"**
- Yes → Plan an SVG concept visualization (use_svg=True)
- Examples where SVG adds value:
  - "5 pillars of X" → Building with labeled pillars
  - "Security layers" → Layered shields or fortress walls
  - "Innovation ecosystem" → Connected growing elements
  - "Data pipeline" → Visual pipeline with transformation stages
  - "Relationship between A, B, C" → Connected nodes or Venn diagram
  - "Technology stack" → Stacked layers with labels
  - "Decision tree" → Branching paths with labels
  - "Cycle of improvement" → Circular flow with stages
- SVG is NOT just for "complex" diagrams — use it whenever a visual metaphor makes the concept easier to understand

**Question 2: "Would a real-world illustration add context?"**
- Yes → Plan an AI image (via image_prompt)
- Good image prompts are specific to the concept, not generic stock photos
- Examples: "student collaborating on digital whiteboard", "smart city IoT sensors connected"
- Images complement text — they don't repeat it

**Question 3: "Is the layout pattern itself sufficient?"**
- Yes → Native PPTX only (stat cards, timelines, comparisons carry their own visual weight)
- These patterns are self-explanatory — adding an image or SVG would be clutter

**Note**: A slide CAN have both SVG + AI Image when the concept benefits from both a diagram AND contextual illustration.

### Step 4: SVG Concept Descriptions

For each slide marked "Yes" for SVG, write a one-line visualization concept:

```
Slide 4: "Five pillars as an architectural building — each pillar labeled, connected by a roof labeled 'محو الأمية الرقمية'"
Slide 5: "Pipeline flowing right-to-left with 4 connected chambers, each containing a stage icon and label"
Slide 8: "Three concentric shield layers — outer=physical, middle=technical, inner=human, each with icons"
```

These descriptions guide the SVG generator prompt. Be specific about the metaphor, not just the data.

### Step 5: Image Prompts

For each slide marked "Yes" for AI Image, draft the English prompt and image_type:

```
Slide 1: prompt="modern university campus with digital holographic displays, flat vector style" | type=content
Slide 6: prompt="student applying design thinking on tablet with sticky notes, flat vector" | type=two_column
Slide 9: prompt="student thinking at computer screen with question marks, flat vector" | type=quiz
```

Target density: **8-12 images per lecture** (see image-gen.md for full guidelines).

### Step 6: Pacing & Density Check

Before presenting the plan, verify:

- [ ] No 3+ dense slides in a row (insert breathing slide: quote_highlight, section_divider)
- [ ] No same visual pattern on 2 consecutive slides
- [ ] Section divider every 4-6 content slides
- [ ] Interaction slide every 3-4 content slides (quiz, drag_drop, click_reveal, scenario)
- [ ] SVG visuals: 4-8 per lecture (enough to make concepts tangible, not so many it slows build)
- [ ] AI images: 8-12 per lecture (most content slides should have visual support)
- [ ] Total: 25-30 slides (if more, split into two lectures)
- [ ] Narrative arc complete: Hook(1-2) → Build(3-5) → Insight(1) → Practice(2-3) → Summary(1-2)

### Inspiration: Read Composition Examples
Before building, study the creative composition examples at `references/composition-examples.md`. These show HOW to reason about visual choices — not just which patterns to use, but WHY each one serves the learner.

### Present the Plan

Show the complete Visual Composition Table to the user. Wait for their approval before building any slides. The user may want to:
- Swap a visual pattern for a different one
- Add or remove SVG visualizations
- Change image prompts
- Adjust pacing

---

## Philosophy

The agent is an **art director**, not a template filler. Every visual decision serves the LEARNER:

- "Will this layout help the learner UNDERSTAND the concept faster?"
- "Does this slide FEEL professional, or does it feel auto-generated?"
- "Am I choosing this pattern because it fits the content, or because it is easy?"

A generic PowerPoint has uniform bullet slides, no visual hierarchy, and no pacing. Our lectures have narrative arc, visual variety, and deliberate breathing room.

## Narrative Arc

Every lecture follows a 5-act structure. The agent plans the full arc BEFORE building any slides.

```
ACT 1: HOOK (1-2 slides)
  Purpose: Grab attention. Make the learner curious.
  Patterns: stat_cards (surprising number), quote_highlight (provocative question),
            visual metaphor (SVG), or a striking image.
  Example: "92% of organizations will adopt AI by 2025 — are you ready?"

ACT 2: BUILD (3-5 slides)
  Purpose: Introduce core concepts. Build understanding incrementally.
  Patterns: process_flow, icon_grid, comparison, content slides with images.
  Rule: Each slide introduces ONE concept. Never combine two topics.

ACT 3: INSIGHT (1 slide)
  Purpose: The "aha" moment. The key revelation that ties everything together.
  Patterns: stat_cards (the payoff number), quote_highlight (expert insight),
            or a single powerful visual.
  This is the slide the learner remembers.

ACT 4: PRACTICE (2-3 slides)
  Purpose: Let the learner interact. Test understanding.
  Patterns: quiz (multiple choice), drag-drop (ordering/matching),
            click-reveal (exploration), scenario (decision-making).
  Rule: Interactions should test UNDERSTANDING, not just recall.

ACT 5: SUMMARY (1-2 slides)
  Purpose: Reinforce learning. Provide a visual recap.
  Patterns: icon_grid (key concepts), process_flow (recap steps),
            or summary slide.
  Rule: Use a DIFFERENT pattern than what was used in the build act.
```

## Pacing Rules

### The Breathing Rule
Never place 3+ dense information slides in a row. After 2 dense slides, insert a breathing slide.

**Dense slides**: content slides with 4+ bullets, comparison, process_flow with 5+ steps, icon_grid.

**Breathing slides**: quote_highlight, section_divider, stat_cards (2-3 stats), image-only slides.

```
GOOD:  [content] → [process_flow] → [quote_highlight] → [comparison] → [quiz]
BAD:   [content] → [process_flow] → [comparison] → [icon_grid] → [content]
```

### The Variety Rule
Never use the same visual pattern on two consecutive slides.

```
GOOD:  process_flow → stat_cards → content → comparison
BAD:   content → content → content → content
```

### The Section Rule
Insert a section_divider every 4-6 content slides. Each section represents one concept or theme.

```
[title] → [objectives] → [DIVIDER: Section 1] → [4-5 slides] → [DIVIDER: Section 2] → [4-5 slides] → [summary]
```

## Interaction Placement

After every 3-4 content slides, place an interaction slide (quiz, click-reveal, drag-drop, or scenario). This keeps learners engaged and tests comprehension incrementally.

```
[content] → [content] → [process_flow] → [QUIZ] → [content] → [comparison] → [content] → [DRAG-DROP]
```

Interaction rules:
- Quiz after factual content (tests recall)
- Click-reveal after detailed concepts (tests exploration)
- Drag-drop after sequential/ordered content (tests understanding of order)
- Scenario after decision-focused content (tests application)

## Slide Count

Target **25-30 slides** per lecture (including interactions and structural slides).

| Slide Type | Count | Percentage |
|---|---|---|
| Structural (title, objectives, dividers, summary, closing) | 6-8 | ~25% |
| Content (visual grammar patterns) | 12-16 | ~50% |
| Interactions (quiz, drag-drop, click-reveal) | 4-6 | ~20% |
| Breathing (quotes, transitions) | 2-3 | ~5% |

If content requires more than 30 slides, split into two lectures.

## SVG vs Native PPTX — Learner-First Decision

Use **native PPTX shapes** when the layout pattern itself carries the visual meaning (stat cards show numbers, timelines show progression, comparisons show differences). Native shapes handle Arabic RTL, line wrapping, and font rendering correctly.

Use **SVG concept visualization** (via Gemini AI, `use_svg=True`) when a **visual metaphor or diagram** would make the concept easier for the learner to understand. This includes:
- **Visual metaphors**: "5 pillars" as a building, "security layers" as shields, "ecosystem" as connected organisms
- **Architecture diagrams**: technology stacks, system components, layered models
- **Relationship maps**: how concepts connect, cause-and-effect chains, Venn-style overlaps
- **Circular flows**: cycles, feedback loops, iterative processes
- **Transformation pipelines**: data flowing through stages, input→process→output
- **Complex processes**: 5+ step flows that benefit from creative layout

SVG is a **primary visualization tool**, not a last resort. Ask: "Would seeing this concept as a picture help the learner understand it faster?" If yes, use SVG.

**Note on Arabic text**: SVG text is rasterized to PNG for PPTX embedding. Keep labels short (1-3 words). Long Arabic text should be in native PPTX shapes alongside the SVG visual.

## Visual Strategy — 3-Tool Palette

Not every slide needs every tool. Choose deliberately based on what helps the LEARNER:

| Slide Type | AI Image? | SVG Concept? | Why |
|---|---|---|---|
| Content slides | Yes (often) | Consider | Image illustrates; SVG if concept is abstract |
| Section dividers | Optional | No | Decorative mood-setting |
| Quiz slides | Optional | No | Visual stimulus for the question |
| Stat cards | No | No | Numbers ARE the visual |
| Process flows | No | Yes (if 5+ steps or metaphor helps) | SVG makes flow tangible |
| Quote highlights | No | No | Text IS the visual |
| Timelines | No | Consider (if events need visual context) | Timeline may benefit from illustrated milestones |
| Icon grids | No | Consider (if items form a system) | SVG if items are interconnected, not just a list |
| Comparisons | No | Consider (if comparing systems/architectures) | SVG for visual side-by-side systems |
| Cycle diagrams | No | Yes (always) | Circular layouts need SVG |

**AI Images** (via `image_prompt`): Real-world illustrations that add context. Keep prompts specific to the concept.

**SVG Concept Visualizations** (via `use_svg=True`): Diagrams and visual metaphors that make abstract ideas tangible. Use whenever a visualization helps understanding — not just for "complex" layouts.

**Combining both**: A content slide can have BOTH an SVG concept diagram AND an AI image when the concept benefits from both perspectives.

## Whitespace

Do not fill every pixel. Generous margins and breathing room make content feel premium.

Rules:
- **5% safe margin** from each slide edge — no content in the outer frame
- **Content zone** is 78% of the slide — leave header (10%) and footer (12%) zones clear
- **Card padding** at minimum 8pt inside, 16pt between cards
- If a slide feels crowded, split into two slides — never cram

## The Squint Test

Blur your eyes and look at the slide. If you can still see the visual hierarchy (title stands out, main content is distinct, secondary elements recede), the design works. If everything blurs into a uniform mass, add more contrast — bigger title, more whitespace, or fewer elements.

## The PowerPoint Test

Does the slide look like a generic corporate PowerPoint? Warning signs:
- All bullet points, no visual patterns
- Same layout on every slide
- No depth (no shadows, no background washes)
- Text filling the entire slide with no breathing room
- Clip-art or placeholder boxes

If yes: add visual variety (change the pattern), add depth (background wash + shadows), and add whitespace (reduce text or split slides).

## Composition Checklist

Before building each slide, the agent should answer:

1. **What relationship** does this content express? (sequential, comparative, hierarchical, etc.)
2. **Which visual pattern** best represents that relationship? (see visual-grammar.md)
3. **Where are we** in the narrative arc? (hook, build, insight, practice, summary)
4. **Is pacing correct?** (no 3+ dense slides in a row, variety in patterns)
5. **Does this slide need an image?** (does the visual pattern already carry the concept?)
6. **Is there enough whitespace?** (content should breathe, not fill every pixel)
7. **Would a Storyline developer understand** what to build from the speaker notes?
