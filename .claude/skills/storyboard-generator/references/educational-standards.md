# Educational Quality Standards Reference

Standards and frameworks that ensure storyboard content is **pedagogically sound**, not just visually polished. The storyboard is the first draft — quality here prevents problems downstream in SCORM packaging and Storyline development.

## When to Use This Reference

- **Phase 1 (Content Analysis)**: Check content against Gagne's Nine Events, identify Bloom's levels per topic
- **Phase 2 (Learning Objectives)**: Validate objectives with Bloom's verb table, ensure measurability
- **Phase 3 (Storyboard Generation)**: Apply alignment checks, pacing rules, feedback templates
- **Final Review**: Run the quality gates checklist

---

## 1. Bloom's Taxonomy — Verb Reference

Every learning objective MUST use a measurable verb from this table. Never use vague verbs like "understand", "know", or "learn".

| Level | Arabic Verbs | English Verbs | Assessment Type | Color |
|-------|-------------|---------------|-----------------|-------|
| **1. التذكر (Remember)** | يُعدد، يُسمي، يُحدد، يستذكر، يعرّف | List, name, identify, recall, define | MCQ, True/False | Blue |
| **2. الفهم (Understand)** | يشرح، يصف، يُلخص، يُفسر، يُوضح | Explain, describe, summarize, interpret | MCQ, Written response | Green |
| **3. التطبيق (Apply)** | يستخدم، يُطبق، يُنفذ، يُوظف، يحل | Use, implement, demonstrate, solve | Practice activity, Scenario | Orange |
| **4. التحليل (Analyze)** | يُقارن، يُميز، يفحص، يُحلل، يُصنف | Compare, contrast, examine, classify | Case study, Comparison | Red |
| **5. التقييم (Evaluate)** | يُقيّم، يحكم، يُوصي، يُبرر، ينتقد | Assess, judge, recommend, justify | Critique, Decision scenario | Purple |
| **6. الإبداع (Create)** | يُصمم، يُطور، يبتكر، يبني، يُنتج | Design, develop, create, construct | Project, Production | Gold |

### Objective Formula (Arabic)
```
أن + الفعل (من تصنيف بلوم) + المتعلم + المحتوى + المعيار/الشرط
```

### Objective Formula (English)
```
"By the end of this [lesson/module], you will be able to [VERB] [WHAT] [CONDITION]."
```

### Bad vs Good Objectives
- BAD: "فهم إدارة المشاريع" (vague — "understand" is not measurable)
- GOOD: "تصميم جدول زمني للمشروع باستخدام مخطط جانت لمدة 3 أشهر" (specific verb + content + condition)

### Bloom's Level Display Rule
When generating the Objectives storyboard (ObjectivesBuilder), show the Bloom's level next to each objective using color coding. When generating tests (TestBuilder), tag each question with its Bloom's level to ensure alignment.

---

## 2. Gagne's Nine Events of Instruction

Every lecture should follow this 9-step pedagogical arc. This maps directly to our PPTX slide sequence:

| # | Event | Purpose | PPTX Implementation | Duration |
|---|-------|---------|---------------------|----------|
| 1 | **جذب الانتباه** (Gain Attention) | Hook the learner | Title slide + stat_cards OR quote_highlight with surprising fact | 30 sec |
| 2 | **عرض الأهداف** (State Objectives) | Set expectations | Objectives slide | 30 sec |
| 3 | **تنشيط المعرفة السابقة** (Recall Prior Knowledge) | Connect to existing knowledge | Content slide: "تذكر ما تعلمنا سابقاً..." | 1 min |
| 4 | **عرض المحتوى** (Present Content) | Core instruction | Visual grammar slides (process_flow, comparison, icon_grid, etc.) | 5-7 min |
| 5 | **تقديم التوجيه** (Provide Guidance) | Examples, tips, best practices | Content slides with examples, two_column for tips vs mistakes | 2 min |
| 6 | **استخلاص الأداء** (Elicit Practice) | Learner does the work | Quiz, drag_drop, scenario, click_reveal interactions | 2 min |
| 7 | **تقديم التغذية الراجعة** (Provide Feedback) | Correct/explain | Feedback in Storyline notes (growth mindset messages) | embedded |
| 8 | **تقييم الأداء** (Assess Performance) | Knowledge check | Quiz slide(s) at end of section | 1 min |
| 9 | **تعزيز الاحتفاظ** (Enhance Retention) | Summary + next steps | Summary slide + closing slide | 1 min |

### How to Apply
When composing a lecture (see also pptx-composition-arc.md), check that your slide sequence covers all 9 events:
1. Does the lecture START with an attention-grabber? (Not just a dry title)
2. Are objectives shown early?
3. Is there a bridge to prior knowledge?
4. Is the core content varied (multiple visual patterns)?
5. Are there worked examples, not just theory?
6. Is there at least ONE practice interaction per section?
7. Does every quiz have meaningful feedback in Storyline notes?
8. Is there a knowledge check before the summary?
9. Does the lecture END with summary + next steps?

---

## 3. Quality Matters (QM) Alignment

The invisible thread: every element must connect back to objectives.

```
الأهداف التعليمية (Learning Objectives)
        ↕
المحتوى التعليمي (Instructional Materials)
   "هل المحتوى يدعم تحقيق الأهداف؟"
        ↕
الأنشطة التعليمية (Learning Activities)
   "هل الأنشطة تُتيح للمتعلم الممارسة؟"
        ↕
التقييم (Assessments)
   "هل التقييم يقيس الأهداف فعلاً؟"
```

### Alignment Map Template

Generate this table during Phase 1 (Content Analysis) to verify alignment:

| الهدف (Objective) | مستوى بلوم (Bloom's) | المحتوى (Content Slide) | النشاط (Activity) | التقييم (Assessment) |
|---|---|---|---|---|
| تعريف التقنية الناشئة | التذكر | شريحة تعريف + أمثلة | اسحب وأفلت: صنف التقنيات | سؤال اختيار من متعدد |
| مقارنة الفوائد والتحديات | التحليل | شريحة مقارنة عمودين | انقر لاكتشاف | سؤال سيناريو |
| تصميم خطة تحول رقمي | الإبداع | عملية مراحل + أمثلة | نشاط تطبيقي | مشروع / واجب |

### QM Essential Standards (Storyboard-Relevant)

| QM # | Standard | How We Apply It |
|------|---------|-----------------|
| 2.1 | Course objectives are measurable | Use Bloom's verbs only — validate in Phase 2 |
| 2.2 | Module objectives map to course objectives | Each unit's objectives must trace to overall course goals |
| 2.4 | Alignment between objectives, activities, assessments is visible | Generate alignment map in Phase 1 |
| 3.1 | Assessments measure stated objectives | Quiz questions must match Bloom's level of the objective they test |
| 4.1 | Materials support learning objectives | Every content slide must serve an objective — no filler |
| 4.5 | Multiple content types per module | Minimum: text + visual + interactive (never all one type) |
| 5.1 | Activities promote objective achievement | At least 1 interaction per section (quiz, drag-drop, scenario) |
| 5.2 | Activities support active learning | No passive-only sections. After 3-4 content slides → interaction |

### Alignment Violation Warnings
When generating storyboards, check for these misalignments:
- Objective says "تطبيق" (Apply) but quiz only tests "تذكر" (Remember) → **Bloom's mismatch**
- Content teaches Topic A but quiz tests Topic B → **Content-assessment gap**
- 6+ content slides with no interaction → **Passive learning violation (QM 5.2)**
- All slides are text-only → **Content type violation (QM 4.5)**

---

## 4. NELC Saudi Standards (المعايير الوطنية)

Mandatory for Saudi university projects. Key requirements:

### Content Rules
| Rule | Requirement | Our Implementation |
|------|------------|-------------------|
| Video duration | Max 10 minutes per clip | Video storyboard scenes ≤ 10 min each |
| Arabic font size | 18px+ body text minimum | Tajawal 18pt+ in PPTX engine |
| Line height | 1.6-1.8 for Arabic | Engine default 1.3x-1.4x — **check if sufficient** |
| Content chunking | Small, manageable segments | Max 25-30 slides per lecture, sections every 4-6 slides |
| Content types | At least 3 types per module | Text + visual patterns + interactions |
| Interactions | Minimum 2 different types per module | Quiz + at least one other (drag-drop, scenario, click-reveal) |
| Cultural alignment | Saudi/Islamic values respected | No prohibited imagery (enforced via config.json negativeRules) |
| Accessibility | WCAG 2.1 AA compliance | Color contrast, font sizes, shape naming for screen readers |
| RTL | Full Arabic RTL support | Engine handles via _pptx_core.py RTL system |

### NELC Instructional Design Requirements
- [ ] Clear learning objectives at start of each unit (Bloom's verbs)
- [ ] Content aligned with objectives (alignment map)
- [ ] Activities aligned with objectives
- [ ] Assessments aligned with objectives
- [ ] Student-centered design approach
- [ ] Universal Design for Learning (UDL) principles

### NELC Assessment Requirements
- [ ] Formative knowledge checks after each lesson section
- [ ] Summative module quiz at end
- [ ] Clear passing criteria defined
- [ ] Meaningful feedback on responses (not just "correct/incorrect")
- [ ] Remediation paths for failed assessments (e.g., "review section 2")

---

## 5. Growth Mindset Feedback Library

Use these templates when writing quiz/interaction feedback in Storyline notes. Never just say "صح" or "خطأ".

### Correct Answer Feedback
```
أحسنت! إجابة صحيحة. [اشرح لماذا هذه الإجابة صحيحة بجملة واحدة]
```
Variations:
- "ممتاز! أنت تبني فهماً متيناً لهذا الموضوع."
- "رائع! هذا يدل على استيعابك للمفهوم."
- "إجابة دقيقة! لاحظ كيف يرتبط هذا بـ [المفهوم التالي]."

### Incorrect Answer Feedback
```
ليس بعد — لكنك تتعلم! الإجابة الصحيحة هي [X] لأن [شرح مختصر]. راجع [القسم المحدد].
```
Variations:
- "فكرة جيدة، لكن الإجابة الأدق هي [X]. السبب: [شرح]."
- "هذا خطأ شائع. المفتاح هنا هو [النقطة الأساسية]."
- "حاول مرة أخرى! تلميح: فكر في [إشارة للمفهوم الصحيح]."

### Retry Feedback
```
عودتك للمحاولة مرة أخرى تدل على إصرار حقيقي! خذ وقتك في التفكير.
```

### Quiz Completion Feedback
```
أكملت النشاط! حصلت على [X] من [Y]. [تعليق إيجابي مناسب للدرجة].
```
Score-based:
- 90-100%: "أداء متميز! أنت متمكن من هذا الموضوع."
- 70-89%: "أداء جيد! راجع النقاط التي أخطأت فيها لتعزيز فهمك."
- Below 70%: "لا بأس — التعلم رحلة. ننصحك بمراجعة المحتوى والمحاولة مرة أخرى."

---

## 6. Content Type Distribution Validator

When planning a lecture, ensure variety:

### Minimum Requirements per Lecture
- [ ] At least 1 visual grammar pattern (process_flow, stat_cards, timeline, etc.)
- [ ] At least 2 different interaction types (quiz + drag-drop, or quiz + scenario, etc.)
- [ ] At least 1 image-enhanced slide (content with image_prompt)
- [ ] At least 1 breathing slide (quote_highlight or section_divider)
- [ ] No more than 3 consecutive text-only content slides

### Warnings to Flag
| Issue | Warning |
|-------|---------|
| All slides are content_slide with bullets | "Content type violation — add visual patterns and interactions" |
| No interactions in 6+ slides | "Passive learning — add quiz or activity (QM 5.2)" |
| No images in entire lecture | "Visual variety needed — add image_prompt to key slides" |
| Same visual pattern 3+ times | "Pattern monotony — alternate between different patterns" |
| No breathing slides | "Cognitive overload risk — add quote or section divider" |

---

## 7. "Why This Matters" Relevance Prompts

Before each major section, include a real-world relevance connection. This addresses adult learning principles (relevance, problem-centered) and boosts engagement.

### Template
Add to the first content slide of each section:
```
لماذا هذا مهم؟ [ربط بالواقع العملي للمتعلم]
```

### Examples
- Before "التحول الرقمي": "90% من الشركات الناجحة في 2025 تعتمد على التحول الرقمي — وظيفتك القادمة قد تتطلب هذه المهارة."
- Before "أمن المعلومات": "في 2024، خسرت الشركات السعودية 6 مليار ريال بسبب الهجمات السيبرانية."
- Before "إدارة المشاريع": "المشاريع بدون منهجية واضحة تفشل بنسبة 70% — سنتعلم كيف نتجنب ذلك."

### When to Use
- At the start of each new section (after section_divider)
- As the first bullet or paragraph in the opening content slide
- Can use stat_cards with a striking number to make the "why" visual

---

## 8. Assessment-Objective Alignment Checker

When generating tests (pre-test, post-test, course exam), validate:

### For Each Question, Verify:
1. **Objective mapping**: Which specific objective does this question test?
2. **Bloom's match**: Is the question at the SAME Bloom's level as the objective?
3. **Content coverage**: Was this topic actually covered in the content?
4. **Distractor quality**: Are wrong options plausible but clearly wrong?

### Bloom's Level → Question Type Mapping
| Bloom's Level | Best Question Types | Avoid |
|---------------|-------------------|-------|
| التذكر (Remember) | MCQ, True/False | Open-ended questions |
| الفهم (Understand) | MCQ, Matching | Simple recall questions |
| التطبيق (Apply) | Scenario MCQ, Fill-blank | Pure definition questions |
| التحليل (Analyze) | Scenario MCQ, Drag-drop classification | Simple fact questions |
| التقييم (Evaluate) | Scenario MCQ, Ranking | Questions with obvious answers |
| الإبداع (Create) | Open response, Project assignment | MCQ (too constrained) |

### Factual Accuracy Rule (NON-NEGOTIABLE)
All quiz answers, feedback, and explanations MUST be 100% factually verified:
- Every "correct" answer must actually be correct
- Every "incorrect" option must actually be incorrect
- Feedback must cite accurate facts
- If accuracy cannot be verified, FLAG for human review

**Wrong answers in a quiz destroy learner trust and teach misinformation.**

---

## 9. Backward Design Thinking

Before generating any storyboard, think backwards:

```
الخطوة 3: ما الأنشطة التي تبني المهارة؟ (Plan Experiences)
    ↑
الخطوة 2: كيف سنعرف أن المتعلم تعلّم؟ (Assessment Evidence)
    ↑
الخطوة 1: ماذا نريد أن يتعلم المتعلم؟ (Desired Results)
```

### Apply During Phase 1 (Content Analysis):
1. Start with the END: What should the learner be able to DO after this unit?
2. Then define PROOF: What quiz/activity proves they can do it?
3. Then design CONTENT: What do they need to learn to get there?

This prevents the common mistake of "covering topics" without clear learning outcomes.

---

## 10. Quick Reference: Phase Checklist

### Phase 1 — Content Analysis
- [ ] Identify 4-8 key topics from raw content
- [ ] Assign Bloom's level to each topic
- [ ] Create draft alignment map (objective → content → activity → assessment)
- [ ] Check content type distribution (text, visual, interactive planned)
- [ ] Identify "Why This Matters" hooks for each section

### Phase 2 — Learning Objectives
- [ ] Write objectives using Bloom's verb table (Arabic formula)
- [ ] Verify each objective is measurable (not vague)
- [ ] Confirm alignment map: every objective has content + activity + assessment
- [ ] Check Bloom's distribution: not all at Remember level — include Apply/Analyze

### Phase 3 — Storyboard Generation
- [ ] Lecture follows Gagne's Nine Events arc
- [ ] At least 2 different interaction types per lecture
- [ ] No more than 3 consecutive content-only slides
- [ ] Growth mindset feedback in all quiz/interaction notes
- [ ] "Why This Matters" relevance prompt in each section opener
- [ ] Quiz questions match Bloom's level of their objectives
- [ ] All answers factually verified
