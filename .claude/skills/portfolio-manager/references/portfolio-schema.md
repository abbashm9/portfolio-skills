# portfolio.json — Schema Reference

Single source of truth for Abbas's portfolio state. Every field documented below.

## Top-level structure

```json
{
  "schema_version": "1.0",
  "last_updated": "ISO 8601 timestamp",
  "owner": "string",
  "currency": "USD",
  "broker": "string",
  "strategy": "string",
  "withdrawal_intent": false,
  "positions": [...],
  "cash_available": number,
  "total_cost_basis": number,
  "totals": {...},
  "history": [...]
}
```

## Field definitions

### Metadata fields

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Version of this schema. Bump if structure changes. |
| `last_updated` | ISO 8601 string | When this file was last modified. Asia/Kuwait timezone. |
| `owner` | string | "Abbas Al Madani" |
| `currency` | string | "USD" — all amounts in USD |
| `broker` | string | Optional. E.g., "Wahed Invest", "Sarwa", "Interactive Brokers" |
| `strategy` | string | "halal_aggressive_growth" — the trading framework |
| `withdrawal_intent` | boolean | false — Abbas isn't pulling money out, growth-focused |

### Position object

Each entry in `positions[]`:

```json
{
  "ticker": "NVDA",
  "company": "NVIDIA Corporation",
  "sector": "Semiconductors",
  "shares": 1.3799,
  "entry_price": 217.40,
  "cost_basis": 300.06,
  "entry_date": "2026-05-11",
  "stop_loss": 204.00,
  "stop_loss_pct": -6.4,
  "tp1": {"price": 240.00, "sell_pct": 30},
  "tp2": {"price": 260.00, "sell_pct": 40},
  "tp3": {"price": 285.00, "sell_pct": 30},
  "catalyst": "string",
  "halal_verified": "2026-05-11",
  "halal_source": "Musaffa AAOIFI",
  "notes": "string"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | Yes | Exchange ticker, uppercase |
| `company` | string | Yes | Full company name |
| `sector` | string | Yes | E.g., "Semiconductors", "Pharmaceuticals", "Software" |
| `shares` | number | Yes | Decimal allowed (fractional). 4 decimal precision. |
| `entry_price` | number | Yes | Weighted average entry price (recalculated on adds) |
| `cost_basis` | number | Yes | shares × entry_price |
| `entry_date` | ISO date | Yes | First entry date for this position |
| `stop_loss` | number | Yes | Hard stop-loss price |
| `stop_loss_pct` | number | Yes | Percentage from entry (negative number) |
| `tp1` | object or null | Yes | First take-profit level |
| `tp2` | object or null | Yes | Second take-profit level |
| `tp3` | object or null | Optional | Third take-profit level (may be null) |
| `catalyst` | string | Optional | Upcoming binary event |
| `halal_verified` | ISO date | Yes | Last AAOIFI verification date |
| `halal_source` | string | Yes | Where verified: "Musaffa AAOIFI", "Zoya", "Islamicly" |
| `notes` | string | Optional | Free-form notes |

### Take-profit object

Each `tp1/tp2/tp3` is either `null` or:

```json
{"price": 240.00, "sell_pct": 30}
```

- `price` — trigger price
- `sell_pct` — percentage of remaining shares to sell at this level

### Cash and totals

```json
{
  "cash_available": 15.00,
  "total_cost_basis": 706.99,
  "totals": {
    "positions_count": 5,
    "sectors_held": ["Semiconductors", "Pharmaceuticals"],
    "largest_position_pct": 42.4,
    "concentration_warning": "NVDA 42% — single-event risk on May 20 earnings"
  }
}
```

- `cash_available` — uninvested USD ready to deploy
- `total_cost_basis` — sum of all positions' cost_basis (excludes cash)
- `totals.positions_count` — count of positions[]
- `totals.sectors_held` — unique sectors
- `totals.largest_position_pct` — largest cost_basis / total_cost_basis × 100
- `totals.concentration_warning` — string if any position >40%, else null

### History array

Append-only log of every change. Each entry:

```json
{
  "date": "2026-05-15",
  "action": "BUY",
  "ticker": "MSFT",
  "shares": 0.4,
  "price": 445.00,
  "amount": 178.00,
  "notes": "Optional"
}
```

| Action | Description |
|---|---|
| `BUY` | New position or add-to-existing |
| `SELL` | Partial or full exit |
| `DEPOSIT` | Cash added to account |
| `WITHDRAW` | Cash removed from account |
| `STOP_UPDATE` | Stop-loss changed |
| `TP_UPDATE` | Take-profit level changed |
| `HALAL_RECHECK` | Compliance reverified |
| `CATALYST_UPDATE` | Upcoming event details changed |

For SELL entries, also include:
- `realized_pnl` — the $ profit/loss from this sale

For STOP_UPDATE/TP_UPDATE entries, include:
- `old_value`, `new_value` — track what changed

## Validation rules

When updating the file, enforce:

1. `shares > 0` for all positions (use SELL to remove, don't set to 0)
2. `cost_basis = shares × entry_price` (within $0.01)
3. `stop_loss < entry_price` (stops are below entry for long positions)
4. `tp1.price < tp2.price < tp3.price` if multiple TPs exist
5. `tp1.price > entry_price` (TPs above entry for long positions)
6. `halal_verified` cannot be in the future
7. `cash_available >= 0` (no negative cash)
8. `last_updated` is updated on EVERY change

## When the schema changes

If we add new fields (e.g., dividends, options, currency hedges), bump `schema_version` and update this doc. Backward compatibility: new fields should be optional with sensible defaults.
