# Freqtrade 465 策略详细分类与应用时机全表

| # | 策略名称 (Strategy Name) | 分类 (Category) | 应用时机 (Market Context) | 核心特征 (Core Features) | 策略核心机制 (Mechanism) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `ADXMomentum` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 2 | `ADX_15M_USDT` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 3 | `ADX_15M_USDT2` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 4 | `ASDTSRockwellTrading` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 5 | `ActionZone` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 6 | `AdxSmas` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 7 | `AlligatorStrat` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 8 | `AlligatorStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 9 | `AlwaysBuy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 10 | `Apollo11` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 11 | `AverageStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 12 | `AwesomeMacd` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 13 | `BBMod1` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 14 | `BBRSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 15 | `BBRSI2` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 16 | `BBRSI21` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 17 | `BBRSI3366` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 18 | `BBRSI4cust` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 19 | `BBRSINaiveStrategy` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 20 | `BBRSIOptim2020Strategy` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 21 | `BBRSIOptimStrategy` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 22 | `BBRSIOptimizedStrategy` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 23 | `BBRSIS` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 24 | `BBRSIStrategy` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 25 | `BBRSITV` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 26 | `BBRSIoriginal` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 27 | `BBRSIv2` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 28 | `BB_RPB_TSL` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 29 | `BB_RPB_TSL_2` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 30 | `BB_RPB_TSL_BI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 31 | `BB_RPB_TSL_BIV1` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 32 | `BB_RPB_TSL_RNG` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 33 | `BB_RPB_TSL_RNG_2` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 34 | `BB_RPB_TSL_RNG_TBS` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 35 | `BB_RPB_TSL_RNG_TBS_GOLD` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 36 | `BB_RPB_TSL_RNG_VWAP` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 37 | `BB_RPB_TSL_SMA_Tranz` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 38 | `BB_RPB_TSL_SMA_Tranz_TB_1_1_1` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 39 | `BB_RPB_TSL_SMA_Tranz_TB_MOD` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 40 | `BB_RPB_TSL_Tranz` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 41 | `BB_RPB_TSL_c7c477d_20211030` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 42 | `BB_RPB_TSLmeneguzzo` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 43 | `BB_RSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 44 | `BB_Strategy04` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 45 | `BBands` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 46 | `BBandsRSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 47 | `BBlower` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 48 | `Babico_SMA5xBBmid` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 49 | `Bandtastic` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 50 | `BbRoi` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 51 | `BbandRsi` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 52 | `BbandRsiRolling` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 53 | `BcmbigzDevelop` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 54 | `BcmbigzV1` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 55 | `BigPete` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 56 | `BigZ03` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 57 | `BigZ0307HO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 58 | `BigZ03HO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 59 | `BigZ04` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 60 | `BigZ0407` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 61 | `BigZ0407HO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 62 | `BigZ04HO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 63 | `BigZ04HO2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 64 | `BigZ04_TSL3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 65 | `BigZ04_TSL4` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 66 | `BigZ06` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 67 | `BigZ07` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 68 | `BigZ07Next` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 69 | `BigZ07Next2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 70 | `BinClucMad` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 71 | `BinClucMadDevelop` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 72 | `BinClucMadSMADevelop` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 73 | `BinClucMadV1` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 74 | `BinHV27` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 75 | `BinHV45` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 76 | `BinHV45HO` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 77 | `BreakEven` | 突破交易 (Breakout) | 突破行情 (Breakout) | 最高/最低价、波动率突破 | 适合在关键阻力位/压力位被冲破后的瞬间入场。监测特定周期内的阻力线，放量站上阻力线时进场 |
| 78 | `BuyAllSellAllStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 79 | `BuyOnly` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 80 | `CBPete9` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 81 | `CCIStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 82 | `CMCWinner` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 83 | `Cci` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 84 | `Chandem` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 85 | `Chandemtwo` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 86 | `Chispei` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 87 | `Cluc4` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 88 | `Cluc4werk` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 89 | `Cluc5werk` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 90 | `Cluc7werk` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 91 | `ClucFiatROI` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 92 | `ClucFiatSlow` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 93 | `ClucHAnix` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 94 | `ClucHAnix5m` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 95 | `ClucHAnix_5m` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 96 | `ClucHAnix_5m1` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 97 | `ClucHAnix_BB_RPB_MOD` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 98 | `ClucHAnix_BB_RPB_MOD2_ROI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 99 | `ClucHAnix_BB_RPB_MOD_CTT` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 100 | `ClucHAnix_BB_RPB_MOD_E0V1E_ROI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 101 | `ClucHAnix_hhll` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 102 | `ClucHAwerk` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 103 | `ClucMay72018` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 104 | `CofiBitStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 105 | `CombinedBinHAndCluc` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 106 | `CombinedBinHAndCluc2021` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 107 | `CombinedBinHAndCluc2021Bull` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 108 | `CombinedBinHAndClucHyperV0` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 109 | `CombinedBinHAndClucHyperV3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 110 | `CombinedBinHAndClucV2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 111 | `CombinedBinHAndClucV3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 112 | `CombinedBinHAndClucV4` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 113 | `CombinedBinHAndClucV5` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 114 | `CombinedBinHAndClucV5Hyperoptable` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 115 | `CombinedBinHAndClucV6` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 116 | `CombinedBinHAndClucV6H` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 117 | `CombinedBinHAndClucV7` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 118 | `CombinedBinHAndClucV8` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 119 | `CombinedBinHAndClucV8Hyper` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 120 | `CombinedBinHAndClucV8XH` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 121 | `CombinedBinHAndClucV8XHO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 122 | `CombinedBinHClucAndMADV3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 123 | `CombinedBinHClucAndMADV5` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 124 | `CombinedBinHClucAndMADV6` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 125 | `CombinedBinHClucAndMADV9` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 126 | `Combined_Indicators` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 127 | `Combined_NFIv6_SMA` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 128 | `Combined_NFIv7_SMA` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 129 | `Combined_NFIv7_SMA_Rallipanos_20210707` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 130 | `Combined_NFIv7_SMA_bAdBoY_20211204` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 131 | `CoreStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 132 | `CrossEMAStrategy` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 133 | `CryptoFrog` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 134 | `CryptoFrogHO` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 135 | `CryptoFrogHO2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 136 | `CryptoFrogHO2A` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 137 | `CryptoFrogHO3A1` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 138 | `CryptoFrogHO3A2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 139 | `CryptoFrogHO3A3` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 140 | `CryptoFrogHO3A4` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 141 | `CryptoFrogNFI` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 142 | `CryptoFrogNFIHO1A` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 143 | `CryptoFrogOffset` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 144 | `CustomStoplossWithPSAR` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 145 | `DCBBBounce` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 146 | `DD` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 147 | `DIV_v1` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 148 | `DevilStra` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 149 | `Diamond` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 150 | `Divergences` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 151 | `Dracula` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 152 | `Dyna_opti` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 153 | `EI3v2_tag_cofi_green` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 154 | `EMA50` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 155 | `EMA520015_V17` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 156 | `EMABBRSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 157 | `EMABreakout` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 158 | `EMASkipPump` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 159 | `EMAVolume` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 160 | `EMA_CROSSOVER_STRATEGY` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 161 | `EXPERIMENTAL_STRATEGY` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 162 | `ElliotV2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 163 | `ElliotV4` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 164 | `ElliotV531` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 165 | `ElliotV5HO` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 166 | `ElliotV5HOMod2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 167 | `ElliotV5HOMod3` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 168 | `ElliotV7` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 169 | `ElliotV8HO` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 170 | `ElliotV8_original` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 171 | `ElliotV8_original_ichiv2` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 172 | `ElliotV8_original_ichiv3` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 173 | `Elliotv8` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 174 | `FRAYSTRAT` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 175 | `Fakebuy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 176 | `FastSupertrend` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 177 | `FastSupertrendOpt` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 178 | `FiveMinCrossAbove` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 179 | `FixedRiskRewardLoss` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 180 | `ForexSignal` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 181 | `FrostAuraM115mStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 182 | `FrostAuraM11hStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 183 | `FrostAuraM21hStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 184 | `FrostAuraM315mStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 185 | `FrostAuraM31hStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 186 | `FrostAuraRandomStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 187 | `GodCard` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 188 | `GodStraNew` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 189 | `GodStraNew40` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 190 | `GodStraNew_SMAonly` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 191 | `Guacamole` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 192 | `Gumbo1` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 193 | `Hacklemore2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 194 | `Hacklemore3` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 195 | `HansenSmaOffsetV1` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 196 | `HarmonicDivergence` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 197 | `Heracles` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 198 | `HourBasedStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 199 | `HyperStra_GSN_SMAOnly` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 200 | `HyperStra_SMAOnly` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 201 | `INSIDEUP` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 202 | `Ichess` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 203 | `Ichi` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 204 | `Ichimoku` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 205 | `Ichimoku_SenkouSpanCross` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 206 | `Ichimoku_v12` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 207 | `Ichimoku_v30` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 208 | `Ichimoku_v31` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 209 | `Ichimoku_v32` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 210 | `Ichimoku_v33` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 211 | `Ichimoku_v37` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 212 | `InformativeSample` | 机器学习/统计增强 (ML/Stat) | 复杂多变市场 | 归一化处理、动态参数 | 适合市场节奏变换较快的情况，动态调整参数。根据当前波动率或市场状态动态修正买卖阈值和止损位 |
| 213 | `Inverse` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 214 | `InverseV2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 215 | `JustROCR` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 216 | `JustROCR3` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 217 | `JustROCR5` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 218 | `JustROCR6` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 219 | `KAMACCIRSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 220 | `KC_BB` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 221 | `Kamaflage` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 222 | `Leveraged` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 223 | `LookaheadStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 224 | `Low_BB` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 225 | `LuxOSC` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 226 | `MAC` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 227 | `MACDCCI` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 228 | `MACDRSI200` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 229 | `MACDStrategy` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 230 | `MACDStrategy_crossed` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 231 | `MACD_EMA` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 232 | `MACD_TRIPLE_MA` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 233 | `MACD_TRI_EMA` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 234 | `MADisplaceV3` | 抄底/波动 (Dip Buying) | 暴跌/插针 (Flash Crash) | Clucas算法、BinH算法 | 在市场极速探底或出现异常插针时捕捉反弹。通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入 |
| 235 | `MFI` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 236 | `Macd` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 237 | `MacheteV8b` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 238 | `MacheteV8bRallimod2` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 239 | `MarketChyperHyperStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 240 | `Maro4hMacdSd` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 241 | `Martin` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 242 | `MiniLambo` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 243 | `Minmax` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 244 | `MomStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 245 | `Momentumv2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 246 | `MontrealStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 247 | `MostOfAll` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 248 | `MultiMA_TSL` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 249 | `MultiMA_TSL3` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 250 | `MultiMA_TSL3_Mod` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 251 | `MultiMa` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 252 | `MultiOffsetLamboV0` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 253 | `MultiRSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 254 | `NASOSRv6_private_Reinuvader_20211121` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 255 | `NASOSv4` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 256 | `NASOSv5` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 257 | `NASOSv5_mod1` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 258 | `NASOSv5_mod1_DanMod` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 259 | `NASOSv5_mod2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 260 | `NASOSv5_mod3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 261 | `NFI46` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 262 | `NFI46Frog` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 263 | `NFI46FrogZ` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 264 | `NFI46Offset` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 265 | `NFI46OffsetHOA1` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 266 | `NFI46Z` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 267 | `NFI47V2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 268 | `NFI4Frog` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 269 | `NFI5MOHO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 270 | `NFI5MOHO2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 271 | `NFI5MOHO_WIP` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 272 | `NFI5MOHO_WIP_1` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 273 | `NFI5MOHO_WIP_2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 274 | `NFI731_BUSD` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 275 | `NFI7MOHO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 276 | `NFINextMOHO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 277 | `NFINextMOHO2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 278 | `NFINextMultiOffsetAndHO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 279 | `NFINextMultiOffsetAndHO2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 280 | `NFIX_BB_RPB` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 281 | `NFIX_BB_RPB_c7c477d_20211030` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 282 | `NfiNextModded` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 283 | `NormalizerStrategy` | 机器学习/统计增强 (ML/Stat) | 复杂多变市场 | 归一化处理、动态参数 | 适合市场节奏变换较快的情况，动态调整参数。根据当前波动率或市场状态动态修正买卖阈值和止损位 |
| 284 | `NormalizerStrategyHO2` | 机器学习/统计增强 (ML/Stat) | 复杂多变市场 | 归一化处理、动态参数 | 适合市场节奏变换较快的情况，动态调整参数。根据当前波动率或市场状态动态修正买卖阈值和止损位 |
| 285 | `Nostalgia` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 286 | `NostalgiaForInfinityNext` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 287 | `NostalgiaForInfinityNextGen` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 288 | `NostalgiaForInfinityNextGen_TSL` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 289 | `NostalgiaForInfinityNextV7155` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 290 | `NostalgiaForInfinityNext_ChangeToTower_V5_2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 291 | `NostalgiaForInfinityNext_ChangeToTower_V5_3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 292 | `NostalgiaForInfinityNext_ChangeToTower_V6` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 293 | `NostalgiaForInfinityNext_maximizer` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 294 | `NostalgiaForInfinityV1` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 295 | `NostalgiaForInfinityV2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 296 | `NostalgiaForInfinityV3` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 297 | `NostalgiaForInfinityV4` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 298 | `NostalgiaForInfinityV4HO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 299 | `NostalgiaForInfinityV5` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 300 | `NostalgiaForInfinityV5MultiOffsetAndHO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 301 | `NostalgiaForInfinityV5MultiOffsetAndHO2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 302 | `NostalgiaForInfinityV6` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 303 | `NostalgiaForInfinityV6HO` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 304 | `NostalgiaForInfinityV7` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 305 | `NostalgiaForInfinityV7_7_2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 306 | `NostalgiaForInfinityV7_SMA` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 307 | `NostalgiaForInfinityV7_SMAv2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 308 | `NostalgiaForInfinityV7_SMAv2_1` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 309 | `NostalgiaForInfinityX` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 310 | `NostalgiaForInfinityX2` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 311 | `NostalgiaForInfinityXw` | 复合优化 (Hybrid/Complex) | 全天候 (All-Weather) | 多维过滤、深度参数优化 | 适合各种市场环境，通过多重过滤降低回撤。集成趋势、回归、动量等10+种子逻辑的分支判断 |
| 312 | `NotAnotherSMAOffSetStrategy_V2` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 313 | `NotAnotherSMAOffsetStrategy` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 314 | `NotAnotherSMAOffsetStrategyHO` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 315 | `NotAnotherSMAOffsetStrategyHOv3` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 316 | `NotAnotherSMAOffsetStrategyLite` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 317 | `NotAnotherSMAOffsetStrategyModHO` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 318 | `NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 319 | `NotAnotherSMAOffsetStrategyX1` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 320 | `NotAnotherSMAOffsetStrategy_uzi` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 321 | `NotAnotherSMAOffsetStrategy_uzi3` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 322 | `NowoIchimoku1hV1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 323 | `NowoIchimoku1hV2` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 324 | `NowoIchimoku5mV2` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 325 | `ONUR` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 326 | `ObeliskIM_v1_1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 327 | `ObeliskRSI_v6_1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 328 | `Obelisk_3EMA_StochRSI_ATR` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 329 | `Obelisk_Ichimoku_Slow_v1_3` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 330 | `Obelisk_Ichimoku_ZEMA_v1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 331 | `Obelisk_TradePro_Ichi_v1_1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 332 | `Obelisk_TradePro_Ichi_v2_1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 333 | `PRICEFOLLOWING` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 334 | `PRICEFOLLOWING2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 335 | `PRICEFOLLOWINGX` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 336 | `Persia` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 337 | `PrawnstarOBV` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 338 | `PumpDetector` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 339 | `Quickie` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 340 | `RSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 341 | `RSIBB02` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 342 | `RSIv2` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 343 | `RalliV1` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 344 | `RalliV1_disable56` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 345 | `RaposaDivergenceV1` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 346 | `ReinforcedAverageStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 347 | `ReinforcedQuickie` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 348 | `ReinforcedSmoothScalp` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 349 | `Renko` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 350 | `RobotradingBody` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 351 | `Roth01` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 352 | `Roth03` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 353 | `SAR` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 354 | `SMAIP3` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 355 | `SMAIP3v2` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 356 | `SMAOG` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 357 | `SMAOPv1_TTF` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 358 | `SMAOffset` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 359 | `SMAOffsetProtectOpt` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 360 | `SMAOffsetProtectOptV0` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 361 | `SMAOffsetProtectOptV1` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 362 | `SMAOffsetProtectOptV1HO1` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 363 | `SMAOffsetProtectOptV1Mod` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 364 | `SMAOffsetProtectOptV1Mod2` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 365 | `SMAOffsetProtectOptV1_kkeue_20210619` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 366 | `SMAOffsetV2` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 367 | `SMA_BBRSI` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 368 | `SRsi` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 369 | `STRATEGY_RSI_BB_BOUNDS_CROSS` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 370 | `STRATEGY_RSI_BB_CROSS` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 371 | `SampleStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 372 | `SampleStrategyV2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 373 | `Saturn5` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 374 | `Scalp` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 375 | `Schism` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 376 | `Schism2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 377 | `Schism2MM` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 378 | `Schism3` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 379 | `Schism4` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 380 | `Schism5` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 381 | `Schism6` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 382 | `Seb` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 383 | `Simple` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 384 | `SlowPotato` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 385 | `Slowbro` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 386 | `SmoothOperator` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 387 | `SmoothScalp` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 388 | `Stavix2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 389 | `Stinkfist` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 390 | `StochRSITEMA` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 391 | `Strategy001` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 392 | `Strategy001_custom_sell` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 393 | `Strategy002` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 394 | `Strategy003` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 395 | `Strategy004` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 396 | `Strategy005` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 397 | `StrategyScalpingFast` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 398 | `StrategyScalpingFast2` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 399 | `SuperHV27` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 400 | `SuperTrend` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 401 | `SuperTrendPure` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 402 | `SupertrendStrategy` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 403 | `SwingHigh` | 突破交易 (Breakout) | 突破行情 (Breakout) | 最高/最低价、波动率突破 | 适合在关键阻力位/压力位被冲破后的瞬间入场。监测特定周期内的阻力线，放量站上阻力线时进场 |
| 404 | `SwingHighToSky` | 突破交易 (Breakout) | 突破行情 (Breakout) | 最高/最低价、波动率突破 | 适合在关键阻力位/压力位被冲破后的瞬间入场。监测特定周期内的阻力线，放量站上阻力线时进场 |
| 405 | `TDSequentialStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 406 | `TEMA` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 407 | `TechnicalExampleStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 408 | `TemaMaster` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 409 | `TemaMaster3` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 410 | `TemaPure` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 411 | `TemaPureNeat` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 412 | `TemaPureTwo` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 413 | `TenderEnter` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 414 | `TheForce` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 415 | `TheRealPullbackV2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 416 | `TrailingBuyStrat2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 417 | `Trend_Strength_Directional` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 418 | `TrixStrategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 419 | `TrixV15Strategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 420 | `TrixV21Strategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 421 | `TrixV23Strategy` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 422 | `UltimateMomentumIndicator` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 423 | `Uptrend` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 424 | `UziChan` | 机器学习/统计增强 (ML/Stat) | 复杂多变市场 | 归一化处理、动态参数 | 适合市场节奏变换较快的情况，动态调整参数。根据当前波动率或市场状态动态修正买卖阈值和止损位 |
| 425 | `UziChan2` | 机器学习/统计增强 (ML/Stat) | 复杂多变市场 | 归一化处理、动态参数 | 适合市场节奏变换较快的情况，动态调整参数。根据当前波动率或市场状态动态修正买卖阈值和止损位 |
| 426 | `VWAP` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 427 | `WaveTrendStra` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 428 | `XebTradeStrat` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 429 | `XtraThicc` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 430 | `YOLO` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 431 | `adaptive` | 机器学习/统计增强 (ML/Stat) | 复杂多变市场 | 归一化处理、动态参数 | 适合市场节奏变换较快的情况，动态调整参数。根据当前波动率或市场状态动态修正买卖阈值和止损位 |
| 432 | `adx_opt_strat` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 433 | `adxbbrsi2` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 434 | `bb_rsi_opt_new` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 435 | `bbema` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 436 | `bbrsi1_strategy` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 437 | `bbrsi4Freq` | 均线回归 (Mean Reversion) | 震荡市场 (Ranging) | 布林带、RSI指标 | 在市场没有明显趋势，价格在区间内波动时表现最佳。利用价格回归均值的统计原理，逢低买入逢高卖出 |
| 438 | `bestV2` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 439 | `botbaby` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 440 | `conny` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 441 | `cryptohassle` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 442 | `custom` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 443 | `custom_sell` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 444 | `e6v34` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 445 | `ema` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 446 | `epretrace` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 447 | `fahmibah` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 448 | `flawless_lambo` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 449 | `hansencandlepatternV1` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 450 | `heikin` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 451 | `hlhb` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 452 | `ichiV1` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 453 | `ichiV1_Marius` | 一目均衡表 (Ichimoku) | 趋势延续/震荡突破 | 云图、基准线、转换线 | 适合单边趋势或从云层突破后的行情。利用云层厚度及延迟线位置判断市场强弱 |
| 454 | `keltnerchannel` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 455 | `mabStra` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 456 | `macd_recovery` | 趋势跟踪 (Trend Following) | 强牛市/强熊市 (Trend) | 均线交叉、ADX强度、SuperTrend | 在有明显方向的单边行情中捕获利润。通过长短周期的价格均线确认方向，金叉买入死叉卖出 |
| 457 | `mark_strat` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 458 | `mark_strat_opt` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 459 | `quantumfirst` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 460 | `redditMA` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 461 | `stoploss` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 462 | `stratfib` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 463 | `strato` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
| 464 | `true_lambo` | 剥头皮 (Scalping) | 高波动 (High Volatility) | 低ROI、紧止损、TEMA | 在极短时间内博取微小点位差，适合波动剧烈的行情。利用1m/5m的高频信号进行快速进出，减少持仓时间风险 |
| 465 | `wtc` | 多指标综合 (General) | 标准环境 | 多指标组合 | 适合一般震荡偏上行市场。基于常规技术指标组合生成的买卖信号 |
