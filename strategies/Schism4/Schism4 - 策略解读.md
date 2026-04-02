# Schism4 策略深度解读

> **策略编号**: #379 (465 个策略中的第 379 个)  
> **策略类型**: 多时间框架动量跟踪 + 动态止损策略  
> **时间框架**: 5 分钟 (5m) + 1 小时信息层

---

## 一、策略概览

Schism4 是一个基于相对动量指数（RMI）和多时间框架分析的量化交易策略。它采用双重时间框架确认机制，在 5 分钟图上进行交易决策，同时参考 1 小时图的趋势判断。策略的核心特点是买入条件严格、卖出机制灵活，并配有完善的订单保护机制。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 5 个核心买入信号（可独立启用/禁用），支持 BTC/ETH 质押币额外条件 |
| **卖出条件** | ROI 分级止盈 + 动态止损信号 |
| **保护机制** | 3 组订单保护（入场确认、买入超时、卖出超时） |
| **时间框架** | 5m 主时间框架 + 1h 信息时间框架 |
| **依赖库** | talib, arrow, cachetools, technical.indicators (RMI) |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.05,      # 立即：5%
    "10": 0.025,    # 10分钟后：2.5%
    "20": 0.015,    # 20分钟后：1.5%
    "30": 0.01,     # 30分钟后：1%
    "720": 0.005,   # 12小时后：0.5%
    "1440": 0       # 24小时后：0%（无条件退出）
}

# 止损设置
stoploss = -0.30    # 30% 固定止损
```

**设计思路**：
- 采用渐进式 ROI 策略，开盘即要求 5% 利润
- 随持仓时间延长，逐步降低利润目标
- 24 小时后无条件退出，避免长期套牢

### 2.2 订单类型配置

```python
use_sell_signal = False       # 不使用卖出信号强制卖出
sell_profit_only = True       # 仅盈利时卖出
ignore_roi_if_buy_signal = True  # 有买入信号时忽略 ROI
```

**配置解读**：策略的卖出信号仅作为"动态止损"使用，真正的盈利退出依赖 ROI 表。这一设计让策略在趋势行情中能持续持仓。

---

## 三、买入条件详解

### 3.1 核心买入参数

| 参数名 | 默认值 | 说明 |
|--------|--------|------|
| `inf-rsi` | 58 | 1小时 RSI 上限阈值 |
| `mp` | 26 | Momentum Pinball 下限阈值 |
| `rmi-fast` | 11 | 快速 RMI 下限阈值 |
| `rmi-slow` | 55 | 慢速 RMI 上限阈值 |
| `xinf-stake-rsi` | 25 | 质押币 1小时 RMI 上限（仅 BTC/ETH） |
| `xtf-fiat-rsi` | 64 | 法币 RSI 下限（仅 BTC/ETH） |
| `xtf-stake-rsi` | 90 | 质押币 RSI 上限（仅 BTC/ETH） |

### 3.2 买入条件逻辑分解

#### 条件组 1：趋势确认（基础层）

```python
# 条件逻辑
- 1小时 RSI <= 58 (大周期未过热)
- RMI 上升趋势确认 (rmi-up-trend == 1)
- 慢速 RMI <= 55 (动量未过高)
- 快速 RMI >= 11 (动量足够)
- Momentum Pinball >= 26 (动量强度达标)
```

#### 条件组 2：BTC/ETH 质押币专属条件

当质押币为 BTC 或 ETH 时，需额外满足：

```python
# 默认时间框架条件
- 质押币 RSI < 90 或 法币 RSI > 64
# 信息时间框架条件
- 质押币 1小时 RMI < 25
```

### 3.3 持仓信号延续机制

策略设计了一个独特的"持仓信号延续"机制：

```python
if trade_data['active_trade']:
    # 利润因子随 RMI 动态调整
    profit_factor = (1 - (dataframe['rmi-slow'].iloc[-1] / 400))
    # RMI 阈值从 30 渐进增长到 70
    rmi_grow = linear_growth(30, 70, 180, 720, trade_data['open_minutes'])
    
    conditions.append(dataframe['rmi-up-trend'] == 1)
    conditions.append(trade_data['current_profit'] > (trade_data['peak_profit'] * profit_factor))
    conditions.append(dataframe['rmi-slow'] >= rmi_grow)
```

**设计意图**：已持仓的交易对若仍满足买入信号条件，可通过 `ignore_roi_if_buy_signal = True` 继续持有，从而在趋势行情中获取更大收益。

---

## 四、卖出逻辑详解

### 4.1 多层止盈系统

策略采用分级 ROI 止盈机制：

```
持仓时间       目标利润率    说明
──────────────────────────────────
0 分钟        5%          开盘即要求高收益
10 分钟       2.5%        短期调整目标
20 分钟       1.5%        中期调整目标
30 分钟       1%          逐步降低期望
12 小时       0.5%        长期持仓底线
24 小时       0%          无条件退出
```

### 4.2 动态止损机制

卖出信号设计为"动态止损"，仅在亏损情况下触发：

```python
# 亏损容忍度随时间增长
# 从 -3% 开始，300 分钟后变为 0
loss_cutoff = linear_growth(-0.03, 0, 0, 300, trade_data['open_minutes'])

# 触发条件
conditions.append(
    (trade_data['current_profit'] < loss_cutoff) & 
    (trade_data['current_profit'] > self.stoploss) &
    (dataframe['rmi-dn-trend'] == 1) & 
    (dataframe['volume'].gt(0))
)
```

### 4.3 智能卖出决策

策略根据持仓历史动态调整卖出条件：

| 场景 | 触发条件 | 卖出阈值 |
|------|---------|---------|
| 曾盈利但未达 ROI | `peak_profit > 0` | RMI 下穿 50 |
| 始终亏损 | `peak_profit <= 0` | RMI 下穿 10 |

### 4.4 仓位管理卖出

```python
# 根据空闲仓位数量调整卖出条件
if trade_data['free_slots'] > 0:
    max_market_down = -0.04 
    hold_pct = (1 / trade_data['free_slots']) * max_market_down
    conditions.append(trade_data['avg_other_profit'] >= hold_pct)
else:
    # 无空闲仓位时，允许最大亏损交易卖出
    conditions.append(trade_data['biggest_loser'] == True)
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| 动量指标 | RMI (相对动量指数) | 快速：8周期，慢速：21周期 |
| 趋势确认 | RMI 趋势方向 | 3周期滚动确认 |
| 动量强度 | Momentum Pinball | ROC(6) + RSI(6) 组合 |
| 超买超卖 | RSI (14周期) | 多时间框架确认 |

### 5.2 信息时间框架指标（1h）

策略使用 1 小时时间框架提供更高维度的趋势判断：

- **RSI (14)**：1 小时级别超买超卖判断
- **质押币 RMI**：仅 BTC/ETH 质押时使用
- **法币 RSI**：COIN/USD 汇率动量

### 5.3 指标计算详解

```python
# 相对动量指数 (RMI)
dataframe['rmi-slow'] = RMI(dataframe, length=21, mom=5)
dataframe['rmi-fast'] = RMI(dataframe, length=8, mom=4)

# Momentum Pinball
dataframe['roc'] = ta.ROC(dataframe, timeperiod=6)
dataframe['mp'] = ta.RSI(dataframe['roc'], timeperiod=6)

# RMI 趋势判断
dataframe['rmi-up'] = np.where(dataframe['rmi-slow'] >= dataframe['rmi-slow'].shift(), 1, 0)
dataframe['rmi-dn'] = np.where(dataframe['rmi-slow'] <= dataframe['rmi-slow'].shift(), 1, 0)
dataframe['rmi-up-trend'] = np.where(dataframe['rmi-up'].rolling(3).sum() >= 2, 1, 0)
dataframe['rmi-dn-trend'] = np.where(dataframe['rmi-dn'].rolling(3).sum() >= 2, 1, 0)
```

---

## 六、风险管理特色

### 6.1 订单价格保护

策略在订单层面设置了 1% 的价格保护：

```python
def check_buy_timeout(self, pair, trade, order, **kwargs):
    # 当前价格高于订单价格 1% 时取消买入
    if current_price > order['price'] * 1.01:
        return True

def check_sell_timeout(self, pair, trade, order, **kwargs):
    # 当前价格低于订单价格 1% 时取消卖出
    if current_price < order['price'] * 0.99:
        return True

def confirm_trade_entry(self, pair, order_type, amount, rate, **kwargs):
    # 入场确认时同样保护
    if current_price > rate * 1.01:
        return False
```

### 6.2 动态止损

止损逻辑随持仓时间变化：

- **初期**：容忍 -3% 亏损
- **300 分钟后**：亏损容忍度归零
- **硬止损**：-30% 固定止损

### 6.3 仓位智能管理

```python
# 空闲仓位与卖出决策联动
# 1 个空闲仓位：允许在平均利润 >= -4% 时卖出
# 4 个空闲仓位：允许在平均利润 >= -1% 时卖出
hold_pct = (1 / free_slots) * (-0.04)
```

---

## 七、策略优势与局限

### ✅ 优势

1. **多时间框架确认**：5 分钟入场，1 小时趋势确认，降低假信号
2. **动态参数调整**：RMI 阈值随持仓时间增长，利润因子动态调整
3. **完善的保护机制**：订单超时保护、入场确认、仓位管理联动
4. **质押币适配**：针对 BTC/ETH 质押场景有专门的买入条件
5. **子策略支持**：内置 Schism4_BTC 和 Schism4_ETH 子策略

### ⚠️ 局限

1. **参数较多**：7 个买入参数 + 2 个卖出参数，优化难度大
2. **依赖实时数据**：大量使用 `Trade` 数据库查询，回测与实盘差异明显
3. **高初始 ROI**：5% 的初始目标可能导致频繁错过短期机会
4. **固定止损较大**：30% 止损对保守交易者来说偏高

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 震荡上行 | 默认配置 | 策略设计场景，能捕捉趋势中的回调入场 |
| 强趋势 | 降低 ROI 目标 | 提高持仓时间，获取更大收益 |
| 高波动 | 增大止损保护 | 可考虑调整 `stoploss` 至 -20% |
| 低流动性 | 谨慎使用 | 订单簿保护可能频繁触发 |

---

## 九、适用市场环境详解

Schism4 系列是典型的**多时间框架动量跟踪策略**。基于其代码架构和社区长期实盘验证的经验，它最适合 **震荡上行的趋势市场**，而在 **单边暴跌或极端波动市场** 时表现不佳。

### 9.1 策略核心逻辑

- **双重 RMI 确认**：快速和慢速 RMI 结合，过滤假突破
- **趋势跟踪优先**：rmi-up-trend 确保只在趋势向上时入场
- **时间衰减 ROI**：随持仓时间延长降低目标，平衡收益与风险

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛震荡 | ⭐⭐⭐⭐⭐ | 完美场景，回调入场+趋势持仓 |
| 🔄 横盘震荡 | ⭐⭐⭐☆☆ | 可能频繁止损，ROI 目标难达 |
| 📉 单边下跌 | ⭐⭐☆☆☆ | 趋势判断失效，持续止损 |
| ⚡️ 极端波动 | ⭐☆☆☆☆ | 订单保护频繁触发，无法入场 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| `stoploss` | -0.25 ~ -0.30 | 根据风险承受调整 |
| `inf-rsi` | 50 ~ 60 | 趋势市场可提高，震荡市场降低 |
| `startup_candle_count` | 72 | 必须保持，确保指标稳定 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

Schism4 代码量约 300 行，涉及多个自定义方法和实时交易数据查询。新手需要理解：
- RMI 指标计算原理
- 线性增长函数的使用
- 仓位管理与卖出条件的联动
- 多时间框架数据的合并

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 1-5 对 | 2GB | 4GB |
| 6-15 对 | 4GB | 8GB |
| 16+ 对 | 8GB | 16GB |

### 10.3 回测与实盘的差异

**重要警告**：策略大量使用 `Trade.get_trades()` 查询当前持仓信息，这在回测模式下无法正确模拟。实盘表现可能与回测有较大差异。

### 10.4 手动交易者建议

若想手动借鉴此策略，重点关注：
1. RMI 上升趋势确认（3 周期内 2 次上涨）
2. 1 小时 RSI 未过热（< 58）
3. 快速 RMI 有动量（> 11），慢速 RMI 未超买（< 55）

---

## 十一、总结

**Schism4** 是一个**成熟的多时间框架动量跟踪策略**。它的核心价值在于：

1. **趋势确认优先**：双重 RMI + 多时间框架确认，降低假信号
2. **动态风控**：时间衰减止损、仓位联动卖出，风险控制灵活
3. **质押币适配**：针对 BTC/ETH 质押场景有专门优化
4. **子策略扩展**：支持 BTC 和 ETH 专属参数集

对于量化交易者而言，这是一个**值得深入研究的策略模板**，尤其适合希望在动量策略基础上加入多时间框架确认的交易者。但需注意回测与实盘的差异，建议先小资金验证。

---

## 附录：子策略参数

### Schism4_BTC（BTC 质押专用）

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
```

### Schism4_ETH（ETH 质押专用）

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
```