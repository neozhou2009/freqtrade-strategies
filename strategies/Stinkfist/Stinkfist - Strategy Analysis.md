# Stinkfist Strategy In-Depth Analysis

> **Strategy Number**: #389 (389th of 465 strategies)  
> **Strategy Type**: Custom Indicators + Dynamic Position Sizing + Price Protection Mechanism  
> **Timeframe**: 5 minutes (5m) + 1-hour informative layer (1h)

---

## I. Strategy Overview

Stinkfist is a complex trend-following strategy based on multiple custom technical indicators, supporting dynamic position sizing and sophisticated price protection mechanisms. The strategy name originates from Tool's classic song, embodying the design philosophy of "deep digging" — finding trading opportunities through multi-layered technical analysis.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signal sets (new positions + additions), can trigger independently |
| **Sell Conditions** | Multi-condition combined exits, including dynamic stop-loss and position management |
| **Protection Mechanism** | 3 protection parameter groups (price protection, timeout check, order confirmation) |
| **Timeframe** | 5m main timeframe + 1h informative timeframe |
| **Dependencies** | numpy, talib, technical.indicators, qtpylib, arrow, cachetools, pandas |
| **Sub-strategies** | BTC-specific version (Stinkfist_BTC) and ETH-specific version (Stinkfist_ETH) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.05,      # Immediate: 5% profit target
    "10": 0.025,    # After 10 minutes: 2.5% profit target
    "20": 0.015,    # After 20 minutes: 1.5% profit target
    "30": 0.01,     # After 30 minutes: 1% profit target
    "720": 0.005,   # After 12 hours: 0.5% profit target
    "1440": 0       # After 24 hours: close position
}

# Stop-loss setting
stoploss = -0.40    # 40% hard stop-loss
```

**Design Philosophy**:
- Adopts a stepped ROI mechanism — the longer the position is held, the lower the profit target
- 40% loose stop-loss gives the strategy sufficient room for volatility
- Forced exit after 24 hours to avoid long-term entrapment

### 2.2 Order Type Configuration

```python
use_sell_signal = True         # Enable sell signals
sell_profit_only = True        # Only use sell signals when profitable
ignore_roi_if_buy_signal = True  # Ignore ROI when buy signal is active
```

### 2.3 Buy Parameters

```python
buy_params = {
    'inf-pct-adr': 0.80,  # Informative layer ADR percentage threshold
    'mp': 30              # Momentum Pinball threshold
}
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Protection Mechanisms (3 Groups)

Each buy condition is equipped with independent protection parameter groups:

| Protection Type | Parameter Description | Default Example |
|-----------------|----------------------|-----------------|
| **Price Protection** | Order price vs. current price deviation check | Reject if > 1% |
| **Buy Timeout** | Unfilled order check | Cancel if price deviation > 1% |
| **Sell Timeout** | Unfilled order check | Cancel if price deviation < 1% |

### 3.2 Buy Condition Classification

The strategy contains two independent buy logic sets:

#### Condition Group 1: New Position Buy (4 Conditions)

```python
# Logic
- Informative layer condition: close <= 3d_low + (0.80 * adr)
- Momentum Pinball: mp < 30
- Streak ROC: streak-roc > pcc-lowerband
- MA Cross: mac == 1
```

**Condition Details**:

| Condition # | Indicator | Condition | Meaning |
|-------------|-----------|-----------|---------|
| 1 | Informative Layer | `close <= 3d_low + (0.80 * adr)` | Price near 3-day low + 80% daily volatility range |
| 2 | Momentum Pinball | `mp < 30` | Momentum indicator shows oversold condition |
| 3 | Streak ROC | `streak-roc > pcc-lowerband` | Rate of change above lower band |
| 4 | MA Cross | `mac == 1` | Fast MA crosses above slow MA |

#### Condition Group 2: Position Addition Buy (Dynamic Growth Logic)

```python
# Logic (only triggers when active trades exist)
- RMI trend upward: rmi-up-trend == 1
- Profit protection: current_profit > (peak_profit * profit_factor)
- RMI growth threshold: rmi-slow >= linear_growth(30, 70, 180, 720)
```

**Dynamic Growth Function**:
```python
def linear_growth(self, start: float, end: float, 
                  start_time: int, end_time: int, trade_time: int) -> float:
    # Linear growth from start (30) to end (70)
    # Time range: 180-720 minutes
    # The longer held, the higher the threshold
```

### 3.3 Informative Layer Indicators Detailed

The strategy uses 1-hour timeframe as informative layer for higher-dimensional trend judgment:

```python
# Informative layer indicators
informative['1d_high'] = informative['close'].rolling(24).max()   # 24-hour high
informative['3d_low'] = informative['close'].rolling(72).min()     # 3-day low
informative['adr'] = informative['1d_high'] - informative['3d_low']  # Volatility range
```

---

## IV. Sell Logic Detailed Analysis

### 4.1 Dynamic Stop-Loss System

The strategy adopts a dynamic stop-loss mechanism:

```python
# Dynamic stop-loss threshold calculation
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
# The longer held, the tighter the stop-loss (from -3% to 0%)
```

### 4.2 Sell Signal Combination

| Condition Group | Trigger Condition | Description |
|-----------------|-------------------|-------------|
| Dynamic Stop-Loss | `current_profit < loss_cutoff` and `profit > stoploss` | Stop-loss tightens over time |
| RMI Trend Reversal | `rmi-dn-trend == 1` | RMI trend turning downward |
| Profit State Judgment | `peak_profit > 0` then `rmi-slow < 50`, else `rmi-slow < 10` | Distinguishes profit/loss states |
| Position Management | Comprehensive judgment when other positions exist | Considers global position |

### 4.3 Sell Signal Logic

```python
# Sell signal combination
conditions.append(
    (trade_data['current_profit'] < loss_cutoff) & 
    (trade_data['current_profit'] > self.stoploss) &  
    (dataframe['rmi-dn-trend'] == 1) &
    (dataframe['volume'].gt(0))
)
if trade_data['peak_profit'] > 0:
    conditions.append(dataframe['rmi-slow'] < 50)
else:
    conditions.append(dataframe['rmi-slow'] < 10)
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| **RMI** | RMI(21, 5) slow, RMI(8, 4) fast | Relative Momentum Index, trend judgment |
| **MA Streak** | MA Streak(4) | Consecutive up/down count |
| **PCC** | Percent Change Channel(20, 2) | Percentage change channel |
| **MAC** | Moving Average Cross(20, 50) | MA cross determination |
| **ROC/RSI** | ROC(1), RSI(ROC, 3) | Momentum pinball indicator |

### 5.2 Informative Timeframe Indicators (1h)

The strategy uses 1-hour timeframe as informative layer:

- **24-hour High**: `1d_high = close.rolling(24).max()`
- **3-day Low**: `3d_low = close.rolling(72).min()`
- **Volatility Range**: `adr = 1d_high - 3d_low`

### 5.3 Custom Indicator Implementation

#### MA Streak (Consecutive Count)
```python
def ma_streak(self, dataframe: DataFrame, period: int = 4) -> Series:
    # Calculate consecutive up/down count
    # Positive = consecutive up, negative = consecutive down
```

#### Percent Change Channel
```python
def pcc(self, dataframe: DataFrame, period: int = 20, mult: int = 2):
    # Similar to Keltner channel but uses percentage change
    # Calculates upper, middle, lower bands
```

#### MA Cross
```python
def mac(self, dataframe: DataFrame, fast: int = 20, slow: int = 50) -> Series:
    # Fast EMA (20) and slow EMA (50) cross determination
    # Returns 1 (bullish) or -1 (bearish)
```

---

## VI. Risk Management Features

### 6.1 Price Protection Mechanism

The strategy implements three layers of price protection:

```python
def confirm_trade_entry(self, pair: str, order_type: str, 
                        amount: float, rate: float, ...) -> bool:
    # Entry price protection: reject when current price > order price * 1.01
    if current_price > rate * 1.01:
        return False
    return True

def check_buy_timeout(self, pair: str, trade: Trade, order: dict, ...) -> bool:
    # Buy timeout: cancel order when price deviation > 1%
    if current_price > order['price'] * 1.01:
        return True
    return False

def check_sell_timeout(self, pair: str, trade: Trade, order: dict, ...) -> bool:
    # Sell timeout: cancel order when price deviation < 1%
    if current_price < order['price'] * 0.99:
        return True
    return False
```

### 6.2 Global Position Management

The strategy tracks all open trades for comprehensive judgment:

| Data Item | Description |
|-----------|-------------|
| `active_trade` | Whether current pair has active trade |
| `current_profit` | Current profit ratio |
| `peak_profit` | Peak profit |
| `open_minutes` | Position holding time (minutes) |
| `other_trades` | Whether there are other trades |
| `avg_other_profit` | Average profit of other trades |
| `biggest_loser` | Whether current is the biggest losing trade |
| `free_slots` | Remaining available positions |

### 6.3 Cache Mechanism

```python
custom_current_price_cache: TTLCache = TTLCache(maxsize=100, ttl=300)
# 5-minute price cache, reduces API calls
```

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-layer Protection Mechanism**: Three layers — price protection, timeout check, order confirmation
2. **Dynamic Position Sizing Logic**: Intelligent addition based on holding time and profit state
3. **Informative Layer Assisted Decision**: 1-hour timeframe provides higher-dimensional trend judgment
4. **Sub-strategy Customization**: BTC and ETH versions have independent optimized parameters
5. **Global Position Management**: Considers comprehensive profit and risk of all positions

### ⚠️ Limitations

1. **High Complexity**: Many custom indicators, difficult to understand and debug
2. **Loose Stop-Loss**: 40% stop-loss may lead to significant drawdowns
3. **Real-time Data Dependency**: Requires frequent current price and orderbook data
4. **Position Addition Risk**: Adding positions during trend reversal may amplify losses

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Volatile Market | Default parameters | Capture opportunities using volatility range indicators |
| Trending Market | ETH version | Enable trailing stop to lock profits |
| Ranging Market | Raise mp threshold | Reduce false signals |
| High-volatility Assets | BTC version | Disable sell signals, exit via ROI |

---

## IX. Applicable Market Environment Detailed Analysis

Stinkfist is a **deep-digging strategy**. Based on its code architecture and multi-layer protection mechanism, it is best suited for **high-volatility market environments**, while performing poorly during one-sided crashes.

### 9.1 Strategy Core Logic

- **Informative Layer Assistance**: Uses 1-hour timeframe's 3-day low and volatility range to determine entry timing
- **Dynamic Position Addition**: Intelligently adjusts addition strategy based on holding time and profit state
- **Global Perspective**: Considers comprehensive performance of all positions for position management
- **Price Protection**: Prevents unfavorable execution during sharp price fluctuations

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|-------------|--------|----------|
| 📈 Volatile Uptrend | ⭐⭐⭐⭐⭐ | Captures pullback buying opportunities using volatility range indicators |
| 🔄 Ranging Volatility | ⭐⭐⭐⭐☆ | Strategy design intent, effective with informative layer judgment |
| 📉 One-sided Decline | ⭐⭐☆☆☆ | Position addition logic may amplify losses |
| ⚡ Low-volatility Sideways | ⭐⭐☆☆☆ | Lacks clear trend signals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| `inf-pct-adr` | 0.80-0.92 | Controls entry position aggressiveness |
| `mp` | 30-66 | Momentum threshold, lower = more conservative |
| `stoploss` | -0.40 | Keep loose to accommodate volatility |
| Timeframe | 5m + 1h | Do not modify easily |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

The strategy contains multiple custom indicators (RMI, MA Streak, PCC, MAC), requiring deep understanding of each indicator's meaning and interactions. Recommend thorough testing in backtest environment first.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-5 pairs | 2 GB | 4 GB |
| 5-20 pairs | 4 GB | 8 GB |
| 20+ pairs | 8 GB | 16 GB |

### 10.3 Backtest vs. Live Trading Differences

The strategy relies on real-time price data and orderbook information:
- Backtest environment may not fully simulate price protection logic
- Position addition logic is more sensitive in live trading
- Cache mechanism may perform differently in backtests

### 10.4 Manual Trading Recommendations

If wanting to apply this strategy in manual trading:
1. Focus on 3-day low + 80% daily volatility range as entry zone
2. Use RMI and MA Cross to confirm trend
3. Set dynamic stop-loss instead of fixed stop-loss
4. Don't add positions blindly, wait for trend confirmation

---

## XI. Summary

**Stinkfist** is a **complex deep-digging strategy** that finds trading opportunities through multi-layered technical analysis and protection mechanisms. Its core value lies in:

1. **Informative Layer Assisted Decision**: Uses 1-hour timeframe for higher-dimensional trend judgment
2. **Dynamic Risk Management**: Adjusts strategy parameters based on holding time and profit state
3. **Global Position Perspective**: Considers comprehensive performance of all positions rather than isolated judgment

For quantitative traders, this is a strategy suitable for volatile markets, but requires full understanding of its position addition logic and price protection mechanisms before live deployment. Recommend starting with single pair testing and gradually expanding to multi-pair scenarios.

---

## XII. Sub-strategy Variants

### Stinkfist_BTC (BTC-specific Version)

```python
buy_params = {
    'inf-pct-adr': 0.91556,
    'mp': 66,
}
use_sell_signal = False  # Disable sell signals, rely on ROI exit
```

**Characteristics**: Higher entry threshold, disabled sell signals, more suitable for BTC's volatility characteristics.

### Stinkfist_ETH (ETH-specific Version)

```python
buy_params = {
    'inf-pct-adr': 0.81628,
    'mp': 40,
}
trailing_stop = True
trailing_stop_positive = 0.014
trailing_stop_positive_offset = 0.022
trailing_only_offset_is_reached = False
use_sell_signal = False
```

**Characteristics**: Enables trailing stop, parameters optimized for ETH market conditions.