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
- **Halal compliance:** AAOIFI standards (verify quarterly, but don't include daily halal education — he doesn't want this)
- **Disclosure:** Research, not financial advice

## Transaction cost framework

**Broker commission:** $3.00 per trade (buy or sell). Entry commission already paid — only exit commission ($3) remains on open positions. Round-trip total = $6.

### Rules that override all exit suggestions

1. **Minimum profit threshold for any sell/trim:** Gross P&L on the shares sold must exceed $3 (the exit commission). Entry cost already sunk.
   - Formula: `(current_price − entry_price) × shares_to_sell > $3`
   - If the result is ≤ $3: show the math, label it "HOLD (commission eats profit)", move on.

2. **Minimum profit threshold for a rotation:** Full round-trip costs $6 (sell $3 + buy $3). Expected gain from the new position must justify $6 in friction.
   - If the rotation doesn't clear $6 in projected upside: skip it or note "commission drag too high for this move."

3. **Small positions (<$75 market value):** Never suggest a partial trim. The position is too small to split — either hold or exit fully.
   - Example: a $70 position trimmed 50% frees ~$35 but the $3 exit commission is ~9% of proceeds.

4. **Always show net P&L:** In every sell, trim, or rotation suggestion, display both gross and net:
   - `Gross: +$18.40 | Exit commission: −$3.00 | Net: +$15.40`
   - Never present a gross P&L without the commission line.

5. **Cash deployment minimum:** Don't suggest buying into a new position if the cash being deployed (after commission) would result in a position worth < $30. Too small to be meaningful.

## Source of truth: portfolio.json

**The portfolio is NOT hardcoded in this skill.** Read it fresh at the start of every run from the GitHub repo:

```
https://raw.githubusercontent.com/abbashm9/portfolio-skills/main/portfolio.json
```

If the routine has GitHub connector access, use it. Otherwise fetch via web_fetch on the raw URL above (works for public repos).

The file structure includes:
- `positions[]` — list of holdings with shares, entry, stops, TPs, catalysts
- `cash_available` — uninvested USD
- `total_cost_basis` — total invested
- `totals` — concentration warnings, sectors, etc.
- `history` — past transactions for context

Use this data dynamically. If a position has been added since the last run, include it. If one has been sold, exclude it. **Never use stale hardcoded data — always read the file.**

If the file can't be read for any reason (repo down, file deleted, JSON malformed):
1. STOP the run
2. Email Abbas a short notice: "⚠️ portfolio.json could not be read — daily check skipped. Please verify the file exists at https://github.com/abbashm9/portfolio-skills/blob/main/portfolio.json"
3. Do not proceed with stale or assumed data

## Workflow — every daily check

### Step 0: Read portfolio.json

**BEFORE doing anything else**, fetch the current portfolio state from:
```
https://raw.githubusercontent.com/abbashm9/portfolio-skills/main/portfolio.json
```

Parse the JSON. Extract:
- `positions[]` array (the live holdings)
- `watchlist[]` array (pending positions waiting on broker approval or entry conditions)
- `cash_available` (dry powder)
- `total_cost_basis` (total invested)
- `totals.concentration_warning` (if any)
- `last_updated` timestamp (so report can note when portfolio was last changed)

This is the dynamic input for everything that follows. The position table, exit checks, rotation suggestions — all derived from this file.

### Step 1: Fetch live closing prices

Use `web_search` for each ticker **currently in `positions[]`** (from Step 0). **Required:** verified close prices for ALL positions.

**Price verification protocol — mandatory for every ticker:**

1. Search `"[TICKER] stock price today"` or `"[TICKER] closing price [today's date]"` to force recency.
2. Record the **source name and date** shown in the result (e.g., "Yahoo Finance, June 5 2026"). Include this in the email footer table.
3. **Cross-check rule:** If the fetched price differs by more than 5% from your own training-data estimate of recent price, run a second search from a different source before accepting it. A $100 error on a $500 stock is not a "broker spread" — it's a bad data pull.
4. If a price can't be confirmed from a reliable source (Yahoo Finance, Google Finance, Bloomberg, CNBC, Reuters) with a **current date**, flag it explicitly — do NOT estimate. **A $10 error on a stock is not a rounding issue — it's a bad data pull that breaks stop/TP math and misleads Abbas. Estimated data is worse than missing data.** Write "⚠️ PRICE UNCONFIRMED — could not verify [TICKER] close today" in that cell rather than using a stale or estimated figure.
5. In the email, include a small "Prices as of [date], sources: [list]" line under the position table so Abbas can instantly spot if a source is stale.

### Step 2: Build the data tables and withdrawal goal tracker

**Withdrawal goal tracker — show in every email, near the top.**

Read `withdrawal_goal` from portfolio.json. Calculate:
- `current_total_value` = sum of (shares × current_price) for all positions + cash_available
- `gap` = withdrawal_goal.target_total_value − current_total_value
- `progress_pct` = (current_total_value / withdrawal_goal.target_total_value) × 100

Format as a single compact line in the email hero section, right under the total P&L:

> 🎯 **Withdrawal goal:** $[current_total_value] / $1,000 — **$[gap] to go** ([progress_pct]% there)

Color the gap green if < $50, amber if $50–$150, grey if > $150.

If `gap ≤ 0`: replace with a bold alert — "🎯 **Withdrawal target hit. $1,000 reached. Consider withdrawing.**"

This tracker does NOT change the exit strategy — stops and TPs still apply as normal. It's a progress indicator only.

Calculate per-position:
- Current value (shares × current price)
- P&L $ and % vs cost basis
- Day's change $ and % (vs prior close)

Calculate portfolio totals:
- Total cost basis
- Total current value
- Total P&L $ and %
- Day's change $ and %

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

### Step 3.5: Catalyst Discovery — full stock-finder run

**Purpose:** Surface small/mid-cap names with imminent binary catalysts that nobody in mainstream media is currently talking about. This runs the same methodology as the standalone `stock-finder` skill — not a shortened version of it.

**Everything here must come from live web_search. Training data is useless for discovery.**

#### 3.5.1 — Cast the net (15 searches in parallel)

Run all simultaneously:

**FDA & regulatory:**
1. `FDA PDUFA action dates [current month] [next month] upcoming decisions`
2. `site:biopharmcatalyst.com PDUFA [current month] OR [next month]`
3. `FDA NDA BLA "action date" [current month] [next month] 2026`
4. `"advisory committee" OR AdCom meeting scheduled [current month] [next month] FDA`
5. `"complete response letter" resubmission PDUFA upcoming 2026`

**Clinical trial readouts:**
6. `"phase 3" "data readout" OR "results expected" [current month] [next month] biotech`
7. `"interim analysis" OR "primary endpoint" expected [current month] OR [next month] 2026`
8. `"top-line data" expected [current month] [next month] small cap 2026`

**Market signals:**
9. `"unusual options activity" small cap [today's date] OR [this week]`
10. `"insider buying" cluster multiple [current month] small cap`
11. `"short squeeze" catalyst upcoming [current month] 2026`
12. `"most shorted stocks" catalyst binary event 2026`
13. `"premarket movers" OR "premarket gainers" [today's date] catalyst`
14. `"small cap" "upcoming catalyst" OR "binary event" [current month] [next month]`
15. `biotech catalyst calendar [current month] [next month] 2026`

Extract all distinct tickers mentioned. Target 15–25 raw candidates. Tickers appearing in multiple searches = stronger signal.

#### 3.5.2 — Rapid 3-gate pre-screen (per candidate)

Drop any candidate that fails any gate:

- **Gate 1 — Confirmed event date ≤ 45 days?** No confirmed date → drop
- **Gate 2 — Market cap < $2B?** Search `"[TICKER]" market cap` → ≥ $2B → drop
- **Gate 3 — Halal quick check.** Search `"[TICKER]" revenue OR "interest income" OR halal`. Obvious disqualifier → drop. Unclear → keep with ⚠️ flag.

#### 3.5.3 — Score survivors (5-point pre-score)

| Factor | Points |
|---|---|
| Event ≤ 14 days out | 2 |
| Event 15–45 days out | 1 |
| Short interest ≥ 15% float | 1 |
| Appears in 2+ search sources | 1 |
| Any smart money signal (insider buy, big fund 13F, unusual options) | 1 |

Sort by score. Keep top 3 candidates. These go to Step 3.8 for condensed analysis.

If fewer than 3 survive: fall back to Tier A/B/C list in `references/rotation-playbook.md` to fill remaining slots. Note clearly which names are fallback large-caps vs. catalyst finds.

Feed top 3 into Step 3.8, Step 3.7, and Step 4.

### Step 3.8: Condensed analysis — top candidates from Step 3.5

For each of the top 3 candidates from Step 3.5, run a condensed 5-point analysis. This is NOT the full 8-section stock-analyzer deep dive — that's available on demand in chat. This is the daily email version: tight, actionable, enough to decide whether to investigate further.

Run these searches per candidate (in parallel across all 3 candidates):
- `"[TICKER]" FDA PDUFA OR "phase 3" OR earnings date confirmed`
- `"[TICKER]" market cap float short interest`
- `"[TICKER]" AdCom vote OR "phase 3 results" OR "EPS beat" history`
- `"[TICKER]" cash position runway OR dilution OR shelf registration`
- `"[TICKER]" insider buying OR "Form 4" OR institutional 13F 2026`

For each candidate, produce this block (this is what goes in the email):

---

> **🔬 [TICKER] — [COMPANY NAME]**
> **Catalyst:** [event type] on [exact date] — [X] days away
> **Market cap:** $[X]M | **Float:** $[X]M | **Short interest:** [X]%
>
> **Probability:** [X]% — [1-line rationale referencing base rate + key modifier e.g. "oncology NDA base rate 79%, lifted by BTD designation and 8-2 AdCom vote"]
>
> **Scenarios:**
> - ✅ If positive: ~$[price] (+[%]) — [this price = real technical/fundamental level: prior high / analyst target / resistance]
> - 💀 If negative: ~$[price] (-[%]) — [this price = real support / typical rejection drop for this catalyst type]
> - Expected value on 30% position (~$[amount]): **+$[EV] / -$[EV]**
>
> **Smart money:** [insider buys / institutional buildup / unusual options / none visible]
> **Cash runway:** [X months — dilution risk: yes/no]
>
> **Halal:** ✅ Verified / ⚠️ Unverified — check Musaffa / ❌ Fails
>
> **Conviction: [X]/5** (pre-score) → [INVESTIGATE / WATCH / SKIP]
> *Run `analyze [TICKER]` for the full 8-section deep dive before entering.*

---

**INVESTIGATE** = pre-score 4–5, halal clear, event ≤ 14 days
**WATCH** = pre-score 3, or event 15–45 days, or halal unverified
**SKIP** = pre-score ≤ 2, or halal fails, or no confirmed event date

All 3 candidate blocks go into the email under the "📡 Catalyst Plays" section. Even SKIP candidates are shown so Abbas can see what was found and why it didn't make the cut.

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

Abbas currently keeps a **$3 minimum cash reserve** at all times (to cover any exit commission without liquidating a position). So deployable cash = `cash_available − $3`. Commission on the new buy = $3. Net capital available for a new position = `cash_available − $6`.

If `cash_available − $6 < $30`: the remaining capital after commission is too small to be meaningful. State this explicitly:
> "Cash: $[X] — after $3 buy commission and $3 reserve, only $[X−6] deployable. Too small for a meaningful new position. Holding as dry powder."

If `cash_available − $6 ≥ $30`: **always** provide a concrete deployment recommendation. Do not leave this section blank or vague. Format:

> 💵 **Cash deployment — $[deployable] available**
> - **Option A — Catalyst play:** [TOP CANDIDATE from Step 3.5 Catalyst Radar, if conviction ≥ 6], buy [N] shares at ~$[price]. Event: [date]. Upside: +[%]. Downside: [%]. Halal: [status]. Position: $[amount] = [%]% of portfolio.
> - **Option B — Add to existing position:** [TICKER] (Risk: [score]/100, [LOW/MODERATE] from Step 3.6), buy [N] shares at ~$[price]. Rationale: [1 line]. Net position after: [shares] shares, avg entry ~$[blended].
> - **Recommended:** [A or B] because [1-line reason].
> - **Your call.**

**Position sizing for catalyst plays:** Abbas's target max allocation per catalyst name is **30% of total portfolio value** (positions + cash). Calculate: `0.30 × (total_positions_value + cash_available)`. Never exceed this cap in a single catalyst position, even if the conviction is high — binary events can go -70% on rejection.

Always show the math: shares × price + $3 commission ≤ deployable cash. Never suggest a buy that would leave cash_available below $3.

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

1. **Hero banner** — total P&L today, withdrawal goal tracker
2. **⚠️ MANDATORY — Positions snapshot table** — a single HTML table with ONE ROW PER POSITION showing: Status badge | Ticker | Close price | Day % | P&L $ | P&L % — then a TOTAL row. This is the first thing Abbas reads every morning. It MUST appear in every email, including weekend emails (use last known price if market closed). NEVER omit this table, collapse it into prose, or replace it with per-position cards only.
3. **Exit alerts** — any position needing action, with exact recommendation
4. **⏳ Pending Watchlist** — watchlist items from portfolio.json (see below) — always shown if watchlist is non-empty
5. **📡 Catalyst Plays** — daily catalyst discovery
6. **💵 Cash deployment** — recommendation from Step 3.7
7. **🔄 Rotation suggestions** — from Step 4, if any
8. **📚 Today's concept** — education, in a colored box
9. **Footer** — disclaimer, prices as of [date + sources]

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
