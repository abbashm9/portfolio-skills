# Catalyst Scanner — Deep Research Protocol

This file defines the full research protocol for each candidate surfaced in Step 3.5 of the daily check. The goal is to estimate the probability-weighted expected value of a catalyst play and assign a conviction score (0–10).

## What makes a valid catalyst play

A catalyst play is a small/mid-cap stock with:
1. A **dated, near-term binary event** (1–14 days out) — FDA decision, Phase 3 readout, earnings, merger close, regulatory ruling
2. An **asymmetric payoff** — upside if catalyst resolves positively is significantly larger than the entry price (ideally >100%)
3. A **knowable probability estimate** — not pure speculation; the event is publicly scheduled and historical base rates exist
4. **Halal compliance** — no interest-dependent revenue, clean debt ratios

The stocks that go up 500–1300% in a day are almost always pre-catalyst plays. The move was already coming — someone sized in before the event.

---

## Research protocol — run for each candidate

### 1. Confirm the event (mandatory)

- Search `"[TICKER] FDA PDUFA" OR "[TICKER] data readout" OR "[TICKER] earnings date"`
- Find the **exact date** of the catalyst. If no confirmed date found, discard the candidate.
- Confirm the date hasn't been pushed (FDA frequently extends PDUFA by 3 months when they issue a Complete Response Letter). Search: `"[TICKER] PDUFA extended" OR "[TICKER] FDA delay"`

### 2. What is the binary outcome?

State clearly what happens in each scenario:
- **Bull case:** [event resolves positively] → stock does [expected price move, cite analyst targets or historical analogs]
- **Bear case:** [event resolves negatively] → stock does [typical rejection drop, usually -50% to -80% for FDA rejections; -15% to -40% for earnings misses]

### 3. Estimate approval / success probability

**For FDA catalysts:**
- Search `"[indication] FDA approval rate" OR "[drug class] PDUFA success rate"`
- Check the FDA's historical approval rate for that indication and drug class (e.g., oncology NDA approvals are ~85%; rare disease is ~90%+ with breakthrough therapy designation)
- Check if the drug has **breakthrough therapy designation** (BTD), **fast track**, or **priority review** — each raises probability
- Check AdCom (advisory committee) vote if one has already occurred — an 8-2 AdCom vote in favor is a very strong signal
- Check if a **Complete Response Letter (CRL)** was issued before — a CRL history lowers probability
- Check the **PDUFA action date** vs. the actual company announcement — sometimes companies pre-announce ahead of PDUFA

Search: `"[TICKER] advisory committee" OR "[TICKER] AdCom vote" OR "[TICKER] breakthrough therapy"`

**For clinical trial readouts:**
- Search `"[TICKER] phase 3 primary endpoint" OR "[TICKER] trial results"`
- Find the primary endpoint and whether phase 2 results were strong (phase 2 → phase 3 success rate is ~50% overall, but much higher when phase 2 was strongly positive)

**For earnings plays:**
- Search `"[TICKER] earnings estimate" OR "[TICKER] EPS surprise history"`
- Check the last 4 quarters — does this company consistently beat? (3+ of 4 beats = high quality setup)
- Check analyst consensus vs. whisper number
- Check short interest — high SI + earnings beat = short squeeze amplifier

### 4. Market cap and float analysis

- Search `"[TICKER] market cap" OR "[TICKER] shares outstanding float"`
- **Small float = larger % move.** A $50M market cap stock that gets FDA approval in a large indication can 10x; a $5B stock might do +30%.
- Ideal target zone: **$50M – $1B market cap** at time of entry
- Check if there's been recent insider buying (Form 4 filings) — search `"[TICKER] insider buying" OR "[TICKER] Form 4"`

### 5. Short interest

- Search `"[TICKER] short interest" OR "[TICKER] short float %"`
- High short interest (> 15% of float) + positive catalyst = short squeeze amplifier on top of the move itself
- This is what turns a +50% approval move into a +200% approval move

### 6. Cash runway (for biotech/pharma)

- A company that needs to raise cash before or just after the catalyst will dilute shareholders — this caps the upside
- Search `"[TICKER] cash runway" OR "[TICKER] cash position quarterly"`
- If cash < 6 months runway, heavily discount the upside

### 7. Options market implied move

- If options data is available, the implied move (straddle price / stock price) shows what the market is pricing in for the event
- Search `"[TICKER] options implied move" OR "[TICKER] IV earnings"`
- If the stock is already pricing in a +80% move but you think upside is +100%, the edge is thin. If the stock is pricing in +30% but the analog drugs ran +400% on approval, that's a fat pitch.

### 8. Halal compliance deep check

Beyond the rapid filter in Step 3.5.2:
- Search `"[TICKER] annual report revenue breakdown" OR "[TICKER] 10-K interest income"`
- Confirm interest income is < 5% of total revenue (AAOIFI threshold)
- Confirm total debt / total assets < 33%
- Confirm accounts receivable / market cap < 49%
- If the company is a pharma/biotech with no approved products, it typically has zero revenue — debt ratios are often fine, but check for any credit facility with interest charges

---

## Conviction scoring (0–10)

| Factor | Max points |
|---|---|
| Event date confirmed and ≤ 14 days out | 1 |
| Probability estimate > 60% OR very strong prior data | 2 |
| Small float / small market cap (< $500M) | 1 |
| High short interest (> 15%) = squeeze amplifier | 1 |
| Cash runway > 12 months (no dilution risk) | 1 |
| AdCom already voted in favor OR phase 2 was strongly positive | 2 |
| Options implied move suggests market is underpricing the event | 1 |
| Halal fully verified | 1 |
| **Total** | **10** |

**Threshold:** Score ≥ 6 to include in the report. Score < 6 → discard.

---

## Position sizing rules for catalyst plays

Abbas's max allocation per catalyst name: **30% of total portfolio value** (positions + cash combined).

With ~$800 total portfolio: max position = ~$240 per name.

**Why 30% and not more:**
- Binary events can go -70% on rejection. A 30% position losing 70% = -21% portfolio hit — painful but survivable.
- A 30% position gaining 300% = +90% portfolio gain from a single play.
- Never stack two catalyst plays simultaneously above 30% each — max combined catalyst exposure = 50% of portfolio.

**Entry timing:**
- For FDA PDUFA plays: enter 5–10 trading days before the date. Later entries have compressed risk/reward because the move has already started.
- For earnings plays: enter 3–5 days before the print.
- Avoid entering on the day of the event — you're paying the full "hope premium" with no time to benefit from pre-event drift.

---

## After the catalyst fires

- If **positive:** reassess immediately. Is the move done or is there a sustained re-rating? If the stock is up 200%+ in one day, take 50% off the table — lock in the win, let the rest run.
- If **negative:** exit at market open, don't average down. The thesis is broken. A stock down 70% on FDA rejection doesn't recover quickly — capital needs to be redeployed.

---

## Analog reference — why these moves happen

For context on size of moves by catalyst type:

| Catalyst type | Typical positive move | Typical negative move |
|---|---|---|
| FDA approval (NDA) | +50% to +500% | -50% to -80% |
| Phase 3 success | +100% to +1000% | -40% to -80% |
| Earnings beat + raise (small cap) | +20% to +100% | -15% to -40% |
| Short squeeze trigger | +100% to +1000% | Fades -30% to -70% |
| Merger/acquisition announcement | +20% to +60% | -5% to -15% |

The 500%–1300% moves Abbas sees (SUME, INHT, NPT, BYAH) are typically Phase 3 readouts or FDA approvals on small-float biotech names, often combined with high short interest producing a squeeze on top of the underlying approval move. These are findable in advance from the FDA calendar and biotech catalyst trackers.
