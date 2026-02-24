# HTML Screenshot — Reference

**When to load this file**: When generating any custom visual using HTML+CSS — diagrams, infographics, activity illustrations, video scenes, question visuals, UI screens, or anything requiring precise design control.

---

## When to Use

Use HTML+CSS Screenshot for any visual where you want to control the output precisely:
- **Diagrams and concept visuals** — process flows, concept maps, hierarchies, comparisons
- **Infographics** — data visualizations, stats panels, icon+text layouts
- **Activity illustrations** — show what a drag-and-drop, matching, or quiz activity looks like
- **Video scenes / شاشة توضيحية** — what the learner sees on screen at each moment in a motion video
- **Question visuals** — scenario setups, visual multiple-choice, illustrated prompts
- **UI screens** — when the content happens to involve software (forms, dashboards, portals)
- **Anything where precise layout, color, and Arabic text control matters**

Use **AI-generated images** instead only when you want a photorealistic or stylized illustration (a scene photo, a textural background).

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
- No decorative images inside the mockup HTML (slows render, increases wait_ms)

---

## Caching

If `{name}.png` already exists, the script prints `CACHED: path` and exits 0.
**Do not regenerate** — reuse the cached path. Same mockup can be referenced multiple times across slides.

---

## Error Handling

On `ERROR:` output:
1. Check HTML file exists at the path you wrote
2. Check Playwright is installed: `python -m playwright --version`
3. Check Chromium: `python -m playwright install chromium`
4. Try increasing wait_ms if content looks blank
