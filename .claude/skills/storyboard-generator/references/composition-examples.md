# Composition Examples — Creative Design Thinking

How the agent should REASON about visual composition — not just which API to call, but HOW to think about what makes a slide sequence effective for the learner.

These examples show the agent's **inner monologue**: the creative decisions, trade-offs, and visual reasoning that separate a professional lecture from a template dump.

## How to Use This Reference

Read this BEFORE building any PPTX lecture. These are not templates to copy — they are **thinking patterns** to internalize. Each example shows:

1. **The scenario** — what kind of content the agent is working with
2. **The agent's reasoning** — inner monologue about visual choices
3. **The visual plan** — a composition table (the artifact presented to the user)
4. **Key method calls** — illustrative code showing pattern selection
5. **Why it works** — the learning science behind the choices
6. **What would be WRONG** — the lazy/mechanical approach and why it fails

After reading these, you should be able to reason about ANY content the same way.

---

## Example 1: Process-Heavy Content

### The Scenario

Content: **"مراحل التفكير التصميمي"** (Design Thinking Stages)
The raw content describes 5 stages of design thinking (Empathize, Define, Ideate, Prototype, Test) with details on each stage, a case study, and practical tips. This is a section within a larger lecture on innovation.

### The Agent's Reasoning (inner monologue)

> "I have 5 sequential stages — that is a process_flow. But wait. If I just drop all 5 into one process_flow slide, I get a dense, forgettable slide that looks like every other corporate presentation.
>
> Let me think about what serves the LEARNER:
>
> - The learner needs to REMEMBER the sequence — a visual pipeline metaphor would make it stick. I will use SVG to show the 5 stages as a pipeline flowing right-to-left, with each chamber containing an icon. This becomes the 'mental model' slide.
> - But the learner ALSO needs depth on each stage — I cannot cram that into one SVG. I will follow the overview with a content slide that gives details on 2-3 key stages using cards.
> - After two dense slides, the learner needs to BREATHE — a quote from a design thinking practitioner will create a pause and reinforce the 'why.'
> - Then I will TEST understanding — a drag-drop where the learner orders the stages. This checks if the pipeline metaphor stuck.
> - Finally, a SCENARIO — apply design thinking to a real situation. This moves from Remember to Apply on Bloom's.
>
> The narrative arc: Hook (stat about companies using design thinking) → Build (pipeline + details) → Breathe (quote) → Practice (drag-drop + scenario)."

### Visual Composition Plan

| # | Title | Act | Pattern | SVG? | AI Image? | Image Prompt | Why This Visual |
|---|-------|-----|---------|------|-----------|--------------|-----------------|
| 1 | 85% من الشركات الرائدة... | Hook | stat_cards | No | No | — | Numbers grab attention — no image needed |
| 2 | مراحل التفكير التصميمي | Build | process_flow | Yes: pipeline metaphor | No | — | SVG pipeline makes sequence memorable |
| 3 | التعاطف والتعريف: الأساس | Build | content_with_cards | No | Yes | "designer interviewing users in modern workspace, flat vector" | Cards for two related sub-concepts + image adds real-world context |
| 4 | — | Build | quote_highlight | No | No | — | Breathing slide after 2 dense slides |
| 5 | رتّب المراحل بالترتيب الصحيح | Practice | drag_drop | No | No | — | Interaction IS the visual — tests sequence recall |
| 6 | سيناريو: تطبيق التفكير التصميمي | Practice | scenario | No | Yes | "team brainstorming around whiteboard with sticky notes, flat vector" | Real-world context for decision-making |

### Key Method Calls

```python
# HOOK: Numbers ARE the visual
builder.add_stat_cards(title="لماذا التفكير التصميمي؟", stats=[
    {"number": "85%", "label": "من الشركات الرائدة تستخدمه", "trend": "up"},
    {"number": "3x", "label": "تحسين في رضا المستخدم", "trend": "up"},
    {"number": "60%", "label": "تقليل وقت التطوير", "trend": "down"},
], notes="...")

# BUILD: SVG pipeline — the mental model slide
builder.add_process_flow(title="مراحل التفكير التصميمي الخمس", steps=[
    {"num": 1, "label": "التعاطف", "desc": "فهم احتياجات المستخدم"},
    {"num": 2, "label": "التعريف", "desc": "تحديد المشكلة بدقة"},
    {"num": 3, "label": "التصور", "desc": "توليد الأفكار الإبداعية"},
    {"num": 4, "label": "النمذجة", "desc": "بناء نماذج أولية سريعة"},
    {"num": 5, "label": "الاختبار", "desc": "التحقق مع المستخدمين"},
], use_svg=True, notes="...")  # SVG pipeline metaphor

# BUILD: Cards for depth on key stages
builder.add_content_with_cards(title="التعاطف والتعريف: أساس التفكير التصميمي", cards=[
    {"title": "التعاطف", "body": "المقابلات الميدانية والملاحظة المباشرة...", "image_prompt": "designer interviewing users..."},
    {"title": "التعريف", "body": "تحليل البيانات وصياغة بيان المشكلة...", "image_prompt": "person organizing sticky notes..."},
], notes="...")

# BREATHE → PRACTICE: quote_highlight → drag_drop → scenario
```

### Why This Works

1. **The hook uses numbers, not words.** "85% of leading companies" is more compelling than "Design thinking is important." The stat_cards pattern makes numbers the visual — no image needed.
2. **The SVG pipeline creates a mental model.** A visual pipeline metaphor is something the learner can "see" in their mind later. A bullet list of 5 stages would be forgotten in minutes.
3. **Cards break dense content into scannable chunks.** Two stages per card with concept-specific images gives depth without overwhelm.
4. **The quote provides a breathing moment.** After 2 dense slides, the learner needs a pause.
5. **The drag-drop tests the pipeline.** If the SVG pipeline metaphor worked, the learner should recall the sequence.
6. **The scenario moves up Bloom's.** Ordering stages tests Remember. Choosing the right first step tests Apply.

### What Would Be WRONG

```
Slide 1: content_slide with bullets listing all 5 stages
Slide 2-5: content_slide with bullets about each stage
Slide 6: quiz asking "what is the first stage?"
```

**Why this fails:** Five consecutive content slides with bullets — no visual variety, no breathing, no engagement. No visual metaphor — the learner has no mental model. Same pattern repeated 5 times violates the variety rule. Quiz tests trivial recall instead of understanding.

---

## Example 2: Concept-Heavy Content

### The Scenario

Content: **"ركائز محو الأمية الرقمية"** (Digital Literacy Pillars)
The content describes 5 interconnected pillars of digital literacy: Information Literacy, Communication, Content Creation, Safety, and Problem Solving. Each pillar has 3-4 sub-skills. The pillars work together as a system — they are not independent items.

### The Agent's Reasoning (inner monologue)

> "I have 5 abstract pillars that form a system. My first instinct is icon_grid — 5 items, each with a label and description. But wait — icon_grid treats items as INDEPENDENT. These pillars are interconnected and build on each other. The word 'pillars' itself is a visual metaphor.
>
> A better approach:
>
> - First, I will HOOK with stat cards showing why digital literacy matters (concrete numbers before abstract concepts).
> - Then, I will use an SVG concept_visual with a BUILDING metaphor — 5 pillars holding up a roof labeled 'محو الأمية الرقمية'. This makes the abstract concept tangible and shows the pillars as structural supports, not just a list.
> - Then I will zoom into the details using a click_reveal interaction — the learner explores each pillar's sub-skills at their own pace. This is BETTER than 5 separate content slides because it keeps the learner in control.
> - After the exploration, a content_slide with an AI image showing someone demonstrating digital literacy in practice — connecting the abstract pillars to a real-world scene.
> - Finally, a quiz that tests understanding of the pillar RELATIONSHIPS, not just recall of names.
>
> The key insight: the BUILDING metaphor is the entire teaching strategy. If the learner 'sees' the pillars as structural supports, they understand that removing one weakens the whole structure."

### Visual Composition Plan

| # | Title | Act | Pattern | SVG? | AI Image? | Image Prompt | Why This Visual |
|---|-------|-----|---------|------|-----------|--------------|-----------------|
| 1 | 67% من البالغين... | Hook | stat_cards | No | No | — | Real-world urgency before abstract concept |
| 2 | ركائز محو الأمية الرقمية | Build | concept_visual | Yes: building with 5 pillars | No | — | Metaphor makes abstract concept tangible |
| 3 | استكشف كل ركيزة | Build | click_reveal | No | No | — | Learner-paced exploration of depth |
| 4 | محو الأمية الرقمية في الممارسة | Build | content_slide | No | Yes | "professional using multiple digital tools confidently, flat vector" | Connects abstract concept to real life |
| 5 | اختبر فهمك | Practice | quiz | No | No | — | Tests relationship understanding |

### Key Method Calls

```python
# HOOK: Numbers first, abstract concepts second
builder.add_stat_cards(title="لماذا محو الأمية الرقمية؟", stats=[
    {"number": "67%", "label": "من البالغين يفتقرون لمهارات رقمية أساسية", "trend": "down"},
    {"number": "90%", "label": "من الوظائف تتطلب مهارات رقمية", "trend": "up"},
], notes="...")

# BUILD: SVG building metaphor — the anchor visual
builder.add_concept_visual(title="الركائز الخمس لمحو الأمية الرقمية",
    visual_type="process_flow", data=[...],
    use_svg=True,  # SVG building metaphor — 5 pillars supporting a structure
    notes="...")

# BUILD: Click-reveal respects learner autonomy
builder.add_click_reveal_slide(title="استكشف كل ركيزة بالتفصيل",
    instruction="انقر على كل ركيزة لاكتشاف مهاراتها الفرعية",
    reveal_items=[
        {"label": "المعلومات", "description": "تشمل مهارات البحث الفعّال..."},
        {"label": "التواصل", "description": "تشمل المشاركة الفعّالة..."},
        # ... 3 more pillars
    ], notes="...")

# BUILD: Real-world connection → PRACTICE: Quiz testing RELATIONSHIPS
builder.add_quiz_slide(
    question="إذا أتقن شخص جميع ركائز محو الأمية الرقمية ما عدا 'الأمان'، ماذا يحدث؟",
    options=["لا يتأثر أداؤه...", "يصبح عرضة للمخاطر الرقمية...", "يحتاج فقط لبرنامج حماية...", "يمكنه الاعتماد على ركيزة حل المشكلات..."],
    correct_index=1, notes="...")
```

### Why This Works

1. **The building metaphor IS the teaching.** By showing pillars as structural supports, the learner intuitively understands that each one is necessary. This is not decoration — it is the pedagogical strategy.
2. **Click-reveal respects learner autonomy.** Instead of force-feeding 5 slides of details, the learner explores at their own pace.
3. **The quiz tests the METAPHOR, not the list.** "What happens if you remove one pillar?" directly tests whether the building metaphor worked. A lazy quiz would ask "How many pillars are there?"
4. **Content slide bridges abstract to concrete.** After conceptual exploration, a real-world image grounds the idea.
5. **Visual variety across 5 slides:** stat_cards → concept_visual(SVG) → click_reveal → content_slide → quiz. Five different patterns, zero repetition.

### What Would Be WRONG

```
Slide 1: icon_grid with 5 items (one per pillar)
Slides 2-6: content_slide with bullets about each pillar
Slide 7: quiz: "How many pillars of digital literacy are there?"
```

**Why this fails:** icon_grid treats the pillars as independent items — misses the interconnection. Five consecutive content_slides with bullets — massive pacing violation. No visual metaphor. The quiz tests trivial recall ("count to 5") instead of conceptual understanding. No click-reveal or learner control.

---

## Example 3: Data-Heavy Content

### The Scenario

Content: **"إحصائيات الإنترنت العالمية وتطورها"** (Global Internet Statistics and Evolution)
The content contains key internet adoption numbers, a historical timeline, a comparison of internet access across regions, and emerging trends. Heavy on data, light on concepts.

### The Agent's Reasoning (inner monologue)

> "This is mostly numbers and data. The trap is to dump all statistics into one giant table or a series of bullet slides. Instead, I need to make numbers TELL A STORY.
>
> - The HOOK should be the most surprising numbers — stat_cards are perfect because numbers ARE the visual.
> - Then I will use a TIMELINE for the historical evolution — this shows how we got here. Milestones with dates create a sense of journey.
> - The COMPARISON of regions is a natural fit for the comparison pattern — side by side columns showing the digital divide.
> - For the 'emerging trends' section, I will use content_with_cards because trends are distinct items that benefit from card formatting with per-card images.
> - Finally, a SCENARIO interaction — given these statistics, what decision would you make? This pushes from passive data consumption to active analysis.
>
> The narrative arc here is: SURPRISE (stats) → JOURNEY (timeline) → CONTRAST (comparison) → FUTURE (trends + scenario). The data tells a story of growth, inequality, and opportunity."

### Visual Composition Plan

| # | Title | Act | Pattern | SVG? | AI Image? | Image Prompt | Why This Visual |
|---|-------|-----|---------|------|-----------|--------------|-----------------|
| 1 | أرقام مذهلة عن الإنترنت | Hook | stat_cards | No | No | — | Numbers are the hook — let them speak |
| 2 | رحلة الإنترنت عبر العقود | Build | timeline | No | No | — | Timeline shows the journey |
| 3 | — | Build | quote_highlight | No | No | — | Breathing slide between dense data |
| 4 | الفجوة الرقمية بين المناطق | Build | comparison | No | No | — | Side-by-side makes inequality visible |
| 5 | الاتجاهات الناشئة | Build | content_with_cards | No | Yes (per card) | concept-specific per card | Cards + images show what trends look like |
| 6 | سيناريو: قرار استراتيجي | Practice | scenario | No | Yes | "executive looking at data dashboard, flat vector" | Data analysis in action |

### Key Method Calls

```python
# HOOK: Most surprising numbers
builder.add_stat_cards(title="الإنترنت اليوم — أرقام مذهلة", stats=[
    {"number": "5.4B", "label": "مستخدم إنترنت حول العالم", "trend": "up"},
    {"number": "92%", "label": "يتصفحون عبر الهاتف المحمول", "trend": "up"},
    {"number": "2.5 ساعة", "label": "متوسط الاستخدام اليومي لوسائل التواصل", "trend": "up"},
], notes="...")

# BUILD: Timeline showing the journey
builder.add_timeline(title="رحلة الإنترنت — من الفكرة إلى العالمية", milestones=[
    {"year": "1969", "title": "أربانت", "desc": "أول شبكة حاسوبية بين أربع جامعات", "status": "done"},
    {"year": "1991", "title": "الويب العالمي", "desc": "تيم بيرنرز لي يطلق شبكة الويب", "status": "done"},
    {"year": "2024", "title": "الذكاء التوليدي", "desc": "نماذج لغوية تعيد تشكيل التفاعل الرقمي", "status": "active"},
], notes="...")

# BREATHE → BUILD: quote_highlight → comparison → content_with_cards
# PRACTICE: Scenario demanding data-driven reasoning
builder.add_scenario_slide(title="سيناريو: قرار استراتيجي",
    situation="أنت مسؤول التحول الرقمي في شركة سعودية. بناءً على إحصائيات الإنترنت — 92% يتصفحون عبر المحمول والفجوة الرقمية بين المناطق — ما هي أولويتك الاستراتيجية؟",
    choices=["بناء تطبيق ويب متطور يعمل فقط على الحواسيب المكتبية", "تطوير تطبيق محمول أولاً مع دعم للمناطق ذات الاتصال المحدود", "الانتظار حتى تتحسن البنية التحتية في جميع المناطق"],
    correct_index=1, notes="...")
```

### Why This Works

1. **Data tells a story, not a dump.** The sequence Surprise → Journey → Contrast → Future transforms raw statistics into a narrative. Each pattern is chosen for the RELATIONSHIP it expresses.
2. **The timeline creates a sense of journey.** Instead of bullets, the timeline visually places the learner ON the journey. The "active" status on 2024 says "you are HERE."
3. **Comparison makes inequality VISIBLE.** Side-by-side columns with specific numbers make the digital divide undeniable.
4. **Cards with concept-specific images for trends.** Each trend card has an AI image showing WHAT that trend looks like — not a generic technology image.
5. **The scenario demands data-driven reasoning.** The learner must connect statistics to a strategic decision. This is Bloom's Apply/Analyze.
6. **Breathing quote between dense data.** After timeline (dense) and before comparison (dense), the quote gives the mind a moment to process.

### What Would Be WRONG

```
Slides 1-4: content_slide with bullet lists of statistics, milestones, regional differences, trends
Slide 5: quiz: "How many internet users are there globally?"
```

**Why this fails:** All data crammed into bullet lists — no visual differentiation between types of data. Timeline as bullets loses the sense of journey. No breathing slides. Quiz tests trivial number recall instead of data-driven reasoning. Every slide uses the same pattern.

---

## Anti-Patterns Summary

| Anti-Pattern | Problem | Fix |
|---|---|---|
| **Bullet Machine** | Same `content_slide` pattern repeated — no visual variety | Ask "What relationship does this content express?" and pick the matching pattern |
| **Generic Image** | Vague prompts like "technology background" — adds nothing to learning | Write concept-specific prompts: "layered security shields protecting a central data core..." |
| **Skipping Breathing** | 3+ dense slides without breaks — cognitive overload | After every 2 dense slides, insert a quote_highlight, section_divider, or interaction |
| **Trivial Quiz** | Tests number recall ("How many users?") instead of understanding | Test application: "Given that 92% access via mobile, what should a new service prioritize?" |
