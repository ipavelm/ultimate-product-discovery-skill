# Survey templates for `ask_user_input_v0`

Ready-made JSON objects for Step 0. Do not rebuild the question structure from scratch — take it from here and adapt it to the specific project if needed.

Grouping: each `ask_user_input_v0` call carries up to 3 related questions, so the person answers in a flow rather than through 16 separate taps. Open questions with no fixed options (project name, description, competitors, budget, investment) should be asked as plain text — `ask_user_input_v0` is overkill for those.

## First call: market + audience type + stage

```
ask_user_input_v0(questions=[
  {
    "question": "Which market is the project in (country/region)?",
    "type": "single_select",
    "options": ["Russia", "CIS", "EU/UK", "USA", "Global", "Other"]
  },
  {
    "question": "B2B or B2C?",
    "type": "single_select",
    "options": ["B2C", "B2B SMB", "B2B Enterprise", "B2B2C"]
  },
  {
    "question": "What stage is the project at?",
    "type": "single_select",
    "options": ["Idea (no MVP yet)", "MVP ready, no customers", "First customers", "Has revenue"]
  }
])
```

## Second call: business type + horizon + market type

Ask this after the person has described what the product does — otherwise the business type is hard to pick.

```
ask_user_input_v0(questions=[
  {
    "question": "Business type?",
    "type": "single_select",
    "options": [
      "Product (SaaS, app, physical good with installation)",
      "Service / consulting (selling time and expertise)",
      "Marketplace (two-sided platform)",
      "Hardware (physical device with a production cycle)"
    ]
  },
  {
    "question": "Financial planning horizon?",
    "type": "single_select",
    "options": ["12 months", "24 months"]
  },
  {
    "question": "Market type (if you know it)?",
    "type": "single_select",
    "options": [
      "Existing (competitors exist, customers know the problem)",
      "Resegmented (a new niche inside an existing market)",
      "New (customers do not recognise the problem yet)",
      "Not sure — let's determine it in task 1"
    ]
  }
])
```

## Third call (only if the stage is not idea): customers + CRM data

Skip it at the idea stage — that data does not exist yet.

```
ask_user_input_v0(questions=[
  {
    "question": "Do you have first customers or sales?",
    "type": "single_select",
    "options": ["No", "Yes, up to 10", "Yes, 10–50", "Yes, 50–200", "Yes, more than 200"]
  },
  {
    "question": "Is there CRM or analytics data you can attach to the PD?",
    "type": "single_select",
    "options": [
      "Yes, I will attach a file (CSV/Excel)",
      "There is, but I would rather not share it — use expert estimates",
      "No, it is all in my head"
    ]
  },
  {
    "question": "Has PD been run on this project before?",
    "type": "single_select",
    "options": [
      "Yes, I will attach the previous financial plan (.xlsx)",
      "Yes, but the file is gone — let's start fresh",
      "No, this is the first time"
    ]
  }
])
```

**A note on marketplaces:** if the user gives customer count as a single number ("800 active users"), always follow up in free form: "Is that both sides combined (suppliers + buyers) or each side separately?". Marketplace liquidity is judged on the **smaller** side — 800 combined with a 700/100 skew means liquidity of 100, which is already below the investment tracker's threshold of ≥ 20 per side.

## Fourth call: mode selection + round stage (if relevant)

Ask this once the rest is collected — from the stage and goals you can propose a suitable mode yourself.

```
ask_user_input_v0(questions=[
  {
    "question": "Which mode should the PD run in?",
    "type": "single_select",
    "options": [
      "Light (~45 minutes) — a quick check of the idea",
      "Full (~2–3 hours) — full analysis for an investor"
    ]
  },
  {
    "question": "Which investment round are you planning (if any)?",
    "type": "single_select",
    "options": [
      "Pre-seed / seed (angel or early-stage fund)",
      "Series A",
      "Series B or later",
      "Not raising — bootstrapping",
      "Do not know yet"
    ]
  }
])
```

The round stage changes the investment-tracker thresholds in the final summary. If the person picks "Pre-seed/seed" or "Do not know", the skill uses the default early-stage thresholds. For Series A the thresholds are qualitatively different: ARR ≥ $1M, growth ≥ 10% MoM, NRR ≥ 110%, payback ≤ 12 months. See the "Investment readiness tracker" section in SKILL.md for detail.

## Free-form questions (not through `ask_user_input_v0`)

Ask these as plain text — they have no closed list of answers:

1. Project name?
2. What does the product do? What problem does it solve? (2–3 sentences)
3. Main target segments? (who the customer is)
4. 2–3 main competitors (names)
5. Business model: subscription / commission / one-off sale / freemium / other?
6. Budget for testing hypotheses, ₽ (used in task 16)
7. Investment (amount in ₽, or "none")

## Example of the overall flow

1. Read the project description from the user (in their first message).
2. Make the first `ask_user_input_v0` call (market + B2B/B2C + stage).
3. If the first message carried no description, ask in free form: name, what it does, competitors.
4. Make the second `ask_user_input_v0` call (business type + horizon + market type).
5. If the stage is not idea, make the third `ask_user_input_v0` call (customers + CRM + previous PD).
6. Ask in free form: budget, investment.
7. Propose a mode from what you collected (idea → Light; MVP + customers + seed → Full) and make the fourth `ask_user_input_v0` call.
8. Run the pre-flight check, initialise the KB, confirm the plan with the person.

That is **4 `ask_user_input_v0` calls** plus a handful of free-form questions instead of 16 separate ones. The user answers quickly and does not get worn down.

## Final step: pin the mode into the environment

Once the user has chosen Light or Full, you MUST set the environment variable:

```bash
export PD_MODE=light   # or full
echo "PD_MODE=$PD_MODE"
```

This guards against two failure scenarios:

1. **`delete_light_slides.py` in Full mode** — run by mistake, it deletes 13 slides you need (trends, PESTEL, CJM, alternative scenario, PMF). The script checks `PD_MODE` and refuses to run when the mode does not match.
2. **Running with no explicit mode** — the scripts refuse to run at all and demand that `PD_MODE` be set.

Verify it: `scripts/preflight_check.sh` prints the current value of `PD_MODE`.
