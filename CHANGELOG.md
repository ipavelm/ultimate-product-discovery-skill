# Changelog

## v4.0 (2026-08-24)

Breaking for anything that reads the artifact templates or the pptx pipeline by
name. Knowledge Bases written by v3.x remain readable, but their `skill-version`
will not match.

### Added
- **`scripts/self_check.py`** — checks the skill's own integrity after an edit:
  frontmatter, internal links, referenced files, workbook formulas and
  cross-sheet references, placeholder coverage in the templates, leftover data.
  It found three defects on its first run, including two in the documentation.

### Fixed
- **The financial model produced impossible numbers.** Almost every formula on
  the Model sheet referenced the row above its own label: the first funnel
  product multiplied by an empty section header, the average-bill rows pulled
  customer counts instead of prices, the returning-customer rows multiplied by
  Total paying customers instead of the churn rate, and cumulative GMV added the
  cost column. Recalculated on the same inputs, the sheet used to return
  `Total paying = -1` and `Total GMV = -9,385` by month 2, with operating profit
  spiralling to `-6,883,000` by month 5. It now returns a coherent funnel
  (121 leads → 7 conversions), GMV rising from 221,760 to 1,587,573 over eight
  months and break-even in month 5. 641 formulas across months 1-12 and 13-17.
- **GMV per segment multiplied two customer counts together** and took prices
  from the wrong segment; **Total paying customers** counted potential customers
  and omitted one segment's returning customers; **ARPPU** divided an empty
  header row by an empty row.
- **Five formulas on Scenarios pointed at a sheet that no longer existed** after
  the sheet names were translated.
- The `{{SEGMENT_{idx}_CONTEXT}}` placeholder in the interview guide never had
  its index substituted; it is now `{{SEGMENT_CONTEXT}}`.
- `init_kb.py` stamped `skill-version: 3.7` while the skill was 3.8, so every
  Knowledge Base was marked stale against the skill's own resume check.
- `delete_light_slides.py`'s docstring listed slides that predated the
  competitor-comparison slide, contradicting its own constant.

### Changed
- **The pptx pipeline no longer depends on `pack.py` or `unpack.py`.** Those
  scripts were removed from the public pptx skill, which left Rules 2 and 3 —
  both STOP-GATEs — unable to run at all. Packaging is now a plain zip and
  validation is a separate step through `office/validate.py`. `finalize_pptx.sh`
  accepts either a finished `.pptx` or an unpacked directory, matching how the
  documentation calls it, and both finalize scripts go through
  `office/soffice.py` rather than bare `soffice`.
- **Both finalize scripts now report honestly.** When the LibreOffice round-trip
  cannot run they say the file is unverified instead of claiming Word or
  PowerPoint compatibility they did not test.
- **Template paths resolve through `$SKILL_DIR`.** They were hardcoded to
  `/mnt/skills/user/product-discovery`, which does not exist for a CLI install —
  the distribution path for the catalogue. SKILL.md documents the directory per
  runtime.
- **The skill is now entirely in English**, including the four artifact
  templates and the workbook's 22 sheet names.
- `preflight_check.sh` also checks for `defusedxml`, `lxml` and the public
  pptx/docx skills' `validate.py` and `soffice.py`.
- Step 2.6 no longer tells the agent to replace segment labels that are not in
  the workbook, and the 24-month horizon is documented as it really is: the P&L
  holds 24 months, Model's labels stop at 17 and Cash Flow at 12, and
  `roll_formulas.py` covers months 2-12 only.

### Removed
- **Third-party project data from every template.** The deck shipped as a
  completed Product Discovery for a real company — 21 of its 34 slides carried
  that project's unit economics, burn rate, runway, funding need, persona and
  competitor teardown, and none of those slides held a placeholder, so the
  documented "no unfilled placeholders" check passed over all of them. The
  workbook carried a real weekly sales log naming four client projects, plus
  apparel-specific segment labels and a personal name in the document metadata.

## v3.8 (2026-04-22)

### Added
- **`assets/interview-guide-template.docx`** — a general-purpose interview guide template with 8 ready-made sections (how to use the guide, consent, 3 per-segment guides, insight table, red flags, market cheat sheet). Placeholders: {{PROJECT_NAME}}, {{GEO}}, {{SEGMENT_1-3}}, {{PRODUCT_DESCRIPTION}}, {{PRODUCT_CATEGORY}}, {{MONTH_YEAR}}, {{AUDIENCE}}, {{NAME}}, {{PAIN_POINT}}, {{SEGMENT_CONTEXT}} — 12 in total.
- **`scripts/finalize_docx.sh`** — finalizes docx artifacts through a LibreOffice round-trip plus python-docx verification. Guarantees Word compatibility.
- **Rule 6 (new, STOP-GATE)** — Word round-trip for docx artifacts. Fires before any `cp *.docx` into outputs.

### Changed
- **The "Task 9" section in `references/block-2-customers.md`** — updated to use the template and python-docx instead of the docx npm package.
- **Tooling recommendation:** use python-docx, not the docx npm package. Reason: the npm library produces files with broken style references (~30% of paragraphs end up with `style: None`) — LibreOffice and Google Docs open them, Word does not.

### Fixed
- The interview guide now opens reliably in Microsoft Word. The problem showed up in v3.6–3.7: files generated through the docx npm package were technically valid to an XML parser but rejected by Word.

---

## v3.7 (2026-04-22)

### Added
- **Geographic Expansion mode** for products entering a new geography
- **One-pager limit table** in references/block-6-artifacts.md
- **PD_MODE export** through /home/claude/.pd_env

### Changed
- Rules 3, 4 and 5 rewritten in STOP-GATE form with explicit triggers and failure modes
- `assets/financial-plan-template.xlsx`: all 24 references to apparel-specific data replaced with neutral "Segment 1-4" labels

---

## v3.6 (previous version)

- Baseline methodology: 18 tasks across 6 blocks
- Light and Full modes
- 5 safety rules
