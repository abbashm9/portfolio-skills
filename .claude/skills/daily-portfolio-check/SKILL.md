---
name: daily-portfolio-check
description: Run a daily post-market portfolio review for Abbas's halal stock portfolio — fetches live closing prices, calculates P&L per position and total, evaluates each position against its exit strategy (stop-loss, take-profit ladder, time-based exit, catalyst), flags any positions needing action, and proposes rebalancing or rotation moves. Since Abbas isn't withdrawing money, suggestions can be aggressive (e.g., trim 30% of a winner to buy 1 share of a new high-conviction name). Use whenever Abbas says "daily check", "portfolio check", "how am I doing", "market closed", "check my stocks", "run the daily", or any variant of "review my portfolio." Trigger even if he just says "daily" or pastes a screenshot of his brokerage app at end of day.
---

# Daily Portfolio Check

A post-NYSE-close daily review skill for Abbas's halal stock portfolio. One message from the user triggers the full review.

## When to use

Trigger on any of: "daily check", "portfolio check", "how am I doing", "market closed", "check my stocks", "run the daily", "review my portfolio", "daily", or similar end-of-day review requests.

## Context (always-true facts)

- **User:** Abbas Al Madani, based in Kuwait
- **Strategy:** Halal-compliant, aggressive growth/momentum
- **Withdrawal intent:** None — he's not pulling money out, so rotation suggestions can be aggressive (e.g., "trim 30% of NVDA to buy 1 share of X")
- **Halal compliance:** AAOIFI standards, re-verify quarterly
- **Disclosure:** This is research, not financial advice

## Current Portfolio (baseline — update as positions change)

| Ticker | Shares | Entry Price | Cost Basis | Stop-Loss | TP1 | TP2 | TP3 | Key Catalyst |
|--------|--------|-------------|------------|-----------|-----|-----|-----|--------------|
| NVDA | 1.3799 | $217.40 | $300.06 | $204 | $240 (sell 30%) | $260 (sell 40%) | $285+ (hold 30%) | Earnings May 20, 2026 |
| LLY | 0.1407 | $994.87 | $139.98 | -8% ($915) | +12% ($1,114) sell 30% | +25% ($1,243) sell 40% | +40% ($1,393) hold 30% | Foundayo launch Q2 |
| AVGO | 0.315 | $412.04 | $129.79 | -8% ($379) | +15% ($474) sell 50% | +30% ($536) hold 50% | — | Earnings early June |
| TSM | 0.224 | $388.35 | $86.99 | -8% ($357) | +12% ($435) sell 50% | +25% ($485) hold 50% | — | Geopolitical risk |
| AMD | 0.117 | $428.84 | $50.17 | -10% ($386) | +15% ($493) sell 50% | +30% ($558) hold 50% | — | Earnings Aug 4, 2026 |

**Total cost basis: $706.99**
**Universe to consider for rotations:** From the halal-stock-picker skill's `halal-universe.md` — prioritize MSFT, ASML, QCOM, TXN, AMAT, LRCX, KLA, ABT, ISRG, NVO, JNJ, SHOP, CRWD, PANW, ADBE, ORCL, SPUS, HLAL.

## Workflow — Every Daily Check

### Step 1: Fetch current prices

Use `web_search` for each ticker to get the latest closing price. Don't rely on training data. Search the actual current date.

### Step 2: Build the snapshot table

| Ticker | Shares | Entry | Current | Cost Basis | Current Value | P&L $ | P&L % | Day Change |
|--------|--------|-------|---------|------------|---------------|-------|-------|------------|
| ... | | | | | | | | |
| **TOTAL** | | | | $X | $X | +/-$X | +/-X% | +/-X% |

Always include:
- Per-position cost basis vs current value
- Day's $ and % change (vs prior close, not vs entry)
- Total portfolio cost basis, current value, P&L, and % return since inception

### Step 3: Exit-strategy check per position

For each position, run through:

1. **Stop-loss check** — Is the price below the stop level? If yes → **SELL ALERT**
2. **TP1 check** — Has it hit TP1? If yes → recommend trimming the specified %
3. **TP2 check** — Has it hit TP2? If yes → recommend trimming further
4. **TP3 check** — Has it hit TP3? If yes → recommend full exit or trailing stop
5. **Catalyst proximity** — Is a catalyst within 5 trading days? Flag it.
6. **Halal compliance** — Any news on debt, M&A, or business changes that could affect AAOIFI status? Flag.
7. **Time-based exit** — Has position been flat ±3% for 30+ days with no catalyst? Suggest trimming.
8. **Parabolic warning** — RSI overbought (>80) after a big run? Flag possible mean reversion.

Output a clear status per position:
- ✅ HOLD — Within range, thesis intact
- ⚠️ WATCH — Approaching a level, no action yet
- 🔔 ACTION — Hit a level, recommend trim/exit
- 🚨 ALERT — Stop hit or thesis broken, exit now

### Step 4: Market context (brief)

3–5 lines covering:
- Major indices' day's move (S&P, Nasdaq)
- Any sector-specific news affecting Abbas's positions
- Upcoming catalysts in next 5 trading days

### Step 5: Rotation suggestions (the exciting part)

Since Abbas isn't withdrawing money, propose aggressive rotations when:

- **A position hits TP1 or TP2** → Suggest where to redeploy the freed cash
- **A new high-conviction halal name emerges** → Suggest trimming a winner to fund it
- **A position is dead money** (flat 30+ days) → Suggest a rotation
- **A new catalyst is approaching on a stock he doesn't own** → Suggest a small position

Format rotation suggestions like:

> 🔄 **Suggested rotation:** Trim 30% of NVDA (~$25 freed) and buy 0.05 shares of ASML. Rationale: [1-line thesis]. Risk: [1-line]. Your call.

Always include:
- Exact dollar amount being freed up
- Exact share quantity being suggested (account for fractional shares)
- One-line rationale + one-line risk
- Reminder that the user decides

### Step 6: Halal compliance refresh

Once a week (Fridays), remind to re-verify halal status on Zoya/Musaffa. Note any business changes that might affect compliance (large debt raises, M&A in non-compliant sectors, etc.)

### Step 7: Wrap-up

End with a clear "what to do tomorrow" line:
- "No action needed — review again Friday close" (most common)
- "Action: place limit sell at $X for NVDA TP1, 0.11 shares"
- "Catalyst tomorrow: NVDA earnings after close. Decide now whether to trim before print."

## Output style

- **Lead with the headline:** total P&L $ and % since inception, day's move
- **Status table:** snapshot with all positions
- **Action items:** bulleted, specific, with exact share quantities and prices
- **Rotation suggestions:** separate section, clearly framed as suggestions
- **Brief market context:** 3–5 lines, no fluff
- **No long disclaimers** every day — keep it tight; user knows the standard caveats

## Special triggers

- **Day before a held name's earnings:** Highlight the decision (hold through / trim / exit before print). Ask Abbas to decide BEFORE the print, not in the moment.
- **Halal compliance breach detected:** Override everything else — recommend exit at next open regardless of P&L
- **Portfolio down >8% from cost basis:** Stop suggesting new entries. Move to defensive review.
- **Portfolio up >20% from cost basis:** Suggest taking some profits even if no individual TP has hit, to lock gains.
- **NYSE holidays:** If markets are closed, skip the daily check and tell the user. Reference the US market calendar.

## What this skill does NOT do

- Execute trades — user does this himself in his broker
- Give financial advice — this is research output
- Make halal rulings — refer to qualified scholars for borderline cases
- Track positions Abbas doesn't actually own — if he hasn't confirmed buying it, it's not in the portfolio

## Updating positions

When Abbas reports new buys/sells, update the position table in this SKILL.md or note the change in conversation. Always confirm:
- Exact shares bought/sold
- Exact fill price
- Updated cost basis for that position

## Reference files

- `references/exit-rules.md` — Detailed exit logic (mirrors halal-stock-picker skill)
- `references/rotation-playbook.md` — When and how to suggest rotations
