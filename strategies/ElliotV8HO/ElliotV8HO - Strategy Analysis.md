# ElliotV8HO - Strategy Analysis

## I. Strategy Overview

ElliotV8HO is a quantitative trading strategy based on Elliott Wave Oscillator, built for Freqtrade. The "V8HO" designation indicates Version 8, Hyperopt Optimized. It combines Elliott Wave theory with modern quantitative methods, using EWO to identify wave positions and multiple confirmations for signal quality.

### Core Design Philosophy
- **Trend following + mean reversion hybrid**
- **Multi-indicator confirmation**
- **Dynamic parameter optimization**
- **Comprehensive risk management**

## II. Technical Indicators

### EWO
- Formula: (EMA(50) - EMA(200)) / Close × 100
- ewo_high = 5.417
- ewo_low = -17.251

### RSI System
- Standard RSI(14)
- Fast RSI(4)
- Slow RSI(20)
- Buy requires: fast RSI < 35

### Moving Averages
- Buy EMA: 19-period (default)
- Sell EMA: 24-period (default)
- HMA(50): Trend direction
- SMA(9): Short-term reference

## III. Entry Signals

### Buy Channel 1: High EWO (EWO > 5.417)
```python
rsi_fast < 35 AND
close < ma_buy × 0.983 AND
EWO > 5.417 AND
rsi < 61 AND
volume > 0 AND
close < ma_sell × 1.011
```

### Buy Channel 2: Low EWO (EWO < -17.251)
```python
rsi_fast < 35 AND
close < ma_buy × 0.983 AND
EWO < -17.251 AND
volume > 0 AND
close < ma_sell × 1.011
```

No RSI filter in Channel 2 (extreme EWO implies extreme RSI).

## IV. Exit Signals

### Sell Channel 1: Strong (Price > HMA_50)
```python
close > hma_50 AND
close > ma_sell × 1.011 AND
rsi > 50 AND
volume > 0 AND
rsi_fast > rsi_slow
```

### Sell Channel 2: Weak (Price < HMA_50)
```python
close < hma_50 AND
close > ma_sell × 0.997 AND
volume > 0 AND
rsi_fast > rsi_slow
```

## V. Risk Management

### ROI (Phased)
```python
minimal_roi = {
    "0": 0.08,   # 8% immediately
    "40": 0.032, # 3.2% after 40 min
    "87": 0.016  # 1.6% after 87 min
}
```

### Fixed Stop-Loss: -18.9%

### Trailing Stop
- Activates at 2% profit
- 0.5% below highest price

### Signal Protection
- `use_sell_signal = True`
- `sell_profit_only = True`
- `sell_profit_offset = 0.01` (minimum 1% profit)

## VI. Parameter Space

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 19 | 15-60 |
| low_offset | 0.983 | 0.9-0.99 |
| ewo_high | 5.417 | 1.0-8.0 |
| ewo_low | -17.251 | -20.0--15.0 |
| rsi_buy | 61 | 25-75 |
| base_nb_candles_sell | 24 | 15-60 |
| high_offset | 1.011 | 0.9-1.1 |
| high_offset_2 | 0.997 | 0.99-1.2 |

## VII. Strategy Advantages

1. **High EWO threshold (5.417)**: Only enters on strong momentum, fewer but higher-quality signals
2. **Phased ROI**: Declining targets over time, optimizes capital efficiency
3. **HMA-based sell confirmation**: Low-lag MA prevents late exits
4. **Strong hyperopt optimization**: Parameters optimized via extensive backtesting
5. **Dual sell channels**: Adapts to strong vs. weak momentum

## VIII. Strategy Limitations

1. **Fewer signals**: High EWO threshold reduces frequency
2. **Higher entry standard**: May miss some trend opportunities
3. **RSI filter relatively loose**: rsi_buy = 61 allows higher RSI entries
4. **1h informative timeframe not fully utilized**: Defined but not integrated in trading logic

## IX. Summary

ElliotV8HO is the "quality and patience" variant — its higher EWO threshold (5.417 vs. ~2-3 in other variants) means it only enters when momentum is exceptionally strong. This results in fewer but potentially higher-quality signals. Best suited for traders prioritizing signal quality and willing to wait for optimal setups.

**Disclaimer**: For learning reference only, not investment advice.
