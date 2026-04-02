# ElliotV5HOMod2 - Strategy Analysis

## I. Strategy Overview

ElliotV5HOMod2 is an EWO-based trend-following strategy optimized for the Freqtrade framework. Key design: catching pullback opportunities in trends and identifying reversal points using wave oscillator extremes.

### Core Design

The strategy uses a bidirectional entry logic:
- EWO high (> 3.34): Trend continuation pullback
- EWO low (< -17.457): Extreme oversold bounce

### Key Parameters
- Buy EMA: 17-period, offset 0.978
- Sell EMA: 39-period, offset 1.011
- RSI buy threshold: 60
- EWO high: 3.34
- EWO low: -17.457
- Stop-loss: -10%
- Minimal ROI: 5% → 4% → 3% (decreasing over time)

## II. Entry Signals

### Condition 1: Trend Pullback
```python
close < ma_buy × 0.978 AND EWO > 3.34 AND RSI < 60 AND volume > 0
```

### Condition 2: Oversold Bounce
```python
close < ma_buy × 0.978 AND EWO < -17.457 AND volume > 0
```

No RSI filter in Condition 2 (extreme EWO already implies oversold RSI).

## III. Exit Signals

```python
close > ma_sell × 1.011 AND volume > 0
```

Uses 39-period EMA for exit, longer than the 17-period buy EMA ("slow exit").

## IV. Risk Management

### Fixed Stop-Loss: -10%

### Trailing Stop
- Activates at 3% profit
- 0.5% below highest price

### Time Stop
After 140 minutes, if still at a loss near entry, tightens stop to -0.5%.

### ROI Targets
- 0 min: 5%
- 40 min: 4%
- 201 min: 3%

## V. Strategy Pros & Cons

### Advantages
- Dual-entry covering both trend and reversal
- 10% stop-loss is tighter than most Elliot strategies
- Time-based stop clears "zombie" positions
- Complete risk management system

### Limitations
- May underperform in choppy markets
- 1-hour informative timeframe not fully utilized in current version
- Missing volume confirmation (only checks volume > 0)

## VI. Summary

ElliotV5HOMod2 is a mature, well-structured strategy. Its 10% stop-loss and time-based stop for zombie positions show thoughtful risk design. Best suited for traders who want tighter control than other Elliot variants.

**Disclaimer**: For learning reference only, not investment advice.
