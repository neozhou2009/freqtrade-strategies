# Schism3 Strategy Deep Dive

> **Strategy Number**: #378 (378th of 465 strategies)  
> **Strategy Type**: Multi-condition Rebound Trading + Cross-timeframe Filtering + Multi-currency Support  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h information layer) / 1 hour + 4 hour (sub-strategy)

---

## 1. Strategy Overview

Schism3 is a **highly configurable rebound trading strategy** with important upgrades over Schism2MM. Core innovations include: **Bounce Pending Signal System**, **Multi-currency Pair Support** (BTC/ETH stake currencies), and **Three Strategy Variants** (base, BTC, ETH versions). The strategy captures rebound signal prices and enters when prices recover, achieving more precise entry timing.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | Bounce pending signal + price confirmation + multi-timeframe filtering + multi-currency conditions |
| **Sell Conditions** | Dynamic stop-loss + RMI trend reversal + portfolio profit management |
| **Protection Mechanisms** | 5-layer protection (stop-loss, order timeout, entry confirmation, price protection, bounce price tracking) |
| **Timeframe** | 5m + 1h (base) / 1h + 4h (sub-strategy) |
| **Dependencies** | numpy, talib, qtpylib, arrow, cachetools, technical |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.05,     # Take 5% profit immediately
    "10": 0.025,   # After 10 minutes: 2.5%
    "20": 0.015,   # After 20 minutes: 1.5%
    "30": 0.01,    # After 30 minutes: 1%
    "720": 0.005,  # After 12 hours: 0.5%
    "1440": 0      # After 24 hours: no profit requirement
}

# Stop-loss setting
stoploss = -0.30  # 30% fixed stop-loss (Note: relatively high)
```

**Design Rationale**:
- ROI table spans 24 hours, suitable for **medium-to-long term holding**
- Stop-loss as high as 30%, giving greater **price volatility room**
- Combined with `ignore_roi_if_buy_signal = True`, delays exit when buy signal is valid

### 2.2 Order Type Configuration

```python
use_sell_signal = False      # Don't use standard sell signals
sell_profit_only = True      # Only sell when profitable
ignore_roi_if_buy_signal = True  # Ignore ROI when buy signal is valid
```

### 2.3 Buy Parameters

```python
buy_params = {
    'bounce-lookback': 8,        # Bounce signal lookback period
    'bounce-price': 'min',       # Bounce price takes minimum value
    'down-inf-rsi': 37,          # Downtrend 1h RSI threshold
    'down-mp': 60,               # Downtrend MP threshold
    'down-rmi-fast': 28,         # Downtrend fast RMI
    'down-rmi-slow': 35,         # Downtrend slow RMI
    'up-inf-rsi': 59,            # Uptrend 1h RSI threshold
    'xinf-stake-rmi': 70,        # Stake currency 1h RMI
    'xtf-fiat-rsi': 15,         # Fiat timeframe RSI
    'xtf-stake-rsi': 60          # Stake currency timeframe RSI
}
```

---

## 3. Buy Conditions Detailed Analysis

### 3.1 Bounce Pending Signal System (Core Innovation)

Schism3 pioneered the **bounce pending signal** mechanism, working in three steps:

#### Step 1: Detect Bounce Conditions

```python
dataframe['bounce-pending'] = np.where(
    (1h_rsi >= 37) &              # 1h RSI not too low
    (rmi-dn-trend == 1) &         # RMI downtrend
    (rmi-slow >= 35) &            # Slow RMI not oversold
    (rmi-fast <= 28) &            # Fast RMI relatively low
    (mp <= 60),                   # Momentum ping-pong not high
    1, 0
)
```

#### Step 2: Capture Bounce Price

```python
dataframe['bounce-price'] = np.where(
    bounce-pending == 1,
    close,                        # Record price at signal time
    close.rolling(8).min()        # Otherwise take 8-period lowest price
)
```

#### Step 3: Confirm Entry

```python
# Actual buy requires confirmation
(1h_rsi >= 59) &                  # Large timeframe trend confirmation
(bounce-range == 1) &              # Bounce signal within 8 periods
(rmi-up-trend == 1) &             # RMI turned to uptrend
(close >= bounce-price)           # Price recovery confirmed
```

**Logic Interpretation**:
1. First detect "might rebound" conditions
2. Record price when signal appears
3. Wait for price recovery confirmation before entering

### 3.2 Multi-currency Pair Support

When stake currency is BTC or ETH, the strategy additionally checks:

```python
if stake_currency in ('BTC', 'ETH'):
    # Timeframe conditions
    (stake_rsi < 60) | (fiat_rsi > 15)   # Stake currency not overbought OR fiat oversold
    # Information frame conditions
    stake_rmi_1h < 70                      # Stake currency 1h RMI not high
```

**Purpose**: Avoid longing altcoins when BTC/ETH are dropping sharply.

### 3.3 Add Position Logic

```python
if active_trade:
    profit_factor = 1 - (rmi-slow / 400)  # Profit factor
    rmi_grow = linear_growth(30, 70, 180, 720, open_minutes)  # Linear growth
    
    conditions.append(rmi-up-trend == 1)
    conditions.append(current_profit > peak_profit * factor)
    conditions.append(rmi-slow >= rmi_grow)
```

---

## 4. Sell Logic Detailed Analysis

### 4.1 Dynamic Stop-loss System

```python
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
# Holding 0 minutes: allow 3% loss
# Holding 300 minutes: require profit
```

### 4.2 RMI Stop-loss Signal

```python
if peak_profit > 0:
    crossed_below(rmi-slow, 50)    # Was profitable: RMI falls below 50
else:
    crossed_below(rmi-slow, 10)    # Never profitable: RMI falls below 10
```

### 4.3 Portfolio Profit Management

```python
if free_slots > 0:
    hold_pct = (1 / free_slots) * -0.04
    avg_other_profit >= hold_pct
else:
    biggest_loser == True          # Only allow biggest loser to sell
```

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Momentum | RMI(21,5), RMI(8,4) | Trend direction, overbought/oversold |
| Rate of Change | ROC(6), MP | Momentum strength measurement |
| Trend | RMI trend count | Trend confirmation |
| Bounce System | bounce-pending, bounce-price, bounce-range | Entry timing |

### 5.2 Information Timeframe Indicators (1h)

- **RSI(14)**: Confirm large timeframe trend
- **Stake Currency RMI** (BTC/ETH only): Cross-currency filtering

### 5.3 Multi-currency Frame Indicators

When stake currency is BTC or ETH:

| Indicator | Data Source | Purpose |
|-----------|-------------|---------|
| `{coin}_rsi` | COIN/USD (5m) | Coin fiat price trend |
| `{stake}_rsi` | STAKE/USD (5m) | Stake currency fiat trend |
| `{stake}_rmi_1h` | STAKE/USD (1h) | Stake currency long-term trend |

---

## 6. Risk Management Features

### 6.1 Multi-layer Stop-loss Protection

| Stop-loss Type | Trigger Condition | Description |
|----------------|-------------------|-------------|
| Fixed Stop-loss | Loss >= 30% | Hard exit (Note: relatively loose) |
| Dynamic Stop-loss | Profit < time threshold | Soft exit |
| RMI Stop-loss | RMI falls below threshold | Trend reversal |
| Portfolio Stop-loss | Overall position consideration | Fund management |
| Bounce Invalid | Price doesn't recover | Signal invalidation |

### 6.2 Order Timeout Protection

```python
def check_buy_timeout(self, pair, trade, order, **kwargs):
    if current_price > order['price'] * 1.01:  # Price deviates 1%
        return True
    return False

def check_sell_timeout(self, pair, trade, order, **kwargs):
    if current_price < order['price'] * 0.99:  # Price deviates 1%
        return True
    return False
```

### 6.3 Entry Price Protection

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, **kwargs):
    if current_price > rate * 1.01:  # Price deviates more than 1%
        return False
    return True
```

### 6.4 Bounce Price Tracking

The strategy records the price when bounce signal appears, ensuring entry only when price recovers, avoiding buying halfway down.

---

## 7. Strategy Variants

### 7.1 Schism3_BTC (BTC Stake Currency Specific)

```python
timeframe = '1h'
inf_timeframe = '4h'

buy_params = {
    'inf-rsi': 64,
    'mp': 55,
    'rmi-fast': 31,
    'rmi-slow': 16,
    'xinf-stake-rmi': 67,
    'xtf-fiat-rsi': 17,
    'xtf-stake-rsi': 57
}

minimal_roi = {
    "0": 0.05,
    "240": 0.025,   # 4 hours
    "1440": 0.01,   # 1 day
    "4320": 0       # 3 days
}
```

**Features**: Uses longer timeframes, suitable for BTC volatility characteristics.

### 7.2 Schism3_ETH (ETH Stake Currency Specific)

```python
timeframe = '1h'
inf_timeframe = '4h'

buy_params = {
    'inf-rsi': 13,
    'mp': 40,
    'rmi-fast': 42,
    'rmi-slow': 17,
    'xinf-stake-rmi': 69,
    'xtf-fiat-rsi': 15,
    'xtf-stake-rsi': 92
}
```

**Features**: Parameter optimization for ETH volatility characteristics.

---

## 8. Strategy Advantages and Limitations

### ✅ Advantages

1. **Bounce Pending Signal System**: First record signal price, confirm recovery before entry
2. **Multi-currency Support**: Automatically adapts to BTC/ETH stake currencies
3. **Configurable Parameters**: Supports per-coin-group parameter override
4. **Three Variants**: Base, BTC, ETH versions for different scenarios

### ⚠️ Limitations

1. **High Stop-loss Risk**: 30% stop-loss may bear significant drawdown
2. **Multi-data Source Dependency**: Requires additional STAKE/USD and COIN/USD data
3. **High Complexity**: Bounce system + multi-currency conditions + portfolio management
4. **Backtest Limitations**: Multi-currency conditions may need extra configuration in backtest

---

## 9. Suitable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| BTC/ETH Stake | Schism3_BTC / Schism3_ETH | Use specialized variants |
| Stablecoin Stake | Schism3 base version | Default parameters |
| High Volatility Market | Adjust stop-loss | Lower stoploss |
| Long-term Holding | Use sub-strategy | 1h+4h framework |

---

## 10. Suitable Market Environment Details

Schism3 is a **smart rebound strategy**. Based on its code architecture and community long-term live trading verification, it is most suitable for **oscillating uptrend markets** and performs poorly in **one-sided downtrends**.

### 10.1 Strategy Core Logic

- **Bounce Pending Signal**: Detect potential rebound conditions, record price
- **Price Confirmation**: Wait for price recovery confirmation before entry
- **Multi-currency Filtering**: Extra check on stake currency trend when using BTC/ETH
- **Portfolio Management**: Sell decisions considering overall positions

### 10.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:-----------:|:------------------:|----------|
| 📈 Oscillating Uptrend | ⭐⭐⭐⭐⭐ | Bounce signals precise, price confirmation effective |
| 🔄 Sideways Oscillation | ⭐⭐⭐☆☆ | Bounce signals may trigger frequently |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | 30% stop-loss may be triggered |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Bounce price tracking may fail |

### 10.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| `bounce-lookback` | 5-10 | Lookback period, increase for high volatility |
| `stoploss` | -0.15 ~ -0.25 | Adjust based on risk tolerance |
| `up-inf-rsi` | 55-65 | Trend confirmation threshold |

---

## 11. Summary

**Schism3** is a **highly configurable rebound trading strategy**. Its core value lies in:

1. **Bounce Pending Signal System**: Detect first, confirm later, avoid buying halfway down
2. **Multi-currency Support**: Automatically adapts to BTC/ETH stake currencies
3. **Strategy Variants**: Three versions for different scenarios
4. **Portfolio Management**: Smart decisions considering overall positions

For quantitative traders, this is a medium-to-high complexity strategy suitable for **oscillating uptrend markets**, requiring proper multi-currency data source configuration to achieve maximum effect.

---