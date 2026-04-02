# Guacamole 策略深度解读

> **策略编号**: #191 (465 个策略中的第 191 个)  
> **策略类型**: 多指标综合 / 趋势跟踪  
> **时间框架**: 5 分钟 (5m)

---

## 一、策略概览

**Guacamole** 是一个基于 MACD、KAMA 和 RMI 指标的趋势跟踪策略。策略核心思想是：在上升趋势中捕捉买入机会，通过多指标确认趋势方向和动量变化。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 多条件组合：KAMA 趋势确认 + MACD 信号 + RMI 动量 |
| **卖出条件** | 订单簿动态止盈/止损 + RMI 极端值退出 |
| **保护机制** | 追踪止损 + 订单超时管理 |
| **时间框架** | 5 分钟 |
| **依赖库** | TA-Lib, technical (qtpylib, RMI, VIDYA) |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
minimal_roi = {
    "0": 0.13336,    # 立即退出：13.34% 利润
    "19": 0.07455,   # 19分钟后：7.46% 利润
    "37": 0.04206,   # 37分钟后：4.21% 利润
    "57": 0.02682,   # 57分钟后：2.68% 利润
    "73": 0.01225,   # 73分钟后：1.23% 利润
    "125": 0.0037,   # 125分钟后：0.37% 利润
    "244": 0.0025,   # 244分钟后：0.25% 利润
}

stoploss = -0.10     # -10% 硬止损

trailing_stop = True
trailing_stop_positive = 0.01673     # 1.67% 追踪启动点
trailing_stop_positive_offset = 0.01851  # 1.85% 偏移触发
```

**设计思路**：
- **激进 ROI**：首级 ROI 高达 13.34%，表明策略预期捕捉大波动
- **紧凑止损**：-10% 止损较为紧凑，给予交易较小波动空间
- **追踪止损**：1.67% 启动点 + 1.85% 偏移，适合趋势延续行情

### 2.2 订单类型配置

```python
order_types = {
    'entry': 'limit',
    'exit': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}
```

---

## 三、买入条件详解

### 3.1 无持仓时的买入逻辑

```python
# 核心买入条件
conditions.append(dataframe["kama-3"] > dataframe["kama-21"])  # KAMA 上升趋势
conditions.append(dataframe["macd"] > dataframe["macdsignal"])  # MACD 金叉
conditions.append(dataframe["macd"] > params["macd"])  # MACD 值阈值
conditions.append(dataframe["macdhist"] > params["macdhist"])  # MACD 柱状图
conditions.append(dataframe["rmi"] > dataframe["rmi"].shift())  # RMI 上升
conditions.append(dataframe["rmi"] > params["rmi"])  # RMI 阈值
conditions.append(dataframe["volume"] < (dataframe["volume_ma"] * 20))  # 成交量过滤
```

**逻辑解析**：
1. **KAMA 趋势确认**：3 期 KAMA > 21 期 KAMA，表明短期趋势向上
2. **MACD 金叉确认**：MACD 线 > Signal 线，同时满足阈值条件
3. **RMI 动量确认**：RMI 持续上升并突破阈值
4. **成交量过滤**：当前成交量低于平均成交量 20 倍，避免放量假突破

### 3.2 有持仓时的买入逻辑（持续买入信号）

```python
# 持仓时：价格突破 SAR 且 RMI 强势
conditions.append(dataframe["close"] > dataframe["sar"])  # 价格在 SAR 上方
conditions.append(dataframe["rmi"] >= 75)  # RMI 强势
```

---

## 四、卖出逻辑详解

### 4.1 主动卖出条件

```python
# 卖出条件（仅在有持仓时检查）
conditions.append(dataframe["rmi"] < 30)  # RMI 进入超卖区域
conditions.append(current_profit > -0.03)  # 盈利或小亏
conditions.append(dataframe["volume"].gt(0))  # 有成交量
```

### 4.2 订单超时管理

```python
# 入场超时：价格超过订单价格 1% 时取消
def check_entry_timeout(pair, trade, order):
    if current_price > order["price"] * 1.01:
        return True
    return False

# 出场超时：价格低于订单价格 1% 时取消
def check_exit_timeout(pair, trade, order):
    if current_price < order["price"] * 0.99:
        return True
    return False

# 确认交易入场：价格超过报价 1% 时拒绝
def confirm_trade_entry(pair, order_type, amount, rate, time_in_force):
    if current_price > rate * 1.01:
        return False
    return True
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| **趋势指标** | KAMA (3, 21) | 趋势方向确认 |
| **动量指标** | MACD, MACD Signal, MACD Hist | 趋势动量 |
| **动量指标** | RMI | 相对动量变化 |
| **价格指标** | SAR | 趋势反转点 |
| **成交量指标** | Volume MA (24) | 成交量过滤 |

### 5.2 指标计算细节

```python
# KAMA 计算
dataframe["kama-3"] = ta.KAMA(dataframe, timeperiod=3)
dataframe["kama-21"] = ta.KAMA(dataframe, timeperiod=21)

# MACD 计算
macd = ta.MACD(dataframe)
dataframe["macd"] = macd["macd"]
dataframe["macdsignal"] = macd["macdsignal"]
dataframe["macdhist"] = macd["macdhist"]

# RMI 计算
dataframe["rmi"] = RMI(dataframe)

# SAR 计算
dataframe["sar"] = ta.SAR(dataframe)

# 成交量均线
dataframe["volume_ma"] = dataframe["volume"].rolling(window=24).mean()
```

---

## 六、风险管理特色

### 6.1 追踪止损系统

- **启动条件**：盈利 1.67% 后激活
- **追踪距离**：1.85% 偏移
- **适用场景**：趋势延续行情

### 6.2 订单超时管理

| 场景 | 超时条件 | 处理方式 |
|------|---------|---------|
| 入场超时 | 价格 > 订单价格 × 1.01 | 取消订单 |
| 出场超时 | 价格 < 订单价格 × 0.99 | 取消订单 |
| 确认入场 | 价格 > 报价 × 1.01 | 拒绝下单 |

---

## 七、策略优势与局限

### ✅ 优势

1. **多指标确认**：使用 KAMA、MACD、RMI 三个独立指标，降低假信号概率
2. **成交量过滤**：避免在高成交量假突破中入场
3. **订单管理严格**：完善的超时和确认机制，减少滑点损失
4. **追踪止损**：保护已有利润

### ⚠️ 局限

1. **参数敏感**：MACD 和 RMI 阈值需要针对不同市场优化
2. **趋势依赖**：在震荡市场中表现不佳
3. **复杂条件**：7 个条件同时满足，入场机会较少

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 强牛市 | 启用 | 多指标确认，趋势中表现优异 |
| 强熊市 | 启用 | 做空逻辑相同，可捕捉下跌趋势 |
| 震荡市场 | 谨慎 | 条件难以同时满足 |
| 横盘整理 | 不推荐 | 假信号较多 |

---

## 九、适用市场环境详解

**Guacamole** 是一个典型的多指标趋势跟踪策略。基于其代码架构和指标组合，它最适合 **有明显趋势的市场**（如强牛市或强熊市），而在 **震荡市场和横盘整理** 时表现不佳。

### 9.1 策略核心逻辑

- **趋势确认**：KAMA 均线交叉判断趋势方向
- **动量验证**：MACD 和 RMI 验证趋势强度
- **过滤机制**：成交量过滤避免假突破

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 强牛市 | ⭐⭐⭐⭐⭐ | 趋势明确，多指标共振 |
| 🔄 震荡市场 | ⭐⭐⭐☆☆ | 条件难以同时满足 |
| 📉 强熊市 | ⭐⭐⭐⭐☆ | 可捕捉下跌趋势 |
| ⚡️ 横盘整理 | ⭐⭐☆☆☆ | 频繁出现假信号 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

策略包含 7 个独立买入条件，需要深入理解每个指标的含义和相互作用。

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 10-20 对 | 2GB | 4GB |
| 20-50 对 | 4GB | 8GB |

### 10.3 回测与实盘的差异

- 订单超时逻辑在实盘中有助于避免滑点
- 成交量过滤条件可能在低流动性币种上过于严格

---

## 十一、总结

**Guacamole** 是一个设计精良的多指标趋势跟踪策略。它的核心价值在于：

1. **多维度验证**：通过趋势、动量、成交量三个维度验证信号
2. **严格的订单管理**：完善的超时机制减少不必要的损失
3. **追踪止损保护**：在趋势行情中锁定利润

对于量化交易者而言，建议先在历史数据上充分回测，调整 MACD 和 RMI 阈值以适应目标市场，然后再进行小资金实盘测试。

---