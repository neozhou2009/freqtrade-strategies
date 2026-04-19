#!/bin/bash
# ==============================================================================
# VecAlpha 全时段排行榜自动化更新脚本
#
# 用法:
#   ./scripts/auto_update_all_periods.sh --all                   # 运行全部 5 个时段
#   ./scripts/auto_update_all_periods.sh --daily                 # 每日快更: 仅 1w + 1m
#   ./scripts/auto_update_all_periods.sh --period 1w             # 单独跑 1 周
#   ./scripts/auto_update_all_periods.sh --period 3m             # 单独跑 3 个月
#   ./scripts/auto_update_all_periods.sh --period 6m --limit 10  # 只跑前 10 个策略（测试用）
#   ./scripts/auto_update_all_periods.sh --all --limit 50        # 全时段只跑前 50 个策略
#
# 参数:
#   --period <时段>  单独运行指定时段 (1w, 1m, 3m, 6m, 1y)
#   --all            运行全部 5 个时段
#   --daily          仅更新 1w + 1m
#   --limit <N>      限制每个时段只测试前 N 个策略（默认: 100，0=全部）
#   --workers <N>    并行进程数（默认: 4）
# ==============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# ── 默认参数 ──────────────────────────────────────────────────────────────────
LIMIT=100
WORKERS=4
MODE_VECSCORE=fast   # fast=快速估算(默认), full=完整多时段回测(精度高)

# ── 日志函数 ──────────────────────────────────────────────────────────────────
log()  { echo -e "\033[1;32m[$(date +'%Y-%m-%d %H:%M:%S')] $1\033[0m"; }
warn() { echo -e "\033[1;33m[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $1\033[0m"; }
err()  { echo -e "\033[1;31m[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1\033[0m"; }

# ── 单时段更新函数 ─────────────────────────────────────────────────────────────
update_period() {
    local days=$1
    local suffix=$2
    local period_slug=$3
    local label=$4

    log "══════════════════════════════════════════════════"
    log "  时段: $label  |  回测天数: $days  |  后缀: $suffix  |  策略数: $LIMIT  |  评分模式: $MODE_VECSCORE"
    log "══════════════════════════════════════════════════"

    # Pre-Check: 验证历史行情数据是否覆盖所需天数
    log "Pre-Check: 检查历史行情数据覆盖范围..."
    if ! python3 scripts/check_data_coverage.py --days "$days"; then
        err "历史数据不足，无法运行 $days 天回测。"
        err "请先运行以下命令补充数据，然后重试："
        err "  freqtrade download-data --config user_data/config.json --timeframe 5m 15m 1h 1d --days $((days + 30))"
        exit 1
    fi

    # Step 1: Phase 1 回测 + Phase 2 VecScore 评分
    log "Step 1/3: 回测 + VecScore 评分（模式: $MODE_VECSCORE）..."
    
    local CMD=(
        python3 scripts/run_pipeline.py
        --days "$days"
        --suffix "$suffix"
        --workers "$WORKERS"
        --phase1-limit "$LIMIT"
        --vecscore-mode "$MODE_VECSCORE"
    )
    if [[ -n "$TARGET_STRATEGIES" ]]; then
        CMD+=(--strategies $TARGET_STRATEGIES)
        log "  => 指定策略: $TARGET_STRATEGIES"
    fi

    "${CMD[@]}"

    # Step 2: 生成排行榜 JSON 和 Markdown
    log "Step 2/3: 生成 $label 排行榜文件..."
    python3 scripts/generate_leaderboard.py \
        --vecscore "user_data/vecscore_results_${suffix}.json" \
        --period "$period_slug" \
        --limit "$LIMIT"

    # Step 3: 同步到数据库
    log "Step 3/3: 同步到数据库..."
    python3 scripts/db_sync_leaderboard.py --env auto

    log "✅ $label 更新完成！（共 $LIMIT 个策略）"
    echo ""
}

# ── 时段快捷函数 ───────────────────────────────────────────────────────────────
run_1w()  { update_period 7   "7d"  "last_1_week"    "Last 1 Week"; }
run_1m()  { update_period 30  "30d" "last_1_month"   "Last 1 Month"; }
run_3m()  { update_period 90  "90d" "last_3_months"  "Last 3 Months"; }
run_6m()  { update_period 180 "6m"  "last_6_months"  "Last 6 Months"; }
run_1y()  { update_period 365 "1y"  "last_1_year"    "Last 1 Year"; }

# ── 参数解析 ──────────────────────────────────────────────────────────────────
MODE=""
TARGET=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all|--daily)
            MODE="$1"
            shift
            ;;
        --period)
            MODE="--period"
            TARGET="$2"
            shift 2
            ;;
        --mode)
            MODE_VECSCORE="$2"
            if [[ "$MODE_VECSCORE" != "fast" && "$MODE_VECSCORE" != "full" ]]; then
                err "--mode 只支持 'fast' 或 'full'"
                exit 1
            fi
            shift 2
            ;;
        --strategies|-s)
            TARGET_STRATEGIES="$2"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        --help|-h)
            MODE="--help"
            shift
            ;;
        *)
            err "未知参数: '$1'，使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

# ── 主逻辑 ────────────────────────────────────────────────────────────────────
case "$MODE" in
    --all)
        log "🚀 运行全部时段（1w, 1m, 3m，为节省k8s资源暂时屏蔽 6m 和 1y），每个时段取前 $LIMIT 个策略..."
        run_1w
        run_1m
        run_3m
        # run_6m
        # run_1y
        ;;
    --daily)
        log "📅 每日快更（1w + 1m），每个时段取前 $LIMIT 个策略..."
        run_1w
        run_1m
        ;;
    --period)
        case "$TARGET" in
            "1w"|"7d")   run_1w ;;
            "1m"|"30d")  run_1m ;;
            "3m"|"90d")  run_3m ;;
            "6m"|"180d") run_6m ;;
            "1y"|"365d") run_1y ;;
            *)
                err "无效的时段: '$TARGET'"
                echo "  支持: 1w, 1m, 3m, 6m, 1y"
                exit 1
                ;;
        esac
        ;;
    --help|"")
        echo ""
        echo "  用法: $0 <模式> [选项]"
        echo ""
        echo "  模式:"
        echo "    --all                  运行全部 5 个时段 (1w, 1m, 3m, 6m, 1y)"
        echo "    --daily                每日快更: 仅 1w + 1m"
        echo "    --period <时段>        单独运行指定时段"
        echo ""
        echo "  时段参数 (与 --period 配合使用):"
        echo "    1w / 7d               最近 1 周"
        echo "    1m / 30d              最近 1 个月"
        echo "    3m / 90d              最近 3 个月"
        echo "    6m / 180d             最近 6 个月"
        echo "    1y / 365d             最近 1 年"
        echo ""
        echo "  选项:"
        echo "    --limit <N>           只测试前 N 个策略（默认: 100，0=全部）"
        echo "    --workers <N>         并行进程数（默认: 4）"
        echo "    --mode fast|full      VecScore 评分模式（默认: fast）"
        echo "                          fast = 快速估算，速度快，结果带~标记"
        echo "                          full = 完整多时段回测，精度高但耗时数倍"
        echo "    -s, --strategies      仅测试指定策略，需用引号括起来，如: \"Strat1 Strat2\""
        echo ""
        echo "  示例:"
        echo "    $0 --period 6m -s \"ADXMomentum Apollo11\"         # 指定两个策略跑 6 个月"
        echo "    $0 --period 1y --limit 50 --mode full            # 1y 时段精确模式，前 50 个策略"
        echo "    $0 --daily                                       # 每日更新 1w + 1m（默认 fast）"
        echo "    $0 --all --limit 100 --mode fast                 # 全时段全量运行"
        echo ""
        exit 0
        ;;
    *)
        err "未知模式: '$MODE'，使用 --help 查看帮助"
        exit 1
        ;;
esac

log "🏆 所有指定任务已执行完毕！"
