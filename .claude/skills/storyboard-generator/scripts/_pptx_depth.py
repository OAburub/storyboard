"""
PPTX Depth System — Visual depth layers for slides.
=====================================================

Provides background washes, accent bars, decorative elements, and
header/banner components. Inspired by the "3-layer depth" concept
from motion graphics:

    Layer 1 (Background) — Subtle washes at 3-8% opacity
    Layer 2 (Content)    — Primary content shapes and text
    Layer 3 (Emphasis)   — Foreground accents, decorative corners

Architecture:
    This is a MIXIN class — it uses `self` to access SlideEngine's
    private helpers (_add_shape, _add_arabic_textbox, etc.) via
    Python's MRO (Method Resolution Order). It does NOT import
    SlideEngine directly (would cause circular imports).

Usage:
    class LectureBuilder(DepthMixin, StructuralMixin, SlideEngine):
        pass

    builder = LectureBuilder(...)
    builder.add_depth_wash(slide, style="corner_oval")
    builder.add_depth_accent(slide, position="right")
"""

from _pptx_core import (
    # Slide dimensions
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    # Colors
    PRIMARY_BLUE,
    WHITE,
    BODY_TEXT,
    OPTION_ALT_BG,
    PRIMARY_BLUE_LIGHT,
    # Fonts
    FONT_EXTRABOLD,
    # Positions — title bar
    TITLE_BAR_LEFT,
    TITLE_BAR_TOP,
    TITLE_BAR_WIDTH,
    TITLE_BAR_HEIGHT,
    # Positions — section banners
    BANNER_LEFT,
    BANNER_TOP,
    BANNER_WIDTH,
    BANNER_HEIGHT,
    WIDE_BANNER_LEFT,
    WIDE_BANNER_TOP,
    WIDE_BANNER_WIDTH,
    WIDE_BANNER_HEIGHT,
    WIDE_BANNER_TEXT_LEFT,
    WIDE_BANNER_TEXT_TOP,
    WIDE_BANNER_TEXT_WIDTH,
    WIDE_BANNER_TEXT_HEIGHT,
    NARROW_BANNER_TEXT_LEFT,
    NARROW_BANNER_TEXT_TOP,
    NARROW_BANNER_TEXT_WIDTH,
    NARROW_BANNER_TEXT_HEIGHT,
    # Assets
    ASSET_BANNER_NARROW,
    ASSET_BANNER_WIDE,
)

import os
from pptx.util import Cm, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor


# ---------------------------------------------------------------------------
# Depth-specific color constants
# ---------------------------------------------------------------------------

# Background wash colors — barely visible tints for visual depth
WASH_CORNER_OVAL = RGBColor(0xF0, 0xF4, 0xF8)     # Very light blue-gray
WASH_RADIAL_GLOW = RGBColor(0xF5, 0xF0, 0xEB)      # Very light warm tone
WASH_GRADIENT_STRIP = RGBColor(0xE8, 0xEE, 0xF4)    # Light blue strip

# Accent bar — light tint of primary blue (simulates 30% opacity)
ACCENT_BAR_COLOR = RGBColor(0xC0, 0xD0, 0xE0)       # 30% tint of #2D588C

# Progress dot colors
DOT_ACTIVE_COLOR = WHITE
DOT_INACTIVE_COLOR = RGBColor(0x80, 0x9F, 0xBF)     # Muted blue-gray


class DepthMixin:
    """
    Mixin that adds visual depth capabilities to SlideEngine.

    All methods use `self` to access SlideEngine helpers:
      - self._add_shape()
      - self._add_arabic_textbox()
      - self._add_decorative_corner()  (from _pptx_core)
      - self._add_header_bar()         (from _pptx_core)
      - self._add_section_banner()     (from _pptx_core)
      - self.assets_dir

    The mixin provides both NEW depth methods and PUBLIC wrappers
    around existing private helpers for a clean API.
    """

    # ------------------------------------------------------------------
    # LAYER 1: BACKGROUND WASHES — Subtle shapes at 3-8% visual weight
    # ------------------------------------------------------------------

    def add_depth_wash(self, slide, style="corner_oval"):
        """
        Add a subtle background shape for visual depth.

        These are barely visible shapes that give slides a sense of
        layered depth — like a faint watermark or vignette. They sit
        behind all content and should never distract.

        Args:
            slide: The slide object
            style: Wash style to apply:
                - "corner_oval": Large oval in top-right, very light blue-gray
                - "radial_glow": Centered large oval, warm light tone
                - "gradient_strip": Thin horizontal bar at bottom, light blue
                - "none": Skip (no wash applied)

        Visual output (corner_oval):
            +------------------------------------------+
            |                          ....            |
            |                       ..      ..         |
            |                      .  (oval)  .        |
            |                       ..      ..         |
            |                          ....            |
            |                                          |
            +------------------------------------------+
            The oval is very faint — barely visible background tint.
        """
        if style == "none":
            return

        if style == "corner_oval":
            # Large oval in the top-right quadrant — subtle blue-gray tint
            self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=SLIDE_WIDTH - Cm(16),   # Starts roughly center-right
                top=Cm(-3),                  # Extends slightly above slide
                width=Cm(20),
                height=Cm(14),
                fill_color=WASH_CORNER_OVAL,
                name="bg_depth_wash",
            )

        elif style == "radial_glow":
            # Centered large oval — warm light tone
            oval_w = Cm(18)
            oval_h = Cm(12)
            self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=(SLIDE_WIDTH - oval_w) // 2,
                top=(SLIDE_HEIGHT - oval_h) // 2,
                width=oval_w,
                height=oval_h,
                fill_color=WASH_RADIAL_GLOW,
                name="bg_depth_wash",
            )

        elif style == "gradient_strip":
            # Thin horizontal bar at the bottom — light blue accent
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=0,
                top=SLIDE_HEIGHT - Cm(1.5),
                width=SLIDE_WIDTH,
                height=Cm(1.5),
                fill_color=WASH_GRADIENT_STRIP,
                name="bg_depth_wash",
            )

    # ------------------------------------------------------------------
    # LAYER 3: ACCENT BARS — Thin colored bars for visual rhythm
    # ------------------------------------------------------------------

    def add_depth_accent(self, slide, position="right", color=None):
        """
        Add a thin accent bar for visual rhythm.

        These bars are subtle colored strips along slide edges that
        create a sense of structure and rhythm across slides. They
        use a light tint (simulating 30% opacity) of the given color.

        Args:
            slide: The slide object
            position: Where to place the bar:
                - "right": Thin vertical bar on right edge
                - "left": Thin vertical bar on left edge
                - "bottom": Thin horizontal bar at bottom
            color: Bar color (default: light tint of primary blue)

        Visual output (position="right"):
            +------------------------------------------+
            |                                        | |
            |                                        | |
            |                                        | |  <- 0.3cm wide
            |                                        | |
            |                                        | |
            +------------------------------------------+
        """
        bar_color = color if color else ACCENT_BAR_COLOR
        bar_thickness = Cm(0.3)

        if position == "right":
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=SLIDE_WIDTH - bar_thickness,
                top=Cm(2),           # Start below header area
                width=bar_thickness,
                height=SLIDE_HEIGHT - Cm(4),  # Leave space top and bottom
                fill_color=bar_color,
                name="bg_depth_accent_right",
            )

        elif position == "left":
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=0,
                top=Cm(2),
                width=bar_thickness,
                height=SLIDE_HEIGHT - Cm(4),
                fill_color=bar_color,
                name="bg_depth_accent_left",
            )

        elif position == "bottom":
            self._add_shape(
                slide,
                MSO_SHAPE.RECTANGLE,
                left=Cm(2),
                top=SLIDE_HEIGHT - bar_thickness - Cm(1),
                width=SLIDE_WIDTH - Cm(4),
                height=bar_thickness,
                fill_color=bar_color,
                name="bg_depth_accent_bottom",
            )

    # ------------------------------------------------------------------
    # DECORATIVE CORNERS — Public wrapper around _add_decorative_corner
    # ------------------------------------------------------------------

    def add_decorative_corner(self, slide, position="top_right",
                              color=None, size=None):
        """
        Draw a decorative corner accent (2 lines + dot).

        Public wrapper around SlideEngine._add_decorative_corner().
        Creates 2 thin lines (horizontal + vertical) meeting at the
        corner, plus a small circle at the junction for elegance.

        Args:
            slide: The slide object
            position: "top_right" or "bottom_left"
            color: Line color (default: WHITE)
            size: Overall corner size (default: Cm(4))
        """
        self._add_decorative_corner(slide, position=position,
                                    color=color, size=size)

    # ------------------------------------------------------------------
    # PROGRESS DOTS — Section progress indicator
    # ------------------------------------------------------------------

    def add_progress_dots(self, slide, current, total):
        """
        Show section progress as a row of dots at the bottom of a slide.

        The current section dot is larger and white; other dots are
        smaller and muted blue-gray. Dots are centered horizontally.

        Args:
            slide: The slide object
            current: Current section number (1-based)
            total: Total number of sections

        Visual output:
            +------------------------------------------+
            |                                          |
            |              content area                |
            |                                          |
            |          o   o   O   o   o               |
            +------------------------------------------+
            O = current (larger, white)
            o = other (smaller, muted)
        """
        if total is None or total <= 0:
            return

        dot_size = Cm(0.6)
        dot_gap = Cm(1)
        total_width = total * dot_size + (total - 1) * dot_gap
        dots_left = (SLIDE_WIDTH - total_width) // 2
        dots_top = SLIDE_HEIGHT - Cm(3)

        for i in range(total):
            dot_left = int(dots_left + i * (dot_size + dot_gap))
            is_current = (i + 1) == current

            # Current dot is larger (0.8cm) and white
            dot_color = DOT_ACTIVE_COLOR if is_current else DOT_INACTIVE_COLOR
            dot_shape_size = Cm(0.8) if is_current else dot_size
            # Center the larger dot relative to the baseline
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

    # ------------------------------------------------------------------
    # HEADER BAR — Public wrapper around _add_header_bar
    # ------------------------------------------------------------------

    def add_header_bar(self, slide, title, subtitle="", color=None):
        """
        Add the lecture title bar at the top of a slide.

        Public wrapper around SlideEngine._add_header_bar().
        The bar appears on slides 2+ and shows the lecture name
        in centered ExtraBold text.

        Args:
            slide: The slide object
            title: Text to display in the bar
            subtitle: Optional subtitle text
            color: Text color override (defaults to BODY_TEXT)
        """
        self._add_header_bar(slide, title, subtitle=subtitle, color=color)

    # ------------------------------------------------------------------
    # SECTION BANNER — Public wrapper around _add_section_banner
    # ------------------------------------------------------------------

    def add_section_banner(self, slide, title, wide=False):
        """
        Add a section banner using PNG image with dark text.

        Public wrapper around SlideEngine._add_section_banner().
        Uses template PNG images (banner_narrow.png or banner_wide.png)
        with dark text overlay.

        Args:
            slide: The slide object
            title: Banner title text
            wide: If True, uses wider banner (for activities/summary)
        """
        self._add_section_banner(slide, title, wide=wide)
