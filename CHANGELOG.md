# Changelog

## v3.8 (2026-04-22)

### Added
- **`assets/interview-guide-template.docx`** — a general-purpose interview guide template with 8 ready-made sections (how to use the guide, consent, 3 per-segment guides, insight table, red flags, market cheat sheet). Placeholders: {{PROJECT_NAME}}, {{GEO}}, {{SEGMENT_1-3}}, {{PRODUCT_DESCRIPTION}}, {{PRODUCT_CATEGORY}}, {{MONTH_YEAR}}, {{AUDIENCE}}, {{NAME}}, {{PAIN_POINT}} — 11 in total.
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
