# NotAnotherSMAOffsetStrategy 策略深度解读

> **策略编号**: #23 (465 个策略中的第 23 个)  
> **策略类型**: SMA 偏移 + EWO 趋势跟踪  
> **时间框架**: 5 分钟 (5m)

---

## 一、策略概览

**NotAnotherSMAOffsetStrategy** 是一个基于 SMA 偏移的趋势跟踪策略，由 @Rallipanos 开发。策略名称自嘲"Not Another"（又一个），表明这是众多 SMA 策略中的又一个变体，但通过偏移量（offset）来捕捉深度回调，并结合 EWO（Elliot Wave Oscillator）来确认趋势。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 3 种模式（EWO 高 + EWO 低 + EWO 极低） |
| **卖出条件** | 多条件组合（SMA9 + EMA + RSI） |
| **保护机制** | 追踪止损 + 确认交易退出 |
| **时间框架** | 5 分钟 |
| **依赖库** | TA-Lib, technical, numpy |
| **特殊功能** | SMA 偏移交易、EWO 确认 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.215,     # 立即退出：21.5% 利润
    "40": 0.032,    # 40 分钟后：3.2% 利润
    "87": 0.016,    # 87 分钟后：1.6% 利润
    "201": 0,       # 201 分钟后：保本退出
}

# 止损设置
stoploss = -0.35  # -35% 硬止损（极宽松）

# 追踪止损
trailing_stop = True
trailing_stop_positive = 0.005       # 0.5% 追踪启动
trailing_stop_positive_offset = 0.03  # 3% 偏移触发
trailing_only_offset_is_reached = True
```

**设计思路**：
- **高 ROI**：首级 21.5% ROI，预期捕捉大趋势
- **极宽松止损**：-35% 硬止损，给予极大波动空间
- **追踪止损**：3% 利润后启动 0.5% 追踪

### 2.2 超参数

```python
# 买入超参数
base_nb_candles_buy = IntParameter(5, 80, default=14, space="buy")
low_offset = DecimalParameter(0.9, 0.99, default=0.975, space="buy")
low_offset_2 = DecimalParameter(0.9, 0.99, default=0.955, space="buy")
ewo_low = DecimalParameter(-20.0, -8.0, default=-20.988, space="buy")
ewo_high = DecimalParameter(2.0, 12.0, default=2.327, space="buy")
ewo_high_2 = DecimalParameter(-6.0, 12.0, default=-2.327, space="buy")
rsi_buy = IntParameter(30, 70, default=69, space="buy")

# 卖出超参数
base_nb_candles_sell = IntParameter(5, 80, default=24, space="sell")
high_offset = DecimalParameter(0.95, 1.1, default=0.991, space="sell")
high_offset_2 = DecimalParameter(0.99, 1.5, default=0.997, space="sell")
```

### 2.3 订单类型配置

```python
order_time_in_force = {
    "entry": "GTC",
    "exit": "ioc",  # Immediate Or Cancel
}
```

---

## 三、买入条件详解

### 3.1 买入逻辑（3 种模式）

**模式 1：EWO 高位回调**
```python
(
    (rsi_fast < 35) &
    (close < ma_buy_14 * low_offset_0.975) &
    (EWO > ewo_high_2.327) &
    (rsi < rsi_buy_69) &
    (volume > 0) &
    (close < ma_sell_24 * high_offset_0.991)
)
```

**模式 2：EWO 高位深度回调**
```python
(
    (rsi_fast < 35) &
    (close < ma_buy_14 * low_offset_2_0.955) &
    (EWO > ewo_high_2_-2.327) &
    (rsi < rsi_buy_69) &
    (volume > 0) &
    (close < ma_sell_24 * high_offset_0.991) &
    (rsi < 25)
)
```

**模式 3：EWO 低位回调**
```python
(
    (rsi_fast < 35) &
    (close < ma_buy_14 * low_offset_0.975) &
    (EWO < ewo_low_-20.988) &
    (volume > 0) &
    (close < ma_sell_24 * high_offset_0.991)
)
```

**逻辑解析**：
- **RSI 快速超卖**：RSI(4) < 35，确认短期超卖
- **SMA 偏移买入**：价格低于 SMA×偏移量（如 0.975），捕捉深度回调
- **EWO 确认**：EWO 高位或低位，确认波浪位置
- **成交量过滤**：排除异常成交量

### 3.2 指标计算

```python
# SMA 偏移
for val in self.base_nb_candles_buy.range:
    dataframe[f"ma_buy_{val}"] = ta.EMA(dataframe, timeperiod=val)

for val in self.base_nb_candles_sell.range:
    dataframe[f"ma_sell_{val}"] = ta.EMA(dataframe, timeperiod=val)

# HMA + EMA
dataframe["hma_50"] = qtpylib.hull_moving_average(dataframe["close"], window=50)
dataframe["ema_100"] = ta.EMA(dataframe, timeperiod=100)

# EWO（Elliot Wave Oscillator）
dataframe["EWO"] = EWO(dataframe, self.fast_ewo, self.slow_ewo)

# RSI
dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
dataframe["rsi_fast"] = ta.RSI(dataframe, timeperiod=4)
dataframe["rsi_slow"] = ta.RSI(dataframe, timeperiod=20)
```

---

## 四、卖出逻辑详解

### 4.1 技术卖出信号

**模式 1：SMA9 + EMA 偏移**
```python
(
    (close > sma_9) &
    (close > ma_sell_24 * high_offset_2_0.997) &
    (rsi > 50) &
    (volume > 0) &
    (rsi_fast > rsi_slow)
)
```

**模式 2：HMA + EMA 偏移**
```python
(
    (close < hma_50) &
    (close > ma_sell_24 * high_offset_0.991) &
    (volume > 0) &
    (rsi_fast > rsi_slow)
)
```

### 4.2 确认交易退出

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, current_time, **kwargs) -> bool:
    if sell_reason in ["sell_signal"]:
        if (last_candle["hma_50"] * 1.149 > last_candle["ema_100"]) and (
            last_candle["close"] < last_candle["ema_100"] * 0.951
        ):
            return False  # 阻止退出
    return True
```

**作用**：
- 根据 HMA 和 EMA 关系阻止过早退出
- 让利润在趋势中奔跑

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **趋势指标** | EMA | 5-80 周期（可优化） | SMA 偏移买入/卖出 |
| **趋势指标** | HMA | 50 周期 | 趋势判断 |
| **趋势指标** | EMA | 100 周期 | 长期趋势 |
| **动量指标** | EWO | 50/200 | 波浪振荡器 |
| **动量指标** | RSI | 4/14/20 周期 | 超买超卖 |
| **SMA** | SMA | 9 周期 | 卖出确认 |

### 5.2 EWO（Elliot Wave Oscillator）

```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(dataframe, timeperiod=ema_length)
    ema2 = ta.EMA(dataframe, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / dataframe["low"] * 100
    return emadif
```

**用途**：
- 确认波浪位置
- EWO > 2.327：高位回调买入
- EWO < -20.988：低位回调买入

---

## 六、风险管理特色

### 6.1 极宽松硬止损

```python
stoploss = -0.35  # -35%
```

**说明**：极宽松止损，给予极大波动空间，适合捕捉大趋势。

### 6.2 追踪止损

```python
trailing_stop = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.03
trailing_only_offset_is_reached = True
```

**工作机制**：
1. 利润达到 3% 后启动追踪止损
2. 从最高点回撤 0.5% 时触发退出

### 6.3 确认交易退出

```python
if (hma_50 * 1.149 > ema_100) and (close < ema_100 * 0.951):
    return False  # 阻止退出
```

**作用**：
- 根据 HMA 和 EMA 关系阻止过早退出
- 让利润在趋势中奔跑

---

## 七、策略优势与局限

### ✅ 优势

1. **SMA 偏移交易**：捕捉深度回调
2. **EWO 确认**：波浪振荡器确认趋势
3. **多买入模式**：3 种模式覆盖不同场景
4. **确认交易退出**：根据 HMA/EMA 阻止过早退出
5. **超参数优化**：支持 Hyperopt 优化关键参数
6. **追踪止损**：锁定利润，保护盈利

### ⚠️ 局限

1. **复杂度高**：多模式 + 多指标，调试困难
2. **无 BTC 关联**：不检测比特币大盘趋势
3. **参数敏感**：超参数优化结果可能过拟合
4. **极宽松止损**：-35% 止损在极端行情下可能造成较大亏损
5. **计算量大**：多 EMA + HMA + EWO 增加计算负担

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **震荡市** | 默认配置 | SMA 偏移适合震荡行情 |
| **上涨趋势** | 默认配置 | EWO + 追踪止损表现好 |
| **下跌趋势** | 暂停或轻仓 | 无长期趋势过滤，易亏损 |
| **高波动** | 调整参数 | 可能需要调整止损阈值 |
| **低波动** | 调整 ROI | 降低 ROI 门槛适应小波动 |

---

## 九、适用市场环境详解

NotAnotherSMAOffsetStrategy 是基于"SMA 偏移 + EWO 确认"核心哲学的策略。

### 9.1 策略核心逻辑

- **SMA 偏移**：价格低于 SMA×偏移量时买入，捕捉深度回调
- **EWO 确认**：波浪振荡器确认趋势位置
- **多模式买入**：3 种模式覆盖不同场景
- **确认退出**：根据 HMA/EMA 阻止过早退出

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★★ | SMA 偏移 + EWO + 追踪止损，完美匹配 |
| 🔄 宽幅震荡 | ★★★★☆ | SMA 偏移适合震荡行情 |
| 📉 单边暴跌 | ★★☆☆☆ | 无长期趋势过滤，可能连续亏损 |
| ⚡️ 极端横盘 | ★★★☆☆ | 波动太小，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-40 个 | 信号频率适中 |
| **最大持仓数** | 3-6 个 | 控制风险 |
| **仓位模式** | 固定仓位 | 建议固定仓位 |
| **时间框架** | 5m | 强制要求 |

---

## 十、重要提醒：SMA 偏移的使用

### 10.1 学习成本高

策略代码约 200 行，需要理解 SMA 偏移、EWO、确认交易退出等概念。

### 10.2 硬件要求中等

多 EMA + HMA + EWO 增加计算量：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 1GB | 2GB |
| 40-80 对 | 2GB | 4GB |

### 10.3 SMA 偏移优势

- **捕捉深度回调**：价格低于 SMA×偏移量时买入
- **减少假信号**：偏移量过滤浅层回调
- **灵活调整**：可通过 Hyperopt 优化偏移量

### 10.4 手动交易者建议

手动交易者可参考此策略的 SMA 偏移思路：
- 设置价格低于 SMA×偏移量时买入
- 使用 EWO 确认波浪位置
- 设置追踪止损保护利润

---

## 十一、总结

**NotAnotherSMAOffsetStrategy** 是一个设计精良的 SMA 偏移策略，它的核心价值在于：

1. **SMA 偏移交易**：捕捉深度回调
2. **EWO 确认**：波浪振荡器确认趋势
3. **多买入模式**：3 种模式覆盖不同场景
4. **确认交易退出**：根据 HMA/EMA 阻止过早退出
5. **超参数优化**：支持 Hyperopt 优化关键参数
6. **追踪止损**：锁定利润，保护盈利

对于量化交易者而言，这是一个优秀的 SMA 偏移学习模板。建议：
- 作为学习 SMA 偏移策略的进阶案例
- 理解 EWO 波浪振荡器的使用方法
- 学习确认交易退出的应用
- 注意超参数可能过拟合，实盘前需充分测试

---
