# ichiV1 策略深度解读

> **策略编号**: #27 (465 个策略中的第 27 个)  
> **策略类型**: 一目均衡表 + 多时间框架趋势跟踪  
> **时间框架**: 5 分钟 (5m)

---

## 一、策略概览

**ichiV1** 是一个基于一目均衡表（Ichimoku Cloud）的多时间框架趋势跟踪策略。策略特色是使用多个时间框架的 EMA 来确认趋势强度（Fan 扇形），并结合一目均衡表的云层来过滤趋势。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 多条件组合（云层 + 多时间框架趋势 + Fan 扇形） |
| **卖出条件** | 1 个条件：趋势交叉 |
| **保护机制** | 硬止损 + 追踪止损 |
| **时间框架** | 5 分钟 |
| **依赖库** | TA-Lib, technical, pandas, numpy |
| **特殊功能** | 多时间框架趋势确认、Fan 扇形 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.059,     # 立即退出：5.9% 利润
    "10": 0.037,    # 10 分钟后：3.7% 利润
    "41": 0.012,    # 41 分钟后：1.2% 利润
    "114": 0,       # 114 分钟后：保本退出
}

# 止损设置
stoploss = -0.275  # -27.5% 硬止损

# 追踪止损
trailing_stop = True
```

**设计思路**：
- **多级 ROI**：4 级递减 ROI，持仓时间越长退出门槛越低
- **宽松止损**：-27.5% 硬止损，给予充分波动空间
- **追踪止损**：启用但未配置具体参数

### 2.2 超参数

```python
# 买入超参数
buy_params = {
    "buy_trend_above_senkou_level": 1,      # 趋势在云层上方级别
    "buy_trend_bullish_level": 6,           # 趋势多头级别
    "buy_fan_magnitude_shift_value": 3,     # Fan 幅度偏移
    "buy_min_fan_magnitude_gain": 1.002,    # 最小 Fan 幅度增益
}

# 卖出超参数
sell_params = {
    "sell_trend_indicator": "trend_close_2h",  # 卖出趋势指标
}
```

---

## 三、买入条件详解

### 3.1 买入逻辑

**趋势在云层上方（8 个级别）**
```python
# 级别 1-8，从 5m 到 8h
if buy_trend_above_senkou_level >= 1:
    conditions.append(trend_close_5m > senkou_a)
    conditions.append(trend_close_5m > senkou_b)
if buy_trend_above_senkou_level >= 2:
    conditions.append(trend_close_15m > senkou_a)
    conditions.append(trend_close_15m > senkou_b)
# ... 直到 8h
```

**趋势多头（8 个级别）**
```python
# 级别 1-8，从 5m 到 8h
if buy_trend_bullish_level >= 1:
    conditions.append(trend_close_5m > trend_open_5m)
if buy_trend_bullish_level >= 2:
    conditions.append(trend_close_15m > trend_open_15m)
# ... 直到 8h
```

**Fan 扇形确认**
```python
# Fan 幅度增益
conditions.append(fan_magnitude_gain >= buy_min_fan_magnitude_gain)
conditions.append(fan_magnitude > 1)

# Fan 幅度持续上升
for x in range(buy_fan_magnitude_shift_value):
    conditions.append(fan_magnitude.shift(x+1) < fan_magnitude)
```

### 3.2 指标计算

```python
# Heikin Ashi 蜡烛图
heikinashi = qtpylib.heikinashi(dataframe)
dataframe['open'] = heikinashi['open']
dataframe['high'] = heikinashi['high']
dataframe['low'] = heikinashi['low']

# 多时间框架趋势
dataframe['trend_close_5m'] = dataframe['close']
dataframe['trend_close_15m'] = ta.EMA(dataframe['close'], timeperiod=3)
dataframe['trend_close_30m'] = ta.EMA(dataframe['close'], timeperiod=6)
dataframe['trend_close_1h'] = ta.EMA(dataframe['close'], timeperiod=12)
dataframe['trend_close_2h'] = ta.EMA(dataframe['close'], timeperiod=24)
dataframe['trend_close_4h'] = ta.EMA(dataframe['close'], timeperiod=48)
dataframe['trend_close_6h'] = ta.EMA(dataframe['close'], timeperiod=72)
dataframe['trend_close_8h'] = ta.EMA(dataframe['close'], timeperiod=96)

# Fan 扇形
dataframe['fan_magnitude'] = trend_close_1h / trend_close_8h
dataframe['fan_magnitude_gain'] = fan_magnitude / fan_magnitude.shift(1)

# 一目均衡表
ichimoku = ftt.ichimoku(dataframe, conversion_line_period=20, base_line_periods=60, laggin_span=120, displacement=30)
dataframe['senkou_a'] = ichimoku['senkou_span_a']
dataframe['senkou_b'] = ichimoku['senkou_span_b']
dataframe['cloud_green'] = ichimoku['cloud_green']
```

---

## 四、卖出逻辑详解

### 4.1 卖出条件

```python
# 卖出条件
dataframe.loc[
    (
        qtpylib.crossed_below(dataframe['trend_close_5m'], dataframe[sell_trend_indicator])
    ),
    'sell',
] = 1
```

**逻辑解析**：
- **趋势交叉**：5m 趋势下穿卖出趋势指标（默认 2h）
- **默认卖出指标**：trend_close_2h

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **蜡烛图** | Heikin Ashi | - | 平滑蜡烛图 |
| **趋势指标** | EMA | 3/6/12/24/48/72/96 | 多时间框架趋势 |
| **趋势指标** | Ichimoku Cloud | 20/60/120 | 云层过滤 |
| **扇形指标** | Fan Magnitude | 1h/8h | 趋势强度 |

### 5.2 多时间框架趋势

| 时间框架 | EMA 周期 | 用途 |
|---------|---------|------|
| 5m | - | 基础趋势 |
| 15m | 3 | 短期趋势 |
| 30m | 6 | 中短期趋势 |
| 1h | 12 | 中期趋势 |
| 2h | 24 | 中长期趋势 |
| 4h | 48 | 长期趋势 |
| 6h | 72 | 更长趋势 |
| 8h | 96 | 最长趋势 |

### 5.3 Fan 扇形

```python
fan_magnitude = trend_close_1h / trend_close_8h
fan_magnitude_gain = fan_magnitude / fan_magnitude.shift(1)
```

**用途**：
- 衡量 1h 和 8h 趋势的差距
- fan_magnitude > 1：上涨趋势
- fan_magnitude_gain > 1：趋势增强

---

## 六、风险管理特色

### 6.1 宽松硬止损

```python
stoploss = -0.275  # -27.5%
```

**说明**：宽松止损，给予充分波动空间。

### 6.2 追踪止损

```python
trailing_stop = True
```

**作用**：启用追踪止损，保护盈利。

### 6.3 多层趋势过滤

```python
# 8 个级别的趋势确认
if buy_trend_above_senkou_level >= 8:
    # 从 5m 到 8h 都在云层上方
```

**作用**：
- 多层趋势确认，减少假信号
- 只在强趋势中交易

---

## 七、策略优势与局限

### ✅ 优势

1. **多时间框架**：8 个时间框架确认趋势
2. **一目均衡表**：云层过滤趋势
3. **Fan 扇形**：衡量趋势强度
4. **Heikin Ashi**：平滑蜡烛图减少噪音
5. **超参数优化**：支持 Hyperopt 优化关键参数
6. **宽松止损**：-27.5% 止损，给予充分波动空间

### ⚠️ 局限

1. **复杂度极高**：多时间框架 + 一目均衡表，调试困难
2. **无 BTC 关联**：不检测比特币大盘趋势
3. **参数敏感**：超参数优化结果可能过拟合
4. **计算量大**：多 EMA + 一目均衡表增加计算负担
5. **宽松止损**：-27.5% 止损在极端行情下可能造成较大亏损

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **上涨趋势** | 强烈推荐 | 多时间框架 + 云层过滤，完美匹配 |
| **震荡市** | 不推荐 | 趋势策略在震荡中假信号多 |
| **下跌趋势** | 暂停 | 多层趋势过滤会阻止大部分交易 |
| **高波动** | 调整参数 | 可能需要调整止损阈值 |
| **低波动** | 调整 ROI | 降低 ROI 门槛适应小波动 |

---

## 九、适用市场环境详解

ichiV1 是基于"多时间框架 + 一目均衡表"核心哲学的高级趋势跟踪策略。

### 9.1 策略核心逻辑

- **多时间框架**：8 个时间框架确认趋势
- **云层过滤**：只在云层上方交易
- **Fan 扇形**：衡量趋势强度

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★★ | 多时间框架 + 云层过滤，完美匹配 |
| 🔄 宽幅震荡 | ★★☆☆☆ | 趋势策略在震荡中假信号多 |
| 📉 单边暴跌 | ★★★☆☆ | 多层趋势过滤会阻止大部分交易，自动躺平 |
| ⚡️ 极端横盘 | ★★☆☆☆ | 波动太小，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-40 个 | 信号频率适中 |
| **最大持仓数** | 3-6 个 | 控制风险 |
| **仓位模式** | 固定仓位 | 建议固定仓位 |
| **时间框架** | 5m | 强制要求 |

---

## 十、重要提醒：多时间框架的使用

### 10.1 学习成本极高

策略代码约 200 行，需要理解多时间框架、一目均衡表、Fan 扇形等复杂概念。

### 10.2 硬件要求高

多 EMA + 一目均衡表增加计算量：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 2GB | 4GB |
| 40-80 对 | 4GB | 8GB |

### 10.3 多时间框架优势

- **趋势确认**：8 个时间框架确认，减少假信号
- **云层过滤**：只在云层上方交易
- **自动躺平**：趋势向下时自动停止交易

### 10.4 手动交易者建议

手动交易者可参考此策略的多时间框架思路：
- 同时观察多个时间框架趋势
- 使用云层过滤趋势
- 设置宽松止损（如 -25%）

---

## 十一、总结

**ichiV1** 是一个设计精良的高级趋势跟踪策略，它的核心价值在于：

1. **多时间框架**：8 个时间框架确认趋势
2. **一目均衡表**：云层过滤趋势
3. **Fan 扇形**：衡量趋势强度
4. **Heikin Ashi**：平滑蜡烛图减少噪音
5. **超参数优化**：支持 Hyperopt 优化关键参数
6. **宽松止损**：-27.5% 止损，给予充分波动空间

对于量化交易者而言，这是一个优秀的多时间框架学习模板。建议：
- 作为学习多时间框架策略的进阶案例
- 理解一目均衡表的使用方法
- 学习 Fan 扇形的应用
- 注意超参数可能过拟合，实盘前需充分测试

---
