# Probability Models — Base Rates for Catalyst Events

This file contains historical base rates for different catalyst types. These are the starting point for Section 4 probability estimates — apply company-specific modifiers on top.

All figures are approximate historical averages. Always search for the most recent FDA statistics or relevant studies before using these as the only reference.

---

## FDA Drug Approval (NDA / BLA — at PDUFA date)

These rates apply **at the PDUFA action date** — after the drug has already been accepted for review. The probability of reaching PDUFA from Phase 1 is much lower (see pipeline section).

| Indication | Base approval rate at PDUFA | Notes |
|---|---|---|
| Oncology (solid tumors) | ~79% | High unmet need drives permissive review |
| Hematologic malignancies | ~86% | Accelerated approval pathways common |
| Rare disease / orphan drug | ~88% | FDA strongly incentivized |
| CNS (depression, schizophrenia) | ~63% | High bar for safety signals |
| Cardiovascular | ~78% | Large outcomes trial usually required |
| Infectious disease / antiviral | ~82% | Post-COVID, FDA pathway clearer |
| Metabolic / endocrine | ~75% | GLP-1 class well-established |
| Dermatology | ~84% | Strong precedent from biologics |
| Respiratory | ~77% | COPD/asthma well-understood endpoint |
| Pain / opioid | ~58% | Heightened FDA scrutiny |
| Overall NDA average | ~85% | Across all indications (once accepted) |
| Overall BLA average | ~82% | Biologics slightly more complex |

### Positive modifiers (each adds ~5–10% to base rate)

- **Breakthrough Therapy Designation (BTD):** Strong FDA collaboration during development, higher approval rate than average. +8–12%
- **Fast Track designation:** Expedited review, more FDA interaction. +4–6%
- **Priority Review:** 6-month review vs. standard 10-month. Doesn't directly increase approval probability but signals FDA urgency. +3–5%
- **Accelerated Approval already granted:** Full approval decision usually positive if confirmatory trial is positive. +10–15%
- **Positive AdCom vote (≥ 7-3):** Overwhelming AdCom support. FDA follows AdCom ~75% of the time. +15–20%
- **Close AdCom vote (5-4 or 6-3):** FDA still often approves despite divided committee. +5–10%
- **Previously approved drug in same class:** Precedent reduces uncertainty. +5–8%
- **Strong Phase 3 (p < 0.001, large effect size):** Statistically overwhelming data. +8–12%
- **Experienced management team (CEO/CMO has brought drug to approval before):** Regulatory execution risk is lower. +4–6%
- **No FDA Complete Response Letter (CRL) history on any prior application:** Clean track record. +3–5%

### Negative modifiers (each subtracts ~5–15%)

- **Prior CRL on this specific drug:** FDA has already rejected it once. Resubmission approval rate ~60–70%. −10–15%
- **Narrow AdCom vote against (4-5):** FDA unlikely to override a negative AdCom unless clear path to addressing concern. −20–30%
- **Safety signals in Phase 3:** Mortality imbalance, serious adverse events, boxed warning required. −15–25%
- **Surrogate endpoint only (no OS data in oncology):** Accelerated approval; may require post-market confirmatory trial. −5%
- **Manufacturing / CMC issues raised in FDA inspection:** Can delay or prevent approval even if drug is effective. −10–20%
- **REMS required (Risk Evaluation and Mitigation Strategy):** FDA concerns about post-market safety. Approval still likely but complicated. −5%
- **Highly competitive market (multiple approvals already):** FDA may set higher bar. −3–5%
- **No orphan designation in rare disease:** Missed an opportunity to raise base rate. −0% (just no boost)

---

## Clinical Trial Phase Transition Rates

Use these when the catalyst is a Phase 2 or Phase 3 readout (not yet at PDUFA).

| Transition | Overall success rate | Oncology | CNS | Infectious disease |
|---|---|---|---|---|
| Phase 1 → Phase 2 | ~63% | ~70% | ~52% | ~68% |
| Phase 2 → Phase 3 | ~31% | ~29% | ~21% | ~38% |
| Phase 3 → NDA submission | ~58% | ~55% | ~44% | ~66% |
| Phase 3 → FDA approval | ~52% | ~50% | ~39% | ~60% |
| Phase 1 → approval (full pipeline) | ~10–14% | ~11% | ~7% | ~13% |

**Important:** These are averages across all trials including first-in-class and "me-too" drugs. A Phase 3 with:
- Strong Phase 2 data (p < 0.01, large effect size): upgrade success rate to ~65–75%
- Weak Phase 2 (p = 0.04, marginal effect): downgrade to ~35–45%
- Unblinded positive interim: upgrade to ~70–80%

---

## Earnings Surprise (small/mid-cap)

| Historical beat pattern | Probability of beating consensus next quarter |
|---|---|
| 4 of last 4 beats | ~75% |
| 3 of last 4 beats | ~65% |
| 2 of last 4 beats | ~50% |
| 1 of last 4 beats | ~35% |
| 0 of last 4 beats | ~25% |

**Squeeze amplifier:** If short interest > 15% of float AND the company beats + raises guidance, historical data shows the average move is ~2.5x the implied move from options.

**Post-earnings drift:** Small-cap earnings beats tend to drift further in the direction of the surprise for 5–10 trading days. Large-cap beats mean-revert faster.

---

## Short Squeeze Base Rates

A short squeeze requires: high short interest + a trigger (positive catalyst) + limited borrow availability + options (call buying adds fuel).

| Short float % | Probability of meaningful squeeze on positive catalyst |
|---|---|
| 5–10% | ~10–15% (small effect) |
| 10–20% | ~25–35% (moderate amplification) |
| 20–35% | ~45–60% (significant amplification) |
| > 35% | ~65–80% (major amplifier — short squeeze thesis itself) |

**Note:** Short squeeze timing is unpredictable even when the setup is present. Size positions based on the underlying catalyst, treat the squeeze as upside optionality, not the base case.

---

## Merger / Acquisition Completion

| Stage | Probability of close |
|---|---|
| Deal announced, no regulatory issues flagged | ~85% |
| Deal announced, antitrust review expected | ~70% |
| Deal in regulatory review (Phase 2 FTC) | ~55% |
| Deal approved by shareholders, awaiting regulatory | ~90% |

**Spread plays:** The annualized return on an M&A spread (current price vs. deal price) reflects the market's completion probability. A 5% spread on a 3-month close = ~20% annualized implied failure probability. Not typically a catalyst play — more of a risk arbitrage setup.

---

## How to combine base rates and modifiers

Example:
- Drug: oncology NDA at PDUFA
- Base rate: 79%
- Modifiers: BTD (+10%), positive AdCom 8-2 vote (+17%), strong Phase 3 p < 0.001 (+10%)
- Raw total: 79 + 10 + 17 + 10 = 116% → cap at 95% (never assign > 95%, uncertainty always exists)
- Final estimate: **92%**

Example 2:
- Drug: CNS depression NDA at PDUFA
- Base rate: 63%
- Modifiers: Prior CRL on this drug (−12%), marginal Phase 3 (p = 0.04) (−8%), no AdCom held (no boost, unusual — may signal FDA concerns) (−5%)
- Raw total: 63 − 12 − 8 − 5 = 38%
- Final estimate: **38%** — this is essentially a coin flip, not a high-conviction play

---

## Notes on using these rates

1. **These are averages.** Individual drugs can and do defy base rates in both directions.
2. **The most important input is Phase 3 data quality.** A drug with overwhelming efficacy data and an 8-2 AdCom is a different bet than a drug scraping by with p = 0.048 and no AdCom.
3. **Always search for the most recent FDA statistics.** FDA approval rates have shifted over time. Search: `"FDA approval rate" [year] NDA BLA statistics` before every report.
4. **The stock move matters more than the approval probability.** A 90% probability of +10% vs. a 60% probability of +200% — the EV on the second is higher. Always calculate expected value, not just probability.
