---
name: stock-finder
description: Proactive catalyst discovery engine. Scans the FDA calendar, clinical trial databases, SEC filings, unusual options flow, insider buying clusters, and short squeeze setups to surface 5–10 small/mid-cap stocks with imminent high-impact catalysts that most people aren't talking about yet. The output is a ranked shortlist of candidates for Abbas to pick from — each one ready to hand to stock-analyzer for a full deep dive. Use whenever Abbas says "find me something", "what's moving this week", "any catalyst plays", "hunt for stocks", "find catalyst plays", "what should I be looking at", "discovery run", or any variant of wanting new ideas rather than analyzing a specific ticker.
---

# Stock Finder — Catalyst Discovery Engine

This skill's only job is **finding**. Not analyzing deeply — that's stock-analyzer's job. The finder casts a wide net, does a fast pre-screen, and hands Abbas a shortlist of names worth investigating further.

The goal: surface stocks that have a dated, near-term binary event that could produce a 100–1000%+ move, that nobody in the mainstream financial media is currently talking about.

---

## Critical rule: everything from live search

**Every run must use fresh web_search results.** Training data is useless for discovery — the catalysts we're hunting are happening right now, this week, this month. Never answer this skill from memory.

---

## Workflow

### Phase 1: Cast the net (all searches in parallel)

Run all of these simultaneously. The goal is raw candidates — volume matters here, not precision. Precision comes in Phase 2.

**FDA & regulatory:**
1. `FDA PDUFA action dates [current month] [next month] upcoming decisions`
2. `site:biopharmcatalyst.com PDUFA [current month] OR [next month]`
3. `FDA NDA BLA "action date" [current month] [next month] 2026`
4. `"complete response letter" OR "CRL resubmission" PDUFA 2026 upcoming`
5. `"advisory committee" OR AdCom meeting scheduled [current month] [next month] FDA`

**Clinical trial readouts:**
6. `"phase 3" "data readout" OR "results expected" [current month] [next month] biotech`
7. `"interim analysis" OR "primary endpoint" expected [current month] OR [next month] 2026`
8. `site:clinicaltrials.gov "estimated completion" [current month] [next month] phase 3`

**Unusual market signals:**
9. `"unusual options activity" small cap [today's date] OR [this week]`
10. `"insider buying" cluster OR multiple [current month] small cap`
11. `"short squeeze" catalyst upcoming [current month] 2026`
12. `"most shorted stocks" catalyst upcoming 2026`

**Pre-market and momentum:**
13. `"premarket movers" OR "premarket gainers" [today's date] catalyst`
14. `"small cap" "upcoming catalyst" OR "binary event" [current month] [next month]`
15. `biotech catalyst calendar [current month] [next month] 2026`

From this batch, extract all distinct tickers mentioned. Aim for 15–25 raw candidates. Duplicates across sources = stronger signal.

---

### Phase 2: Rapid pre-screen (per candidate, fast)

For each raw candidate, apply a 3-gate filter. This takes 30–60 seconds per name — not a deep dive. If a gate fails, drop the candidate and move on.

**Gate 1 — Event date confirmed?**
- Does it have a specific, confirmed catalyst date within 45 days?
- If no confirmed date: drop it

**Gate 2 — Float and market cap in range?**
- Market cap < $2B? (preferably < $500M for max move potential)
- Quick search: `"[TICKER]" market cap float shares`
- If market cap > $2B: drop it (big-cap plays don't move the needle on an $800 portfolio)

**Gate 3 — Halal quick check**
- Search: `"[TICKER]" revenue breakdown OR "interest income" OR halal OR Musaffa`
- Any obvious disqualifiers? (bank, insurance, alcohol, weapons)
- If clearly not halal: drop it
- If unclear: keep with ⚠️ flag, Abbas confirms before entering

Candidates surviving all 3 gates go to Phase 3.

---

### Phase 3: Score and rank surviving candidates

For each surviving candidate, run a fast 5-point conviction pre-score. This is NOT the full 10-point scoring rubric from stock-analyzer — that comes later. This is a fast filter to rank the shortlist.

| Factor | Points |
|---|---|
| Event ≤ 14 days out | 2 |
| Event 15–45 days out | 1 |
| Short interest ≥ 15% of float | 1 |
| Appears in 2+ of the Phase 1 search sources (duplicate signal) | 1 |
| Any smart money signal visible (insider buy, big fund 13F, unusual options) | 1 |
| **Max** | **5** |

Score each candidate. Sort by score descending.

---

### Phase 4: Output — ranked shortlist

Present the top **5–10 candidates** ranked by pre-score. Format:

---

> ## 🎯 Catalyst Shortlist — [today's date]
>
> *[X] candidates found across [Y] sources. Showing top [N] by conviction pre-score. Run `stock-analyzer` on any name for the full deep dive.*
>
> ---
>
> **#1 — [TICKER] | [COMPANY NAME]** ⭐⭐⭐⭐⭐ (5/5)
> - **Catalyst:** [what event] on **[exact date]** ([X] days from now)
> - **Market cap:** $[X]M | **Float:** $[X]M | **Short interest:** [X]%
> - **Why it's interesting:** [2–3 sentences — what makes this specific setup compelling. Not generic. Specific: "Phase 3 in non-small cell lung cancer with BTD — same indication where Keytruda got approved in 2014 and ran +280% at approval. AdCom hasn't been scheduled yet which may mean FDA is comfortable approving without one."]
> - **Halal:** ✅ Verified / ⚠️ Unverified — check Musaffa / ❌ Fails
> - **Next step:** `analyze [TICKER]`
>
> ---
>
> **#2 — [TICKER] | [COMPANY NAME]** ⭐⭐⭐⭐ (4/5)
> [same format]
>
> ---
> [continue for all candidates]

---

### Phase 5: Highlight the single best setup

After the full shortlist, add a one-paragraph summary:

> **Today's best setup:** [TICKER] — [2–3 sentence case for why this is the most compelling name on the list right now, referencing specific data points: the catalyst date, the float size, the short interest, any smart money signal. End with the honest risk: what kills this trade if it goes wrong.]

---

## What this skill does NOT do

- Deep fundamental analysis — that's `stock-analyzer`
- Portfolio updates — that's `portfolio-manager`
- Guarantee any of these plays work — research only
- Daily email — this is on-demand, chat output only
- Cover large-cap names — if a name is on CNBC or in Instagram groups, it doesn't belong in this output

## How to use the output

The shortlist is a menu, not a trade recommendation. The right workflow:

1. Scan the shortlist
2. Pick 1–2 names that feel interesting
3. Say "analyze [TICKER]" — the `stock-analyzer` runs the full 8-section deep dive
4. Decide based on the conviction score
5. If conviction ≥ 7: enter the trade and log it with `portfolio-manager`

The `stock-finder` output alone is NOT enough to enter a trade. It's a first filter, not a final decision.

---

## Refresh cadence

Run this skill:
- **Once a week minimum** — catalyst calendars update weekly
- **Any time a position hits a take-profit** — freed cash needs a new home
- **When you feel like the portfolio is stagnant** — the market always has something brewing

Do NOT run it every day and chase every single name — that creates overtrading. Find candidates, then be patient with the ones that make the cut.
