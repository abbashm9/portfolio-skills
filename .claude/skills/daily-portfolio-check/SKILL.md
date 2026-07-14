---
name: daily-portfolio-check
description: Run a daily post-market portfolio review for Abbas's halal stock portfolio — fetches live closing prices, calculates P&L per position and total, evaluates each position against its exit strategy (stop-loss, take-profit ladder, time-based exit, catalyst), flags any positions needing action, proposes rebalancing or rotation moves, and produces a designed HTML email report with a daily education module on US equity concepts. Since Abbas isn't withdrawing money, suggestions can be aggressive (e.g., trim 30% of a winner to buy 1 share of a new high-conviction name). Use whenever Abbas says "daily check", "portfolio check", "how am I doing", "market closed", "check my stocks", "run the daily", or any variant of "review my portfolio." Trigger even if he just says "daily" or pastes a screenshot of his brokerage app at end of day.
---

# Daily Portfolio Check (v2 — HTML Email + Education)

A post-NYSE-close daily review skill for Abbas's halal stock portfolio. Outputs a designed HTML email report and emails it via Gmail connector.

## Critical user context

- **User:** Abbas Al Madani, Kuwait
- **Trading experience:** 8 years in forex and indices — strong on technicals, mechanics, risk management
- **Stock-market gap:** New to single-name US equities — needs to learn valuation multiples, fundamentals language, sector-specific cycles
- **Tone preference:** Pragmatic, no condescension, no "what is a stop-loss" basics. Treat him as an experienced trader who needs the equity-specific vocabulary
- **Withdrawal intent:** NONE — rotation suggestions can be aggressive
- **Halal compliance:** Business activity only. Core business must be permissible (no alcohol, gambling, weapons, pork, pornography, conventional banking/insurance as primary business). Financial ratio screens (debt, interest income %) are irrelevant — Abbas is a capital gains trader not a dividend investor. Do NOT flag stocks for Musaffa/AAOIFI financial ratio checks. Don't include halal education in emails.
- **Disclosure:** Research, not financial advice

## Transaction cost framework

**Broker commission:** ~$1.00 per trade (buy or sell) on IBKR. Entry commission already paid — only exit commission (~$1) remains on open positions. Round-trip total = ~$2.

### Rules that override all exit suggestions

1. **Minimum profit threshold for any sell/trim:** Gross P&L on the shares sold must exceed $1 (the exit commission). Entry cost already sunk.
   - Formula: `(current_price − entry_price) × shares_to_sell > $1`
   - If the result is ≤ $1: show the math, label it "HOLD (commission eats profit)", move on.

2. **Minimum profit threshold for a rotation:** Full round-trip costs ~$2 (sell $1 + buy $1). Expected gain from the new position must justify $2 in friction.
   - If the rotation doesn't clear $2 in projected upside: skip it or note "commission drag too high for this move."

3. **Small positions (<$75 market value):** Never suggest a partial trim. The position is too small to split — either hold or exit fully.
   - Example: a $70 position trimmed 50% frees ~$35 but the $1 exit commission is ~3% of proceeds.

4. **Always show net P&L:** In every sell, trim, or rotation suggestion, display both gross and net:
   - `Gross: +$18.40 | Exit commission: −$1.00 | Net: +$17.40`
   - Never present a gross P&L without the commission line.

5. **Cash deployment minimum:** Don't suggest buying into a new position if the cash being deployed (after commission) would result in a position worth < $30. Too small to be meaningful.

## Sources of truth: IBKR (live) + portfolio.json (metadata)

**Two data sources. Both required. Neither can substitute for the other.**

| Data | Source | Why |
|------|--------|-----|
| Live positions (shares, avg cost, market value, P&L) | IBKR `get_account_positions` | Broker is authoritative on what you actually hold |
| Cash balance, net liquidation value | IBKR `get_account_balances` | Settled cash, real-time |
| Live prices | IBKR `get_price_snapshot` | Single authoritative source — no web scraping needed |
| Account performance (1D, MTD, YTD) | IBKR `get_pa_performance_all_periods` | Broker-verified TWR/MWR |
| Portfolio allocation by sector/region | IBKR `get_pa_allocation` | Live breakdown |
| Stops, TPs, catalysts, notes | GitHub `portfolio.json` | Context the broker doesn't know |
| Watchlist, education tracker | GitHub `portfolio.json` | Metadata only stored here |

**IBKR is always the source of truth for financial numbers. portfolio.json is the source of truth for strategy metadata.**

If IBKR is unreachable: fall back to portfolio.json + web search (see Step 0 Fallback below). Do NOT send a skip email — send the best email you can with clearly flagged data sources.
If portfolio.json is unreachable: proceed with IBKR data for positions/prices, but note "⚠️ portfolio.json unavailable — stops, TPs, and catalyst data missing. Metadata sections skipped."

## Workflow — every daily check

### Step 0: Pull live data from IBKR + metadata from portfolio.json

**Run both calls in parallel — BEFORE anything else.**

**0A — IBKR live state (two parallel calls):**
```
get_account_positions  →  shares held, avg_price, market_value, unrealized_pnl, daily_pnl, contract_id per position
get_account_balances   →  cash_balance, net_liquidation_value
```

**IBKR failure — fall back, don't skip.** If `get_account_positions` returns an empty list or an error, activate the fallback mode:

**Step 0 Fallback — portfolio.json + web search for prices:**
1. Use `portfolio.json` positions[] for shares held and avg cost (clearly flag: "⚠️ IBKR unavailable — using portfolio.json share counts")
2. For each ticker, run `WebSearch "[TICKER] stock price today"` and extract the current price from Yahoo Finance or Google Finance results. Flag every price: "⚠️ Price from web search — verify in your broker app before acting on any recommendation"
3. Skip all IBKR-specific calls (get_pa_performance_all_periods, get_pa_allocation, get_company_themes) — omit those sections from the email
4. Include a banner at the top of the email: `⚠️ IBKR connector unavailable — prices sourced from web search. Verify before trading.`
5. Continue with all remaining steps using portfolio.json + web prices. A web-priced email is better than no email.

If web search also returns no prices for a ticker: label that position "⚠️ PRICE UNAVAILABLE — check broker app manually."

From the positions response, build your working positions list:
- Use `contract_description` as the ticker
- Use `position` as shares — **IBKR is the authoritative share count.** If IBKR shows a different share count than portfolio.json, trust IBKR and flag the discrepancy: "⚠️ [TICKER]: IBKR shows [X] shares, portfolio.json shows [Y] — portfolio.json is stale. Run portfolio-manager to sync."
- Use `average_price` as cost-per-share (this is the real fill price)
- Use `market_value`, `unrealized_pnl`, `daily_pnl` directly — do NOT recalculate from prices
- Store each position's `contract_id` — needed for price snapshots and theme lookups in Steps 1 and 1.5

From balances: use `cash_balance` as dry powder and `net_liquidation_value` as total account value.

**0B — GitHub portfolio.json (metadata):**
Fetch from:
```
https://raw.githubusercontent.com/abbashm9/portfolio-skills/main/portfolio.json
```

Extract ONLY the metadata IBKR doesn't provide:
- Per-position: `stop_loss`, `tp1`, `tp2`, `catalyst`, `catalyst_date`, `approval_probability_pct`, `halal_verified`, `notes` — matched to IBKR tickers
- `watchlist[]` array
- `totals.concentration_warning`
- `last_updated` timestamp
- `education_tracker`
- `investment_goal`

**Reconciliation check:** If IBKR returns a ticker not present in portfolio.json positions[], flag it in the email: "⚠️ [TICKER] held in IBKR but not in portfolio.json — run portfolio-manager to sync metadata."

### Step 1: Fetch live prices from IBKR

Use `get_price_snapshot` for each position's `contract_id` (from Step 0A). Run all tickers in parallel.

**Request these fields for every position:**
```
market_data_names: ["last", "change", "prior_close", "misc_statistics"]
```

- `last` → current/closing price (use this for all P&L display)
- `change` → day's $ change and % change (pre-calculated by IBKR)
- `prior_close` → yesterday's close (for day-change verification)
- `misc_statistics` → 52-week high/low (used in Step 3 for stop/TP context)

**No multi-source cross-check needed.** IBKR is the broker — its price feed is definitionally authoritative. If the snapshot returns null or an empty `last` field for a ticker:
- Fall back to `unrealized_pnl` + `average_price` from Step 0A to back-calculate: `implied_price = average_price + (unrealized_pnl / shares)`
- Flag the position: "⚠️ IBKR price snapshot unavailable for [TICKER] — using implied price from P&L data"
- If `unrealized_pnl` is also null or missing: do NOT guess. Label this position as "⚠️ PRICE UNAVAILABLE" and skip its P&L calculation. Do not fill in a number.

**ABSOLUTE PROHIBITION: Do NOT use web_search, WebFetch, or any external URL to fill in prices — ever, under any circumstances.** If IBKR is unavailable and the back-calculation also fails, the price cell shows "N/A". A wrong price in the email is worse than a missing one. Abbas will see "N/A" and know to check his broker app manually.

**Plausibility gate:** After fetching all prices from IBKR, run this sanity check per position before writing the email:
- If `last` price differs from `average_price` by more than 50% in either direction AND the position has no recent catalyst that would explain a move that large: flag it with "⚠️ Price looks suspicious — verify manually" and show both the IBKR-returned price and the implied price from `unrealized_pnl`. Do not silently use the suspicious price.
- This gate catches cases where `get_price_snapshot` returns stale or wrong contract data.

In the email footer: `"Prices: IBKR live feed — [timestamp from last response]"`. If any price was back-calculated from P&L data instead of `get_price_snapshot`, note it: `"[TICKER]: implied from P&L, not snapshot"`.

**Also fetch prices for watchlist tickers** (Step 2.5): search their contract_ids via `search_contracts` if not already known, then `get_price_snapshot` in parallel with position price fetches.

### Step 1.5: IBKR Market Intelligence (run in parallel with Step 1)

Pull three additional IBKR data layers simultaneously. These feed the intelligence sections of the email — they do NOT block the price/P&L workflow.

**1.5A — Account Performance:**
```
get_pa_performance_all_periods
```
Returns broker-verified TWR or MWR returns for: 1D, 7D, MTD, 1M, YTD, 1Y.
Extract and store: 1D cumulative return %, MTD %, YTD % — displayed in the email hero section.
Note the `portfolio_measure` field (TWR or MWR) and show it in the email: "Returns: TWR" or "Returns: MWR".

**1.5B — Portfolio Allocation:**
```
get_pa_allocation  →  type: "ALL"
```
Returns NAV breakdown by: SECTOR, REGION, COUNTRY, ASSET_CLASS, FINANCIAL_INSTRUMENT.
Extract sector weights (e.g., Technology X%, Biotechnology Y%) and region (US vs international) for the email Intelligence section.
Flag any sector weight > 60% as a concentration note.

**1.5C — Investment Themes per Position:**
For each position's `contract_id` (from Step 0A), call:
```
get_company_themes  →  contract_id, max_themes: 3, max_companies: 5
```
Run in parallel across all positions.

This returns the investment themes/trends IBKR associates with each stock (e.g., "AI Infrastructure", "Data Center Networking", "IgAN Treatment") plus the top 5 peer companies ranked by thematic relevance.

Use the themes output for two purposes:
1. **Email context** — show each position's top 2 themes as smart tags in the position card
2. **Rotation intelligence** — the peer companies listed in themes are candidates for future rotation. If a catalyst play from Step 3.5 appears as a peer of a current holding, note the thematic connection ("CAPR is a theme-peer of VERA in the rare disease space").

**1.5D — Investment Topic Search (for catalyst radar context):**
For each current position's primary sector/theme, run:
```
search_investment_topics  →  query: "[primary theme keyword]"
```
Example: for VERA → "nephrology" or "rare disease"; for ANET → "ethernet" or "data center".
Use the returned topic keys to enrich Step 3.5 — the themes give you adjacent sectors where catalyst plays may exist that web search alone might miss.

All 1.5 results are non-blocking: if any call returns empty or errors, continue without it and omit that subsection from the email.

### Step 2: Build the data tables and withdrawal goal tracker

**Investment goal tracker — show in every email, near the top.**

Read `investment_goal` from portfolio.json. Calculate:
- `current_total_value` = sum of (shares × current_price) for all positions + cash_available
- `gap` = investment_goal.target_total_value − current_total_value
- `progress_pct` = (current_total_value / investment_goal.target_total_value) × 100

Format as a single compact line in the email hero section, right under the total P&L:

> 🎯 **Investment goal:** $[current_total_value] / $1,000 — **$[gap] to go** ([progress_pct]% there)

Color the gap green if < $50, amber if $50–$150, grey if > $150.

If `gap ≤ 0`: replace with a bold alert — "🎯 **$1,000 reached. Investment goal hit.**"

This tracker does NOT change the exit strategy — stops and TPs still apply as normal. It's a progress indicator only.

**Use IBKR values directly — do NOT recalculate what IBKR already provides:**

Per-position (from Step 0A + Step 1):
- `market_value` → current position value (IBKR)
- `unrealized_pnl` → P&L $ vs avg cost (IBKR)
- `unrealized_pnl / (shares × average_price)` → P&L % (calculate this one)
- `daily_pnl` → day's change $ (IBKR)
- `change` from price snapshot → day's change % (IBKR)

Portfolio totals (from Step 0A + Step 1.5A):
- Total current value → `net_liquidation_value` from `get_account_balances`
- Total P&L $ → sum of all positions' `unrealized_pnl`
- Total P&L % → total P&L / total cost basis (cost basis = sum of shares × average_price per position)
- Total day's change $ → sum of all `daily_pnl`
- 1D/MTD/YTD % → from `get_pa_performance_all_periods` (broker-verified)

### Step 2.5: Watchlist tracking — fetch live prices for watchlist items

If `watchlist[]` exists and has entries in portfolio.json, fetch live prices for each watchlist ticker (same verification protocol as Step 1). Run these fetches in parallel with Step 1.

For each watchlist item, calculate:
- **Days to event:** `pdufa_date − today` in calendar days
- **Price vs entry target:** `(current_price − entry_target) / entry_target × 100` — how much has price moved since the analysis was done?
- **Entry still valid?** If current_price > entry_target × 1.15 (moved >15% above target), flag as "ENTRY MOVED — re-analyze before buying". If current_price < entry_target × 0.90 (dropped >10% below target), flag as "PRICE DROPPED — check thesis still intact".
- **Event urgency:** if days_to_event ≤ 7, flag with 🔴 URGENT. If 8–14, flag 🟡 SOON. If 15–30, flag 🟢 WATCH.

This data feeds directly into the email section in Step 6.

### Step 3: Exit-strategy check per position (in order)

1. **Halal compliance** — quarterly check, not daily, but flag if breaking news suggests a change
2. **Stop-loss** — Below stop? 🚨 ALERT. Within 2% of stop? ⚠️ WATCH.
3. **TP1/TP2/TP3 — validate and re-derive if stale** (see below)
4. **Catalyst proximity** — within 5 trading days? Flag prominently
5. **Time-based** — flat ±3% for 30+ days, no catalyst? Consider trim
6. **Parabolic warning** — up >40% in 30 days, RSI >80? Mean-reversion risk

**Stop and TP level validation — runs on EVERY position, EVERY day, regardless of proximity.**

The values stored in portfolio.json are reference points only — they are NOT displayed as-is in the email. Every run must re-derive the real stop and TP levels from live market structure and show those in the email instead. This is not optional and does not depend on how close the price is to the stored level.

**For each position, run these two searches (in parallel with the price fetch in Step 1):**
- `"[TICKER]" support "swing low" OR "200-day" OR "50-day" OR "key level" [current month]`
- `"[TICKER]" resistance OR "prior high" OR "52-week high" OR "analyst target" OR "price target" [current month]`

**Stop derivation — for each position:**
- Find the most recent real support level below current price: prior swing low, moving average (200-day or 50-day), pre-catalyst base, or a breakout level the stock held before running
- Place the stop **just below** that level (1–3% below), not at it
- If the stored portfolio.json stop coincides with a real level: confirm it and display it
- If the stored stop has no market structure behind it: replace it with the real level and note the change
- Alert logic: flag when price is within 2% of the stop AND volume is surging (real break). Do not alert on low-volume tests.

**TP derivation — for each position:**
- Find real resistance levels above current price: prior ATH, prior swing high, 52-week high, round number confluence, analyst consensus target, bull-case target
- If the stored TP coincides with a real level: confirm it and display it
- If the stored TP has no market structure behind it: replace with the nearest real resistance level and note the change
- Show up to 3 TP levels per position ranked by proximity

**Format for each position in the email:**
> **[TICKER]** | Stop: $[real level] ([reason]) | TP1: $[real level] ([reason]) | TP2: $[real level] ([reason])

Example:
> **NVDA** | Stop: $197 (just below $200 pre-breakout base + 200-day MA) | TP1: $235 (May 14 ATH) | TP2: $275 (BofA target / next analyst cluster)

**When recommending action at either level, always state why that price is real:**
> "🔔 NVDA approaching TP1 $235 — May 14 ATH, real resistance. Recommend trimming [X]% here."
> "🚨 NVDA breaking below $197 stop — pre-breakout base lost, thesis broken. Exit now."

Never display a stored portfolio.json stop or TP without first verifying it against live market structure.

Status emoji per position:
- ✅ HOLD — within range, thesis intact
- ⚠️ WATCH — approaching a level, no action yet
- 🔔 ACTION — hit a level, recommend trim/exit
- 🚨 ALERT — stop hit or thesis broken, exit now

### Step 3.5: Catalyst Discovery — full market scan

**Purpose:** Surface small/mid-cap names with imminent catalysts across the ENTIRE market — not just pharma. Earnings beats, AI contract wins, guidance raises, analyst upgrades, short squeezes, sector momentum plays, and yes, FDA events too. The point is to find the stocks that are about to move 30–60% in any sector, not just biotech.

**Everything here must come from live web_search. Training data is useless for discovery.**

#### 3.5.1 — Cast the net (30 searches in parallel)

Run ALL simultaneously — they execute in parallel so 30 searches takes no longer than 15. More searches = more candidates = better market coverage.

**Earnings & corporate catalysts (8 searches):**
1. `small cap "earnings beat" OR "EPS beat" "revenue beat" upcoming [current month] [next month] catalyst`
2. `small mid cap "guidance raised" OR "raised guidance" OR "raised full year outlook" [current month] 2026`
3. `"contract award" OR "government contract" OR "IDIQ contract" small cap [current month] 2026`
4. `"analyst upgrade" "price target raised" small cap outperform [current week] [current month] 2026`
5. `"product launch" OR "FDA clearance 510k" OR "CE mark" medical device small cap [current month] [next month] 2026`
6. `upcoming earnings small cap "whisper number" OR "earnings whisper" beat expected [current month]`
7. `"spin-off" OR "strategic review" OR "divestiture" small mid cap catalyst 2026`
8. `"partnership" OR "licensing deal" OR "milestone payment" small cap biotech OR tech [current month] 2026`

**Tech, AI, semiconductors & sector momentum (8 searches):**
9. `AI OR "artificial intelligence" OR "data center" small mid cap catalyst earnings [current month] [next month] 2026`
10. `semiconductor OR "chip" OR "HBM" OR "CoWoS" small cap catalyst upcoming [current month] 2026`
11. `defense OR aerospace "contract win" OR "LPTA award" small cap [current month] 2026`
12. `energy OR "clean energy" OR "nuclear" small mid cap catalyst [current month] [next month] 2026`
13. `"52-week high" breakout small cap high volume catalyst [current week] 2026`
14. `"short squeeze" catalyst upcoming [current month] high short interest "days to cover" small cap 2026`
15. `"unusual options activity" small cap [today's date] OR [this week] bullish call sweep`
16. `"insider buying" cluster "Form 4" multiple executives small cap [current month] 2026`

**Market structure & momentum signals (6 searches):**
17. `"premarket gainers" OR "premarket movers" catalyst [today's date] small cap`
18. `"most active" OR "volume spike" small mid cap catalyst [today's date] OR [this week]`
19. `"gamma squeeze" OR "options expiry" catalyst small cap [current week] [next week] 2026`
20. `"breakout" "bull flag" OR "cup and handle" small cap high volume [current week] 2026`
21. `"institutional buying" 13F "new position" small cap [current month] 2026`
22. `"heavily shorted" "upcoming catalyst" OR "short interest" small cap 2026 [current month]`

**FDA & biotech (8 searches):**
23. `FDA PDUFA action dates [current month] [next month] upcoming decisions`
24. `"advisory committee" OR AdCom meeting scheduled [current month] [next month] FDA 2026`
25. `"phase 3" "top-line data" OR "data readout" expected [current month] [next month] 2026`
26. `site:biopharmcatalyst.com PDUFA [current month] OR [next month]`
27. `biotech catalyst calendar [current month] [next month] 2026`
28. `"complete response letter" resubmission PDUFA upcoming 2026`
29. `"interim analysis" OR "primary endpoint" met OR "phase 2b" results [current month] [next month] 2026`
30. `"rare disease" OR "orphan drug" PDUFA OR "breakthrough therapy" designation upcoming [current month] 2026`

Extract all distinct tickers mentioned. Target 25–40 raw candidates. Tickers appearing in multiple searches across different categories = strongest signal — weight these heavily.

**Sector balance rule:** The top 3 final candidates must not all be from the same sector. If the top 3 survivors are all biotech/pharma, promote the highest-scoring non-pharma candidate into the third slot and push the lowest-scoring pharma pick to WATCH status. Abbas needs to see the full market, not a pharma newsletter.

#### 3.5.2 — Rapid 3-gate pre-screen (per candidate)

Drop any candidate that fails any gate:

- **Gate 1 — Confirmed catalyst date ≤ 45 days?** This includes: PDUFA date, earnings date, product launch date, contract announcement date, scheduled data readout. No confirmed date → drop.
- **Gate 2 — Market cap < $2B?** Search `"[TICKER]" market cap` → ≥ $2B → drop.
- **Gate 3 — Halal quick check.** Search `"[TICKER]" business model OR revenue OR products`. Obvious disqualifier (alcohol, gambling, weapons manufacturer as primary business, conventional bank/insurer) → drop. Unclear → keep with ⚠️ flag.

#### 3.5.3 — Score survivors (5-point pre-score)

| Factor | Points |
|---|---|
| Event ≤ 14 days out | 2 |
| Event 15–45 days out | 1 |
| Short interest ≥ 15% float (squeeze potential) | 1 |
| Appears in 2+ search sources OR 2+ categories | 1 |
| Any smart money signal (insider buy, unusual options, institutional 13F buildup) | 1 |

Sort by score. Keep top 3 candidates, enforcing the sector balance rule above. These go to Step 3.8 for condensed analysis.

If fewer than 3 survive all gates: fill remaining slots with the highest-conviction name from the current watchlist in portfolio.json that hasn't been analyzed recently, and note it as "watchlist carry-forward — no new candidate found today."

Feed top 3 into Step 3.8, Step 3.7, and Step 4.

### Step 3.8: Condensed analysis — top candidates from Step 3.5

For each of the top 3 candidates from Step 3.5, run a condensed 5-point analysis. This is NOT the full 8-section stock-analyzer deep dive — that's available on demand in chat. This is the daily email version: tight, actionable, enough to decide whether to investigate further.

Run these searches per candidate (in parallel across all 3 candidates):
- `"[TICKER]" earnings date OR PDUFA OR catalyst confirmed [current month] [next month]`
- `"[TICKER]" market cap float short interest`
- `"[TICKER]" revenue growth OR "earnings history" OR "beat estimates" OR "phase 3" history`
- `"[TICKER]" balance sheet OR "cash position" OR dilution OR debt 2026`
- `"[TICKER]" insider buying OR "Form 4" OR institutional 13F OR "analyst target" 2026`

**Identify the catalyst type first**, then adapt the analysis accordingly:

**For FDA/clinical catalysts:** approval probability, accelerated approval vs full approval distinction, CRL downside, drug pricing, cash runway/dilution risk.

**For earnings catalysts:** EPS consensus vs whisper number, revenue beat history (last 4 quarters), guidance raise probability, what drove the move in prior beats, whether the stock is up/down into earnings (run-up = higher sell-the-news risk).

**For contract/partnership catalysts:** size of contract relative to market cap, likelihood of announcement, revenue impact, competitive moat.

**For analyst upgrades / sector momentum:** what changed in the analyst's thesis, price target gap to current price, whether sector ETF flows support the move.

For each candidate, produce this block (this is what goes in the email):

---

> **🔬 [TICKER] — [COMPANY NAME]** `[SECTOR / CATALYST TYPE]`
> **Catalyst:** [event type] on [exact date] — [X] days away
> **Market cap:** $[X]M | **Float:** $[X]M | **Short interest:** [X]%
>
> **Edge:** [1-line reason this is worth looking at — what's the specific setup? e.g. "Beat estimates 4 of last 4 quarters, entering earnings with 18% short interest and unusual call activity" OR "AdCom vote in 9 days, RTOR program, Phase 3 positive"]
>
> **Probability:** [X]% — [1-line rationale. For FDA: base rate + key modifier. For earnings: beat frequency + whisper vs consensus. For contracts: deal size vs cap, prior win rate.]
>
> **Scenarios:**
> - ✅ If positive: ~$[price] (+[%]) — [real level: prior high / analyst target / resistance / typical post-beat move for this name]
> - 💀 If negative: ~$[price] (-[%]) — [real level: support / typical post-miss move / CRL reaction]
> - Expected value on 30% position (~$[amount]): **+$[EV] / -$[EV]**
>
> **Smart money:** [insider buys / unusual options / institutional buildup / none visible]
> **Key risk:** [the one thing that kills this trade — dilution shelf, sector rotation, guidance cut, CRL, etc.]
>
> **Halal:** ✅ Clean (core business permissible) / ⚠️ Unverified — check business model / ❌ Fails (forbidden core business)
>
> **Conviction: [X]/5** (pre-score) → [INVESTIGATE / WATCH / SKIP]
> *Run `analyze [TICKER]` for the full 8-section deep dive before entering.*

---

**INVESTIGATE** = pre-score 4–5, halal clear, event ≤ 14 days
**WATCH** = pre-score 3, or event 15–45 days, or halal unverified
**SKIP** = pre-score ≤ 2, or halal fails, or no confirmed event date

All 3 candidate blocks go into the email under the "📡 Catalyst Plays" section. Even SKIP candidates are shown — transparency on what was found and why it didn't make the cut. At least one block should be a non-pharma name whenever one qualifies.

### Step 3.6: Risk-score current holdings

Apply the three-sub-score risk scoring algorithm from `.claude/skills/stock-risk-report/SKILL.md` to each position in `positions[]`.

Calculate for each position:
- **Valuation Risk** (40% weight): Forward P/E, P/S, P/B, PEG vs sector norms
- **Growth Risk** (35% weight): revenue trend, margin direction, concentration, binary events
- **Financial Health Risk** (25% weight): D/E, ROE, net cash/debt position
- **Overall score** = weighted average → map to: LOW (0–30) / MODERATE (31–50) / HIGH (51–70) / EXTREME (71–100)

**Scope:** You are NOT rendering the full HTML widget. Output a per-position summary table:
> `[TICKER] | [SCORE]/100 | [LABEL] | [1-line driver]`

Any position scoring HIGH or EXTREME feeds into Step 4 as a rotation candidate.
Feed the full table into the Intelligence Layer in Step 6.

### Step 3.7: Cash deployment recommendation (mandatory when cash > $6)

**This section is required every run** whenever `cash_available` from portfolio.json exceeds $6.

**This recommendation MUST be driven by the actual outputs of Steps 3.5 and 3.6 — not by generic intuition or the pre-vetted list alone.**

- **From Step 3.5 (halal screener):** use the top 2–3 shortlisted candidates as the candidate pool for new positions. These have already passed the 5-pillar screen — don't re-screen, just pick the highest-conviction one that fits within the deployable cash amount.
- **From Step 3.6 (risk scorer):** use the per-position risk scores to evaluate the "add to existing" option. Only suggest adding to a current position if its risk label is LOW or MODERATE. Never suggest doubling down on a HIGH or EXTREME risk position with idle cash.

Abbas currently keeps a **$1 minimum cash reserve** at all times (to cover any exit commission without liquidating a position). So deployable cash = `cash_available − $1`. Commission on the new buy = $1. Net capital available for a new position = `cash_available − $2`.

If `cash_available − $2 < $30`: the remaining capital after commission is too small to be meaningful. State this explicitly:
> "Cash: $[X] — after $1 buy commission and $1 reserve, only $[X−2] deployable. Too small for a meaningful new position. Holding as dry powder."

If `cash_available − $2 ≥ $30`: **always** provide a concrete deployment recommendation. Do not leave this section blank or vague. Format:

> 💵 **Cash deployment — $[deployable] available**
> - **Option A — Catalyst play:** [TOP CANDIDATE from Step 3.5 Catalyst Radar, if conviction ≥ 6], buy [N] shares at ~$[price]. Event: [date]. Upside: +[%]. Downside: [%]. Halal: [status]. Position: $[amount] = [%]% of portfolio.
> - **Option B — Add to existing position:** [TICKER] (Risk: [score]/100, [LOW/MODERATE] from Step 3.6), buy [N] shares at ~$[price]. Rationale: [1 line]. Net position after: [shares] shares, avg entry ~$[blended].
> - **Recommended:** [A or B] because [1-line reason].
> - **Your call.**

**Position sizing for catalyst plays:** Abbas's target max allocation per catalyst name is **30% of total portfolio value** (positions + cash). Calculate: `0.30 × (total_positions_value + cash_available)`. Never exceed this cap in a single catalyst position, even if the conviction is high — binary events can go -70% on rejection.

Always show the math: shares × price + $1 commission ≤ deployable cash. Never suggest a buy that would leave cash_available below $1.

Feed the recommendation into Step 4 and the Intelligence Layer in Step 6.

### Step 4: Rotation suggestions (intelligence-driven)

Since Abbas isn't withdrawing money, propose moves when:
- A position hits TP1/TP2 → suggest where to redeploy (use Step 3.5 top candidates)
- A new high-conviction halal name has a near-term catalyst → suggest trimming a winner to fund a starter position
- A position is dead money (flat 30+ days) → suggest a rotation
- Pre-binary-event (earnings within 5 days) → suggest a risk-management trim

**When a HIGH-risk current position and a high-conviction screener candidate exist simultaneously, lead with a comparative rotation:**

> "[TICKER_HELD] is flagged HIGH risk ([reason from Step 3.6]) — [CANDIDATE] has [catalyst] in [N] days with [valuation note from Step 3.5]. Consider trimming [X] shares of [TICKER_HELD] (Net: +$Y after $6 commission) to buy [Z] shares of [CANDIDATE]."

Format all rotation suggestions with: exact shares to sell, exact $ freed, exact shares of replacement to buy, 1-line rationale, 1-line risk, end with "Your call."

### Step 5: Select today's education concept

See `references/education-curriculum.md` for the full 30-day curriculum (concepts numbered 1–30).

**How to pick — read `education_tracker` from portfolio.json first:**

1. Read `education_tracker.last_concept_number` — this is the last concept taught (0 = none taught yet).
2. **Priority 1 — term appeared in today's report:** If today's report used a term that maps to a specific curriculum concept that hasn't been taught yet, teach that one (set its number as current).
3. **Priority 2 — sequential next:** Otherwise, teach concept number `last_concept_number + 1`. If last was 30, wrap back to 1.
4. Never repeat the same concept number as `last_concept_number` unless it's an intentional Part 2 (Days 26–30) following its base lesson.

**After selecting the concept:**
- Note the concept number and name
- This gets written back to `portfolio.json` in Step 7 (see below) — the tracker is updated in the same GitHub commit as the email outbox

**Education paragraph format:**
- ONE main concept, one tight paragraph (~80–120 words)
- Plus a 1-line "also today" mention of a related term
- Voice: mixed register — trader-to-trader for the main concept, analytical when stakes need precision, slang/punchy when the term has a clean colloquial frame
- Always anchor to Abbas's actual positions and numbers — never use generic examples
- Place at the very bottom of the email

### Step 6: Generate the HTML email

Build a responsive HTML email with the structure in `references/email-template.md`. Key requirements:
- Inline CSS only (email clients strip `<style>` tags)
- Use tables for layout (still the most reliable email layout method)
- Color-coded status badges
- Hero banner with total P&L (green if positive, red if negative)
- Position cards with sparkline-style mini SVG charts (last 30 days when available)
- Education section in a colored box at the bottom
- Footer with disclaimer in 10px grey

**Email section order (top to bottom):**

1. **Hero banner** — total P&L today + 1D/MTD/YTD returns (from IBKR `get_pa_performance_all_periods`), investment goal tracker. Show the return type label: "TWR" or "MWR".
2. **⚠️ MANDATORY — Positions snapshot table** — a single HTML table with ONE ROW PER POSITION showing: Status badge | Ticker | Themes (top 2 from Step 1.5C, as small pill tags) | Close price | Day % | P&L $ | P&L % — then a TOTAL row. This is the first thing Abbas reads every morning. It MUST appear in every email, including weekend emails (use last known price if market closed). NEVER omit this table, collapse it into prose, or replace it with per-position cards only.
3. **Exit alerts** — any position needing action, with exact recommendation
4. **⏳ Pending Watchlist** — watchlist items from portfolio.json (see below) — always shown if watchlist is non-empty
5. **📡 Catalyst Plays** — daily catalyst discovery
6. **💵 Cash deployment** — recommendation from Step 3.7
7. **🔄 Rotation suggestions** — from Step 4, if any
8. **📊 IBKR Intelligence** — broker-sourced analysis section (see design below)
9. **📚 Today's concept** — education, in a colored box
10. **Footer** — disclaimer, `"Prices: IBKR live feed — [timestamp]"`, returns method (TWR/MWR)

**📊 IBKR Intelligence section design:**

Dark card, `background: #0a0f1a; border-left: 3px solid #3b82f6;`. Header: "📊 IBKR Intelligence — [today's date]".

Three sub-blocks rendered side by side (table layout for email compatibility):

**Block 1 — Account Performance (from Step 1.5A):**
```
1D:  [+X.X%]   [green/red badge]
MTD: [+X.X%]   [green/red badge]
YTD: [+X.X%]   [green/red badge]
Method: TWR (or MWR)
```

**Block 2 — Allocation Breakdown (from Step 1.5B):**
Show sector weights as a simple horizontal bar chart using HTML/CSS:
```
Technology     ██████████  X%
Biotechnology  ████████    X%
Cash           ████        X%
```
Flag any sector > 60%: ⚠️ Concentration

**Block 3 — Position Themes (from Step 1.5C):**
For each held ticker, list its top 2 IBKR themes + top 3 peer companies:
```
ANET  →  AI Infrastructure · Data Center Networking
         Peers: CSCO, JNPR, HPE
VERA  →  Rare Disease · Nephrology
         Peers: JNCE, RCKT, FOLD
```
If a Step 3.5 catalyst candidate appears in any position's peer list, add a note: "🔗 [CANDIDATE] is a theme-peer of [HELD TICKER]"

Omit any block where the underlying IBKR call returned empty.

**⏳ Pending Watchlist section design:**

This section is rendered for every item in `watchlist[]`. Skip this section only if `watchlist[]` is empty.

Visual treatment: amber/orange-tinted dark background card (`background: #1a1400; border-left: 3px solid #f59e0b;`). Header: "⏳ Pending — Waiting on IBKR Approval".

For each watchlist item render a compact card containing:

1. **Header row:** Ticker (large, bold) + company name + verdict badge (WATCH in amber / BUY NOW in green) + conviction score (X/10)

2. **Broker blocker banner** (if `broker_blocker` is set): amber pill reading "🔒 [broker_blocker text]" — e.g., "🔒 IBKR application pending — current broker does not allow this stock"

3. **Live price row** (from Step 2.5 fetch):
   - Current price (bold)
   - Target entry: $[entry_target] — and whether it's still accessible: ✅ "Entry still valid" / ⚠️ "Price moved +X% above target — re-check" / 🔴 "Price dropped X% — verify thesis"
   - Stop: $[stop] | TP1: $[tp1] | TP2: $[tp2] — 1 line, compact

4. **Event countdown** (from Step 2.5): "[PDUFA drug] for [indication]" + urgency badge:
   - 🔴 URGENT: X days left — if ≤ 7 days
   - 🟡 SOON: X days left — if 8–14 days
   - 🟢 X days left — if 15–30 days
   - ⚫ Event passed — if pdufa_date < today (note result if known)

5. **Approval probability bar:** horizontal HTML/CSS bar showing [approval_probability_pct]%. Color: green if ≥80%, amber if 60–79%, red if <60%.

6. **Halal status:** ✅ VERIFIED / ⚠️ UNVERIFIED (show the halal_note from portfolio.json) / ❌ FAILS

7. **Notes line:** the `notes` field from portfolio.json — 1–2 lines, muted color

8. **Call to action line** (bottom of card):
   - If broker_blocker is set AND event is still in the future: *"IBKR approval needed before entry. When approved: enter $[position_size_target] at ~$[entry_target], stop $[stop]."*
   - If event is ≤ 7 days out AND broker still not approved: *"🚨 Only [X] days to PDUFA — if IBKR not approved in time, this entry window will close."*
   - If event has passed: *"Event passed. Check outcome and decide whether to remove from watchlist."*

**Price drift warning rule:** If the current price is more than 20% above the entry_target, add a prominent amber banner:
> ⚠️ **Entry window at risk** — [TICKER] has moved from $[entry_target] to $[current_price] (+X%) while waiting on broker approval. The original stop at $[stop] is now [Y]% below current price. Re-run `/stock-analyzer [TICKER]` to re-derive updated levels before entering.

**📡 Catalyst Plays section design:**

This section has a distinct visual treatment — a dark-background card (e.g., `background: #0f1117; border-left: 3px solid #6366f1;`) to make it visually separate from the portfolio review. Header: "📡 Catalyst Plays — [today's date]".

For each of the 3 candidates from Step 3.8, render a compact card:
- Ticker + company name (bold, large)
- Catalyst event + date (with a countdown: "in X days")
- Probability bar — a simple HTML/CSS horizontal bar showing [X]%
- Bull scenario price and % (green)
- Bear scenario price and % (red)
- Expected value on 30% position (bold — this is the headline number)
- Smart money signal (1 line)
- Halal badge (green ✅ / amber ⚠️ / red ❌)
- Conviction badge (INVESTIGATE / WATCH / SKIP) — color-coded
- One-line call to action: *"Say 'analyze [TICKER]' for the full deep dive"*

If a candidate is SKIP: still show it, but render the card with reduced opacity (0.5) and a grey SKIP badge. Abbas should see what was found and why it didn't make the cut — transparency builds trust in the system.

If no catalyst plays found (all 3 are large-cap fallbacks): note it clearly at the top of this section: *"No catalyst plays found today — showing large-cap setups as fallback."*

### Step 7: SEND via GitHub outbox relay

The routine environment blocks outbound HTTP to external webhooks. Instead, write
the email to the GitHub repo — a GitHub Action picks it up and sends via Gmail SMTP.

Use the **GitHub connector** to push **two files** in a single commit to the `abbashm9/portfolio-skills` repo on the `main` branch:

**File 1 — `outbox/email.json`:**
```json
{
  "subject": "<subject line>",
  "html_body": "<full HTML email string>"
}
```

**File 2 — `portfolio.json`:**
Update the `education_tracker` block with today's concept before writing:
```json
"education_tracker": {
  "last_concept_number": <number of concept taught today>,
  "last_concept_name": "<name of concept taught today>",
  "last_taught_date": "<today's date ISO format YYYY-MM-DD>",
  "taught_concepts": [<append concept name to existing array if not already present>]
}
```
All other fields in portfolio.json remain unchanged — only `education_tracker` is modified.

Commit message: `"chore: daily portfolio email"`

The GitHub Action at `.github/workflows/send-email.yml` triggers automatically on
every push to `outbox/email.json` and emails `almadani.abbas@gmail.com` via Gmail SMTP.

If the GitHub connector write fails, fall back to `create_draft` via the Gmail
connector and log **"GITHUB WRITE FAILED — email saved as draft"** in the routine
output.

**Subject line format:**
```
📊 Daily Portfolio: [+X.X% / -X.X%] | [headline event of the day]
```

Examples:
- `📊 Daily Portfolio: +2.75% | NVDA earnings in 5 days`
- `📊 Daily Portfolio: -1.2% | AMD post-earnings fade continues`
- `📊 Daily Portfolio: +0.4% | Quiet session, no actions`

Use Asia/Kuwait timezone for date references.

**Date/day-of-week rule (critical — do not skip):** Whenever you display a date with a day name (e.g., "Monday July 7"), you MUST derive the day name by computing it from the actual calendar date — do not estimate, infer, or count backwards from "today." July 7, 2026 = Tuesday. July 6, 2026 = Monday. Always state the day correctly. Kuwait is UTC+3 and does not observe DST. For US catalyst dates (PDUFA, earnings), the calendar date is the same in Kuwait as in the US (Kuwait is ahead, so a Tuesday in the US is still Tuesday in Kuwait, not Monday). Never subtract a day to "convert" from US to Kuwait — the date label does not change, only the clock time does.

### Step 8: Handle market-closed days

If NYSE was closed today (weekend, US holiday), send a condensed email:
- Subject: `📊 Daily Portfolio: Markets closed | [top catalyst play if found]`
- Body: 1 sentence noting markets were closed, then **still run Steps 3.5 and 3.8 fully** — the FDA calendar and clinical trial readouts don't pause on weekends, and upcoming events are worth knowing about even when the market is closed
- Include the full 📡 Catalyst Plays section
- Skip the positions table and exit alerts (no price movement to report)
- Include the education concept

## Output style rules

- **No fluff** — Abbas reads this fast, every sentence earns its place
- **Numbers always** — when you say something moved, give the number
- **Honest about data gaps** — flag missing/unreliable data, don't paper over it
- **Pre-event decisions** — surface binary decisions early (e.g., NVDA earnings call BY Friday, not the morning of)
- **Education at bottom** — never lead with it

## Special triggers

- **Day before held name's earnings:** highlight the decision (hold/trim/exit before print) prominently in the email
- **Halal compliance breach detected:** override everything else, recommend exit at next open
- **Portfolio down >8% from cost basis:** stop suggesting new entries, defensive review only
- **Portfolio up >20% from cost basis:** suggest taking some profits
- **NYSE holidays:** short closed-market email with education only

## Position updates

When Abbas reports new buys/sells in chat, he should use the **`portfolio-manager` skill** (or any Claude chat will trigger it) — that skill is responsible for updating `portfolio.json`. This daily-portfolio-check skill only READS the file. Never writes to it. The two skills are separated to keep concerns clean:

- `portfolio-manager` — handles updates (buys, sells, deposits, stop changes)
- `daily-portfolio-check` — reads state and produces daily report

If Abbas mentions a trade in conversation with this skill, redirect him: "I'll handle the daily review. To log that trade, just say something like 'I bought X at $Y' and the portfolio-manager skill will record it."

## Reference files

- `references/email-template.md` — HTML email structure with inline CSS
- `references/exit-rules.md` — Detailed exit logic (stops, TPs, catalysts, time-based)
- `references/rotation-playbook.md` — When and how to suggest rotations
- `references/education-curriculum.md` — 30-day learning track with concept-by-concept content guides
- `references/buffett-indicator-history.html` — Designed HTML case studies of every historical episode where the Buffett Indicator exceeded 190%, with drawdown data, timelines, and portfolio implications. Use as macro context when discussing risk environment or cash deployment. Current reading: 232.5% (June 2026). Open in any browser.

## What this skill does NOT do

- Execute trades — Abbas does this in his broker
- Give financial advice — research only
- Daily halal compliance lectures — quarterly check only, no daily education on this
- Generic education — every concept anchors to Abbas's actual portfolio
