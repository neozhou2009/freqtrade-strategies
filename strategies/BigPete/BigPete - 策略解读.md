# BigPete 策略深度解读

## 一、策略概览

BigPete 是基于 BigZ04 改进的量化交易策略，由 Perkmeister 开发。该策略在 BigZ04 的基础上增加了**自定义跟踪止损系统**，实现了更灵活的风险回报管理。其核心设计理念是**在控制最大回撤的前提下，追求趋势行情中的更大利润**。

### 核心特征表

| 特征项 | 配置值 |
|--------|--------|
| 时间框架 | 5分钟（5m） |
| 信息时间框架 | 1小时（1h） |
| 止盈（ROI） | 0-30分钟：10%，30-60分钟：5%，60分钟以上：2% |
| 止损 | -0.99（禁用默认止损，使用自定义止损） |
| 跟踪止损 | 启用，自适应跟踪止损系统 |
| 买入条件数 | 13个独立条件 |
| 适合交易对数 | 2-4个（建议） |
| 特色 | 动态跟踪止损 + 分层止盈 |

---

## 二、策略配置解析

### 2.1 基础配置

```python
timeframe = "5m"
inf_1h = "1h"
minimal_roi = {
    "0": 0.10,    # 持仓立即获利10%
    "30": 0.05,   # 30分钟后获利5%
    "60": 0.02    # 60分钟后获利2%
}
stoploss = -0.99  # 禁用默认止损
trailing_stop = True
trailing_stop_positive = 0.003
trailing_stop_positive_offset = 0.0187
```

### 2.2 跟踪止损参数（核心特色）

```python
# 硬止损阈值
pHSL = -0.08  # 亏损超过8%强制止损

# 利润阈值1（触发第一档跟踪）
pPF_1 = 0.016  # 1.6%利润触发
pSL_1 = 0.011  # 对应止损1.1%

# 利润阈值2（触发第二档跟踪）
pPF_2 = 0.080  # 8%利润触发
pSL_2 = 0.040  # 对应止损4%

# 动态止损公式
# 利润 > 8%：sl_profit = 4% + (当前利润 - 8%)
# 利润 1.6%-8%：sl_profit = 1.1% + (当前利润 - 1.6%) × 比例
# 利润 < 1.6%：sl_profit = -8%（硬止损）
```

### 2.3 关键参数

```python
# 成交量参数
buy_volume_pump_1 = 0.1    # 成交量较48周期均值的比例
buy_volume_drop_1 = 5.4    # 成交量萎缩倍数

# RSI参数
buy_rsi_1h_0 = 81.7        # 高位RSI（条件0）
buy_rsi_1h_1 = 14.2        # 低位RSI（条件1-4）
buy_rsi_0 = 11.2           # 5分钟RSI
buy_rsi_1 = 15.7
buy_rsi_2 = 11.3

# MACD参数
buy_macd_1 = 0.05
buy_macd_2 = 0.03
```

---

## 三、买入条件详解

BigPete 包含 **13个独立买入条件**：

### 3.1 条件0：高位RSI + 价格下跌

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["rsi"] < 11.2) &
((dataframe["close"] * 1.029 < dataframe["open"].shift(3)) | 
 (dataframe["close"] * 1.029 < dataframe["open"].shift(2)) |
 (dataframe["close"] * 1.029 < dataframe["open"].shift(1))) &
(dataframe["rsi_1h"] < 81.7)
```

**逻辑**：价格在EMA200之上但RSI极低（11.2），说明虽然长期多头但短期超卖。连续3天内有大幅下跌。

### 3.2 条件1：布林带下轨 + 阴线

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["close"] < dataframe["bb_lowerband"] * 0.999) &
(dataframe["rsi_1h"] < 67.8) &
(dataframe["open"] > dataframe["close"])
```

**逻辑**：价格在布林带下轨附近，收阴线，1小时RSI适中。

### 3.3 条件2：深度下轨

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] < dataframe["bb_lowerband"] * 1.01)
```

**逻辑**：更宽松的下轨条件，接近布林带即可。

### 3.4 条件3：1小时EMA200之上 + RSI超卖

```python
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["close"] < dataframe["bb_lowerband"]) &
(dataframe["rsi"] < 35.6)
```

### 3.5 条件4：1小时RSI极低

```python
(dataframe["rsi_1h"] < 16.5) &
(dataframe["close"] < dataframe["bb_lowerband"])
```

### 3.6 条件5：MACD金叉 + 布林带下轨

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["ema_26"] > dataframe["ema_12"]) &
((dataframe["ema_26"] - dataframe["ema_12"]) > (dataframe["open"] * 0.05)) &
(dataframe["close"] < dataframe["bb_lowerband"])
```

### 3.7 条件6-7：MACD不同参数组合

类似条件5，但使用不同的RSI和MACD参数阈值。

### 3.8 条件8-9：双RSI超卖

```python
(dataframe["rsi_1h"] < 阈值) &
(dataframe["rsi"] < 阈值)
```

### 3.9 条件10：1小时超卖 + MACD反转

```python
(dataframe["rsi_1h"] < 31.3) &
(dataframe["close_1h"] < dataframe["bb_lowerband_1h"]) &
(dataframe["hist"] > 0) &
(dataframe["hist"].shift(2) < 0) &
(dataframe["rsi"] < 40.5)
```

### 3.10 条件11：成交量窄幅震荡

```python
# 连续10根K线波幅 < 1%
((dataframe["high"] - dataframe["low"]) < dataframe["open"] / 100)
```

### 3.11 条件12：假突破形态

```python
(dataframe["close"] < dataframe["bb_lowerband"] * 0.993) &
(dataframe["low"] < dataframe["bb_lowerband"] * 0.985) &
(dataframe["close"].shift() > dataframe["bb_lowerband"])
```

---

## 四、卖出逻辑详解

### 4.1 自定义跟踪止损（核心）

BigPete 的最大特色是其**自适应跟踪止损系统**：

```python
def custom_stoploss(current_profit):
    HSL = -0.08  # 硬止损-8%
    PF_1 = 0.016  # 1.6%利润阈值
    SL_1 = 0.011  # 1.1%对应止损
    PF_2 = 0.080  # 8%利润阈值
    SL_2 = 0.040  # 4%对应止损
    
    if current_profit > PF_2:
        # 利润>8%：止损线上移，锁定更多利润
        sl_profit = SL_2 + (current_profit - PF_2)
    elif current_profit > PF_1:
        # 利润1.6%-8%：线性插值
        sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
    else:
        # 利润<1.6%：使用硬止损-8%
        sl_profit = HSL
    
    return stoploss_from_open(sl_profit, current_profit)
```

**逻辑解读**：
- 利润<1.6%：最多亏8%（硬止损保护）
- 利润1.6%-8%：止损线上移，1.1%→4%
- 利润>8%：止损线跟随利润上涨，锁定大部分利润

### 4.2 利润保护机制图解

```
利润:   -8%   0%    1.6%   4%    8%    12%   16%   20%
        |-----|-----|------|-----|-----|-----|-----|
止损线: -8%  -8%   -8%   -1.1% -4%   -8%  -12%  -16%
               (硬止损)  (动态上升)
```

### 4.3 ROI时间止盈

```python
minimal_roi = {
    "0": 0.10,    # 持仓即赚10%！
    "30": 0.05,   # 30分钟后赚5%
    "60": 0.02    # 60分钟后赚2%
}
```

**注意**：由于使用跟踪止损，ROI主要在早期起作用。

---

## 五、技术指标体系

### 5.1 5分钟周期指标

| 指标名称 | 参数 | 用途 |
|----------|------|------|
| EMA200 | 200 | 长期趋势判断 |
| EMA12/26 | 12,26 | MACD计算 |
| SMA5 | 5 | 短期趋势 |
| RSI | 14 | 动量 |
| Bollinger Bands | 20,2 | 超买超卖 |
| ATR | 14 | 波动率 |

### 5.2 1小时周期指标

| 指标名称 | 参数 | 用途 |
|----------|------|------|
| SMA50 | 50 | 中期趋势 |
| SMA200 | 200 | 长期趋势 |
| RSI | 14 | 1小时动量 |
| Bollinger Bands | 20,2 | 超买超卖 |

---

## 六、风险管理特色

### 6.1 自适应止损系统

BigPete 的核心创新是**根据利润动态调整止损线**：

1. **亏损阶段**（利润<1.6%）：
   - 硬止损-8%
   - 允许一定浮亏空间

2. **初步盈利阶段**（利润1.6%-8%）：
   - 止损线上移至-1.1%至-4%
   - 保护已有利润

3. **大幅盈利阶段**（利润>8%）：
   - 止损线跟随上涨
   - 永远锁定至少4%的利润

### 6.2 与BigZ04的区别

| 特性 | BigZ04 | BigPete |
|------|--------|---------|
| 止损类型 | 固定时间止损 | 自适应跟踪止损 |
| 硬止损 | -10% | -8% |
| 跟踪止损 | 无 | 有 |
| 利润目标 | 阶梯ROI | 10%首目标 |

---

## 七、策略优势与局限

### 7.1 优势

1. **灵活止损**：根据利润自动调整，风险可控
2. **趋势跟踪**：能抓住大趋势的更多利润
3. **多条件覆盖**：13个条件覆盖多种形态
4. **双重验证**：5分钟+1小时时间框架

### 7.2 局限

1. **参数复杂**：多个阈值参数优化困难
2. **高目标**：10%首目标可能导致部分交易失败
3. **波动敏感**：跟踪止损可能被正常波动触发

---

## 八、适用场景建议

### 8.1 推荐场景

- **强势趋势中的回调**
- **高波动市场**
- **主要加密货币交易对**

### 8.2 不推荐场景

- **低波动横盘**
- **剧烈波动的垃圾币**
- **需要快速交易的场景**

---

## 九、适用市场环境详解

### 9.1 理想环境

1. **清晰趋势**：单边上涨或下跌后的回调
2. **正常波动**：日波动5-15%
3. **高流动性**：主流币种

### 9.2 警告环境

- ⚠️ 横盘震荡（高交易频率，低胜率）
- ⚠️ 暴跌行情（硬止损会触发）
- ⚠️ 极端波动（跟踪止损过窄）

---

## 十、重要提醒：复杂性的代价

### 10.1 跟踪止损的代价

虽然跟踪止损能保护利润，但它也有代价：

1. **正常回撤触发**：趋势中的正常波动可能导致止损
2. **参数敏感性**：PF_1、PF_2等参数需要精细调整
3. **复杂性增加**：难以理解实际盈亏来源

### 10.2 建议

1. **先观察**：使用默认值运行2周
2. **记录交易**：分析哪些止损是"正确"的
3. **谨慎调整**：每次只改一个参数

---

## 十一、总结

BigPete 是 **BigZ04的增强版**，通过自适应跟踪止损系统实现更智能的风险管理：

- ✅ 13个买入条件，覆盖多种形态
- ✅ 跟踪止损，保护利润
- ✅ 8%硬止损，控制最大亏损
- ⚠️ 参数复杂，需要时间理解
- ⚠️ 10%首目标较高

**适合**：有一定经验的交易者，追求稳健的利润增长。

---

*本文档基于 BigPete.py 代码自动生成*