# BigZ07 Strategy Analysis

## I. Strategy Overview

**BigZ07** is a **low drawdown, buy dips, sell quickly** quantitative trading strategy. Its core philosophy can be summarized as:

- **Minimize drawdown as much as possible**
- **Buy at price valleys**
- **Sell quickly to release capital**
- **Soft check whether market is rising, hard check whether market is declining**

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 14 independent conditions |
| **Exit Signals** | No active exit signals (relies on ROI or stoploss) |
| **Protection Mechanisms** | Custom intelligent stoploss |
| **Timeframe** | 5-minute main cycle + 1-hour auxiliary |
| **Recommended Positions** | 3-5 pairs |

---

## II. Strategy Configuration Analysis

### 2.1 Timeframe Configuration

```python
timeframe = '5m'        # Main timeframe: 5-minute candles
inf_1h = '1h'           # Information timeframe: 1-hour candles
```

Strategy uses **dual-timeframe analysis**:
- **5-minute candles**: Used for daily signal judgment and entry decisions
- **1-hour candles**: Used for trend filtering and long-term RSI judgment

### 2.2 Profit Target (Minimal ROI)

```python
minimal_roi = {
    "0": 0.028,         # Immediate 2.8% profit
    "10": 0.018,        # After 10 minutes: 1.8%
    "40": 0.005,        # After 40 minutes: 0.5%
    "180": 0.018,       # After 3 hours: 1.8%
}
```

### 2.3 Stoploss Configuration

```python
stoploss = -0.99  # Actually disabled, relies on custom stoploss
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

### 2.4 Order Types

```python
order_types = {
    'entry': 'market',
    'exit': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Entry Conditions Details

BigZ07 contains **14 independent entry conditions** (buy_condition_0 to buy_condition_13), each with independent parameter switches.

### Entry Conditions Overview

| Condition | Main Feature | Core Indicators |
|---------|---------|---------|
| buy_condition_0 | RSI oversold + above EMA200 | RSI < 30, EMA200 rising |
| buy_condition_1 | Bollinger lower rail + bearish | Close below BB lower |
| buy_condition_2 | Bollinger lower rail (simplified) | Close below BB lower |
| buy_condition_3 | RSI oversold + above EMA200_1h | RSI < 14.2 |
| buy_condition_4 | 1-hour RSI oversold | RSI_1h < 16.5 |
| buy_condition_5 | MACD golden cross + BB lower | EMA26 > EMA12 |
| buy_condition_6 | MACD golden cross + 1h RSI | RSI_1h < 39 |
| buy_condition_7 | MACD + 1-hour RSI | RSI_1h < 15 |
| buy_condition_8 | Dual RSI oversold | RSI < 28, RSI_1h < 20 |
| buy_condition_9 | Dual RSI oversold (variant) | RSI < 10, RSI_1h < 35 |
| buy_condition_10 | BB breakout + MACD | 1-hour BB lower rail |
| buy_condition_11 | MACD continuous rise | Histogram positive for 5 periods |
| buy_condition_12 | BB lower rail breakout | Low breaks BB lower |
| buy_condition_13 | CMF outflow + RSI | CMF < -0.435, RSI < 22 |

---

## IV. Exit Logic Details

### 4.1 No Active Exit Signals

Strategy doesn't use active exit signals, relies on:
- ROI take-profit
- Trailing stop
- Custom stoploss

### 4.2 Custom Stoploss

Core protection mechanism with intelligent logic based on:
- Holding time
- RSI levels
- Price position relative to EMA200

---

## V. Technical Indicator System

### Trend Indicators
- EMA200 (5-minute and 1-hour)
- EMA50 (1-hour)

### Momentum Indicators
- RSI (14-period, 5-minute and 1-hour)
- MACD (12,26,9)

### Volatility Indicators
- Bollinger Bands (20,2)

### Volume Indicators
- Volume mean (48-period)
- CMF (Chaikin Money Flow)

---

## VI. Strategy Pros & Cons

### 6.1 Advantages
1. Excellent drawdown control
2. Rich entry conditions (14 types)
3. Fast turnover releases capital quickly
4. Multi-timeframe analysis

### 6.2 Limitations
1. May exit too early in strong trends
2. Complex custom stoploss logic
3. Parameter sensitivity

---

## VII. Applicable Scenarios

### 7.1 Recommended
- Oscillating markets
- High volatility environments
- Dip buying opportunities

### 7.2 Not Recommended
- Strong bull markets (may exit early)
- Low volatility (hard to trigger entries)
- Continuous downtrends

---

## VIII. Summary

BigZ07 is a mean reversion strategy emphasizing low drawdown and fast turnover. Through 14 entry conditions and custom stoploss, it builds a system focused on "buy low, sell fast, control losses."

**Key Features:**
- 14 independent entry conditions
- Custom intelligent stoploss
- ROI ladder for quick profits
- Suitable for oscillating markets

**Risk Warning:**
Fast-exit design means limited profits per trade. Ensure full understanding before use.
