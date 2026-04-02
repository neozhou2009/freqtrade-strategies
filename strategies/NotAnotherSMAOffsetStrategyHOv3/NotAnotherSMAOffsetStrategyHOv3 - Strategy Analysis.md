# NotAnotherSMAOffsetStrategyHOv3 Strategy Analysis

## 1. Strategy Overview and Design Philosophy

### 1.1 Strategy Background

NotAnotherSMAOffsetStrategyHOv3 is a quantitative trading strategy based on SMA Offset technology, built for the Freqtrade framework. The core idea: when prices significantly deviate from their average, trading opportunities emerge. The name's "NotAnother" signals this breaks from conventional MA strategies — a carefully optimized version.

The design philosophy: **"Seek opportunities in panic, lock profits in greed."** It identifies extreme price offset positions from MAs, combined with EWO for market sentiment, buying when markets are overly pessimistic and selling when sentiment normalizes or becomes overly optimistic.

### 1.2 Strategy Positioning

Medium-short term trading on 5-minute timeframe as primary chart, with 1-hour auxiliary data for reliability through multi-timeframe analysis.

### 1.3 Core Innovations

1. **Dual offset mechanism**: Buy offset (low_offset) and sell offset (high_offset) asymmetrically — aggressive on dips, conservative on rises
2. **Triple entry logic**: Three buy conditions (ewo1, ewo2, ewolow) for different sentiment states
3. **Dynamic risk management**: Fixed stop-loss + trailing stop + ROI goals

---

## 2. Technical Indicator System

### 2.1 MA Family

- **EMA** for buy/sell: Periods `base_nb_candles_buy` (default 8) and `base_nb_candles_sell` (default 16)
- **EMA_100**: Long-term trend reference
- **SMA_9**: Short-term price trend
- **HMA_50**: Mid-term trend, low lag

### 2.2 Elliott Wave Oscillator (EWO)

```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(df, timeperiod=ema_length)
    ema2 = ta.EMA(df, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / df['low'] * 100
    return emadif
```

Strategy uses slow parameters: fast=50, slow=200 to capture longer-term momentum.

### 2.3 RSI Multi-Period

- RSI(14): Standard overbought/oversold
- RSI(4): Short-term fast response
- RSI(20): Mid-term trend confirmation

---

## 3. Entry Signal Details

### 3.1 Signal ewo1: Strong Momentum Pullback

```python
1. rsi_fast < 35
2. close < ma_buy * low_offset (default 0.986)
3. EWO > ewo_high (default 4.179)
4. rsi < rsi_buy (default 58)
5. volume > 0
6. close < ma_sell * high_offset
```

**Interpretation**: EWO > 4.179 shows strong uptrend; price pullback + RSI_fast < 35 = temporary dip, buy opportunity.

### 3.2 Signal ewo2: Deep Pullback

```python
1. rsi_fast < 35
2. close < ma_buy * low_offset_2 (default 0.944)
3. EWO > ewo_high_2 (default -2.609)
4. rsi < rsi_buy
5. volume > 0
6. close < ma_sell * high_offset
7. rsi < 25
```

**Interpretation**: Requires deeper discount (5.6% below MA), RSI < 25 = extreme oversold, potential rebound.

### 3.3 Signal ewolow: Extreme Panic

```python
1. rsi_fast < 35
2. close < ma_buy * low_offset
3. EWO < ewo_low (default -16.917)
4. volume > 0
5. close < ma_sell * high_offset
```

**Interpretation**: EWO < -16.917 = extreme market pessimism, potential reversal.

### 3.4 Parameter Summary

| Parameter | Default | Meaning |
|-----------|---------|---------|
| low_offset | 0.986 | Buy when price < EMA's 98.6% |
| low_offset_2 | 0.944 | Deep buy when price < EMA's 94.4% |
| high_offset | 1.054 | Sell when price > EMA's 105.4% |
| high_offset_2 | 1.018 | Sell when price > EMA's 101.8% |

---

## 4. Exit Signal Details

### 4.1 Exit Condition 1: Trend Reversal

```python
1. close > sma_9
2. close > ma_sell * high_offset_2
3. rsi > 50
4. volume > 0
5. rsi_fast > rsi_slow
```

### 4.2 Exit Condition 2: Trend Breakdown

```python
1. close < hma_50
2. close > ma_sell * high_offset
3. volume > 0
4. rsi_fast > rsi_slow
```

### 4.3 Exit Confirmation

```python
if (HMA_50 * 1.149 > EMA_100) and (close < EMA_100 * 0.951):
    return False  # Cancel exit
```

---

## 5. Risk Management

### 5.1 Stop-Loss

- Fixed: **-30%** (slightly tighter than v1/v2)
- Trailing: 0.5% distance, activates at 2.5% profit

### 5.2 ROI

```python
minimal_roi = {
    "0": 0.10,   # 10%
    "30": 0.05,  # 5%
    "60": 0.02   # 2%
}
```

### 5.3 Slippage Protection

```python
'max_slippage': -0.02  # 2%
'retries': 3
```

---

## 6. Parameter Optimization

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 8 | 2-20 |
| low_offset | 0.986 | 0.9-0.99 |
| low_offset_2 | 0.944 | 0.9-0.99 |
| ewo_high | 4.179 | 2.0-12.0 |
| ewo_low | -16.917 | -20.0--8.0 |
| ewo_high_2 | -2.609 | -6.0-12.0 |
| rsi_buy | 58 | 30-70 |

---

## 7. Strategy Pros & Cons

### 7.1 Pros

- Trend following + mean reversion combination
- Three buy signals cover different states
- Multi-layer risk control
- High parameter flexibility

### 7.2 Cons

- Trend market risk: may exit too early in strong rallies
- Ranging market risk: frequent false signals
- Parameter overfitting risk
- Timeframe limitations

---

## 8. Summary

NotAnotherSMAOffsetStrategyHOv3 combines price offset + momentum indicators for a precise trading system. Suitable for experienced Freqtrade users who understand technical indicators and are willing to optimize parameters. Remember: backtesting ≠ future performance.

*Document for learning and research only. Crypto trading involves risk.*
