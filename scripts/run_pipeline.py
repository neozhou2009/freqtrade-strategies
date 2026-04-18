#!/usr/bin/env python3
"""
VecAlpha 策略筛选流水线 - 三阶段一键执行

流程：
  Phase 0 → Phase 1 → Phase 2 → 生成 Leaderboard

用法:
    # 完整流水线（从头开始）
    python scripts/run_pipeline.py

    # 跳过 Phase 0（已有 static_filter_result.json）
    python scripts/run_pipeline.py --skip-phase0

    # 只运行到 Phase 1（回测结果）
    python scripts/run_pipeline.py --stop-after phase1

    # Phase 1 并行加速
    python scripts/run_pipeline.py --workers 4

    # 完整模式评分（多时段稳定性 + Train/Test）
    python scripts/run_pipeline.py --vecscore-mode full

    # 断点续跑 Phase 1
    python scripts/run_pipeline.py --skip-phase0 --resume-phase1
"""

import os
import sys
import json
import time
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# 路径配置
# ──────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
USER_DATA    = PROJECT_ROOT / "user_data"

PHASE0_SCRIPT  = SCRIPT_DIR / "static_filter.py"
PHASE1_SCRIPT  = SCRIPT_DIR / "phase1_quick_backtest.py"
PHASE2_SCRIPT  = SCRIPT_DIR / "vecscore.py"
LEADERBOARD    = SCRIPT_DIR / "generate_leaderboard.py"

# 这些将在 main 中根据 suffix 动态调整
PHASE0_OUTPUT  = USER_DATA / "static_filter_result.json"
PHASE1_OUTPUT  = USER_DATA / "phase1_results.json"
PHASE2_OUTPUT  = USER_DATA / "vecscore_results.json"


# ──────────────────────────────────────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────────────────────────────────────

def banner(title: str):
    width = 68
    print()
    print("╔" + "═" * (width - 2) + "╗")
    print("║" + f" {title}".center(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝")


def run_phase(phase_name: str, cmd: list, capture: bool = False) -> tuple[bool, str]:
    """执行一个阶段脚本，返回 (成功, 输出摘要)"""
    print(f"\n▶ 执行: {' '.join(str(c) for c in cmd)}\n")
    t_start = time.time()
    try:
        if capture:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                env=os.environ.copy(), cwd=str(PROJECT_ROOT)
            )
            output = result.stdout + result.stderr
        else:
            result = subprocess.run(
                cmd, env=os.environ.copy(), cwd=str(PROJECT_ROOT)
            )
            output = ""

        duration = time.time() - t_start
        success = result.returncode == 0

        status = "✅ 完成" if success else "❌ 失败"
        print(f"\n{status}  {phase_name}  ({duration:.1f}s)")
        return success, output

    except KeyboardInterrupt:
        print(f"\n⚠️  {phase_name} 被用户中断")
        return False, ""
    except Exception as e:
        print(f"\n❌ {phase_name} 执行异常: {e}")
        return False, str(e)


def load_json_safe(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def print_summary_table(vecscore_path: Path):
    """读取 vecscore_results.json，打印最终排行榜"""
    if not vecscore_path.exists():
        return
    data = load_json_safe(vecscore_path)
    ranked = data.get("ranked", [])
    if not ranked:
        return

    print()
    print("═" * 72)
    print("🏆 最终策略排行榜（VecScore 降序）")
    print("═" * 72)
    print(f"  {'排名':<4}  {'等级':<5}  {'分数':<7}  {'策略名':<45}  {'商用'}")
    print(f"  {'-'*4}  {'-'*5}  {'-'*7}  {'-'*45}  {'-'*4}")

    grade_icons = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️ ", "D": "❌"}

    for s in ranked[:30]:  # 展示 top 30
        icon = grade_icons.get(s["grade"], "?")
        est = "~" if s.get("is_estimated") else " "
        commercial = "💼" if s.get("commercial_eligible") else "  "
        print(f"  {s['rank']:<4}  {icon} {s['grade']:<3}  {s['vecscore']:>5.1f}{est}  {s['name']:<45}  {commercial}")

    if len(ranked) > 30:
        print(f"  ... 还有 {len(ranked) - 30} 个策略（见 vecscore_results.json）")

    meta = data.get("meta", {})
    dist = meta.get("grade_distribution", {})
    commercial_count = meta.get("commercial_eligible_count", 0)

    print()
    print("📊 等级分布:")
    for g in ["S", "A", "B", "C", "D"]:
        cnt = dist.get(g, 0)
        if cnt > 0:
            bar = "█" * min(cnt, 30)
            print(f"    {g}级: {cnt:3d}  {bar}")

    print(f"\n💼 符合商用资格: {commercial_count} 个策略")

    if meta.get("mode") == "fast":
        print(
            "\n⚠️  注意：当前评分使用快速模式（~）估算，S/T 维度不完整。"
            "\n   重要策略建议用 --vecscore-mode full 精确评分。"
        )


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VecAlpha 策略筛选流水线 - 三阶段一键执行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--skip-phase0",
        action="store_true",
        help="跳过静态预筛（使用已有 static_filter_result.json）",
    )
    parser.add_argument(
        "--skip-phase1",
        action="store_true",
        help="跳过快速回测初筛（使用已有 phase1_results.json）",
    )
    parser.add_argument(
        "--stop-after",
        choices=["phase0", "phase1", "phase2"],
        default=None,
        help="在指定阶段后停止（不继续后续步骤）",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Phase 1 并行工作进程数（默认: 1）",
    )
    parser.add_argument(
        "--resume-phase1",
        action="store_true",
        help="Phase 1 断点续跑（跳过已有结果的策略）",
    )
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="不使用 Docker（需要本地 freqtrade 安装）",
    )
    parser.add_argument(
        "--vecscore-mode",
        choices=["fast", "full"],
        default="fast",
        help="VecScore 评分模式（fast: 估算；full: 完整多时段回测）",
    )
    parser.add_argument(
        "--phase1-limit",
        type=int,
        default=100,
        help="Phase 1 限制策略数（默认: 100，设置为 0 则不限制数据量）",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="回测天数 (默认: 30)",
    )
    parser.add_argument(
        "--strategies",
        nargs="+",
        help="指定仅测试这些策略（会透传给 Phase 1 和 Phase 2），用于针对性测试单个策略",
    )
    parser.add_argument(
        "--suffix",
        default="",
        help="输出文件后缀 (例如 '7d', '1y')，用于区分不同时段的结果",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预演：只检查文件状态，不实际运行任何脚本",
    )

    args = parser.parse_args()

    # Phase 0 静态分析与时段无关，始终使用固定文件名
    # 只有 Phase 1/2 的中间结果才需要按时段隔离
    global PHASE1_OUTPUT, PHASE2_OUTPUT
    if args.suffix:
        s = f"_{args.suffix}"
        PHASE1_OUTPUT = USER_DATA / f"phase1_results{s}.json"
        PHASE2_OUTPUT = USER_DATA / f"vecscore_results{s}.json"

    python_exe = sys.executable

    banner("VecAlpha 策略筛选流水线 v1.0")
    print(f"  项目根目录  : {PROJECT_ROOT}")
    print(f"  开始时间    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  并行工作数  : {args.workers}")
    print(f"  评分模式    : {args.vecscore_mode}")

    pipeline_start = time.time()
    results = {}

    # ═══════════════════════════════════════════════════════
    # Phase 0: 静态代码预筛
    # ═══════════════════════════════════════════════════════
    banner("Phase 0 · 静态代码预筛")

    if args.skip_phase0:
        if PHASE0_OUTPUT.exists():
            data = load_json_safe(PHASE0_OUTPUT)
            meta = data.get("meta", {})
            print(f"⏭️  跳过 Phase 0（使用已有结果）")
            print(f"   文件: {PHASE0_OUTPUT}")
            print(f"   PASS: {meta.get('pass_count', '?')} / ELIMINATED: {meta.get('eliminated_count', '?')}")
            results["phase0"] = True
        else:
            print(f"❌ 找不到 Phase 0 结果文件: {PHASE0_OUTPUT}")
            print("   请先运行 Phase 0，或去掉 --skip-phase0 选项")
            results["phase0"] = False
    else:
        cmd = [python_exe, str(PHASE0_SCRIPT), "--summary-only"]
        if args.dry_run:
            print(f"[预演] 将执行: {' '.join(str(c) for c in cmd)}")
            results["phase0"] = True
        else:
            ok, _ = run_phase("Phase 0 静态预筛", cmd)
            results["phase0"] = ok

    if args.stop_after == "phase0":
        print("\n🛑 --stop-after phase0，流水线在此停止")
        return

    if not results.get("phase0"):
        print("\n❌ Phase 0 失败，中止流水线")
        sys.exit(1)

    # ═══════════════════════════════════════════════════════
    # Phase 1: 快速回测初筛
    # ═══════════════════════════════════════════════════════
    banner("Phase 1 · 30天快速回测初筛")

    if args.skip_phase1:
        if PHASE1_OUTPUT.exists():
            data = load_json_safe(PHASE1_OUTPUT)
            meta = data.get("meta", {})
            print(f"⏭️  跳过 Phase 1（使用已有结果）")
            print(f"   文件: {PHASE1_OUTPUT}")
            print(f"   PASS: {meta.get('pass_count', '?')} / 测试: {meta.get('total_tested', '?')}")
            results["phase1"] = True
        else:
            print(f"❌ 找不到 Phase 1 结果文件: {PHASE1_OUTPUT}")
            results["phase1"] = False
    else:
        # 估算运行时间
        phase0_data = load_json_safe(PHASE0_OUTPUT)
        candidate_count = phase0_data.get("meta", {}).get("pass_count", 312)
        per_strategy_sec = 45  # 每个策略约 45 秒（Docker + 30天数据）
        est_total = candidate_count * per_strategy_sec / max(args.workers, 1)
        print(f"📋 候选策略: {candidate_count} 个")
        print(f"⏱️  预估时间: {est_total/3600:.1f} 小时（{args.workers} 个并行工作进程）")
        print(f"   提示: 可以先用 --phase1-limit 50 测试前 50 个")

        cmd = [python_exe, str(PHASE1_SCRIPT)]
        cmd += ["--days", str(args.days)]
        cmd += ["--output", str(PHASE1_OUTPUT)]          # 显式指定输出路径（含后缀）
        cmd += ["--filter-result", str(PHASE0_OUTPUT)]  # 显式指定 Phase 0 输入
        if args.workers > 1:
            cmd += ["--workers", str(args.workers)]
        if args.resume_phase1:
            cmd += ["--resume"]
        if args.no_docker:
            cmd += ["--no-docker"]
        if args.strategies:
            cmd += ["--strategies"] + args.strategies
        cmd += ["--limit", str(args.phase1_limit)]

        if args.dry_run:
            print(f"[预演] 将执行: {' '.join(str(c) for c in cmd)}")
            results["phase1"] = True
        else:
            ok, _ = run_phase("Phase 1 快速回测", cmd)
            results["phase1"] = ok

    if args.stop_after == "phase1":
        print("\n🛑 --stop-after phase1，流水线在此停止")
        if PHASE1_OUTPUT.exists():
            data = load_json_safe(PHASE1_OUTPUT)
            print(f"\nPhase 1 结果：PASS = {data['meta'].get('pass_count', '?')} 个")
        return

    if not results.get("phase1"):
        print("\n❌ Phase 1 失败，中止流水线")
        sys.exit(1)

    # ═══════════════════════════════════════════════════════
    # Phase 2: VecScore 评分
    # ═══════════════════════════════════════════════════════
    banner("Phase 2 · VecScore 五维评分")

    if not PHASE1_OUTPUT.exists():
        print(f"❌ 找不到 Phase 1 结果文件（已跳过 Phase 1 但文件不存在）")
        results["phase2"] = False
    else:
        phase1_data = load_json_safe(PHASE1_OUTPUT)
        pass_count = len(phase1_data.get("pass_list", []))
        print(f"📋 待评分策略: {pass_count} 个")

        cmd = [
            python_exe, str(PHASE2_SCRIPT),
            "--mode", args.vecscore_mode,
            "--phase1", str(PHASE1_OUTPUT),   # 显式指定输入
            "--output", str(PHASE2_OUTPUT),   # 显式指定输出
        ]
        if args.no_docker:
            cmd += ["--no-docker"]
        if args.strategies:
            cmd += ["--strategies"] + args.strategies

        if args.dry_run:
            print(f"[预演] 将执行: {' '.join(str(c) for c in cmd)}")
            results["phase2"] = True
        else:
            ok, _ = run_phase("Phase 2 VecScore", cmd)
            results["phase2"] = ok

    if not results.get("phase2"):
        print("\n❌ Phase 2 失败，中止流水线")
        sys.exit(1)

    if args.stop_after == "phase2":
        print("\n🛑 --stop-after phase2，流水线在此停止")

    # ═══════════════════════════════════════════════════════
    # 最终汇总
    # ═══════════════════════════════════════════════════════
    pipeline_time = time.time() - pipeline_start
    banner("流水线执行完成")
    print(f"  总耗时: {pipeline_time/60:.1f} 分钟")
    print()
    print("  阶段状态:")
    for phase, ok in results.items():
        icon = "✅" if ok else "❌"
        print(f"    {icon} {phase}")

    # 打印最终排行榜
    if results.get("phase2"):
        print_summary_table(PHASE2_OUTPUT)

    print()
    print("📁 输出文件:")
    for label, path in [
        ("Phase 0 预筛结果", PHASE0_OUTPUT),
        ("Phase 1 回测结果", PHASE1_OUTPUT),
        ("Phase 2 VecScore", PHASE2_OUTPUT),
    ]:
        exists = "✅" if path.exists() else "❌ (未生成)"
        print(f"    {exists}  {label}: {path.relative_to(PROJECT_ROOT)}")

    print()
    print("🔜 下一步：将生成的评分记录同步到排行榜")
    print(f"   运行: python scripts/generate_leaderboard.py --vecscore {PHASE2_OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
