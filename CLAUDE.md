# Storyboard Generator

AI-powered system that transforms raw client course content into production-ready educational storyboard documents (DOCX/PPTX) for Arabic e-learning courses. PPTX output is designed for direct import into Storyline 360.

## Entry Point

Use `/storyboard` command or invoke the `storyboard-generator` skill. All instructions, engine scripts, references, and assets live in `.claude/skills/storyboard-generator/`.

## Project Structure

```
projects/[code]/config.json       — Per-project metadata, branding, visual direction
projects/[code]/branding/         — Logos, headers per client
output/[project-code]/U[XX]/      — Generated storyboard files
```

### File Naming Convention

```
[PROJECT_CODE]_U[UNIT_NUMBER]_[Element_Type]
```

### Project Setup

When starting a new project, collect:
- Project code (e.g., `NJR01`), project name, client name, institution
- Client logo + header image file paths
- Designer name
- Unit count and names

Save to: `projects/[project-code]/config.json`

## Content Input

- User shares **file paths** — read them directly using Read tool
- Content can be: .pptx, .docx, .pdf, images, .txt
- Each content share = one complete unit

## Key Rules

1. **One agent** — main agent coordinates AND generates content (no subagents)
2. **One at a time** — generate each storyboard type with user review between each
3. **Engine builds documents** — call Python builders via Bash, never construct documents manually
4. **Arabic RTL** — all content in Arabic, right-to-left, no tashkeel/diacritics
5. **User decides** — AI suggests, user approves before proceeding
