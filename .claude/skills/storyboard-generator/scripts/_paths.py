"""
Path auto-detection for the Storyboard Generator engine.

This module finds the project root and key directories automatically,
so the skill works on any machine without hardcoded paths.

Usage (in python3 -c calls):
    import sys, os
    # Bootstrap: find scripts/ from project root
    _p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
    sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))

    from _paths import PROJECT_ROOT, SCRIPTS_DIR, ASSETS_DIR
    from pptx_engine import LectureBuilder

Usage (inside engine modules):
    from _paths import PROJECT_ROOT, ASSETS_DIR
"""

import os
import subprocess
from pathlib import Path


def _find_project_root() -> Path:
    """
    Find the project root directory.

    Strategy (in order):
    1. git rev-parse --show-toplevel (works in any subdirectory of a git repo)
    2. Walk up from this file: scripts/ -> storyboard-generator/ -> skills/ -> .claude/ -> PROJECT_ROOT
    3. Fall back to current working directory
    """
    # Strategy 1: git
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Strategy 2: walk up from this file
    # _paths.py is at: PROJECT_ROOT/.claude/skills/storyboard-generator/scripts/_paths.py
    # So parent x5 = PROJECT_ROOT
    candidate = Path(__file__).resolve().parent.parent.parent.parent.parent
    if (candidate / ".claude").is_dir():
        return candidate

    # Strategy 3: fallback
    return Path.cwd()


# === Exported paths (use these in engine modules) ===

# Project root directory (where CLAUDE.md, projects/, output/ live)
PROJECT_ROOT = _find_project_root()

# This scripts/ directory (where engine .py files live)
SCRIPTS_DIR = Path(__file__).resolve().parent

# Skill root directory (storyboard-generator/)
SKILL_DIR = SCRIPTS_DIR.parent

# Assets directory (PPTX decorative images, icons, etc.)
ASSETS_DIR = SKILL_DIR / "assets" / "pptx_assets"

# References directory (documentation loaded by the agent on-demand)
REFERENCES_DIR = SKILL_DIR / "references"

# Common project paths
PROJECTS_DIR = PROJECT_ROOT / "projects"
OUTPUT_DIR = PROJECT_ROOT / "output"
