## BLOCK III: STRATEGIC SCENARIOS

> 📋 **Worked examples** of the Lean Canvas, BMC, PAC and OST are in [examples.md](examples.md). Read the matching example section before filling a canvas, to keep the level of detail consistent.

### Task 10: the current strategic scenario

**Goal:** formalise the business model hypothesis.

**Choosing the canvas:** ask the user:
- **Lean Canvas** — a startup at idea or MVP stage (the problem is not solved yet, the hypotheses are untested)
- **BMC** — there are customers or revenue (the model already works, so describe it as it is)

**Business model type:** ask this as well:
- **Product** — you sell an outcome (SaaS, a physical good, an app). Key metrics: average ticket, COGS of production or development, gross margin.
- **Service** — you sell time and expertise (consulting, agency, outstaffing). Key metrics: billable hours, utilisation rate (target ≥ 70%), average project value, gross margin = revenue − delivery payroll.
- **Marketplace** — a two-sided platform connecting suppliers and buyers. Key metrics: GMV, take rate (%), Revenue = GMV × take rate. Important: the JTBD and the personas are described separately for each side (supplier and buyer). **For the Lean Canvas / BMC, build two separate canvases — one for the supply side, one for the demand side.** They have different problems, value propositions, channels and metrics; trying to fit both sides on one canvas produces a shallow result. In task 18a pick the leading side (usually the one that is harder to acquire — supply, in most cases) and build the financial plan around it, but count both sides in the liquidity tracker. The core problem at launch is chicken-and-egg: no suppliers means no buyers and vice versa. Record it in task 15 as a separate scalability hypothesis.

  **Geographic locality of marketplaces.** If the transaction requires physical contact (food delivery, at-home services, transport, short-term rentals), liquidity is measured **not globally** but **per geographic cell** (a district, or a city area within 30 minutes' reach). 100 cooks and 500 customers spread across Moscow is not liquidity if the cook is in Butovo and the customer is in Khimki. The correct metric: "each dense cell of radius N km must have ≥ 10 suppliers and ≥ 20 transactions a week". Action: in task 5 (TAM/SAM/SOM), size a single dense cell and work out how many cells are needed to reach the target SAM. In task 16 (rapid testing), prove liquidity in one cell before expanding geographically — the classic Uber/DoorDash playbook. For non-physical marketplaces (SaaS integrations, digital services, freelance exchanges) geography does not matter and liquidity can be counted globally.
- **Hardware / physical device** — you sell a physical product (IoT, devices, wearables). The key differences: COGS = manufacturing + logistics + returns (usually 40–60%, far above SaaS); no subscription, only one-off and repeat sales; the development cycle to MVP depends on complexity (4–6 months for IoT on off-the-shelf components, 12–18 months for consumer electronics with custom hardware); MOQ (minimum order quantity) creates cash flow risk at launch. Record these in task 15 as separate hypotheses: "manufacturing at the required volume and target unit cost" and "a distribution channel with acceptable CAC".

**A) Lean Canvas** (for idea/MVP):

| Block | What to fill in |
|-------|-----------------|
| Problem | The top 3 problems of the target customers |
| Segments | The early adopters — who are they? |
| Unique value proposition | Why you, and why now |
| Solution | The features that close the top 3 problems |
| Channels | How you reach customers |
| Revenue streams | The monetisation model, average ticket |
| Cost structure | Fixed + variable |
| Key metrics | How you measure progress |
| Unfair advantage | What is hard to copy |

**B) Business Model Canvas** (when there are customers or revenue):

| Block | What to fill in |
|-------|-----------------|
| Customer Segments | Different when needs, channels or amounts differ |
| Value Propositions | Quantitative (price, speed) or qualitative (emotion) |
| Customer Relationships | Along AARRR: Acquisition → Activation → Retention → Referral → Revenue |
| Channels | Awareness → Evaluation → Sales → Delivery → After-sales |
| Key Activities | Along Porter's value chain |
| Key Resources | Physical, financial, intellectual, human |
| Key Partners | Collaboration / coopetition (working with competitors) / joint ventures / suppliers |
| Revenue Streams | One-off vs recurring. Subscription, commission, rental, freemium |
| Cost Structure | Fixed / variable |

**For B2B:** reflect the long sales cycle in Channels (lead → qualification → demo → pilot → contract → onboarding → renewal, 1–12 months).

**C) Product Attribute Canvas (PAC)**

- **Customer World:** segments, jobs, value propositions
- **Competitor World:** competitors, differentiation, OS — where they lose
- **Distribution World:** aha moment, activation, growth loop
- **Product World:** features mapped to Job Stories, unique properties

**Consistency check:**
- **Desirability** — do the value propositions match the jobs?
- **Viability** — is the model scalable?
- **Feasibility** — are the resources sufficient?

**Value Proposition formula (the final wording for the one-pager and the slide):**

Once the canvas is filled in, state the value proposition in a single sentence:

*"We help [whom — the segment] [do what — the Job-to-be-Done], unlike [the main competitor / the current solution], because [the unfair advantage / unique mechanism]."*

Example: "We help freelancers track project time automatically, unlike manual bookkeeping in Excel, because we integrate directly into Telegram and require no context switching."

This wording is reused in: task 18b (one-pager, the "Solution" section), task 18d (slide 16) and task 18a (the "Value proposition" parameter).

**Output:** the "Business model" sheet (Lean Canvas or BMC) and the "Product" sheet (PAC) in the financial plan.

---

### Task 11: SWOT analysis

Checklists:
- **Strengths:** network effects, margin, recurring revenue, a unique channel, switching costs
- **Weaknesses:** from the canvas — where resources or activities are lacking
- **Opportunities:** new segments, recurring payments, trends, partners
- **Threats:** competitors, alternatives, regulatory change

**9 key risks (checklist):**
- [ ] The need does not match the value propositions
- [ ] The market is too small for the stated goals
- [ ] Differentiation from competitors was not accounted for
- [ ] The channels do not make sense on this market
- [ ] Monetisation cannot make the economics work
- [ ] The processes and resources are unrealistic
- [ ] The business model does not exploit the trends
- [ ] The influence of regulators and the value chain was not accounted for
- [ ] The revenue and value growth drivers are not aligned

⚠️ **Red flag:** no differentiation from any of the 4 competitor types → report it.

**Output:** the "SWOT" sheet in the financial plan.

---

### Task 12: Opportunity Solution Tree (OST)

**Structure (4 levels):**

```
BUSINESS OUTCOME — concrete and measurable
└── OPPORTUNITY 1
│   ├── Sub-opportunity 1.1
│   │   ├── Solution A → Experiment A1
│   │   └── Solution B → Experiment B1
│   └── Sub-opportunity 1.2
└── OPPORTUNITY 2
```

**Algorithm:**
1. The business outcome must be measurable. Not "become the best" but "retention 20% → 35% in 6 months".
2. Opportunities come from tasks 7–9. Decompose the big ones into smaller ones.
3. Pick the target opportunity by OS. One at a time.
4. At least 3 solutions (this prevents confirmation bias).
5. Experiments: take the riskiest assumption → the smallest experiment that tests it.

**Versioning:** record the date and what changed on every update.

**Output:** the OST diagram (the "OST" sheet in the financial plan).

---

### Task 13: alternative scenarios

**Step 1 — are alternatives needed?**

Score the current scenario against the same 7 criteria used for the comparison in task 14. Here you score only the current scenario (0 = not met, 1 = met):

| Criterion | Score for the current scenario (0–1) |
|-----------|--------------------------------------|
| Market size (SAM) | |
| Desirability (jobs ↔ value proposition) | |
| Viability (economics) | |
| Feasibility (resources) | |
| Differentiation | |
| Use of trends | |
| Risky hypotheses (fewer is better) | |
| **Total** | |

- Total < 4/7 **or** Desirability / Viability / Feasibility = 0 → alternatives **are needed**
- Total ≥ 5/7 → alternatives are **optional**; move on to task 14

**Step 2 — the SWOT matrix:**

| Pair | Question |
|------|----------|
| Strengths + Opportunities | How do we use the strength? |
| Strengths + Threats | How does the strength head off the threats? |
| Weaknesses + Opportunities | How do the opportunities remove the weaknesses? |
| Weaknesses + Threats | How do we minimise the risk? |

**Step 3:** each alternative scenario gets a Lean Canvas or BMC plus a PAC, headed "SCENARIO 2: [Name]", on the "Business model" sheet (one sheet, with separators).

**Output:** the alternative scenarios on the "Business model" sheet of the financial plan.

---

### Task 14: scenario scoring + RICE

> ⚠️ **Light mode:** task 13 is skipped in Light, so there are no fully developed alternative scenarios. Three options:
>
> 1. **Default:** score only the current scenario against the 7 criteria (section A). If the total is < 4/7, offer the person Full mode or a move to option 2 or 3.
> 2. **A quick alternative from the OST:** take opportunity 2 (the second-highest OS) from the task 12 OST and state it as an alternative scenario in 3 sentences (target segment + value proposition + monetisation). Not a full Lean Canvas, but it gives a second option to compare against. 5–10 minutes.
> 3. **A full alternative:** run task 13 in short form (Lean Canvas without the PAC) for one alternative scenario. Adds 15 minutes to Light.
>
> The RICE prioritisation (section B) runs as normal.

**A) Scenario comparison:**

This uses **the same 7-criteria table as task 13 (Step 1)**, with a column per scenario. If you already scored the current scenario in task 13, reuse those values in the "Scenario 1" column instead of recalculating.

| Criterion | Scenario 1 | Scenario 2 | Scenario 3 |
|-----------|-----------|-----------|-----------|
| Market size (SAM) | | | |
| Desirability (jobs ↔ value proposition) | | | |
| Viability (economics) | | | |
| Feasibility (resources) | | | |
| Differentiation | | | |
| Use of trends | | | |
| Risky hypotheses (fewer is better) | | | |
| **Total** | | | |

If the user does not accept the scoring result, ask what the blocking factor is, adjust the weights and recalculate.

**B) RICE prioritisation of the opportunities from the OST:**

`RICE = (Reach × Impact × Confidence) / Effort`

- Reach — people per month
- **Impact** — derive it from the task 7 OS: OS ≥ 15 → Impact = 3; OS 10–14 → Impact = 2; OS 6–9 → Impact = 1; OS < 6 → Impact = 0.5. This removes duplicated judgement work and grounds RICE in the interview data.
- Confidence — 100% / 80% / 50%
- Effort — person-months

**Output:**
- Scenario scoring → the "Hypothesis pool" sheet, section "Scenario scoring"
- RICE → the "Hypothesis pool" sheet, section "RICE prioritisation"

---
