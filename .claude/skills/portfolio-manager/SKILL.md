---
name: portfolio-manager
description: Update Abbas's halal stock portfolio when he reports buys, sells, deposits, withdrawals, or changes to stops/take-profits. Reads and updates the portfolio.json file in his GitHub repo (abbashm9/portfolio-skills). Trigger this skill whenever Abbas says things like "I bought X shares of Y at $Z", "I sold half my AMD", "add 0.5 NVDA at $225", "I deposited $300", "show me my portfolio", "what do I own", "update stop on NVDA to $210", "trim my LLY position", "I sold all my TSM", or any variant where he reports a transaction or asks about current holdings. Also triggers when he says "log this trade" or "record my buy."
---

# Portfolio Manager

A skill that maintains Abbas's portfolio state in `portfolio.json` (in his GitHub repo `abbashm9/portfolio-skills`). Reads, updates, validates, and commits portfolio changes.

## When to use

Trigger on any of:
- Buy/sell reports: "I bought 0.5 NVDA at $225", "Sold half my AMD", "Add LLY 0.2 shares"
- Cash changes: "Deposited $500", "Added $300 to invest"
- Stop/TP updates: "Move my NVDA stop to $210", "Update TSM TP1 to $440"
- Position queries: "Show my portfolio", "What do I own", "Current positions"
- Catalyst updates: "NVDA earnings was actually May 22", "Note: LLY launch delayed"

## Critical context

- **User:** Abbas Al Madani, Kuwait, 8 years forex/indices, new to single-name US equities
- **Strategy:** Halal-compliant (AAOIFI), aggressive growth/momentum
- **Withdrawal intent:** None — money stays invested, growth-focused
- **Source of truth:** `portfolio.json` in `abbashm9/portfolio-skills` repo (currently public)
- **Stop/TP policy:** Ask each time when adding new position — sometimes auto, sometimes custom

## Workflow

### Step 1: Read current state

**For any update, ALWAYS read the current `portfolio.json` first.** Never assume — the file is the truth.

Two ways to read it depending on context:
1. **In claude.ai web with GitHub connector:** use connector to fetch the file
2. **Without GitHub connector:** fetch via raw GitHub URL (works for public repos): `https://raw.githubusercontent.com/abbashm9/portfolio-skills/main/portfolio.json`

If the file can't be read, STOP and tell Abbas to verify the repo is accessible. Do not proceed without current state.

### Step 2: Parse the request

Identify what kind of change is being made:

| Request type | Examples | Action |
|---|---|---|
| **BUY (new position)** | "Bought 0.5 MSFT at $445" | Add new position object, ask for stops/TPs |
| **BUY (add to existing)** | "Added 0.3 more NVDA at $220" | Update existing position: recalculate avg entry, shares, cost basis |
| **SELL (partial)** | "Sold half my AMD at $475" | Reduce shares, log realized P&L, keep position |
| **SELL (full)** | "Sold all my TSM at $410" | Remove position entirely, log final P&L |
| **CASH DEPOSIT** | "Deposited $300" | Increase `cash_available` |
| **CASH WITHDRAW** | "Took out $100" | Decrease `cash_available` (rare, since withdrawal_intent is false) |
| **STOP UPDATE** | "Move NVDA stop to $210" | Update `stop_loss` and `stop_loss_pct` |
| **TP UPDATE** | "Change LLY TP1 to $1100" | Update specific TP object |
| **CATALYST UPDATE** | "NVDA earnings moved to May 22" | Update `catalyst` field |
| **HALAL REVERIFICATION** | "Just checked Musaffa, all clean" | Update `halal_verified` date for each position |
| **QUERY** | "Show portfolio" | Read-only, no update |

### Step 3: Validate the math

Before pushing any change, validate:

- **New cost basis** = shares × entry price (within $0.01 tolerance)
- **For adds:** new avg entry = (old_shares × old_entry + new_shares × new_price) / total_shares
- **For sells:** realized P&L = sold_shares × (sold_price − avg_entry)
- **Shares cannot go negative** — if user reports selling more than they own, flag the error
- **Cash cannot go negative** — flag if buy exceeds cash_available
- **Date formats:** ISO 8601 (`YYYY-MM-DD` for dates, `YYYY-MM-DDTHH:MM:SS+03:00` for timestamps)
- **All numeric fields:** validated as numbers, not strings

### Step 4: For NEW positions — ask about stops/TPs

When adding a position that wasn't in the portfolio before, ask Abbas:

> "I'm adding [X shares] of [TICKER] at $[price] (cost basis $[Y]). Two questions before I save:
> 
> 1. **Stop-loss:** auto (-8% to -10% based on volatility) or custom?
> 2. **Take-profit ladder:** auto (+15% / +30% / +50% standard) or custom?
>
> Also: catalyst to track? (earnings date, product launch, etc. — optional)"

Wait for his answer. Use defaults if he says "auto." Apply custom values if he specifies. Either way, confirm the full setup before pushing.

**Auto-default rules:**

| Stock type | Stop | TP1 | TP2 | TP3 |
|---|---|---|---|---|
| High-beta semi (NVDA, AMD, ASML) | -7% to -8% | +12-15% sell 30% | +25-30% sell 40% | +40-50% hold 30% |
| Mid-beta semi/tech (AVGO, MSFT, TSM) | -8% | +15% sell 50% | +30% hold 50% | none |
| Defensive (LLY, JNJ, ABT) | -8% | +12% sell 30% | +25% sell 40% | +40% hold 30% |
| Cyclical (MU, MEM) | -10% | +15% sell 40% | +30% sell 35% | +50%+ hold 25% |

### Step 5: Halal verification check

For NEW positions, before adding, verify halal status:
1. Check `references/halal-universe.md` for known-compliant names
2. If unknown, prompt: "Have you verified [TICKER] on Zoya or Musaffa? AAOIFI compliance is non-negotiable."
3. Wait for confirmation before proceeding
4. Set `halal_verified` to today's date and `halal_source` to whatever Abbas reports

### Step 6: Present the diff to confirm

Before pushing to GitHub, show Abbas the full change in a table:

```
**Change to portfolio.json:**

Position: NVDA
- Shares: 1.3799 → 1.6299 (+0.25)
- Avg entry: $217.40 → $218.16  
- Cost basis: $300.06 → $354.91 (+$54.85)

Cash: $15.00 → -$39.85 ⚠️ INSUFFICIENT CASH — please deposit before this trade

Confirm? (yes/no/edit)
```

Wait for explicit confirmation. Do not push without "yes" or equivalent.

### Step 7: Update history

Always append to the `history` array:

```json
{
  "date": "2026-05-15",
  "action": "BUY",
  "ticker": "MSFT",
  "shares": 0.4,
  "price": 445.00,
  "amount": 178.00,
  "notes": "Optional notes from Abbas"
}
```

Actions: `BUY`, `SELL`, `DEPOSIT`, `WITHDRAW`, `STOP_UPDATE`, `TP_UPDATE`, `HALAL_RECHECK`, `CATALYST_UPDATE`

### Step 8: Update totals

Recalculate after every change:
- `total_cost_basis` = sum of all positions' cost_basis
- `totals.positions_count` = number of positions
- `totals.sectors_held` = unique sectors across positions
- `totals.largest_position_pct` = largest cost_basis / total_cost_basis × 100
- `totals.concentration_warning` = generate if any position >40%, otherwise null
- `last_updated` = current ISO 8601 timestamp in Asia/Kuwait

### Step 9: Push to GitHub

Use the GitHub connector to commit and push the updated `portfolio.json`.

Commit message format: `Update portfolio: [ACTION] [ticker/amount]`

Examples:
- `Update portfolio: BUY 0.25 NVDA @ $220`
- `Update portfolio: SELL 50% AMD @ $475`
- `Update portfolio: DEPOSIT $300`
- `Update portfolio: STOP_UPDATE NVDA to $210`

### Step 10: Confirm to user

Reply with:
- ✅ Confirmation that the change was saved
- Updated position summary
- Any flags (concentration, low cash, missing halal verification)
- Next daily check will use updated portfolio

## Special cases

### Adding cash from client payment

When Abbas says "got paid $X from client, adding Y to investment":
1. Update `cash_available` by Y
2. Log to history as `DEPOSIT`
3. Note in commit message
4. Optionally suggest deployment ideas based on current opportunities (but only if asked)

### Selling for a loss

When a sell results in a loss:
1. Calculate realized loss
2. Note it in history with the loss amount
3. Don't lecture about it — Abbas is an experienced trader
4. If the loss was due to a stop-loss hit, note "STOP-LOSS EXIT" in the history entry

### Stops/TPs hit during the day

If Abbas reports "my NVDA TP1 hit, sold 30%":
1. Reduce shares by the sold amount
2. Log as SELL with realized P&L
3. Note "TP1_HIT" in notes
4. Update the position's TP1 status (or remove TP1 if fully exhausted)
5. Suggest considering rotation per the rotation-playbook

### Portfolio screenshot uploaded

If Abbas uploads a brokerage screenshot (Wahed, Robinhood, etc.):
1. Parse what positions and shares are shown
2. Compare to current portfolio.json
3. Highlight any discrepancies
4. Ask which version is correct
5. Update accordingly

## What this skill does NOT do

- Execute trades (broker only)
- Recommend specific buys without being asked
- Modify halal verification dates without explicit user confirmation
- Allow shares to go negative (math validation prevents)
- Push without showing diff and getting confirmation
- Touch other files in the repo (only portfolio.json)

## Reference files

- `references/portfolio-schema.md` — Full JSON schema and field definitions
- `references/transaction-examples.md` — Worked examples of each transaction type
- `references/halal-universe.md` — Pre-vetted compliant stocks (mirrors halal-stock-picker skill)
