#!/bin/bash
# Deck finalisation — one command that guarantees PowerPoint compatibility.
#
# It performs four steps:
# 1. Repack, when given an unpacked directory (skipped when given a .pptx)
# 2. Schema and relationship validation through the pptx skill's office/validate.py
# 3. A PowerPoint round-trip through LibreOffice, via office/soffice.py
#    (the wrapper, not bare soffice — bare soffice is unreliable in the sandbox)
# 4. Verification through python-pptx, plus an unfilled-placeholder check
#
# Usage:
#     bash scripts/finalize_pptx.sh <input.pptx | unpacked-dir> <output.pptx> [original-template.pptx]
#
# Where:
#   input         — either a finished .pptx or the unpacked directory holding ppt/...
#   output.pptx   — the final file (usually /mnt/user-data/outputs/presentation-[slug].pptx)
#   original      — optional; the template the deck came from. Pass it for any
#                   template-derived deck so the template's own schema quirks are
#                   not reported as yours.
#
# Set PPTX_SKILL to override where the public pptx skill lives.

set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"
ORIGINAL="${3:-}"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: bash finalize_pptx.sh <input.pptx | unpacked-dir> <output.pptx> [original-template.pptx]"
    exit 1
fi

PPTX_SKILL="${PPTX_SKILL:-/mnt/skills/public/pptx}"
VALIDATE="$PPTX_SKILL/scripts/office/validate.py"
SOFFICE_WRAP="$PPTX_SKILL/scripts/office/soffice.py"

if [ ! -f "$VALIDATE" ]; then
    echo "🔴 Not found: $VALIDATE"
    echo "   The public pptx skill is required. Set PPTX_SKILL to its directory."
    exit 1
fi

# validate.py needs these; without them it dies with ModuleNotFoundError, which
# would otherwise read as a validation failure.
if ! python3 -c "import defusedxml, lxml" 2>/dev/null; then
    echo "⚠️  validate.py needs defusedxml and lxml. Installing them:"
    pip install --quiet defusedxml lxml || {
        echo "🔴 Could not install defusedxml/lxml — validation cannot run."; exit 1; }
fi

OUTPUT_DIR=$(dirname "$OUTPUT")
mkdir -p "$OUTPUT_DIR"
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
STEP1="$TMPDIR/step1.pptx"

echo "=== Step 1/4: packaging ==="
if [ -d "$INPUT" ]; then
    # zip from INSIDE the directory, and remove the target first, or deleted parts survive
    ( cd "$INPUT" && rm -f "$STEP1" && zip -qXr "$STEP1" . )
    echo "   ✅ repacked from $INPUT"
elif [ -f "$INPUT" ]; then
    cp "$INPUT" "$STEP1"
    echo "   ✅ taken as-is (already a .pptx)"
else
    echo "❌ Input not found: $INPUT"
    exit 1
fi

echo "=== Step 2/4: validation ==="
if [ -n "$ORIGINAL" ] && [ -f "$ORIGINAL" ]; then
    VALIDATE_ARGS=("$STEP1" --original "$ORIGINAL")
else
    VALIDATE_ARGS=("$STEP1")
fi
if ! python3 "$VALIDATE" "${VALIDATE_ARGS[@]}"; then
    echo ""
    echo "🔴 validate.py reported failures. Each one names its fix — apply it."
    echo ""
    echo "Common causes:"
    echo "  1. Duplicated notesSlides references — left behind by"
    echo "     add_competitor_comparison_slide.py. Run it again;"
    echo "     it now cleans them up itself."
    echo "  2. Missing rels. Check that every slide referenced by"
    echo "     presentation.xml exists as a file."
    echo ""
    echo "See references/block-6-artifacts.md, section 'Troubleshooting validation'."
    echo "Never ship a deck that failed validation — PowerPoint will refuse it."
    exit 1
fi
echo "   ✅ validation passed"

echo "=== Step 3/4: LibreOffice round-trip ==="
if [ -f "$SOFFICE_WRAP" ]; then
    timeout 180 python3 "$SOFFICE_WRAP" --headless --convert-to pptx "$STEP1" --outdir "$TMPDIR/lo/" 2>&1 | tail -2 || true
    LO_OUTPUT="$TMPDIR/lo/$(basename "$STEP1")"
    if [ -f "$LO_OUTPUT" ]; then
        cp "$LO_OUTPUT" "$OUTPUT"
        echo "   ✅ rebuilt through the Office Open XML filter"
    else
        cp "$STEP1" "$OUTPUT"
        echo "   ⚠️  round-trip produced no file — copied the validated package instead."
        echo "      The deck may still fail to open in PowerPoint; check it before sending."
    fi
else
    cp "$STEP1" "$OUTPUT"
    echo "   ⚠️  $SOFFICE_WRAP not found — copied without the round-trip."
fi

echo "=== Step 4/4: verification through python-pptx ==="
python3 - <<PYEOF
import sys, os, re, subprocess
try:
    from pptx import Presentation
    p = Presentation("$OUTPUT")
    print(f"   ✅ python-pptx opens the file")
    print(f"   Slides: {len(p.slides)}")
    print(f"   Size:   {os.path.getsize('$OUTPUT')/1024:.1f} KB")
    texts = [r.text for s in p.slides for sh in s.shapes
             if sh.has_text_frame for para in sh.text_frame.paragraphs for r in para.runs]
    ph = [t for t in texts if re.search(r'\[[^\]]{1,80}\]', t)]
    real = [t for t in ph if not any(x in t for x in ['✅','⚠️','🔴','🟠','🟡','🟢'])]
    if real:
        print(f"   ⚠️  Unfilled placeholders found: {len(real)}")
        for t in real[:5]:
            print(f"      - {t[:70]}")
    else:
        print(f"   ✅ No unfilled placeholders")
except Exception as e:
    print(f"🔴 python-pptx cannot open the file: {e}")
    sys.exit(1)
PYEOF

echo ""
echo "🎉 File ready: $OUTPUT"
