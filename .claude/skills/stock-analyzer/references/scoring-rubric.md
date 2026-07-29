# Conviction Scoring Rubric — 0 to 10 (Momentum Era, v2)

Rebuilt 2026-07-29 for the post-pivot momentum strategy (see `decisions.md`, 2026-07-27). The old rubric scored binary-catalyst quality (confirmed event dates, AdCom votes, approval probability) — none of which is the thesis anymore. This one scores what actually predicts a fast momentum trade working: signal freshness, structure, participation, and whether the company can blow up underneath the trade.

Every analyzed stock gets a score with a point-by-point breakdown — never just a number. The breakdown makes the score contestable: if Abbas disagrees with a point, he can challenge it directly.

---

## Scoring breakdown (10 points total)

### 1. Signal freshness (0, 1, or 2 points)

**2 points:** The technical/flow signal fired within the last **1-2 trading days** and is intact (price holding above the trigger level).

**1 point:** Signal fired **3-5 trading days ago** and is still intact — no close back below the trigger.

**0 points:** Signal older than 5 trading days, OR price has already closed back below the trigger level (the edge is gone), OR there is no live signal at all — just a story, a future dated event, or a "cheap" valuation argument.

> A future catalyst date is worth 0 here no matter how exciting. If the only thing interesting is a date on the calendar, this is not a momentum trade.

---

### 2. Structure quality (0, 1, or 2 points)

**2 points:** Clean, definable structure from the actual OHLCV bars: a breakout above weeks-long resistance, a flag/consolidation continuation, or a gap-and-hold — with an obvious invalidation level (you can point at the exact price that proves the trade wrong).

**1 point:** Real move but messy structure — extended from the base, wide/overlapping bars, or the invalidation level is far enough away that the stop gets expensive.

**0 points:** One-day spike inside a downtrend, no definable base, or no invalidation level closer than a catastrophic distance. A spike inside a downtrend is a fade candidate, not a momentum entry.

---

### 3. Volume confirmation (0 or 1 point)

**1 point:** Signal-day volume ≥ 2x the 90-day average (from real IBKR bars, not narrative), and volume on any pullback days since is lighter than the signal day.

**0 points:** Signal on average or below-average volume — a move nobody participated in is a move nobody defends.

---

### 4. Relative strength (0 or 1 point)

**1 point:** Clearly outperforming its sector peers and SPY over the signal window (compare IBKR `cumulative_perf_1w` / `_1m` against SPY's).

**0 points:** Moving with the market/sector tide rather than leading it, or underperforming.

---

### 5. Liquidity for a fast exit (0 or 1 point)

**1 point:** IBKR `avg_90d_usd_volume` comfortably supports entering AND exiting the full position within a session without moving the price, and the bid-ask spread is tight.

**0 points:** Thin tape, wide spread, or a share price so high the position can't size sanely on this account (one share > ~half the max allocation). Note: a 0 here is usually a hard SKIP, not just a lost point — a momentum trade you can't exit fast is a trap.

---

### 6. Fundamentals health (0 or 1 point)

**1 point:** Passes the Section-4 health check with 0-1 red flags (no negative equity, no consistent-miss pattern, no imminent dilution/cash crisis, debt manageable).

**0 points:** 2+ red flags. The trade can still proceed as an explicitly-labeled "momentum on a weak company" play, but it loses this point AND triggers the mandatory adjustments: 10-12% sizing, tighter time-stop, never hold through a dated event. (This point exists because a GRPN buy call once went out with negative equity, 4 straight misses, and negative cash flow unexamined — Abbas caught it, not the analysis.)

---

### 7. Risk/reward ≥ 2:1 (0 or 1 point)

**1 point:** Distance from entry to Target 1 (nearest REAL resistance) is at least 2x the distance from entry to the stop (just below REAL support). Both levels from actual market structure, not percentages.

**0 points:** R:R below 2:1. On a fast trade with ~$2 round-trip commission and slippage, thin R:R means the math barely clears even when right.

---

### 8. Clean event window (0 or 1 point)

**1 point:** No binary dated event (earnings, FDA/regulatory, court, lock-up) inside the expected 1-10 trading-day holding window — clean runway.

**0 points:** A dated event sits inside the window. The trade can survive this ONLY with a hard time-stop set before the event date (exit regardless of price — the CAPR lesson: the gap can come before the event). If the event is so close there's no runway for the trade to work first (< ~3 trading days), treat as SKIP regardless of total score.

---

### 9. Smart money confirmation (0 or 1 point)

**1 point:** At least one of: insider open-market cash purchase in the last 90 days; a known fund opening/majorly increasing a position in the latest 13F; unusual call buying above the current price within the last 2 weeks, aligned with the momentum direction.

**0 points:** No visible smart-money positioning — or flow pointing the other way (opportunistic insider selling, put sweeps).

---

## Total and interpretation

| Score | Label | Recommendation |
|---|---|---|
| 8-10 | **Strong setup** | BUY — full 15-18% sizing (10-12% if fundamentals-flagged) |
| 7 | **Good setup** | BUY — standard sizing, tighter time-stop |
| 5-6 | **Borderline** | WATCH — state exactly what flips it to BUY (usually one more confirmation day or a pullback entry) |
| 3-4 | **Weak** | SKIP — no live edge or bad structure |
| 0-2 | **No setup** | SKIP — do not force it |

---

## Override rules — these beat the score, always

- **Halal business-activity failure:** automatic SKIP. No exceptions.
- **Defense/military contractor, or the catalyst is itself a gov/DoD contract award:** automatic SKIP. Separate from halal, no exceptions.
- **No live signal (factor 1 = 0 for staleness/absence):** cannot be BUY regardless of total. Best case WATCH.
- **Liquidity fail (factor 5 = 0):** SKIP — an exit you can't execute isn't a plan.
- **Event inside window with no room to work first:** SKIP.
- **Every stop is a STOP-LIMIT.** Not scored — mandated. A plain stop became a market order and turned a planned -36% into a -72% fill on 2026-07-27.

---

## How to present the score

Point-by-point table, exactly like this:

> **Conviction score: 7/10**
>
> | Factor | Points |
> |---|---|
> | Signal freshness (fired yesterday, intact) | ✅ 2/2 |
> | Structure quality (clean breakout, tight invalidation) | ✅ 2/2 |
> | Volume ≥ 2x average on signal day | ✅ 1/1 |
> | Relative strength vs sector/SPY | ❌ 0/1 — moving with the sector, not leading |
> | Liquidity for fast exit | ✅ 1/1 |
> | Fundamentals health (0-1 red flags) | ❌ 0/1 — negative op. cash flow + 3 misses → 10-12% sizing, tight time-stop |
> | Risk/reward ≥ 2:1 to first real resistance | ✅ 1/1 |
> | Clean event window | ❌ 0/1 — earnings Aug 6 inside window → hard time-stop Aug 5 |
> | Smart money confirmation | ❌ 0/1 — nothing visible |
> | **Total** | **7/10 → BUY (reduced size, time-stop Aug 5)** |
