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
        ],
        help="Timeframe period for the backtests"
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        default=False,
        help="Use Docker mode (passed through to run_batch_backtests.py)"
    )
    parser.add_argument(
        "--docker-image",
        default="neozhou2009/freqtrade-full:latest",
        help="Docker image to use (passed through to run_batch_backtests.py)"
    )
    args = parser.parse_args()
    period = args.period

    print(f"=== Running all {TOTAL_BATCHES} batches ===")
    print(f"Period: {period}")
    print()

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
