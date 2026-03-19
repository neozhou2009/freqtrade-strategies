# 策略排行榜：全流程操作手册 (Operations Manual)

本手册提供了从生成策略元数据到最终排行榜产出的全流程终端命令。

## 流程概览
1. [分类] 生成策略注册表
2. [同步] 补全历史数据
3. [环境] 初始化测试目录
4. [运行] 执行批量回测
5. [榜单] 生成最终排行榜

---

## 1. 生成策略注册表 (Registry)
**目标**：扫描 `strategies/` 目录，识别 465 个策略的特征、复杂度与交易方向。
```bash
python scripts/classify_strategies.py
```
*   **产出**：`strategy_registry.json`

## 2. 数据补全与同步 (Data Sync)
**目标**：下载 2025 全年数据，支持 10 种时间框架（1m 至 1d）。
```bash
python scripts/download_data.py --period 2025_year --docker
```
*   **多交易所配置**：
    如果不指定参数，默认下载 `binance` 的 `futures` 数据。如需切换：
    ```bash
    # 下载 Bybit 的现货数据
    python scripts/download_data.py --period 2025_year --exchange bybit --trading-mode spot --docker
    ```

## 2.5 数据完整性自检 (Data Check)
**目标**：验证本地数据是否真正完整覆盖了目标时间段。
```bash
python scripts/check_data_range.py
```
*   **作用**：列出每个币种和每个时间框架的起始记录时间，确保没有数据空洞或覆盖不足。

## 3. 准备回测运行环境 (Flatten Env)
**目标**：将子目录中的策略展平并同步到 `test/` 运行目录。
```bash
python scripts/prepare_test_env.py
```
*   **产出**：`test/user_data/strategies/` 目录下将包含所有可运行的策略。

## 4. 执行批量并行回测 (Execution)
**目标**：调度 Freqtrade 进行大规模分片计算。我们提供了两个层级的方案：

### A. 全量自动化运行 (推荐)
如果您想后台挂起依次自动跑完 1-10 批所有策略，请使用：
```bash
python scripts/run_all_batches.py --period 2025_year --docker
```

### B. 按批次手动调试
如果您想运行特定的一批，并在遇到错误（如策略代码过时）时进行跳过，请加 `--skip-errors` 参数：
```bash
python scripts/run_batch_backtests.py --period 2025_year --batch 1 --total-batches 10 --docker --skip-errors
```
*   `--skip-errors`: 开启后，如果某个策略因报错导致失败，回测将自动跳过它并继续运行接下来的策略。

---

## 5. 生成最终排行榜 (Leaderboard)
**目标**：聚合各批次数据，生成多维度的 Markdown 报表。
```bash
python scripts/generate_leaderboard.py --period "2025年全年回测报告"
```
*   **产出**：
    *   `LEADERBOARD.md`: Markdown 格式排行榜。
    *   `leaderboard.json`: 结构化 JSON 原始数据。

---

## 维护与更新
- **新增策略**：请重新执行 **Step 1** 和 **Step 3**。
- **时间更新**：请重新执行 **Step 2** 补全最新月份的数据。
- **重新跑榜**：请清理 `test/user_data/backtest_results/` 目录后重复 **Step 4** 和 **Step 5**。
