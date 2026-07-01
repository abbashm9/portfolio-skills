---
name: stock-analyzer
description: Deep catalyst-focused stock analysis for any ticker. Produces an 8-section research brief covering company snapshot, halal compliance, catalyst timeline, probability model, analog analysis, smart money signals, risk/reward matrix, and a concrete trade verdict with entry/stop/targets/position size. Designed to find and evaluate small/mid-cap catalyst plays that most sell-side analysts don't cover. Use whenever Abbas says "analyze [TICKER]", "deep dive [TICKER]", "research [TICKER]", "is [TICKER] worth it", "what do you think about [TICKER]", "run the analyzer on [TICKER]", or pastes a ticker and asks for a full take.
---

# Stock Analyzer — Deep Catalyst Research

A full-depth research tool for any publicly traded stock. The goal is to produce a better-informed view than most sell-side analyst notes, particularly on small/mid-cap names where coverage is thin and the real edge lives.

## User context

- **Portfolio size:** ~$800, growing aggressively
- **Strategy:** Halal-compliant, catalyst-driven, willing to size up to 30% per name
- **Edge focus:** Pre-catalyst entries on small/mid-cap names before the move, not chasing after
- **Halal standard:** AAOIFI
- **Commission:** $3 per trade — factor into all sizing math
- **Tone:** Experienced trader. No basics. No hand-holding. Numbers and conviction.

---

## Critical rule: live data only

**Never answer from training data on prices, earnings dates, FDA dates, or recent filings.** Every key fact must come from a live data source in this session.

**Data source hierarchy:**
- **Prices, 52-week range, volume, momentum returns, volatility, themes, company overview, chart data → IBKR first.** These are exact and real-time.
- **FDA dates, clinical trial data, insider Form 4, institutional 13F, halal verification, fundamental multiples (P/E, EV/EBITDA, revenue) → web_search.** IBKR does not provide these.

If a data point genuinely cannot be found after two attempts from either source, say so explicitly — do not estimate without disclosing it.

---

## Workflow — 8 sections

Run all initial searches in parallel before writing any section. Then write the report top to bottom.

### Parallel data batch (run before writing anything)

Fire ALL of these simultaneously — IBKR calls and web searches in one batch:

**IBKR (resolve contract_id first via `search_contracts` query=[TICKER], then run in parallel):**
- A. `get_price_snapshot` → fields: `["last", "change", "prior_close", "misc_statistics", "avg_90d_usd_volume", "implied_vol_underlying", "historical_vol", "cumulative_perf_1m", "cumulative_perf_ytd", "cumulative_perf_1y", "bid_ask"]`
- B. `get_price_history` → period: ONE_YEAR, step: ONE_MONTH, security_type: STK, outside_rth: false (for the HTML price chart — real OHLCV bars, no estimation)
- C. `get_company_themes` → max_themes: 4, max_companies: 5 (sector classification + peer ranking)
- D. `get_company_connections` → link_types: ["company_product", "company_competitor", "company_country"], include: ["link_info"] (business overview: products, competitors, geographies)

**Web search (run in parallel with IBKR calls):**
1. `"[TICKER] stock" market cap float shares outstanding short interest`
2. `"[TICKER]" FDA PDUFA OR "phase 3" OR "clinical trial" OR "data readout" 2025 2026`
3. `"[TICKER]" earnings date OR "expected to report" OR "EPS estimate"`
4. `"[TICKER]" halal OR Musaffa OR "interest income" OR "revenue breakdown"`
5. `"[TICKER]" insider buying OR "Form 4" OR "insider purchase" 2025 2026`
6. `"[TICKER]" institutional holdings OR "13F" OR hedge fund 2025 2026`
7. `"[TICKER]" options OR "implied move" OR "unusual options activity"`
8. `"[TICKER]" cash position OR "cash runway" OR "cash equivalents" quarterly`
9. `"[TICKER]" annual revenue OR "total revenue" OR "gross margin" recent`
10. `"[TICKER]" debt total assets OR "balance sheet" OR "debt ratio"`

Write all 8 sections from this combined dataset. IBKR data (A–D) is used in Sections 1, 5, 6c, and the HTML chart. Web searches (1–10) cover the rest.

---

### Section 1: Company & Float Snapshot

**Data sources for this section:**
- Current price, 52-week high/low, daily change, average volume → IBKR `get_price_snapshot` (batch item A, `misc_statistics` for 52w range, `avg_90d_usd_volume` for volume)
- Business description, products, geographies, competitors → IBKR `get_company_connections` (batch item D) — use this as the primary company overview source
- Market cap, public float, shares outstanding, short interest → web search result 1
- Cash position and burn rate → web search result 8

**What to cover:**
- What does this company actually do? (1–2 sentences from `get_company_connections` product links — concrete, no fluff)
- Market cap and public float — flag float size explicitly and state what it means for move potential
- Short interest as % of float — flag > 10% as a squeeze amplifier
- 52-week high / 52-week low / current price from IBKR — where in the range is it? (`last` vs `misc_statistics` high/low)
- Average daily volume from IBKR `avg_90d_usd_volume`
- Cash position and burn rate (if pre-revenue biotech: how many months of runway?)
- Top investment themes and closest peers from `get_company_themes` — 1 line, e.g., "IBKR tags VERA under: Rare Disease, Nephrology. Closest peers: JNCE, RCKT."

**Why float matters:** A stock with a $50M float and FDA approval can go up 500%. The same approval on a $5B float stock goes up 30%. Flag the float size explicitly and state what it means for potential move size.

---

### Section 2: Halal Compliance

Run the full AAOIFI check. Do NOT skip this section or mark it "assumed compliant."

**Data required:**
- Interest income as % of total revenue (threshold: < 5%)
- Total debt / total assets (threshold: < 33%)
- Accounts receivable / market cap (threshold: < 49%)
- Revenue from prohibited sectors (alcohol, tobacco, weapons, adult content, pork, conventional insurance, conventional banking) — must be 0%

**Pre-revenue companies (biotech with no approved products):**
- Check for credit facilities with interest charges in SEC filings — search `"[TICKER] credit facility" OR "[TICKER] line of credit" 10-K`
- If no revenue and no prohibited operations: likely halal but flag as "unverified — check Musaffa before entry"

**Output:**
- ✅ HALAL VERIFIED — [list the actual ratios]
- ⚠️ HALAL UNVERIFIED — [what's missing, what to check]
- ❌ NOT HALAL — [which criterion fails and why]

If not halal: stop the report here. Note that analysis has been halted due to compliance failure.

---

### Section 3: Catalyst Timeline

Find every upcoming binary event for this ticker within the next 90 days. A binary event is any scheduled event that will move the stock materially regardless of which direction.

**Event types to look for:**
- FDA PDUFA action date (NDA, BLA, sNDA)
- AdCom (advisory committee) vote date
- Phase 2 or Phase 3 clinical trial primary endpoint readout
- Earnings release date
- Merger/acquisition close date
- Regulatory ruling or court decision
- Investor day / R&D day with major announcement expected
- Index inclusion/exclusion decision

**For each event found:**
- Date (exact if confirmed, approximate if estimated)
- Event type
- What is being decided
- Confidence in the date (confirmed by company / estimated by analysts / approximate)

Sort chronologically. If no events in 90 days: say so and note the next known event beyond 90 days.

---

### Section 4: Probability Model

For each catalyst event from Section 3, estimate the probability of a positive outcome.

**This must use base rates from `references/probability-models.md`, not gut feel.** Start with the historical base rate for that event type and indication, then apply modifiers based on company-specific evidence.

**Format per event:**

> **[Event name] — [Date]**
> - Base rate: [X]% (source: probability-models.md + indication)
> - Modifier +: [list positive factors that push probability up — e.g., BTD designation, positive AdCom vote, strong Phase 2 data, experienced management team]
> - Modifier −: [list negative factors — e.g., CRL history, weak Phase 2, FDA has rejected similar drugs recently]
> - **Final estimate: [X]%** — [1-sentence rationale]
> - If positive: expected price range [low end → high end], based on [analog or analyst target]
> - If negative: expected price range [likely floor], based on [typical rejection drop for this type of event]

For earnings events: use the company's historical beat rate (last 4 quarters). If 3+ of 4 beats: high base rate. If 1 of 4: low.

---

### Section 5: Analog Analysis

Find 3 historical situations that closely match this setup. Analogs make the probability estimate credible — they show that similar plays have happened before, with documented outcomes.

**Search:** `"[drug class or indication] FDA approval" stock move OR "similar to [TICKER]" OR "[company type] [catalyst type] result"`

For each analog:
> **[TICKER analog] — [year]**
> - Setup: [brief — what was similar: same indication, same drug class, similar float, similar pre-catalyst price action]
> - Outcome: [positive or negative] → stock moved [+X% or -X%] in [timeframe]
> - Key difference from [TICKER]: [1 line — what's different that should adjust the expectation]

Three analogs minimum. If fewer than 3 are findable, state that and explain what's unusual about this setup that makes analogs hard to find.

---

### Section 6: Smart Money Signals

Three sub-sections, each pointing to whether institutional and informed money is positioning for the catalyst.

#### 6a. Insider transactions (Form 4)

Search for Form 4 filings in the last 90 days. Insiders buying open-market shares (not option exercises, not granted shares — actual cash purchases) is the strongest possible signal.

- List any insider purchases: who, how many shares, at what price, on what date
- Note if executives are selling (normal if pre-planned 10b5-1 plan; concerning if opportunistic)
- If no insider activity: note it

#### 6b. Institutional changes (13F)

Search for recent 13F filings showing new positions or significant increases from known hedge funds or specialist biotech/tech funds.

- Note any new institutional positions opened in last quarter
- Note any major position increases (>50% increase in holdings)
- If institutions are reducing: flag as cautionary signal
- Key: a specialist biotech fund (e.g., Baker Bros, RA Capital, Perceptive Advisors) adding a large position in a pre-PDUFA name is a very strong signal

#### 6c. Options unusual activity

**Implied volatility — use IBKR first:**
- `implied_vol_underlying` from `get_price_snapshot` (batch item A) gives the underlying's IV directly — multiply by 100 for percentage. This is the market's real-time expectation of future volatility.
- `historical_vol` gives 30-day realized volatility. If `implied_vol_underlying > historical_vol` significantly: elevated uncertainty, likely a catalyst priced in.
- Implied move estimate: `implied_vol_underlying × sqrt(days_to_event / 365) × current_price` = expected $ move

**Unusual options activity — web search:**
- Note any large call buying (strike, expiry, volume vs. open interest)
- Note implied move from ATM straddle if available: `(call price + put price) / stock price`
- Compare to IBKR implied move calculation above
  - If ATM straddle move < your probability-weighted expected move: market underpricing the event → favorable entry
  - If ATM straddle move > your probability-weighted expected move: already priced in more → thin edge

---

### Section 7: Risk/Reward Matrix

Build three scenarios. Use the probability estimates from Section 4 and analog outcomes from Section 5.

| Scenario | Probability | Price target | From current price | $ on 30% position (~$240) |
|---|---|---|---|---|
| Bull — [catalyst positive + squeeze] | [X]% | $[price] | +[%] | +$[amount] |
| Base — [catalyst positive, no squeeze] | [X]% | $[price] | +[%] | +$[amount] |
| Bear — [catalyst negative] | [X]% | $[price] | -[%] | -$[amount] |

**Expected value calculation:**
`EV = (P_bull × bull_gain) + (P_base × base_gain) + (P_bear × bear_loss)`

If EV > 0 and EV > $6 (round-trip commission): positive expected value trade.
If EV < $6: commission drag eats the edge, do not enter.

**Stated as:** 
> "EV = +$[X] per $240 deployed — [positive/negative] expected value trade."

---

### Section 8: Verdict & Trade Setup

**Conviction score: [X]/10**

Use the scoring rubric from `references/scoring-rubric.md`. Show the breakdown — do not just give a number without showing what earned each point.

**Recommendation:** [BUY NOW / WATCH / SKIP]

- **BUY NOW:** Conviction ≥ 7, EV positive, halal verified, event within 14 days
- **WATCH:** Conviction 5–6, or event > 14 days out, or halal unverified — set a reminder date
- **SKIP:** Conviction < 5, or EV negative, or halal fails

**If BUY NOW or WATCH:**

> **Trade setup:**
> - Entry: $[price] — [why this level: current price / at support / breakout above resistance]
> - Stop: $[price] — [must be a real technical level: prior swing low, pre-catalyst base, key support — NOT a fixed % from entry]
> - **Target 1: $[price] — [exact technical OR fundamental reason this level is real resistance]**
> - **Target 2: $[price] — [exact technical OR fundamental reason this level is real resistance]**
> - Max position: $[amount] ([X] shares) = 30% of ~$[portfolio_value] — costs $[amount] + $3 commission
> - Do NOT size larger than 30% — this is a binary event.
> - Exit rule: if catalyst resolves negatively, exit at market open, no averaging down.

**Stop loss derivation rules — mandatory, no exceptions:**

A stop loss is NOT a percentage from entry. The market does not know where you bought. A stop must be placed just below a level that, if broken, proves the thesis is wrong. Run this process for every stop:

**Technical levels to check (search `"[TICKER]" support OR "swing low" OR "prior low" OR "200-day MA" OR "50-day MA"`):**
- Most recent swing low before entry (the last place buyers stepped in — if it breaks, they're gone)
- Pre-catalyst base / consolidation low (for catalyst plays: the low the stock held before the event was known)
- Key moving average (200-day MA = major institutional floor; 50-day = short-term trend support)
- Prior breakout level (a stock that broke out of a range at $X — that $X is now support; below it = breakout failed)
- Round number support ($100, $200 etc. — large options strikes cluster here, market defends these)
- Gap fill level (if the stock gapped up on news, the bottom of the gap = where the gap fully fills = real support)

**Stop placement rules:**
- Place the stop **just below** the support level (1–3% below), not at it — a stop AT support gets hunted by market makers
- The stop must answer: "If price reaches here, what was wrong about the trade?" If you can't answer that, it's not a real stop.
- For catalyst plays: the stop is usually the pre-announcement low. If the stock was at $8 before the FDA filing and you entered at $12, a break below $10 (the base) means the catalyst premium is evaporating — that's your stop, not "$12 × 0.92."

**Format the stop as:**
> - **Stop: $[price]** (-[%] from entry) — [exact reason: "prior swing low from May 3" / "200-day MA" / "pre-catalyst base" / "breakout level that held for 3 weeks before entry"]

**What NOT to do:**
- ❌ "Stop: −8% from entry" — not a level, just a loss limit
- ❌ "Stop: $[entry × 0.92]" — the market doesn't know your entry
- ❌ Same stop % for every stock — a volatile biotech needs a wider stop than a mega-cap; the stop is dictated by structure, not preference

---

**Target derivation rules — mandatory, no exceptions:**

Targets must be derived from real market structure. A percentage from entry is NOT a target. Run this process for every target level:

**Technical levels to check (search `"[TICKER]" resistance support "52-week high" OR "prior high" OR "all-time high"`):**
- Prior swing highs (levels where price previously rejected and reversed — market has memory here)
- 52-week high / all-time high (major resistance if not already broken)
- Round number confluence ($100, $150, $200 etc. — high psychological significance, options market clusters here)
- Post-earnings gap fills (if stock gapped up on earnings, the top of that gap is often resistance)
- Volume profile nodes (high-volume price levels = where most shares changed hands = stickiest support/resistance)
- Moving averages (200-day MA = major institutional level; 50-day = shorter-term trend level)

**Fundamental levels to check (search `"[TICKER]" analyst price target OR "fair value" OR "price target" 2026`):**
- Analyst consensus price target (where the majority of sell-side models point to)
- Bull-case analyst target (highest credible estimate — a stock often pauses here before going higher)
- DCF / EV/Sales / P/E mean reversion fair value (what does the stock price at a "normal" multiple for its sector?)
- Previous cycle high valuation multiple (if NVDA peaked at 35x forward P/E last cycle, 35x current EPS = a real ceiling)

**Format each target as:**
> - **Target 1: $[price]** (+[%] from entry) — [technical reason] + [fundamental reason if applicable]
>   - e.g. "$240 — prior ATH from May 14 (technical) + where sell-side consensus clusters (fundamental). If NVDA breaks through $240 on volume, next target applies. If it stalls here with declining volume, take partial profit."
> - **Target 2: $[price]** (+[%] from entry) — [technical reason] + [fundamental reason if applicable]
>   - e.g. "$285 — top of the post-earnings gap from Feb 2026 + BofA bull-case target. Parabolic territory — if reached, take remaining profit, don't hold hoping for more."

**What NOT to do:**
- ❌ "Target 1: $[entry × 1.12]" — meaningless, the market doesn't know your entry price
- ❌ "Target 1: +15% from entry" — not a level, just a wish
- ❌ Using the same % for every stock — NVDA and a $5 biotech have completely different structures

**If SKIP:**
> One sentence on why — what would need to change to revisit.

---

---

### Section 9: HTML Report

**After completing all 8 sections, always generate a self-contained HTML report and open it in the browser. This is not optional.**

**File path:** `reports/analysis-[YYYY-MM-DD].html`
(If multiple tickers analyzed in one session, put them all in the same file.)

**Design reference:** `reports/analysis-2026-06-10.html` is the canonical template. Match its structure exactly.

---

#### Required visual components

**1. Header**
- Title, date, portfolio size ($800), max position size (30% = $240), halal standard (AAOIFI)
- Data source line: "Market data: IBKR live feed | Fundamentals: web search"

**2. Verdict summary cards (one per ticker)**
- Ticker name + company + WATCH / BUY NOW / SKIP badge (color-coded: green/amber/red)
- Conviction score (X/10)
- Days to PDUFA countdown in top-right corner
- 1-line summary of the key risk and key positive
- IBKR theme tags (top 2 from `get_company_themes`) as small pill badges

**3. Radar comparison chart (Chart.js)**
- One radar dataset per ticker
- 6 axes: Approval %, Conviction (×10 scale), Short Interest (% of float), Cash Runway (normalized), Smart Money signal (0–100), Data Quality (0–100)
- Scores: map values to 0–100 for chart (e.g. 82% approval → 82, conviction 7/10 → 70)
- SKIP tickers: set all scores to 0 and use dashed border

**4. Per-ticker sections** (in order: BUY NOW first, then WATCH, then SKIP)

Each ticker section contains:

- **Ticker pill** (color-coded), company name, sector
- **Stats grid** — market cap, shares outstanding, short interest (highlighted red if >10%), confirmed price, cash position, PDUFA date. Use colored values for anything notable.
- **Halal compliance table** — AAOIFI criteria with pass/warn/fail per row. Always show the ✅ HALAL VERIFIED / ⚠️ HALAL UNVERIFIED / ❌ NOT HALAL badge. If NOT HALAL → show red stop banner and skip remaining sections for that ticker.
- **Catalyst timeline** — vertical timeline with numbered dots (primary catalyst = green dot, secondary = blue, further out = grey). Show date, event name, description, CONFIRMED badge where applicable.
- **Probability model** — large % number (colored by value: ≥80% green, 60–79% amber, <60% red). Horizontal bar rows showing base rate, each positive modifier (+%), each negative modifier (−%). If-approved and if-rejected price ranges below.
- **Scenario chart** (Chart.js bar chart) — Bull / Base / Bear scenarios. Bars show P&L in dollars on the $240 position. Bull bar = indigo/green, Base bar = amber, Bear bar = red. Negative bars shown below zero.
- **EV box** — large EV dollar figure (green if positive, red if negative). Breakdown of each scenario's contribution. Note whether EV > $6 commission.
- **Analogs** — 3 cards side by side. Each: company + year, outcome % (green if positive, red if negative), setup description, key difference note.
- **Smart money signals** — 3 rows: Insider (Form 4), Institutional (13F), Options. Each has a BULLISH / NEUTRAL / BEARISH badge and description.
- **Trade setup box** — Entry / Stop / TP1 / TP2 / Position size rows. Color-code: stop = red, entry = white, TP1 = amber, TP2 = green.
- **Price levels chart** (Chart.js horizontal bar chart) — 5 bars: Stop, Entry, TP1, TP2, Bull Case. Colors match trade setup box.
- **Conviction breakdown** — large score number + row-by-row checklist with earned (green dot) / missed (grey dot) and points.

**5. Action items section**
- One card per ticker summarizing the exact next steps (numbered list).

---

#### Chart.js implementation rules

- Use CDN: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
- Always set `responsive: true, maintainAspectRatio: false` and wrap in a fixed-height div
- Dark theme throughout: background `#0d0f14`, surface `#161a23`, card `#1e2330`, border `#2a3040`, text `#e2e8f0`, muted `#7a8499`
- Grid lines: `#2a3040` (dark, subtle)
- Axis tick colors: `#7a8499`
- No chart legend when it adds clutter (single-dataset charts)

**Price chart data — use IBKR `get_price_history` (batch item B), NOT estimated closes:**
- The batch already fetched ONE_YEAR / ONE_MONTH bars with real OHLCV data
- Use the `close` field from each bar as the monthly close price
- Use `t` (timestamp) for the x-axis labels
- Mark the 52-week low (green dot) and 52-week high (red dot) using `misc_statistics` from the price snapshot
- This eliminates chart data estimation entirely — every data point is a real broker-sourced close

---

#### HTML generation rules

- Self-contained single file (no external assets except Chart.js CDN)
- All CSS inline in `<style>` block
- No framework dependencies (vanilla HTML/CSS/JS only)
- `max-width: 1200px` centered layout
- Mobile-responsive grid (collapse to single column below 768px)
- After writing the file, run: `open reports/analysis-[date].html` to launch in browser

---

## Output format

In chat: deliver a brief summary after the HTML is opened — ticker verdict, key risk per ticker, and the single most important action item. Do not repeat the full 8-section analysis as markdown; the HTML report is the deliverable.

If the user explicitly asks for a markdown breakdown of a specific section, provide it. Otherwise, point to the HTML file.

---

## What this skill does NOT do

- Execute trades — Abbas does this in his broker
- Update portfolio.json — use portfolio-manager for that
- Give financial advice — research only, disclosed in every report
- Replace the daily check — this is an on-demand deep dive, not the daily routine
