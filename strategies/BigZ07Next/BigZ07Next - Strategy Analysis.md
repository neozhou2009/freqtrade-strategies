# BigZ07Next Strategy Analysis

## I. Strategy Overview

**BigZ07Next** is a high-complexity trend-following quantitative trading strategy built on the NostalgiaForInfinityV8 framework. The strategy uses multi-timeframe analysis and multi-condition composite filtering to capture trend reversal and continuation opportunities in volatile markets.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 14 independent conditions |
| **Exit Conditions** | 8 basic conditions + 50+ custom rules |
| **Protection Mechanisms** | Multi-level take-profit + pump protection + recovery mechanisms |
| **Timeframe** | 5-minute main cycle + 1-hour auxiliary |
| **Recommended Positions** | 4-6 pairs |

### Core Parameters

| Parameter | Default | Description |
|--------|--------|------|
| timeframe | 5m | Main trading cycle |
| stoploss | -0.10 | Fixed stoploss line -10% |
| trailing_stop | True | Enable trailing take-profit |
| trailing_stop_positive | 0.01 | Trailing activation threshold 1% |
| trailing_stop_positive_offset | 0.025 | Trailing pullback starting point 2.5% |
| exit_profit_only | True | Only allow exit when profitable |

---

## II. Strategy Configuration Analysis

### 2.1 Timeframe Configuration

BigZ07Next uses dual-timeframe architecture:

- **Main Timeframe (5 minutes)**: Used for daily trading decisions, capturing short-term price volatility
- **Information Timeframe (1 hour)**: Used for trend judgment and filtering, providing medium to long-term market perspective

Core logic of this design: Confirm trend direction at 1-hour level, find specific entry points at 5-minute level.

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'market',
    'exit': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

### 2.3 ROI Return Target Table

| Holding Time (minutes) | Expected Return |
|-----------------|-----------|
| 0-10 | 2.8% |
| 10-40 | 1.8% |
| 40-180 | 0.5% |
| 180+ | 1.8% |

---

## III. Entry Conditions Details

Strategy contains **14 independent entry conditions** (buy_condition_0 to buy_condition_13), each can be independently enabled/disabled. All conditions are "OR" relationship, satisfying any one triggers buy signal.

### Conditions Overview

| Condition | Core Logic | Key Indicators |
|----------|----------|----------|
| buy_condition_0 | RSI oversold + continuous decline filter | RSI < 30, RSI_1h < 71 |
| buy_condition_1 | Bollinger lower rail + volume contraction | Close < BB_lower * 0.989 |
| buy_condition_2 | Bollinger lower rail + volume contraction variant | Close < BB_lower * 0.982 |
| buy_condition_3 | 1h level above EMA200 + RSI oversold | RSI < 14.2 |
| buy_condition_4 | 1h RSI extremely low + volume contraction | RSI_1h < 16.5 |
| buy_condition_5 | MACD golden cross + Bollinger lower rail | EMA26 > EMA12 |
| buy_condition_6 | RSI_1h low + MACD golden cross | RSI_1h < 39 |
| buy_condition_7 | RSI_1h extremely low + MACD pattern | RSI_1h < 15 |
| buy_condition_8 | Dual RSI oversold | RSI < 28, RSI_1h < 20 |
| buy_condition_9 | RSI combination filter | RSI < 10, RSI_1h < 35 |
| buy_condition_10 | MACD momentum reversal + 1h Bollinger | MACD Hist > 0, 1h close < BB_lower |
| buy_condition_11 | Bollinger Band narrowing + MACD continuous rise | BB bandwidth narrows, Hist continuously positive |
| buy_condition_12 | Breakout buy pattern | Close > EMA200, breaks BB lower rail |
| buy_condition_13 | Extreme oversold + capital outflow | CMF < -0.435, RSI < 22 |

### Entry Conditions Common Characteristics

All entry conditions share following filtering logic:

1. **Volume Threshold**: 48-period volume mean needs to be 40% higher than 48 periods ago
2. **Trend Requirement**: Most conditions require closing price above EMA200
3. **Volume Validity**: All conditions require current volume > 0

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Exit System

Strategy implements comprehensive exit protection:

1. **ROI Take-Profit**: Time-based profit targets
2. **Trailing Stop**: Dynamic profit protection
3. **Custom Exit Rules**: 50+ custom conditions
4. **Pump Protection**: Detects abnormal volatility

### 4.2 Recovery Mechanisms

Strategy includes recovery exit conditions for positions with losses, allowing exit at small profits to minimize losses.

---

## V. Technical Indicator System

### Trend Indicators
- EMA200 (5-minute and 1-hour)
- EMA50 (1-hour)

### Momentum Indicators
- RSI (14-period, dual timeframe)
- MACD (12,26,9)

### Volatility Indicators
- Bollinger Bands (20,2)

### Volume Indicators
- Volume mean (48-period)
- CMF

---

## VI. Strategy Pros & Cons

### 6.1 Advantages
1. Comprehensive protection mechanisms
2. Rich entry conditions (14 types)
3. Multi-layer exit system
4. Pump protection for extreme volatility

### 6.2 Limitations
1. High complexity increases understanding difficulty
2. May exit too early in strong trends
3. Requires significant monitoring

---

## VII. Applicable Scenarios

### 7.1 Recommended
- Volatile markets
- Oscillating conditions
- Markets with clear support/resistance

### 7.2 Not Recommended
- Strong one-sided trends
- Low volatility environments
- Illiquid trading pairs

---

## VIII. Summary

BigZ07Next is a complex trend-following strategy built on NostalgiaForInfinityV8 framework. Through 14 entry conditions, multi-layer exit system, and comprehensive protection mechanisms, it builds a sophisticated trading system.

**Key Features:**
- 14 independent entry conditions
- 50+ custom exit rules
- Multi-level protection
- Suitable for volatile markets

**Risk Warning:**
High complexity requires thorough understanding before use. Conduct sufficient backtesting and paper trading.
