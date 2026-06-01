# Changelog

All notable changes to the portfolio skills.

## [Unreleased]

### Pending
- Add transaction cost framework ($6 commission) to all rotation suggestions
- Add portfolio.json verification step
- Add net P&L (after commission) to all sell/trim recommendations

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