# Education Curriculum — 30-Day US Equity Learning Track

Designed for Abbas: 8 years of forex/indices trading, strong on technicals and risk management, learning the single-name US equity world. Skip basics, focus on what's *different* from forex.

## Selection rules

- Pick ONE concept per day (one tight paragraph, ~80–120 words)
- Plus ONE 1-line "also today" mention of a related term
- Always anchor to Abbas's actual portfolio positions and numbers
- Repeat concepts on subsequent days if they deserve more depth — no rush
- Prefer concepts that appeared in TODAY'S report (e.g., if today's report mentioned forward P/E, teach forward P/E)
- Track which concepts have been taught and rotate appropriately
- Mixed voice register: trader-to-trader, analytical, occasional slang — match the concept

## Week 1 — Valuation Multiples

### Day 1: Forward P/E vs Trailing P/E

Trailing P/E uses the last 12 months of earnings — useful for stable businesses, useless for a company growing 65% a year. By the time NVDA reports last quarter, the business is already much bigger. Forward P/E uses analyst consensus for the *next* 12 months of earnings, which is what the market actually prices.

The trick: a stock can look "expensive" at 60x trailing and "cheap" at 35x forward simultaneously, because the E in the denominator nearly doubled. NVDA's trailing P/E is ~62x; forward is ~40x. Same company, same price, different math. Pros quote forward — Yahoo Finance defaults to trailing, which is misleading for growers. Your LLY is similar: trailing P/E ~58x, forward ~32x, because Mounjaro/Zepbound revenue is still ramping.

**Anchor to portfolio:** Pull current forward P/E for each holding, note the trailing P/E if dramatically different.

**Also today:** *Multiple expansion* — when investors are willing to pay a higher P/E for the same earnings (sentiment-driven).

### Day 2: EV/EBITDA

Forward P/E ignores debt and cash. EV/EBITDA fixes both. EV (enterprise value) = market cap + debt − cash. EBITDA = earnings before interest, tax, depreciation, amortization. The ratio tells you what an acquirer would actually pay, normalized for capital structure.

A company with $10B market cap and $5B in cash is cheaper than one with $10B market cap and $5B in debt — P/E misses this entirely. EV/EBITDA catches it. Semis trade around 15–25x EV/EBITDA in normal times; NVDA is 32x, premium for growth. Software at 20–40x is normal. Banks shouldn't be valued on EV/EBITDA at all (they're capital structures).

**Also today:** *Net debt* — when subtracting cash from debt gives a negative number, the company has more cash than debt (like Apple or Alphabet).

### Day 3: Price/Sales (P/S)

When a company isn't profitable yet (or earnings are temporarily depressed), P/E breaks. P/S sidesteps this — just market cap divided by trailing revenue. Useful for high-growth SaaS, biotech pre-product, hyper-growth consumer (early Shopify, early Tesla).

Rule of thumb: software trading >15x P/S is priced for perfection. >25x means the market expects 40%+ growth indefinitely. Sub-5x P/S for software usually signals trouble. Doesn't work for low-margin businesses (a grocery chain at 0.5x P/S isn't "cheap" — that's just how that industry trades). LLY trades around 18x P/S, which is rich for pharma but consistent with their GLP-1 franchise growth.

**Also today:** *Rule of 40* — for SaaS, growth rate + profit margin should exceed 40%.

### Day 4: Price/Book (P/B) — and why it's mostly useless now

P/B = market cap / book value (assets minus liabilities on the balance sheet). It worked when companies were factories and inventory — book value reflected what you'd recover liquidating. It's broken for modern businesses. NVDA's "book value" is mostly cash plus some servers. Its real value is the CUDA software ecosystem and engineering talent — neither shows up on the balance sheet.

P/B still works for banks, insurance, REITs, and some industrials, because those businesses actually are their balance sheets. For tech, healthcare, software, brands — ignore it. When you see Tesla "trading at 20x book" being called expensive, that's the wrong frame entirely. NVDA trades at 50x book; nobody cares because book isn't where the value lives.

**Also today:** *Tangible book value* — book value minus goodwill/intangibles; even stricter, even less useful for modern co's.

### Day 5: PEG ratio

PEG = forward P/E ÷ earnings growth rate. Ties valuation to growth in one number. PEG of 1.0 = fair. Below 1.0 = potentially cheap. Above 1.5 = expensive unless growth accelerates. Peter Lynch made this famous in the 80s.

The trap: PEG is sensitive to whose growth estimate you use. Sellside analysts are systematically optimistic. Better to use management's own guidance (more conservative) or your own estimate. NVDA at 40x forward growing 50% = PEG of 0.8 (cheap by classical standard). LLY at 32x forward growing 30% = PEG 1.1 (fair). AVGO at 38x forward growing 25% = PEG 1.5 (full). PEG helps you compare growers head-to-head — but only when the growth is actually durable.

**Also today:** *Earnings revisions trend* — analysts raising estimates over time is a stronger signal than any single PEG number.

## Week 2 — Fundamentals & Quality Signals

### Day 6: Gross margin vs operating margin vs net margin

Three different stories. **Gross margin** = (revenue − cost of goods sold) / revenue. Tells you whether the product itself is profitable. NVDA's 75% gross margin says their chips have monopoly pricing power; commodity DRAM (Micron) runs 30–50% depending on cycle. **Operating margin** = gross profit minus operating expenses (R&D, sales, G&A). Tells you about the business model. NVDA operating margin: ~63%. Compare to Tesla auto: ~7%. **Net margin** = after interest, taxes. Mostly noise — affected by tax structure and one-time items.

Watch gross margin trend more than the absolute number. Expanding gross margin = pricing power growing. Contracting = competition arriving or input costs rising. AVGO's gross margin expanded ~3 points over 2 years = the AI chip mix shift toward higher-margin products.

**Also today:** *Mix shift* — when revenue from higher-margin products grows faster than low-margin products, total gross margin rises mechanically.

### Day 7: Free cash flow (FCF) vs net income

Net income is an accounting construct — it includes depreciation (non-cash) and ignores capex (real cash going out). FCF = operating cash flow − capital expenditures. It's the actual money the business generates that's available to return to shareholders or invest in growth.

Why it matters: a company can show rising net income while FCF declines if they're stuffing inventory or building factories. Or vice versa — depreciation can suppress net income while FCF is fine. NVDA generated $96B in FCF FY2026 — that's real cash, available to buy back stock or invest. AVGO's FCF conversion (FCF/net income) is >90% — sign of a high-quality business. Tesla's FCF conversion has historically been weaker because of factory capex. Always look at multi-year FCF trend, not single-quarter swings.

**Also today:** *Owner earnings* — Buffett's variant: net income + depreciation − required capex. Cleaner than FCF for capital-intensive businesses.

### Day 8: Return on invested capital (ROIC)

ROIC = NOPAT (net operating profit after tax) / invested capital (debt + equity). It tells you how efficiently the business converts every dollar of capital into profit. The single best quality metric.

Why: high ROIC = competitive moat. The math forces it. If a business consistently earns 30% on capital while peers earn 10%, capital should flood in until returns equalize. The fact that they don't means something is preventing competition — patents, network effects, switching costs, brand. NVDA's ROIC is ~80% (insane). AVGO ~50%. LLY ~35% (high for pharma). A consistent ROIC above 15% over a full cycle = look closer; below 10% = the business is probably commoditized.

**Also today:** *Cost of capital (WACC)* — ROIC matters only relative to WACC; ROIC > WACC creates value, ROIC < WACC destroys it.

### Day 9: Operating leverage

When revenue grows faster than costs, operating profit grows even faster — that's operating leverage. Tied to fixed cost intensity. Semis have very high operating leverage: a chip fab costs the same to run whether utilization is 70% or 95%. So a small revenue uptick produces a huge profit uptick.

The flip side: in downturns, revenue falls but fixed costs stay — profit collapses. This is why semi stocks like AMD or MU swing so violently between cycles. NVDA's leverage played out perfectly: revenue +65% YoY, but operating profit +110%. ASML similarly: revenue +20% can produce 30%+ EPS growth. When you see a semi company guide for revenue acceleration, the earnings acceleration is usually larger. The trade is positioning ahead of the inflection.

**Also today:** *Incremental margin* — the operating margin on each additional dollar of revenue; high incrementals = operating leverage in action.

### Day 10: Share-based compensation (SBC)

US tech companies pay employees in stock. A lot of it. Like a third of total comp at NVDA. The accounting treatment is generous — SBC reduces "GAAP" earnings but is often added back in "adjusted" / "non-GAAP" / "pro forma" numbers that companies emphasize. This is silent dilution: every year, the share count creeps up unless management buys back stock at scale.

Why it matters for valuation: when you compare two software companies at 30x P/E, the one with 8% annual SBC is much more expensive in reality — your share of future earnings is shrinking. Always compute "diluted share count growth" — if it's >2% annually, factor it in. NVDA buys back more stock than it issues, so net dilution is negative — that's the high-quality version. Younger high-growth companies often have +3–5% annual dilution that destroys 20–25% of returns over 5 years.

**Also today:** *Buyback yield* — the % of float repurchased annually; combine with dividend yield to get total shareholder yield.

## Week 3 — Sector-Specific Concepts (your portfolio's drivers)

### Day 11: Hyperscaler capex

Hyperscalers = the four cloud giants: Microsoft, Amazon (AWS), Alphabet (Google Cloud), Meta. They build the data centers everyone else rents. Their combined capex (capital expenditure) is the single biggest demand driver for NVDA, AVGO, ASML, AMD. When MSFT raises capex guidance, NVDA rips. When META cuts capex, the whole semi complex sells off.

2026 combined hyperscaler capex: ~$725B, up from ~$410B in 2025. That's a 77% YoY surge. Every quarter, listen to these four companies' guidance calls — that's the leading indicator for your semi positions. The order of importance: META and MSFT lead (most aggressive); GOOGL and AMZN follow. Smaller cloud players (Oracle, CoreWeave) are starting to matter too. If you ever see "AI capex digestion" trending on FinTwit, that's the warning sign.

**Also today:** *Capex intensity* — capex as % of revenue; rising = company is investing for future, falling = harvesting.

### Day 12: DRAM/NAND cycle

Memory (Micron, Samsung, SK Hynix) is the most cyclical part of tech. Two products: DRAM (fast, volatile memory) and NAND (slow, persistent storage). Both are commodities — same product, same specs across vendors. Pricing is set by supply/demand globally and swings wildly.

Cycle: demand picks up → prices rise → fabs run 100% utilization → fabs add capacity → 18 months later new capacity comes online → supply floods → prices crash → low margins kill weak players → consolidation → demand recovers → repeat. Each cycle is 3–5 years peak-to-peak. We're currently in an up-cycle driven by AI memory (HBM — high bandwidth memory used in NVDA chips). Micron stock 750% in 12 months reflects this. The signal to exit: spot DRAM prices reversing down >10% week-over-week. When the cycle turns, it turns fast.

**Also today:** *HBM (high bandwidth memory)* — specialized DRAM stacked vertically for AI accelerators; much higher margin than standard DRAM.

### Day 13: Foundry vs fabless

NVDA designs chips but doesn't make them — they're *fabless*. TSMC actually fabricates the silicon — that's a *foundry*. Two completely different business models. Fabless = high margin (NVDA 75%), low capex, agile, valued on intellectual property. Foundry = mid margin (TSMC ~55%), enormous capex ($30B+/year), valued on capacity and process leadership.

Why it matters: TSMC has a near-monopoly on leading-edge chips (3nm, 2nm). Samsung tried to compete and lost. So NVDA, AMD, Apple, AVGO are all customers of TSMC — they share the same supply chain bottleneck. When TSMC raises prices, gross margins shift down the chain. ASML sits one level deeper — they make the EUV machines TSMC uses. So ASML → TSMC → NVDA = one supply chain. Intel is the weird hybrid trying to be both fabless designer and foundry — historically poorly.

**Also today:** *Process node* — the manufacturing generation (e.g., "3nm"); each node ~30% better performance or lower power than the previous.

### Day 14: GLP-1 mechanism & TAM

GLP-1 (glucagon-like peptide 1) is a hormone that regulates blood sugar and appetite. Mounjaro/Zepbound (Eli Lilly) and Ozempic/Wegovy (Novo Nordisk) are synthetic versions that hit GLP-1 receptors. Originally approved for diabetes, the weight-loss side effect turned out to be enormous (15–25% body weight reduction).

TAM (total addressable market) is the catch. ~40% of US adults are obese, ~75% are overweight. Global numbers worse. Wall Street estimates GLP-1 market at $150B by 2030, possibly $200B+. Today's run-rate: ~$50B combined. LLY and NVO have a duopoly with maybe 6–10 years before next-gen competitors arrive. LLY's pipeline (orforglipron — oral, no injection) extends the moat. The investment thesis isn't "drugs sell well" — it's "this is the largest drug class in history, and two companies own it."

**Also today:** *TAM (total addressable market)* — the total dollar market a product could theoretically capture if it had 100% share.

### Day 15: Process node transitions

Every 2 years, foundries (TSMC, Samsung, Intel) launch a new process node — denoted in nanometers (now angstroms). TSMC's path: 7nm → 5nm → 3nm → 2nm → A16 → A14. Each step: smaller transistors, more density, better performance per watt. Drives a hardware upgrade cycle across every customer.

Why it matters: NVDA's next-gen chips need TSMC's next node. AAPL gets first crack at each node, NVDA usually second or third in line. The semi capex cycle is timed to these transitions. ASML's EUV (and now High-NA EUV) machines are what enable the lithography for these smaller nodes — a single High-NA machine costs $380M and there's a multi-year backlog. When you see "Apple Silicon moving to 2nm in 2026," what you're really seeing is the entire supply chain ratcheting up — TSMC capex, ASML orders, NVDA's next chip generation. Track node news; it's your leading indicator.

**Also today:** *Yield* — % of chips that come off the line working; new nodes start with low yields (~50%) and improve over time. Bad yields = expensive chips.

## Week 4 — Trading Mechanics Specific to US Equities

### Day 16: Earnings whisper numbers

Sellside analysts publish consensus estimates (the "official" expectation). But buyside (hedge funds, mutual funds) often have a different number they expect — the "whisper." Whispers are usually higher than consensus because the buyside has better channel checks. The whisper is what actually moves the stock when results print.

How to read it: NVDA's Q1 official consensus might be $0.75 EPS. The whisper on FinTwit and in earnings preview notes might be $0.80. If NVDA prints $0.78 — a beat on consensus, miss on whisper — the stock can DROP despite the beat. The headlines say "beats expectations" but the buyside is selling. Sites like EarningsWhispers track these. Pay attention especially in heavily-followed names (NVDA, AAPL, TSLA) where the whisper-consensus gap is largest.

**Also today:** *Expectations beat* — beating consensus doesn't matter; beating the *expected* magnitude of beat does.

### Day 17: Options-implied move

The options market prices in an expected magnitude of move around binary events (earnings, FDA decisions). To extract it: look at the at-the-money straddle price right before the event. Sum of ATM call + ATM put = the expected move (roughly). Divide by stock price to get the %.

For NVDA going into Q1: if the May 22 expiry straddle costs $14 with stock at $200, the implied move is ±7%. This is what's already priced in. To make money on a long position through earnings, you need NVDA to move MORE than +7% — anything less and the option market got it right and you might not see much upside. Historical implied moves for mega-caps: NVDA ~7–9%, TSLA ~8–10%, AAPL ~3–5%, MSFT ~4–6%. Useful for sizing decisions: if implied move is too big to stomach, trim before the print.

**Also today:** *IV crush* — implied volatility collapses post-earnings, destroying option value even when the stock moves; why long options into earnings is a hard trade.

### Day 18: Short interest and squeeze setups

Short interest = % of shares sold short. Above 20% is high; above 40% is squeeze territory. Different from forex squeezes — in equities, shorts have to borrow shares from holders. When a shorted stock rises sharply, brokers force shorts to buy back (cover) to prevent losses. Their buying drives the stock higher, forcing more covering. Self-feeding loop.

Classic short squeezes: GME 2021 (140% short interest, 800% move), HOOD 2024, parts of TSLA's 2020 run. To find squeeze candidates: high short interest (>25%), low float (under 50M shares), upcoming catalyst, momentum already building. Days-to-cover (short interest ÷ daily volume) above 5 means it would take a week to unwind — that's fuel. Most of your holdings have low short interest (NVDA ~1%, AVGO ~2%), so this isn't a daily concern, but understand the mechanic for opportunistic trades elsewhere.

**Also today:** *Float* — shares actually available for trading (total shares minus locked-up insider holdings).

### Day 19: Sector rotation (XLK, XLV, XLF)

Money flows between sectors over time — sometimes the market rotates from growth → defensive, sometimes from tech → financials, sometimes into cyclicals out of staples. The "sector ETFs" let you measure this: XLK = tech, XLV = healthcare, XLF = financials, XLE = energy, XLY = consumer discretionary, XLP = consumer staples, XLI = industrials.

Watch the relative strength chart of XLK/SPY or XLV/SPY. Trending up = sector outperforming the market. When you see XLK breaking out vs SPY, the AI/semi trade is alive. When XLK rolls over while XLV breaks out, money is rotating to healthcare — that's exactly when LLY would benefit. Sector rotation is the biggest "where to put your money" decision a few times a year. Use these ETFs as your dashboard, not your watchlist of individual stocks.

**Also today:** *Defensive vs cyclical sectors* — defensives (utilities, staples, healthcare) outperform in slowdowns; cyclicals (financials, materials, industrials) outperform in expansions.

### Day 20: Beta vs SPY

Beta measures a stock's volatility relative to the S&P 500. Beta of 1.0 = moves with the market. Beta of 1.5 = 50% more volatile (a 1% market move = 1.5% stock move on average). Beta of 0.5 = half as volatile. Negative beta = inverse correlation (rare; gold miners sometimes).

Your holdings: NVDA beta ~2.3 (highly volatile), AMD ~2.0, AVGO ~1.4, TSM ~1.2, LLY ~0.5 (defensive). This matters for position sizing — a 40% allocation to NVDA isn't the same risk as 40% in LLY because NVDA swings more than 4x as much per move. Useful rule: weight by inverse beta when you want equal risk contribution, not equal dollar weights. Forex pairs have implicit volatilities you grew used to — equities require you to think in beta because broad-market sentiment dominates short-term moves more than in FX.

**Also today:** *Idiosyncratic risk* — the part of a stock's move not explained by beta (i.e., company-specific news); diversification eliminates this.

## Week 5 — Market Microstructure & Edge

### Day 21: Bid-ask spread on stocks vs forex

In major FX pairs you grew used to 0.5–2 pip spreads on EURUSD — virtually frictionless. US equities are similar on mega-caps (NVDA bid-ask: $0.01–$0.02 spread on $200 stock = 5–10bps). But mid/small caps can be much wider — 50bps or more on a $50 stock. The spread is your hidden cost on every entry/exit.

What changes: market orders are fine on NVDA, AAPL, MSFT — the spread cost is trivial. On something like a $20 small-cap with $0.10 spread (50bps), always use limit orders. Pre-market and after-hours: spreads widen dramatically — sometimes 200–500bps even on mega-caps. Avoid market orders outside 9:30–16:00 ET. Your fractional shares on Robinhood/Fidelity/etc. internalize the spread to some degree, but you're still paying it indirectly.

**Also today:** *NBBO (national best bid offer)* — the consolidated best bid/ask across all US exchanges; what you should reference when checking if a fill was fair.

### Day 22: Pre-market and after-hours liquidity traps

Earnings drop after market close (4:00 PM ET). Stock trades in "after-hours" session (4:00–8:00 PM ET) and "pre-market" (4:00–9:30 AM ET). Volumes here are 1–5% of regular session volume. Price action looks dramatic but rests on tiny size — a single $100K order can move a mega-cap 2% after hours.

The trap: NVDA reports, jumps 12% after hours on light volume, "looks like a moonshot." Then the regular session opens 9:30 AM, real institutional flow arrives, and it gives back 8% of the gain. Common pattern. Rule: don't trade the after-hours print unless you absolutely have to. Wait for the 9:30 open at minimum, ideally for 30 minutes of regular trading to see where real price discovery settles. Setting overnight limit orders ahead of earnings to "capture the move" almost always ends badly.

**Also today:** *Gap fill* — many earnings gaps eventually "fill" within a few weeks as the initial euphoria/panic fades; trades like dip-buying winners often work.

### Day 23: Market-on-close auction (MOC)

The last 10 minutes of the US session (3:50–4:00 PM ET) features the closing auction. Institutions submit MOC (market-on-close) and LOC (limit-on-close) orders. Volume in the closing auction is often 5–10% of total daily volume — sometimes 20%+ on index rebalancing days. The closing print is THE most important price of the day (most ETFs, indices, and benchmarks use it).

What this means: the last 10 min can produce sharp moves that don't reflect any news — just position-balancing into a benchmark. Don't use a market order to exit at 3:55 PM unless you want to be filled in the auction at unknowable price. Don't take "the stock is rising into close" as a sentiment signal — could just be index flows. End-of-quarter (March 31, June 30, etc.) and end-of-month closes are particularly heavy auction days.

**Also today:** *Index rebalancing* — quarterly events where index ETFs adjust holdings; predictable but huge volume.

### Day 24: Volume profile and VWAP

VWAP (volume-weighted average price) = the average price weighted by how much volume traded at each price during the session. It's what institutions benchmark their executions against. If they're buying, they try to fill below VWAP. If selling, above.

For you: VWAP tells you whether today's price action is institutional buying or selling. Stock trading above VWAP in the afternoon, holding the level = institutions buying the dip. Stock below VWAP, lower highs throughout the day = institutions distributing. On a chart, draw the daily VWAP line; the relationship of price to VWAP at 2 PM ET is a strong tell for closing action. Volume profile (volume at price) extends this — shows where most of today's trading happened, which becomes support/resistance for tomorrow.

**Also today:** *Anchored VWAP* — start the VWAP calculation from a specific event (earnings, breakout); cleaner level than daily VWAP for swing trades.

### Day 25: Block trades and dark pools

Most retail trades happen on lit exchanges (NYSE, Nasdaq). But institutions trade huge blocks (>10,000 shares of liquid names, much more of less-liquid) in *dark pools* — private venues where size doesn't show on the order book. Block trades print to the consolidated tape with a delay, often after the move has happened.

Why it matters: when you see a stock spike 1% in 5 minutes on no news, what you're often seeing is the equity market reacting to a block being placed in a dark pool — you see the price reaction before you see the print. Services like Cheddar Flow and Unusual Whales track these. Most retail platforms hide this entirely. You don't have to act on it, but understanding why mysterious moves happen disabuses you of the "must be insider trading" theory — most of it is institutions executing for clients.

**Also today:** *Sweep orders* — buying or selling across multiple venues simultaneously to fill big size fast; often shows up in options data as bullish/bearish signal.

## Week 6 — Deeper passes on Week 1–3 concepts

### Day 26: EV/EBITDA Part 2 — calculating it yourself

The traps: EBITDA is non-GAAP and companies report it differently. Some include stock-based comp (the "honest" version), some exclude it (the optimistic version). When NVDA reports "adjusted EBITDA," that excludes SBC — making it look ~25% better than GAAP EBITDA. For a real comparison, calculate "EBITDA including SBC" yourself: operating income + D&A. That's apples-to-apples.

Second trap: "EV" is supposed to include all debt + minority interests + preferred stock. Many simplistic versions use only "debt − cash." For most US large-caps that's fine, but for messy capital structures (energy, holding companies), do the full calc. Third trap: trailing EBITDA can include one-time items (lawsuit settlements, restructuring charges). Always normalize. EV/EBITDA is meant to be a clean cross-company comparison metric — keep it clean.

**Also today:** *EBITDA margin* — EBITDA / revenue; the operating profitability story stripped of capital structure.

### Day 27: FCF Part 2 — owner earnings, capex normalization

Buffett's "owner earnings" = net income + depreciation/amortization − maintenance capex. The key insight: not all capex is created equal. "Maintenance capex" = what you'd need to spend just to keep the business running at current scale. "Growth capex" = building new factories, expanding capacity. Companies bundle them together in financials.

For NVDA, maintenance capex is tiny ($1–2B) — they don't own fabs. Almost all capex is growth or unnecessary. So NVDA's "owner earnings" are close to GAAP net income. For TSMC, maintenance capex is enormous ($15–20B) just to keep existing fabs running on leading nodes; growth capex is on top. So TSMC's "owner earnings" are much lower than reported FCF suggests. This is why a 25x P/FCF on TSMC isn't the same as 25x P/FCF on a software company. Adjust for it.

**Also today:** *Capital intensity* — total capex / revenue over time; high = factories/infrastructure business; low = software/IP business.

### Day 28: Forward P/E Part 2 — analyst revision trends

Single-number forward P/E is a snapshot. Analyst revision trend is the *signal*. When estimates are being raised every month — that's analyst capitulation, the stock usually outperforms even if it looks "expensive" by P/E. When estimates are being cut quietly — even a low P/E doesn't help, because the E is shrinking.

Where to find it: Bloomberg, Refinitiv, Visible Alpha track this. Free version: FactSet's earnings insight reports. Look at the % of analysts revising up vs down in the last 30 days. NVDA in 2024–2026: 100% of revisions up, every quarter — that's why the P/E held even as the stock 3x'd. Counterexample: Intel in 2023–2024 looked "cheap" at 12x forward but estimates kept getting cut — and the stock kept falling. A stock with falling forward P/E during rising price is bullish (E is growing faster than P).

**Also today:** *Beat-and-raise* — when a company beats earnings AND raises guidance; the strongest combo for stock performance.

### Day 29: Hyperscaler capex Part 2 — the actual flows

Tracing dollars: MSFT spends ~$80B annually on capex. About 60% goes to data center construction (Turner/Fluor/Bechtel get this) and 40% to equipment. Of the equipment dollar: ~50% to AI accelerators (NVDA), ~15% to networking (AVGO/CSCO/ARSP), ~15% to memory (MU/Samsung/Hynix), ~10% to storage (WDC/STX), ~10% to misc (CPUs, power). So MSFT's $80B capex flows ~$15B to NVDA, ~$5B to AVGO, ~$4B to MU.

Multiply by four hyperscalers and you get the rough demand picture. This is why $725B combined 2026 hyperscaler capex = ~$120B for NVDA alone (matches their forward revenue estimate). When MSFT signals capex acceleration, NVDA's forward revenue estimate goes up *in real time*. The transmission is fast and direct. You don't have to wait for NVDA's earnings to know — track the hyperscaler capex commentary in real time.

**Also today:** *Capex unit economics* — the revenue a hyperscaler generates per dollar of capex; declining = AI capex bubble warning sign.

### Day 30: Sector rotation Part 2 — using ETF flows

Beyond just watching XLK vs XLV charts: track actual ETF money flows. When billions flow into XLK over a week and out of XLV, that's the rotation in real-time, not a chart pattern after the fact. Sites: ETF.com, ETFdb.com, ICI weekly flow data, Bloomberg ETF dashboard.

The pattern: institutional rotation is gradual (weeks), retail rotation is sharp (days). When you see XLK flows positive AND high-beta semi stocks outperforming AND low-beta defensives lagging — three confirms = rotation into growth/tech is real. When flows turn and retail piles in late, that's often near the rotation peak. Reverse for healthcare/defensive rotations. This is the highest-level pattern recognition — sector rotation drives more 6-month performance than individual stock picking. The rotation chart matters more than your TA on any single name.

**Also today:** *Smart beta ETFs* — factor-based ETFs (value, momentum, quality, low-vol) that tilt within a sector; rotation can happen within sectors too.

## Selection algorithm reminder

When picking today's concept:

1. Did today's report use a term that hasn't been taught? → Teach that one
2. Did a previous concept come up again? → Teach Part 2 if there is one
3. Has a position's sector been the focus? → Teach a sector-specific concept
4. Quiet day with no triggers? → Pick the next concept in sequence
5. Track what's been taught — avoid same concept two days running unless intentionally going deeper

The goal: 30 days from now, Abbas reads the daily report 3x faster because every term in it has been explained, anchored to his own portfolio.
