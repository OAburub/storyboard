# SVG Prompt Engineering Patterns (for Gemini 3.1 Pro)

Source: Practical guide tested in early 2026.

## Key Keywords That Improve Output Quality
- "buttery smooth", "cinematic", "minimal", "isometric", "pastel"
- "ease-in-out timing", "infinite loop", "smooth easing"
- Always specify viewBox (e.g., "viewBox 0 0 500 300")
- Mention `<animate>`, `<animateTransform>`, or `CSS @keyframes inside <style>`
- "clean code, no groups/transform hell, logical layer order"
- "Output only the <svg>...</svg> code" (prevents markdown wrapping)

## Three Proven Prompt Patterns

### Pattern A — Simple & Reliable
```
Generate a complete, standalone animated SVG (no HTML wrapper needed) that shows:
[DESCRIPTION].
Use <animate> and <animateTransform> elements.
viewBox="0 0 500 300", modern flat style, pastel colors, infinite loop, smooth easing.
Output only the <svg>…</svg> code.
```

### Pattern B — Cinematic / Detailed
```
Create a beautiful looping SVG animation:
[MULTI-STEP DESCRIPTION with timing per step].
Use only paths, lines, ellipses and circles.
viewBox 0 0 400 500, [color scheme], very smooth animations with ease-in-out timing, repeat indefinite.
Include <style> with CSS animations if it gives better control.
Give clean, well-commented SVG code.
```

### Pattern C — Isometric / 3D-ish
```
One-shot prompt: generate an isometric SVG animation
[SCENE DESCRIPTION with motion path].
[Color scheme], flat minimal style with soft shadows.
Smooth 5-7 second loop, use animateMotion along path + scale/rotate transforms.
viewBox 0 0 600 400, infinite repeat, buttery smooth easing.
```

## Iteration Pattern (for refinement)
After first SVG, paste code back and say:
"Make these changes: [specific changes]. Keep everything else almost identical. Output the full updated <svg> code."

## How the Agent Uses This

When planning SVG concept visualizations in the Visual Composition Plan (see `slide-composition.md`), write SVG concept descriptions using these patterns:

**For simple educational diagrams** (process flows, icon grids) → use Pattern A keywords:
```
SVG Concept: "5 connected pipeline chambers flowing right-to-left, each labeled with a stage name, modern flat style, pastel primary/secondary tints"
```

**For rich concept metaphors** (pillars, ecosystems, layered systems) → use Pattern B keywords:
```
SVG Concept: "A building with 5 labeled pillars supporting a roof. First the foundation draws in (2s), then pillars rise sequentially (1s each), then roof settles on top (2s). Minimal flat style, primary blue pillars, accent gold roof."
```

**For architectural/3D-feel visuals** (tech stacks, cloud architecture) → use Pattern C keywords:
```
SVG Concept: "Isometric layered stack — hardware at bottom, OS middle, application top. Each layer slides in from left with soft shadow. Pastel blue-green scheme, flat minimal with depth."
```

## Engine Integration (already applied)

These quality keywords are built into `scripts/_pptx_svg_generator.py`:
- `_build_svg_prompt()` common_style includes: "minimal flat style", "clean code logical layer order", "soft pastel tints", "generous white space"
- Animation mode includes: "buttery smooth easing", "ease-in-out or cubic-bezier", "seamless loop"
- All 8 pattern-specific prompt builders (`_prompt_process_flow`, etc.) benefit from these common keywords
