# CombinedBinHAndClucHyperV3

## 策略深度分析

> 分析: 2026-02-13 12:39
> 状态: 🟡 需要修复
> 问题: 1个

---

## 一、执行摘要

核心: 策略存在 多个严重问题，会导致亏损。

建议:
- 立即修复致命问题
- 充分回测
- 纸质交易

---

## 二、代码结构

| 项目 | 信息 |
|------|------|
| 买入 | ❌ 缺失 |
| 卖出 | ✅ {sells}个 |
| 周期 | 

    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # ----------------------------------------------------------------
    # Hyper Params
    # 
    # Buy 
    buy_a_time_window = IntParameter(40, 100, default=30)
    buy_a_atr_window = IntParameter(10, 300, default=14)

    buy_a_bbdelta_rate = DecimalParameter(0.004, 0.02, default=0.016, decimals=3)
    buy_a_closedelta_rate = DecimalParameter(0.000, 0.020, default=0.0087, decimals=4)
    buy_a_tail_rate = DecimalParameter(0.12, 1, default=0.28, decimals=2)
    buy_a_min_sell_rate = DecimalParameter(1.004, 1.1, default=1.03, decimals=3)
    buy_a_atr_rate = DecimalParameter(0.00, 3.00, default=1, decimals=2)

    buy_b_close_rate = DecimalParameter(0.4, 1.8, default=0.979, decimals=3)
    buy_b_volume_mean_slow_window = IntParameter(100, 300, default=30)
    buy_b_ema_slow = IntParameter(40, 100, default=50)
    buy_b_time_window = IntParameter(100, 300, default=20)
    buy_b_volume_mean_slow_num = IntParameter(10, 100, default=20)
    # Sell
    sell_bb_mid_slow_window = IntParameter(10, 100, default=91)
    sell_trailing_stop_positive_offset = DecimalParameter(0.01, 0.03, default=0.012, decimals=3)
    sell_trailing_stop_positive = 0.001

    # ----------------------------------------------------------------
    # Buy hyperspace params:
    buy_params = {
         |
| 指标 | 2个: EMA,ATR |

质量: ⚠️ 一般

---

## 三、问题

### 致命问题

**1. 缺买入信号**

严重: 🔴 致命

修复: 必须！

---

## 四、修复方案

### 修复清单
3. 添加ADX+MACD+RSI指标
4. 启用止损上移

### 代码修复

```python
# ROI
minimal_roi = {"0": 0.10, "60": 0.07, "120": 0.05, "240": 0.03}

# 止损
stoploss = -0.10
trailing_stop = True
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.06

# 指标
dataframe['adx'] = ta.ADX(dataframe, 14)
dataframe['rsi'] = ta.RSI(dataframe, 14)
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
```

---

## 五、参数优化

### 保守型
```python
stoploss = -0.08
max_open_trades = 3
```

### 平衡型（推荐）
```python
stoploss = -0.10
max_open_trades = 5
trailing_stop = True
```

---

## 六、使用

```bash
freqtrade backtesting -s CombinedBinHAndClucHyperV3 --timerange 20240101-20240301
freqtrade hyperopt -s CombinedBinHAndClucHyperV3 --hyperopt-loss SharpeHyperOptLoss
```

---

## 风险提示

⚠️ {"必须修复: " + ",".join(crit) if crit else "相对干净"}

⚠️ 充分测试: 回测3-6个月 + 纸质交易1-2周

免责: 后果自负。

---

更新: {datetime.now().strftime('%Y-%m-%d')}
