# Portfolio Skills — Claude Code Context

This repository contains personal Claude skills for Abbas Al Madani's halal stock portfolio. You (Claude Code) help maintain and update these skills based on real-world feedback.

## Owner context

- **Name:** Abbas Al Madani, based in Kuwait
- **Trading background:** 8 years in forex and indices, new to single-name US equities
- **Tone preference:** Pragmatic, direct, no condescension. Treat as an experienced trader.
- **Strategy:** Halal-compliant (personal definition), aggressive growth, no withdrawals
- **Halal definition:** Business activity only. A stock is halal if the company's core business is permissible (no alcohol, gambling, weapons, pork, pornography, conventional banking/insurance as primary business). Financial ratio screens (debt levels, interest income %) are irrelevant — Abbas is a capital gains trader, not a dividend investor, so he receives none of the company's interest income. Do NOT require Musaffa/AAOIFI financial ratio checks. Only screen the business model.
- **Broker:** Interactive Brokers (IBKR). Commission ~$1.00 per trade (buy or sell). Entry already paid — only ~$1 exit commission remains on open positions. Round-trip = ~$2.

## Repository structure

portfolio-skills/
├── CLAUDE.md                          ← this file
├── portfolio.json                     ← live portfolio state (single source of truth)
├── .claude/
│   └── skills/
│       ├── daily-portfolio-check/     ← runs as Cloud Routine, emails daily report
│       │   ├── SKILL.md
│       │   └── references/
│       └── portfolio-manager/         ← chat-triggered updates to portfolio.json
│           ├── SKILL.md
│           └── references/


## Workflow expectations

When Abbas asks you to make changes:

1. **Read the relevant SKILL.md FIRST** before editing — never assume current state
2. **Show the diff before committing** — Abbas should see what's changing
3. **Use clear, descriptive git commit messages** — e.g., "Add commission framework to rotation logic"
4. **Push to main automatically after his confirmation** — no need to ask "should I push?" every time
5. **Update CHANGELOG.md** with major changes (create it if missing)

## Critical rules that must persist across all edits

### For the daily-portfolio-check skill:

1. **Commission accounting:** Every trim/sell/rotation must show NET P&L after ~$1 exit commission (entry already paid). Broker: IBKR.
2. **No money-losing trims:** If gross profit < $1, recommend HOLD, not partial trim
3. **No money-losing rotations:** Round-trip costs ~$2 minimum ($1 sell + $1 buy)
4. **Small positions (<$75):** Don't suggest partial trims at all
5. **Price verification:** Multi-source confirmation required, NO estimation
6. **Email delivery:** Routine writes outbox/email.json via GitHub connector → GitHub Actions sends via Gmail SMTP
7. **Read portfolio.json fresh each run:** Show last_updated timestamp in email header

### For the portfolio-manager skill:

1. **Always read portfolio.json before updating** — file is source of truth
2. **Validate math:** shares × entry_price = cost_basis (within $0.01)
3. **Show diff and confirm before pushing**
4. **Halal verification required for new positions** — refer to AAOIFI standards
5. **Log every change to history[] array**

## Current portfolio state

Reference `portfolio.json` in repo root for current positions. Last known state:

| Ticker | Shares | Entry | Cost Basis |
|--------|--------|-------|------------|
| NVDA   | 1.3799 | $217.40 | $300.06 |
| LLY    | 0.0986 | $994.87 | $98.11  |
| AVGO   | 0.315  | $412.04 | $129.79 |
| TSM    | 0.224  | $388.35 | $86.99 |
Total cost basis: $614.95. Cash: ~$213.81.

## Known issues and constraints

- Gmail connector can only DRAFT, not SEND — Zapier webhook relay required
- Repo currently PUBLIC (for raw URL access in routines) — don't add secrets
- Cloud Routine fires every day (including weekends) at 6:00 AM GMT+3 (Kuwait) — Abbas reads on waking up
- Weekend emails skip price P&L but still run full catalyst discovery (FDA calendar doesn't pause)
- No DST adjustment needed — delivery time is Kuwait-relative, not NYSE-close relative