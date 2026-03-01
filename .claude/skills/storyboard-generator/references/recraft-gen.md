# Recraft Image Generation via MCP

Recraft generates high-quality **vector (SVG)** and **raster (PNG)** illustrations via MCP tools. Images are saved to `output/recraft/` and passed as `image_path` to any builder method.

## When to Use Recraft

Recraft is the **2nd priority method for Illustrations** (after Freepik stock search). Use it when:
- Freepik stock doesn't have what you need
- You need **style consistency** across many illustrations in the same project
- You need **background removal** (built-in `remove_background` + `vectorize_image` pipeline)
- You need **high-res upscaling** (native 2x upscale)
- You want illustrations that look like they came from the same designer

| Output Type | Recraft's Role |
|-------------|---------------|
| **Illustration** | 2nd priority (after Freepik stock, before SVG via Gemini) |
| **Photo** | Not recommended — use Freepik stock or Gemini AI raster instead |
| **Infographic** | Not the method itself, but can generate illustrations embedded within infographics |
| **Screen** | Not the method itself, but can generate illustrations embedded within screens |

**Cost awareness**: ~$0.04/raster, ~$0.08/vector. Freepik stock is free to search. Use Recraft when the quality/consistency advantage justifies the cost.

## MCP Tools Reference (9 tools)

### Core Generation

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `generate_image` | Generate raster (PNG) or vector (SVG) image | `prompt`, `style` (required), `model`, `size`, `n`, `negative_prompt`, `colors` |
| `generate_image_with_text` | Generate image with embedded text labels | Same as above + text layer support |

### Post-Processing

| Tool | Purpose |
|------|---------|
| `remove_background` | Remove background from an image (returns transparent PNG) |
| `vectorize_image` | Convert raster image to vector SVG |
| `replace_background` | Replace image background with a new one |
| `crisp_upscale` | Upscale image 2x with detail preservation |
| `creative_upscale` | Upscale image 2x with creative enhancement |

### Utility

| Tool | Purpose |
|------|---------|
| `get_user` | Check API balance and account info |
| `create_style` | Create a custom style from reference images for consistency |

## Workflow

### 1. Read Visual Direction

Load from `projects/{code}/config.json` → `visualDirection`:
- `promptPrefix` → prepend to Recraft prompt
- `promptSuffix` → append as style descriptors
- `negativeRules` → pass as Recraft's `negative_prompt` (native support — no need to convert to "IMPORTANT:" instructions)

### 2. Build the Prompt

```
{promptPrefix} {your description of the illustration} {promptSuffix}
```

Write prompts in English. Be specific about composition, elements, and mood.

### 3. Choose Style

Map project `visualDirection.style` to Recraft styles:

| Project Style | Recraft Style | Notes |
|---------------|---------------|-------|
| `vector-flat` | `digital_illustration` or `vector_illustration` | Clean flat vector look |
| `vector-detailed` | `digital_illustration` | More detailed vector |
| `realistic` | `realistic_image` | Photorealistic output |
| `icon` | `icon` | Simple icon style |
| (default) | `digital_illustration` | Safe default for e-learning |

### 4. Choose Size

Map to Recraft dimensions based on where the image will be used:

| Usage | Recraft Size | Aspect |
|-------|-------------|--------|
| Full slide background | `1820x1024` | 16:9 |
| Content slide image | `1365x1024` | 4:3 |
| Card image | `1024x1024` | 1:1 |
| Two-column image | `1024x1365` | 3:4 |
| Hero/banner image | `1820x1024` | 16:9 |
| Icon/small element | `1024x1024` | 1:1 |

### 5. Call the MCP Tool

```
Call generate_image with:
  prompt: "{built prompt}"
  style: "digital_illustration"
  size: "1365x1024"
  negative_prompt: "{negativeRules from config}"
  model: "recraftv3"
```

For vector output, use style `vector_illustration` — Recraft returns SVG natively.

### 6. Use the Result

The MCP tool returns a file path in `output/recraft/`. Pass it directly:

```python
builder.add_content_slide(
    title="...",
    bullets=[...],
    image_path="/absolute/path/returned/by/recraft.png"
)
```

## Style Consistency Across Slides

For a lecture with many illustrations, create a consistent look:

1. **Use the same `style` parameter** for all images in a lecture
2. **Use consistent prompt structure**: same prefix/suffix, similar composition language
3. **Optional**: Use `create_style` with a reference image to create a custom style ID, then pass `style_id` to all subsequent `generate_image` calls

## Cost Awareness

| Operation | Cost |
|-----------|------|
| Raster image (PNG) | ~$0.04 |
| Vector image (SVG) | ~$0.08 |
| Background removal | ~$0.04 |
| Vectorization | ~$0.04 |
| Upscale | ~$0.04 |

Check balance before a large batch: call `get_user` to see remaining credits.

**Compare**: Gemini image generation is free (included in API). Use Recraft when the quality/consistency advantage justifies the cost.

## Caching

Recraft MCP has **no built-in caching**. Before calling `generate_image`:

1. Check if an appropriate image already exists in `output/recraft/` or the project's `output/{PROJECT}/U{XX}/images/` directory
2. If regenerating, the old file is NOT overwritten — Recraft creates new filenames

After generation, you may want to copy/move the file to the project's output directory for organization.

## Error Handling

If a Recraft call fails:
1. Check balance with `get_user` — may be out of credits
2. Check if the prompt violates content policies
3. Fall back to Gemini AI image generation as alternative
4. Ask the user if they want to retry, skip, or provide their own image

## Combining with Other Tools

Recraft images work well in combination:
- **Recraft illustration + native PPTX shapes**: Use the illustration as a visual anchor, add labeled shapes around it
- **Recraft + background removal → overlay on slide**: Generate illustration, remove background, place on gradient/pattern slide
- **Recraft vector → embed as SVG**: Generate vector illustration, use as inline SVG element
