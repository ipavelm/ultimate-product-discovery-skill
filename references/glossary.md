# Glossary of Product Discovery terms

Read this file before starting the first task, or whenever you hit an unfamiliar term in the other files of the skill. It is short — skim it once and come back for specifics.

## Methodological concepts

| Term | Definition |
|------|------------|
| **JTBD** (Jobs-to-be-Done) | People "hire" products to get a specific job done. The task is to understand that job, not to describe the customer |
| **Job Map** | A map of the 8 stages of the customer's job. For each one: where the pain is and where time or money leaks |
| **Job Story** | The format: "When [situation], I want to [job], so that [outcome]" |
| **OS** (Opportunity Score) | The formula: `OS = Importance + max(Importance − Satisfaction, 0)`. The higher it is, the bigger the opportunity |
| **OST** (Opportunity Solution Tree) | Teresa Torres's tree: business outcome → opportunities → solutions → experiments |
| **BMC** (Business Model Canvas) | The 9-block canvas for a mature business model |
| **Lean Canvas** | The startup adaptation of the BMC: problem, solution, unique value proposition, unfair advantage, key metrics |
| **PAC** (Product Attribute Canvas) | The product's 4 worlds: Customer, Competitor, Distribution, Product |
| **AARRR** | Acquisition → Activation → Retention → Referral → Revenue |
| **RICE** | The prioritisation formula: `(Reach × Impact × Confidence) / Effort` |
| **Value Proposition** | One sentence: "We help [whom] [do what], unlike [competitor], because [unique mechanism]" |
| **Value Chain** | The value creation chain: every link from raw material to the end customer |

## Market metrics

| Term | Definition |
|------|------------|
| **TAM / SAM / SOM** | Total / Serviceable / Obtainable Addressable Market |
| **PMF** (Product-Market Fit) | The product precisely meets a market need. The marker: ≥40% on the Sean Ellis Test |
| **Sean Ellis Test** | The survey question "How would you feel if you could no longer use [product]?". ≥40% answering "very disappointed" is a PMF signal |

## Validation methods

| Term | Definition |
|------|------------|
| **Smoke Test** | A landing page describing the product without the product existing — tests demand |
| **Wizard of Oz** | Automation simulated by hand — tests the value without writing code |
| **Concierge MVP** | You walk through the "job" personally with the customer — for B2B and high tickets |

## Unit economics

| Term | Definition |
|------|------------|
| **CAC** | The cost of acquiring one new customer |
| **CPL** (Cost Per Lead) | The cost of one lead = channel budget / number of leads |
| **LTV** | Total revenue from one customer over a period. Calculated as `LTV = GM × (ticket_new + Σ(ticket_return × Retention_m^t))` for a cohort, or `LTV = ARPU × GM / Churn_m` for subscriptions |
| **ARPU** | Average revenue per user over a period (usually a month or a year) |
| **GMV** | Gross merchandise value transacted through the platform. For marketplaces: Revenue = GMV × take rate |
| **K-factor** | The viral growth coefficient: how many new users one existing user brings. K ≥ 1 → exponential growth |
| **Churn rate** | The share of customers lost over a month |
| **Retention (monthly)** | The share of customers who stay over one month. `Retention_m = 1 − Churn`. Used in the LTV formula |
| **Month-N retention (cohort)** | The share of the month-M1 cohort still active at the start of month N. `Retention_N = Retention_m^(N−1)` when churn is stable. This skill indexes M1 as the first full month after signup — some industry benchmarks index from M0, so check with the source when comparing |
| **Runway** | `Runway = cash remaining / monthly burn rate` (months) |
| **Burn rate** | Monthly spend net of operating income |
