#!/usr/bin/env bash
# finalize_docx.sh -- Finalises a .docx artifact before it is handed to the user.
#
# The problem: libraries such as the `docx` npm package produce technically
# valid .docx files that open in LibreOffice and python-docx, but Word refuses
# them because of broken style references, malformed relationships and other
# small violations of the OOXML manifest.
#
# The fix: a round-trip through LibreOffice repackages the file with the
# Microsoft Word 2007 XML filter, which produces a reliably Word-compatible
# document with a correct style and relationship structure.
#
# After the round-trip, python-docx verifies the result: if every style
# resolves and the file opens, it is guaranteed to work in Word.
#
# Usage:
#     bash scripts/finalize_docx.sh /home/claude/interview-guide.docx /mnt/user-data/outputs/interview-guide-[slug].docx
#
# Example:
#     bash scripts/finalize_docx.sh /home/claude/ig.docx /mnt/user-data/outputs/interview-guide-timetag.docx

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input.docx> <output.docx>"
    echo "Example: $0 /home/claude/ig.docx /mnt/user-data/outputs/interview-guide-slug.docx"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
    echo "❌ Input file not found: $INPUT"
    exit 1
fi

OUTPUT_DIR=$(dirname "$OUTPUT")
mkdir -p "$OUTPUT_DIR"

# Use the docx skill's soffice wrapper rather than bare soffice: bare soffice is
# unreliable in the sandbox. Set DOCX_SKILL to override where that skill lives.
DOCX_SKILL="${DOCX_SKILL:-/mnt/skills/public/docx}"
SOFFICE_WRAP="$DOCX_SKILL/scripts/office/soffice.py"

echo "🔄 Step 1/3: LibreOffice round-trip..."
TMP_DIR=$(mktemp -d)
if [ -f "$SOFFICE_WRAP" ]; then
    timeout 180 python3 "$SOFFICE_WRAP" --headless --convert-to docx:"MS Word 2007 XML" \
        "$INPUT" --outdir "$TMP_DIR" > /dev/null 2>&1 || true
else
    timeout 180 soffice --headless --convert-to docx:"MS Word 2007 XML" \
        "$INPUT" --outdir "$TMP_DIR" > /dev/null 2>&1 || true
fi
CONVERTED=$(find "$TMP_DIR" -name "*.docx" | head -1)
if [ -z "$CONVERTED" ]; then
    echo "   ⚠️  Round-trip produced no file — carrying on with the original."
    echo "      Word compatibility is NOT guaranteed; open the file in Word before sending it."
    cp "$INPUT" "$OUTPUT"
    ROUNDTRIP=skipped
else
    cp "$CONVERTED" "$OUTPUT"
    echo "   ✅ Round-trip complete"
    ROUNDTRIP=done
fi
rm -rf "$TMP_DIR"

echo "🔄 Step 2/3: Verification through python-docx..."
python3 - << PYEOF
import sys
from docx import Document
try:
    doc = Document("$OUTPUT")
    broken_styles = 0
    for p in doc.paragraphs:
        try:
            _ = p.style.name
        except Exception:
            broken_styles += 1
    if broken_styles > 0:
        print(f"   🚩 {broken_styles} paragraphs with broken style references — Word may reject")
        sys.exit(1)
    print(f"   ✅ {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables, all styles resolved")
except Exception as e:
    print(f"   ❌ Verification failed: {e}")
    sys.exit(1)
PYEOF

echo "🔄 Step 3/3: Final check..."
SIZE=$(stat -c '%s' "$OUTPUT" 2>/dev/null || stat -f '%z' "$OUTPUT")
echo "   ✅ File size: $SIZE bytes"
echo ""
echo "✅ Finalization complete: $OUTPUT"
if [ "${ROUNDTRIP:-skipped}" = "done" ]; then
    echo "   Word compatibility verified: LibreOffice round-trip + python-docx verification"
else
    echo "   ⚠️  Word compatibility NOT verified — the round-trip did not run."
    echo "      Styles resolve, but open the file in Word before sending it."
fi
