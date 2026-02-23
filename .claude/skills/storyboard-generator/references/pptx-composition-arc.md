# PPTX Composition & Engagement Design

Art direction guide for composing full interactive lectures. Read before building any PPTX lecture.
Use alongside `visual-grammar.md` and `pptx-design-system.md`.

---

## Part 1: Pre-Build Planning (REQUIRED)

Before building ANY slide, create a Visual Composition Plan. Present it to the user for approval BEFORE calling any engine builder.

### Step 1: Map Content to Slides

List every topic from the content analysis. For each topic:
- How many slides does this topic need? (1 concept = 1 slide)
- Where does it sit in the 5-act narrative arc? (Hook / Build / Insight / Practice / Summary)
- What type of slide? (structural, content, interaction, breathing)

### Step 2: Visual Composition Table

For EACH slide, fill in this table:

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
```

### Step 3: Visual Tool Palette — Learner-First Decisions

For EACH content slide, ask these questions in order:

**Q1: "Would a concept visualization make this idea tangible?"**
- Yes → Plan an SVG concept visualization (`use_svg=True`)
- Use SVG whenever a visual metaphor makes the concept easier to understand — not just for complex diagrams

**Q2: "Would a real-world illustration add context?"**
- Yes → Plan an AI image (`image_prompt`)
- Prompts must be specific, not generic stock photos

**Q3: "Is the layout pattern itself sufficient?"**
- Yes → Native PPTX only — stat cards, timelines, comparisons carry their own visual weight

A slide CAN have both SVG + AI Image when the concept benefits from both.

### Step 4: SVG Concept Descriptions

For each SVG slide, write a one-line visualization concept:

```
Slide 4: "Five pillars as an architectural building — each pillar labeled, connected by a roof labeled 'محو الأمية الرقمية'"
Slide 5: "Pipeline flowing right-to-left with 4 connected chambers, each containing a stage icon and label"
Slide 8: "Three concentric shield layers — outer=physical, middle=technical, inner=human, each with icons"
```

### Step 5: Image Prompts

For each AI Image slide, draft the English prompt and image_type:

```
Slide 1: prompt="modern university campus with digital holographic displays, flat vector style" | type=content
Slide 6: prompt="student applying design thinking on tablet with sticky notes, flat vector" | type=two_column
Slide 9: prompt="student thinking at computer screen with question marks, flat vector" | type=quiz
```

Target density: **8-12 images per lecture** (see `image-gen.md`).

### Step 6: Pacing & Density Check

Before presenting the plan, verify:
- [ ] No 3+ dense slides in a row (insert breathing slide: quote_highlight, section_divider)
- [ ] No same visual pattern on 2 consecutive slides
- [ ] Section divider every 4-6 content slides
- [ ] Interaction slide every 3-4 content slides
- [ ] SVG visuals: 4-8 per lecture
- [ ] AI images: 8-12 per lecture
- [ ] Total: 25-30 slides (if more, split into two lectures)
- [ ] Narrative arc complete: Hook(1-2) → Build(3-5) → Insight(1) → Practice(2-3) → Summary(1-2)

Before building, study creative composition examples at `references/composition-examples.md`.

---

## Part 2: Narrative Arc

Every lecture follows a 5-act structure. Plan the full arc BEFORE building any slides.

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
  Patterns: quiz, drag-drop, click-reveal, scenario.
  Rule: Interactions should test UNDERSTANDING, not just recall.

ACT 5: SUMMARY (1-2 slides)
  Purpose: Reinforce learning. Provide a visual recap.
  Patterns: icon_grid (key concepts), process_flow (recap steps), summary slide.
  Rule: Use a DIFFERENT pattern than what was used in the build act.
```

---

## Part 3: Motivation Arc

The narrative arc tells you WHAT to cover. The motivation arc tells you HOW learners should FEEL.
Design for emotional journey, not just information delivery.

```
WRONG: Title → Objectives → Slides 3-15 (content) → Summary  ← passive, forgettable
RIGHT: "What question will haunt the learner until they find the answer?"
       → Build toward insight through curiosity, challenge, and discovery
```

```
ENGAGEMENT
  ^
  |      IGNITE              TRIUMPH
  |     /  (curiosity         /  (mastery
  |    /    peaks)           /    moment)
  |   /                    /
  |  /   STRUGGLE         /     LAUNCH
  | /   /  (productive   /     / (transfer)
  |/   /    difficulty) /     /
  | HOOK              _/     /
  |  (grab)                 /
  +---------------------------→ LECTURE PROGRESS
  Sl.1-3  Sl.4-7  Sl.8-15  Sl.16-20  Sl.21-25
```

### Phase 1: HOOK (Slides 1-3)
**Goal:** Create an information gap. Make the learner NEED to know.

| Pattern | Example | Visual Method |
|---------|---------|--------------|
| Surprising statistic | "73% of managers make this mistake daily" | `stat_cards` with bold number |
| Provocative question | "What would you do if this happened to your team?" | `content_slide` with large question |
| Real scenario | "Last month, Company X lost $2M because..." | `content_with_cards` |
| Myth-buster | "Everything you know about leadership is wrong" | `quote_highlight` |
| Visual puzzle | Show complex diagram — "By the end, you'll understand this" | `concept_visual` or SVG |

**What NOT to do:** "Welcome to Unit 3: Risk Management Procedures" — this hooks nobody.

### Phase 2: IGNITE (Slides 4-7)
**Goal:** Build foundational understanding. Curiosity deepens as gaps expand.

| Pattern | Purpose | Visual Method |
|---------|---------|--------------|
| Concept + Example | Make abstract tangible | `two_column` |
| Visual metaphor | Connect new to known | SVG or AI image |
| Micro-check | Low-stakes thinking prompt | `quiz` (ungraded) |
| Analogy bridge | "Think of it like..." | `content_with_cards` |

### Phase 3: STRUGGLE (Slides 8-15)
**Goal:** Productive difficulty. This is where real learning happens.

| Pattern | Purpose | Visual Method |
|---------|---------|--------------|
| Scenario decision | Apply knowledge under pressure | `scenario` |
| Process application | Practice a procedure | `process_flow` |
| Comparison challenge | Distinguish similar concepts | `comparison` |
| Error analysis | "What went wrong here?" | `content_slide` with flawed example |
| Drag-and-drop | Categorize, sequence, or match | `drag_drop` |

**CRITICAL:** Never go more than 3-4 content slides without an interaction. Include hints in Storyline notes — don't let struggle become frustration.

### Phase 4: TRIUMPH (Slides 16-20)
**Goal:** The mastery moment. Learner demonstrates competence.

| Pattern | Purpose | Visual Method |
|---------|---------|--------------|
| Culminating scenario | Integrate everything learned | `scenario` with branching |
| Before/after | Show how much they've learned | `comparison` |
| Expert-level question | Highest Bloom's level | `quiz` at Evaluate/Analyze |
| "Now YOU explain" | Teach-back prompt | `content_slide` with reflection |

### Phase 5: LAUNCH (Slides 21-25)
**Goal:** Transfer to real world. Anticipation for next unit.

| Pattern | Purpose | Visual Method |
|---------|---------|--------------|
| Visual summary | Map of everything learned | `icon_grid` or SVG knowledge map |
| Transfer prompt | "Try this at work tomorrow..." | `content_slide` with action items |
| Next preview | Open a new information gap | Tease next unit |
| Celebration | Acknowledge achievement | `closing` |

---

## Part 4: Pre-Build Design Questions

Answer these five questions before composing any lecture:

### Q1: What should the learner FEEL?

| Aesthetic | When to Choose | Design Implication |
|-----------|---------------|-------------------|
| Challenge | Skills training, procedures | Progressive difficulty, practice interactions |
| Discovery | Exploring new concepts | Revealing slides, "what if" prompts, branching |
| Narrative | Case studies, real-world | Story arc, characters, consequences |
| Sensation | When visual impact reinforces learning | Premium design, SVG metaphors |
| Expression | Creative/leadership topics | Open-ended prompts, reflection |

### Q2: What's the learner's motivation level?

| Level | What It Sounds Like | Design Response |
|-------|---------------------|-----------------|
| Amotivated | "I don't care about this" | STRONG hook. Lead with real-world consequences. |
| External | "My boss told me to take this" | Acknowledge reality. Make it painless. Quick wins. |
| Identified | "I know this is important" | Build on motivation. Give depth and challenge. |
| Intrinsic | "I want to learn this" | Get out of the way. Provide depth, not hand-holding. |

### Q3: What RAMP balance fits this content?

| Content Type | R (Relatedness) | A (Autonomy) | M (Mastery) | P (Purpose) |
|-------------|----------------|--------------|-------------|-------------|
| Compliance | 20% | 10% | 30% | 40% |
| Technical skill | 10% | 25% | 45% | 20% |
| Soft skill | 30% | 25% | 20% | 25% |
| Academic | 10% | 30% | 35% | 25% |

### Q4: Where are the "Why This Matters" moments?
Plan at least ONE relevance block per section: connect to actual job/life, show real consequences, reference people they care about.

### Q5: Where is the culminating challenge?
Every lecture needs ONE moment where the learner proves mastery without scaffolding. Plan this FIRST.

---

## Part 5: Pacing Rules

### The 3-4 Slide Rule
**Never go more than 3-4 content slides without an interaction.**

After 3-4 content slides, insert one of: `quiz`, `click_reveal`, `drag_drop`, `scenario`, `slider`, or a reflection prompt.

### The Breathing Rule
Never place 3+ dense information slides in a row. After 2 dense slides, insert a breathing slide.

**Dense slides**: content slides with 4+ bullets, comparison, process_flow with 5+ steps, icon_grid.
**Breathing slides**: `quote_highlight`, `section_divider`, `stat_cards` (2-3 stats), image-only slides.

```
GOOD:  [content] → [process_flow] → [quote_highlight] → [comparison] → [quiz]
BAD:   [content] → [process_flow] → [comparison] → [icon_grid] → [content]
```

### The Variety Rule
Never use the same visual pattern on two consecutive slides.

### The Section Rule
Insert a `section_divider` every 4-6 content slides.

```
[title] → [objectives] → [DIVIDER: Section 1] → [4-5 slides] → [DIVIDER: Section 2] → ...
```

### Cognitive Load Management

| Signal | Problem | Solution |
|--------|---------|----------|
| Dense text slide | Overload | Split into 2-3 simpler slides |
| Complex diagram | Processing strain | Build progressively (reveal parts) |
| 3+ concepts per slide | Working memory limit | One concept per slide |
| 5+ content slides in a row | Attention fatigue | Insert interaction or breathing slide |

### Slide Count

Target **25-30 slides** per lecture.

| Slide Type | Count | % |
|---|---|---|
| Structural (title, objectives, dividers, summary, closing) | 6-8 | ~25% |
| Content (visual grammar patterns) | 12-16 | ~50% |
| Interactions (quiz, drag-drop, click-reveal) | 4-6 | ~20% |
| Breathing (quotes, transitions) | 2-3 | ~5% |

If content requires more than 30 slides, split into two lectures.

---

## Part 6: Visual Tools

### SVG vs Native PPTX

Use **native PPTX shapes** when the layout pattern carries the visual meaning (stat cards show numbers, timelines show progression, comparisons show differences).

Use **SVG concept visualization** (`use_svg=True`) when a visual metaphor or diagram helps the learner understand. Includes: visual metaphors, architecture diagrams, relationship maps, circular flows, transformation pipelines, complex processes.

SVG is a **primary visualization tool**, not a last resort. Ask: "Would seeing this as a picture help the learner understand it faster?" If yes, use SVG.

**Note on Arabic text**: SVG text is rasterized to PNG. Keep labels short (1-3 words). Long Arabic text should be in native PPTX shapes alongside the SVG.

### 3-Tool Palette by Slide Type

| Slide Type | AI Image? | SVG Concept? | Why |
|---|---|---|---|
| Content slides | Yes (often) | Consider | Image illustrates; SVG if concept is abstract |
| Section dividers | Optional | No | Decorative mood-setting |
| Quiz slides | Optional | No | Visual stimulus for the question |
| Stat cards | No | No | Numbers ARE the visual |
| Process flows | No | Yes (if 5+ steps or metaphor helps) | SVG makes flow tangible |
| Quote highlights | No | No | Text IS the visual |
| Timelines | No | Consider | Timeline may benefit from illustrated milestones |
| Icon grids | No | Consider (if items form a system) | SVG if items are interconnected |
| Comparisons | No | Consider (if comparing systems) | SVG for visual side-by-side systems |
| Cycle diagrams | No | Yes (always) | Circular layouts need SVG |

### Visual Grammar + Engagement Effect

| Visual Pattern | Information Effect | Engagement Effect | Best For |
|---------------|-------------------|-------------------|----------|
| `process_flow` | Shows sequence | Clarity → Competence | Teaching procedures |
| `stat_cards` | Highlights numbers | Surprise → Curiosity | Hook slides, impact data |
| `quote_highlight` | Expert insight | Credibility → Relatedness | Expert voice, inspiration |
| `timeline` | Shows progression | Narrative → Story flow | History, project phases |
| `comparison` | Contrasts two things | Distinction → Understanding | Differentiating concepts |
| `icon_grid` | Organizes categories | Overview → Structure | Summarizing multiple items |
| `cycle_diagram` | Shows recurring process | System thinking → Depth | Feedback loops, cycles |
| `concept_visual` | SVG/AI visualization | "Aha!" → Discovery | Abstract concepts |

**Choose visual patterns that create EMOTIONAL connection, not just information clarity.**

---

## Part 7: SDT in PPTX Design

### Autonomy
| Technique | Storyline Implementation | Storyboard Notation |
|-----------|------------------------|-------------------|
| Choose your scenario | Branching slide with 2-3 options | "BRANCH: learner selects scenario A, B, or C" |
| Optional deep-dive | Hidden layer on click | "OPTIONAL: click 'Learn more' for extended content" |
| Self-paced review | No forced navigation timing | "NO auto-advance — learner controls pace" |
| Skip if you know | Pre-test gates content | "If pre-test score >80%, skip to Slide X" |

### Competence
| Slide Pattern | Competence Effect | When to Use |
|--------------|-------------------|-------------|
| `quiz` (easy) | "I already know something!" | Early (confidence builder) |
| `process_flow` | "I can see the steps clearly" | After teaching a procedure |
| `drag_drop` | "I can categorize this!" | After teaching classification |
| `scenario` (hard) | "I can handle complex situations!" | Near end (mastery proof) |

### Relatedness
| Technique | How to Design It |
|-----------|-----------------|
| Real scenarios | Use "you" and real workplace situations |
| Team framing | "Your team depends on..." or "When your colleague asks..." |
| Expert voice | Quote from industry expert |
| "What would you do?" | Invite reflection, not just correct-answer selection |
| Social proof | "87% of professionals in this field say..." |

---

## Part 8: Growth Mindset Feedback

### Quiz Feedback Language

| Situation | Growth Mindset (use) | Fixed Mindset (avoid) |
|-----------|---------------------|----------------------|
| Correct | "Your reasoning is solid. You identified [X] because [Y]." | "Correct!" |
| Correct on retry | "Persistence pays off! You adjusted your approach and found it." | "Finally correct." |
| Incorrect | "Not quite yet. The key insight is [X]. Try thinking about [Y]." | "Wrong. The answer is B." |
| Partial | "You're on the right track — you got [correct part]. Now consider [missing part]." | "Partially correct." |

### Instructional Language

| Purpose | Engagement Language | Avoid |
|---------|--------------------|-----------------------------|
| Introducing difficulty | "This next concept challenges even experts. Let's work through it." | "This is basic." |
| Transitions | "Now that you understand X, you're ready for the next level." | "Moving on to the next topic." |
| Effort acknowledgment | "Working through this shows real commitment to your growth." | "You should find this easy." |

---

## Part 9: Gagne's 9 Events — Engagement Enhancement

| Gagne's Event | Standard | Engagement-Enhanced |
|---------------|----------|---------------------|
| 1. Gain Attention | Show title slide | Information Gap: surprising stat, provocative question |
| 2. State Objectives | Bullet list | Frame as benefit: "After this, you'll be able to..." |
| 3. Recall Prior | "You may already know..." | Quick quiz activating prior knowledge |
| 4. Present Content | Slides with info | Visual metaphors, stories, progressive reveal |
| 5. Provide Guidance | Worked examples | "Think like an expert" — show expert reasoning |
| 6. Elicit Practice | Quiz at the end | Distributed practice (the 3-4 slide rule) |
| 7. Provide Feedback | "Correct/Incorrect" | Growth mindset: specific, encouraging, next-step |
| 8. Assess Performance | Final test | Culminating scenario integrating all concepts |
| 9. Enhance Retention | Summary bullets | Transfer prompt + visual summary + next-unit tease |

---

## Part 10: Information Gap Techniques

| Technique | How to Use | Slide Type |
|-----------|-----------|------------|
| Open with a question | "What causes 80% of workplace accidents?" | `content_slide` with large question |
| Show partial data | Reveal 3 of 5 factors, tease remaining 2 | `icon_grid` with hidden items |
| Myth-then-truth | State common belief, then reveal it's wrong | `comparison` (myth vs. reality) |
| Predict-then-reveal | "What do you think happens next?" | `click_reveal` |
| Cliffhanger | End section with unresolved question | `content_slide` before section divider |

**Curiosity rhythm:** Open gap → Build tension → Fill gap → Open NEW gap → repeat across the lecture.

---

## Part 11: Design Quality

### Whitespace
- **5% safe margin** from each slide edge — no content in the outer frame
- **Content zone** is 78% of the slide — leave header (10%) and footer (12%) zones clear
- **Card padding**: minimum 8pt inside, 16pt between cards
- If a slide feels crowded, split — never cram

### The Squint Test
Blur your eyes and look at the slide. If you can still see the visual hierarchy (title stands out, main content is distinct, secondary elements recede), it works. If everything blurs into a uniform mass, add contrast: bigger title, more whitespace, fewer elements.

### The PowerPoint Test
Does the slide look like generic corporate PowerPoint? Warning signs:
- All bullet points, no visual patterns
- Same layout on every slide
- No depth (no shadows, no background washes)
- Text filling the entire slide with no breathing room

If yes: add visual variety, add depth (background wash + shadows), add whitespace.

---

## Part 12: Combined Quality Checklist

### Narrative & Motivation (all must pass)
- [ ] Opening creates curiosity or urgency (not "Welcome to Unit X")
- [ ] 5-act narrative arc planned before building
- [ ] At least one "aha moment" designed into the lecture
- [ ] Culminating challenge near end where learner proves mastery without scaffolding
- [ ] Closing connects to real-world application AND teases next unit

### SDT Compliance (at least 4 of 6)
- [ ] Autonomy: At least one choice point or branching path
- [ ] Autonomy: Language is invitational, not controlling
- [ ] Competence: Difficulty increases progressively
- [ ] Competence: Feedback is specific and growth-oriented
- [ ] Relatedness: At least one real-world scenario from learner's context
- [ ] Relatedness: At least one "Why This Matters" block

### Pacing & Interactions (all must pass)
- [ ] No more than 3-4 content slides without an interaction
- [ ] At least 20% of slides are interactive
- [ ] No same visual pattern on consecutive slides
- [ ] Section divider every 4-6 content slides
- [ ] Visual variety: mix stat_cards, comparison, process_flow (not all content_slide)

### Visual Design (all must pass)
- [ ] Composition Table completed and approved before building
- [ ] 4-8 SVG visuals planned for abstract concepts
- [ ] 8-12 AI images for contextual illustration
- [ ] Squint Test passes: visual hierarchy clear at a glance
- [ ] No generic PowerPoint slide patterns

### Storyline Readiness
- [ ] Every slide has named shapes in speaker notes
- [ ] Interaction slides have full Storyline blueprints (layers, states, triggers, variables)
- [ ] A Storyline developer could build from notes without asking questions

---

## Sources

- Hunicke, R., LeBlanc, M., & Zubek, R. (2004). "MDA: A Formal Approach to Game Design."
- Deci, E. L. & Ryan, R. M. (2000). "Self-Determination Theory."
- Csikszentmihalyi, M. (1990). "Flow: The Psychology of Optimal Experience."
- Keller, J. (2010). "Motivational Design for Learning and Performance" (ARCS Model).
- Loewenstein, G. (1994). "The Psychology of Curiosity" (Information Gap Theory).
- Dweck, C. (2006). "Mindset: The New Psychology of Success."
- Gagne, R. (1985). "The Conditions of Learning."
- Marczewski, A. (2015). RAMP Framework. gamified.uk
