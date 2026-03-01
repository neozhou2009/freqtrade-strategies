# 策略设计思想与评审报告

说明：本报告为静态源码分析推断（不执行策略），以“代码评审”口吻给出设计思想与建议。

**总计分析策略数量:** 471
**重点关注策略(已通过回测):** 87

## 总表（含设计思想列）

| 序号 | 策略名称 | 周期 | 评分 | 可读性 | 风格 | 设计思想(摘要) | 评审概要 | 改进建议 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [CustomStoplossWit...](freqtrade-strategies/strategies/CustomStoplossWithPSAR/CustomStoplossWithPSAR.py) | 1h | 6.5 | 高 | 风控导向 | 基于阈值条件的规则策略；动态风控（自定义止损） | ✅ **重点(已通过回测)**；评分良好；高风险；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 2 | [Macd.py](freqtrade-strategies/strategies/Macd/Macd.py) | 1h | 6.5 | 高 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | ✅ **重点(已通过回测)**；评分良好；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 3 | [KC_BB.py](freqtrade-strategies/strategies/KC_BB/KC_BB.py) | 5m | 6.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | ✅ **重点(已通过回测)**；评分良好；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 4 | [Obelisk_3EMA_Stoc...](freqtrade-strategies/strategies/Obelisk_3EMA_StochRSI_ATR/Obelisk_3EMA_StochRSI_ATR.py) | 5m | 6.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | ✅ **重点(已通过回测)**；评分良好；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 5 | [LookaheadStrategy.py](freqtrade-strategies/strategies/LookaheadStrategy/LookaheadStrategy.py) | 5m | 5.5 | 高 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 6 | [Combined_Indicato...](freqtrade-strategies/strategies/Combined_Indicators/Combined_Indicators.py) | 1m | 5.5 | 高 | 常规 | 通道类策略（布林带/Keltner 等） | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 7 | [ObeliskRSI_v6_1.py](freqtrade-strategies/strategies/ObeliskRSI_v6_1/ObeliskRSI_v6_1.py) | 5m | 5.5 | 中 | 风控导向 | 基于阈值条件的规则策略；动态风控（自定义止损） | ✅ **重点(已通过回测)**；评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 8 | [MACD_TRIPLE_MA.py](freqtrade-strategies/strategies/MACD_TRIPLE_MA/MACD_TRIPLE_MA.py) | 5m | 5.5 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 9 | [XebTradeStrat.py](freqtrade-strategies/strategies/XebTradeStrat/XebTradeStrat.py) | 1m | 5.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 10 | [FixedRiskRewardLo...](freqtrade-strategies/strategies/FixedRiskRewardLoss/FixedRiskRewardLoss.py) | 5m | 5.5 | 中 | 风控导向 | 基于阈值条件的规则策略；动态风控（自定义止损） | ✅ **重点(已通过回测)**；评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 11 | [Scalp.py](freqtrade-strategies/strategies/Scalp/Scalp.py) | 1m | 5.0 | 高 | 常规 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 12 | [MACD_TRI_EMA.py](freqtrade-strategies/strategies/MACD_TRI_EMA/MACD_TRI_EMA.py) | 5m | 5.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 13 | [AverageStrategy.py](freqtrade-strategies/strategies/AverageStrategy/AverageStrategy.py) | 4h | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 14 | [ADX_15M_USDT.py](freqtrade-strategies/strategies/ADX_15M_USDT/ADX_15M_USDT.py) | Unknown | 5.0 | 高 | 常规 | 趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 15 | [BinHV45.py](freqtrade-strategies/strategies/BinHV45/BinHV45.py) | 1m | 5.0 | 高 | 常规 | 通道类策略（布林带/Keltner 等） | ✅ **重点(已通过回测)**；评分一般；逻辑简单；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 16 | [SmoothOperator.py](freqtrade-strategies/strategies/SmoothOperator/SmoothOperator.py) | 5m | 5.0 | 低 | 模板化/堆叠型 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；逻辑复杂；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 17 | [ObeliskIM_v1_1.py](freqtrade-strategies/strategies/ObeliskIM_v1_1/ObeliskIM_v1_1.py) | 5m | 5.0 | 低 | 常规 | 一目均衡的趋势识别 | ✅ **重点(已通过回测)**；评分一般；低风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 18 | [ClucMay72018.py](freqtrade-strategies/strategies/ClucMay72018/ClucMay72018.py) | 5m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 19 | [MACDRSI200.py](freqtrade-strategies/strategies/MACDRSI200/MACDRSI200.py) | Unknown | 5.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 20 | [adaptive.py](freqtrade-strategies/strategies/adaptive/adaptive.py) | 5m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 21 | [MultiRSI.py](freqtrade-strategies/strategies/MultiRSI/MultiRSI.py) | 5m | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润 |
| 22 | [BreakEven.py](freqtrade-strategies/strategies/BreakEven/BreakEven.py) | 5m | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 23 | [Obelisk_TradePro_...](freqtrade-strategies/strategies/Obelisk_TradePro_Ichi_v1_1/Obelisk_TradePro_Ichi_v1_1.py) | 1h | 5.0 | 中 | 常规 | 一目均衡的趋势识别 | ✅ **重点(已通过回测)**；评分一般；低风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 24 | [MFI.py](freqtrade-strategies/strategies/MFI/MFI.py) | 5m | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 25 | [BBRSI4cust.py](freqtrade-strategies/strategies/BBRSI4cust/BBRSI4cust.py) | 15m | 5.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖 | ✅ **重点(已通过回测)**；评分一般；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 26 | [EMASkipPump.py](freqtrade-strategies/strategies/EMASkipPump/EMASkipPump.py) | 5m | 5.0 | 高 | 常规 | 通道类策略（布林带/Keltner 等） | ✅ **重点(已通过回测)**；评分一般；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 27 | [VWAP.py](freqtrade-strategies/strategies/VWAP/VWAP.py) | 5m | 5.0 | 高 | 常规 | 围绕 VWAP 的回归/基准定价 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 28 | [Low_BB.py](freqtrade-strategies/strategies/Low_BB/Low_BB.py) | 1m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；低风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 29 | [Leveraged.py](freqtrade-strategies/strategies/Leveraged/Leveraged.py) | 5m | 5.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 30 | [macd_recovery.py](freqtrade-strategies/strategies/macd_recovery/macd_recovery.py) | Unknown | 5.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 31 | [CMCWinner.py](freqtrade-strategies/strategies/CMCWinner/CMCWinner.py) | 15m | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 32 | [UziChan.py](freqtrade-strategies/strategies/UziChan/UziChan.py) | 5m | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突 |
| 33 | [heikin.py](freqtrade-strategies/strategies/heikin/heikin.py) | 1h | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 34 | [hansencandlepatte...](freqtrade-strategies/strategies/hansencandlepatternV1/hansencandlepatternV1.py) | 1h | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 35 | [ReinforcedQuickie.py](freqtrade-strategies/strategies/ReinforcedQuickie/ReinforcedQuickie.py) | 5m | 5.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 36 | [EMAVolume.py](freqtrade-strategies/strategies/EMAVolume/EMAVolume.py) | Unknown | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 37 | [AlligatorStrat.py](freqtrade-strategies/strategies/AlligatorStrat/AlligatorStrat.py) | Unknown | 5.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 38 | [BbandRsiRolling.py](freqtrade-strategies/strategies/BbandRsiRolling/BbandRsiRolling.py) | 5m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 39 | [BinHV45HO.py](freqtrade-strategies/strategies/BinHV45HO/BinHV45HO.py) | 1m | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 40 | [ReinforcedSmoothS...](freqtrade-strategies/strategies/ReinforcedSmoothScalp/ReinforcedSmoothScalp.py) | 1m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 41 | [CCIStrategy.py](freqtrade-strategies/strategies/CCIStrategy/CCIStrategy.py) | 1m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | ✅ **重点(已通过回测)**；评分一般；低风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 42 | [BBRSI3366.py](freqtrade-strategies/strategies/BBRSI3366/BBRSI3366.py) | 5m | 4.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 43 | [Ichimoku_v32.py](freqtrade-strategies/strategies/Ichimoku_v32/Ichimoku_v32.py) | Unknown | 4.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 44 | [BBRSI21.py](freqtrade-strategies/strategies/BBRSI21/BBRSI21.py) | 5m | 4.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 45 | [Ichimoku_v30.py](freqtrade-strategies/strategies/Ichimoku_v30/Ichimoku_v30.py) | Unknown | 4.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 46 | [SwingHigh.py](freqtrade-strategies/strategies/SwingHigh/SwingHigh.py) | Unknown | 4.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 47 | [DD.py](freqtrade-strategies/strategies/DD/DD.py) | 5m | 4.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 48 | [adxbbrsi2.py](freqtrade-strategies/strategies/adxbbrsi2/adxbbrsi2.py) | 1h | 4.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 49 | [Ichimoku_v33.py](freqtrade-strategies/strategies/Ichimoku_v33/Ichimoku_v33.py) | Unknown | 4.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 50 | [Trend_Strength_Di...](freqtrade-strategies/strategies/Trend_Strength_Directional/Trend_Strength_Directional.py) | 15m | 4.5 | 中 | 常规 | 趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 51 | [adx_opt_strat.py](freqtrade-strategies/strategies/adx_opt_strat/adx_opt_strat.py) | Unknown | 4.5 | 高 | 常规 | 趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 52 | [Bandtastic.py](freqtrade-strategies/strategies/Bandtastic/Bandtastic.py) | 15m | 4.5 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖 | ✅ **重点(已通过回测)**；评分一般；高风险；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 53 | [Ichimoku_v12.py](freqtrade-strategies/strategies/Ichimoku_v12/Ichimoku_v12.py) | Unknown | 4.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 54 | [e6v34.py](freqtrade-strategies/strategies/e6v34/e6v34.py) | 15m | 4.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 55 | [ADX_15M_USDT2.py](freqtrade-strategies/strategies/ADX_15M_USDT2/ADX_15M_USDT2.py) | Unknown | 4.0 | 高 | 常规 | 趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 56 | [HourBasedStrategy.py](freqtrade-strategies/strategies/HourBasedStrategy/HourBasedStrategy.py) | 1h | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 57 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOpt/SMAOffsetProtectOpt.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 58 | [WaveTrendStra.py](freqtrade-strategies/strategies/WaveTrendStra/WaveTrendStra.py) | 4h | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 59 | [CofiBitStrategy.py](freqtrade-strategies/strategies/CofiBitStrategy/CofiBitStrategy.py) | 5m | 4.0 | 高 | 常规 | 动量/均线趋势跟随；趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 60 | [Roth03.py](freqtrade-strategies/strategies/Roth03/Roth03.py) | 5m | 4.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 61 | [Quickie.py](freqtrade-strategies/strategies/Quickie/Quickie.py) | 5m | 4.0 | 高 | 常规 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 62 | [ASDTSRockwellTrad...](freqtrade-strategies/strategies/ASDTSRockwellTrading/ASDTSRockwellTrading.py) | 5m | 4.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 63 | [SmoothScalp.py](freqtrade-strategies/strategies/SmoothScalp/SmoothScalp.py) | 1m | 4.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 64 | [Roth01.py](freqtrade-strategies/strategies/Roth01/Roth01.py) | 5m | 4.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 65 | [ADXMomentum.py](freqtrade-strategies/strategies/ADXMomentum/ADXMomentum.py) | 1h | 4.0 | 高 | 常规 | 趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 66 | [Simple.py](freqtrade-strategies/strategies/Simple/Simple.py) | 5m | 4.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 67 | [keltnerchannel.py](freqtrade-strategies/strategies/keltnerchannel/keltnerchannel.py) | 6h | 4.0 | 中 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 68 | [BbandRsi.py](freqtrade-strategies/strategies/BbandRsi/BbandRsi.py) | 1h | 4.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 69 | [Cci.py](freqtrade-strategies/strategies/Cci/Cci.py) | 1m | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 70 | [AdxSmas.py](freqtrade-strategies/strategies/AdxSmas/AdxSmas.py) | 1h | 4.0 | 高 | 常规 | 动量/均线趋势跟随；趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 71 | [Chispei.py](freqtrade-strategies/strategies/Chispei/Chispei.py) | Unknown | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 72 | [AwesomeMacd.py](freqtrade-strategies/strategies/AwesomeMacd/AwesomeMacd.py) | 1h | 4.0 | 高 | 常规 | 动量/均线趋势跟随；趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 73 | [SwingHighToSky.py](freqtrade-strategies/strategies/SwingHighToSky/SwingHighToSky.py) | 15m | 4.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 74 | [MACDCCI.py](freqtrade-strategies/strategies/MACDCCI/MACDCCI.py) | Unknown | 4.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 75 | [BinHV27.py](freqtrade-strategies/strategies/BinHV27/BinHV27.py) | 5m | 4.0 | 中 | 常规 | 动量/均线趋势跟随；趋势强度过滤 | ✅ **重点(已通过回测)**；评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 76 | [MACD_EMA.py](freqtrade-strategies/strategies/MACD_EMA/MACD_EMA.py) | 5m | 4.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 77 | [Ichess.py](freqtrade-strategies/strategies/Ichess/Ichess.py) | 1d | 4.0 | 中 | 常规 | 一目均衡的趋势识别 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 78 | [MACDStrategy_cros...](freqtrade-strategies/strategies/MACDStrategy_crossed/MACDStrategy_crossed.py) | 5m | 4.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 79 | [MACDStrategy.py](freqtrade-strategies/strategies/MACDStrategy/MACDStrategy.py) | 5m | 4.0 | 高 | 常规 | 动量/均线趋势跟随 | ✅ **重点(已通过回测)**；评分一般；高风险；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制 |
| 80 | [HansenSmaOffsetV1.py](freqtrade-strategies/strategies/HansenSmaOffsetV1/HansenSmaOffsetV1.py) | 15m | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 81 | [JustROCR6.py](freqtrade-strategies/strategies/JustROCR6/JustROCR6.py) | Unknown | 3.5 | 高 | 常规 | 动量突破 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 82 | [JustROCR3.py](freqtrade-strategies/strategies/JustROCR3/JustROCR3.py) | Unknown | 3.5 | 高 | 常规 | 动量突破 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 83 | [JustROCR.py](freqtrade-strategies/strategies/JustROCR/JustROCR.py) | Unknown | 3.5 | 高 | 常规 | 动量突破 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 84 | [TechnicalExampleS...](freqtrade-strategies/strategies/TechnicalExampleStrategy/TechnicalExampleStrategy.py) | 5m | 3.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 85 | [Stavix2.py](freqtrade-strategies/strategies/Stavix2/Stavix2.py) | Unknown | 3.0 | 高 | 常规 | 一目均衡的趋势识别 | ✅ **重点(已通过回测)**；评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 86 | [JustROCR5.py](freqtrade-strategies/strategies/JustROCR5/JustROCR5.py) | 1m | 3.0 | 高 | 常规 | 动量突破 | ✅ **重点(已通过回测)**；评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 87 | [AlwaysBuy.py](freqtrade-strategies/strategies/AlwaysBuy/AlwaysBuy.py) | 5m | 1.0 | 高 | 常规 | 基于阈值条件的规则策略 | ✅ **重点(已通过回测)**；评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 88 | [AlexNexusForgeV8A...](user_data/strategies/AlexNexusForgeV8AIV2.py) | 1h | 9.5 | 中 | 实验性/研究型 | 动量/均线趋势跟随；机器学习/特征工程驱动；多周期确认；动态风控（自定义止损） | 评分优秀；高风险；逻辑复杂；多周期 | 止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 89 | [AlexNexusForgeV8A...](user_data/strategies/AlexNexusForgeV8AIV3.py) | 1h | 9.5 | 中 | 实验性/研究型 | 动量/均线趋势跟随；机器学习/特征工程驱动；多周期确认；动态风控（自定义止损） | 评分优秀；逻辑复杂；多周期 | 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 90 | [MultiMA_TSL.py](freqtrade-strategies/strategies/MultiMA_TSL/MultiMA_TSL.py) | 5m | 8.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分优秀；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 91 | [Momentumv2.py](freqtrade-strategies/strategies/Momentumv2/Momentumv2.py) | 4h | 8.0 | 高 | 风控导向 | 动量/均线趋势跟随；动态风控（自定义止损）；保护机制防极端行情 | 评分优秀；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 92 | [BB_RPB_TSL_SMA_Tr...](freqtrade-strategies/strategies/BB_RPB_TSL_SMA_Tranz_TB_MOD/BB_RPB_TSL_SMA_Tranz_TB_MOD.py) | 5m | 8.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分优秀；高风险；逻辑复杂；多周期 | 建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 93 | [MultiMA_TSL3.py](freqtrade-strategies/strategies/MultiMA_TSL3/MultiMA_TSL3.py) | 5m | 8.0 | 低 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分优秀；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 94 | [MultiMA_TSL3_Mod.py](freqtrade-strategies/strategies/MultiMA_TSL3_Mod/MultiMA_TSL3_Mod.py) | 5m | 8.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分优秀；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 95 | [AlexNexusForgeV7.py](user_data/strategies/AlexNexusForgeV7.py) | 1h | 8.0 | 中 | 风控导向 | 动量/均线趋势跟随；趋势强度过滤；动态风控（自定义止损）；保护机制防极端行情 | 评分优秀；lint禁用 | 建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 96 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV6H/CombinedBinHAndClucV6H.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 97 | [BcmbigzDevelop.py](freqtrade-strategies/strategies/BcmbigzDevelop/BcmbigzDevelop.py) | 5m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 98 | [BinClucMadDevelop.py](freqtrade-strategies/strategies/BinClucMadDevelop/BinClucMadDevelop.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 99 | [BigPete.py](freqtrade-strategies/strategies/BigPete/BigPete.py) | 5m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 100 | [MADisplaceV3.py](freqtrade-strategies/strategies/MADisplaceV3/MADisplaceV3.py) | 5m | 7.0 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认；动态风控（自定义止损） | 评分良好；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 101 | [ElliotV8_original...](freqtrade-strategies/strategies/ElliotV8_original_ichiv3/ElliotV8_original_ichiv3.py) | 5m | 7.0 | 高 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认；保护机制防极端行情 | 评分良好；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 102 | [FRAYSTRAT.py](freqtrade-strategies/strategies/FRAYSTRAT/FRAYSTRAT.py) | 15m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；保护机制防极端行情 | 评分良好；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 103 | [CryptoFrog.py](freqtrade-strategies/strategies/CryptoFrog/CryptoFrog.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 104 | [ElliotV5HO.py](freqtrade-strategies/strategies/ElliotV5HO/ElliotV5HO.py) | 5m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 105 | [GodCard.py](freqtrade-strategies/strategies/GodCard/GodCard.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；保护机制防极端行情 | 评分良好；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 106 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8Hyper/CombinedBinHAndClucV8Hyper.py) | 5m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 107 | [CryptoFrogHO2A.py](freqtrade-strategies/strategies/CryptoFrogHO2A/CryptoFrogHO2A.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 108 | [ElliotV5HOMod2.py](freqtrade-strategies/strategies/ElliotV5HOMod2/ElliotV5HOMod2.py) | 5m | 7.0 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认；动态风控（自定义止损） | 评分良好；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 109 | [NormalizerStrateg...](freqtrade-strategies/strategies/NormalizerStrategyHO2/NormalizerStrategyHO2.py) | 1h | 7.0 | 高 | 风控导向 | 趋势持有 + 移动止损跟踪；动态风控（自定义止损） | 评分良好；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 110 | [ElliotV8_original...](freqtrade-strategies/strategies/ElliotV8_original_ichiv2/ElliotV8_original_ichiv2.py) | 5m | 7.0 | 高 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认；保护机制防极端行情 | 评分良好；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 111 | [Combined_NFIv6_SM...](freqtrade-strategies/strategies/Combined_NFIv6_SMA/Combined_NFIv6_SMA.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 112 | [NormalizerStrateg...](freqtrade-strategies/strategies/NormalizerStrategy/NormalizerStrategy.py) | 1h | 7.0 | 高 | 风控导向 | 趋势持有 + 移动止损跟踪；动态风控（自定义止损） | 评分良好；逻辑简单；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 113 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV6/CombinedBinHAndClucV6.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 114 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV5Hyperoptable/CombinedBinHAndClucV5Hyperoptable.py) | 5m | 7.0 | 中 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认；动态风控（自定义止损） | 评分良好；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 115 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV5/CombinedBinHAndClucV5.py) | 5m | 7.0 | 中 | 风控导向 | 通道类策略（布林带/Keltner 等）；动态风控（自定义止损） | 评分良好；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 116 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV7/CombinedBinHAndClucV7.py) | 5m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 117 | [CryptoFrogHO2.py](freqtrade-strategies/strategies/CryptoFrogHO2/CryptoFrogHO2.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 118 | [EI3v2_tag_cofi_gr...](freqtrade-strategies/strategies/EI3v2_tag_cofi_green/EI3v2_tag_cofi_green.py) | 5m | 7.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认；保护机制防极端行情 | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 119 | [NASOSv4.py](freqtrade-strategies/strategies/NASOSv4/NASOSv4.py) | 5m | 7.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 120 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV3/CombinedBinHAndClucV3.py) | 5m | 7.0 | 高 | 风控导向 | 通道类策略（布林带/Keltner 等）；动态风控（自定义止损） | 评分良好 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 121 | [CryptoFrogHO.py](freqtrade-strategies/strategies/CryptoFrogHO/CryptoFrogHO.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 122 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV4/CombinedBinHAndClucV4.py) | 5m | 7.0 | 中 | 风控导向 | 通道类策略（布林带/Keltner 等）；动态风控（自定义止损） | 评分良好；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 123 | [CryptoFrogOffset.py](freqtrade-strategies/strategies/CryptoFrogOffset/CryptoFrogOffset.py) | 5m | 7.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 124 | [AlexNexusForgeV6.py](user_data/strategies/AlexNexusForgeV6.py) | 1h | 7.0 | 中 | 常规 | 动量/均线趋势跟随；趋势强度过滤；保护机制防极端行情 | 评分良好；lint禁用 | 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 125 | [AlexNexusForgeV4.py](user_data/strategies/AlexNexusForgeV4.py) | 1h | 7.0 | 中 | 常规 | 趋势持有 + 移动止损跟踪；保护机制防极端行情 | 评分良好；低风险；lint禁用 | 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 126 | [NFIX_BB_RPB.py](freqtrade-strategies/strategies/NFIX_BB_RPB/NFIX_BB_RPB.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 127 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV9/CombinedBinHClucAndMADV9.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 128 | [ClucHAnix_hhll.py](freqtrade-strategies/strategies/ClucHAnix_hhll/ClucHAnix_hhll.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 129 | [BigZ07.py](freqtrade-strategies/strategies/BigZ07/BigZ07.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 130 | [SMAOffsetV2.py](freqtrade-strategies/strategies/SMAOffsetV2/SMAOffsetV2.py) | 5m | 6.5 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分良好；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 131 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8XH/CombinedBinHAndClucV8XH.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 132 | [BigZ03HO.py](freqtrade-strategies/strategies/BigZ03HO/BigZ03HO.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 133 | [HyperStra_GSN_SMA...](freqtrade-strategies/strategies/HyperStra_GSN_SMAOnly/HyperStra_GSN_SMAOnly.py) | 5m | 6.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；保护机制防极端行情 | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 134 | [BB_RPB_TSL_BI.py](freqtrade-strategies/strategies/BB_RPB_TSL_BI/BB_RPB_TSL_BI.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 135 | [NASOSRv6_private_...](freqtrade-strategies/strategies/NASOSRv6_private_Reinuvader_20211121/NASOSRv6_private_Reinuvader_20211121.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 136 | [BigZ03.py](freqtrade-strategies/strategies/BigZ03/BigZ03.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 137 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD_E0V1E_ROI/ClucHAnix_BB_RPB_MOD_E0V1E_ROI.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 138 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyLite/NotAnotherSMAOffsetStrategyLite.py) | 5m | 6.5 | 高 | 风控导向 | 基于阈值条件的规则策略；动态风控（自定义止损） | 评分良好；逻辑简单；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 139 | [BinClucMadV1.py](freqtrade-strategies/strategies/BinClucMadV1/BinClucMadV1.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 140 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucHyperV3/CombinedBinHAndClucHyperV3.py) | 1m | 6.5 | 中 | 风控导向 | 通道类策略（布林带/Keltner 等）；动态风控（自定义止损） | 评分良好 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 141 | [BB_RPB_TSL_RNG_2.py](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_2/BB_RPB_TSL_RNG_2.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 142 | [BB_RPB_TSL_RNG_VW...](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_VWAP/BB_RPB_TSL_RNG_VWAP.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 143 | [BB_RPB_TSL_RNG.py](freqtrade-strategies/strategies/BB_RPB_TSL_RNG/BB_RPB_TSL_RNG.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 144 | [MostOfAll.py](freqtrade-strategies/strategies/MostOfAll/MostOfAll.py) | 5m | 6.5 | 高 | 风控导向 | 基于阈值条件的规则策略；动态风控（自定义止损） | 评分良好；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 145 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD/ClucHAnix_BB_RPB_MOD.py) | 1m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 146 | [BcmbigzV1.py](freqtrade-strategies/strategies/BcmbigzV1/BcmbigzV1.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 147 | [BigZ04HO2.py](freqtrade-strategies/strategies/BigZ04HO2/BigZ04HO2.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 148 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD2_ROI/ClucHAnix_BB_RPB_MOD2_ROI.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 149 | [NFI46FrogZ.py](freqtrade-strategies/strategies/NFI46FrogZ/NFI46FrogZ.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 150 | [BigZ0407.py](freqtrade-strategies/strategies/BigZ0407/BigZ0407.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 151 | [BigZ04_TSL3.py](freqtrade-strategies/strategies/BigZ04_TSL3/BigZ04_TSL3.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 152 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV3/CombinedBinHClucAndMADV3.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 153 | [BBRSIv2.py](freqtrade-strategies/strategies/BBRSIv2/BBRSIv2.py) | 15m | 6.5 | 高 | 风控导向 | 布林带+RSI 的均值回归/超买超卖；动态风控（自定义止损） | 评分良好 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 154 | [BigZ04.py](freqtrade-strategies/strategies/BigZ04/BigZ04.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 155 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV6/CombinedBinHClucAndMADV6.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 156 | [BinClucMad.py](freqtrade-strategies/strategies/BinClucMad/BinClucMad.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 157 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV5/CombinedBinHClucAndMADV5.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 158 | [BB_RPB_TSL_RNG_TB...](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_TBS_GOLD/BB_RPB_TSL_RNG_TBS_GOLD.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；低风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 159 | [BigZ0307HO.py](freqtrade-strategies/strategies/BigZ0307HO/BigZ0307HO.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 160 | [BB_RPB_TSL_c7c477...](freqtrade-strategies/strategies/BB_RPB_TSL_c7c477d_20211030/BB_RPB_TSL_c7c477d_20211030.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 161 | [BigZ0407HO.py](freqtrade-strategies/strategies/BigZ0407HO/BigZ0407HO.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 162 | [NASOSv5.py](freqtrade-strategies/strategies/NASOSv5/NASOSv5.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 163 | [ClucHAnix_5m.py](freqtrade-strategies/strategies/ClucHAnix_5m/ClucHAnix_5m.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 164 | [NFI46Z.py](freqtrade-strategies/strategies/NFI46Z/NFI46Z.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 165 | [ClucHAnix5m.py](freqtrade-strategies/strategies/ClucHAnix5m/ClucHAnix5m.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 166 | [BBMod1.py](freqtrade-strategies/strategies/BBMod1/BBMod1.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 167 | [BB_RPB_TSL_2.py](freqtrade-strategies/strategies/BB_RPB_TSL_2/BB_RPB_TSL_2.py) | 3m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 168 | [true_lambo.py](freqtrade-strategies/strategies/true_lambo/true_lambo.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 169 | [NFIX_BB_RPB_c7c47...](freqtrade-strategies/strategies/NFIX_BB_RPB_c7c477d_20211030/NFIX_BB_RPB_c7c477d_20211030.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 170 | [MacheteV8bRallimo...](freqtrade-strategies/strategies/MacheteV8bRallimod2/MacheteV8bRallimod2.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 171 | [BB_RPB_TSL_BIV1.py](freqtrade-strategies/strategies/BB_RPB_TSL_BIV1/BB_RPB_TSL_BIV1.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 172 | [BigZ04_TSL4.py](freqtrade-strategies/strategies/BigZ04_TSL4/BigZ04_TSL4.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 173 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucHyperV0/CombinedBinHAndClucHyperV0.py) | 1m | 6.5 | 中 | 风控导向 | 通道类策略（布林带/Keltner 等）；动态风控（自定义止损） | 评分良好 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 174 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD_CTT/ClucHAnix_BB_RPB_MOD_CTT.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 175 | [ClucHAnix.py](freqtrade-strategies/strategies/ClucHAnix/ClucHAnix.py) | 1m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 176 | [BB_RPB_TSL.py](freqtrade-strategies/strategies/BB_RPB_TSL/BB_RPB_TSL.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 177 | [BB_RPB_TSLmeneguz...](freqtrade-strategies/strategies/BB_RPB_TSLmeneguzzo/BB_RPB_TSLmeneguzzo.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 178 | [HyperStra_SMAOnly.py](freqtrade-strategies/strategies/HyperStra_SMAOnly/HyperStra_SMAOnly.py) | 5m | 6.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；保护机制防极端行情 | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 179 | [BigZ04HO.py](freqtrade-strategies/strategies/BigZ04HO/BigZ04HO.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 180 | [Uptrend.py](freqtrade-strategies/strategies/Uptrend/Uptrend.py) | 5m | 6.5 | 低 | 模板化/堆叠型 | 基于阈值条件的规则策略；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 181 | [BB_RPB_TSL_RNG_TB...](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_TBS/BB_RPB_TSL_RNG_TBS.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 182 | [ClucHAnix_5m1.py](freqtrade-strategies/strategies/ClucHAnix_5m1/ClucHAnix_5m1.py) | 5m | 6.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 183 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8XHO/CombinedBinHAndClucV8XHO.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 184 | [BB_RPB_TSL_Tranz.py](freqtrade-strategies/strategies/BB_RPB_TSL_Tranz/BB_RPB_TSL_Tranz.py) | 5m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 185 | [BigZ06.py](freqtrade-strategies/strategies/BigZ06/BigZ06.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 186 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8/CombinedBinHAndClucV8.py) | 5m | 6.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 187 | [MacheteV8b.py](freqtrade-strategies/strategies/MacheteV8b/MacheteV8b.py) | 15m | 6.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 188 | [CryptoFrogHO3A4.py](freqtrade-strategies/strategies/CryptoFrogHO3A4/CryptoFrogHO3A4.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 189 | [CryptoFrogNFIHO1A.py](freqtrade-strategies/strategies/CryptoFrogNFIHO1A/CryptoFrogNFIHO1A.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 190 | [CryptoFrogHO3A3.py](freqtrade-strategies/strategies/CryptoFrogHO3A3/CryptoFrogHO3A3.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 191 | [CryptoFrogHO3A1.py](freqtrade-strategies/strategies/CryptoFrogHO3A1/CryptoFrogHO3A1.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 192 | [NASOSv5_mod1_DanM...](freqtrade-strategies/strategies/NASOSv5_mod1_DanMod/NASOSv5_mod1_DanMod.py) | 5m | 6.0 | 低 | 工程化/多周期 | 围绕 VWAP 的回归/基准定价；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 193 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyModHO/NotAnotherSMAOffsetStrategyModHO.py) | 5m | 6.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 194 | [epretrace.py](freqtrade-strategies/strategies/epretrace/epretrace.py) | 5m | 6.0 | 中 | 风控导向 | 一目均衡的趋势识别；动量/均线趋势跟随；动态风控（自定义止损） | 评分良好；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 195 | [CryptoFrogNFI.py](freqtrade-strategies/strategies/CryptoFrogNFI/CryptoFrogNFI.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 196 | [MiniLambo.py](freqtrade-strategies/strategies/MiniLambo/MiniLambo.py) | 1m | 6.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分良好；逻辑复杂；多周期 | 建议评估开启移动止损，用于锁定利润；建议启用主动离场信号或补充退出条件；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 197 | [Apollo11.py](freqtrade-strategies/strategies/Apollo11/Apollo11.py) | 15m | 6.0 | 中 | 风控导向 | 动量/均线趋势跟随；动态风控（自定义止损）；保护机制防极端行情 | 评分良好；高风险 | 建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 198 | [NASOSv5_mod3.py](freqtrade-strategies/strategies/NASOSv5_mod3/NASOSv5_mod3.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 199 | [BinClucMadSMADeve...](freqtrade-strategies/strategies/BinClucMadSMADevelop/BinClucMadSMADevelop.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 200 | [HarmonicDivergenc...](freqtrade-strategies/strategies/HarmonicDivergence/HarmonicDivergence.py) | 15m | 6.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 201 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901/NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901.py) | 5m | 6.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 202 | [ElliotV7.py](freqtrade-strategies/strategies/ElliotV7/ElliotV7.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 203 | [NASOSv5_mod2.py](freqtrade-strategies/strategies/NASOSv5_mod2/NASOSv5_mod2.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 204 | [PRICEFOLLOWINGX.py](freqtrade-strategies/strategies/PRICEFOLLOWINGX/PRICEFOLLOWINGX.py) | 15m | 6.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；保护机制防极端行情 | 评分良好；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 205 | [BBRSITV.py](freqtrade-strategies/strategies/BBRSITV/BBRSITV.py) | 5m | 6.0 | 中 | 风控导向 | 趋势持有 + 移动止损跟踪；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 206 | [NASOSv5_mod1.py](freqtrade-strategies/strategies/NASOSv5_mod1/NASOSv5_mod1.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 207 | [wtc.py](freqtrade-strategies/strategies/wtc/wtc.py) | 30m | 6.0 | 中 | 实验性/研究型 | 机器学习/特征工程驱动 | 评分良好；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 208 | [CoreStrategy.py](freqtrade-strategies/strategies/CoreStrategy/CoreStrategy.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 209 | [CryptoFrogHO3A2.py](freqtrade-strategies/strategies/CryptoFrogHO3A2/CryptoFrogHO3A2.py) | 5m | 6.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分良好；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 210 | [Inverse.py](freqtrade-strategies/strategies/Inverse/Inverse.py) | 1h | 5.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 211 | [Combined_NFIv7_SM...](freqtrade-strategies/strategies/Combined_NFIv7_SMA_Rallipanos_20210707/Combined_NFIv7_SMA_Rallipanos_20210707.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 212 | [Heracles.py](freqtrade-strategies/strategies/Heracles/Heracles.py) | 12h | 5.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；低风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 213 | [SampleStrategyV2.py](freqtrade-strategies/strategies/SampleStrategyV2/SampleStrategyV2.py) | 5m | 5.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 214 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_SMA/NostalgiaForInfinityV7_SMA.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 215 | [RalliV1_disable56.py](freqtrade-strategies/strategies/RalliV1_disable56/RalliV1_disable56.py) | 5m | 5.5 | 低 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 216 | [PRICEFOLLOWING2.py](freqtrade-strategies/strategies/PRICEFOLLOWING2/PRICEFOLLOWING2.py) | 15m | 5.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 217 | [EMA520015_V17.py](freqtrade-strategies/strategies/EMA520015_V17/EMA520015_V17.py) | 4h | 5.5 | 高 | 常规 | 动量/均线趋势跟随 | 评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 218 | [Hacklemore3.py](freqtrade-strategies/strategies/Hacklemore3/Hacklemore3.py) | 5m | 5.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 219 | [SMA_BBRSI.py](freqtrade-strategies/strategies/SMA_BBRSI/SMA_BBRSI.py) | 5m | 5.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 220 | [TemaMaster3.py](freqtrade-strategies/strategies/TemaMaster3/TemaMaster3.py) | 1m | 5.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 221 | [Combined_NFIv7_SM...](freqtrade-strategies/strategies/Combined_NFIv7_SMA/Combined_NFIv7_SMA.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 222 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategy_uzi/NotAnotherSMAOffsetStrategy_uzi.py) | 5m | 5.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 223 | [DIV_v1.py](freqtrade-strategies/strategies/DIV_v1/DIV_v1.py) | 5m | 5.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 224 | [RalliV1.py](freqtrade-strategies/strategies/RalliV1/RalliV1.py) | 5m | 5.5 | 低 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 225 | [BBlower.py](freqtrade-strategies/strategies/BBlower/BBlower.py) | 5m | 5.5 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 226 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategy_uzi3/NotAnotherSMAOffsetStrategy_uzi3.py) | 5m | 5.5 | 低 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；逻辑复杂；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 227 | [ClucHAwerk.py](freqtrade-strategies/strategies/ClucHAwerk/ClucHAwerk.py) | 1m | 5.5 | 中 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随；多周期确认 | 评分一般；低风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 228 | [Obelisk_TradePro_...](freqtrade-strategies/strategies/Obelisk_TradePro_Ichi_v2_1/Obelisk_TradePro_Ichi_v2_1.py) | 1h | 5.5 | 中 | 常规 | 一目均衡的趋势识别；动量突破 | 评分一般 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 229 | [StochRSITEMA.py](freqtrade-strategies/strategies/StochRSITEMA/StochRSITEMA.py) | 5m | 5.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；低风险；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 230 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_SMAv2/NostalgiaForInfinityV7_SMAv2.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 231 | [SMAOffset.py](freqtrade-strategies/strategies/SMAOffset/SMAOffset.py) | 5m | 5.5 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 232 | [SlowPotato.py](freqtrade-strategies/strategies/SlowPotato/SlowPotato.py) | 5m | 5.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 233 | [ActionZone.py](freqtrade-strategies/strategies/ActionZone/ActionZone.py) | 1d | 5.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 234 | [NFI46Frog.py](freqtrade-strategies/strategies/NFI46Frog/NFI46Frog.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 235 | [InverseV2.py](freqtrade-strategies/strategies/InverseV2/InverseV2.py) | 1h | 5.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 236 | [Obelisk_Ichimoku_...](freqtrade-strategies/strategies/Obelisk_Ichimoku_Slow_v1_3/Obelisk_Ichimoku_Slow_v1_3.py) | 1h | 5.5 | 低 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 237 | [NFINextMultiOffse...](freqtrade-strategies/strategies/NFINextMultiOffsetAndHO2/NFINextMultiOffsetAndHO2.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 238 | [BBRSI2.py](freqtrade-strategies/strategies/BBRSI2/BBRSI2.py) | 1m | 5.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 239 | [MarketChyperHyper...](freqtrade-strategies/strategies/MarketChyperHyperStrategy/MarketChyperHyperStrategy.py) | 1h | 5.5 | 低 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；高风险；逻辑复杂；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 240 | [NFI5MOHO_WIP_1.py](freqtrade-strategies/strategies/NFI5MOHO_WIP_1/NFI5MOHO_WIP_1.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 241 | [Hacklemore2.py](freqtrade-strategies/strategies/Hacklemore2/Hacklemore2.py) | 15m | 5.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 242 | [ElliotV8HO.py](freqtrade-strategies/strategies/ElliotV8HO/ElliotV8HO.py) | 5m | 5.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 243 | [NFI5MOHO.py](freqtrade-strategies/strategies/NFI5MOHO/NFI5MOHO.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 244 | [bestV2.py](freqtrade-strategies/strategies/bestV2/bestV2.py) | 5m | 5.5 | 高 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 245 | [NFI5MOHO_WIP_2.py](freqtrade-strategies/strategies/NFI5MOHO_WIP_2/NFI5MOHO_WIP_2.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 246 | [flawless_lambo.py](freqtrade-strategies/strategies/flawless_lambo/flawless_lambo.py) | 15m | 5.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；保护机制防极端行情 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 247 | [cryptohassle.py](freqtrade-strategies/strategies/cryptohassle/cryptohassle.py) | Unknown | 5.5 | 高 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 248 | [Combined_NFIv7_SM...](freqtrade-strategies/strategies/Combined_NFIv7_SMA_bAdBoY_20211204/Combined_NFIv7_SMA_bAdBoY_20211204.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 249 | [Cluc7werk.py](freqtrade-strategies/strategies/Cluc7werk/Cluc7werk.py) | 1m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；低风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 250 | [TemaPureTwo.py](freqtrade-strategies/strategies/TemaPureTwo/TemaPureTwo.py) | 5m | 5.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 251 | [NFI4Frog.py](freqtrade-strategies/strategies/NFI4Frog/NFI4Frog.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 252 | [PRICEFOLLOWING.py](freqtrade-strategies/strategies/PRICEFOLLOWING/PRICEFOLLOWING.py) | 5m | 5.5 | 低 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 253 | [Guacamole.py](freqtrade-strategies/strategies/Guacamole/Guacamole.py) | 5m | 5.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 254 | [ElliotV2.py](freqtrade-strategies/strategies/ElliotV2/ElliotV2.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 255 | [TrixV21Strategy.py](freqtrade-strategies/strategies/TrixV21Strategy/TrixV21Strategy.py) | 1h | 5.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 256 | [Divergences.py](freqtrade-strategies/strategies/Divergences/Divergences.py) | 1h | 5.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 257 | [Ichimoku.py](freqtrade-strategies/strategies/Ichimoku/Ichimoku.py) | 5m | 5.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 258 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyX1/NotAnotherSMAOffsetStrategyX1.py) | 5m | 5.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 259 | [TemaPure.py](freqtrade-strategies/strategies/TemaPure/TemaPure.py) | 5m | 5.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 260 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_SMAv2_1/NostalgiaForInfinityV7_SMAv2_1.py) | 5m | 5.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 261 | [BB_RSI.py](freqtrade-strategies/strategies/BB_RSI/BB_RSI.py) | Unknown | 5.5 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 262 | [TemaPureNeat.py](freqtrade-strategies/strategies/TemaPureNeat/TemaPureNeat.py) | 5m | 5.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 263 | [TemaMaster.py](freqtrade-strategies/strategies/TemaMaster/TemaMaster.py) | 5m | 5.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 264 | [ONUR.py](freqtrade-strategies/strategies/ONUR/ONUR.py) | 15m | 5.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 265 | [TrixV23Strategy.py](freqtrade-strategies/strategies/TrixV23Strategy/TrixV23Strategy.py) | 1h | 5.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 266 | [Ichimoku_SenkouSp...](freqtrade-strategies/strategies/Ichimoku_SenkouSpanCross/Ichimoku_SenkouSpanCross.py) | 4h | 5.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 267 | [BB_RPB_TSL_SMA_Tr...](freqtrade-strategies/strategies/BB_RPB_TSL_SMA_Tranz/BB_RPB_TSL_SMA_Tranz.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 268 | [Persia.py](freqtrade-strategies/strategies/Persia/Persia.py) | 5m | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 269 | [STRATEGY_RSI_BB_B...](freqtrade-strategies/strategies/STRATEGY_RSI_BB_BOUNDS_CROSS/STRATEGY_RSI_BB_BOUNDS_CROSS.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 270 | [XtraThicc.py](freqtrade-strategies/strategies/XtraThicc/XtraThicc.py) | 5m | 5.0 | 高 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 271 | [RSIv2.py](freqtrade-strategies/strategies/RSIv2/RSIv2.py) | 15m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 272 | [RSIBB02.py](freqtrade-strategies/strategies/RSIBB02/RSIBB02.py) | Unknown | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 273 | [NFI731_BUSD.py](freqtrade-strategies/strategies/NFI731_BUSD/NFI731_BUSD.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 274 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV6HO/NostalgiaForInfinityV6HO.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 275 | [botbaby.py](freqtrade-strategies/strategies/botbaby/botbaby.py) | 30m | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；低风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 276 | [Strategy003.py](freqtrade-strategies/strategies/Strategy003/Strategy003.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 277 | [TheRealPullbackV2.py](freqtrade-strategies/strategies/TheRealPullbackV2/TheRealPullbackV2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；低风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 278 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV2/CombinedBinHAndClucV2.py) | 1h | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 279 | [Dracula.py](freqtrade-strategies/strategies/Dracula/Dracula.py) | 5m | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制 |
| 280 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_maximizer/NostalgiaForInfinityNext_maximizer.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 281 | [Fakebuy.py](freqtrade-strategies/strategies/Fakebuy/Fakebuy.py) | 5m | 5.0 | 中 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 282 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndCluc2021Bull/CombinedBinHAndCluc2021Bull.py) | 5m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 283 | [EMA_CROSSOVER_STR...](freqtrade-strategies/strategies/EMA_CROSSOVER_STRATEGY/EMA_CROSSOVER_STRATEGY.py) | 5m | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 284 | [PumpDetector.py](freqtrade-strategies/strategies/PumpDetector/PumpDetector.py) | 5m | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | 评分一般；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 285 | [NFINextMOHO.py](freqtrade-strategies/strategies/NFINextMOHO/NFINextMOHO.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 286 | [stoploss.py](freqtrade-strategies/strategies/stoploss/stoploss.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 287 | [strato.py](freqtrade-strategies/strategies/strato/strato.py) | 1m | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；逻辑简单；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 288 | [NFI46OffsetHOA1.py](freqtrade-strategies/strategies/NFI46OffsetHOA1/NFI46OffsetHOA1.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 289 | [NFI7MOHO.py](freqtrade-strategies/strategies/NFI7MOHO/NFI7MOHO.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 290 | [RSI.py](freqtrade-strategies/strategies/RSI/RSI.py) | 15m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 291 | [quantumfirst.py](freqtrade-strategies/strategies/quantumfirst/quantumfirst.py) | Unknown | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 292 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndCluc2021/CombinedBinHAndCluc2021.py) | 5m | 5.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 293 | [SupertrendStrateg...](freqtrade-strategies/strategies/SupertrendStrategy/SupertrendStrategy.py) | 1h | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 294 | [Strategy005.py](freqtrade-strategies/strategies/Strategy005/Strategy005.py) | 5m | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 295 | [SampleStrategy.py](freqtrade-strategies/strategies/SampleStrategy/SampleStrategy.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 296 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_7_2/NostalgiaForInfinityV7_7_2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 297 | [Ichimoku_v31.py](freqtrade-strategies/strategies/Ichimoku_v31/Ichimoku_v31.py) | 1h | 5.0 | 高 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 298 | [EMABBRSI.py](freqtrade-strategies/strategies/EMABBRSI/EMABBRSI.py) | Unknown | 5.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 299 | [stratfib.py](freqtrade-strategies/strategies/stratfib/stratfib.py) | 1h | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 300 | [BuyOnly.py](freqtrade-strategies/strategies/BuyOnly/BuyOnly.py) | 15m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 301 | [Ichi.py](freqtrade-strategies/strategies/Ichi/Ichi.py) | 15m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 302 | [TDSequentialStrat...](freqtrade-strategies/strategies/TDSequentialStrategy/TDSequentialStrategy.py) | 1h | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 303 | [NFI5MOHO2.py](freqtrade-strategies/strategies/NFI5MOHO2/NFI5MOHO2.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 304 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityXw/NostalgiaForInfinityXw.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 305 | [AlligatorStrategy.py](freqtrade-strategies/strategies/AlligatorStrategy/AlligatorStrategy.py) | 1h | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 306 | [BigZ07Next.py](freqtrade-strategies/strategies/BigZ07Next/BigZ07Next.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 307 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7/NostalgiaForInfinityV7.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 308 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_2/NostalgiaForInfinityNext_ChangeToTower_V5_2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 309 | [Babico_SMA5xBBmid.py](freqtrade-strategies/strategies/Babico_SMA5xBBmid/Babico_SMA5xBBmid.py) | 1d | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 310 | [TrixStrategy.py](freqtrade-strategies/strategies/TrixStrategy/TrixStrategy.py) | 1h | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 311 | [CrossEMAStrategy.py](freqtrade-strategies/strategies/CrossEMAStrategy/CrossEMAStrategy.py) | 1h | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 312 | [NFI47V2.py](freqtrade-strategies/strategies/NFI47V2/NFI47V2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 313 | [ForexSignal.py](freqtrade-strategies/strategies/ForexSignal/ForexSignal.py) | 5m | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；低风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 314 | [NFINextMultiOffse...](freqtrade-strategies/strategies/NFINextMultiOffsetAndHO/NFINextMultiOffsetAndHO.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 315 | [Slowbro.py](freqtrade-strategies/strategies/Slowbro/Slowbro.py) | 1h | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 316 | [Strategy004.py](freqtrade-strategies/strategies/Strategy004/Strategy004.py) | 5m | 5.0 | 高 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 317 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV3/NostalgiaForInfinityV3.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 318 | [InformativeSample.py](freqtrade-strategies/strategies/InformativeSample/InformativeSample.py) | 5m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 319 | [BB_RPB_TSL_SMA_Tr...](freqtrade-strategies/strategies/BB_RPB_TSL_SMA_Tranz_TB_1_1_1/BB_RPB_TSL_SMA_Tranz_TB_1_1_1.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 320 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext/NostalgiaForInfinityNext.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 321 | [ElliotV531.py](freqtrade-strategies/strategies/ElliotV531/ElliotV531.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 322 | [Strategy001_custo...](freqtrade-strategies/strategies/Strategy001_custom_sell/Strategy001_custom_sell.py) | 5m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 323 | [NFINextMOHO2.py](freqtrade-strategies/strategies/NFINextMOHO2/NFINextMOHO2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 324 | [Minmax.py](freqtrade-strategies/strategies/Minmax/Minmax.py) | 1h | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 325 | [STRATEGY_RSI_BB_C...](freqtrade-strategies/strategies/STRATEGY_RSI_BB_CROSS/STRATEGY_RSI_BB_CROSS.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 326 | [NFI5MOHO_WIP.py](freqtrade-strategies/strategies/NFI5MOHO_WIP/NFI5MOHO_WIP.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 327 | [EXPERIMENTAL_STRA...](freqtrade-strategies/strategies/EXPERIMENTAL_STRATEGY/EXPERIMENTAL_STRATEGY.py) | Unknown | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 328 | [UziChan2.py](freqtrade-strategies/strategies/UziChan2/UziChan2.py) | 1m | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | 评分一般；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突 |
| 329 | [Nostalgia.py](freqtrade-strategies/strategies/Nostalgia/Nostalgia.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 330 | [BigZ07Next2.py](freqtrade-strategies/strategies/BigZ07Next2/BigZ07Next2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 331 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityX/NostalgiaForInfinityX.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 332 | [Strategy002.py](freqtrade-strategies/strategies/Strategy002/Strategy002.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 333 | [SRsi.py](freqtrade-strategies/strategies/SRsi/SRsi.py) | 1m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；逻辑简单；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 334 | [RobotradingBody.py](freqtrade-strategies/strategies/RobotradingBody/RobotradingBody.py) | 4h | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；逻辑简单；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 335 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV5MultiOffsetAndHO/NostalgiaForInfinityV5MultiOffsetAndHO.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 336 | [BBands.py](freqtrade-strategies/strategies/BBands/BBands.py) | 1m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 337 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_3/NostalgiaForInfinityNext_ChangeToTower_V5_3.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 338 | [MAC.py](freqtrade-strategies/strategies/MAC/MAC.py) | 1d | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 339 | [conny.py](freqtrade-strategies/strategies/conny/conny.py) | 15m | 5.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；低风险；逻辑简单；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 340 | [NFI46Offset.py](freqtrade-strategies/strategies/NFI46Offset/NFI46Offset.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 341 | [NFI46.py](freqtrade-strategies/strategies/NFI46/NFI46.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 342 | [bbrsi1_strategy.py](freqtrade-strategies/strategies/bbrsi1_strategy/bbrsi1_strategy.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 343 | [Strategy001.py](freqtrade-strategies/strategies/Strategy001/Strategy001.py) | 5m | 5.0 | 高 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 344 | [Cluc4.py](freqtrade-strategies/strategies/Cluc4/Cluc4.py) | 1m | 5.0 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随；多周期确认 | 评分一般；低风险；逻辑简单；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 345 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndCluc/CombinedBinHAndCluc.py) | 5m | 5.0 | 高 | 常规 | 通道类策略（布林带/Keltner 等） | 评分一般；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 346 | [Ichimoku_v37.py](freqtrade-strategies/strategies/Ichimoku_v37/Ichimoku_v37.py) | 4h | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 347 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV5/NostalgiaForInfinityV5.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 348 | [TheForce.py](freqtrade-strategies/strategies/TheForce/TheForce.py) | 15m | 5.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；低风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 349 | [TEMA.py](freqtrade-strategies/strategies/TEMA/TEMA.py) | 1m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 350 | [BBRSINaiveStrateg...](freqtrade-strategies/strategies/BBRSINaiveStrategy/BBRSINaiveStrategy.py) | 15m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 351 | [Martin.py](freqtrade-strategies/strategies/Martin/Martin.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 352 | [SAR.py](freqtrade-strategies/strategies/SAR/SAR.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 353 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV6/NostalgiaForInfinityV6.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 354 | [CBPete9.py](freqtrade-strategies/strategies/CBPete9/CBPete9.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 355 | [BBRSIS.py](freqtrade-strategies/strategies/BBRSIS/BBRSIS.py) | Unknown | 5.0 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 356 | [Seb.py](freqtrade-strategies/strategies/Seb/Seb.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 357 | [bbema.py](freqtrade-strategies/strategies/bbema/bbema.py) | Unknown | 5.0 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 358 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityX2/NostalgiaForInfinityX2.py) | 5m | 5.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 359 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV5MultiOffsetAndHO2/NostalgiaForInfinityV5MultiOffsetAndHO2.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 360 | [mabStra.py](freqtrade-strategies/strategies/mabStra/mabStra.py) | 4h | 5.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 361 | [ReinforcedAverage...](freqtrade-strategies/strategies/ReinforcedAverageStrategy/ReinforcedAverageStrategy.py) | 4h | 5.0 | 高 | 常规 | 通道类策略（布林带/Keltner 等） | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 362 | [LuxOSC.py](freqtrade-strategies/strategies/LuxOSC/LuxOSC.py) | 5m | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | 评分一般；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 363 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_ChangeToTower_V6/NostalgiaForInfinityNext_ChangeToTower_V6.py) | 5m | 5.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 364 | [UltimateMomentumI...](freqtrade-strategies/strategies/UltimateMomentumIndicator/UltimateMomentumIndicator.py) | 5m | 5.0 | 中 | 常规 | 基于阈值条件的规则策略 | 评分一般；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 365 | [BBandsRSI.py](freqtrade-strategies/strategies/BBandsRSI/BBandsRSI.py) | 5m | 5.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；高风险；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 366 | [sample_strategy.py](user_data/strategies/sample_strategy.py) | 5m | 5.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；逻辑复杂；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 367 | [AlexNexusForgeV5.py](user_data/strategies/AlexNexusForgeV5.py) | 1h | 5.0 | 中 | 常规 | 动量/均线趋势跟随；趋势强度过滤；保护机制防极端行情 | 评分一般；低风险；lint禁用 | 建议启用主动离场信号或补充退出条件；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 368 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategy/NotAnotherSMAOffsetStrategy.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 369 | [EMA50.py](freqtrade-strategies/strategies/EMA50/EMA50.py) | 5m | 4.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 370 | [mark_strat.py](freqtrade-strategies/strategies/mark_strat/mark_strat.py) | Unknown | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 371 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyHO/NotAnotherSMAOffsetStrategyHO.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 372 | [Kamaflage.py](freqtrade-strategies/strategies/Kamaflage/Kamaflage.py) | 5m | 4.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；高风险；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 373 | [FastSupertrendOpt.py](freqtrade-strategies/strategies/FastSupertrendOpt/FastSupertrendOpt.py) | 1h | 4.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制 |
| 374 | [ElliotV8_original.py](freqtrade-strategies/strategies/ElliotV8_original/ElliotV8_original.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 375 | [custom.py](freqtrade-strategies/strategies/custom/custom.py) | 5m | 4.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；动量突破；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 376 | [Chandem.py](freqtrade-strategies/strategies/Chandem/Chandem.py) | 5m | 4.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 377 | [ClucFiatSlow.py](freqtrade-strategies/strategies/ClucFiatSlow/ClucFiatSlow.py) | 5m | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 378 | [hlhb.py](freqtrade-strategies/strategies/hlhb/hlhb.py) | 4h | 4.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 379 | [DCBBBounce.py](freqtrade-strategies/strategies/DCBBBounce/DCBBBounce.py) | 5m | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 380 | [Chandemtwo.py](freqtrade-strategies/strategies/Chandemtwo/Chandemtwo.py) | 5m | 4.5 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 381 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyHOv3/NotAnotherSMAOffsetStrategyHOv3.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 382 | [Saturn5.py](freqtrade-strategies/strategies/Saturn5/Saturn5.py) | 15m | 4.5 | 中 | 常规 | 动量/均线趋势跟随；保护机制防极端行情 | 评分一般；高风险 | 建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 383 | [SuperTrendPure.py](freqtrade-strategies/strategies/SuperTrendPure/SuperTrendPure.py) | 1h | 4.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 384 | [Cluc5werk.py](freqtrade-strategies/strategies/Cluc5werk/Cluc5werk.py) | 1m | 4.5 | 中 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 385 | [mark_strat_opt.py](freqtrade-strategies/strategies/mark_strat_opt/mark_strat_opt.py) | Unknown | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 386 | [fahmibah.py](freqtrade-strategies/strategies/fahmibah/fahmibah.py) | 5m | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议启用主动离场信号或补充退出条件；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 387 | [EMABreakout.py](freqtrade-strategies/strategies/EMABreakout/EMABreakout.py) | 5m | 4.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 388 | [GodStraNew_SMAonl...](freqtrade-strategies/strategies/GodStraNew_SMAonly/GodStraNew_SMAonly.py) | 5m | 4.5 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | 评分一般；高风险；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 389 | [SuperTrend.py](freqtrade-strategies/strategies/SuperTrend/SuperTrend.py) | 1h | 4.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制 |
| 390 | [SMAOG.py](freqtrade-strategies/strategies/SMAOG/SMAOG.py) | 5m | 4.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制 |
| 391 | [KAMACCIRSI.py](freqtrade-strategies/strategies/KAMACCIRSI/KAMACCIRSI.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 392 | [NotAnotherSMAOffS...](freqtrade-strategies/strategies/NotAnotherSMAOffSetStrategy_V2/NotAnotherSMAOffSetStrategy_V2.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 393 | [Elliotv8.py](freqtrade-strategies/strategies/Elliotv8/Elliotv8.py) | 5m | 4.5 | 中 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 394 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNextGen_TSL/NostalgiaForInfinityNextGen_TSL.py) | 15m | 4.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认；动态风控（自定义止损） | 评分一般；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议启用主动离场信号或补充退出条件；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 395 | [bb_rsi_opt_new.py](freqtrade-strategies/strategies/bb_rsi_opt_new/bb_rsi_opt_new.py) | Unknown | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 396 | [ElliotV5HOMod3.py](freqtrade-strategies/strategies/ElliotV5HOMod3/ElliotV5HOMod3.py) | 5m | 4.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 397 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV1/NostalgiaForInfinityV1.py) | 5m | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 398 | [FastSupertrend.py](freqtrade-strategies/strategies/FastSupertrend/FastSupertrend.py) | 1h | 4.5 | 高 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制 |
| 399 | [SMAIP3v2.py](freqtrade-strategies/strategies/SMAIP3v2/SMAIP3v2.py) | 5m | 4.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制 |
| 400 | [BbRoi.py](freqtrade-strategies/strategies/BbRoi/BbRoi.py) | Unknown | 4.5 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 401 | [ClucFiatROI.py](freqtrade-strategies/strategies/ClucFiatROI/ClucFiatROI.py) | 5m | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 402 | [NowoIchimoku1hV1.py](freqtrade-strategies/strategies/NowoIchimoku1hV1/NowoIchimoku1hV1.py) | 1h | 4.5 | 中 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认；动态风控（自定义止损） | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 403 | [Cluc4werk.py](freqtrade-strategies/strategies/Cluc4werk/Cluc4werk.py) | 1m | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 404 | [Diamond.py](freqtrade-strategies/strategies/Diamond/Diamond.py) | 5m | 4.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 405 | [bbrsi4Freq.py](freqtrade-strategies/strategies/bbrsi4Freq/bbrsi4Freq.py) | 1h | 4.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 406 | [SMAIP3.py](freqtrade-strategies/strategies/SMAIP3/SMAIP3.py) | 5m | 4.5 | 中 | 常规 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制 |
| 407 | [BBRSIOptim2020Str...](freqtrade-strategies/strategies/BBRSIOptim2020Strategy/BBRSIOptim2020Strategy.py) | 5m | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 408 | [ichiV1.py](freqtrade-strategies/strategies/ichiV1/ichiV1.py) | 5m | 4.0 | 低 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；高风险；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 409 | [DevilStra.py](freqtrade-strategies/strategies/DevilStra/DevilStra.py) | 4h | 4.0 | 中 | 常规 | 通道类策略（布林带/Keltner 等）；动量/均线趋势跟随 | 评分一般；高风险；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 410 | [NfiNextModded.py](freqtrade-strategies/strategies/NfiNextModded/NfiNextModded.py) | 5m | 4.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 411 | [FrostAuraM21hStra...](freqtrade-strategies/strategies/FrostAuraM21hStrategy/FrostAuraM21hStrategy.py) | 15m | 4.0 | 高 | 工程化/多周期 | 动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 412 | [Gumbo1.py](freqtrade-strategies/strategies/Gumbo1/Gumbo1.py) | 5m | 4.0 | 高 | 工程化/多周期 | 通道类策略（布林带/Keltner 等）；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 413 | [BBRSIStrategy.py](freqtrade-strategies/strategies/BBRSIStrategy/BBRSIStrategy.py) | 15m | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 414 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1/SMAOffsetProtectOptV1.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 415 | [ema.py](freqtrade-strategies/strategies/ema/ema.py) | 5m | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险；逻辑简单；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 416 | [GodStraNew.py](freqtrade-strategies/strategies/GodStraNew/GodStraNew.py) | 4h | 4.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | 评分一般；高风险；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 417 | [BBRSI.py](freqtrade-strategies/strategies/BBRSI/BBRSI.py) | 4h | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 418 | [BBRSIOptimizedStr...](freqtrade-strategies/strategies/BBRSIOptimizedStrategy/BBRSIOptimizedStrategy.py) | 5m | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 419 | [NowoIchimoku1hV2.py](freqtrade-strategies/strategies/NowoIchimoku1hV2/NowoIchimoku1hV2.py) | 1h | 4.0 | 中 | 风控导向 | 一目均衡的趋势识别；动态风控（自定义止损） | 评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 420 | [TrixV15Strategy.py](freqtrade-strategies/strategies/TrixV15Strategy/TrixV15Strategy.py) | 1h | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 421 | [Obelisk_Ichimoku_...](freqtrade-strategies/strategies/Obelisk_Ichimoku_ZEMA_v1/Obelisk_Ichimoku_ZEMA_v1.py) | 5m | 4.0 | 低 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 422 | [Renko.py](freqtrade-strategies/strategies/Renko/Renko.py) | 15m | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 423 | [MultiOffsetLamboV...](freqtrade-strategies/strategies/MultiOffsetLamboV0/MultiOffsetLamboV0.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 424 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1Mod2/SMAOffsetProtectOptV1Mod2.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 425 | [custom_sell.py](freqtrade-strategies/strategies/custom_sell/custom_sell.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 426 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV4HO/NostalgiaForInfinityV4HO.py) | 5m | 4.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 427 | [MultiMa.py](freqtrade-strategies/strategies/MultiMa/MultiMa.py) | 4h | 4.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 428 | [FrostAuraM31hStra...](freqtrade-strategies/strategies/FrostAuraM31hStrategy/FrostAuraM31hStrategy.py) | 1h | 4.0 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 429 | [NowoIchimoku5mV2.py](freqtrade-strategies/strategies/NowoIchimoku5mV2/NowoIchimoku5mV2.py) | 5m | 4.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 430 | [redditMA.py](freqtrade-strategies/strategies/redditMA/redditMA.py) | Unknown | 4.0 | 高 | 工程化/多周期 | 围绕 VWAP 的回归/基准定价；多周期确认 | 评分一般；高风险；逻辑简单；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 431 | [Schism.py](freqtrade-strategies/strategies/Schism/Schism.py) | 5m | 4.0 | 中 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 432 | [BBRSIOptimStrateg...](freqtrade-strategies/strategies/BBRSIOptimStrategy/BBRSIOptimStrategy.py) | 5m | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 433 | [FrostAuraM115mStr...](freqtrade-strategies/strategies/FrostAuraM115mStrategy/FrostAuraM115mStrategy.py) | 15m | 4.0 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 434 | [MontrealStrategy.py](freqtrade-strategies/strategies/MontrealStrategy/MontrealStrategy.py) | 15m | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 435 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV2/NostalgiaForInfinityV2.py) | 5m | 4.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 436 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1Mod/SMAOffsetProtectOptV1Mod.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 437 | [BB_Strategy04.py](freqtrade-strategies/strategies/BB_Strategy04/BB_Strategy04.py) | Unknown | 4.0 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 438 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNextGen/NostalgiaForInfinityNextGen.py) | 15m | 4.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 439 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV4/NostalgiaForInfinityV4.py) | 5m | 4.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 440 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV0/SMAOffsetProtectOptV0.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 441 | [Schism6.py](freqtrade-strategies/strategies/Schism6/Schism6.py) | 5m | 4.0 | 中 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；高风险；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 442 | [BBRSIoriginal.py](freqtrade-strategies/strategies/BBRSIoriginal/BBRSIoriginal.py) | Unknown | 4.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖 | 评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 443 | [Maro4hMacdSd.py](freqtrade-strategies/strategies/Maro4hMacdSd/Maro4hMacdSd.py) | 5m | 4.0 | 高 | 常规 | 动量/均线趋势跟随 | 评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 444 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1HO1/SMAOffsetProtectOptV1HO1.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 445 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNextV7155/NostalgiaForInfinityNextV7155.py) | 5m | 4.0 | 中 | 工程化/多周期 | 一目均衡的趋势识别；布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 446 | [FrostAuraRandomSt...](freqtrade-strategies/strategies/FrostAuraRandomStrategy/FrostAuraRandomStrategy.py) | 1h | 4.0 | 高 | 常规 | 动量/均线趋势跟随 | 评分一般；高风险；接口不匹配 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制 |
| 447 | [FrostAuraM315mStr...](freqtrade-strategies/strategies/FrostAuraM315mStrategy/FrostAuraM315mStrategy.py) | 15m | 4.0 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 448 | [FrostAuraM11hStra...](freqtrade-strategies/strategies/FrostAuraM11hStrategy/FrostAuraM11hStrategy.py) | 1h | 4.0 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 449 | [SMAOPv1_TTF.py](freqtrade-strategies/strategies/SMAOPv1_TTF/SMAOPv1_TTF.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 450 | [MomStrategy.py](freqtrade-strategies/strategies/MomStrategy/MomStrategy.py) | 1h | 4.0 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 451 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1_kkeue_20210619/SMAOffsetProtectOptV1_kkeue_20210619.py) | 5m | 4.0 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认 | 评分一般；高风险；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 452 | [GodStraNew40.py](freqtrade-strategies/strategies/GodStraNew40/GodStraNew40.py) | 4h | 4.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | 评分一般；高风险；逻辑复杂 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 453 | [YOLO.py](freqtrade-strategies/strategies/YOLO/YOLO.py) | 1m | 3.5 | 高 | 常规 | 趋势强度过滤 | 评分一般；低风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议启用主动离场信号或补充退出条件；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 454 | [ichiV1_Marius.py](freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py) | 5m | 3.5 | 低 | 工程化/多周期 | 一目均衡的趋势识别；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 455 | [FiveMinCrossAbove.py](freqtrade-strategies/strategies/FiveMinCrossAbove/FiveMinCrossAbove.py) | 5m | 3.5 | 高 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；多周期确认 | 评分一般；多周期；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 456 | [Schism5.py](freqtrade-strategies/strategies/Schism5/Schism5.py) | 5m | 3.5 | 中 | 工程化/多周期 | 基于阈值条件的规则策略；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；指标较少，建议增加二次确认（趋势+动量或波动率）；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |
| 457 | [PrawnstarOBV.py](freqtrade-strategies/strategies/PrawnstarOBV/PrawnstarOBV.py) | 1h | 3.5 | 高 | 工程化/多周期 | 趋势持有 + 移动止损跟踪；多周期确认 | 评分一般；高风险；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 458 | [Dyna_opti.py](freqtrade-strategies/strategies/Dyna_opti/Dyna_opti.py) | 5m | 3.5 | 中 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认；动态风控（自定义止损） | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 459 | [INSIDEUP.py](freqtrade-strategies/strategies/INSIDEUP/INSIDEUP.py) | 1d | 3.5 | 高 | 工程化/多周期 | 一目均衡的趋势识别；趋势强度过滤；多周期确认 | 评分一般；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议启用主动离场信号或补充退出条件；同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 460 | [Schism2MM.py](freqtrade-strategies/strategies/Schism2MM/Schism2MM.py) | 5m | 3.0 | 中 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 461 | [TenderEnter.py](freqtrade-strategies/strategies/TenderEnter/TenderEnter.py) | 15m | 2.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 462 | [Stinkfist.py](freqtrade-strategies/strategies/Stinkfist/Stinkfist.py) | 5m | 2.5 | 中 | 工程化/多周期 | 动量/均线趋势跟随；动量突破；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 463 | [RaposaDivergenceV...](freqtrade-strategies/strategies/RaposaDivergenceV1/RaposaDivergenceV1.py) | 5m | 2.5 | 中 | 模板化/堆叠型 | 趋势持有 + 移动止损跟踪 | 评分一般；高风险；接口不匹配；lint禁用 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；指标较少，建议增加二次确认（趋势+动量或波动率）；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 464 | [ElliotV4.py](freqtrade-strategies/strategies/ElliotV4/ElliotV4.py) | 5m | 2.5 | 低 | 工程化/多周期 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随；多周期确认 | 评分一般；高风险；逻辑复杂；接口不匹配；多周期 | 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）；建议补充保护机制(Protections)，如 cooldown/stoploss guard；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 465 | [Schism2.py](freqtrade-strategies/strategies/Schism2/Schism2.py) | 5m | 2.0 | 中 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 466 | [SuperHV27.py](freqtrade-strategies/strategies/SuperHV27/SuperHV27.py) | 5m | 2.0 | 中 | 工程化/多周期 | 动量/均线趋势跟随；趋势强度过滤；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 467 | [StrategyScalpingF...](freqtrade-strategies/strategies/StrategyScalpingFast2/StrategyScalpingFast2.py) | 1m | 2.0 | 中 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | 评分一般；高风险；lint禁用 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码 |
| 468 | [Schism3.py](freqtrade-strategies/strategies/Schism3/Schism3.py) | 5m | 2.0 | 中 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 469 | [Schism4.py](freqtrade-strategies/strategies/Schism4/Schism4.py) | 5m | 2.0 | 中 | 工程化/多周期 | 动量突破；多周期确认 | 评分一般；高风险；逻辑复杂；多周期 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性；多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count |
| 470 | [BuyAllSellAllStra...](freqtrade-strategies/strategies/BuyAllSellAllStrategy/BuyAllSellAllStrategy.py) | 5m | 2.0 | 高 | 常规 | 基于阈值条件的规则策略 | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声；指标较少，建议增加二次确认（趋势+动量或波动率） |
| 471 | [StrategyScalpingF...](freqtrade-strategies/strategies/StrategyScalpingFast/StrategyScalpingFast.py) | 1m | 2.0 | 高 | 常规 | 布林带+RSI 的均值回归/超买超卖；动量/均线趋势跟随 | 评分一般；高风险；逻辑简单 | 建议补充保护机制(Protections)，如 cooldown/stoploss guard；建议评估开启移动止损，用于锁定利润；止损偏大，建议收紧或配合动态止损/保护机制；建议启用主动离场信号或补充退出条件；建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性 |

## 重点策略：设计思想详述

### CustomStoplossWithPSAR.py

- 文件：[CustomStoplossWithPSAR.py](freqtrade-strategies/strategies/CustomStoplossWithPSAR/CustomStoplossWithPSAR.py)
- 周期：1h；止损：-0.2；评分：6.5
- 设计思想：核心思路：以 RSI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 风控设计：通过自定义止损实现更精细的风险分层与行情自适应。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：风控导向。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Macd.py

- 文件：[Macd.py](freqtrade-strategies/strategies/Macd/Macd.py)
- 周期：1h；止损：-0.1；评分：6.5
- 设计思想：核心思路：以 RSI、MACD 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 风控设计：通过自定义止损实现更精细的风险分层与行情自适应。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### KC_BB.py

- 文件：[KC_BB.py](freqtrade-strategies/strategies/KC_BB/KC_BB.py)
- 周期：5m；止损：-0.99；评分：6.5
- 设计思想：核心思路：以 RSI、EMA、SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 风控设计：通过自定义止损实现更精细的风险分层与行情自适应。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### Obelisk_3EMA_StochRSI_ATR.py

- 文件：[Obelisk_3EMA_StochRSI_ATR.py](freqtrade-strategies/strategies/Obelisk_3EMA_StochRSI_ATR/Obelisk_3EMA_StochRSI_ATR.py)
- 周期：5m；止损：-0.99；评分：6.5
- 设计思想：核心思路：以 RSI、EMA、ATR 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 风控设计：通过自定义止损实现更精细的风险分层与行情自适应。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ATR，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### LookaheadStrategy.py

- 文件：[LookaheadStrategy.py](freqtrade-strategies/strategies/LookaheadStrategy/LookaheadStrategy.py)
- 周期：5m；止损：-0.194；评分：5.5
- 设计思想：核心思路：以 EMA、SMA 作为主要信号与过滤条件，整体偏向 趋势持有 + 移动止损跟踪。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口V3，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### Combined_Indicators.py

- 文件：[Combined_Indicators.py](freqtrade-strategies/strategies/Combined_Indicators/Combined_Indicators.py)
- 周期：1m；止损：-0.0658；评分：5.5
- 设计思想：核心思路：以 EMA、BBANDS 作为主要信号与过滤条件，整体偏向 通道类策略（布林带/Keltner 等）。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ObeliskRSI_v6_1.py

- 文件：[ObeliskRSI_v6_1.py](freqtrade-strategies/strategies/ObeliskRSI_v6_1/ObeliskRSI_v6_1.py)
- 周期：5m；止损：-0.3；评分：5.5
- 设计思想：核心思路：以 RSI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 风控设计：通过自定义止损实现更精细的风险分层与行情自适应。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：风控导向。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MACD_TRIPLE_MA.py

- 文件：[MACD_TRIPLE_MA.py](freqtrade-strategies/strategies/MACD_TRIPLE_MA/MACD_TRIPLE_MA.py)
- 周期：5m；止损：-0.03；评分：5.5
- 设计思想：核心思路：以 MACD、SMA 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### XebTradeStrat.py

- 文件：[XebTradeStrat.py](freqtrade-strategies/strategies/XebTradeStrat/XebTradeStrat.py)
- 周期：1m；止损：-0.01；评分：5.5
- 设计思想：核心思路：以 EMA 作为主要信号与过滤条件，整体偏向 趋势持有 + 移动止损跟踪。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### FixedRiskRewardLoss.py

- 文件：[FixedRiskRewardLoss.py](freqtrade-strategies/strategies/FixedRiskRewardLoss/FixedRiskRewardLoss.py)
- 周期：5m；止损：-0.9；评分：5.5
- 设计思想：核心思路：以 RSI、ATR 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 风控设计：通过自定义止损实现更精细的风险分层与行情自适应。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、ATR，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：风控导向。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Scalp.py

- 文件：[Scalp.py](freqtrade-strategies/strategies/Scalp/Scalp.py)
- 周期：1m；止损：-0.04；评分：5.0
- 设计思想：核心思路：以 EMA、BBANDS、ADX 作为主要信号与过滤条件，整体偏向 通道类策略（布林带/Keltner 等）。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MACD_TRI_EMA.py

- 文件：[MACD_TRI_EMA.py](freqtrade-strategies/strategies/MACD_TRI_EMA/MACD_TRI_EMA.py)
- 周期：5m；止损：-0.03；评分：5.0
- 设计思想：核心思路：以 MACD 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AverageStrategy.py

- 文件：[AverageStrategy.py](freqtrade-strategies/strategies/AverageStrategy/AverageStrategy.py)
- 周期：4h；止损：-0.2；评分：5.0
- 设计思想：核心思路：以 EMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ADX_15M_USDT.py

- 文件：[ADX_15M_USDT.py](freqtrade-strategies/strategies/ADX_15M_USDT/ADX_15M_USDT.py)
- 周期：Unknown；止损：-0.1255；评分：5.0
- 设计思想：核心思路：以 ADX 作为主要信号与过滤条件，整体偏向 趋势强度过滤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BinHV45.py

- 文件：[BinHV45.py](freqtrade-strategies/strategies/BinHV45/BinHV45.py)
- 周期：1m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 BBANDS 作为主要信号与过滤条件，整体偏向 通道类策略（布林带/Keltner 等）。
- 评审意见：概览：接口V2，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SmoothOperator.py

- 文件：[SmoothOperator.py](freqtrade-strategies/strategies/SmoothOperator/SmoothOperator.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、EMA、SMA、BBANDS、ADX… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：低；风格：模板化/堆叠型。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### ObeliskIM_v1_1.py

- 文件：[ObeliskIM_v1_1.py](freqtrade-strategies/strategies/ObeliskIM_v1_1/ObeliskIM_v1_1.py)
- 周期：5m；止损：-0.04；评分：5.0
- 设计思想：核心思路：以 RSI、EMA、ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：低；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### ClucMay72018.py

- 文件：[ClucMay72018.py](freqtrade-strategies/strategies/ClucMay72018/ClucMay72018.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、EMA、BBANDS、ADX 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MACDRSI200.py

- 文件：[MACDRSI200.py](freqtrade-strategies/strategies/MACDRSI200/MACDRSI200.py)
- 周期：Unknown；止损：-0.04032；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、EMA 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### adaptive.py

- 文件：[adaptive.py](freqtrade-strategies/strategies/adaptive/adaptive.py)
- 周期：5m；止损：-0.109；评分：5.0
- 设计思想：核心思路：以 RSI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MultiRSI.py

- 文件：[MultiRSI.py](freqtrade-strategies/strategies/MultiRSI/MultiRSI.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 RSI、SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润

### BreakEven.py

- 文件：[BreakEven.py](freqtrade-strategies/strategies/BreakEven/BreakEven.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 较少 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Obelisk_TradePro_Ichi_v1_1.py

- 文件：[Obelisk_TradePro_Ichi_v1_1.py](freqtrade-strategies/strategies/Obelisk_TradePro_Ichi_v1_1/Obelisk_TradePro_Ichi_v1_1.py)
- 周期：1h；止损：-0.015；评分：5.0
- 设计思想：核心思路：以 ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MFI.py

- 文件：[MFI.py](freqtrade-strategies/strategies/MFI/MFI.py)
- 周期：5m；止损：-0.1；评分：5.0
- 设计思想：核心思路：以 MFI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BBRSI4cust.py

- 文件：[BBRSI4cust.py](freqtrade-strategies/strategies/BBRSI4cust/BBRSI4cust.py)
- 周期：15m；止损：-0.1；评分：5.0
- 设计思想：核心思路：以 RSI、BBANDS 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口V3，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### EMASkipPump.py

- 文件：[EMASkipPump.py](freqtrade-strategies/strategies/EMASkipPump/EMASkipPump.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 EMA、BBANDS 作为主要信号与过滤条件，整体偏向 通道类策略（布林带/Keltner 等）。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### VWAP.py

- 文件：[VWAP.py](freqtrade-strategies/strategies/VWAP/VWAP.py)
- 周期：5m；止损：-0.15；评分：5.0
- 设计思想：核心思路：以 RSI、VWAP 作为主要信号与过滤条件，整体偏向 围绕 VWAP 的回归/基准定价。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、VWAP，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Low_BB.py

- 文件：[Low_BB.py](freqtrade-strategies/strategies/Low_BB/Low_BB.py)
- 周期：1m；止损：-0.015；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、BBANDS、MFI、CCI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Leveraged.py

- 文件：[Leveraged.py](freqtrade-strategies/strategies/Leveraged/Leveraged.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、EMA、SMA、BBANDS、MFI… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### macd_recovery.py

- 文件：[macd_recovery.py](freqtrade-strategies/strategies/macd_recovery/macd_recovery.py)
- 周期：Unknown；止损：-0.04032；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、EMA 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### CMCWinner.py

- 文件：[CMCWinner.py](freqtrade-strategies/strategies/CMCWinner/CMCWinner.py)
- 周期：15m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 MFI、CCI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### UziChan.py

- 文件：[UziChan.py](freqtrade-strategies/strategies/UziChan/UziChan.py)
- 周期：5m；止损：-0.1；评分：5.0
- 设计思想：核心思路：以 EMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), pandas_ta。 可读性：中；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突

### heikin.py

- 文件：[heikin.py](freqtrade-strategies/strategies/heikin/heikin.py)
- 周期：1h；止损：-0.99；评分：5.0
- 设计思想：核心思路：以 SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；疑似虚假止损但未发现自定义止损逻辑。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### hansencandlepatternV1.py

- 文件：[hansencandlepatternV1.py](freqtrade-strategies/strategies/hansencandlepatternV1/hansencandlepatternV1.py)
- 周期：1h；止损：-0.1；评分：5.0
- 设计思想：核心思路：以 SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### ReinforcedQuickie.py

- 文件：[ReinforcedQuickie.py](freqtrade-strategies/strategies/ReinforcedQuickie/ReinforcedQuickie.py)
- 周期：5m；止损：-0.05；评分：5.0
- 设计思想：核心思路：以 RSI、MACD、EMA、SMA、BBANDS、MFI… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### EMAVolume.py

- 文件：[EMAVolume.py](freqtrade-strategies/strategies/EMAVolume/EMAVolume.py)
- 周期：Unknown；止损：-0.2；评分：5.0
- 设计思想：核心思路：以 EMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AlligatorStrat.py

- 文件：[AlligatorStrat.py](freqtrade-strategies/strategies/AlligatorStrat/AlligatorStrat.py)
- 周期：Unknown；止损：-0.2；评分：5.0
- 设计思想：核心思路：以 MACD、SMA、CCI 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、SMA、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BbandRsiRolling.py

- 文件：[BbandRsiRolling.py](freqtrade-strategies/strategies/BbandRsiRolling/BbandRsiRolling.py)
- 周期：5m；止损：-0.08；评分：5.0
- 设计思想：核心思路：以 RSI、BBANDS 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BinHV45HO.py

- 文件：[BinHV45HO.py](freqtrade-strategies/strategies/BinHV45HO/BinHV45HO.py)
- 周期：1m；止损：-0.19；评分：5.0
- 设计思想：核心思路：以 较少 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ReinforcedSmoothScalp.py

- 文件：[ReinforcedSmoothScalp.py](freqtrade-strategies/strategies/ReinforcedSmoothScalp/ReinforcedSmoothScalp.py)
- 周期：1m；止损：-0.1；评分：5.0
- 设计思想：核心思路：以 RSI、EMA、SMA、BBANDS、ADX、MFI… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### CCIStrategy.py

- 文件：[CCIStrategy.py](freqtrade-strategies/strategies/CCIStrategy/CCIStrategy.py)
- 周期：1m；止损：-0.02；评分：5.0
- 设计思想：核心思路：以 RSI、SMA、BBANDS、MFI、CCI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BBRSI3366.py

- 文件：[BBRSI3366.py](freqtrade-strategies/strategies/BBRSI3366/BBRSI3366.py)
- 周期：5m；止损：-0.33233；评分：4.5
- 设计思想：核心思路：以 RSI、MACD、BBANDS、ADX、MFI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichimoku_v32.py

- 文件：[Ichimoku_v32.py](freqtrade-strategies/strategies/Ichimoku_v32/Ichimoku_v32.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 设计思想：核心思路：以 ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### BBRSI21.py

- 文件：[BBRSI21.py](freqtrade-strategies/strategies/BBRSI21/BBRSI21.py)
- 周期：5m；止损：-0.30054；评分：4.5
- 设计思想：核心思路：以 RSI、MACD、BBANDS、ADX、MFI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichimoku_v30.py

- 文件：[Ichimoku_v30.py](freqtrade-strategies/strategies/Ichimoku_v30/Ichimoku_v30.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 设计思想：核心思路：以 ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### SwingHigh.py

- 文件：[SwingHigh.py](freqtrade-strategies/strategies/SwingHigh/SwingHigh.py)
- 周期：Unknown；止损：-0.22274；评分：4.5
- 设计思想：核心思路：以 MACD、CCI 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### DD.py

- 文件：[DD.py](freqtrade-strategies/strategies/DD/DD.py)
- 周期：5m；止损：-0.32745；评分：4.5
- 设计思想：核心思路：以 RSI、MACD、BBANDS、ADX、MFI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### adxbbrsi2.py

- 文件：[adxbbrsi2.py](freqtrade-strategies/strategies/adxbbrsi2/adxbbrsi2.py)
- 周期：1h；止损：-0.32237；评分：4.5
- 设计思想：核心思路：以 RSI、BBANDS、ADX、MFI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichimoku_v33.py

- 文件：[Ichimoku_v33.py](freqtrade-strategies/strategies/Ichimoku_v33/Ichimoku_v33.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 设计思想：核心思路：以 ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### Trend_Strength_Directional.py

- 文件：[Trend_Strength_Directional.py](freqtrade-strategies/strategies/Trend_Strength_Directional/Trend_Strength_Directional.py)
- 周期：15m；止损：-0.314；评分：4.5
- 设计思想：核心思路：以 RSI、ADX 作为主要信号与过滤条件，整体偏向 趋势强度过滤。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口V2，方法风格 entry/exit，主要指标 RSI、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### adx_opt_strat.py

- 文件：[adx_opt_strat.py](freqtrade-strategies/strategies/adx_opt_strat/adx_opt_strat.py)
- 周期：Unknown；止损：-0.32766；评分：4.5
- 设计思想：核心思路：以 ADX 作为主要信号与过滤条件，整体偏向 趋势强度过滤。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Bandtastic.py

- 文件：[Bandtastic.py](freqtrade-strategies/strategies/Bandtastic/Bandtastic.py)
- 周期：15m；止损：-0.345；评分：4.5
- 设计思想：核心思路：以 RSI、EMA、BBANDS、MFI 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Ichimoku_v12.py

- 文件：[Ichimoku_v12.py](freqtrade-strategies/strategies/Ichimoku_v12/Ichimoku_v12.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 设计思想：核心思路：以 ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### e6v34.py

- 文件：[e6v34.py](freqtrade-strategies/strategies/e6v34/e6v34.py)
- 周期：15m；止损：-0.54；评分：4.5
- 设计思想：核心思路：以 EMA、SMA 作为主要信号与过滤条件，整体偏向 趋势持有 + 移动止损跟踪。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ADX_15M_USDT2.py

- 文件：[ADX_15M_USDT2.py](freqtrade-strategies/strategies/ADX_15M_USDT2/ADX_15M_USDT2.py)
- 周期：Unknown；止损：-0.31941；评分：4.0
- 设计思想：核心思路：以 ADX 作为主要信号与过滤条件，整体偏向 趋势强度过滤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### HourBasedStrategy.py

- 文件：[HourBasedStrategy.py](freqtrade-strategies/strategies/HourBasedStrategy/HourBasedStrategy.py)
- 周期：1h；止损：-0.292；评分：4.0
- 设计思想：核心思路：以 较少 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SMAOffsetProtectOpt.py

- 文件：[SMAOffsetProtectOpt.py](freqtrade-strategies/strategies/SMAOffsetProtectOpt/SMAOffsetProtectOpt.py)
- 周期：5m；止损：-0.5；评分：4.0
- 设计思想：核心思路：以 RSI、EMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。
- 评审意见：概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### WaveTrendStra.py

- 文件：[WaveTrendStra.py](freqtrade-strategies/strategies/WaveTrendStra/WaveTrendStra.py)
- 周期：4h；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 EMA、SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### CofiBitStrategy.py

- 文件：[CofiBitStrategy.py](freqtrade-strategies/strategies/CofiBitStrategy/CofiBitStrategy.py)
- 周期：5m；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 EMA、ADX 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 EMA、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Roth03.py

- 文件：[Roth03.py](freqtrade-strategies/strategies/Roth03/Roth03.py)
- 周期：5m；止损：-0.31939；评分：4.0
- 设计思想：核心思路：以 RSI、MACD、BBANDS、ADX、MFI、STOCH… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI、STOCH、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Quickie.py

- 文件：[Quickie.py](freqtrade-strategies/strategies/Quickie/Quickie.py)
- 周期：5m；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 MACD、SMA、BBANDS、ADX 作为主要信号与过滤条件，整体偏向 通道类策略（布林带/Keltner 等）。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、SMA、BBANDS、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ASDTSRockwellTrading.py

- 文件：[ASDTSRockwellTrading.py](freqtrade-strategies/strategies/ASDTSRockwellTrading/ASDTSRockwellTrading.py)
- 周期：5m；止损：-0.3；评分：4.0
- 设计思想：核心思路：以 MACD 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SmoothScalp.py

- 文件：[SmoothScalp.py](freqtrade-strategies/strategies/SmoothScalp/SmoothScalp.py)
- 周期：1m；止损：-0.5；评分：4.0
- 设计思想：核心思路：以 RSI、MACD、EMA、BBANDS、ADX、MFI… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Roth01.py

- 文件：[Roth01.py](freqtrade-strategies/strategies/Roth01/Roth01.py)
- 周期：5m；止损：-0.29585；评分：4.0
- 设计思想：核心思路：以 RSI、MACD、BBANDS、ADX、MFI、STOCH… 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI、STOCH、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ADXMomentum.py

- 文件：[ADXMomentum.py](freqtrade-strategies/strategies/ADXMomentum/ADXMomentum.py)
- 周期：1h；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 ADX 作为主要信号与过滤条件，整体偏向 趋势强度过滤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Simple.py

- 文件：[Simple.py](freqtrade-strategies/strategies/Simple/Simple.py)
- 周期：5m；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 RSI、MACD、BBANDS 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### keltnerchannel.py

- 文件：[keltnerchannel.py](freqtrade-strategies/strategies/keltnerchannel/keltnerchannel.py)
- 周期：6h；止损：-0.254；评分：4.0
- 设计思想：核心思路：以 RSI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BbandRsi.py

- 文件：[BbandRsi.py](freqtrade-strategies/strategies/BbandRsi/BbandRsi.py)
- 周期：1h；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 RSI、BBANDS 作为主要信号与过滤条件，整体偏向 布林带+RSI 的均值回归/超买超卖。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Cci.py

- 文件：[Cci.py](freqtrade-strategies/strategies/Cci/Cci.py)
- 周期：1m；止损：-0.23；评分：4.0
- 设计思想：核心思路：以 SMA、CCI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AdxSmas.py

- 文件：[AdxSmas.py](freqtrade-strategies/strategies/AdxSmas/AdxSmas.py)
- 周期：1h；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 SMA、ADX 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Chispei.py

- 文件：[Chispei.py](freqtrade-strategies/strategies/Chispei/Chispei.py)
- 周期：Unknown；止损：-0.32336；评分：4.0
- 设计思想：核心思路：以 SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AwesomeMacd.py

- 文件：[AwesomeMacd.py](freqtrade-strategies/strategies/AwesomeMacd/AwesomeMacd.py)
- 周期：1h；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 MACD、ADX 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SwingHighToSky.py

- 文件：[SwingHighToSky.py](freqtrade-strategies/strategies/SwingHighToSky/SwingHighToSky.py)
- 周期：15m；止损：-0.34338；评分：4.0
- 设计思想：核心思路：以 RSI、CCI 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。
- 评审意见：概览：接口V2，方法风格 entry/exit，主要指标 RSI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### MACDCCI.py

- 文件：[MACDCCI.py](freqtrade-strategies/strategies/MACDCCI/MACDCCI.py)
- 周期：Unknown；止损：-0.3；评分：4.0
- 设计思想：核心思路：以 MACD、CCI 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。 结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### BinHV27.py

- 文件：[BinHV27.py](freqtrade-strategies/strategies/BinHV27/BinHV27.py)
- 周期：5m；止损：-0.5；评分：4.0
- 设计思想：核心思路：以 RSI、EMA、SMA、ADX 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MACD_EMA.py

- 文件：[MACD_EMA.py](freqtrade-strategies/strategies/MACD_EMA/MACD_EMA.py)
- 周期：5m；止损：-0.25；评分：4.0
- 设计思想：核心思路：以 MACD、EMA 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichess.py

- 文件：[Ichess.py](freqtrade-strategies/strategies/Ichess/Ichess.py)
- 周期：1d；止损：-0.314；评分：4.0
- 设计思想：核心思路：以 SMA、ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA、ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MACDStrategy_crossed.py

- 文件：[MACDStrategy_crossed.py](freqtrade-strategies/strategies/MACDStrategy_crossed/MACDStrategy_crossed.py)
- 周期：5m；止损：-0.3；评分：4.0
- 设计思想：核心思路：以 MACD、CCI 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MACDStrategy.py

- 文件：[MACDStrategy.py](freqtrade-strategies/strategies/MACDStrategy/MACDStrategy.py)
- 周期：5m；止损：-0.3；评分：4.0
- 设计思想：核心思路：以 MACD、CCI 作为主要信号与过滤条件，整体偏向 动量/均线趋势跟随。
- 评审意见：概览：接口V2，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；止损较大（回撤风险偏高）。
- 改进建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制

### HansenSmaOffsetV1.py

- 文件：[HansenSmaOffsetV1.py](freqtrade-strategies/strategies/HansenSmaOffsetV1/HansenSmaOffsetV1.py)
- 周期：15m；止损：-99.0；评分：4.0
- 设计思想：核心思路：以 SMA 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### JustROCR6.py

- 文件：[JustROCR6.py](freqtrade-strategies/strategies/JustROCR6/JustROCR6.py)
- 周期：Unknown；止损：-0.01；评分：3.5
- 设计思想：核心思路：以 ROC 作为主要信号与过滤条件，整体偏向 动量突破。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### JustROCR3.py

- 文件：[JustROCR3.py](freqtrade-strategies/strategies/JustROCR3/JustROCR3.py)
- 周期：Unknown；止损：-0.01；评分：3.5
- 设计思想：核心思路：以 ROC 作为主要信号与过滤条件，整体偏向 动量突破。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### JustROCR.py

- 文件：[JustROCR.py](freqtrade-strategies/strategies/JustROCR/JustROCR.py)
- 周期：Unknown；止损：-0.2；评分：3.5
- 设计思想：核心思路：以 ROC 作为主要信号与过滤条件，整体偏向 动量突破。 持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### TechnicalExampleStrategy.py

- 文件：[TechnicalExampleStrategy.py](freqtrade-strategies/strategies/TechnicalExampleStrategy/TechnicalExampleStrategy.py)
- 周期：5m；止损：-0.05；评分：3.0
- 设计思想：核心思路：以 较少 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Stavix2.py

- 文件：[Stavix2.py](freqtrade-strategies/strategies/Stavix2/Stavix2.py)
- 周期：Unknown；止损：-0.1；评分：3.0
- 设计思想：核心思路：以 ICHIMOKU 作为主要信号与过滤条件，整体偏向 一目均衡的趋势识别。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### JustROCR5.py

- 文件：[JustROCR5.py](freqtrade-strategies/strategies/JustROCR5/JustROCR5.py)
- 周期：1m；止损：-0.01；评分：3.0
- 设计思想：核心思路：以 ROC 作为主要信号与过滤条件，整体偏向 动量突破。
- 评审意见：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### AlwaysBuy.py

- 文件：[AlwaysBuy.py](freqtrade-strategies/strategies/AlwaysBuy/AlwaysBuy.py)
- 周期：5m；止损：-0.2；评分：1.0
- 设计思想：核心思路：以 较少 作为主要信号与过滤条件，整体偏向 基于阈值条件的规则策略。
- 评审意见：概览：接口V3，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 改进建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议启用主动离场信号或补充退出条件
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

