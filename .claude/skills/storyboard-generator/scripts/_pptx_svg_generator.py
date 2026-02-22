"""
SVG Visual Generator — Uses Gemini AI to create professional SVG visuals for slides.
====================================================================================

Each visual pattern gets a tailored prompt that produces beautiful, RTL-ready SVGs.
SVGs are converted to PNG for embedding in PPTX (python-pptx cannot embed SVG directly).

Pipeline: Gemini generates SVG -> cairosvg converts to PNG -> python-pptx embeds PNG

Animated SVGs: When animated=True, the SVG includes CSS @keyframes animations.
These are saved as standalone .svg files for web/Storyline use (PNG strips animation).

Architecture:
    This module is used by _pptx_visual_grammar.py methods.
    Each method tries SVG generation first, then falls back to shape-based rendering.

Usage:
    from _pptx_svg_generator import generate_slide_svg

    # Static (for PPTX embedding)
    png_path = generate_slide_svg(
        pattern_type="process_flow",
        data=[{"num": 1, "label": "التحليل", "desc": "..."}, ...],
        colors={"primary": "#2D588C", "secondary": "#4A90D9", "accent": "#F5A623"},
        title="مراحل التصميم",
        output_path="output/TEST/U01/slides/slide_3_process.svg"
    )

    # Animated (standalone SVG with CSS @keyframes)
    svg_path = generate_slide_svg(
        pattern_type="process_flow",
        data=[...],
        colors={...},
        title="...",
        output_path="output/TEST/U01/slides/slide_3_process.svg",
        animated=True
    )
"""

import os
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Gemini 3.1 Pro — highest quality SVG generation
# Fallback to 3.0 Pro, then 2.5 Flash if 3.1 is unavailable
MODELS_TO_TRY = [
    "gemini-3.1-pro-preview",
    "gemini-3-pro-preview",
    "gemini-2.5-flash",
]

# SVG canvas dimensions (matches PPTX 16:9 aspect ratio)
SVG_WIDTH = 1280
SVG_HEIGHT = 720

# PNG output resolution (2x for crisp rendering in PPTX)
PNG_WIDTH = 2560
PNG_HEIGHT = 1440


# ---------------------------------------------------------------------------
# API Client
# ---------------------------------------------------------------------------

def _get_client():
    """Get a Gemini API client using the project's API key."""
    from google import genai

    # Reuse the same key logic as image_gen.py
    key = (
        os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
        or "AIzaSyDNpJzwtR62rXRqJs0RCyfF6ldpE3fZ0kY"
    )
    return genai.Client(api_key=key)


# ---------------------------------------------------------------------------
# SVG Prompt Templates — one per visual pattern type
# ---------------------------------------------------------------------------

def _build_svg_prompt(pattern_type, data, colors, title="", animated=False):
    """
    Build a Gemini prompt for generating an SVG visual.

    Each pattern type has a specialized prompt that describes the exact
    visual layout, styling, and data to render.

    Args:
        pattern_type: One of the supported pattern types
        data: Pattern-specific data (list of dicts or dict)
        colors: Dict with "primary", "secondary", "accent" hex colors
        title: Slide title in Arabic
        animated: If True, adds CSS @keyframes animation instructions

    Returns:
        String prompt for Gemini
    """
    primary = colors.get("primary", "#2D588C")
    secondary = colors.get("secondary", "#4A90D9")
    accent = colors.get("accent", "#F5A623")

    # Animation instructions — only when animated=True
    if animated:
        animation_style = """
Animation requirements (CSS @keyframes inside <style> tag):
- Add a <style> block inside the SVG with CSS @keyframes animations
- Cards/shapes should fade in sequentially with staggered delays (0.2s apart)
- Use @keyframes fadeSlideIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
- Arrows should draw in using stroke-dasharray/stroke-dashoffset animation
- Numbers/stats should count up using @keyframes countPulse (scale 0.8 -> 1.0 with opacity)
- Keep animations subtle, cinematic, and professional — no bouncing or spinning
- Buttery smooth easing: use ease-in-out or cubic-bezier for natural motion
- Total animation sequence should complete within 3-5 seconds, then loop smoothly
- Use animation-fill-mode: both so elements stay visible after animating
- Title should fade in first (delay: 0s), then content elements sequentially
- For motion paths use <animateMotion> along smooth bezier paths
- repeatCount="indefinite" for looping animations — make the loop seamless
"""
        static_rule = ""
    else:
        animation_style = ""
        static_rule = "- NO animation tags, NO JavaScript — static SVG only\n"

    # Common style instructions appended to every prompt
    common_style = f"""
Style requirements for the SVG:
- viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
- All text uses font-family="Tajawal, sans-serif"
- All Arabic text must use direction="rtl" and text-anchor="middle" or "end"
- Keep Arabic text labels SHORT (1-3 words max) — long text renders poorly in SVG
- Colors: primary={primary}, secondary={secondary}, accent={accent}
- Background: subtle gradient from #F8F9FA to #EEF2F7
- Use SVG defs for gradients, shadows (feGaussianBlur), and reusable elements
- Cards should have rounded corners (rx="12" or rx="15")
- Add subtle drop shadows using SVG filter with feGaussianBlur
- Modern, premium, minimal flat style — like a top design agency made it
- Use clean code with logical layer order — no unnecessary nested groups or transform chains
- Generous white space — don't overcrowd, let the visual breathe
{static_rule}- NO emojis anywhere — use elegant geometric shapes (circles, hexagons, rounded rectangles) for icons
- Use soft pastel tints of the primary/secondary colors for backgrounds and fills
- Return ONLY the raw SVG code, nothing else — no markdown fences, no explanation
{animation_style}"""

    builders = {
        "process_flow": _prompt_process_flow,
        "stat_cards": _prompt_stat_cards,
        "timeline": _prompt_timeline,
        "comparison": _prompt_comparison,
        "icon_grid": _prompt_icon_grid,
        "cycle": _prompt_cycle,
        "quote": _prompt_quote,
        "content": _prompt_content,
    }

    builder = builders.get(pattern_type)
    if not builder:
        return None

    specific_prompt = builder(data, colors, title)
    return specific_prompt + "\n" + common_style


def _prompt_process_flow(data, colors, title):
    """Prompt for process flow: connected RTL cards with gradients and arrows."""
    primary = colors.get("primary", "#2D588C")
    secondary = colors.get("secondary", "#4A90D9")

    steps_desc = "\n".join(
        f"  Step {s.get('num', i+1)}: {s.get('label', '')} — {s.get('desc', '')}"
        for i, s in enumerate(data)
    )

    rows_hint = "Split into 2 rows (top row right-to-left, then bottom row right-to-left) with a smooth curved connector between rows." if len(data) > 4 else "Single row, right-to-left."

    return f"""Generate a complete, standalone SVG showing a cinematic process flow pipeline.

Title (top center, bold 28px, {primary}): {title}

Steps (flow RIGHT to LEFT for Arabic RTL):
{steps_desc}

Visual concept — think of this as a PIPELINE with connected chambers:
- Each step is a rounded rectangle card (rx=15) with smooth gradient fill from {primary} to {secondary}
- Step number in a white circle badge (glow effect) floating above each card
- Step label in white bold 18px centered on the card
- Step description in white 13px below the label, generous padding inside
- Cards connected by smooth curved SVG path arrows pointing LEFT (←), not straight lines
- Arrow paths use quadratic bezier curves for elegant flow
- {rows_hint}
- Each card has a soft drop shadow (feGaussianBlur stdDeviation=4)
- Subtle background: light gradient wash from #F8FAFE to #EEF2F7
- Generous spacing between cards — let the flow breathe"""


def _prompt_stat_cards(data, colors, title):
    """Prompt for stat cards: big numbers in card frames."""
    primary = colors.get("primary", "#2D588C")
    accent = colors.get("accent", "#F5A623")

    cards_desc = "\n".join(
        f"  Card {i+1}: number=\"{s.get('number', '0')}\" label=\"{s.get('label', '')}\" "
        f"trend=\"{s.get('trend', 'none')}\" desc=\"{s.get('desc', '')}\""
        for i, s in enumerate(data)
    )

    return f"""Generate a complete, standalone SVG showing elegant statistic dashboard cards.

Title (top center, bold 28px, {primary}): {title}

Cards:
{cards_desc}

Visual concept — the numbers are the HEROES of this slide:
- {len(data)} cards arranged horizontally with generous equal spacing
- Each card: white rounded rectangle (rx=15) with a 4px colored accent bar at the very top
- The BIG NUMBER is the visual star: 54-60px, bold, colored with the card's accent color
- Add a very subtle glow effect (feGaussianBlur) behind each number to make it pop
- Trend arrow below number: smooth triangle pointing UP (green #27AE60) or DOWN (red #E74C3C)
- Label below trend in dark text (16px), description in gray (13px)
- Card accent colors cycle: {primary}, {accent}, #009688, #FF9800
- Cards have soft drop shadows (feGaussianBlur stdDeviation=4, opacity 0.12)
- Cards feel like they float slightly above the background
- Background: very subtle radial gradient wash centered behind the cards"""


def _prompt_timeline(data, colors, title):
    """Prompt for timeline: horizontal line with milestone markers."""
    primary = colors.get("primary", "#2D588C")

    milestones_desc = "\n".join(
        f"  Milestone {i+1}: date=\"{m.get('year', m.get('date', ''))}\" "
        f"title=\"{m.get('title', '')}\" desc=\"{m.get('desc', '')}\" "
        f"status=\"{m.get('status', 'done')}\""
        for i, m in enumerate(data)
    )

    return f"""Generate a complete, standalone SVG showing a beautiful horizontal timeline journey.

Title (top center, bold 28px, {primary}): {title}

Milestones (RIGHT to LEFT for Arabic RTL):
{milestones_desc}

Visual concept — this is a JOURNEY, not just dots on a line:
- A smooth horizontal path (SVG path, not a straight line — slight wave or gentle curve) across the middle
- The path itself is a gradient stroke from light-gray (start) to {primary} (current)
- Milestone markers ON the path: filled circle with glow for "done" ({primary}), larger pulsing circle for "active" (accent), dashed outline for "pending"
- Done markers: solid fill + subtle inner glow
- Active marker: larger (1.5x), accent color, outer glow ring to draw attention
- Pending markers: outline only, lighter color, suggests "not yet reached"
- Milestones alternate above/below the path for visual rhythm
- Date/year in bold {primary} (16px), title in dark medium (14px), desc in gray (12px)
- Rightmost milestone is the first/earliest (RTL reading direction)
- Generous vertical spacing between marker and text labels
- Thin vertical connector lines from path to text labels"""


def _prompt_comparison(data, colors, title):
    """Prompt for comparison: side-by-side columns."""
    primary = colors.get("primary", "#2D588C")
    default_colors = [primary, "#009688", "#FF9800"]

    columns_desc = "\n".join(
        f"  Column {i+1}: title=\"{c.get('title', '')}\" "
        f"items={c.get('items', [])} "
        f"highlight={c.get('highlight', False)}"
        for i, c in enumerate(data)
    )

    return f"""Generate a complete, standalone SVG showing a clear visual comparison.

Title (top center, bold 28px, {primary}): {title}

Columns (RIGHT to LEFT for Arabic RTL):
{columns_desc}

Visual concept — make the DIFFERENCES visually obvious:
- {len(data)} columns side by side with generous gap between them
- Each column: tall rounded rectangle card (rx=15) with a gradient-filled header section
- Column headers: gradient from each column's color to a slightly darker shade. White title text, bold 18px
- Header colors: {', '.join(default_colors[:len(data)])}
- Below header: each item as a small MINI-CARD (rounded rect, light tint of column color, 8px padding)
- Mini-cards stacked vertically with 8px gap — NOT plain bullet text
- Each mini-card has the item text right-aligned (RTL) in dark 14px
- Highlighted column: slightly larger, bolder shadow, subtle accent border glow
- All cards have soft drop shadows (feGaussianBlur stdDeviation=3)
- Clear visual separation between columns — the comparison should be scannable at a glance"""


def _prompt_icon_grid(data, colors, title):
    """Prompt for icon grid: grid of cards with geometric shapes."""
    primary = colors.get("primary", "#2D588C")
    accent = colors.get("accent", "#F5A623")

    items_desc = "\n".join(
        f"  Item {i+1}: icon=\"{it.get('icon', '')}\" label=\"{it.get('label', '')}\" "
        f"desc=\"{it.get('desc', '')}\""
        for i, it in enumerate(data)
    )

    count = len(data)
    if count <= 4:
        grid = "2x2"
    elif count <= 6:
        grid = "3x2"
    else:
        grid = "3x3"

    return f"""Generate a complete, standalone SVG showing a polished {grid} icon grid.

Title (top center, bold 28px, {primary}): {title}

Items:
{items_desc}

Visual concept — each cell should feel like a mini feature card:
- {grid} grid arranged right-to-left, top-to-bottom with generous 16px gaps
- Each cell: white rounded rectangle (rx=12) with a thin 3px colored accent bar at top
- ICON AREA: a soft-colored circle (50px diameter, 10% opacity of accent color) as background
- Inside the circle: a unique GEOMETRIC SVG SHAPE per cell — each item gets a DIFFERENT shape:
  - Use these in order: circle, hexagon, rounded-square, diamond, triangle, pentagon, star, octagon
  - Shape is 28px, filled with the accent color, centered in the background circle
- Label below icon area in bold dark text (15px), right-aligned for RTL
- Description below label in gray text (12px), right-aligned
- Accent colors cycle: {primary}, {accent}, #009688, #FF9800, #4A7AAE
- Each card has soft drop shadow (feGaussianBlur stdDeviation=3)
- The grid should feel like a feature showcase, not a monotonous wall of boxes"""


def _prompt_cycle(data, colors, title):
    """Prompt for cycle diagram: circular arrangement with arrows."""
    primary = colors.get("primary", "#2D588C")
    accent = colors.get("accent", "#F5A623")

    if isinstance(data, dict):
        stages = data.get("stages", [])
        center_label = data.get("center_label", "")
    else:
        stages = data
        center_label = ""

    stages_desc = "\n".join(
        f"  Stage {i+1}: label=\"{s.get('label', '')}\" desc=\"{s.get('desc', '')}\""
        for i, s in enumerate(stages)
    )

    center_text = f"\nCenter label: {center_label}" if center_label else ""

    return f"""Generate a complete, standalone SVG showing a beautiful circular cycle diagram.

Title (top center, bold 28px, {primary}): {title}
{center_text}

Stages (arranged in a circle, counterclockwise for RTL):
{stages_desc}

Visual concept — this should feel like a living, flowing cycle:
- {len(stages)} stages arranged in a perfect circular layout
- Each stage: rounded rectangle (rx=12) with gradient fill (stage color to slightly darker shade)
- Stage label in white bold 15px, description in white 11px below
- Smooth CURVED arrow paths (SVG quadratic/cubic bezier) connecting each stage to the next
- Arrows follow the circular flow, not straight lines — they should curve elegantly along the circle
- Arrow heads are clean triangles, colored to match the source stage
- Stage colors cycle: {primary}, {accent}, #009688, #FF9800, #4A7AAE
- If center label: elegant white circle with soft shadow, {primary} text, subtle border glow
- Each stage card has soft drop shadow (feGaussianBlur stdDeviation=4)
- The cycle should feel like perpetual motion — stages connected in an unbroken ring
- Generous space between stages and arrows — don't crowd the circle"""


def _prompt_quote(data, colors, title):
    """Prompt for quote highlight: elegant typography."""
    primary = colors.get("primary", "#2D588C")

    if isinstance(data, dict):
        quote_text = data.get("quote", "")
        attribution = data.get("attribution", "")
    else:
        quote_text = str(data)
        attribution = ""

    attr_line = f"\nAttribution: — {attribution}" if attribution else ""

    return f"""Generate a complete, standalone SVG showing typographic art — an elegant breathing slide.

Title (top center, 22px, {primary}): {title}

Quote text: "{quote_text}"
{attr_line}

Visual concept — this is TYPOGRAPHIC ART, the text IS the design:
- Very large decorative quotation marks (» «) in ultra-light pastel ({primary} at 8% opacity), 140px
- Position them as background elements — top-right and bottom-left, slightly rotated for dynamism
- Quote text centered, 26-30px, {primary} color, font-weight 500, generous line-height (1.6x)
- A very subtle decorative line or thin accent bar above and below the quote (3px, accent color, 50% width, centered)
- Attribution below in 15px gray italic text, preceded by em dash
- MASSIVE white space — this slide should feel like a pause, a breath, a moment of reflection
- Background: very subtle radial gradient glow (almost white center, faintly tinted edges)
- No cards, no boxes — just beautiful typography floating in space
- The overall feeling should be calm, premium, editorial"""


def _prompt_content(data, colors, title):
    """Prompt for general content: card-based layout."""
    primary = colors.get("primary", "#2D588C")

    if isinstance(data, list):
        items_desc = "\n".join(f"  - {item}" for item in data)
    elif isinstance(data, dict):
        items_desc = "\n".join(f"  - {k}: {v}" for k, v in data.items())
    else:
        items_desc = f"  - {data}"

    return f"""Generate a complete, standalone SVG showing content in an elegant card layout.

Title (top center, bold 28px, {primary}): {title}

Content:
{items_desc}

Visual concept — premium content card, not a plain text box:
- Main content area: large white rounded rectangle (rx=15) with 4px gradient accent bar at top ({primary} to lighter shade)
- Each content item displayed as a mini-row with:
  - A small colored dot (8px circle, cycling through accent colors) as bullet marker, right-aligned for RTL
  - Item text in 16px dark, right-aligned, generous 1.4x line height
  - Subtle 1px separator line between items (very light gray, 60% width, centered)
- Card has soft drop shadow (feGaussianBlur stdDeviation=4)
- Generous internal padding (24px top/bottom, 32px sides)
- The card should feel like a premium content block, not a plain text dump
- Background: very subtle gradient wash behind the card"""


# ---------------------------------------------------------------------------
# SVG Extraction — parse SVG from Gemini response
# ---------------------------------------------------------------------------

def _extract_svg(response_text):
    """
    Extract SVG code from Gemini response, handling markdown fences.

    Returns the SVG string if found, None otherwise.
    """
    raw = response_text.strip()

    # Case 1: Response wrapped in markdown code fences
    if "```" in raw:
        parts = raw.split("```")
        for part in parts[1:]:
            stripped = part.strip()
            if "<svg" in stripped:
                # Remove language tag on first line if present
                first_line = stripped.split("\n", 1)[0].strip().lower()
                if first_line in ("svg", "xml", "html"):
                    stripped = stripped.split("\n", 1)[1]
                return stripped.strip()

    # Case 2: Raw SVG (no fences)
    if "<svg" in raw:
        start = raw.index("<svg")
        return raw[start:].strip()

    return None


# ---------------------------------------------------------------------------
# SVG to PNG Conversion
# ---------------------------------------------------------------------------

def _svg_to_png(svg_path, png_path, width=PNG_WIDTH, height=PNG_HEIGHT):
    """
    Convert SVG to high-resolution PNG using cairosvg.

    Args:
        svg_path: Path to input SVG file
        png_path: Path to output PNG file
        width: Output width in pixels
        height: Output height in pixels

    Returns:
        Path to PNG file if successful, None if conversion fails.
    """
    try:
        import cairosvg
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        cairosvg.svg2png(
            url=svg_path,
            write_to=png_path,
            output_width=width,
            output_height=height,
        )
        return png_path
    except ImportError:
        print("[SVG Generator] cairosvg not installed — cannot convert SVG to PNG")
        return None
    except Exception as e:
        print(f"[SVG Generator] SVG->PNG conversion failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def generate_slide_svg(pattern_type, data, colors, title="", output_path=None, animated=False):
    """
    Generate an SVG visual for a slide pattern using Gemini.

    This is the main function called by visual grammar methods.
    It generates an SVG via Gemini, saves it, converts to PNG,
    and returns the PNG path for embedding in PPTX.

    When animated=True, the SVG includes CSS @keyframes animations
    for web/Storyline use. The SVG file is always saved alongside
    the PNG for independent review.

    Args:
        pattern_type: "process_flow", "stat_cards", "timeline", "comparison",
                     "icon_grid", "cycle", "quote", "content"
        data: Pattern-specific data (list of dicts or dict)
        colors: Dict with "primary", "secondary", "accent" hex colors
        title: Slide title (Arabic)
        output_path: Where to save the .svg file. If None, uses a temp path.
        animated: If True, adds CSS @keyframes animations to the SVG.
                  Animated SVGs are saved as standalone files for web use.
                  PNG conversion strips animations (static snapshot).

    Returns:
        If animated=False: Path to the PNG file (for PPTX embedding).
        If animated=True: Path to the animated SVG file (for web/Storyline).
        Returns None if generation fails.
    """
    # Build the prompt with animation flag
    prompt = _build_svg_prompt(pattern_type, data, colors, title, animated=animated)
    if not prompt:
        print(f"[SVG Generator] Unknown pattern type: {pattern_type}")
        return None

    # Determine output paths
    if not output_path:
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        anim_suffix = "_animated" if animated else ""
        output_path = f"/tmp/svg_slide_{pattern_type}{anim_suffix}_{ts}.svg"

    svg_path = str(output_path)
    # PNG goes alongside the SVG
    png_path = svg_path.rsplit(".", 1)[0] + ".png"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(svg_path) or ".", exist_ok=True)

    # Try Gemini models in preference order
    client = _get_client()
    svg_code = None
    used_model = None

    for model_name in MODELS_TO_TRY:
        try:
            print(f"[SVG Generator] Trying {model_name}...", flush=True)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            svg_code = _extract_svg(response.text)
            if svg_code and "<svg" in svg_code:
                used_model = model_name
                print(f"[SVG Generator] {model_name} succeeded ({len(svg_code)} chars)", flush=True)
                break
            svg_code = None
        except Exception as e:
            print(f"[SVG Generator] {model_name} failed: {e}")
            continue

    if not svg_code:
        print(f"[SVG Generator] All models failed for pattern: {pattern_type}")
        return None

    # Save SVG
    try:
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)
    except Exception as e:
        print(f"[SVG Generator] Failed to save SVG: {e}")
        return None

    # For animated SVGs, return the SVG path directly
    # (PNG conversion strips CSS animations — the SVG is the deliverable)
    if animated:
        print(f"[SVG Generator] Animated SVG saved: {svg_path}", flush=True)
        return svg_path

    # For static SVGs, convert to PNG for PPTX embedding
    result_png = _svg_to_png(svg_path, png_path)
    if result_png:
        return result_png

    # If PNG conversion fails, return the SVG path
    # (caller will need to handle this — likely skip SVG embedding)
    print("[SVG Generator] PNG conversion failed, returning SVG path")
    return svg_path
