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
2. **Defense/military contractors** — excluded as a personal rule, separate from and in addition to the halal screen. This means no government/DoD contract-award plays, no aerospace-defense primes, no ammunition/systems suppliers, even if their business model would otherwise pass the halal screen. **This includes names whose current catalyst is itself a government/DoD contract award** — a memory-chip maker rallying on an Army SBIR contract is a defense-contract play for the purposes of this rule, even though the company isn't a defense prime. If the move exists because of a military contract, drop it.

No other sector restriction. Biotech, tech, energy, consumer, industrials (non-defense), financials (non-banking), retail — all fair game if the setup is real.

---

## Critical rule: everything from live data

**Every run must use fresh live data.** Never answer this skill from memory or training data — momentum by definition is happening right now.

**Data source split:**
- Momentum/flow discovery, news catalysts, options flow, insider activity → web_search (IBKR doesn't have this)
- Current prices, volume, relative strength, 52-week range, themes → IBKR `get_price_snapshot`, `get_price_history`, `search_investment_topics`

**When web search and IBKR disagree, IBKR wins — always.** Search results routinely report moves that are stale or already reversed (a real case: search said a stock "soared 13% premarket" while the live IBKR quote showed it down 3.6% and 48% off its high — the pop had already faded). Never put a candidate on the shortlist on the strength of a search narrative alone; Phase 2's IBKR confirmation exists precisely to catch this.

---

## Workflow

### Phase 1: Cast the net (all searches in parallel)

Run all of these simultaneously. Volume matters here, not precision — precision comes in Phase 2.

**IBKR supplementary discovery (run alongside web searches):**
- `search_investment_topics` → query: "momentum"
- `search_investment_topics` → query: "breakout"
- `search_investment_topics` → query: your read of today's hot sector (e.g. "semiconductor", "energy") based on Phase 1 web results — use short singular keywords, the matcher is narrow
These return topic keys; pass each to `get_theme_details` to pull associated company lists. (If a query returns no themes, retry once with a shorter/singular synonym, then move on — don't burn time here.)

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

From this batch, extract all distinct tickers mentioned. Aim for 15-25 raw candidates. Duplicates across sources = stronger signal. Immediately drop any name that's a defense/military contractor (or whose catalyst is a military contract) or fails the haram screen on sight — don't waste a Phase 2 slot on it.

**If a batch of searches comes back generic** (trend commentary, ETF think-pieces, no concrete tickers): run 2-3 targeted follow-ups on curated mover roundups (e.g. WebFetch a movers-list article that the search surfaced) rather than re-running the same generic queries. Concrete tickers with named catalysts are the goal; commentary is noise.

---

### Phase 2: Rapid pre-screen (per candidate, fast)

For each raw candidate, apply a 3-gate filter. 30-60 seconds per name, not a deep dive.

**Gate 1 — Live momentum signal confirmed against real data?**
- Does the name have an active technical/flow signal in the last 5 trading days — breakout above resistance on volume, gap-up continuation, unusual options flow, insider buying cluster, or clear relative-strength leadership vs its sector/SPY?
- A future dated catalyst (earnings, PDUFA, etc.) is NOT sufficient on its own anymore — the trade needs to be moving now, not waiting on an event. If the only thing interesting is a future date, drop it.
- **Confirm the move with IBKR before it passes:** `get_price_snapshot` fields `["last", "change", "prior_close", "misc_statistics", "volume", "avg_90d_usd_volume"]`. If the live quote contradicts the search narrative (down on the day, well off the high, spike already retraced), the signal is stale — drop it or flag it as FADED. Search narrative alone never passes this gate.
- If no live signal: drop it

**Gate 2 — Liquid enough for a fast exit, and sizeable on this account?**
- From the same `get_price_snapshot` call: average daily $ volume should be enough to enter and exit a position in this size without meaningfully moving the price — thin/illiquid micro-caps make a fast in-and-out plan pointless (you can get the momentum entry but not the fast exit)
- **Price-per-share sanity:** this is a small account (fetch current value from `portfolio.json` — recently in the ~$500-800 range). If a single share is a large chunk of the max 15-18% position (roughly, share price > ~half the max position $), the name can't size sanely no matter how good the setup. Don't shortlist it — mention it in a one-line "real setup, wrong account size" note instead.
- If avg_90d_usd_volume looks too thin to exit within a session or two: drop it

**Gate 3 — Exclusion + halal quick check**
- Defense/military contractor, or catalyst is a gov/DoD contract award? Drop, no exceptions.
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

Present the top **5-10 candidates** — but **only if that many real ones exist.**

**Honesty rule — never pad a thin scan.** Some days the market simply doesn't offer 5 fresh setups that clear the gates. When the scan yields only 1-3 real candidates, present exactly those and say plainly "thin day — [X] candidates cleared the gates," with a short list of what got cut and why (stale, faded-vs-IBKR, excluded, illiquid, wrong account size). A padded list of stale or weak names is worse than a short honest one — every padded name is a candidate for a bad entry. Show the rejects; that's the analyst showing their work.

Format:

---

> ## 🎯 Momentum Shortlist — [today's date]
>
> *[X] candidates found across [Y] sources. [N] cleared all gates. Run `stock-analyzer` on any name for the full deep dive.*
>
> ---
>
> **#1 — [TICKER] | [COMPANY NAME]** ⭐⭐⭐⭐⭐ (5/5) `[SECTOR]`
> - **Signal:** [what fired — e.g. "Broke above $42 resistance on 3x avg volume Tuesday, held the breakout Wednesday"] — [X] trading days ago
> - **Price:** $[X] (IBKR live) | **Avg daily $ vol:** $[X]M (IBKR) | **RS vs SPY:** [outperforming/underperforming, by how much]
> - **Why it's interesting:** [2-3 sentences — the specific setup, not generic. What's the actual edge and why now.]
> - **Realistic near-term target:** +[5-15]% over [1-10] trading days — [reason, e.g. next resistance level, measured move from the flag]
> - **Halal:** ✅ Verified / ⚠️ Unverified — check before entering / ❌ Fails
> - **Defense/military check:** ✅ Clear
> - **Next step:** `analyze [TICKER]`
>
> ---
> [continue for all candidates]
>
> **Cut this run:** [TICKER — reason] · [TICKER — reason] · ... (one line each: FADED vs live data / stale catalyst / defense-contract catalyst / haram / illiquid / wrong account size)

---

### Phase 5: Highlight the single best setup

> **Today's best setup:** [TICKER] — [2-3 sentence case: what's driving it, why it's fresher/stronger than the rest, what invalidates it.] **Invalidation:** [the specific technical/flow level that says "this thesis is wrong, exit"] — this is the stop reference, not a percentage guess.

If nothing on the day genuinely deserves the label, say "no standout setup today" — the label has to mean something.

---

## What this skill does NOT do

- Deep fundamental analysis — that's `stock-analyzer` (which now runs a mandatory fundamentals health check on every name — the finder's shortlist is NOT pre-cleared on fundamentals)
- Portfolio updates — that's `portfolio-manager`
- Guarantee any of these plays work — research only
- Hunt for binary-catalyst/FDA/PDUFA setups — retired 2026-07-27, see `decisions.md`
- Surface defense/military contractor names or military-contract-driven moves, ever
- Cover names already all over CNBC/mainstream retail chatter — look for what's moving before it's obvious
- Pad a thin day's results to hit a candidate count

## How to use the output

1. Scan the shortlist
2. Pick 1-2 names that feel interesting
3. Say "analyze [TICKER]" — `stock-analyzer` runs the full deep dive: fundamentals health check, event risk map, and a **stop-limit** level (not a plain stop — see the CAPR lesson in `decisions.md`: plain STOP orders become market orders on trigger and offer zero protection against a gap)
4. Decide based on conviction
5. If entering: size it to leave room for 5-7 concurrent positions, not one dominant name. Log it with `portfolio-manager`.

The `stock-finder` output alone is NOT enough to enter a trade — it's a first filter.

---

## Refresh cadence

This runs automatically as the **"Stock Finder - Tue/Sun" cloud routine** (Sundays and Tuesdays, ~7:05am Kuwait), which emails the shortlist via the same GitHub outbox pipeline as the daily check. It is intentionally NOT part of the daily portfolio email — full-market discovery inside a daily routine caused the 2026-07-28 token-limit failure, so the daily check covers positions/exits/macro/cash only. Trigger this skill manually any time you want a fresh on-demand pull between scheduled runs, or when cash frees up and needs a new home.
