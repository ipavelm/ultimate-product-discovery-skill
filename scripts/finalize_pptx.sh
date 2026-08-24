#!/bin/bash
# Deck finalisation — one command that guarantees PowerPoint compatibility.
#
# It performs three steps:
# 1. pack.py with full validation (WITHOUT --validate false!)
# 2. A PowerPoint round-trip through LibreOffice (Microsoft Impress Office Open XML filter)
# 3. Verification through python-pptx — that the file really does open
#
# Usage:
#     bash scripts/finalize_pptx.sh /path/to/unpacked-dir /path/to/output.pptx /path/to/original.pptx
#
# Where:
#   unpacked-dir  — the folder holding unpacked/ppt/... (the result of unpack.py)
#   output.pptx   — the final file (usually /mnt/user-data/outputs/presentation-[slug].pptx)
#   original.pptx — the original template (for --original in pack.py)

set -e

UNPACKED="$1"
OUTPUT="$2"
ORIGINAL="$3"

if [ -z "$UNPACKED" ] || [ -z "$OUTPUT" ] || [ -z "$ORIGINAL" ]; then
    echo "Usage: bash finalize_pptx.sh <unpacked-dir> <output.pptx> <original.pptx>"
    exit 1
fi

if [ ! -d "$UNPACKED" ]; then
    echo "❌ Unpacked directory not found: $UNPACKED"
    exit 1
fi

# Check that LibreOffice is present
if ! command -v libreoffice >/dev/null 2>&1; then
    echo "🔴 LibreOffice not found — PowerPoint compatibility is not guaranteed."
    echo "   The file will be produced by pack.py alone, with no round-trip."
    echo "   Install LibreOffice for maximum reliability."
    NO_LIBREOFFICE=1
fi

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

STEP1="$TMPDIR/step1.pptx"

echo "=== Step 1: pack.py with full validation ==="
# Path to pack.py from the pptx skill
PACK_PY="/mnt/skills/public/pptx/scripts/office/pack.py"
if [ ! -f "$PACK_PY" ]; then
    # Fallback: search for pack.py
    PACK_PY=$(find / -name "pack.py" -path "*pptx*" 2>/dev/null | head -1)
    if [ -z "$PACK_PY" ]; then
        echo "🔴 pack.py not found. Check that the pptx skill is installed."
        exit 1
    fi
fi

if ! python3 "$PACK_PY" "$UNPACKED" "$STEP1" --original "$ORIGINAL" 2>&1; then
    echo ""
    echo "🔴 pack.py failed validation."
    echo ""
    echo "Common causes:"
    echo "  1. Duplicated notesSlides references — left behind by"
    echo "     add_competitor_comparison_slide.py. Run it again;"
    echo "     it now cleans them up itself."
    echo "  2. Missing rels. Check that every slide referenced by"
    echo "     presentation.xml exists as a file."
    echo ""
    echo "See references/block-6-artifacts.md, section 'Troubleshooting pack.py'."
    echo ""
    echo "NEVER use --validate false — the file will not open in PowerPoint."
    exit 1
fi

echo "✅ pack.py passed validation"

if [ "$NO_LIBREOFFICE" = "1" ]; then
    # No LibreOffice — just copy the pack.py result
    cp "$STEP1" "$OUTPUT"
    echo "⚠️  Copied without the LibreOffice round-trip (it may not open in PowerPoint)"
else
    echo ""
    echo "=== Step 2: LibreOffice round-trip ==="
    timeout 60 libreoffice --headless --convert-to pptx "$STEP1" \
        --outdir "$TMPDIR/lo/" 2>&1 | tail -2

    LO_OUTPUT="$TMPDIR/lo/$(basename "$STEP1")"
    if [ ! -f "$LO_OUTPUT" ]; then
        echo "🔴 The LibreOffice conversion produced no file."
        echo "   Check the LibreOffice install: libreoffice --version"
        exit 1
    fi

    cp "$LO_OUTPUT" "$OUTPUT"
    echo "✅ LibreOffice round-trip — the file was rebuilt through the"
    echo "   Microsoft Impress Office Open XML filter"
fi

echo ""
echo "=== Step 3: verification through python-pptx ==="
python3 - <<PYEOF
import sys
try:
    from pptx import Presentation
    p = Presentation("$OUTPUT")
    import os
    size_kb = os.path.getsize("$OUTPUT") / 1024
    print(f"✅ python-pptx opens the file")
    print(f"   Slides: {len(p.slides)}")
    print(f"   Size:   {size_kb:.1f} KB")
    # Check that no placeholders were left unfilled
    import subprocess, re
    result = subprocess.run(['extract-text', "$OUTPUT"], capture_output=True, text=True)
    if result.returncode == 0:
        placeholders = re.findall(r'\[[^\]]{1,80}\]', result.stdout)
        real = [p for p in placeholders if not any(x in p for x in ['✅','⚠️','🔴','🟠','🟡','🟢'])]
        if real:
            print(f"   ⚠️  Unfilled placeholders found: {len(real)}")
            for p in real[:5]:
                print(f"      - {p}")
        else:
            print(f"   ✅ No unfilled placeholders")
except Exception as e:
    print(f"🔴 python-pptx cannot open the file: {e}")
    sys.exit(1)
PYEOF

echo ""
echo "🎉 File ready: $OUTPUT"
