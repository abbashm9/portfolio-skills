---
name: halal-stock-picker
description: Generate a monthly Shariah-compliant stock pick list using a multi-factor screening framework (valuation, growth, financial strength, momentum, catalyst) with full AAOIFI halal verification, position sizing for any budget, and concrete exit strategies (stop-losses, take-profit ladders, cancel rules). Use whenever the user asks for halal stock picks, Shariah-compliant investment ideas, monthly stock recommendations, a halal portfolio, how to invest a specific amount in halal stocks, halal stock screening, AAOIFI-compliant stocks, or anything resembling "where should I invest my money this month" with an Islamic/halal constraint. Trigger even if the user just says "run my stock picker" or "do the halal screen" or names this skill by phrase like "halal stock picker."
---

# Halal Stock Picker

A monthly Shariah-compliant stock-picking workflow modeled on multi-factor quant screening, with full AAOIFI halal verification and explicit exit strategies.

## When to use this skill

Trigger this skill whenever the user wants halal/Shariah-compliant investment ideas, monthly stock picks, portfolio allocation across a budget, or asks "what should I buy this month." Also trigger if they say things like "run the picker," "do my monthly picks," "halal screen," or name the skill directly.

## Core principles

1. **AAOIFI halal compliance is non-negotiable.** Every pick must pass AAOIFI screens. If compliance can't be verified, the stock is excluded.
2. **Always use live data.** Never rely on training data for prices, multiples, guidance, or earnings dates. Search the web on every run.
3. **Provide complete trade plans.** Entry, stop-loss, take-profit ladder, time-based exit, catalyst, and cancel-order rules.
4. **Show your work.** Every claim gets a number and a source citation.
5. **Honest about risk.** This is research output, not financial advice. Past performance ≠ future results.

## Workflow

### Step 1: Capture parameters

Always ask the user (use `ask_user_input_v0` if available, otherwise inline questions):

1. **Universe** — Halal-only is the default if this skill is being used. Ask if they want a specific tilt: US large-cap halal, halal small-cap, global halal (TSM, ASML, Novo Nordisk, etc.), or sector-specific halal (semis, healthcare, software).
2. **Risk tolerance** — Conservative (quality/value, halal dividend stocks), Balanced, or Aggressive (growth/momentum, AI/GLP-1 leaders).
3. **Budget** — Exact dollar amount they want to allocate. Determines position sizing math.
4. **Broker** — Important: does it support fractional shares? If not, stocks priced above the budget get excluded.
5. **Sectors to exclude** — Beyond the auto-excluded haram sectors. Some users skip energy, biotech, or Chinese ADRs.

### Step 2: Halal screening (AAOIFI standards)

All picks must pass these AAOIFI thresholds (see `references/aaoifi-criteria.md` for full detail):

- **Business activity:** Core business not in alcohol, gambling, conventional banking/insurance, pork, adult content, tobacco, weapons, or interest-based finance
- **Interest-bearing debt:** < 30% of market cap
- **Interest-bearing securities (cash + deposits):** < 30% of market cap
- **Non-permissible income:** < 5% of total revenue

Verify on Zoya, Musaffa, Islamicly, or halal.sh before including any stock. Compliance shifts quarterly — always check the most recent screen.

### Step 3: Five-pillar fundamental screen

A stock needs strength in at least 3 of these 5 pillars. Use the data sources specified per pillar — IBKR for market data, web_search for fundamentals.

**Before running the pillars:** resolve each candidate's contract_id via IBKR `search_contracts` (query = ticker). Then fetch IBKR market data for all candidates in parallel:
```
get_price_snapshot  →  fields: ["last", "change", "prior_close", "misc_statistics",
                                 "avg_90d_usd_volume", "implied_vol_underlying",
                                 "cumulative_perf_1w", "cumulative_perf_1m",
                                 "cumulative_perf_ytd", "cumulative_perf_1y",
                                 "year_to_date_change", "historical_vol"]
get_company_themes  →  max_themes: 3, max_companies: 5
```

1. **Valuation gap** — Use IBKR `misc_statistics` for 52-week high/low and where the current price sits in that range. Use `web_search` for forward P/E, EV/EBITDA, analyst fair value targets (IBKR does not provide fundamental multiples).
2. **Growth trajectory** — `web_search` only: revenue YoY/QoQ, EPS growth and revisions, forward guidance, segment breakdown. IBKR does not provide financials.
3. **Financial strength** — `web_search` only: gross margin, operating margin, FCF, debt/EBITDA, interest coverage.
4. **Momentum & technicals** — Use IBKR directly: `cumulative_perf_1w`, `cumulative_perf_1m`, `cumulative_perf_ytd`, `cumulative_perf_1y` for price returns; `historical_vol` for volatility; `avg_90d_usd_volume` for volume profile. Flag RSI >70 via `web_search` (IBKR doesn't provide RSI). Relative strength vs S&P 500 = `year_to_date_change` vs SPY YTD.
5. **Catalyst** — `web_search` only: earnings dates, FDA dates, M&A, analyst upgrades, insider buying. Supplement with `get_company_themes` peers to spot sector tailwinds.

### Step 4: Exclusion filters (auto-reject)

- High debt with deteriorating coverage
- Thin volume (<$10M avg daily)
- Sluggish 6mo trend with no catalyst
- Valuation >50% above analyst targets (no upside left)
- Pending major litigation or accounting concerns
- **Parabolic chart with RSI >80** — these are mean-reversion traps, not entries

### Step 5: Output the pick list

See `references/output-format.md` for the full template. Group by conviction tier (High / Medium / Watchlist). For each pick include:

- Ticker, company, sector, current price, market cap
- One-line thesis
- All 5 pillars with numbers and citations
- Halal status confirmation (AAOIFI ratios if available)
- Key risks
- Conviction level

### Step 6: Position sizing for the user's budget

Once picks are selected, allocate based on the budget. Rules:

- **Concentrate when conviction is high.** Don't over-diversify on small accounts — 4–6 names is enough for $500–$2000.
- **Account for share price.** A $1500/share stock takes too much of a $722 budget without fractional shares.
- **Weight by conviction, not equally.** High-conviction picks get 25–40%; medium get 10–20%.
- **Reserve cash if a major catalyst is days away** (e.g., 10–15% cash before an NVDA earnings print).

### Step 7: Exit strategy for every position

Every position needs:

**Stop-loss** — Hard exit if hit. Sized to the stock's normal volatility (high-beta names like MU get -10%, lower-beta like LLY get -8%).

**Take-profit ladder** — Scale out at multiple levels. Typical structure:
- TP1: sell 30–50% at +12–18%
- TP2: sell another 30–40% at +25–35%
- TP3: hold remainder for +40%+ or until thesis breaks

**Time-based exit** — If the stock is flat with no catalyst by X date, trim.

**Catalyst exit** — Earnings date or sector-specific risk events.

**Universal rules:**
- Halal compliance breach → sell at market open next day
- Single position >45% of portfolio → trim back
- Portfolio down >8% from start → stop trading, move to cash, re-evaluate
- Never average down on stop-out

See `references/exit-rules.md` for full exit templates and cancel-order rules.

### Step 8: Verify prices before finalizing

**Critical step:** Before delivering the final allocation, re-fetch current prices for every recommended stock via IBKR `get_price_snapshot` (fields: `last`, `change`, `misc_statistics`). Do NOT use web search for this — IBKR is the broker and gives exact real-time prices. Prices move daily. If a stock has moved >5% since the screening, recalibrate the entry, stop, and take-profit levels. If a stock has moved into "parabolic with RSI >80" territory (check via `web_search` since IBKR doesn't provide RSI), downgrade or remove it from the list.

### Step 9: Present clearly

- Use tables for allocation, exits, and scenarios
- Show share quantities at current prices if budget is small
- Show best/realistic/worst case portfolio outcomes
- End with: "Re-verify halal status on Zoya/Musaffa before buying. This is research, not financial advice."

## Standard caveats to always include

- "Halal compliance can change quarterly — re-screen on Zoya, Musaffa, or Islamicly before each rebalance."
- "Past performance does not guarantee future results."
- "This is research output, not financial advice. Do your own due diligence."
- "Position sizing assumes fractional shares are available on your broker."

## Format guidelines

- Lead with a short context note (market backdrop, key themes for the month, major catalysts)
- Use tables for allocations and exits — these are the user's primary reference
- Tier picks by conviction (High / Medium / Watchlist), not by sector
- Cite every numeric claim with `` tags from web search results
- End every screen with a clear "next steps" — what the user does now

## Reference files

- `references/aaoifi-criteria.md` — Full AAOIFI halal screening methodology and thresholds
- `references/output-format.md` — Template for the final pick list
- `references/exit-rules.md` — Detailed exit strategy templates and cancel-order rules
- `references/halal-universe.md` — Pre-vetted list of frequently halal-compliant US/global stocks to start from

## A note on what NOT to do

- Don't recommend stocks you haven't verified for halal compliance
- Don't use training-data prices — always search live
- Don't chase parabolic charts; missing a trade is fine, blowing up an account isn't
- Don't promise specific returns
- Don't recommend a position without an exit plan
- Don't simulate confidence; if data conflicts, say so and let the user decide
