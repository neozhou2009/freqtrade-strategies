# Schism3 策略深度解读

> **策略编号**: #378 (465 个策略中的第 378 个)  
> **策略类型**: 多条件反弹交易 + 跨时间框架过滤 + 多货币支持  
> **时间框架**: 5 分钟 (5m) + 1 小时 (1h 信息层) / 1 小时 + 4 小时（子策略）

---

## 一、策略概览

Schism3 是一个**高度可配置的反弹交易策略**，在 Schism2MM 的基础上进行了重要升级。核心创新包括：**反弹预信号系统**（bounce-pending）、**多货币对支持**（BTC/ETH 抵押货币）、以及**三个策略变体**（基础版、BTC版、ETH版）。策略通过捕获反弹信号价格，在价格回升时入场，实现了更精准的入场时机。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 反弹预信号 + 价格确认 + 多时间框架过滤 + 多货币条件 |
| **卖出条件** | 动态止损 + RMI 趋势反转 + 组合利润管理 |
| **保护机制** | 5 重保护（止损、订单超时、入场确认、价格保护、反弹价格跟踪） |
| **时间框架** | 5m + 1h（基础）/ 1h + 4h（子策略） |
| **依赖库** | numpy, talib, qtpylib, arrow, cachetools, technical |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.05,     # 立即获利 5%
    "10": 0.025,   # 10分钟后降为 2.5%
    "20": 0.015,   # 20分钟后降为 1.5%
    "30": 0.01,    # 30分钟后降为 1%
    "720": 0.005,  # 12小时后降为 0.5%
    "1440": 0      # 24小时后无利润要求
}

# 止损设置
stoploss = -0.30  # 30% 固定止损（注意：较高）
```

**设计思路**：
- ROI 表跨度长达24小时，适合**中长期持有**
- 止损高达30%，给予更大的**价格波动空间**
- 配合 `ignore_roi_if_buy_signal = True`，买入信号有效时延迟退出

### 2.2 订单类型配置

```python
use_sell_signal = False      # 不使用标准卖出信号
sell_profit_only = True      # 仅盈利时卖出
ignore_roi_if_buy_signal = True  # 买入信号有效时忽略 ROI
```

### 2.3 买入参数

```python
buy_params = {
    'bounce-lookback': 8,        # 反弹信号回看周期
    'bounce-price': 'min',       # 反弹价格取最小值
    'down-inf-rsi': 37,          # 下跌时1h RSI阈值
    'down-mp': 60,               # 下跌时MP阈值
    'down-rmi-fast': 28,        # 下跌时快速RMI
    'down-rmi-slow': 35,        # 下跌时慢速RMI
    'up-inf-rsi': 59,           # 上涨时1h RSI阈值
    'xinf-stake-rmi': 70,       # 抵押货币1h RMI
    'xtf-fiat-rsi': 15,         # 法币时间框架RSI
    'xtf-stake-rsi': 60         # 抵押货币时间框架RSI
}
```

---

## 三、买入条件详解

### 3.1 反弹预信号系统（核心创新）

Schism3 独创了**反弹预信号**机制，分三步工作：

#### 第一步：检测反弹条件

```python
dataframe['bounce-pending'] = np.where(
    (1h_rsi >= 37) &              # 1h RSI 不太低
    (rmi-dn-trend == 1) &         # RMI 下降趋势
    (rmi-slow >= 35) &            # 慢 RMI 不超卖
    (rmi-fast <= 28) &            # 快 RMI 较低
    (mp <= 60),                   # 动量乒乓球不高
    1, 0
)
```

#### 第二步：捕获反弹价格

```python
dataframe['bounce-price'] = np.where(
    bounce-pending == 1,
    close,                        # 信号时刻记录价格
    close.rolling(8).min()        # 否则取8周期最低价
)
```

#### 第三步：确认入场

```python
# 真正买入需要确认
(1h_rsi >= 59) &                  # 大周期趋势确认
(bounce-range == 1) &              # 8周期内有反弹信号
(rmi-up-trend == 1) &             # RMI 转为上升
(close >= bounce-price)           # 价格回升确认
```

**逻辑解读**：
1. 先检测"可能会反弹"的条件
2. 记录信号出现时的价格
3. 等待价格回升确认才入场

### 3.2 多货币对支持

当抵押货币为 BTC 或 ETH 时，策略会额外检查：

```python
if stake_currency in ('BTC', 'ETH'):
    # 时间框架条件
    (stake_rsi < 60) | (fiat_rsi > 15)   # 抵押货币不超买 或 法币超卖
    # 信息框架条件
    stake_rmi_1h < 70                      # 抵押货币1h RMI 不高
```

**目的**：避免在 BTC/ETH 大跌时做多山寨币。

### 3.3 加仓逻辑

```python
if active_trade:
    profit_factor = 1 - (rmi-slow / 400)  # 利润因子
    rmi_grow = linear_growth(30, 70, 180, 720, open_minutes)  # 线性增长
    
    conditions.append(rmi-up-trend == 1)
    conditions.append(current_profit > peak_profit * factor)
    conditions.append(rmi-slow >= rmi_grow)
```

---

## 四、卖出逻辑详解

### 4.1 动态止损系统

```python
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
# 持仓0分钟: 允许亏损3%
# 持仓300分钟后: 要求盈利
```

### 4.2 RMI 止损信号

```python
if peak_profit > 0:
    crossed_below(rmi-slow, 50)    # 曾盈利：RMI跌破50
else:
    crossed_below(rmi-slow, 10)    # 从未盈利：RMI跌破10
```

### 4.3 组合利润管理

```python
if free_slots > 0:
    hold_pct = (1 / free_slots) * -0.04
    avg_other_profit >= hold_pct
else:
    biggest_loser == True          # 只允许最大亏损者卖出
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| 动量指标 | RMI(21,5), RMI(8,4) | 趋势方向、超买超卖 |
| 变化率 | ROC(6), MP | 动量强度测量 |
| 趋势指标 | RMI 趋势计数 | 趋势确认 |
| 反弹系统 | bounce-pending, bounce-price, bounce-range | 入场时机 |

### 5.2 信息时间框架指标（1h）

- **RSI(14)**：确认大周期趋势
- **抵押货币 RMI**（仅 BTC/ETH）：跨货币过滤

### 5.3 多货币框架指标

当抵押货币为 BTC 或 ETH 时：

| 指标 | 数据源 | 用途 |
|------|--------|------|
| `{coin}_rsi` | COIN/USD (5m) | 币种法币价格趋势 |
| `{stake}_rsi` | STAKE/USD (5m) | 抵押货币法币趋势 |
| `{stake}_rmi_1h` | STAKE/USD (1h) | 抵押货币长期趋势 |

---

## 六、风险管理特色

### 6.1 多层止损保护

| 止损类型 | 触发条件 | 说明 |
|---------|---------|------|
| 固定止损 | 亏损 >= 30% | 硬性退出（注意：较宽松） |
| 动态止损 | 利润 < 时间阈值 | 软性退出 |
| RMI 止损 | RMI 跌破阈值 | 趋势反转 |
| 组合止损 | 整体仓位考虑 | 资金管理 |
| 反弹失效 | 价格未回升 | 信号失效 |

### 6.2 订单超时保护

```python
def check_buy_timeout(self, pair, trade, order, **kwargs):
    if current_price > order['price'] * 1.01:  # 价格偏离1%
        return True
    return False

def check_sell_timeout(self, pair, trade, order, **kwargs):
    if current_price < order['price'] * 0.99:  # 价格偏离1%
        return True
    return False
```

### 6.3 入场价格保护

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, **kwargs):
    if current_price > rate * 1.01:  # 价格偏离超过1%
        return False
    return True
```

### 6.4 反弹价格跟踪

策略记录反弹信号出现时的价格，确保在价格回升时才入场，避免抄在半山腰。

---

## 七、策略变体

### 7.1 Schism3_BTC（BTC 抵押货币专用）

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
    "240": 0.025,   # 4小时
    "1440": 0.01,   # 1天
    "4320": 0       # 3天
}
```

**特点**：使用更长时间框架，适合 BTC 波动特性。

### 7.2 Schism3_ETH（ETH 抵押货币专用）

```python
timeframe = '1h'
inf_timeframe = '4h'

buy_params = {
    'inf-rsi': 13,
    'mp': 40,
    'rmi-fast': 42,
    'rmi-slow': 17,
    'xinf-stake-rmi': 69,
    'xtf-fiat-rsi': 15,
    'xtf-stake-rsi': 92
}
```

**特点**：针对 ETH 波动特性的参数优化。

---

## 八、策略优势与局限

### ✅ 优势

1. **反弹预信号系统**：先记录信号价格，确认回升才入场
2. **多货币支持**：自动适配 BTC/ETH 抵押货币
3. **参数可配置**：支持按币种组覆盖参数
4. **三个变体**：基础版、BTC版、ETH版，适用不同场景

### ⚠️ 局限

1. **高止损风险**：30% 止损可能承受较大回撤
2. **多数据源依赖**：需要额外的 STAKE/USD 和 COIN/USD 数据
3. **复杂度高**：反弹系统 + 多货币条件 + 组合管理
4. **回测限制**：多货币条件在回测中可能需要额外配置

---

## 九、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| BTC/ETH 抵押 | Schism3_BTC / Schism3_ETH | 使用专用变体 |
| 稳定币抵押 | Schism3 基础版 | 默认参数 |
| 高波动市场 | 调整止损 | 降低 stoploss |
| 长期持有 | 使用子策略 | 1h+4h 框架 |

---

## 十、适用市场环境详解

Schism3 是**智能反弹型策略**。基于其代码架构和社区长期实盘验证的经验，它最适合**震荡上行市场**，而在**单边下跌**时表现不佳。

### 10.1 策略核心逻辑

- **反弹预信号**：检测潜在反弹条件，记录价格
- **价格确认**：等待价格回升确认才入场
- **多货币过滤**：BTC/ETH 抵押时额外检查抵押货币趋势
- **组合管理**：考虑整体仓位的卖出决策

### 10.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 震荡上行 | ⭐⭐⭐⭐⭐ | 反弹信号精准，价格确认有效 |
| 🔄 横盘震荡 | ⭐⭐⭐☆☆ | 反弹信号可能频繁触发 |
| 📉 单边下跌 | ⭐⭐☆☆☆ | 30% 止损可能被触发 |
| ⚡️ 高波动 | ⭐⭐⭐☆☆ | 反弹价格跟踪可能失效 |

### 10.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| `bounce-lookback` | 5-10 | 回看周期，波动大时可调大 |
| `stoploss` | -0.15 ~ -0.25 | 根据风险承受调整 |
| `up-inf-rsi` | 55-65 | 趋势确认阈值 |

---

## 十一、总结

**Schism3** 是一个**高度可配置的反弹交易策略**。它的核心价值在于：

1. **反弹预信号系统**：先检测后确认，避免抄在半山腰
2. **多货币支持**：自动适配 BTC/ETH 抵押货币
3. **策略变体**：三个版本适用不同场景
4. **组合管理**：考虑整体仓位的智能决策

对于量化交易者而言，这是一个适合**震荡上行市场**的中高复杂度策略，需要配置好多货币数据源才能发挥最大效果。

---