# 排行榜数据生成操作手册

> 面向新手的完整指引，从零开始生成各时段策略排行榜并同步到前端展示。

---

## 一、背景与基本概念

### 排行榜是怎么生成的？

排行榜数据经过一条 **三阶段流水线** 自动计算生成：

```
Phase 0 (静态分析)
   ↓ 从 465 个策略中过滤出质量合格的候选策略 (~300个)
Phase 1 (快速回测)
   ↓ 对前 100 个策略运行指定时间段的回测，获取真实交易数据
Phase 2 (VecScore 评分)
   ↓ 对回测结果进行五维评分（收益/风险/效率/稳定/成本）
生成排行榜 JSON
   ↓ 输出前端所需的排行榜文件
同步数据库
   ↓ 推送到 PostgreSQL，前端页面实时读取展示
```

### 前端支持哪些时段？

| 时段标识 | 回测天数 | 前端显示名 | 数据库枚举值 |
|---|---|---|---|
| `1w` | 7 天 | Last 1 Week | `last_1_week` |
| `1m` | 30 天 | Last 1 Month | `last_1_month` |
| `3m` | 90 天 | Last 3 Months | `last_3_months` |
| `6m` | 180 天 | Last 6 Months | `last_6_months` |
| `1y` | 365 天 | Last 1 Year | `last_1_year` |

> **为什么刚开始只有 1周 和 1个月？**
> 因为每个时段的数据需要**单独跑回测**才能生成。`auto_update_leaderboard.sh` 默认只跑 30 天（1 个月）的数据。3个月、6个月和1年的数据需要手动触发或配置定时任务来补全。

---

## 二、环境要求

在开始之前，请确认以下条件已满足：

- [ ] 已安装 Python 3（`python3 --version`）
- [ ] 已安装 `psycopg2`（`pip install psycopg2-binary`）
- [ ] 项目在 `/home/neozh/freqtrade-strategies` 目录下
- [ ] K3s 集群可访问（`kubectl get nodes` 有输出）
- [ ] `user_data/config.json` 存在且配置正确
- [ ] `user_data/data/` 下有足够的历史行情数据（1年回测需要1年以上的数据）

---

## 三、第一次运行：初始化全部时段

### 步骤 1：运行 Phase 0 静态分析（只需做一次）

Phase 0 对策略库做代码静态分析，过滤出合格候选策略。**只在策略库有新增/删除时才需要重新运行。**

```bash
cd /home/neozh/freqtrade-strategies

python3 scripts/static_filter.py --summary-only
```

正常输出如下：
```
✅ 已加载 strategy_registry.json (465 个策略)
📁 发现 465 个策略文件
📊 VecAlpha 静态预筛结果摘要
  总扫描策略数  : 465
  ✅ PASS       : 312 (67.1%)
  ❌ ELIMINATED : 153
```

### 步骤 2：补全所有时段数据

> ⚠️ **注意时间成本**：
> - 1周 + 1个月：约 30-60 分钟
> - 3个月：约 2-3 小时
> - 6个月：约 4-6 小时
> - 1年：约 8-12 小时
>
> 建议在下班后或夜间运行长时段任务。

**方案A：一次性运行全部（建议夜间运行）**

```bash
./scripts/auto_update_all_periods.sh --all
```

**方案B：分批运行（推荐，可中途暂停）**

```bash
# 先跑最快的两个时段
./scripts/auto_update_all_periods.sh --period 1w
./scripts/auto_update_all_periods.sh --period 1m

# 休息后再跑中等时长的
./scripts/auto_update_all_periods.sh --period 3m
./scripts/auto_update_all_periods.sh --period 6m

# 最后跑最耗时的（夜间）
./scripts/auto_update_all_periods.sh --period 1y
```

### 步骤 3：验证数据库中的结果

```bash
python3 scripts/db_sync_leaderboard.py --env auto --check
```

正常输出应包含全部 5 个时段：
```
══════════════════════════════════════════════════════════════════════
 📊 数据库排行榜统计摘要
══════════════════════════════════════════════════════════════════════
  时段 (Period)        | 策略数量   | 最后同步时间
  ─────────────────────────────────────────────────────────────────
  last_1_week          |   100    | 2026-04-17 20:00:01
  last_1_month         |   100    | 2026-04-17 20:30:00
  last_3_months        |   100    | 2026-04-17 22:00:00
  last_6_months        |   100    | 2026-04-18 01:00:00
  last_1_year          |   100    | 2026-04-18 06:00:00
══════════════════════════════════════════════════════════════════════
```

---

## 四、日常更新（已有全量数据后）

### 每日快速更新（推荐）

每天只更新 1周 和 1个月的最新数据，速度快（约 30 分钟）：

```bash
./scripts/auto_update_all_periods.sh --daily
```

### 单独更新某一时段

如果某个时段的数据过期了，单独更新它：

```bash
./scripts/auto_update_all_periods.sh --period 3m
```

---

## 五、各脚本的独立使用方法

如果你需要更精细地控制，可以单独运行每个脚本。

### 5.1 只跑策略评分流水线（不生成排行榜）

```bash
# 运行 30 天回测 + VecScore 评分，结果存到 vecscore_results_30d.json
python3 scripts/run_pipeline.py \
    --skip-phase0 \
    --days 30 \
    --suffix 30d \
    --workers 4 \
    --phase1-limit 100
```

参数说明：
- `--skip-phase0`：跳过静态分析（已有结果时省时间）
- `--days 30`：回测最近 30 天
- `--suffix 30d`：输出文件名后缀，避免覆盖其他时段结果
- `--workers 4`：4 个并行进程加速回测
- `--phase1-limit 100`：只取前 100 个策略（0 = 全部）

### 5.2 只生成排行榜 JSON（已有评分结果时）

```bash
python3 scripts/generate_leaderboard.py \
    --vecscore user_data/vecscore_results_30d.json \
    --period last_1_month \
    --limit 100
```

参数说明：
- `--vecscore`：指定 VecScore 评分结果文件
- `--period`：时段标识（必须与前端枚举匹配，见上方表格）
- `--limit 100`：只输出 Top 100（0 = 输出全部）

生成的文件位于：
- JSON：`user_data/leaderboard/leaderboard_last_1_month.json`
- Markdown：`user_data/leaderboard/LEADERBOARD_last_1_month.md`

### 5.3 只同步数据库（已有排行榜 JSON 时）

```bash
python3 scripts/db_sync_leaderboard.py --env auto
```

参数说明：
- `--env auto`：自动检测连接方式（本地 / K3s port-forward / 集群内）
- `--env local`：强制走本地 5432 端口
- `--env k3s`：强制走 K3s 集群内连接

### 5.4 查看数据库中当前数据状态

```bash
python3 scripts/db_sync_leaderboard.py --env auto --check
```

---

## 六、常见问题排查

### Q1: `vecscore_results_Xd.json` 文件不存在？

原因：流水线还没跑完，或者跑失败了。

解决方案：
```bash
# 确认文件是否存在
ls -lh user_data/vecscore_results*.json

# 重新运行对应时段
./scripts/auto_update_all_periods.sh --period 1m
```

### Q2: 数据库连接超时？

原因：K3s 集群不可达。

解决方案：
```bash
# 检查是否能连接到集群
kubectl get nodes

# 手动启动端口转发
kubectl port-forward svc/mx-postgres-ha-postgresql-ha-pgpool 5432:5432 -n infra &

# 再次同步
python3 scripts/db_sync_leaderboard.py --env auto
```

### Q3: 回测时出现 `DDosProtection` 错误？

原因：缺少本地历史数据，策略回测时尝试实时拉取行情，但被限流。

解决方案：先下载足够的历史数据：
```bash
freqtrade download-data \
    --pairs BTC/USDT:USDT ETH/USDT:USDT \
    --timeframe 5m 1h 1d \
    --days 400 \
    --config user_data/config.json
```

### Q4: 前端刷新后还是显示旧数据？

可能原因：
1. 浏览器缓存 → 强制刷新（Ctrl + F5）
2. 数据库同步失败 → 运行 `--check` 确认数据已入库
3. 前端有 Redis 缓存 → 重启前端服务

### Q5: 排行榜只显示部分时段？

说明某些时段的数据库记录为空。运行 `--check` 确认后，单独补充缺失的时段：
```bash
python3 scripts/db_sync_leaderboard.py --env auto --check
# 查看哪些 period 缺失，然后：
./scripts/auto_update_all_periods.sh --period 6m
```

---

## 七、推荐定时任务配置

如果你希望排行榜完全自动更新，可以配置 Crontab：

```bash
crontab -e
```

添加以下内容：
```cron
# 每天凌晨 2 点：更新 1 周和 1 个月的数据（约 30 分钟）
0 2 * * * cd /home/neozh/freqtrade-strategies && ./scripts/auto_update_all_periods.sh --daily >> user_data/auto_update.log 2>&1

# 每周日凌晨 0 点：更新 3 个月数据
0 0 * * 0 cd /home/neozh/freqtrade-strategies && ./scripts/auto_update_all_periods.sh --period 3m >> user_data/auto_update.log 2>&1

# 每月 1 日凌晨 0 点：更新 6 个月和 1 年数据
0 0 1 * * cd /home/neozh/freqtrade-strategies && ./scripts/auto_update_all_periods.sh --period 6m >> user_data/auto_update.log 2>&1
30 0 1 * * cd /home/neozh/freqtrade-strategies && ./scripts/auto_update_all_periods.sh --period 1y >> user_data/auto_update.log 2>&1
```

查看自动更新日志：
```bash
tail -f user_data/auto_update.log
```

---

## 八、相关文件说明

| 文件/目录 | 说明 |
|---|---|
| `scripts/auto_update_all_periods.sh` | **主入口** - 全时段自动更新脚本 |
| `scripts/auto_update_leaderboard.sh` | 简单版：只跑 1 个月 |
| `scripts/run_pipeline.py` | 流水线总控（Phase0 + Phase1 + Phase2）|
| `scripts/static_filter.py` | Phase 0：策略静态分析 |
| `scripts/phase1_quick_backtest.py` | Phase 1：快速回测 |
| `scripts/vecscore.py` | Phase 2：VecScore 五维评分 |
| `scripts/generate_leaderboard.py` | 排行榜 JSON 生成器 |
| `scripts/db_sync_leaderboard.py` | 数据库同步工具 |
| `user_data/vecscore_results_*.json` | 各时段 VecScore 评分结果 |
| `user_data/leaderboard/leaderboard_*.json` | 各时段排行榜 JSON（前端读取）|
| `user_data/auto_update.log` | 定时任务运行日志 |

---

## 九、用少量策略快速验证新时段流程

在正式跑全量（100个策略）之前，建议先用少量策略（如 10 个）跑通整条链路，确认数据能正确推送到前端，再安排夜间跑完整版。

### 示例：用 10 个策略跑通 6 个月流程

```bash
# Step 1: 回测 + 评分（只跑前 10 个策略，180 天回测）
python3 scripts/run_pipeline.py \
    --skip-phase0 \
    --days 180 \
    --suffix 6m \
    --workers 4 \
    --phase1-limit 10

# Step 2: 生成排行榜 JSON
python3 scripts/generate_leaderboard.py \
    --vecscore user_data/vecscore_results_6m.json \
    --period last_6_months \
    --limit 10

# Step 3: 同步到数据库
python3 scripts/db_sync_leaderboard.py --env auto

# Step 4: 验证数据是否进库
python3 scripts/db_sync_leaderboard.py --env auto --check
```

### 通用模板（适用于任何时段）

把时段参数替换即可复用：

| 时段 | `--days` | `--suffix` | `--period` |
|---|---|---|---|
| 1 周 | `7` | `7d` | `last_1_week` |
| 1 个月 | `30` | `30d` | `last_1_month` |
| 3 个月 | `90` | `90d` | `last_3_months` |
| 6 个月 | `180` | `6m` | `last_6_months` |
| 1 年 | `365` | `1y` | `last_1_year` |

> **流程验证通过后**，把 `--phase1-limit 10` 改回 `--phase1-limit 100`（或不加，使用默认值 100），再跑一次即可生成完整的排行榜。

### 如果上次已经跑了 Phase 1，不想重跑

只需复制结果文件，然后跳过 Phase 1：

```bash
# 例：复用已有的 phase1_results.json（无后缀）作为 6m 的输入
cp user_data/phase1_results.json user_data/phase1_results_6m.json

# 从 Phase 2 开始继续，跳过 Phase 0 和 Phase 1
python3 scripts/run_pipeline.py \
    --skip-phase0 \
    --skip-phase1 \
    --suffix 6m

# 后续步骤同上（生成排行榜、同步数据库）
python3 scripts/generate_leaderboard.py \
    --vecscore user_data/vecscore_results_6m.json \
    --period last_6_months \
    --limit 100

python3 scripts/db_sync_leaderboard.py --env auto
```

---

## 十、进阶功能：数据预检与精准评分

随着日常使用深入，你可能会遇到“本地数据够不够跑 1 年回测？”或“需要最顶尖的严格评分验证”等场景，流水线提供了相应的进阶支持：

### 10.1 历史数据预检机制

在运行任何时段的 `auto_update_all_periods.sh` 时，系统都会**自动在第一步执行数据覆盖情况预检**。

- 机制：通过扫描 `user_data/data/` 下的文件大小和最新修改时间，快速估算当前历史数据涵盖的天数（避免完整读取产生的极慢耗时）。
- 如果数据不满足请求的回测天数（例如想跑 1 年，但数据仅有 100 天），脚本会**立即报错中止**，并输出修复命令（避免流水线空跑数十分钟最后失败）：
  ```
  ❌ 历史数据不足，无法运行 365 天回测。
  ❌ 请先运行以下命令补充数据：
    freqtrade download-data --config user_data/config.json --timeframe 5m 15m 1h 1d --days 395
  ```

如果你想手动检查数据健康程度，也可以单独运行该预检工具：
```bash
# 单独检查能否跑 180 天回测
python3 scripts/check_data_coverage.py --days 180

# 增加自动下载参数，一旦发现不足自动启动补数据进程
python3 scripts/check_data_coverage.py --days 365 --auto-download

# 开启严格模式（默认存在 20% 时间戳估算容差，开启后强制足量验证）
python3 scripts/check_data_coverage.py --days 90 --strict
```

### 10.2 评分模式控制 (`fast` vs `full`)

`auto_update_all_periods.sh` 支持 `--mode` 选项来决定 VecScore 的计算深度：

```bash
# 默认快速模式 (适合日常快刷榜单)
./scripts/auto_update_all_periods.sh --period 6m --limit 100 --mode fast

# 完整精确模式 (适合给策略做最后商用审核)
./scripts/auto_update_all_periods.sh --period 6m --limit 20 --mode full
```

**两种模式的核心差异详情：**

| 特性 | `fast` 模式（默认） | `full` 模式 |
|---|---|---|
| **执行速度** | 极快（读缓存，秒级） | 极慢（需要分钟至小时级跑附加回测）|
| **S 维度 (稳定性)** | 使用 30 天基础数据估算 `~` | 启动 Train / Test 分段回测 (牛/熊/震荡市分析) |
| **T 维度 (多维度跨期)** | 推理估算 | 真实多重时长交叉验证 |
| **分数标记** | 分数后带有 `~` 估算标记，如 `59.0~` | 精确分数，无估算标记 |
| **推荐场景** | 日常定时更新、快速刷榜单排查大致范围 | 对 Top 20 策略进行二次验证分析及商用投产审核 |

#### 深入理解 `full` 模式的底层逻辑：
当使用 `--mode full` 运行评估时，流水线会为每个策略执行高强度的交叉验证操作（因此极度耗时）：

1. **市场类型切片扫描 (S 维度严格测试)**
   系统在后台会划分出几段典型的历史行情（例如：2024年初的牛市段、年中的震荡市段、年末的新趋势段）。每个策略都会在这些**互相独立的切片**中反复回测。只有在“牛熊皆可盈利，震荡不仅能保本且不暴亏”的策略，才能在 S 维度拿到高分。
   
2. **Train/Test 样本外验证 (T 维度严格测试)**
   系统不再仅仅看 Phase 1 的总利润，而是通过 `Train/Test` 将历史切成两半：前半段跑回测（Train阶段），如果盈利很高，就在后半段“未见过的行情”（Test阶段）再跑一遍。如果 Test 阶段立刻翻车亏损，说明该策略严重“过拟合 (Overfitting)”，T 维度将被打极低分数；反之如果表现一致，说明鲁棒性强，分数极高。

**建议实践**：平时用默认的 `fast` 模式生成前 100 排行榜进行初筛。遇到排名前列、想拿去挂实盘的策略时，单独用 `full` 模式对这几个策略做一次深度体检跑分。

### 10.3 指定单个或多个特定策略进行测试

有些时候你不希望跑全量策略，例如：你想测试一个刚写好的新策略，或者想对榜单上 Top 3 的金钻策略用 `full` 模式进行最严苛的复检。系统支持通过 `-s`（或 `--strategies`）参数将策略名进行透传。

**使用场景与命令示例：**

1. **测单个策略** (比如给 `ADXMomentum` 跑一次 6个月 的估算测试)
   ```bash
   ./scripts/auto_update_all_periods.sh --period 6m -s "ADXMomentum"
   ```

2. **同时测试多个策略** (挑出 3 个表现不错的策略并行跑)
   > **注意**：多个策略之间用**空格**隔开，并且一定要套在 `" "` 双引号里面。
   ```bash
   ./scripts/auto_update_all_periods.sh --period 3m -s "ADXMomentum Apollo11 AwesomeMacd"
   ```

3. **【终极体检】实盘投产前必做**
   对你在其他时段看好的“准实盘”策略，用最严苛的 `full` 模式跑一遍 1 年数据，这包含了市场多切片验证和 Train/Test 样本外验证等极度防过拟合的机制：
   ```bash
   ./scripts/auto_update_all_periods.sh --period 1y -s "ADXMomentum" --mode full
   ```
