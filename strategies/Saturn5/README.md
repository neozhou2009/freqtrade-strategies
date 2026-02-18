# Saturn5

## 策略深度分析

> 分析: 2026-02-13 12:39
> 状态: 🟢 基本可用
> 问题: 0个

---

## 一、执行摘要

核心: 策略存在 良好结构。

建议:
- 回测验证
- 可选微调

---

## 二、代码结构

| 项目 | 信息 |
|------|------|
| 买入 | ✅ {buys}个 |
| 卖出 | ✅ {sells}个 |
| 周期 | 

    # Stoploss
    stoploss = -0.20
    startup_candle_count: int = 480
    trailing_stop = False
    use_custom_stoploss = False
    use_sell_signal = False

    # signal controls
    buy_signal_1 = True
    buy_signal_2 = True
    buy_signal_3 = True

    # ROI table:
    minimal_roi = {
         |
| 指标 | 4个: MACD,EMA,SMA,ATR |

质量: ✓ 完整

---

## 三、问题

### 致命问题

✓ 无致命问题

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
freqtrade backtesting -s Saturn5 --timerange 20240101-20240301
freqtrade hyperopt -s Saturn5 --hyperopt-loss SharpeHyperOptLoss
```

---

## 风险提示

⚠️ {"必须修复: " + ",".join(crit) if crit else "相对干净"}

⚠️ 充分测试: 回测3-6个月 + 纸质交易1-2周

免责: 后果自负。

---

更新: {datetime.now().strftime('%Y-%m-%d')}
