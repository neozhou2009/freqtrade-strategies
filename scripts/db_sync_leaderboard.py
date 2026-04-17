#!/usr/bin/env python3
import os
import json
import glob
import logging
import argparse
import subprocess
from datetime import datetime
import psycopg2
from psycopg2.extras import Json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ─── Environment presets ────────────────────────────────────────────────────────
# local: plain PostgreSQL on localhost (dev / CI)
LOCAL_DB_URL = "postgresql://postgres:postgres@localhost:5432/quantrading"

# k3s: HA pgpool inside the cluster — credentials read from env or defaults
K3S_PG_USER     = os.getenv("K3S_PG_USER",     os.getenv("POSTGRES_USER",     "quantrading"))
K3S_PG_PASSWORD = os.getenv("K3S_PG_PASSWORD", os.getenv("POSTGRES_PASSWORD", "quantrading123"))
K3S_PG_DB       = os.getenv("K3S_PG_DB",       os.getenv("POSTGRES_DB",       "quantrading"))
K3S_PG_SVC      = os.getenv("K3S_PG_SVC",      "mx-postgres-ha-postgresql-ha-pgpool")
K3S_PG_NS       = os.getenv("K3S_PG_NS",       "infra")


def _k3s_db_url() -> str:
    """Resolve the pgpool ClusterIP via kubectl."""
    try:
        ip = subprocess.check_output(
            ["kubectl", "get", "svc", K3S_PG_SVC, "-n", K3S_PG_NS,
             "-o", "jsonpath={.spec.clusterIP}"],
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).decode().strip()
        if not ip or ip == "None":
            return None
        return f"postgresql://{K3S_PG_USER}:{K3S_PG_PASSWORD}@{ip}:5432/{K3S_PG_DB}"
    except:
        return None


def _resolve_db_url(env: str, explicit_db: str | None) -> str:
    """Determine the best DB URL to use by probing reachability."""
    if explicit_db:
        return explicit_db
    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]

    potential_urls = []
    
    # 1. Identify which URLs to probe based on env flag
    if env in ("auto", "local"):
        # Standard local Postgres
        potential_urls.append(("local", LOCAL_DB_URL))
        # K3s credentials on localhost (handles port-forwarding)
        potential_urls.append(("local-port-forward", f"postgresql://{K3S_PG_USER}:{K3S_PG_PASSWORD}@localhost:5432/{K3S_PG_DB}"))
    
    if env in ("auto", "k3s"):
        k3s_url = _k3s_db_url()
        if k3s_url:
            potential_urls.append(("k3s-cluster", k3s_url))

    # 2. Probe each URL with a short timeout
    for label, url in potential_urls:
        try:
            conn = psycopg2.connect(url, connect_timeout=1)
            conn.close()
            logger.info(f"Connected to database via {label}")
            return url
        except Exception:
            continue
    
    # 3. If no probe succeeded but an environment was explicitly chosen, return it anyway
    if env == "local": return LOCAL_DB_URL
    if env == "k3s": 
        url = _k3s_db_url()
        if url: return url
        
    return LOCAL_DB_URL # Final fallback


# Legacy default (used only when --db flag is parsed with its argparse default)
DEFAULT_DB_URL = os.getenv("DATABASE_URL", LOCAL_DB_URL)

def sync_leaderboard_file(file_path, conn):
    """Sync a single leaderboard JSON file to the database."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        period = data.get("period_slug", data.get("period", "unknown"))
        generated_at = data.get("generated_at")
        leaderboard = data.get("leaderboard", [])
        
        logger.info(f"Syncing {len(leaderboard)} strategies for period: {period}")
        
        with conn.cursor() as cur:
            for strat in leaderboard:
                strategy_name = strat.get("strategy")
                if not strategy_name:
                    continue
                
                # Extract main metrics
                composite_score = strat.get("composite_score", 0)
                cagr = strat.get("cagr", 0)
                sharpe = strat.get("sharpe", 0)
                max_drawdown_pct = strat.get("max_drawdown_pct", 0)
                winrate = strat.get("winrate", 0)
                trades = strat.get("trades", 0)
                
                # Prepare metadata (styles, indicators, category, family, complexity, side, timeframe,
                #                   rank_delta, profit_factor, calmar)
                metadata = {
                    "styles": strat.get("styles", []),
                    "category": strat.get("category", "Uncategorized"),
                    "family": strat.get("family"),
                    "complexity": strat.get("complexity"),
                    "side": strat.get("side"),
                    "indicators": strat.get("indicators", []),
                    "timeframe": strat.get("timeframe"),
                    "rank_delta": strat.get("rank_delta", 0),
                    "profit_factor": strat.get("profit_factor", 0),
                    "calmar": strat.get("calmar", 0),
                }
                
                # UPSERT logic: INSERT ... ON CONFLICT (strategy_name, period) DO UPDATE
                upsert_query = """
                INSERT INTO public.strategy_leaderboard (
                    strategy_name, period, composite_score, cagr, sharpe, 
                    max_drawdown_pct, winrate, trades, metadata, generated_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (strategy_name, period) DO UPDATE SET
                    composite_score = EXCLUDED.composite_score,
                    cagr = EXCLUDED.cagr,
                    sharpe = EXCLUDED.sharpe,
                    max_drawdown_pct = EXCLUDED.max_drawdown_pct,
                    winrate = EXCLUDED.winrate,
                    trades = EXCLUDED.trades,
                    metadata = EXCLUDED.metadata,
                    generated_at = EXCLUDED.generated_at,
                    updated_at = CURRENT_TIMESTAMP;
                """
                
                cur.execute(upsert_query, (
                    strategy_name, period, composite_score, cagr, sharpe,
                    max_drawdown_pct, winrate, trades, Json(metadata), generated_at
                ))
            
            # Record history snapshot (Optional but recommended)
            for idx, strat in enumerate(leaderboard):
                rank = idx + 1
                history_query = """
                INSERT INTO public.leaderboard_history (
                    strategy_name, period, rank, score, recorded_at
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (strategy_name, period, recorded_at) DO NOTHING
                """
                cur.execute(history_query, (
                    strat["strategy"], period, rank, strat["composite_score"], generated_at
                ))
                
        conn.commit()
        logger.info(f"[✓] Successfully synced {file_path}")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"[✗] Error syncing {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sync Strategy Leaderboard JSON results to PostgreSQL")
    parser.add_argument("--dir", default="user_data/leaderboard", help="Directory containing leaderboard JSON files")
    parser.add_argument("--db", default=None, help="Explicit database connection URL (overrides --env)")
    parser.add_argument(
        "--env",
        default="auto",
        choices=["auto", "local", "k3s"],
        help=(
            "Target environment: "
            "'local' = localhost:5432, "
            "'k3s' = resolve pgpool ClusterIP via kubectl, "
            "'auto' = try local first then k3s (default)"
        ),
    )
    args = parser.parse_args()

    # 1. Resolve DB URL
    try:
        db_url = _resolve_db_url(args.env, args.db)
    except RuntimeError as e:
        logger.error(f"Failed to resolve database URL: {e}")
        return

    # 2. Connect to Database
    try:
        conn = psycopg2.connect(db_url)
        logger.info(f"Connected to database: {db_url.split('@')[-1]}")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return

    # 2. Find all leaderboard_*.json files
    json_files = glob.glob(os.path.join(args.dir, "leaderboard_*.json"))
    if not json_files:
        logger.warning(f"No leaderboard JSON files found in {args.dir}")
        conn.close()
        return

    # 3. Sync each file
    for file_path in sorted(json_files):
        sync_leaderboard_file(file_path, conn)

    conn.close()
    logger.info("Sync completed.")

if __name__ == "__main__":
    main()
