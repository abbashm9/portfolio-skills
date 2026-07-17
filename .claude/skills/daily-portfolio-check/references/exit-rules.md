# Exit Rules — Daily Check Reference

Concise decision tree for the daily portfolio review.

## Per-position decision tree

For each position, in this order:

### 1. Halal compliance breach?
- Yes → 🚨 EXIT at market open next session, regardless of P&L
- No → continue

### 2. Stop-loss hit?
- Current price ≤ stop level → 🚨 EXIT entire position
- Within 2% of stop → ⚠️ WATCH, alert user
- Above stop by >2% → continue

### 3. Take-profit levels?
- ≥ TP3 → 🔔 ACTION: hold final tranche or trail stop tight; suggest taking some
- ≥ TP2 → 🔔 ACTION: trim TP2 percentage
- ≥ TP1 → 🔔 ACTION: trim TP1 percentage
- Between entry and TP1 → ✅ HOLD

### 4. Below entry but above stop?
- Within 3% of entry → ✅ HOLD (normal noise)
- Down 3–7% from entry → ⚠️ WATCH, check for thesis-breaking news
- Down 7%+ from entry (and stop not hit) → ⚠️ Reassess — tighter stop or partial exit

### 5. Time-based check
- Flat (±3% from entry) for 30+ days, no upcoming catalyst → ⚠️ Consider trimming 50%
- Flat for 60+ days → 🔔 ROTATE out

### 6. Catalyst proximity
- Earnings within 1 trading day → ⚠️ FLAG: decide hold/trim/exit before print
- Earnings within 5 trading days → Note in summary
- Other catalyst within 5 days → Note in summary

### 7. Parabolic warning
- Stock up >40% in 30 days AND RSI >80 → ⚠️ Mean-reversion risk; consider trim 30%
- One-day drop >8% on no news after parabolic run → 🚨 Likely cycle top, exit remaining

## Universal portfolio rules

| Condition | Action |
|---|---|
| Single position >45% of portfolio | Trim back to original target weight |
| Portfolio down >8% from cost basis | Stop new entries, defensive review |
| Portfolio up >20% from cost basis | Suggest taking 10–20% off the table to lock gains |
| Stop-loss already hit | Never average down — re-entry only on new setup |
| Halal compliance breach | Overrides everything — exit next open |

## TSM-specific override

Any credible Taiwan Strait military escalation (PLA encirclement exercises, US naval response, major diplomatic crisis) → **sell TSM at market open immediately**. This is binary tail risk that can't be hedged.

## Cyclical semi override

If MU (when held) or other deeply cyclical semi has -8% one-day drop on no news after parabolic run → likely cycle top. Sell remaining position that day, don't wait.

## Pre-earnings decision template

For any position with earnings within 5 trading days, present three options BEFORE the print:

1. **Hold through** — only if conviction extreme and -15% gap is stomachable
2. **Trim 30–50% the day before** — most common, locks gains, keeps upside
3. **Exit fully before print** — when R/R asymmetric to downside

Decide BEFORE seeing the price reaction. Decisions made in the moment of a -10% gap are almost always wrong.
