# BigZ04_TSL4 Strategy Analysis

## I. Strategy Overview

**BigZ04_TSL4** is a quantitative trading strategy modified by Perkmeister based on ilya's BigZ04 strategy. The strategy's core design philosophy is: **achieving profits by buying at price lows while controlling drawdown**. The strategy adopts a combination mechanism of hard stoploss + dynamic trailing take-profit, representing a relatively conservative grid/trend hybrid strategy.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 14 independent conditions (13 enabled) |
| **Exit Conditions** | Relies on stoploss/take-profit mechanisms |
| **Protection Mechanisms** | 8% hard stoploss + dynamic trailing take-profit |
| **Timeframe** | 5-minute main cycle + 1-hour auxiliary |
| **Recommended Positions** | 2-4 pairs |

---

## II. Strategy Configuration Analysis

### 2.1 Timeframe Configuration

```python
timeframe = '5m'      # Main timeframe: 5-minute candles
inf_1h = '1h'         # Information timeframe: 1-hour candles
```

Strategy uses dual-timeframe analysis:
- **5-minute candles**: Used for generating entry signals and daily monitoring
- **1-hour candles**: Used for calculating long-term trend indicators (such as EMA200_1h, RSI_1h, etc.)

### 2.2 Take-Profit Configuration

```python
minimal_roi = {
    "0": 0.10,    # Execute 10% take-profit immediately after 0 minutes
    "30": 0.05,   # Reduce to 5% take-profit after 30 minutes
    "60": 0.02    # Reduce to 2% take-profit after 60 minutes
}
```

### 2.3 Stoploss Configuration

```python
stoploss = -0.99  # Basic stoploss disabled, taken over by custom_stoploss
```

### 2.4 Trailing Take-Profit Configuration

```python
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01        # 1% trailing amplitude
trailing_stop_positive_offset = 0.025 # 2.5% profit trigger
```

---

## III. Entry Conditions Details

The strategy contains **14 independent entry conditions** (numbered 0-13), each using different technical indicator combinations. Core logic is: **finding opportunities where price pulls back to Bollinger Band lower rail during uptrends**.

### Condition 0: Basic RSI Oversold

- Closing price > EMA200
- RSI < 30
- 1-hour RSI < 71

### Condition 1: Bollinger Band Dip Buy (Conservative)

- Closing price > EMA200 and > EMA200_1h
- Closing price < BB lower rail × 0.989

### Condition 2: Bollinger Band Dip Buy (Aggressive)

- Closing price > EMA200
- Closing price < BB lower rail × 0.982

### Conditions 3-4: RSI Dual-Cycle Filter

- Closing price > EMA200_1h
- RSI < 14.2
- 1-hour RSI < 35

### Conditions 5-7: MACD Golden Cross + Bollinger Band

- EMA26 > EMA12
- Closing price < BB lower rail
- MACD upward

### Conditions 8-9: Pure RSI Oversold

- 1-hour RSI < 20-35
- 5-minute RSI < 10-28

### Condition 10: 1-Hour Bollinger Band Breakout

- 1-hour RSI < 35
- 1-hour closing price < BB lower rail
- MACD turns positive

### Condition 11: MACD Continuous Uptrend

- Consecutive 5 candles MACD Histogram > 0
- Breaks above middle rail

### Condition 12: Volume Contraction + Price Reversal

- Volume drops over 60% compared to 48-cycle mean
- Price rebounds from lower rail

---

## IV. Exit Logic Details

### 4.1 Custom Stoploss Function (Core)

Strategy uses `custom_stoploss()` to implement tiered stoploss:

| Profit Range | Stoploss Strategy |
|---------|---------|
| Profit < 1.6% | Use hard stoploss -8% |
| Profit 1.6%-8% | Linear interpolation calculates stoploss position |
| Profit > 8% | Trailing stoploss starts, locks at least 4% profit |

### 4.2 Exit Signals

```python
use_exit_signal = True
exit_profit_only = True          # Only exit when profitable
exit_profit_offset = 0.001       # 0.1% profit satisfies
```

Actual exit condition: Closing price > Bollinger Band middle rail × 1.01

---

## V. Technical Indicator System

### Trend Indicators

| Indicator | Period | Usage |
|------|------|------|
| EMA200 | 200 | Long-term trend judgment |
| EMA200_1h | 200 (1h) | 1-hour long-term trend |

### Momentum Indicators

| Indicator | Parameters | Usage |
|------|------|------|
| RSI | 14 | Overbought/oversold judgment |
| RSI_1h | 14 (1h) | 1-hour momentum |
| MACD | 12,26,9 | Trend momentum |

### Volatility Indicators

| Indicator | Parameters | Usage |
|------|------|------|
| Bollinger Bands | 20,2 | Support/resistance identification |

### Volume Indicators

| Indicator | Period | Usage |
|------|------|------|
| Volume | - | Trading confirmation |
| Volume Mean Slow | 48 | Volume trend |

---

## VI. Strategy Pros & Cons

### 6.1 Advantages

1. **Excellent Drawdown Control**: Through 8% hard stoploss and dynamic trailing, effectively controls maximum loss
2. **Multiple Entry Conditions**: 14 conditions provide rich entry opportunities
3. **Profit Protection**: Dynamic trailing ensures profits don't turn into losses
4. **Trend Filtering**: EMA200 filter avoids counter-trend trading

### 6.2 Limitations

1. **Conservative Design**: May exit too early in strong trends
2. **Complex Stoploss Logic**: Tiered stoploss increases understanding difficulty
3. **Parameter Sensitivity**: Default parameters may not suit all market conditions

---

## VII. Applicable Scenarios

### 7.1 Recommended Scenarios

- **Oscillating Markets**: Strategy excels in range-bound markets
- **Moderate Volatility**: Suitable for normal volatility environments
- **Trend Pullbacks**: Good at capturing pullback opportunities in uptrends

### 7.2 Not Recommended Scenarios

- **Strong Bull Markets**: May exit too early, missing major gains
- **Extreme Volatility**: Hard stoploss may be triggered frequently
- **Sideways with Low Volume**: Entry conditions may be difficult to trigger

---

## VIII. Parameter Optimization

### 8.1 Default Parameter Philosophy

Default parameters are conservatively designed, prioritizing capital protection over aggressive profit seeking. Unless you have specific market understanding, recommended to use default parameters.

### 8.2 Optimization Directions

**Stoploss Adjustment**: Can adjust 8% hard stoploss based on personal risk tolerance. More aggressive traders may increase to 10-12%, conservative traders may reduce to 5-6%.

**Take-Profit Adjustment**: ROI ladder can be adjusted based on trading style. Short-term traders may lower thresholds, medium-term traders may raise them.

---

## IX. Live Trading Notes

### 9.1 Preparation Before Live Trading

Conduct sufficient backtesting before live deployment. Test across different market conditions (bull, bear, oscillating). Only deploy strategies performing well in backtests.

### 9.2 Monitoring During Live Trading

Monitor strategy performance regularly. Watch for:
- Stoploss trigger frequency
- Average profit per trade
- Maximum drawdown

### 9.3 Parameter Adjustment

Adjust parameters cautiously based on market conditions. Avoid frequent changes. Each adjustment should be based on data analysis, not emotions.

---

## X. Summary

BigZ04_TSL4 is a conservative grid/trend hybrid strategy emphasizing drawdown control. Through 14 entry conditions, 8% hard stoploss, and dynamic trailing take-profit, it builds a trading system centered on "capital protection first."

**Key Features:**
- 14 independent entry conditions
- 8% hard stoploss protection
- Dynamic trailing take-profit locks profits
- Suitable for oscillating markets

**Risk Warning:**
The strategy's conservative design means it may underperform in strong bull markets. Ensure full understanding before use and conduct proper risk management.
