# 策略源码评审报告 (Code Review Report)

评审模型：静态规则评审 v2（基于源码特征提取与启发式规则生成）。

**总计分析策略数量:** 471

## 总览

- **重点关注策略(已通过回测):** 87
- **接口版本分布:** {None: 244, 3: 4, 2: 223}
- **指标库使用分布:** {'TA-Lib': 460, 'pandas_ta': 58, 'qtpylib': 438}
- **常见指标 Top12:** [('RSI', 342), ('EMA', 316), ('BBANDS', 253), ('SMA', 243), ('MFI', 137), ('MACD', 122), ('ADX', 109), ('ATR', 97), ('ROC', 92), ('STOCH', 85), ('CCI', 81), ('ICHIMOKU', 48)]
- **可读性分布(高/中/低):** {'高': 143, '中': 263, '低': 65}
- **风格分布:** {'风控导向': 19, '工程化/多周期': 323, '常规': 123, '模板化/堆叠型': 3, '实验性/研究型': 3}
- **主要风险计数:** {'接口不匹配': 223, 'vendor qtpylib': 437, '多周期': 325, 'lint禁用': 120}

## 重点策略评审

### CustomStoplossWithPSAR.py

- 文件：[CustomStoplossWithPSAR.py](freqtrade-strategies/strategies/CustomStoplossWithPSAR/CustomStoplossWithPSAR.py)
- 周期：1h；止损：-0.2；评分：6.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：风控导向。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Macd.py

- 文件：[Macd.py](freqtrade-strategies/strategies/Macd/Macd.py)
- 周期：1h；止损：-0.1；评分：6.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### KC_BB.py

- 文件：[KC_BB.py](freqtrade-strategies/strategies/KC_BB/KC_BB.py)
- 周期：5m；止损：-0.99；评分：6.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### Obelisk_3EMA_StochRSI_ATR.py

- 文件：[Obelisk_3EMA_StochRSI_ATR.py](freqtrade-strategies/strategies/Obelisk_3EMA_StochRSI_ATR/Obelisk_3EMA_StochRSI_ATR.py)
- 周期：5m；止损：-0.99；评分：6.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ATR，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### LookaheadStrategy.py

- 文件：[LookaheadStrategy.py](freqtrade-strategies/strategies/LookaheadStrategy/LookaheadStrategy.py)
- 周期：5m；止损：-0.194；评分：5.5
- 评审结论：概览：接口V3，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### Combined_Indicators.py

- 文件：[Combined_Indicators.py](freqtrade-strategies/strategies/Combined_Indicators/Combined_Indicators.py)
- 周期：1m；止损：-0.0658；评分：5.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ObeliskRSI_v6_1.py

- 文件：[ObeliskRSI_v6_1.py](freqtrade-strategies/strategies/ObeliskRSI_v6_1/ObeliskRSI_v6_1.py)
- 周期：5m；止损：-0.3；评分：5.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：风控导向。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MACD_TRIPLE_MA.py

- 文件：[MACD_TRIPLE_MA.py](freqtrade-strategies/strategies/MACD_TRIPLE_MA/MACD_TRIPLE_MA.py)
- 周期：5m；止损：-0.03；评分：5.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### XebTradeStrat.py

- 文件：[XebTradeStrat.py](freqtrade-strategies/strategies/XebTradeStrat/XebTradeStrat.py)
- 周期：1m；止损：-0.01；评分：5.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### FixedRiskRewardLoss.py

- 文件：[FixedRiskRewardLoss.py](freqtrade-strategies/strategies/FixedRiskRewardLoss/FixedRiskRewardLoss.py)
- 周期：5m；止损：-0.9；评分：5.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、ATR，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：风控导向。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Scalp.py

- 文件：[Scalp.py](freqtrade-strategies/strategies/Scalp/Scalp.py)
- 周期：1m；止损：-0.04；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MACD_TRI_EMA.py

- 文件：[MACD_TRI_EMA.py](freqtrade-strategies/strategies/MACD_TRI_EMA/MACD_TRI_EMA.py)
- 周期：5m；止损：-0.03；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AverageStrategy.py

- 文件：[AverageStrategy.py](freqtrade-strategies/strategies/AverageStrategy/AverageStrategy.py)
- 周期：4h；止损：-0.2；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ADX_15M_USDT.py

- 文件：[ADX_15M_USDT.py](freqtrade-strategies/strategies/ADX_15M_USDT/ADX_15M_USDT.py)
- 周期：Unknown；止损：-0.1255；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BinHV45.py

- 文件：[BinHV45.py](freqtrade-strategies/strategies/BinHV45/BinHV45.py)
- 周期：1m；止损：-0.05；评分：5.0
- 评审结论：概览：接口V2，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SmoothOperator.py

- 文件：[SmoothOperator.py](freqtrade-strategies/strategies/SmoothOperator/SmoothOperator.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：低；风格：模板化/堆叠型。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### ObeliskIM_v1_1.py

- 文件：[ObeliskIM_v1_1.py](freqtrade-strategies/strategies/ObeliskIM_v1_1/ObeliskIM_v1_1.py)
- 周期：5m；止损：-0.04；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：低；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### ClucMay72018.py

- 文件：[ClucMay72018.py](freqtrade-strategies/strategies/ClucMay72018/ClucMay72018.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MACDRSI200.py

- 文件：[MACDRSI200.py](freqtrade-strategies/strategies/MACDRSI200/MACDRSI200.py)
- 周期：Unknown；止损：-0.04032；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### adaptive.py

- 文件：[adaptive.py](freqtrade-strategies/strategies/adaptive/adaptive.py)
- 周期：5m；止损：-0.109；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MultiRSI.py

- 文件：[MultiRSI.py](freqtrade-strategies/strategies/MultiRSI/MultiRSI.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润

### BreakEven.py

- 文件：[BreakEven.py](freqtrade-strategies/strategies/BreakEven/BreakEven.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Obelisk_TradePro_Ichi_v1_1.py

- 文件：[Obelisk_TradePro_Ichi_v1_1.py](freqtrade-strategies/strategies/Obelisk_TradePro_Ichi_v1_1/Obelisk_TradePro_Ichi_v1_1.py)
- 周期：1h；止损：-0.015；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MFI.py

- 文件：[MFI.py](freqtrade-strategies/strategies/MFI/MFI.py)
- 周期：5m；止损：-0.1；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BBRSI4cust.py

- 文件：[BBRSI4cust.py](freqtrade-strategies/strategies/BBRSI4cust/BBRSI4cust.py)
- 周期：15m；止损：-0.1；评分：5.0
- 评审结论：概览：接口V3，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### EMASkipPump.py

- 文件：[EMASkipPump.py](freqtrade-strategies/strategies/EMASkipPump/EMASkipPump.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### VWAP.py

- 文件：[VWAP.py](freqtrade-strategies/strategies/VWAP/VWAP.py)
- 周期：5m；止损：-0.15；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、VWAP，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Low_BB.py

- 文件：[Low_BB.py](freqtrade-strategies/strategies/Low_BB/Low_BB.py)
- 周期：1m；止损：-0.015；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Leveraged.py

- 文件：[Leveraged.py](freqtrade-strategies/strategies/Leveraged/Leveraged.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### macd_recovery.py

- 文件：[macd_recovery.py](freqtrade-strategies/strategies/macd_recovery/macd_recovery.py)
- 周期：Unknown；止损：-0.04032；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### CMCWinner.py

- 文件：[CMCWinner.py](freqtrade-strategies/strategies/CMCWinner/CMCWinner.py)
- 周期：15m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### UziChan.py

- 文件：[UziChan.py](freqtrade-strategies/strategies/UziChan/UziChan.py)
- 周期：5m；止损：-0.1；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), pandas_ta。 可读性：中；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突

### heikin.py

- 文件：[heikin.py](freqtrade-strategies/strategies/heikin/heikin.py)
- 周期：1h；止损：-0.99；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；疑似虚假止损但未发现自定义止损逻辑。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### hansencandlepatternV1.py

- 文件：[hansencandlepatternV1.py](freqtrade-strategies/strategies/hansencandlepatternV1/hansencandlepatternV1.py)
- 周期：1h；止损：-0.1；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### ReinforcedQuickie.py

- 文件：[ReinforcedQuickie.py](freqtrade-strategies/strategies/ReinforcedQuickie/ReinforcedQuickie.py)
- 周期：5m；止损：-0.05；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### EMAVolume.py

- 文件：[EMAVolume.py](freqtrade-strategies/strategies/EMAVolume/EMAVolume.py)
- 周期：Unknown；止损：-0.2；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AlligatorStrat.py

- 文件：[AlligatorStrat.py](freqtrade-strategies/strategies/AlligatorStrat/AlligatorStrat.py)
- 周期：Unknown；止损：-0.2；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、SMA、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BbandRsiRolling.py

- 文件：[BbandRsiRolling.py](freqtrade-strategies/strategies/BbandRsiRolling/BbandRsiRolling.py)
- 周期：5m；止损：-0.08；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BinHV45HO.py

- 文件：[BinHV45HO.py](freqtrade-strategies/strategies/BinHV45HO/BinHV45HO.py)
- 周期：1m；止损：-0.19；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ReinforcedSmoothScalp.py

- 文件：[ReinforcedSmoothScalp.py](freqtrade-strategies/strategies/ReinforcedSmoothScalp/ReinforcedSmoothScalp.py)
- 周期：1m；止损：-0.1；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### CCIStrategy.py

- 文件：[CCIStrategy.py](freqtrade-strategies/strategies/CCIStrategy/CCIStrategy.py)
- 周期：1m；止损：-0.02；评分：5.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA、BBANDS、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BBRSI3366.py

- 文件：[BBRSI3366.py](freqtrade-strategies/strategies/BBRSI3366/BBRSI3366.py)
- 周期：5m；止损：-0.33233；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichimoku_v32.py

- 文件：[Ichimoku_v32.py](freqtrade-strategies/strategies/Ichimoku_v32/Ichimoku_v32.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### BBRSI21.py

- 文件：[BBRSI21.py](freqtrade-strategies/strategies/BBRSI21/BBRSI21.py)
- 周期：5m；止损：-0.30054；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichimoku_v30.py

- 文件：[Ichimoku_v30.py](freqtrade-strategies/strategies/Ichimoku_v30/Ichimoku_v30.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### SwingHigh.py

- 文件：[SwingHigh.py](freqtrade-strategies/strategies/SwingHigh/SwingHigh.py)
- 周期：Unknown；止损：-0.22274；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### DD.py

- 文件：[DD.py](freqtrade-strategies/strategies/DD/DD.py)
- 周期：5m；止损：-0.32745；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### adxbbrsi2.py

- 文件：[adxbbrsi2.py](freqtrade-strategies/strategies/adxbbrsi2/adxbbrsi2.py)
- 周期：1h；止损：-0.32237；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS、ADX、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichimoku_v33.py

- 文件：[Ichimoku_v33.py](freqtrade-strategies/strategies/Ichimoku_v33/Ichimoku_v33.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### Trend_Strength_Directional.py

- 文件：[Trend_Strength_Directional.py](freqtrade-strategies/strategies/Trend_Strength_Directional/Trend_Strength_Directional.py)
- 周期：15m；止损：-0.314；评分：4.5
- 评审结论：概览：接口V2，方法风格 entry/exit，主要指标 RSI、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### adx_opt_strat.py

- 文件：[adx_opt_strat.py](freqtrade-strategies/strategies/adx_opt_strat/adx_opt_strat.py)
- 周期：Unknown；止损：-0.32766；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Bandtastic.py

- 文件：[Bandtastic.py](freqtrade-strategies/strategies/Bandtastic/Bandtastic.py)
- 周期：15m；止损：-0.345；评分：4.5
- 评审结论：概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、MFI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Ichimoku_v12.py

- 文件：[Ichimoku_v12.py](freqtrade-strategies/strategies/Ichimoku_v12/Ichimoku_v12.py)
- 周期：Unknown；止损：-1.0；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### e6v34.py

- 文件：[e6v34.py](freqtrade-strategies/strategies/e6v34/e6v34.py)
- 周期：15m；止损：-0.54；评分：4.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ADX_15M_USDT2.py

- 文件：[ADX_15M_USDT2.py](freqtrade-strategies/strategies/ADX_15M_USDT2/ADX_15M_USDT2.py)
- 周期：Unknown；止损：-0.31941；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### HourBasedStrategy.py

- 文件：[HourBasedStrategy.py](freqtrade-strategies/strategies/HourBasedStrategy/HourBasedStrategy.py)
- 周期：1h；止损：-0.292；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SMAOffsetProtectOpt.py

- 文件：[SMAOffsetProtectOpt.py](freqtrade-strategies/strategies/SMAOffsetProtectOpt/SMAOffsetProtectOpt.py)
- 周期：5m；止损：-0.5；评分：4.0
- 评审结论：概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### WaveTrendStra.py

- 文件：[WaveTrendStra.py](freqtrade-strategies/strategies/WaveTrendStra/WaveTrendStra.py)
- 周期：4h；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### CofiBitStrategy.py

- 文件：[CofiBitStrategy.py](freqtrade-strategies/strategies/CofiBitStrategy/CofiBitStrategy.py)
- 周期：5m；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 EMA、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Roth03.py

- 文件：[Roth03.py](freqtrade-strategies/strategies/Roth03/Roth03.py)
- 周期：5m；止损：-0.31939；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI、STOCH、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Quickie.py

- 文件：[Quickie.py](freqtrade-strategies/strategies/Quickie/Quickie.py)
- 周期：5m；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、SMA、BBANDS、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ASDTSRockwellTrading.py

- 文件：[ASDTSRockwellTrading.py](freqtrade-strategies/strategies/ASDTSRockwellTrading/ASDTSRockwellTrading.py)
- 周期：5m；止损：-0.3；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SmoothScalp.py

- 文件：[SmoothScalp.py](freqtrade-strategies/strategies/SmoothScalp/SmoothScalp.py)
- 周期：1m；止损：-0.5；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、MFI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### Roth01.py

- 文件：[Roth01.py](freqtrade-strategies/strategies/Roth01/Roth01.py)
- 周期：5m；止损：-0.29585；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI、STOCH、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### ADXMomentum.py

- 文件：[ADXMomentum.py](freqtrade-strategies/strategies/ADXMomentum/ADXMomentum.py)
- 周期：1h；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Simple.py

- 文件：[Simple.py](freqtrade-strategies/strategies/Simple/Simple.py)
- 周期：5m；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### keltnerchannel.py

- 文件：[keltnerchannel.py](freqtrade-strategies/strategies/keltnerchannel/keltnerchannel.py)
- 周期：6h；止损：-0.254；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), pandas_ta, freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### BbandRsi.py

- 文件：[BbandRsi.py](freqtrade-strategies/strategies/BbandRsi/BbandRsi.py)
- 周期：1h；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Cci.py

- 文件：[Cci.py](freqtrade-strategies/strategies/Cci/Cci.py)
- 周期：1m；止损：-0.23；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AdxSmas.py

- 文件：[AdxSmas.py](freqtrade-strategies/strategies/AdxSmas/AdxSmas.py)
- 周期：1h；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Chispei.py

- 文件：[Chispei.py](freqtrade-strategies/strategies/Chispei/Chispei.py)
- 周期：Unknown；止损：-0.32336；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### AwesomeMacd.py

- 文件：[AwesomeMacd.py](freqtrade-strategies/strategies/AwesomeMacd/AwesomeMacd.py)
- 周期：1h；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### SwingHighToSky.py

- 文件：[SwingHighToSky.py](freqtrade-strategies/strategies/SwingHighToSky/SwingHighToSky.py)
- 周期：15m；止损：-0.34338；评分：4.0
- 评审结论：概览：接口V2，方法风格 entry/exit，主要指标 RSI、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：工程化/多周期。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）。
- 建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count

### MACDCCI.py

- 文件：[MACDCCI.py](freqtrade-strategies/strategies/MACDCCI/MACDCCI.py)
- 周期：Unknown；止损：-0.3；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：工程化/多周期。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；使用多周期合并（需关注对齐与前视偏差）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### BinHV27.py

- 文件：[BinHV27.py](freqtrade-strategies/strategies/BinHV27/BinHV27.py)
- 周期：5m；止损：-0.5；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ADX，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### MACD_EMA.py

- 文件：[MACD_EMA.py](freqtrade-strategies/strategies/MACD_EMA/MACD_EMA.py)
- 周期：5m；止损：-0.25；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、EMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### Ichess.py

- 文件：[Ichess.py](freqtrade-strategies/strategies/Ichess/Ichess.py)
- 周期：1d；止损：-0.314；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA、ICHIMOKU，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：中；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MACDStrategy_crossed.py

- 文件：[MACDStrategy_crossed.py](freqtrade-strategies/strategies/MACDStrategy_crossed/MACDStrategy_crossed.py)
- 周期：5m；止损：-0.3；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### MACDStrategy.py

- 文件：[MACDStrategy.py](freqtrade-strategies/strategies/MACDStrategy/MACDStrategy.py)
- 周期：5m；止损：-0.3；评分：4.0
- 评审结论：概览：接口V2，方法风格 entry/exit，主要指标 MACD、CCI，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：接口版本与方法命名可能不匹配（升级/运行风险）；止损较大（回撤风险偏高）。
- 建议：
  - 建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制

### HansenSmaOffsetV1.py

- 文件：[HansenSmaOffsetV1.py](freqtrade-strategies/strategies/HansenSmaOffsetV1/HansenSmaOffsetV1.py)
- 周期：15m；止损：-99.0；评分：4.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）；止损较大（回撤风险偏高）；存在 lint/格式化禁用标记（可能隐藏无用代码）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性
  - 建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码

### JustROCR6.py

- 文件：[JustROCR6.py](freqtrade-strategies/strategies/JustROCR6/JustROCR6.py)
- 周期：Unknown；止损：-0.01；评分：3.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### JustROCR3.py

- 文件：[JustROCR3.py](freqtrade-strategies/strategies/JustROCR3/JustROCR3.py)
- 周期：Unknown；止损：-0.01；评分：3.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### JustROCR.py

- 文件：[JustROCR.py](freqtrade-strategies/strategies/JustROCR/JustROCR.py)
- 周期：Unknown；止损：-0.2；评分：3.5
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### TechnicalExampleStrategy.py

- 文件：[TechnicalExampleStrategy.py](freqtrade-strategies/strategies/TechnicalExampleStrategy/TechnicalExampleStrategy.py)
- 周期：5m；止损：-0.05；评分：3.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### Stavix2.py

- 文件：[Stavix2.py](freqtrade-strategies/strategies/Stavix2/Stavix2.py)
- 周期：Unknown；止损：-0.1；评分：3.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 freqtrade.vendor.qtpylib。 可读性：高；风格：常规。风险点：依赖 vendor qtpylib 路径（未来版本兼容风险）。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）
  - 建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性

### JustROCR5.py

- 文件：[JustROCR5.py](freqtrade-strategies/strategies/JustROCR5/JustROCR5.py)
- 周期：1m；止损：-0.01；评分：3.0
- 评审结论：概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

### AlwaysBuy.py

- 文件：[AlwaysBuy.py](freqtrade-strategies/strategies/AlwaysBuy/AlwaysBuy.py)
- 周期：5m；止损：-0.2；评分：1.0
- 评审结论：概览：接口V3，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：未发现明显结构性风险。
- 建议：
  - 建议补充保护机制(Protections)，如 cooldown/stoploss guard
  - 建议评估开启移动止损，用于锁定利润
  - 止损偏大，建议收紧或配合动态止损/保护机制
  - 建议启用主动离场信号或补充退出条件
  - 逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声
  - 指标较少，建议增加二次确认（趋势+动量或波动率）

## 其它策略摘要

| 序号 | 策略名称 | 周期 | 止损 | 评分 | 可读性 | 风格 | 一句话评审 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [AlexNexusForgeV8A...](user_data/strategies/AlexNexusForgeV8AIV2.py) | 1h | -0.11 | 9.5 | 中 | 实验性/研究型 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、ATR、ML、WAVELET，指标库 TA... |
| 2 | [AlexNexusForgeV8A...](user_data/strategies/AlexNexusForgeV8AIV3.py) | 1h | -0.05 | 9.5 | 中 | 实验性/研究型 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、ATR、ML、WAVELET，指标库 TA... |
| 3 | [MultiMA_TSL.py](freqtrade-strategies/strategies/MultiMA_TSL/MultiMA_TSL.py) | 5m | -0.15 | 8.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 4 | [Momentumv2.py](freqtrade-strategies/strategies/Momentumv2/Momentumv2.py) | 4h | -0.08 | 8.0 | 高 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、ATR，指标库 TA-Lib(ta), freqt... |
| 5 | [BB_RPB_TSL_SMA_Tr...](freqtrade-strategies/strategies/BB_RPB_TSL_SMA_Tranz_TB_MOD/BB_RPB_TSL_SMA_Tranz_TB_MOD.py) | 5m | -0.15 | 8.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 6 | [MultiMA_TSL3.py](freqtrade-strategies/strategies/MultiMA_TSL3/MultiMA_TSL3.py) | 5m | -0.15 | 8.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ATR，指标库 TA-Lib(ta), freqtr... |
| 7 | [MultiMA_TSL3_Mod.py](freqtrade-strategies/strategies/MultiMA_TSL3_Mod/MultiMA_TSL3_Mod.py) | 5m | -0.15 | 8.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ATR，指标库 TA-Lib(ta), freqtr... |
| 8 | [AlexNexusForgeV7.py](user_data/strategies/AlexNexusForgeV7.py) | 1h | -0.05 | 8.0 | 中 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、ADX，指标库 TA-Lib(ta), freqt... |
| 9 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV6H/CombinedBinHAndClucV6H.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR，指标库 TA-Lib(ta),... |
| 10 | [BcmbigzDevelop.py](freqtrade-strategies/strategies/BcmbigzDevelop/BcmbigzDevelop.py) | 5m | -0.99 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR、MFI，指标库 TA... |
| 11 | [BinClucMadDevelop.py](freqtrade-strategies/strategies/BinClucMadDevelop/BinClucMadDevelop.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 12 | [BigPete.py](freqtrade-strategies/strategies/BigPete/BigPete.py) | 5m | -0.99 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR，指标库 TA-Lib... |
| 13 | [MADisplaceV3.py](freqtrade-strategies/strategies/MADisplaceV3/MADisplaceV3.py) | 5m | -0.2 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 14 | [ElliotV8_original...](freqtrade-strategies/strategies/ElliotV8_original_ichiv3/ElliotV8_original_ichiv3.py) | 5m | -0.2 | 7.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 15 | [FRAYSTRAT.py](freqtrade-strategies/strategies/FRAYSTRAT/FRAYSTRAT.py) | 15m | -0.1 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 16 | [CryptoFrog.py](freqtrade-strategies/strategies/CryptoFrog/CryptoFrog.py) | 5m | -0.085 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 17 | [ElliotV5HO.py](freqtrade-strategies/strategies/ElliotV5HO/ElliotV5HO.py) | 5m | -0.189 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、MFI、STOCH、ROC…... |
| 18 | [GodCard.py](freqtrade-strategies/strategies/GodCard/GodCard.py) | 5m | -0.087 | 7.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 19 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8Hyper/CombinedBinHAndClucV8Hyper.py) | 5m | -0.99 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 20 | [CryptoFrogHO2A.py](freqtrade-strategies/strategies/CryptoFrogHO2A/CryptoFrogHO2A.py) | 5m | -0.13 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 21 | [ElliotV5HOMod2.py](freqtrade-strategies/strategies/ElliotV5HOMod2/ElliotV5HOMod2.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 22 | [NormalizerStrateg...](freqtrade-strategies/strategies/NormalizerStrategyHO2/NormalizerStrategyHO2.py) | 1h | -0.99 | 7.0 | 高 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 23 | [ElliotV8_original...](freqtrade-strategies/strategies/ElliotV8_original_ichiv2/ElliotV8_original_ichiv2.py) | 5m | -0.2 | 7.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 24 | [Combined_NFIv6_SM...](freqtrade-strategies/strategies/Combined_NFIv6_SMA/Combined_NFIv6_SMA.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 25 | [NormalizerStrateg...](freqtrade-strategies/strategies/NormalizerStrategy/NormalizerStrategy.py) | 1h | -0.99 | 7.0 | 高 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 26 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV6/CombinedBinHAndClucV6.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR，指标库 TA-Lib(ta),... |
| 27 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV5Hyperoptable/CombinedBinHAndClucV5Hyperoptable.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 28 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV5/CombinedBinHAndClucV5.py) | 5m | -0.99 | 7.0 | 中 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 29 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV7/CombinedBinHAndClucV7.py) | 5m | -0.99 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 30 | [CryptoFrogHO2.py](freqtrade-strategies/strategies/CryptoFrogHO2/CryptoFrogHO2.py) | 5m | -0.13 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 31 | [EI3v2_tag_cofi_gr...](freqtrade-strategies/strategies/EI3v2_tag_cofi_green/EI3v2_tag_cofi_green.py) | 5m | -0.99 | 7.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ADX，指标库 TA-Lib(ta), freqtr... |
| 32 | [NASOSv4.py](freqtrade-strategies/strategies/NASOSv4/NASOSv4.py) | 5m | -0.15 | 7.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 33 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV3/CombinedBinHAndClucV3.py) | 5m | -0.99 | 7.0 | 高 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 34 | [CryptoFrogHO.py](freqtrade-strategies/strategies/CryptoFrogHO/CryptoFrogHO.py) | 5m | -0.13 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 35 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV4/CombinedBinHAndClucV4.py) | 5m | -0.99 | 7.0 | 中 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 36 | [CryptoFrogOffset.py](freqtrade-strategies/strategies/CryptoFrogOffset/CryptoFrogOffset.py) | 5m | -0.085 | 7.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、ATR、MFI…，指... |
| 37 | [AlexNexusForgeV6.py](user_data/strategies/AlexNexusForgeV6.py) | 1h | -0.05 | 7.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、ADX，指标库 TA-Lib(ta), freqt... |
| 38 | [AlexNexusForgeV4.py](user_data/strategies/AlexNexusForgeV4.py) | 1h | -0.04 | 7.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ATR，指标库 TA-Lib(ta)。 可读性：中；风格：常... |
| 39 | [NFIX_BB_RPB.py](freqtrade-strategies/strategies/NFIX_BB_RPB/NFIX_BB_RPB.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 40 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV9/CombinedBinHClucAndMADV9.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR，指标库 TA-Lib(ta),... |
| 41 | [ClucHAnix_hhll.py](freqtrade-strategies/strategies/ClucHAnix_hhll/ClucHAnix_hhll.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ROC，指标库 TA-Lib(ta),... |
| 42 | [BigZ07.py](freqtrade-strategies/strategies/BigZ07/BigZ07.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS，指标库 TA-Lib(ta), fr... |
| 43 | [SMAOffsetV2.py](freqtrade-strategies/strategies/SMAOffsetV2/SMAOffsetV2.py) | 5m | -0.2 | 6.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta)。 可读性：高；风格：工程化/多... |
| 44 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8XH/CombinedBinHAndClucV8XH.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 45 | [BigZ03HO.py](freqtrade-strategies/strategies/BigZ03HO/BigZ03HO.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 46 | [HyperStra_GSN_SMA...](freqtrade-strategies/strategies/HyperStra_GSN_SMAOnly/HyperStra_GSN_SMAOnly.py) | 5m | -0.05 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 47 | [BB_RPB_TSL_BI.py](freqtrade-strategies/strategies/BB_RPB_TSL_BI/BB_RPB_TSL_BI.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 48 | [NASOSRv6_private_...](freqtrade-strategies/strategies/NASOSRv6_private_Reinuvader_20211121/NASOSRv6_private_Reinuvader_20211121.py) | 5m | -0.15 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR、ROC，指标库 TA... |
| 49 | [BigZ03.py](freqtrade-strategies/strategies/BigZ03/BigZ03.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 50 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD_E0V1E_ROI/ClucHAnix_BB_RPB_MOD_E0V1E_ROI.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ROC，指标库 TA-Lib(... |
| 51 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyLite/NotAnotherSMAOffsetStrategyLite.py) | 5m | -0.1 | 6.5 | 高 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 52 | [BinClucMadV1.py](freqtrade-strategies/strategies/BinClucMadV1/BinClucMadV1.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR、MFI，指标库 TA... |
| 53 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucHyperV3/CombinedBinHAndClucHyperV3.py) | 1m | -0.06 | 6.5 | 中 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ATR，指标库 TA-Lib(ta), freqtra... |
| 54 | [BB_RPB_TSL_RNG_2.py](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_2/BB_RPB_TSL_RNG_2.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、STOCH、CCI，指标库 T... |
| 55 | [BB_RPB_TSL_RNG_VW...](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_VWAP/BB_RPB_TSL_RNG_VWAP.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、STOCH、VWAP、CCI，... |
| 56 | [BB_RPB_TSL_RNG.py](freqtrade-strategies/strategies/BB_RPB_TSL_RNG/BB_RPB_TSL_RNG.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、STOCH、CCI，指标库 T... |
| 57 | [MostOfAll.py](freqtrade-strategies/strategies/MostOfAll/MostOfAll.py) | 5m | -0.2 | 6.5 | 高 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 58 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD/ClucHAnix_BB_RPB_MOD.py) | 1m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ROC，指标库 TA-Lib(... |
| 59 | [BcmbigzV1.py](freqtrade-strategies/strategies/BcmbigzV1/BcmbigzV1.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS，指标库 TA-Lib(ta), fr... |
| 60 | [BigZ04HO2.py](freqtrade-strategies/strategies/BigZ04HO2/BigZ04HO2.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 61 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD2_ROI/ClucHAnix_BB_RPB_MOD2_ROI.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ROC，指标库 TA-Lib(... |
| 62 | [NFI46FrogZ.py](freqtrade-strategies/strategies/NFI46FrogZ/NFI46FrogZ.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 63 | [BigZ0407.py](freqtrade-strategies/strategies/BigZ0407/BigZ0407.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI，指标库 TA-Lib... |
| 64 | [BigZ04_TSL3.py](freqtrade-strategies/strategies/BigZ04_TSL3/BigZ04_TSL3.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR，指标库 TA-Lib... |
| 65 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV3/CombinedBinHClucAndMADV3.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS，指标库 TA-Lib(ta), fr... |
| 66 | [BBRSIv2.py](freqtrade-strategies/strategies/BBRSIv2/BBRSIv2.py) | 15m | -0.99 | 6.5 | 高 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 67 | [BigZ04.py](freqtrade-strategies/strategies/BigZ04/BigZ04.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 68 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV6/CombinedBinHClucAndMADV6.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR，指标库 TA-Lib... |
| 69 | [BinClucMad.py](freqtrade-strategies/strategies/BinClucMad/BinClucMad.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR，指标库 TA-Lib... |
| 70 | [CombinedBinHClucA...](freqtrade-strategies/strategies/CombinedBinHClucAndMADV5/CombinedBinHClucAndMADV5.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR，指标库 TA-Lib... |
| 71 | [BB_RPB_TSL_RNG_TB...](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_TBS_GOLD/BB_RPB_TSL_RNG_TBS_GOLD.py) | 5m | -0.049 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、STOCH、CCI，指标库 T... |
| 72 | [BigZ0307HO.py](freqtrade-strategies/strategies/BigZ0307HO/BigZ0307HO.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI，指标库 TA-Lib... |
| 73 | [BB_RPB_TSL_c7c477...](freqtrade-strategies/strategies/BB_RPB_TSL_c7c477d_20211030/BB_RPB_TSL_c7c477d_20211030.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、STOCH、ICHIMOKU、... |
| 74 | [BigZ0407HO.py](freqtrade-strategies/strategies/BigZ0407HO/BigZ0407HO.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI，指标库 TA-Lib... |
| 75 | [NASOSv5.py](freqtrade-strategies/strategies/NASOSv5/NASOSv5.py) | 5m | -0.15 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 76 | [ClucHAnix_5m.py](freqtrade-strategies/strategies/ClucHAnix_5m/ClucHAnix_5m.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、ROC，指标库 TA-Lib(ta), fre... |
| 77 | [NFI46Z.py](freqtrade-strategies/strategies/NFI46Z/NFI46Z.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI，指标库 TA-Lib... |
| 78 | [ClucHAnix5m.py](freqtrade-strategies/strategies/ClucHAnix5m/ClucHAnix5m.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ROC，指标库 TA-Lib(... |
| 79 | [BBMod1.py](freqtrade-strategies/strategies/BBMod1/BBMod1.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 80 | [BB_RPB_TSL_2.py](freqtrade-strategies/strategies/BB_RPB_TSL_2/BB_RPB_TSL_2.py) | 3m | -0.15 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 81 | [true_lambo.py](freqtrade-strategies/strategies/true_lambo/true_lambo.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、MFI、VWAP、ROC…，指... |
| 82 | [NFIX_BB_RPB_c7c47...](freqtrade-strategies/strategies/NFIX_BB_RPB_c7c477d_20211030/NFIX_BB_RPB_c7c477d_20211030.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、STOCH、ICHIM... |
| 83 | [MacheteV8bRallimo...](freqtrade-strategies/strategies/MacheteV8bRallimod2/MacheteV8bRallimod2.py) | 5m | -0.05 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、ICHIMOKU、ROC，指标... |
| 84 | [BB_RPB_TSL_BIV1.py](freqtrade-strategies/strategies/BB_RPB_TSL_BIV1/BB_RPB_TSL_BIV1.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 85 | [BigZ04_TSL4.py](freqtrade-strategies/strategies/BigZ04_TSL4/BigZ04_TSL4.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ATR，指标库 TA-Lib... |
| 86 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucHyperV0/CombinedBinHAndClucHyperV0.py) | 1m | -0.1 | 6.5 | 中 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 87 | [ClucHAnix_BB_RPB_...](freqtrade-strategies/strategies/ClucHAnix_BB_RPB_MOD_CTT/ClucHAnix_BB_RPB_MOD_CTT.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ROC，指标库 TA-Lib(... |
| 88 | [ClucHAnix.py](freqtrade-strategies/strategies/ClucHAnix/ClucHAnix.py) | 1m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、ROC，指标库 TA-Lib(ta), fre... |
| 89 | [BB_RPB_TSL.py](freqtrade-strategies/strategies/BB_RPB_TSL/BB_RPB_TSL.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 90 | [BB_RPB_TSLmeneguz...](freqtrade-strategies/strategies/BB_RPB_TSLmeneguzzo/BB_RPB_TSLmeneguzzo.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 91 | [HyperStra_SMAOnly.py](freqtrade-strategies/strategies/HyperStra_SMAOnly/HyperStra_SMAOnly.py) | 5m | -0.05 | 6.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 92 | [BigZ04HO.py](freqtrade-strategies/strategies/BigZ04HO/BigZ04HO.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 93 | [Uptrend.py](freqtrade-strategies/strategies/Uptrend/Uptrend.py) | 5m | -0.1 | 6.5 | 低 | 模板化/堆叠型 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 94 | [BB_RPB_TSL_RNG_TB...](freqtrade-strategies/strategies/BB_RPB_TSL_RNG_TBS/BB_RPB_TSL_RNG_TBS.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、STOCH、CCI，指标库 T... |
| 95 | [ClucHAnix_5m1.py](freqtrade-strategies/strategies/ClucHAnix_5m1/ClucHAnix_5m1.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、ROC，指标库 TA-Lib(ta), fre... |
| 96 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8XHO/CombinedBinHAndClucV8XHO.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 97 | [BB_RPB_TSL_Tranz.py](freqtrade-strategies/strategies/BB_RPB_TSL_Tranz/BB_RPB_TSL_Tranz.py) | 5m | -0.99 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 98 | [BigZ06.py](freqtrade-strategies/strategies/BigZ06/BigZ06.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 99 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV8/CombinedBinHAndClucV8.py) | 5m | -0.99 | 6.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 100 | [MacheteV8b.py](freqtrade-strategies/strategies/MacheteV8b/MacheteV8b.py) | 15m | -0.1 | 6.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、ATR、ICHIMO... |
| 101 | [CryptoFrogHO3A4.py](freqtrade-strategies/strategies/CryptoFrogHO3A4/CryptoFrogHO3A4.py) | 5m | -0.299 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 102 | [CryptoFrogNFIHO1A.py](freqtrade-strategies/strategies/CryptoFrogNFIHO1A/CryptoFrogNFIHO1A.py) | 5m | -0.299 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 103 | [CryptoFrogHO3A3.py](freqtrade-strategies/strategies/CryptoFrogHO3A3/CryptoFrogHO3A3.py) | 5m | -0.299 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 104 | [CryptoFrogHO3A1.py](freqtrade-strategies/strategies/CryptoFrogHO3A1/CryptoFrogHO3A1.py) | 5m | -0.299 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 105 | [NASOSv5_mod1_DanM...](freqtrade-strategies/strategies/NASOSv5_mod1_DanMod/NASOSv5_mod1_DanMod.py) | 5m | -0.3 | 6.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、VWAP，指标库 TA-Lib(ta), freqt... |
| 106 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyModHO/NotAnotherSMAOffsetStrategyModHO.py) | 5m | -0.32 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ADX，指标库 TA-Lib(ta), freqtr... |
| 107 | [epretrace.py](freqtrade-strategies/strategies/epretrace/epretrace.py) | 5m | -0.999 | 6.0 | 中 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、ATR、ICHIMOKU、CCI，指标库 TA-L... |
| 108 | [CryptoFrogNFI.py](freqtrade-strategies/strategies/CryptoFrogNFI/CryptoFrogNFI.py) | 5m | -0.299 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 109 | [MiniLambo.py](freqtrade-strategies/strategies/MiniLambo/MiniLambo.py) | 1m | -0.1 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), pandas_ta, fre... |
| 110 | [Apollo11.py](freqtrade-strategies/strategies/Apollo11/Apollo11.py) | 15m | -0.16 | 6.0 | 中 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD、EMA、SMA、ATR，指标库 TA-Lib(ta), freqt... |
| 111 | [NASOSv5_mod3.py](freqtrade-strategies/strategies/NASOSv5_mod3/NASOSv5_mod3.py) | 5m | -0.3 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 112 | [BinClucMadSMADeve...](freqtrade-strategies/strategies/BinClucMadSMADevelop/BinClucMadSMADevelop.py) | 5m | -0.228 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 113 | [HarmonicDivergenc...](freqtrade-strategies/strategies/HarmonicDivergence/HarmonicDivergence.py) | 15m | -0.5 | 6.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、ATR、MFI、STOCH…... |
| 114 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901/NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901.py) | 5m | -0.9 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ADX，指标库 TA-Lib(ta), freqtr... |
| 115 | [ElliotV7.py](freqtrade-strategies/strategies/ElliotV7/ElliotV7.py) | 5m | -0.32 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS，指标库 TA-Lib(ta)... |
| 116 | [NASOSv5_mod2.py](freqtrade-strategies/strategies/NASOSv5_mod2/NASOSv5_mod2.py) | 5m | -0.3 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 117 | [PRICEFOLLOWINGX.py](freqtrade-strategies/strategies/PRICEFOLLOWINGX/PRICEFOLLOWINGX.py) | 15m | -0.5 | 6.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX，指标库 TA-Lib... |
| 118 | [BBRSITV.py](freqtrade-strategies/strategies/BBRSITV/BBRSITV.py) | 5m | -0.25 | 6.0 | 中 | 风控导向 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 119 | [NASOSv5_mod1.py](freqtrade-strategies/strategies/NASOSv5_mod1/NASOSv5_mod1.py) | 5m | -0.3 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 120 | [wtc.py](freqtrade-strategies/strategies/wtc/wtc.py) | 30m | -0.128 | 6.0 | 中 | 实验性/研究型 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、STOCH、ML，指标库 TA-Lib(ta), f... |
| 121 | [CoreStrategy.py](freqtrade-strategies/strategies/CoreStrategy/CoreStrategy.py) | 5m | -0.228 | 6.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI，指标库 TA-Lib(... |
| 122 | [CryptoFrogHO3A2.py](freqtrade-strategies/strategies/CryptoFrogHO3A2/CryptoFrogHO3A2.py) | 5m | -0.239 | 6.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 123 | [Inverse.py](freqtrade-strategies/strategies/Inverse/Inverse.py) | 1h | -0.2 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、ADX、ATR、MFI、STOCH、CCI，指标库 TA-L... |
| 124 | [Combined_NFIv7_SM...](freqtrade-strategies/strategies/Combined_NFIv7_SMA_Rallipanos_20210707/Combined_NFIv7_SMA_Rallipanos_20210707.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 125 | [Heracles.py](freqtrade-strategies/strategies/Heracles/Heracles.py) | 12h | -0.04655 | 5.5 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 126 | [SampleStrategyV2.py](freqtrade-strategies/strategies/SampleStrategyV2/SampleStrategyV2.py) | 5m | -0.2 | 5.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、ATR、MFI…，指... |
| 127 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_SMA/NostalgiaForInfinityV7_SMA.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 128 | [RalliV1_disable56.py](freqtrade-strategies/strategies/RalliV1_disable56/RalliV1_disable56.py) | 5m | -0.3 | 5.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 129 | [PRICEFOLLOWING2.py](freqtrade-strategies/strategies/PRICEFOLLOWING2/PRICEFOLLOWING2.py) | 15m | -0.1 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、ADX，指标库 TA-Lib(ta), freqt... |
| 130 | [EMA520015_V17.py](freqtrade-strategies/strategies/EMA520015_V17/EMA520015_V17.py) | 4h | -0.1 | 5.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD、EMA，指标库 TA-Lib(ta), freqtrade.ven... |
| 131 | [Hacklemore3.py](freqtrade-strategies/strategies/Hacklemore3/Hacklemore3.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 132 | [SMA_BBRSI.py](freqtrade-strategies/strategies/SMA_BBRSI/SMA_BBRSI.py) | 5m | -0.5 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ATR、CCI，指标库 TA-Lib(ta), pa... |
| 133 | [TemaMaster3.py](freqtrade-strategies/strategies/TemaMaster3/TemaMaster3.py) | 1m | -0.08848 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 134 | [Combined_NFIv7_SM...](freqtrade-strategies/strategies/Combined_NFIv7_SMA/Combined_NFIv7_SMA.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 135 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategy_uzi/NotAnotherSMAOffsetStrategy_uzi.py) | 5m | -0.07 | 5.5 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 136 | [DIV_v1.py](freqtrade-strategies/strategies/DIV_v1/DIV_v1.py) | 5m | -0.15 | 5.5 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta)。 可读性：中；风格：常规。风险点：未发... |
| 137 | [RalliV1.py](freqtrade-strategies/strategies/RalliV1/RalliV1.py) | 5m | -0.3 | 5.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 138 | [BBlower.py](freqtrade-strategies/strategies/BBlower/BBlower.py) | 5m | -0.13912 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 139 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategy_uzi3/NotAnotherSMAOffsetStrategy_uzi3.py) | 5m | -0.1 | 5.5 | 低 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 140 | [ClucHAwerk.py](freqtrade-strategies/strategies/ClucHAwerk/ClucHAwerk.py) | 1m | -0.02139 | 5.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ROC，指标库 TA-Lib(ta), freqtra... |
| 141 | [Obelisk_TradePro_...](freqtrade-strategies/strategies/Obelisk_TradePro_Ichi_v2_1/Obelisk_TradePro_Ichi_v2_1.py) | 1h | -0.075 | 5.5 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 ATR、ICHIMOKU、ROC，指标库 TA-Lib(ta), freqt... |
| 142 | [StochRSITEMA.py](freqtrade-strategies/strategies/StochRSITEMA/StochRSITEMA.py) | 5m | -0.02205 | 5.5 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、STOCH，指标库 TA-Lib(ta), freqtrade.ve... |
| 143 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_SMAv2/NostalgiaForInfinityV7_SMAv2.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 144 | [SMAOffset.py](freqtrade-strategies/strategies/SMAOffset/SMAOffset.py) | 5m | -0.5 | 5.5 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 145 | [SlowPotato.py](freqtrade-strategies/strategies/SlowPotato/SlowPotato.py) | 5m | -0.99 | 5.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 146 | [ActionZone.py](freqtrade-strategies/strategies/ActionZone/ActionZone.py) | 1d | -1.0 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 147 | [NFI46Frog.py](freqtrade-strategies/strategies/NFI46Frog/NFI46Frog.py) | 5m | -1.0 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 148 | [InverseV2.py](freqtrade-strategies/strategies/InverseV2/InverseV2.py) | 1h | -0.2 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、ADX、ATR、MFI、STOCH、CCI，指标库 TA-L... |
| 149 | [Obelisk_Ichimoku_...](freqtrade-strategies/strategies/Obelisk_Ichimoku_Slow_v1_3/Obelisk_Ichimoku_Slow_v1_3.py) | 1h | -0.99 | 5.5 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、ATR、ICHIMOKU，指标库 TA-Lib(ta), freqt... |
| 150 | [NFINextMultiOffse...](freqtrade-strategies/strategies/NFINextMultiOffsetAndHO2/NFINextMultiOffsetAndHO2.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 151 | [BBRSI2.py](freqtrade-strategies/strategies/BBRSI2/BBRSI2.py) | 1m | -0.2 | 5.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 152 | [MarketChyperHyper...](freqtrade-strategies/strategies/MarketChyperHyperStrategy/MarketChyperHyperStrategy.py) | 1h | -0.12447 | 5.5 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、ADX，指标库 TA-Lib(ta), f... |
| 153 | [NFI5MOHO_WIP_1.py](freqtrade-strategies/strategies/NFI5MOHO_WIP_1/NFI5MOHO_WIP_1.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 154 | [Hacklemore2.py](freqtrade-strategies/strategies/Hacklemore2/Hacklemore2.py) | 15m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 155 | [ElliotV8HO.py](freqtrade-strategies/strategies/ElliotV8HO/ElliotV8HO.py) | 5m | -0.189 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 156 | [NFI5MOHO.py](freqtrade-strategies/strategies/NFI5MOHO/NFI5MOHO.py) | 5m | -0.1 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 157 | [bestV2.py](freqtrade-strategies/strategies/bestV2/bestV2.py) | 5m | -0.19 | 5.5 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 158 | [NFI5MOHO_WIP_2.py](freqtrade-strategies/strategies/NFI5MOHO_WIP_2/NFI5MOHO_WIP_2.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 159 | [flawless_lambo.py](freqtrade-strategies/strategies/flawless_lambo/flawless_lambo.py) | 15m | -1.0 | 5.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、STOCH、VWAP，指标库... |
| 160 | [cryptohassle.py](freqtrade-strategies/strategies/cryptohassle/cryptohassle.py) | Unknown | -0.2 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、ADX，指标库 TA-Lib(ta), f... |
| 161 | [Combined_NFIv7_SM...](freqtrade-strategies/strategies/Combined_NFIv7_SMA_bAdBoY_20211204/Combined_NFIv7_SMA_bAdBoY_20211204.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 162 | [Cluc7werk.py](freqtrade-strategies/strategies/Cluc7werk/Cluc7werk.py) | 1m | -0.02 | 5.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 163 | [TemaPureTwo.py](freqtrade-strategies/strategies/TemaPureTwo/TemaPureTwo.py) | 5m | -0.11 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 164 | [NFI4Frog.py](freqtrade-strategies/strategies/NFI4Frog/NFI4Frog.py) | 5m | -1.0 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 165 | [PRICEFOLLOWING.py](freqtrade-strategies/strategies/PRICEFOLLOWING/PRICEFOLLOWING.py) | 5m | -0.1 | 5.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、ADX，指标库 TA-Lib(ta), freqt... |
| 166 | [Guacamole.py](freqtrade-strategies/strategies/Guacamole/Guacamole.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.... |
| 167 | [ElliotV2.py](freqtrade-strategies/strategies/ElliotV2/ElliotV2.py) | 5m | -0.179 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 168 | [TrixV21Strategy.py](freqtrade-strategies/strategies/TrixV21Strategy/TrixV21Strategy.py) | 1h | -0.31 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ATR、STOCH，指标库 TA-Lib(ta), ... |
| 169 | [Divergences.py](freqtrade-strategies/strategies/Divergences/Divergences.py) | 1h | -0.1 | 5.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 170 | [Ichimoku.py](freqtrade-strategies/strategies/Ichimoku/Ichimoku.py) | 5m | -0.1 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.ven... |
| 171 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyX1/NotAnotherSMAOffsetStrategyX1.py) | 5m | -0.35 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), pandas_ta,... |
| 172 | [TemaPure.py](freqtrade-strategies/strategies/TemaPure/TemaPure.py) | 5m | -0.09754 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 173 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_SMAv2_1/NostalgiaForInfinityV7_SMAv2_1.py) | 5m | -0.99 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 174 | [BB_RSI.py](freqtrade-strategies/strategies/BB_RSI/BB_RSI.py) | Unknown | -0.06491 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 175 | [TemaPureNeat.py](freqtrade-strategies/strategies/TemaPureNeat/TemaPureNeat.py) | 5m | -0.10145 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 176 | [TemaMaster.py](freqtrade-strategies/strategies/TemaMaster/TemaMaster.py) | 5m | -0.14791 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 177 | [ONUR.py](freqtrade-strategies/strategies/ONUR/ONUR.py) | 15m | -0.99 | 5.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 178 | [TrixV23Strategy.py](freqtrade-strategies/strategies/TrixV23Strategy/TrixV23Strategy.py) | 1h | -0.31 | 5.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ATR、STOCH，指标库 TA-Lib(ta), ... |
| 179 | [Ichimoku_SenkouSp...](freqtrade-strategies/strategies/Ichimoku_SenkouSpanCross/Ichimoku_SenkouSpanCross.py) | 4h | -0.99 | 5.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ICHIMOKU，指标库 TA-Lib(ta), freqtrade... |
| 180 | [BB_RPB_TSL_SMA_Tr...](freqtrade-strategies/strategies/BB_RPB_TSL_SMA_Tranz/BB_RPB_TSL_SMA_Tranz.py) | 5m | -0.15 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 181 | [Persia.py](freqtrade-strategies/strategies/Persia/Persia.py) | 5m | -0.19 | 5.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 182 | [STRATEGY_RSI_BB_B...](freqtrade-strategies/strategies/STRATEGY_RSI_BB_BOUNDS_CROSS/STRATEGY_RSI_BB_BOUNDS_CROSS.py) | 5m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS，指标库 TA-Lib(ta), fr... |
| 183 | [XtraThicc.py](freqtrade-strategies/strategies/XtraThicc/XtraThicc.py) | 5m | -0.1 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 ROC，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 184 | [RSIv2.py](freqtrade-strategies/strategies/RSIv2/RSIv2.py) | 15m | -0.99 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 185 | [RSIBB02.py](freqtrade-strategies/strategies/RSIBB02/RSIBB02.py) | Unknown | -0.12515406445006344 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 186 | [NFI731_BUSD.py](freqtrade-strategies/strategies/NFI731_BUSD/NFI731_BUSD.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ROC，指标库 TA-... |
| 187 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV6HO/NostalgiaForInfinityV6HO.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 188 | [botbaby.py](freqtrade-strategies/strategies/botbaby/botbaby.py) | 30m | -0.007 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、ADX，指标库 TA-Lib(ta), freqtrade.vend... |
| 189 | [Strategy003.py](freqtrade-strategies/strategies/Strategy003/Strategy003.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI、STOCH，指标库 TA-Li... |
| 190 | [TheRealPullbackV2.py](freqtrade-strategies/strategies/TheRealPullbackV2/TheRealPullbackV2.py) | 5m | -0.035 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、MFI、STOCH、CCI，指标库 TA-Li... |
| 191 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndClucV2/CombinedBinHAndClucV2.py) | 1h | -0.05 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ATR、MFI、STOCH，指标库 TA-Lib(ta), ... |
| 192 | [Dracula.py](freqtrade-strategies/strategies/Dracula/Dracula.py) | 5m | -0.2 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta)。 可读性：高；风格：常... |
| 193 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_maximizer/NostalgiaForInfinityNext_maximizer.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、CC... |
| 194 | [Fakebuy.py](freqtrade-strategies/strategies/Fakebuy/Fakebuy.py) | 5m | -0.085 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ROC，指标库 TA-Lib(ta), freqtra... |
| 195 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndCluc2021Bull/CombinedBinHAndCluc2021Bull.py) | 5m | -0.09 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 196 | [EMA_CROSSOVER_STR...](freqtrade-strategies/strategies/EMA_CROSSOVER_STRATEGY/EMA_CROSSOVER_STRATEGY.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade... |
| 197 | [PumpDetector.py](freqtrade-strategies/strategies/PumpDetector/PumpDetector.py) | 5m | -0.99 | 5.0 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 198 | [NFINextMOHO.py](freqtrade-strategies/strategies/NFINextMOHO/NFINextMOHO.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 199 | [stoploss.py](freqtrade-strategies/strategies/stoploss/stoploss.py) | 5m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 200 | [strato.py](freqtrade-strategies/strategies/strato/strato.py) | 1m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 201 | [NFI46OffsetHOA1.py](freqtrade-strategies/strategies/NFI46OffsetHOA1/NFI46OffsetHOA1.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 202 | [NFI7MOHO.py](freqtrade-strategies/strategies/NFI7MOHO/NFI7MOHO.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 203 | [RSI.py](freqtrade-strategies/strategies/RSI/RSI.py) | 15m | -0.99 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 204 | [quantumfirst.py](freqtrade-strategies/strategies/quantumfirst/quantumfirst.py) | Unknown | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、SMA、STOCH，指标库 TA-Lib(ta), fre... |
| 205 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndCluc2021/CombinedBinHAndCluc2021.py) | 5m | -0.09 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 206 | [SupertrendStrateg...](freqtrade-strategies/strategies/SupertrendStrategy/SupertrendStrategy.py) | 1h | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、STOCH，指标库 pandas_ta。 可读性：中；风格：... |
| 207 | [Strategy005.py](freqtrade-strategies/strategies/Strategy005/Strategy005.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、SMA、STOCH，指标库 TA-Lib(ta), fre... |
| 208 | [SampleStrategy.py](freqtrade-strategies/strategies/SampleStrategy/SampleStrategy.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 209 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7_7_2/NostalgiaForInfinityV7_7_2.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、CC... |
| 210 | [Ichimoku_v31.py](freqtrade-strategies/strategies/Ichimoku_v31/Ichimoku_v31.py) | 1h | -0.99 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.ven... |
| 211 | [EMABBRSI.py](freqtrade-strategies/strategies/EMABBRSI/EMABBRSI.py) | Unknown | -0.2 | 5.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 212 | [stratfib.py](freqtrade-strategies/strategies/stratfib/stratfib.py) | 1h | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD，指标库 TA-Lib(ta), freqtrade.ven... |
| 213 | [BuyOnly.py](freqtrade-strategies/strategies/BuyOnly/BuyOnly.py) | 15m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 214 | [Ichi.py](freqtrade-strategies/strategies/Ichi/Ichi.py) | 15m | -0.2 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、ICHIMOKU，指标库 TA-Lib(ta), freqtrade... |
| 215 | [TDSequentialStrat...](freqtrade-strategies/strategies/TDSequentialStrategy/TDSequentialStrategy.py) | 1h | -0.05 | 5.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 216 | [NFI5MOHO2.py](freqtrade-strategies/strategies/NFI5MOHO2/NFI5MOHO2.py) | 5m | -0.99 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 217 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityXw/NostalgiaForInfinityXw.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 218 | [AlligatorStrategy.py](freqtrade-strategies/strategies/AlligatorStrategy/AlligatorStrategy.py) | 1h | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、STOCH，指标库 未明确识别指标库。 可读性：中；风格：工... |
| 219 | [BigZ07Next.py](freqtrade-strategies/strategies/BigZ07Next/BigZ07Next.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI，指标库 TA-Lib... |
| 220 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV7/NostalgiaForInfinityV7.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 221 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_2/NostalgiaForInfinityNext_ChangeToTower_V5_2.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、CC... |
| 222 | [Babico_SMA5xBBmid.py](freqtrade-strategies/strategies/Babico_SMA5xBBmid/Babico_SMA5xBBmid.py) | 1d | -0.99 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 223 | [TrixStrategy.py](freqtrade-strategies/strategies/TrixStrategy/TrixStrategy.py) | 1h | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、STOCH，指标库 未明确识别指标库。 可读性：中；风格：工程化/多... |
| 224 | [CrossEMAStrategy.py](freqtrade-strategies/strategies/CrossEMAStrategy/CrossEMAStrategy.py) | 1h | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、STOCH，指标库 TA-Lib(ta)。 可读性：中；风格... |
| 225 | [NFI47V2.py](freqtrade-strategies/strategies/NFI47V2/NFI47V2.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 226 | [ForexSignal.py](freqtrade-strategies/strategies/ForexSignal/ForexSignal.py) | 5m | -0.03 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade... |
| 227 | [NFINextMultiOffse...](freqtrade-strategies/strategies/NFINextMultiOffsetAndHO/NFINextMultiOffsetAndHO.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 228 | [Slowbro.py](freqtrade-strategies/strategies/Slowbro/Slowbro.py) | 1h | -0.99 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 freqtrade.vendor.qtpylib。 可... |
| 229 | [Strategy004.py](freqtrade-strategies/strategies/Strategy004/Strategy004.py) | 5m | -0.1 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、ADX、STOCH、CCI，指标库 TA-Lib(ta)。 可读性：... |
| 230 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV3/NostalgiaForInfinityV3.py) | 5m | -0.99 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 231 | [InformativeSample.py](freqtrade-strategies/strategies/InformativeSample/InformativeSample.py) | 5m | -0.1 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 232 | [BB_RPB_TSL_SMA_Tr...](freqtrade-strategies/strategies/BB_RPB_TSL_SMA_Tranz_TB_1_1_1/BB_RPB_TSL_SMA_Tranz_TB_1_1_1.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 233 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext/NostalgiaForInfinityNext.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ROC，指标库 TA-... |
| 234 | [ElliotV531.py](freqtrade-strategies/strategies/ElliotV531/ElliotV531.py) | 5m | -0.189 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、MFI、STOCH、ROC…... |
| 235 | [Strategy001_custo...](freqtrade-strategies/strategies/Strategy001_custom_sell/Strategy001_custom_sell.py) | 5m | -0.1 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 236 | [NFINextMOHO2.py](freqtrade-strategies/strategies/NFINextMOHO2/NFINextMOHO2.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 237 | [Minmax.py](freqtrade-strategies/strategies/Minmax/Minmax.py) | 1h | -0.05 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 238 | [STRATEGY_RSI_BB_C...](freqtrade-strategies/strategies/STRATEGY_RSI_BB_CROSS/STRATEGY_RSI_BB_CROSS.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 239 | [NFI5MOHO_WIP.py](freqtrade-strategies/strategies/NFI5MOHO_WIP/NFI5MOHO_WIP.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 240 | [EXPERIMENTAL_STRA...](freqtrade-strategies/strategies/EXPERIMENTAL_STRATEGY/EXPERIMENTAL_STRATEGY.py) | Unknown | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、STOCH，指标库 ... |
| 241 | [UziChan2.py](freqtrade-strategies/strategies/UziChan2/UziChan2.py) | 1m | -0.1 | 5.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), pandas_ta。 可读性：中；风... |
| 242 | [Nostalgia.py](freqtrade-strategies/strategies/Nostalgia/Nostalgia.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 243 | [BigZ07Next2.py](freqtrade-strategies/strategies/BigZ07Next2/BigZ07Next2.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、MFI，指标库 TA-Lib... |
| 244 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityX/NostalgiaForInfinityX.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、ATR、MFI、STOCH…，... |
| 245 | [Strategy002.py](freqtrade-strategies/strategies/Strategy002/Strategy002.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS、STOCH，指标库 TA-Lib(ta), freqt... |
| 246 | [SRsi.py](freqtrade-strategies/strategies/SRsi/SRsi.py) | 1m | -0.15 | 5.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 247 | [RobotradingBody.py](freqtrade-strategies/strategies/RobotradingBody/RobotradingBody.py) | 4h | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 248 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV5MultiOffsetAndHO/NostalgiaForInfinityV5MultiOffsetAndHO.py) | 5m | -0.99 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 249 | [BBands.py](freqtrade-strategies/strategies/BBands/BBands.py) | 1m | -0.05 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 250 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_3/NostalgiaForInfinityNext_ChangeToTower_V5_3.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、CC... |
| 251 | [MAC.py](freqtrade-strategies/strategies/MAC/MAC.py) | 1d | -0.15 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA，指标库 TA-Lib(ta), panda... |
| 252 | [conny.py](freqtrade-strategies/strategies/conny/conny.py) | 15m | -0.0203 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 253 | [NFI46Offset.py](freqtrade-strategies/strategies/NFI46Offset/NFI46Offset.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 254 | [NFI46.py](freqtrade-strategies/strategies/NFI46/NFI46.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 255 | [bbrsi1_strategy.py](freqtrade-strategies/strategies/bbrsi1_strategy/bbrsi1_strategy.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 256 | [Strategy001.py](freqtrade-strategies/strategies/Strategy001/Strategy001.py) | 5m | -0.1 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 257 | [Cluc4.py](freqtrade-strategies/strategies/Cluc4/Cluc4.py) | 1m | -0.01 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ROC，指标库 TA-Lib(ta), freqtra... |
| 258 | [CombinedBinHAndCl...](freqtrade-strategies/strategies/CombinedBinHAndCluc/CombinedBinHAndCluc.py) | 5m | -0.05 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 259 | [Ichimoku_v37.py](freqtrade-strategies/strategies/Ichimoku_v37/Ichimoku_v37.py) | 4h | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 ICHIMOKU，指标库 TA-Lib(ta), freqtrade.ven... |
| 260 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV5/NostalgiaForInfinityV5.py) | 5m | -0.99 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 261 | [TheForce.py](freqtrade-strategies/strategies/TheForce/TheForce.py) | 15m | -0.015 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA，指标库 TA-Lib(ta), freqtrade... |
| 262 | [TEMA.py](freqtrade-strategies/strategies/TEMA/TEMA.py) | 1m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 263 | [BBRSINaiveStrateg...](freqtrade-strategies/strategies/BBRSINaiveStrategy/BBRSINaiveStrategy.py) | 15m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 264 | [Martin.py](freqtrade-strategies/strategies/Martin/Martin.py) | 5m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 265 | [SAR.py](freqtrade-strategies/strategies/SAR/SAR.py) | 5m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 266 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV6/NostalgiaForInfinityV6.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 267 | [CBPete9.py](freqtrade-strategies/strategies/CBPete9/CBPete9.py) | 5m | -0.99 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR，指标库 TA-Lib(ta),... |
| 268 | [BBRSIS.py](freqtrade-strategies/strategies/BBRSIS/BBRSIS.py) | Unknown | -0.99 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 269 | [Seb.py](freqtrade-strategies/strategies/Seb/Seb.py) | 5m | -0.1 | 5.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、STOCH、CCI，... |
| 270 | [bbema.py](freqtrade-strategies/strategies/bbema/bbema.py) | Unknown | -0.1 | 5.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 271 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityX2/NostalgiaForInfinityX2.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS，指标库 TA-Lib(ta), fre... |
| 272 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV5MultiOffsetAndHO2/NostalgiaForInfinityV5MultiOffsetAndHO2.py) | 5m | -0.99 | 5.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 273 | [mabStra.py](freqtrade-strategies/strategies/mabStra/mabStra.py) | 4h | -0.128 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险点：未发... |
| 274 | [ReinforcedAverage...](freqtrade-strategies/strategies/ReinforcedAverageStrategy/ReinforcedAverageStrategy.py) | 4h | -0.2 | 5.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 275 | [LuxOSC.py](freqtrade-strategies/strategies/LuxOSC/LuxOSC.py) | 5m | -0.99 | 5.0 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、ATR，指标库 TA-Lib(ta), freqtrade.vend... |
| 276 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNext_ChangeToTower_V6/NostalgiaForInfinityNext_ChangeToTower_V6.py) | 5m | -0.99 | 5.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、CC... |
| 277 | [UltimateMomentumI...](freqtrade-strategies/strategies/UltimateMomentumIndicator/UltimateMomentumIndicator.py) | 5m | -0.99 | 5.0 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、MFI，指标库 TA-Lib(ta), freqtr... |
| 278 | [BBandsRSI.py](freqtrade-strategies/strategies/BBandsRSI/BBandsRSI.py) | 5m | -0.15 | 5.0 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), pandas_ta, ... |
| 279 | [sample_strategy.py](user_data/strategies/sample_strategy.py) | 5m | -0.1 | 5.0 | 低 | 工程化/多周期 | 概览：接口V3，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 280 | [AlexNexusForgeV5.py](user_data/strategies/AlexNexusForgeV5.py) | 1h | -0.03 | 5.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ADX，指标库 TA-Lib(ta)。 可读性：中；风格：常... |
| 281 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategy/NotAnotherSMAOffsetStrategy.py) | 5m | -0.35 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 282 | [EMA50.py](freqtrade-strategies/strategies/EMA50/EMA50.py) | 5m | -0.333 | 4.5 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 283 | [mark_strat.py](freqtrade-strategies/strategies/mark_strat/mark_strat.py) | Unknown | -0.23936 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ROC，指标库 TA-Lib... |
| 284 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyHO/NotAnotherSMAOffsetStrategyHO.py) | 5m | -0.35 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 285 | [Kamaflage.py](freqtrade-strategies/strategies/Kamaflage/Kamaflage.py) | 5m | -1.0 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.... |
| 286 | [FastSupertrendOpt.py](freqtrade-strategies/strategies/FastSupertrendOpt/FastSupertrendOpt.py) | 1h | -0.265 | 4.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 SMA、ATR，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险... |
| 287 | [ElliotV8_original.py](freqtrade-strategies/strategies/ElliotV8_original/ElliotV8_original.py) | 5m | -0.32 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 288 | [custom.py](freqtrade-strategies/strategies/custom/custom.py) | 5m | -0.11 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ROC，指标库 TA-Lib(ta), freqtr... |
| 289 | [Chandem.py](freqtrade-strategies/strategies/Chandem/Chandem.py) | 5m | -0.28031 | 4.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 290 | [ClucFiatSlow.py](freqtrade-strategies/strategies/ClucFiatSlow/ClucFiatSlow.py) | 5m | -0.34299 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 291 | [hlhb.py](freqtrade-strategies/strategies/hlhb/hlhb.py) | 4h | -0.3211 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、ADX，指标库 TA-Lib(ta), freqtrade.... |
| 292 | [DCBBBounce.py](freqtrade-strategies/strategies/DCBBBounce/DCBBBounce.py) | 5m | -0.333 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH，... |
| 293 | [Chandemtwo.py](freqtrade-strategies/strategies/Chandemtwo/Chandemtwo.py) | 5m | -0.33572 | 4.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 BBANDS，指标库 TA-Lib(ta), freqtrade.vendo... |
| 294 | [NotAnotherSMAOffs...](freqtrade-strategies/strategies/NotAnotherSMAOffsetStrategyHOv3/NotAnotherSMAOffsetStrategyHOv3.py) | 5m | -0.3 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 295 | [Saturn5.py](freqtrade-strategies/strategies/Saturn5/Saturn5.py) | 15m | -0.2 | 4.5 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD、EMA、SMA、ATR，指标库 TA-Lib(ta), freqt... |
| 296 | [SuperTrendPure.py](freqtrade-strategies/strategies/SuperTrendPure/SuperTrendPure.py) | 1h | -0.265 | 4.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 SMA、ATR，指标库 TA-Lib(ta), freqtrade.vend... |
| 297 | [Cluc5werk.py](freqtrade-strategies/strategies/Cluc5werk/Cluc5werk.py) | 1m | -0.22405 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、BBANDS、ROC，指标库 TA-Lib(ta), freqtra... |
| 298 | [mark_strat_opt.py](freqtrade-strategies/strategies/mark_strat_opt/mark_strat_opt.py) | Unknown | -0.20206 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、ADX、MFI，指标库 TA-Lib(ta)... |
| 299 | [fahmibah.py](freqtrade-strategies/strategies/fahmibah/fahmibah.py) | 5m | -0.1 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、ROC，指标库 TA-Lib(ta), pan... |
| 300 | [EMABreakout.py](freqtrade-strategies/strategies/EMABreakout/EMABreakout.py) | 5m | -0.333 | 4.5 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 301 | [GodStraNew_SMAonl...](freqtrade-strategies/strategies/GodStraNew_SMAonly/GodStraNew_SMAonly.py) | 5m | -1.0 | 4.5 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、ATR、MFI…，指... |
| 302 | [SuperTrend.py](freqtrade-strategies/strategies/SuperTrend/SuperTrend.py) | 1h | -0.265 | 4.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 SMA、ATR，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险... |
| 303 | [SMAOG.py](freqtrade-strategies/strategies/SMAOG/SMAOG.py) | 5m | -0.23 | 4.5 | 高 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta)。 可读性：高；风格：常... |
| 304 | [KAMACCIRSI.py](freqtrade-strategies/strategies/KAMACCIRSI/KAMACCIRSI.py) | 5m | -0.32982 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、CCI，指标库 TA-Lib(ta), freqtrade.vend... |
| 305 | [NotAnotherSMAOffS...](freqtrade-strategies/strategies/NotAnotherSMAOffSetStrategy_V2/NotAnotherSMAOffSetStrategy_V2.py) | 5m | -0.35 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 306 | [Elliotv8.py](freqtrade-strategies/strategies/Elliotv8/Elliotv8.py) | 5m | -0.32 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 307 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNextGen_TSL/NostalgiaForInfinityNextGen_TSL.py) | 15m | -0.1 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI、ICHIMOKU、ROC、CC... |
| 308 | [bb_rsi_opt_new.py](freqtrade-strategies/strategies/bb_rsi_opt_new/bb_rsi_opt_new.py) | Unknown | -0.29207 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 309 | [ElliotV5HOMod3.py](freqtrade-strategies/strategies/ElliotV5HOMod3/ElliotV5HOMod3.py) | 5m | -0.06 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 310 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV1/NostalgiaForInfinityV1.py) | 5m | -0.36 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR，指标库 TA-Lib(ta),... |
| 311 | [FastSupertrend.py](freqtrade-strategies/strategies/FastSupertrend/FastSupertrend.py) | 1h | -0.265 | 4.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 SMA、ATR，指标库 TA-Lib(ta)。 可读性：高；风格：常规。风险... |
| 312 | [SMAIP3v2.py](freqtrade-strategies/strategies/SMAIP3v2/SMAIP3v2.py) | 5m | -0.23 | 4.5 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta)。 可读性：中；风格：常... |
| 313 | [BbRoi.py](freqtrade-strategies/strategies/BbRoi/BbRoi.py) | Unknown | -0.23701 | 4.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 314 | [ClucFiatROI.py](freqtrade-strategies/strategies/ClucFiatROI/ClucFiatROI.py) | 5m | -0.34299 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS，指标库 TA-Lib(ta), freqtra... |
| 315 | [NowoIchimoku1hV1.py](freqtrade-strategies/strategies/NowoIchimoku1hV1/NowoIchimoku1hV1.py) | 1h | -0.08 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA、ICHIMOKU，指标库 TA-Lib(ta), freqt... |
| 316 | [Cluc4werk.py](freqtrade-strategies/strategies/Cluc4werk/Cluc4werk.py) | 1m | -0.31742 | 4.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、BBANDS、ROC，指标库 TA-Lib(ta), fre... |
| 317 | [Diamond.py](freqtrade-strategies/strategies/Diamond/Diamond.py) | 5m | -0.271 | 4.5 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 SMA，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 318 | [bbrsi4Freq.py](freqtrade-strategies/strategies/bbrsi4Freq/bbrsi4Freq.py) | 1h | -0.36727 | 4.5 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 319 | [SMAIP3.py](freqtrade-strategies/strategies/SMAIP3/SMAIP3.py) | 5m | -0.331 | 4.5 | 中 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta)。 可读性：中；风格：常规。风险... |
| 320 | [BBRSIOptim2020Str...](freqtrade-strategies/strategies/BBRSIOptim2020Strategy/BBRSIOptim2020Strategy.py) | 5m | -0.331 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 321 | [ichiV1.py](freqtrade-strategies/strategies/ichiV1/ichiV1.py) | 5m | -0.275 | 4.0 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、ATR、ICHIMOKU，指标库 TA-Lib(ta), freqt... |
| 322 | [DevilStra.py](freqtrade-strategies/strategies/DevilStra/DevilStra.py) | 4h | -0.28 | 4.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD、EMA、SMA、BBANDS、STOCH、ROC、CCI，指标库 ... |
| 323 | [NfiNextModded.py](freqtrade-strategies/strategies/NfiNextModded/NfiNextModded.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、RO... |
| 324 | [FrostAuraM21hStra...](freqtrade-strategies/strategies/FrostAuraM21hStrategy/FrostAuraM21hStrategy.py) | 15m | -0.44897 | 4.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、STOCH，指标库 TA-Lib(ta), freqtra... |
| 325 | [Gumbo1.py](freqtrade-strategies/strategies/Gumbo1/Gumbo1.py) | 5m | -0.25 | 4.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA、BBANDS、STOCH，指标库 TA-Lib(ta), f... |
| 326 | [BBRSIStrategy.py](freqtrade-strategies/strategies/BBRSIStrategy/BBRSIStrategy.py) | 15m | -0.3603667187598833 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 327 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1/SMAOffsetProtectOptV1.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 328 | [ema.py](freqtrade-strategies/strategies/ema/ema.py) | 5m | -1.0 | 4.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 329 | [GodStraNew.py](freqtrade-strategies/strategies/GodStraNew/GodStraNew.py) | 4h | -1.0 | 4.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、ATR、MFI…，指... |
| 330 | [BBRSI.py](freqtrade-strategies/strategies/BBRSI/BBRSI.py) | 4h | -0.3603667187598833 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 331 | [BBRSIOptimizedStr...](freqtrade-strategies/strategies/BBRSIOptimizedStrategy/BBRSIOptimizedStrategy.py) | 5m | -0.295 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 332 | [NowoIchimoku1hV2.py](freqtrade-strategies/strategies/NowoIchimoku1hV2/NowoIchimoku1hV2.py) | 1h | -0.345 | 4.0 | 中 | 风控导向 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA、ICHIMOKU，指标库 TA-Lib(ta), freqt... |
| 333 | [TrixV15Strategy.py](freqtrade-strategies/strategies/TrixV15Strategy/TrixV15Strategy.py) | 1h | -0.31 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、STOCH，指标库 TA-Lib(ta), freq... |
| 334 | [Obelisk_Ichimoku_...](freqtrade-strategies/strategies/Obelisk_Ichimoku_ZEMA_v1/Obelisk_Ichimoku_ZEMA_v1.py) | 5m | -0.294 | 4.0 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 ATR、ICHIMOKU，指标库 TA-Lib(ta), freqtrade... |
| 335 | [Renko.py](freqtrade-strategies/strategies/Renko/Renko.py) | 15m | -100.0 | 4.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 ATR，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 336 | [MultiOffsetLamboV...](freqtrade-strategies/strategies/MultiOffsetLamboV0/MultiOffsetLamboV0.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 EMA、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 337 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1Mod2/SMAOffsetProtectOptV1Mod2.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 338 | [custom_sell.py](freqtrade-strategies/strategies/custom_sell/custom_sell.py) | 5m | -0.347 | 4.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 339 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV4HO/NostalgiaForInfinityV4HO.py) | 5m | -1.0 | 4.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 340 | [MultiMa.py](freqtrade-strategies/strategies/MultiMa/MultiMa.py) | 4h | -0.345 | 4.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 TA-Lib(ta), freqtrade.vendo... |
| 341 | [FrostAuraM31hStra...](freqtrade-strategies/strategies/FrostAuraM31hStrategy/FrostAuraM31hStrategy.py) | 1h | -0.44439 | 4.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、STOCH，指标库 TA-Lib(ta), ... |
| 342 | [NowoIchimoku5mV2.py](freqtrade-strategies/strategies/NowoIchimoku5mV2/NowoIchimoku5mV2.py) | 5m | -0.293 | 4.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、SMA、ICHIMOKU，指标库 TA-Lib(ta), freqt... |
| 343 | [redditMA.py](freqtrade-strategies/strategies/redditMA/redditMA.py) | Unknown | -0.5 | 4.0 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 EMA、SMA、VWAP，指标库 freqtrade.vendor.qtpy... |
| 344 | [Schism.py](freqtrade-strategies/strategies/Schism/Schism.py) | 5m | -0.4 | 4.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ROC，指标库 TA-Lib(ta), freqtrade.vend... |
| 345 | [BBRSIOptimStrateg...](freqtrade-strategies/strategies/BBRSIOptimStrategy/BBRSIOptimStrategy.py) | 5m | -0.344 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 346 | [FrostAuraM115mStr...](freqtrade-strategies/strategies/FrostAuraM115mStrategy/FrostAuraM115mStrategy.py) | 15m | -0.34316 | 4.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 347 | [MontrealStrategy.py](freqtrade-strategies/strategies/MontrealStrategy/MontrealStrategy.py) | 15m | -0.28646 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 348 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV2/NostalgiaForInfinityV2.py) | 5m | -1.0 | 4.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR，指标库 TA-Lib(ta),... |
| 349 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1Mod/SMAOffsetProtectOptV1Mod.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 350 | [BB_Strategy04.py](freqtrade-strategies/strategies/BB_Strategy04/BB_Strategy04.py) | Unknown | -0.32530922906811843 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 351 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNextGen/NostalgiaForInfinityNextGen.py) | 15m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI、ICHIMOKU、ROC、CC... |
| 352 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityV4/NostalgiaForInfinityV4.py) | 5m | -1.0 | 4.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、MFI，指标库 TA-Lib(ta),... |
| 353 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV0/SMAOffsetProtectOptV0.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA，指标库 TA-Lib(ta), freqtrade.... |
| 354 | [Schism6.py](freqtrade-strategies/strategies/Schism6/Schism6.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ROC，指标库 TA-Lib(ta), freqtrade.vend... |
| 355 | [BBRSIoriginal.py](freqtrade-strategies/strategies/BBRSIoriginal/BBRSIoriginal.py) | Unknown | -0.36828 | 4.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 356 | [Maro4hMacdSd.py](freqtrade-strategies/strategies/Maro4hMacdSd/Maro4hMacdSd.py) | 5m | -0.21611 | 4.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 MACD，指标库 TA-Lib(ta), freqtrade.vendor.... |
| 357 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1HO1/SMAOffsetProtectOptV1HO1.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 358 | [NostalgiaForInfin...](freqtrade-strategies/strategies/NostalgiaForInfinityNextV7155/NostalgiaForInfinityNextV7155.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、MFI、ICHIMOKU、RO... |
| 359 | [FrostAuraRandomSt...](freqtrade-strategies/strategies/FrostAuraRandomStrategy/FrostAuraRandomStrategy.py) | 1h | -0.231 | 4.0 | 高 | 常规 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点... |
| 360 | [FrostAuraM315mStr...](freqtrade-strategies/strategies/FrostAuraM315mStrategy/FrostAuraM315mStrategy.py) | 15m | -0.41114 | 4.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS、STOCH，指标库 TA-Lib(ta), ... |
| 361 | [FrostAuraM11hStra...](freqtrade-strategies/strategies/FrostAuraM11hStrategy/FrostAuraM11hStrategy.py) | 1h | -0.40618 | 4.0 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、BBANDS，指标库 TA-Lib(ta), freqtr... |
| 362 | [SMAOPv1_TTF.py](freqtrade-strategies/strategies/SMAOPv1_TTF/SMAOPv1_TTF.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 363 | [MomStrategy.py](freqtrade-strategies/strategies/MomStrategy/MomStrategy.py) | 1h | -1.0 | 4.0 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 364 | [SMAOffsetProtectO...](freqtrade-strategies/strategies/SMAOffsetProtectOptV1_kkeue_20210619/SMAOffsetProtectOptV1_kkeue_20210619.py) | 5m | -0.5 | 4.0 | 中 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、EMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 365 | [GodStraNew40.py](freqtrade-strategies/strategies/GodStraNew40/GodStraNew40.py) | 4h | -1.0 | 4.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、ATR、MFI…，指... |
| 366 | [YOLO.py](freqtrade-strategies/strategies/YOLO/YOLO.py) | 1m | -0.01 | 3.5 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 ADX，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 367 | [ichiV1_Marius.py](freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py) | 5m | -0.275 | 3.5 | 低 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ATR、MFI、ICHIMOKU，指标库 TA-Lib(ta... |
| 368 | [FiveMinCrossAbove.py](freqtrade-strategies/strategies/FiveMinCrossAbove/FiveMinCrossAbove.py) | 5m | -0.99 | 3.5 | 高 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、BBANDS，指标库 TA-Lib(ta), freqtrade.v... |
| 369 | [Schism5.py](freqtrade-strategies/strategies/Schism5/Schism5.py) | 5m | -0.3 | 3.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta), freqtrade.vendor.q... |
| 370 | [PrawnstarOBV.py](freqtrade-strategies/strategies/PrawnstarOBV/PrawnstarOBV.py) | 1h | -0.15 | 3.5 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、SMA，指标库 TA-Lib(ta), freqtrade.vend... |
| 371 | [Dyna_opti.py](freqtrade-strategies/strategies/Dyna_opti/Dyna_opti.py) | 5m | -0.28819 | 3.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ATR、ROC，指标库 TA-Lib(... |
| 372 | [INSIDEUP.py](freqtrade-strategies/strategies/INSIDEUP/INSIDEUP.py) | 1d | -0.99 | 3.5 | 高 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、ADX、ICHIMOKU，指标库 TA-Lib(ta), panda... |
| 373 | [Schism2MM.py](freqtrade-strategies/strategies/Schism2MM/Schism2MM.py) | 5m | -0.99 | 3.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ROC，指标库 TA-Lib(ta), freqtrade.vend... |
| 374 | [TenderEnter.py](freqtrade-strategies/strategies/TenderEnter/TenderEnter.py) | 15m | -0.4 | 2.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、SMA、BBANDS、ADX、MFI、STOCH…... |
| 375 | [Stinkfist.py](freqtrade-strategies/strategies/Stinkfist/Stinkfist.py) | 5m | -0.4 | 2.5 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、ROC，指标库 TA-Lib(ta), freqtrade.... |
| 376 | [RaposaDivergenceV...](freqtrade-strategies/strategies/RaposaDivergenceV1/RaposaDivergenceV1.py) | 5m | -0.3 | 2.5 | 中 | 模板化/堆叠型 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI，指标库 TA-Lib(ta)。 可读性：中；风格：模板化/堆叠型。风... |
| 377 | [ElliotV4.py](freqtrade-strategies/strategies/ElliotV4/ElliotV4.py) | 5m | -0.97 | 2.5 | 低 | 工程化/多周期 | 概览：接口V2，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、MFI、STOCH、ROC…... |
| 378 | [Schism2.py](freqtrade-strategies/strategies/Schism2/Schism2.py) | 5m | -0.3 | 2.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ROC，指标库 TA-Lib(ta), freqtrade.vend... |
| 379 | [SuperHV27.py](freqtrade-strategies/strategies/SuperHV27/SuperHV27.py) | 5m | -0.4 | 2.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、ADX，指标库 TA-Lib(ta), freqtr... |
| 380 | [StrategyScalpingF...](freqtrade-strategies/strategies/StrategyScalpingFast2/StrategyScalpingFast2.py) | 1m | -0.326 | 2.0 | 中 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、EMA、SMA、BBANDS、ADX、MFI、CCI，指标库 TA-... |
| 381 | [Schism3.py](freqtrade-strategies/strategies/Schism3/Schism3.py) | 5m | -0.3 | 2.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ROC，指标库 TA-Lib(ta), freqtrade.vend... |
| 382 | [Schism4.py](freqtrade-strategies/strategies/Schism4/Schism4.py) | 5m | -0.3 | 2.0 | 中 | 工程化/多周期 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、ROC，指标库 TA-Lib(ta), freqtrade.vend... |
| 383 | [BuyAllSellAllStra...](freqtrade-strategies/strategies/BuyAllSellAllStrategy/BuyAllSellAllStrategy.py) | 5m | -0.25 | 2.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 未识别/较少，指标库 未明确识别指标库。 可读性：高；风格：常规。风险点：止... |
| 384 | [StrategyScalpingF...](freqtrade-strategies/strategies/StrategyScalpingFast/StrategyScalpingFast.py) | 1m | -0.5 | 2.0 | 高 | 常规 | 概览：接口未知，方法风格 entry/exit，主要指标 RSI、MACD、EMA、BBANDS、ADX、MFI、CCI，指标库 TA... |
