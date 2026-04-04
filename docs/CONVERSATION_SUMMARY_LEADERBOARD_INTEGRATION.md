# Strategy Leaderboard Integration: Project & State Summary
**Project**: `freqtrade-strategies` ➔ `marketxpress`
**Date**: 2026-04-03

## 1. Objective
Replace the mock-based leaderboard in `marketxpress` with the real-time, scoring-based pipeline from `freqtrade-strategies`.

## 2. Agreed Architectural Design (Scheme A: Hybrid JSONB)
To balance performance (sorting/filtering) and flexibility (nested tags/metadata), we decided on a **Relational + Document** hybrid approach.

### SQL Schema (PostgreSQL)
```sql
-- 1. Main Leaderboard Table
CREATE TABLE IF NOT EXISTS public.strategy_leaderboard (
    strategy_name VARCHAR(255) NOT NULL,
    period VARCHAR(50) NOT NULL, -- 'last_1_week', 'last_1_month', etc.
    composite_score NUMERIC(10, 2) DEFAULT 0,
    cagr NUMERIC(10, 4) DEFAULT 0,
    sharpe NUMERIC(10, 4) DEFAULT 0,
    max_drawdown_pct NUMERIC(10, 4) DEFAULT 0,
    winrate NUMERIC(10, 4) DEFAULT 0,
    trades INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb, -- Stores styles, indicators, category
    generated_at TIMESTAMP WITH TIME ZONE, -- When the backtest was actually run
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- DB insertion time
    PRIMARY KEY (strategy_name, period)
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_leaderboard_rank ON public.strategy_leaderboard (period, composite_score DESC);
CREATE INDEX IF NOT EXISTS idx_leaderboard_cagr ON public.strategy_leaderboard (period, cagr DESC);

-- 2. History Table (Optional, for trend analysis)
CREATE TABLE IF NOT EXISTS public.leaderboard_history (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(255) NOT NULL,
    period VARCHAR(50) NOT NULL,
    rank INTEGER,
    score NUMERIC(10, 2),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 3. Current State of Work
| Component | Status | File Location |
| :--- | :--- | :--- |
| **Data Pipeline** | 🟢 Done | `scripts/generate_leaderboard.py` |
| **Automated Batches** | 🟢 Done | `scripts/run_all_batches.py` |
| **Frontend Prototype** | 🟢 Done | `docs/vecalpha-ranking-prototype.html` |
| **Integration Plan** | 🟢 Saved | `docs/STRATEGY_LEADERBOARD_DB_INTEGRATION_PLAN.md` |
| **DB Migration** | 🟡 Drafted | `~/marketxpress/database/migrations/001_...sql` |
| **Backend Ingestion** | 🔴 Pending | `scripts/db_sync_leaderboard.py` |

## 4. Next Steps for Execution
When ready to proceed, the following sequence is recommended:

1.  **Execute DB Migration**: Apply the SQL schema to the `marketxpress` PostgreSQL instance.
2.  **Define FastAPI Models**: Create the SQLAlchemy model in `marketxpress/backend/services/strategy-service/src/models/leaderboard.py`.
3.  **Build Ingestion Script**: Implement `scripts/db_sync_leaderboard.py` to push the local JSON data into the database.
4.  **Update Frontend Next.js**: Switch `leaderboardApi.ts` from mock data to real API endpoints.

---
**Summary for AI**: This document serves as the "Baton" for future sessions. Use the provided SQL and the "Hybrid JSONB" logic to finalize the integration.
