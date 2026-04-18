#!/usr/bin/env python3
"""
VecAlpha 数据覆盖预检工具 (scripts/check_data_coverage.py)

在运行回测流水线之前，检查本地历史行情数据是否覆盖了所需的时间范围。

功能:
  1. 从 user_data/config.json 读取交易所和交易对配置
  2. 扫描 user_data/data/<exchange>/ 目录下的 .feather 数据文件
  3. 通过文件修改时间和文件大小估算数据覆盖天数
  4. 与所需天数对比，输出 ✅/⚠️/❌ 状态报告
  5. 提供缺失时的修复命令

使用:
    python3 scripts/check_data_coverage.py --days 90
    python3 scripts/check_data_coverage.py --days 365 --strict
    python3 scripts/check_data_coverage.py --days 365 --auto-download
"""
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ── 常量 ──────────────────────────────────────────────────────────────────────
# 每个 timeframe 每天的大约 K 线数量
CANDLES_PER_DAY = {
    "1m":  1440,
    "3m":   480,
    "5m":   288,
    "15m":   96,
    "30m":   48,
    "1h":    24,
    "2h":    12,
    "4h":     6,
    "1d":     1,
}

# feather 格式：每行约 40 字节（8列 × 8字节 + 开销）
BYTES_PER_CANDLE = 40

# 需要覆盖的关键交易对和时间框架（用于预检）
KEY_PAIRS = ["BTC/USDT:USDT", "ETH/USDT:USDT"]
KEY_TIMEFRAMES = ["5m", "1h"]

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def load_config(config_path: Path) -> dict:
    """读取 freqtrade config.json"""
    if not config_path.exists():
        return {}
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception:
        return {}


def pair_to_filename(pair: str, timeframe: str, trading_mode: str = "spot") -> list[str]:
    """
    将交易对转换为可能的文件名列表。
    BTC/USDT:USDT + 5m → BTC_USDT_USDT-5m-futures.feather (futures)
                        → BTC_USDT-5m.feather (spot)
    """
    # 规范化交易对名称
    base = pair.replace("/", "_").replace(":", "_").replace("-", "_")
    results = []

    if trading_mode == "futures":
        results.append(f"{base}-{timeframe}-futures.feather")
    else:
        # spot: BTC/USDT → BTC_USDT
        spot_base = pair.split(":")[0].replace("/", "_")
        results.append(f"{spot_base}-{timeframe}.feather")

    return results


def estimate_days_from_file(filepath: Path, timeframe: str) -> float:
    """
    通过文件大小估算数据覆盖的天数。
    公式: 天数 = 文件字节数 / (每天K线数 × 每条K线字节数)
    """
    if not filepath.exists():
        return 0.0
    size_bytes = filepath.stat().st_size
    if size_bytes < 1000:  # 文件过小，忽略
        return 0.0
    candles_per_day = CANDLES_PER_DAY.get(timeframe, 288)
    estimated_candles = size_bytes / BYTES_PER_CANDLE
    return estimated_candles / candles_per_day


def find_data_file(data_dir: Path, exchange: str, pair: str, timeframe: str,
                   trading_mode: str) -> tuple[Path | None, float]:
    """
    搜索数据文件，返回 (文件路径或None, 估算天数)。
    """
    exchange_dir = data_dir / exchange
    filenames = pair_to_filename(pair, timeframe, trading_mode)

    # 根据 trading_mode 决定子目录
    if trading_mode == "futures":
        search_dirs = [exchange_dir / "futures", exchange_dir]
    else:
        search_dirs = [exchange_dir]

    for search_dir in search_dirs:
        for fname in filenames:
            fpath = search_dir / fname
            if fpath.exists():
                days = estimate_days_from_file(fpath, timeframe)
                return fpath, days

    return None, 0.0


def check_last_modified_freshness(filepath: Path, max_stale_hours: int = 48) -> bool:
    """检查文件是否在最近 max_stale_hours 小时内有更新"""
    if not filepath:
        return False
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    age = datetime.now() - mtime
    return age.total_seconds() < max_stale_hours * 3600


# ── 主逻辑 ────────────────────────────────────────────────────────────────────

def run_check(required_days: int, config_path: Path, data_dir: Path,
              strict: bool = False, auto_download: bool = False) -> bool:
    """
    执行数据覆盖预检，返回 True 表示数据充足，False 表示不足。
    """
    print()
    print("═" * 65)
    print(f"  📡 行情数据覆盖预检  (需要 {required_days} 天)")
    print("═" * 65)

    config = load_config(config_path)
    exchange = config.get("exchange", {}).get("name", "binance").lower()
    trading_mode = config.get("trading_mode", "spot").lower()
    configured_pairs = config.get("exchange", {}).get("pair_whitelist", [])

    print(f"  交易所   : {exchange}")
    print(f"  交易模式 : {trading_mode}")
    print(f"  数据目录 : {data_dir / exchange}")
    print()

    # 确定要检查的交易对：config 中的交易对 + 关键对
    check_pairs = list(dict.fromkeys(KEY_PAIRS + configured_pairs[:3]))
    check_tfs = KEY_TIMEFRAMES

    all_ok = True
    missing_pairs = []

    print(f"  {'交易对':<25} {'时间框架':<8} {'覆盖天数':>8}  {'状态'}")
    print("  " + "─" * 58)

    for pair in check_pairs:
        for tf in check_tfs:
            fpath, days = find_data_file(data_dir, exchange, pair, tf, trading_mode)

            if fpath is None:
                status = "❌ 文件不存在"
                icon = "❌"
                all_ok = False
                missing_pairs.append((pair, tf))
            elif days < required_days * 0.8:
                status = f"⚠️  不足 (估算仅 {days:.0f} 天)"
                icon = "⚠️ "
                if strict:
                    all_ok = False
                missing_pairs.append((pair, tf))
            else:
                status = f"✅ 充足"
                icon = "✅"

            pair_short = pair.replace(":USDT", "")
            print(f"  {pair_short:<25} {tf:<8} {days:>8.0f}天  {status}")

    print("  " + "─" * 58)

    if all_ok:
        print()
        print("  ✅ 数据检查通过！可以开始回测。")
        print("═" * 65)
        print()
        return True
    else:
        print()
        print(f"  ⚠️  发现数据不足，需要至少 {required_days} 天历史数据。")
        print()

        # 生成修复命令
        download_cmd = (
            f"freqtrade download-data \\\n"
            f"    --config user_data/config.json \\\n"
            f"    --timeframe 5m 15m 1h 1d \\\n"
            f"    --days {required_days + 30}"
        )

        print("  修复方法：运行以下命令下载历史数据：")
        print()
        print("  " + download_cmd.replace("\n", "\n  "))
        print()

        if auto_download:
            print("  🔄 --auto-download 已启用，正在自动下载数据...")
            print()
            cmd = [
                "freqtrade", "download-data",
                "--config", str(config_path),
                "--timeframe", "5m", "15m", "1h", "1d",
                "--days", str(required_days + 30),
            ]
            result = subprocess.run(cmd, cwd=str(data_dir.parent.parent))
            if result.returncode == 0:
                print()
                print("  ✅ 数据下载完成！")
                all_ok = True
            else:
                print()
                print("  ❌ 数据下载失败，请手动运行上方命令。")
                all_ok = False
        else:
            print("  提示: 加 --auto-download 参数可自动触发下载。")

        print("═" * 65)
        print()
        return all_ok


def main():
    parser = argparse.ArgumentParser(
        description="VecAlpha 数据覆盖预检：在回测前验证历史行情数据是否足够",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="需要的历史数据天数（默认: 30）",
    )
    parser.add_argument(
        "--config",
        default="user_data/config.json",
        help="freqtrade config 文件路径（默认: user_data/config.json）",
    )
    parser.add_argument(
        "--data-dir",
        default="user_data/data",
        help="数据目录路径（默认: user_data/data）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：数据不足也视为失败（默认允许 20%% 误差）",
    )
    parser.add_argument(
        "--auto-download",
        action="store_true",
        help="数据不足时自动运行 freqtrade download-data",
    )
    args = parser.parse_args()

    # 路径解析
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent

    def resolve(p):
        return Path(p) if Path(p).is_absolute() else project_root / p

    ok = run_check(
        required_days=args.days,
        config_path=resolve(args.config),
        data_dir=resolve(args.data_dir),
        strict=args.strict,
        auto_download=args.auto_download,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
