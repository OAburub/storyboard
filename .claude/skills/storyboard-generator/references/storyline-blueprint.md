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

Our PPTX must make this developer's job as easy as possible.

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

```
=== STORYLINE BLUEPRINT ===

Slide Type: static-content
Duration: learner-paced
Audio: narration_s[XX].mp3

Layers:
- base (default visible)

Triggers:
1. Play media 'narration_s[XX]' when timeline starts

=== NARRATOR SCRIPT ===
[Arabic narration text]
```

### Click-to-Reveal (Tabs / Hotspots)

```
=== STORYLINE BLUEPRINT ===

Slide Type: click-reveal
Duration: learner-paced
Audio: narration_s[XX].mp3

Layers:
- base (default visible) — contains tab buttons
- detail_1: [content description for tab 1]
- detail_2: [content description for tab 2]
- detail_3: [content description for tab 3]
- completion: "أحسنت! لقد استكشفت جميع المحتوى" (shown when all tabs visited)

States:
- btn_tab1: [Normal, Hover, Visited]
- btn_tab2: [Normal, Hover, Visited]
- btn_tab3: [Normal, Hover, Visited]

Triggers:
1. Show layer 'detail_1' when user clicks 'btn_tab1'
   - Set state of 'btn_tab1' to 'Visited'
   - Add 1 to 'clickCount'
2. Show layer 'detail_2' when user clicks 'btn_tab2'
   - Set state of 'btn_tab2' to 'Visited'
   - Add 1 to 'clickCount'
3. Show layer 'detail_3' when user clicks 'btn_tab3'
   - Set state of 'btn_tab3' to 'Visited'
   - Add 1 to 'clickCount'
4. Show layer 'completion' when 'clickCount' >= 3

Variables:
- clickCount (Number, default 0): tracks revealed tabs

=== NARRATOR SCRIPT ===
[Arabic narration — "اضغط على كل علامة تبويب لاستكشاف المحتوى"]
```

### Quiz (Multiple Choice)

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

```
=== STORYLINE BLUEPRINT ===

Slide Type: drag-drop
Duration: learner-paced
Audio: narration_s[XX].mp3

Layers:
- base (default visible) — drag items + drop zones
- feedback_correct: "أحسنت! ترتيب صحيح"
- feedback_incorrect: "حاول مرة أخرى — راجع الترتيب"

States:
- item_1: [Normal, Drop Correct, Drop Incorrect]
- item_2: [Normal, Drop Correct, Drop Incorrect]
- zone_1: [Normal, Hover, Accepted]
- zone_2: [Normal, Hover, Accepted]

Triggers:
1. Set state of 'zone_[N]' to 'Accepted' when correct item dropped
2. Set state of 'item_[N]' to 'Drop Correct' when dropped on correct zone
3. Set state of 'item_[N]' to 'Drop Incorrect' and return to start when dropped on wrong zone
4. Show 'feedback_correct' when all items correctly placed
5. Allow 3 attempts before showing correct answers

Drag Mapping:
- item_1 → zone_[target]: [explanation]
- item_2 → zone_[target]: [explanation]

Variables:
- dragAttempts (Number, default 0): total attempts
- correctPlacements (Number, default 0): items correctly placed

=== NARRATOR SCRIPT ===
[Arabic instruction — "اسحب كل عنصر إلى المكان المناسب"]
```

### Branching Scenario

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

```
=== STORYLINE BLUEPRINT ===

Slide Type: slider
Duration: learner-paced

Layers:
- base (default visible) — slider + dynamic feedback area

Triggers:
1. Update 'txt_feedback' text based on 'sliderValue' ranges:
   - 0-3: [low range feedback in Arabic]
   - 4-7: [mid range feedback in Arabic]
   - 8-10: [high range feedback in Arabic]

Variables:
- sliderValue (Number, default 5): current slider position
```

## Shape Naming Convention

Every shape in the PPTX MUST be named meaningfully. The Storyline developer uses these names to set up triggers without renaming 50 objects per slide.

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
- Content: Arabic title for Storyline's navigation panel

## Import Instructions

The title slide's speaker notes must include Storyline import instructions:

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

Font Requirements:
- Tajawal Regular (400)
- Tajawal Bold (700)
- Tajawal ExtraBold (800)

QA Checklist:
□ All text is right-aligned (RTL)
□ Shape names match blueprint specifications
□ Fonts render correctly (Tajawal installed)
□ Section tags visible in header zone
□ Progress dots update per section
□ All layers created per blueprint
□ Quiz scoring variables initialized
□ Audio files linked to narration scripts
```

## Audio Narration

The `NARRATOR SCRIPT` section in each slide's notes is the **exact text** to be recorded as audio. Rules:
- Written in formal academic Arabic
- No tashkeel/diacritics (the narrator reads naturally)
- Each slide's narration = 15-30 seconds
- Reference the slide content ("كما ترون في الرسم البياني...")
- Pacing cues in brackets: [وقفة قصيرة], [تأكيد], [انتقال]
