#!/usr/bin/env python3
import os
import json
import subprocess
import argparse
from datetime import datetime, timedelta


def get_timerange(period: str) -> str:
    now = datetime.now()
    if period == "2025_year":
        return "20250101-20251231"
    elif period == "last_1_week":
        start = now - timedelta(days=7)
    elif period == "last_1_month":
        start = now - timedelta(days=30)
    elif period == "last_3_months":
        start = now - timedelta(days=90)
    elif period == "last_6_months":
        start = now - timedelta(days=180)
    else:
        raise ValueError(f"Unknown period: {period}")
    return f"{start.strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"


def main():
    parser = argparse.ArgumentParser(description="Run Batched Freqtrade Backtests")
    parser.add_argument(
        "--period",
        required=True,
        choices=[
            "2025_year",
            "last_1_week",
            "last_1_month",
            "last_3_months",
            "last_6_months",
        ],
    )
    parser.add_argument("--batch", type=int, required=True, help="Batch ID (1-indexed)")
    parser.add_argument(
        "--total-batches", type=int, required=True, help="Total number of batches"
    )
    parser.add_argument("--docker", action="store_true", help="Use Docker mode")
    parser.add_argument(
        "--docker-image", default="neozhou2009/freqtrade-full:latest", help="Docker image"
    )
    parser.add_argument(
        "--skip-errors", action="store_true", help="Skip strategies with errors"
    )
    parser.add_argument(
        "--strategy",
        help="Run a single specific strategy (overrides batch selectors)",
        default=None,
    )
    args = parser.parse_args()

    timerange = get_timerange(args.period)
    print(f"[*] Timerange for {args.period}: {timerange}")

    registry_file = "strategy_registry.json"
    if not os.path.exists(registry_file):
        print(
            "[!] strategy_registry.json not found! Run: python scripts/classify_strategies.py"
        )
        return

    with open(registry_file, "r") as f:
        registry = json.load(f)

    if args.strategy:
        batch_strats = [args.strategy]
    else:
        strategies = sorted(list(registry.keys()))
        total_strats = len(strategies)
        batch_size = (total_strats + args.total_batches - 1) // args.total_batches
        start_idx = (args.batch - 1) * batch_size
        end_idx = min(start_idx + batch_size, total_strats)

        batch_strats = strategies[start_idx:end_idx]

    if not batch_strats:
        print("[*] No strategies in this batch. Exiting.")
        return

    print(
        f"[*] Batch {args.batch}/{args.total_batches}: Running {len(batch_strats)} strategies..."
    )

    project_root = os.getcwd()
    test_dir = os.path.join(project_root, "test")

    if not os.path.exists(test_dir):
        print(f"[!] Test directory not found: {test_dir}")
        return

    if not os.path.exists(os.path.join(test_dir, "config.json")):
        print(f"[!] Config not found: {test_dir}/config.json")
        return

    if args.skip_errors:
        run_strategies_individually(args, batch_strats, test_dir, timerange)
    else:
        run_strategies_batch(args, batch_strats, test_dir, timerange)


def run_strategies_batch(args, batch_strats, test_dir, timerange):
    """Run all strategies in a single batch."""
    if args.docker:
        print(f"[*] Using Docker mode with image: {args.docker_image}")
        cmd = (
            [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{test_dir}:/work/freqtrade_test",
                args.docker_image,
                "backtesting",
                "--userdir",
                "/work/freqtrade_test/user_data",
                "--strategy-list",
            ]
            + batch_strats
            + [
                "--timerange",
                timerange,
                "--config",
                "/work/freqtrade_test/config.json",
                "--max-open-trades",
                "3",
                "--stake-amount",
                "100",
                "--dry-run-wallet",
                "10000",
            ]
        )
    else:
        print("[*] Using native freqtrade")
        cmd = (
            ["freqtrade", "backtesting", "--strategy-list"]
            + batch_strats
            + [
                "--timerange",
                timerange,
                "--config",
                os.path.join(test_dir, "config.json"),
            ]
        )

    print(f"[*] Executing Command:\n{' '.join(cmd)}")

    result = subprocess.run(cmd, env=os.environ.copy())

    if result.returncode != 0:
        print(f"[!] Freqtrade returned non-zero exit code: {result.returncode}")
    else:
        print(f"[*] Backtest completed for batch {args.batch}")


def run_strategies_individually(args, batch_strats, test_dir, timerange):
    """Run each strategy individually, skipping errors."""
    success_count = 0
    fail_count = 0
    failed_strategies = []

    for strategy in batch_strats:
        print(f"\n[*] Testing strategy: {strategy}")

        if args.docker:
            cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{test_dir}:/work/freqtrade_test",
                args.docker_image,
                "backtesting",
                "--userdir",
                "/work/freqtrade_test/user_data",
                "--strategy",
                strategy,
                "--timerange",
                timerange,
                "--config",
                "/work/freqtrade_test/config.json",
                "--max-open-trades",
                "3",
                "--stake-amount",
                "100",
                "--dry-run-wallet",
                "10000",
            ]
        else:
            cmd = [
                "freqtrade",
                "backtesting",
                "--strategy",
                strategy,
                "--timerange",
                timerange,
                "--config",
                os.path.join(test_dir, "config.json"),
            ]

        result = subprocess.run(
            cmd, env=os.environ.copy(), capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"  [✗] Failed: {strategy}")
            fail_count += 1
            failed_strategies.append(strategy)
        else:
            print(f"  [✓] Success: {strategy}")
            success_count += 1

    print(f"\n=== Batch {args.batch} Summary ===")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    if failed_strategies:
        print(f"Failed strategies: {', '.join(failed_strategies)}")


if __name__ == "__main__":
    main()
