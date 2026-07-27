---
name: stock-finder
description: Sector-agnostic momentum discovery engine. Scans breakouts, volume surges, relative strength leaders, gap continuations, unusual options flow, insider buying clusters, earnings-reaction momentum, and sector rotation flows to surface 5-10 stocks worth a fast in-and-out trade (days, not weeks). No sector preference and no binary-catalyst bias — only exclusions are haram businesses and defense/military contractors. Use whenever Abbas says "find me something", "what's moving this week", "hunt for stocks", "find momentum plays", "what should I be looking at", "discovery run", or any variant of wanting new ideas rather than analyzing a specific ticker.
---

# Stock Finder — Momentum Discovery Engine

This skill's only job is **finding**. Not analyzing deeply — that's `stock-analyzer`'s job. The finder casts a wide net across the whole market, does a fast pre-screen, and hands Abbas a shortlist worth investigating further.

**The goal changed on 2026-07-27 (see `decisions.md`).** This is no longer a binary-catalyst hunter. Betting the portfolio on single dated events (FDA AdCom/PDUFA, earnings surprise) produced 3 losses in a row, one of them -$235 on a name that never even saw its catalyst — a gap-down stop-out two days before the event. The new mandate: **find liquid, already-moving stocks with a real technical or flow-based edge, size them modestly, hold days not weeks, take 5-15% and move on.** Many small wins beat one binary swing.

---

## Hard exclusions (apply before anything else)

1. **Haram business activity** — no alcohol, gambling, conventional banking/insurance as primary business, pork, adult content, tobacco, weapons manufacturing, interest-based finance. Business-activity screen only (see CLAUDE.md halal definition) — no AAOIFI financial-ratio checks needed.
2. **Defense/military contractors** — excluded as a personal rule, separate from and in addition to the halal screen. This means no government/DoD contract-award plays, no aerospace-defense primes, no ammunition/systems suppliers, even if their business model would otherwise pass the halal screen.

No other sector restriction. Biotech, tech, energy, consumer, industrials (non-defense), financials (non-banking), retail — all fair game if the setup is real.

---

## Critical rule: everything from live data

**Every run must use fresh live data.** Never answer this skill from memory or training data — momentum by definition is happening right now.

**Data source split:**
- Momentum/flow discovery, news catalysts, options flow, insider activity → web_search (IBKR doesn't have this)
- Current prices, volume, relative strength, 52-week range, themes → IBKR `get_price_snapshot`, `get_price_history`, `search_investment_topics`

---

## Workflow

### Phase 1: Cast the net (all searches in parallel)

Run all of these simultaneously. Volume matters here, not precision — precision comes in Phase 2.

**IBKR supplementary discovery (run alongside web searches):**
- `search_investment_topics` → query: "momentum"
- `search_investment_topics` → query: "breakout"
- `search_investment_topics` → query: your read of today's hot sector (e.g. "semiconductors", "energy") based on Phase 1 web results
These return topic keys; pass each to `get_theme_details` to pull associated company lists.

**Technical breakouts & volume (5 searches):**
1. `"52-week high" breakout small mid cap high volume [today's date] OR [this week] 2026`
2. `"most active" OR "volume spike" small mid cap [today's date] OR [this week]`
3. `"bull flag" OR "cup and handle" OR "breakout" high volume small cap [current week] 2026`
4. `"relative strength" leaders outperforming market small cap [current week] 2026`
5. `"premarket gainers" OR "premarket movers" [today's date] catalyst -defense -pentagon -military`

**Flow & smart money signals (5 searches):**
6. `"unusual options activity" OR "call sweep" small cap [today's date] OR [this week]`
7. `"insider buying" cluster "Form 4" multiple executives small cap [current month] 2026`
8. `"institutional buying" 13F "new position" small cap [current month] 2026`
9. `"short squeeze" setup high short interest "days to cover" small cap 2026`
10. `"gamma squeeze" OR "options expiry" pin small cap [current week] [next week] 2026`

**Earnings-reaction momentum — already happened, riding continuation, not predicting (5 searches):**
11. `"earnings beat" OR "guidance raised" stock reaction gap up small mid cap [current week] 2026`
12. `"gapped up" OR "gap and go" earnings OR contract OR upgrade [today's date] OR [this week] small cap`
13. `"analyst upgrade" "price target raised" small cap [current week] 2026`
14. `stocks up "20 percent" OR "30 percent" this week reason -defense -pentagon -military`
15. `sector rotation ETF inflows [current week] 2026 leading sector`

**Sector-agnostic sweep (broad, no biotech/FDA bias — 5 searches):**
16. `AI OR data center OR semiconductor momentum small mid cap [current week] 2026`
17. `energy OR clean energy OR nuclear momentum small mid cap [current week] 2026`
18. `consumer OR retail OR e-commerce momentum small mid cap [current week] 2026`
19. `industrials OR materials OR shipping momentum small mid cap -defense -military [current week] 2026`
20. `fintech OR financials momentum small mid cap [current week] 2026`

From this batch, extract all distinct tickers mentioned. Aim for 15-25 raw candidates. Duplicates across sources = stronger signal. Immediately drop any name that's a defense/military contractor or fails the haram screen on sight — don't waste a Phase 2 slot on it.

---

### Phase 2: Rapid pre-screen (per candidate, fast)

For each raw candidate, apply a 3-gate filter. 30-60 seconds per name, not a deep dive.

**Gate 1 — Live momentum signal confirmed?**
- Does the name have an active technical/flow signal in the last 5 trading days — breakout above resistance on volume, gap-up continuation, unusual options flow, insider buying cluster, or clear relative-strength leadership vs its sector/SPY?
- A future dated catalyst (earnings, PDUFA, etc.) is NOT sufficient on its own anymore — the trade needs to be moving now, not waiting on an event. If the only thing interesting is a future date, drop it.
- If no live signal: drop it

**Gate 2 — Liquid enough for a fast exit?**
- Use IBKR `search_contracts` (query = ticker) → `get_price_snapshot` fields: `["last", "misc_statistics", "avg_90d_usd_volume", "bid_ask"]`
- Average daily $ volume should be enough to enter and exit a position in this size without meaningfully moving the price — thin/illiquid micro-caps make a fast in-and-out plan pointless (you can get the momentum entry but not the fast exit)
- If avg_90d_usd_volume looks too thin to exit within a session or two: drop it

**Gate 3 — Exclusion + halal quick check**
- Defense/military contractor? Drop, no exceptions.
- Obvious haram business (bank, insurer, alcohol, gambling, weapons, adult, tobacco)? Drop.
- Unclear? Keep with ⚠️ flag, Abbas confirms before entering.

Candidates surviving all 3 gates go to Phase 3.

---

### Phase 3: Score and rank surviving candidates

Fast 5-point conviction pre-score — not the full 10-point rubric from `stock-analyzer`, just enough to rank the shortlist.

| Factor | Points |
|---|---|
| Signal fired in last 1-2 trading days (fresher = better) | 2 |
| Signal fired 3-5 trading days ago, still intact | 1 |
| Appears in 2+ of the Phase 1 search sources (duplicate signal) | 1 |
| Smart money signal visible (insider buy, unusual options, 13F, institutional buildup) | 1 |
| Relative strength clearly outperforming its sector/SPY over the signal window | 1 |
| **Max** | **5** |

Sort by score descending.

---

### Phase 4: Output — ranked shortlist

Present the top **5-10 candidates**. Format:

---

> ## 🎯 Momentum Shortlist — [today's date]
>
> *[X] candidates found across [Y] sources. Showing top [N] by conviction pre-score. Run `stock-analyzer` on any name for the full deep dive.*
>
> ---
>
> **#1 — [TICKER] | [COMPANY NAME]** ⭐⭐⭐⭐⭐ (5/5) `[SECTOR]`
> - **Signal:** [what fired — e.g. "Broke above $42 resistance on 3x avg volume Tuesday, held the breakout Wednesday"] — [X] trading days ago
> - **Price:** $[X] | **Avg daily $ vol:** $[X]M (from IBKR) | **RS vs SPY:** [outperforming/underperforming, by how much]
> - **Why it's interesting:** [2-3 sentences — the specific setup, not generic. What's the actual edge and why now.]
> - **Realistic near-term target:** +[5-15]% over [1-10] trading days — [reason, e.g. next resistance level, measured move from the flag]
> - **Halal:** ✅ Verified / ⚠️ Unverified — check before entering / ❌ Fails
> - **Defense/military check:** ✅ Clear
> - **Next step:** `analyze [TICKER]`
>
> ---
> [continue for all candidates]

---

### Phase 5: Highlight the single best setup

> **Today's best setup:** [TICKER] — [2-3 sentence case: what's driving it, why it's fresher/stronger than the rest, what invalidates it.] **Invalidation:** [the specific technical/flow level that says "this thesis is wrong, exit"] — this is the stop reference, not a percentage guess.

---

## What this skill does NOT do

- Deep fundamental analysis — that's `stock-analyzer`
- Portfolio updates — that's `portfolio-manager`
- Guarantee any of these plays work — research only
- Hunt for binary-catalyst/FDA/PDUFA setups — retired 2026-07-27, see `decisions.md`
- Surface defense/military contractor names, ever
- Cover names already all over CNBC/mainstream retail chatter — look for what's moving before it's obvious

## How to use the output

1. Scan the shortlist
2. Pick 1-2 names that feel interesting
3. Say "analyze [TICKER]" — `stock-analyzer` runs the full deep dive, including a **stop-limit** level (not a plain stop — see the CAPR lesson in `decisions.md`: plain STOP orders become market orders on trigger and offer zero protection against a gap)
4. Decide based on conviction
5. If entering: size it to leave room for 5-7 concurrent positions, not one dominant name. Log it with `portfolio-manager`.

The `stock-finder` output alone is NOT enough to enter a trade — it's a first filter.

---

## Refresh cadence

This now also runs automatically inside the daily 6am email (`daily-portfolio-check` Step 3.5). Trigger this skill manually any time you want a fresh on-demand pull between emails, or when cash frees up and needs a new home.
