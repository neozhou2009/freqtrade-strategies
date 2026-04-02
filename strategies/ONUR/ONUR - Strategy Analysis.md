# ONUR Strategy Analysis

> **Strategy Number**: #32  
> **Strategy Type**: Bollinger Band Mean Reversion + RSI Filtering  
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

ONUR is a medium-complexity cryptocurrency trading strategy that adopts a design combining Bollinger Band mean reversion strategy with RSI (Relative Strength Index). The strategy's design philosophy is based on a classic technical analysis assumption: price will fall back due to mean reversion effect after touching the upper Bollinger Band, and trading above the middle band indicates the market is in a relatively strong state.

The core logic can be summarized as: when price is above the Bollinger Band middle band (strong area), and RSI has not yet entered overbought territory, it forms a buying opportunity. This design attempts to capture trend continuation while avoiding entry at extreme positions.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 independent entry signal |
| **Exit Conditions** | 0 (commented out exit conditions, no active exit) |
| **Protection** | No explicit protection mechanisms |
| **Timeframe** | 15 minutes |
| **Dependencies** | talib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.131,    # Immediate exit requires 13.1% profit
    "109": 0.08,   # Exit at 8% profit after 109 minutes
    "226": 0.03    # Exit at 3% profit after 226 minutes
}

# Stoploss setting
stoploss = -0.10  # 10% fixed stoploss
```

**Design Logic**:

ONUR's ROI configuration is quite unique, showing the strategy author's preference for long-term holding. Unlike common short-term strategies, this ROI table sets an extremely high immediate take-profit threshold (13.1%), meaning considerable profit is needed after opening to trigger take-profit.

- **0 minutes threshold 13.1%**: This is an extremely aggressive setting; on 15-minute timeframe, 13.1% profit requires considerable price movement to achieve
- **109 minutes threshold 8%**: After about 7 hours, take-profit threshold drops to 8%
- **226 minutes threshold 3%**: After about 15 hours, take-profit threshold further drops to 3%

This design indicates the strategy author expects medium-term holding, not frequent intraday trading.

### 2.2 Trailing Stop Configuration

```python
# Trailing stop settings
trailing_stop = True
trailing_stop_positive = 0.293     # 29.3% retracement triggers exit
trailing_stop_positive_offset = 0.362  # Start tracking after 36.2% offset
trailing_only_offset_is_reached = True  # Only activate after reaching offset
```

**Design Logic**:

The trailing stop setting is very aggressive. A 29.3% retracement threshold means the strategy allows significant profit retracement before triggering exit. This "let profits run" design philosophy combined with high-threshold ROI constitutes a trading system pursuing major trends.

### 2.3 Order Type Configuration

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": True,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99,
}
```

**Detailed Analysis**:

- **stoploss_on_exchange = True**: Uses exchange's native stoploss function, not Freqtrade server-side stoploss, which can reduce network latency impact
- **stoploss_on_exchange_interval = 60**: Updates stoploss price every 60 seconds
- **stoploss_on_exchange_limit_ratio = 0.99**: Stoploss price set at 99% of market price, ensuring immediate execution

---

## III. Entry Conditions Details

### 3.1 Single Entry Condition

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (dataframe["rsi"] < 74) &
            (dataframe["close"] > dataframe["bb_middleband"])
        ),
        "buy",
    ] = 1
    return dataframe
```

**Logic Breakdown**:

1. **RSI < 74**: Relative Strength Index below 74, leaving room for rise
2. **close > bb_middleband**: Close price above Bollinger Band middle band, confirming market in relatively strong state

**Technical Meaning**:

This entry condition design is very clever:
- **RSI < 74** is not a traditional overbought/oversold signal. RSI's overbought area is typically above 70, oversold area below 30. The 74 threshold is very loose, meaning the strategy barely restricts RSI's high position
- **Close price > Bollinger Band middle band** is a trend confirmation signal. Bollinger Band middle band is 20-period simple moving average, price above it indicates current price higher than recent average price

The combination of these two conditions essentially says: "As long as price is in relatively strong area (>middle band), and hasn't risen to extreme position (RSI < 74), can buy".

### 3.2 Indicator Calculation

```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    # RSI
    dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

    # Bollinger Bands
    bollinger = qtpylib.bollinger_bands(
        qtpylib.typical_price(dataframe), window=20, stds=2
    )
    dataframe["bb_lowerband"] = bollinger["lower"]
    dataframe["bb_middleband"] = bollinger["mid"]
    dataframe["bb_upperband"] = bollinger["upper"]

    return dataframe
```

**Indicator Parameters**:

| Indicator | Parameter | Description |
|-----------|-----------|-------------|
| RSI | 14 periods | Standard RSI period |
| Bollinger Bands | 20 periods, 2 standard deviations | Classic Bollinger Band setting |

---

## IV. Exit Logic Details

### 4.1 Exit Signal Status

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            # (dataframe['close'] > dataframe['bb_upperband'])
        ),
        "sell",
    ] = 1
    return dataframe
```

**Key Finding**: Exit conditions are completely commented out! This means the strategy has no active exit signals.

### 4.2 Actual Exit Mechanisms

Since there are no active exit signals, exits completely rely on:

| Exit Method | Trigger Condition | Priority |
|-------------|------------------|----------|
| Fixed Stoploss | Loss 10% | First priority |
| Trailing Stop | Profit retracement 29.3% | Second priority |
| ROI Take-Profit | Holding time reaches threshold | Third priority |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend/Mean Reversion | Bollinger Bands (20, 2) | Identify price position and volatility |
| Momentum | RSI (14) | Measure price movement speed and magnitude |
| Price | Typical Price (H+L+C)/3 | Bollinger Band calculation base |

### 5.2 Bollinger Bands Details

Bollinger Bands consist of three lines:
- **Upper Band**: Middle band + 2 standard deviations
- **Middle Band**: 20-period simple moving average
- **Lower Band**: Middle band - 2 standard deviations

Under normal distribution assumption, price should run within Bollinger Bands about 95% of the time.

**ONUR's Use of Bollinger Bands**:
- Only uses middle band as strong/weak dividing line
- Doesn't use upper/lower bands for overbought/oversold judgment
- This is a simplified Bollinger Band application

---

## VI. Risk Management Features

### 6.1 Fixed Stoploss

```python
stoploss = -0.10  # 10% stoploss
```

10% fixed stoploss is relatively loose in cryptocurrency market. This setting gives price sufficient fluctuation space, avoiding being stopped out by normal volatility. However, single trade loss ceiling is also relatively high.

### 6.2 Aggressive Trailing Stop

```python
trailing_stop_positive = 0.293
trailing_stop_positive_offset = 0.362
```

Design logic:
1. Profit must exceed 36.2% to activate trailing stop
2. Once activated, allows 29.3% profit retracement before triggering exit
3. This setting designed for capturing major trends

### 6.3 Exchange Native Stoploss

```python
stoploss_on_exchange = True
stoploss_on_exchange_interval = 60
```

Using exchange's native stoploss function can:
- Reduce network latency
- Execute faster in extreme market conditions
- Reduce Freqtrade server-side pressure

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Simple Logic**: Only two conditions, easy to understand and modify
2. **Medium-Term Holding Design**: 13.1% take-profit threshold indicates expectation for trend moves
3. **Loose Stoploss**: 10% fixed stoploss gives market sufficient fluctuation space
4. **Aggressive Trailing Stop**: "Let profits run" design philosophy
5. **Exchange Stoploss**: Fast response, extreme market protection

### ⚠️ Cons

1. **No Active Exit**: Completely relies on take-profit/stoploss system
2. **RSI Threshold Too Loose**: 74 barely constitutes restriction
3. **Conditions Too Simple**: May generate many false signals
4. **No Protection Mechanisms**: No additional conditions to filter noise
5. **Long Only**: No short logic

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Uptrend | Usable | Performs better during trend continuation |
| Ranging market | Use with caution | More false signals |
| High volatility coins | Adjust stoploss | 10% may not be enough |
| Mainstream coins | Recommended | Good liquidity, predictable volatility |

---

## IX. Detailed Applicable Market Environments

### 9.1 Strategy Core Logic

ONUR's design philosophy can be summarized as simplified version of "trend pullback buy" strategy. It assumes:
- Price in relatively strong state when above Bollinger Band middle band
- RSI as auxiliary indicator, but threshold set very loose
- Stoploss and take-profit system responsible for risk management

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Uptrend | ⭐⭐⭐⭐ | Price continuously above middle band, large profit space during trend continuation |
| 📉 Downtrend | ⭐⭐ | Counter-trend buying, even rebounds may fail |
| 🔄 Ranging market | ⭐⭐⭐ | Middle band crossing generates trading signals |
| ⚡ High volatility | ⭐⭐⭐ | Large volatility brings large profits, but may quickly hit stoploss |

### 9.3 Key Configuration Recommendations

| Configuration Item | Suggested Value | Description |
|-------------------|-----------------|-------------|
| Trading pairs | 10-20 | Risk diversification |
| Timeframe | Keep 15m | Suitable for medium-term holding |
| Stoploss | Can tighten to -5% | Depends on risk preference |

---

## X. Important Reminders: The Cost of Complexity

### 10.1 Learning Cost

Although ONUR strategy is simple, there are some unique designs worth deep understanding:
- Extremely high immediate take-profit threshold
- Aggressive trailing stop
- Exchange native stoploss

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 1-20 | 1GB | 2GB |
| 20-50 | 2GB | 4GB |

### 10.3 Backtest vs Live Trading Differences

- **RSI Threshold**: 74 threshold may produce excessive trading in historical data
- **Bollinger Band Calculation**: Need to pay attention to adjusted data impact
- **Slippage**: 10% stoploss may execute at worse price in extreme market conditions

### 10.4 Manual Trader Suggestions

When executing manually:
- Confirm overall trend direction
- Wait for price to pull back near middle band before buying
- Consider using more conservative take-profit targets

---

## XI. Summary

ONUR is a "simple but not simplistic" strategy. Although entry conditions are only two, combined with aggressive trailing stop and extremely high take-profit threshold, it constitutes a complete trading system.

Its core values are:

1. **Simplicity**: Easy to understand and implement
2. **Trend Following**: Let profits run through trailing stop
3. **Medium-Term Positioning**: Suitable for 15-minute level trend moves
4. **Customizability**: Large parameter adjustment space

For quantitative traders, ONUR is suitable as entry-level strategy or as foundation skeleton for more complex strategies. But considering its simple logic, recommended to add additional filtering conditions in practical application to improve signal quality.

---

*Document Version: v1.0*  
*Strategy Series: Bollinger Band Mean Reversion Strategy*
