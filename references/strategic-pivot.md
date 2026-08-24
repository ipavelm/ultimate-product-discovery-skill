# Strategic pivot: PD for an operating business

This file is the alternative way to run PD when the person already has a working business and is weighing a **strategic move** into a new direction: from services into a product, from one segment into another, from B2C into B2B, from one geography into another.

Read this file when Step 0 makes it clear that:
- The stage is "has revenue" (not idea, not MVP)
- The business has been running for ≥ 1 year
- The person frames the task not as "validate a new idea from scratch" but as "should we change direction / add something new / drop what we do today"

Typical requests that fit this scenario:
- "We run a growth agency, and we want to know whether to build a product module or stay in services"
- "We have been operating in Russia for 3 years and are thinking about Kazakhstan or the Arab market — which makes sense?"
- "Our SMB SaaS does $500k ARR but growth has slowed. Should we move into Enterprise?"
- "We sell coffee to offices and want to launch a B2C line on Wildberries — is it worth it?"

An ordinary idea- or MVP-stage startup does not need this route — work through the standard 18 tasks in SKILL.md.

## How a strategic pivot differs from ordinary PD

Ordinary PD starts from zero: the person has an idea and you check whether a market exists for it. A strategic pivot starts from something that exists: **the current business works**, **the alternative is hypothetical**, and the question is not "is there a market" but "is changing course worth it, given that what we do today already pays for itself".

That produces three fundamental differences:

1. **Two scenarios are compared as equals.** The current scenario ("carry on as we are") is as much a candidate as the new one. It cannot be treated as a zero baseline. It has its own metrics, risks and trajectory.

2. **Historical data is the primary source.** A business with ≥ 1 year behind it has real conversions, retention, CAC and churn. Use those instead of expert estimates and benchmarks. Data confidence is automatically 🟢 for the current scenario and 🟡–🔴 for the alternative.

3. **Cost of change is a separate cost category.** Switching course is not free: the team has to be retrained or replaced, some current customers will be lost, and 6–12 months will pass with no revenue in the new direction. These are explicit lines in the new scenario's financial plan.

## The strategic pivot protocol

### Stage 1: describe the current state (not "from scratch")

Replace parts of tasks 1, 3 and 5 — instead of hunting for external market estimates, ask the person for their internal data. At minimum:

- Revenue for the last 12 months, month by month
- Customer structure: segments, average ticket per segment, concentration (% of revenue from the top 10% of customers)
- CAC by channel (if available) or at least by source (organic / paid / referral / outbound)
- Churn and retention by cohort
- P&L with gross margin
- Team: roles and cost

If the data does not exist, ask for exports from the CRM or the accounting system. Without them a strategic pivot cannot be done honestly. If the person will not share, run PD in hybrid mode: use expert estimates for the current scenario and mark confidence 🔴 explicitly.

### Stage 2: two Lean Canvases, treated as equals

Replace the usual task 10 (one canvas for the current scenario) with two canvases:

- **Scenario A: carry on as we are** — what happens if nothing changes. Value Proposition, segments, channels and monetisation come from reality. The problems: slowing growth? a plateau? competitors? Fill it in honestly.
- **Scenario B: the new course** — the pivot hypothesis. Value Proposition, segments and channels may be completely different. Fill it in as you would for a new product.

### Stage 3: project the metrics 24 months out for both

An ordinary financial plan covers 12–24 months from zero. For a strategic pivot:

- **Scenario A (continuation)**: extrapolate the current trajectory. If growth has been 5% MoM for the last six months and is slowing, model further slowdown, a plateau, and a possible decline as competition intensifies. Not "magically hold 5% MoM forever".
- **Scenario B (pivot)**: 6–12 months of transition (zero or negative revenue in the new direction plus contraction in the old), then growth in the new one. Book the cost of change separately.

Use the "Scenarios" sheet of the financial plan in a non-standard way: instead of pessimistic/base/optimistic for one hypothesis, build the columns "Scenario A base", "Scenario A pessimistic", "Scenario B base", "Scenario B pessimistic". The agent can add the columns through openpyxl if that is easier.

### Stage 4: cost of change for scenario B

List separately what has to be lost or invested to make the transition:

| Category | Examples | Estimate |
|----------|----------|----------|
| Lost revenue | Existing customers who fall away during the transition | ₽/month × N months |
| Lost competencies | Team members who do not transfer to the new course (retraining or replacement) | ₽ one-off |
| Foregone upside | The growth scenario A would have produced if you had not stopped | ₽ over the period |
| Investment in the new | Development, marketing, hiring, tests | ₽ over the period |
| Reputational risk | If the switch is public (rebranding, repositioning) — a possible dip in B2B trust | Assess qualitatively |

These numbers are summed and subtracted from scenario B's NPV in the final comparison. Without them the comparison is dishonest — scenario B looks better than it is.

### Stage 5: decision criteria

Instead of the usual Go/Pivot/No-go algorithm, use three questions:

1. **NPV over a 3–5 year horizon:** which scenario delivers more present value once cost of change and risk are accounted for?
2. **Feasibility:** does the team have the competencies for scenario B? If not, add hiring or replacing 30–70% of the team to the cost of change — that alone often kills the pivot's economics.
3. **Reversibility:** if it becomes clear in 6–12 months that scenario B is not working, can you return to A? If yes, the pivot's risk is low. If not (burned customers, a damaged brand, a dispersed team), it is high.

Final verdicts:
- **Pivot to scenario B** — when NPV(B) > NPV(A) × 1.5 (a risk premium), feasibility is ≥ 70%, and there is at least partial reversibility.
- **Continue with A and reinforce it** — when NPV(A) ≥ NPV(B), or NPV(B) is only slightly higher while risk is high. Propose 2–3 improvements to the current scenario (a new segment inside the current niche, raising prices, international expansion without changing the product).
- **Run both in parallel** — when the company is large enough to launch B as a separate line without winding A down. Usually feasible at revenue ≥ ₽30–50M/month and a team of ≥ 15 people.
- **Stay in A but pin down hypothesis B** — when NPV(B) is higher but the risk is high: propose a small experiment in B (1–2 months, 5–10% of the budget) to reduce the uncertainty before committing to a full pivot.

## Adapting the artifacts

- **One-pager** — instead of one Value Proposition, show the comparison of the two scenarios and the recommendation.
- **Financial plan** — both scenarios on the same sheets, with a separator. The Summary shows the comparison of NPV, break-even, team and risk.
- **Presentation** — a scenario comparison slide (the analogue of slide 8, "Competitor comparison", but for internal options). Use the same table format.

If the person picks scenario B after the PD, run **another PD** through the standard 18 tasks, with scenario B now as the primary hypothesis rather than an alternative. A strategic pivot delivers a strategic decision, not a detailed validation of the new hypothesis.
