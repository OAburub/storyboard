"""
PPTX Core Module — SlideEngine base class
==========================================

Contains ALL shared constants, design tokens, color palette, font definitions,
and the SlideEngine base class with every private helper method used by the
public slide-building methods.

This is the foundation that all slide modules import from.

Architecture:
    _pptx_core.py (this file)  — SlideEngine base + constants + helpers
    _pptx_depth.py             — Visual depth system (shadows, gradients)
    _pptx_structural.py        — Structural slide methods (dividers, closings)
    pptx_engine.py             — Thin LectureBuilder composer (public API)

Usage:
    from _pptx_core import SlideEngine, PRIMARY_BLUE, FONT_EXTRABOLD, ...
"""

import os
from datetime import datetime
from typing import Optional

from PIL import Image as PILImage  # For reading image dimensions (aspect ratio)

from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE

# Shared RTL helpers — critical workarounds for Arabic text in python-pptx.
# These functions handle XML-level operations that python-pptx doesn't
# expose natively (paragraph RTL direction, complex script font assignment).
from rtl_helpers import (
    pptx_set_paragraph_rtl,
    pptx_set_paragraph_ltr,
    pptx_set_run_font_arabic,
)

# Image generation — auto-generates images when agent provides a prompt
# but no pre-existing image file. Falls back gracefully if API key missing.
from image_gen import generate_storyboard_image


# ---------------------------------------------------------------------------
# Design Constants — extracted from the real template
# ---------------------------------------------------------------------------

# Template file path — PPTX assets (banners, corners, icons, etc.)
# Auto-detected via _paths module (portable across machines)
from _paths import ASSETS_DIR, PROJECT_ROOT
TEMPLATE_PATH = str(ASSETS_DIR)

# Slide dimensions (EMU) — standard 16:9 widescreen
SLIDE_WIDTH = 12192000
SLIDE_HEIGHT = 6858000

# Color palette — hex values from the template analysis
PRIMARY_BLUE = RGBColor(0x2D, 0x58, 0x8C)     # #2D588C — headings, slide numbers
ACCENT1_BLUE = RGBColor(0x15, 0x60, 0x82)     # #156082 — theme accent1, button fills
BODY_TEXT = RGBColor(0x33, 0x33, 0x33)          # #333333 — body and section titles
SUBTITLE_TEXT = RGBColor(0x26, 0x26, 0x26)      # #262626 — lecture subtitle
LINK_BLUE = RGBColor(0x2E, 0x6C, 0xEC)         # #2E6CEC — summary link text
WHITE = RGBColor(0xFF, 0xFF, 0xFF)              # #FFFFFF — button text, light bg
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)           # Dark background for quiz/card slides
BUTTON_BORDER = RGBColor(0x08, 0x28, 0x36)      # #082836 — button border
NOTES_YELLOW = RGBColor(0xFF, 0xFF, 0x00)       # #FFFF00 — notes callout

# Accent colors for cards and interactive elements
TEAL = RGBColor(0x00, 0x96, 0x88)              # Teal for accent bars
ACCENT_GREEN = RGBColor(0x4C, 0xAF, 0x50)      # Green for correct answers
ACCENT_RED = RGBColor(0xF4, 0x43, 0x36)         # Red for wrong answers
ACCENT_ORANGE = RGBColor(0xFF, 0x98, 0x00)      # Orange for cards
LIGHT_BLUE_BG = RGBColor(0xE3, 0xF2, 0xFD)     # Light blue background

# Professional design colors — added for consultancy-quality slides
CONTENT_CARD_BG = RGBColor(0xF5, 0xF7, 0xFA)    # Light gray for content cards
CONTENT_CARD_BORDER = RGBColor(0xE0, 0xE5, 0xEC) # Subtle border for content cards
CARD_LIGHT_BG = RGBColor(0xFA, 0xFB, 0xFC)       # Very light card body background
OPTION_ALT_BG = RGBColor(0xF0, 0xF4, 0xF8)       # Alternating option background
DIVIDER_BG = RGBColor(0x2D, 0x58, 0x8C)          # Section divider background
BULLET_MARKER_COLOR = RGBColor(0x2D, 0x58, 0x8C) # Blue bullet circles
SHADOW_COLOR = RGBColor(0xE0, 0xE0, 0xE0)        # Lighter shadow color

# Extended palette — tints and shades for visual depth
PRIMARY_BLUE_LIGHT = RGBColor(0x4A, 0x7A, 0xAE)    # Lighter tint of primary
PRIMARY_BLUE_DARK = RGBColor(0x1E, 0x3D, 0x63)      # Darker shade for depth
TEAL_LIGHT = RGBColor(0x4D, 0xBF, 0xB3)             # Lighter teal
WARM_GRAY = RGBColor(0x6B, 0x6B, 0x6B)              # Secondary text color
ACCENT_DEFINITION = RGBColor(0x00, 0x96, 0x88)       # Teal for definitions
ACCENT_EXAMPLE = RGBColor(0xFF, 0x98, 0x00)          # Orange for examples

# Header bar color — a slightly darker blue for the top banner
HEADER_BAR_BLUE = RGBColor(0x2D, 0x58, 0x8C)

# 5-color accent rotation cycle for visual variety across slides
ACCENT_CYCLE = [PRIMARY_BLUE, ACCENT1_BLUE, TEAL, ACCENT_ORANGE, PRIMARY_BLUE_LIGHT]

# PNG asset file names (extracted from the template)
ASSET_BANNER_NARROW = "banner_narrow.png"   # Section banner (objectives, content slides)
ASSET_BANNER_WIDE = "banner_wide.png"       # Activity/summary banner (wider)
ASSET_OBJECTIVE_ROW = "objective_row.png"   # Gradient bar for objective rows
ASSET_TARGET_ICON = "target_icon.png"       # Target/circle icon at end of objective rows
ASSET_PLAY_ICON = "play_icon.png"           # Play button triangle icon (title slide)
ASSET_HAND_CURSOR = "hand_cursor.png"       # Hand cursor icon (title slide)

# Additional template assets — decorative elements for visual variety
ASSET_CORNER_TR = "corner_tr.png"          # Decorative corner, top-right
ASSET_CORNER_BL = "corner_bl.png"          # Decorative corner, bottom-left
ASSET_TEXT_BUBBLE = "text_bubble.png"       # Speech/thought bubble shape
ASSET_IMAGE_FRAME = "image_frame.png"      # Frame for image placeholders
ASSET_CONTENT_BG = "content_bg.png"        # Subtle texture background

# Font names — Tajawal is the primary font from the template.
# We set it on cs_font (Complex Script) for Arabic rendering,
# and also on latin_font and ea_font for consistency.
# STORYLINE REQUIREMENT: Developer must install Tajawal fonts
# before importing. Download: https://fonts.google.com/specimen/Tajawal
FONT_EXTRABOLD = "Tajawal ExtraBold"
FONT_MEDIUM = "Tajawal Medium"
FONT_REGULAR = "Tajawal"
FONT_FALLBACK = "Sakkal Majalla"  # Fallback if Tajawal not installed

# Positions (EMU) — extracted from the template's exact coordinates
# These ensure shapes land in the same spots as the original template.

# Lecture title bar — appears on slides 2-8 at the top center
TITLE_BAR_LEFT = 3405034
TITLE_BAR_TOP = 114300
TITLE_BAR_WIDTH = 5181600
TITLE_BAR_HEIGHT = 369332

# Section banner — centered below title bar
BANNER_LEFT = 4790969
BANNER_TOP = 898751
BANNER_WIDTH = 2610062
BANNER_HEIGHT = 695099

# Wider banner — used on activity and summary slides
WIDE_BANNER_LEFT = 3884635
WIDE_BANNER_TOP = 860142
WIDE_BANNER_WIDTH = 4422731
WIDE_BANNER_HEIGHT = 695099

# Wide banner text position (from template)
WIDE_BANNER_TEXT_LEFT = 3818244
WIDE_BANNER_TEXT_TOP = 977750
WIDE_BANNER_TEXT_WIDTH = 4555512
WIDE_BANNER_TEXT_HEIGHT = 400110

# Narrow banner text position (from template)
NARROW_BANNER_TEXT_LEFT = 4947367
NARROW_BANNER_TEXT_TOP = 1035917
NARROW_BANNER_TEXT_WIDTH = 2297266
NARROW_BANNER_TEXT_HEIGHT = 369332

# Content area — main body region for text
CONTENT_LEFT = 900000       # ~2.5cm from left
CONTENT_TOP = 2000000       # ~5.5cm from top
CONTENT_WIDTH = 10300000    # ~28.6cm wide
CONTENT_HEIGHT = 4000000    # ~11.1cm tall

# Text margins (EMU) — the template uses 0.25cm left/right, 0.13cm top/bottom
TEXT_MARGIN_LR = Cm(0.25)
TEXT_MARGIN_TB = Cm(0.13)


class SlideEngine:
    """
    Base class for building PPTX slides from scratch.

    Provides the presentation setup, all private helper methods,
    and shared state (slide count, layout cycle, accent index).

    Subclasses or composers add public slide methods on top of
    this foundation.

    Attributes:
        project_code: Short code like "DSAI" or "NJR01"
        unit_number: Integer unit number (1, 2, 3, ...)
        unit_name: Arabic name of the unit
        institution: Arabic name of the university/institution
        designer: Name of the instructional designer
        prs: The python-pptx Presentation object
        slide_count: Running count of slides (for page numbering)
    """

    def __init__(
        self,
        project_code: str,
        unit_number: int,
        unit_name: str,
        institution: str,
        designer: str = "",
        template_path: str = None,
    ):
        """
        Initialize a new SlideEngine.

        Opens the template PPTX as the base presentation (gets backgrounds,
        headers, footers, logos from the layouts), then deletes all example
        slides so we start with a clean slate.

        Args:
            project_code: Short project identifier (e.g., "DSAI")
            unit_number: Unit number (e.g., 1)
            unit_name: Arabic name of the unit
            institution: Arabic name of the institution
            designer: Name of the instructional designer (optional)
            template_path: Path to the template PPTX file (optional override)

        Visual output:
            Sets up an empty presentation with these dimensions:
            +------------------------------------------+
            |                                          |
            |          12192000 EMU (33.87cm)           |
            |                                          |
            |  6858000 EMU                             |
            |  (19.05cm)                               |
            |                                          |
            +------------------------------------------+
        """
        # Resolve the template file path
        if template_path and os.path.exists(template_path):
            tpl_path = template_path
        else:
            # Default: look for the template in the standard download location
            tpl_path = os.path.join(
                os.path.expanduser("~"),
                "Downloads",
                "storyboard template",
                "قالب المحاضرة التفاعلية- عربي.pptx",
            )

        # Open the template as the base presentation — this gives us all
        # the layout backgrounds, header bars, footer bars, and logos
        if os.path.exists(tpl_path):
            self.prs = Presentation(tpl_path)
            # Delete ALL existing example slides from the template
            # The rId attribute uses a namespace prefix, so we use the full URI
            _REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            while len(self.prs.slides) > 0:
                sld_id_elem = self.prs.slides._sldIdLst[0]
                rId = sld_id_elem.get(f'{{{_REL_NS}}}id')
                self.prs.part.drop_rel(rId)
                self.prs.slides._sldIdLst.remove(sld_id_elem)
        else:
            # Fallback: create blank presentation if template not found
            self.prs = Presentation()
            self.prs.slide_width = SLIDE_WIDTH
            self.prs.slide_height = SLIDE_HEIGHT

        # Store the assets directory path for PNG images
        self.assets_dir = TEMPLATE_PATH

        # Store project metadata for reuse across slides
        self.project_code = project_code
        self.unit_number = unit_number
        self.unit_name = unit_name
        self.institution = institution
        self.designer = designer

        # Build the lecture title string that appears on every slide (2+)
        # Format: "المحاضرة [N]: [unit_name]"
        self.lecture_title = ""  # Will be set by add_title_slide

        # Track slide count for automatic page numbering
        self.slide_count = 0

        # Layout variant cycle for content slides (0=A, 1=B, 2=C)
        self._content_layout_cycle = 0

        # Accent color rotation index — cycles through ACCENT_CYCLE
        self._accent_index = 0

    # -----------------------------------------------------------------------
    # ACCENT COLOR ROTATION
    # -----------------------------------------------------------------------

    def _get_accent_color(self, index=None):
        """
        Return the next accent color from the 5-color rotation cycle.

        If index is provided, returns the color at that position.
        Otherwise uses and advances the internal counter.

        Args:
            index: Optional explicit index into the cycle

        Returns:
            RGBColor from ACCENT_CYCLE
        """
        if index is not None:
            return ACCENT_CYCLE[index % len(ACCENT_CYCLE)]
        color = ACCENT_CYCLE[self._accent_index % len(ACCENT_CYCLE)]
        self._accent_index += 1
        return color

    # -----------------------------------------------------------------------
    # FINALIZE & SAVE
    # -----------------------------------------------------------------------

    def finalize(self):
        """
        Set up cross-slide references after all slides are added.

        Call this BEFORE save() to:
        - Link btn_start on the title slide to slide 2
        - Any other cross-slide click actions

        Example:
            >>> builder.add_title_slide(...)
            >>> builder.add_objectives_slide(...)
            >>> builder.finalize()  # Sets up cross-slide links
            >>> builder.save("output.pptx")
        """
        if len(self.prs.slides) > 1:
            title_slide = self.prs.slides[0]
            for shape in title_slide.shapes:
                if hasattr(shape, 'name') and shape.name == "btn_start":
                    shape.click_action.target_slide = self.prs.slides[1]
                    break

    def save(self, filepath: str):
        """
        Save the presentation to a file.

        Automatically calls finalize() to set up cross-slide links,
        then creates any necessary directories and writes the .pptx file.

        Args:
            filepath: Output file path (e.g., "output/DSAI/U01/lecture.pptx")

        Example:
            >>> builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
        """
        # Set up cross-slide references
        self.finalize()

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        self.prs.save(filepath)

    # -----------------------------------------------------------------------
    # PRIVATE HELPER METHODS
    # -----------------------------------------------------------------------

    def _calculate_adaptive_spacing(self, item_count, available_top, available_bottom, min_item_height):
        """
        Calculate item height and gap to fit N items between top and bottom bounds.

        This prevents content from overflowing past the page number area.
        If items don't fit at their preferred height, they shrink to fit.

        Args:
            item_count: Number of items to fit
            available_top: Top of available area (EMU)
            available_bottom: Bottom of available area (EMU)
            min_item_height: Preferred/minimum height per item (EMU)

        Returns:
            (item_height, gap) — both in EMU
        """
        if item_count <= 0:
            return min_item_height, 0

        available = available_bottom - available_top
        min_gap = Cm(0.2)  # Minimum gap between items

        # Total space needed at preferred height
        total_needed = item_count * min_item_height + max(item_count - 1, 0) * min_gap
        if total_needed <= available:
            # Everything fits — distribute extra space as gaps
            item_height = min_item_height
            remaining = available - (item_count * item_height)
            gap = remaining // max(item_count - 1, 1)
        else:
            # Too many items — shrink height to fit
            gap = min_gap
            total_gaps = gap * max(item_count - 1, 0)
            item_height = (available - total_gaps) // item_count

        return item_height, gap

    def _add_slide_with_layout(self, layout_index):
        """
        Add a slide using a specific layout from the template.

        Layout 0 = "Title Slide" (has full background image, logo, line)
        Layout 1 = "Title and Content" (has bg, header bar, footer bar, logo)

        CRITICAL: Do NOT modify any placeholder shapes on the returned slide.
        Always use slide.shapes.add_textbox() for text content.

        Args:
            layout_index: Index of the layout to use (0 or 1)

        Returns:
            The new slide object.
        """
        # Use the template's layouts (they contain all background elements)
        try:
            slide_layout = self.prs.slide_layouts[layout_index]
        except IndexError:
            # Fallback to layout 0 if index out of range
            slide_layout = self.prs.slide_layouts[0]
        return self.prs.slides.add_slide(slide_layout)

    def _add_content_slide_with_layout(self):
        """
        Add a content slide using Layout 1 ("Title and Content").

        This layout provides:
        - Background image (nearly white/subtle texture)
        - Header bar (blue gradient rounded bar PNG)
        - Footer bar (blue strip at bottom)
        - University logo (top-left corner)

        Returns:
            The new slide object with all template visuals.
        """
        return self._add_slide_with_layout(1)

    def _add_header_bar(self, slide, title: str, subtitle: str = "", color=None):
        """
        Add the lecture title bar at the top of a slide.

        This bar appears on slides 2+ and shows the lecture name
        in centered ExtraBold text.

        Args:
            slide: The slide object
            title: Text to display in the bar
            subtitle: Optional subtitle text (not commonly used)
            color: Text color override (defaults to BODY_TEXT)

        Visual output:
            +------------------------------------------+
            |       [  Lecture Title Text  ]            |
            +------------------------------------------+
            The bar is 14.39cm wide, centered horizontally on the slide.
        """
        text_color = color if color else BODY_TEXT

        self._add_arabic_textbox(
            slide,
            left=TITLE_BAR_LEFT,
            top=TITLE_BAR_TOP,
            width=TITLE_BAR_WIDTH,
            height=TITLE_BAR_HEIGHT,
            text=title,
            font_name=FONT_EXTRABOLD,
            font_size=Pt(18),
            bold=False,
            color=text_color,
            alignment=PP_ALIGN.CENTER,
            name="header_title",
        )

    def _add_section_banner(self, slide, title: str, wide: bool = False):
        """
        Add a section banner using PNG image with dark text.

        Uses the actual template PNG images (banner_narrow.png or banner_wide.png)
        instead of colored rectangles. Text color is #333333 (dark) on the
        light grey/blue PNG background.

        Args:
            slide: The slide object
            title: Banner title text
            wide: If True, uses the wider banner (for activities/summary)

        Visual output:
            +------------------------------------------+
            |        [======= Title =======]           |
            +------------------------------------------+
        """
        if wide:
            banner_left = WIDE_BANNER_LEFT
            banner_top = WIDE_BANNER_TOP
            banner_width = WIDE_BANNER_WIDTH
            banner_height = WIDE_BANNER_HEIGHT
            text_left = WIDE_BANNER_TEXT_LEFT
            text_top = WIDE_BANNER_TEXT_TOP
            text_width = WIDE_BANNER_TEXT_WIDTH
            text_height = WIDE_BANNER_TEXT_HEIGHT
            asset_name = ASSET_BANNER_WIDE
            font_size = Pt(20)
        else:
            banner_left = BANNER_LEFT
            banner_top = BANNER_TOP
            banner_width = BANNER_WIDTH
            banner_height = BANNER_HEIGHT
            text_left = NARROW_BANNER_TEXT_LEFT
            text_top = NARROW_BANNER_TEXT_TOP
            text_width = NARROW_BANNER_TEXT_WIDTH
            text_height = NARROW_BANNER_TEXT_HEIGHT
            asset_name = ASSET_BANNER_NARROW
            font_size = Pt(18)

        # Banner background — PNG image from the template
        banner_path = os.path.join(self.assets_dir, asset_name)
        if os.path.exists(banner_path):
            pic = slide.shapes.add_picture(
                banner_path,
                banner_left,
                banner_top,
                banner_width,
                banner_height,
            )
            pic.name = "header_banner"
        else:
            # Fallback: colored rectangle if PNG not found
            self._add_shape(
                slide,
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left=banner_left,
                top=banner_top,
                width=banner_width,
                height=banner_height,
                fill_color=PRIMARY_BLUE,
                name="header_banner",
            )

        # Banner title text — dark color #333333 on light PNG bg
        self._add_arabic_textbox(
            slide,
            left=text_left,
            top=text_top,
            width=text_width,
            height=text_height,
            text=title,
            font_name=FONT_EXTRABOLD,
            font_size=font_size,
            bold=False,
            color=BODY_TEXT,     # #333333 — dark text on light banner
            alignment=PP_ALIGN.CENTER,
            name="header_banner_text",
        )

    def _add_arabic_textbox(
        self,
        slide,
        left: int,
        top: int,
        width: int,
        height: int,
        text: str,
        font_name: str = FONT_REGULAR,
        font_size=Pt(16),
        bold: bool = False,
        color: RGBColor = BODY_TEXT,
        alignment=PP_ALIGN.RIGHT,
        word_wrap: bool = True,
        auto_size=MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT,
        line_spacing: float = None,
        name: str = None,
    ):
        """
        Add a text box with Arabic RTL text to a slide.

        This is the core text-rendering helper. Every text element in the
        presentation goes through this method, which ensures:
        1. Correct RTL paragraph direction
        2. Arabic language tag (ar-JO)
        3. Proper font assignment (cs_font, latin_font, ea_font)
        4. Consistent margins and sizing

        Args:
            slide: The slide object to add the textbox to
            left: Left position in EMU
            top: Top position in EMU
            width: Width in EMU
            height: Height in EMU
            text: The Arabic text to display
            font_name: Font name (default: Tajawal)
            font_size: Font size in Pt (default: 16pt)
            bold: Whether to make the text bold
            color: Text color as RGBColor
            alignment: Paragraph alignment (RIGHT for RTL body text)
            word_wrap: Whether to wrap text
            auto_size: Auto-size behavior
            line_spacing: Line spacing multiplier (e.g., 1.5)

        Returns:
            The created textbox shape.
        """
        txBox = slide.shapes.add_textbox(left, top, width, height)
        if name:
            txBox.name = name
        tf = txBox.text_frame
        tf.word_wrap = word_wrap
        tf.auto_size = auto_size
        tf.margin_left = TEXT_MARGIN_LR
        tf.margin_right = TEXT_MARGIN_LR
        tf.margin_top = TEXT_MARGIN_TB
        tf.margin_bottom = TEXT_MARGIN_TB

        # Use the first (default) paragraph
        p = tf.paragraphs[0]
        p.alignment = alignment

        # Set line spacing — default 1.3 for body text (>= 18pt) for Arabic readability
        if line_spacing:
            p.line_spacing = line_spacing
        elif font_size >= Pt(18):
            p.line_spacing = 1.3

        # Add the text run
        run = p.add_run()
        run.text = text

        # Apply font settings
        self._set_run_font(run, font_name, font_size, bold, color)

        # Set RTL direction — critical for Arabic text
        self._set_rtl(p)

        return txBox

    def _set_run_font(self, run, font_name: str, font_size, bold: bool, color: RGBColor):
        """
        Apply font settings to a text run.

        Sets size, bold, and color using the python-pptx API, then delegates
        to the shared rtl_helpers.pptx_set_run_font_arabic() for the font
        name assignment. This ensures the font is set on all three slots
        (cs, latin, ea) via XML for reliable Arabic rendering.

        Args:
            run: The text run to style
            font_name: Font family name (e.g., "Tajawal ExtraBold")
            font_size: Font size (Pt value)
            bold: Whether to bold the text
            color: Text color as RGBColor
        """
        font = run.font
        font.size = font_size
        font.bold = bold
        font.color.rgb = color

        # Delegate font name + language to the shared RTL helper.
        # This sets cs, latin, ea fonts and the ar-JO language tag via XML.
        pptx_set_run_font_arabic(run, font_name)

    def _set_rtl(self, paragraph):
        """
        Set paragraph direction to RTL for Arabic text.

        Delegates to the shared rtl_helpers.pptx_set_paragraph_rtl().

        Args:
            paragraph: The paragraph object to set RTL on
        """
        pptx_set_paragraph_rtl(paragraph)

    def _validate_bounds(self, left, top, width, height, context=""):
        """
        Warn if a shape would extend beyond slide boundaries.

        Prints a console warning when shapes overflow — helps catch
        layout bugs during development without crashing production.

        Args:
            left: Left position in EMU
            top: Top position in EMU
            width: Width in EMU
            height: Height in EMU
            context: Description of the shape (e.g., "bg_col1_card")
        """
        right_edge = left + width
        bottom_edge = top + height
        if right_edge > SLIDE_WIDTH:
            overflow_cm = (right_edge - SLIDE_WIDTH) / 360000
            print(f"⚠ OVERFLOW: {context} extends {overflow_cm:.1f}cm beyond right edge")
        if bottom_edge > SLIDE_HEIGHT:
            overflow_cm = (bottom_edge - SLIDE_HEIGHT) / 360000
            print(f"⚠ OVERFLOW: {context} extends {overflow_cm:.1f}cm beyond bottom edge")

    def _add_shape(
        self,
        slide,
        shape_type,
        left: int,
        top: int,
        width: int,
        height: int,
        fill_color: RGBColor = None,
        border_color: RGBColor = None,
        border_width=None,
        name: str = None,
        corner_radius: float = None,
    ):
        """
        Add a shape to a slide with optional fill and border.

        Used for rectangles, rounded rectangles, ovals, etc. that make up
        the visual structure of slides (banners, cards, buttons, etc.)

        Args:
            slide: The slide object
            shape_type: MSO_SHAPE enum value (e.g., MSO_SHAPE.RECTANGLE)
            left: Left position in EMU
            top: Top position in EMU
            width: Width in EMU
            height: Height in EMU
            fill_color: Optional solid fill color
            border_color: Optional border color
            border_width: Optional border width (Pt value)
            name: Optional shape name (for Storyline identification)
            corner_radius: Optional corner radius for rounded rectangles (0.0 to 1.0)

        Returns:
            The created shape object.
        """
        # Check for overflow before creating the shape
        self._validate_bounds(left, top, width, height, name or "unnamed_shape")

        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        if name:
            shape.name = name

        if fill_color:
            shape.fill.solid()
            shape.fill.fore_color.rgb = fill_color

        if border_color:
            shape.line.color.rgb = border_color
            if border_width:
                shape.line.width = border_width
        else:
            # No border — set to no line
            shape.line.fill.background()

        # Set custom corner radius for rounded rectangles
        if corner_radius is not None and shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
            # adjustments[0] controls corner radius (0.0 to 1.0)
            shape.adjustments[0] = corner_radius

        return shape

    def _add_shadow_to_shape(self, shape, blur_pt=6, dist_pt=3, direction=2700000, opacity_pct=25):
        """
        Add a real OOXML outer shadow effect to a shape.

        Uses effectLst > outerShdw for professional drop shadows that
        Storyline 360 respects (standard OOXML effects).

        Args:
            shape: The shape to add shadow to
            blur_pt: Shadow blur radius in points (default: 6)
            dist_pt: Shadow distance in points (default: 3)
            direction: Shadow direction in 60000ths of degree (default: 2700000 = bottom-right)
            opacity_pct: Shadow opacity 0-100 (default: 25)
        """
        from lxml import etree

        nsmap = {
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        }

        # Build shadow XML
        blur_emu = blur_pt * 12700  # Points to EMU
        dist_emu = dist_pt * 12700
        alpha_val = (100 - opacity_pct) * 1000  # Convert to OOXML alpha (0=opaque, 100000=transparent)

        shadow_xml = (
            f'<a:outerShdw xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            f' blurRad="{blur_emu}" dist="{dist_emu}" dir="{direction}" rotWithShape="0">'
            f'<a:srgbClr val="000000"><a:alpha val="{alpha_val}"/></a:srgbClr>'
            f'</a:outerShdw>'
        )
        shadow_elem = etree.fromstring(shadow_xml)

        # Find or create effectLst on the shape's spPr
        spPr = shape._element.spPr
        effectLst = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        if effectLst is None:
            effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')

        effectLst.append(shadow_elem)

    def _add_decorative_corner(self, slide, position="top_right",
                               color=None, size=None):
        """
        Draw a decorative corner accent using shapes instead of low-res PNGs.

        Creates 2 thin lines (horizontal + vertical) meeting at the corner,
        plus a small arc for elegance. Scales perfectly at any resolution.

        Args:
            slide: The slide object
            position: "top_right" or "bottom_left"
            color: Line color (default: WHITE)
            size: Overall size of the corner decoration (default: Cm(4))
        """
        line_color = color if color else WHITE
        corner_size = size if size else Cm(4)
        line_thickness = Pt(2)

        if position == "top_right":
            # Horizontal line extending left from top-right corner area
            self._add_shape(
                slide, MSO_SHAPE.RECTANGLE,
                left=SLIDE_WIDTH - Cm(3) - corner_size,
                top=Cm(2.5),
                width=corner_size,
                height=line_thickness,
                fill_color=line_color,
                name="deco_corner_tr_h",
            )
            # Vertical line extending down from top-right corner area
            self._add_shape(
                slide, MSO_SHAPE.RECTANGLE,
                left=SLIDE_WIDTH - Cm(3),
                top=Cm(2.5),
                width=line_thickness,
                height=corner_size,
                fill_color=line_color,
                name="deco_corner_tr_v",
            )
            # Small circle at the corner junction for elegance
            dot_size = Cm(0.4)
            self._add_shape(
                slide, MSO_SHAPE.OVAL,
                left=SLIDE_WIDTH - Cm(3) - dot_size // 2,
                top=Cm(2.5) - dot_size // 2,
                width=dot_size,
                height=dot_size,
                fill_color=line_color,
                name="deco_corner_tr_dot",
            )
        elif position == "bottom_left":
            # Horizontal line extending right from bottom-left corner area
            self._add_shape(
                slide, MSO_SHAPE.RECTANGLE,
                left=Cm(3),
                top=SLIDE_HEIGHT - Cm(2.5),
                width=corner_size,
                height=line_thickness,
                fill_color=line_color,
                name="deco_corner_bl_h",
            )
            # Vertical line extending up from bottom-left corner area
            self._add_shape(
                slide, MSO_SHAPE.RECTANGLE,
                left=Cm(3),
                top=SLIDE_HEIGHT - Cm(2.5) - corner_size,
                width=line_thickness,
                height=corner_size,
                fill_color=line_color,
                name="deco_corner_bl_v",
            )
            # Small circle at the corner junction
            dot_size = Cm(0.4)
            self._add_shape(
                slide, MSO_SHAPE.OVAL,
                left=Cm(3) - dot_size // 2,
                top=SLIDE_HEIGHT - Cm(2.5) - dot_size // 2,
                width=dot_size,
                height=dot_size,
                fill_color=line_color,
                name="deco_corner_bl_dot",
            )

    # ------------------------------------------------------------------
    # IMAGE GENERATION HELPER — Auto-generate images from prompts
    # ------------------------------------------------------------------

    def _generate_image_for_slide(self, image_prompt, image_type, topic_key=None):
        """
        Generate an image using the project's visual direction.

        Called by slide methods when an image_prompt is provided but no
        image_path. Uses the project's config.json visual direction
        (prefix, suffix, negative rules) to build the final prompt.

        Args:
            image_prompt: Description of the image to generate
            image_type: One of "content", "card", "section", "two_column",
                       "closing", "quiz" — used for aspect ratio lookup
            topic_key: Optional cache key (e.g. "design_thinking").
                      If an image already exists for this key, returns
                      the cached path instead of regenerating.

        Returns:
            Absolute path to the generated image file, or None if
            generation failed or no project_code is set.
        """
        if not image_prompt or not self.project_code:
            return None
        try:
            result = generate_storyboard_image(
                prompt=image_prompt,
                project_code=self.project_code,
                unit_number=self.unit_number or 1,
                image_type=image_type,
                topic_key=topic_key,
            )
            if result["success"]:
                return result["path"]
        except Exception:
            # Graceful fallback — image generation is optional
            pass
        return None

    # ------------------------------------------------------------------
    # IMAGE HELPERS — Smart image placement with aspect ratio preservation
    # ------------------------------------------------------------------

    def _get_image_dimensions(self, image_path, max_width, max_height):
        """
        Calculate display dimensions that fit inside a bounding box
        while preserving the image's natural aspect ratio.

        Uses min(scale_w, scale_h) — so the image NEVER stretches or
        overflows the bounding box. A portrait image stays tall,
        a landscape image stays wide.

        Args:
            image_path: Path to the image file (PNG, JPG, etc.)
            max_width: Maximum allowed width in EMU
            max_height: Maximum allowed height in EMU

        Returns:
            Tuple of (display_width, display_height) in EMU,
            or None if the file can't be read.
        """
        try:
            with PILImage.open(image_path) as img:
                img_w, img_h = img.size  # pixels

            # Calculate scale factors for width and height
            scale_w = max_width / img_w
            scale_h = max_height / img_h

            # Use the SMALLER scale — this ensures the image fits
            # entirely within the box without overflowing either dimension
            scale = min(scale_w, scale_h)

            display_w = int(img_w * scale)
            display_h = int(img_h * scale)
            return (display_w, display_h)
        except Exception:
            return None

    def _add_image(self, slide, image_path, left, top, max_width, max_height,
                   name=None, center_in_area=True):
        """
        Smart image inserter with aspect ratio preservation and centering.

        This is the main method agents use to add images to slides.
        It handles:
        - Aspect ratio preservation (never stretches)
        - Centering within bounding box (so images look balanced)
        - Missing file guard (returns None instead of crashing)
        - Shape naming for Storyline selection pane

        Args:
            slide: The slide object to add the image to
            image_path: Path to the image file (PNG, JPG, etc.)
            left: Left edge of bounding box (EMU)
            top: Top edge of bounding box (EMU)
            max_width: Maximum width of bounding box (EMU)
            max_height: Maximum height of bounding box (EMU)
            name: Shape name for Storyline (e.g., "img_content")
            center_in_area: If True, center the image within the box

        Returns:
            The picture shape object, or None if image file is missing.
        """
        # Guard: don't crash if the file doesn't exist
        if not image_path or not os.path.exists(image_path):
            return None

        # Calculate display size that fits within the bounding box
        dims = self._get_image_dimensions(image_path, max_width, max_height)
        if dims is None:
            return None

        display_w, display_h = dims

        # Center the image within the bounding box
        if center_in_area:
            # Offset to center horizontally and vertically
            offset_left = (max_width - display_w) // 2
            offset_top = (max_height - display_h) // 2
            img_left = left + offset_left
            img_top = top + offset_top
        else:
            img_left = left
            img_top = top

        # Check for overflow before adding
        self._validate_bounds(img_left, img_top, display_w, display_h,
                              name or "unnamed_image")

        # Add the picture to the slide
        pic = slide.shapes.add_picture(
            image_path,
            left=img_left,
            top=img_top,
            width=display_w,
            height=display_h,
        )

        # Name the shape for Storyline's Selection Pane
        if name:
            pic.name = name

        return pic

    def _add_accent_stripe(self, slide, color=None):
        """
        Add a vertical accent stripe on the right side of the slide.

        Used in content slide Variant B for visual variety.
        The stripe provides a colorful accent that breaks the monotony
        of full-width content cards.

        Args:
            slide: The slide object
            color: Stripe color (default: PRIMARY_BLUE_LIGHT)
        """
        stripe_color = color if color else PRIMARY_BLUE_LIGHT
        self._add_shape(
            slide,
            MSO_SHAPE.RECTANGLE,
            left=Cm(31),
            top=Cm(4),
            width=Cm(1.2),
            height=Cm(13),
            fill_color=stripe_color,
            name="bg_accent_stripe",
        )

    def _add_numbered_points(self, slide, items, start_top=Cm(5.5), left=Cm(3), width=Cm(28)):
        """
        Add content as numbered points with circle badges instead of bullets.

        Used in content slide Variant C for visual variety.
        Each point gets a numbered circle badge (RTL: badge on right side).

        Args:
            slide: The slide object
            items: List of point strings
            start_top: Starting Y position
            left: Starting X position
            width: Width of content area
        """
        point_spacing = Cm(2.5)

        for i, item_text in enumerate(items):
            point_top = int(start_top + i * point_spacing)
            point_num = i + 1

            # Number badge (circle on the right for RTL)
            badge_size = Cm(1.8)
            badge = self._add_shape(
                slide,
                MSO_SHAPE.OVAL,
                left=left + width - badge_size,
                top=point_top,
                width=badge_size,
                height=badge_size,
                fill_color=PRIMARY_BLUE,
                name=f"num_point_{point_num}",
            )
            tf = badge.text_frame
            tf.word_wrap = False
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = str(point_num)
            self._set_run_font(run, FONT_EXTRABOLD, Pt(18), False, WHITE)

            # Point text (to the left of badge for RTL)
            self._add_arabic_textbox(
                slide,
                left=left,
                top=point_top,
                width=width - badge_size - Cm(0.5),
                height=badge_size,
                text=item_text,
                font_name=FONT_REGULAR,
                font_size=Pt(20),
                bold=False,
                color=BODY_TEXT,
                alignment=PP_ALIGN.RIGHT,
                word_wrap=True,
                auto_size=MSO_AUTO_SIZE.NONE,
                name=f"txt_point_{point_num}",
            )

    def _add_footer(self, slide):
        """
        Add a footer to the slide (placeholder for future use).

        The template doesn't have a visible footer on content slides,
        but this method is here for completeness and can be extended
        if needed for specific project requirements.

        Args:
            slide: The slide object
        """
        pass

    def _add_notes(self, slide, notes_text: str):
        """
        Add speaker notes to a slide.

        Speaker notes are used to store Storyline instructions,
        correct answers, image links, and other metadata that
        shouldn't be visible on the slide itself.

        Args:
            slide: The slide object
            notes_text: The notes content
        """
        notes_slide = slide.notes_slide
        notes_tf = notes_slide.notes_text_frame
        notes_tf.text = notes_text

    def _set_slide_title_for_toc(self, slide, title_text: str):
        """
        Set a hidden title for Storyline TOC (Table of Contents).

        Storyline 360 reads the slide title placeholder to populate its
        sidebar menu. Without a title, slides appear as "Untitled Slide".

        This adds an off-screen textbox named "title" that Storyline
        reads but learners never see.

        Args:
            slide: The slide object
            title_text: Arabic title text for the TOC entry
        """
        # Place far off-screen so it's invisible in the presentation
        txBox = slide.shapes.add_textbox(
            left=-Cm(20),
            top=-Cm(20),
            width=Cm(10),
            height=Cm(2),
        )
        txBox.name = "title"
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = title_text
        self._set_run_font(run, FONT_REGULAR, Pt(12), False, WHITE)
        self._set_rtl(p)

    def _build_import_instructions(self, lecture_title: str):
        """
        Build Storyline 360 import instructions for the developer.

        Returns a formatted string to be placed in the title slide's
        speaker notes, giving the Storyline developer everything they
        need to import and configure the presentation.
        """
        now = datetime.now().strftime("%Y-%m-%d")
        return (
            "=== STORYLINE 360 IMPORT INSTRUCTIONS ===\n\n"
            f"Project: {self.project_code}\n"
            f"Unit: {self.unit_number}\n"
            f"Lecture: {lecture_title}\n"
            f"Generated: {now}\n"
            f"Designer: {self.designer}\n\n"
            "--- REQUIRED FONTS ---\n"
            "Install BEFORE importing:\n"
            "  1. Tajawal ExtraBold\n"
            "  2. Tajawal Medium\n"
            "  3. Tajawal (Regular)\n"
            "Download: https://fonts.google.com/specimen/Tajawal\n\n"
            "--- IMPORT STEPS ---\n"
            "1. File > Import > PowerPoint\n"
            "2. Select THIS .pptx file\n"
            "3. Import ALL slides\n"
            "4. Story Size: 1280 x 720 pixels (must match)\n\n"
            "--- POST-IMPORT QA ---\n"
            "[ ] Verify TOC shows Arabic slide titles (not 'Untitled')\n"
            "[ ] Verify fonts render correctly (Tajawal family)\n"
            "[ ] Check RTL text direction on all slides\n"
            "[ ] Test all interactive elements (buttons, quiz, drag-drop)\n"
            "[ ] Verify speaker notes contain Storyline instructions per slide\n\n"
            "--- SHAPE NAMING CONVENTION ---\n"
            "txt_*  = Text elements\n"
            "btn_*  = Clickable buttons (add triggers)\n"
            "icon_* = Decorative icons\n"
            "bg_*   = Background shapes\n"
            "opt_*  = Quiz option shapes (add triggers)\n"
            "num_*  = Numbered elements\n"
            "title  = Hidden TOC title (do not move)\n"
        )

    def _add_bullet_list(
        self,
        slide,
        left: int,
        top: int,
        width: int,
        height: int,
        items: list,
        font_size=Pt(16),
        color: RGBColor = None,
        name: str = None,
    ):
        """
        Add a bullet list as a text box with multiple paragraphs.

        Each item becomes a separate paragraph. RTL direction is set
        on every paragraph for consistent Arabic rendering.

        Args:
            slide: The slide object
            left: Left position in EMU
            top: Top position in EMU
            width: Width in EMU
            height: Height in EMU
            items: List of bullet point strings
            font_size: Font size for bullet text
            color: Text color (default: BODY_TEXT)
            name: Optional shape name

        Returns:
            The created textbox shape.
        """
        text_color = color if color else BODY_TEXT

        txBox = slide.shapes.add_textbox(left, top, width, height)
        if name:
            txBox.name = name
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = TEXT_MARGIN_LR
        tf.margin_right = TEXT_MARGIN_LR
        tf.margin_top = TEXT_MARGIN_TB
        tf.margin_bottom = TEXT_MARGIN_TB

        for i, item_text in enumerate(items):
            # Use the existing first paragraph for the first item,
            # add new paragraphs for subsequent items
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()

            p.alignment = PP_ALIGN.RIGHT

            # Colored filled circle marker (BULLET_MARKER_COLOR) + body text
            bullet_run = p.add_run()
            bullet_run.text = "\u25CF "  # Filled circle character
            self._set_run_font(bullet_run, FONT_REGULAR, Pt(16), False, BULLET_MARKER_COLOR)

            text_run = p.add_run()
            text_run.text = item_text
            self._set_run_font(text_run, FONT_REGULAR, font_size, False, text_color)
            self._set_rtl(p)

            # Comfortable spacing for Arabic bullet items
            p.space_before = Pt(10)
            p.space_after = Pt(10)
            p.line_spacing = 1.4

        return txBox
