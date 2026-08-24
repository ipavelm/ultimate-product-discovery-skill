#!/usr/bin/env python3
"""Check that the skill itself is internally consistent.

This is not the pre-flight check — `preflight_check.sh` verifies the environment
before a PD run. This one verifies the skill's own files after they are edited:
frontmatter, internal links, sheet names the instructions point at, formula
integrity, leftover third-party data, and placeholder coverage in the templates.

Usage:
    python3 scripts/self_check.py            # run from the skill directory
    python3 scripts/self_check.py <path>     # or point it at one

Exit code 0 when everything passes, 1 when any check fails.
"""
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
CYRILLIC = re.compile('[\u0400-\u052f]')  # written as escapes so this file stays ASCII
# Cyrillic that is expected: the localised name of Excel's built-in Normal style,
# which Excel identifies by builtinId rather than by name.
ALLOWED_CYRILLIC = {'assets/financial-plan-template.xlsx': 7}

failures = []
notes = []


def check(name, ok, detail=''):
    print(f"  {'✅' if ok else '❌'} {name}" + (f" — {detail}" if detail else ''))
    if not ok:
        failures.append(name)


def decode_refs(raw: bytes) -> str:
    """Office parts store non-ASCII as numeric character references; expand them."""
    text = raw.decode('utf-8', 'replace')
    return re.sub(r'&#(\d+);',
                  lambda m: chr(int(m.group(1))) if int(m.group(1)) > 127 else m.group(0),
                  text)


def office_text(path: Path) -> str:
    z = zipfile.ZipFile(path)
    return ''.join(decode_refs(z.read(n)) for n in z.namelist() if n.endswith('.xml'))


print('Frontmatter')
try:
    import yaml
    body = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n', body, re.S)
    fm = yaml.safe_load(m.group(1)) if m else None
    check('parses as YAML into a mapping', isinstance(fm, dict))
    if isinstance(fm, dict):
        name = fm.get('name', '')
        desc = fm.get('description', '')
        check('name matches [a-z0-9-]{1,64}', bool(re.fullmatch(r'[a-z0-9-]{1,64}', name)), name)
        check('description within 1024 chars', len(desc) <= 1024, f'{len(desc)} chars')
        version = str(fm.get('metadata', {}).get('version', ''))
        stamped = re.search(r'SKILL_VERSION = "([^"]+)"',
                            (ROOT / 'scripts/init_kb.py').read_text(encoding='utf-8'))
        check('init_kb.py stamps the same version',
              bool(stamped) and stamped.group(1) == version,
              f'SKILL.md {version} vs init_kb {stamped.group(1) if stamped else "?"}')
except ImportError:
    notes.append('PyYAML missing — frontmatter not parsed (pip install pyyaml)')

print('\nInternal links')
broken = []
for md in [ROOT / 'SKILL.md', ROOT / 'README.md'] + sorted((ROOT / 'references').glob('*.md')):
    for link in re.findall(r'\]\(([^)#][^)]*)\)', md.read_text(encoding='utf-8')):
        if link.startswith(('http://', 'https://')):
            continue
        if not (md.parent / link).resolve().exists():
            broken.append(f'{md.name} → {link}')
check('every relative link resolves', not broken, '; '.join(broken[:5]))

print('\nScripts and assets the instructions name')
docs = '\n'.join(p.read_text(encoding='utf-8') for p in
                 [ROOT / 'SKILL.md'] + sorted((ROOT / 'references').glob('*.md')))
# Only paths relative to the skill; an absolute path such as
# /home/claude/scripts/recalc.py points at a different skill's copy.
refs = sorted(set(re.findall(r'(?<![\w/])(?:scripts|assets)/[\w.-]+\.(?:py|sh|pptx|xlsx|docx)', docs)))
missing = [ref for ref in refs if not (ROOT / ref).exists()]
check('all referenced files exist', not missing, ', '.join(missing) or f'{len(refs)} checked')

print('\nWorkbook')
wb_path = ROOT / 'assets/financial-plan-template.xlsx'
try:
    import openpyxl
    wb = openpyxl.load_workbook(wb_path)
    formulas = [c.value for ws in wb.worksheets for row in ws.iter_rows()
                for c in row if isinstance(c.value, str) and c.value.startswith('=')]
    check('opens and has sheets', len(wb.sheetnames) > 0, f'{len(wb.sheetnames)} sheets')
    check('no error values in formulas',
          not [f for f in formulas if re.search(r'#(REF|NAME\?|VALUE|DIV/0)', f)],
          f'{len(formulas)} formulas')
    sheet_refs = set()
    for f in formulas:
        sheet_refs |= set(re.findall(r"'([^']+)'!", f))
    dangling = sorted(sheet_refs - set(wb.sheetnames))
    check('every cross-sheet reference resolves', not dangling, ', '.join(dangling))
    named = set(re.findall(r"='([^']+)'!", docs))
    unknown = sorted(named - set(wb.sheetnames))
    check('sheet names used in the docs exist', not unknown, ', '.join(unknown))
except ImportError:
    notes.append('openpyxl missing — workbook not checked (pip install openpyxl)')

print('\nTemplates')
for rel, tag in [('assets/presentation-template.pptx', 'a:t'),
                 ('assets/one-pager-template.pptx', 'a:t'),
                 ('assets/interview-guide-template.docx', 'w:t')]:
    path = ROOT / rel
    if not path.exists():
        check(f'{Path(rel).name} present', False)
        continue
    text = office_text(path)
    runs = [s for s in re.findall(rf'<{tag}(?:\s[^>]*)?>([^<]*)</{tag}>', text) if s.strip()]
    placeholders = [s for s in runs if re.search(r'\[[^\]]{1,80}\]|\{\{[^}]+\}\}', s)]
    share = 100 * len(placeholders) // max(len(runs), 1)
    check(f'{Path(rel).name} keeps placeholders', share >= 10,
          f'{len(placeholders)}/{len(runs)} runs ({share}%)')

print('\nLeftover data')
for path in sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and '.git' not in p.parts and '__pycache__' not in p.parts):
    rel = str(path.relative_to(ROOT))
    if path.suffix in ('.xlsx', '.pptx', '.docx'):
        count = len(CYRILLIC.findall(office_text(path)))
    elif path.suffix in ('.md', '.py', '.sh', '.json'):
        count = len(CYRILLIC.findall(path.read_text(encoding='utf-8')))
    else:
        continue
    check(f'{rel}: no unexpected Cyrillic', count <= ALLOWED_CYRILLIC.get(rel, 0),
          f'{count} chars' if count else '')

print()
for note in notes:
    print(f'  ⚠️  {note}')
if failures:
    print(f'\n❌ {len(failures)} check(s) failed:')
    for f in failures:
        print(f'   - {f}')
    sys.exit(1)
print('\n✅ All checks passed.')
