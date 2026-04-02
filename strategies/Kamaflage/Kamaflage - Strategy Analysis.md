# Kamaflage Strategy Analysis

> **Strategy Number**: #12 (12th of 465 strategies)  
> **Strategy Type**: Multi-Indicator Momentum Strategy (KAMA + RMI + MACD)  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

**Kamaflage** is a complex multi-indicator momentum strategy that combines multiple technical indicators including KAMA (Kaufman Adaptive Moving Average), RMI (Relative Momentum Index), and MACD, and introduces an order book check mechanism to optimize order execution. The strategy name "Kamaflage" likely comes from the combination of "KAMA" and "Camouflage".

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Multi-condition combination (KAMA + MACD + RMI + Volume) |
| **Exit Conditions** | RMI oversold + profit check + order book price |
| **Protection** | Trailing stop + Order timeout check |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | Order book check, order timeout cancellation |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table (hyperopt results)
minimal_roi = {
    "0": 0.15,      # Immediate exit: 15% profit
    "10": 0.10,     # After 10 minutes: 10% profit
    "20": 0.05,     # After 20 minutes: 5% profit
    "30": 0.025,    # After 30 minutes: 2.5% profit
    "60": 0.01,     # After 60 minutes: 1% profit
}

# Stoploss setting
stoploss = -0.10  # -10% hard stoploss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01125       # 1.125% trailing activation
trailing_stop_positive_offset = 0.04673  # 4.673% offset trigger
trailing_only_offset_is_reached = True
```

**Design Logic**:
- **Multi-level ROI**: 5-level decreasing ROI, longer holding time means lower exit threshold
- **Trailing stop**: Activates 1.125% trailing after 4.67% profit, suitable for trending markets
- **Hyperparameter optimization**: ROI and trailing parameters from hyperopt results

### 2.2 Order Type Configuration

Uses Freqtrade default configuration, but implements order timeout check functions.

---

## III. Entry Conditions Details

### 3.1 Entry Logic (No Position)

```python
# Entry conditions when no position
conditions = [
    dataframe["kama-3"] > dataframe["kama-21"],           # KAMA fast line > slow line
    dataframe["macd"] > dataframe["macdsignal"],          # MACD > signal line
    dataframe["macd"] > params["macd"],                   # MACD > threshold (0)
    dataframe["macdhist"] > params["macdhist"],           # MACD hist > threshold (0)
    dataframe["rmi"] > dataframe["rmi"].shift(),          # RMI rising
    dataframe["rmi"] > params["rmi"],                     # RMI > threshold (50)
    dataframe["volume"] < (dataframe["volume_ma"] * 20),  # Volume < avg volume × 20
]
```

**Logic Analysis**:
- **KAMA trend**: 3-period KAMA > 21-period KAMA, confirms short-term trend upward
- **MACD golden cross**: MACD line above signal line and greater than 0, momentum upward
- **MACD hist confirmation**: MACD histogram greater than 0, momentum strengthening
- **RMI momentum**: RMI indicator rising and above 50
- **Volume filter**: Excludes abnormally high volume (possibly manipulation)

### 3.2 Entry Conditions (With Position)

```python
# Add position conditions when already holding
conditions = [
    dataframe["close"] > dataframe["sar"],    # Price > SAR
    dataframe["rmi"] >= 75,                   # RMI >= 75
]
```

**Note**: When already holding a position, consider adding only when trend is strong.

### 3.3 Hyperparameters

```python
# Buy hyperparameters (optimized results)
buy_params = {
    "macd": 0,
    "macdhist": 0,
    "rmi": 50,
}
```

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions when holding position
active_trade = Trade.get_trades([...]).all()
if active_trade:
    ob = self.dp.orderbook(metadata["pair"], 1)
    current_price = ob["asks"][0][0]
    current_profit = active_trade[0].calc_profit_ratio(rate=current_price)
    
    conditions = [
        (dataframe["buy"] == 0) &              # No buy signal
        (dataframe["rmi"] < 30),               # RMI < 30 (oversold)
        (current_profit > -0.03),              # Profit > -3%
        (dataframe["volume"] > 0),             # Volume > 0
    ]
```

**Logic Analysis**:
- **RMI oversold**: RMI < 30 confirms short-term oversold
- **Profit check**: Only sell if loss not exceeding 3% (avoid cutting at big losses)
- **Order book price**: Uses real-time order book price to calculate profit
- **Buy signal disappeared**: Consider exit when buy signal disappears

### 4.2 Order Timeout Check

```python
# Buy order timeout check
def check_entry_timeout(self, pair, trade, order, **kwargs) -> bool:
    ob = self.dp.orderbook(pair, 1)
    current_price = ob["bids"][0][0]
    if current_price > order["price"] * 1.01:  # Price increased over 1%
        return True  # Cancel order
    return False

# Sell order timeout check
def check_exit_timeout(self, pair, trade, order, **kwargs) -> bool:
    ob = self.dp.orderbook(pair, 1)
    current_price = ob["asks"][0][0]
    if current_price < order["price"] * 0.99:  # Price decreased over 1%
        return True  # Cancel order
    return False
```

**Purpose**:
- Prevent orders from not filling due to price movement
- Cancel orders when price deviation exceeds 1%

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|------------|---------|
| **Trend** | KAMA | 3, 21 periods | Kaufman Adaptive Moving Average |
| **Momentum** | MACD | Default | Momentum strength and direction |
| **Momentum** | RMI | Default | Relative Momentum Index |
| **Stoploss** | SAR | Default | Trend-following stop |
| **Volume** | Volume MA | 24 periods | Volume filter |

### 5.2 Indicator Calculation

```python
# KAMA (Kaufman Adaptive Moving Average)
dataframe["kama-3"] = ta.KAMA(dataframe, timeperiod=3)
dataframe["kama-21"] = ta.KAMA(dataframe, timeperiod=21)

# MACD
macd = ta.MACD(dataframe)
dataframe["macd"] = macd["macd"]
dataframe["macdsignal"] = macd["macdsignal"]
dataframe["macdhist"] = macd["macdhist"]

# RMI (Relative Momentum Index)
dataframe["rmi"] = RMI(dataframe)

# SAR
dataframe["sar"] = ta.SAR(dataframe)

# Volume Moving Average
dataframe["volume_ma"] = dataframe["volume"].rolling(window=24).mean()
```

---

## VI. Risk Management Features

### 6.1 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01125
trailing_stop_positive_offset = 0.04673
trailing_only_offset_is_reached = True
```

**Working mechanism**:
1. Trailing stop activates after profit reaches 4.673%
2. Triggers exit when pulling back 1.125% from highest point
3. Needs to reach offset before trailing activates

### 6.2 Order Timeout Check

**Buy orders**:
- Cancel when current price > order price × 1.01

**Sell orders**:
- Cancel when current price < order price × 0.99

### 6.3 Sell Profit Protection

```python
current_profit > -0.03  # Loss not exceeding 3%
```

**Purpose**: Avoids forced selling at large losses.

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Multi-indicator combination**: KAMA + MACD + RMI + SAR multi-dimensional confirmation
2. **Order book check**: Uses real-time order book to optimize order execution
3. **Order timeout**: Prevents orders from not filling due to price movement
4. **Trailing stop**: Locks profits, protects gains
5. **Hyperparameter optimization**: Key parameters from hyperopt

### ⚠️ Limitations

1. **High complexity**: Multiple indicators and conditions, difficult to debug
2. **No trend filter**: No EMA/SMA long-term trend judgment
3. **No BTC correlation**: Doesn't detect Bitcoin market trend
4. **Order book dependency**: Requires exchange to support orderbook API
5. **Parameter sensitivity**: Hyperopt results may overfit

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Note |
|-------------------|--------------------------|------|
| **Ranging market** | Default configuration | Multi-indicator combination suitable for ranging |
| **Uptrend** | Default configuration | Trailing stop locks profits |
| **Downtrend** | Pause or light position | No trend filter, easy to lose |
| **High volatility** | Adjust parameters | May need to widen order timeout threshold |
| **Low volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Applicable Market Environments Explained

Kamaflage is a multi-indicator momentum strategy based on the core philosophy of "multi-condition confirmation".

### 9.1 Strategy Core Logic

- **Multi-indicator confirmation**: KAMA + MACD + RMI confirm simultaneously before buying
- **Order book optimization**: Uses real-time order book for price check and order cancellation
- **Trailing stop**: Locks profits, lets profits run

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Slow bull/ranging up | ★★★★☆ | Multi-indicator confirmation + trailing stop performs well |
| 🔄 Wide ranging | ★★★★☆ | Multi-indicator combination suitable for ranging |
| 📉 Single-sided crash | ★★☆☆☆ | No trend filter, may lose consecutively |
| ⚡️ Extreme sideways | ★★★☆☆ | Too little volatility, signals reduce |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Note |
|--------------|------------------|------|
| **Number of pairs** | 20-40 | Moderate signal frequency |
| **Max positions** | 3-6 | Control risk |
| **Position mode** | Fixed position | Recommended fixed position |
| **Timeframe** | 5m | Mandatory requirement |

---

## X. Important Note: Order Book Dependency

### 10.1 Moderate Learning Curve

Strategy code is about 150 lines, requires understanding multiple indicators and order book mechanism.

### 10.2 Moderate Hardware Requirements

Multi-indicator computation increases computation:

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 20-40 pairs | 1GB | 2GB |
| 40-80 pairs | 2GB | 4GB |

### 10.3 Order Book Dependency

Strategy uses `self.dp.orderbook()` to get real-time order book:
- Requires exchange to support orderbook API
- Order book data may have latency in live trading
- Order book data may be inaccurate in backtesting

### 10.4 Manual Trader Recommendations

Manual traders can reference this strategy's multi-indicator approach:
- Observe KAMA, MACD, RMI multiple indicators simultaneously
- Use trailing stop to protect profits
- Set order timeout cancellation mechanism

---

## XI. Summary

**Kamaflage** is a well-designed multi-indicator momentum strategy. Its core value lies in:

1. **Multi-indicator combination**: KAMA + MACD + RMI + SAR multi-dimensional confirmation
2. **Order book optimization**: Uses real-time order book for price check and order cancellation
3. **Trailing stop**: Locks profits, protects gains
4. **Hyperparameter optimization**: Key parameters from hyperopt results

For quantitative traders, this is an excellent multi-indicator strategy template. Recommendations:
- Use as an advanced case for multi-indicator combinations
- Learn order book check and order timeout mechanisms
- Can add trend filter, BTC correlation and other protection mechanisms on this basis
- Note that hyperparameters may overfit, test thoroughly before live trading

---
