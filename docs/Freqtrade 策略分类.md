# Freqtrade 策略分类

## 1. Freqtrade 策略源码分类指南

本项目（`minimax2.5` 分支）包含 465 个开源策略，按照主流的量化交易流派可分类如下：

### 策略分类概览图表

| 策略大类 (Category) | 代表性策略 (Example) | 核心源码思想 (Core Logic) | 分类说明 (Description) |
| :--- | :--- | :--- | :--- |
| **均线回归 / 超买超卖** | `BBRSI`, `BBandsRSI` | **布林带 (BB) + RSI**。触及下轨且 RSI 极低时买入。 | 利用价格回归特性，适合震荡行情。 |
| **趋势跟踪 (Trend)** | `ADXMomentum`, `SuperTrend` | **均线交叉 (Golden Cross)**。利用 EMA/SMA 交叉确认趋势。 | 旨在捕获大波段行情，源码多含有 `fast_ma > slow_ma`。 |
| **波段交易 (Swing)** | `ActionZone`, `Alligator` | **多层均线区间**。利用多条 EMA 形成的“区域”划分入场位。 | 视觉化代码丰富，适合寻找中期转折点。 |
| **突破交易 (Breakout)** | `EMABreakout`, `SwingHigh` | **突破压力位**。监测最高价或阻力位，放量突破即入场。 | 使用 `ta.MAX` 或 `rolling_max` 定义突破线。 |
| **剥头皮 (Scalping)** | `SmoothScalp`, `FastScalp` | **超短线 (1m/5m)**。利用极速指标快进快出，赚取微小价差。 | 包含复杂的 `minimal_roi` 配置以确保极小利快速触发。 |
| **复合优化 (Hybrid)** | `NFI (NostalgiaForInfinity)` | **多维过滤**。结合波动、成交量及多指标，并深度优化。 | 社区明星策略，源码逻辑分支多，容错性强。 |
| **机器学习增强 (ML)** | `UziChan`, `Normalizer` | **动态参数**。对波动率进行归一化，动态调整止损或阈值。 | 如 `UziChan` 中的 `perc_norm` 逻辑。 |
| **一目均衡表 (Ichimoku)** | `Ichimoku_v12` | **云图 (Cloud)**。利用云层及转换线的相对位置判断势头。 | 专门针对 Ichimoku 指标开发的独特流派。 |

---

## 2. 重点策略源码分析

### ActionZone (波段交易流派)
- **核心逻辑**：基于 EMA12 和 EMA26。
- **源码特性**：`fastMA > slowMA` 且 `close > fastMA` 即可由于“黄转绿”触发买入信号。

### UziChan (复合/动态流派)
- **核心逻辑**：结合通道技术与动量过滤，使用 `ssf`（Super Smoothed Filter）。
- **源码特性**：包含复杂的 `trailing_buy`（追踪落点买入）逻辑，能有效防止在急跌中过早“接飞刀”。

### NostalgiaForInfinity (NFI)
- **核心逻辑**：集大成者，集成了趋势、均线回归、成交量突破等 10 多个子策略。
- **源码特性**：极度依赖超参数优化（Hyperopt），适合复杂多变的市场环境。
