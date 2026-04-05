#!/usr/bin/env python3
import os
import json
import subprocess
import argparse
import re
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
    elif period == "last_1_year":
        start = now - timedelta(days=365)
    else:
        raise ValueError(f"Unknown period: {period}")
    return f"{start.strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"


def get_strategy_timeframe(
    strategy_name: str, registry: dict, strategies_dir: str
) -> str:
    """Detect timeframe for a strategy, prioritizing registry then file inspection."""
    # Try registry first
    if strategy_name in registry and "timeframe" in registry[strategy_name]:
        tf = registry[strategy_name]["timeframe"]
        if tf:
            return tf

    # Fallback: inspect the strategy file
    strategies_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.pardir, strategies_dir
    )
    for ext in ("", ".py"):
        filepath = os.path.join(strategies_dir, strategy_name + ext)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            # Match timeframe = "5m" or timeframe = '5m'
            match = re.search(r"timeframe\s*=\s*[\"']([^\"']+)[\"']", content)
            if match:
                return match.group(1)

    # Ultimate fallback
    return "5m"


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
            "last_1_year",
        ],
    )
    parser.add_argument(
        "--batch", type=int, required=False, help="Batch ID (1-indexed)"
    )
    parser.add_argument(
        "--total-batches", type=int, required=False, help="Total number of batches"
    )
    import shutil
    has_freqtrade = shutil.which("freqtrade") is not None

    parser.add_argument("--docker", action="store_true", default=not has_freqtrade, help="Use Docker mode")
    parser.add_argument(
        "--docker-image",
        default="neozhou2009/freqtrade-full:latest",
        help="Docker image",
    )
    parser.add_argument(
        "--skip-errors", action="store_true", help="Skip strategies with errors"
    )
    parser.add_argument(
        "--strategy",
        help="Run a single specific strategy (overrides batch selectors)",
        default=None,
    )
    parser.add_argument(
        "--timeframe",
        "-t",
        help="Timeframe for batch mode (ignored in --skip-errors mode, per-strategy timeframe is used)",
        default="5m",
    )
    args = parser.parse_args()

    timerange = get_timerange(args.period)
    print(f"[*] Timerange for {args.period}: {timerange}")

    if args.strategy is None and (args.batch is None or args.total_batches is None):
        raise ValueError(
            "--batch and --total-batches are required unless --strategy is specified"
        )

    # Allow running from any current working directory by resolving repo root
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, os.pardir))

    registry_file = os.path.join(repo_root, "strategy_registry.json")
    registry = {}
    if os.path.exists(registry_file):
        with open(registry_file, "r") as f:
            registry = json.load(f)

    if args.strategy:
        batch_strats = [args.strategy]
    else:
        strategies = sorted(list(registry.keys()))
        excluded = [s for s in strategies if registry.get(s, {}).get("excluded")]
        strategies = [s for s in strategies if not registry.get(s, {}).get("excluded")]
        if excluded:
            print(
                f"[*] Skipping {len(excluded)} excluded strategies: {', '.join(sorted(excluded))}"
            )
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

    project_root = repo_root
    test_dir = os.path.join(project_root, "test")

    if not os.path.exists(test_dir):
        print(f"[!] Test directory not found: {test_dir}")
        return

    if not os.path.exists(os.path.join(test_dir, "config.json")):
        print(f"[!] Config not found: {test_dir}/config.json")
        return

    if args.skip_errors:
        run_strategies_individually(args, batch_strats, test_dir, timerange, registry)
    else:
        run_strategies_batch(args, batch_strats, test_dir, timerange)


def run_strategies_batch(args, batch_strats, test_dir, timerange):
    """Run all strategies in a single batch (shared timeframe for all)."""
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
                "--timeframe",
                args.timeframe,
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
                "--timeframe",
                args.timeframe,
                "--config",
                os.path.join(test_dir, "config.json"),
            ]
        )

    print(f"[*] Executing Command:\n{' '.join(cmd)}")

    result = subprocess.run(cmd, env=os.environ.copy())

    if result.returncode != 0:
        print(f"[!] Freqtrade returned non-zero exit code: {result.returncode}")
        print(result.stdout)
        print(result.stderr)
    else:
        print(f"[*] Backtest completed for batch {args.batch}")


def run_strategies_individually(args, batch_strats, test_dir, timerange, registry):
    """Run each strategy individually, skipping errors. Uses per-strategy timeframe."""
    success_count = 0
    fail_count = 0
    failed_strategies = []

    strategies_dir = "test/user_data/strategies"

    for strategy in batch_strats:
        timeframe = get_strategy_timeframe(strategy, registry, strategies_dir)
        print(f"\n[*] Testing strategy: {strategy} (timeframe: {timeframe})")

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
                "--timeframe",
                timeframe,
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
                "--timeframe",
                timeframe,
                "--config",
                os.path.join(test_dir, "config.json"),
            ]

        result = subprocess.run(
            cmd, env=os.environ.copy(), capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"  [✗] Failed: {strategy}")
            print(result.stdout[-1000:] if result.stdout else "(no stdout)")
            print(result.stderr[-500:] if result.stderr else "(no stderr)")
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
