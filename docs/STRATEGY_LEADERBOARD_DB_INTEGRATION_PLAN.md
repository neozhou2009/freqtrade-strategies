# Implementation Plan: Database-Driven Strategy Leaderboard (Hybrid JSONB)

This plan details the transition from static JSON files to a PostgreSQL-backed leaderboard in `~/marketxpress`, using the **Hybrid JSONB (Scheme A)** approach for optimal performance and flexibility.

## User Review Required

> [!IMPORTANT]
> This migration will transition the source of truth for the leaderboard from local `.json` files to the `marketxpress` PostgreSQL database.
> The generation script in `freqtrade-strategies` will now act as a **pushed worker**, sending processed data to the database via an API call or direct DB connection.

> [!CAUTION]
> Once implemented, the frontend will no longer reflect manual changes made to the `.json` files; instead, it will strictly show what is stored in the database.

## Proposed Changes

### 1. Database Layer (MarketXpress Backend)

We need to define the schema and models in the `strategy-service`.

#### [NEW] `backend/services/strategy-service/src/models/leaderboard.py`
Define the `StrategyLeaderboard` model:
- Columns: `strategy_name` (PK/Index), `period` (PK/Index).
- Flat Columns: `composite_score`, `cagr`, `sharpe`, `max_drawdown_pct`, `winrate`, `trades`.
- JSONB Column: `metadata` (for `styles`, `indicators`, `category`).
- Timestamp: `updated_at`.

#### [NEW] `backend/services/strategy-service/src/routers/leaderboard_api.py`
Add endpoints:
- `GET /leaderboard`: Fetch rankings (supports sorting by `cagr`, `sharpe`, etc.).
- `POST /leaderboard/upsert`: (Internal) Used by the generation script to sync data.

---

### 2. Synchronization Layer (Strategies Repo)

Update the ingestion logic to push data to the database.

#### [NEW] `scripts/db_sync_leaderboard.py`
A new script in the `freqtrade-strategies` repo who's responsibility is:
- Reads `leaderboard_*.json`.
- Maps the nested JSON to the flat columns + JSONB metadata.
- Executes `INSERT ... ON CONFLICT (strategy_name, period) DO UPDATE`.

---

### 3. Frontend Layer (MarketXpress Frontend)

Update the Next.js frontend to fetch from the new real-time API.

#### [MODIFY] `frontend-next/src/services/leaderboardApi.ts`
Replace mock data calls with `fetch("${BACKEND_URL}/api/v1/leaderboard?period=${period}")`.

#### [MODIFY] `frontend-next/src/components/MainLeaderboardSection.tsx`
Update the table component to match the new schema fields.

## Open Questions

1. **Authentication**: Do we need API Key authentication for the `POST /leaderboard/upsert` endpoint to prevent unauthorized data injection?
2. **History Retention**: How many months of `leaderboard_history` records should we keep in the database before archiving/purging?

## Verification Plan

### Automated Tests
- **API Tests**: Verify that `POST /leaderboard/upsert` correctly handles JSONB payloads and preserves data integrity.
- **Query Performance**: Verify that `ORDER BY composite_score` on the database table takes < 100ms for 1000+ strategies.

### Manual Verification
- Run `python scripts/db_sync_leaderboard.py`.
- Check the PostgreSQL database via `psql` to confirm the records exist.
- Navigate to the `/leaderboard` page in the MarketXpress UI and verify that real data is displayed.
