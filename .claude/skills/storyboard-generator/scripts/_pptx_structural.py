"""
PPTX Structural Slides — Title, objectives, section dividers, summary, closing.
These slides provide the lecture framework (beginning, sections, ending).

Architecture:
    This is a MIXIN class. Methods use `self` to access SlideEngine helpers
    from _pptx_core.py. Do NOT import SlideEngine here (circular import).

    The final LectureBuilder composes:
        SlideEngine (base) + DepthMixin + StructuralMixin + ...
"""
from _pptx_core import *  # Import all constants, colors, fonts, positions


class StructuralMixin:
    """Mixin that adds structural slide methods to SlideEngine."""

    def add_title_slide(
        self,
        title: str,
        subtitle: str = "",
        start_button_text: str = "ابدأ المحاضرة",
    ):
        """
        Add the opening title slide (matches template slide 1).

        This is the first thing learners see — it shows the institution
        name, lecture title, and a "Start" button.

        Args:
            title: Main lecture title (e.g., "المحاضرة الأولى")
            subtitle: Subtitle text (e.g., "مقدمة في علوم الحاسوب")
            start_button_text: Text for the start button (default: "ابدأ المحاضرة")

        Visual output (ASCII mockup):
            +------------------------------------------+
            |  [=== Blue header decoration bar ===]    |
            |                                          |
            |                                          |
            |              [Institution Name]          |
            |                                          |
            |              [Lecture Title:]             |
            |              [Subtitle]                  |
            |                                          |
            |              [  ابدأ المحاضرة  ]         |
            +------------------------------------------+

        Example:
            >>> builder.add_title_slide(
            ...     title="المحاضرة الأولى:",
            ...     subtitle="المهارات الرقميّة: المشهد التحوليّ"
            ... )
        """
        self.slide_count += 1

        # Store the lecture title for reuse on other slides
        # Combines title + subtitle for the top bar on subsequent slides
        self.lecture_title = f"{title} {subtitle}".strip()

        # Use Layout 0 ("Title Slide") — has background image, logo, etc.
        slide = self._add_slide_with_layout(0)

        # Set hidden TOC title for Storyline sidebar menu
        self._set_slide_title_for_toc(slide, title)

        # --- Institution name ---
        # Positioned in the right-center area (RTL layout puts content on right)
        self._add_arabic_textbox(
            slide,
            left=6096000,       # ~16.93cm from left
            top=3198167,        # ~8.88cm from top
            width=5181600,      # ~14.39cm wide
            height=461665,      # ~1.28cm tall
            text=self.institution,
            font_name=FONT_EXTRABOLD,
            font_size=Pt(24),
            bold=False,
            color=PRIMARY_BLUE,
            alignment=PP_ALIGN.CENTER,
            name="txt_institution",
        )

        # --- Lecture title + subtitle in a single textbox (template uses 1 box) ---
        title_box = slide.shapes.add_textbox(6096000, 4257368, 5181600, 1077218)
        title_box.name = "txt_title"
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
        tf.margin_left = TEXT_MARGIN_LR
        tf.margin_right = TEXT_MARGIN_LR
        tf.margin_top = TEXT_MARGIN_TB
        tf.margin_bottom = TEXT_MARGIN_TB

        # Title paragraph
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        run1 = p1.add_run()
        run1.text = title
        self._set_run_font(run1, FONT_EXTRABOLD, Pt(24), False, PRIMARY_BLUE)
        self._set_rtl(p1)

        # Subtitle paragraph (in the same textbox, as 3rd paragraph)
        if subtitle:
            # Empty line between title and subtitle
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            run2 = p2.add_run()
            run2.text = subtitle
            self._set_run_font(run2, FONT_EXTRABOLD, Pt(20), False, SUBTITLE_TEXT)
            self._set_rtl(p2)

        # --- Start button ---
        # Rounded rectangle with accent1 blue fill (#156082) and dark border
        button = self._add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left=7398084,       # ~20.55cm
            top=5599525,        # ~15.55cm
            width=2773680,      # ~7.7cm
            height=665193,      # ~1.85cm
            fill_color=ACCENT1_BLUE,   # accent1 #156082 (not #2D588C)
            border_color=BUTTON_BORDER,
            border_width=Pt(1.5),
            name="btn_start",
        )
        # Add text to the button
        tf_btn = button.text_frame
        tf_btn.word_wrap = True
        tf_btn.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_btn.margin_left = TEXT_MARGIN_LR
        tf_btn.margin_right = TEXT_MARGIN_LR
        tf_btn.margin_top = TEXT_MARGIN_TB
        tf_btn.margin_bottom = TEXT_MARGIN_TB
        p = tf_btn.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = start_button_text
        self._set_run_font(run, FONT_REGULAR, Pt(20), False, WHITE)
        self._set_rtl(p)

        # --- Play icon (triangle) to the right of the button ---
        play_path = os.path.join(self.assets_dir, ASSET_PLAY_ICON)
        if os.path.exists(play_path):
            pic = slide.shapes.add_picture(
                play_path,
                9476078,    # left
                5599525,    # top
                619211,     # width
                657317,     # height
            )
            pic.name = "icon_play"

        # --- Hand cursor icon below the button ---
        hand_path = os.path.join(self.assets_dir, ASSET_HAND_CURSOR)
        if os.path.exists(hand_path):
            pic = slide.shapes.add_picture(
                hand_path,
                7570916,    # left
                5888428,    # top
                724001,     # width
                752580,     # height
            )
            pic.name = "icon_hand"

        # Add Storyline import instructions as speaker notes
        self._add_notes(slide, self._build_import_instructions(title))

    def add_objectives_slide(self, objectives: list):
        """
        Add a Learning Objectives slide (matches template slide 2).

        Shows numbered objectives in RTL with colored accent bars as
        row backgrounds for each objective.

        Args:
            objectives: List of objective strings in Arabic.
                        Typically 3-5 objectives per lecture.

        Visual output (ASCII mockup):
            +------------------------------------------+
            | [Title Bar: Lecture Name]                 |
            |          [الأهداف التعليمية]              |
            | يتوقع منك في نهاية هذه المحاضرة...       |
            |                                          |
            | [===== Objective Row 1 (colored bg) =====]|
            | [===== Objective Row 2 (colored bg) =====]|
            | [===== Objective Row 3 (colored bg) =====]|
            |                                          |
            | [2]                                       |
            +------------------------------------------+

        Example:
            >>> builder.add_objectives_slide([
            ...     "تعريف ماهي التقنية الناشئة.",
            ...     "التعرف إلى فوائد التقنيات الرقميّة.",
            ...     "اكتشاف عيوب التقنية الرقميّة.",
            ... ])
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        # Set hidden TOC title for Storyline sidebar menu
        self._set_slide_title_for_toc(slide, "الأهداف التعليمية")

        # --- Lecture title bar at top ---
        self._add_header_bar(slide, self.lecture_title)

        # --- Section banner (PNG image instead of colored rectangle) ---
        self._add_section_banner(slide, "الأهداف التعليمية")

        # --- Intro text ---
        # "يتوقع منك في نهاية هذه المحاضرة أن تكون قادرًا على:"
        self._add_arabic_textbox(
            slide,
            left=6280654,       # ~17.45cm
            top=1830945,        # ~5.09cm
            width=5361940,      # ~14.89cm
            height=369332,
            text="يتوقع منك في نهاية هذه المحاضرة أن تكون قادرًا على:",
            font_name=FONT_MEDIUM,
            font_size=Pt(18),
            bold=False,
            color=BODY_TEXT,
            alignment=PP_ALIGN.RIGHT,
            name="txt_obj_intro",
        )

        # --- Objective rows ---
        # Each objective gets a gradient PNG background bar + target icon + text
        # Adaptive spacing: fits up to 8 objectives without overflow
        row_top_start = 2315612     # ~6.43cm from top
        row_left = 612770           # ~1.7cm from left
        row_width = 11029824        # ~30.64cm wide
        safe_bottom = 6300000       # Safe zone above page number

        # Adaptive row sizing — shrinks to fit more items
        preferred_row_height = 600002   # ~1.67cm
        row_height, row_spacing = self._calculate_adaptive_spacing(
            item_count=len(objectives),
            available_top=row_top_start,
            available_bottom=safe_bottom,
            min_item_height=preferred_row_height,
        )
        # row_spacing here is the full gap; convert to "step" = height + gap
        row_step = row_height + row_spacing

        # Paths for PNG row assets
        row_img_path = os.path.join(self.assets_dir, ASSET_OBJECTIVE_ROW)
        icon_img_path = os.path.join(self.assets_dir, ASSET_TARGET_ICON)

        for i, objective in enumerate(objectives):
            row_top = row_top_start + (i * row_step)

            # Background gradient bar (image6.png) — the template uses a PNG
            obj_num = i + 1
            if os.path.exists(row_img_path):
                pic = slide.shapes.add_picture(
                    row_img_path,
                    row_left,
                    row_top,
                    row_width,
                    row_height,
                )
                pic.name = f"bg_obj_{obj_num}"
            else:
                # Fallback: colored rectangle if PNG not found
                self._add_shape(
                    slide,
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    left=row_left,
                    top=row_top,
                    width=row_width,
                    height=row_height,
                    fill_color=LIGHT_BLUE_BG,
                    name=f"bg_obj_{obj_num}",
                )

            # Target/circle icon at the right end of the row (image13.png)
            icon_left = 10922693   # from template
            icon_width = 703228
            if os.path.exists(icon_img_path):
                pic = slide.shapes.add_picture(
                    icon_img_path,
                    icon_left,
                    row_top,
                    icon_width,
                    row_height,
                )
                pic.name = f"icon_obj_{obj_num}"

            # Objective text — positioned within the row
            text_left = 1462617   # ~4.06cm
            text_width = 9443403  # ~26.23cm
            text_height = 338554  # ~0.94cm
            # Center text vertically within the row
            text_top = row_top + (row_height - text_height) // 2

            self._add_arabic_textbox(
                slide,
                left=text_left,
                top=text_top,
                width=text_width,
                height=text_height,
                text=objective,
                font_name=FONT_REGULAR,
                font_size=Pt(18),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.RIGHT,
                name=f"txt_obj_{obj_num}",
            )

    def add_section_divider(
        self,
        section_title: str,
        section_subtitle: str = "",
        section_number: int = None,
        total_sections: int = None,
        image_path: Optional[str] = None,
        image_prompt: Optional[str] = None,
    ):
        """
        Add a full-color section transition slide with decorative elements.

        Used to mark the boundary between major sections of the lecture
        (e.g., transitioning from "Introduction" to "Main Content").

        Enhanced with:
        - Decorative corner images (top-right, bottom-left) from template assets
        - Thicker accent bar on the right side (RTL primary side)
        - Progress dots showing current section position
        - Optional background illustration

        Args:
            section_title: Main section title
            section_subtitle: Optional subtitle text
            section_number: Current section number (1-based) for progress dots
            total_sections: Total number of sections for progress dots
            image_path: Optional path to a subtle background illustration (PNG)
            image_prompt: Optional prompt to auto-generate a background illustration

        Visual output (ASCII mockup):
            +------------------------------------------+
            |                             [corner_tr] +|
            |  ++++++++++++++++++++++++++++++++++++ +  |
            |  ++                              ++  +  |
            |  ++      [Section Title]         ++  +  |
            |  ++      [Section Subtitle]      ++  +  |
            |  ++                              ++     |
            |  ++++++++++++++++++++++++++++++++++++    |
            | [corner_bl]       . . O . .              |
            +------------------------------------------+

        Example:
            >>> builder.add_section_divider(
            ...     section_title="المحور الثاني",
            ...     section_subtitle="فوائد التقنية الرقمية",
            ...     section_number=2,
            ...     total_sections=5,
            ... )
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        # Set hidden TOC title for Storyline sidebar menu
        self._set_slide_title_for_toc(slide, section_title)

        # --- Bold PRIMARY_BLUE background with gradient for visual impact ---
        # Full-color rectangle covering most of the slide
        card_margin_h = Cm(2)
        card_margin_v = Cm(2)
        bg_shape = self._add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left=card_margin_h,
            top=card_margin_v,
            width=SLIDE_WIDTH - (card_margin_h * 2),
            height=SLIDE_HEIGHT - (card_margin_v * 2),
            fill_color=DIVIDER_BG,
            name="bg_divider",
        )
        # Subtle diagonal gradient adds depth to divider slides
        self._apply_gradient_fill(bg_shape, "#2D588C", "#1E3D63", angle=135)

        # --- Subtle depth overlay at bottom edge (darker strip for depth) ---
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=card_margin_h,
            top=SLIDE_HEIGHT - Cm(4),
            width=SLIDE_WIDTH - (card_margin_h * 2),
            height=Cm(2),
            fill_color=PRIMARY_BLUE_DARK,
            name="bg_divider_depth",
        )

        # --- Refined accent bar on the right (RTL primary side) ---
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=SLIDE_WIDTH - Cm(2.5),
            top=Cm(2),
            width=Cm(0.3),
            height=SLIDE_HEIGHT - Cm(4),
            fill_color=WHITE,
            name="accent_right_bar",
        )

        # --- Optional background illustration (behind text, above bg) ---
        # Auto-generate image if prompt provided but no path
        if image_prompt and not image_path:
            image_path = self._generate_image_for_slide(image_prompt, "section")
        if image_path:
            self._add_image(
                slide, image_path,
                left=Cm(3), top=Cm(3),
                max_width=Cm(8), max_height=Cm(8),
                name="img_section_bg",
            )

        # --- Decorative corners — code-drawn shapes (no blurry PNGs) ---
        self._add_decorative_corner(slide, "top_right", WHITE, Cm(4))
        self._add_decorative_corner(slide, "bottom_left", WHITE, Cm(4))

        # --- Section title — large white text, moved up for better balance ---
        title_box = self._add_arabic_textbox(
            slide,
            left=Cm(4),
            top=Cm(5),
            width=Cm(26),
            height=Cm(3.5),
            text=section_title,
            font_name=FONT_EXTRABOLD,
            font_size=Pt(40),
            bold=False,
            color=WHITE,
            alignment=PP_ALIGN.CENTER,
            name="txt_section_title",
        )
        title_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

        # --- Thin decorative white line — increased gap below title ---
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=Cm(9),
            top=Cm(8.7),
            width=Cm(15),
            height=Cm(0.08),
            fill_color=WHITE,
            name="divider_line",
        )

        # --- Section subtitle — more room between line and subtitle ---
        if section_subtitle:
            self._add_arabic_textbox(
                slide,
                left=Cm(4),
                top=Cm(9.3),
                width=Cm(26),
                height=Cm(2.5),
                text=section_subtitle,
                font_name=FONT_MEDIUM,
                font_size=Pt(24),
                bold=False,
                color=WHITE,
                alignment=PP_ALIGN.CENTER,
                name="txt_section_subtitle",
            )

        # --- Progress dots showing current section position ---
        if section_number is not None and total_sections is not None:
            dot_size = Cm(0.6)
            dot_gap = Cm(1)
            total_width = total_sections * dot_size + (total_sections - 1) * dot_gap
            dots_left = (SLIDE_WIDTH - total_width) // 2
            dots_top = SLIDE_HEIGHT - Cm(3)

            for i in range(total_sections):
                dot_left = int(dots_left + i * (dot_size + dot_gap))
                is_current = (i + 1) == section_number
                dot_color = WHITE if is_current else RGBColor(0x80, 0x9F, 0xBF)
                dot_shape_size = Cm(0.8) if is_current else dot_size
                dot_offset = (dot_shape_size - dot_size) // 2 if is_current else 0

                self._add_shape(
                    slide,
                    MSO_SHAPE.OVAL,
                    left=dot_left - dot_offset,
                    top=dots_top - dot_offset,
                    width=dot_shape_size,
                    height=dot_shape_size,
                    fill_color=dot_color,
                    name=f"dot_section_{i + 1}",
                )

    def add_summary_slide(self, summary_items: list):
        """
        Add a summary/recap slide (matches template slide 8).

        Shows key takeaways from the lecture in a list format
        with blue link-style text.

        Args:
            summary_items: List of dicts with:
                - "title": Summary item title (optional)
                - "text": Summary text

                OR simply a list of strings for plain summary points.

        Visual output (ASCII mockup):
            +------------------------------------------+
            | [Title Bar: Lecture Name]                 |
            | [ملخص الوحدة الدراسية]                   |
            |                                          |
            | . Summary point 1 text here              |
            | . Summary point 2 text here              |
            | . Summary point 3 text here              |
            |                                          |
            | [12]                                      |
            +------------------------------------------+

        Example:
            >>> builder.add_summary_slide([
            ...     "التقنيات الناشئة هي تقنيات في مراحلها الأولى",
            ...     "للتقنية الرقمية فوائد وسلبيات يجب مراعاتها",
            ... ])
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        # Set hidden TOC title for Storyline sidebar menu
        self._set_slide_title_for_toc(slide, "ملخص المحاضرة")

        # --- Lecture title bar ---
        self._add_header_bar(slide, self.lecture_title)

        # --- Section banner ---
        self._add_section_banner(slide, "ملخّص الوحدة الدراسيّة", wide=True)

        # --- Summary content card background for professional look ---
        self._add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left=Cm(2),
            top=Cm(4.2),
            width=Cm(30),
            height=Cm(10.5),
            fill_color=CONTENT_CARD_BG,
            border_color=CONTENT_CARD_BORDER,
            border_width=Pt(1),
            name="bg_summary_card",
        )

        # Build each item as a paragraph with bold label + regular text
        txBox = slide.shapes.add_textbox(Cm(2.5), Cm(4.5), Cm(29), Cm(10))
        txBox.name = "txt_summary"
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = TEXT_MARGIN_LR
        tf.margin_right = TEXT_MARGIN_LR
        tf.margin_top = TEXT_MARGIN_TB
        tf.margin_bottom = TEXT_MARGIN_TB

        for idx, item in enumerate(summary_items):
            if idx == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()

            p.alignment = PP_ALIGN.RIGHT
            p.line_spacing = 1.5
            p.space_after = Pt(8)

            if isinstance(item, dict):
                title = item.get("title", "")
                text = item.get("text", item.get("body", ""))
                if title:
                    # Bold label run (PRIMARY_BLUE for emphasis)
                    label_run = p.add_run()
                    label_run.text = f"{title}: "
                    self._set_run_font(label_run, FONT_EXTRABOLD, Pt(20), True, PRIMARY_BLUE)
                    # Regular text run (BODY_TEXT for readability)
                    text_run = p.add_run()
                    text_run.text = text
                    self._set_run_font(text_run, FONT_REGULAR, Pt(20), False, BODY_TEXT)
                else:
                    run = p.add_run()
                    run.text = text
                    self._set_run_font(run, FONT_REGULAR, Pt(20), False, BODY_TEXT)
            else:
                run = p.add_run()
                run.text = str(item)
                self._set_run_font(run, FONT_REGULAR, Pt(20), False, BODY_TEXT)

            self._set_rtl(p)

    def add_closing_slide(self, next_steps: list = None, image_path: Optional[str] = None, image_prompt: Optional[str] = None):
        """
        Add the final closing slide with optional next steps.

        This is the last slide of the lecture — it thanks the learner
        and optionally lists what comes next.

        Args:
            next_steps: Optional list of next step strings
            image_path: Optional decorative illustration above thank-you text
            image_prompt: Optional prompt to auto-generate a decorative illustration

        Visual output (ASCII mockup):
            +------------------------------------------+
            |  +++++++++++++++++++++++++++++++++++++++ |
            |  ++                                  ++ |
            |  ++         شكراً لكم                ++ |
            |  ++                                  ++ |
            |  ++   Next Steps:                    ++ |
            |  ++   . Step 1                       ++ |
            |  ++   . Step 2                       ++ |
            |  ++                                  ++ |
            |  +++++++++++++++++++++++++++++++++++++++ |
            +------------------------------------------+

        Example:
            >>> builder.add_closing_slide([
            ...     "مراجعة المحاضرة التفاعلية",
            ...     "حل النشاط التفاعلي",
            ...     "الاستعداد للاختبار البعدي",
            ... ])
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()

        # Set hidden TOC title for Storyline sidebar menu
        self._set_slide_title_for_toc(slide, "شكراً لكم")

        # --- Full-slide colored background ---
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=0,
            top=0,
            width=SLIDE_WIDTH,
            height=SLIDE_HEIGHT,
            fill_color=PRIMARY_BLUE,
        )

        # --- White content area ---
        margin = Cm(3)
        card_shape = self._add_shape(
            slide,
            MSO_SHAPE.ROUNDED_RECTANGLE,
            left=margin,
            top=margin,
            width=SLIDE_WIDTH - (margin * 2),
            height=SLIDE_HEIGHT - (margin * 2),
            fill_color=WHITE,
            name="bg_card",
        )
        self._add_shadow_to_shape(card_shape)

        # --- Decorative corner — code-drawn shapes (no blurry PNGs) ---
        self._add_decorative_corner(slide, "top_right", PRIMARY_BLUE_LIGHT, Cm(3))

        # --- Optional decorative illustration above thank-you text ---
        # Auto-generate image if prompt provided but no path
        if image_prompt and not image_path:
            image_path = self._generate_image_for_slide(image_prompt, "closing")
        closing_has_image = False
        if image_path:
            pic = self._add_image(
                slide, image_path,
                left=Cm(9), top=Cm(3.5),
                max_width=Cm(15), max_height=Cm(5),
                name="img_closing",
            )
            if pic is not None:
                closing_has_image = True

        # --- Thank you text (shifts down when image present) ---
        thanks_top = Cm(9) if closing_has_image else Cm(5)
        self._add_arabic_textbox(
            slide,
            left=Cm(5),
            top=thanks_top,
            width=Cm(24),
            height=Cm(2.5),
            text="شكراً لكم",
            font_name=FONT_EXTRABOLD,
            font_size=Pt(36),
            bold=False,
            color=PRIMARY_BLUE,
            alignment=PP_ALIGN.CENTER,
            name="txt_thanks",
        )

        # --- Next steps ---
        if next_steps:
            # Accent line above next steps
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=Cm(10),
                top=Cm(7.5),
                width=Cm(14),
                height=Cm(0.1),
                fill_color=PRIMARY_BLUE,
                name="accent_steps_line",
            )

            self._add_arabic_textbox(
                slide,
                left=Cm(5),
                top=Cm(8),
                width=Cm(24),
                height=Cm(1.5),
                text="الخطوات القادمة:",
                font_name=FONT_EXTRABOLD,
                font_size=Pt(20),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.CENTER,
                name="txt_next_steps_label",
            )

            # Numbered next steps (circles instead of bullets)
            for i, step in enumerate(next_steps):
                step_num = i + 1
                step_top = Cm(10) + i * Cm(2)

                # Number circle
                circle = self._add_shape(
                    slide,
                    MSO_SHAPE.OVAL,
                    left=Cm(24),
                    top=step_top,
                    width=Cm(1.5),
                    height=Cm(1.5),
                    fill_color=PRIMARY_BLUE,
                    name=f"num_step_{step_num}",
                )
                tf_c = circle.text_frame
                tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
                p_c = tf_c.paragraphs[0]
                p_c.alignment = PP_ALIGN.CENTER
                run_c = p_c.add_run()
                run_c.text = str(step_num)
                self._set_run_font(run_c, FONT_EXTRABOLD, Pt(16), False, WHITE)

                # Step text
                self._add_arabic_textbox(
                    slide,
                    left=Cm(6),
                    top=step_top,
                    width=Cm(17),
                    height=Cm(1.5),
                    text=step,
                    font_name=FONT_REGULAR,
                    font_size=Pt(18),
                    bold=False,
                    color=BODY_TEXT,
                    alignment=PP_ALIGN.RIGHT,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_step_{step_num}",
                )
