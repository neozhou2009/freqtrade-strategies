# BBRSI4cust 策略深度解读

> **策略编号**: #21 (465 个策略中的第 21 个)  
> **策略类型**: 布林带 + RSI + 自定义退出  
> **时间框架**: 15 分钟 (15m)

---

## 一、策略概览

**BBRSI4cust** 是一个基于布林带和 RSI 的均值回归策略，特色是使用了自定义退出（custom_exit）函数来优化卖出逻辑。策略名称中的"4cust"表明其自定义退出功能，"BB"代表布林带，"RSI"代表相对强弱指标。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 1 个条件：PLUS_DI + 布林带突破 |
| **卖出条件** | 自定义退出函数 + 技术卖出信号 |
| **保护机制** | 硬止损 + 追踪止损 |
| **时间框架** | 15 分钟 |
| **依赖库** | TA-Lib, technical |
| **特殊功能** | custom_exit 自定义退出 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.003    # 立即退出：0.3% 利润
}

# 止损设置
stoploss = -0.1  # -10% 硬止损

# 追踪止损
trailing_stop = True
```

**设计思路**：
- **极低 ROI**：仅 0.3% ROI，追求快速周转
- **标准止损**：-10% 硬止损
- **追踪止损**：启用但未配置具体参数

### 2.2 订单类型配置

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}

order_time_in_force = {
    "entry": "GTC",
    "exit": "GTC",
}
```

### 2.3 超参数

```python
# 买入超参数
buy_bb = IntParameter(low=1, high=4, default=1, space="entry")  # 布林带标准差
buy_di = IntParameter(low=10, high=20, default=20, space="entry")  # PLUS_DI 阈值

# 卖出超参数
sell_bb = IntParameter(low=1, high=4, default=1, space="exit")  # 布林带标准差
```

---

## 三、买入条件详解

### 3.1 买入逻辑

```python
# 买入条件
dataframe.loc[
    (
        (dataframe["plus_di"] > self.buy_di.value) &           # PLUS_DI > 阈值
        (qtpylib.crossed_below(dataframe["low"], dataframe["bb_lowerband"])) &  # 价格跌破布林带下轨
        (dataframe["volume"] > 0)                               # 成交量 > 0
    ),
    "enter_long",
] = 1
```

**逻辑解析**：
- **PLUS_DI 确认**：+DI 高于阈值（默认 20），确认上升动能
- **布林带突破**：价格跌破布林带下轨，统计意义上的低位
- **成交量过滤**：排除零成交量

### 3.2 指标计算

```python
# PLUS_DI
dataframe["plus_di"] = ta.PLUS_DI(dataframe)

# RSI
dataframe["rsi"] = ta.RSI(dataframe)

# 布林带（20 周期，可调节标准差）
bollinger = qtpylib.bollinger_bands(
    qtpylib.typical_price(dataframe), window=20, stds=self.buy_bb.value
)
dataframe["bb_lowerband"] = bollinger["lower"]
dataframe["bb_middleband"] = bollinger["mid"]
dataframe["bb_upperband"] = bollinger["upper"]
```

---

## 四、卖出逻辑详解

### 4.1 技术卖出信号

```python
# 卖出条件
dataframe.loc[
    (
        (qtpylib.crossed_above(dataframe["high"], dataframe["bb_middleband1"])) &
        (dataframe["volume"] > 0)
    ),
    "exit_long",
] = 1
```

**逻辑解析**：
- **布林带中轨突破**：价格上穿布林带中轨（使用 sell_bb 参数）
- **成交量确认**：成交量大于 0

### 4.2 自定义退出函数

```python
def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
    current_candle = dataframe.iloc[-1].squeeze()
    
    # 检查价格是否突破布林带中轨
    if current_rate > current_candle["bb_middleband1"]:
        return "bb_profit_sell"
    
    return None
```

**作用**：
- 实时监控价格突破布林带中轨
- 返回自定义退出原因"bb_profit_sell"
- 补充技术卖出信号的不足

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **动量指标** | PLUS_DI | 默认 | 上升方向指标 |
| **动量指标** | RSI | 14 周期 | 超买超卖 |
| **波动指标** | Bollinger Bands | 20 周期，可调标准差 | 价格边界 |

### 5.2 双布林带系统

策略使用两套布林带系统：

| 布林带 | 周期 | 标准差 | 用途 |
|--------|------|--------|------|
| BB1 | 20 | buy_bb（默认 1） | 买入参考 |
| BB2 | 20 | sell_bb（默认 1） | 卖出参考 |

---

## 六、风险管理特色

### 6.1 硬止损

```python
stoploss = -0.1  # -10%
```

**说明**：标准止损，控制单笔亏损在 10% 以内。

### 6.2 追踪止损

```python
trailing_stop = True
```

**作用**：启用追踪止损，保护盈利。

### 6.3 自定义退出

```python
if current_rate > current_candle["bb_middleband1"]:
    return "bb_profit_sell"
```

**作用**：
- 实时监控价格突破
- 补充技术信号延迟
- 提高退出及时性

---

## 七、策略优势与局限

### ✅ 优势

1. **自定义退出**：灵活控制卖出时机
2. **超参数优化**：支持 Hyperopt 优化布林带标准差
3. **双重卖出**：技术信号 + 自定义退出
4. **计算量小**：指标少，对硬件要求低
5. **低 ROI**：0.3% ROI，快速周转

### ⚠️ 局限

1. **无趋势过滤**：没有长期趋势判断
2. **无 BTC 关联**：不检测比特币大盘趋势
3. **极低 ROI**：0.3% 可能过早退出
4. **15 分钟框架**：信号频率较低
5. **参数敏感**：布林带标准差需要优化

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **震荡市** | 默认配置 | 均值回归最适合震荡行情 |
| **上涨趋势** | 默认配置 | 低 ROI 可快速周转 |
| **下跌趋势** | 暂停或轻仓 | 无趋势过滤，易亏损 |
| **高波动** | 调整布林带 | 可能需要调整标准差 |
| **低波动** | 调整 ROI | 降低 ROI 门槛适应小波动 |

---

## 九、适用市场环境详解

BBRSI4cust 是经典的均值回归策略，基于"价格回归均值"的核心哲学。

### 9.1 策略核心逻辑

- **布林带突破**：价格跌破下轨买入，突破中轨卖出
- **PLUS_DI 确认**：确认上升动能
- **自定义退出**：实时监控价格突破

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★☆ | 均值回归 + 低 ROI 表现好 |
| 🔄 宽幅震荡 | ★★★★★ | 震荡行情是均值回归的理想环境 |
| 📉 单边暴跌 | ★★☆☆☆ | 无趋势过滤，可能连续亏损 |
| ⚡️ 极端横盘 | ★★★☆☆ | 波动太小，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-40 个 | 信号频率适中 |
| **最大持仓数** | 3-6 个 | 控制风险 |
| **仓位模式** | 固定仓位 | 建议固定仓位 |
| **时间框架** | 15m | 强制要求 |

---

## 十、重要提醒：自定义退出的使用

### 10.1 学习成本中等

策略代码约 100 行，需要理解自定义退出函数。

### 10.2 硬件要求低

仅计算 PLUS_DI、RSI、布林带，对 VPS 要求低：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 512MB | 1GB |
| 40-80 对 | 1GB | 2GB |

### 10.3 自定义退出优势

- **实时监控**：不受 K 线闭合限制
- **灵活控制**：可以添加任意退出条件
- **提高及时性**：减少信号延迟

### 10.4 手动交易者建议

手动交易者可参考此策略的自定义退出思路：
- 设置价格突破布林带中轨退出
- 使用 PLUS_DI 确认上升动能
- 设置严格止损（如 -10%）

---

## 十一、总结

**BBRSI4cust** 是一个经典的均值回归策略，它的核心价值在于：

1. **自定义退出**：灵活控制卖出时机
2. **超参数优化**：支持 Hyperopt 优化布林带标准差
3. **双重卖出**：技术信号 + 自定义退出
4. **计算量小**：指标少，对硬件要求低
5. **低 ROI**：0.3% ROI，快速周转

对于量化交易者而言，这是一个优秀的自定义退出学习模板。建议：
- 作为学习 custom_exit 函数的入门案例
- 理解布林带均值回归的使用方法
- 可在此基础上添加趋势过滤、BTC 关联等机制
- 注意超低 ROI 可能过早退出大趋势

---
