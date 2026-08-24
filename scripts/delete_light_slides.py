#!/usr/bin/env python3
"""Delete the slides that are not applicable in Light mode.

Light mode skips tasks 2, 4, 6, 8, 9, 13, 15, 16 and 17, so the matching slides
(5, 6, 9, 10, 13, 14, 27-33 — the list in LIGHT_SKIP_SLIDES_1BASED below) are
left with no data. This script removes them and flags updating the contents page
as a job for the agent.

Usage:
    export PD_MODE=light   # the mode must be set
    python3 delete_light_slides.py <path-to-presentation.pptx>

Input and output are the same file — the script modifies it in place.

⚠️ The script REFUSES to run in Full mode (PD_MODE=full) without --force.
   That is the guard: Full mode needs all 34 slides for the investor.
"""
import sys
import os
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# Mode guard — prevents losing 13 slides in Full mode
# ═══════════════════════════════════════════════════════════════════════════
_mode = os.environ.get("PD_MODE", "").lower()
_force = "--force" in sys.argv

if _mode == "full" and not _force:
    print("🔴 REFUSING: PD_MODE=full, and this script is for Light only.")
    print()
    print("In Full mode the deck must keep all 34 slides,")
    print("including trends, PESTEL, CJM, the alternative scenario and PMF.")
    print()
    print("If the mode was set by mistake, reset it: export PD_MODE=light")
    print("If you really do need to delete slides in Full, pass --force — but you")
    print("will lose 13 slides the investor needs.")
    sys.exit(2)

if _mode not in ("light", "full"):
    print("⚠️  PD_MODE is not set.")
    print()
    print("This script requires the mode to be set explicitly, to avoid mistakes:")
    print("    export PD_MODE=light   # for Light mode (45 min)")
    print("    export PD_MODE=full    # for Full mode (2-3 hours; do not run this script)")
    print()
    print("See references/step-0-questions.md, section 'Final step'.")
    sys.exit(3)

# Strip --force out of argv so it does not shift sys.argv[1]
if _force:
    sys.argv = [a for a in sys.argv if a != "--force"]

try:
    from pptx import Presentation
except ImportError:
    print("❌ python-pptx is required. Install it with: pip install python-pptx")
    sys.exit(1)

# The slides that end up empty in Light (1-based, for a 34-slide deck):
# 5, 6 — trends and the value chain (task 2)
# 9 — key competitor (task 4)  [was 8 before the competitor comparison slide was inserted]
# 10 — PESTEL (task 6)
# 13 — CJM (task 8)
# 14 — interview insights (task 9)
# 27-30 — section 05: the alternative scenario and the hypothesis pool (tasks 13-16)
# 31-33 — section 06 apart from the next steps (task 17)
# Slide 8 (competitor comparison) is NOT deleted in Light, because task 3 does run
LIGHT_SKIP_SLIDES_1BASED = [5, 6, 9, 10, 13, 14, 27, 28, 29, 30, 31, 32, 33]


def delete_light_slides(pptx_path: str) -> int:
    """Delete the empty Light slides from the deck. Returns how many were removed."""
    prs = Presentation(pptx_path)
    # python-pptx indexes slides from 0, so convert
    skip_indices = sorted({i - 1 for i in LIGHT_SKIP_SLIDES_1BASED}, reverse=True)

    xml_slides = prs.slides._sldIdLst
    slides = list(xml_slides)
    deleted = 0
    for i in skip_indices:
        if 0 <= i < len(slides):
            xml_slides.remove(slides[i])
            deleted += 1

    prs.save(pptx_path)
    return deleted


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    n = delete_light_slides(str(path))
    total_left = 34 - n  # 34 is the template's standard slide count (including the competitor comparison slide)
    print(f"✅ Deleted {n} slides. Remaining: {total_left}.")
    print("⚠️  Remember to update slide 2 (Contents) — it now points at pages that are gone.")
