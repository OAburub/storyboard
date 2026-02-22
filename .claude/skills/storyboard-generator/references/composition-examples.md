# Composition Examples — Creative Design Thinking

How the agent should REASON about visual composition — not just which API to call, but HOW to think about what makes a slide sequence effective for the learner.

These examples show the agent's **inner monologue**: the creative decisions, trade-offs, and visual reasoning that separate a professional lecture from a template dump.

## How to Use This Reference

Read this BEFORE building any PPTX lecture. These are not templates to copy — they are **thinking patterns** to internalize. Each example shows:

1. **The scenario** — what kind of content the agent is working with
2. **The agent's reasoning** — inner monologue about visual choices
3. **The visual plan** — a composition table (the artifact presented to the user)
4. **The code** — actual Python calls with LectureBuilder
5. **Why it works** — the learning science behind the choices
6. **What would be WRONG** — the lazy/mechanical approach and why it fails

After reading these, you should be able to reason about ANY content the same way — not just the three types shown here.

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

### The Code

```python
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="INNOV", unit_number=2,
    unit_name="الابتكار والتفكير التصميمي",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
)

# --- HOOK: Surprising stat grabs attention ---
builder.add_stat_cards(
    title="لماذا التفكير التصميمي؟",
    stats=[
        {"number": "85%", "label": "من الشركات الرائدة تستخدمه", "trend": "up"},
        {"number": "3x", "label": "تحسين في رضا المستخدم", "trend": "up"},
        {"number": "60%", "label": "تقليل وقت التطوير", "trend": "down"},
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: stat_cards
Duration: auto-advance after 8s or click
Audio: INNOV_U02_slide01.mp3

Layers:
- base (default visible)

States:
- stat_card_1: [Normal, Hover] — scale up on hover
- stat_card_2: [Normal, Hover]
- stat_card_3: [Normal, Hover]

Triggers:
1. Change state of stat_card_1 to Hover when mouse hovers
2. Play animation entrance on each card sequentially (0.3s delay)

=== NARRATOR SCRIPT ===
هل تعلم أن 85 بالمئة من الشركات الرائدة عالمياً تعتمد على التفكير التصميمي في تطوير منتجاتها؟ دعونا نكتشف لماذا.""",
)

# --- BUILD: SVG pipeline — the mental model slide ---
builder.add_process_flow(
    title="مراحل التفكير التصميمي الخمس",
    steps=[
        {"num": 1, "label": "التعاطف", "desc": "فهم احتياجات المستخدم"},
        {"num": 2, "label": "التعريف", "desc": "تحديد المشكلة بدقة"},
        {"num": 3, "label": "التصور", "desc": "توليد الأفكار الإبداعية"},
        {"num": 4, "label": "النمذجة", "desc": "بناء نماذج أولية سريعة"},
        {"num": 5, "label": "الاختبار", "desc": "التحقق مع المستخدمين"},
    ],
    use_svg=True,  # SVG pipeline metaphor — makes stages tangible
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: process_flow (SVG)
Duration: learner-paced

Layers:
- base (default visible)
- detail_1 through detail_5: expanded description per stage

States:
- Each stage shape: [Normal, Hover, Selected]

Triggers:
1. Show layer detail_N when user clicks stage_N
2. Change state of stage_N to Selected when clicked
3. Hide other detail layers when new stage selected

Variables:
- stages_visited (Number, default 0): tracks exploration

Conditions:
- Enable Next button when stages_visited >= 3

=== NARRATOR SCRIPT ===
التفكير التصميمي يمر بخمس مراحل متكاملة. تبدأ بالتعاطف مع المستخدم، ثم تحديد المشكلة، ثم توليد الأفكار، ثم بناء النماذج الأولية، وأخيراً الاختبار والتحقق.""",
)

# --- BUILD: Details on key stages with cards ---
builder.add_content_with_cards(
    title="التعاطف والتعريف: أساس التفكير التصميمي",
    cards=[
        {
            "title": "التعاطف",
            "body": "المقابلات الميدانية والملاحظة المباشرة لفهم تجربة المستخدم الحقيقية",
            "image_prompt": "designer interviewing users in modern workspace, flat vector style",
        },
        {
            "title": "التعريف",
            "body": "تحليل البيانات وصياغة بيان المشكلة من منظور المستخدم",
            "image_prompt": "person organizing sticky notes on wall into categories, flat vector style",
        },
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: content_with_cards
Duration: learner-paced

Layers:
- base (default visible)

Triggers:
1. Play entrance animation on cards sequentially

=== NARRATOR SCRIPT ===
المرحلتان الأوليتان هما الأساس. في مرحلة التعاطف، نتعرف على المستخدم عن قرب من خلال المقابلات والملاحظة. ثم في مرحلة التعريف، نحول ما تعلمناه إلى بيان مشكلة واضح.""",
)

# --- BREATHE: Quote to pause and reflect ---
builder.add_quote_highlight(
    title="رؤية",
    quote="التصميم ليس فقط كيف يبدو الشيء — بل كيف يعمل",
    attribution="ستيف جوبز",
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: quote_highlight
Duration: auto-advance after 6s or click
Audio: INNOV_U02_slide04.mp3

Layers:
- base (default visible)

Triggers:
1. Play fade-in animation on quote text (0.5s)
2. Play fade-in on attribution (delay 1s)

=== NARRATOR SCRIPT ===
كما قال ستيف جوبز: التصميم ليس فقط كيف يبدو الشيء، بل كيف يعمل. وهذا هو جوهر التفكير التصميمي.""",
)

# --- PRACTICE: Drag-drop to test sequence recall ---
builder.add_drag_drop_slide(
    question="رتّب مراحل التفكير التصميمي بالترتيب الصحيح",
    items=["الاختبار", "التعاطف", "النمذجة", "التعريف", "التصور"],
    correct_order=["التعاطف", "التعريف", "التصور", "النمذجة", "الاختبار"],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: drag_drop (ordering)
Duration: learner-paced
Audio: none

Layers:
- base (default visible)
- feedback_correct: "أحسنت! ترتيب صحيح"
- feedback_incorrect: "حاول مرة أخرى — تذكر أن التعاطف يأتي أولاً"

States:
- Each drag item: [Normal, Drag Over, Drop Correct, Drop Incorrect]

Triggers:
1. Allow drag on all items
2. Submit button evaluates order
3. Show feedback_correct if order matches
4. Show feedback_incorrect if order wrong
5. Allow 2 attempts before showing correct answer

Variables:
- attempts (Number, default 0)
- score_drag1 (Number, default 0)

=== NARRATOR SCRIPT ===
حان وقت التطبيق! رتّب مراحل التفكير التصميمي الخمس بالترتيب الصحيح.""",
)

# --- PRACTICE: Scenario for application-level thinking ---
builder.add_scenario_slide(
    title="سيناريو: تطبيق التفكير التصميمي",
    situation="أنت مصمم تجربة مستخدم في شركة تقنية. تلقيت شكاوى متكررة من العملاء حول صعوبة التسجيل في التطبيق. ما هي الخطوة الأولى التي يجب اتخاذها؟",
    choices=[
        "إعادة تصميم صفحة التسجيل فوراً",
        "إجراء مقابلات مع المستخدمين لفهم المشكلة",
        "إضافة فيديو تعليمي لشرح التسجيل",
    ],
    correct_index=1,
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: scenario (branching)
Duration: learner-paced

Layers:
- base (default visible)
- feedback_choice_0: "إعادة التصميم دون فهم المشكلة قد يكرر نفس الأخطاء"
- feedback_choice_1: "صحيح! التعاطف هو الخطوة الأولى دائماً في التفكير التصميمي"
- feedback_choice_2: "الفيديو يعالج العَرَض وليس السبب — الأفضل فهم المشكلة أولاً"

Triggers:
1. Show feedback_choice_N when user clicks choice_N
2. Highlight correct choice after feedback shown
3. Enable Next when any choice is made

Variables:
- scenario_score (Number, default 0): +1 if correct

=== NARRATOR SCRIPT ===
لنختبر فهمك بسيناريو عملي. اقرأ الموقف واختر الخطوة الأنسب بناءً على مراحل التفكير التصميمي.""",
)
```

### Why This Works

1. **The hook uses numbers, not words.** "85% of leading companies" is more compelling than "Design thinking is important." The stat_cards pattern makes numbers the visual — no image needed.

2. **The SVG pipeline creates a mental model.** A visual pipeline metaphor is something the learner can "see" in their mind later. A bullet list of 5 stages would be forgotten in minutes.

3. **Cards break dense content into scannable chunks.** Two stages per card with concept-specific images gives depth without overwhelm. The images show real designers at work — not generic clip art.

4. **The quote provides a breathing moment.** After the pipeline overview + details (2 dense slides), the learner needs a pause. The quote reinforces the "why" of design thinking.

5. **The drag-drop tests the pipeline.** If the SVG pipeline metaphor worked, the learner should recall the sequence. This interaction directly validates whether the visual teaching succeeded.

6. **The scenario moves up Bloom's.** Ordering stages tests Remember. Choosing the right first step tests Apply. The feedback explains WHY each choice is right or wrong.

### What Would Be WRONG

The lazy approach:

```
Slide 1: content_slide with bullets listing all 5 stages
Slide 2: content_slide with bullets about stage 1 details
Slide 3: content_slide with bullets about stage 2 details
Slide 4: content_slide with bullets about stage 3 details
Slide 5: quiz asking "what is the first stage?"
```

**Why this fails:**
- Five consecutive content slides with bullets — no visual variety, no breathing, no engagement
- No visual metaphor — the learner has no mental model to anchor the sequence
- Same pattern (content_slide) used 4 times in a row — violates the variety rule
- Quiz tests trivial recall instead of understanding or application
- No pacing — dense slides with no breaks lead to cognitive overload
- Looks like a generic corporate PowerPoint, not a designed learning experience

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

### The Code

```python
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DLIT", unit_number=1,
    unit_name="محو الأمية الرقمية",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
)

# --- HOOK: Why digital literacy matters (numbers first) ---
builder.add_stat_cards(
    title="لماذا محو الأمية الرقمية؟",
    stats=[
        {"number": "67%", "label": "من البالغين يفتقرون لمهارات رقمية أساسية", "trend": "down"},
        {"number": "90%", "label": "من الوظائف تتطلب مهارات رقمية", "trend": "up"},
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: stat_cards
Duration: auto-advance after 8s or click
Audio: DLIT_U01_slide01.mp3

Layers:
- base (default visible)

Triggers:
1. Entrance animation: cards fade in sequentially (0.4s delay each)

=== NARRATOR SCRIPT ===
قبل أن نتعرف على ركائز محو الأمية الرقمية، دعونا نلقي نظرة على هذه الأرقام. 67 بالمئة من البالغين حول العالم يفتقرون لمهارات رقمية أساسية، بينما 90 بالمئة من الوظائف الحديثة تتطلب هذه المهارات.""",
)

# --- BUILD: SVG building metaphor — the anchor visual ---
builder.add_concept_visual(
    title="الركائز الخمس لمحو الأمية الرقمية",
    visual_type="process_flow",  # Using concept_visual dispatcher
    data=[
        {"num": 1, "label": "المعلومات", "desc": "البحث والتقييم والتنظيم"},
        {"num": 2, "label": "التواصل", "desc": "المشاركة والتعاون الرقمي"},
        {"num": 3, "label": "إنشاء المحتوى", "desc": "الإنتاج والبرمجة والحقوق"},
        {"num": 4, "label": "الأمان", "desc": "الحماية والخصوصية والصحة"},
        {"num": 5, "label": "حل المشكلات", "desc": "التحليل والابتكار التقني"},
    ],
    use_svg=True,  # SVG building metaphor — 5 pillars supporting a structure
    image_prompt="five architectural pillars supporting a roof structure, each pillar with a distinct icon, modern flat design",
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: concept_visual (SVG)
Duration: learner-paced

Layers:
- base (default visible)
- pillar_detail_1 through pillar_detail_5: expanded sub-skills per pillar

States:
- Each pillar shape: [Normal, Hover, Selected]

Triggers:
1. Show layer pillar_detail_N when user clicks pillar_N
2. Highlight selected pillar with glow effect
3. Dim other pillars when one is selected

Variables:
- pillars_explored (Number, default 0): tracks completion

Conditions:
- Show "Next" when pillars_explored >= 3

=== NARRATOR SCRIPT ===
محو الأمية الرقمية يرتكز على خمس ركائز أساسية — كالأعمدة التي تحمل بناءً متكاملاً. كل ركيزة ضرورية، وإزالة أي منها تُضعف البناء بأكمله. انقر على كل ركيزة لاستكشاف مهاراتها.""",
)

# --- BUILD: Click-reveal for learner-paced exploration ---
builder.add_click_reveal_slide(
    title="استكشف كل ركيزة بالتفصيل",
    instruction="انقر على كل ركيزة لاكتشاف مهاراتها الفرعية",
    reveal_items=[
        {"label": "المعلومات", "description": "تشمل مهارات البحث الفعّال في الإنترنت، وتقييم مصداقية المصادر، وتنظيم المعلومات وأرشفتها رقمياً"},
        {"label": "التواصل", "description": "تشمل المشاركة الفعّالة عبر المنصات الرقمية، والتعاون في المشاريع عن بُعد، وآداب التواصل الإلكتروني"},
        {"label": "إنشاء المحتوى", "description": "تشمل إنتاج المحتوى الرقمي بأشكاله، ومبادئ البرمجة، وفهم حقوق الملكية الفكرية والتراخيص"},
        {"label": "الأمان", "description": "تشمل حماية الأجهزة والبيانات، وإدارة الخصوصية الرقمية، والحفاظ على الصحة الرقمية والتوازن"},
        {"label": "حل المشكلات", "description": "تشمل تحديد المشكلات التقنية وحلها، وتقييم الأدوات الرقمية، والابتكار باستخدام التقنية"},
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: click_reveal (tabs)
Duration: learner-paced

Layers:
- base (default visible — shows all 5 tab labels)
- content_1 through content_5: detailed description per pillar

States:
- tab_1 through tab_5: [Normal, Hover, Selected, Visited]

Triggers:
1. Show layer content_N when user clicks tab_N
2. Change tab_N state to Selected (active) and Visited (after deselect)
3. Hide previously visible content layer

Variables:
- tabs_visited (Number, default 0): +1 on each new tab click

Conditions:
- Enable Next button when tabs_visited >= 4

=== NARRATOR SCRIPT ===
الآن استكشف كل ركيزة بالتفصيل. انقر على كل عنوان لتتعرف على المهارات الفرعية التي تتضمنها.""",
)

# --- BUILD: Real-world connection with AI image ---
builder.add_content_slide(
    title="محو الأمية الرقمية في الممارسة اليومية",
    bullets=[
        "الموظف الذي يتقن الركائز الخمس يتعامل بثقة مع التحديات الرقمية",
        "المهارات الرقمية لم تعد اختيارية — بل أساسية كالقراءة والكتابة",
        "التطوير المستمر ضروري لمواكبة التغير السريع في التقنية",
    ],
    image_prompt="professional confidently using multiple digital tools and screens, modern office, flat vector style",
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: content_slide
Duration: learner-paced
Audio: DLIT_U01_slide04.mp3

Layers:
- base (default visible)

Triggers:
1. Entrance animation on bullets (fade in sequentially)

=== NARRATOR SCRIPT ===
في الممارسة اليومية، الموظف الذي يتقن هذه الركائز الخمس يتعامل مع أي تحدٍّ رقمي بثقة. المهارات الرقمية أصبحت كالقراءة والكتابة — لا غنى عنها.""",
)

# --- PRACTICE: Quiz testing relationships, not just names ---
builder.add_quiz_slide(
    question="إذا أتقن شخص جميع ركائز محو الأمية الرقمية ما عدا 'الأمان'، ماذا يحدث؟",
    options=[
        "لا يتأثر أداؤه الرقمي لأن الأمان ركيزة ثانوية",
        "يصبح عرضة للمخاطر الرقمية رغم كفاءته في المهارات الأخرى",
        "يحتاج فقط لبرنامج حماية ليعوّض النقص",
        "يمكنه الاعتماد على ركيزة حل المشكلات لتعويض النقص",
    ],
    correct_index=1,
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: quiz (MCQ)
Duration: learner-paced

Layers:
- base (default visible)
- feedback_correct: "أحسنت! كل ركيزة ضرورية — إزالة أي منها تُضعف البناء بأكمله"
- feedback_incorrect: "فكّر مرة أخرى — تذكّر أن الركائز الخمس كأعمدة البناء"

States:
- opt_0 through opt_3: [Normal, Hover, Selected, Correct, Incorrect]

Triggers:
1. Select option on click (deselect others)
2. Submit button evaluates answer
3. Show feedback_correct if correct_index selected
4. Show feedback_incorrect otherwise
5. Highlight correct answer after 2 attempts

Variables:
- quiz_attempts (Number, default 0)
- quiz_score (Number, default 0)

=== NARRATOR SCRIPT ===
سؤال للتفكير: إذا أتقن شخص أربع ركائز من خمس ما عدا الأمان، ما الذي سيحدث؟""",
)
```

### Why This Works

1. **The building metaphor IS the teaching.** By showing pillars as structural supports, the learner intuitively understands that each one is necessary. This is not decoration — it is the pedagogical strategy.

2. **Click-reveal respects learner autonomy.** Instead of force-feeding 5 slides of details, the learner explores at their own pace. The "visited" states create a sense of progress and completion.

3. **The quiz tests the METAPHOR, not the list.** "What happens if you remove one pillar?" directly tests whether the building metaphor worked. A lazy quiz would ask "How many pillars are there?" — that tests nothing.

4. **Content slide bridges abstract to concrete.** After the conceptual exploration (SVG + click-reveal), the content slide with a real-world image grounds the idea: "This is what it looks like in practice."

5. **Visual variety across 5 slides:** stat_cards → concept_visual(SVG) → click_reveal → content_slide → quiz. Five different patterns, zero repetition.

### What Would Be WRONG

The mechanical approach:

```
Slide 1: icon_grid with 5 items (one per pillar)
Slide 2: content_slide with bullets about Pillar 1
Slide 3: content_slide with bullets about Pillar 2
Slide 4: content_slide with bullets about Pillar 3
Slide 5: content_slide with bullets about Pillar 4
Slide 6: content_slide with bullets about Pillar 5
Slide 7: quiz: "How many pillars of digital literacy are there?"
```

**Why this fails:**
- icon_grid treats the pillars as independent items — misses the interconnection
- Five consecutive content_slides with bullets — massive pacing violation
- No visual metaphor — "pillars" remain an abstract word, not a tangible image
- The quiz tests trivial recall ("count to 5") instead of conceptual understanding
- No click-reveal or learner control — everything is force-fed linearly
- The learner forgets everything by slide 4 because there is no variety or engagement

---

## Example 3: Data-Heavy Content

### The Scenario

Content: **"إحصائيات الإنترنت العالمية وتطورها"** (Global Internet Statistics and Evolution)
The content contains key internet adoption numbers (users, mobile penetration, social media), a historical timeline of internet milestones, a comparison of internet access across regions, and emerging trends. Heavy on data, light on concepts.

### The Agent's Reasoning (inner monologue)

> "This is mostly numbers and data. The trap is to dump all statistics into one giant table or a series of bullet slides. Instead, I need to make numbers TELL A STORY.
>
> - The HOOK should be the most surprising numbers — stat_cards are perfect because numbers ARE the visual. I will pick the 3 most impactful stats.
> - Then I will use a TIMELINE for the historical evolution — this shows how we got here. Milestones with dates create a sense of journey, which is more engaging than a bullet list of historical facts.
> - The COMPARISON of regions is a natural fit for the comparison pattern — side by side columns showing the digital divide. I will use native PPTX here because the text labels are the content.
> - For the 'emerging trends' section, I will use content_with_cards because trends are distinct items that benefit from card formatting. Each trend gets an image prompt showing what that trend looks like.
> - Finally, a SCENARIO interaction — given these statistics, what decision would you make? This pushes the learner from passive data consumption to active analysis.
>
> The narrative arc here is: SURPRISE (stats) → JOURNEY (timeline) → CONTRAST (comparison) → FUTURE (trends + scenario). The data tells a story of growth, inequality, and opportunity."

### Visual Composition Plan

| # | Title | Act | Pattern | SVG? | AI Image? | Image Prompt | Why This Visual |
|---|-------|-----|---------|------|-----------|--------------|-----------------|
| 1 | أرقام مذهلة عن الإنترنت | Hook | stat_cards | No | No | — | Numbers are the hook — let them speak |
| 2 | رحلة الإنترنت عبر العقود | Build | timeline | No | No | — | Timeline shows the journey — native is better for text-heavy milestones |
| 3 | — | Build | quote_highlight | No | No | — | Breathing slide between dense data |
| 4 | الفجوة الرقمية بين المناطق | Build | comparison | No | No | — | Side-by-side makes inequality visible |
| 5 | الاتجاهات الناشئة | Build | content_with_cards | No | Yes (per card) | concept-specific per card | Cards + images show what trends look like |
| 6 | سيناريو: قرار استراتيجي | Practice | scenario | No | Yes | "executive looking at data dashboard, flat vector" | Data analysis in action |

### The Code

```python
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="GINT", unit_number=3,
    unit_name="إحصائيات الإنترنت العالمية",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
)

# --- HOOK: Most surprising numbers ---
builder.add_stat_cards(
    title="الإنترنت اليوم — أرقام مذهلة",
    stats=[
        {"number": "5.4B", "label": "مستخدم إنترنت حول العالم", "trend": "up"},
        {"number": "92%", "label": "يتصفحون عبر الهاتف المحمول", "trend": "up"},
        {"number": "2.5 ساعة", "label": "متوسط الاستخدام اليومي لوسائل التواصل", "trend": "up"},
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: stat_cards
Duration: auto-advance after 10s or click
Audio: GINT_U03_slide01.mp3

Layers:
- base (default visible)

Triggers:
1. Cards entrance: scale up from 0 to 100%, sequentially (0.3s delay each)
2. Number counter animation from 0 to final value

=== NARRATOR SCRIPT ===
لنبدأ بأرقام مذهلة: أكثر من خمسة مليارات شخص يستخدمون الإنترنت اليوم، 92 بالمئة منهم عبر هواتفهم المحمولة، ويقضون في المتوسط ساعتين ونصف يومياً على وسائل التواصل الاجتماعي.""",
)

# --- BUILD: Timeline showing the journey ---
builder.add_timeline(
    title="رحلة الإنترنت — من الفكرة إلى العالمية",
    milestones=[
        {"year": "1969", "title": "أربانت", "desc": "أول شبكة حاسوبية بين أربع جامعات", "status": "done"},
        {"year": "1991", "title": "الويب العالمي", "desc": "تيم بيرنرز لي يطلق شبكة الويب", "status": "done"},
        {"year": "2004", "title": "ويب 2.0", "desc": "ظهور التواصل الاجتماعي والمحتوى التشاركي", "status": "done"},
        {"year": "2007", "title": "عصر المحمول", "desc": "آيفون يغيّر قواعد الوصول للإنترنت", "status": "done"},
        {"year": "2024", "title": "الذكاء التوليدي", "desc": "نماذج لغوية تعيد تشكيل التفاعل الرقمي", "status": "active"},
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: timeline
Duration: learner-paced

Layers:
- base (default visible — shows all milestones)
- detail_1969 through detail_2024: expanded description per milestone

States:
- milestone_1 through milestone_5: [Normal, Hover, Selected]

Triggers:
1. Timeline draws progressively (line animation left to right)
2. Each milestone marker appears with pop animation
3. Click milestone to show detail layer

Variables:
- milestones_viewed (Number, default 0)

=== NARRATOR SCRIPT ===
رحلة الإنترنت بدأت عام 1969 بشبكة أربانت، ثم تحولت للويب العالمي عام 1991، وشهدت ثورة التواصل الاجتماعي في 2004، ثم عصر المحمول في 2007، وصولاً إلى الذكاء التوليدي اليوم.""",
)

# --- BREATHE: Reflection quote ---
builder.add_quote_highlight(
    title="تأمل",
    quote="الإنترنت لم يغيّر فقط كيف نتواصل — بل غيّر كيف نفكر ونتعلم ونعمل",
    attribution="",
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: quote_highlight
Duration: auto-advance after 6s or click
Audio: GINT_U03_slide03.mp3

Layers:
- base (default visible)

Triggers:
1. Fade-in animation on quote (0.5s)

=== NARRATOR SCRIPT ===
الإنترنت لم يغيّر فقط كيف نتواصل، بل غيّر كيف نفكر ونتعلم ونعمل. هذا التحول العميق يظهر بوضوح عندما نقارن بين المناطق المختلفة.""",
)

# --- BUILD: Comparison showing digital divide ---
builder.add_comparison(
    title="الفجوة الرقمية — مقارنة بين المناطق",
    columns=[
        {
            "title": "المناطق المتقدمة",
            "items": [
                "نسبة الوصول: 95%+",
                "سرعة متوسطة: 100 ميجابت/ث",
                "اقتصاد رقمي ناضج",
                "بنية تحتية متطورة",
            ],
            "highlight": False,
        },
        {
            "title": "المناطق النامية",
            "items": [
                "نسبة الوصول: 35-60%",
                "سرعة متوسطة: 10 ميجابت/ث",
                "اقتصاد رقمي ناشئ",
                "فجوة في البنية التحتية",
            ],
            "highlight": True,
        },
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: comparison
Duration: learner-paced

Layers:
- base (default visible)

States:
- column_left, column_right: [Normal, Hover]

Triggers:
1. Columns slide in from opposite sides (0.5s)
2. Hover on column highlights differences

=== NARRATOR SCRIPT ===
رغم التقدم الكبير، لا تزال الفجوة الرقمية واسعة بين المناطق. في المناطق المتقدمة، نسبة الوصول تتجاوز 95 بالمئة، بينما في المناطق النامية قد لا تتجاوز 60 بالمئة.""",
)

# --- BUILD: Emerging trends as cards with images ---
builder.add_content_with_cards(
    title="الاتجاهات الناشئة في عالم الإنترنت",
    cards=[
        {
            "title": "الذكاء الاصطناعي التوليدي",
            "body": "نماذج لغوية وتوليد صور تعيد تشكيل إنتاج المحتوى والتفاعل الرقمي",
            "image_prompt": "AI brain generating creative content streams, modern flat vector",
        },
        {
            "title": "إنترنت الأشياء (IoT)",
            "body": "50 مليار جهاز متصل بحلول 2030 — من المنازل الذكية إلى المدن الذكية",
            "image_prompt": "smart city with connected IoT sensors and devices, flat vector",
        },
        {
            "title": "الجيل السادس (6G)",
            "body": "سرعات فائقة وزمن استجابة شبه معدوم تمهّد لتجارب رقمية غامرة",
            "image_prompt": "futuristic wireless communication tower with data streams, flat vector",
        },
    ],
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: content_with_cards
Duration: learner-paced

Layers:
- base (default visible)

Triggers:
1. Cards entrance: slide up from bottom, sequentially (0.4s delay)

=== NARRATOR SCRIPT ===
ثلاثة اتجاهات ستشكّل مستقبل الإنترنت: الذكاء الاصطناعي التوليدي يعيد تشكيل المحتوى، إنترنت الأشياء يربط المليارات من الأجهزة، والجيل السادس يمهد لتجارب رقمية غامرة.""",
)

# --- PRACTICE: Scenario using data for decision-making ---
builder.add_scenario_slide(
    title="سيناريو: قرار استراتيجي",
    situation="أنت مسؤول التحول الرقمي في شركة سعودية. بناءً على إحصائيات الإنترنت التي درستها — 92% يتصفحون عبر المحمول والفجوة الرقمية بين المناطق — ما هي أولويتك الاستراتيجية؟",
    choices=[
        "بناء تطبيق ويب متطور يعمل فقط على الحواسيب المكتبية",
        "تطوير تطبيق محمول أولاً مع دعم للمناطق ذات الاتصال المحدود",
        "الانتظار حتى تتحسن البنية التحتية في جميع المناطق",
    ],
    correct_index=1,
    notes="""=== STORYLINE BLUEPRINT ===
Slide Type: scenario (branching)
Duration: learner-paced

Layers:
- base (default visible)
- feedback_choice_0: "92% يتصفحون عبر المحمول — تطبيق مكتبي فقط يتجاهل الواقع"
- feedback_choice_1: "ممتاز! قرار يستند إلى البيانات ويراعي الفجوة الرقمية"
- feedback_choice_2: "الانتظار ليس استراتيجية — يمكن تصميم حلول تعمل مع البنية الحالية"

Triggers:
1. Show feedback_choice_N on choice click
2. Highlight correct choice after feedback
3. Enable Next after any choice

Variables:
- scenario_score (Number, default 0)

=== NARRATOR SCRIPT ===
لنطبّق ما تعلمناه في سيناريو عملي. بصفتك مسؤول التحول الرقمي، كيف ستستخدم هذه الإحصائيات لاتخاذ قرار استراتيجي؟""",
)
```

### Why This Works

1. **Data tells a story, not a dump.** The sequence Surprise → Journey → Contrast → Future transforms raw statistics into a narrative. Each pattern is chosen for the RELATIONSHIP it expresses: stat_cards for impact, timeline for evolution, comparison for contrast, cards for categories.

2. **The timeline creates a sense of journey.** Instead of "Internet started in 1969. Then in 1991..." as bullets, the timeline visually places the learner ON the journey. The "active" status on 2024 says "you are HERE."

3. **Comparison makes inequality VISIBLE.** Side-by-side columns with specific numbers make the digital divide undeniable. This is more powerful than a paragraph about inequality.

4. **Cards with concept-specific images for trends.** Each trend card has an AI image prompt that shows WHAT that trend looks like — not a generic technology image but a specific visualization of IoT, AI, or 6G.

5. **The scenario demands data-driven reasoning.** The learner must connect the statistics (92% mobile, digital divide) to a strategic decision. This is Bloom's Apply/Analyze — much higher than a quiz asking "What percentage use mobile?"

6. **Breathing quote between dense data.** After timeline (dense) and before comparison (dense), the quote gives the mind a moment to process.

### What Would Be WRONG

The data-dump approach:

```
Slide 1: content_slide with bullet list of all internet statistics
Slide 2: content_slide with bullet list of historical milestones
Slide 3: content_slide with bullet list of regional differences
Slide 4: content_slide with bullet list of emerging trends
Slide 5: quiz: "How many internet users are there globally?"
```

**Why this fails:**
- All data crammed into bullet lists — no visual differentiation between types of data
- Timeline as bullets loses the sense of journey and progression
- Comparison as bullets hides the stark contrast between regions
- No breathing slides — four dense slides in a row overwhelms the learner
- Quiz tests trivial number recall instead of data-driven reasoning
- Every slide uses the same pattern — the learner cannot tell statistics from history from trends

---

## Anti-Patterns: What NOT to Do

### Anti-Pattern 1: The Bullet Machine

```python
# WRONG — same pattern 4 times in a row, no visual variety
builder.add_content_slide(title="المحور الأول", bullets=["نقطة 1", "نقطة 2", "نقطة 3"])
builder.add_content_slide(title="المحور الثاني", bullets=["نقطة 1", "نقطة 2", "نقطة 3"])
builder.add_content_slide(title="المحور الثالث", bullets=["نقطة 1", "نقطة 2", "نقطة 3"])
builder.add_content_slide(title="المحور الرابع", bullets=["نقطة 1", "نقطة 2", "نقطة 3"])
```

**Why it is wrong:** Uses `content_slide` for everything. The agent did not ask "What relationship does this content express?" Different content relationships demand different visual patterns.

### Anti-Pattern 2: The Generic Image

```python
# WRONG — image prompts are vague and decorative, not concept-specific
builder.add_content_slide(
    title="الأمن السيبراني",
    bullets=["حماية البيانات", "التشفير", "جدران الحماية"],
    image_prompt="technology background",  # Too generic! Does not help understanding
)
```

**Why it is wrong:** The image prompt "technology background" adds nothing to learning. A good prompt would be "layered security shields protecting a central data core, showing firewall, encryption, and access control layers, flat vector" — specific to the concept being taught.

### Anti-Pattern 3: Skipping the Breathing

```python
# WRONG — 5 dense slides with no breaks
builder.add_process_flow(title="...", steps=[...])          # Dense
builder.add_comparison(title="...", columns=[...])          # Dense
builder.add_icon_grid(title="...", items=[...])             # Dense
builder.add_timeline(title="...", milestones=[...])         # Dense
builder.add_content_with_cards(title="...", cards=[...])    # Dense
```

**Why it is wrong:** Five information-dense slides with no breathing room causes cognitive overload. After every 2 dense slides, insert a quote_highlight, section_divider, or interaction slide.

### Anti-Pattern 4: Trivial Quiz Questions

```python
# WRONG — tests recall of a number, not understanding
builder.add_quiz_slide(
    question="كم عدد مستخدمي الإنترنت في العالم؟",
    options=["3 مليار", "5.4 مليار", "8 مليار", "10 مليار"],
    correct_index=1,
)
```

**Why it is wrong:** "How many users?" tests trivial recall. The learner could guess or memorize this without understanding anything. A better question would require applying or analyzing the data: "Given that 92% access the internet via mobile, what should a new service prioritize?" — this tests whether the learner can USE the data, not just recall it.
