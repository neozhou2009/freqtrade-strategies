# Inverse 策略深度解读

> **策略编号**: #28 (465 个策略中的第 28 个)  
> **策略类型**: 反向 Fisher RSI 趋势跟踪  
> **时间框架**: 1 小时 (1h)

---

## 一、策略概览

**Inverse** 是一个基于反向 Fisher RSI 的趋势跟踪策略。策略使用 Fisher RSI 的逆变换来捕捉趋势反转点，并结合 4 小时信息时间框架来确认趋势。策略特色是使用了超参数优化来确定最佳买卖阈值。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 多条件组合（Fisher RSI + SSL + EMA） |
| **卖出条件** | 多条件组合（Fisher RSI） |
| **保护机制** | 硬止损 + 追踪止损 + 确认交易退出 |
| **时间框架** | 1 小时 |
| **依赖库** | TA-Lib, technical, numpy |
| **特殊功能** | 4h 信息时间框架、Fisher RSI 逆变换 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.10,    # 立即退出：10% 利润
    "30": 0.05,   # 30 分钟后：5% 利润
    "60": 0.02,   # 60 分钟后：2% 利润
}

# 止损设置
stoploss = -0.2  # -20% 硬止损

# 追踪止损
trailing_stop = True
trailing_stop_positive = 0.078       # 7.8% 追踪启动
trailing_stop_positive_offset = 0.174  # 17.4% 偏移触发
trailing_only_offset_is_reached = False
```

**设计思路**：
- **多级 ROI**：3 级递减 ROI，持仓时间越长退出门槛越低
- **宽松止损**：-20% 硬止损，给予充分波动空间
- **追踪止损**：17.4% 利润后启动 7.8% 追踪

### 2.2 超参数

```python
# 买入超参数
buy_fisher_length = IntParameter(low=13, high=55, default=31, space="buy")
buy_fisher_cci_1 = DecimalParameter(low=-0.6, high=-0.3, default=-0.42, space="buy")
buy_fisher_cci_2 = DecimalParameter(low=0.3, high=0.6, default=0.41, space="buy")

# 卖出超参数
sell_fisher_cci_1 = DecimalParameter(low=0.3, high=0.6, default=0.42, space="sell")
sell_fisher_cci_2 = DecimalParameter(low=-0.6, high=-0.3, default=-0.34, space="sell")
```

### 2.3 订单类型配置

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

---

## 三、买入条件详解

### 3.1 买入逻辑

```python
# 买入条件
dataframe.loc[
    (
        (
            (qtpylib.crossed_above(dataframe[f"fisher_cci_{buy_fisher_length}"], buy_fisher_cci_1)) |
            (
                (qtpylib.crossed_below(dataframe[f"fisher_cci_{buy_fisher_length}"], buy_fisher_cci_2).rolling(8).max() == 1) &
                (qtpylib.crossed_above(dataframe[f"fisher_cci_{buy_fisher_length}"], buy_fisher_cci_2))
            )
        ) &
        (ssl_up_4h > ssl_down_4h) &           # 4h SSL 向上
        (ema_50 > ema_200) &                   # 50EMA > 200EMA
        (ema_50_4h > ema_100_4h) &             # 4h 50EMA > 100EMA
        (ema_50_4h > ema_200_4h) &             # 4h 50EMA > 200EMA
        (volume > 0)                            # 成交量 > 0
    ),
    "buy",
] = 1
```

**逻辑解析**：
- **Fisher CCI 交叉**：Fisher CCI 上穿阈值 1 或 下穿阈值 2 后反弹
- **4h SSL 确认**：4 小时 SSL 通道向上
- **EMA 多头排列**：50EMA > 200EMA（1h 和 4h）
- **成交量过滤**：排除零成交量

### 3.2 指标计算

```python
# Fisher CCI
for cci_length in self.buy_fisher_length.range:
    dataframe[f"cci"] = ta.CCI(dataframe, timeperiod=cci_length)
    cci = 0.1 * (dataframe[f"cci"] / 4)
    wmacci = ta.WMA(cci, timeperiod=9)
    dataframe[f"fisher_cci_{cci_length}"] = (numpy.exp(2 * wmacci) - 1) / (numpy.exp(2 * wmacci) + 1)

# EMA
dataframe["ema_50"] = ta.EMA(dataframe, timeperiod=50)
dataframe["ema_200"] = ta.EMA(dataframe, timeperiod=200)

# 4h 信息时间框架
informative_p = self.dp.get_pair_dataframe(pair=metadata["pair"], timeframe=self.info_timeframe)
informative_p["ema_50"] = ta.EMA(informative_p, timeperiod=50)
informative_p["ema_100"] = ta.EMA(informative_p, timeperiod=100)
informative_p["ema_200"] = ta.EMA(informative_p, timeperiod=200)

# SSL Channels
ssl_down, ssl_up = self.SSLChannels(informative_p, 20)
```

---

## 四、卖出逻辑详解

### 4.1 卖出条件

```python
# 卖出条件
dataframe.loc[
    (
        (
            (qtpylib.crossed_below(dataframe[f"fisher_cci_{buy_fisher_length}"], sell_fisher_cci_1)) |
            (qtpylib.crossed_below(dataframe[f"fisher_cci_{buy_fisher_length}"], sell_fisher_cci_2))
        ) &
        (volume > 0)
    ),
    "sell",
] = 1
```

**逻辑解析**：
- **Fisher CCI 下穿**：Fisher CCI 下穿阈值 1 或 阈值 2
- **成交量确认**：成交量大于 0

### 4.2 确认交易退出

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, current_time, **kwargs) -> bool:
    if sell_reason in ["sell_signal"]:
        if last_candle["di_up"] and (last_candle["adx"] > previous_candle_1["adx"]):
            return False  # 阻止退出
    return True
```

**作用**：
- 根据 ADX 和 DI 阻止过早退出
- 让利润在趋势中奔跑

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **动量指标** | Fisher CCI | 13-55 周期（可优化） | 反向 Fisher CCI |
| **趋势指标** | EMA | 50/200 周期 | 趋势判断 |
| **趋势指标** | SSL Channels | 20 周期 | 趋势方向（4h） |
| **动量指标** | ADX | 3 周期 | 趋势强度 |
| **动量指标** | DI | 3 周期 | 方向指标 |

### 5.2 信息时间框架（4h）

策略使用 4 小时信息时间框架：

| 指标 | 用途 |
|------|------|
| ema_50_4h | 4h 中期趋势 |
| ema_100_4h | 4h 中长期趋势 |
| ema_200_4h | 4h 长期趋势 |
| ssl_down_4h, ssl_up_4h | 4h 趋势方向 |

---

## 六、风险管理特色

### 6.1 宽松硬止损

```python
stoploss = -0.2  # -20%
```

**说明**：宽松止损，给予充分波动空间。

### 6.2 追踪止损

```python
trailing_stop = True
trailing_stop_positive = 0.078
trailing_stop_positive_offset = 0.174
trailing_only_offset_is_reached = False
```

**工作机制**：
1. 利润达到 17.4% 后启动追踪止损
2. 从最高点回撤 7.8% 时触发退出
3. 不需要先达到 offset 才启动

### 6.3 确认交易退出

```python
if last_candle["di_up"] and (last_candle["adx"] > previous_candle_1["adx"]):
    return False  # 阻止退出
```

**作用**：
- 根据 ADX 和 DI 阻止过早退出
- 让利润在趋势中奔跑

---

## 七、策略优势与局限

### ✅ 优势

1. **Fisher RSI 逆变换**：捕捉趋势反转点
2. **多时间框架**：1h + 4h 确认趋势
3. **确认交易退出**：根据 ADX/DI 阻止过早退出
4. **超参数优化**：支持 Hyperopt 优化关键参数
5. **追踪止损**：锁定利润，保护盈利
6. **宽松止损**：-20% 止损，给予充分波动空间

### ⚠️ 局限

1. **复杂度高**：Fisher RSI + 多时间框架，调试困难
2. **无 BTC 关联**：不检测比特币大盘趋势
3. **参数敏感**：超参数优化结果可能过拟合
4. **计算量大**：多指标 + 信息时间框架增加计算负担
5. **1 小时框架**：信号频率较低

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **上涨趋势** | 强烈推荐 | 多时间框架 + 追踪止损，完美匹配 |
| **震荡市** | 推荐 | Fisher RSI 适合震荡行情 |
| **下跌趋势** | 暂停或轻仓 | 多时间框架会阻止大部分交易 |
| **高波动** | 调整参数 | 可能需要调整止损阈值 |
| **低波动** | 调整 ROI | 降低 ROI 门槛适应小波动 |

---

## 九、适用市场环境详解

Inverse 是基于"Fisher RSI 逆变换 + 多时间框架确认"核心哲学的趋势跟踪策略。

### 9.1 策略核心逻辑

- **Fisher RSI 逆变换**：捕捉趋势反转点
- **多时间框架**：1h + 4h 确认趋势
- **确认退出**：根据 ADX/DI 阻止过早退出

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★★ | 多时间框架 + 追踪止损，完美匹配 |
| 🔄 宽幅震荡 | ★★★★☆ | Fisher RSI 适合震荡行情 |
| 📉 单边暴跌 | ★★★☆☆ | 多时间框架会阻止大部分交易，自动躺平 |
| ⚡️ 极端横盘 | ★★★☆☆ | 波动太小，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-40 个 | 信号频率适中 |
| **最大持仓数** | 3-6 个 | 控制风险 |
| **仓位模式** | 固定仓位 | 建议固定仓位 |
| **时间框架** | 1h | 强制要求 |

---

## 十、重要提醒：Fisher RSI 逆变换的使用

### 10.1 学习成本高

策略代码约 200 行，需要理解 Fisher RSI 逆变换、多时间框架等概念。

### 10.2 硬件要求中等

多指标 + 信息时间框架增加计算量：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 1GB | 2GB |
| 40-80 对 | 2GB | 4GB |

### 10.3 Fisher RSI 逆变换优势

- **捕捉反转点**：Fisher RSI 逆变换更敏感
- **减少假信号**：多时间框架确认
- **灵活调整**：可通过 Hyperopt 优化阈值

### 10.4 手动交易者建议

手动交易者可参考此策略的 Fisher RSI 思路：
- 使用 Fisher RSI 逆变换捕捉反转点
- 同时观察 1h 和 4h 趋势
- 设置宽松止损（如 -20%）

---

## 十一、总结

**Inverse** 是一个设计精良的 Fisher RSI 趋势跟踪策略，它的核心价值在于：

1. **Fisher RSI 逆变换**：捕捉趋势反转点
2. **多时间框架**：1h + 4h 确认趋势
3. **确认交易退出**：根据 ADX/DI 阻止过早退出
4. **超参数优化**：支持 Hyperopt 优化关键参数
5. **追踪止损**：锁定利润，保护盈利
6. **宽松止损**：-20% 止损，给予充分波动空间

对于量化交易者而言，这是一个优秀的 Fisher RSI 学习模板。建议：
- 作为学习 Fisher RSI 逆变换的进阶案例
- 理解多时间框架的使用方法
- 学习确认交易退出的应用
- 注意超参数可能过拟合，实盘前需充分测试

---
