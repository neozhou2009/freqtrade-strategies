# Apollo11 策略深度解读

> **策略编号**: #420 (465 个策略中的第 420 个)  
> **策略类型**: 多信号趋势跟踪 + 自定义止损 + 多层保护  
> **时间框架**: 15 分钟 (15m)  
> **作者**: Shane Jones (https://twitter.com/shanejones)  
> **原始仓库**: https://github.com/shanejones/goddard

---

## 一、策略概览

Apollo11 是一个复杂的多信号趋势跟踪策略，由 Shane Jones 开发，社区贡献者协助完善。该策略融合了 EMA 趋势、布林带突破、斐波那契回撤等多种技术分析方法，并配备了动态止损系统和 5 层保护机制，是一个适合中级量化交易者的"防御型进攻策略"。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 3 个独立买入信号，可独立启用/禁用 |
| **卖出条件** | 无主动卖出信号，依赖 ROI 和自定义止损 |
| **保护机制** | 5 组保护参数（冷却期、最大回撤、止损保护、低收益保护×2） |
| **时间框架** | 15 分钟 (15m) |
| **启动蜡烛数** | 480 根（约 5 天数据） |
| **依赖库** | talib, qtpylib, freqtrade.persistence.Trade |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.10,   # 0 分钟后，10% 利润退出
    "30": 0.05,  # 30 分钟后，5% 利润退出
    "60": 0.02,  # 60 分钟后，2% 利润退出
}

# 止损设置
stoploss = -0.16  # 16% 固定止损
```

**设计思路**：
- ROI 表采用递进式止盈，时间越长，止盈阈值越低
- 初始目标 10% 较高，适合捕捉较大波动
- 60 分钟后降至 2%，确保至少锁定部分利润
- 16% 固定止损较宽，给予交易足够的波动空间

### 2.2 追踪止损配置

```python
trailing_stop = False  # 禁用标准追踪止损
use_custom_stoploss = True  # 使用自定义止损
use_sell_signal = False  # 禁用卖出信号
```

**设计思路**：
- 禁用标准追踪止损，改用更灵活的自定义止损逻辑
- 自定义止损可根据持仓时间和利润动态调整
- 不依赖技术指标卖出，专注于入场时机

### 2.3 自定义止损逻辑

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    # 盈利保护档位
    if current_profit > 0.20:  # 利润 > 20%
        return 0.04  # 止损上移至 4% 利润
    if current_profit > 0.10:  # 利润 > 10%
        return 0.03  # 止损上移至 3% 利润
    if current_profit > 0.06:  # 利润 > 6%
        return 0.02  # 止损上移至 2% 利润
    if current_profit > 0.03:  # 利润 > 3%
        return 0.01  # 止损上移至 1% 利润
    
    # 亏损止损缓解（基于持仓时间）
    if current_profit <= -0.10:  # 亏损 > 10%
        if trade.open_date_utc + timedelta(hours=60) < current_time:
            return current_profit / 1.75  # 60小时后收紧止损
    
    if current_profit <= -0.08:  # 亏损 > 8%
        if trade.open_date_utc + timedelta(hours=120) < current_time:
            return current_profit / 1.70  # 120小时后进一步收紧
    
    return -1  # 使用默认止损
```

**止损逻辑详解**：

| 利润区间 | 止损位置 | 保护效果 |
|---------|---------|---------|
| > 20% | 锁定 4% 利润 | 强保护 |
| > 10% | 锁定 3% 利润 | 中强保护 |
| > 6% | 锁定 2% 利润 | 中等保护 |
| > 3% | 锁定 1% 利润 | 轻度保护 |
| -10% (60h后) | 动态收紧 | 限时止损 |
| -8% (120h后) | 动态收紧 | 限时止损 |

---

## 三、买入条件详解

### 3.1 信号控制开关

```python
buy_signal_1 = True  # EMA 趋势交叉信号
buy_signal_2 = True  # 布林带+斐波那契信号
buy_signal_3 = True  # 成交量加权突破信号
```

每个信号可独立启用或禁用，便于策略优化和回测分析。

### 3.2 买入信号 #1：EMA 趋势交叉 + VWMACD

**指标配置**：
```python
s1_ema_xs = 3    # 超短周期 EMA
s1_ema_sm = 5    # 短周期 EMA
s1_ema_md = 10   # 中周期 EMA
s1_ema_xl = 50   # 长周期 EMA
s1_ema_xxl = 240 # 超长周期 EMA（趋势基准）
```

**触发条件**：
```python
conditions = [
    dataframe["vwmacd"] < dataframe["signal"],           # VWMACD 在信号线下方
    dataframe["low"] < dataframe["s1_ema_xxl"],           # 最低价低于 240 EMA
    dataframe["close"] > dataframe["s1_ema_xxl"],         # 收盘价高于 240 EMA
    qtpylib.crossed_above(dataframe["s1_ema_sm"], dataframe["s1_ema_md"]),  # 5 EMA 上穿 10 EMA
    dataframe["s1_ema_xs"] < dataframe["s1_ema_xl"],      # 3 EMA 低于 50 EMA
    dataframe["volume"] > 0,                             # 有成交量
]
```

**逻辑解读**：
1. **VWMACD 条件**：成交量加权 MACD 在信号线下方，表示动能尚未过热
2. **价格位置**：最低价触及 240 EMA 但收盘价在其上方，典型的"假突破后回归"
3. **EMA 交叉**：5 EMA 上穿 10 EMA，短趋势转强信号
4. **相对位置**：3 EMA 低于 50 EMA，确保不是高位追涨
5. **成交量确认**：必须有成交量为前提

**信号标签**: `buy_signal_1`

### 3.3 买入信号 #2：布林带下轨 + 斐波那契支撑

**指标配置**：
```python
s2_ema_input = 50          # EMA 周期
s2_ema_offset_input = -1   # EMA 偏移量
s2_bb_sma_length = 49      # 布林带 SMA 周期
s2_bb_std_dev_length = 64  # 标准差周期
s2_bb_lower_offset = 3     # 下轨偏移（3倍标准差）
s2_fib_sma_len = 50        # 斐波那契 SMA 周期
s2_fib_atr_len = 14        # ATR 周期
s2_fib_lower_value = 4.236 # 斐波那契扩展系数
```

**触发条件**：
```python
conditions = [
    qtpylib.crossed_above(dataframe["s2_fib_lower_band"], dataframe["s2_bb_lower_band"]),  # 斐波那契下轨上穿布林下轨
    dataframe["close"] < dataframe["s2_ema"],  # 收盘价低于偏移 EMA
    dataframe["volume"] > 0,                     # 有成交量
]
```

**逻辑解读**：
1. **极端超卖检测**：当斐波那契扩展下轨（4.236 倍 ATR）上穿布林带下轨（3 倍标准差），表示价格处于极端超卖
2. **价格位置确认**：收盘价低于偏移 EMA，确保买入时机在低位
3. **成交量确认**：必须有成交量

**信号标签**: `buy_signal_2`

### 3.4 买入信号 #3：成交量加权突破

**指标配置**：
```python
s3_ema_long = 50   # 长周期 EMA
s3_ema_short = 20  # 短周期 EMA
s3_ma_fast = 10    # 快速成交量加权 MA
s3_ma_slow = 20    # 慢速成交量加权 MA
```

**触发条件**：
```python
conditions = [
    dataframe["low"] < dataframe["s3_bb_lowerband"],   # 最低价低于布林下轨
    dataframe["high"] > dataframe["s3_slow_ma"],       # 最高价高于慢速量价 MA
    dataframe["high"] < dataframe["s3_ema_long"],      # 最高价低于长周期 EMA
    dataframe["volume"] > 0,                           # 有成交量
]
```

**逻辑解读**：
1. **布林带穿透**：价格触及布林带下轨，表示超卖
2. **量价突破**：最高价突破慢速成交量加权 MA，表示有资金介入
3. **趋势确认**：最高价仍低于 50 EMA，避免高位追涨
4. **成交量确认**：必须有成交量

**信号标签**: `buy_signal_3`

### 3.5 买入条件分类汇总

| 条件组 | 条件编号 | 核心逻辑 | 信号标签 |
|-------|---------|---------|---------|
| 趋势跟踪 | #1 | EMA 交叉 + VWMACD + 240 EMA 支撑 | buy_signal_1 |
| 极端超卖 | #2 | 布林带 + 斐波那契扩展双重确认 | buy_signal_2 |
| 量价突破 | #3 | 布林带 + 成交量加权 MA 组合 | buy_signal_3 |

---

## 四、卖出逻辑详解

### 4.1 无主动卖出信号

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[(), "sell"] = 0
    return dataframe
```

策略不使用技术指标驱动的卖出信号，完全依赖 ROI 表和自定义止损机制退出。

### 4.2 ROI 分级止盈

```
时间（分钟）    最小利润阈值    信号名称
──────────────────────────────────────
0              10%            ROI_0
30             5%             ROI_30
60             2%             ROI_60
```

**止盈逻辑**：
- 开仓后立即要求 10% 利润
- 30 分钟后降低要求至 5%
- 60 分钟后进一步降低至 2%
- 超过 60 分钟完全依赖止损

### 4.3 自定义止损动态调整

| 阶段 | 利润区间 | 止损位置 | 说明 |
|------|---------|---------|------|
| 盈利保护 1 | > 20% | 锁定 4% 利润 | 高收益保护 |
| 盈利保护 2 | > 10% | 锁定 3% 利润 | 中高收益保护 |
| 盈利保护 3 | > 6% | 锁定 2% 利润 | 中等收益保护 |
| 盈利保护 4 | > 3% | 锁定 1% 利润 | 轻度保护 |
| 时间止损 1 | < -10%，持仓 > 60h | 动态收紧 | 长期亏损处理 |
| 时间止损 2 | < -8%，持仓 > 120h | 动态收紧 | 极长期亏损处理 |

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| EMA 系列 | 3, 5, 10, 20, 50, 200, 240 EMA | 趋势判断、支撑阻力 |
| 布林带 | 20 周期，3 倍标准差 | 超卖检测、波动区间 |
| ATR | 14 周期 | 波动率测量 |
| 成交量加权 MA | 10, 20 周期 VWMA | 量价关系分析 |
| VWMACD | 12, 26, 9 参数 | 成交量加权 MACD |
| 斐波那契扩展 | 4.236 倍 ATR | 极端支撑位 |

### 5.2 指标计算详解

**EMA 计算**：
```python
dataframe["s1_ema_xs"] = ta.EMA(dataframe, timeperiod=3)   # 超短
dataframe["s1_ema_sm"] = ta.EMA(dataframe, timeperiod=5)   # 短
dataframe["s1_ema_md"] = ta.EMA(dataframe, timeperiod=10)  # 中
dataframe["s1_ema_xl"] = ta.EMA(dataframe, timeperiod=50)  # 长
dataframe["s1_ema_xxl"] = ta.EMA(dataframe, timeperiod=240) # 超长
```

**布林带计算**：
```python
s3_bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
dataframe["s3_bb_lowerband"] = s3_bollinger["lower"]
```

**成交量加权 MACD**：
```python
dataframe["fastMA"] = ta.EMA(dataframe["volume"] * dataframe["close"], 12) / ta.EMA(dataframe["volume"], 12)
dataframe["slowMA"] = ta.EMA(dataframe["volume"] * dataframe["close"], 26) / ta.EMA(dataframe["volume"], 26)
dataframe["vwmacd"] = dataframe["fastMA"] - dataframe["slowMA"]
dataframe["signal"] = ta.EMA(dataframe["vwmacd"], 9)
```

**斐波那契扩展下轨**：
```python
s2_fib_atr_value = ta.ATR(dataframe, timeframe=14)
s2_fib_sma_value = ta.SMA(dataframe, timeperiod=50)
dataframe["s2_fib_lower_band"] = s2_fib_sma_value - s2_fib_atr_value * 4.236
```

---

## 六、风险管理特色

### 6.1 多层保护机制

```python
@property
def protections(self):
    return [
        # 保护 1：冷却期
        {
            "method": "CooldownPeriod",
            "stop_duration": to_minutes(minutes=0),  # 0 分钟冷却
        },
        # 保护 2：最大回撤保护
        {
            "method": "MaxDrawdown",
            "lookback_period": to_minutes(hours=12),  # 12 小时回看
            "trade_limit": 20,                        # 最少 20 笔交易
            "stop_duration": to_minutes(hours=1),     # 停 1 小时
            "max_allowed_drawdown": 0.2,              # 最大 20% 回撤
        },
        # 保护 3：连续止损保护
        {
            "method": "StoplossGuard",
            "lookback_period": to_minutes(hours=6),   # 6 小时回看
            "trade_limit": 4,                         # 最少 4 笔交易
            "stop_duration": to_minutes(minutes=30),  # 停 30 分钟
            "only_per_pair": False,                   # 全交易对
        },
        # 保护 4：低收益保护（短周期）
        {
            "method": "LowProfitPairs",
            "lookback_period": to_minutes(hours=1, minutes=30),  # 1.5 小时回看
            "trade_limit": 2,                         # 最少 2 笔交易
            "stop_duration": to_minutes(hours=15),    # 停 15 分钟
            "required_profit": 0.02,                 # 2% 最低利润
        },
        # 保护 5：低收益保护（长周期）
        {
            "method": "LowProfitPairs",
            "lookback_period": to_minutes(hours=6),   # 6 小时回看
            "trade_limit": 4,                         # 最少 4 笔交易
            "stop_duration": to_minutes(minutes=30),  # 停 30 分钟
            "required_profit": 0.01,                  # 1% 最低利润
        },
    ]
```

### 6.2 保护机制详解

| 保护类型 | 触发条件 | 停止时间 | 说明 |
|---------|---------|---------|------|
| 冷却期 | 每次卖出后 | 0 分钟 | 即时可再次交易 |
| 最大回撤 | 12h内20笔交易回撤>20% | 1 小时 | 整体风险控制 |
| 止损保护 | 6h内≥4次止损 | 30 分钟 | 防止连续亏损 |
| 低收益保护(短) | 1.5h内≥2笔利润<2% | 15 分钟 | 短期收益过滤 |
| 低收益保护(长) | 6h内≥4笔利润<1% | 30 分钟 | 长期收益过滤 |

### 6.3 自定义止损的智能保护

策略的自定义止损实现了"盈利越多，保护越强"的动态机制：

- **阶梯式保护**：利润每上升一个档位，止损就上移一个档位
- **时间止损**：持仓时间过长且亏损严重时，逐步收紧止损
- **渐进退出**：避免"要么翻倍要么归零"的极端情况

---

## 七、策略优势与局限

### ✅ 优势

1. **多信号融合**：3 个独立买入信号，覆盖趋势跟踪、极端超卖、量价突破等多种场景
2. **动态止损**：5 档盈利保护 + 时间止损，智能且灵活
3. **多层保护**：5 组保护机制，从多个维度控制风险
4. **成交量加权**：使用 VWMACD 和成交量加权 MA，有效过滤假信号
5. **参数可调**：所有关键参数均可配置，便于优化

### ⚠️ 局限

1. **无主动卖出**：依赖 ROI 和止损，可能错过最佳卖点
2. **启动数据量大**：需要 480 根 K 线（约 5 天）的预热数据
3. **参数较多**：优化难度大，过拟合风险存在
4. **仅限做多**：没有做空逻辑，不适合熊市

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 温和上涨 | 全开 3 信号 | 利用趋势和超卖信号捕捉机会 |
| 震荡市场 | 仅开信号 2 | 专注极端超卖反弹 |
| 高波动 | 信号 1+3 | 结合趋势和量价突破 |
| 下跌趋势 | 谨慎使用 | 可降低 max_open_trades |

---

## 九、适用市场环境详解

Apollo11 是一个**防御型进攻策略**。它通过多层保护机制和动态止损，在追求收益的同时严格控制风险，最适合**温和趋势或震荡偏上**的市场环境。

### 9.1 策略核心逻辑

- **趋势跟踪为主**：信号 1 和信号 3 都依赖 EMA 趋势
- **超卖反弹为辅**：信号 2 捕捉极端超卖机会
- **防御优先**：5 层保护机制确保风险可控
- **盈利保护**：动态止损锁定利润

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 温和上涨 | ⭐⭐⭐⭐⭐ | 趋势跟踪信号发挥最佳，止盈机制有效 |
| 🔄 震荡市场 | ⭐⭐⭐⭐☆ | 超卖信号捕捉反弹，保护机制减少损耗 |
| 📉 下跌趋势 | ⭐⭐☆☆☆ | 止损频繁触发，建议降低仓位 |
| ⚡️ 高波动 | ⭐⭐⭐☆☆ | 可能误判趋势，需要调整参数 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| max_open_trades | 3-5 | 适中的持仓数量 |
| stake_amount | 2-5% | 单笔仓位控制 |
| startup_candle_count | 480+ | 确保足够预热数据 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

该策略涉及多种技术指标和复杂的条件组合：
- 需要理解 EMA 趋势系统
- 需要理解布林带和斐波那契扩展
- 需要理解成交量加权指标
- 需要理解自定义止损逻辑

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 1-10 对 | 2GB | 4GB |
| 10-30 对 | 4GB | 8GB |
| 30+ 对 | 8GB | 16GB |

### 10.3 回测与实盘的差异

由于策略使用成交量加权指标和自定义止损：
- 回测中止损逻辑可能与实盘有差异
- 成交量数据在不同交易所可能有差异
- 建议先在模拟环境测试

### 10.4 手动交易者建议

对于手动交易者，可以从策略中学习：
- **动态止损**：根据利润和时间调整止损位置的思路
- **多信号确认**：不依赖单一指标，多维度验证
- **保护机制**：建立自己的风险管理框架

---

## 十一、总结

**Apollo11** 是一个精心设计的多信号趋势跟踪策略。它的核心价值在于：

1. **信号多样性**：3 个独立信号覆盖不同市场状态
2. **风险控制**：5 层保护机制 + 动态止损形成完整风控体系
3. **可配置性**：所有参数开放，便于优化调整
4. **社区验证**：源自 GitHub 开源项目，经过社区检验

对于量化交易者而言，这是一个值得深入研究和优化的策略框架。建议先理解各信号逻辑，再进行参数调整，最后小仓位实盘验证。