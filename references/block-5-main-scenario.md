## BLOCK V: MAIN SCENARIO

### Task 18a: choosing the main strategic scenario

Take the highest score from the task 14 ranking. On a tie, prefer the scenario with fewer risky hypotheses.

**Pin down the parameters:**

```
MAIN SCENARIO
────────────────────────────────────────
Name:                   [e.g. "B2B SaaS with freemium"]
Target segments:        [from the canvas → Customer Segments]
Value proposition:      [from PAC → Value Propositions]
Monetisation model:     [subscription / commission / one-off]
Average ticket NEW:     [X RUB]
Average ticket RETURN:  [Y RUB]
Key channels:           [from the canvas → Channels]
Team in month 1:        [roles and headcount]

FINANCIAL INPUTS (month 1)
────────────────────────────────────────
Leads per month:        [N — from task 16, or an estimate]
End-to-end conversion:  [X%]
New customers month 1:  [= leads × conversion]
GMV month 1:            [= new customers × average ticket NEW]
OPEX month 1:           [marketing + payroll + infrastructure]
COGS %:                 [from Cost Structure]
Gross Margin %:         [= 1 − COGS%]
CAC:                    [= (marketing + sales payroll) / new customers]
LTV (12 months):        [= GM × (ticket_new + Σ(ticket_return × Retention_m^t)), t=1..11]
                         where GM = Gross Margin % = 1 − COGS%
                         Simplified form (for subscriptions): LTV = ARPU × GM / Churn_m
LTV/CAC:                [target ≥ 3x]
Break-even month:       [the month cumulative P&L turns ≥ 0]
```

> **Light mode:** the CPL, conversion and retention inputs are expert estimates (tasks 16 and 17 are skipped). Shade the matching cells in the financial plan yellow and add "hypothesis, needs verification after 3–5 interviews and/or a smoke test".

Hand the parameters over to task 18c.

---
