# Worked examples of canvases and diagrams

This module holds realistic, filled-in examples for the Lean Canvas, BMC, PAC, OST and Job Map. Use them as a reference so the agent does not produce shallow templates.

**The illustrative project used across every canvas:** "TimeTag" — a Telegram bot that automatically tracks freelancers' time by project. B2C SaaS, ₽490/month subscription, segment: IT freelancers in Russia.

---

## Example 1: Lean Canvas (idea / MVP stage)

| Block | Content |
|-------|---------|
| **Problem** | 1. Freelancers under-report hours by 15–20% when tracking manually in Excel<br>2. They forget to switch the timer between projects — no accurate data to invoice from<br>3. They spend 2–4 hours a week reconstructing time records from memory |
| **Segments** | Early adopters: IT freelancers with 3+ concurrent projects, earning ₽150–500k/month, active Telegram users |
| **Unique value proposition** | "Automatic tracking inside Telegram with no context switching — it logs time from commands in the client's working chats" |
| **Solution** | 1. The bot listens for `/start`, `/stop`, `/switch [project]` in direct messages<br>2. Automatic context recognition from forwarded messages out of client chats<br>3. A weekly report that exports to CSV for invoicing |
| **Channels** | Telegram channels for freelancers (4–6 of them, ~50k subscribers), habr.com and vc.ru guest posts, a referral programme |
| **Revenue streams** | Freemium: 2 projects free, unlimited for ₽490/month or ₽4,900/year |
| **Cost structure** | Hosting (₽3k/month), MVP development (₽200k one-off), marketing (₽20k/month), payment infrastructure (2.5% of GMV) |
| **Key metrics** | DAU/MAU ≥ 40%, Free→Paid conversion ≥ 5%, month-1 retention ≥ 60%, CAC ≤ ₽800 |
| **Unfair advantage** | Integration with client Telegram chats through a webhook — competitors work only inside a separate app, which is the very source of the "forgot to switch" problem |

---

## Example 2: Business Model Canvas (has customers / revenue)

| Block | Content |
|-------|---------|
| **Customer Segments** | 1. Solo IT freelancers (500 customers, 70% of revenue)<br>2. Small agencies of 3–10 people (120 customers, 25% of revenue)<br>3. Accountant-consultants (20 customers, 5% — they use it to track billable hours for their own clients) |
| **Value Propositions** | For solos: 3 hours a week saved plus a 15% income increase from accurate tracking.<br>For agencies: visibility into team load plus automatic project profitability analytics.<br>For accountants: export in a 1C-compatible format. |
| **Customer Relationships** | Acquisition: content marketing, affiliates.<br>Activation: a 3-step onboarding bot; the aha moment is the first automatic report at the end of the week.<br>Retention: a weekly digest and triggered messages when activity drops.<br>Revenue: freemium → paid, prompted by hitting the 2-project limit.<br>Referral: a free month for every referred paying customer. |
| **Channels** | Awareness: Telegram channels, Habr, vc.ru.<br>Evaluation: the free tier (2 projects).<br>Sales: in-app upgrade.<br>Delivery: Telegram (WebApp).<br>After-sales: bot support plus a chat with the founder for the first 30 days. |
| **Key Activities** | Building and running the bot, content marketing, partner integrations, first-line support — done personally by the founder for the first 6 months |
| **Key Resources** | The codebase (Python + Telegram Bot API + PostgreSQL), a base of 640 users, a content library (48 publications), the "TimeTag" brand in Russian-language Telegram |
| **Key Partners** | The payment provider (YooKassa), cloud hosting (Selectel), 3 Telegram channels with an exclusive promo code |
| **Revenue Streams** | Subscription (94% of revenue): ₽490/month, ₽4,900/year<br>White-label for agencies (6%): ₽15k/month for a team of up to 20 |
| **Cost Structure** | Fixed: payroll ₽250k (1 full-stack engineer + 0.5 marketer), hosting ₽8k, tooling ₽15k.<br>Variable: payment processing 2.5% of GMV, advertising ₽50–80k/month (varies with the plan) |

---

## Example 3: Product Attribute Canvas (PAC) — the 4 worlds

### Customer World
- **Segments:** solo IT freelancers (primary), agencies of 3–10 people (growing)
- **Jobs (top 3 by OS):**
  - "When I close out the week, I want to know the exact hours per client, so that I can invoice correctly" (OS = 16)
  - "When I work on several projects at once, I want to not forget to switch the timer, so that I do not lose 15–20% of my time" (OS = 14)
  - "When a client asks for the monthly report, I want to export it in 30 seconds, so that I do not spend an hour assembling it in Excel" (OS = 12)
- **Value Propositions:**
  - "Automatic tracking with no app switching" → covers jobs 1 and 2
  - "One-click report" → covers job 3

### Competitor World
- **Direct:** Toggl (global), Kaiten (Russia) — separate apps that require manual switching
- **Indirect:** Excel + Google Calendar — "it works, but it hurts"
- **Differentiation:** the integration lives in Telegram, where the freelancer already talks to the client. No competitor has tracking built into the client's messenger.
- **Where we lose:** deep per-project analytics (Toggl), team features (Harvest). Deliberately out of focus — the audience is solo.

### Distribution World
- **Aha moment:** the first automatic weekly report — "wow, I did not realise I spent 14 hours on Client X"
- **Activation:** 3-step onboarding — connect → create 2 projects → receive a report after 7 days
- **Growth loop:** the freelancer forwards the report to the client to justify the invoice → the client sees the TimeTag brand → invites it into another project of theirs → signs up as a new user. Target K-factor ≥ 0.3.

### Product World
- **Features mapped to Job Stories:**
  - Automatic tracking from keywords in the chat → job 2
  - Automatic weekly report → jobs 1 and 3
  - CSV / 1C export → job 3
- **Unique properties:** it works without installing an app (the client is Telegram itself), data syncs across devices through the Telegram account, encryption at chat level.

---

## Example 4: Opportunity Solution Tree (OST)

```
BUSINESS OUTCOME:
Month-3 retention (cohort) 35% → 50% within 6 months
(we currently lose half our customers in 3 months — critical for LTV)

├── OPPORTUNITY 1: strengthen the aha moment in week 1 (OS = 16)
│   ├── Sub-opportunity 1.1: shorten time-to-first-report
│   │   ├── Solution A: generate the first report after 3 days, not 7
│   │   │   └── Experiment A1: A/B test on 200 new users — 7 days vs 3 days
│   │   │       Criterion: week-2 retention higher by ≥10%
│   │   └── Solution B: interactive onboarding with an instant mini-report
│   │       └── Experiment B1: Wizard of Oz — show a prepared report after the
│   │           first 3 tracked sessions (50 users, 1 week)
│   │           Criterion: ≥70% finish the onboarding
│   └── Sub-opportunity 1.2: show the value in money
│       └── Solution C: state in the report "you saved X hours = ₽Y"
│           (calculated from the hourly rate the user entered)
│           └── Experiment C1: ship the feature to 50% of users and measure the
│               difference in Free→Paid conversion after 14 days
│               Criterion: conversion higher by ≥20%
│
├── OPPORTUNITY 2: reduce the friction of switching (OS = 14)
│   ├── Sub-opportunity 2.1: automatic context detection
│   │   ├── Solution D: an ML classifier that assigns projects from message text
│   │   │   └── Experiment D1: label 500 messages by hand, train a baseline and
│   │   │       measure accuracy on a holdout — target ≥85%
│   │   └── Solution E: quick-switch buttons on a pinned bot message
│   │       └── Experiment E1: roll out to 100 users and measure the share of manual
│   │           switches made through buttons vs commands — target 70% via buttons
│
└── OPPORTUNITY 3: bring in social pressure (OS = 11)
    └── Sub-opportunity 3.1: comparison with similar freelancers
        └── Solution F: anonymous statistics — "you are in the top 30% for tracking accuracy"
            └── Experiment F1: show it to 50 users and measure week-4 retention
                against a control group. Criterion: +15% month-1 retention
```

**Key rules when building an OST:**
- The business outcome is always measurable (metric + current value → target + deadline)
- At least 3 opportunities at the top level — this prevents tunnel vision
- At least 2 solutions per opportunity — this prevents confirmation bias
- Every experiment needs a clear confirm/refute criterion with a number in it
- Prioritise by the OS from task 7 — start with the opportunity carrying the highest OS

---

## Example 5: Job Map — the 8 stages

An example for TimeTag. The most painful stages are highlighted.

| Stage | Freelancer's action | Pain / cost |
|-------|---------------------|-------------|
| 1. Define | Allocate the week across 3–5 projects | No objective baseline — it is done by feel, off by ±30% |
| 2. Locate | Find a tracking tool | Tried 3 apps, abandoned them all because of the context switching |
| 3. Prepare | Set the projects up in the tracker | 15 minutes per new client — configuration, imports, integrations |
| 4. Confirm | Check that everything works | Constant checking — "did I remember to start it?" |
| **5. Execute** ⚠️ | **Work and switch between tasks** | **Forgets to start or stop it 40% of the time — loses 2–4 hours a week** |
| 6. Monitor | Check the hours so far | Opens the tracker 5–10 times a day — friction |
| **7. Modify** ⚠️ | **Reconstruct the forgotten sessions from memory** | **2 hours a week reconstructing — inaccurate and stressful** |
| **8. Conclude** ⚠️ | **Invoice the client** | **Under-reports by 15–20% out of doubt about the records → −₽30k/month** |

**Conclusion:** the main pains sit at stages 5, 7 and 8 — that is where the solutions in the PAC Product World should point.

---

## How to use these examples

1. **Do not copy them verbatim** — adapt them to the user's project.
2. **Keep the level of detail** — where the example gives numbers and specifics, give the same. Filling a canvas with generalities is not filling a canvas.
3. **Keep it coherent** — one project runs through every canvas. Job 2 in the PAC has to reflect the pain of stage 5 in the Job Map.
4. **Check the logic** — if the Lean Canvas says the unfair advantage is the Telegram integration, the PAC's Distribution world must show a growth loop through Telegram, not through Google Ads.
