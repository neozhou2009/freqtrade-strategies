# TEMA Strategy In-Depth Analysis

> **Strategy ID**: #406 (406th of 465 strategies)  
> **Strategy Type**: TEMA Moving Average Trend Following + Bollinger Band Channel Strategy  
> **Timeframe**: 1 Minute (1m)

---

## 1. Strategy Overview

TEMA is a trend-following strategy based on Triple Exponential Moving Average. The strategy leverages TEMA's fast response characteristics, combined with Bollinger Band middle band as dynamic support/resistance, to capture short-term trend initiation and reversal. This strategy is one of Freqtrade's official strategy templates with optimizable parameters.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 core buy signal (TEMA breakout above Bollinger Band middle band) |
| **Sell Condition** | 1 basic sell signal (TEMA breakdown below Bollinger Band middle band) |
| **Protection Mechanism** | Tiered take-profit + 10% stop-loss + trailing stop |
| **Timeframe** | 1 Minute (1m) |
| **Dependencies** | talib, pandas_ta, qtpylib |
| **Optimizable Parameters** | RSI buy/sell thresholds via Hyperopt |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (Tiered Take-Profit)
minimal_roi = {
    "60": 0.01,   # After 60 minutes, 1% take-profit
    "30": 0.02,   # After 30 minutes, 2% take-profit
    "0": 0.04     # Immediately, 4% take-profit
}

# Stop-loss Setting
stoploss = -0.10  # 10% fixed stop-loss

# Trailing Stop
trailing_stop = True
```

**Design Philosophy**:
- Tiered take-profit: Take 4% profit immediately, lower take-profit threshold over time (time for space)
- 10% stop-loss: Relatively loose, suitable for 1-minute high-frequency trading
- Trailing stop enabled: Lock in profits after gains

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

**Design Philosophy**: Use limit orders for buy/sell to reduce slippage, market order for stop-loss to ensure execution

### 2.3 Optimizable Parameters

```python
# Strategy Parameters (Support Hyperopt Optimization)
buy_rsi = IntParameter(10, 40, default=30, space="buy")
sell_rsi = IntParameter(60, 90, default=70, space="sell")
```

---

## 3. Buy Condition Details

### 3.1 Core Buy Logic

```python
dataframe.loc[
    (
        (dataframe['tema'] <= dataframe['bb_middleband']) &  # TEMA below BB middle band
        (dataframe['tema'] > dataframe['tema'].shift(1)) &   # TEMA rising
        (dataframe['volume'] > 0)                             # Has volume
    ),
    'buy'] = 1
```

**Buy Signal Components**:

| Condition | Logic | Description |
|-----------|-------|-------------|
| TEMA Position | `tema <= bb_middleband` | TEMA below Bollinger Band middle band (relatively low price zone) |
| TEMA Direction | `tema > tema.shift(1)` | TEMA rising (trend initiation) |
| Volume | `volume > 0` | Confirms volume exists (avoids data anomalies) |

### 3.2 TEMA Indicator Characteristics

TEMA (Triple Exponential Moving Average) calculation formula:
```
TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
```

**Advantages**:
- Faster response than EMA and SMA
- Reduced lag
- Earlier detection of trend changes

---

## 4. Sell Logic Details

### 4.1 Core Sell Logic

```python
dataframe.loc[
    (
        (dataframe['tema'] > dataframe['bb_middleband']) &   # TEMA above BB middle band
        (dataframe['tema'] < dataframe['tema'].shift(1)) &   # TEMA falling
        (dataframe['volume'] > 0)                             # Has volume
    ),
    'sell'] = 1
```

**Sell Signal Components**:

| Condition | Logic | Description |
|-----------|-------|-------------|
| TEMA Position | `tema > bb_middleband` | TEMA above Bollinger Band middle band (relatively high price zone) |
| TEMA Direction | `tema < tema.shift(1)` | TEMA falling (trend reversal) |
| Volume | `volume > 0` | Confirms volume exists |

### 4.2 Signal Symmetry

Buy and sell logic are completely symmetrical:
- Buy: TEMA below middle band + upward breakout
- Sell: TEMA above middle band + downward breakout

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend Indicator | TEMA(9) | Main trend determination, trading signal core |
| Volatility Indicator | Bollinger Bands(20, 2) | Middle band as dynamic support/resistance |
| Momentum Indicator | RSI(14) | Optimizable parameter, auxiliary judgment |
| Trend Indicator | MACD(12, 26, 9) | Calculated but not used for trading signals |
| Trend Indicator | ADX(14) | Calculated but not used for trading signals |
| Overbought/Oversold | Stochastic Fast | Calculated but not used for trading signals |
| Volume | MFI | Calculated but not used for trading signals |
| Trend Indicator | SAR | Calculated but not used for trading signals |
| Cycle Indicator | Hilbert Transform | Calculated but not used for trading signals |

### 5.2 Visualization Configuration

The strategy provides complete chart configuration:

```python
plot_config = {
    'main_plot': {
        'tema': {},                    # TEMA line
        'sar': {'color': 'white'},     # SAR dots
    },
    'subplots': {
        "MACD": {
            'macd': {'color': 'blue'},
            'macdsignal': {'color': 'orange'},
        },
        "RSI": {
            'rsi': {'color': 'red'},
        }
    }
}
```

---

## 6. Risk Management Features

### 6.1 Tiered Take-Profit Mechanism

```
Holding Time    Take-Profit Target
─────────────────────
0 minutes      4%
30 minutes     2%
60 minutes     1%
```

**Design Purpose**:
- Quick profit: Take 4% immediately, capturing short-term volatility
- Time decay: Longer holding, more conservative take-profit
- Prevent drawdown: Avoid profit giveback

### 6.2 Stop-Loss Configuration

```python
stoploss = -0.10  # 10% stop-loss
trailing_stop = True  # Enable trailing stop
```

**Features**:
- 10% stop-loss is relatively loose, suitable for high-frequency strategies
- Trailing stop can lock in profits after gains

### 6.3 Volume Verification

All buy/sell signals verify `volume > 0`, avoiding data anomalies.

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Fast Response**: TEMA responds faster than EMA, catching trends earlier
2. **Simple Logic**: Only 3 buy conditions, 3 sell conditions, clear and understandable
3. **Optimizable Parameters**: RSI parameters can be auto-optimized via Hyperopt
4. **Tiered Take-Profit**: Dynamically adjusts take-profit targets, balancing return and risk

### ⚠️ Limitations

1. **High-Frequency Nature**: 1-minute timeframe, high trade frequency, significant fee impact
2. **Many False Signals**: Frequent short-term volatility, prone to false breakouts
3. **Unused Indicators**: Calculates many indicators but doesn't use them for trading, wasting computational resources
4. **Missing Trend Filter**: No ADX or MA direction filter, may generate signals in ranging markets

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Trending Market | Default configuration | TEMA can quickly follow trends |
| High Volatility | Increase stop-loss | 10% may need adjustment |
| High-Frequency Environment | Enable | 1-minute timeframe suitable for HFT |
| Ranging Market | Add trend filter | Recommend adding ADX or MA direction filter |

---

## 9. Applicable Market Environment Details

TEMA is a **short-term trend following strategy**. Based on TEMA's fast response characteristics, it performs best in **clearly trending markets** and may underperform in **sideways ranging markets**.

### 9.1 Strategy Core Logic

- **TEMA Trend Determination**: Use TEMA's fast response to catch trend initiation
- **Bollinger Band Middle Band**: As dynamic support/resistance, confirming entry position
- **Direction Verification**: TEMA must be rising/falling to enter

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | TEMA quickly follows, BB middle band provides support confirmation |
| 📉 Downtrend | ⭐⭐⭐⭐☆ | Equally effective, but short signals rely on sell triggers |
| 📊 Volatile Trend | ⭐⭐⭐⭐☆ | Trends within volatility can be effectively captured |
| 🔄 Sideways Range | ⭐⭐☆☆☆ | Frequent false breakouts, stop-losses may be frequently triggered |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|---------------|------------------|-------|
| Timeframe | 1m (high-frequency) | Can try 5m to reduce trade frequency |
| Stop-loss | -10% | Adjust based on volatility |
| RSI Parameters | Hyperopt optimize | Let machine find optimal parameters |

---

## 10. Important Note: Cost of Complexity

### 10.1 Learning Curve

Strategy logic is simple, but requires understanding:
- TEMA calculation principles and characteristics
- Bollinger Band middle band support/resistance role
- Tiered take-profit time decay mechanism

### 10.2 Hardware Requirements

| Trading Pairs | Minimum Memory | Recommended Memory |
|--------------|----------------|-------------------|
| 1-10 pairs | 4GB | 8GB |
| 10-50 pairs | 8GB | 16GB |

**Note**: 1-minute timeframe, large data processing volume

### 10.3 Backtesting vs Live Trading Differences

- **Backtesting Challenge**: 1-minute data is large, requires sufficient historical data
- **Live Trading Challenge**: High-frequency trading fee accumulation significantly impacts returns
- **Recommendation**: Consider fee impact when optimizing parameters

### 10.4 Manual Trader Suggestions

TEMA can be used for manual trading assistance:
- Add TEMA indicator to charts
- Overlay Bollinger Bands
- Observe TEMA relationship with BB middle band
- Confirm with RSI overbought/oversold levels

---

## 11. Summary

**TEMA** is a simple and efficient short-term trend following strategy. Its core value lies in:

1. **Fast Response**: TEMA responds faster than EMA, catching trends earlier
2. **Clear Logic**: Symmetrical buy/sell signals, easy to understand and verify
3. **Optimizable Parameters**: RSI parameters support auto-optimization

For quantitative traders, this is a high-frequency strategy suitable for trending markets. Recommended for use in clear trend environments, and pay attention to fee impact on returns.