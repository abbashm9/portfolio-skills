# Portfolio Skills — Claude Code Context

This repository contains personal Claude skills for Abbas Al Madani's halal stock portfolio. You (Claude Code) help maintain and update these skills based on real-world feedback.

## Owner context

- **Name:** Abbas Al Madani, based in Kuwait
- **Trading background:** 8 years in forex and indices, new to single-name US equities
- **Tone preference:** Pragmatic, direct, no condescension. Treat as an experienced trader.
- **Strategy:** Halal-compliant (AAOIFI), aggressive growth, no withdrawals
- **Broker commission:** $3.00 per trade (buy or sell). Entry already paid — only $3 exit commission remains on open positions.

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

1. **Commission accounting:** Every trim/sell/rotation must show NET P&L after $3 exit commission (entry already paid)
2. **No money-losing trims:** If gross profit < $3, recommend HOLD, not partial trim
3. **No money-losing rotations:** Round-trip costs $6 minimum ($3 sell + $3 buy)
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
| AMD    | 0.117  | $428.84 | $50.17 |

Total cost basis: $665.12. Cash: ~$158.53.

## Known issues and constraints

- Gmail connector can only DRAFT, not SEND — Zapier webhook relay required
- Repo currently PUBLIC (for raw URL access in routines) — don't add secrets
- Cloud Routine fires every day (including weekends) at 6:00 AM GMT+3 (Kuwait) — Abbas reads on waking up
- Weekend emails skip price P&L but still run full catalyst discovery (FDA calendar doesn't pause)
- No DST adjustment needed — delivery time is Kuwait-relative, not NYSE-close relative