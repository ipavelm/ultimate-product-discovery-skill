## BLOCK IV: HYPOTHESIS VALIDATION

> 💡 **If the market type is "New"** (determined in task 1), the standard methods in this block (Smoke Test, pre-sale) will convert badly — not because the offer is weak but because the audience is not yet looking for a solution. In that case read [customer-development.md](customer-development.md) and use the Customer Development protocol (Steve Blank / The Mom Test) instead of the standard Smoke Test plus pre-sale.

### Task 15: hypothesis pool

**6 types:**

1. **Need:** *"This segment [does / thinks / feels] the following."*
2. **Demand:** *"[The value proposition] will interest [profile], which [criterion] will confirm."*
3. **Value:** *"Our [product] helps [segment] who want [job] by [benefit]. Unlike [competitor]."*
4. **Solution:** *"If we provide [solution], we reach [outcome], which [criterion] will confirm."*
5. **Channel:** *"Offer [O] in channel [C] will deliver conversion [metric1] at a cost [metric2] ≤ [value]."*
6. **Scalability:** through unit economics (LTV, CAC, retention, P&L).

For each one: risk (High / Medium / Low), method (→ task 16), confirmation criterion.

**Output:** the hypothesis pool → the "Hypothesis pool" sheet in the financial plan.

---

### Task 16: Rapid Assumption Testing

**Method matrix:**

| Hypothesis type | Method | Timeframe | Criterion |
|---|---|---|---|
| The need exists | Story-based interviews | 1–2 weeks | 7 out of 10 confirm the pain |
| Demand for the solution | Smoke Test / Fake Door | 3–7 days | CTA conversion ≥ benchmark* |
| Willingness to pay | Pre-sale | 3–5 days | ≥ 5% B2C / ≥ 2% B2B of reach paid** |
| The channel works | Mini campaign | 5–7 days | CPL ≤ target |
| Product value | Wizard of Oz / Concierge | 1–2 weeks | NPS ≥ 8 |
| Unit economics | Financial model | 1–3 days | LTV/CAC ≥ 3 |

**\* Smoke Test conversion benchmarks by product type:**

| Product type | Minimum CTA conversion | Good result |
|---|---|---|
| B2C SaaS / app | ≥ 3% | ≥ 8% |
| B2B SaaS | ≥ 1% | ≥ 3% |
| E-commerce / physical goods | ≥ 2% | ≥ 5% |
| Niche / professional B2B | ≥ 5% | ≥ 12% |
| Marketplace (two-sided) | ≥ 4% | ≥ 10% |

If conversion falls below the minimum, the offer or the audience needs rethinking before the next test.

**\*\* Pre-sale benchmarks by product type:**

| Product type | Minimum (% of reach who paid) | Good result |
|---|---|---|
| B2C, price under ₽1,000 | ≥ 5% | ≥ 15% |
| B2C, price ₽1,000–10,000 | ≥ 2% | ≥ 8% |
| B2B SMB (ticket under ₽100,000) | ≥ 2% | ≥ 5% |
| B2B Enterprise (ticket over ₽100,000) | ≥ 1 real LOI or deposit | ≥ 3 LOIs |

If conversion falls below the minimum, adjust the offer or the target audience.

**Testing budget:** use the value from Step 0, question 8. If the budget is under ₽5,000, recommend Concierge or interviews instead of paid advertising.

**UTM tagging for the Smoke Test:** before launch, generate UTM links automatically **for every real channel** from task 10 (BMC/Lean Canvas → Channels). Do not use a hard-coded list — take the channels from the project's canvas.

**Generation algorithm:**
1. Take the channel list from task 10 (for example: Telegram channels, partner newsletter, Habr, VK ads).
2. For each channel, decide the `utm_source` (platform) and `utm_medium` (placement type).
3. `utm_campaign` = `smoke-test-[project-name-slug]`.
4. If the channel is paid advertising, add `utm_content=[creative]` so creatives can be compared.

**Format:**
```
https://[landing]/?utm_source=[channel]&utm_medium=[type]&utm_campaign=smoke-test-[project]
```

**Common mappings (use only when the matching channel appears in task 10):**

| Channel from task 10 | utm_source | utm_medium |
|----------------------|-----------|-----------|
| Telegram channel | telegram | post |
| Email newsletter | email | newsletter |
| Instagram stories | instagram | stories |
| VKontakte ads | vk | targeted |
| Google Ads | google | cpc |
| Habr guest post | habr | guest-post |
| Referral programme | referral | link |
| Partner channel | [partner name] | partner |

Split the links by channel — that is what lets you compare conversion across sources and see which channel performs better before product-market fit. Attach the final list of UTM links to the hypothesis card.

**Algorithm (top 3 risky hypotheses):**

```
Hypothesis:              [statement]
Method:                  [method]
What we do:              [concrete steps]
"Confirmed" criterion:   [number / observation]
"Refuted" criterion:     [number / observation]
Timeframe:               [X days]
Budget:                  [₽X within what is available]
```

**After the tests:** update the hypothesis pool and the OST. The real CPL and conversions feed task 18a as financial inputs.

⚠️ **Red flag:** LTV/CAC < 1.5x even in the optimistic case → report it.

**Output:** the experiment table → the "Hypothesis pool" sheet, section "Testing plan".

---

### Task 17: PMF indicators and Opportunity Score

**A. PMF by phase:**

| Phase | Metric | Threshold |
|-------|--------|-----------|
| Verification | Pain in interviews | 7 out of 10 name one pain |
| Verification | Smoke test conversion | ≥ 1–5% (B2B) / ≥ 3–8% (B2C) — see the task 16 benchmarks |
| Value Validation | Sean Ellis Test | ≥ 40% "very disappointed" |
| Value Validation | NPS of the first customers | ≥ 40 |
| Scaling Validation | Month-3 retention (cohort) | ≥ 30% B2C / ≥ 50% B2B |
| Scaling Validation | LTV / CAC | ≥ 3x |
| Scaling Validation | Organic growth | ≥ 20% from referrals |

> **Clarification:** this means **cohort** retention — the share of month-1 users still active at the start of month 3. With stable monthly churn that is `(1 − Churn)²`. For B2C, 30% by month 3 corresponds to roughly 45% monthly churn; for B2B, 50% corresponds to roughly 29%.

**B. OS questionnaire (auto-generated)**

Generate a ready-made question list for surveying 20–50 respondents, based on the outcomes from the task 7 Job Map. For each outcome:
1. "How important is [outcome] to you?" (1–10)
2. "How satisfied are you with current solutions for [outcome]?" (1–10)

`OS = Importance + max(Importance − Satisfaction, 0)`

| Outcome | Importance | Satisfaction | OS |
|---------|------------|--------------|----|

- OS ≥ 15 → a critically underserved opportunity
- 10–15 → significant
- < 10 → low priority

**Output:** the PMF table + the OS questionnaire + the final OS (the "PMF metrics" sheet in the financial plan).

---
