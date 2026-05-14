# Transaction Examples

Worked examples of every transaction type for the portfolio-manager skill.

## Example 1 — BUY new position

**User says:** "I bought 0.4 shares of MSFT at $445"

**Skill response:**

> I'm adding **0.4 shares of MSFT (Microsoft Corporation)** at $445.00 — cost basis $178.00.
>
> Two questions before I save:
>
> 1. **Stop-loss:** auto (-8% = $409.40) or custom?
> 2. **Take-profit ladder:** auto (+15%/+30%/+50% = $511.75 / $578.50 / $667.50) or custom?
>
> Also: any catalyst to track? (earnings date, product launch, etc.)
>
> MSFT is a known AAOIFI-compliant name (Musaffa A+), so halal status confirmed.

**After user confirms "auto, no catalyst":**

> Confirmed. Saving the following:
>
> ```
> + MSFT: 0.4 shares @ $445.00, cost $178.00
>   Stop: $409.40 (-8%)
>   TP1: $511.75 (sell 50%)
>   TP2: $578.50 (sell 50%)
>   Halal: verified today via Musaffa
> ```
>
> Cash: $193.00 → $15.00 (after $178.00 buy)
>
> ⚠️ **Insufficient cash detected.** Your current cash is $15.00 but this trade needs $178.00. Either:
> 1. Deposit more first
> 2. This was already deducted from your account — confirm cash is correct
> 3. Cancel
>
> What's the situation?

## Example 2 — ADD to existing position

**User says:** "Added another 0.25 shares of NVDA at $230"

**Skill response (after reading current state — NVDA was 1.3799 @ $217.40):**

> Adding 0.25 shares of NVDA at $230.00.
>
> **Math:**
> - Existing: 1.3799 shares @ $217.40 (cost basis $300.06)
> - New buy: 0.25 shares @ $230.00 (cost $57.50)
> - **New total: 1.6299 shares**
> - **New avg entry: $219.36** ((1.3799 × $217.40 + 0.25 × $230) / 1.6299)
> - **New cost basis: $357.56**
>
> Stop-loss adjustment? Current stop is $204 (-6.4% from $217.40). With new avg entry $219.36, that's now -7.0% — still within range. Keep as-is, or move to ~$202 to maintain -8%?
>
> Confirm? (yes / adjust stop / cancel)

## Example 3 — Partial SELL

**User says:** "Sold half my AMD at $475"

**Skill response (current AMD: 0.117 shares @ $428.84):**

> Selling 50% of AMD = 0.0585 shares at $475.00.
>
> **Math:**
> - Sold: 0.0585 shares × $475.00 = $27.79 proceeds
> - Cost basis on sold portion: 0.0585 × $428.84 = $25.09
> - **Realized P&L: +$2.70 (+10.8%)**
> - **Remaining: 0.0585 shares** (cost basis $25.08)
>
> Cash: $15.00 → $42.79
>
> Saving this. Want me to suggest a rotation for the freed cash, or hold as dry powder?

## Example 4 — Full SELL (close position)

**User says:** "Sold all my TSM at $410"

**Skill response (current TSM: 0.224 shares @ $388.35):**

> Closing TSM position.
>
> **Math:**
> - Sold: 0.224 × $410.00 = $91.84 proceeds
> - Cost basis: $86.99
> - **Realized P&L: +$4.85 (+5.6%)**
>
> Removing TSM from positions array. Cash: $15.00 → $106.84.
>
> History entry will note: full exit, no remaining position.
>
> Confirm? (yes/no)
>
> If you want, I can suggest where to redeploy the $91.84 — TSM's geopolitical risk was the main reason to exit, so I'd recommend names without that overhang.

## Example 5 — Cash deposit

**User says:** "Got paid $1200 from a client, adding $400 to investments"

**Skill response:**

> Adding $400.00 to your investment cash.
>
> Cash: $15.00 → $415.00
>
> Want me to suggest deployments? Right now your portfolio is:
> - 4 semi positions (NVDA, AVGO, TSM, AMD) = 80% of cost basis
> - 1 healthcare (LLY) = 20%
>
> $400 could:
> - Add to LLY before Foundayo launch (reduces semi concentration)
> - Start a new position (MSFT, ASML, NVO are all halal mega-caps with current catalysts)
> - Be saved as dry powder for post-NVDA-earnings reaction
>
> Or just record the deposit and let you decide? Your call.

## Example 6 — Stop update

**User says:** "Move my NVDA stop to $215 — I'm getting nervous before earnings"

**Skill response:**

> Updating NVDA stop-loss from $204 to $215.
>
> **Math:**
> - Old stop: $204 (-6.4% from entry $217.40)
> - New stop: $215 (-1.1% from entry $217.40)
> - Current price (latest known): ~$228 — your new stop is 5.7% below market
>
> ⚠️ **Heads up:** This is a tight stop. NVDA's typical intraday range is 2-4%. A normal pullback could trigger this without the thesis actually breaking. If you're nervous about earnings, the cleaner trade is usually to *trim 30%* (lock gains) and hold the rest, rather than tighten the stop on full size.
>
> Still want to update the stop, or want to discuss the trim alternative? Your call either way — just flagging the tradeoff.

## Example 7 — TP hit during the day

**User says:** "My NVDA TP1 hit at $240, sold 30% of position"

**Skill response (current NVDA: 1.6299 shares @ $219.36):**

> Logging TP1 execution.
>
> **Math:**
> - Sold: 30% of 1.6299 = 0.4890 shares
> - Proceeds: 0.4890 × $240 = $117.36
> - Cost basis on sold portion: 0.4890 × $219.36 = $107.27
> - **Realized P&L: +$10.09 (+9.4%)**
> - **Remaining: 1.1409 shares** (cost basis $250.29)
>
> Cash: $42.79 → $160.15
>
> TP1 marked as executed. TP2 ($260) and TP3 ($285) still active on remaining shares.
>
> Now you've got $160 of dry powder. Some rotation ideas — these are aggressive given no withdrawal intent:
>
> 1. Start an MSFT position (0.36 shares @ $445) — adds cloud/AI exposure
> 2. Add to LLY before Foundayo (0.16 shares @ ~$995)
> 3. Hold for post-earnings reaction (5 trading days away)
>
> Want to act on any, or hold cash?

## Example 8 — Halal recheck

**User says:** "Just ran Musaffa on all my positions, all clean except AVGO is now A grade instead of A+"

**Skill response:**

> Updating halal verification dates for all 5 positions to today.
>
> No status changes — all 5 still AAOIFI compliant. AVGO grade change (A+ → A) is within Musaffa's internal scoring; doesn't affect compliance threshold. Noting in AVGO's notes field.
>
> History entry: `HALAL_RECHECK` on all positions, date 2026-05-15.
>
> All good. Next quarterly check: target Aug 15, 2026.

## Example 9 — Portfolio query

**User says:** "Show me my current portfolio"

**Skill response (read-only):**

> **Current Portfolio (as of [last_updated])**
>
> | Ticker | Shares | Entry | Cost Basis | % of PF | Stop | Next TP |
> |---|---|---|---|---|---|---|
> | NVDA | 1.3799 | $217.40 | $300.06 | 42.4% | $204 | $240 (sell 30%) |
> | LLY | 0.1407 | $994.87 | $139.98 | 19.8% | $915 | $1,114 (sell 30%) |
> | AVGO | 0.315 | $412.04 | $129.79 | 18.4% | $379 | $474 (sell 50%) |
> | TSM | 0.224 | $388.35 | $86.99 | 12.3% | $357 | $435 (sell 50%) |
> | AMD | 0.117 | $428.84 | $50.17 | 7.1% | $386 | $493 (sell 50%) |
>
> **Total cost basis:** $706.99
> **Cash:** $15.00
> **Total account value (cost basis + cash):** $721.99
>
> ⚠️ NVDA is 42% of portfolio — single-event risk on May 20 earnings.
>
> Halal status: All 5 verified May 11, 2026 (Musaffa AAOIFI). Next recheck: Aug 11, 2026.
>
> Want the live current value (with today's prices) or just cost basis?

## Example 10 — Mistake / undo

**User says:** "Wait, I said 0.4 MSFT but I actually bought 0.04 shares — way smaller"

**Skill response (assuming the previous BUY hasn't been saved yet):**

> No problem. Updating before save:
>
> - Shares: 0.04 (not 0.4)
> - Cost: $17.80 (not $178.00)
> - Cash: $15.00 → -$2.80 ⚠️ Still insufficient cash. Did you deposit more, or is this from a different funding source?

**If the bad data was ALREADY saved:**

> Got it. Two ways to fix:
>
> 1. **Correction entry:** I'll add a correction note to history, then update the position to the correct shares
> 2. **Restore from previous commit:** Roll back the GitHub commit
>
> Option 1 is cleaner — preserves audit trail. Should I proceed?
