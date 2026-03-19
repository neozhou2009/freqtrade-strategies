#!/usr/bin/env python3
"""
Freqtrade 数据自动补全脚本 (download_data.py)
--------------------------------------------
该脚本旨在简化历史 K 线数据的同步流程。它会自动读取配置，计算缓冲时间，
并根据您的策略需求补全所有必要的时间频率。

主要参数说明:
  --period: 下载周期 (2025_year, last_1_month, last_3_months, last_6_months)
  --docker: 使用 Docker 模式运行 (推荐)
  --erase:  擦除旧数据并重新下载 (确保数据最纯净，无空洞)
  --timeframes: 可选，指定要下载的时间频率（默认为全部 10 种常用的）

示例:
  python scripts/download_data.py --period 2025_year --docker
"""

import os
import json
import subprocess
import argparse
from datetime import datetime, timedelta

def get_timerange(period: str) -> str:
    now = datetime.now()
    if period == "2025_year":
        # 2025 全年，外加前后各 15 天缓冲区
        return "20241215-20260115"
    elif period == "last_1_week":
        start = now - timedelta(days=7 + 2)
    elif period == "last_1_month":
        start = now - timedelta(days=30 + 5)
    elif period == "last_3_months":
        start = now - timedelta(days=90 + 10)
    elif period == "last_6_months":
        start = now - timedelta(days=180 + 15)
    else:
        raise ValueError(f"Unknown period: {period}")
    return f"{start.strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"

def main():
    parser = argparse.ArgumentParser(description="Freqtrade Data Sync Helper")
    parser.add_argument(
        "--period", 
        required=True, 
        choices=["2025_year", "last_1_week", "last_1_month", "last_3_months", "last_6_months"],
        help="下载周期"
    )
    parser.add_argument("--docker", action="store_true", help="使用 Docker 模式")
    parser.add_argument(
        "--docker-image", 
        default="neozhou2009/freqtrade-full:latest", 
        help="Docker 镜像名称"
    )
    parser.add_argument("--erase", action="store_true", help="擦除已存在的本地数据并重新下载")
    parser.add_argument(
        "--timeframes", 
        nargs='+', 
        default=["1m", "3m", "5m", "15m", "30m", "1h", "4h", "6h", "12h", "1d"],
        help="要下载的时间频率列表 (默认下载 10 种)"
    )
    parser.add_argument("--exchange", default="binance", help="交易所名称 (如 binance, gate, bybit)")
    parser.add_argument("--trading-mode", default="futures", choices=["spot", "futures", "margin"], help="交易模式")
    
    args = parser.parse_args()
    
    project_root = os.getcwd()
    config_path = os.path.join(project_root, "user_data", "config.json")
    
    if not os.path.exists(config_path):
        print(f"[!] 找不到配置文件: {config_path}")
        return

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"[!] 无法读取配置文件: {e}")
        return
    
    pairs = config.get("exchange", {}).get("pair_whitelist", [])
    if not pairs:
        print("[!] config.json 的 pair_whitelist 中未发现交易对")
        return
        
    timerange = get_timerange(args.period)
    
    print("\n" + "="*50)
    print(f"[*] 准备启动数据下载")
    print(f"[*] 交易对数量: {len(pairs)}")
    print(f"[*] 时间段范围: {timerange}")
    print(f"[*] 时间频率　: {', '.join(args.timeframes)}")
    print(f"[*] 运行模式　: {'Docker (' + args.docker_image + ')' if args.docker else 'Native'}")
    print("="*50 + "\n")

    base_cmd = ["download-data", "--exchange", args.exchange, "--trading-mode", args.trading_mode]
    base_cmd += ["--timerange", timerange]
    base_cmd += ["--data-format-ohlcv", "feather"]
    # Freqtrade 2026.2+ 会根据 --trading-mode futures 自动下载 funding_rate 和 mark
    
    if args.erase:
        base_cmd.append("--erase")
    
    if args.docker:
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{project_root}/user_data:/freqtrade/user_data",
            args.docker_image
        ] + base_cmd
    else:
        cmd = ["freqtrade"] + base_cmd
        
    cmd += ["--pairs"] + pairs
    cmd += ["--timeframes"] + args.timeframes

    print(f"[*] 执行命令:\n{' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n[✓] 数据同步完成！")
    except FileNotFoundError:
        print("\n[!] 错误: 找不到 'freqtrade' 命令。")
        print("[*] 提示: 您的本地环境似乎没有安装 Freqtrade，请尝试增加 '--docker' 参数来使用 Docker 镜像运行。")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] 同步失败。Exit code: {e.returncode}")
    except Exception as e:
        print(f"\n[!] 发生错误: {e}")

if __name__ == "__main__":
    main()
