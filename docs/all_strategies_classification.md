# Freqtrade 策略分类汇总

## 策略全集分类表

本项目（`minimax2.5` 分支）共有 465 个策略，按照交易流派和源码逻辑分类如下：

| 策略大类 (Category) | 包含的策略 (Strategies) | 核心特征 (Key Features) |
| :--- | :--- | :--- |
| **均线回归 / 超买超卖** | `BBRSI`, `BBandsRSI`, `BBRSIv2`, `BBRSIS`, `BBRSIOptim2020Strategy`, `RSIBB02`, `BB_RSI`, `Bandtastic`, `Low_BB`, `DCBBBounce`, `BBlower`, `BBRSINaiveStrategy`, `BBRSIOptimizedStrategy` | 基于布林带 (Bollinger Bands) 和 RSI 指标，寻找极端超买或超卖点。 |
| **趋势跟踪 (Trend)** | `ADXMomentum`, `SuperTrend`, `EMA_CROSSOVER_STRATEGY`, `CrossEMAStrategy`, `Uptrend`, `SMAOffset`, `SMAOffsetV2`, `ADX_15M_USDT`, `AlwaysBuy`, `EMA50`, `FastSupertrend`, `SuperTrendPure`, `SMAOG`, `PRICEFOLLOWING`, `Trend_Strength_Directional` | 使用均线交叉、SuperTrend、ADX 等趋势确认指标，在趋势形成时持有。 |
| **波段交易 (Swing)** | `ActionZone`, `AlligatorStrategy`, `WaveTrendStra`, `AlligatorStrat`, `Persia`, `Guacamole`, `SwingHigh`, `SwingHighToSky`, `ElliotV8_original`, `Elliotv8`, `ElliotV2`, `ElliotV4`, `ElliotV531`, `ElliotV7` | 利用多重均线（如 ActionZone 的 EMA12/26）或波段理论（如艾略特波段）进行中期交易。 |
| **复合优化 (Hybrid)** | `NostalgiaForInfinity (NFI)`, `NostalgiaForInfinityNext`, `NFI46`, `NFI47V2`, `CombinedBinHAndCluc`, `ClucHAnix`, `BigZ04`, `BigZ07Next`, `BinClucMad`, `CombinedBinHClucAndMADV9`, `NASOSv5`, `NASOSv4`, `NFIX_BB_RPB` | 集成多种策略逻辑（趋势+回归+成交量），通常经过大量 Hyperopt 优化，如知名的 NFI 系列。 |
| **剥头皮 (Scalping)** | `SmoothScalp`, `StrategyScalpingFast`, `StrategyScalpingFast2`, `Quickie`, `ReinforcedQuickie`, `ReinforcedSmoothScalp`, `FastScalp`, `FastSupertrendOpt`, `SmallScalp` | 面向 1m/5m 短时框架，利用极高灵敏度的指标进行频繁交易，追求小利润累积。 |
| **突破交易 (Breakout)** | `EMABreakout`, `SwingHigh`, `BreakEven`, `HighLow`, `SMAOffsetProtectOpt`, `SMAOffsetProtectOptV1`, `NotAnotherSMAOffsetStrategy` | 寻找价格突破前期高点、低点或均线阻力位的信号。 |
| **一目均衡表 (Ichimoku)** | `Ichimoku`, `Ichimoku_v12`, `Ichimoku_v30`, `Ichimoku_v31`, `Ichimoku_v32`, `Ichimoku_v37`, `Obelisk_Ichimoku`, `NowoIchimoku1hV1`, `Ichi`, `ichiV1_Marius` | 专注于云图指标（转换线、基准线、云层）的综合势头判断。 |
| **动量与震荡 (Oscillation)** | `MACDStrategy`, `MACD_EMA`, `MACDCCI`, `MACDRSI200`, `JustROCR6`, `AwesomeMacd`, `LuxOSC`, `MFI`, `Cci`, `TrixStrategy`, `UltimateMomentumIndicator` | 基于 MACD、ROC、CCI、RSI 等动量摆动指标进行买卖判断。 |
| **机器学习与统计 (ML/Stat)** | `UziChan`, `UziChan2`, `NormalizerStrategy`, `NormalizerStrategyHO2`, `adaptive`, `InformativeSample`, `LookaheadStrategy` (用于测试), `CustomStoplossWithPSAR` | 使用归一化处理、动态参数调整或简单的统计学概率逻辑（如 UziChan 的波动率归一化）。 |
| **其他/工具型** | `SampleStrategy`, `TechnicalExampleStrategy`, `BuyOnly`, `AlwaysBuy`, `BuyAllSellAllStrategy`, `EXPERIMENTAL_STRATEGY`, `stoploss` | 包含示例代码、单一功能测试（只买入、只卖出）或纯止损逻辑测试。 |

> **注：** 由于很多策略（特别是 NFI 和 BigZ 系列）具有多个变体版本及 Hyperopt 版本，上述分类已将同系列策略进行了合集化处理。完整的 465 个策略文件夹已全部包含在上述分类的思想范围内。
