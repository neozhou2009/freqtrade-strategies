# Inverse Strategy Analysis

> **Strategy Number**: #28 (28th of 465 strategies)  
> **Strategy Type**: Inverse Fisher RSI Trend Following  
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

**Inverse** is a trend following strategy based on inverse Fisher RSI. The strategy uses Fisher RSI inverse transformation to capture trend reversal points, combined with 4-hour informative timeframe to confirm trends. Key feature is using hyperopt optimization to determine optimal buy/sell thresholds.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | Multi-condition combination (Fisher RSI + SSL + EMA) |
| **Exit Conditions** | Multi-condition combination (Fisher RSI) |
| **Protection** | Hard stoploss + Trailing stop + Confirm trade exit |
| **Timeframe** | 1 hour |
| **Dependencies** | TA-Lib, technical, numpy |
| **Special Features** | 4h informative timeframe, Fisher RSI inverse transformation |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "30": 0.05,   # After 30 minutes: 5% profit
    "60": 0.02,   # After 60 minutes: 2% profit
}

# Stoploss setting
stoploss = -0.2  # -20% hard stoploss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.078       # 7.8% trailing activation
trailing_stop_positive_offset = 0.174  # 17.4% offset trigger
trailing_only_offset_is_reached = False
```

**Design Logic**:
- **Multi-Level ROI**: 3-level decreasing ROI, longer holding time means lower exit threshold
- **Loose Stoploss**: -20% hard stoploss, giving ample room for fluctuation
- **Trailing Stop**: 7.8% trailing activates after 17.4% profit

### 2.2 Hyperopt Parameters

```python
# Entry hyperopt parameters
buy_fisher_length = IntParameter(low=13, high=55, default=31, space="buy")
buy_fisher_cci_1 = DecimalParameter(low=-0.6, high=-0.3, default=-0.42, space="buy")
buy_fisher_cci_2 = DecimalParameter(low=0.3, high=0.6, default=0.41, space="buy")

# Exit hyperopt parameters
sell_fisher_cci_1 = DecimalParameter(low=0.3, high=0.6, default=0.42, space="sell")
sell_fisher_cci_2 = DecimalParameter(low=-0.6, high=-0.3, default=-0.34, space="sell")
```

---

## III. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (
            (qtpylib.crossed_above(dataframe[f"fisher_cci_{buy_fisher_length}"], buy_fisher_cci_1)) |
            (
                (qtpylib.crossed_below(dataframe[f"fisher_cci_{buy_fisher_length}"], buy_fisher_cci_2).rolling(8).max() == 1) &
                (qtpylib.crossed_above(dataframe[f"fisher_cci_{buy_fisher_length}"], buy_fisher_cci_2))
            )
        ) &
        (ssl_up_4h > ssl_down_4h) &           # 4h SSL up
        (ema_50 > ema_200) &                   # 50EMA > 200EMA
        (ema_50_4h > ema_100_4h) &             # 4h 50EMA > 100EMA
        (ema_50_4h > ema_200_4h) &             # 4h 50EMA > 200EMA
        (volume > 0)                            # Volume > 0
    ),
    "buy",
] = 1
```

**Logic Analysis**:
- **Fisher CCI Cross**: Fisher CCI crosses above threshold 1 or crosses below threshold 2 then bounces back
- **4h SSL Confirmation**: 4-hour SSL channel up
- **EMA Bullish Alignment**: 50EMA > 200EMA (1h and 4h)
- **Volume Filter**: Exclude zero volume

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (
        (
            (qtpylib.crossed_below(dataframe[f"fisher_cci_{buy_fisher_length}"], sell_fisher_cci_1)) |
            (qtpylib.crossed_below(dataframe[f"fisher_cci_{buy_fisher_length}"], sell_fisher_cci_2))
        ) &
        (volume > 0)
    ),
    "sell",
] = 1
```

**Logic Analysis**:
- **Fisher CCI Cross Below**: Fisher CCI crosses below threshold 1 or threshold 2
- **Volume Confirmation**: Volume greater than 0

### 4.2 Confirm Trade Exit

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, current_time, **kwargs) -> bool:
    if sell_reason in ["sell_signal"]:
        if last_candle["di_up"] and (last_candle["adx"] > previous_candle_1["adx"]):
            return False  # Block exit
    return True
```

**Purpose**:
- Block premature exit based on ADX and DI
- Let profits run in trends

---

## V. Risk Management Features

### 5.1 Loose Hard Stoploss

```python
stoploss = -0.2  # -20%
```

**Description**: Loose stoploss, giving ample room for fluctuation.

### 5.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.078
trailing_stop_positive_offset = 0.174
trailing_only_offset_is_reached = False
```

**Working Mechanism**:
1. Trailing stop activates after 17.4% profit
2. Exit triggers when 7.8% pullback from highest point
3. Doesn't need to reach offset first to activate

### 5.3 Confirm Trade Exit

```python
if last_candle["di_up"] and (last_candle["adx"] > previous_candle_1["adx"]):
    return False  # Block exit
```

**Purpose**:
- Block premature exit based on ADX and DI
- Let profits run in trends

---

## VI. Strategy Pros & Cons

### ✅ Advantages

1. **Fisher RSI Inverse**: Captures trend reversal points
2. **Multi-Timeframe**: 1h + 4h confirms trend
3. **Confirm Trade Exit**: Blocks premature exit based on ADX/DI
4. **Hyperopt Optimization**: Supports Hyperopt for key parameters
5. **Trailing Stop**: Locks profits, protects gains
6. **Loose Stoploss**: -20% stoploss, giving ample room

### ⚠️ Limitations

1. **High Complexity**: Fisher RSI + multi-timeframe, difficult to debug
2. **No BTC Correlation**: Does not detect Bitcoin market trend
3. **Parameter Sensitive**: Hyperopt results may overfit
4. **High Computation**: Multi-indicator + informative timeframe increases computation
5. **1h Timeframe**: Lower signal frequency

---

## VII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Uptrend** | Highly recommended | Multi-timeframe + trailing stop, perfect match |
| **Ranging Market** | Recommended | Fisher RSI suitable for ranging markets |
| **Downtrend** | Pause or light position | Multi-timeframe blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## VIII. Summary

**Inverse** is a well-designed Fisher RSI trend following strategy, its core value lies in:

1. **Fisher RSI Inverse**: Captures trend reversal points
2. **Multi-Timeframe**: 1h + 4h confirms trend
3. **Confirm Trade Exit**: Blocks premature exit based on ADX/DI
4. **Hyperopt Optimization**: Supports Hyperopt for key parameters
5. **Trailing Stop**: Locks profits, protects gains
6. **Loose Stoploss**: -20% stoploss, giving ample room

For quantitative traders, this is an excellent Fisher RSI learning template. Recommendations:
- Use as an advanced case for learning Fisher RSI inverse transformation
- Understand multi-timeframe usage
- Learn confirm trade exit application
- Note that hyperopt parameters may overfit, testthoroughly before live trading

---
