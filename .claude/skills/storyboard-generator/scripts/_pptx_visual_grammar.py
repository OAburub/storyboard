"""
PPTX Visual Grammar — Rich content slide patterns.
====================================================

Provides visual pattern methods that replace default bullet slides
with meaningful data-driven layouts. Each method maps a content
RELATIONSHIP to a visual FORM:

    Process Flow  → Sequential steps (3-7) with arrows
    Stat Cards    → 2-4 key numbers with trend indicators
    Quote         → Breathing slide with featured quote
    Timeline      → Events over time with milestone markers
    Comparison    → Side-by-side columns with criteria
    Icon Grid     → 2x2 or 3x3 grid of icon-label pairs
    Cycle Diagram → 3-6 repeating stages in a circle
    Concept Visual→ Dispatcher that routes to the right pattern

Native-First Rendering:
    Educational slides are TEXT-HEAVY — most Arabic content belongs in
    native PPTX textboxes that handle RTL, line wrapping, and font
    substitution properly. SVG is reserved for complex visual diagrams
    only (cycle diagrams, large process flows) where layout geometry
    is genuinely hard with basic shapes.

    All 8 pattern methods default to native PPTX shapes. SVG can be
    forced via use_svg=True, or is auto-selected for:
      - cycle_diagram (circular layout with curved arrows)
      - process_flow with 6+ steps (multi-row complex layout)

    OOXML XML enhancements (gradients, glow, soft edges) bridge the gap
    between "code-generated" and "professionally designed" slides.

Architecture:
    This is a MIXIN class. Methods use `self` to access SlideEngine
    helpers from _pptx_core.py. Do NOT import SlideEngine here
    (would cause circular imports).

    The final LectureBuilder composes:
        SlideEngine (base) + DepthMixin + StructuralMixin
                           + VisualGrammarMixin + ...

Usage:
    # Called by LectureBuilder which inherits this mixin
    builder.add_process_flow(
        title="مراحل التصميم",
        steps=[{"num": 1, "label": "التحليل", "desc": "دراسة الاحتياجات"}, ...]
    )
"""

from _pptx_core import *  # Import all constants, colors, fonts, positions

import os
import math
from pptx.util import Cm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


class VisualGrammarMixin:
    """
    Mixin that adds visual grammar slide methods to SlideEngine.

    Art Direction Philosophy:
        Educational content is TEXT-HEAVY. Native PPTX shapes with real
        textboxes excel here because they handle RTL, line wrapping, and
        font substitution properly. SVG (rasterized to PNG) loses text
        editability and often has Arabic font rendering issues.

        SVG is reserved ONLY for complex visual diagrams where layout
        geometry is genuinely hard with basic shapes:
          - cycle_diagram: circular layout with curved arrows
          - process_flow with 6+ steps: multi-row complex layout

        Every pattern should feel DESIGNED, not assembled. OOXML XML
        effects (gradient fills, glow, soft edges) applied directly via
        lxml bridge the gap between "code-generated shapes" and
        "professionally designed slides."

        The agent should think about composition, whitespace, and focal
        points — not just "which pattern to use."

    Every method follows the standard content slide pattern:
      1. Increment slide_count
      2. Add content slide with layout
      3. Set TOC title
      4. Add header bar + section banner
      5. Add depth wash
      6. If use_svg=True or auto-SVG eligible: try SVG generation
      7. Render pattern-specific shapes (primary path)
      8. Apply OOXML effects (gradients, glow, soft edges)
      9. Optional image + speaker notes
    """

    # ------------------------------------------------------------------
    # SVG VISUAL HELPER — Smart SVG/PPTX routing
    # ------------------------------------------------------------------

    def _should_use_svg(self, pattern_type, data, use_svg=False):
        """
        Decide whether to attempt SVG generation for a given pattern.

        SVG is only beneficial for complex visual layouts where geometry
        is hard to achieve with basic PPTX shapes. Most educational
        slides are text-heavy and benefit from native PPTX textboxes
        that handle RTL, line wrapping, and font substitution properly.

        Auto-SVG patterns:
          - cycle_diagram: circular layout with curved arrows
          - process_flow with 6+ steps: multi-row complex layout

        All other patterns always use native PPTX shapes unless the
        caller explicitly sets use_svg=True.

        Args:
            pattern_type: Visual pattern name (e.g., "process_flow")
            data: Pattern-specific data (used to check step count)
            use_svg: Explicit override — if True, always try SVG

        Returns:
            True if SVG should be attempted, False otherwise.
        """
        # Explicit override — caller wants SVG
        if use_svg:
            return True

        # Auto-SVG for cycle diagrams (circular layout is genuinely hard)
        if pattern_type == "cycle":
            return True

        # Auto-SVG for large process flows (6+ steps need multi-row layout)
        if pattern_type == "process_flow" and isinstance(data, list) and len(data) >= 6:
            return True

        # All other patterns — native PPTX shapes (text-heavy, editable)
        return False

    def _try_svg_visual(self, slide, pattern_type, data, title, notes="", use_svg=False):
        """
        Try to generate an SVG visual for a slide pattern using Gemini AI.

        Only attempts SVG when _should_use_svg() returns True. This ensures
        text-heavy educational slides use native PPTX shapes by default.

        If successful, embeds the rendered PNG as a full-slide background
        image. The SVG file is also saved alongside for Storyline developers.

        Args:
            slide: The slide object to add the visual to
            pattern_type: Visual pattern name (e.g., "process_flow")
            data: Pattern-specific data
            title: Slide title in Arabic
            notes: Speaker notes to append SVG info to
            use_svg: If True, force SVG generation regardless of pattern type

        Returns:
            True if SVG was generated and embedded, False to use native shapes.
        """
        # Smart routing: skip SVG unless this pattern benefits from it
        if not self._should_use_svg(pattern_type, data, use_svg):
            return False

        try:
            from _pptx_svg_generator import generate_slide_svg

            # Build output path based on project/unit/slide
            slides_dir = os.path.join(
                str(PROJECT_ROOT), "output", self.project_code,
                f"U{self.unit_number:02d}", "slides"
            )
            svg_output = os.path.join(
                slides_dir, f"slide_{self.slide_count}_{pattern_type}.svg"
            )

            colors = {
                "primary": "#2D588C",
                "secondary": "#4A90D9",
                "accent": "#F5A623",
            }

            png_path = generate_slide_svg(
                pattern_type=pattern_type,
                data=data,
                colors=colors,
                title=title,
                output_path=svg_output,
                animated=False,
            )

            if png_path and os.path.exists(png_path):
                # Embed PNG as full-slide background image
                self._add_image(
                    slide, png_path,
                    left=0, top=0,
                    max_width=SLIDE_WIDTH, max_height=SLIDE_HEIGHT,
                    name="bg_svg_visual",
                )

                # Append SVG reference to notes
                svg_note = f"\n\n=== SVG VISUAL ===\nFile: {svg_output}\nPNG: {png_path}"
                if notes:
                    self._add_notes(slide, notes + svg_note)
                else:
                    self._add_notes(slide, svg_note.strip())

                return True

        except ImportError:
            pass  # _pptx_svg_generator not available — use shape fallback
        except Exception as e:
            print(f"[Visual Grammar] SVG generation failed for {pattern_type}: {e}")

        return False

    # ------------------------------------------------------------------
    # OOXML ENHANCEMENT HELPERS — Professional visual effects via XML
    # ------------------------------------------------------------------
    # These methods use direct lxml XML manipulation to add effects that
    # python-pptx doesn't expose natively. Same technique as the shadow
    # method in _pptx_core.py (_add_shadow_to_shape).

    def _apply_gradient_fill(self, shape, color1_hex, color2_hex, angle=270):
        """
        Apply a linear gradient fill to a shape via OOXML XML.

        Replaces any existing solid fill with a smooth gradient between
        two colors. Much more professional than flat solid fills.

        Args:
            shape: The shape to apply gradient to
            color1_hex: Start color as hex string (e.g., "#2D588C")
            color2_hex: End color as hex string (e.g., "#4A90D9")
            angle: Gradient angle in degrees (270 = top-to-bottom, default)
        """
        from lxml import etree

        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        spPr = shape._element.spPr

        # Remove existing solid or gradient fills
        for child in list(spPr):
            if child.tag.endswith('}solidFill') or child.tag.endswith('}gradFill'):
                spPr.remove(child)

        # Build gradient fill XML
        gradFill = etree.SubElement(spPr, f'{{{ns}}}gradFill')
        gsLst = etree.SubElement(gradFill, f'{{{ns}}}gsLst')

        # Gradient stop 1 (start color)
        gs1 = etree.SubElement(gsLst, f'{{{ns}}}gs')
        gs1.set('pos', '0')
        srgb1 = etree.SubElement(gs1, f'{{{ns}}}srgbClr')
        srgb1.set('val', color1_hex.lstrip('#'))

        # Gradient stop 2 (end color)
        gs2 = etree.SubElement(gsLst, f'{{{ns}}}gs')
        gs2.set('pos', '100000')
        srgb2 = etree.SubElement(gs2, f'{{{ns}}}srgbClr')
        srgb2.set('val', color2_hex.lstrip('#'))

        # Linear direction
        lin = etree.SubElement(gradFill, f'{{{ns}}}lin')
        lin.set('ang', str(angle * 60000))  # Degrees to 60000ths of a degree
        lin.set('scaled', '1')

    def _apply_glow(self, shape, color_hex, radius_pt=8, alpha=40):
        """
        Add a glow effect to a shape via OOXML XML.

        Creates a colored halo around the shape, drawing attention to
        important elements like stat numbers or active timeline markers.

        Args:
            shape: The shape to add glow to
            color_hex: Glow color as hex string (e.g., "#2D588C")
            radius_pt: Glow radius in points (default: 8)
            alpha: Glow opacity 0-100 (default: 40)
        """
        from lxml import etree

        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        spPr = shape._element.spPr

        # Find or create effectLst
        effectLst = spPr.find(f'{{{ns}}}effectLst')
        if effectLst is None:
            effectLst = etree.SubElement(spPr, f'{{{ns}}}effectLst')

        # Add glow element
        glow = etree.SubElement(effectLst, f'{{{ns}}}glow')
        glow.set('rad', str(int(radius_pt * 12700)))  # Points to EMU
        srgb = etree.SubElement(glow, f'{{{ns}}}srgbClr')
        srgb.set('val', color_hex.lstrip('#'))
        alpha_el = etree.SubElement(srgb, f'{{{ns}}}alpha')
        alpha_el.set('val', str(alpha * 1000))  # Percentage to OOXML units

    def _apply_soft_edge(self, shape, radius_pt=5):
        """
        Add a soft edge effect to a shape via OOXML XML.

        Softens the edges of decorative background shapes so they blend
        into the slide more naturally instead of having hard boundaries.

        Args:
            shape: The shape to soften edges on
            radius_pt: Edge softness radius in points (default: 5)
        """
        from lxml import etree

        ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        spPr = shape._element.spPr

        # Find or create effectLst
        effectLst = spPr.find(f'{{{ns}}}effectLst')
        if effectLst is None:
            effectLst = etree.SubElement(spPr, f'{{{ns}}}effectLst')

        # Add soft edge element
        softEdge = etree.SubElement(effectLst, f'{{{ns}}}softEdge')
        softEdge.set('rad', str(int(radius_pt * 12700)))  # Points to EMU

    # ------------------------------------------------------------------
    # 1. PROCESS FLOW — Sequential steps with connecting arrows (RTL)
    # ------------------------------------------------------------------

    def add_process_flow(self, title, steps, notes="", image_prompt=None, use_svg=False):
        """
        Add a process flow slide showing sequential steps connected by arrows.

        Uses native PPTX shapes by default for editable Arabic text.
        SVG is auto-selected for 6+ steps or when use_svg=True.

        Steps flow RIGHT to LEFT (RTL). Each step is a rounded card with
        a gradient-filled top bar, number badge, label, and description.
        Steps are connected by arrow shapes.

        If there are 5+ steps, they split into 2 rows.

        Args:
            title: Section title (Arabic)
            steps: List of dicts with "num", "label", "desc" (3-7 items)
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate a background image
            use_svg: If True, force SVG generation (default: False)

        Visual output (4 steps, RTL):
            +------------------------------------------+
            |        [Header Bar]                      |
            |        [=== Title Banner ===]            |
            |                                          |
            |   <-- [Step 4] <-- [Step 3] <-- [Step 2] <-- [Step 1]
            |                                          |
            +------------------------------------------+
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (auto for 6+ steps, or when explicitly requested)
        if self._try_svg_visual(slide, "process_flow", steps, title, notes, use_svg=use_svg):
            return  # SVG succeeded — skip native shapes

        # Native PPTX shape rendering (primary path)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title)
        self.add_depth_wash(slide)

        step_count = len(steps)

        # Determine single-row vs two-row layout
        if step_count <= 4:
            # Single row layout
            self._render_process_row(slide, steps, row_top=Cm(5.5), row_index=0)
        else:
            # Two-row layout: split steps roughly in half
            mid = (step_count + 1) // 2
            top_steps = steps[:mid]
            bottom_steps = steps[mid:]
            self._render_process_row(slide, top_steps, row_top=Cm(4.5), row_index=0)
            self._render_process_row(slide, bottom_steps, row_top=Cm(10.5), row_index=mid)

        # Optional image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(
                    slide, img_path,
                    left=Cm(1), top=Cm(14),
                    max_width=Cm(5), max_height=Cm(3),
                    name="img_process_flow",
                )

        if notes:
            self._add_notes(slide, notes)

    def _render_process_row(self, slide, steps, row_top, row_index=0):
        """
        Render a single row of process flow steps with arrows between them.

        Steps are laid out RIGHT to LEFT (RTL). The rightmost step is
        the first step. Arrows point left (←) between steps.

        Args:
            slide: The slide object
            steps: List of step dicts for this row
            row_top: Y position for the row (EMU from Cm)
            row_index: Starting index for shape naming (0 for first row)
        """
        step_count = len(steps)
        if step_count == 0:
            return

        # Layout measurements
        area_left = Cm(2)
        area_width = Cm(29.5)
        card_height = Cm(5)
        arrow_width = Cm(1.2)
        accent_bar_height = Cm(0.5)
        badge_size = Cm(1.4)

        # Calculate card width based on available space
        total_arrow_space = arrow_width * (step_count - 1) if step_count > 1 else 0
        card_width = int((area_width - total_arrow_space) / step_count)

        for i, step in enumerate(steps):
            step_num = step.get("num", row_index + i + 1)
            label = step.get("label", "")
            desc = step.get("desc", "")

            # RTL: step 1 on the RIGHT, step N on the LEFT
            # Position from right: rightmost card starts at area_left + area_width - card_width
            card_left = int(
                area_left + area_width - (i + 1) * card_width - i * arrow_width
            )

            # Get rotating accent color for this step
            accent = self._get_accent_color()

            # Card background
            card = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=card_left,
                top=row_top,
                width=card_width,
                height=card_height,
                fill_color=CONTENT_CARD_BG,
                border_color=CONTENT_CARD_BORDER,
                border_width=Pt(1),
                name=f"card_step_{step_num}",
                corner_radius=0.04,
            )
            self._add_shadow_to_shape(card, blur_pt=4, opacity_pct=15)

            # Accent bar at top of card — gradient fill for depth
            accent_bar = self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=card_left,
                top=row_top,
                width=card_width,
                height=accent_bar_height,
                fill_color=accent,
                name=f"accent_step_{step_num}",
            )
            # Apply gradient from accent color to a slightly lighter tint
            accent_hex = f"#{accent[0]:02X}{accent[1]:02X}{accent[2]:02X}"
            lighter_hex = f"#{min(accent[0]+40,255):02X}{min(accent[1]+40,255):02X}{min(accent[2]+40,255):02X}"
            self._apply_gradient_fill(accent_bar, accent_hex, lighter_hex, angle=0)

            # Number badge (centered horizontally on the card)
            badge_left = card_left + (card_width - badge_size) // 2
            badge_top = row_top + accent_bar_height + Cm(0.3)
            badge = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=badge_left,
                top=badge_top,
                width=badge_size,
                height=badge_size,
                fill_color=accent,
                name=f"num_step_{step_num}",
            )
            self._apply_glow(badge, accent_hex, radius_pt=6, alpha=30)
            tf = badge.text_frame
            tf.word_wrap = False
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = str(step_num)
            self._set_run_font(run, FONT_EXTRABOLD, Pt(14), False, WHITE)

            # Step label
            label_top = badge_top + badge_size + Cm(0.2)
            self._add_arabic_textbox(
                slide,
                left=card_left + Cm(0.3),
                top=label_top,
                width=card_width - Cm(0.6),
                height=Cm(1.2),
                text=label,
                font_name=FONT_EXTRABOLD,
                font_size=Pt(14),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_step_{step_num}_label",
            )

            # Step description
            desc_top = label_top + Cm(1.2)
            self._add_arabic_textbox(
                slide,
                left=card_left + Cm(0.3),
                top=desc_top,
                width=card_width - Cm(0.6),
                height=Cm(1.3),
                text=desc,
                font_name=FONT_REGULAR,
                font_size=Pt(11),
                bold=False,
                color=WARM_GRAY,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_step_{step_num}_desc",
            )

            # Arrow between this step and the next (RTL: ← arrow to the LEFT)
            if i < step_count - 1:
                arrow_left = card_left - arrow_width
                arrow_top = row_top + (card_height - Cm(0.8)) // 2
                arrow = self._add_shape(
                    slide,
                    MSO_SHAPE.NOTCHED_RIGHT_ARROW,
                    left=arrow_left,
                    top=arrow_top,
                    width=arrow_width,
                    height=Cm(0.8),
                    fill_color=PRIMARY_BLUE_LIGHT,
                    name=f"arrow_{step_num}_{step_num + 1}",
                )
                # Rotate 180 degrees to point left (RTL direction)
                arrow.rotation = 180.0

    # ------------------------------------------------------------------
    # 2. STAT CARDS — Key numbers with trend indicators
    # ------------------------------------------------------------------

    def add_stat_cards(self, title, stats, notes="", image_prompt=None, use_svg=False):
        """
        Add a stat cards slide showing 2-4 key numbers.

        Uses native PPTX shapes by default for editable Arabic text.
        Cards feature gradient fills and glow effects on numbers for
        a professional, polished appearance.

        Args:
            title: Section title (Arabic)
            stats: List of dicts with "number", "label",
                   optional "trend" ("up"/"down"), optional "desc"
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate a background image
            use_svg: If True, force SVG generation (default: False)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (stat_cards never auto-selects SVG)
        if self._try_svg_visual(slide, "stat_cards", stats, title, notes, use_svg=use_svg):
            return

        # Native PPTX shape rendering (primary path)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)
        self.add_depth_wash(slide)

        card_count = len(stats)
        if card_count == 0:
            return

        # Layout measurements
        area_left = Cm(2.5)
        area_width = Cm(28.5)
        card_top = Cm(5.5)
        card_height = Cm(8.5)
        gap = Cm(1)
        accent_bar_height = Cm(0.5)

        total_gaps = gap * (card_count - 1) if card_count > 1 else 0
        card_width = int((area_width - total_gaps) / card_count)

        # Scale number font size based on card count
        number_font_size = Pt(56) if card_count <= 2 else Pt(48) if card_count <= 3 else Pt(40)

        for i, stat in enumerate(stats):
            card_num = i + 1
            number = stat.get("number", "0")
            label = stat.get("label", "")
            trend = stat.get("trend", None)
            desc = stat.get("desc", "")

            card_left = int(area_left + i * (card_width + gap))

            # Get rotating accent color
            accent = self._get_accent_color()

            # Card background
            card = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=card_left,
                top=card_top,
                width=card_width,
                height=card_height,
                fill_color=WHITE,
                border_color=CONTENT_CARD_BORDER,
                border_width=Pt(1),
                name=f"card_stat_{card_num}",
                corner_radius=0.04,
            )
            self._add_shadow_to_shape(card, blur_pt=3, opacity_pct=12)

            # Accent bar at top — gradient fill for professional depth
            accent_bar = self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=card_left,
                top=card_top,
                width=card_width,
                height=accent_bar_height,
                fill_color=accent,
                name=f"accent_stat_{card_num}",
            )
            accent_hex = f"#{accent[0]:02X}{accent[1]:02X}{accent[2]:02X}"
            lighter_hex = f"#{min(accent[0]+40,255):02X}{min(accent[1]+40,255):02X}{min(accent[2]+40,255):02X}"
            self._apply_gradient_fill(accent_bar, accent_hex, lighter_hex, angle=0)

            # Big number — centered, prominent, with subtle glow for emphasis
            number_top = card_top + accent_bar_height + Cm(0.8)
            number_box = self._add_arabic_textbox(
                slide,
                left=card_left + Cm(0.5),
                top=number_top,
                width=card_width - Cm(1),
                height=Cm(2.5),
                text=number,
                font_name=FONT_EXTRABOLD,
                font_size=number_font_size,
                bold=False,
                color=accent,
                alignment=PP_ALIGN.CENTER,
                word_wrap=False,
                auto_size=MSO_AUTO_SIZE.NONE,
                line_spacing=1.1,
                name=f"txt_stat_{card_num}_number",
            )
            self._apply_glow(number_box, accent_hex, radius_pt=6, alpha=25)

            # Trend indicator (arrow + color)
            if trend:
                trend_top = number_top + Cm(2.5)
                trend_text = "\u2191" if trend == "up" else "\u2193"  # ↑ or ↓
                trend_color = ACCENT_GREEN if trend == "up" else ACCENT_RED
                self._add_arabic_textbox(
                    slide,
                    left=card_left + Cm(0.5),
                    top=trend_top,
                    width=card_width - Cm(1),
                    height=Cm(1),
                    text=trend_text,
                    font_name=FONT_EXTRABOLD,
                    font_size=Pt(24),
                    bold=False,
                    color=trend_color,
                    alignment=PP_ALIGN.CENTER,
                    word_wrap=False,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"icon_trend_{card_num}",
                )

            # Label — below number/trend
            label_top = card_top + accent_bar_height + Cm(4.5)
            self._add_arabic_textbox(
                slide,
                left=card_left + Cm(0.3),
                top=label_top,
                width=card_width - Cm(0.6),
                height=Cm(1.5),
                text=label,
                font_name=FONT_MEDIUM,
                font_size=Pt(16),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_stat_{card_num}_label",
            )

            # Optional description
            if desc:
                desc_top = label_top + Cm(1.8)
                self._add_arabic_textbox(
                    slide,
                    left=card_left + Cm(0.3),
                    top=desc_top,
                    width=card_width - Cm(0.6),
                    height=Cm(1.5),
                    text=desc,
                    font_name=FONT_REGULAR,
                    font_size=Pt(12),
                    bold=False,
                    color=WARM_GRAY,
                    alignment=PP_ALIGN.CENTER,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_stat_{card_num}_desc",
                )

        # Optional image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(
                    slide, img_path,
                    left=Cm(1), top=Cm(14),
                    max_width=Cm(5), max_height=Cm(3),
                    name="img_stat_cards",
                )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # 3. QUOTE HIGHLIGHT — Breathing slide with featured quote
    # ------------------------------------------------------------------

    def add_quote_highlight(self, title, quote, attribution="", notes="", use_svg=False):
        """
        Add a quote highlight slide — a breathing slide with generous whitespace.

        Uses native PPTX shapes by default for editable Arabic text.
        Decorative quotation marks get soft edge effects for elegance.

        Args:
            title: Section title (Arabic)
            quote: The quote text (Arabic)
            attribution: Source/author name (optional)
            notes: Speaker notes / Storyline instructions
            use_svg: If True, force SVG generation (default: False)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (quote never auto-selects SVG)
        quote_data = {"quote": quote, "attribution": attribution}
        if self._try_svg_visual(slide, "quote", quote_data, title, notes, use_svg=use_svg):
            return

        # Native PPTX shape rendering (primary path)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title)
        self.add_depth_wash(slide, style="radial_glow")

        # Decorative quotation marks — large, light-colored, behind quote
        # Soft edges make them blend naturally into the background
        # Right quotation mark (» in Arabic typography, appears on the right for RTL)
        deco_color = RGBColor(0xE0, 0xE8, 0xF0)  # Very light blue-gray
        deco_right = self._add_arabic_textbox(
            slide,
            left=Cm(20),
            top=Cm(4.5),
            width=Cm(6),
            height=Cm(4),
            text="\u00BB",  # >> right-pointing guillemet
            font_name=FONT_EXTRABOLD,
            font_size=Pt(120),
            bold=False,
            color=deco_color,
            alignment=PP_ALIGN.CENTER,
            word_wrap=False,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="deco_quote_mark_right",
        )
        self._apply_soft_edge(deco_right, radius_pt=8)

        # Left quotation mark (« appears on the left side)
        deco_left = self._add_arabic_textbox(
            slide,
            left=Cm(7),
            top=Cm(9),
            width=Cm(6),
            height=Cm(4),
            text="\u00AB",  # << left-pointing guillemet
            font_name=FONT_EXTRABOLD,
            font_size=Pt(120),
            bold=False,
            color=deco_color,
            alignment=PP_ALIGN.CENTER,
            word_wrap=False,
            auto_size=MSO_AUTO_SIZE.NONE,
            name="deco_quote_mark_left",
        )
        self._apply_soft_edge(deco_left, radius_pt=8)

        # Quote text — centered, medium weight, generous size
        quote_top = Cm(6)
        quote_width = Cm(22)
        quote_left = (SLIDE_WIDTH - quote_width) // 2

        self._add_arabic_textbox(
            slide,
            left=quote_left,
            top=quote_top,
            width=quote_width,
            height=Cm(5),
            text=quote,
            font_name=FONT_MEDIUM,
            font_size=Pt(26),
            bold=False,
            color=PRIMARY_BLUE_DARK,
            alignment=PP_ALIGN.CENTER,
            word_wrap=True,
            auto_size=MSO_AUTO_SIZE.NONE,
            line_spacing=1.5,
            name="txt_quote",
        )

        # Attribution line
        if attribution:
            attr_top = Cm(11.5)
            attr_text = f"\u2014 {attribution}"  # — dash before name
            self._add_arabic_textbox(
                slide,
                left=quote_left,
                top=attr_top,
                width=quote_width,
                height=Cm(1.5),
                text=attr_text,
                font_name=FONT_REGULAR,
                font_size=Pt(14),
                bold=False,
                color=WARM_GRAY,
                alignment=PP_ALIGN.CENTER,
                word_wrap=False,
                auto_size=MSO_AUTO_SIZE.NONE,
                name="txt_attribution",
            )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # 4. TIMELINE — Events over time with milestone markers
    # ------------------------------------------------------------------

    def add_timeline(self, title, milestones, notes="", image_prompt=None, use_svg=False):
        """
        Add a timeline slide showing events along a horizontal line.

        Uses native PPTX shapes by default for editable Arabic text.
        Active milestone markers get glow effects for emphasis.

        Args:
            title: Section title (Arabic)
            milestones: List of dicts with "year"/"date", "title", "desc",
                        optional "status" ("done"/"active"/"pending")
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate a background image
            use_svg: If True, force SVG generation (default: False)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (timeline never auto-selects SVG)
        if self._try_svg_visual(slide, "timeline", milestones, title, notes, use_svg=use_svg):
            return

        # Native PPTX shape rendering (primary path)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)
        self.add_depth_wash(slide)

        count = len(milestones)
        if count == 0:
            return

        # Layout measurements
        line_left = Cm(3)
        line_width = Cm(27.5)
        line_top = Cm(9.5)         # Horizontal center line Y position
        line_height = Cm(0.15)     # Line thickness
        dot_size = Cm(1)
        dot_active_size = Cm(1.4)

        # Draw the horizontal timeline line
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=line_left,
            top=line_top,
            width=line_width,
            height=line_height,
            fill_color=PRIMARY_BLUE_LIGHT,
            name="line_timeline",
        )

        # Calculate horizontal spacing for milestones (RTL: first on right)
        spacing = int(line_width / (count + 1)) if count > 0 else line_width

        for i, ms in enumerate(milestones):
            ms_num = i + 1
            date_text = ms.get("year", ms.get("date", ""))
            ms_title = ms.get("title", "")
            ms_desc = ms.get("desc", "")
            status = ms.get("status", "done")

            # RTL: milestone 1 on the right side
            dot_center_x = int(line_left + line_width - (i + 1) * spacing)

            # Determine dot appearance by status
            if status == "active":
                d_size = dot_active_size
                dot_color = ACCENT_ORANGE
            elif status == "pending":
                d_size = dot_size
                dot_color = None  # outline only
            else:  # "done"
                d_size = dot_size
                dot_color = PRIMARY_BLUE

            dot_left = dot_center_x - d_size // 2
            dot_top = line_top + line_height // 2 - d_size // 2

            if dot_color:
                dot = self._add_shape(
                    slide,
                    MSO_SHAPE.OVAL,
                    left=dot_left,
                    top=dot_top,
                    width=d_size,
                    height=d_size,
                    fill_color=dot_color,
                    name=f"dot_milestone_{ms_num}",
                )
                # Active milestones get a glow effect for emphasis
                if status == "active":
                    self._apply_glow(dot, "FF9800", radius_pt=10, alpha=35)
            else:
                # Pending: outline only (white fill + blue border)
                dot = self._add_shape(
                    slide,
                    MSO_SHAPE.OVAL,
                    left=dot_left,
                    top=dot_top,
                    width=d_size,
                    height=d_size,
                    fill_color=WHITE,
                    border_color=PRIMARY_BLUE,
                    border_width=Pt(2),
                    name=f"dot_milestone_{ms_num}",
                )

            # Alternate above/below the line
            is_above = (i % 2 == 0)
            text_width = Cm(6)
            text_left = dot_center_x - text_width // 2

            if is_above:
                # Date label ABOVE the line
                date_top = line_top - Cm(5.5)
                title_top = line_top - Cm(4)
                desc_top = line_top - Cm(2.5)
            else:
                # Date label BELOW the line
                date_top = line_top + Cm(1.5)
                title_top = line_top + Cm(3)
                desc_top = line_top + Cm(4.5)

            # Date/year label
            self._add_arabic_textbox(
                slide,
                left=text_left,
                top=date_top,
                width=text_width,
                height=Cm(1.2),
                text=date_text,
                font_name=FONT_EXTRABOLD,
                font_size=Pt(14),
                bold=False,
                color=PRIMARY_BLUE,
                alignment=PP_ALIGN.CENTER,
                word_wrap=False,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_milestone_{ms_num}_date",
            )

            # Milestone title
            self._add_arabic_textbox(
                slide,
                left=text_left,
                top=title_top,
                width=text_width,
                height=Cm(1.2),
                text=ms_title,
                font_name=FONT_MEDIUM,
                font_size=Pt(13),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_milestone_{ms_num}_title",
            )

            # Milestone description
            if ms_desc:
                self._add_arabic_textbox(
                    slide,
                    left=text_left,
                    top=desc_top,
                    width=text_width,
                    height=Cm(1.5),
                    text=ms_desc,
                    font_name=FONT_REGULAR,
                    font_size=Pt(11),
                    bold=False,
                    color=WARM_GRAY,
                    alignment=PP_ALIGN.CENTER,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_milestone_{ms_num}_desc",
                )

        # Optional image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(
                    slide, img_path,
                    left=Cm(1), top=Cm(14),
                    max_width=Cm(5), max_height=Cm(3),
                    name="img_timeline",
                )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # 5. COMPARISON — Side-by-side columns with criteria
    # ------------------------------------------------------------------

    def add_comparison(self, title, columns, notes="", image_prompt=None, use_svg=False):
        """
        Add a comparison slide with 2-3 side-by-side card columns.

        Uses native PPTX shapes by default for editable Arabic text.
        Column headers feature gradient fills for a polished look.

        Args:
            title: Section title (Arabic)
            columns: List of dicts with "title", "items" (list of strings),
                     optional "color" (RGBColor), optional "highlight" (bool)
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate a background image
            use_svg: If True, force SVG generation (default: False)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (comparison never auto-selects SVG)
        if self._try_svg_visual(slide, "comparison", columns, title, notes, use_svg=use_svg):
            return

        # Native PPTX shape rendering (primary path)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)
        self.add_depth_wash(slide)

        col_count = len(columns)
        if col_count == 0:
            return

        # Default column colors
        default_colors = [PRIMARY_BLUE, TEAL, ACCENT_ORANGE]

        # Layout measurements
        area_left = Cm(2.5)
        area_width = Cm(28.5)
        col_top = Cm(5)
        col_gap = Cm(1)
        header_height = Cm(2)
        accent_bar_height = Cm(0.4)

        total_gaps = col_gap * (col_count - 1) if col_count > 1 else 0
        col_width = int((area_width - total_gaps) / col_count)
        col_body_height = Cm(9)

        for i, col_data in enumerate(columns):
            col_num = i + 1
            col_title = col_data.get("title", "")
            col_items = col_data.get("items", [])
            col_color = col_data.get("color", default_colors[i % len(default_colors)])
            is_highlight = col_data.get("highlight", False)

            # RTL: first column on the RIGHT
            col_left = int(area_left + area_width - (i + 1) * col_width - i * col_gap)

            total_card_height = header_height + col_body_height

            # Card background
            card = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=col_left,
                top=col_top,
                width=col_width,
                height=total_card_height,
                fill_color=WHITE,
                border_color=CONTENT_CARD_BORDER,
                border_width=Pt(1),
                name=f"card_col_{col_num}",
                corner_radius=0.04,
            )
            if is_highlight:
                self._add_shadow_to_shape(card, blur_pt=6, opacity_pct=20)
            else:
                self._add_shadow_to_shape(card, blur_pt=3, opacity_pct=12)

            # Accent bar at top
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=col_left,
                top=col_top,
                width=col_width,
                height=accent_bar_height,
                fill_color=col_color,
                name=f"accent_col_{col_num}",
            )

            # Column header with gradient-filled background
            header_bg = self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=col_left,
                top=col_top + accent_bar_height,
                width=col_width,
                height=header_height - accent_bar_height,
                fill_color=col_color,
                name=f"bg_col_{col_num}_header",
            )
            # Apply gradient from column color to a lighter tint
            col_hex = f"#{col_color[0]:02X}{col_color[1]:02X}{col_color[2]:02X}"
            col_lighter = f"#{min(col_color[0]+35,255):02X}{min(col_color[1]+35,255):02X}{min(col_color[2]+35,255):02X}"
            self._apply_gradient_fill(header_bg, col_hex, col_lighter, angle=90)

            # Column title text (white on colored header)
            self._add_arabic_textbox(
                slide,
                left=col_left + Cm(0.5),
                top=col_top + accent_bar_height,
                width=col_width - Cm(1),
                height=header_height - accent_bar_height,
                text=col_title,
                font_name=FONT_EXTRABOLD,
                font_size=Pt(18),
                bold=False,
                color=WHITE,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_col_{col_num}_title",
            )

            # Column body — render each item as a mini-card for scannability
            body_top = col_top + header_height + Cm(0.3)
            item_height = Cm(1.4)
            item_gap = Cm(0.3)
            # Light tint per column for item card backgrounds
            item_bg = RGBColor(
                min(col_color[0] + 180, 255),
                min(col_color[1] + 180, 255),
                min(col_color[2] + 180, 255),
            )

            for j, item_text in enumerate(col_items):
                item_top = int(body_top + j * (item_height + item_gap))
                # Don't overflow past the card bottom
                if item_top + item_height > col_top + total_card_height - Cm(0.3):
                    break

                # Mini-card background
                mini_card = self._add_shape(
                    slide,
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    left=col_left + Cm(0.3),
                    top=item_top,
                    width=col_width - Cm(0.6),
                    height=item_height,
                    fill_color=item_bg,
                    name=f"card_col_{col_num}_item_{j + 1}",
                    corner_radius=0.06,
                )
                self._apply_soft_edge(mini_card, radius_pt=2)

                # Item text inside the mini-card
                self._add_arabic_textbox(
                    slide,
                    left=col_left + Cm(0.6),
                    top=item_top + Cm(0.1),
                    width=col_width - Cm(1.2),
                    height=item_height - Cm(0.2),
                    text=item_text,
                    font_name=FONT_REGULAR,
                    font_size=Pt(14),
                    bold=False,
                    color=BODY_TEXT,
                    alignment=PP_ALIGN.RIGHT,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_col_{col_num}_item_{j + 1}",
                )

        # Optional image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(
                    slide, img_path,
                    left=Cm(1), top=Cm(14),
                    max_width=Cm(5), max_height=Cm(3),
                    name="img_comparison",
                )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # 6. ICON GRID — Grid of icon-label pairs
    # ------------------------------------------------------------------

    def add_icon_grid(self, title, items, notes="", image_prompt=None, use_svg=False):
        """
        Add an icon grid slide with a 2x2, 2x3, or 3x3 grid of cells.

        Uses native PPTX shapes by default for editable Arabic text.
        Grid cells feature gradient accent bars for visual polish.

        Args:
            title: Section title (Arabic)
            items: List of dicts with "icon" (emoji string), "label",
                   optional "desc"
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate a background image
            use_svg: If True, force SVG generation (default: False)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (icon_grid never auto-selects SVG)
        if self._try_svg_visual(slide, "icon_grid", items, title, notes, use_svg=use_svg):
            return

        # Native PPTX shape rendering (primary path)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)
        self.add_depth_wash(slide)

        count = len(items)
        if count == 0:
            return

        # Auto-detect grid dimensions
        if count <= 4:
            cols = 2
            rows = 2
        elif count <= 6:
            cols = 3
            rows = 2
        else:
            cols = 3
            rows = 3

        # Layout measurements
        area_left = Cm(2.5)
        area_width = Cm(28.5)
        grid_top = Cm(5)
        col_gap = Cm(0.8)
        row_gap = Cm(0.6)
        accent_bar_height = Cm(0.3)

        total_col_gaps = col_gap * (cols - 1)
        cell_width = int((area_width - total_col_gaps) / cols)

        # Calculate cell height based on available space
        available_height = Cm(12)
        total_row_gaps = row_gap * (rows - 1)
        cell_height = int((available_height - total_row_gaps) / rows)

        for idx, item in enumerate(items):
            if idx >= rows * cols:
                break  # Don't exceed grid capacity

            cell_num = idx + 1
            row = idx // cols
            col = idx % cols
            icon = item.get("icon", "")
            label = item.get("label", "")
            desc = item.get("desc", "")

            # Get rotating accent color
            accent = self._get_accent_color()

            # RTL: columns go right-to-left
            cell_left = int(area_left + area_width - (col + 1) * cell_width - col * col_gap)
            cell_top = int(grid_top + row * (cell_height + row_gap))

            # Cell card background
            card = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=cell_left,
                top=cell_top,
                width=cell_width,
                height=cell_height,
                fill_color=CONTENT_CARD_BG,
                border_color=CONTENT_CARD_BORDER,
                border_width=Pt(0.5),
                name=f"card_grid_{cell_num}",
                corner_radius=0.04,
            )
            self._add_shadow_to_shape(card, blur_pt=2, opacity_pct=10)

            # Accent bar at top of cell — gradient fill for polish
            accent_bar = self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=cell_left,
                top=cell_top,
                width=cell_width,
                height=accent_bar_height,
                fill_color=accent,
                name=f"accent_grid_{cell_num}",
            )
            accent_hex = f"#{accent[0]:02X}{accent[1]:02X}{accent[2]:02X}"
            lighter_hex = f"#{min(accent[0]+40,255):02X}{min(accent[1]+40,255):02X}{min(accent[2]+40,255):02X}"
            self._apply_gradient_fill(accent_bar, accent_hex, lighter_hex, angle=0)

            # Circular background behind emoji icon
            icon_top = cell_top + accent_bar_height + Cm(0.3)
            icon_height = Cm(1.8)
            circle_size = Cm(1.5)
            circle_left = cell_left + (cell_width - circle_size) // 2
            circle_top = icon_top + (icon_height - circle_size) // 2
            # Light tint of accent color for the circle background
            circle_bg = RGBColor(
                min(accent[0] + 180, 255),
                min(accent[1] + 180, 255),
                min(accent[2] + 180, 255),
            )
            icon_circle = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=circle_left,
                top=circle_top,
                width=circle_size,
                height=circle_size,
                fill_color=circle_bg,
                name=f"bg_grid_{cell_num}_icon",
            )
            self._apply_soft_edge(icon_circle, radius_pt=3)

            # Icon / emoji — centered on the circle, large
            self._add_arabic_textbox(
                slide,
                left=cell_left + Cm(0.3),
                top=icon_top,
                width=cell_width - Cm(0.6),
                height=icon_height,
                text=icon,
                font_name=FONT_REGULAR,
                font_size=Pt(32),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.CENTER,
                word_wrap=False,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_grid_{cell_num}_icon",
            )

            # Label — bold, below icon
            label_top = icon_top + icon_height
            self._add_arabic_textbox(
                slide,
                left=cell_left + Cm(0.3),
                top=label_top,
                width=cell_width - Cm(0.6),
                height=Cm(1.2),
                text=label,
                font_name=FONT_EXTRABOLD,
                font_size=Pt(14),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_grid_{cell_num}_label",
            )

            # Description (optional) — regular, below label
            if desc:
                desc_top = label_top + Cm(1.2)
                remaining = cell_height - (desc_top - cell_top) - Cm(0.3)
                self._add_arabic_textbox(
                    slide,
                    left=cell_left + Cm(0.3),
                    top=desc_top,
                    width=cell_width - Cm(0.6),
                    height=max(remaining, Cm(1)),
                    text=desc,
                    font_name=FONT_REGULAR,
                    font_size=Pt(11),
                    bold=False,
                    color=WARM_GRAY,
                    alignment=PP_ALIGN.CENTER,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_grid_{cell_num}_desc",
                )

        # Optional image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(
                    slide, img_path,
                    left=Cm(1), top=Cm(14),
                    max_width=Cm(5), max_height=Cm(3),
                    name="img_icon_grid",
                )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # 7. CYCLE DIAGRAM — Repeating stages in a circular arrangement
    # ------------------------------------------------------------------

    def add_cycle_diagram(self, title, stages, center_label="", notes="", image_prompt=None, use_svg=False):
        """
        Add a cycle diagram slide showing 3-6 stages in a circular layout.

        Auto-selects SVG by default because circular layouts with curved
        arrows are genuinely hard to achieve with basic PPTX shapes.
        Falls back to native shapes if SVG generation fails.

        Args:
            title: Section title (Arabic)
            stages: List of dicts with "label", optional "desc" (3-6 items)
            center_label: Optional label in the center of the cycle
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate a background image
            use_svg: If True, force SVG generation (default: False, but
                     cycle_diagram auto-selects SVG via _should_use_svg)
        """
        self.slide_count += 1
        slide = self._add_content_slide_with_layout()
        self._set_slide_title_for_toc(slide, title)

        # Smart SVG routing (cycle auto-selects SVG — circular layout is hard)
        cycle_data = {"stages": stages, "center_label": center_label}
        if self._try_svg_visual(slide, "cycle", cycle_data, title, notes, use_svg=use_svg):
            return

        # Native PPTX shape fallback (used when SVG generation fails)
        self._add_header_bar(slide, self.lecture_title)
        self._add_section_banner(slide, title, wide=True)
        self.add_depth_wash(slide)

        count = len(stages)
        if count == 0:
            return

        # Center of the cycle arrangement
        center_x = SLIDE_WIDTH // 2
        center_y = Cm(10)  # Vertical center of content area
        radius = Cm(5.5)   # Distance from center to stage centers

        # Stage shape dimensions
        stage_width = Cm(5)
        stage_height = Cm(2.5)
        arrow_size = Cm(1)

        # Calculate positions for each stage using polar coordinates
        # Start at top (270 degrees) and go clockwise (for RTL visual)
        for i, stage in enumerate(stages):
            stage_num = i + 1
            label = stage.get("label", "")
            desc = stage.get("desc", "")

            # Angle: start at top (270°), distribute evenly clockwise
            angle_deg = 270 + (i * 360 / count)
            angle_rad = math.radians(angle_deg)

            # Position of this stage's center
            sx = center_x + int(radius * math.cos(angle_rad))
            sy = int(center_y + radius * math.sin(angle_rad))

            # Stage shape (rounded rectangle)
            stage_left = sx - stage_width // 2
            stage_top = sy - stage_height // 2

            accent = self._get_accent_color()

            stage_shape = self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=stage_left,
                top=stage_top,
                width=stage_width,
                height=stage_height,
                fill_color=accent,
                name=f"stage_{stage_num}",
                corner_radius=0.06,
            )
            self._add_shadow_to_shape(stage_shape, blur_pt=4, opacity_pct=15)

            # Stage label (white text on colored shape)
            self._add_arabic_textbox(
                slide,
                left=stage_left + Cm(0.3),
                top=stage_top + Cm(0.2),
                width=stage_width - Cm(0.6),
                height=Cm(1.2),
                text=label,
                font_name=FONT_EXTRABOLD,
                font_size=Pt(14),
                bold=False,
                color=WHITE,
                alignment=PP_ALIGN.CENTER,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_stage_{stage_num}",
            )

            # Stage description (below label, smaller)
            if desc:
                self._add_arabic_textbox(
                    slide,
                    left=stage_left + Cm(0.3),
                    top=stage_top + Cm(1.3),
                    width=stage_width - Cm(0.6),
                    height=Cm(1),
                    text=desc,
                    font_name=FONT_REGULAR,
                    font_size=Pt(10),
                    bold=False,
                    color=WHITE,
                    alignment=PP_ALIGN.CENTER,
                    word_wrap=True,
                    auto_size=MSO_AUTO_SIZE.NONE,
                    name=f"txt_stage_{stage_num}_desc",
                )

            # Arrow from this stage to the next (clockwise)
            next_i = (i + 1) % count
            next_angle_deg = 270 + (next_i * 360 / count)
            next_angle_rad = math.radians(next_angle_deg)

            # Midpoint between current and next stage for arrow placement
            nx = center_x + int(radius * math.cos(next_angle_rad))
            ny = int(center_y + radius * math.sin(next_angle_rad))
            mid_x = (sx + nx) // 2
            mid_y = (sy + ny) // 2

            # Calculate arrow rotation angle
            dx = nx - sx
            dy = ny - sy
            arrow_angle = math.degrees(math.atan2(dy, dx))

            arrow_shape = self._add_shape(
                slide,
                MSO_SHAPE.NOTCHED_RIGHT_ARROW,
                left=mid_x - arrow_size // 2,
                top=mid_y - arrow_size // 2,
                width=arrow_size,
                height=Cm(0.6),
                fill_color=PRIMARY_BLUE_LIGHT,
                name=f"arrow_{stage_num}_{next_i + 1}",
            )
            arrow_shape.rotation = arrow_angle

        # Center label (optional) — glow effect draws attention to the hub
        if center_label:
            cl_width = Cm(5)
            cl_height = Cm(2)
            center_shape = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=center_x - cl_width // 2,
                top=int(center_y) - cl_height // 2,
                width=cl_width,
                height=cl_height,
                fill_color=WHITE,
                border_color=PRIMARY_BLUE,
                border_width=Pt(2),
                name="txt_center",
            )
            self._apply_glow(center_shape, "2D588C", radius_pt=10, alpha=30)
            tf = center_shape.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = center_label
            self._set_run_font(run, FONT_EXTRABOLD, Pt(14), False, PRIMARY_BLUE)
            self._set_rtl(p)

        # Optional image
        if image_prompt:
            img_path = self._generate_image_for_slide(image_prompt, "content")
            if img_path:
                self._add_image(
                    slide, img_path,
                    left=Cm(1), top=Cm(14),
                    max_width=Cm(5), max_height=Cm(3),
                    name="img_cycle",
                )

        if notes:
            self._add_notes(slide, notes)

    # ------------------------------------------------------------------
    # 8. CONCEPT VISUAL — Dispatcher to the right pattern
    # ------------------------------------------------------------------

    def add_concept_visual(self, title, visual_type, data, notes="", image_prompt=None, use_svg=False):
        """
        Dispatcher method that routes to the correct visual pattern.

        This provides a unified interface for agents to create visual
        slides without needing to know the exact method name. The agent
        specifies the visual_type and the data format that matches it.

        Args:
            title: Section title (Arabic)
            visual_type: One of: "process_flow", "timeline", "stat_cards",
                         "comparison", "icon_grid", "cycle", "quote"
            data: Dict or list — format depends on visual_type:
                  - "process_flow": list of step dicts
                  - "timeline": list of milestone dicts
                  - "stat_cards": list of stat dicts
                  - "comparison": list of column dicts
                  - "icon_grid": list of item dicts
                  - "cycle": list of stage dicts
                  - "quote": dict with "quote" and optional "attribution"
            notes: Speaker notes / Storyline instructions
            image_prompt: Optional prompt to auto-generate an image
            use_svg: If True, force SVG generation for the pattern (default: False)

        Example:
            builder.add_concept_visual(
                title="مراحل التصميم",
                visual_type="process_flow",
                data=[
                    {"num": 1, "label": "التحليل", "desc": "دراسة الاحتياجات"},
                    {"num": 2, "label": "التصميم", "desc": "إعداد المخطط"},
                ]
            )
        """
        vt = visual_type.lower().strip()

        if vt == "process_flow":
            self.add_process_flow(title, steps=data, notes=notes,
                                  image_prompt=image_prompt, use_svg=use_svg)

        elif vt == "timeline":
            self.add_timeline(title, milestones=data, notes=notes,
                              image_prompt=image_prompt, use_svg=use_svg)

        elif vt == "stat_cards":
            self.add_stat_cards(title, stats=data, notes=notes,
                                image_prompt=image_prompt, use_svg=use_svg)

        elif vt == "comparison":
            self.add_comparison(title, columns=data, notes=notes,
                                image_prompt=image_prompt, use_svg=use_svg)

        elif vt == "icon_grid":
            self.add_icon_grid(title, items=data, notes=notes,
                               image_prompt=image_prompt, use_svg=use_svg)

        elif vt == "cycle":
            center = ""
            if isinstance(data, dict):
                center = data.get("center_label", "")
                stages = data.get("stages", [])
            else:
                stages = data
            self.add_cycle_diagram(title, stages=stages, center_label=center,
                                   notes=notes, image_prompt=image_prompt,
                                   use_svg=use_svg)

        elif vt == "quote":
            if isinstance(data, dict):
                quote_text = data.get("quote", "")
                attribution = data.get("attribution", "")
            else:
                quote_text = str(data)
                attribution = ""
            self.add_quote_highlight(title, quote=quote_text,
                                     attribution=attribution, notes=notes,
                                     use_svg=use_svg)

        else:
            # Fallback: unrecognized visual_type — use content slide with bullets
            fallback_note = (
                f"[VISUAL GRAMMAR WARNING] Unrecognized visual_type: '{visual_type}'. "
                f"Falling back to bullet slide. Supported types: process_flow, timeline, "
                f"stat_cards, comparison, icon_grid, cycle, quote."
            )
            if isinstance(data, list):
                bullets = [str(item) for item in data]
            elif isinstance(data, dict):
                bullets = [f"{k}: {v}" for k, v in data.items()]
            else:
                bullets = [str(data)]

            full_notes = f"{fallback_note}\n\n{notes}" if notes else fallback_note
            self.add_content_slide(title, bullets=bullets, notes=full_notes,
                                   image_prompt=image_prompt)
