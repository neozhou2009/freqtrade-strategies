# Guacamole 策略深度解读

> **策略编号**: #7 (465 个策略中的第 7 个)  
> **策略类型**: 多指标动量策略（带订单簿检查）  
> **时间框架**: 5 分钟 (5m)

---

## 一、策略概览

**Guacamole** 是一个复杂的多指标动量策略，结合了 KAMA、MACD、RMI、SAR 等多个技术指标，并引入了订单簿（orderbook）检查机制来优化订单执行。策略名称来源于其"混合多种成分"的特点，就像制作鳄梨酱需要混合多种食材一样。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 多条件组合（KAMA + MACD + RMI + 成交量） |
| **卖出条件** | RMI 超卖 + 利润检查 |
| **保护机制** | 追踪止损 + 订单超时检查 |
| **时间框架** | 5 分钟 |
| **依赖库** | TA-Lib, technical |
| **特殊功能** | 订单簿检查、订单超时取消 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表（超参数优化结果）
minimal_roi = {
    "0": 0.13336,
    "19": 0.07455,
    "37": 0.04206,
    "57": 0.02682,
    "73": 0.01225,
    "125": 0.0037,
    "244": 0.0025,
}

# 止损设置
stoploss = -0.10  # -10%

# 追踪止损
trailing_stop = True
trailing_stop_positive = 0.01673
trailing_stop_positive_offset = 0.01851
trailing_only_offset_is_reached = False
```

**设计思路**：
- **多级 ROI**：7 级递减 ROI，持仓时间越长退出门槛越低
- **追踪止损**：1.67% 追踪启动，1.85% 偏移触发
- **超参数优化**：ROI 和追踪参数来自超参数优化结果

### 2.2 订单类型配置

使用 Freqtrade 默认配置，但实现了订单超时检查函数。

---

## 三、买入条件详解

### 3.1 买入逻辑（无持仓时）

```python
# 无持仓时的买入条件
conditions = [
    dataframe["kama-3"] > dataframe["kama-21"],           # KAMA 快线 > 慢线
    dataframe["macd"] > dataframe["macdsignal"],          # MACD > 信号线
    dataframe["macd"] > params["macd"],                   # MACD > 阈值
    dataframe["macdhist"] > params["macdhist"],           # MACD 柱 > 阈值
    dataframe["rmi"] > dataframe["rmi"].shift(),          # RMI 上升
    dataframe["rmi"] > params["rmi"],                     # RMI > 阈值
    dataframe["volume"] < (dataframe["volume_ma"] * 20),  # 成交量 < 均量×20
]
```

**逻辑解析**：
- **KAMA 趋势**：3 周期 KAMA > 21 周期 KAMA，确认短期趋势向上
- **MACD 金叉**：MACD 线在信号线上方，动量向上
- **MACD 阈值**：MACD 和 MACD 柱高于优化阈值
- **RMI 动量**：RMI 指标上升且高于阈值
- **成交量过滤**：排除异常高成交量（可能是操纵）

### 3.2 买入条件（有持仓时）

```python
# 有持仓时的加仓条件
conditions = [
    dataframe["close"] > dataframe["sar"],    # 价格 > SAR
    dataframe["rmi"] >= 75,                   # RMI >= 75
]
```

**说明**：已有持仓时，仅在趋势强劲时考虑加仓。

### 3.3 超参数

```python
# 买入超参数（优化结果）
buy_params = {
    "macd": -0.75454,
    "macdhist": -1,
    "rmi": 49,
}
```

---

## 四、卖出逻辑详解

### 4.1 卖出条件

```python
# 有持仓时的卖出条件
active_trade = Trade.get_trades([...]).all()
if active_trade:
    ob = self.dp.orderbook(metadata["pair"], 1)
    current_price = ob["asks"][0][0]
    current_profit = active_trade[0].calc_profit_ratio(rate=current_price)
    
    conditions = [
        dataframe["rmi"] < 30,           # RMI < 30（超卖）
        current_profit > -0.03,          # 利润 > -3%
        dataframe["volume"] > 0,         # 成交量 > 0
    ]
```

**逻辑解析**：
- **RMI 超卖**：RMI < 30 确认短期超卖
- **利润检查**：亏损不超过 3% 才卖出（避免大亏时割肉）
- **订单簿价格**：使用实时订单簿价格计算利润

### 4.2 订单超时检查

```python
# 买入订单超时检查
def check_entry_timeout(self, pair, trade, order, **kwargs) -> bool:
    ob = self.dp.orderbook(pair, 1)
    current_price = ob["bids"][0][0]
    if current_price > order["price"] * 1.01:  # 价格上涨超过 1%
        return True  # 取消订单
    return False

# 卖出订单超时检查
def check_exit_timeout(self, pair, trade, order, **kwargs) -> bool:
    ob = self.dp.orderbook(pair, 1)
    current_price = ob["asks"][0][0]
    if current_price < order["price"] * 0.99:  # 价格下跌超过 1%
        return True  # 取消订单
    return False
```

**作用**：
- 防止订单因价格变动而无法成交
- 超过 1% 价格偏离时取消订单

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **趋势指标** | KAMA | 3, 21 周期 | 趋势方向判断 |
| **动量指标** | MACD | 默认 | 动量强度和方向 |
| **动量指标** | RMI | 默认 | 相对动量指标 |
| **止损指标** | SAR | 默认 | 趋势跟踪止损 |
| **成交量** | Volume MA | 24 周期 | 成交量过滤 |

### 5.2 指标计算

```python
# KAMA（考夫曼自适应移动平均）
dataframe["kama-3"] = ta.KAMA(dataframe, timeperiod=3)
dataframe["kama-21"] = ta.KAMA(dataframe, timeperiod=21)

# MACD
macd = ta.MACD(dataframe)
dataframe["macd"] = macd["macd"]
dataframe["macdsignal"] = macd["macdsignal"]
dataframe["macdhist"] = macd["macdhist"]

# RMI（相对动量指标）
dataframe["rmi"] = RMI(dataframe)

# SAR
dataframe["sar"] = ta.SAR(dataframe)

# 成交量移动平均
dataframe["volume_ma"] = dataframe["volume"].rolling(window=24).mean()
```

---

## 六、风险管理特色

### 6.1 追踪止损

```python
trailing_stop = True
trailing_stop_positive = 0.01673
trailing_stop_positive_offset = 0.01851
trailing_only_offset_is_reached = False
```

**工作机制**：
1. 利润达到 1.851% 后启动追踪止损
2. 从最高点回撤 1.673% 时触发退出
3. 不需要先达到 offset 才启动（`trailing_only_offset_is_reached = False`）

### 6.2 订单超时检查

**买入订单**：
- 当前价格 > 订单价格 × 1.01 时取消

**卖出订单**：
- 当前价格 < 订单价格 × 0.99 时取消

### 6.3 卖出利润保护

```python
current_profit > -0.03  # 亏损不超过 3%
```

**作用**：避免在大额亏损时强制卖出。

---

## 七、策略优势与局限

### ✅ 优势

1. **多指标组合**：KAMA + MACD + RMI + SAR 多维度确认
2. **订单簿检查**：使用实时订单簿优化订单执行
3. **订单超时**：防止订单因价格变动无法成交
4. **追踪止损**：锁定利润，保护盈利
5. **超参数优化**：关键参数来自超参数优化

### ⚠️ 局限

1. **复杂度高**：多个指标和条件，调试困难
2. **无趋势过滤**：没有 EMA/SMA 长期趋势判断
3. **无 BTC 关联**：不检测比特币大盘趋势
4. **依赖订单簿**：需要交易所支持 orderbook API
5. **参数敏感**：超参数优化结果可能过拟合

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **震荡市** | 默认配置 | 多指标组合适合震荡行情 |
| **上涨趋势** | 默认配置 | 追踪止损能锁定利润 |
| **下跌趋势** | 暂停或轻仓 | 无趋势过滤，易亏损 |
| **高波动** | 调整参数 | 可能需要放宽订单超时阈值 |
| **低波动** | 调整 ROI | 降低 ROI 门槛适应小波动 |

---

## 九、适用市场环境详解

Guacamole 是一个多指标动量策略，基于"多条件确认"的核心哲学。

### 9.1 策略核心逻辑

- **多指标确认**：KAMA + MACD + RMI 同时确认才买入
- **订单簿优化**：使用实时订单簿价格检查和取消订单
- **追踪止损**：锁定利润，让利润奔跑

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★☆ | 多指标确认 + 追踪止损表现好 |
| 🔄 宽幅震荡 | ★★★★☆ | 多指标组合适合震荡行情 |
| 📉 单边暴跌 | ★★☆☆☆ | 无趋势过滤，可能连续亏损 |
| ⚡️ 极端横盘 | ★★★☆☆ | 波动太小，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-40 个 | 信号频率适中 |
| **最大持仓数** | 3-6 个 | 控制风险 |
| **仓位模式** | 固定仓位 | 建议固定仓位 |
| **时间框架** | 5m | 强制要求 |

---

## 十、重要提醒：订单簿依赖

### 10.1 学习成本中等

策略代码约 150 行，需要理解多个指标和订单簿机制。

### 10.2 硬件要求中等

多指标计算增加计算量：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 1GB | 2GB |
| 40-80 对 | 2GB | 4GB |

### 10.3 订单簿依赖

策略使用 `self.dp.orderbook()` 获取实时订单簿：
- 需要交易所支持 orderbook API
- 实盘中订单簿数据可能有延迟
- 回测中订单簿数据可能不准确

### 10.4 手动交易者建议

手动交易者可参考此策略的多指标思路：
- 同时观察 KAMA、MACD、RMI 多个指标
- 使用追踪止损保护利润
- 设置订单超时取消机制

---

## 十一、总结

**Guacamole** 是一个设计精良的多指标动量策略，它的核心价值在于：

1. **多指标组合**：KAMA + MACD + RMI + SAR 多维度确认
2. **订单簿优化**：使用实时订单簿价格检查和取消订单
3. **追踪止损**：锁定利润，保护盈利
4. **超参数优化**：关键参数来自超参数优化结果

对于量化交易者而言，这是一个优秀的多指标策略模板。建议：
- 作为多指标组合的进阶案例
- 学习订单簿检查和订单超时机制
- 可在此基础上添加趋势过滤、BTC 关联等保护机制
- 注意超参数可能过拟合，实盘前需充分测试

---
