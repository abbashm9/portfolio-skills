# Changelog

All notable changes to the portfolio skills.

## [Unreleased]

### Pending
- Add portfolio.json verification step
- Add net P&L (after commission) to all sell/trim recommendations

## [1.4.0] — 2026-07-27
### Changed — strategy pivot away from binary-catalyst trading (see decisions.md)
- stock-finder: full rewrite from FDA/PDUFA catalyst-only discovery to sector-agnostic momentum/technical discovery (breakouts, volume, flow, RS leadership). Hard exclusions: haram businesses + defense/military contractors.
- daily-portfolio-check Step 3.5.1: replaced the 8-query FDA/biotech-only search block with a broad sector-agnostic momentum sweep; removed the defense-contract-award search entirely
- daily-portfolio-check Gate 1 (Step 3.5.2): now requires a live momentum/flow signal in the last 5 trading days, not just a dated future catalyst
- daily-portfolio-check Step 2.6: de-hardcoded the CAPR/VERA-specific news queries (both positions closed) — now builds queries dynamically from any `enhanced_news_watch` position's ticker/company/notes
- daily-portfolio-check Step 2.6D: replaced the obsolete CAPR-specific "FDA briefing docs" special case with a general holding-period staleness check (flag positions held >10-15 trading days)
- daily-portfolio-check Step 3.7: max position size cut from 30% to 15-18% of portfolio; target 5-7 concurrent positions instead of one dominant name; added mandatory stop-limit (not stop-market) rule
- Added `decisions.md` — append-only strategy decision log, starting with the 2026-07-27 pivot rationale (CAPR gap-stop loss, 3-for-5 binary-catalyst loss pattern)

## [1.3.0] — 2026-06-01
### Added
- daily-portfolio-check: transaction cost framework — $6 commission gates on all sell/trim/rotation suggestions, net P&L display required, small-position (<$75) partial trim ban

## [1.2.0] — 2026-05-15
### Changed
- daily-portfolio-check: stricter anti-estimation rules (multi-source verification)
- daily-portfolio-check: stronger send-not-draft instructions
- portfolio-manager: connector-first fetch strategy for portfolio.json

## [1.1.0] — 2026-05-14
### Added
- portfolio-manager skill (chat-triggered portfolio updates)
- portfolio.json as single source of truth

### Changed
- daily-portfolio-check: read positions from portfolio.json instead of hardcoded

## [1.0.0] — 2026-05-13
### Added
- daily-portfolio-check skill with HTML email output
- 30-day education curriculum (US equity concepts)
- Cloud Routine triggered weekdays 11:05 PM GMT+3