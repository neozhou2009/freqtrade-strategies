# VecAlpha 商用策略筛选流水线 (Workflow)

本文档详细介绍了 VecAlpha 策略筛选框架的工作流程。该框架旨在从海量原始策略代码中，通过自动化、多阶段的筛选，提取出符合商用标准的顶级量化策略。

---

## 工作流概览 (Workflow Overview)

整个流水线分为四个核心阶段，采用典型的“漏斗式”筛选机制：**Phase 0 (静态) → Phase 1 (回测) → Phase 2 (评分) → 评估与同步**。

### 阶段 0：静态代码预筛 (Phase 0 - Static Screening)
*   **执行脚本**：`scripts/static_filter.py`
*   **目标**：在不运行回测的情况下，通过静态代码分析（AST）剔除低质量或不合规的策略。
*   **核心指标**：
    *   **合规性**：代码语法、必要函数（`populate_indicators`等）、逻辑一致性。
    *   **复杂度分析**：评估代码行数与逻辑深度，避免过于简单（无逻辑）或过于复杂（回测极慢）的策略。
    *   **指标扫描**：检查是否使用了非法指标或导致回测偏差的特定逻辑。
*   **产出**：`user_data/static_filter_result.json`

### 阶段 1：快速回测初筛 (Phase 1 - Quick Backtest)
*   **执行脚本**：`scripts/phase1_quick_backtest.py`
*   **目标**：用真实行情数据验证策略的初步盈利潜力和风控表现。
*   **运行环境**：隔离的 **Docker 容器**。
*   **筛选标准**：
    *   **30 天快速测试**：取最近一个月的行情数据进行高频回测。
    *   **盈利/交易门槛**：自动剔除一个月内无交易（Zero Trade）、持续大幅亏损或最大回撤（MDD）不可控的策略。
*   **产出**：`user_data/phase1_results.json`

### 阶段 2：VecScore 五维评价体系 (Phase 2 - VecScore Evaluation)
*   **执行脚本**：`scripts/vecscore.py`
*   **目标**：通过多维加权数学模型，对策略进行深度画像，并划分商用等级。
*   **评分维度 (0-100分)**：
    1.  **P (Return, 30%)**：收益能力。采用同池策略相对排名分位制。
    2.  **R (Risk, 25%)**：风控能力。核心考核 Sharpe Ratio 与 Max Drawdown，触碰红线（MDD > 40%）将触发评分上限。
    3.  **S (Stability, 20%)**：稳定性。考察在牛、熊、震荡三种市场环境下的收益一致性（Full 模式）。
    4.  **T (Reliability, 15%)**：可靠性。执行 Train/Test 分离测试，严防参数过拟合。
    5.  **E (Efficiency, 10%)**：交易效率。综合考核换手率、交易频率与资金利用率。
*   **等级划分**：
    *   **S (Score ≥ 80)**：旗舰策略，首页核心推荐。
    *   **A (Score ≥ 70)**：商用推荐，上架推荐池。
    *   **B (Score ≥ 60)**：可用，上架展示。
    *   **C / D**：高风险或不合格，禁止在商用区上架。
*   **产出**：`user_data/vecscore_results.json`

### 阶段 3：数据同步与部署 (Phase 3 - Integration)
*   **执行脚本**：`scripts/generate_leaderboard.py` 与 `scripts/db_sync_leaderboard.py`
*   **目标**：将研发成果直接转化为商用产品。
*   **产出成果**：
    *   **前端排行榜**：生成 `leaderboard.json` 供商用平台 Web UI 渲染。
    *   **数据库持久化**：将评分细节、指标历史同步至 PostgreSQL 数据库，支撑后端业务逻辑。

---

## 常见问题解答

`generate_leaderboard.py` **不是重新跑这 226 个或 465 个策略**，它更像是一个“汇总打包工具”。

以下是它的具体工作逻辑：

### 1. 它用的数据来源
当你运行 `generate_leaderboard.py --vecscore user_data/vecscore_results.json` 时：
*   它会直接读取 `vecscore_results.json` 里的结果（即经过 Phase 2 评分后的那 **226** 个策略）。
*   它不再运行任何回测，只是把 Phase 2 算好的分数、级别、风控指标提取出来，转换成前端 UI（排行榜页面）需要的格式。

### 2. 为什么是 226 个而不是 465 个？
*   **465 个**：是最初在 `strategies` 目录下扫描到的总数。
*   **153 个**：在 Phase 0（静态筛）因为代码质量、缺少必要指标或 MTF 复杂性被剔除了。
*   **其余在 Phase 1 失败的**：在 30 天回测中表现极差（比如 0 交易或回撤归零）的策略也被剔除了。
*   **226 个**：是最终**有资格进入评分系统**的策略。

### 3. 该脚本的主要任务
由于 Phase 2 已经完成了最重的算力消耗（回测和评分），`generate_leaderboard.py` 的任务非常轻量：
1.  **分级标注**：给每个策略贴上“S/A/B/C/D”标签。
2.  **排行计算**：根据分数值进行全量排序。
3.  **格式转换**：生成 `leaderboard.json`（供前端调用）和 `LEADERBOARD.md`（供你在 GitHub/本地查看）。
4.  **历史对比**：计算每个策略相对于上次排名的升降（`rank_delta`）。

### 3. 指标数据的兼容性问题
**问：`vecscore_results.json` 跑出的指标数据是否完全兼容我们之前排行榜的各项指标与数据框架？**

**答：是的，完全兼容。** 这种兼容性是通过 `generate_leaderboard.py` 这个“适配器”脚本来实现的。

以下是详细的兼容性对应逻辑：

*   **指标的自动映射**：为了在前端显示和数据库存储时保持一致，系统在处理评分数据时做了如下映射：
    *   **分数兼容**：之前的 `composite_score` 现在直接对应 `vecscore_results.json` 里的 `vecscore`。
    *   **收益率兼容**：我们的排行榜 UI 使用的是 `cagr`（年化收益），脚本会自动将 Phase 1 里的 30 天 `roi` 映射为排行榜中的收益指标。
    *   **风控指标**：`max_drawdown_pct` 和 `sharpe` 会完美对接 `R_risk` 维度中的原始输入数据（Inputs）。
    *   **交易量**：`trades` 字段会自动关联 `E_efficiency` 维度中的 `trades_30d`。
*   **数据的补充增强（联动机制）**：`vecscore_results.json` 专注于评分。为了确保完全兼容，`generate_leaderboard.py` 设计了一个**联动读取机制**：
    *   当它处理 `vecscore_results.json` 时，会自动查找同目录下的 `phase1_results.json`。
    *   它会从 `phase1_results.json` 中抓取 `win_rate`（胜率）等 VecScore 维度中未包含的原始数据，并填充到最终的排行榜中。
*   **后端与数据库的兼容**：由于 `db_sync_leaderboard.py` 是读取经处理后的 `leaderboard_*.json`，而这个文件的结构与老版本完全一致。因此**数据库字段不需要任何修改**，**前端 API 接口调用也不需要任何修改**。

---

## 核心设计理念

1.  **算力最优化**：通过分层过滤，将复杂的 Full 回测仅保留给通过初筛的少数优质策略，极大节省服务器资源。
2.  **风险前置**：在 Phase 0 阶段即剔除有潜在缺陷的代码，在 Phase 1 快速剔除高风险交易逻辑。
3.  **商用闭环**：实现了从“实验室代码”到“生产数据库”的一键式自动化同步，消除了人工干预带来的延迟与错误。

---

## 4. 自动化更新机制 (Automation Strategy)

**问：如何设计一个自动化工作流让排行榜实现自动更新？**

**答：** 要实现排行榜的自动更新，我们需要将现有的 Python 脚本串联起来，并利用系统的调度工具（如 Linux 的 **Crontab** 或 Kubernetes 的 **CronJob**）来定期触发。

以下是设计自动化工作流的三种方案：

1.  **编写自动化入口脚本 (Wrapper Script)**：创建一个总控脚本，确保每个步骤执行成功后再进行下一步。串行执行：`run_pipeline.py` -> `generate_leaderboard.py` -> `db_sync_leaderboard.py`。
2.  **使用 Linux Crontab (最简单)**：如果是本地服务器，可以使用 Crontab 定时（如每天凌晨 2 点）触发上述总控脚本。
3.  **使用 Kubernetes CronJob (推荐)**：考虑到 K3s 环境，在集群内运行一个 CronJob，利用已有的数据库 Secret 获取密码，读取 PVC 存储的数据，是最稳健的做法。

**自动化的增强建议：**
*   **健康检查**：在跑回测前确保行情数据是最新的，否则结果无意义。
*   **通知回调**：更新成功或失败后通过 Webhook 发送到即时通讯工具。
*   **锁定机制**：防止重复执行。
