# Storyboard Type Specifications

Instructions for each of the 12 storyboard types. Read the relevant section before generating that type. Each section contains the domain-specific rules, quality standards, and engine API for that type.

## Shared Rules (Apply to ALL Types)

1. **All content in Arabic** — formal academic Arabic, right-to-left, no tashkeel/diacritics
2. **Read project config** from `projects/[code]/config.json` for constructor parameters
3. **Read the content analysis** before generating any storyboard
4. **Image priority**: `image_path` (manual) > `image_prompt` (AI-generated)
5. **Output path**: `output/[project-code]/U[XX]/[CODE]_U[XX]_[Type].[ext]`
6. **Engine scripts** at `.claude/skills/storyboard-generator/scripts/`

---

## 1. Content Analysis (تحليل المحتوى)

**Builder**: None (text analysis only — no document output)
**Output**: Structured Arabic analysis summary presented to user

### Analysis Checklist
Analyze ALL provided content files and produce:

- **الموضوعات الرئيسية**: All key topics covered
- **هيكل المحتوى**: Content structure (sections, subsections)
- **المفاهيم الأساسية**: Key concepts that need to be taught
- **المصطلحات المهمة**: Important terminology
- **الصور والوسائط**: Catalog of images, diagrams, videos referenced
- **الفجوات المحتملة**: Gaps or missing content
- **توزيع المحتوى المقترح**: Suggested distribution across storyboard types

### Activity Suggestions
For interactive activities, suggest:
- Which content segments work best as activities
- Recommended interaction types (multiple-choice, drag-and-drop, matching, sorting, etc.)
- At least 3 different activity ideas

### Test Concept Identification
Identify concepts suitable for assessment:
- Key facts that can be tested (for pre/post tests)
- Application scenarios (for higher-level questions)
- Common misconceptions (for effective distractors)

---

## 2. Learning Objectives (الأهداف التعليمية)

**Builder**: ObjectivesBuilder (DOCX)
**Image density**: 1 (hero image only)
**Output**: `[CODE]_U[XX]_Learning_Objectives.docx`

### Bloom's Taxonomy Levels
Use verbs from these levels (Arabic):

| Level | Arabic | Example Verbs |
|---|---|---|
| Remember (تذكر) | يُعرّف، يذكر، يسمّي | Define, list, name |
| Understand (فهم) | يشرح، يوضّح، يلخّص | Explain, describe, summarize |
| Apply (تطبيق) | يطبّق، يستخدم، ينفّذ | Apply, use, execute |
| Analyze (تحليل) | يحلّل، يقارن، يصنّف | Analyze, compare, classify |
| Evaluate (تقييم) | يقيّم، يبرّر، ينقد | Evaluate, justify, critique |
| Create (إبداع) | يصمّم، يبتكر، يخطّط | Design, create, plan |

### Objective Format
"أن + الفعل + المتعلم + المحتوى + المعيار"
Example: "أن يشرح المتعلم مفهوم الذكاء الاصطناعي بدقة 80%"

### Quality Rules
- 4-8 objectives per unit
- Cover multiple Bloom's levels (not just remember/understand)
- Each objective must be measurable and specific
- Objectives should align with the content analysis topics

### Engine Call
```python
from docx_engine import ObjectivesBuilder
builder = ObjectivesBuilder(project_code=..., unit_number=..., ...)
builder.set_element_name("الأهداف التعليمية")
builder.set_element_code("[CODE]_U[XX]_Learning_Objectives")
builder.set_screen_description("...")
builder.set_content_text("...")
builder.set_image_sources("...")
builder.set_detailed_description("...")
builder.set_image(image_prompt="educational concept visualization...")
builder.build()
builder.save("output/[CODE]/U[XX]/[CODE]_U[XX]_Learning_Objectives.docx")
```

---

## 3. Learning Map / Infographic (خارطة التعلم)

**Builder**: InfographicBuilder (DOCX)
**Image density**: 2-3 (per learning milestone)
**Output**: `[CODE]_U[XX]_Learning_Map.docx`

### Key Rule: Adapt to Actual Deliverables
The learning journey steps MUST match what's actually being produced:
- If no video requested, don't include a video milestone
- If 3 activities requested, show as sub-items under the activity milestone
- Match the order to the suggested storyboard order from the analysis

### Engine Call
```python
from docx_engine import InfographicBuilder
builder = InfographicBuilder(...)
builder.set_element_name("خارطة التعلم")
builder.set_screen_description("...")
builder.set_content_text("[learning journey description]")
builder.set_image_sources("[milestone descriptions]")
builder.set_detailed_description("[detailed learning path]")
builder.set_image(image_prompt="learning journey roadmap...")
builder.build()
builder.save("output/...")
```

---

## 4. Pre-Test (الاختبار القبلي)

**Builder**: TestBuilder (DOCX)
**Image density**: 1-2
**Output**: `[CODE]_U[XX]_Pre_Test.docx`

### Rules
- **3-5 questions ONLY** (diagnostic, not comprehensive)
- Multiple choice or True/False
- Easy to medium difficulty
- Tests prior knowledge (what do they already know?)
- Single attempt
- Covers the main topics from the content analysis

### Question Quality
- ONE concept per question
- No double negatives
- Plausible distractors (wrong answers should be believable)
- Formal academic Arabic
- If True/False: mix of true and false statements (not all true)

### Engine Call
```python
from docx_engine import TestBuilder
builder = TestBuilder(...)
builder.set_element_name("الاختبار القبلي")
builder.set_element_code("[CODE]_U[XX]_Pre_Test")
builder.set_test_info(description="...", instructions="...")
builder.set_image(image_prompt="...")
builder.add_question(
    question_text="...",
    choices=["أ. ...", "ب. ...", "ج. ...", "د. ..."],
    correct_answer="أ",
    image_description="..."  # optional
)
# Repeat add_question for each question
builder.build()
builder.save("output/...")
```

---

## 5. Interactive Lecture (المحاضرة التفاعلية)

**Builder**: LectureBuilder (PPTX)
**Image density**: 8-12
**Output**: `[CODE]_U[XX]_Interactive_Lecture.pptx`

### THIS IS THE MOST CRITICAL STORYBOARD TYPE

Before building, read these references:
- `references/visual-grammar.md` — choose the right visual pattern per concept
- `references/pptx-design-system.md` — art direction and design rules
- `references/storyline-blueprint.md` — speaker notes format

### Slide Structure (Narrative Arc)
1. **Title slide** (1) — visual impact, not just text
2. **Objectives slide** (1) — what will the learner achieve
3. **Hook** (1-2 slides) — surprising stat, question, or visual metaphor
4. **Core content** (8-15 slides) — varied visual patterns, see visual-grammar.md
5. **Practice interactions** (3-5 slides) — quiz, drag-drop, click-reveal, scenario
6. **Summary** (1) — visual recap using DIFFERENT pattern than content used
7. **Closing** (1) — next steps, encouragement

### Content Slide Rules
- ONE concept per slide maximum
- 6x6 rule: no more than 6 lines with 6 words each (for text-based slides)
- **Use visual grammar**: process flows, timelines, comparisons, stat cards, concept maps
- **Maximum 30% bullet/card slides** — the rest must use richer visual patterns
- Section dividers every 4-6 slides with progress indicator

### Variety Rules
- NEVER use the same visual pattern on 2 consecutive slides
- Mix interaction types (don't use 3 quizzes in a row)
- After 2-3 dense slides, insert a breathing slide (quote, reflection, visual-only)
- Use two-column layout for comparisons, NOT for cramming more content

### Speaker Notes Convention
Every slide MUST have Storyline blueprint in notes (see storyline-blueprint.md):
```
=== STORYLINE BLUEPRINT ===
[Interaction specification]

=== NARRATOR SCRIPT ===
[Arabic narration text]
```

### Maximum: 25-30 slides per lecture

---

## 6. PDF Lecture (محاضرة PDF)

**Builder**: LectureBuilder (PPTX)
**Image density**: 6-8
**Output**: `[CODE]_U[XX]_PDF_Lecture.pptx`

### Same as Interactive Lecture EXCEPT:
- **Skip** all interaction slides (quiz, drag-drop, click-reveal, scenario)
- **Skip** Storyline blueprint in notes (not needed for PDF export)
- **Keep** narrator script in notes (can be used as reading content)
- Pure content only — suitable for PDF export
- Focus on visual richness since there's no interaction to engage the learner

---

## 7. Motion Video (فيديو موشن)

**Builder**: VideoBuilder (DOCX)
**Image density**: 6-8 (one per scene)
**Output**: `[CODE]_U[XX]_Video.docx`

### Scene Structure
Each scene has a 6-row metadata table:
1. **شاشة توضيحية للمشهد** — Screen layout description
2. **مؤثرات صوتية خاصة** — Sound effects
3. **النص العلمي المقروء** — Narration script (the EXACT text to be read)
4. **النصوص التي تظهر في المشاهد** — On-screen text elements
5. **الوصف التفصيلي للمشهد والتزامن** — Detailed sync description with "بالتزامن مع..."
6. **روابط الصور** — Image/video references

### Quality Rules
- Total video duration: 3-7 minutes (estimate from narration length at ~130 words/min Arabic)
- Title scene first, closing scene last
- 2-4 narration segments per scene
- **Detailed visual descriptions** for the motion designer (not vague "show the concept")
- Varied visual techniques: split-screen, zoom, text overlays, image sequences, transitions
- Each scene should have a clear visual flow description

### Engine Call
```python
from docx_engine import VideoBuilder
builder = VideoBuilder(...)
builder.set_element_name("فيديو موشن")
builder.add_scene(
    title="مقدمة",
    screen_description="...",
    sound_effects="موسيقى هادئة",
    narration_segments=[
        {"narration": "...", "on_screen_text": "...", "scene_description": "...", "image_links": "..."}
    ],
    image_prompt="concept visualization for introduction scene..."
)
builder.build()
builder.save("output/...")
```

---

## 8. Interactive Activity (نشاط تفاعلي)

**Builder**: ActivityBuilder (DOCX)
**Image density**: 3-5 (one per interaction step)
**Output**: `[CODE]_U[XX]_Activity[Unit].[Seq].docx`

### Interaction Types (suggest to user — they decide)
- **اختيار من متعدد** — Multiple choice
- **سحب وإفلات** — Drag and drop
- **مطابقة** — Matching
- **ترتيب** — Sorting/Sequencing
- **ملء الفراغ** — Fill in the blank
- **صح/خطأ** — True/False
- **النقر على الصورة** — Hotspot (click on image)

### Quality Rules
- 1-2 learning objectives per activity
- Feedback must be **EDUCATIONAL** (explain WHY the answer is correct/incorrect, not just "correct!")
- Test UNDERSTANDING, not just recall
- Connect to real-world application when possible
- Each activity should have a clear learning purpose

### Engine Call
```python
from docx_engine import ActivityBuilder
builder = ActivityBuilder(...)
builder.set_element_name("نشاط تفاعلي")
builder.add_scene(
    title="...",
    description="...",
    elements="...",
    image_desc="...",
    motion_desc="...",
    sound_effects="...",
    on_screen_text="...",
    steps="...",
    correct_answer="...",
    buttons="...",
    image_prompt="activity scene visualization..."
)
builder.build()
builder.save("output/...")
```

---

## 9. Discussion (النقاش)

**Builder**: DiscussionBuilder (DOCX)
**Image density**: 1 (hero only)
**Output**: `[CODE]_U[XX]_Discussion.docx`

### Quality Rules
- **OPEN-ENDED question** — not yes/no, not factual recall
- Context paragraph: 3-5 sentences connecting to unit content
- Question should encourage:
  - Critical analysis of the concepts
  - Real-world application
  - Personal reflection
- Relevant to Saudi/Arab educational and professional context
- No single "correct" answer — multiple valid perspectives

### Engine Call
```python
from docx_engine import DiscussionBuilder
builder = DiscussionBuilder(...)
builder.set_element_name("نشاط نقاش")
builder.set_screen_description("...")
builder.set_content_text("[discussion question and context]")
builder.set_instructions("[participation guidelines]")
builder.set_related_objectives("[linked learning objectives]")
builder.set_image(image_prompt="discussion topic visualization...")
builder.build()
builder.save("output/...")
```

---

## 10. Assignment (الواجب)

**Builder**: AssignmentBuilder (DOCX)
**Image density**: 1 (hero only)
**Output**: `[CODE]_U[XX]_Assignment.docx`

### Quality Rules
- **APPLICATION-level or higher** on Bloom's Taxonomy
- Apply course concepts to new situations (not repeat what was taught)
- **Clearly scoped** — student knows exactly what to deliver
- Connect to real-world scenarios in the student's field
- Include clear evaluation criteria or rubric outline
- Reasonable scope (completable in the allocated time)

### Engine Call
```python
from docx_engine import AssignmentBuilder
builder = AssignmentBuilder(...)
builder.set_element_name("واجب")
builder.set_screen_description("...")
builder.set_content_text("[assignment description]")
builder.set_instructions("[submission guidelines and rubric]")
builder.set_related_objectives("[linked learning objectives]")
builder.set_image(image_prompt="assignment concept visualization...")
builder.build()
builder.save("output/...")
```

---

## 11. Post-Test (الاختبار البعدي)

**Builder**: TestBuilder (DOCX)
**Image density**: 1-2
**Output**: `[CODE]_U[XX]_Post_Test.docx`

### Rules
- **7-10 questions** (summative assessment)
- Multiple choice or True/False
- Medium to hard difficulty
- Cover multiple Bloom's levels (not just remember)
- Should align with learning objectives
- Include some application/analysis level questions
- Multiple attempts allowed (per client preference)

### Question Quality
Same as Pre-Test plus:
- At least 2-3 questions at Apply/Analyze level
- Distractors should reflect common misconceptions
- Questions should cover ALL major topics from the unit

---

## 12. Summary (الملخص)

**Builder**: SummaryBuilder (DOCX)
**Image density**: 2-3 (per topic section)
**Output**: `[CODE]_U[XX]_Summary.docx`

### Quality Rules
- **Maximum 2 pages** — this is a SUMMARY, not a textbook
- Use bullet points for clarity
- Key terms with brief definitions
- Reference learning objectives (each objective should be addressed)
- Clear, simple Arabic (simpler than lecture content)
- Focus on what the student **SHOULD REMEMBER** after completing the unit

### Engine Call
```python
from docx_engine import SummaryBuilder
builder = SummaryBuilder(...)
builder.set_element_name("الملخص")
builder.set_screen_description("...")
builder.set_content_text("[summary content organized by topic]")
builder.set_image_sources("[key concept descriptions]")
builder.set_detailed_description("[detailed summary]")
builder.set_image(image_prompt="unit summary visualization...")
builder.build()
builder.save("output/...")
```

---

## 13. Course Exam (اختبار المقرر)

**Builder**: TestBuilder (DOCX)
**Image density**: 1-2
**Output**: `[CODE]_Course_Exam.docx`

### Rules
- Question count per **client agreement** (stored in project config)
- Covers ALL units in the course (not just one unit)
- Balanced distribution across units
- Mix of Bloom's levels with emphasis on Apply/Analyze
- Comprehensive — the student who mastered all units should score well
- Time-appropriate (estimate ~1.5 minutes per question)
