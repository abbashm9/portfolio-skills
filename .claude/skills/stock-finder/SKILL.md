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

**Large cap & mega cap — MANDATORY lane, never skip (5 searches):**

Added 2026-07-29 because Abbas pointed out he wasn't seeing a familiar name in any scan. That wasn't a judgment call — every search above has "small mid cap" hardcoded, so large caps were *structurally invisible* to this skill. They are not second-class candidates; on some tapes they're the best setups available.

21. `large cap OR "S&P 500" stocks "52-week high" breakout [this week] [current month] 2026`
22. `"earnings beat" "raised guidance" large cap stock jumped OR surged [today's date] OR [this week] 2026`
23. `mega cap OR "Dow" rotation winners leading sector [this week] 2026 breakout`
24. `"most oversold" OR "RSI below 30" large cap quality stocks bounce candidates [current week] 2026`
25. `large cap "analyst upgrade" "price target raised" [this week] 2026`

**Why large caps often beat small caps for this strategy — three structural advantages:**
1. **The binary event is usually already behind them.** A mega-cap that beat and raised *yesterday* has its earnings risk resolved — there's nothing left to time-stop before. Compare that to a small cap running *into* a catalyst, which is the exact CAPR failure mode. Post-earnings large caps are the single cleanest setup shape this strategy can take.
2. **Liquidity is never the constraint.** Hundreds of millions in daily volume means the fast exit the whole strategy depends on is guaranteed.
3. **Post-earnings drift is a real, well-documented tendency** in liquid names that beat *and* raise on heavy volume — that's continuation, exactly what this skill hunts.

Their trade-off: smaller percentage moves, so target 4-10% rather than 15%+, and R:R depends heavily on not chasing an extended gap (see Phase 2 Gate 4).

**Rotation awareness:** when the market is violently rotating (e.g. money fleeing tech/semis into value/industrials/healthcare), the large-cap lane is where that shows up first. Read the rotation from searches 15 and 23, then bias the whole scan toward the receiving side of the flow, not the side being sold.

From this batch, extract all distinct tickers mentioned. Aim for 15-25 raw candidates across ALL cap sizes. Duplicates across sources = stronger signal. Immediately drop any name that's a defense/military contractor (or whose catalyst is a military contract) or fails the haram screen on sight — don't waste a Phase 2 slot on it.

**Cap-size balance rule:** the final shortlist must not be all-small-cap or all-large-cap unless the scan genuinely produced nothing on one side — and if so, say that explicitly. Tag every shortlisted name with its cap size so the mix is visible at a glance.

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
- **Sizing check — fractional shares change this, do NOT reflexively reject a high-priced stock.** IBKR supports fractional shares on most large US names, and Abbas's `portfolio-manager` skill explicitly handles fractional entries ("add 0.5 NVDA at $225"). So a $240 stock sizes fine on a $550 account: 15% = ~$82 = ~0.34 shares. **A high share price is only disqualifying if the name is NOT fractional-eligible** — that's the actual test, not the share price. (This gate previously read "share price > half the max position → drop," which wrongly killed a valid large-cap candidate on 2026-07-28. Fixed 2026-07-29.)
  - Where fractional eligibility is unclear, keep the candidate and flag it: "requires fractional — confirm enabled before entering."
  - The one real sizing constraint that remains: commission. ~$2 round trip on an ~$82 position is ~2.4% of the position, so the trade must clear ~2.4% just to break even. State this drag explicitly on any small-dollar position; it argues for targets ≥5%, not 2-3% scalps.
- If avg_90d_usd_volume looks too thin to exit within a session or two: drop it

**Gate 3 — Exclusion + halal quick check**
- Defense/military contractor, or catalyst is a gov/DoD contract award? Drop, no exceptions.
- Obvious haram business (bank, insurer, alcohol, gambling, weapons, adult, tobacco)? Drop.
- **Large-cap-specific halal traps** — check these, they're easy to wave through on a familiar name: cruise lines and casinos/resorts (onboard casino + alcohol revenue), airlines/hotels only if alcohol is incidental (usually fine), diversified holdings with a conventional insurance or lending arm as a *primary* segment (e.g. a retailer's credit arm is incidental — fine; an insurer is not). Judge on the CORE business, and flag ⚠️ when a major segment is questionable rather than silently passing it.
- Unclear? Keep with ⚠️ flag, Abbas confirms before entering.

**Gate 4 — Is there room left, or is this already extended?** *(added 2026-07-29 — matters most on big gap days)*
- Measure where the current price sits inside the signal day's range, and how far the stop must go to sit below a real invalidation level.
- **If entering now means risking more to the stop than the realistic distance to the first genuine resistance/target, the setup is real but the ENTRY is bad.** Don't drop the candidate and don't recommend chasing it — shortlist it as "WAIT FOR PULLBACK" with the specific price zone that would make the R:R work.
- This is the single most common way a genuinely good momentum setup turns into a bad trade: correct thesis, chased entry.

Candidates surviving all 4 gates go to Phase 3.

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

**Order-plan rule — MANDATORY, added 2026-08-05.** Every shortlisted candidate must carry a complete, copy-paste order plan with explicit DOLLAR levels — entry limit price, stop-limit trigger AND limit prices (derived from the actual invalidation level found in Gate 4, never a percentage guess), TP1 sell limit (TP2 if a clear second resistance exists), and share count at default ~15% sizing. Reason this is non-negotiable: Abbas places GTC orders directly from this email. On 2026-08-04 three buy limits (AXTI, SPXC, GOOG) went into IBKR with NO stop leg and no TP reference because the shortlist email only stated "+X% target" — the levels lived one step away in `stock-analyzer`, which is not a reliable step to assume. The email must be safe to act on directly. If a stop or TP genuinely cannot be derived within the scan, the candidate's order plan must say in bold: **"DO NOT place any order yet — run `analyze [TICKER]` for levels first"** — never leave the fields blank or vague.

**Honesty rule — never pad a thin scan.** Some days the market simply doesn't offer 5 fresh setups that clear the gates. When the scan yields only 1-3 real candidates, present exactly those and say plainly "thin day — [X] candidates cleared the gates," with a short list of what got cut and why (stale, faded-vs-IBKR, excluded, illiquid, wrong account size). A padded list of stale or weak names is worse than a short honest one — every padded name is a candidate for a bad entry. Show the rejects; that's the analyst showing their work.

Format:

---

> ## 🎯 Momentum Shortlist — [today's date]
>
> *[X] candidates found across [Y] sources. [N] cleared all gates. Run `stock-analyzer` on any name for the full deep dive.*
>
> ---
>
> **#1 — [TICKER] | [COMPANY NAME]** ⭐⭐⭐⭐⭐ (5/5) `[SECTOR]` `[SMALL/MID/LARGE CAP]`
> - **Signal:** [what fired — e.g. "Broke above $42 resistance on 3x avg volume Tuesday, held the breakout Wednesday"] — [X] trading days ago
> - **Price:** $[X] (IBKR live) | **Avg daily $ vol:** $[X]M (IBKR) | **RS vs SPY:** [outperforming/underperforming, by how much]
> - **Why it's interesting:** [2-3 sentences — the specific setup, not generic. What's the actual edge and why now.]
> - **Realistic near-term target:** +[4-15]% over [1-10] trading days — [reason: next resistance level, measured move, analyst target cluster]
> - **Entry read:** BUY AT MARKET / **WAIT FOR PULLBACK to $[zone]** — [if extended, say so and give the zone that makes R:R work; never recommend chasing]
> - **Order plan (all three legs together, GTC):** BUY limit **$[X.XX]** · stop-limit trigger **$[X.XX]** / limit **$[X.XX]** (just below [the specific invalidation level — e.g. "the $42 breakout shelf"]) · TP1 sell limit **$[X.XX]** [· TP2 $[X.XX]] · size ~[N] shares ≈ $[X] (~15% of account) · R:R [X.X]:1
> - **Event window:** [earnings/catalyst already behind it ✅ / dated event [X] on [date] → time-stop [date]]
> - **Halal:** ✅ Verified / ⚠️ Unverified — check before entering / ❌ Fails
> - **Defense/military check:** ✅ Clear
> - **Sizing note:** [only if relevant — "requires fractional shares" / commission drag on a small position]
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
