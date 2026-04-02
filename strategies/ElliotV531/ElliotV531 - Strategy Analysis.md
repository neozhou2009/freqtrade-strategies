# ElliotV531 - Strategy Analysis

## I. Strategy Overview

### 1.1 Strategy Background and Positioning

ElliotV531 is a quantitative trading strategy developed based on Elliott Wave Theory, specifically designed for the cryptocurrency market. The strategy combines trend-following and momentum reversal trading philosophies, using the Elliott Wave Oscillator (EWO) to capture market wave rhythms and the moving average system to identify value zones, achieving precise entry timing.

The "V531" in the strategy name suggests a mature version that has undergone multiple iterations and has been fully validated in live trading. Its design embodies the trading wisdom of "follow the trend, counter-trend entry" — finding low-buy opportunities during pullbacks in uptrends and capturing rebound opportunities in oversold areas of downtrends.

### 1.2 Core Trading Philosophy

The core philosophy operates on three levels:

**Wave Identification**: Uses EWO to identify the wave stage the market is in. EWO standardizes the difference between short-term and long-term moving averages, effectively identifying the degree of price deviation from the long-term trend.

**Mean Reversion**: Uses the EMA moving average system as a value anchor point. Price deviation from EMA reflects the degree of market overreaction.

**Momentum Confirmation**: Introduces RSI as an auxiliary confirmation tool, forming multi-dimensional entry signal confirmation.

### 1.3 Applicable Scenarios

ElliotV531 is best suited for:
- Pullback phases in trending markets
- Boundary trading in ranging markets
- Trading pairs with moderate volatility

The strategy operates on a 5-minute timeframe, suitable for short-term and intraday traders. The 30-minute informative timeframe provides higher-level trend judgment.

---

## II. Technical Indicator System

### 2.1 EWO

```
EWO = (EMA(5) - EMA(35)) / Close × 100
```

EWO uses:
- Fast EMA: 50-period
- Slow EMA: 200-period
- ewo_high default: 2.337
- ewo_low default: -15.87

### 2.2 EMA System

- **Buy EMA**: Default 11-period, offset 0.979
- **Sell EMA**: Default 17-period, offset 0.997

### 2.3 RSI

- Period: 14
- Buy threshold: 55

### 2.4 Hull Moving Average (HMA)

- Period: 50
- Used with EMA(100) for exit confirmation

---

## III. Entry Signal Logic

### 3.1 Entry Condition 1: High EWO Reversal

```python
(close < ma_buy × 0.979) AND (EWO > 2.337) AND (RSI < 55) AND (volume > 0)
```

This captures "healthy pullback" opportunities in uptrends.

### 3.2 Entry Condition 2: Low EWO Rebound

```python
(close < ma_buy × 0.979) AND (EWO < -15.87) AND (volume > 0)
```

This captures oversold rebound opportunities. No RSI check needed since extreme EWO already implies low RSI.

---

## IV. Exit Signal Logic

### 4.1 Basic Exit Signal

```python
(close > ma_sell × 0.997) AND (volume > 0)
```

### 4.2 Exit Confirmation

The `confirm_trade_exit` function prevents premature exits when trend is still strong.

### 4.3 Slippage Protection

```python
slippage_protection = {'retries': 3, 'max_slippage': -0.05}
```

---

## V. Risk Management System

### 5.1 Fixed Stop-Loss: -18.9%

Provides adequate room for cryptocurrency volatility.

### 5.2 Trailing Stop

- Activates at 1.57% profit
- Stop distance: 0.7% below high

### 5.3 Custom Stop-Loss Function

- Locks profits when profitable
- Time-based stop after 241 minutes if still losing

### 5.4 ROI Targets

```python
minimal_roi = {
    "0": 0.215,    # 21.5% immediately
    "40": 0.132,   # 13.2% after 40 min
    "87": 0.086,   # 8.6% after 87 min
    "201": 0.03    # 3% after 201 min
}
```

---

## VI. Parameter Optimization

### 6.1 Buy Parameters

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 11 | 5-80 |
| ewo_high | 2.337 | 2.0-12.0 |
| ewo_low | -15.87 | -20.0--8.0 |
| low_offset | 0.979 | 0.9-0.99 |
| rsi_buy | 55 | 30-70 |

### 6.2 Sell Parameters

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_sell | 17 | 5-80 |
| high_offset | 0.997 | 0.99-1.1 |

---

## VII. Strategy Pros & Cons

### 7.1 Advantages

- Solid theoretical foundation based on Elliott Wave
- Multi-layered risk management (fixed + trailing + custom + ROI)
- Dual entry covering trending and ranging markets
- Slippage protection mechanism

### 7.2 Limitations

- May trigger frequent stop-losses in extreme volatility
- 5-minute timeframe sensitive to noise
- Parameter overfitting risk

---

## VIII. Summary

ElliotV531 combines Elliott Wave theory with modern quantitative techniques. Its dual-entry design covers both trend continuation and reversal opportunities, while multi-layered risk management protects capital effectively. Best suited for short-term traders familiar with Elliott Wave theory.

**Disclaimer**: This document is for learning reference only and does not constitute investment advice.
