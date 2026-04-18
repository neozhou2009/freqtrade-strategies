#!/bin/bash
# ==============================================================================
# VecAlpha 策略排行榜自动化更新脚本
# 执行流程：Phase 0 -> Phase 1 -> Phase 2 -> Generate -> DB Sync
# ==============================================================================

set -e # 遇到错误立即停止

# 设置项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 日志输出函数
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "开始排行榜自动化更新任务..."

# 1. 环境准备 (可选：同步代码或下载最新行情)
# log "正在更新行情数据..."
# python3 scripts/download_data.py --days 40

# 2. 运行核心流水线 (Phase 0 -> Phase 2)
# 使用 fast 模式快速扫描，workers 根据 CPU 核心数调整
log "Step 1/3: 运行策略筛选与评分流水线 (Fast Mode)..."
python3 scripts/run_pipeline.py --vecscore-mode fast --workers 4

# 3. 生成排行榜文件
log "Step 2/3: 生成排行榜聚合文件..."
python3 scripts/generate_leaderboard.py --vecscore user_data/vecscore_results.json --period "Last 30 Days"

# 4. 同步至数据库
log "Step 3/3: 同步排行榜数据至数据库..."
# 如果在集群外，env 请根据实际情况设为 local 或 auto
python3 scripts/db_sync_leaderboard.py --env auto

log "任务圆满完成！"
