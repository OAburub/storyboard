# Storyline 360 Blueprint System

How to write speaker notes that serve as complete Storyline 360 production instructions. The goal: the Storyline developer opens the PPTX, reads the notes, and knows EXACTLY what to build without guessing.

## Why This Matters

The PPTX is an **input for Storyline 360**, not a standalone presentation. Every slide will be imported into Storyline where the developer adds:
- Layers (feedback, hover states, hidden content panels)
- States (normal, hover, selected, visited, disabled)
- Triggers (show layer on click, change state on hover, jump to slide)
- Variables (score, attempts, completion tracking)
- Conditions (show X if score > 80, enable next when all visited)
- Audio sync (narration tied to timeline cues)

## Speaker Notes Format

Every slide's speaker notes use this exact structure:

```
=== STORYLINE BLUEPRINT ===

Slide Type: [interaction type]
Duration: [learner-paced / auto-advance after Xs]
Audio: [filename or "none"]

Layers:
- base (default visible)
- [layer_name]: [purpose]

States:
- [shape_name]: [Normal, Hover, Selected, Visited, Disabled]

Triggers:
1. [Action] when [Event] on [Object]
   - [Additional consequence]
2. [Next trigger]

Variables:
- [var_name] ([Type], default [value]): [purpose]

Conditions:
- [condition description]

=== NARRATOR SCRIPT ===
[Full Arabic narration text for audio recording]

=== PRODUCTION NOTES ===
[Optional: special instructions for the Storyline developer]
```

## Blueprint Templates by Interaction Type

### Static Content Slide

Simplest form — just base layer, audio trigger, narrator script:

```
Slide Type: static-content | Duration: learner-paced | Audio: narration_s[XX].mp3
Layers: base (default visible)
Triggers: 1. Play media 'narration_s[XX]' when timeline starts
```

### Click-to-Reveal (Tabs / Hotspots)

Like quiz but with tab buttons instead of options. Key additions:
- One layer per revealable content panel (`detail_1`, `detail_2`, etc.)
- Tab states: `[Normal, Hover, Visited]`
- `clickCount` variable tracks tabs visited
- Completion layer shown when `clickCount >= N`
- Enable Next button when enough tabs visited

### Quiz (Multiple Choice) — Full Template

```
=== STORYLINE BLUEPRINT ===

Slide Type: quiz-mc
Duration: learner-paced
Audio: none
Scoring: 10 points

Layers:
- base (default visible) — question + options
- feedback_correct: [correct answer explanation in Arabic]
- feedback_incorrect: [explanation of why other options are wrong]

States:
- opt_1: [Normal, Hover, Selected]
- opt_2: [Normal, Hover, Selected]
- opt_3: [Normal, Hover, Selected]
- opt_4: [Normal, Hover, Selected]
- btn_submit: [Normal, Hover, Disabled]

Triggers:
1. Set state of 'opt_[N]' to 'Selected' when user clicks 'opt_[N]'
   - Deselect all other options (set to 'Normal')
   - Set state of 'btn_submit' to 'Normal' (enable it)
2. Show layer 'feedback_correct' when user clicks 'btn_submit'
   IF selected option = 'opt_[correct]'
   - Add 10 to 'quizScore'
3. Show layer 'feedback_incorrect' when user clicks 'btn_submit'
   IF selected option != 'opt_[correct]'
   - Add 1 to 'attempts'
4. Hide layer 'feedback_incorrect' and allow retry when 'attempts' < 2
5. Jump to next slide from feedback_correct layer 'btn_continue'

Variables:
- quizScore (Number, default 0): cumulative quiz score
- attempts (Number, default 0): attempts on this question

Correct Answer: opt_[N] — [answer text]

=== NARRATOR SCRIPT ===
[Question narration in Arabic]
```

### Drag-and-Drop

Like quiz but with drag items and drop zones. Key additions:
- Item states: `[Normal, Drop Correct, Drop Incorrect]`
- Zone states: `[Normal, Hover, Accepted]`
- Triggers: correct placement → `Drop Correct` state; wrong → return to start
- `dragAttempts` and `correctPlacements` variables
- Drag mapping in notes: `item_1 → zone_[target]: [explanation]`
- Allow N attempts before showing correct answers

### Branching Scenario — Full Template

```
=== STORYLINE BLUEPRINT ===

Slide Type: scenario
Duration: learner-paced
Audio: narration_s[XX].mp3

Layers:
- base (default visible) — situation description + choice buttons
- consequence_a: [what happens if choice A]
- consequence_b: [what happens if choice B]
- consequence_c: [what happens if choice C]
- reflection: [debrief after seeing consequence]

States:
- btn_choice_a: [Normal, Hover, Selected]
- btn_choice_b: [Normal, Hover, Selected]
- btn_choice_c: [Normal, Hover, Selected]

Triggers:
1. Show layer 'consequence_a' when user clicks 'btn_choice_a'
   - Set 'lastChoice' to 'A'
2. Show layer 'consequence_b' when user clicks 'btn_choice_b'
   - Set 'lastChoice' to 'B'
3. Show layer 'consequence_c' when user clicks 'btn_choice_c'
   - Set 'lastChoice' to 'C'
4. Show layer 'reflection' from any consequence layer 'btn_continue'
5. IF 'lastChoice' = 'B' (optimal): Add 10 to 'scenarioScore'

Best Choice: B — [explanation of why]

Variables:
- lastChoice (Text, default ""): which path was chosen
- scenarioScore (Number, default 0): scenario performance

=== NARRATOR SCRIPT ===
[Arabic scenario description and instruction]
```

### Slider / Rating

Simplest interaction — just a slider variable and conditional text feedback:
- `sliderValue` variable (Number, default 5)
- Triggers update `txt_feedback` text based on value ranges (0-3, 4-7, 8-10)

## Shape Naming Convention

Every shape in the PPTX MUST be named meaningfully. The Storyline developer uses these names to set up triggers.

| Prefix | Element | Examples |
|---|---|---|
| `bg_` | Background elements | bg_depth_oval, bg_header_bar |
| `hdr_` | Header zone | hdr_section_tag, hdr_progress |
| `txt_` | Text content | txt_title, txt_body, txt_caption |
| `btn_` | Clickable buttons | btn_tab1, btn_submit, btn_next |
| `opt_` | Quiz options | opt_1, opt_2, opt_3, opt_4 |
| `card_` | Content cards | card_step1, card_stat_revenue |
| `icon_` | Visual indicators | icon_check, icon_arrow |
| `zone_` | Drop zones | zone_category1, zone_target |
| `item_` | Draggable items | item_concept1, item_term2 |
| `num_` | Number indicators | num_step1, num_score |
| `svg_` | SVG concept visuals | svg_diagram, svg_metaphor |
| `img_` | Generated images | img_hero, img_concept |
| `grp_` | Shape groups | grp_process_flow, grp_timeline |
| `line_` | Connecting lines | line_arrow, line_connector |

## Hidden TOC Title

Every slide MUST have an off-screen textbox named `title` containing the Arabic slide title. This prevents "Untitled Slide" in Storyline's sidebar.

- Position: x=-2", y=0" (off-screen to the right in RTL)
- Size: 1" x 0.3"

## Import Instructions

The title slide's speaker notes must include:

```
=== STORYLINE IMPORT INSTRUCTIONS ===

1. Open Storyline 360 → New Project → Import PowerPoint
2. Select this PPTX file
3. Story Size: 1280 x 720 px
4. After import:
   a. Install fonts: Tajawal (all weights from Google Fonts)
   b. Verify RTL: Text should be right-aligned
   c. Check shape names in Timeline panel
   d. Set up triggers following the blueprint in each slide's notes

Font Requirements: Tajawal Regular (400), Bold (700), ExtraBold (800)

QA Checklist:
□ All text is right-aligned (RTL)
□ Shape names match blueprint specifications
□ Fonts render correctly (Tajawal installed)
□ All layers created per blueprint
□ Quiz scoring variables initialized
□ Audio files linked to narration scripts
```

## Audio Narration

The `NARRATOR SCRIPT` section is the **exact text** to be recorded as audio. Rules:
- Written in formal academic Arabic
- No tashkeel/diacritics
- Each slide's narration = 15-30 seconds
- Reference the slide content ("كما ترون في الرسم البياني...")
- Pacing cues in brackets: [وقفة قصيرة], [تأكيد], [انتقال]
