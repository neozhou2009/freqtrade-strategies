# Obelisk_Ichimoku_Slow_v1_3 策略深度解读

## 目录

1. [策略概述与设计理念](#1-策略概述与设计理念)
2. [核心技术指标解析](#2-核心技术指标解析)
3. [Ichimoku云图系统详解](#3-ichimoku云图系统详解)
4. [SSL通道确认机制](#4-ssl通道确认机制)
5. [EMA趋势过滤系统](#5-ema趋势过滤系统)
6. [Elder Force Index动量指标](#6-elder-force-index动量指标)
7. [入场信号逻辑](#7-入场信号逻辑)
8. [出场信号逻辑](#8-出场信号逻辑)
9. [风险管理体系](#9-风险管理体系)
10. [回测配置建议](#10-回测配置建议)
11. [实战应用指南](#11-实战应用指南)

---

## 1. 策略概述与设计理念

### 1.1 策略定位

Obelisk_Ichimoku_Slow_v1_3 是一款专注于**中长期趋势跟踪**的量化交易策略。策略名称中的"Slow"已经明确表明了其设计倾向——这不是一个追求高频交易、快进快出的短线策略，而是一个旨在**捕捉并持有一段完整上升趋势**的系统性方法。

策略作者 Obelisk 在代码注释中开宗明义地指出："本策略的目的是尽可能长时间地买入并持有一个上升趋势"。这一设计理念贯穿了整个策略的构建逻辑，从指标参数的选择到入场出场规则的设定，无不体现出对趋势的尊重和对噪音的过滤。

### 1.2 版本演进

v1.3 版本在 v1.2 的基础上进行了重要优化：

- **新增 EMA 入场守卫**：通过引入 EMA50 和 EMA200 的过滤机制，进一步确认趋势的有效性，避免在假突破或弱势趋势中入场。
- **移除云顶出场信号**：v1.2 版本中当价格跌破云顶时会触发出场信号，但在 v1.3 中这一过于敏感的出场条件被移除，允许策略在趋势调整时继续持有仓位，从而获得更大的收益空间。

这些改动的目标是"在不显著增加回撤的前提下提高收益"，体现了策略设计者对风险收益平衡的深入思考。

### 1.3 核心设计哲学

策略的设计哲学可以概括为以下几个要点：

**趋势为王**：策略完全服务于趋势跟踪的理念。无论是入场还是出场，都以趋势状态为核心判断依据。任何可能干扰趋势判断的噪音信号都被刻意过滤。

**多维度确认**：策略采用了四套独立的技术指标系统（Ichimoku、EMA、SSL、EFI），每个系统从不同维度确认趋势的存在。这种多维度交叉验证的设计大幅降低了假信号的概率。

**耐心持有**：策略不设置激进的止盈目标和紧密的追踪止损。作者明确警告："如果你想要添加 ROI 或追踪止损，你需要同时做其他修改。"这表明策略的各个组件是相互配合的，单独修改可能破坏策略的整体有效性。

### 1.4 适用场景与限制

**适用场景**：
- 明显的上升趋势市场
- 波动率适中、趋势持续时间较长的交易对
- 中长期投资视角的交易者

**不适用场景**：
- 震荡横盘市场
- 快速反转的市场环境
- 追求高频交易收益的短线交易者

策略作者特别警告："本策略会在趋势进行中买入，所以启动策略的时机很重要。如果市场正在见顶，你可能会买入那些即将结束的趋势。"这提醒使用者需要对市场整体状态有基本的判断。

---

## 2. 核心技术指标解析

### 2.1 指标体系架构

策略构建了一个四层指标验证体系，每一层负责验证趋势的不同方面：

| 指标系统 | 验证维度 | 权重设置 |
|---------|---------|---------|
| Ichimoku 云图 | 趋势方向与强度 | 4（最高） |
| SSL 通道 | 价格动量与位置 | 3 |
| EMA 双均线 | 中期趋势确认 | 2 |
| Elder Force Index | 资金流入强度 | 1 |

这种分层加权的设计体现了策略对各个信号重要性的判断，同时也为信号解读提供了清晰的框架。

### 2.2 时间框架选择

策略采用 **1小时时间框架** 作为主时间框架，这一选择具有深刻的技术含义：

- **足够的价格样本**：1小时K线能够有效过滤分钟级别的市场噪音
- **合理的响应速度**：对于中期趋势的转折能够做出及时反应
- **云图指标的需求**：Ichimoku 云图需要较长的历史数据才能稳定，1小时框架下180根K线相当于7.5天的数据

策略设置的 `startup_candle_count = 180` 也就是基于此考虑。作者特别警告："Ichimoku 是一个长周期指标，如果你减少或使用更短的启动K线数量，回测或实盘运行的结果将在前一周内不稳定或无效。"

### 2.3 指标计算优化

策略在指标计算上采取了多项优化措施：

**延迟线（Chikou Span）的特殊处理**：
```python
dataframe['chikou_high'] = (
    (dataframe['chikou_span'] > dataframe['senkou_a']) &
    (dataframe['chikou_span'] > dataframe['senkou_b'])
).shift(displacement).fillna(0).astype('int')
```

这段代码解决了延迟线在使用上的技术难题。延迟线默认是将当前收盘价向过去移动26个周期，这意味着最新数据的延迟线值实际上是当前价格，直接使用会造成"未来数据泄露"。策略通过将比较结果向前位移，恢复延迟线的正确位置关系。

---

## 3. Ichimoku云图系统详解

### 3.1 云图参数定制

策略采用了经过调整的 Ichimoku 参数，而非传统的 (9, 26, 52, 26) 配置：

| 参数 | 传统值 | 策略值 | 说明 |
|------|-------|-------|------|
| 转换线周期 | 9 | 20 | Tenkan-sen 计算周期 |
| 基准线周期 | 26 | 60 | Kijun-sen 计算周期 |
| 延迟线位移 | 26 | 120 | Chikou Span 位移 |
| 云图位移 | 26 | 30 | 云图向前位移 |

这些参数的调整使得策略更加适应加密货币市场的特性。更大的周期意味着对趋势的确认更加稳定，但也意味着入场信号的延迟增加。这是策略作者在稳定性和时效性之间做出的权衡。

### 3.2 云图组件功能

**转换线（Tenkan Sen）**：
- 计算：(20周期最高价 + 20周期最低价) / 2
- 功能：反映短期价格动量
- 与基准线的交叉作为趋势信号

**基准线（Kijun Sen）**：
- 计算：(60周期最高价 + 60周期最低价) / 2
- 功能：反映中期价格平衡点
- 作为支撑/阻力参考

**先行带A（Senkou Span A）**：
- 计算：(转换线 + 基准线) / 2，向前位移30周期
- 与先行带B构成云图的边缘

**先行带B（Senkou Span B）**：
- 计算：(120周期最高价 + 120周期最低价) / 2，向前位移30周期
- 构成云图的另一边缘

**延迟线（Chikou Span）**：
- 当前收盘价向后位移120周期
- 用于确认价格与历史云图的关系

### 3.3 云图趋势判断逻辑

策略通过 `ichimoku_ok` 变量综合判断云图状态：

```python
dataframe['ichimoku_ok'] = (
    (dataframe['tenkan_sen'] > dataframe['kijun_sen'])  # 转换线在基准线上方
    & (dataframe['close'] > dataframe['cloud_top'])     # 价格在云图上方
    & (dataframe['future_green'] > 0)                     # 未来云图是绿色（看涨）
    & (dataframe['chikou_high'] > 0)                     # 延迟线在云图上方
).astype('int') * 4
```

这四个条件分别验证：

1. **短期动量**：转换线 > 基准线表示短期价格动量向上
2. **价格位置**：收盘价在云顶之上，确认多头市场
3. **未来预期**：先行云为绿色（A > B），预示未来趋势向上
4. **历史验证**：延迟线在云图上方，确认当前价格相对于历史云图的位置

### 3.4 "未来数据"的正确使用

策略中有一个标记为"DANGER ZONE"的代码段：

```python
# NOTE: Not actually the future, present data that is normally shifted forward for display as the cloud
dataframe['future_green'] = (dataframe['leading_senkou_span_a'] > dataframe['leading_senkou_span_b']).astype('int') * 2
```

这里的注释非常关键：这并非真正的未来数据。先行带A和B是根据当前计算并向未来位移的值，它们代表的是"当前对未来的预测"，使用这些数据不会造成未来函数问题。策略作者通过详细的注释解释了这一点，避免使用者误解。

---

## 4. SSL通道确认机制

### 4.1 SSL通道原理

SSL（SSL Channel）是一个基于ATR（平均真实波幅）的通道指标，策略中使用自定义函数 `ssl_atr` 进行计算：

```python
def ssl_atr(dataframe, length=7):
    df = dataframe.copy()
    df['smaHigh'] = df['high'].rolling(length).mean() + df['atr']
    df['smaLow'] = df['low'].rolling(length).mean() - df['atr']
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, 
                np.where(df['close'] < df['smaLow'], -1, np.NAN))
    df['hlv'] = df['hlv'].ffill()
    df['sslDown'] = np.where(df['hlv'] < 0, df['smaHigh'], df['smaLow'])
    df['sslUp'] = np.where(df['hlv'] < 0, df['smaLow'], df['smaHigh'])
    return df['sslDown'], df['sslUp']
```

**计算逻辑**：
1. 计算最高价和最低价的移动平均
2. 分别加减ATR值形成上下通道
3. 根据价格与通道的关系确定趋势方向
4. `sslUp` 和 `sslDown` 随趋势方向动态切换

### 4.2 SSL在策略中的应用

策略使用10周期的SSL通道参数：

```python
ssl_down, ssl_up = ssl_atr(dataframe, 10)
dataframe['ssl_ok'] = (ssl_up > ssl_down).astype('int') * 3
```

当 `ssl_up > ssl_down` 时，表示价格处于上升趋势通道中。这个条件被赋予了权重3，在信号体系中占据重要位置。

### 4.3 入场时机与SSL的关系

在入场信号中，SSL通道不仅用于趋势确认，还用于确定入场时机：

```python
dataframe['entry_ok'] = (
    (dataframe['efi_ok'] > 0)
    & (dataframe['open'] < dataframe['ssl_up'])
    & (dataframe['close'] < dataframe['ssl_up'])
).astype('int') * 1
```

这里要求开盘价和收盘价都低于SSL上轨，这意味着策略在价格回调时入场，而非追涨。这是一个重要的风控设计——在上升趋势中等待回调买入，可以降低入场成本并减少被假突破套住的风险。

---

## 5. EMA趋势过滤系统

### 5.1 双EMA配置

v1.3 版本新增了 EMA 入场守卫，采用经典的50周期和200周期指数移动平均线：

```python
dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
```

**EMA50** 代表中期趋势方向，**EMA200** 代表长期趋势方向。两者的组合使用可以：
- 确认价格处于中期上升趋势
- 验证长期趋势的支持
- 避免在下降趋势中的反弹中错误入场

### 5.2 EMA过滤条件

策略设置的 EMA 过滤条件：

```python
dataframe['ema_ok'] = (
    (dataframe['close'] > dataframe['ema50'])
    & (dataframe['ema50'] > dataframe['ema200'])
).astype('int') * 2
```

**两个条件同时满足**：
1. 收盘价在 EMA50 之上——确认当前价格相对强势
2. EMA50 在 EMA200 之上——确认中期趋势向上

这种设计遵循了经典的趋势跟踪原则：只在均线多头排列时参与交易。

### 5.3 EMA在信号体系中的权重

EMA 过滤被赋予了权重2，介于 EFI（权重1）和 SSL（权重3）之间。这表明 EMA 的作用是作为"确认者"而非"触发者"——它不会独立产生入场信号，但可以在其他指标给出信号时进行二次确认。

---

## 6. Elder Force Index动量指标

### 6.1 EFI指标原理

Elder Force Index (EFI) 是由 Alexander Elder 开发的动量指标，它将价格变化和成交量结合起来：

```python
dataframe['efi_base'] = ((dataframe['close'] - dataframe['close'].shift()) * dataframe['volume'])
dataframe['efi'] = ta.EMA(dataframe['efi_base'], 13)
```

**计算步骤**：
1. 计算价格变化：当前收盘价 - 前一根K线收盘价
2. 乘以成交量：得到"力量"值
3. 对力量值进行13周期EMA平滑

**指标解读**：
- EFI > 0：多头力量占优，价格上涨伴随成交量放大
- EFI < 0：空头力量占优，价格下跌伴随成交量放大
- EFI 绝对值：反映力量的强度

### 6.2 EFI在策略中的作用

```python
dataframe['efi_ok'] = (dataframe['efi'] > 0).astype('int')
```

策略仅使用 EFI 作为多头力量的确认指标。EFI 为正是入场的必要条件之一，这确保了策略只在有资金流入支撑的价格上涨时才参与。

### 6.3 入场时机的EFI过滤

在 `entry_ok` 信号中，EFI 是三个条件之一：

```python
dataframe['entry_ok'] = (
    (dataframe['efi_ok'] > 0)           # 多头力量存在
    & (dataframe['open'] < dataframe['ssl_up'])   # 开盘价低于SSL上轨
    & (dataframe['close'] < dataframe['ssl_up'])  # 收盘价低于SSL上轨
).astype('int') * 1
```

这种设计确保入场时机满足"有资金支持的回调"这一理想条件。

---

## 7. 入场信号逻辑

### 7.1 信号组合体系

策略的入场信号采用分层验证的设计：

**第一层：趋势状态（trending）**

```python
dataframe['trend_pulse'] = (
    (dataframe['ichimoku_ok'] > 0) 
    & (dataframe['ssl_ok'] > 0)
    & (dataframe['ema_ok'] > 0)
).astype('int') * 2

dataframe.loc[(dataframe['trend_pulse'] > 0), 'trending'] = 3
dataframe.loc[(dataframe['trend_over'] > 0), 'trending'] = 0
dataframe['trending'].fillna(method='ffill', inplace=True)
```

趋势状态通过前向填充（ffill）来维持。一旦三个指标同时确认趋势，`trending` 状态会被设为3并持续，直到趋势结束信号出现。

**第二层：入场时机（entry_ok）**

```python
dataframe['entry_ok'] = (
    (dataframe['efi_ok'] > 0)
    & (dataframe['open'] < dataframe['ssl_up'])
    & (dataframe['close'] < dataframe['ssl_up'])
).astype('int') * 1
```

入场时机在趋势确认的基础上，寻找合适的切入点。

### 7.2 最终入场条件

```python
dataframe.loc[
    (dataframe['trending'] > 0)
    & (dataframe['entry_ok'] > 0)
    & (dataframe['date'].dt.minute == 0)
, 'buy'] = 1
```

入场需要同时满足：
1. `trending > 0`：当前处于趋势状态
2. `entry_ok > 0`：入场时机确认
3. `minute == 0`：只在整点小时产生信号（防止高频回测时的重复信号）

### 7.3 入场逻辑的深层含义

这一设计体现了几层重要的交易思想：

**回调入场**：通过要求价格低于 SSL 上轨，策略避免在价格过度延伸时追涨，而是在回调时寻找入场机会。

**资金确认**：EFI > 0 确保价格上涨有成交量支撑，而非无量空涨。

**趋势延续**：trending 状态的前向填充机制意味着策略不会因为单根K线的指标变化而频繁进出，而是持有直到趋势真正结束。

---

## 8. 出场信号逻辑

### 8.1 趋势结束判断

策略的出场逻辑极其简洁：

```python
dataframe['trend_over'] = (
    (dataframe['ssl_ok'] == 0)
).astype('int') * 1
```

**唯一的出场触发条件是 SSL 通道翻转为空头状态**。

这种设计的考量在于：

1. **避免过度敏感**：Ichimoku 云图的信号相对滞后，如果用它作为出场条件，可能会导致出场过晚。相反，SSL 通道对价格变化更加敏感。

2. **简化判断**：v1.3 移除了云顶出场信号，只用 SSL 作为出场依据，使得出场逻辑更加清晰。

3. **允许回调**：在上升趋势中的短期调整不会触发出场，只有当价格真正跌破 SSL 下轨时才确认趋势可能结束。

### 8.2 出场信号生成

```python
dataframe.loc[
    (dataframe['trending'] == 0)
    & (dataframe['date'].dt.minute == 0)
, 'sell'] = 1
```

出场信号只在 `trending` 状态从正值变为0时产生。由于 `trending` 使用前向填充，一旦被设为0，后续K线也会保持为0，因此需要在出场后重置状态或通过其他机制避免重复出场。

### 8.3 出场逻辑的权衡

简洁的出场逻辑是一把双刃剑：

**优点**：
- 减少了假出场信号
- 允许策略在趋势中的调整期继续持有
- 执行简单，便于理解和维护

**缺点**：
- 在趋势反转初期可能反应不够迅速
- 不适合快速反转的市场环境

策略作者的选择体现了"宁可少赚，不可做错"的保守思路，用牺牲一定的时效性换取更高的可靠性。

---

## 9. 风险管理体系

### 9.1 止损设置

```python
stoploss = -0.10
```

策略设置了10%的固定止损。但作者特别指出：

> "为这个策略设置止损没有太大意义，因为它会在下一个机会买回趋势，除非趋势已经结束，而在那种情况下它无论如何都会卖出。"

这一观点基于趋势跟踪的本质——如果止损触发后趋势仍在继续，策略会重新入场；如果趋势确实结束了，出场信号本身就会触发卖出。

### 9.2 追踪止损

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.04
```

追踪止损参数虽然设置了，但作者注释表明"未实际使用"。这些参数的逻辑是：
- 当收益达到4%后，激活追踪止损
- 追踪止损距离为0.5%
- 锁定至少0.5%的利润

然而，这与策略的长期持有理念存在冲突，因此作者建议不要启用。

### 9.3 ROI设置

```python
minimal_roi = {
    "0": 0.10,
    "60": 0.072,
    "120": 0.049,
    "240": 0.02,
    "360": 0,
}
```

ROI 配置会在持仓一定时间后逐步降低目标收益：
- 即时目标：10%
- 60小时后：7.2%
- 120小时后：4.9%
- 240小时后：2%
- 360小时后：任何正收益

这实际上是一个"收益衰减"机制，鼓励策略在长期持有没有新的收益增长时及时出场。

### 9.4 关于止损的重要警告

策略代码中有一个特别重要的警告：

```
WARNING: Do not use stoploss_on_exchange or the bot may trigger emergencysell 
when it fails to place the stoploss.
```

这个警告提醒用户不要在交易所端设置止损单，因为在某些情况下（如交易所API问题、网络延迟等），止损单可能无法成功放置，导致机器人触发紧急卖出，这可能造成不必要损失。

---

## 10. 回测配置建议

### 10.1 推荐的配对列表配置

策略作者提供了经过验证的配对列表配置：

```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 25,
        "sort_key": "quoteVolume",
        "refresh_period": 1800
    },
    {"method": "AgeFilter", "min_days_listed": 10},
    {"method": "PrecisionFilter"},
    {"method": "PriceFilter", "low_price_ratio": 0.001},
    {
        "method": "RangeStabilityFilter",
        "lookback_days": 3,
        "min_rate_of_change": 0.1,
        "refresh_period": 1440
    }
]
```

**配置解读**：

1. **VolumePairList**：选择交易量最大的25个交易对
2. **AgeFilter**：排除上市不足10天的新币
3. **PrecisionFilter**：过滤精度不合适的交易对
4. **PriceFilter**：排除价格过低的山寨币
5. **RangeStabilityFilter**：排除波动率过低的交易对

### 10.2 时间框架验证

策略可以在1分钟或5分钟框架下回测，以验证在更细粒度下的表现：

```python
# Obelisk_Ichimoku_Slow does not use trailing stop or roi 
# and should be safe to backtest at 1h
# if self.config['runmode'].value in ('backtest', 'hyperopt'):
#     assert (timeframe_to_minutes(self.timeframe) <= 5), 
#     "Backtest this strategy in 5m or 1m timeframe."
```

但正常使用时，1小时是推荐的主时间框架。

### 10.3 启动数据要求

由于 Ichimoku 云图需要较长的历史数据，策略设置了：

```python
startup_candle_count = 180
```

这意味着回测或实盘运行前需要准备至少180根K线的历史数据。在1小时框架下，这相当于7.5天的数据。如果没有足够的历史数据，前一周的策略信号将不可靠。

---

## 11. 实战应用指南

### 11.1 启动时机选择

策略作者反复强调启动时机的重要性：

> "本策略会在趋势进行中买入，所以启动策略的时机很重要。如果市场正在见顶，你可能会买入那些即将结束的趋势。"

**建议的启动时机**：
- 市场经过一段时间调整后重新走强
- 整体加密货币市场处于上升周期
- 避免 FOMO 情绪高涨的时期

### 11.2 资金管理建议

基于策略的特性，建议：

**仓位规模**：
- 单笔交易风险控制在总资金的1-2%
- 考虑到10%的止损，单笔交易金额约为总资金的10-20%

**分散投资**：
- 同时运行多个交易对
- 使用 VolumePairList 自动选择活跃交易对
- 避免过度集中在单一板块

### 11.3 监控要点

**趋势信号**：
- 关注 `trending` 状态的变化
- 当 `trend_pulse` 从正值变为0时，准备出场

**持仓管理**：
- 不要手动干预策略的出场信号
- 避免频繁调整止损参数

**异常情况处理**：
- 如遇交易所 API 问题导致的紧急卖出，需要手动检查持仓
- 市场剧烈波动时可以暂时停止策略

### 11.4 策略优化方向

如果需要优化策略，可以考虑：

**入场优化**：
- 调整 Ichimoku 参数适应特定交易对
- 添加 RSI 或其他动量指标作为过滤

**出场优化**：
- 添加基于波动率的动态止损
- 在极端行情下增加额外的出场条件

**风险管理优化**：
- 根据市场波动率调整仓位
- 添加最大回撤限制

### 11.5 总结

Obelisk_Ichimoku_Slow_v1_3 是一个设计思路清晰、逻辑严谨的趋势跟踪策略。它通过多维度指标确认来过滤假信号，通过回调入场来优化成本，通过简化的出场逻辑来避免过度交易。

策略的核心理念是"趋势为王"，所有设计都服务于捕捉并持有上升趋势。使用者需要理解这一理念，并根据自身的风险偏好和市场判断来选择合适的启动时机。

正如策略作者所言，这是一个"买入并持有"的策略，而非快进快出的短线策略。只有在接受这一理念的前提下，策略才能发挥其应有的效果。

---

*文档版本：1.0*  
*策略版本：Obelisk_Ichimoku_Slow_v1_3*  
*作者：Obelisk*  
*文档整理日期：2026年3月*