# Schism5 策略深度解读

> **策略编号**: #380 (465 个策略中的第 380 个)  
> **策略类型**: 牛熊自适应 + 动态止损策略  
> **时间框架**: 5 分钟 (5m) + 1 小时信息层

---

## 一、策略概览

Schism5 是一个基于牛熊市场状态自适应的量化交易策略。其核心创新在于根据 1 小时 RSI 判断市场处于牛市还是熊市，并动态调整买卖阈值。策略还引入了渐进式自定义止损机制，使止损阈值随持仓时间变化而收紧，实现更灵活的风险控制。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 2 个自适应买入信号（牛市/熊市分别触发） |
| **卖出条件** | 2 个自适应卖出信号 + ROI 分级止盈 |
| **保护机制** | 渐进式自定义止损 + 订单价格保护 |
| **时间框架** | 5m 主时间框架 + 1h 信息时间框架 |
| **依赖库** | talib, arrow, cachetools, technical.indicators (RMI) |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.14025,    # 立即：14.025%
    "34": 0.08031,   # 34分钟后：8.031%
    "86": 0.03995,   # 86分钟后：3.995%
    "203": 0         # 203分钟后：0%（无条件退出）
}

# 止损设置
stoploss = -0.30                    # 30% 硬止损
use_custom_stoploss = True          # 启用自定义止损
custom_stop_ramp_minutes = 110      # 止损渐进时间（110分钟）
custom_stop_trailing = 0.001       # 追踪止损偏移
```

**设计思路**：
- ROI 采用激进的渐进式设计，初始目标高达 14%
- 自定义止损在 110 分钟内从 -30% 渐进收紧到 0%
- 追踪止损偏移 0.1%，提供微小的追踪空间

### 2.2 牛熊自适应参数

```python
buy_params = {
    'bear-buy-rsi': 49,   # 熊市买入阈值：RSI < 49
    'bull-buy-rsi': 39    # 牛市买入阈值：RSI < 39
}

sell_params = {
    'bear-sell-rsi': 86,  # 熊市卖出阈值：RSI > 86
    'bull-sell-rsi': 86   # 牛市卖出阈值：RSI > 86
}
```

**参数解读**：
- 牛市买入更谨慎：RSI 需低于 39（更低的超卖）
- 熊市买入更宽松：RSI 需低于 49（更高的超卖）
- 卖出阈值一致：RSI > 86 无论牛熊都卖出

### 2.3 订单类型配置

```python
use_sell_signal = True           # 启用卖出信号
sell_profit_only = True          # 仅盈利时卖出
ignore_roi_if_buy_signal = True  # 有买入信号时忽略 ROI
```

**配置解读**：与 Schism4 不同，Schism5 的卖出信号是真正的交易信号，而非仅作为动态止损。

---

## 三、买入条件详解

### 3.1 牛熊判断机制

策略通过 1 小时 RSI 判断市场状态：

```python
# 1小时 RSI 数据合并
informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.inf_timeframe)
informative['rsi'] = ta.RSI(informative, timeperiod=14)
dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.inf_timeframe, ffill=True)

# 牛市标记
dataframe['bull'] = dataframe[f"rsi_{self.inf_timeframe}"].gt(60).astype('int') * 20
```

**判断逻辑**：
- 1 小时 RSI > 60 → 牛市标记（bull > 0）
- 1 小时 RSI ≤ 60 → 熊市标记（bull == 0）

### 3.2 自适应买入条件

```python
# 新交易买入逻辑
conditions.append(
    ((dataframe['bull'] > 0) & qtpylib.crossed_below(dataframe['rsi'], params['bull-buy-rsi'])) |
    (~(dataframe['bull'] > 0) & qtpylib.crossed_below(dataframe['rsi'], params['bear-buy-rsi']))
)
```

**条件分解**：

| 市场状态 | 触发条件 | 阈值 |
|---------|---------|------|
| 牛市（1h RSI > 60） | RSI 下穿 39 | 更严格 |
| 熊市（1h RSI ≤ 60） | RSI 下穿 49 | 更宽松 |

**设计意图**：牛市中价格回调更深才入场，熊市中反弹信号更早入场。

### 3.3 持仓信号延续机制

与 Schism4 类似，策略设计了持仓信号延续机制：

```python
if trade_data['active_trade']:
    profit_factor = (1 - (dataframe['rmi-slow'].iloc[-1] / 400))
    rmi_grow = self.linear_growth(30, 70, 0, 240, trade_data['open_minutes'])

    conditions.append(dataframe['rmi-up-trend'] == 1)
    conditions.append(trade_data['current_profit'] > (trade_data['peak_profit'] * profit_factor))
    conditions.append(dataframe['rmi-slow'] >= rmi_grow)
```

**参数解读**：
- RMI 阈值从 30 开始，240 分钟内增长到 70
- 利润因子随 RMI 动态调整
- 持仓期间需要保持 RMI 上升趋势

---

## 四、卖出逻辑详解

### 4.1 多层止盈系统

```
持仓时间       目标利润率    说明
──────────────────────────────────
0 分钟        14.025%      非常激进的目标
34 分钟       8.031%       短期调整
86 分钟       3.995%       中期调整
203 分钟      0%           约3.4小时无条件退出
```

### 4.2 自适应卖出信号

```python
conditions.append(
    ((dataframe['bull'] > 0) & (dataframe['rsi'] > params['bull-sell-rsi'])) |
    (~(dataframe['bull'] > 0) & (dataframe['rsi'] > params['bear-sell-rsi']))
)
```

**卖出逻辑**：
- 牛市：RSI > 86 → 卖出
- 熊市：RSI > 86 → 卖出

**注意**：买卖阈值在卖出时统一，均为 86。

### 4.3 渐进式自定义止损

这是 Schism5 最具特色的机制：

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    since_open = current_time - trade.open_date
    
    # 渐进因子：0 → 1（110分钟内）
    sl_pct = 1 - (max(min(since_open / timedelta(minutes=self.custom_stop_ramp_minutes), 1), 0))**3
    
    # 渐进止损：从 -30% 渐进到接近 0
    sl_ramp = self.stoploss * sl_pct
    
    return min(0, sl_ramp) - self.custom_stop_trailing
```

**止损演变时间线**：

| 持仓时间 | 渐进因子 | 止损位 | 说明 |
|---------|---------|--------|------|
| 0 分钟 | 0 | -30% | 初始止损 |
| 27.5 分钟 | 0.5 | 约 -26% | 渐进收紧 |
| 55 分钟 | 0.75 | 约 -16% | 继续收紧 |
| 82.5 分钟 | 0.875 | 约 -9% | 接近盈利区 |
| 110 分钟 | 1 | 接近 0% | 基本保本 |

**立方渐进曲线**：使用三次方计算，使止损收紧先慢后快。

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| 动量指标 | RSI (14周期) | 主买卖信号 |
| 动量指标 | RMI 慢速 (21周期) | 趋势确认 |
| 动量指标 | RMI 快速 (8周期) | 短期动量 |
| 趋势判断 | Bull 标记 | 牛熊状态识别 |

### 5.2 信息时间框架指标（1h）

- **RSI (14)**：判断牛熊状态
- **Bull 标记**：RSI > 60 则为牛市

### 5.3 指标计算详解

```python
# 相对动量指数
dataframe['rmi-slow'] = RMI(dataframe, length=21, mom=5)
dataframe['rmi-fast'] = RMI(dataframe, length=8, mom=4)

# 常规 RSI
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

# RMI 趋势判断
dataframe['rmi-up'] = np.where(dataframe['rmi-slow'] >= dataframe['rmi-slow'].shift(), 1, 0)
dataframe['rmi-dn'] = np.where(dataframe['rmi-slow'] <= dataframe['rmi-slow'].shift(), 1, 0)
dataframe['rmi-up-trend'] = np.where(dataframe['rmi-up'].rolling(3).sum() >= 2, 1, 0)
dataframe['rmi-dn-trend'] = np.where(dataframe['rmi-dn'].rolling(3).sum() >= 2, 1, 0)

# 牛市标记
dataframe['bull'] = dataframe[f"rsi_{self.inf_timeframe}"].gt(60).astype('int') * 20
```

---

## 六、风险管理特色

### 6.1 渐进式止损

止损阈值随时间变化，形成"时间锁"：

- **初期**：允许 -30% 亏损，给交易"喘息空间"
- **中期**：止损逐步收紧
- **后期**：接近保本止损，锁定已有利润

### 6.2 订单价格保护

与 Schism4 相同的 1% 价格保护机制：

```python
def check_buy_timeout(self, pair, trade, order, **kwargs):
    if current_price > order['price'] * 1.01:
        return True  # 价格涨超1%，取消买入

def check_sell_timeout(self, pair, trade, order, **kwargs):
    if current_price < order['price'] * 0.99:
        return True  # 价格跌超1%，取消卖出

def confirm_trade_entry(self, pair, order_type, amount, rate, **kwargs):
    if current_price > rate * 1.01:
        return False  # 入场确认时同样保护
```

### 6.3 牛熊自适应风控

根据市场状态动态调整策略行为：

| 市场状态 | 买入阈值 | 卖出阈值 | 风格 |
|---------|---------|---------|------|
| 牛市 | RSI < 39 | RSI > 86 | 更谨慎 |
| 熊市 | RSI < 49 | RSI > 86 | 更积极 |

---

## 七、策略优势与局限

### ✅ 优势

1. **牛熊自适应**：根据大周期自动调整买卖阈值
2. **渐进式止损**：从宽松到收紧，平衡风险与收益
3. **简洁逻辑**：相比 Schism4 参数更少，更易理解
4. **持仓延续**：趋势好时忽略 ROI 继续持有
5. **子策略支持**：内置 BTC/ETH 专属参数

### ⚠️ 局限

1. **激进 ROI**：14% 的初始目标可能过于乐观
2. **单一指标**：主要依赖 RSI，缺乏多重确认
3. **依赖实时数据**：同样使用数据库查询，回测不准确
4. **卖出阈值统一**：牛熊卖出条件相同，缺少差异化

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 震荡市场 | 默认配置 | 牛熊切换适应震荡 |
| 强趋势 | 降低 ROI 目标 | 提高持仓时间，获取更大收益 |
| 高波动 | 调整止损参数 | 可考虑缩短止损渐进时间 |
| 低流动性 | 谨慎使用 | 订单保护可能频繁触发 |

---

## 九、适用市场环境详解

Schism5 是**牛熊自适应策略**的代表。它通过 1 小时 RSI 自动识别市场状态并调整策略行为，最适合 **震荡切换的市场**，而在 **单边趋势市场** 时表现可能不如趋势策略。

### 9.1 策略核心逻辑

- **牛熊识别**：1 小时 RSI > 60 为牛市，否则为熊市
- **动态阈值**：牛市更谨慎（RSI < 39 入场），熊市更积极（RSI < 49 入场）
- **时间锁止损**：止损从 -30% 渐进收紧到 0%

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 🔄 震荡切换 | ⭐⭐⭐⭐⭐ | 牛熊自适应机制发挥最大作用 |
| 📈 慢牛 | ⭐⭐⭐⭐☆ | 牛市阈值可能错过一些机会 |
| 📉 慢熊 | ⭐⭐⭐☆☆ | 熊市阈值更积极，但整体环境差 |
| ⚡️ 极端波动 | ⭐⭐☆☆☆ | RSI 信号可能失效 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| `bull-buy-rsi` | 35-42 | 根据市场波动调整 |
| `bear-buy-rsi` | 45-52 | 根据市场波动调整 |
| `custom_stop_ramp_minutes` | 90-130 | 根据风险偏好调整 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

Schism5 代码量约 200 行，比 Schism4 简洁。核心概念：
- 牛熊自适应机制
- 渐进式止损计算
- RSI 下穿信号

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 1-5 对 | 2GB | 4GB |
| 6-15 对 | 4GB | 8GB |
| 16+ 对 | 8GB | 16GB |

### 10.3 回测与实盘的差异

**重要警告**：策略使用 `Trade.get_trades()` 查询持仓信息，回测模式下无法完全模拟。建议：

1. 使用 `--enable-position-stacking` 回测
2. 重点关注实盘表现
3. 小资金验证后再扩大

### 10.4 手动交易者建议

若想手动借鉴此策略，重点关注：
1. 1 小时 RSI 判断牛熊（> 60 牛市，≤ 60 熊市）
2. 牛市等 RSI 下穿 39 入场
3. 熊市等 RSI 下穿 49 入场
4. RSI > 86 卖出
5. 止损从 -30% 逐渐收紧

---

## 十一、总结

**Schism5** 是一个**简洁高效的牛熊自适应策略**。它的核心价值在于：

1. **市场感知**：自动识别牛熊状态，调整策略行为
2. **渐进止损**：从宽松到收紧，平衡风险与收益
3. **简洁设计**：参数少，逻辑清晰，易于理解和调整
4. **持仓延续**：趋势好时忽略 ROI 继续持有

对于量化交易者而言，这是一个**适合入门的牛熊自适应策略模板**。相比 Schism4，它的参数更少，逻辑更清晰，但 ROI 目标较为激进，建议根据实际情况调整。

---

## 附录：子策略参数

### Schism5_BTC（BTC 质押专用）

```python
timeframe = '1h'
inf_timeframe = '4h'

buy_params = {
    'inf-rsi': 64,
    'mp': 55,
    'rmi-fast': 31,
    'rmi-slow': 16,
    'xinf-stake-rmi': 67,
    'xtf-fiat-rsi': 17,
    'xtf-stake-rsi': 57
}

minimal_roi = {
    "0": 0.05,
    "240": 0.025,
    "1440": 0.01,
    "4320": 0
}

use_sell_signal = False
```

### Schism5_ETH（ETH 质押专用）

```python
timeframe = '1h'
inf_timeframe = '4h'

buy_params = {
    'inf-rsi': 13,
    'inf-stake-rmi': 69,
    'mp': 40,
    'rmi-fast': 42,
    'rmi-slow': 17,
    'tf-fiat-rsi': 15,
    'tf-stake-rsi': 92
}

minimal_roi = {
    "0": 0.05,
    "240": 0.025,
    "1440": 0.01,
    "4320": 0
}

use_sell_signal = False
```

**注意**：子策略继承自 Schism5，但使用了不同的参数集。子策略的时间框架为 1 小时 + 4 小时，更适合较长周期的交易。