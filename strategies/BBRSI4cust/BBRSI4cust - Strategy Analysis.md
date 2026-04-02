# BBRSI4cust Strategy Analysis

> **Strategy Number**: #21 (21st of 465 strategies)  
> **Strategy Type**: Bollinger Bands + RSI + Custom Exit  
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

**BBRSI4cust** is a mean reversion strategy based on Bollinger Bands and RSI, featuring a custom_exit function to optimize sell logic. The "4cust" in the strategy name indicates its custom exit functionality, "BB" represents Bollinger Bands, and "RSI" represents Relative Strength Index.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 1 condition: PLUS_DI + Bollinger Band breakout |
| **Exit Conditions** | Custom exit function + technical sell signals |
| **Protection** | Hard stoploss + Trailing stop |
| **Timeframe** | 15 minutes |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | custom_exit custom exit |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.003    # Immediate exit: 0.3% profit
}

# Stoploss setting
stoploss = -0.1  # -10% hard stoploss

# Trailing stop
trailing_stop = True
```

**Design Logic**:
- **Very Low ROI**: Only 0.3% ROI, pursuing quick turnover
- **Standard Stoploss**: -10% hard stoploss
- **Trailing Stop**: Enabled but no specific parameters configured

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}

order_time_in_force = {
    "entry": "GTC",
    "exit": "GTC",
}
```

### 2.3 Hyperopt Parameters

```python
# Entry hyperopt parameters
buy_bb = IntParameter(low=1, high=4, default=1, space="buy")  # Bollinger Band std dev
buy_di = IntParameter(low=10, high=20, default=20, space="buy")  # PLUS_DI threshold

# Exit hyperopt parameters
sell_bb = IntParameter(low=1, high=4, default=1, space="exit")  # Bollinger Band std dev
```

---

## III. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (dataframe["plus_di"] > self.buy_di.value) &           # PLUS_DI > threshold
        (qtpylib.crossed_below(dataframe["low"], dataframe["bb_lowerband"])) &  # Price breaks below BB lower
        (dataframe["volume"] > 0)                               # Volume > 0
    ),
    "enter_long",
] = 1
```

**Logic Analysis**:
- **PLUS_DI Confirmation**: +DI above threshold (default 20), confirming upward momentum
- **Bollinger Band Breakout**: Price breaks below Bollinger Band lower band, statistically low position
- **Volume Filter**: Exclude zero volume

### 3.2 Indicator Calculation

```python
# PLUS_DI
dataframe["plus_di"] = ta.PLUS_DI(dataframe)

# RSI
dataframe["rsi"] = ta.RSI(dataframe)

# Bollinger Bands (20 periods, adjustable std dev)
bollinger = qtpylib.bollinger_bands(
    qtpylib.typical_price(dataframe), window=20, stds=self.buy_bb.value
)
dataframe["bb_lowerband"] = bollinger["lower"]
dataframe["bb_middleband"] = bollinger["mid"]
dataframe["bb_upperband"] = bollinger["upper"]
```

---

## IV. Exit Logic Explained

### 4.1 Technical Sell Signals

```python
# Exit conditions
dataframe.loc[
    (
        (qtpylib.crossed_above(dataframe["high"], dataframe["bb_middleband1"])) &
        (dataframe["volume"] > 0)
    ),
    "exit_long",
] = 1
```

**Logic Analysis**:
- **Bollinger Band Middle Breakout**: Price crosses above Bollinger Band middle band (using sell_bb parameter)
- **Volume Confirmation**: Volume greater than 0

### 4.2 Custom Exit Function

```python
def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
    current_candle = dataframe.iloc[-1].squeeze()
    
    # Check if price breaks through Bollinger Band middle band
    if current_rate > current_candle["bb_middleband1"]:
        return "bb_profit_sell"
    
    return None
```

**Purpose**:
- Real-time monitoring of price breaking through Bollinger Band middle band
- Returns custom exit reason "bb_profit_sell"
- Supplements technical sell signal limitations

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|---------|---------|------|------|
| **Momentum** | PLUS_DI | Default | Upward direction indicator |
| **Momentum** | RSI | 14 periods | Overbought/Oversold |
| **Volatility** | Bollinger Bands | 20 periods, adjustable std dev | Price boundaries |

### 5.2 Dual Bollinger Band System

The strategy uses two Bollinger Band systems:

| Bollinger Band | Period | Standard Deviation | Purpose |
|--------|------|--------|------|
| BB1 | 20 | buy_bb (default 1) | Entry reference |
| BB2 | 20 | sell_bb (default 1) | Exit reference |

---

## VI. Risk Management Features

### 6.1 Hard Stoploss

```python
stoploss = -0.1  # -10%
```

**Description**: Standard stoploss, controlling single trade loss within 10%.

### 6.2 Trailing Stop

```python
trailing_stop = True
```

**Purpose**: Enable trailing stop to protect profits.

### 6.3 Custom Exit

```python
if current_rate > current_candle["bb_middleband1"]:
    return "bb_profit_sell"
```

**Purpose**:
- Real-time price breakout monitoring
- Supplements technical signal delays
- Improves exit timeliness

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Custom Exit**: Flexible control of sell timing
2. **Hyperopt Optimization**: Supports Hyperopt for Bollinger Band std dev optimization
3. **Dual Exit**: Technical signals + custom exit
4. **Low Computation**: Few indicators, low hardware requirements
5. **Low ROI**: 0.3% ROI, quick turnover

### ⚠️ Limitations

1. **No Trend Filter**: No long-term trend judgment
2. **No BTC Correlation**: Does not detect Bitcoin market trend
3. **Very Low ROI**: 0.3% may exit too early
4. **15m Timeframe**: Lower signal frequency
5. **Parameter Sensitive**: Bollinger Band std dev needs optimization

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Ranging Market** | Default configuration | Mean reversion most suitable for ranging markets |
| **Uptrend** | Default configuration | Low ROI enables quick turnover |
| **Downtrend** | Pause or light position | No trend filter, easy to lose |
| **High Volatility** | Adjust Bollinger Bands | May need to adjust std dev |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Applicable Market Environments

BBRSI4cust is a classic mean reversion strategy based on the core philosophy of "price returns to mean".

### 9.1 Strategy Core Logic

- **Bollinger Band Breakout**: Buy when price breaks below lower band, sell when breaks above middle band
- **PLUS_DI Confirmation**: Confirm upward momentum
- **Custom Exit**: Real-time price breakout monitoring

### 9.2 Performance in Different Markets

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ★★★★☆ | Mean reversion + low ROI performs well |
| 🔄 Wide Ranging | ★★★★★ | Ranging market is ideal for mean reversion |
| 📉 Single-sided Crash | ★★☆☆☆ | No trend filter, may lose consecutively |
| ⚡️ Extreme Sideways | ★★★☆☆ | Too little volatility, signals decrease |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Max Open Trades** | 3-6 | Control risk |
| **Position Mode** | Fixed position | Recommended fixed position |
| **Timeframe** | 15m | Mandatory requirement |

---

## X. Important Notes: Custom Exit Usage

### 10.1 Moderate Learning Cost

Strategy code is about 100 lines, requires understanding custom exit function.

### 10.2 Low Hardware Requirements

Only calculates PLUS_DI, RSI, Bollinger Bands, low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------|---------|---------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

### 10.3 Custom Exit Advantages

- **Real-time Monitoring**: Not limited by candle close
- **Flexible Control**: Can add any exit conditions
- **Improved Timeliness**: Reduces signal delays

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's custom exit approach:
- Set price breakout above Bollinger Band middle band to exit
- Use PLUS_DI to confirm upward momentum
- Set strict stoploss (e.g., -10%)

---

## XI. Summary

**BBRSI4cust** is a classic mean reversion strategy, its core value lies in:

1. **Custom Exit**: Flexible control of sell timing
2. **Hyperopt Optimization**: Supports Hyperopt for Bollinger Band std dev optimization
3. **Dual Exit**: Technical signals + custom exit
4. **Low Computation**: Few indicators, low hardware requirements
5. **Low ROI**: 0.3% ROI, quick turnover

For quantitative traders, this is an excellent custom exit learning template. Recommendations:
- Use as an introductory case for learning custom_exit function
- Understand Bollinger Band mean reversion usage
- Can add trend filters, BTC correlation, etc. on this basis
- Note that ultra-low ROI may exit large trends too early

---
