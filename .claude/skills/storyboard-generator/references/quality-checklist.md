# Quality Checklist — Pre-Delivery Gates

Run through this checklist before delivering any lecture PPTX to the user. Every item must pass.

For design principles, see `references/principles.md` (single source of truth).

## Planning & Approval (BEFORE building)

- [ ] Visual Composition Plan was created (slide-by-slide with patterns, SVG concepts, image prompts)
- [ ] Plan was presented to and approved by the user BEFORE building
- [ ] SVG concept descriptions are specific metaphors, not generic ("pipeline with chambers" not just "process flow")
- [ ] AI image prompts are concept-specific, not generic stock-photo descriptions
- [ ] Image density target met: 8-12 images per lecture
- [ ] SVG visualization target: 4-8 per lecture where concepts benefit from visual explanation

## Visual Quality

- [ ] No two consecutive slides use the same visual pattern
- [ ] Content card backgrounds are not all the same color (accent rotation applied)
- [ ] At least one breathing slide per section (quote_highlight, section_divider, or stat_cards)
- [ ] Background depth washes present on content slides (corner_oval, radial_glow, or gradient_strip)
- [ ] Shadows applied to content cards (OOXML `effectLst > outerShdw`, not fake offset shapes)
- [ ] Section dividers have decorative corners and progress dots
- [ ] No slide looks like a generic PowerPoint (the PowerPoint Test)
- [ ] Visual hierarchy is clear when you squint (the Squint Test)

## RTL Correctness

- [ ] All body text is right-aligned (`PP_ALIGN.RIGHT`)
- [ ] All titles are center-aligned (`PP_ALIGN.CENTER`)
- [ ] Every paragraph has RTL set via `pPr.set('rtl', '1')`
- [ ] Fonts render via `cs_name` (Complex Script), not just `font.name`
- [ ] Process flows read right-to-left (rightmost shape = step 1)
- [ ] Arrow markers point left (`<--` direction in RTL)
- [ ] No tashkeel/diacritics in any text
- [ ] Line spacing is at least 1.3x for body text (1.4x for bullets)

## Shape Naming

Every interactive shape follows the naming convention:

- [ ] Background elements: `bg_*` (e.g., `bg_depth_wash`, `bg_header_bar`)
- [ ] Header elements: `hdr_*` (e.g., `hdr_section_tag`)
- [ ] Text content: `txt_*` (e.g., `txt_title`, `txt_body`)
- [ ] Buttons: `btn_*` (e.g., `btn_tab1`, `btn_submit`)
- [ ] Quiz options: `opt_*` (e.g., `opt_1`, `opt_2`)
- [ ] Content cards: `card_*` (e.g., `card_step1`)
- [ ] Drop zones: `zone_*` (e.g., `zone_category1`)
- [ ] Draggable items: `item_*` (e.g., `item_concept1`)
- [ ] Images: `img_*` (e.g., `img_hero`, `img_content`)
- [ ] SVG visuals: `svg_*` (e.g., `svg_diagram`)
- [ ] Connectors/lines: `line_*` (e.g., `line_arrow`)

## Storyline Notes

- [ ] Every slide has speaker notes (not empty)
- [ ] Static content slides have `=== STORYLINE BLUEPRINT ===` with slide type and duration
- [ ] Interaction slides (quiz, click-reveal, drag-drop) have full blueprint:
  - Layers listed with purpose
  - States listed per interactive shape
  - Triggers listed in order with conditions
  - Variables listed with type, default, and purpose
- [ ] Every slide has a `=== NARRATOR SCRIPT ===` section in formal Arabic
- [ ] Title slide has `=== STORYLINE IMPORT INSTRUCTIONS ===`
- [ ] Correct answer is clearly marked in quiz blueprints

## Images

- [ ] No broken image paths (every `image_path` points to an existing file)
- [ ] All images are aspect-ratio preserved (`_add_image` handles this)
- [ ] No placeholder text remaining (gray boxes with "صورة توضيحية" replaced with actual images)
- [ ] Generated images match the cultural rules from `config.json` (`negativeRules`)
- [ ] Image file sizes are reasonable (no single image over 5MB)

## Pacing and Structure

- [ ] Lecture follows the narrative arc: Hook -> Build -> Insight -> Practice -> Summary
- [ ] Breathing slides present (at least 1 per section)
- [ ] Section dividers inserted every 4-6 content slides
- [ ] Interactions placed after every 3-4 content slides
- [ ] Total slide count is 25-30 (not exceeding 30)
- [ ] No 3+ dense information slides in a row without a breathing slide

## TOC Titles

- [ ] Every slide has a hidden off-screen textbox named `title`
- [ ] Position: x=-2" (off-screen to the right in RTL)
- [ ] Contains the Arabic slide title for Storyline's sidebar navigation
- [ ] No slide shows "Untitled Slide" in Storyline

## Typography

- [ ] Slide titles use `FONT_EXTRABOLD` (Tajawal ExtraBold, 28-32pt)
- [ ] Body text uses `FONT_REGULAR` (Tajawal, 16-18pt)
- [ ] Card titles use `FONT_MEDIUM` or `FONT_EXTRABOLD` (18-20pt)
- [ ] Big numbers (stat cards) use `FONT_EXTRABOLD` (48-72pt)
- [ ] Line spacing: 1.3x for body text, 1.4x for bullets, 1.1x for big numbers
- [ ] Maximum 3 font weights used per slide (title + body + accent)
- [ ] Weight contrast is aggressive: 800 vs 400 (never similar weights adjacent)

## File Integrity

- [ ] File saves without errors
- [ ] File size under 50MB
- [ ] File opens in PowerPoint without repair prompts
- [ ] Output path follows convention: `output/[PROJECT]/U[XX]/[PROJECT]_U[XX]_Interactive_Lecture.pptx`
