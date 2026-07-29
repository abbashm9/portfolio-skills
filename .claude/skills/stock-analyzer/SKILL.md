---
name: stock-analyzer
description: Deep momentum-focused stock analysis for any ticker. Produces an 8-section research brief covering company snapshot, halal compliance, live signal & technical structure, fundamentals health check, event risk map, smart money signals, risk/reward scenarios, and a concrete trade verdict with entry/stop-limit/targets/position size. Built for fast in-and-out momentum trades (days, not weeks) on liquid small/mid-cap names. Use whenever Abbas says "analyze [TICKER]", "deep dive [TICKER]", "research [TICKER]", "is [TICKER] worth it", "what do you think about [TICKER]", "run the analyzer on [TICKER]", or pastes a ticker and asks for a full take.
---

# Stock Analyzer — Deep Momentum Research (v2, post-2026-07-27 pivot)

A full-depth research tool for any publicly traded stock. The goal: a better-informed view than a sell-side note, focused on whether a **live momentum setup** is worth a fast, modestly-sized trade — not whether a binary event will go the right way.

**The mandate changed 2026-07-27 (see `decisions.md`).** Binary-catalyst betting (PDUFA/AdCom/earnings-surprise as the thesis) produced 3 straight losses, one of them -$235 on a gap-down stop-out before the event even arrived. This skill now analyzes **already-moving stocks with a real technical or flow edge**: confirm the signal, check the company won't blow up underneath it, derive real levels, size modestly, exit fast.

## User context

- **Portfolio:** small account — always fetch the current value and cash from `portfolio.json` (repo root) at the start of every run; never hardcode it, it goes stale fast
- **Strategy:** halal-compliant momentum/technical trades, days not weeks, take 5-15% and move on
- **Sizing:** max 15-18% of portfolio per name, target 5-7 concurrent positions, no name > 20%
- **Halal standard:** business activity only (see Section 2) — NO AAOIFI financial-ratio screens
- **Commission:** ~$1 per trade (~$2 round trip) — factor into all EV math
- **Tone:** experienced trader (8 years forex/indices). No basics. Numbers and conviction.

---

## Critical rule: live data only

**Never answer from training data on prices, dates, filings, or financials.** Every key fact must come from a live source in this session.

**Data source hierarchy:**
- **Prices, 52-week range, volume, momentum returns, volatility, themes, company overview, OHLCV history → IBKR first.** Exact and real-time.
- **Fundamentals (revenue, debt, equity, cash), insider Form 4, institutional 13F, halal verification, news catalysts → web_search.** IBKR does not provide these.

**When web search and IBKR disagree, IBKR wins.** A search result saying a stock "soared today" while the live IBKR quote shows it down on the day means the narrative is stale or wrong — correct it in the report, don't pass it through. (This exact conflict has happened; treat it as routine, not exceptional.)

If a data point genuinely cannot be found after two attempts from either source, say so explicitly — never estimate without disclosing it.

---

## Workflow — 8 sections

Run all initial data pulls in parallel before writing any section. Then write the report top to bottom.

### Parallel data batch (run before writing anything)

**IBKR (resolve contract_id first via `search_contracts` query=[TICKER], then run in parallel):**
- A. `get_price_snapshot` → fields: `["last", "change", "prior_close", "misc_statistics", "avg_90d_usd_volume", "implied_vol_underlying", "historical_vol", "cumulative_perf_1w", "cumulative_perf_1m", "cumulative_perf_ytd", "bid_ask", "volume"]`
- B. `get_price_history` → period: THREE_MONTHS, step: ONE_DAY, security_type: STK, outside_rth: false — daily OHLCV bars are the basis for ALL technical levels (stops, targets, signal confirmation). Also pull ONE_YEAR / ONE_WEEK for the HTML chart context.
- C. `get_company_themes` → max_themes: 4, max_companies: 5 (sector classification + peer ranking)
- D. `get_company_connections` → link_types: ["company_product", "company_competitor", "company_country"], include: ["link_info"] (business overview)

**Web search (run in parallel with IBKR calls):**
1. `"[TICKER] stock" market cap float shares outstanding short interest`
2. `"[TICKER]" news catalyst reason move [this week] [current month] 2026` — what's driving the current signal
3. `"[TICKER]" earnings date next report expected 2026` — event-risk mapping, not thesis
4. `"[TICKER]" revenue growth OR "quarterly results" OR "earnings history" beat OR miss`
5. `"[TICKER]" balance sheet cash debt OR "stockholders equity" OR "negative equity" OR dilution 2026`
6. `"[TICKER]" operating cash flow OR "cash burn" OR "cash runway" quarterly`
7. `"[TICKER]" insider buying OR "Form 4" OR "insider purchase" 2026`
8. `"[TICKER]" institutional holdings OR "13F" OR hedge fund 2026`
9. `"[TICKER]" unusual options OR "call sweep" OR "implied move" [current month]`
10. `"[TICKER]" support resistance "52-week high" OR "prior high" OR "analyst price target" 2026`
11. `"[TICKER]" core business products revenue segments` — halal business-activity check (skip if obvious from IBKR item D)

---

### Section 1: Company & Market Snapshot

**Sources:** IBKR A (price, range, volume), D (business), themes from C; web 1 (cap/float/SI).

- What the company actually does (1-2 concrete sentences from `get_company_connections`)
- Market cap and public float — flag float size and what it means for move potential
- Short interest % of float — >15% is a squeeze amplifier on momentum continuation
- 52-week high/low/current from IBKR — where in the range, and how far off the high
- Average daily $ volume from `avg_90d_usd_volume` — this feeds the liquidity gate in Section 8
- **Price-per-share sanity check:** if one share is a large chunk of the max position size (roughly, share price > ~half the 15-18% allocation), flag immediately — the trade may not size sanely on this account regardless of setup quality
- IBKR theme tags + closest peers, 1 line

---

### Section 2: Halal Compliance — business activity ONLY

**The standard (per CLAUDE.md, confirmed post-pivot): core business activity must be permissible. NO AAOIFI financial-ratio checks** (interest-income %, debt/assets, receivables/cap are all irrelevant — Abbas is a capital-gains trader, not a dividend investor). Do not run ratio math; do not flag names for Musaffa ratio screening.

**Fails if core business is:** alcohol, gambling, conventional banking/insurance as primary business, pork, adult content, tobacco, weapons manufacturing, interest-based finance.

**Separate hard exclusion (not halal, a personal rule): defense/military contractors** — including names whose current catalyst is itself a government/DoD contract award, even if the company's overall business would pass.

**Output:** ✅ CLEAR (state the core business) / ⚠️ UNCLEAR (what needs confirming — Abbas decides before entry) / ❌ FAILS (which business, stop the report here).

---

### Section 3: Live Signal & Technical Structure — the actual thesis

This section replaces the old catalyst-timeline-as-thesis. The question: **is there a real, live, technical or flow edge right now?**

**From IBKR daily OHLCV (batch item B) + web 2:**

1. **What fired, and when?** Breakout above defined resistance, gap-up continuation, volume surge, relative-strength leadership, unusual options flow, insider cluster. Name the exact signal and the exact date.
2. **Freshness gate:** signal must have fired within the **last 5 trading days** and still be intact (price holding above the breakout level / continuation not already faded). Older, or already retraced below the trigger level → the edge is gone → this alone can drop the verdict to SKIP.
3. **Trend context:** where is price vs the 3-month structure? Higher highs/higher lows, or a one-day spike inside a downtrend? A spike inside a downtrend is a FADE risk, not a momentum trade.
4. **Volume confirmation:** signal-day volume vs 90-day average (from real bars, not narrative). ≥2x average = real participation; below-average = suspect.
5. **Relative strength:** performance vs sector peers / SPY over the signal window (IBKR `cumulative_perf_1w` / `_1m` vs SPY's).
6. **Derive the key levels from the actual bars:** signal trigger level, nearest real support below, nearest real resistance above. These feed Section 8 directly.

If there is **no live signal**, say so plainly and mark the report SKIP-leaning from here — the remaining sections still run (Abbas may be asking about a watchlist name), but the verdict cannot be BUY without a live signal.

---

### Section 4: Fundamentals Health Check — mandatory, every name, no exceptions

**Why this exists:** a GRPN "BUY NOW" call went out on technicals + halal alone; Abbas caught that nobody had checked the financials — which showed negative equity, four straight earnings misses, negative operating cash flow, and ~$250M debt. Never again. This check runs even for pure momentum trades on names you'll hold for 3 days.

**From web 4, 5, 6 — check and state each:**

| Check | Red flag |
|---|---|
| Stockholders' equity | Negative equity |
| Revenue trend (last 4 quarters) | Flat/declining while the stock runs |
| Earnings vs estimates (last 4) | 3+ consecutive misses |
| Operating cash flow | Negative and worsening |
| Debt load vs cash | Debt >> cash with near-term maturities |
| Dilution risk | Open shelf/ATM, or burn rate forcing a raise within ~2 quarters |

**This check does NOT auto-kill a momentum trade — it reframes and resizes it.** A squeeze on a fundamentally weak company can still be a valid fast trade. But it must be labeled honestly:

- **2+ red flags → mandatory adjustments:** label the trade explicitly ("momentum/squeeze trade on a fundamentally weak company — not an improving-fundamentals story"), cut position size toward the 10-12% end, tighten the time-stop, and never hold through any dated event (Section 5).
- **0-1 red flags:** note it and move on.

---

### Section 5: Event Risk Map — dated events as RISK, not thesis

Find every scheduled event (earnings, FDA/regulatory, court, lock-up expiry, index rebalance) within the **next 30 days** — web 3 plus anything surfaced in web 2.

**The rule (direct CAPR + GRPN application):** momentum trades do not hold through binary events. For each event found:

- Date, type, confidence in the date (company-confirmed / estimated)
- **Is it inside the expected holding window (1-10 trading days)?**
  - **Yes → set a hard time-stop: exit by the last trading day BEFORE the event, regardless of price.** State the exact date in Section 8. If the event is so close that there's no room for the trade to work first (< ~3 trading days of runway), that alone is grounds for SKIP.
  - No → note it as the outer boundary; the trade must be closed well before it.

If no events in 30 days: say so — that's a clean runway and worth a point in the score.

*(The old FDA base-rate probability modeling and analog analysis are retired as default sections — binary events are no longer the thesis. `references/probability-models.md` is kept for the rare case Abbas explicitly asks for a binary-event assessment.)*

---

### Section 6: Smart Money Signals

Three sub-checks, each with a BULLISH / NEUTRAL / BEARISH read:

**6a. Insider Form 4 (web 7):** open-market cash purchases in last 90 days (strongest signal); opportunistic selling (concerning); nothing (neutral).

**6b. Institutional 13F (web 8):** new positions or >50% increases from known funds last quarter; reductions = cautionary.

**6c. Options flow (IBKR A + web 9):**
- `implied_vol_underlying` vs `historical_vol` from IBKR: IV >> HV = market pricing an event or continuation; note which.
- Unusual call buying (strike, expiry, volume vs OI) supporting the momentum direction, or put buying against it.

---

### Section 7: Risk/Reward & Scenarios

Momentum scenarios, not binary-outcome scenarios. Position basis = **15% of current portfolio value** (from portfolio.json — compute the actual dollar figure fresh; drop toward 10-12% if Section 4 flagged 2+ red flags).

| Scenario | Basis | Price | From current | $ on the position |
|---|---|---|---|---|
| Target 2 hit — continuation extends | next major resistance (real level) | $[X] | +[%] | +$[X] |
| Target 1 hit — normal follow-through | nearest real resistance | $[X] | +[%] | +$[X] |
| Stop-limit hit — signal invalidated | just below real support | $[X] | -[%] | -$[X] |

- **R:R to Target 1 must be ≥ 2:1 vs the stop.** Below that, the math doesn't clear commissions + slippage on a fast trade — say so.
- Rough EV using honest probabilities (momentum continuation after a confirmed fresh breakout is roughly a coin flip; weight accordingly — do NOT import FDA-style 80% confidence into technical setups). EV must clear the ~$2 round-trip commission to matter.

---

### Section 8: Verdict & Trade Setup

**Conviction score: [X]/10** — use `references/scoring-rubric.md` (momentum rubric). Show the point-by-point breakdown; never just a number.

**Recommendation:** [BUY / WATCH / SKIP]
- **BUY:** score ≥ 7, live signal ≤ 5 trading days old and intact, halal clear, liquid enough, R:R ≥ 2:1, no un-time-stopped event inside the window
- **WATCH:** score 5-6, or signal needs one more confirmation day, or halal unclear — state exactly what flips it to BUY
- **SKIP:** score < 5, or no live signal, or halal/defense fails, or R:R < 2:1 with no better entry available

**If BUY or WATCH:**

> **Trade setup:**
> - Entry: $[price] — [why this level]
> - **Stop: $[trigger] / limit $[limit] — STOP-LIMIT, never a plain stop.** A plain STOP becomes a market order on trigger and gives zero gap protection (a planned -36% CAPR stop filled at -72% this way on 2026-07-27). Set the limit a few % below the trigger — enough to fill in normal tape, tight enough to refuse a catastrophic gap fill. If price gaps through the limit, it's a manual same-day decision, not a silent fill.
> - Target 1: $[price] — [exact real level + reason] — take partial or full profit
> - Target 2: $[price] — [exact real level + reason] — if held, exit remainder here
> - **Time-stop: [date]** — [earlier of: last trading day before any Section-5 event, or ~10 trading days from entry with no continuation signal]. Exit regardless of price.
> - Position: $[amount] ([X] shares) = [X]% of $[current portfolio value] — max 15-18%, reduced toward 10-12% if fundamentals-flagged. Commission ~$1 in, ~$1 out.
> - Exit rule: signal invalidation (close below stop level) or time-stop, whichever first. No averaging down. No "it'll come back."

**Stop and target derivation — same mandatory rules as always:**
- Stops sit just below (1-3%) a REAL level from the actual OHLCV bars: prior swing low, breakout level, key MA, gap fill. Never a % from entry — the market doesn't know your entry.
- Targets sit at REAL resistance: prior swing highs, 52-week high, round-number confluence, gap tops, analyst-target clusters (web 10). Never entry × 1.X.
- Every level formatted with its reason: "$42.80 — breakout level that held 3 weeks (technical)".

**If SKIP:** one sentence on why — and what specific change (fresh signal, better entry, cleaner event window) would make it worth re-running.

---

### Section 9: HTML Report

**After completing all 8 sections, generate a self-contained HTML report.** File: `reports/analysis-[YYYY-MM-DD].html` (multiple tickers in one session share the file).

**Do NOT auto-open it.** Write the file, give Abbas the path, let him open it. (Standing rule — auto-`open` steals focus from other work.)

**Design:** match the canonical dark-theme template (`reports/analysis-2026-06-10.html` structure): background `#0d0f14`, surface `#161a23`, card `#1e2330`, border `#2a3040`, text `#e2e8f0`, muted `#7a8499`. Chart.js from CDN `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`, `responsive: true, maintainAspectRatio: false`, fixed-height wrappers.

**Components (updated for momentum framing):**
1. **Header** — title, date, current portfolio value + max position (both computed fresh from portfolio.json), halal standard ("business activity"), data source line
2. **Verdict cards** — ticker + BUY/WATCH/SKIP badge, conviction score, signal-age counter ("signal fired [X] trading days ago"), time-stop date if set, 1-line key risk + key positive, IBKR theme pills
3. **Price chart** — real IBKR OHLCV (batch item B), with the signal trigger level, stop, and targets drawn as horizontal lines; 52-week high/low marked
4. **Per-ticker sections** (BUY first, then WATCH, then SKIP): stats grid, halal badge row, **signal & structure panel** (what fired, freshness, volume vs avg, RS), **fundamentals health table** (the six checks, red-flagged rows highlighted), **event risk strip** (any dated events in 30 days with the time-stop marked), smart money rows, scenario bar chart ($ on the actual position size), trade setup box (entry white / stop red / TP1 amber / TP2 green / time-stop purple), conviction breakdown checklist
5. **Action items** — numbered next steps per ticker

Self-contained single file, inline CSS, vanilla JS, max-width 1200px, mobile-responsive.

---

## Output format

In chat: after writing the HTML, deliver a brief summary — verdict per ticker, the single key risk, the time-stop date if any, and the report file path. Don't repeat the full analysis as markdown; the HTML is the deliverable. Provide markdown for a specific section only if asked.

---

## What this skill does NOT do

- Execute trades — Abbas does this in his broker
- Update portfolio.json — that's `portfolio-manager`
- Give financial advice — research only, disclosed in every report
- Replace the daily check — this is an on-demand deep dive
- Binary-catalyst probability modeling as the thesis — retired 2026-07-27; event dates are risk inputs now, not the play
- Auto-open reports in the browser — write the file, hand over the path


## Free-tier delegation, with senior review

Before doing grunt/mechanical sub-steps of this skill yourself — data pulls, formatting,
boilerplate generation, repetitive edits, first-draft text — route them through the free/
cheap-tier channel instead of spending full-model effort on them:

- **OpenCode** (agentic, has file/bash tool use): `opencode run "<precise, self-contained task
  brief>" -m opencode/deepseek-v4-flash-free` (alternatives: `opencode/north-mini-code-free`,
  `opencode/nemotron-3-ultra-free`, `opencode/mimo-v2.5-free`). No API key needed.
- **OmniRoute** (`omniroute chat "<prompt>"`, localhost:20128): non-agentic text in/out —
  research summaries, first drafts, brainstorming lists.

**You are the senior reviewing this output before it ever reaches Abbas.** "It ran" or "it
returned text" is not verification — actually check the delegated result against what the task
needed (read the file it edited, check the numbers it pulled, read the copy against the actual
ask) before anything is presented as done. Free-tier models make confident, subtle mistakes
more often than they flag their own uncertainty — hold their output to a higher scrutiny bar
than your own first-draft work, not a lower one. Fix or redo anything that does not hold up;
never pass delegated output straight through to Abbas unchecked.

Reserve full-quality effort (skip delegation) for the judgment/taste/voice-dependent parts of
this skill — synthesis calls, anything reviewed against Abbas's voice, a decision only he or
you should make directly. If free-tier output is consistently weak for a task class, say so
rather than silently shipping it — Abbas prioritizes quality over cost savings and will
provide paid-tier keys if needed.
