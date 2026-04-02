# CombinedBinHAndClucV7 策略深度解读

> **策略编号**: #22 (465 个策略中的第 22 个)  
> **策略类型**: 布林带 + 多策略组合 V7  
> **时间框架**: 5 分钟 (5m)

---

## 一、策略概览

**CombinedBinHAndClucV7** 是 CombinedBinHAndCluc 系列的第 7 个版本，由 iterativ 开发。策略融合了 BinHV45、ClucMay72018 等多种买入逻辑，并使用了 1 小时信息时间框架来确认趋势。策略特色是使用了自定义止损（custom_stoploss）和确认交易退出（confirm_trade_exit）函数。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 4 种模式组合（BinHV45 + Cluc + RSI + MFI） |
| **卖出条件** | 2 种模式（布林带上轨 + RSI） |
| **保护机制** | 自定义止损 + 确认交易退出 + 追踪止损 |
| **时间框架** | 5 分钟 |
| **依赖库** | TA-Lib, technical, numpy |
| **特殊功能** | 1h 信息时间框架、自定义止损 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.0181    # 立即退出：1.81% 利润
}

# 止损设置
stoploss = -0.99  # -99% 硬止损（ effectively disabled）

# 追踪止损
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01      # 1% 追踪启动
trailing_stop_positive_offset = 0.03  # 3% 偏移触发
```

**设计思路**：
- **低 ROI**：1.81% ROI，追求快速周转
- **几乎无硬止损**：-99% 止损，依赖自定义止损
- **追踪止损**：3% 利润后启动 1% 追踪

### 2.2 自定义止损

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs) -> float:
    # 管理亏损交易，为更好的交易腾出空间
    if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
        return 0.01  # 亏损超过 280 分钟，止损 1%
    return 0.99  # 否则几乎不止损
```

**作用**：
- 亏损超过 280 分钟（约 4.7 小时）后，止损 1%
- 为更好的交易腾出空间
- 避免长期套牢

### 2.3 确认交易退出

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, **kwargs) -> bool:
    if sell_reason == "roi":
        if current_profit > sell_roi_profit_1:
            if last_candle["rsi"] > sell_roi_rsi_1:
                return False  # 阻止退出，让利润奔跑
        # ... 更多条件
    return True
```

**作用**：
- 根据 RSI 阻止过早退出
- 让利润在趋势中奔跑

### 2.4 超参数

```python
# 买入超参数
buy_bb40_bbdelta_close = DecimalParameter(0.005, 0.04, default=0.031, space="buy")
buy_bb40_closedelta_close = DecimalParameter(0.01, 0.03, default=0.021, space="buy")
buy_bb40_tail_bbdelta = DecimalParameter(0.2, 0.4, default=0.264, space="buy")
buy_bb20_close_bblowerband = DecimalParameter(0.8, 1.1, default=0.992, space="buy")
buy_bb20_volume = IntParameter(18, 36, default=29, space="buy")
buy_rsi_diff = DecimalParameter(34.0, 60.0, default=50.48, space="buy")
buy_min_inc = DecimalParameter(0.005, 0.05, default=0.01, space="buy")
buy_rsi_1h = DecimalParameter(40.0, 70.0, default=67.0, space="buy")
buy_rsi = DecimalParameter(30.0, 40.0, default=38.5, space="buy")
buy_mfi = DecimalParameter(36.0, 65.0, default=36.0, space="buy")

# 卖出超参数
sell_rsi_main = DecimalParameter(72.0, 90.0, default=77, space="sell")
```

---

## 三、买入条件详解

### 3.1 买入逻辑（4 种模式）

**模式 1：BinHV45 变体**
```python
(
    (close > ema_200_1h) &
    (ema_50 > ema_200) &
    (ema_50_1h > ema_200_1h) &
    (lower.shift().gt(0)) &
    (bbdelta.gt(close * buy_bb40_bbdelta_close)) &
    (closedelta.gt(close * buy_bb40_closedelta_close)) &
    (tail.lt(bbdelta * buy_bb40_tail_bbdelta)) &
    (close.lt(lower.shift())) &
    (close.le(close.shift()))
)
```

**模式 2：ClucMay72018 变体**
```python
(
    (close > ema_200) &
    (close > ema_200_1h) &
    (close < ema_slow) &
    (close < buy_bb20_close_bblowerband * bb_lowerband) &
    (volume < volume_mean_slow.shift(1) * buy_bb20_volume)
)
```

**模式 3：RSI 差异**
```python
(
    (close < sma_5) &
    (ssl_up_1h > ssl_down_1h) &
    (ema_50 > ema_200) &
    (ema_50_1h > ema_200_1h) &
    (rsi < rsi_1h - buy_rsi_diff)
)
```

**模式 4：RSI + MFI**
```python
(
    (sma_200 > sma_200.shift(20)) &
    (sma_200_1h > sma_200_1h.shift(16)) &
    (rsi_1h > buy_rsi_1h) &
    (rsi < buy_rsi) &
    (mfi < buy_mfi)
)
```

---

## 四、卖出逻辑详解

### 4.1 技术卖出信号

**模式 1：布林带上轨**
```python
(
    (close > bb_upperband) &
    (close.shift(1) > bb_upperband.shift(1)) &
    (close.shift(2) > bb_upperband.shift(2))
)
```

**模式 2：RSI 超买**
```python
(rsi > sell_rsi_main)
```

### 4.2 自定义止损

```python
if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
    return 0.01  # 亏损超过 280 分钟，止损 1%
return 0.99  # 否则几乎不止损
```

### 4.3 确认交易退出

```python
if sell_reason == "roi":
    if current_profit > sell_roi_profit_1:
        if last_candle["rsi"] > sell_roi_rsi_1:
            return False  # 阻止退出
    elif current_profit > sell_roi_profit_2:
        if last_candle["rsi"] > sell_roi_rsi_2:
            return False  # 阻止退出
    elif current_profit > sell_roi_profit_3:
        if last_candle["rsi"] > sell_roi_rsi_3:
            return False  # 阻止退出
return True
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **波动指标** | Bollinger Bands | 40 周期，2 倍标准差 | BinHV45 变体 |
| **波动指标** | Bollinger Bands | 20 周期，2 倍标准差 | Cluc 变体 |
| **趋势指标** | EMA | 50, 200 周期 | 趋势判断 |
| **趋势指标** | SMA | 200 周期 | 趋势判断 |
| **动量指标** | RSI | 14 周期 | 超买超卖 |
| **动量指标** | MFI | 14 周期 | 资金流 |
| **趋势指标** | SSL Channels | 20 周期 | 趋势方向 |

### 5.2 信息时间框架（1h）

策略使用 1 小时信息时间框架：

| 指标 | 用途 |
|------|------|
| ema_50_1h | 1h 中期趋势 |
| ema_200_1h | 1h 长期趋势 |
| sma_200_1h | 1h 长期趋势 |
| rsi_1h | 1h 超买超卖 |
| ssl_down_1h, ssl_up_1h | 1h 趋势方向 |

---

## 六、风险管理特色

### 6.1 自定义止损

```python
if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
    return 0.01
```

**作用**：
- 亏损超过 280 分钟后止损 1%
- 为更好的交易腾出空间
- 避免长期套牢

### 6.2 确认交易退出

```python
if current_profit > sell_roi_profit_1:
    if last_candle["rsi"] > sell_roi_rsi_1:
        return False  # 阻止退出
```

**作用**：
- 根据 RSI 阻止过早退出
- 让利润在趋势中奔跑

### 6.3 追踪止损

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.03
trailing_only_offset_is_reached = True
```

**工作机制**：
1. 利润达到 3% 后启动追踪止损
2. 从最高点回撤 1% 时触发退出

---

## 七、策略优势与局限

### ✅ 优势

1. **多策略组合**：4 种买入模式，覆盖不同场景
2. **信息时间框架**：1h 确认趋势，减少假信号
3. **自定义止损**：管理亏损交易，腾出空间
4. **确认交易退出**：根据 RSI 阻止过早退出
5. **超参数优化**：支持 Hyperopt 优化关键参数
6. **追踪止损**：锁定利润，保护盈利

### ⚠️ 局限

1. **复杂度高**：多策略 + 多指标，调试困难
2. **无 BTC 关联**：不检测比特币大盘趋势
3. **参数敏感**：超参数优化结果可能过拟合
4. **计算量大**：多指标 + 信息时间框架增加计算负担
5. **几乎无硬止损**：-99% 止损依赖自定义止损

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **震荡市** | 默认配置 | 多策略组合适合震荡行情 |
| **上涨趋势** | 默认配置 | 信息时间框架 + 追踪止损表现好 |
| **下跌趋势** | 暂停或轻仓 | 信息时间框架会阻止大部分交易 |
| **高波动** | 调整参数 | 可能需要调整止损阈值 |
| **低波动** | 调整 ROI | 降低 ROI 门槛适应小波动 |

---

## 九、适用市场环境详解

CombinedBinHAndClucV7 是基于"多策略组合 + 信息时间框架"核心哲学的策略。

### 9.1 策略核心逻辑

- **多策略组合**：4 种买入模式，覆盖不同场景
- **信息时间框架**：1h 确认趋势，减少假信号
- **自定义止损**：管理亏损交易
- **确认交易退出**：让利润奔跑

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★★ | 多策略 + 信息时间框架 + 追踪止损，完美匹配 |
| 🔄 宽幅震荡 | ★★★★☆ | 多策略组合适合震荡行情 |
| 📉 单边暴跌 | ★★★☆☆ | 信息时间框架会阻止大部分交易，自动躺平 |
| ⚡️ 极端横盘 | ★★★☆☆ | 波动太小，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-60 个 | 推荐 20-60 个交易对 |
| **最大持仓数** | 4-6 个 | 推荐 4-6 个开放交易 |
| **仓位模式** | 无限仓位 | 推荐 unlimited stake |
| **时间框架** | 5m | 强制要求 |

---

## 十、重要提醒：信息时间框架的使用

### 10.1 学习成本高

策略代码约 300 行，需要理解多策略组合、信息时间框架、自定义止损等概念。

### 10.2 硬件要求中等

多指标 + 信息时间框架增加计算量：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 1GB | 2GB |
| 40-80 对 | 2GB | 4GB |

### 10.3 信息时间框架优势

- **趋势确认**：1h 趋势比 5m 可靠
- **减少假信号**：只在 1h 趋势向上时交易
- **自动躺平**：1h 趋势向下时自动停止交易

### 10.4 手动交易者建议

手动交易者可参考此策略的多策略思路：
- 同时观察 5m 和 1h 趋势
- 使用多策略组合覆盖不同场景
- 设置自定义止损管理亏损交易

---

## 十一、总结

**CombinedBinHAndClucV7** 是一个设计精良的多策略组合策略，它的核心价值在于：

1. **多策略组合**：4 种买入模式，覆盖不同场景
2. **信息时间框架**：1h 确认趋势，减少假信号
3. **自定义止损**：管理亏损交易，腾出空间
4. **确认交易退出**：根据 RSI 阻止过早退出
5. **超参数优化**：支持 Hyperopt 优化关键参数
6. **追踪止损**：锁定利润，保护盈利

对于量化交易者而言，这是一个优秀的多策略学习模板。建议：
- 作为学习多策略组合的进阶案例
- 理解信息时间框架的使用方法
- 学习自定义止损和确认交易退出
- 注意超参数可能过拟合，实盘前需充分测试

---
