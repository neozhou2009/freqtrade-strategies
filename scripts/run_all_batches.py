#!/usr/bin/env python3
"""
Run all batches for complete backtesting
"""

import subprocess
import sys

TOTAL_BATCHES = 10
PERIOD = "2025_year"


def main():
    print(f"=== Running all {TOTAL_BATCHES} batches ===")
    print(f"Period: {PERIOD}")
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
            PERIOD,
            "--batch",
            str(batch),
            "--total-batches",
            str(TOTAL_BATCHES),
            "--docker",
        ]

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

    print(f"\nRunning: python scripts/generate_leaderboard.py --period {PERIOD}")
    subprocess.run(["python", "scripts/generate_leaderboard.py", "--period", PERIOD])

    print("\nDone! Check LEADERBOARD.md for results.")


if __name__ == "__main__":
    main()
