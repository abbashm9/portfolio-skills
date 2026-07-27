# Decisions Log

Append-only record of strategy decisions for Abbas's halal stock portfolio and why they were made.

---

## 2026-07-27 — Pause binary-catalyst trading, pivot to daily momentum discovery

**Trigger:** CAPR stopped out at $5.80 on 2026-07-27, two days before the July 29 AdCom vote the trade was built around. Stop was correctly placed at $14, but it was a plain STOP order — once the market gapped down hard at the open (pre-event), the order triggered and filled as a market order at $5.80, 59% below the trigger. Net P&L: -$234.73 (-71.9%).

**Pattern across the last 5 closed trades:**
- 3 losers, all binary PDUFA/AdCom catalyst bets: CELC (-$26.32), VERA (-$33.28), CAPR (-$234.73)
- 2 winners, both plain momentum trades with real stops: ANET (+$36.43, +18.2%), META (+$4.49, +1.2%)
- Net: -$253.41 across the 5 trades

**Root cause, structural not just bad luck:** stop-losses cannot protect against binary-catalyst gap risk. A stop assumes gradual price movement; a catalyst event (or pre-event sentiment shift) moves the price in one discontinuous jump, and by the time the market reopens the price has already gapped past any stop level. Sizing one position at ~30% of the portfolio for a single dated event means one loss erases 5-6 wins the size of ANET.

**Decision:**
1. Pause binary-catalyst (FDA PDUFA/AdCom, single dated-event) trading for now.
2. Shift to daily momentum/technical discovery — breakouts, volume surges, unusual options flow, insider buying clusters, relative-strength leadership, gap-continuation. Sector-agnostic: no sector preference, only exclusions are haram businesses (per CLAUDE.md's business-activity halal definition) and defense/military contractors (Abbas's personal exclusion, separate from and in addition to the halal screen).
3. Target smaller, faster trades: 5-15% gains, held days not weeks (not the 2-week-plus holds that preceded the binary losses), many positions instead of one dominant bet.
4. Cap position size at 15-18% of portfolio per name; target 5-7 concurrent positions when cash allows.
5. All stops going forward must be **stop-limit**, not plain stop-market — a plain stop offers no protection against exactly the gap risk that just cost $234.73.
6. Discovery now runs automatically in the daily 6am email (`daily-portfolio-check` Step 3.5) in addition to on-demand (`stock-finder`).

**How to apply:** Any new trade proposal — from `stock-finder`, `stock-analyzer`, or the daily email — should be screened against this decision. A dated future event alone (earnings date, FDA date) is not sufficient reason to enter; there needs to be a live technical or flow signal firing now. Revisit this pause once there's a track record of momentum trades to evaluate — this isn't a permanent ban on binary catalysts, it's a pause pending evidence the alternative works better.

**July 31 monthly goal ($1,000 total account value):** acknowledged as not achievable this month given the CAPR loss. Not forcing trades to chase it in the remaining days — that pressure is exactly what feeds binary-catalyst thinking.
