#!/usr/bin/env python3
"""
Run all batches for complete backtesting
"""

import subprocess
import argparse

TOTAL_BATCHES = 10

def main():
    parser = argparse.ArgumentParser(description="Run all batches for complete backtesting")
    parser.add_argument(
        "--period",
        required=False,
        default="2025_year",
        choices=[
            "2025_year",
            "last_1_week",
            "last_1_month",
            "last_3_months",
            "last_6_months",
            "last_1_year",
        ],
        help="Timeframe period for the backtests"
    )
    # Auto-detect if freqtrade binary is in path
    import shutil
    has_freqtrade = shutil.which("freqtrade") is not None

    parser.add_argument(
        "--docker",
        action="store_true",
        default=not has_freqtrade,
        help="Use Docker mode (defaulted to True if 'freqtrade' binary is not found)"
    )
    parser.add_argument(
        "--docker-image",
        default="neozhou2009/freqtrade-full:latest",
        help="Docker image to use (passed through to run_batch_backtests.py)"
    )
    parser.add_argument(
        "--skip-errors",
        action="store_true",
        default=True,
        help="Run each strategy individually and skip those with errors (default: True)"
    )
    parser.add_argument(
        "--no-skip-errors",
        dest="skip_errors",
        action="store_false",
        help="Run all strategies in a single batch call (faster, but one error aborts the whole batch)"
    )
    args = parser.parse_args()
    period = args.period

    print(f"=== Running all {TOTAL_BATCHES} batches ===")
    print(f"Period: {period}")
    print(f"Skip errors: {args.skip_errors} (each strategy runs individually when True)")
    print()

    # Step 1: Data Check & Download
    print("[*] Step 1: Ensuring backtest data is available...")
    from datetime import datetime, timedelta
    
    # Calculate timerange (matching run_batch_backtests logic)
    now = datetime.now()
    if period == "2025_year":
        timerange = "20250101-20251231"
    elif period == "last_1_week":
        timerange = f"{(now - timedelta(days=7)).strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"
    elif period == "last_1_month":
        timerange = f"{(now - timedelta(days=30)).strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"
    elif period == "last_3_months":
        timerange = f"{(now - timedelta(days=90)).strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"
    elif period == "last_6_months":
        timerange = f"{(now - timedelta(days=180)).strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"
    elif period == "last_1_year":
        timerange = f"{(now - timedelta(days=365)).strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"
    
    import os
    test_dir = os.path.abspath("test")
    
    # Download data command (Common timeframes used in registry)
    download_cmd = [
        "docker", "run", "--rm",
        "-v", f"{test_dir}:/work/freqtrade_test",
        args.docker_image,
        "download-data",
        "--userdir", "/work/freqtrade_test/user_data",
        "--config", "/work/freqtrade_test/config.json",
        "--timerange", timerange,
        "-t", "5m", "15m", "1h", "4h", "1d",
        "--trading-mode", "futures"
    ]
    
    print(f"[*] Executing Data Download:\n{' '.join(download_cmd)}")
    download_res = subprocess.run(download_cmd)
    if download_res.returncode != 0:
        print("[!] Data download failed or was interrupted. Proceeding with existing data...")
    else:
        print("[✓] Data check/download completed.")

    print(f"\n[*] Step 2: Running {TOTAL_BATCHES} backtest batches...")

    success_batches = []
    failed_batches = []

    for batch in range(1, TOTAL_BATCHES + 1):
        print(f"\n{'=' * 50}")
        print(f"Batch {batch}/{TOTAL_BATCHES}")
        print(f"{'=' * 50}")

        cmd = [
            "python",
            "scripts/run_batch_backtests.py",
            "--period",
            period,
            "--batch",
            str(batch),
            "--total-batches",
            str(TOTAL_BATCHES),
        ]
        if args.docker:
            cmd += ["--docker", "--docker-image", args.docker_image]
        if args.skip_errors:
            cmd += ["--skip-errors"]

        result = subprocess.run(cmd)

        if result.returncode == 0:
            success_batches.append(batch)
            print(f"[✓] Batch {batch} completed successfully")
        else:
            failed_batches.append(batch)
            print(f"[✗] Batch {batch} had errors (continuing...)")

    print(f"\n{'=' * 50}")
    print("FINAL SUMMARY")
    print(f"{'=' * 50}")
    print(f"Successful batches: {len(success_batches)}/{TOTAL_BATCHES}")
    print(f"Failed batches: {len(failed_batches)}/{TOTAL_BATCHES}")

    if failed_batches:
        print(f"Failed batch numbers: {failed_batches}")

    print(f"\nRunning: python scripts/generate_leaderboard.py --period {period}")
    subprocess.run(["python", "scripts/generate_leaderboard.py", "--period", period])

    print("\nDone! Check LEADERBOARD.md for results.")

if __name__ == "__main__":
    main()
