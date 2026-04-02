# ElliotV8_original - Strategy Analysis

## I. Strategy Overview

ElliotV8_original is a quantitative trading strategy based on Elliott Wave Theory, developed by @Rallipanos. This is the original/reference version of the V8 series, combining Elliott Wave Oscillator with multiple technical indicators for multi-dimensional signal verification.

### Core Design
- **Strict entry conditions**: Only enters in confirmed uptrends with pullback
- **Multi-indicator confirmation**: RSI, EWO, moving averages all aligned
- **Complete risk management**: Fixed stop-loss, trailing stop, ROI, signal protection
- **Highly optimizable**: All key parameters tunable via Freqtrade hyperopt

### Timeframe
- Primary: 5 minutes
- Auxiliary: 1 hour (trend context)
- Startup: 400 candles (requires significant historical data)

## II. Technical Indicators

### EWO
- Formula: (EMA(50) - EMA(200)) / Close × 100
- ewo_high = 2.327
- ewo_low = -19.988

### Moving Averages
- Buy EMA: 14-period (default)
- Sell EMA: 24-period (default)
- HMA(50): Low-lag MA for sell confirmation
- SMA(9): Short-term reference

### RSI Matrix
- RSI(4): Fast, oversold confirmation
- RSI(14): Standard
- RSI(20): Slow sell confirmation

## III. Entry Signals

### Entry Channel 1: Strong Pullback
```python
rsi_fast < 35 AND
close < ma_buy × 0.975 AND
EWO > 2.327 AND
rsi < 69 AND
volume > 0 AND
close < ma_sell × 0.991
```

### Entry Channel 2: Deep Oversold
```python
rsi_fast < 35 AND
close < ma_buy × 0.975 AND
EWO < -19.988 AND
volume > 0 AND
close < ma_sell × 0.991
```

## IV. Exit Signals

### Exit Channel 1: Strong Momentum
```python
close > hma_50 AND
close > ma_sell × 0.997 AND
rsi > 50 AND
volume > 0 AND
rsi_fast > rsi_slow
```

### Exit Channel 2: Weak Momentum
```python
close < hma_50 AND
close > ma_sell × 0.991 AND
volume > 0 AND
rsi_fast > rsi_slow
```

## V. Risk Management

### Fixed Stop-Loss: -32%
Wide stop-loss reflecting the V8 series' capital-preservation approach.

### Trailing Stop
- Activates at 2% profit
- 0.1% below highest price

### ROI
```python
minimal_roi = {
    "0": 0.08,    # 8% immediately
    "40": 0.032,  # 3.2% after 40 min
    "87": 0.016,  # 1.6% after 87 min
    "201": 0      # Any profit after 201 min
}
```

### Sell Signal Protection
- `use_sell_signal = True`
- `sell_profit_only = True`
- `sell_profit_offset = 0.01`

## VI. Parameter Space

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 14 | 5-80 |
| ewo_high | 2.327 | 2.0-12.0 |
| ewo_low | -19.988 | -20.0--8.0 |
| low_offset | 0.975 | 0.9-0.99 |
| rsi_buy | 69 | 30-70 |
| base_nb_candles_sell | 24 | 5-80 |
| high_offset | 0.991 | 0.95-1.1 |
| high_offset_2 | 0.997 | 0.99-1.5 |

## VII. Strategy Advantages

1. **Multi-dimensional signal verification**: RSI, EWO, price position, and volume all aligned
2. **Dual entry mechanism**: Trend continuation AND reversal opportunities
3. **Complete risk management**: 4-layer protection (fixed, trailing, ROI, signal)
4. **Highly optimizable**: 8 tunable parameters for market adaptation
5. **Clear code structure**: Well-documented, suitable for learning and customization

## VIII. Strategy Limitations

1. **Trend-dependent**: Limited trades in choppy/bear markets
2. **Wide -32% stop-loss**: Largest single loss potential
3. **400-candle startup**: Requires extensive historical data
4. **Parameter sensitivity**: Requires regular re-optimization
5. **Slippage impact**: Frequent small-profit trades affected by fees

## IX. Summary

ElliotV8_original is the foundational strategy of the V8 series — the reference implementation from which variants like V8HO evolved. It offers the most complete framework for understanding the Elliot Wave-based approach in Freqtrade. Best suited for traders seeking the full feature set and willing to invest time in parameter optimization.

**Disclaimer**: For learning reference only, not investment advice.
