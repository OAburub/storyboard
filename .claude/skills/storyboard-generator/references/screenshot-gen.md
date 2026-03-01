# HTML Screenshot — Reference

**When to load this file**: When building a **Screen** (Output Type 4) or an **Infographic** (Output Type 3, 2nd priority) using HTML+CSS via Playwright.

---

## When to Use

HTML+CSS is an **organizational tool**, not a drawing tool. It arranges text, images, embedded SVGs, and other elements with precise layout control. Use it for:

- **Screens** (Output Type 4 — the ONLY method):
  - **UI mockups** — software interfaces, dashboards, forms, portals
  - **Activity previews** — what a drag-and-drop, matching, or quiz activity looks like
  - **Video scenes / شاشة توضيحية** — what the learner sees on screen at each moment in a motion video
  - **Motion graphics scenes** — scene compositions for video storyboards
- **Infographics** (Output Type 3 — 2nd priority, when SVG text limitations are a problem):
  - Data visualizations with rich Arabic text
  - Multi-column structured layouts
  - Stats panels, icon+text layouts

### What goes INSIDE the HTML

Screens and infographics often contain images. Source those images using their output type's priority order:
- Need a **photo** inside the screen? → Freepik stock first, then AI raster (Gemini)
- Need an **illustration** inside? → Freepik stock first, then Recraft, then SVG
- Need a **diagram** inside? → Embed inline SVG

See `references/principles.md` → "The Visual Palette" for the full decision framework.

### Template Strategy for Many Screens

When a project requires many screens (e.g., a motion video with 8+ scenes, or an activity with many steps), build a **reusable HTML template** and a script to fill it with per-screen data. This ensures visual consistency across all screens.

### Embedding External Images

Use **Freepik stock images** (via MCP) when the HTML visual needs a real photo or illustration. See [Using Freepik Stock Images](#using-freepik-stock-images) below.

## 3-Step Workflow

### Step 1 — Write HTML to file

Save to: `output/{PROJECT}/U{XX}/screenshots/{name}.html`

Use the template below. Fill in the UI content. Keep the viewport at exact target dimensions — no scrollbars.

### Step 2 — Run screenshot script

```bash
python3 .claude/skills/storyboard-generator/scripts/screenshot_gen.py \
  output/{PROJECT}/U{XX}/screenshots/{name}.html \
  output/{PROJECT}/U{XX}/screenshots/{name}.png \
  [width] [height] [wait_ms]
```

| Arg | Default | Notes |
|-----|---------|-------|
| width | 1280 | Match viewport in HTML |
| height | 720 | Match viewport in HTML |
| wait_ms | 500 | Use 1500 if loading Google Fonts |

Output: prints path on success · `CACHED: path` if PNG already exists (reuse it) · `ERROR: ...` on failure.

### Step 3 — Use in builder

Pass the PNG path as `image_path` to any builder method. `image_path` always wins over `image_prompt`.

```python
# DOCX (VideoBuilder scene)
builder.add_scene(..., image_path="output/NJR01/U02/screenshots/login_screen.png")

# PPTX
builder.add_content_slide(..., image_path="output/NJR01/U02/screenshots/dashboard.png")
```

---

## HTML Template

```html
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Tajawal', Arial, sans-serif;
    direction: rtl;
    width: 1280px;
    height: 720px;
    overflow: hidden;
    background: #f0f2f5;
    color: #1a1a2e;
  }
</style>
</head>
<body>
  <!-- UI content here — stays within 1280×720, no scrolling -->
</body>
</html>
```

**Offline / no Google Fonts**: remove the `@import` line and use `font-family: Arial, sans-serif` — renders instantly, no wait_ms needed.

---

## Common Viewport Sizes

| Use Case | width | height |
|----------|-------|--------|
| Lecture slide / widescreen | 1280 | 720 |
| Desktop app / dashboard | 1440 | 900 |
| Mobile app | 390 | 844 |
| Tablet | 768 | 1024 |

---

## Design Rules for Arabic UI Mockups

- Always `dir="rtl"` on `<html>` and `lang="ar"`
- Navigation: rightmost item = primary (RTL flow)
- Use realistic Arabic placeholder text — not "lorem ipsum"
- Brand colors: check `projects/{code}/config.json` → `branding` section
- Keep it realistic: show actual UI state (logged in, data visible, not empty states unless that's the point)
- No remote/hotlinked images inside the mockup HTML (network fetch slows render) — download first via Freepik MCP, then reference as a local `file://` path

---

## Caching

If `{name}.png` already exists, the script prints `CACHED: path` and exits 0.
**Do not regenerate** — reuse the cached path. Same mockup can be referenced multiple times across slides.

---

## Using Freepik Stock Images

When the HTML visual would benefit from a real photo or illustration (a person at a computer, a meeting scene, a background texture, an icon set), use Freepik MCP to search and download before building the HTML.

### When to use Freepik vs other tools

| Need | Tool |
|------|------|
| Real photo or illustration (person, scene, object) | **Freepik MCP** |
| Abstract concept / metaphor / custom diagram | **SVG via Gemini** |
| Photorealistic custom scene (no stock match) | **AI image gen** |
| Pure layout, data, text, shapes | **Native HTML+CSS** |

### Workflow

**Step 1 — Search**

Use the `mcp__plugin_freepik_freepik__freepik_search` tool with relevant English keywords:

```
keywords: "team meeting arabic office"
type: photo or vector
orientation: horizontal (for wide slides) / vertical (for portrait panels)
```

Scan the results. Pick the ID whose title/type best matches the visual need.

**Step 2 — Download**

Use `mcp__plugin_freepik_freepik__freepik_download` with the chosen resource ID. The tool downloads the file to the configured Freepik download directory and returns the local file path.

**Step 3 — Embed in HTML**

Reference the downloaded file using an absolute `file://` path in the `<img>` tag or as a CSS `background-image`. Local files render instantly — no extra wait_ms needed.

```html
<!-- img tag -->
<img src="file:///C:/Users/name/Downloads/freepik/image.jpg"
     style="width:100%; height:100%; object-fit:cover;">

<!-- CSS background -->
<div style="background-image: url('file:///C:/Users/name/Downloads/freepik/image.jpg');
            background-size: cover; background-position: center;">
</div>
```

**Important path formatting on Windows**: use forward slashes and three slashes after `file:` — e.g. `file:///C:/path/to/image.jpg`.

### Design tips

- Overlay a semi-transparent color layer on top of photos so Arabic text remains legible:
  ```css
  background: linear-gradient(rgba(10,20,60,0.55), rgba(10,20,60,0.55)),
              url('file:///...') center/cover;
  ```
- Keep the image as a background or decorative element — the HTML layout still carries the content
- If the downloaded file is an SVG or vector format, it can be used directly in `<img src>` or inlined

---

## Error Handling

On `ERROR:` output:
1. Check HTML file exists at the path you wrote
2. Check Playwright is installed: `python -m playwright --version`
3. Check Chromium: `python -m playwright install chromium`
4. Try increasing wait_ms if content looks blank
