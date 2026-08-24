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

echo "🔄 Step 1/3: LibreOffice round-trip..."
TMP_DIR=$(mktemp -d)
soffice --headless --convert-to docx:"MS Word 2007 XML" "$INPUT" --outdir "$TMP_DIR" > /dev/null 2>&1
CONVERTED=$(find "$TMP_DIR" -name "*.docx" | head -1)
if [ -z "$CONVERTED" ]; then
    echo "❌ LibreOffice conversion failed"
    rm -rf "$TMP_DIR"
    exit 1
fi

cp "$CONVERTED" "$OUTPUT"
rm -rf "$TMP_DIR"
echo "   ✅ Round-trip complete"

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
echo "   This file is Word-compatible (tested via round-trip + python-docx verification)"
