---
name: daily-portfolio-check
description: Run a daily post-market portfolio review for Abbas's halal stock portfolio — fetches live closing prices, calculates P&L per position and total, evaluates each position against its exit strategy (stop-loss, take-profit ladder, time-based exit, catalyst), flags any positions needing action, proposes rebalancing or rotation moves, and produces a designed HTML email report with a daily education module on US equity concepts. Since Abbas isn't withdrawing money, suggestions can be aggressive (e.g., trim 30% of a winner to buy 1 share of a new high-conviction name). Use whenever Abbas says "daily check", "portfolio check", "how am I doing", "market closed", "check my stocks", "run the daily", or any variant of "review my portfolio." Trigger even if he just says "daily" or pastes a screenshot of his brokerage app at end of day.
---

# Daily Portfolio Check (v2 — HTML Email + Education)

A post-NYSE-close daily review skill for Abbas's halal stock portfolio. Outputs a designed HTML email report and emails it via Gmail connector.

## Critical user context

- **User:** Abbas Al Madani, Kuwait
- **Trading experience:** 8 years in forex and indices — strong on technicals, mechanics, risk management
- **Stock-market gap:** New to single-name US equities — needs to learn valuation multiples, fundamentals language, sector-specific cycles
- **Tone preference:** Pragmatic, no condescension, no "what is a stop-loss" basics. Treat him as an experienced trader who needs the equity-specific vocabulary
- **Withdrawal intent:** NONE — rotation suggestions can be aggressive
- **Halal compliance:** AAOIFI standards (verify quarterly, but don't include daily halal education — he doesn't want this)
- **Disclosure:** Research, not financial advice

## Current portfolio (baseline — update when positions change)

| Ticker | Shares | Entry | Cost Basis | Stop-Loss | TP1 | TP2 | TP3 | Catalyst |
|--------|--------|-------|------------|-----------|-----|-----|-----|----------|
| NVDA | 1.3799 | $217.40 | $300.06 | $204 (-6.4%) | $240 sell 30% | $260 sell 40% | $285+ hold 30% | Earnings May 20, 2026 |
| LLY | 0.1407 | $994.87 | $139.98 | $915 (-8%) | $1,114 sell 30% | $1,243 sell 40% | $1,393 hold 30% | Foundayo Q2 launch |
| AVGO | 0.315 | $412.04 | $129.79 | $379 (-8%) | $474 sell 50% | $536 hold 50% | — | Earnings early June |
| TSM | 0.224 | $388.35 | $86.99 | $357 (-8%) | $435 sell 50% | $485 hold 50% | — | Taiwan geopolitical risk |
| AMD | 0.117 | $428.84 | $50.17 | $386 (-10%) | $493 sell 50% | $558 hold 50% | — | Q2 earnings ~Aug 4, 2026 |

**Total cost basis: $706.99**

## Workflow — every daily check

### Step 1: Fetch live closing prices

Use `web_search` for each ticker. **Required:** verified close prices for ALL 5 positions. If a price can't be confirmed from a reliable source (Yahoo Finance, Google Finance, Bloomberg, CNBC, Reuters), flag it explicitly — do NOT estimate. Estimated data is worse than missing data.

### Step 2: Build the data tables

Calculate per-position:
- Current value (shares × current price)
- P&L $ and % vs cost basis
- Day's change $ and % (vs prior close)

Calculate portfolio totals:
- Total cost basis
- Total current value
- Total P&L $ and %
- Day's change $ and %

### Step 3: Exit-strategy check per position (in order)

1. **Halal compliance** — quarterly check, not daily, but flag if breaking news suggests a change
2. **Stop-loss** — Below stop? 🚨 ALERT. Within 2% of stop? ⚠️ WATCH.
3. **TP1/TP2/TP3** — Hit? 🔔 ACTION with trim recommendation
4. **Catalyst proximity** — within 5 trading days? Flag prominently
5. **Time-based** — flat ±3% for 30+ days, no catalyst? Consider trim
6. **Parabolic warning** — up >40% in 30 days, RSI >80? Mean-reversion risk

Status emoji per position:
- ✅ HOLD — within range, thesis intact
- ⚠️ WATCH — approaching a level, no action yet
- 🔔 ACTION — hit a level, recommend trim/exit
- 🚨 ALERT — stop hit or thesis broken, exit now

### Step 4: Rotation suggestions (aggressive)

Since Abbas isn't withdrawing money, propose moves when:
- A position hits TP1/TP2 → suggest where to redeploy
- A new high-conviction halal name has a near-term catalyst → suggest trimming a winner to fund a starter position
- A position is dead money (flat 30+ days) → suggest a rotation
- Pre-binary-event (earnings within 5 days) → suggest a risk-management trim

Format rotation suggestions with: exact shares to sell, exact $ freed, exact shares of replacement to buy, 1-line rationale, 1-line risk, end with "Your call."

### Step 5: Select today's education concept

See `references/education-curriculum.md` for the full 30-day curriculum. Pick the concept that's most relevant to TODAY's portfolio activity, with a slight bias toward terms that appeared in today's report. Repeat concepts on subsequent days for deeper coverage when warranted — no rush.

Track which concepts have already been taught (in conversation context) to avoid teaching the same one twice in a row unless intentionally going deeper.

**Education paragraph format:**
- ONE main concept, one tight paragraph (~80–120 words)
- Plus a 1-line "also today" mention of a related term
- Voice: mixed register — trader-to-trader for the main concept, analytical when stakes need precision, slang/punchy when the term has a clean colloquial frame
- Always anchor to Abbas's actual positions and numbers — never use generic examples
- Place at the very bottom of the email

### Step 6: Generate the HTML email

Build a responsive HTML email with the structure in `references/email-template.md`. Key requirements:
- Inline CSS only (email clients strip `<style>` tags)
- Use tables for layout (still the most reliable email layout method)
- Color-coded status badges
- Hero banner with total P&L (green if positive, red if negative)
- Position cards with sparkline-style mini SVG charts (last 30 days when available)
- Education section in a colored box at the bottom
- Footer with disclaimer in 10px grey

### Step 7: Send via Gmail connector

Send the HTML email to Abbas's configured email address (he'll set this in the routine).

**Subject line format:**
```
📊 Daily Portfolio: [+X.X% / -X.X%] | [headline event of the day]
```

Examples:
- `📊 Daily Portfolio: +2.75% | NVDA earnings in 5 days`
- `📊 Daily Portfolio: -1.2% | AMD post-earnings fade continues`
- `📊 Daily Portfolio: +0.4% | Quiet session, no actions`

Use Asia/Kuwait timezone for date references.

### Step 8: Handle market-closed days

If NYSE was closed today (weekend, US holiday), send a SHORT email:
- Subject: `📊 Daily Portfolio: Markets closed today`
- Body: 1 sentence noting markets were closed, plus the education concept of the day (still valuable on closed days)

## Output style rules

- **No fluff** — Abbas reads this fast, every sentence earns its place
- **Numbers always** — when you say something moved, give the number
- **Honest about data gaps** — flag missing/unreliable data, don't paper over it
- **Pre-event decisions** — surface binary decisions early (e.g., NVDA earnings call BY Friday, not the morning of)
- **Education at bottom** — never lead with it

## Special triggers

- **Day before held name's earnings:** highlight the decision (hold/trim/exit before print) prominently in the email
- **Halal compliance breach detected:** override everything else, recommend exit at next open
- **Portfolio down >8% from cost basis:** stop suggesting new entries, defensive review only
- **Portfolio up >20% from cost basis:** suggest taking some profits
- **NYSE holidays:** short closed-market email with education only

## Position updates

When Abbas reports new buys/sells in chat, update the position table in this SKILL.md or note in conversation. Always confirm:
- Exact shares bought/sold
- Exact fill price
- Updated cost basis
- New stop/TP levels if needed

## Reference files

- `references/email-template.md` — HTML email structure with inline CSS
- `references/exit-rules.md` — Detailed exit logic (stops, TPs, catalysts, time-based)
- `references/rotation-playbook.md` — When and how to suggest rotations
- `references/education-curriculum.md` — 30-day learning track with concept-by-concept content guides

## What this skill does NOT do

- Execute trades — Abbas does this in his broker
- Give financial advice — research only
- Daily halal compliance lectures — quarterly check only, no daily education on this
- Generic education — every concept anchors to Abbas's actual portfolio
