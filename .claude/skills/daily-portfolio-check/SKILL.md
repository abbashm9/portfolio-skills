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

## Sources of truth: Yahoo Finance JSON API (prices) + portfolio.json (metadata)

**Price source: Yahoo Finance JSON API via WebFetch — primary for all automated runs.**

The IBKR MCP connector is only available in interactive chat sessions. The Cloud Routine runs on Claude's servers where IBKR is not reachable. Use the Yahoo Finance JSON API as the price source for all automated daily email runs.

**CRITICAL: Do NOT fetch the HTML quote page (`yahoo.com/quote/TICKER`) — it is JavaScript-rendered and WebFetch cannot extract prices from it. Always use the JSON API endpoint:**

```
WebFetch: https://query1.finance.yahoo.com/v8/finance/chart/[TICKER]?interval=1d&range=2d
```

This returns structured JSON. Extract prices from:
```json
response.chart.result[0].meta.regularMarketPrice      → current/closing price
response.chart.result[0].meta.previousClose            → previous close
response.chart.result[0].meta.regularMarketChangePercent → day % change
response.chart.result[0].meta.fiftyTwoWeekHigh         → 52-week high
response.chart.result[0].meta.fiftyTwoWeekLow          → 52-week low
response.chart.result[0].meta.regularMarketVolume       → volume
```

**Fallback if query1 is blocked:** try `https://query2.finance.yahoo.com/v8/finance/chart/[TICKER]?interval=1d&range=2d` (same structure, alternate host).

**Fallback if both are blocked:** try `https://stooq.com/q/l/?s=[TICKER].US&f=sd2op` which returns CSV: Date, Open, Close. Use the Close value.

This is deterministic (one URL = one ticker's exact data) and far more reliable than fetching the HTML quote page or using web search. **Always use this method — never estimate or use search results for prices.**

Flag every price in the email with: `"Prices: Yahoo Finance JSON API — [fetch timestamp]"`

If all Yahoo Finance endpoints return no price: label that position "⚠️ PRICE UNAVAILABLE — check broker app manually." Do NOT guess or estimate.

**IBKR in chat mode:** When the skill is triggered interactively (not as a routine), IBKR MCP tools ARE available. In that case, use IBKR as the primary source (more accurate, real-time) and fall back to Yahoo Finance only if IBKR fails. Display which source was used in the email footer.

**portfolio.json is the source of truth for strategy metadata:**

| Data | Source |
|------|--------|
| Live prices, day change | Yahoo Finance WebFetch (routine) / IBKR (interactive) |
| Stops, TPs, catalysts, notes | GitHub `portfolio.json` |
| Watchlist, education tracker | GitHub `portfolio.json` |
| Cash balance | `portfolio.json` `cash_available` field (routine) / IBKR (interactive) |

If portfolio.json is unreachable: proceed with Yahoo Finance prices but note "⚠️ portfolio.json unavailable — stops, TPs, and catalyst data missing. Metadata sections skipped."

## Workflow — every daily check

### Step 0: Pull live data

**Run both in parallel — BEFORE anything else.**

**0A — Live prices via Yahoo Finance JSON API (WebFetch):**

For each ticker in portfolio.json positions[] and watchlist[], fetch:
```
https://query1.finance.yahoo.com/v8/finance/chart/[TICKER]?interval=1d&range=2d
```

This returns JSON. Extract from `response.chart.result[0].meta`:
- `regularMarketPrice` → current/closing price
- `previousClose` → previous close  
- `regularMarketChangePercent` → day % change
- `fiftyTwoWeekHigh` / `fiftyTwoWeekLow` → 52-week range
- `regularMarketVolume` → volume

Fetch all tickers in parallel. If query1 is blocked, try query2 (same URL, replace `query1` with `query2`). If both blocked, try stooq: `https://stooq.com/q/l/?s=[TICKER].US&f=sd2op` (CSV → use Close column). Store per ticker.

**If running interactively with IBKR available:** use `get_account_positions` and `get_account_balances` for live P&L and share counts. Still fetch Yahoo Finance for watchlist tickers not in IBKR.

From portfolio.json positions[]: use `shares`, `entry_price`, `cost_basis` as the position metadata.
Calculate per position:
- `market_value` = shares × current_price
- `unrealized_pnl` = (current_price − entry_price) × shares
- `unrealized_pnl_pct` = unrealized_pnl / cost_basis × 100
- `daily_pnl` = shares × (current_price − previous_close)

**0B — GitHub portfolio.json (metadata):**
Fetch from:
```
https://raw.githubusercontent.com/abbashm9/portfolio-skills/main/portfolio.json
```

Extract:
- `positions[]` — shares, entry_price, cost_basis, stop_loss, tp1, tp2, catalyst, catalyst_date, approval_probability_pct, halal_note, notes
- `cash_available` — use as the cash balance
- `watchlist[]` array
- `investment_goal`
- `education_tracker`
- `last_updated` timestamp

**Reconciliation (interactive mode only):** If IBKR shows a different share count than portfolio.json, trust IBKR and flag: "⚠️ [TICKER]: IBKR shows [X] shares, portfolio.json shows [Y] — portfolio.json is stale. Run portfolio-manager to sync."

### Step 1: Validate prices

After fetching all prices, run this sanity check per position:
- If current_price differs from entry_price by more than 50% in either direction AND no recent catalyst explains it: flag "⚠️ Price looks suspicious — verify manually"
- If Yahoo Finance returns no price: label "⚠️ PRICE UNAVAILABLE"

Never fill in a missing price with an estimate or training data. N/A is better than wrong.

### Step 1.5: IBKR Market Intelligence (interactive mode only)

These calls require IBKR MCP and are skipped in automated routine mode. If running interactively:

**1.5A — Account Performance:**
```
get_pa_performance_all_periods
```
Returns 1D, MTD, YTD % returns (TWR or MWR). Use in the email hero section.

**1.5B — Portfolio Allocation:**
```
get_pa_allocation → type: "ALL"
```
Sector weights for the Intelligence section.

**1.5C — Investment Themes per Position:**
```
get_company_themes → contract_id, max_themes: 3, max_companies: 5
```
Top 2 themes + peer companies per position.

**1.5D — Investment Topic Search:**
```
search_investment_topics → query: "[primary theme keyword]"
```
Use to enrich Step 3.5 catalyst radar.

All 1.5 results are non-blocking. If unavailable (routine mode), omit the IBKR Intelligence section from the email and note: "📊 IBKR Intelligence — unavailable in routine mode. Run daily check in chat for full broker analytics."

### Step 2: Build the data tables and investment goal tracker

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

### Step 2.5: Watchlist tracking — fetch live prices for watchlist items

Already done in Step 0A. For each watchlist item, calculate:
- **Days to event:** `pdufa_date − today` in calendar days
- **Price vs entry target:** `(current_price − entry_target) / entry_target × 100`
- **Entry still valid?** If current_price > entry_target × 1.15: "ENTRY MOVED — re-analyze before buying". If current_price < entry_target × 0.90: "PRICE DROPPED — check thesis still intact".
- **Event urgency:** ≤ 7 days → 🔴 URGENT. 8–14 days → 🟡 SOON. 15–30 days → 🟢 WATCH.

### Step 2.6: Active Position News Scan — enhanced monitoring

**Run in parallel with Step 2.5.** Applies to every position with `"enhanced_news_watch": true` in portfolio.json. Runs every day until that position is closed (removed from positions[]).

**Purpose:** Surface any news that could change the thesis, signal early action, or require same-day response for binary-event positions. Nothing gets missed.

#### 2.6A — For each `enhanced_news_watch: true` position, run 4 targeted searches in parallel

**For CAPR / any AdCom-PDUFA position:**
```
"[TICKER]" OR "[drug name]" news [today's date] OR yesterday FDA advisory OR briefing OR analyst
"[TICKER]" FDA "briefing document" OR "background material" OR "advisory committee" [current month] 2026
"[TICKER]" analyst OR "price target" OR upgrade OR downgrade [this week] 2026
"[drug name]" "[indication]" competitor OR "competing drug" OR "same class" data OR CRL [current month] 2026
```

**For VERA / any post-approval confirmatory trial position:**
```
"VERA" OR "Vera Therapeutics" OR "atacicept" OR "TRUTAKNA" news [today's date] OR yesterday
"ORIGIN 3" OR "eGFR" OR "IgA nephropathy" confirmatory OR "full approval" data 2026
"Vera Therapeutics" analyst OR "price target" OR upgrade OR downgrade [this week] 2026
"IgA nephropathy" competitor OR "same class" OR "sparsentan" OR "iptacopan" data [current month] 2026
```

#### 2.6B — Classify every finding

| Priority | Type | Action |
|---|---|---|
| 🚨 URGENT | FDA early action, briefing docs released, CRL signal, major competitor approval/CRL in same indication | Lead the email — surface ABOVE the hero banner |
| ⚠️ WATCH | Analyst rating change, label expansion filing, competitor Phase 3 result, publication | Dedicated news section after macro card |
| ℹ️ FYI | Routine press release, conference attendance | 1-line mention only |
| — | Nothing new | Write "No material news for [TICKER] today." |

#### 2.6C — Email output format

Insert a **📰 POSITION NEWS** section immediately after the Macro Context card and before the Positions table. Always render it — even if empty — so Abbas knows the scan ran.

```
📰 POSITION NEWS — [today's date]

🔵 CAPR — [finding, or "No material news today."]
[1-2 sentences if something found. Source link. Action implication.]

🟢 VERA — [finding, or "No material news today."]
[1-2 sentences if something found. Source link. Action implication.]
```

**If 🚨 URGENT news found:** move it to the VERY TOP of the email, above the hero banner, in a red alert box:
```
🚨 URGENT — [TICKER]: [headline]
[2-sentence summary of what happened and what it means for the position.]
[Action: HOLD / CUT NOW / WAIT FOR MORE INFO]
```

#### 2.6D — Special: July 25 FDA Briefing Documents (CAPR)

On or after July 25, 2026, the FDA releases its internal briefing documents for the CAPR AdCom (July 29). These are the single most important signal before the vote.

Run these searches on July 25 and every day after until the AdCom:
```
"Capricor" OR "deramiocel" OR "CAP-1002" FDA "briefing document" OR "background material" July 2026
site:fda.gov deramiocel "advisory committee" briefing 2026
```

If briefing documents are found:
- Summarize FDA's stance on HOPE-3 data and the 2.4% LVEF improvement
- **If FDA appears supportive:** recommend HOLD through AdCom
- **If FDA is clearly skeptical:** recommend CONSIDER CUTTING before the AdCom vote to limit downside
- Mark as 🚨 URGENT and place above hero banner

If not yet available: note "FDA briefing docs not yet released — expected July 25."

### Step 2.7: Previous Day Movers — top gainers and losers

**Run in parallel with Step 2.5.** Mandatory daily section — not optional, not skipped on weekends.

**Purpose:**
1. Understand what the market rewarded and punished yesterday
2. Catch actionable names still in motion (gap-and-go continuation, follow-through day 2)
3. Check contagion — did any loser's cause affect your holdings or watchlist?

#### 2.7A — Fetch the movers (4 searches in parallel)

```
"top percentage gainers" small cap yesterday OR [previous trading date] NYSE NASDAQ site:finviz.com OR "percent gain"
"biggest stock gainers" "50 percent" OR "100 percent" OR "200 percent" [previous trading date] 2026 small cap catalyst
"top stock losers" small cap yesterday OR [previous trading date] NYSE NASDAQ "down percent"
"stocks down 30 percent" OR "stocks down 50 percent" [previous trading date] reason catalyst small cap
```

Target: top 10 gainers (by % gain) and top 10 losers (by % loss) for the previous trading day. **Minimum threshold: ≥ 20% move. Anything under 20% is noise — exclude it.** Large-cap stocks (market cap > $5B) moving less than 20% are explicitly excluded — Abbas wants NXTC +200%, CNEY +58%, VEEE +54% type movers, not Meta or NVIDIA on a typical good session. Sort all results by % move descending before any further filtering.

#### 2.7B — Identify the reason (1 search per mover, all in parallel)

For each mover, run:
```
"[TICKER]" [previous date] OR yesterday reason gain OR loss earnings OR FDA OR contract OR upgrade OR downgrade OR guidance
```

Classify each move:
- **FDA** — PDUFA approval, CRL, AdCom result, label expansion
- **Earnings** — beat/miss, guidance raise/cut, revenue surprise
- **Contract/Deal** — government contract, M&A, partnership, licensing
- **Analyst** — upgrade/downgrade, price target change, initiation
- **Macro/Sector** — sector ETF rotation, interest rate move, geopolitical
- **Short squeeze** — high short interest + positive catalyst
- **Technical** — breakout, index rebalancing, no clear fundamental reason
- **Unknown** — no identifiable catalyst found

#### 2.7C — Build the movers table

**LARGE-CAP FILTER (apply first, before any other analysis):** Drop every mover where market cap > $5B AND move < 20%. Large-cap names on a normal session are index noise, not opportunity. If Meta, NVIDIA, Apple, or any other mega-cap appears in raw results at +4-8%, remove it before building the table. This section is exclusively for small/micro-cap movers that Abbas would otherwise miss — the NXTC +201%, CNEY +58%, VEEE +54% class. Only names passing this filter proceed to the table.

For each mover that passes the filter, determine:
- **Still actionable?** Flag as ✅ RUNNABLE or ❌ FADED. RUNNABLE = catalyst-driven + more runway. FADED = one-day spike on no ongoing catalyst.
- **Contagion check:** Does the loser's reason affect any current positions or watchlist tickers? Same sector? Same drug class?
- **Halal quick check** (gainers only, if actionable): Drop if forbidden business.

#### 2.7D — Email output format

**MANDATORY: This section MUST always appear in the email.** Even if searches returned nothing useful, or no mover cleared 20%, still render the section header and a fallback note. Never omit this section entirely.

**📈 Top Gainers — [previous trading date]**

| Ticker | +% | Catalyst | Type | Still in play? |
|---|---|---|---|---|
| TICKER | +X% | [1-line reason] | FDA / Earnings / Deal / Squeeze | ✅ RUNNABLE — [why] / ❌ FADED |

Show top 5 gainers sorted by % move descending (highest first), minimum ≥ 20%. If a gainer is RUNNABLE and halal-clean, add:
> 🔔 **[TICKER] still running** — [1-line thesis for continuation]. Say `analyze [TICKER]` for the full setup.

**If no gainer cleared ≥20%:** show:
> *No small-cap gainers found clearing the 20% threshold for [date]. Market was quiet or search returned insufficient data. Large-cap movers (META +6%, NVDA +4%) excluded by design — see "Large-cap on deck" section for those.*

**📉 Top Losers — [previous trading date]**

| Ticker | -% | Catalyst | Type | Contagion to your portfolio? |
|---|---|---|---|---|
| TICKER | -X% | [1-line reason] | CRL / Miss / Cut / Downgrade | ⚠️ Affects [HELD TICKER] because [reason] / None |

Show top 5 losers sorted by % move descending (largest drop first), minimum ≥ 20%. If contagion exists, add:
> ⚠️ **[LOSER] CRL may signal sector headwind for [HELD/WATCHLIST TICKER]** — [1-line explanation].

**If no loser cleared ≥20%:** show:
> *No small-cap losers found clearing the 20% threshold for [date].*

**On weekends:** use Friday's movers data. Label clearly: "📈 Friday's Movers — [date]"

#### 2.7E — Pattern extraction: inject learnings into today's catalyst scan

For every gainer ≥ 20%, run:
```
"[TICKER]" "unusual options" OR "Form 4" OR "short interest" OR "analyst initiation" OR "contract" [2-4 days before the move date]
```

Extract the precursor pattern and feed it into Step 3.5.1 searches for today:
- Big gainer preceded by unusual options → add `"[SAME SECTOR]" "unusual call buying" OR "sweep" [today]` to Step 3.5.1
- Big gainer on earnings beat → add `"[PEER TICKERS]" earnings [month] guidance` to Step 3.5.1
- Big gainer on sector rotation → add `[SECTOR ETF] inflows [today]` to Step 3.5.1

**In the email:** add under each big gainer:
> 🔍 **Precursor signal:** [what smart money was doing 1-3 days before] — scanning for same pattern in [SECTOR/PEERS] today.

### Step 2.8: Large-cap earnings & catalyst watch

**Run in parallel with Step 2.7.** This is a mandatory daily section — separate from movers, separate from catalyst plays.

**Purpose:** Surface mega-cap setups (AAPL, MSFT, NVDA, META, AMZN, GOOG, TSLA, AMD, AVGO, TSM, LLY, and any other name >$50B market cap) where there's a tradeable catalyst coming up — earnings, product launch, analyst day, major contract. These names rarely move 20%+ on a single day but can be exceptional pre-earnings entries or rotation targets. They never appear in the Movers section for that reason.

#### 2.8A — Fetch the upcoming large-cap events (3 searches in parallel)

```
"earnings date" NVDA OR META OR AAPL OR MSFT OR AMZN OR GOOG OR TSLA OR AMD OR AVGO OR TSM [current month] [next month] 2026
"earnings date" LLY OR JNJ OR PFE OR MRK OR ABBV OR BMY large cap pharma [current month] [next month] 2026
mega cap "catalyst" OR "product launch" OR "analyst day" OR "investor day" OR "AI announcement" [current month] [next month] 2026
```

Target: identify which mega-caps have earnings within the next 21 days. Focus on names where there's a directional thesis — either a strong expected beat, a guidance raise, a new product reveal, or a sector tailwind.

#### 2.8B — For each name with an event ≤ 21 days, run 1 quick search

```
"[TICKER]" earnings [date] consensus estimate "beat" OR "guidance" OR "AI" OR "data center" OR "revenue" 2026
```

Produce a 1-line setup note per name. You are looking for pre-earnings entry opportunities — not post-event analysis.

#### 2.8C — Email output format

Keep this section tight — it's a radar, not a deep dive. 3–5 names max.

**🏢 Large-cap on deck — next 21 days**

| Ticker | Event | Date | Setup in 1 line | Implied move | Direction |
|---|---|---|---|---|---|
| NVDA | Earnings | Jul 23 | AI data center demand accelerating; Jensen guidance track record | ±X% | 🟢 Bullish / 🔴 Bearish / ⚪ Neutral |
| META | Earnings | Jul 30 | Ad revenue reacceleration, AI capex update | ±X% | 🟢 Bullish |
| ... | | | | | |

**Implied move:** Use the options market implied move if findable via search (`"[TICKER]" "implied move" earnings 2026`). If not findable, estimate: large-cap tech typically ±5-10% on earnings.

**Direction:** Your read based on the 1-line search — is the setup leaning bullish, bearish, or genuinely 50/50? Don't manufacture a view where you don't have one.

**Below the table, for any name with a 🟢 Bullish tag**, add a callout:
> 💡 **[TICKER] earnings [date]** — [1-line entry thesis]. Pre-earnings entry: buy X days before, exit before print OR hold through. Say `analyze [TICKER]` for full setup with entry/stop/TP.

**On weekends:** still run this section using the same event calendar. Upcoming events don't pause on weekends.

### Step 2.9: Macro context — Buffett Indicator & market temperature

**Run once per email, in parallel with Steps 2.7 and 2.8.** Always shown — never skipped, including weekends.

**Purpose:** Give Abbas the big picture every morning. A single macro read that frames everything else in the email — are we in a historically expensive market or a cheap one? Is the macro environment supporting his aggressive growth strategy, or is it raising a red flag?

#### 2.9A — Fetch the current Buffett Indicator reading (2 searches in parallel)

```
Buffett Indicator "total market cap" GDP ratio current 2026 site:currentmarketvaluation.com OR site:longtermtrends.net
"Wilshire 5000" GDP ratio current level 2026 market valuation
```

Extract:
- **Current reading** (e.g., "232.5%") — the ratio of total US stock market cap to GDP
- **Trend** — up or down from last month/quarter
- **Historical context** — which zone is it in? (see thresholds below)

**MANDATORY FALLBACK — this section MUST always appear in the email, even if searches return nothing.**

If the search doesn't return a precise number, use this hardcoded fallback and display the card anyway:
- Reading: **232.5%** (last known: June 2026)
- Zone: 🔴 ALL-TIME EXTREME
- Flag it as: "⚠️ Live fetch failed — showing last known reading (June 2026: 232.5%). Verify at currentmarketvaluation.com."

Do NOT skip this section. Do NOT omit the card. The email must always contain the macro context card — a failed web search is not a reason to hide the big picture from Abbas. Show the fallback card with the ⚠️ flag and he can verify manually.

**Historical zone thresholds:**
| Reading | Zone | Historical signal |
|---|---|---|
| < 100% | Undervalued | Rare — major crash aftermath |
| 100–130% | Fair value | Normal / slightly elevated |
| 130–160% | Moderately overvalued | Caution warranted |
| 160–190% | Significantly overvalued | Elevated crash risk |
| > 190% | Extreme / danger zone | Every reading above this has preceded a major drawdown |
| > 220% | All-time extreme | Current territory — historically unprecedented |

#### 2.9B — One additional macro search (optional but always attempted)

```
S&P 500 "forward P/E" current 2026 vs historical average "overvalued" OR "expensive"
```

Extract: current S&P 500 forward P/E vs historical average (15–17x). Gives a second macro data point to confirm or contradict the Buffett Indicator reading.

#### 2.9C — Email output format

Compact dark card, shown near the top of the email — right after the hero banner, before the positions table. It's the first thing Abbas reads to calibrate the whole session.

**Visual treatment:** `background: #0d0d0d; border-left: 3px solid #f59e0b; padding: 12px;`

```
🌍 MACRO CONTEXT — [today's date]

Buffett Indicator:  [X]%   [zone badge]
S&P Forward P/E:    [X]x   [vs. avg: 16x]
Trend:              [↑ Rising / ↓ Falling / → Flat]

[1-sentence plain-English interpretation]
[1-sentence implication for Abbas's strategy]
```

**Zone badges (colored pills):**
- ≥ 220%: 🔴 ALL-TIME EXTREME
- 190–220%: 🔴 DANGER ZONE  
- 160–190%: 🟠 SIGNIFICANTLY OVERVALUED
- 130–160%: 🟡 MODERATELY OVERVALUED
- 100–130%: 🟢 FAIR VALUE
- < 100%: 🟢 UNDERVALUED

**The 1-sentence interpretation** should be direct and contextual — not generic. Examples:
- At 232%: *"Market cap is 2.3× the entire US economy — historically, every reading this high has preceded a multi-year bear market."*
- At 145%: *"Moderately elevated but not extreme — typical bull market territory, no immediate red flag."*
- Falling trend: *"Reading dropped 8 points this month — market pulling back toward fair value, reduces systemic risk."*

**The 1-sentence implication** ties it directly to Abbas's strategy:
- In danger zone: *"Maintain stop-losses strictly — a correction from here could be fast and steep."*
- In fair value zone: *"Macro supports staying invested — focus on stock-specific catalysts."*
- Rising fast: *"Consider keeping some cash dry; if the market corrects hard, you want to buy the dip."*

**Historical reference note** (1 line, grey text at bottom of card):
> *Last historical episodes at this level: [2000 dot-com peak, 2021 COVID bubble peak] — see buffett-indicator-history.html for full case studies.*

This card takes 3 seconds to read and gives Abbas the macro frame for the entire email. Everything else — position decisions, catalyst plays, cash deployment — should be read through this macro lens.

### Step 3: Exit-strategy check per position (in order)

1. **Halal compliance** — quarterly check, not daily, but flag if breaking news suggests a change
2. **Stop-loss** — Below stop? 🚨 ALERT. Within 2% of stop? ⚠️ WATCH.
3. **TP1/TP2/TP3 — validate and re-derive if stale** (see below)
4. **Catalyst proximity** — within 5 trading days? Flag prominently
5. **Time-based** — flat ±3% for 30+ days, no catalyst? Consider trim
6. **Parabolic warning** — up >40% in 30 days, RSI >80? Mean-reversion risk

**Stop and TP level validation — runs on EVERY position, EVERY day.**

For each position, run these two searches in parallel:
- `"[TICKER]" support "swing low" OR "200-day" OR "50-day" OR "key level" [current month]`
- `"[TICKER]" resistance OR "prior high" OR "52-week high" OR "analyst target" OR "price target" [current month]`

**Stop derivation:** Find the most recent real support level below current price. Place stop just below it (1–3%). Confirm or replace the stored portfolio.json stop based on real market structure.

**TP derivation:** Find real resistance above current price. Confirm or replace stored TPs. Show up to 3 TP levels ranked by proximity.

**Format:**
> **[TICKER]** | Stop: $[real level] ([reason]) | TP1: $[real level] ([reason]) | TP2: $[real level] ([reason])

Status emoji: ✅ HOLD / ⚠️ WATCH / 🔔 ACTION / 🚨 ALERT

### Step 3.5: Catalyst Discovery — full market scan

**Purpose:** Surface small/mid-cap names with imminent catalysts across the ENTIRE market — earnings beats, AI contract wins, FDA events, short squeezes, sector momentum plays. Find stocks about to move 30–60% in any sector.

#### 3.5.1 — Cast the net (30 searches in parallel)

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

**Sector balance rule:** Top 3 final candidates must not all be from the same sector. If all biotech, promote highest-scoring non-pharma into third slot.

#### 3.5.2 — Rapid 3-gate pre-screen

- **Gate 1:** Confirmed catalyst date ≤ 45 days? No confirmed date → drop.
- **Gate 2:** Market cap < $2B? ≥ $2B → drop.
- **Gate 3:** Halal quick check. Obvious forbidden business → drop. Unclear → keep with ⚠️.

#### 3.5.3 — Score survivors (5-point pre-score)

| Factor | Points |
|---|---|
| Event ≤ 14 days out | 2 |
| Event 15–45 days out | 1 |
| Short interest ≥ 15% float | 1 |
| Appears in 2+ search sources OR categories | 1 |
| Smart money signal (insider buy, unusual options, 13F) | 1 |

Keep top 3, enforce sector balance. Feed into Step 3.8, 3.7, 4.

### Step 3.8: Condensed analysis — top candidates from Step 3.5

For each of the top 3 candidates, run 5 searches in parallel:
- `"[TICKER]" earnings date OR PDUFA OR catalyst confirmed [current month] [next month]`
- `"[TICKER]" market cap float short interest`
- `"[TICKER]" revenue growth OR "earnings history" OR "beat estimates" OR "phase 3" history`
- `"[TICKER]" balance sheet OR "cash position" OR dilution OR debt 2026`
- `"[TICKER]" insider buying OR "Form 4" OR institutional 13F OR "analyst target" 2026`

For each candidate, produce this block in the email:

---

> **🔬 [TICKER] — [COMPANY NAME]** `[SECTOR / CATALYST TYPE]`
> **Catalyst:** [event type] on [exact date] — [X] days away
> **Market cap:** $[X]M | **Float:** $[X]M | **Short interest:** [X]%
>
> **Edge:** [1-line reason — specific setup]
>
> **Probability:** [X]% — [1-line rationale]
>
> **Scenarios:**
> - ✅ If positive: ~$[price] (+[%]) — [real level reason]
> - 💀 If negative: ~$[price] (-[%]) — [real level reason]
> - Expected value on 30% position (~$[amount]): **+$[EV] / -$[EV]**
>
> **Smart money:** [insider buys / unusual options / institutional buildup / none visible]
> **Key risk:** [the one thing that kills this trade]
>
> **Halal:** ✅ Clean / ⚠️ Unverified / ❌ Fails
>
> **Conviction: [X]/5** → [INVESTIGATE / WATCH / SKIP]
> *Run `analyze [TICKER]` for the full 8-section deep dive before entering.*

---

**INVESTIGATE** = pre-score 4–5, halal clear, event ≤ 14 days
**WATCH** = pre-score 3, or event 15–45 days, or halal unverified
**SKIP** = pre-score ≤ 2, or halal fails, or no confirmed date

### Step 3.6: Risk-score current holdings

Calculate per position:
- **Valuation Risk** (40%): Forward P/E, P/S, P/B, PEG vs sector norms
- **Growth Risk** (35%): revenue trend, margin direction, binary events
- **Financial Health Risk** (25%): D/E, ROE, cash/debt
- **Overall score** → LOW (0–30) / MODERATE (31–50) / HIGH (51–70) / EXTREME (71–100)

Output per-position summary:
> `[TICKER] | [SCORE]/100 | [LABEL] | [1-line driver]`

HIGH/EXTREME feeds into Step 4 as rotation candidate.

### Step 3.7: Cash deployment recommendation (mandatory when cash > $6)

Use `cash_available` from portfolio.json. Deployable = `cash_available − $2` (reserve $1 + buy commission $1).

If `cash_available − $2 < $30`: "Too small for a meaningful new position. Holding as dry powder."

If `cash_available − $2 ≥ $30`, always provide:
> 💵 **Cash deployment — $[deployable] available**
> - **Option A — Catalyst play:** [TOP CANDIDATE], buy [N] shares at ~$[price]. Event: [date]. Upside: +[%]. Downside: [%]. Position: $[amount] = [%]% of portfolio.
> - **Option B — Add to existing:** [TICKER] (Risk: [score]/100), buy [N] shares at ~$[price]. Net position: [shares] shares, avg ~$[blended].
> - **Recommended:** [A or B] because [1-line reason].
> - **Your call.**

Max allocation per catalyst play: 30% of total portfolio value.

### Step 4: Rotation suggestions (intelligence-driven)

Propose moves when:
- Position hits TP1/TP2 → suggest redeployment target from Step 3.5
- New high-conviction name has near-term catalyst → suggest trimming a winner
- Position is dead money (flat 30+ days) → suggest rotation
- Pre-binary-event (within 5 days) → suggest risk-management trim

Format: exact shares to sell, exact $ freed, exact shares to buy, 1-line rationale, 1-line risk, "Your call."

### Step 5: Select today's education concept

Read `education_tracker` from portfolio.json.
- **Priority 1:** Term appeared in today's report → teach that concept (if not yet taught)
- **Priority 2:** Teach `last_concept_number + 1`. Wrap to 1 after 30.

Format: ONE concept, ~80–120 words, trader-to-trader voice, anchored to Abbas's actual positions. Place at the bottom.

### Step 6: Generate the HTML email

Build a responsive HTML email. Requirements:
- Inline CSS only
- Tables for layout
- Color-coded status badges
- Hero banner with total P&L (green/red)
- Education section in colored box at bottom
- Footer with disclaimer in 10px grey

**Email section order (top to bottom):**

1. **Hero banner** — total P&L + 1D/MTD/YTD returns (from IBKR if available, else calculate from Yahoo Finance prices), investment goal tracker
2. **🌍 Macro context** — Buffett Indicator + S&P forward P/E from Step 2.9 (ALWAYS shown)
3. **📰 Position News** — from Step 2.6, shown only when `enhanced_news_watch` positions exist. 🚨 URGENT news overrides all ordering and goes above the hero banner.
4. **⚠️ MANDATORY — Positions snapshot table** — ONE ROW PER POSITION: Status badge | Ticker | Close price | Day % | P&L $ | P&L % | then TOTAL row. NEVER omit this table, including weekend emails.
5. **Exit alerts** — any position needing action
6. **📈📉 Yesterday's Movers** — from Step 2.7 (always shown; Friday data on weekends) — small-cap ≥20% moves only
7. **🏢 Large-cap on deck** — from Step 2.8, mega-cap earnings/catalyst radar (show when any name has event ≤21 days; omit if calendar is empty)
8. **⏳ Pending Watchlist** — all watchlist items from portfolio.json (skip only if empty)
9. **📡 Catalyst Plays** — top 3 candidates from Step 3.8
10. **💵 Cash deployment** — from Step 3.7
11. **🔄 Rotation suggestions** — from Step 4, if any
12. **📊 IBKR Intelligence** — if available (interactive mode only); otherwise omit with note
13. **📚 Today's concept** — education, in a colored box
14. **Footer** — disclaimer, `"Prices: Yahoo Finance — [timestamp]"` (or IBKR if used), returns method

**⏳ Pending Watchlist section design:**

Amber/orange card (`background: #1a1400; border-left: 3px solid #f59e0b;`). Header: "⏳ Pending Watchlist".

For each watchlist item:
1. Ticker + company name + verdict badge + conviction score
2. Broker blocker banner if set
3. Current price (from Yahoo Finance) + entry target comparison + stop/TP levels
4. Event countdown with urgency badge (🔴 ≤7 days / 🟡 8–14 / 🟢 15–30 / ⚫ passed)
5. Approval probability bar
6. Halal status
7. Notes from portfolio.json
8. Call to action

Price drift warning: if current_price > entry_target × 1.20, add:
> ⚠️ **Entry window at risk** — [TICKER] has moved +X% above target. Re-run `analyze [TICKER]` to re-derive levels before entering.

**📡 Catalyst Plays section design:**

Dark card (`background: #0f1117; border-left: 3px solid #6366f1;`). Header: "📡 Catalyst Plays — [today's date]".

Per candidate: Ticker + company (bold), catalyst + date + countdown, probability bar, bull/bear scenarios, EV on 30% position, smart money signal, halal badge, conviction badge, call to action.

SKIP candidates shown at 0.5 opacity with grey badge.

**📊 IBKR Intelligence section (interactive mode only):**

Dark card (`background: #0a0f1a; border-left: 3px solid #3b82f6;`). Three columns: Account Performance (1D/MTD/YTD), Allocation Breakdown (sector bar chart), Position Themes (top 2 themes + peer tickers per position).

If unavailable (routine mode): show a single-line note: "📊 IBKR Intelligence — not available in routine mode. Trigger daily check in chat for full broker analytics."

### Step 7: SEND via GitHub outbox relay

Use the **GitHub connector** to push **two files** in a single commit to `abbashm9/portfolio-skills` on `main`:

**File 1 — `outbox/email.json`:**
```json
{
  "subject": "<subject line>",
  "html_body": "<full HTML email string>"
}
```

**File 2 — `portfolio.json`:**
Update `education_tracker` only:
```json
"education_tracker": {
  "last_concept_number": <number>,
  "last_concept_name": "<name>",
  "last_taught_date": "<YYYY-MM-DD>",
  "taught_concepts": [<append if not already present>]
}
```

Commit message: `"chore: daily portfolio email"`

The GitHub Action at `.github/workflows/send-email.yml` emails `almadani.abbas@gmail.com` via Gmail SMTP on every push to `outbox/email.json`.

If GitHub write fails: fall back to `create_draft` via Gmail connector. Log "GITHUB WRITE FAILED — email saved as draft."

**Subject line format:**
```
📊 Daily Portfolio: [+X.X% / -X.X%] | [headline event of the day]
```

**Date/day-of-week rule:** Always compute day names from the calendar — never estimate. Kuwait is UTC+3, no DST. US catalyst dates use the same calendar date in Kuwait.

### Step 8: Handle market-closed days

If NYSE was closed today (weekend, US holiday):
- Subject: `📊 Daily Portfolio: Markets closed | [top catalyst play if found]`
- Note that markets were closed, then **run Steps 3.5 and 3.8 fully** — FDA calendar doesn't pause on weekends
- Include full 📡 Catalyst Plays section
- Skip positions table and exit alerts
- Include education concept

## Output style rules

- **No fluff** — Abbas reads this fast, every sentence earns its place
- **Numbers always** — when you say something moved, give the number
- **Honest about data gaps** — flag missing/unreliable data, don't paper over it
- **Pre-event decisions** — surface binary decisions early
- **Education at bottom** — never lead with it

## Special triggers

- **Day before held name's earnings:** highlight hold/trim/exit decision prominently
- **Halal compliance breach detected:** override everything else, recommend exit at next open
- **Portfolio down >8% from cost basis:** stop suggesting new entries, defensive review only
- **Portfolio up >20% from cost basis:** suggest taking some profits
- **NYSE holidays:** short closed-market email with education only

## Position updates

When Abbas reports new buys/sells in chat, redirect to portfolio-manager skill. This skill only READS portfolio.json — never writes to it (except education_tracker in Step 7).

## Reference files

- `references/email-template.md` — HTML email structure with inline CSS
- `references/exit-rules.md` — Detailed exit logic
- `references/rotation-playbook.md` — When and how to suggest rotations
- `references/education-curriculum.md` — 30-day learning track
- `references/buffett-indicator-history.html` — Historical Buffett Indicator episodes. Current reading: 232.5% (June 2026). Open in any browser.

## What this skill does NOT do

- Execute trades — Abbas does this in his broker
- Give financial advice — research only
- Daily halal compliance lectures — quarterly check only
- Generic education — every concept anchors to Abbas's actual portfolio
