# 策略批量回测与排行榜生成指南 (BACKTESTING PIPELINE)

本指南详细介绍了如何在本地测试、运行并验证 465 个策略的批量回测方案，并在本地调试通过后再推送到 GitHub Actions 进行完全自动化的 CI/CD 运行。

## 目录
1. [前期准备](#1-前期准备)
2. [本地调试与运行流程](#2-本地调试与运行流程)
    - [第一步：策略分类 (Registry)](#第一步策略分类-registry)
    - [第二步：在本地运行单个批次的回测](#第二步在本地运行单个批次的回测)
    - [第三步：本地生成排行榜](#第三步本地生成排行榜)
3. [推送到 GitHub Actions (CI/CD)](#3-推送到-github-actions-cicd)
4. [脚本参数详情](#4-脚本参数详情)
5. [策略分类体系](#5-策略分类体系)
    - [分类结果统计](#分类结果统计)
    - [分类逻辑说明](#分类逻辑说明)
    - [各类别详细定义](#各类别详细定义)

---

## 1. 前期准备

此方案由四个核心 Python 脚本和一个 GitHub Actions 配置文件组成：
- `scripts/classify_strategies.py`: 策略分类脚本，自动分析策略代码并识别其类别。
- `scripts/prepare_test_env.py`: 准备测试环境，平铺策略文件并复制数据。
- `scripts/run_batch_backtests.py`: 负责时间计算、分批策略、并调用 Freqtrade 执行。
- `scripts/generate_leaderboard.py`: 负责聚合分批生成的 JSON 输出文件，进行排行榜排序并生成 Markdown。
- `.github/workflows/backtest_leaderboard.yml`: 自动化调度配置文件。

**本地运行要求：**
- 您的本地环境必须已经安装并配置好了 Freqtrade。
- `freqtrade` 命令必须可以直接在终端使用（如果您使用 Docker 运行 Freqtrade，需要少量修改 `subprocess.run` 里的执行命令为 `docker-compose run ...`）。
- 存在基础的回测配置文件：`user_data/config.json`。

---

## 2. 本地调试与运行流程

在将代码提交到 Github 之前，请按照以下步骤在本地跑通流程。

### 第一步：数据同步与补全 (Data Sync)
大规模回测前，需确保数据的完整性。

1. **运行同步脚本**：
   ```bash
   python scripts/download_data.py --period 2025_year --docker
   ```

### 第二步：策略分类 (Registry)

系统需要一个文件来存储 465 个策略分别属于哪些类别（如：Trend趋势类、Momentum动量类等）。我们提供了分类脚本，可以自动分析策略代码并识别其类别。

> **分类原理**：脚本通过**正则表达式**匹配策略代码中的技术指标函数调用（如 `ta.RSI`、`ta.EMA`），然后使用**计分算法**根据指标组合判断交易风格。这是纯代码规则匹配，**非 AI 判断**，具有确定性。

1. **运行分类脚本：**
   ```bash
   python scripts/classify_strategies.py
   ```

2. **执行完毕后**，根目录下会生成 `strategy_registry.json` 文件，包含每个策略的多维度分类。

3. **分类结果示例：**
   ```json
   {
     "BBRSI": {
       "style": ["Mean Reversion"],
       "indicators": ["RSI", "BB"],
       "timeframe": "4h",
       "market": "Ranging",
       "features": ["trailing-stop"]
     },
     "Ichimoku": {
       "style": ["Trend"],
       "indicators": ["Ichimoku"],
       "timeframe": "5m",
       "market": "Trending",
       "features": ["trailing-stop", "multi-timeframe"]
     }
   }
   ```

4. **手动调整（可选）：** 如需微调分类，可直接编辑 `strategy_registry.json` 文件。排行榜将通过这个分类字段进行分组对抗。

### 第二步：准备测试环境

由于策略文件采用子目录结构（如 `strategies/ADXMomentum/ADXMomentum.py`），而 Freqtrade 需要**平铺**的策略文件，因此需要先准备测试环境。

1. **运行准备脚本：**
   ```bash
   python scripts/prepare_test_env.py
   ```

2. **该脚本会自动：**
   - 将所有策略文件平铺复制到 `test/user_data/strategies/`
   - 将数据文件复制到 `test/user_data/data/`

3. **预期输出：**
   ```
   [✓] Flattened 430 strategy files to test/user_data/strategies/
   [✓] Copied 13 data files to test/user_data/data/binance/
   ```

### 第三步：在本地运行单个批次的回测

由于在本地一次性运行 465 个策略会占用极大的时间与系统资源，建议在调试时将总批次数设大（例如分成 100 批），这样我们测试第 1 批次时只需要回测 4-5 个策略，即可快速验证脚本功能。

运行以下命令测试回测（使用 Docker 模式）：
```bash
python scripts/run_batch_backtests.py --period 2025_year --batch 1 --total-batches 100 --docker
```

**参数说明：**
- `--period`: 回测时间范围（`2025_year`, `last_1_week`, `last_1_month` 等）
- `--batch`: 当前批次号（从 1 开始）
- `--total-batches`: 总批次数
- `--docker`: 使用 Docker 模式运行

**预期结果：**
- 控制台会打印准备回测的 4-5 个策略名单。
- Freqtrade 开始执行回测。
- 回测完成后显示策略汇总报告。

### 第四步：本地生成排行榜

当回测成功完成后，运行以下命令生成排行榜：

```bash
python scripts/generate_leaderboard.py --period 2025_year
```

**注意**：脚本默认从 `test/user_data/backtest_results/` 读取结果，支持 `.zip` 和 `.json` 格式。

**预期结果：**
- 在当前根目录将生成两个文件：
  1. `LEADERBOARD.md`: Markdown 格式排行榜
  2. `leaderboard.json`: JSON 格式数据

---

## 3. 推送到 GitHub Actions (CI/CD)

一旦上面的第二步和第三步在本地成功生成了 Markdown 排行榜，说明代码逻辑已经完全跑通。此时您可以将这套方案推送到 GitHub。

```bash
git add strategy_registry.json scripts/ .github/
git commit -m "feat: setup parallel backtest CI/CD pipeline"
git push
```

**在 GitHub 上的运作方式：**
1. GitHub Actions 会根据 `.github/workflows/backtest_leaderboard.yml` 的配置自动并列拉起 10 台虚拟服务器（10 个并行 Job）。
2. 将这 465 个策略自动切分为 10 份（每台机器跑 46 个）。
3. 如果其中一台失败，其余台不受影响。
4. 在 10 个批次各自跑完后，将会触发最后一个聚合步骤。
5. 自动运行 `generate_leaderboard.py`，并将生成的最新 `LEADERBOARD.md` 和 JSON 结果文件作为新 Commit 自动推送到当前仓库中。

### 手动触发 CI
在 Github 仓库的 **Actions** 页面，您可以找到名为 "Strategy Leaderboard Backtesting" 的工作流，点击 **Run workflow**，然后下拉选择你要回测的周期（如 `last_3_months`）并点击执行即可。

---

## 4. 脚本参数详情

### `run_batch_backtests.py`
- `--period`: 下拉选择，支持 `2025_year`, `last_1_week`, `last_1_month`, `last_3_months`, `last_6_months`。
- `--batch`: 当前正在运行第几个批次（从 1 开始）。
- `--total-batches`: 总共想要将 465 个策略切割成多少个批次数。

### `generate_leaderboard.py`
- `--input-dir`: 放着各批次生成完毕的 JSON 文件的所在目录（通常为 `user_data/backtest_results/` 或 CI/CD 下载产生的汇总目录）。
- `--period`: 这个值将纯粹用于在展示 `LEADERBOARD.md` 的标题中声明（例如 `Strategy Leaderboard: last_1_week`）。

---

## 5. 策略分类体系

### 多维度标签系统

本系统采用与 Freqtrade 社区一致的**多维度标签体系**，每个策略包含以下维度的分类：

```json
{
  "style": ["Trend", "Mean Reversion"],  // 交易风格
  "indicators": ["BB", "RSI", "EMA"],    // 主要技术指标
  "timeframe": "5m",                      // 时间框架
  "market": "Ranging",                    // 适用市场
  "features": ["custom-stoploss", "hyperopt"]  // 功能特征
}
```

### 维度说明

| 维度 | 说明 | 可能值 |
|------|------|--------|
| **style** | 交易风格（可多选） | Trend, Mean Reversion, Momentum, Breakout, Scalping, Special |
| **indicators** | 使用的技术指标 | RSI, EMA, SMA, MACD, BB, Ichimoku, Supertrend, ADX 等 |
| **timeframe** | 主要时间框架 | 1m, 5m, 15m, 1h, 4h, 1d |
| **market** | 适用市场条件 | Trending(趋势市), Ranging(震荡市), Volatile(高波动), Any |
| **features** | 功能特征 | custom-stoploss, trailing-stop, hyperopt, multi-timeframe 等 |

### 分类结果统计

通过对 465 个策略的代码分析，自动分类结果如下：

#### 交易风格分布（可多选）

| 风格 | 数量 | 说明 |
|------|------|------|
| **Trend** | 282 | 趋势跟踪策略 |
| **Mean Reversion** | 242 | 均值回归策略 |
| **Momentum** | 134 | 动量策略 |
| **Scalping** | 100 | 剥头皮策略 |
| **Breakout** | 29 | 突破策略 |
| **Special** | 9 | 测试/工具策略 |

#### 时间框架分布

| 时间框架 | 数量 | 占比 |
|----------|------|------|
| 5m | 303 | 65.2% |
| 1h | 51 | 11.0% |
| 15m | 39 | 8.4% |
| 1m | 35 | 7.5% |
| 4h | 21 | 4.5% |
| 其他 | 16 | 3.4% |

#### 市场条件分布

| 市场条件 | 数量 | 说明 |
|----------|------|------|
| **Ranging** | 242 | 震荡市策略 |
| **Trending** | 184 | 趋势市策略 |
| **Any** | 24 | 通用策略 |
| **Volatile** | 15 | 高波动策略 |

### 分类示例

```json
// BBMod1 - 复杂混合策略
{
  "style": ["Momentum", "Mean Reversion"],
  "indicators": ["RSI", "EMA", "BB", "ADX", "Stoch", "MFI", "Williams", "RMI", "ROC"],
  "timeframe": "5m",
  "market": "Ranging",
  "features": ["custom-stoploss", "custom-exit", "hyperopt", "multi-timeframe", "multi-condition"]
}

// Ichimoku - 纯趋势策略
{
  "style": ["Trend"],
  "indicators": ["Ichimoku"],
  "timeframe": "5m",
  "market": "Trending",
  "features": ["trailing-stop", "multi-timeframe"]
}

// BBRSI - 经典均值回归
{
  "style": ["Mean Reversion"],
  "indicators": ["RSI", "BB"],
  "timeframe": "4h",
  "market": "Ranging",
  "features": ["trailing-stop"]
}
```

### 分类逻辑说明

`scripts/classify_strategies.py` 通过多维度分析实现智能分类：

> **注意**：分类结果由**纯代码规则**生成，非 AI 判断。脚本使用正则表达式匹配策略代码中的指标函数调用，通过计分算法确定交易风格。相同输入永远产生相同输出，具有确定性。

#### 1. 交易风格检测

通过指标组合和代码模式识别交易风格：

- **Trend**: EMA/SMA交叉、Ichimoku、Supertrend、MACD信号线
- **Mean Reversion**: RSI超买超卖、布林带上下轨、价格回归均值
- **Momentum**: 动量指标(MOM/ROC)、随机指标(Stoch)、资金流量(MFI)
- **Breakout**: Donchian/Keltner通道、价格突破高低点
- **Scalping**: 短时间框架 + 快速交易信号

#### 2. 技术指标提取

自动识别策略中使用的所有技术指标（支持29种）：

```
RSI, EMA, SMA, MACD, BB, CCI, ADX, Ichimoku, Supertrend, ATR, 
Stoch, MFI, VWAP, OBV, Williams, Momentum, ROC, RMI, PSAR, 
Trix, TEMA, Alligator, Awesome, Donchian, Keltner, Fibonacci, Heikin, EWO
```

#### 3. 时间框架提取

从策略代码中提取 `timeframe = "5m"` 等配置

#### 4. 市场条件推断

根据交易风格推断适用市场：
- Mean Reversion → Ranging（震荡市）
- Trend → Trending（趋势市）
- Breakout → Volatile（高波动）

#### 5. 功能特征检测

自动检测策略的高级功能：
- `custom-stoploss` - 自定义止损逻辑
- `trailing-stop` - 追踪止损
- `custom-exit` - 自定义卖出逻辑
- `hyperopt` - 支持参数优化
- `multi-timeframe` - 多时间框架
- `multi-condition` - 多买入条件（>5个）

### 各类别详细定义

#### Trend（趋势跟踪）

**核心逻辑**：跟随市场趋势方向进行交易。

**典型特征**：
- 移动平均线交叉（金叉/死叉）
- Ichimoku 云图判断趋势
- Supertrend 指标
- MACD 信号线交叉

**代表策略**：`Ichimoku`, `MACDStrategy`, `SuperTrend`, `CrossEMAStrategy`

#### Mean Reversion（均值回归）

**核心逻辑**：价格偏离均值后会回归。

**典型特征**：
- RSI 超买(>70)超卖(<30)
- 布林带下轨买入、上轨卖出
- 价格回归支撑/阻力

**代表策略**：`BBRSI`, `BB_RPB_TSL`, `ClucHAnix`

#### Momentum（动量）

**核心逻辑**：利用价格动量延续性。

**典型特征**：
- CCI、ADX 衡量趋势强度
- Stoch、MFI 判断动量
- ROC 计算变化率

**代表策略**：`ADXMomentum`, `Momentumv2`, `StochRSITEMA`

#### Breakout（突破）

**核心逻辑**：价格突破关键位置时入场。

**典型特征**：
- Donchian Channel 突破
- Keltner Channel 波动率突破
- ATR 计算突破阈值

**代表策略**：`DCBBBounce`, `keltnerchannel`

#### Scalping（剥头皮）

**核心逻辑**：短时间频繁交易，获取小幅利润。

**典型特征**：
- 短时间框架（1m/5m）
- 快速入场出场
- 小止损小止盈

**代表策略**：`Scalp`, `Quickie`, `StrategyScalpingFast`

#### Special（特殊/测试）

**核心逻辑**：测试、演示或工具类策略。

**代表策略**：`AlwaysBuy`, `SampleStrategy`, `TrailingBuyStrat2`

---

## 附录：Freqtrade 社区策略分类方法

在 Freqtrade 社区中，并没有一个官方强制的、统一的策略分类系统。策略的分类更多是社区成员和策略开发者们为了方便交流、筛选和管理而约定俗成形成的一些方法。以下是几种最主流的分类维度：

### 1. 按核心技术指标 (By Technical Indicators)

这是最常见、最直观的分类方式。策略通常会根据其产生买卖信号所依赖的主要技术指标来命名或归类。

| 指标类别 | 说明 | 示例策略 |
|----------|------|----------|
| **移动平均线类** | 基于不同周期的移动平均线（如 SMA, EMA）的金叉、死叉来判断趋势 | SimpleMAStrategy |
| **相对强弱指数类** | 利用 RSI 指标的超买（>70）和超卖（<30）区域来寻找反转机会 | BBRSI 系列 |
| **布林带类** | 当价格触及布林带的上轨或下轨时，结合其他条件进行交易，常用于判断支撑和阻力 | BB_RPB_TSL 系列 |
| **MACD 类** | 基于 MACD 线的交叉和柱状图的变化来捕捉动量和趋势 | MACDStrategy |
| **一目均衡表类** | 一种综合性的趋势跟踪系统，通过云层、转换线、基准线等多个组件来判断市场状态 | Ichimoku 系列 |
| **复合指标类** | 结合多个指标进行确认，例如同时使用 RSI、MACD 和布林带，以提高信号的准确性 | NostalgiaForInfinity 系列 |

### 2. 按交易风格或逻辑 (By Trading Style/Logic)

这种分类方式关注策略的底层交易哲学，即它试图从市场的哪种行为中获利。

#### 趋势跟踪 (Trend Following)

**核心思想**："趋势是你的朋友"。这类策略试图在趋势开始时入场，并在趋势结束时离场，以捕捉大段的行情。

**特点**：
- 在单边上涨或下跌市场中表现优异
- 在震荡市中可能频繁亏损

**适用场景**：明显的趋势市场

#### 均值回归 (Mean Reversion)

**核心假设**：资产价格和历史平均值之间存在一个长期均衡关系，当价格偏离均值过远时，最终会回归。

**操作方式**：
- 在价格极端下跌后买入（博反弹）
- 在极端上涨后卖出（博回调）

**适用场景**：震荡市、无明显趋势时

#### 突破 (Breakout)

**核心逻辑**：当价格突破一个重要的支撑位、阻力位或盘整区间时，策略会顺着突破方向开仓。

**假设**：一旦突破发生，价格会沿着该方向继续运行一段距离。

**适用场景**：盘整后的突破行情

#### 剥头皮 (Scalping)

**核心特点**：
- 超短线交易，从微小的价格波动中获取大量的小额利润
- 通常在极短的时间框架（如 1 分钟、5 分钟）上运行
- 持仓时间很短，需要低延迟和低交易费用

**风险提示**：对交易成本敏感，需要高效执行

#### 网格交易 (Grid Trading)

**操作方式**：在价格的特定区间内，预设多个买入和卖出点，形成一张"网"。价格下跌时分批买入，上涨时分批卖出，通过不断地低买高卖来获利。

### 3. 按适用市场条件 (By Market Condition)

一些策略被明确设计为在特定的宏观市场环境下运行。

| 市场类型 | 说明 | 适用策略 |
|----------|------|----------|
| **牛市策略** | 专门为上涨市场设计，可能只做多，或者在回调时积极买入 | Trend Following |
| **熊市策略** | 专门为下跌市场设计，主要通过做空获利（如果交易所支持） | Trend Following (做空) |
| **震荡市策略** | 在价格没有明显趋势、在一定区间内来回波动的市场中表现最好 | Mean Reversion |

### 4. 按其他特征

#### 使用机器学习 (Machine Learning)

一些高级策略会集成机器学习模型（如 scikit-learn, TensorFlow）来预测价格走势，这通常是一个独立的分类。

#### 依赖成交量 (Volume-based)

策略的决策严重依赖成交量数据，例如通过价量齐升或价跌量缩等模式来确认信号。

#### 时间框架 (Timeframe)

虽然不是严格的分类，但社区成员常会标注策略适用的时间框架，如 5m (5分钟), 1h (1小时), 4h (4小时)，因为一个在短周期上表现好的策略不一定适用于长周期。

### 多维度标签理解

在 Freqtrade 社区，当你看到一个策略时，可以尝试从以上几个维度去理解它。一个策略通常可以被贴上多个标签，例如：

> **"基于RSI的均值回归策略，适用于15分钟时间框架的震荡市"**

这种多维度的分类方法能帮助你最快地理解策略的核心逻辑和适用场景。

---

## 6. 常见问题 (FAQ)

**Q: 我想单独运行最近 3 个月的排行榜，要如何执行脚本命令？**

**A:** 我们的脚本均支持通过 `--period` 参数进行动态调节。您可以选择本地运行或完全依赖 GitHub Actions。

**【方式一】 本地终端运行**
连续执行以下指令即可全自动在本地完成 3个月数据的下载和 10 个批次的回测，并最终输出榜单：
1. `python scripts/classify_strategies.py` （更新分类注册表，可选）
2. `python scripts/download_data.py --period last_3_months --docker` （同步近 3 个月 K 线数据）
3. `python scripts/prepare_test_env.py` （载入全部 465 个策略到运行目录）
4. `python scripts/run_all_batches.py --period last_3_months` （后台自动执行全部批次回合并汇总）

**【方式二】 GitHub Actions 云端运行**
1. 访问 GitHub 仓库的 **Actions** 面板。
2. 选择 **Strategy Leaderboard Backtesting** 手动触发工作流。
3. 点击 **Run workflow**，在 `Timeframe period` 变量框内填写 `last_3_months`。
4. 确认执行。GitHub runner 群会自动并发执行，最终替您生成一份新榜单 Commit 合并到主分支。
