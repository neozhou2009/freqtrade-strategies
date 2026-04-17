#!/usr/bin/env python3
"""
Sync a strategy from freqtrade-strategies to the marketxpress database.
Uses the marketxpress configuration and database schemas.

Usage:
  python scripts/sync_to_marketxpress.py --strategy Stinkfist
"""

import os
import sys
import re
import uuid
import logging
import argparse
import subprocess
import psycopg2
from pathlib import Path
from datetime import datetime, timezone
from psycopg2.extras import Json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Environment Presets (Adapted from db_sync_leaderboard.py) ---
K3S_PG_USER     = os.getenv("K3S_PG_USER",     os.getenv("POSTGRES_USER",     "quantrading"))
K3S_PG_PASSWORD = os.getenv("K3S_PG_PASSWORD", os.getenv("POSTGRES_PASSWORD", "quantrading123"))
K3S_PG_DB       = os.getenv("K3S_PG_DB",       os.getenv("POSTGRES_DB",       "quantrading"))
K3S_PG_SVC      = os.getenv("K3S_PG_SVC",      "mx-postgres-ha-postgresql-ha-pgpool")
K3S_PG_NS       = os.getenv("K3S_PG_NS",       "infra")

LOCAL_DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/quantrading")

def _get_k3s_credentials():
    """Retrieve database password from K8s secrets if not provided in environment."""
    user = os.getenv("K3S_PG_USER", os.getenv("POSTGRES_USER", "quantrading"))
    password = os.getenv("K3S_PG_PASSWORD", os.getenv("POSTGRES_PASSWORD"))
    
    if not password:
        # Try different possible secret locations/keys used in marketxpress
        secret_configs = [
            ("infra", "quantrading-secrets", "POSTGRES_PASSWORD"),
            ("infra", "quantrading-secrets", "postgres-password"),
            ("quantrading", "quantrading-secrets", "postgresql-password"),
        ]
        import base64
        for ns, name, key in secret_configs:
            try:
                cmd = ["kubectl", "-n", ns, "get", "secret", name, f"-o=jsonpath={{.data.{key}}}"]
                b64 = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=5).decode().strip()
                if b64:
                    password = base64.b64decode(b64).decode().strip()
                    logger.info(f"Retrieved database password from secret {ns}/{name}:{key}")
                    break
            except:
                continue
    
    return user, (password or "quantrading123")

def _get_k3s_db_url(user, password) -> str:
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
        return f"postgresql://{user}:{password}@{ip}:5432/{K3S_PG_DB}"
    except:
        return None

_PF_PROCESS = None
def _ensure_port_forward(user, password):
    """Attempt to establish a port-forward to the DB if unreachable."""
    global _PF_PROCESS
    local_url = f"postgresql://{user}:{password}@localhost:5432/{K3S_PG_DB}"
    
    # Try existing connection (maybe someone else established a PF)
    try:
        conn = psycopg2.connect(local_url, connect_timeout=1)
        conn.close()
        return local_url
    except:
        pass

    # Start PF
    logger.info(f"Port 5432 unreachable. Attempting automatic port-forward to {K3S_PG_SVC}...")
    try:
        import atexit
        cmd = ["kubectl", "port-forward", f"svc/{K3S_PG_SVC}", "5432:5432", "-n", K3S_PG_NS]
        _PF_PROCESS = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Register cleanup
        def cleanup():
            if _PF_PROCESS:
                logger.info("Cleaning up port-forward process...")
                _PF_PROCESS.terminate()
        atexit.register(cleanup)
        
        # Wait for readiness
        time_waited = 0
        while time_waited < 10:
            import time
            time.sleep(1)
            time_waited += 1
            try:
                conn = psycopg2.connect(local_url, connect_timeout=1)
                conn.close()
                logger.info("Automatic port-forward established and reachable.")
                return local_url
            except:
                if _PF_PROCESS.poll() is not None:
                    break
        
        logger.warning("Port-forward was started but connection failed.")
        return None
    except Exception as e:
        logger.error(f"Failed to launch kubectl port-forward: {e}")
        return None

def resolve_db_url(env: str) -> str:
    """Determine the best DB URL to use by probing reachability."""
    user, password = _get_k3s_credentials()
    potential_urls = []
    
    if env in ("auto", "local"):
        potential_urls.append(("local", LOCAL_DB_URL))
        potential_urls.append(("localhost-k3s-creds", f"postgresql://{user}:{password}@localhost:5432/{K3S_PG_DB}"))
    
    if env in ("auto", "k3s"):
        k3s_url = _get_k3s_db_url(user, password)
        if k3s_url:
            potential_urls.append(("k3s-cluster", k3s_url))

    # 1. Probe established options
    for label, url in potential_urls:
        try:
            conn = psycopg2.connect(url, connect_timeout=1)
            conn.close()
            logger.info(f"Connected to database via {label}")
            return url
        except Exception:
            continue
    
    # 2. If nothing works and we are in auto/k3s, try to establish port-forward
    if env in ("auto", "k3s"):
        url = _ensure_port_forward(user, password)
        if url: return url
        
    # 3. Last stand fallback
    if env == "local": return LOCAL_DB_URL
    if env == "k3s": 
        url = _get_k3s_db_url(user, password)
        if url: return url
        
    logger.error("All connection attempts failed including automatic port-forwarding.")
    return None

def extract_meta(path: Path):
    """Extract class name and basic metadata from the strategy file."""
    try:
        content = path.read_text(encoding='utf-8')
        
        # Class Name
        match = re.search(r"class\s+(\w+)\s*\(\s*IStrategy", content)
        if not match: return None, None
        class_name = match.group(1)
        
        # Timeframe
        tf_match = re.search(r"timeframe\s*[:=]\s*['\"]([^'\"]+)['\"]", content)
        timeframe = tf_match.group(1) if tf_match else "5m"
        
        # Stoploss
        sl_match = re.search(r"stoploss\s*[:=]\s*(-?\d*\.?\d+)", content)
        stoploss = float(sl_match.group(1)) if sl_match else -0.1
        
        return class_name, {
            "timeframe": timeframe,
            "stoploss": stoploss,
            "code": content
        }
    except Exception as e:
        logger.error(f"Failed to parse {path}: {e}")
        return None, None

def sync_strategy(strategy_name: str, db_url: str, export_path: str = None):
    # 1. Connect to DB
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
        
    # 2. Check for existence in market_strategies
    cur.execute("SELECT id, name, strategy_code FROM market_strategies WHERE strategy_class_name = %s", (strategy_name,))
    row = cur.fetchone()
    
    if not row:
        logger.error(f"Strategy {strategy_name} not found in market_strategies. You might need to import it first.")
        conn.close()
        return False
        
    strat_id, display_name, db_code = row

    # --- Mode: Export ---
    if export_path:
        try:
            target_path = Path(export_path)
            target_path.write_text(db_code or "", encoding='utf-8')
            logger.info(f"[✓] Exported database version of {strategy_name} to {target_path}")
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to export code: {e}")
            conn.close()
            return False

    # --- Mode: Sync (Push) ---
    # Final the strategy file
    search_paths = [
        Path(f"strategies/{strategy_name}/{strategy_name}.py"),
        Path(f"strategies/{strategy_name}.py"),
        Path(f"user_data/strategies/{strategy_name}.py")
    ]
    
    strat_file = None
    for p in search_paths:
        if p.exists():
            strat_file = p
            break
            
    if not strat_file:
        logger.error(f"Could not find local strategy script for {strategy_name}")
        conn.close()
        return False
        
    logger.info(f"Found local strategy file: {strat_file}")
    class_name, meta = extract_meta(strat_file)
    if not class_name:
        logger.error(f"Could not identify a Freqtrade strategy class in {strat_file}")
        conn.close()
        return False
        
    # 4. Update the code
    try:
        cur.execute("""
            UPDATE market_strategies SET 
                strategy_code = %s,
                updated_at = %s
            WHERE id = %s
        """, (meta['code'], datetime.now(timezone.utc), strat_id))
        
        conn.commit()
        logger.info(f"[✓] Successfully updated code for {display_name} ({class_name}) in database.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Update failed: {e}")
        return False
    finally:
        conn.close()
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Sync or Export strategy code to/from marketxpress database")
    parser.add_argument("--strategy", required=True, help="Name of the strategy class or file")
    parser.add_argument("--env", default="auto", choices=["auto", "local", "k3s"], help="Database environment")
    parser.add_argument("--export", help="Path to save the strategy code from database (e.g. Stinkfist_db.py)")
    args = parser.parse_args()
    
    db_url = resolve_db_url(args.env)
    if not db_url:
        logger.error("No database connection available.")
        return
        
    sync_strategy(args.strategy, db_url, export_path=args.export)

if __name__ == "__main__":
    main()
