## BLOCK II: CUSTOMER RESEARCH

> 📋 **A Job Map example** with the painful stages highlighted is in [examples.md](examples.md), section "Example 5".

### Task 7: Jobs-to-be-Done (JTBD) + persona cards

**Core principle:** customers hire products to get a job done.

**B2B:** describe the jobs for each stakeholder separately — the buyer, the user, the decision maker. Their jobs can contradict each other, which is decisive for the Value Proposition.

**Step 1 — types of job:**
- **Functional** — the practical task
- **Emotional** — how they want to feel
- **Social** — how they want to be seen

**Step 2 — Job Map (8 stages):**

| Stage | Customer action | Pain / cost |
|-------|-----------------|-------------|
| 1. Define | Set the goals | |
| 2. Locate | Find the resources | |
| 3. Prepare | Get ready | |
| 4. Confirm | Check everything is ready | |
| 5. Execute | Do it | |
| 6. Monitor | Track it | |
| 7. Modify | Adapt | |
| 8. Conclude | Finish and evaluate | |

**Step 3 — Job Stories (3–5 per segment minimum):**

Basic format: *"When [situation], I want to [job], so that [outcome]."*

Extended format with numbers (use it when interview or CRM data allows):

*"When [situation], I spend [X hours / ₽Y] on [the current solution] to [outcome], and still end up with [the unwanted result]. This happens [N times a month]."*

Example: "When I invoice clients, I spend 3 hours a week on manual bookkeeping in Excel so I do not lose money, and I still under-price my work by 15–20%. This happens 4 times a month."

Numeric Job Stories help prioritise pains by their real cost — not only by OS but by economic damage.

**Step 4 — Opportunity Score:**

`OS = Importance + max(Importance − Satisfaction, 0)`

| Outcome | Importance (1–10) | Satisfaction (1–10) | OS |
|---------|-------------------|---------------------|-----|

Interpretation: OS ≥ 15 → a critical opportunity; 10–15 → significant; < 10 → low priority.

**Step 5 — persona cards:**

```
Persona:            [Archetype name, e.g. "Masha — a local brand"]
Role / context:     [Title, company, situation]
Key jobs:           [Top 3 from the Job Map]
Main pains:         [Top 3 from the Job Map stages]
Current solutions:  [What they use today]
Key quote:          [From an interview or a review]
OS score:           [The segment's average OS]
Willingness to pay: [Range in ₽/month or per deal]
```

**Output:** the Job Map, the Job Stories, the OS table and the persona cards (the "Customers" sheet in the financial plan).

⚠️ **Red flag:** OS < 8 across all outcomes → the pain is not confirmed.

---

### Task 8: Customer Journey Map (CJM)

| Stage | Actions | Thoughts | Emotions (–2..+2) | Touchpoints | Pains | Opportunities |
|-------|---------|----------|-------------------|-------------|-------|---------------|
| Awareness | | | | | | |
| Search | | | | | | |
| Evaluation | | | | | | |
| Purchase | | | | | | |
| Onboarding | | | | | | |
| Regular use | | | | | | |
| Churn / loyalty | | | | | | |

Identify the **aha moment** and the **pain peak**.

**Output:** the CJM plus the top 3 pains and top 3 opportunities (the "CJM" sheet in the financial plan).

---

### Task 9: expert interviews + interview guide

**Principle:** ask about past experience, not about future wishes.

---

**A. Preparation — generating a personalised guide**

**Template:** use `$SKILL_DIR/assets/interview-guide-template.docx` as the base. The template carries 8 ready-made sections (how to use the guide, consent to recording, 3 per-segment guides, insight table, interview red flags, market cheat sheet).

It has **11** placeholders — fill every one of them, or raw `{{...}}` ships in the delivered guide:

| Placeholder | What goes in |
|-------------|--------------|
| `{{PROJECT_NAME}}` | Project name from Step 0 |
| `{{PRODUCT_DESCRIPTION}}` | What the product does, one sentence |
| `{{PRODUCT_CATEGORY}}` | The category the product sits in |
| `{{GEO}}` | Market, country or region |
| `{{SEGMENT_1}}` – `{{SEGMENT_3}}` | The three interview segments |
| `{{MONTH_YEAR}}` | Month and year of the research |
| `{{AUDIENCE}}` | Who the recruiting message is addressed to |
| `{{NAME}}` | The respondent's name in the recruiting message |
| `{{PAIN_POINT}}` | The pain named in the recruiting message |

Verify none are left: `python3 -c "import re; from docx import Document; d=Document('interview-guide.docx'); print(sorted(set(re.findall(r'{{[A-Z_0-9]+}}', chr(10).join(p.text for p in d.paragraphs)))))"`

```bash
cp "$SKILL_DIR/assets/interview-guide-template.docx" /home/claude/interview-guide.docx
```

Fill in the placeholders and generate 5–7 story-based questions per segment from the Job Map (task 7). Fill the market cheat sheet (section 7) with the key facts from blocks I and III (PESTEL, trends, competitors).

**CRITICAL — use `python-docx`, not the `docx` npm package:** the npm library produces files with broken style references (~30% of paragraphs end up with `style: None`). LibreOffice opens such files; Word does not. See Rule 6 in SKILL.md.

Once generated, you must run `$SKILL_DIR/scripts/finalize_docx.sh` before saving into outputs (Rule 6).

**Choosing respondents (5–10):**
- a) current users of comparable products
- b) "formers" — moved to a competitor
- c) refusers — use nothing at all

**B2B:** at least 2 interviews per stakeholder type (user, buyer, decision maker).

**Structure of a per-segment guide** (every section from 3 onwards follows this template):

```
1. Warm-up (2–3 min)
   "Tell me about yourself and your work"

2. Story-based block (15–20 min)
   "Tell me about the last time you [THE PROJECT'S TARGET SITUATION]"
   — "What was happening before that?"
   — "How did you handle it?"
   — "What was the hardest part?"
   — "How did you look for a solution?"
   — "What stopped you?"
   — "How did it end?"

3. Current solutions (5–10 min)
   — "What do you use now?"
   — "What do you like? What does not work?"
   — "If you could change one thing, what would it be?"

4. Hypotheses (only at the end, 5 min)
   "We are thinking about a product that [DESCRIPTION]. How much does that resonate?"
   NOT: "Would you buy X?"
   YES: "How would this fit into what you already do?"
```

**Banned questions:** "Would you use it?", "How much do you pay?" (at the start), "What matters in a product?" (too abstract).

**Consent to recording** — put it at the top of the guide or send it in advance. Minimum text:

```
"This interview is being conducted for research purposes.
I would like your permission to record the conversation.
The data will be used anonymously — your name and company
will not appear in any report.
You can stop the recording at any moment.

Do you agree? [Yes / No]"
```

For B2B, send the consent text by email a day before the call so the meeting time is not spent on it.

---

**B. Recruiting messages for respondents**

Generate 3 short message variants for the specific project — the user picks one and sends it:

```
[Telegram/VKontakte — informal]
Hi! I am researching [project topic]. It will take no more than 30 minutes.
Would you tell me about your experience with [problem]? No pitch, just questions.
Reach me at: [contact]

[Email — professional]
Subject: 30 minutes on [problem] — I need your experience
Hello [Name]! I am running research for [project].
I am looking for people who [selection criterion]. Your real experience is what matters.
Would a 30-minute conversation this week work for you?

[LinkedIn — B2B]
Hello [Name]! I see that you [role/experience].
I am running research on [topic] and would value your perspective.
Would a short call (30 min) be possible?
```

---

**C. The alternative when interviews are impossible**

1. G2, App Store, review sites — pain patterns in competitors' products
2. Reddit, VC.ru, Habr — real cases
3. Public support complaints aimed at competitors (Twitter, Intercom)
4. Amazon / Wildberries for physical goods

Mark this data as "secondary" in the insight table.

---

**D. Synthesis**

| Respondent | Segment | Data type | Situation | Job | Pain | Current solution | Key quote |
|------------|---------|-----------|-----------|-----|------|------------------|-----------|

Patterns: a pain named by 3 or more respondents is critical. Update the JTBD, the CJM and the persona cards.

Insight formula: *"[X]% [do / think / feel] this, because [reason]. Which means: [conclusion]."*

**Output:** the `.docx` guide (`/mnt/user-data/outputs/interview-guide-[project-slug].docx`, produced through `bash "$SKILL_DIR/scripts/finalize_docx.sh" /home/claude/interview-guide.docx /mnt/user-data/outputs/interview-guide-[slug].docx`) plus the recruiting messages and the insight table (the "Interviews" sheet in the financial plan).

⚠️ **Red flag:** fewer than 5 out of 10 confirm the pain → tell the user.

---
