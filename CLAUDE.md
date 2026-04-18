# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VecAlpha Freqtrade Strategies Repository - A comprehensive collection of Freqtrade trading strategies with automated evaluation, scoring, and leaderboard generation. Integrates with the MarketXpress database for commercial strategy deployment.

## Project Structure

| Directory | Description |
|-----------|-------------|
| `strategies/` | Source strategy files organized by strategy name (300+ strategies) |
| `user_data/strategies/` | Active strategies used for backtesting |
| `user_data/data/` | Market data (feather format) for backtesting |
| `user_data/backtest_results/` | Backtest output files (.json, .zip) |
| `user_data/leaderboard/` | Generated leaderboard files (JSON + Markdown) |
| `scripts/` | Utility scripts for pipeline execution |
| `docs/` | Strategy evaluation reports (Chinese) |
| `strategy_registry.json` | Strategy metadata registry (indicators, timeframe, style, complexity) |

## Common Commands

### Quick Backtest (Docker)
```bash
./test-freqtrade.sh backtest --strategy MyStrategy --timerange=20250101-20250331
./test-freqtrade.sh backtest-gui --strategy MyStrategy  # Backtest + FreqUI webserver
```

### Data Download
```bash
python scripts/download_data.py --period 2025_year --docker
python scripts/download_data.py --period last_1_month --docker --erase
```

### Full Pipeline (Strategy Evaluation)
```bash
# Run complete pipeline: Phase 0 (static filter) → Phase 1 (backtest) → Phase 2 (VecScore)
python scripts/run_pipeline.py

# Fast mode with parallel workers
python scripts/run_pipeline.py --vecscore-mode fast --workers 4

# Skip earlier phases (resume from existing results)
python scripts/run_pipeline.py --skip-phase0 --skip-phase1

# Target specific strategies
python scripts/run_pipeline.py --strategies Nostalgia BinHV45
```

### Batch Backtesting
```bash
# Run all strategies for last 1 week
python scripts/run_batch_backtests.py --period last_1_week --batch 1 --total-batches 1 --skip-errors

# Split into 4 parallel batches
python scripts/run_batch_backtests.py --period last_1_month --batch 1 --total-batches 4 --skip-errors
```

### Leaderboard Generation
```bash
python scripts/generate_leaderboard.py --vecscore user_data/vecscore_results.json --period "Last 30 Days"
python scripts/generate_leaderboard.py --vecscore user_data/vecscore_results_1y.json --period "2025_year"
```

### Database Sync (MarketXpress Integration)
```bash
python scripts/db_sync_leaderboard.py --env auto
python scripts/db_sync_leaderboard.py --check  # View database status

# Sync strategy code to database
python scripts/sync_to_marketxpress.py --strategy Stinkfist
```

### Automated Pipeline (K8s CronJob)
```bash
./scripts/auto_update_leaderboard.sh
./scripts/auto_update_all_periods.sh
```

## Architecture

### Three-Phase Evaluation Pipeline

**Phase 0: Static Filter** (`scripts/static_filter.py`)
- AST-based code analysis (zero-cost pre-screening)
- Eliminates: syntax errors, lookahead leaks, deprecated APIs, test strategies
- Outputs: `user_data/static_filter_result.json`

**Phase 1: Quick Backtest** (`scripts/phase1_quick_backtest.py`)
- 30-day backtest for passing strategies
- Pass criteria: ROI > -10%, trades >= minimum, no errors
- Outputs: `user_data/phase1_results.json`

**Phase 2: VecScore** (`scripts/vecscore.py`)
- Five-dimensional scoring (0-100): P (Return) + R (Risk) + S (Stability) + T (Reliability) + E (Efficiency)
- Grade assignment: S/A/B/C/D with commercial eligibility check
- Outputs: `user_data/vecscore_results.json`

### VecScore Dimensions (Weighted)
- **P (Return, 30%)**: ROI, profit factor, average profit
- **R (Risk, 25%)**: Max drawdown, Sharpe ratio (hard caps: MDD>40%→40pts, Sharpe<0→50pts)
- **S (Stability, 20%)**: Multi-period profitability, ROI volatility
- **T (Reliability, 15%)**: Train/Test overfitting detection, hyperopt parameter stability
- **E (Efficiency, 10%)**: Trade frequency, holding time, capital utilization

### Docker Configuration
- Default image: `neozhou2009/freqtrade-full:latest`
- Data mount: `user_data/` → `/freqtrade/user_data`
- Auto-detects Docker vs native freqtrade installation

### Database Connection (K3s/MarketXpress)
- Auto-resolves: local PostgreSQL, K3s pgpool, or port-forward
- Tables: `strategy_leaderboard`, `leaderboard_history`, `market_strategies`
- Environment: `--env auto|local|k3s`

## Strategy Registry Format

```json
{
  "StrategyName": {
    "timeframe": "5m",
    "style": ["Trend", "MeanReversion"],
    "indicators": ["EMA", "RSI", "MACD"],
    "complexity": 3,
    "family": "Nostalgia",
    "side": "Long",
    "market": "Trending",
    "features": ["hyperopt"],
    "directory": "StrategyName",
    "filename": "StrategyName.py"
  }
}
```

## Time Period Options

Pipeline supports multiple evaluation periods:
- `last_1_week` / `last_1_month` / `last_3_months` / `last_6_months` / `last_1_year` / `2025_year`

Use `--suffix` to isolate results by period:
```bash
python scripts/run_pipeline.py --suffix 1y --days 365
```