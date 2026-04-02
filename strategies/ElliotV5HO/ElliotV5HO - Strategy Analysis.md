# ElliotV5HO - Strategy Analysis

## I. Strategy Overview and Core Philosophy

ElliotV5HO is a quantitative trading strategy based on Elliott Wave Theory, built for the Freqtrade framework. The strategy combines classical technical analysis theory with modern quantitative methods, using EWO to capture periodic characteristics of market fluctuations and find trading opportunities at key trend continuation or reversal points.

The "V5HO" designation indicates the fifth version with "High Optimization" — a heavily refined iteration. It operates on a 5-minute primary timeframe with 1-hour auxiliary timeframe, representing medium-short-term trading.

## II. Technical Indicators

### 2.1 EWO (Core Indicator)

```
EWO = (EMA(50) - EMA(200)) / Close × 100
```

- ewo_high = 2.337: High momentum, uptrend continuation expected
- ewo_low = -15.87: Extreme low, potential rebound

### 2.2 EMA System

- Buy EMA: 11-period, offset 0.979
- Sell EMA: 17-period, offset 0.997

### 2.3 RSI

- Period: 14
- Buy threshold: 55 (RSI < 55 required)

## III. Entry Signals

### 3.1 Condition 1: Strong Correction Buy

```python
(close < EMA_buy × 0.979) AND (EWO > 2.337) AND (RSI < 55) AND (volume > 0)
```

Captures pullback opportunities during uptrends.

### 3.2 Condition 2: Extreme Oversold Buy

```python
(close < EMA_buy × 0.979) AND (EWO < -15.87) AND (volume > 0)
```

No RSI filter — when EWO is this extreme, RSI is already low.

## IV. Exit Signals

```python
(close > EMA_sell × 0.997) AND (volume > 0)
```

With `sell_profit_only = True` requiring minimum 1% profit.

## V. Risk Management

### 5.1 Fixed Stop-Loss: -30.2%

Wide stop-loss for volatile crypto markets.

### 5.2 Trailing Stop

- Activates at 3% profit
- Stop distance: 0.5% below peak

### 5.3 Custom Layered Stop-Loss

```python
profit > 30%:  stop at -15%
profit > 20%:  lock 10% profit
profit > 10%:  lock 5% profit
profit 0-10%:  use default -30.2%
```

### 5.4 ROI

```python
minimal_roi = {
    "0": 0.051,   # 5.1% immediately
    "20": 0.032,  # 3.2% after 20 min
    "45": 0.016,  # 1.6% after 45 min
    "70": 0       # Accept any profit after 70 min
}
```

## VI. Strategy Advantages

- Solid Elliott Wave theoretical foundation
- Dual-entry covering trend and reversal
- Layered stop-loss including "big fish" strategy (loosens at 30% profit)
- "Ignore ROI if buy signal active" allows holding through trends

## VII. Strategy Limitations

- May underperform in choppy markets
- Wide -30.2% stop-loss is aggressive
- Parameter sensitivity to market conditions

## VIII. Summary

ElliotV5HO is a well-designed strategy combining Elliott Wave theory with modern risk management. Its "big fish" strategy (loosening stop at 30% profit to let trends run) shows deep understanding of trend trading. Suitable for experienced traders who understand Elliott Wave principles and can tolerate wider stop-losses.

**Disclaimer**: For learning reference only, not investment advice.
