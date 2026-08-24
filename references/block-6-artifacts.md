## BLOCK VI: FINAL ARTIFACTS

**Contents:**
1. Output file naming standard
2. Task 18b: one-pager (.pptx)
3. Task 18c: financial plan (.xlsx) — the 7 filling steps
4. Task 18d: presentation (.pptx) — the 34-slide mapping
5. Finishing PD — the final summary in the chat

---

**Output file naming standard.** Every final artifact is saved into `/mnt/user-data/outputs/` under one scheme: `[type]-[project-slug].[extension]`, where `project-slug` is the name transliterated into lower case with hyphens (for example, the project "TimeTag" → slug `timetag`; the project "Smart home for pensioners" → slug `smart-home-seniors`). The resulting names:

| Artifact | File name |
|----------|-----------|
| One-pager | `one-pager-[slug].pptx` |
| Financial plan | `financial-plan-[slug].xlsx` |
| Presentation | `presentation-[slug].pptx` |
| Interview guide (Full only) | `interview-guide-[slug].docx` |

For working copies along the way use `/home/claude/[type].[extension]` with no slug (for example `/home/claude/one-pager.pptx`), and copy into `/mnt/user-data/outputs/` under the proper name only at final delivery.

---

### Task 18b: one-pager (.pptx)

Read the skill at `/mnt/skills/public/pptx/SKILL.md` before building it.

**One-pager template:** the file `assets/one-pager-template.pptx` holds a finished dark design with 9 sections on a single slide. Use it as the base:

```bash
cp "$SKILL_DIR/assets/one-pager-template.pptx" /home/claude/one-pager.pptx
```

**Template structure (one 16:9 slide):**

| Section | Content | Data source |
|---------|---------|-------------|
| **Header** | Project name, tagline, date | Step 0 |
| **Problem** | The customer's pain in 1–2 sentences plus the OS | Task 7 |
| **Solution** | How the product closes the pain, 2–3 features | Task 10 |
| **Market** | TAM / SAM / SOM | Task 5 |
| **Unit economics** | CAC, LTV, LTV/CAC, payback, runway, break-even | Financial plan |
| **Main scenario** | Monetisation, tickets, COGS, gross margin | Task 18a |
| **Top 3 insights** | Patterns from the interviews, with OS | Task 9 |
| **Top 3 hypotheses** | The risky hypotheses + method + timeframe | Task 15 |
| **Next step** | A concrete action + owner + deadline | Task 18a |

**Filling it in:** replace every `[...]` placeholder through `python-pptx` or `pptxgenjs`. Use `extract-text one-pager.pptx` to find them all.

**⚠️ Text limits per section (v3.7).** The template has fixed section sizes. Exceed them and LibreOffice renders overlapping text, so the one-pager looks broken. Work to these limits:

| Section | Max characters | Max font (pt) | Note |
|---------|----------------|---------------|------|
| Header — project name | 60 | 44 | Short and memorable |
| Header — tagline | 180 | 18 | One sentence |
| Problem | 400 | 10 | 2–3 sentences plus the OS numbers |
| Solution — value proposition | 200 | 9 | The value proposition in one phrase |
| Solution — features | 160 | 9 | 3–5 bullets separated by "•" |
| Market — the TAM/SAM/SOM figures | 40 each | 12 | Short values with units |
| Unit economics — each field | 20 | 14 | Just the number and its sign |
| Main scenario — name | 80 | 14 | A short name |
| Main scenario — each field | 100 | 9 | One line |
| Top 3 insights — each | 180 | 9 | One sentence plus source/OS |
| Top 3 hypotheses — statement | 180 | 10 | The hypothesis headline |
| Top 3 hypotheses — detail | 80 | 8 | Method + timeframe + budget |
| Next step — action | 180 | 10 | A concrete action |
| Next step — owner/deadline | 60 | 8 | Role + day range |

If the text does not fit, cut it **before** the first generation, not after. Regenerating through preview and resizing sometimes takes 2–3 iterations (observed in v3.6 sessions). Better to write tight from the start.

**Output:** the `.pptx` → `/mnt/user-data/outputs/one-pager-[name].pptx`

---

### Task 18c: financial plan (.xlsx)

Read the skill at `/mnt/skills/public/xlsx/SKILL.md` before building it.

#### Step 1 — preparation

```bash
cp "$SKILL_DIR/assets/financial-plan-template.xlsx" /home/claude/financial-plan.xlsx
# Copying the scripts is idempotent (it does not fail if they are already there):
mkdir -p /home/claude/scripts
cp -rn /mnt/skills/public/xlsx/scripts/. /home/claude/scripts/
# Check the key script is in place:
test -f /home/claude/scripts/recalc.py && echo "recalc.py OK" || echo "ERROR: recalc.py not found"
# Size it up before reading:
TOTAL=$(extract-text /home/claude/financial-plan.xlsx | wc -l)
echo "The financial plan holds $TOTAL lines of text"
# Read with a threshold: small template — read it all; large — print the structure (sheet headers)
if [ "$TOTAL" -lt 500 ]; then
    extract-text /home/claude/financial-plan.xlsx
else
    extract-text /home/claude/financial-plan.xlsx | head -200
    echo "... [truncated; for detail read specific sheets through openpyxl]"
fi
```

**The template's first sheet is `Summary`.** It is the executive view for the investor or CEO, and the first thing they see when they open the file. It carries the main scenario's key figures: value proposition, TAM/SAM/SOM, LTV/CAC, runway, break-even, top 3 risks and the PD's main conclusion. Fill Summary in **after** every other sheet — it aggregates their numbers. If Summary ends up not being first for some reason (openpyxl appends new sheets at the end when recreating them), use `scripts/reorder_summary_first.py <path-to-xlsx>` to restore the correct order.

#### Step 2 — principles

- 🔵 Blue text — enter by hand
- ⚫ Black text — formulas, do not touch
- 🟢 Green text — references, do not touch
- Start with **Assumptions** — it is the source of every calculation
- Month 1 is filled in as an example; months 2–12 (and 13–24 when the horizon is 24 months) are empty

> **A 24-month horizon:** the template is not uniformly 24 months wide. P&L runs to column Z (24 months); Model carries month labels to month 17; Cash Flow stops at column N (12 months). For a 24-month horizon you must add the missing columns yourself on Model and Cash Flow before filling them — otherwise runway and break-even past month 12 have nowhere to live. `roll_formulas.py` expands D..N only, i.e. months 2–12; months 13+ have to be rolled separately.

> **If the business is a marketplace:** the key P&L differences are:
> - **Revenue** = GMV × take rate (%), NOT GMV directly
> - **GMV** = number of transactions × average ticket — keep it on its own row so the volume is legible
> - **COGS** = payment infrastructure + support + hosting (usually 5–15% of revenue)
> - **Two kinds of CAC:** supplier CAC and buyer CAC — model and optimise them separately
> - On the Assumptions sheet, add: take rate (%), active suppliers in month 1, transactions per supplier per month
> - Record the chicken-and-egg risk on the Hypothesis pool sheet as a scalability hypothesis with its test method (Concierge: fill the first side by hand before launching the platform)

> **If the business is a service:** the key P&L differences are:
> - **Revenue** = number of projects × average project value
> - **COGS** = delivery payroll × (1 − utilisation) + direct project costs
> - **Gross margin** = revenue − delivery COGS (target ≥ 40% for an agency, ≥ 60% for consulting)
> - **Key assumptions:** utilisation rate (target ≥ 70%), average billable rate (₽/hour), average number of concurrent projects
> - On the Assumptions sheet, replace the 💰 PRICES block with: utilisation rate, billable rate, average project duration, average project value

> **If the business is hardware / a physical device:** the key P&L differences are:
> - COGS includes manufacturing, logistics and returns. The 40–60% of sale price range is normal for hardware; SaaS benchmarks do not apply here
> - There is no recurring revenue by default: revenue is one-off sales plus repeat orders where consumables or upgrades exist
> - The first production order requires prepayment for the whole batch (MOQ risk). In Cash Flow, book the manufacturer's deposit as CAPEX in months 1–3, before any revenue arrives
> - The cycle to MVP depends on complexity: IoT on off-the-shelf components — 4–6 months; consumer electronics with custom hardware — 12–18 months. The first N months of the P&L are pure cost, and runway has to cover that period plus a 3-month buffer
> - On the Assumptions sheet, add: unit cost (₽), MOQ (minimum batch), sale price, logistics per unit, % returns
> - **Selling through marketplaces (Wildberries / Ozon in Russia, Amazon globally):** if this is the main or a significant channel, model its specifics on separate P&L rows:
>   - Marketplace commission of 15–25% of sale price (the exact % depends on category and volume — confirm with the person or from current exports)
>   - FBS (fulfilment by seller, stock held by the seller) vs FBO (stock in the marketplace's warehouse) are different models: FBO needs more CAPEX for advance shipments but turns over faster; FBS needs less CAPEX but delivers slower and hurts the listing's rating
>   - The marketplace's internal advertising (listing promotion, auto-targeting) is not classic CAC through Google or Yandex but a line of its own. Promotion spend usually runs at 8–15% of revenue at launch
>   - Return rates on WB and Ozon (WB especially) are often 10–30% because of the "collect it, look at it, send it back" model — higher than on your own site
>   - If marketplace sales exceed 50% of revenue, that is a channel risk (a rule change on the platform can destroy the economics). Record it in task 15 as the hypothesis "channel diversification".

#### Step 2.5 — CRITICAL: expand the formulas into months 2–12

The `financial-plan-template.xlsx` template carries formulas **only in column C (month 1)**. Columns D–N (months 2–12) on the **P&L** and **Cash Flow** sheets are empty. Without this step the plan shows revenue for month 1 only, which is useless to an investor.

**Method 1 (recommended):** use the ready-made script:

```bash
python3 scripts/roll_formulas.py /home/claude/financial-plan.xlsx
```

The script walks the P&L and Cash Flow sheets, finds the rows holding formulas in column C and expands them into D–N with the references shifted.

**Method 2 (manual, if the script is unavailable):**

```python
from openpyxl.utils import get_column_letter, column_index_from_string
import re

def shift_formula(formula, delta):
    if not isinstance(formula, str) or not formula.startswith("="):
        return None
    def shift(m):
        full = m.group(0)
        if full.startswith('$'): return full
        col_letters, row_num = m.group(1), m.group(2)
        new_col = column_index_from_string(col_letters) + delta
        return f"{get_column_letter(new_col)}{row_num}"
    return re.sub(r'\$?([A-Z]+)(\d+)', shift, formula)

# P&L — expand the formulas from C into D..N
for row in range(1, ws.max_row + 1):
    c_value = ws.cell(row=row, column=3).value
    if isinstance(c_value, str) and c_value.startswith("="):
        for col in range(4, 15):  # D..N = months 2..12
            if ws.cell(row=row, column=col).value is None:
                ws.cell(row=row, column=col).value = shift_formula(c_value, col - 3)
```

**Special cases — a growth plan rather than a formula:**

1. **GMV (P&L row 5)** — set the customer growth plan directly instead of referencing the Model sheet:
   ```python
   new_clients = [3, 4, 5, 7, 9, 12, 16, 20, 25, 32, 40, 45]
   avg_check = 240000  # from Assumptions
   for i, n in enumerate(new_clients):
       ws.cell(row=5, column=3+i).value = n * avg_check
   ```

2. **Cash Flow row 4 (opening balance):** for month 2 onwards it is the previous month's closing balance:
   ```python
   for col in range(4, 15):
       prev = get_column_letter(col - 1)
       ws.cell(row=4, column=col).value = f"={prev}25"
   ```

3. **Cumulative P&L totals (row 40 cumulative GMV, row 41 cumulative net profit):**
   ```python
   for col in range(4, 15):
       prev, letter = get_column_letter(col - 1), get_column_letter(col)
       ws.cell(row=40, column=col).value = f"={prev}40+{letter}5"
       ws.cell(row=41, column=col).value = f"={prev}41+{letter}36"
   ```

**Verification:** run `python3 /home/claude/scripts/recalc.py /home/claude/financial-plan.xlsx` — the expected result is `"status": "success", "total_errors": 0`. Look at P&L row 5 (GMV) and row 41 (cumulative net profit) — they must grow from month 1 to month 12, not be identical or empty.

#### Step 2.6 — CRITICAL: clear the example data out of the template

The **Assumptions** and **Model** sheets in `financial-plan-template.xlsx` ship with neutral placeholder segments — "Segment 1" through "Segment 4" — plus a worked example on the analysis sheets (an invoicing SaaS for small business). The Model sheet's formulas reference the segment structure, not the labels.

**If that data is not replaced**, Model keeps calculating the placeholder segments while the assumptions block you filled in above it is ignored by the formulas. Summary then shows a mixed picture.

Check the labels rather than trusting this list: `python3 -c "import openpyxl; wb=openpyxl.load_workbook('financial-plan.xlsx'); ws=wb['Model']; print([ws.cell(row=r,column=1).value for r in range(28,46)])"`

**Option A (recommended):** make the P&L independent of Model.

- In the P&L, set the GMV plan directly (as in Step 2.5, special case 1) instead of using `='Model'!C41`
- Leave the Model sheet as a reference but do not point Summary at it
- In Summary use only formulas of the form `='P&L'!N5`, `='P&L'!N36` and so on

**Option B (when the link to Model must be kept):** rewrite the Assumptions sheet completely:
- Rename the segments in row 18 onwards of the Model sheet
- Replace the NEW/RETURN average tickets
- Replace the churn rate for luxury/premium/mass depending on the business
- Replace the marketing budget
- Recalculate with `python3 /home/claude/scripts/recalc.py`: confirm there are no `#REF!` or `#DIV/0!`

If you chose option A, add a "live metrics" block to Summary referencing the P&L:

```python
live_metrics = [
    ("GMV month 1", "='P&L'!C5"),
    ("GMV month 12", "='P&L'!N5"),
    ("Cumulative GMV, year 1", "='P&L'!N40"),
    ("Cumulative net profit, year 1", "='P&L'!N41"),
    ("Break-even month", "=IFERROR(MATCH(TRUE,'P&L'!C41:N41>=0,0),\"not reached\")"),
]
```

#### Step 3 — filling in the financial sheets

> **If the user uploaded CRM or analytics data (question 13 in Step 0):**
> Read the file through `openpyxl` or `pandas` before filling in Assumptions.
> Extract: the real stage-by-stage funnel conversions, retention rate (by cohort where available), average ticket, churn rate, CAC by channel.
> Use those values instead of expert estimates. Shade the cells holding real data green and note the source ("CRM, export of [date]"). That automatically raises confidence to 🟢 High.

**1. Assumptions**

Depending on the business type (determined in task 10), fill the matching 💰 PRICES block:

> **If the business is a product:** fill the "PRICES (Product)" block in the table below in full. The 📊 FUNNEL block is the standard one.
>
> **If the business is a service:** fill the "PRICES (Service)" block: utilisation rate (target ≥ 70%), billable rate (₽/hour), average project duration (months), average project value (₽). Keep the 📊 FUNNEL block as it is, but read "leads" as "project enquiries".
>
> **If the business is a marketplace:** fill the "PRICES (Marketplace)" block: GMV month 1, take rate (%), supplier CAC, buyer CAC, COGS% (payment infrastructure + hosting + support, 5–15% of revenue). Important: there are **two** parallel funnels (suppliers and buyers), each with its own leads and conversions. Revenue = GMV × take rate, NOT GMV directly.
>
> **If the business is hardware:** fill the "PRICES (Hardware)" block: unit cost, MOQ (the manufacturer's minimum batch), sale price, logistics per unit, % returns. COGS is usually 40–60% of the sale price. The funnel: the first order is a pre-order or a deposit, not simply "lead → customer". Add to OPEX: the manufacturer's deposit as CAPEX in months 1–3 (before any revenue), and runway must cover that period plus a 3-month buffer.

| Block | Field | Source |
|-------|-------|--------|
| 🌍 MARKET | TAM, SAM, SOM year 1, market growth | Tasks 5, 1 |
| 💰 PRICES (Product) | NEW/RETURN average ticket per segment, COGS%, commission | Tasks 18a, 10 |
| 💰 PRICES (Service) | Utilisation rate, billable rate, average project value, COGS% = payroll/revenue | Tasks 18a, 10 |
| 💰 PRICES (Marketplace) | GMV month 1, take rate (%), supplier CAC, buyer CAC, COGS% | Tasks 18a, 10 |
| 💰 PRICES (Hardware) | Unit cost, MOQ, sale price, logistics per unit, % returns | Tasks 18a, 10 |
| 📊 FUNNEL | Leads month 1, conversions, churn | Task 18a (from 16), 10, 17 |
| 🔬 UNIT ECON | CPL, LTV, LTV/CAC, payback | Task 18a |
| 🏗️ OPEX | Marketing, payroll, infrastructure, dev CAPEX | Task 18a |
| 🏛️ TAXES | Regime: 15% simplified if COGS > 60%, otherwise 6% simplified | Automatic |

**2. Model** — the blue cells for month 1: TAM/SAM/SOM, leads, conversions, tickets, costs

**3. P&L and Cash Flow** — month 1:
- P&L: GMV = Model → total GMV; COGS = GMV × COGS%; OPEX from Assumptions
- Cash Flow: opening balance = the investment; receipts = GMV allowing for payment terms

**4. Unit Economics** — CAC, tickets, COGS%, average orders; LTV / LTV/CAC / payback are automatic formulas

**5. Scenarios**

| Parameter | Pessimistic | Base | Optimistic |
|-----------|-------------|------|------------|
| Leads month 1 | −40% | from Assumptions | +75% |
| Conversion | −30% | base | +50% |
| NEW ticket | −20% | base | +25% |
| Churn | +20% | base | −25% |

**6. Cost** — the joint-venture team (row 100 onwards): role, gross salary, hours per week (from task 10)

**7. Total S&M** — the funnel by channel: channels and budget from task 10; conversions and CPL from task 16; the funnel by audience segment from tasks 7 and 10. This sheet merges what used to live in a separate "Marketing & Sales" sheet and the funnel section.

#### Step 4 — runway in Cash Flow

Add a row after "closing balance":

```
Runway (months) = closing balance / average monthly burn rate
Burn rate = total payments − receipts from customers (excluding investment)
```

#### Step 5 — sensitivity analysis

> **Guard:** before starting, confirm that `recalc.py` is in place:
> ```bash
> test -f /home/claude/scripts/recalc.py || cp -r /mnt/skills/public/xlsx/scripts /home/claude/scripts
> ```

Add a sensitivity table to the Scenarios sheet through `openpyxl`.

**Calculation algorithm (Python via openpyxl):**
1. For each of the 5 parameters and each deviation (−30%, −15%, +15%, +30%):
   - Store the base value from the Assumptions sheet
   - Write the new value into the matching cell on Assumptions
   - Run `python3 /home/claude/scripts/recalc.py /home/claude/financial-plan.xlsx 60` to recompute the P&L
   - Open the recomputed file and find the first month where cumulative P&L ≥ 0 → that is the new break-even
   - Write the difference from the base break-even, in months, into the table cell (negative = earlier, positive = later)
   - Restore the parameter's base value
2. Repeat for each parameter
3. The row's leverage = max(|shift|) across all deviations

Write numeric results into the table (not Excel formulas — the values are computed by the Python script):

| Parameter | Base value | −30% | −15% | Base | +15% | +30% | Leverage (max shift, months) |
|-----------|-----------|------|------|------|------|------|------------------------------|
| NEW average ticket | [from Assumptions] | | | 0 | | | |
| Funnel conversion | [from Assumptions] | | | 0 | | | |
| Churn rate | [from Assumptions] | | | 0 | | | |
| Marketing budget | [from Assumptions] | | | 0 | | | |
| COGS % | [from Assumptions] | | | 0 | | | |

The last column, "leverage", is max(|shift|) across the row. The parameter with the largest leverage is the priority for optimisation.

Add a conclusion under the table: **"Main lever: [parameter] — a ±30% change moves break-even by ±[N] months."**

#### Step 6 — the PD analysis sheets

The v3.3 template orders the sheets like this: **Summary → financial (Scenarios, P&L, Cash Flow, Unit Economics, Model, Total S&M, Cost) → analysis (Market, Trends, Competition, PESTEL, Customers, CJM, Interviews, Business model, Product, SWOT, OST, Hypothesis pool, PMF metrics) → Assumptions (last, because that is where you keep coming back to tune things)**. The agent fills the analysis sheets with data from the matching tasks and keeps the existing order — there is **no need** to recreate them through `openpyxl`.

The existing sheets' style: Arial 10, headers #1F3864, data #2E75B6, borders #BFBFBF. Match those settings if you add rows.

| Sheet | Content | Task |
|-------|---------|------|
| **Summary** (first) | Executive view: value proposition, TAM/SAM/SOM, LTV/CAC, runway, break-even, top 3 risks, the PD's main conclusion. Filled in **last** — it aggregates figures from every other sheet | 18a + all |
| Market | TAM/SAM/SOM plus the market card | 1, 5 |
| Trends | The table of 5+ trends plus the value chain | 2 |
| Competition | Feature matrix plus competitor cards | 3, 4 |
| PESTEL | The factor table | 6 |
| Customers | JTBD, Job Map, OS, persona cards | 7 |
| CJM | Customer Journey Map | 8 |
| Interviews | The insight table | 9 |
| Business model | Lean Canvas or BMC plus PAC (every scenario) | 10, 13 |
| Product | The PAC in detail (Product World) | 10 |
| SWOT | The matrix plus the 9 risks | 11 |
| OST | Opportunity Solution Tree | 12 |
| Hypothesis pool | Scoring + RICE + hypotheses + the testing plan | 14, 15, 16 |
| PMF metrics | PMF by phase plus the final OS | 17 |

#### Step 7 — quality checklist

- [ ] Every blue month-1 cell is filled in
- [ ] LTV/CAC ≥ 3x in the base scenario (the investment-readiness target). At 1.5–3x, mark it "acceptable at idea/MVP stage, target 3x by the round". Below 1.5x even in the optimistic case it is a red flag — pivot on monetisation.
- [ ] Runway ≥ 6 months (warn if not)
- [ ] All 13 analysis sheets are present
- [ ] The Product sheet (PAC) exists
- [ ] The sensitivity analysis is filled in (5 parameters)
- [ ] Runway has been added to Cash Flow
- [ ] 24-month horizon: columns for months 13–24 were added to Model and Cash Flow, and filled
- [ ] Formulas: `python3 /home/claude/scripts/recalc.py /home/claude/financial-plan.xlsx 60` → `"status": "success"`
- [ ] The tax regime is chosen correctly
- [ ] Light mode: the task 18a inputs are shaded yellow

---

### Task 18d: presentation (.pptx)

Read the skill at `/mnt/skills/public/pptx/SKILL.md` before building it.

```bash
cp "$SKILL_DIR/assets/presentation-template.pptx" /home/claude/presentation.pptx
```

> ⚠️ **Light mode:** delete the slides that have no data source — 5, 6, 9, 10, 13, 14, 27, 28, 29, 30, 31, 32, 33. The result is 21 slides instead of 34. Use the ready-made script:
> ```bash
> python3 scripts/delete_light_slides.py /home/claude/presentation.pptx
> ```
> It removes the empty slides and reminds you to update slide 2 (Contents).

#### Slide → data mapping

**Card-based design (v3.6).** 8 slides of the template were reworked from monotone blue blocks into a multi-column card design. When filling them in, **do not write all the text into a single `<a:t>` tag** — the template already contains a separate shape per card. Find the placeholder inside each card and fill it individually.

| Slide | Title | Template design | Data |
|-------|-------|-----------------|------|
| 1 | Cover | Full template | Name, date |
| 2 | Contents | Section list | In Light mode you must update the contents after deleting slides |
| **SECTION 01 — MARKET** | | | |
| 3 | Market size | 3 levels: TAM/SAM/SOM | TAM/SAM/SOM — task 5 |
| 4 | Market dynamics | Information block | CAGR — task 1 |
| 5 | Trends | A grid of 4 trends | Top 5 — task 2 |
| **6** | **Value chain** | **5 chain cards** (colours running from light blue to dark; Retail in red when it is being bypassed). A margin strip under each card, arrows between them. A conclusion block at the bottom. | The 5 links of the chain, the margin on each, plus the conclusion about the unclosed link — task 2 |
| 7 | Competitive landscape | 4 columns of competitor types | Direct / indirect / displacers / channel-based — task 3 |
| 8 | **Competitor comparison** | A table of 5 players × 7 columns | The feature matrix table — tasks 3, 4 |
| 9 | Key competitor | 5 AARRR blocks | The AARRR card — task 4 |
| 10 | PESTEL | 6 factors with scores | — task 6 |
| **SECTION 02 — CUSTOMERS** | | | |
| 11 | Section 02 | Section title | — |
| 12 | JTBD | 3 job types plus 3 Job Stories | Job Stories — task 7 |
| **13** | **CJM** | **A 4×7 table**: rows (actions / emotions / pains / opportunities) × 7 stages. **The column header is aligned** to the data columns (x=1.30..8.41, w=1.15) | The table's 28 cells — task 8 |
| 14 | Interview insights | 5 patterns with counters | Top 5 plus quotes — task 9 |
| 15 | Opportunity Score | A table of 5 outcomes | Top 5 — tasks 7, 17 |
| **16** | **Personas / segments** | **3 persona cards** (shades of blue). Each: header → the sections "Context / Jobs / Pain" → quote and OS at the bottom | 3 personas with their sections — tasks 7, 9 |
| **SECTION 03 — CURRENT SCENARIO** | | | |
| 17 | Section 03 | Section title | — |
| 18 | Company goals | 3 KPIs plus 3 goals | Outcomes over 12–24 months — task 12 |
| **19** | **Lean Canvas / BMC** | **The 9 blocks of the classic Lean Canvas**. Top row (1–5) — headers on a dark background with content on light (h=1.25 in). Bottom 2×2 (6–9) — blocks of h=1.08 with a coloured strip on top | The 9 blocks — task 10 |
| 20 | PAC | The 4 worlds | Customer / Competitor / Distribution / Product — task 10 |
| 21 | SWOT | A 2×2 matrix | The 4 quadrants — task 11 |
| **22** | **Consistency** | **3 coloured criterion cards** (✅ green / ⚠️ orange / ✅ green). A header with the name plus "Rationale / Metrics" and a status strip. Conclusion at the bottom | The 3 criteria — task 11 |
| 23 | Unit economics | 3 KPIs plus a metric list | CAC/LTV/payback — financial plan |
| **SECTION 04 — OST** | | | |
| 24 | Section 04 | Section title | — |
| 25 | OST levels 1–2 | The hierarchy outcome → opportunities → solutions | Outcome plus opportunities — task 12 |
| **26** | **OST levels 3–4** | **3 solution columns**. Each: a "SOLUTION A/B/C" header → description → an "EXPERIMENT" block (dark blue) → a criterion/timeframe/budget block (light grey) | 3 solutions × experiment × criteria — task 12 |
| **SECTION 05 — ALTERNATIVE SCENARIO** | | | |
| 27 | Section 05 | Section title | — |
| 28 | Key changes | A "current vs alternative" table | A comparison across 4 parameters — tasks 13, 14 |
| 29 | RICE | 3 opportunities with the formula | Prioritisation — task 14 |
| **30** | **Hypothesis pool + tests** | **3 hypothesis blocks** in a column. Each: a header with a risk tag (🔴 red / 🟠 orange) → "Statement / Method / Criterion ✅" → a timeframe-and-budget strip. The verification rule at the bottom | 3 hypotheses × risk × method — tasks 15, 16 |
| **SECTION 06 — PMF AND NEXT STEPS** | | | |
| 31 | Section 06 | Section title | — |
| 32 | PMF by phase | 3 phases with the Sean Ellis Test | — task 17 |
| **33** | **Final OS** | **A full table of 10 outcomes** with coloured OS badges (red = critical → green = low) and priorities. Alternating white and grey row backgrounds | Top 10 — task 17 |
| 34 | Next steps | The 5 steps of Value Validation | — tasks 16, 17 |

#### Design rules

- The title is the takeaway (the narrative runs through the titles)
- Key words in **bold**
- Sources on every information slide
- Palette: `#FFFFFF`, `#000000`, `#94A3F6`, `#457E4A`, `#F5939E`

#### Filling in placeholders: the technical details

**Step 1 — build a "slide number → `slideN.xml`" mapping**

After any slide manipulation (`delete_light_slides.py`, `add_competitor_comparison_slide.py`), the numbering in `extract-text` diverges from the file numbers. For example, after deleting 13 slides in Light mode, `slide7.xml` may correspond to "Slide 5" in extract-text. Read `presentation.xml.rels`:

```python
import re
with open("unpacked/ppt/presentation.xml") as f:
    pres = f.read()
with open("unpacked/ppt/_rels/presentation.xml.rels") as f:
    rels = f.read()

# The order of rIds in sldIdLst is the order of slides in the deck
sld_ids = re.findall(r'<p:sldId[^/]*r:id="([^"]+)"', pres)
# rId → file
rid_to_file = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))

# Mapping: "Slide N in extract-text" → "slideK.xml"
slide_num_to_file = {
    i+1: rid_to_file[rid]
    for i, rid in enumerate(sld_ids)
    if rid in rid_to_file
}
# Now slide_num_to_file[5] gives the correct slide7.xml (not slide5.xml)
```

**Step 2 — the regex has to allow for the `xml:space="preserve"` attribute**

Text with leading spaces or line breaks is wrapped in XML as `<a:t xml:space="preserve">...</a:t>`. The **wrong** regex skips those tags:

```python
# ❌ Misses <a:t xml:space="preserve">
re.findall(r'<a:t>([^<]*)</a:t>', xml)
```

The **right** regex allows for optional attributes:

```python
# ✅ Catches both <a:t> and <a:t xml:space="preserve">
re.findall(r'<a:t(?:\s[^>]*)?>([^<]*)</a:t>', xml)

# Replacement that preserves the attributes:
def replace_run(xml, old_text, new_text, count=1):
    def xe(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    pattern = r'(<a:t(?:\s[^>]*)?>)' + re.escape(xe(old_text)) + r'(</a:t>)'
    return re.subn(pattern, lambda m: m.group(1) + xe(new_text) + m.group(2), xml, count=count)
```

**Step 3 — check after filling in**

```python
import subprocess
result = subprocess.run(['extract-text', 'output.pptx'], capture_output=True, text=True)
placeholders = re.findall(r'\[[^\]]{1,80}\]', result.stdout)
# Filter out emoji prefixes and legitimate [...] occurrences
real = [p for p in placeholders if not any(x in p for x in ['✅','⚠️','🔴','🟠','🟡','🟢'])]
assert len(real) == 0, f"Still unfilled: {real}"
```

#### Troubleshooting validation

Packaging a deck is a plain zip; validation is a separate step you must not skip:

`extractall` is fine for a deck you built yourself. For an archive that arrived
from anywhere else, resolve each member's destination first and refuse the ones
that escape the target directory — a crafted member name containing `../` writes
wherever it likes. `scripts/add_competitor_comparison_slide.py` shows the guarded form.

```bash
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx
# edit unpacked/ppt/slides/slideN.xml
(cd unpacked && rm -f ../out.pptx && zip -qXr ../out.pptx .)   # zip from INSIDE the dir
python3 /mnt/skills/public/pptx/scripts/office/validate.py out.pptx --original deck.pptx
```

`validate.py` names the fix for each failure. Never ship a deck that failed it — PowerPoint applies the same checks and will refuse the file.

Common errors and how to fix them:

**"Notes slide referenced by multiple slides"** — appears after running `add_competitor_comparison_slide.py` or after copying slides by hand. Several `_rels` files point at the same `notesSlide.xml`. The fix:

```python
import re, os, shutil

# 1. Remove every notesSlides reference from the slide rels
rels_dir = "unpacked/ppt/slides/_rels"
for f in os.listdir(rels_dir):
    path = f"{rels_dir}/{f}"
    with open(path) as fp: content = fp.read()
    # IMPORTANT: [^>]*? — a non-greedy match, otherwise a Target containing '/' is missed
    new = re.sub(r'\s*<Relationship[^>]*?notesSlide[^>]*?/>', '', content)
    if new != content:
        with open(path, "w") as fp: fp.write(new)

# 2. Delete the notesSlides folder entirely
notes_dir = "unpacked/ppt/notesSlides"
if os.path.exists(notes_dir):
    shutil.rmtree(notes_dir)
```

An investor deck does not need notes — removing them is safe.

**"Missing required file" or "Invalid Content_Types"** — usually the result of editing `[Content_Types].xml` by hand, or of zipping from outside the unpacked directory so the paths gained a prefix. Revert the hand edit, and always zip with `(cd unpacked && zip -qXr ../out.pptx .)`.

#### Final step: the PowerPoint round-trip through LibreOffice

Even after validation passes, an OOXML-valid file may still fail to open in PowerPoint because of manifest quirks. Re-saving through LibreOffice fixes it, because LibreOffice exports through the Office Open XML filter:

```bash
bash "$SKILL_DIR/scripts/finalize_pptx.sh" /home/claude/presentation.pptx \
     /mnt/user-data/outputs/presentation-[slug].pptx \
     "$SKILL_DIR/assets/presentation-template.pptx"
```

The first argument accepts a finished `.pptx` or the unpacked directory; the third is the template, optional but worth passing whenever the deck derives from one.

The script does four things:
1. Packaging (a plain zip, when given a directory)
2. `office/validate.py`, with `--original` when a template was passed
3. The LibreOffice round-trip through `office/soffice.py` (the wrapper, not bare `soffice`)
4. Verification through `python-pptx`, including an unfilled-placeholder check

Without step 3 the deck may open in LibreOffice and Google Slides but **not** in PowerPoint. That is fatal if the user sends the file to an investor. If the round-trip cannot run, the script warns instead of claiming the file is verified.

#### Quality checklist

- [ ] No `[...]` left on slides 3, 7, 8, 12, 19, 23 (the key information slides)
- [ ] No unfilled `[placeholders]` anywhere in the deck — check with `extract-text` plus `re.findall(r'\[[^\]]{1,80}\]', text)`
- [ ] Every number has a source
- [ ] Slide 8: the competitor comparison table covers at least 5 players, and every cell holds either a number or "n/a" with a confidence marker
- [ ] Slide 23: runway is present
- [ ] Slide 16: the persona cards come from task 7
- [ ] Slide 18: the horizon matches the answer from Step 0 (12 or 24 months)
- [ ] Slide 22: all 3 consistency criteria are filled in (desirability / viability / feasibility)
- [ ] Slide 33: the final OS holds the top 10 outcomes from task 17
- [ ] `office/validate.py` passed on the final file
- [ ] `scripts/finalize_pptx.sh` has been run — the PowerPoint round-trip through LibreOffice
- [ ] Opening check through `python-pptx`: `Presentation(path)` does not raise and `len(pres.slides)` matches expectations (21 for Light, 34 for Full)

---

### Finishing PD — the final summary in the chat

Once all three artifacts (or four in Full) exist, **do not end the conversation in silence**. Give the user a structured summary in the chat.

**How to determine the main conclusion (Go / Pivot / No-go):**

Apply it across all the PD results. Count the criteria that fired:

| Condition | Signal |
|-----------|--------|
| Red flags fired (from the "STOP / PIVOT" section) | 0 / 1-2 / ≥ 3 |
| Investment readiness (tracker after PD) | ≥ 6/8 / 4-5/8 / < 4/8 |
| OS of the main opportunity | ≥ 15 / 10-14 / < 10 |
| LTV/CAC in the base scenario | ≥ 3x / 1.5-3x / < 1.5x |

**Decision rule:**
- **Go (carry on):** 0 red flags AND investment readiness ≥ 6/8 AND LTV/CAC ≥ 3x
- **Go with risks:** 1–2 red flags (excluding LTV/CAC < 1.5x), investment readiness ≥ 4/8. State the risks and the plan to close them.
- **Pivot (serious changes needed, but the market is there):** 1–2 red flags including LTV/CAC or a lack of differentiation, but OS ≥ 10 and SAM sufficient. Propose a concrete pivot direction (segment / monetisation model / value proposition — see the "Pivot vs adjustment" table).
- **No-go (the market is not confirmed):** ≥ 3 red flags OR SAM below the threshold OR OS < 8 across all segments. Recommend stopping the project or returning to Step 0 with a different problem hypothesis.

**Principles:**
- Honesty beats optimism. If the data says No-go, the agent **must** say No-go without softening it.
- Quote the specific numbers that led to the conclusion.
- Offer an alternative even on a No-go (for example, "the B2C market did not hold up, but the data carries a signal for B2B SMB — worth checking").

**Output template:**

```
✅ PRODUCT DISCOVERY COMPLETE — [Project name]
═══════════════════════════════════════════════

📋 TASKS COMPLETED: [N of 18] in [Light / Full] mode

📁 ARTIFACTS:
  • One-pager:       one-pager-[project-slug].pptx
  • Financial plan:  financial-plan-[project-slug].xlsx
  • Presentation:    presentation-[project-slug].pptx
  • Interview guide: interview-guide-[project-slug].docx (Full only)

🎯 MAIN CONCLUSION: [Go / Go with risks / Pivot / No-go]
  Rationale: [the numbers — how many red flags, investment readiness N/8, LTV/CAC, OS]
  [If Pivot or No-go: exactly what to change, or why the project should not continue]

💡 VALUE VERDICT:
  Value Proposition: "[the wording from task 10]"
  Main segment:      [from task 18a]
  Monetisation:      [model, ticket in roubles]

📊 KEY METRICS (base scenario):
  • TAM / SAM / SOM:   [X / Y / Z ₽bn]
  • LTV / CAC:         [N.Nx]
  • Runway:            [N months]
  • Break-even:        [month N]

🚩 TOP 3 RISKS:
  1. [A hypothesis carrying High risk] — test via: [method] within [timeframe]
  2. ...
  3. ...

🎯 INVESTMENT READINESS: [N / 8 ✅] — [High / Medium / Low]
  Close before the round: [the ⚠️ and ❌ items from the tracker]

▶️ NEXT 3 STEPS (over the coming 2 weeks):
  1. [Action] — owner [role] — due [+N days]
  2. ...
  3. ...

═══════════════════════════════════════════════
```

If any PD blocks were skipped (Light), mark it explicitly: "NPS / retention: needs verification (Light mode, task 17 skipped)".

---
