#!/usr/bin/env python3
"""
Storyboard Image Generator
Wraps Nano Banana Pro (Gemini 3 Pro Image) with project-specific visual direction,
caching, and cultural rules enforcement for Arabic e-learning storyboards.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# API Configuration (using google-genai SDK)
# ---------------------------------------------------------------------------
MODEL_NAME = "gemini-3-pro-image-preview"

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
RESOLUTIONS = ["1K", "2K", "4K"]

# Project root — auto-detected (portable across machines)
from _paths import PROJECT_ROOT


# ---------------------------------------------------------------------------
# API Key
# ---------------------------------------------------------------------------
def _load_dotenv():
    """Load .env file if python-dotenv is installed (optional)."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass


def get_api_key():
    """
    Get Gemini API key.
    Checks (in order): GOOGLE_API_KEY env -> GEMINI_API_KEY env -> embedded fallback.
    """
    _load_dotenv()
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if not key:
        # Embedded fallback key for convenience
        key = "AIzaSyDNpJzwtR62rXRqJs0RCyfF6ldpE3fZ0kY"

    return key


# ---------------------------------------------------------------------------
# Visual Direction & Prompt Building
# ---------------------------------------------------------------------------
def load_visual_direction(project_code: str) -> dict:
    """
    Load visual direction from a project's config.json.

    Returns the visualDirection dict, or sensible defaults if missing.
    """
    config_path = PROJECT_ROOT / "projects" / project_code / "config.json"
    if not config_path.exists():
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config.get("visualDirection", {})


def build_storyboard_prompt(raw_prompt: str, visual_direction: dict) -> str:
    """
    Build a final prompt by applying project visual direction.

    Applies:
      1. promptPrefix (prepended)
      2. raw user prompt
      3. promptSuffix (style descriptors)
      4. negativeRules (as explicit IMPORTANT instructions)
    """
    parts = []

    # 1. Prefix (if any)
    prefix = visual_direction.get("promptPrefix", "").strip()
    if prefix:
        parts.append(prefix)

    # 2. Core prompt from the agent
    parts.append(raw_prompt.strip())

    # 3. Style suffix
    suffix = visual_direction.get("promptSuffix", "").strip()
    if suffix:
        parts.append(suffix)

    # 4. Negative rules as explicit instructions
    for rule in visual_direction.get("negativeRules", []):
        parts.append(f"IMPORTANT: {rule}")

    return ". ".join(parts)


# ---------------------------------------------------------------------------
# Prompt Optimization (from Nano Banana Pro)
# ---------------------------------------------------------------------------
def optimize_prompt(raw_prompt: str, context: dict = None) -> str:
    """
    Optimize a raw prompt for better image generation.
    Adds quality enhancers based on content type.
    """
    context = context or {}
    parts = [raw_prompt.strip()]

    # Add style context if provided
    if context.get("style"):
        parts.append(f"Style: {context['style']}")

    # Quality enhancers by content type
    content_type = context.get("content_type", "illustration")
    quality_enhancers = {
        "photo": "high-quality, professional photography, sharp focus, natural lighting",
        "illustration": "clean lines, professional illustration, detailed artwork",
        "logo": "clean, minimalist, professional logo design, vector-style",
        "infographic": "clear layout, professional infographic, readable text, organized structure",
        "ui": "modern UI design, clean interface, professional mockup",
        "icon": "clean icon design, simple, recognizable, consistent style",
        "marketing": "professional marketing material, eye-catching, brand-appropriate",
        "diagram": "clear diagram, labeled components, professional technical illustration",
        "general": "high-quality, detailed, professional",
    }
    enhancer = quality_enhancers.get(content_type, quality_enhancers["general"])
    parts.append(enhancer)

    # Color context
    if context.get("colors"):
        parts.append(f"Color palette: {context['colors']}")

    # Mood
    if context.get("mood"):
        parts.append(f"Mood: {context['mood']}")

    return ". ".join(parts)


def determine_settings(prompt: str, context: dict = None) -> dict:
    """
    Determine optimal aspect ratio and resolution based on content.
    """
    context = context or {}
    prompt_lower = prompt.lower()

    aspect_ratio = context.get("aspect_ratio") or "1:1"
    resolution = context.get("resolution") or "2K"

    # Auto-detect aspect ratio if not explicitly set
    if not context.get("aspect_ratio"):
        if any(w in prompt_lower for w in ["banner", "header", "hero", "landscape", "panorama", "cover"]):
            aspect_ratio = "16:9"
        elif any(w in prompt_lower for w in ["story", "mobile", "phone", "vertical", "portrait", "poster"]):
            aspect_ratio = "9:16"
        elif any(w in prompt_lower for w in ["social", "instagram", "square", "icon", "logo", "avatar"]):
            aspect_ratio = "1:1"

    # Auto-detect resolution
    if not context.get("resolution"):
        if any(w in prompt_lower for w in ["4k", "high-res", "print", "poster", "large"]):
            resolution = "4K"
        elif any(w in prompt_lower for w in ["thumbnail", "icon", "small", "preview"]):
            resolution = "1K"

    return {"aspect_ratio": aspect_ratio, "resolution": resolution}


# ---------------------------------------------------------------------------
# Caching
# ---------------------------------------------------------------------------
def get_cached_image(project_code: str, unit_number: int, topic_key: str) -> str | None:
    """
    Check if an image already exists for this topic.

    Looks in: output/{project_code}/U{unit_number:02d}/images/{topic_key}.png

    Returns:
        Absolute path string if cached image exists, None otherwise.
    """
    if not topic_key:
        return None

    image_dir = PROJECT_ROOT / "output" / project_code / f"U{unit_number:02d}" / "images"
    cached_path = image_dir / f"{topic_key}.png"

    if cached_path.exists():
        return str(cached_path.absolute())

    return None


# ---------------------------------------------------------------------------
# Base Image Generation (from Nano Banana Pro)
# ---------------------------------------------------------------------------
def generate_image(
    prompt: str,
    input_image: str = None,
    output_path: str = None,
    aspect_ratio: str = None,
    resolution: str = None,
    content_type: str = None,
    style: str = None,
    colors: str = None,
    mood: str = None,
    raw_prompt: bool = False,
) -> dict:
    """
    Generate or edit an image using Nano Banana Pro (Gemini 3 Pro Image).

    Uses the google-genai SDK for reliable API communication.

    Two modes:
      1. TEXT-TO-IMAGE: Just provide a prompt
      2. IMAGE EDITING: Provide prompt + input_image

    Returns:
        dict with 'success', 'path', 'prompt_used', and optionally 'error'
    """
    from google import genai
    from google.genai import types

    api_key = get_api_key()

    # Build context
    context = {
        "content_type": content_type,
        "style": style,
        "colors": colors,
        "mood": mood,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }

    # Optimize prompt unless raw mode
    if raw_prompt:
        final_prompt = prompt
    else:
        final_prompt = optimize_prompt(prompt, context)

    # Determine settings
    settings = determine_settings(prompt, context)
    final_aspect_ratio = aspect_ratio or settings["aspect_ratio"]
    final_resolution = resolution or settings["resolution"]

    # Validate
    if final_aspect_ratio not in ASPECT_RATIOS:
        return {"success": False, "error": f"Invalid aspect ratio. Use one of: {ASPECT_RATIOS}"}
    if final_resolution not in RESOLUTIONS:
        return {"success": False, "error": f"Invalid resolution. Use one of: {RESOLUTIONS}"}

    # Build contents for the API call
    contents = [final_prompt]

    # Add input image for editing mode
    if input_image:
        try:
            img_path = Path(input_image)
            if not img_path.exists():
                return {"success": False, "error": f"Image not found: {input_image}"}

            import mimetypes
            mime_type = mimetypes.guess_type(input_image)[0] or "image/png"
            with open(img_path, "rb") as f:
                image_bytes = f.read()

            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        except Exception as e:
            return {"success": False, "error": f"Failed to load input image: {str(e)}"}

    # API call using google-genai SDK
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )
    except Exception as e:
        return {"success": False, "error": f"API request failed: {str(e)}"}

    # Extract image data from response
    try:
        if not response.candidates:
            return {"success": False, "error": "No image generated"}

        image_data = None
        text_response = None

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
            elif part.text:
                text_response = part.text

        if not image_data:
            return {"success": False, "error": "No image in response", "text": text_response}

    except Exception as e:
        return {"success": False, "error": f"Failed to parse response: {str(e)}"}

    # Determine output path
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"generated_image_{timestamp}.png"

    # Save image
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "wb") as f:
            f.write(image_data)
    except Exception as e:
        return {"success": False, "error": f"Failed to save image: {str(e)}"}

    return {
        "success": True,
        "path": str(output_path.absolute()),
        "prompt_used": final_prompt,
        "aspect_ratio": final_aspect_ratio,
        "resolution": final_resolution,
        "text_response": text_response,
    }


# ---------------------------------------------------------------------------
# Main Entry Point: Storyboard Image Generation
# ---------------------------------------------------------------------------
def generate_storyboard_image(
    prompt: str,
    project_code: str,
    unit_number: int,
    image_type: str = "content",
    topic_key: str = None,
    output_name: str = None,
    aspect_ratio: str = None,
    resolution: str = None,
) -> dict:
    """
    Generate an image with project visual direction applied.

    This is the main entry point for all storyboard image generation.
    It handles visual direction, caching, cultural rules, and output paths.

    Args:
        prompt:       Description of the image to generate.
        project_code: Project identifier (e.g. "NJR01").
        unit_number:  Unit number (e.g. 2).
        image_type:   Type of image for aspect ratio lookup.
                      One of: "content", "card", "section", "two_column",
                      "closing", "quiz", "hero", "scene", "step", "inline"
        topic_key:    Cache key (e.g. "design_thinking"). If provided and
                      an image already exists, returns the cached path.
        output_name:  Custom filename (without extension). Defaults to
                      topic_key or a timestamp.
        aspect_ratio: Override aspect ratio (e.g. "16:9"). If None, looks
                      up from config.json defaultAspectRatios by image_type.
        resolution:   Override resolution ("1K", "2K", "4K"). If None,
                      uses config.json defaultResolution or "2K".

    Returns:
        On success: {"success": True,  "path": str, "cached": bool}
        On failure: {"success": False, "error": str, "action": "ask_user"}
    """
    # 1. Load visual direction from project config
    visual_direction = load_visual_direction(project_code)

    # 2. Check cache
    if topic_key:
        cached = get_cached_image(project_code, unit_number, topic_key)
        if cached:
            return {"success": True, "path": cached, "cached": True}

    # 3. Resolve aspect ratio from config if not overridden
    if not aspect_ratio:
        # Map image_type to config key names
        type_to_config_key = {
            "content": "content_slide",
            "card": "card_thumbnail",
            "section": "section_bg",
            "two_column": "two_column_header",
            "closing": "closing",
            "quiz": "quiz",
            "hero": "content_slide",
            "scene": "content_slide",
            "step": "content_slide",
            "inline": "content_slide",
        }
        config_key = type_to_config_key.get(image_type, "content_slide")
        ratios = visual_direction.get("defaultAspectRatios", {})
        aspect_ratio = ratios.get(config_key, "1:1")

    # 4. Resolve resolution from config if not overridden
    if not resolution:
        resolution = visual_direction.get("defaultResolution", "2K")

    # 5. Build prompt with visual direction (prefix + prompt + suffix + rules)
    final_prompt = build_storyboard_prompt(prompt, visual_direction)

    # 6. Determine output path
    image_dir = PROJECT_ROOT / "output" / project_code / f"U{unit_number:02d}" / "images"
    if output_name:
        filename = f"{output_name}.png"
    elif topic_key:
        filename = f"{topic_key}.png"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img_{timestamp}.png"
    output_path = image_dir / filename

    # 7. Call the base generate_image function
    try:
        result = generate_image(
            prompt=final_prompt,
            output_path=str(output_path),
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            content_type=visual_direction.get("defaultContentType", "illustration"),
            raw_prompt=True,  # Already built the prompt with visual direction
        )

        if result["success"]:
            return {
                "success": True,
                "path": result["path"],
                "cached": False,
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "action": "ask_user",
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "action": "ask_user",
        }
