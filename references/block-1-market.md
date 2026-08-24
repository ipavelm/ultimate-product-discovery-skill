## BLOCK I: MARKET ANALYSIS

### Task 1: market analysis

**Goal:** collect market data from open sources.

**Actions:**
- `web_search`: `"market name" market research [current and next year]`, `"industry" statistics report`. Substitute the current year and the next one (for example, if it is 2026, search for "2026 2027").
- Global: Gartner, McKinsey, BCG, Statista, Deloitte, SimilarWeb
- Russia: Rosstat, RBC, Vedomosti, ACRA, Bank of Russia, Data Insight, Nielsen Russia, Sber, Yandex

**Verifying the key numbers:** for every critical figure (market size, CAGR, share of the top players), use `web_fetch` to open the original source and confirm it. Never accept data from a search snippet alone. Record the direct source link in the market card.

**When there is little data on your exact niche** (typical for narrow verticals and new markets): take the neighbouring broad category and estimate the niche's share of it as an assumption. Example: if you are looking for "the market for time trackers for freelancers in Russia" and only find general freelance figures (19M people, $41bn), work out the share: of 19M, say 10% use paid B2C automation tools → 1.9M potential users. State it explicitly: "Initial estimate: X% share of market Y. To be checked through interviews in task 9." That beats both false precision and refusing to estimate at all.

**Output:** the market card — size, dynamics, structure (the "Market" sheet in the financial plan).

**Market type classification** — determine it before moving to task 3, because it changes the methodology in tasks 7 and 16:

| Market type | Signs | Consequences for PD |
|-------------|-------|---------------------|
| **Existing** | Competitors exist, customers know the problem | Focus on differentiation; the Smoke Test works well |
| **Resegmented** | A new niche inside an existing market | JTBD helps find the underserved segment; benchmarks run lower |
| **New** | Customers do not recognise the problem, or the market is only forming | Interviews are critical; the Smoke Test converts badly and that is normal; the horizon is longer. **For a new market, read [customer-development.md](customer-development.md)** — it carries the Steve Blank protocol (Four Steps to the Epiphany) and The Mom Test as the adaptation of the methodology to this case |

Record the market type in the Knowledge Base — it is used when interpreting the results of tasks 3, 7 and 16.

⚠️ **Red flag:** SAM < ₽1bn (Product/Service/Marketplace) or < ₽500M (Hardware) → report it immediately.

---

### Task 2: trend analysis

**Goal:** identify the trends affecting the market.

- A trend is a change in the properties of the market's objects over time
- Types: technological, behavioural, regulatory, demographic, economic

**Format (5 trends minimum):**

| # | Trend | Type | Statistic / source | Consequence for the market | Consequence for the product |
|---|-------|------|--------------------|----------------------------|-----------------------------|

**Output:** the trend table plus a value chain diagram (the "Trends" sheet in the financial plan).

---

### Task 3: competitive landscape

**4 types of competitor:**
1. **Direct** — same need, same method
2. **Indirect** — same need, different method
3. **Displacers** — competing for the budget or the time
4. **Channel-based** — an advantage in distribution or performance marketing

`web_search`: `top competitors [niche]`, `[category] alternatives [current year]`. Sources: G2, Capterra, TAdviser, ProductHunt, TechCrunch, VC.ru.

**Format — feature matrix (5 competitors minimum):**

| Competitor | Type | Positioning | Price | Channels | Market share | Weakness |
|------------|------|-------------|-------|----------|--------------|----------|

**2×2 positioning map (optional but recommended):**

Pick the two most meaningful axes of differentiation for this market (examples: "price — quality", "simplicity — functionality", "speed — reliability", "B2B — B2C reach"). Place every competitor from the feature matrix on those axes. This is what makes the "white space" visible — an unoccupied position where a new product could live.

Output format:
```
X axis: [name, e.g. "Price: low → high"]
Y axis: [name, e.g. "Simplicity → Functionality"]

Positions:
- [Competitor A]: X=low, Y=high functionality → upper-left quadrant
- [Competitor B]: X=high, Y=low → lower-right quadrant
...
White space: [description of the unoccupied position]
```

**Output:** the competitor map plus the feature matrix (the "Competition" sheet in the financial plan).

---

### Task 4: key competitor analysis

**AARRR analysis:** Acquisition, Activation, Retention, Revenue, Referral.

**Also:** funding rounds (Crunchbase), reviews (G2, App Store), failures.

**Format — competitor card:**

```
Competitor:     [Name]
Type:           [Direct / Indirect / etc.]
Acquisition:    [channels, estimated CAC]
Activation:     [onboarding, aha moment]
Retention:      [mechanisms, retention rate if known]
Revenue:        [model, average ticket, ARR if known]
Referral:       [programmes, NPS if known]
Weaknesses:     [from user reviews]
Funding:        [rounds, amounts]
Key takeaway:   [the main advantage or vulnerability]
```

**Output:** competitor cards (the "Competition" sheet in the financial plan).

---

### Task 5: TAM / SAM / SOM

- **TAM** = number of customers × frequency × average ticket
- **SAM** = the share of TAM once competitors and geography are accounted for
- **SOM** = what resources allow over a 1–3 year horizon

Calculate it in money (₽/year) **and** in number of buyers.

**Verify SAM with both methods (mandatory):**

| Method | Formula | When to use |
|--------|---------|-------------|
| **Top-down** | TAM × share of the accessible segment (%) | Always |
| **Bottom-up** | Number of accessible customers × average ticket × frequency | Always |

If the two results differ by **more than 3x**, recalculate the assumptions. The exact test: `max(Top-down, Bottom-up) / min(Top-down, Bottom-up) > 3`. Example: top-down = ₽10bn, bottom-up = ₽35bn → 35/10 = 3.5x → the divergence is critical, recalculate. At ₽10bn vs ₽25bn (2.5x) it is acceptable, but state both values and explain which one you trust more.

**Proxy market for products with a hardware dependency.** If the product requires the end user to own a specific device (VR headset, AR glasses, IoT controller, a specialised sensor, a premium smartphone for AR features and so on), the real SAM is **not the whole target audience but the intersection of that audience with owners of the required device**. Examples:

| Product | Overall TAM | Proxy constraint | Real SAM |
|---------|-------------|------------------|----------|
| VR platform for Russian schoolchildren | ~15M schoolchildren | ~1% of families own a VR headset (~150k) | Calculate from 150k, not 15M |
| AI assistant for AirPods Pro | Every smartphone owner | AirPods Pro / Pro 2 only | From the number of AirPods Pro |
| IoT app for Tesla | Every car owner | Tesla owners only | From the number of Teslas on the market |

Action: if the product carries a hardware dependency, ask the person outright "What equipment does the end user need to own?" and size SAM through the intersection. If that intersection is < 10% of the overall TAM and the equipment is expensive (> ₽30k), that is a risk in its own right — record it in task 15 as a hypothesis: "The audience owning the required equipment is large enough for the target SAM".

**Data confidence indicator** — assign a confidence level to every key figure:

| Level | When to use | Marker |
|-------|-------------|--------|
| 🟢 High | Data from a primary source (a McKinsey report, Rosstat, an SEC filing), verified through `web_fetch` | ✓ |
| 🟡 Medium | Data from aggregators (Statista, SimilarWeb), analyst estimates, forums | ~ |
| 🔴 Low | Expert guesses, bottom-up calculations with no confirmed inputs | ? |

Apply this indicator to every key number in every task: TAM/SAM/SOM, average ticket, conversions, retention. In the financial plan, shade cells holding 🔴 data yellow — those are the risk points that need checking.

**Output:** the TAM/SAM/SOM table with confidence indicators (the "Market" and "Assumptions" sheets in the financial plan).

⚠️ **Red flag:** SAM < ₽1bn (Product/Service/Marketplace) or < ₽500M (Hardware) → report it immediately.

---

### Task 6: PESTEL analysis

For each factor: Significance (1–3) × Probability of change (1–5).

| Category | Factor | Significance | Probability | Score | Threat / Opportunity |
|----------|--------|--------------|-------------|-------|----------------------|

**Output:** the PESTEL table (the "PESTEL" sheet in the financial plan).

**Risk adjustment into the financial plan:** once the table is filled in, pick the top 3 threats by score (Significance × Probability). For each, describe the scenario's effect on the P&L:

| Threat (from PESTEL) | Probability of occurring | Effect on revenue / costs | Break-even shift (months) |
|----------------------|--------------------------|---------------------------|---------------------------|
| [Threat 1] | High / Medium | −X% GMV or +Y% OPEX | +N months |

Add these rows to the "Scenarios" sheet of the financial plan as "Stress scenario: [threat name]". That is what turns PESTEL from an academic exercise into a practical instrument for investors.

---

