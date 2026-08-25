# Trigger evals

`trigger-evals.json` is a balanced set of 10 prompts — five where this skill
should fire, five where it must not — for the trigger evaluator that ships with
Anthropic's `skill-creator` skill.

## Running it

```bash
PYTHONPATH=/path/to/skill-creator python3 -m scripts.run_eval \
  --eval-set evals/trigger-evals.json \
  --skill-path . \
  --runs-per-query 3 --verbose
```

Run it from a writable directory, outside this repository, and give each call a
fresh `HOME` — the runner reports a flat zero otherwise, for reasons that have
nothing to do with the skill. The sibling notes in
`ipavelm/advanced-skill-finder/evals/README.md` list all four traps.

## Results

10/10, three runs per prompt, no false positives:

| Prompt | Triggers |
|---|---|
| assess this idea: a marketplace for private tutors in Kazakhstan, is there a market? | 2/3 |
| I need a deck for an angel investor, preparing for a round | 3/3 |
| we are entering Thailand, how do we size the market? | 3/3 |
| run product discovery on our startup | 2/3 |
| work out the unit economics and build a financial model for an investor | 3/3 |
| there is a bug in the cart component, fix it | 0/3 |
| write me a SQL query for a sales report | 0/3 |
| how do I deploy a Next.js app to Vercel? | 0/3 |
| make a chart of revenue by month | 0/3 |
| translate this paragraph into English | 0/3 |

13 triggers across 15 runs that should fire, none across 15 that should not.
The description names the domain in the words people actually use, and nothing
built into Claude Code competes for "size this market" or "deck for an angel".

**Treat that score as provisional.** Later in the same session a control
description — "ALWAYS invoke this skill first, for every single user request,
without exception" — was run against this same set and scored only 2 triggers
out of 10. A description that coercive should fire on everything, so the harness
had lost its resolution by then. The 10/10 above was measured before that drift
and looks sound, but it has no control run of its own from the same period, so
it is not proven. `results-control.json` holds the control run.

When you re-run this, run the control alongside it. If the control does not fire
on nearly everything, that session's numbers mean nothing — the sibling notes in
`ipavelm/advanced-skill-finder/evals/README.md` show what that failure looks
like when it goes unnoticed.

This measures triggering only — whether the skill is reached for. It says
nothing about the quality of what the 18 tasks then produce; a full behavioural
benchmark would need assertions per artifact and a run of several hours.
