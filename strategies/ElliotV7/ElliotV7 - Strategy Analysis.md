# ElliotV7 - Strategy Analysis

## I. Strategy Overview

ElliotV7 is a sophisticated quantitative trading strategy combining Elliott Wave theory with multi-dimensional technical analysis, designed for high-volatility cryptocurrency markets. Developed by @Rallipanos, V7 represents the seventh major iteration of this strategy family.

### Core Philosophy: "Trend-First, Buy the Dip"

The strategy follows these principles:
1. **Trend Priority**: Only enters confirmed uptrends (1h trend confirmation)
2. **Pullback Entry**: Never chases; waits for price to pull back to reasonable levels
3. **Multi-Dimensional Verification**: Every signal requires multiple indicators to confirm
4. **Dynamic Adaptation**: Extensive optimizable parameters for different market conditions

### Timeframe
- Primary: 5 minutes
- Auxiliary: 1 hour (trend confirmation)
- Startup: 39 candles

## II. Multi-Timeframe Analysis

### 1h Timeframe
- EMA(20) > EMA(25): Confirms uptrend
- RSI(100): Long-term overbought/oversold

### 5m Timeframe
- Entry/exit execution
- All technical indicators calculated here

### Multi-Timeframe Synergy
1. Fetch 1h candle data
2. Calculate EMA(20), EMA(25), uptrend_1h on 1h
3. Merge 1h indicators to 5m data (forward-filled)
4. Generate signals on 5m but only when uptrend_1h > 0

## III. Technical Indicators

### EWO
```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(df, timeperiod=50)
    ema2 = ta.EMA(df, timeperiod=200)
    return (ema1 - ema2) / df['close'] * 100
```
- ewo_high = 2.327
- ewo_low = -19.988

### Moving Averages
- Buy EMA: 14-period (default)
- Sell EMA: 24-period (default)
- HMA(50): Low-lag MA for sell confirmation
- SMA(9): Short-term trend reference

### RSI Matrix
- RSI(14): Standard, buy confirmation
- RSI(4): Fast, short-term oversold (<35)
- RSI(20): Slow, sell confirmation
- RSI(100): Ultra-long, trend reference

## IV. Entry Signals

### Buy Channel 1: EWO High (Primary Trend Play)
```python
uptrend_1h > 0 AND
rsi_fast < 35 AND
close < ma_buy × 0.975 AND
EWO > 2.327 AND
rsi < 69 AND
volume > 0 AND
close < ma_sell × 0.991
```

7 conditions must ALL be met. This is the strictest entry condition among all Elliot variants.

### Buy Channel 2: EWO Low (Extreme Reversal)
```python
uptrend_1h > 0 AND
rsi_fast < 35 AND
close < ma_buy × 0.975 AND
EWO < -19.988 AND
volume > 0 AND
close < ma_sell × 0.991
```

No RSI filter (extreme EWO implies extreme RSI).

## V. Exit Signals

### Sell Channel 1: Strong Exit
```python
sma_9 > hma_50 AND
close > ma_sell × 0.997 AND
rsi > 50 AND
volume > 0 AND
rsi_fast > rsi_slow
```

For strong momentum markets.

### Sell Channel 2: Normal Exit
```python
sma_9 < hma_50 AND
close > ma_sell × 0.991 AND
volume > 0 AND
rsi_fast > rsi_slow
```

For weaker momentum markets.

Note: `use_sell_signal = True`, `sell_profit_only = True`, offset = 1%.

## VI. Risk Management

### Fixed Stop-Loss: -32%
Wide stop for 5-minute cryptocurrency trading. Combined with tight entry conditions, this provides adequate cushion.

### Trailing Stop
- Activates at 3% profit
- 0.5% below highest price

### Custom Stop-Loss Function
```python
if loss > 10% AND holding > 12 hours:
    tighten to -1%
else:
    default stop
```
After 12 hours with >10% loss, exit aggressively — a losing trade held too long is likely wrong.

### ROI Targets
```python
minimal_roi = {
    "0": 0.051,   # 5.1% immediate
    "10": 0.031,  # 3.1% after 10 min
    "22": 0.018,  # 1.8% after 22 min
    "66": 0       # Any profit after 66 min
}
```

## VII. Parameter Space

### Buy Parameters
| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 14 | 5-80 |
| ewo_high | 2.327 | 2.0-12.0 |
| ewo_low | -19.988 | -20.0--8.0 |
| low_offset | 0.975 | 0.9-0.99 |
| rsi_buy | 69 | 30-70 |

### Sell Parameters
| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_sell | 24 | 5-80 |
| high_offset | 0.991 | 0.95-1.1 |
| high_offset_2 | 0.997 | 0.99-1.5 |

## VIII. Strategy Advantages

1. **Multi-timeframe verification**: 1h trend confirmation prevents counter-trend trades
2. **7-condition entry**: Extremely strict, very few false signals
3. **Dual buy channels**: Trend continuation AND reversal opportunities
4. **Tiered sell logic**: Different thresholds for strong vs. weak markets
5. **5-layer risk management**: Comprehensive protection including time-based stop
6. **Highly optimizable**: All key parameters tunable

## IX. Strategy Limitations

1. **Trend-dependent**: No trades in bear/choppy markets
2. **Wide -32% stop**: May result in large single losses
3. **Parameter sensitivity**: Optimized parameters may overfit
4. **Slippage impact**: Frequent small-profit trades affected by fees

## X. Summary

ElliotV7 is the most sophisticated strategy in the Elliot series. Its multi-timeframe design, strict 7-condition entry, and tiered sell logic represent the most complete risk management. Best suited for traders seeking maximum signal quality over frequency, with capital to withstand wider stop-losses.

**Disclaimer**: For learning reference only, not investment advice.
