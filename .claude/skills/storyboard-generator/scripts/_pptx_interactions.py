"""
PPTX Interactions — Quiz, drag-drop, click-reveal, slider, dropdown, scenario.
================================================================================

Contains all interactive slide types that map to Storyline 360 freeform
interactions. Each method produces a fully laid-out slide with named shapes
and Storyline blueprints in the speaker notes.

Architecture:
    This is a MIXIN class. Methods use `self` to access SlideEngine helpers
    from _pptx_core.py (e.g. _add_shape, _add_arabic_textbox, _set_run_font).
    Do NOT import SlideEngine here (circular import).

    The final LectureBuilder composes:
        SlideEngine (base) + DepthMixin + StructuralMixin
        + InteractionsMixin + VisualGrammarMixin

Shape naming conventions (for Storyline Selection Pane):
    btn_*   — Clickable buttons (quiz check, reveal tabs, scenario choices)
    opt_*   — Quiz option badges (letter circles)
    txt_*   — Text elements (questions, instructions, option text)
    bg_*    — Background shapes (option rows, cards)
    icon_*  — Decorative icons (grip handles, step badges)
    drag_*  — Draggable items
    drop_*  — Drop target zones
    num_*   — Numbered elements

Usage:
    class LectureBuilder(StructuralMixin, InteractionsMixin, VisualGrammarMixin,
                         DepthMixin, SlideEngine):
        pass
"""

import os
from typing import Optional

from pptx.util import Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE

from _pptx_core import (
    # Color palette
    PRIMARY_BLUE,
    ACCENT1_BLUE,
    BODY_TEXT,
    WHITE,
    BUTTON_BORDER,
    WARM_GRAY,
    LIGHT_BLUE_BG,
    CONTENT_CARD_BG,
    CONTENT_CARD_BORDER,
    CARD_LIGHT_BG,
    PRIMARY_BLUE_LIGHT,
    PRIMARY_BLUE_DARK,
    # Font names
    FONT_EXTRABOLD,
    FONT_MEDIUM,
    FONT_REGULAR,
    # Positions
    TEXT_MARGIN_LR,
    TEXT_MARGIN_TB,
)


class InteractionsMixin:
    """
    Mixin that adds interactive slide methods to SlideEngine.

    Expects SlideEngine as the base class in the MRO, providing:
        - self._add_shape()
        - self._add_arabic_textbox()
        - self._add_section_banner()
        - self._add_header_bar()
        - self._add_shadow_to_shape()
        - self._set_run_font()
        - self._set_rtl()
        - self._set_slide_title_for_toc()
        - self._add_content_slide_with_layout()
        - self._add_notes()
        - self._add_image()
        - self._generate_image_for_slide()
        - self._calculate_adaptive_spacing()
        - self.slide_count, self.lecture_title
    """

    # ------------------------------------------------------------------
    # QUIZ — Multiple Choice (Pick One)
    # ------------------------------------------------------------------

    def add_quiz_slide(
        self,
        question: str,
        options: list,
        correct_index: int,
        quiz_number: int = 1,
        total_quizzes: int = 5,
        image_path: Optional[str] = None,
        image_prompt: Optional[str] = None,
    ):
        """
        Add an MCQ quiz slide with letter badges and a check-answer button.

        Produces a Storyline-ready Pick One freeform interaction with named
        option shapes (opt_a, opt_b, ...) and a submit button (btn_check).

        Args:
            question: The question text in Arabic
            options: List of answer option strings (2-4 options)
            correct_index: Zero-based index of the correct answer
            quiz_number: Which quiz number this is (for display)
            total_quizzes: Total number of quizzes (for display)
            image_path: Optional illustration next to the question
            image_prompt: Optional prompt to auto-generate an illustration
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        self._set_slide_title_for_toc(slide, f"نشاط: {question[:30]}")
        self._add_header_bar(slide, self.lecture_title)

        activity_title = "نشاط تفاعلي: اختيار من متعدد"
        self._add_section_banner(slide, activity_title, wide=True)

        # Optional question illustration
        if image_prompt and not image_path:
            image_path = self._generate_image_for_slide(image_prompt, "quiz")
        quiz_has_image = False
        if image_path:
            pic = self._add_image(
                slide, image_path,
                left=Cm(2), top=Cm(4),
                max_width=Cm(7), max_height=Cm(5),
                name="img_quiz",
            )
            if pic is not None:
                quiz_has_image = True

        # Question text
        q_left = Cm(10) if quiz_has_image else Cm(2.5)
        q_width = Cm(21) if quiz_has_image else Cm(29)
        self._add_arabic_textbox(
            slide,
            left=q_left,
            top=Cm(5),
            width=q_width,
            height=Cm(2),
            text=question,
            font_name=FONT_EXTRABOLD,
            font_size=Pt(24),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_question",
        )

        # Answer options with letter badges
        arabic_letters = ["أ", "ب", "ج", "د"]
        option_top_start = Cm(7.5)
        option_spacing = Cm(2.2)
        option_height = Cm(1.7)

        for i, option_text in enumerate(options):
            opt_letter = arabic_letters[i] if i < len(arabic_letters) else str(i + 1)
            opt_id = ["a", "b", "c", "d"][i] if i < 4 else str(i + 1)
            option_top = int(option_top_start + i * option_spacing)

            option_bg = CONTENT_CARD_BG if i % 2 == 0 else WHITE
            option_bg_shape = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=Cm(2.5),
                top=option_top - Cm(0.1),
                width=Cm(28),
                height=option_height + Cm(0.2),
                fill_color=option_bg,
                border_color=CONTENT_CARD_BORDER,
                border_width=Pt(0.5),
                name=f"bg_opt_{opt_id}",
                corner_radius=0.06,
            )
            self._add_shadow_to_shape(option_bg_shape, blur_pt=3, opacity_pct=12)

            # Letter badge (circle)
            badge_left = Cm(28.5)
            badge_size = Cm(1.5)
            badge = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=badge_left,
                top=option_top + Cm(0.1),
                width=badge_size,
                height=badge_size,
                fill_color=PRIMARY_BLUE,
                name=f"opt_{opt_id}",
            )
            # Subtle glow makes badge feel interactive/clickable
            self._apply_glow(badge, "#2D588C", radius_pt=4, alpha=40)
            tf = badge.text_frame
            tf.word_wrap = False
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = opt_letter
            self._set_run_font(run, FONT_EXTRABOLD, Pt(16), False, WHITE)

            # Option text
            self._add_arabic_textbox(
                slide,
                left=Cm(3),
                top=option_top,
                width=Cm(24.5),
                height=option_height,
                text=option_text,
                font_name=FONT_REGULAR,
                font_size=Pt(20),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.RIGHT,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_opt_{opt_id}",
            )

        # "Check Answer" button
        check_btn = self._add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left=Cm(10),
            top=Cm(16),
            width=Cm(10),
            height=Cm(1.6),
            fill_color=ACCENT1_BLUE,
            border_color=BUTTON_BORDER,
            border_width=Pt(1.5),
            name="btn_check",
        )
        # Shadow + glow make button feel pressable/interactive
        self._add_shadow_to_shape(check_btn)
        self._apply_glow(check_btn, "#156082", radius_pt=3, alpha=30)
        tf_btn = check_btn.text_frame
        tf_btn.word_wrap = True
        tf_btn.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_btn = tf_btn.paragraphs[0]
        p_btn.alignment = PP_ALIGN.CENTER
        run_btn = p_btn.add_run()
        run_btn.text = "تحقق من الإجابة"
        self._set_run_font(run_btn, FONT_EXTRABOLD, Pt(22), False, WHITE)
        self._set_rtl(p_btn)

        # Structured notes for Storyline import
        correct_letter = arabic_letters[correct_index] if correct_index < len(arabic_letters) else str(correct_index + 1)
        correct_opt_id = ["a", "b", "c", "d"][correct_index] if correct_index < 4 else str(correct_index + 1)
        notes_text = (
            f"=== STORYLINE INSTRUCTIONS ===\n"
            f"Slide Type: Quiz - Multiple Choice\n"
            f"Correct Answer: {correct_letter} (opt_{correct_opt_id})\n"
            f"Feedback (Correct): احسنت! الاجابة صحيحة\n"
            f"Feedback (Incorrect): الاجابة غير صحيحة، حاول مرة اخرى\n"
            f"Points: 10\n"
            f"Attempts: 2\n\n"
            f"=== FREEFORM SETUP ===\n"
            f"1. Insert > Convert to Freeform > Pick One\n"
            f"2. Assign opt_a, opt_b, opt_c, opt_d as choices\n"
            f"3. Set opt_{correct_opt_id} as correct answer\n"
            f"4. btn_check triggers submit\n\n"
            f"=== NARRATOR SCRIPT ===\n"
            f"{question}"
        )
        self._add_notes(slide, notes_text)

    # ------------------------------------------------------------------
    # DRAG & DROP — Ordering / Classification
    # ------------------------------------------------------------------

    def add_drag_drop_slide(
        self,
        question: str,
        items: list,
        correct_order: list,
        quiz_number: int = 1,
    ):
        """
        Add a drag-and-drop interaction slide with grip handles and drop zones.

        Items appear on the left with grip indicators; numbered drop zones
        on the right with dashed borders and "drag here" hint text.

        Args:
            question: Instruction text for the activity
            items: List of item strings that learners will drag
            correct_order: List showing the correct classification/order
            quiz_number: Activity number (for display)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        self._set_slide_title_for_toc(slide, "نشاط: سحب وإفلات")
        self._add_header_bar(slide, self.lecture_title)

        activity_title = "نشاط تفاعلي: سحب وترتيب"
        self._add_section_banner(slide, activity_title, wide=True)

        # Question text
        self._add_arabic_textbox(
            slide,
            left=Cm(2.5),
            top=Cm(5),
            width=Cm(29),
            height=Cm(2),
            text=question,
            font_name=FONT_EXTRABOLD,
            font_size=Pt(20),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_question",
        )

        # Clear instruction text
        self._add_arabic_textbox(
            slide,
            left=Cm(2.5),
            top=Cm(7),
            width=Cm(29),
            height=Cm(1.2),
            text="اسحب العناصر التالية إلى الترتيب الصحيح",
            font_name=FONT_MEDIUM,
            font_size=Pt(18),
            bold=False,
            color=ACCENT1_BLUE,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_instruction",
        )

        # Draggable items (left side)
        item_count = len(items)
        items_area_left = Cm(2.5)
        items_top = Cm(8.5)
        item_width = Cm(12)
        safe_bottom = 6300000

        item_height, gap = self._calculate_adaptive_spacing(
            item_count=item_count,
            available_top=items_top,
            available_bottom=safe_bottom,
            min_item_height=Cm(2),
        )
        item_step = item_height + gap

        for i, item_text in enumerate(items):
            item_top = int(items_top + i * item_step)

            item_shape = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=items_area_left,
                top=item_top,
                width=item_width,
                height=item_height,
                fill_color=CONTENT_CARD_BG,
                border_color=PRIMARY_BLUE,
                border_width=Pt(1.5),
                name=f"drag_item_{i + 1}",
            )
            self._add_shadow_to_shape(item_shape)
            tf = item_shape.text_frame
            tf.word_wrap = True
            tf.margin_left = TEXT_MARGIN_LR
            tf.margin_right = TEXT_MARGIN_LR
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = item_text
            self._set_run_font(run, FONT_REGULAR, Pt(20), False, BODY_TEXT)
            self._set_rtl(p)

            # Grip indicator (hamburger icon)
            self._add_arabic_textbox(
                slide,
                left=items_area_left + Cm(0.2),
                top=item_top + Cm(0.2),
                width=Cm(1),
                height=Cm(1),
                text="\u2630",
                font_name=FONT_REGULAR,
                font_size=Pt(14),
                bold=False,
                color=WARM_GRAY,
                alignment=PP_ALIGN.LEFT,
                word_wrap=False,
                auto_size=MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT,
                name=f"icon_grip_{i + 1}",
            )

        # Numbered drop positions (right side)
        drop_left = Cm(18)
        drop_width = Cm(12)
        for i in range(item_count):
            drop_top = int(items_top + i * item_step)

            drop_shape = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=drop_left,
                top=drop_top,
                width=drop_width,
                height=item_height,
                name=f"drop_zone_{i + 1}",
                fill_color=CARD_LIGHT_BG,
                border_color=CONTENT_CARD_BORDER,
                border_width=Pt(1.5),
            )
            drop_shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH

            drop_tf = drop_shape.text_frame
            drop_tf.word_wrap = True
            drop_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_hint = drop_tf.paragraphs[0]
            p_hint.alignment = PP_ALIGN.CENTER
            run_hint = p_hint.add_run()
            run_hint.text = "اسحب هنا"
            self._set_run_font(run_hint, FONT_REGULAR, Pt(14), False, WARM_GRAY)
            self._set_rtl(p_hint)

            # Number badge in drop zone
            badge_size = Cm(1.5)
            badge = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=drop_left + drop_width - badge_size - Cm(0.3),
                top=drop_top + (item_height - badge_size) // 2,
                width=badge_size,
                height=badge_size,
                fill_color=PRIMARY_BLUE,
            )
            tf_b = badge.text_frame
            tf_b.word_wrap = False
            tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_b = tf_b.paragraphs[0]
            p_b.alignment = PP_ALIGN.CENTER
            run_b = p_b.add_run()
            run_b.text = str(i + 1)
            self._set_run_font(run_b, FONT_EXTRABOLD, Pt(16), False, WHITE)

        # Structured notes for Storyline import
        mapping_lines = "\n".join(
            f"drag_item_{i+1} → drop_zone_{i+1}: {correct_order[i]}"
            for i in range(len(correct_order))
        )
        notes_text = (
            f"=== STORYLINE INSTRUCTIONS ===\n"
            f"Slide Type: Drag and Drop - Ordering\n"
            f"Correct Order:\n{mapping_lines}\n\n"
            f"=== FREEFORM SETUP ===\n"
            f"1. Insert > Convert to Freeform > Drag and Drop\n"
            f"2. Match drag_item shapes to drop_zone shapes\n"
            f"3. Set correct order as shown above\n\n"
            f"=== NARRATOR SCRIPT ===\n"
            f"{question}"
        )
        self._add_notes(slide, notes_text)

    # ------------------------------------------------------------------
    # CLICK-REVEAL — Tabs / Expandable List
    # ------------------------------------------------------------------

    def add_click_reveal_slide(
        self,
        title: str,
        instruction: str,
        reveal_items: list,
        notes: str = "",
    ):
        """
        Add a click-to-reveal interaction slide with tabs or vertical list.

        For 4 or fewer items: horizontal tab layout with a description area.
        For 5+ items: vertical list layout with numbered badges.

        Args:
            title: Section title
            instruction: Instruction text shown above the interaction
            reveal_items: List of dicts with "label" and "description" (or "detail")
            notes: Additional speaker notes (prepended to Storyline instructions)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        self._set_slide_title_for_toc(slide, title)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)

        # Instruction text
        self._add_arabic_textbox(
            slide,
            left=Cm(2.5),
            top=Cm(4.5),
            width=Cm(29),
            height=Cm(1.5),
            text=instruction,
            font_name=FONT_MEDIUM,
            font_size=Pt(18),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_instruction",
        )

        tab_count = len(reveal_items)

        if tab_count > 4:
            # VERTICAL LIST layout for 5+ items
            list_top_start = Cm(6.5)
            list_left = Cm(2.5)
            list_width = Cm(28.5)
            safe_bottom = 6300000

            row_height, row_gap = self._calculate_adaptive_spacing(
                item_count=tab_count,
                available_top=list_top_start,
                available_bottom=safe_bottom,
                min_item_height=Cm(1.8),
            )
            row_step = row_height + row_gap

            for i, item in enumerate(reveal_items):
                reveal_num = i + 1
                row_top = int(list_top_start + i * row_step)

                row_bg = CONTENT_CARD_BG if i % 2 == 0 else WHITE
                self._add_shape(
                    slide,
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    left=list_left,
                    top=row_top,
                    width=list_width,
                    height=row_height,
                    fill_color=row_bg,
                    border_color=CONTENT_CARD_BORDER,
                    border_width=Pt(1),
                    name=f"bg_reveal_{reveal_num}",
                )

                badge_size = Cm(1.5)
                badge = self._add_shape(
                    slide,
                    MSO_SHAPE.OVAL,
                    left=list_left + list_width - badge_size - Cm(0.3),
                    top=row_top + (row_height - badge_size) // 2,
                    width=badge_size,
                    height=badge_size,
                    fill_color=PRIMARY_BLUE,
                    name=f"btn_reveal_{reveal_num}",
                )
                tf_b = badge.text_frame
                tf_b.word_wrap = False
                tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
                p_b = tf_b.paragraphs[0]
                p_b.alignment = PP_ALIGN.CENTER
                run_b = p_b.add_run()
                run_b.text = str(i + 1)
                self._set_run_font(run_b, FONT_EXTRABOLD, Pt(16), False, WHITE)

                self._add_arabic_textbox(
                    slide,
                    left=list_left + Cm(0.5),
                    top=row_top,
                    width=list_width - badge_size - Cm(1.5),
                    height=row_height,
                    text=item.get("label", ""),
                    font_name=FONT_EXTRABOLD,
                    font_size=Pt(20),
                    bold=False,
                    color=BODY_TEXT,
                    alignment=PP_ALIGN.RIGHT,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_reveal_{reveal_num}",
                )
        else:
            # HORIZONTAL TABS layout for 4 or fewer items
            tab_area_left = Cm(2.5)
            tab_area_width = Cm(28.5)
            tab_top = Cm(7)
            tab_height = Cm(2.5)
            gap = Cm(0.5)

            total_gaps = gap * (tab_count - 1) if tab_count > 1 else 0
            tab_width = int((tab_area_width - total_gaps) / tab_count)

            for i, item in enumerate(reveal_items):
                tab_left = int(tab_area_left + i * (tab_width + gap))

                is_active = (i == 0)
                # Active tab: bold primary blue with shadow
                # Inactive tabs: light gray background for clear contrast
                tab_fill = PRIMARY_BLUE if is_active else CONTENT_CARD_BG
                tab_border = None if is_active else CONTENT_CARD_BORDER
                tab_text_color = WHITE if is_active else BODY_TEXT
                tab_shape = self._add_shape(
                    slide,
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    left=tab_left,
                    top=tab_top,
                    width=tab_width,
                    height=tab_height,
                    fill_color=tab_fill,
                    border_color=tab_border,
                    border_width=Pt(1) if tab_border else None,
                    name=f"btn_reveal_{i + 1}",
                    corner_radius=0.08,
                )
                # Active tab stands out with shadow
                if is_active:
                    self._add_shadow_to_shape(tab_shape)
                tf = tab_shape.text_frame
                tf.word_wrap = True
                tf.margin_left = TEXT_MARGIN_LR
                tf.margin_right = TEXT_MARGIN_LR
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                run.text = item.get("label", "")
                self._set_run_font(run, FONT_EXTRABOLD, Pt(18), False, tab_text_color)
                self._set_rtl(p)

            # Description area below tabs
            self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=Cm(2.5),
                top=Cm(10.5),
                width=Cm(28.5),
                height=Cm(5),
                fill_color=LIGHT_BLUE_BG,
                border_color=PRIMARY_BLUE,
                name="bg_reveal_desc",
            )

            # Left accent bar on description area
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=Cm(30.5),
                top=Cm(10.5),
                width=Cm(0.4),
                height=Cm(5),
                fill_color=PRIMARY_BLUE,
                name="accent_desc_bar",
            )

            # First item's description as default visible text
            if reveal_items:
                self._add_arabic_textbox(
                    slide,
                    left=Cm(3),
                    top=Cm(11),
                    width=Cm(27.5),
                    height=Cm(4),
                    text=reveal_items[0].get("description", reveal_items[0].get("detail", "")),
                    font_name=FONT_REGULAR,
                    font_size=Pt(18),
                    bold=False,
                    color=BODY_TEXT,
                    alignment=PP_ALIGN.RIGHT,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name="txt_reveal_desc",
                )

        # Structured notes for Storyline import
        btn_names = ", ".join(f"btn_reveal_{i+1}" for i in range(tab_count))
        layer_lines = "\n".join(
            f"Layer {i+1}: Show content when btn_reveal_{i+1} clicked — {item.get('label', '')}"
            for i, item in enumerate(reveal_items)
        )
        all_descriptions = "\n".join(
            f"btn_reveal_{i+1} ({item.get('label', '')}): {item.get('description', item.get('detail', ''))}"
            for i, item in enumerate(reveal_items)
        )
        structured_notes = (
            f"=== STORYLINE INSTRUCTIONS ===\n"
            f"Slide Type: Click to Reveal\n"
            f"Items: {btn_names}\n\n"
            f"=== LAYER INSTRUCTIONS ===\n"
            f"{layer_lines}\n\n"
            f"=== CONTENT ===\n"
            f"{all_descriptions}"
        )
        if notes:
            structured_notes = f"{notes}\n\n{structured_notes}"
        self._add_notes(slide, structured_notes)

    # ------------------------------------------------------------------
    # SLIDER — Step-through / Scroll interaction
    # ------------------------------------------------------------------

    def add_slider_slide(
        self,
        title: str,
        items: list,
        notes: str = "",
    ):
        """
        Add a slider/scroll interaction slide with numbered step badges.

        Each item gets a numbered circle badge on the right (RTL) and
        body text on the left. Used for sequential processes or steps.

        Args:
            title: Instruction text for the interaction
            items: List of dicts with "number" and "text" for each step,
                   or simple strings
            notes: Speaker notes / Storyline instructions
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        self._set_slide_title_for_toc(slide, title)
        self._add_header_bar(slide, self.lecture_title)

        # Title/Instructions
        self._add_arabic_textbox(
            slide,
            left=Cm(2.5),
            top=Cm(2.5),
            width=Cm(29),
            height=Cm(2),
            text=title,
            font_name=FONT_MEDIUM,
            font_size=Pt(18),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_instruction",
        )

        # Numbered items
        item_top_start = Cm(5)
        item_spacing = Cm(2)

        # Vertical progress track line connecting all badges
        # Drawn BEFORE badges so it appears behind them
        if len(items) > 1:
            badge_center_x = Cm(28) + Cm(0.75) - Cm(0.15)  # Center of badges minus half line width
            first_badge_center_y = item_top_start + Cm(0.75)  # Center of first badge
            last_badge_center_y = int(item_top_start + (len(items) - 1) * item_spacing) + Cm(0.75)
            track_height = last_badge_center_y - first_badge_center_y
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=badge_center_x,
                top=first_badge_center_y,
                width=Cm(0.3),
                height=track_height,
                fill_color=PRIMARY_BLUE_LIGHT,
                name="bg_progress_track",
            )

        for i, item_data in enumerate(items):
            item_top = int(item_top_start + i * item_spacing)
            slider_num = i + 1

            number = item_data.get("number", str(i + 1)) if isinstance(item_data, dict) else str(i + 1)
            text = item_data.get("text", str(item_data)) if isinstance(item_data, dict) else str(item_data)

            # Number badge
            badge = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=Cm(28),
                top=item_top,
                width=Cm(1.5),
                height=Cm(1.5),
                fill_color=PRIMARY_BLUE,
                name=f"icon_step_{slider_num}",
            )
            tf = badge.text_frame
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = number
            self._set_run_font(run, FONT_EXTRABOLD, Pt(16), False, WHITE)

            # Item text
            self._add_arabic_textbox(
                slide,
                left=Cm(3),
                top=item_top,
                width=Cm(24),
                height=Cm(1.5),
                text=text,
                font_name=FONT_REGULAR,
                font_size=Pt(18),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.RIGHT,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_step_{slider_num}",
            )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # DROPDOWN — Matching activity
    # ------------------------------------------------------------------

    def add_dropdown_slide(
        self,
        title: str,
        instruction: str,
        items: list,
        notes: str = "",
    ):
        """
        Add a dropdown matching activity slide.

        Each item has a statement on the right and a dropdown indicator
        button on the left. Correct answers are stored in speaker notes.

        Args:
            title: Activity title
            instruction: Instruction text shown above the items
            items: List of dicts with "text" (the statement) and
                   "correct" (the correct dropdown value)
            notes: Additional speaker notes
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        self._set_slide_title_for_toc(slide, title)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)

        # Instruction text
        self._add_arabic_textbox(
            slide,
            left=Cm(2.5),
            top=Cm(4.5),
            width=Cm(29),
            height=Cm(2),
            text=instruction,
            font_name=FONT_MEDIUM,
            font_size=Pt(18),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_instruction",
        )

        # Statement rows with dropdown indicators
        row_top_start = Cm(7)
        safe_bottom = 6300000

        dd_row_height, dd_row_gap = self._calculate_adaptive_spacing(
            item_count=len(items),
            available_top=row_top_start,
            available_bottom=safe_bottom,
            min_item_height=Cm(1.8),
        )
        dd_row_step = dd_row_height + dd_row_gap

        for i, item_data in enumerate(items):
            dd_num = i + 1
            row_top = int(row_top_start + i * dd_row_step)

            self._add_arabic_textbox(
                slide,
                left=Cm(7),
                top=row_top,
                width=Cm(22),
                height=dd_row_height,
                text=item_data.get("text", ""),
                font_name=FONT_REGULAR,
                font_size=Pt(18),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.RIGHT,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_statement_{dd_num}",
            )

            dropdown = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=Cm(2.5),
                top=row_top,
                width=Cm(4),
                height=dd_row_height,
                fill_color=WHITE,
                border_color=PRIMARY_BLUE,
                name=f"btn_dropdown_{dd_num}",
            )
            # Shadow + glow make dropdown feel interactive
            self._add_shadow_to_shape(dropdown, blur_pt=3, opacity_pct=12)
            self._apply_glow(dropdown, "#2D588C", radius_pt=2, alpha=20)
            tf = dropdown.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = "\u25BC"
            self._set_run_font(run, FONT_EXTRABOLD, Pt(18), False, PRIMARY_BLUE)

        # Notes with correct answers
        correct_text = "\n".join(
            f"{item.get('text', '')[:40]}... \u2192 {item.get('correct', '')}"
            for item in items
        )
        notes_text = notes if notes else f"\u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0627\u0644\u0635\u062d\u064a\u062d\u0629:\n{correct_text}"
        self._add_notes(slide, notes_text)

    # ------------------------------------------------------------------
    # SCENARIO — Branching decision interaction (NEW)
    # ------------------------------------------------------------------

    def add_scenario_slide(
        self,
        title: str,
        situation: str,
        choices: list,
        correct_index: int = 0,
        notes: str = "",
    ):
        """
        Add a branching scenario slide with a situation and decision choices.

        Presents a scenario description in a full-width card, followed by
        2-3 choice buttons styled as decision cards. The correct choice
        and Storyline layer blueprints are stored in speaker notes.

        Args:
            title: Scenario title (e.g., "سيناريو: التعامل مع البيانات")
            situation: The scenario description text (what happened / context)
            choices: List of choice strings (2-3 options the learner picks from)
            correct_index: Zero-based index of the correct choice (default: 0)
            notes: Additional speaker notes (prepended to Storyline blueprint)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        self._set_slide_title_for_toc(slide, title)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)

        # --- Situation description card (full width) ---
        situation_card = self._add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left=Cm(2.5),
            top=Cm(4.5),
            width=Cm(28.5),
            height=Cm(5),
            fill_color=CONTENT_CARD_BG,
            border_color=CONTENT_CARD_BORDER,
            border_width=Pt(1),
            name="bg_situation",
            corner_radius=0.04,
        )
        self._add_shadow_to_shape(situation_card, blur_pt=4, opacity_pct=15)

        # Accent bar on right side of situation card (RTL emphasis)
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=Cm(30.5),
            top=Cm(4.5),
            width=Cm(0.4),
            height=Cm(5),
            fill_color=PRIMARY_BLUE,
            name="accent_situation_bar",
        )

        # Situation text
        self._add_arabic_textbox(
            slide,
            left=Cm(3.5),
            top=Cm(5),
            width=Cm(26.5),
            height=Cm(4),
            text=situation,
            font_name=FONT_REGULAR,
            font_size=Pt(20),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="txt_situation",
        )

        # --- Choice buttons (styled as decision cards) ---
        choice_count = len(choices)
        choices_area_left = Cm(2.5)
        choices_area_width = Cm(28.5)
        choices_top = Cm(10.5)
        choice_height = Cm(3.5)
        choice_gap = Cm(0.8)

        total_gaps = choice_gap * (choice_count - 1) if choice_count > 1 else 0
        choice_width = int((choices_area_width - total_gaps) / choice_count)

        # Color scheme for choice cards
        choice_colors = [PRIMARY_BLUE, ACCENT1_BLUE, PRIMARY_BLUE_DARK]

        for i, choice_text in enumerate(choices):
            choice_left = int(choices_area_left + i * (choice_width + choice_gap))
            card_color = choice_colors[i % len(choice_colors)]

            # Choice card background
            choice_card = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=choice_left,
                top=choices_top,
                width=choice_width,
                height=choice_height,
                fill_color=card_color,
                name=f"btn_choice_{i}",
                corner_radius=0.06,
            )
            self._add_shadow_to_shape(choice_card, blur_pt=5, opacity_pct=20)

            # Choice number badge (small circle in top-right corner)
            badge_size = Cm(1.3)
            badge = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=choice_left + choice_width - badge_size - Cm(0.3),
                top=choices_top + Cm(0.3),
                width=badge_size,
                height=badge_size,
                fill_color=WHITE,
                name=f"icon_choice_{i}",
            )
            tf_badge = badge.text_frame
            tf_badge.word_wrap = False
            tf_badge.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_badge = tf_badge.paragraphs[0]
            p_badge.alignment = PP_ALIGN.CENTER
            run_badge = p_badge.add_run()
            run_badge.text = str(i + 1)
            self._set_run_font(run_badge, FONT_EXTRABOLD, Pt(14), False, card_color)

            # Choice text
            self._add_arabic_textbox(
                slide,
                left=choice_left + Cm(0.5),
                top=choices_top + Cm(0.8),
                width=choice_width - Cm(1),
                height=choice_height - Cm(1),
                text=choice_text,
                font_name=FONT_MEDIUM,
                font_size=Pt(18),
                bold=False,
                color=WHITE,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_choice_{i}",
            )

        # --- "Choose your decision" prompt ---
        self._add_arabic_textbox(
            slide,
            left=Cm(2.5),
            top=Cm(9.5),
            width=Cm(28.5),
            height=Cm(1),
            text="اختر القرار المناسب:",
            font_name=FONT_EXTRABOLD,
            font_size=Pt(18),
            bold=False,
            color=PRIMARY_BLUE,
            alignment=PP_ALIGN.RIGHT,
            word_wrap=False,
            auto_size=MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT,
            name="txt_choose_prompt",
        )

        # --- Structured notes for Storyline import ---
        btn_names = ", ".join(f"btn_choice_{i}" for i in range(choice_count))
        layer_lines = "\n".join(
            f"Layer 'outcome_{i}': Shows feedback when btn_choice_{i} clicked"
            for i in range(choice_count)
        )
        correct_btn = f"btn_choice_{correct_index}"

        storyline_notes = (
            f"=== STORYLINE INSTRUCTIONS ===\n"
            f"Slide Type: Branching Scenario\n"
            f"Correct Choice: btn_choice_{correct_index} (Choice {correct_index + 1})\n"
            f"Choice Buttons: {btn_names}\n\n"
            f"=== LAYER SETUP ===\n"
            f"{layer_lines}\n\n"
            f"=== TRIGGER SETUP ===\n"
        )
        for i in range(choice_count):
            is_correct = "CORRECT" if i == correct_index else "INCORRECT"
            storyline_notes += (
                f"Trigger {i+1}: Show layer 'outcome_{i}' when user clicks btn_choice_{i} "
                f"[{is_correct}]\n"
            )

        storyline_notes += (
            f"\n=== FEEDBACK CONTENT ===\n"
            f"outcome_{correct_index} (Correct): احسنت! هذا هو القرار الصحيح.\n"
        )
        for i in range(choice_count):
            if i != correct_index:
                storyline_notes += (
                    f"outcome_{i} (Incorrect): هذا ليس القرار الأفضل. حاول مرة أخرى.\n"
                )

        storyline_notes += (
            f"\n=== NARRATOR SCRIPT ===\n"
            f"{situation}"
        )

        if notes:
            storyline_notes = f"{notes}\n\n{storyline_notes}"
        self._add_notes(slide, storyline_notes)
