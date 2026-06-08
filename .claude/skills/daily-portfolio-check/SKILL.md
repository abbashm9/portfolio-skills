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
4. If a price can't be confirmed from a reliable source (Yahoo Finance, Google Finance, Bloomberg, CNBC, Reuters) with a **current date**, flag it explicitly — do NOT estimate. Estimated data is worse than missing data.
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

### Step 3: Exit-strategy check per position (in order)

1. **Halal compliance** — quarterly check, not daily, but flag if breaking news suggests a change
2. **Stop-loss** — Below stop? 🚨 ALERT. Within 2% of stop? ⚠️ WATCH.
3. **TP1/TP2/TP3** — Hit? 🔔 ACTION with trim recommendation
4. **Catalyst proximity** — within 5 trading days? Flag prominently
5. **Time-based** — flat ±3% for 30+ days, no catalyst? Consider trim
6. **Parabolic warning** — up >40% in 30 days, RSI >80? Mean-reversion risk

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
> - ✅ If positive: ~$[price] (+[%]) | 💀 If negative: ~$[price] (-[%])
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

See `references/education-curriculum.md` for the full 30-day curriculum. Pick the concept that's most relevant to TODAY's portfolio activity, with a slight bias toward terms that appeared in today's report. Repeat concepts on subsequent days for deeper coverage when warranted — no rush.

Track which concepts have already been taught (in conversation context) to avoid teaching the same one twice in a row unless intentionally going deeper.

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
2. **Positions table** — all holdings with status badges (✅ HOLD / ⚠️ WATCH / 🔔 ACTION / 🚨 ALERT)
3. **Exit alerts** — any position needing action, with exact recommendation
4. **📡 Catalyst Plays** — the new section (see below)
5. **💵 Cash deployment** — recommendation from Step 3.7
6. **🔄 Rotation suggestions** — from Step 4, if any
7. **📚 Today's concept** — education, in a colored box
8. **Footer** — disclaimer, prices as of [date + sources]

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

Use the **GitHub connector** to create or update the file `outbox/email.json` in
the `abbashm9/portfolio-skills` repo on the `main` branch:

```json
{
  "subject": "<subject line>",
  "html_body": "<full HTML email string>"
}
```

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

## What this skill does NOT do

- Execute trades — Abbas does this in his broker
- Give financial advice — research only
- Daily halal compliance lectures — quarterly check only, no daily education on this
- Generic education — every concept anchors to Abbas's actual portfolio
