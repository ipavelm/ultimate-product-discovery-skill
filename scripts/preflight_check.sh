#!/bin/bash
# Pre-flight check for the product-discovery skill.
#
# Verifies that every required tool is available BEFORE PD starts, so it does not
# die in the middle of block 6 when the financial plan has to be saved as .xlsx.
#
# Usage:
#     bash preflight_check.sh
#
# Prints a list of statuses. All OK means PD can start. If anything shows ⚠️,
# read "Fallback when pre-flight fails" in SKILL.md.

set -u

echo "🔍 Pre-flight check for product-discovery..."
echo ""

# PD mode (critical — see SKILL.md, "Critical safety rules")
if [ -n "${PD_MODE:-}" ]; then
    case "$PD_MODE" in
        light|full|Light|Full|LIGHT|FULL)
            echo "  ✅ PD_MODE: $PD_MODE"
            ;;
        *)
            echo "  ⚠️  PD_MODE=$PD_MODE — unknown value. It must be 'light' or 'full'."
            ;;
    esac
else
    echo "  ⚠️  PD_MODE is not set — scripts/delete_light_slides.py will refuse to run"
    echo "      Once the mode is chosen in Step 0, run: export PD_MODE=light (or full)"
fi

# CLI utilities
if command -v extract-text >/dev/null 2>&1; then
    echo "  ✅ extract-text: available"
else
    echo "  ⚠️  extract-text: MISSING — read .pptx/.xlsx directly through openpyxl/python-pptx"
fi

# LibreOffice — needed for PowerPoint compatibility (finalize_pptx.sh)
if command -v libreoffice >/dev/null 2>&1; then
    echo "  ✅ libreoffice: $(libreoffice --version 2>&1 | head -1)"
else
    echo "  🔴 libreoffice: NOT found — the deck cannot go through the PowerPoint round-trip"
    echo "      The file may fail to open in PowerPoint even when it is valid OOXML"
fi

# Python and the libraries
if ! command -v python3 >/dev/null 2>&1; then
    echo "  ❌ python3: NOT found — critical; without it neither the financial plan nor the deck can be built"
    exit 1
fi
echo "  ✅ python3: $(python3 --version)"

# Check the exact imports — not just "the package exists" but a working API
python3 -c "from openpyxl import load_workbook" 2>/dev/null \
    && echo "  ✅ openpyxl: import works" \
    || echo "  ⚠️  openpyxl: import FAILS — task 18c (financial plan) is impossible"

python3 -c "from pptx import Presentation" 2>/dev/null \
    && echo "  ✅ python-pptx: import works" \
    || echo "  ⚠️  python-pptx: import FAILS — tasks 18b and 18d (one-pager, deck) are impossible"

python3 -c "from docx import Document" 2>/dev/null \
    && echo "  ✅ python-docx: import works" \
    || echo "  ⚠️  python-docx: import FAILS — task 9 will emit the guide as markdown instead of docx"

# Artifact utilities
SKILL_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"
echo ""
echo "Artifact utilities:"
for f in finalize_pptx.sh roll_formulas.py delete_light_slides.py add_competitor_comparison_slide.py reorder_summary_first.py; do
    if [ -f "$SKILL_ROOT/scripts/$f" ]; then
        echo "  ✅ scripts/$f"
    else
        echo "  ⚠️  scripts/$f is missing"
    fi
done

# Templates
echo ""
echo "Templates:"
if [ -d "$SKILL_ROOT/assets" ]; then
    MISSING=0
    for f in one-pager-template.pptx presentation-template.pptx financial-plan-template.xlsx; do
        if [ -f "$SKILL_ROOT/assets/$f" ]; then
            echo "  ✅ assets/$f"
        else
            echo "  ⚠️  assets/$f NOT found"
            MISSING=$((MISSING + 1))
        fi
    done
    if [ "$MISSING" -gt 0 ]; then
        echo "  ⚠️  $MISSING template(s) missing — PD will finish without the matching artifact"
    fi
else
    echo "  ❌ The folder $SKILL_ROOT/assets was not found — critical"
fi

echo ""
echo "Pre-flight done. If anything shows ⚠️ — see SKILL.md, section \"Fallback when pre-flight fails\"."
echo "If anything shows 🔴 — those are critical, fix them before starting PD."
