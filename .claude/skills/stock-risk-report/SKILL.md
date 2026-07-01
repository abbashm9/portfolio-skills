---
name: stock-risk-report
description: Generate a structured investment risk score report for any publicly traded stock. Produces a full-page visual report including: overall risk score out of 100 with label (LOW / MODERATE / HIGH / EXTREME), executive summary, key stats snapshot, 12-month price chart with 52w high/low marked, valuation metrics with qualitative labels, financial health metrics, growth metrics, sub-scores for valuation/financial health/growth, quarterly financial trend table with trend arrows, recent catalyst data vs estimates, catalysts & risks (4–5 bullets each), and a bottom-line verdict. Use whenever the user asks to "analyse [TICKER]", "risk score for [STOCK]", "investment report on [COMPANY]", "generate a stock report", or similar. Also trigger if the user types a ticker in brackets like [NVDA] or [AAPL] with intent to analyse. Always render the full report as an interactive HTML widget using show_widget.
---

# Stock Investment Risk Score Report

A comprehensive, visually-rich investment risk report for any publicly traded stock — rendered as an interactive HTML widget with live-searched data.

## When to use this skill

Trigger whenever the user wants a structured stock analysis, risk score, or investment report. Phrases that trigger this skill:
- "Analyse [TICKER]" / "analyze [TICKER]"
- "Generate a risk report for [STOCK]"
- "Investment report on [COMPANY]"
- "Risk score for [TICKER]"
- "[TICKER] in brackets alone, with an implied request to analyse"
- "Run the stock risk report on X"

## Core principles

1. **Always use live data.** Never rely on training-data prices, multiples, or earnings dates. Use IBKR for market data and web search for fundamentals.
2. **Show your work.** Cite every key metric with a source (IBKR or web search result).
3. **Be honest about risk.** This is research output, not financial advice. State this clearly in the footer.
4. **Render as a widget.** The report must be delivered as a full `show_widget` HTML output — not as markdown prose.
5. **Cover all sections.** Do not skip sections. If a specific data point is unavailable, estimate from the closest available figure and note it.

**Data source split:**
- Current price, 52-week range, daily change, volume, YTD return, 12-month price history, sector/themes → IBKR
- Revenue, EPS, margins, P/E, EV/EBITDA, earnings dates, guidance, quarterly financials → web search

---

## Workflow

### Step 1: Gather all data

Run IBKR calls and web searches simultaneously before writing any HTML.

**IBKR (resolve contract_id via `search_contracts` first, then run in parallel):**

- A. `get_price_snapshot` → fields: `["last", "change", "prior_close", "misc_statistics", "avg_90d_usd_volume", "year_to_date_change", "cumulative_perf_1y", "historical_vol", "implied_vol_underlying", "bid_ask"]`
  - Provides: current price, 1-day change ($/%),  52-week high/low, average daily volume, YTD return, 1-year return, historical and implied volatility
- B. `get_price_history` → period: ONE_YEAR, step: ONE_MONTH, security_type: STK, outside_rth: false
  - Provides: 12 monthly OHLCV bars for the price chart — real broker data, no estimation
- C. `get_company_themes` → max_themes: 3, max_companies: 5
  - Provides: sector classification, investment themes, closest peer companies
- D. `get_company_connections` → link_types: ["company_product", "company_competitor", "company_country"], include: ["link_info"]
  - Provides: business description, products, geographic exposure, competitors

**Web search (run in parallel with IBKR calls):**

**Search 2 — Financials (TTM & annual):**
- TTM Revenue with YoY % change
- TTM EPS (GAAP) with YoY % change
- Gross margin, operating margin, net profit margin
- Free cash flow (TTM)
- Next earnings date

**Search 3 — Valuation & health metrics:**
- Trailing P/E, Forward P/E, EV/EBITDA, Price/Book, Price/Sales, PEG Ratio
- Debt/Equity, Current Ratio, ROE, ROA
- Cash position vs long-term debt
- Market cap and shares outstanding (not available from IBKR snapshot)

**Search 4 — Quarterly trend & recent news:**
- Last 4 quarters: Revenue, Gross Margin, EPS (GAAP), FCF (or estimate from operating CF)
- Most recent earnings beat/miss vs estimates
- Key recent catalysts (product launches, guidance, partnerships, regulatory events)
- Key risks (export controls, competition, regulatory, macro)

Supplement with additional searches if data is missing or ambiguous.

---

### Step 2: Score the stock

Calculate three sub-scores (each out of 100, where 100 = highest risk):

#### Valuation Risk Score (out of 100)
Score based on multiples vs sector average and historical norms:
- Forward P/E > 40×: +25pts | 25–40×: +15pts | 15–25×: +8pts | <15×: +3pts
- P/S > 20×: +20pts | 10–20×: +12pts | 3–10×: +5pts | <3×: +2pts
- P/B > 20×: +15pts | 10–20×: +10pts | 3–10×: +5pts | <3×: +2pts
- PEG < 1: -10pts | 1–2: 0pts | >2: +10pts
- Premium vs analyst fair value > 30%: +10pts | 10–30%: +5pts | at/below fair value: -5pts
- Cap at 100, floor at 5.

#### Financial Health Risk Score (out of 100)
Lower score = healthier (lower risk):
- Debt/Equity > 2×: +30pts | 0.5–2×: +15pts | <0.5×: +5pts
- Current Ratio < 1: +20pts | 1–1.5×: +10pts | >2×: +2pts
- ROE < 10%: +15pts | 10–20%: +8pts | >20%: +2pts
- Net Profit Margin < 5%: +15pts | 5–15%: +8pts | >25%: -5pts
- Net cash position (cash > debt): -10pts
- Cap at 100, floor at 5.

#### Growth Risk Score (out of 100)
Captures deceleration risk and margin volatility:
- Revenue growth > 50% YoY with no deceleration: +10pts (growth is real, not just priced in)
- Revenue growth slowing materially QoQ: +20pts
- Revenue growth < 10%: +25pts
- Gross margin declining > 5pp YoY: +20pts
- Concentrated revenue (1–2 segments >80%): +15pts
- Single-country regulatory/export risk: +15pts
- Strong FCF margin (>30%): -10pts
- Cap at 100, floor at 5.

#### Overall Risk Score
Weighted average:
- Valuation Risk: 40% weight
- Growth Risk: 35% weight
- Financial Health Risk: 25% weight

Round to nearest integer. Map to label:
- 0–30: LOW RISK
- 31–50: MODERATE RISK
- 51–70: MODERATE-HIGH RISK
- 71–85: HIGH RISK
- 86–100: EXTREME RISK

---

### Step 3: Build the report HTML widget

Use `read_me` with modules `["mockup", "data_viz", "chart"]` before calling `show_widget`.

The widget must contain all of the following sections in order:

#### 1. Header
- Stock ticker (large, bold), exchange badge, company name, sector · sub-industry (from IBKR `get_company_themes`)
- Current share price (large, from IBKR `last`), 1-day change in $ and % (from IBKR `change`, green if positive, red if negative)
- "As of [timestamp from IBKR response]" line with intraday high/low (from IBKR `bid_ask`)
- Data source badge: "Market data: IBKR | Financials: web search"

#### 2. Overall Risk Score Box
- Giant risk number (e.g. "58") in risk colour
- "/100" label and risk label (e.g. "⚠ MODERATE-HIGH RISK")
- Horizontal gradient risk bar (green → amber → red) with a pointer at the score position
- Scale labels: 0-Low, 50-Moderate, 75-High, 100-Extreme
- 2–3 sentence executive summary explaining the key risk drivers

#### 3. Key Stats (snapshot grid)
6 cards in a responsive grid:
- Market Cap (from web search, with size label: Nano/Micro/Small/Mid/Large/Mega-cap)
- TTM Revenue (from web search, with +/- YoY %)
- TTM EPS GAAP (from web search, with +/- YoY %)
- 52-Week Range (from IBKR `misc_statistics` — exact low and high, note if at/near high or low)
- Next Earnings Date (from web search, with days until)
- Avg Daily Volume (from IBKR `avg_90d_usd_volume` — 90-day average, more reliable than a single-day figure)

#### 4. 12-Month Share Price Chart (Chart.js line chart)
- Use IBKR `get_price_history` data (Step 1 batch item B) — real monthly OHLCV bars, no interpolation or estimation
- Plot the `close` value from each bar; use the `t` timestamp field for x-axis labels
- Mark 52w low (green dot) and 52w high (red dot) using `misc_statistics` from the price snapshot
- Mark current price (amber dot) using `last` from the price snapshot
- Custom legend above chart (colour squares + labels)
- No Chart.js default legend
- Data source tag under chart: "Source: IBKR live feed"

#### 5. Valuation Metrics
6 metric rows in a 2-column grid, each with:
- Metric name | Value | Qualitative badge
  - Trailing P/E → Cheap / Fair / Elevated / Very High / Extreme
  - Forward P/E → Cheap / Reasonable / Elevated / Very High
  - EV/EBITDA → Low / Fair / Elevated / Very High
  - Price/Book → Low / Fair / Elevated / Very High
  - Price/Sales → Low / Fair / Elevated / Very High
  - PEG Ratio → Growth-Adj. Cheap / Fair / Overvalued

Badge colours: Low/Cheap/Reasonable = green | Fair/Moderate = blue | Elevated = amber | Very High/Extreme = red

#### 6. Financial Health Metrics
6 metric rows in same 2-column grid:
- Debt/Equity → Very Low / Low / Moderate / High / Very High
- Current Ratio → Weak / Adequate / Strong / Very Strong
- Return on Equity → Poor / Average / Good / Exceptional
- Return on Assets → Poor / Average / Good / World-Class
- Net Profit Margin → Loss / Thin / Moderate / Strong / Exceptional
- Cash vs Long-Term Debt → Net Cash / Balanced / Leveraged / Highly Leveraged

#### 7. Growth Metrics
6 metric rows in same layout:
- Revenue Growth (FY) → Declining / Slow / Moderate / Strong / Hyper-Growth
- Key Segment Revenue (largest segment with YoY %)
- Secondary Segment Revenue (second largest, or "N/A" if single segment)
- Gross Margin → Thin / Average / Strong / Best-in-Class
- EBITDA Margin → Thin / Average / Strong / Exceptional
- FCF (TTM) → Negative / Weak / Moderate / Strong (include FCF margin %)

#### 8. Score Breakdown (3 cards side by side)
For each sub-score card:
- Label (Valuation Risk / Financial Health Risk / Growth Risk)
- Score number / 100 (coloured: red >65, amber 35–65, green <35)
- 1–2 line justification

#### 9. Quarterly Financial Trend Table (last 4 quarters)
Table columns: Metric | Q1 | Q2 | Q3 | Q4 (most recent) | Trend Arrow
Rows:
- Revenue
- Gross Margin (GAAP)
- Operating Margin (estimate if needed)
- EBITDA Margin (estimate)
- EPS (GAAP)
- Free Cash Flow (estimate from data)

Trend arrow: ↑ Strong (green) | ↑ Improving (green) | → Flat (gray) | ↓ Declining (red)
Note any one-time charges that distort a quarter.

#### 10. Recent Catalyst / Data Update Box
Amber-tinted box showing the most recent material data point:
- Latest earnings beat/miss: actual vs estimate for Revenue, EPS, Gross Margin
- Most recent guidance for next quarter
- Confirmed next earnings date with days until

#### 11. Catalysts (4–5 bullet items)
Each item:
- Tabler icon (ti-rocket, ti-cpu, ti-world, ti-chart-line, ti-building-factory, etc.)
- Bold title
- 2–3 sentence explanation with specifics

#### 12. Key Risks (4–5 bullet items)
Same structure as catalysts, using warning icons (ti-world-off, ti-alert-triangle, ti-chart-bar-off, etc.)

#### 13. Bottom Line Box
Red border box:
- Risk label + 1-line verdict in risk colour
- 3–4 sentence detailed conclusion covering: fundamentals, valuation, key strengths, who this stock suits (long-horizon growth / income / speculative / not suitable for risk-averse investors)

#### 14. Footer
- Generation date and time
- Data sources: "Market data (price, 52w range, volume, chart): IBKR live feed | Fundamental data (revenue, margins, P/E, earnings): [list web search sources]"
- Disclaimer: "This report is for informational purposes only and does not constitute financial, investment, or legal advice. Past performance is not indicative of future results. All figures are based on publicly available data as of the report date and may contain minor approximations. Consult a licensed financial advisor before making investment decisions."

---

### Step 4: Styling rules

Follow the core design system from the visualizer `read_me`. Additional rules specific to this report:

- **Risk colours by score:** 0–30 = `#3B6D11` (green) | 31–50 = `#BA7517` (amber) | 51–70 = `#E24B4A` (red-orange) | 71–100 = `#A32D2D` (dark red)
- **Positive changes:** `#3B6D11` | **Negative changes:** `#A32D2D`
- **Badge palette:**
  - `badge-low` (good): `background:#EAF3DE; color:#3B6D11`
  - `badge-ok` (neutral/ok): `background:#E6F1FB; color:#185FA5`
  - `badge-med` (caution): `background:#FAEEDA; color:#854F0B`
  - `badge-high` (warning): `background:#FAECE7; color:#993C1D`
- All sections separated by a `section-title` label (small caps, muted, letter-spaced)
- Metric rows use `background:var(--color-background-secondary)` with `border-radius:var(--border-radius-md)`
- Chart box and catalyst box use `background:var(--color-background-primary)` with `border:0.5px solid var(--color-border-tertiary)` and `border-radius:var(--border-radius-lg)`
- Bottom line box: `border:2px solid [risk-colour]` (only exception to 0.5px border rule)
- Recent catalyst box: amber tint — `background:#FAEEDA; border:0.5px solid #FAC775`
- Price change positive: green | negative: red | neutral: secondary text
- All monetary values: `$` prefix, abbreviate with `B` (billions) or `T` (trillions) for large numbers
- Percentage changes: always include `+` sign for positive values

---

### Step 5: Chart.js implementation

```javascript
// 12-month price chart pattern
const labels = ['May 25','Jun 25','Jul 25','Aug 25','Sep 25','Oct 25','Nov 25','Dec 25','Jan 26','Feb 26','Mar 26','Apr 26','May 26'];
const prices = [/* 12-13 approximate monthly closes from search */];
// Compute minIdx and maxIdx from prices array
// Color dots: 52w-low=green, 52w-high=red, current=amber, others=transparent
// Line: borderColor '#185FA5', fill with low-opacity blue
// Scales: y.min = Math.floor(minPrice * 0.9), y.max = Math.ceil(maxPrice * 1.05)
// autoSkip: false, maxRotation: 35 for x-axis labels
// Custom HTML legend above the canvas (not Chart.js default)
```

---

## What NOT to do

- Don't skip sections — every section in the spec must appear in the widget
- Don't use markdown prose as the report — the full report lives inside `show_widget`
- Don't use training-data prices — always search live before rendering
- Don't put text explanations outside the widget (brief citations in the surrounding chat are fine, but the report is self-contained)
- Don't promise specific returns or recommend buying/selling
- Don't use colour alone to distinguish data — pair with labels/badges
- Don't use `position:fixed` or `display:none` inside the widget
- Don't omit the disclaimer footer

## Standard disclaimer (always include in footer)

> This report is for informational purposes only and does not constitute financial, investment, or legal advice. Past performance is not indicative of future results. All figures are based on publicly available data as of the report date and may contain minor approximations. Consult a licensed financial advisor before making investment decisions.
