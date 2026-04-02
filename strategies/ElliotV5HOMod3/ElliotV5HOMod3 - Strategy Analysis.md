# ElliotV5HOMod3 - Strategy Analysis

## I. Strategy Overview

ElliotV5HOMod3 is an Elliott Wave-based trend-following strategy refined for the Freqtrade framework. Its core design: "enter on pullbacks, exit with discipline." The strategy waits for price to retreat to reasonable levels in confirmed uptrends, then enters with multi-layer risk protection.

### Core Philosophy

**"Wait for the discount, then sell when risen."** Not chasing rallies, not panic-selling dumps. Key principles:
- Trend confirmation first
- Pullback entries for better risk/reward
- Multi-indicator filtering to reduce false signals
- Dynamic risk management adapting to market conditions

## II. Technical Indicators

### EWO (Core)
- Formula: (EMA(50) - EMA(200)) / Close × 100
- ewo_high: 3.34 (strong uptrend signal)
- ewo_low: -17.457 (extreme oversold signal)

### EMA System
- Buy EMA: 17-period, offset 0.978
- Sell EMA: 39-period, offset 1.011

### RSI
- Period: 14
- Buy threshold: 60 (RSI < 60 required)

## III. Entry Signals

### Condition 1: Trend Pullback (Primary)
```python
close < ma_buy × 0.978 AND EWO > 3.34 AND RSI < 60 AND volume > 0
```

### Condition 2: Extreme Oversold
```python
close < ma_buy × 0.978 AND EWO < -17.457 AND volume > 0
```

No RSI filter in Condition 2.

## IV. Exit Signals

### Basic Exit
```python
close > ma_sell × 1.011 AND volume > 0
```

Note: `use_sell_signal = False` — exits primarily via ROI and stop-loss.

### ROI
```python
minimal_roi = {"0": 0.07}  # 7% immediate target
```

### Trailing Stop
- Activates at 3% profit
- 0.5% below highest price

### Custom Stop-Loss
```python
profit > 3%:  stop at 1%
profit 1.8-3%: stop at 0.5%
else:           -99% (let fixed stop handle)
```

## V. Risk Management

- **Fixed Stop-Loss**: -6% (tightest among ElliotV5 variants)
- **Minimal ROI**: 7% (single aggressive target)
- **Trailing**: Activates 3%, tracks 0.5% below peak
- **Custom Stop-Loss**: Dynamically tightens as profit grows

## VI. Parameter Optimization Space

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 17 | 5-80 |
| low_offset | 0.978 | 0.9-0.99 |
| ewo_high | 3.34 | 2.0-12.0 |
| ewo_low | -17.457 | -20.0--8.0 |
| rsi_buy | 60 | 30-70 |
| base_nb_candles_sell | 39 | 5-80 |
| high_offset | 1.011 | 0.99-1.1 |

## VII. Strategy Advantages

- Tightest stop-loss (-6%) among V5 variants — better capital protection
- 7% single ROI target — clear profit goal
- Custom stop-loss dynamically tightens on profitable trades
- Multi-indicator confirmation reduces false signals

## VIII. Strategy Limitations

- Single ROI target (not tiered) — less adaptive to varying market speeds
- May exit too early in slow but steady trends
- 1-hour informative timeframe not fully utilized

## IX. Summary

ElliotV5HOMod3 is the most capital-preservation focused variant in the V5 series. Its -6% stop-loss and 7% ROI target provide tighter control compared to siblings. Best suited for traders prioritizing capital protection over maximizing trend rides.

**Disclaimer**: For learning reference only, not investment advice.
