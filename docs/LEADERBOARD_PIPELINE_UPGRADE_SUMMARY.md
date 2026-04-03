# 策略排行榜 UI 设计与后端数据管道升级总结

## 1. 对话背景与目标
本次对话围绕量化策略排行榜（Strategy Leaderboard）的界面设计展开。核心目标是评估现有的 UI 设计稿，并改造现有的 Freqtrade 回测数据脚本，使其能够输出符合 UI 需求的高维度商业数据。

## 2. UI 设计评估与建议
针对用户提供的排行榜设计图，评估结果如下：
*   **优点**：布局逻辑清晰（左侧筛选、顶部统计、右侧列表）、核心指标均衡（年化收益、夏普、回撤、胜率）、视觉层级分明。
*   **改进建议**：
    *   **迷你资金曲线 (Sparkline)**：将“趋势”列升级为资产净值走势图，比起单纯的排名升降更直观稳定。
    *   **最大回撤 %**：明确显示回撤百分比而非绝对值，方便跨策略对比风险。
    *   **实盘/回测标注**：增加策略可信度标签（如：[实盘 60天] / [回测]）。

## 3. 数据管道差距分析 (Gap Analysis)
在改造前，现有的 `scripts/generate_leaderboard.py` 与 UI 需求之间存在以下差距：
*   **缺项**：极度匮乏“综合评分”模型（0-100分）。
*   **漏采指标**：未提取 CAGR（年化复合收益）、最大回撤百分比、Sortino/Calmar 等风险调整收益指标。
*   **历史追踪**：完全没有跨周期的排名变动追踪能力。

## 4. 实施的改造方案

### 4.1. 综合评分系统 (Composite Scoring Algorithm)
引入了全新的 scoring 逻辑，评分区间 0–100，加权项如下：
- **CAGR (40分)**：年化复合收益率，对盈利能力的核心评估。
- **Sharpe Ratio (25分)**：衡量每承担一单位风险所获得的超额回报。
- **Max Drawdown Penalty (20分)**：最大回撤风险惩罚，>50% 回撤得0分。
- **Win Rate (10分)**：反映策略在胜率方面的稳健性。
- **Trades (5分)**：基于交易频次的数据统计显著性评分。

### 4.2. 脚本架构升级 (`scripts/generate_leaderboard.py`)
*   **全指标提取**：现在能从 Freqtrade JSON 中自动扫入 `cagr`, `max_drawdown_pct`, `sortino`, `calmar`, `profit_factor`。
*   **历史快照机制**：引入 `history.json` 自动记录排名变化，从而支持 UI 中的“排名变动趋势”列。
*   **聚合摘要**：增加了 `summary` 字段，提供所有策略的平均分、平均收益等全盘宏观数据。

## 5. 业务数据目录规划
为了保持项目根目录的整洁，将业务生成的非元数据文件从根目录移出：
*   **数据目录**：建议设为 `user_data/leaderboard/`。
*   **受影响文件**：
    *   `user_data/leaderboard/leaderboard.json` (前端 API 源)
    *   `user_data/leaderboard/LEADERBOARD.md` (阅读报告)
    *   `user_data/leaderboard/history.json` (自动排名历史)

## 6. 使用说明
使用新版本管道只需一步命令：
```bash
python scripts/generate_leaderboard.py --input-dir <数据路径> --period <时期标识>
```
脚本会自动处理评分、排名变动计算及目录生成。

---
**文档生成时间**：2026-04-02 17:15
**状态**：P0 核心改动已上线，已支持前端 V1 版本 API 需求。
