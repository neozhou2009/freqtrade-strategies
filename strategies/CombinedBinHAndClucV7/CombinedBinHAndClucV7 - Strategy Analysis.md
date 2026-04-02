# CombinedBinHAndClucV7 Strategy Analysis

> **Strategy Number**: #22 (22nd of 465 strategies)  
> **Strategy Type**: Bollinger Bands + Multi-Strategy Combination V7  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

**CombinedBinHAndClucV7** is the 7th version of the CombinedBinHAndCluc series, developed by iterativ. The strategy integrates multiple entry logics from BinHV45, ClucMay72018, and other strategies, and uses 1-hour informative timeframe to confirm trends. Key features include custom_stoploss and confirm_trade_exit functions.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 4 mode combination (BinHV45 + Cluc + RSI + MFI) |
| **Exit Conditions** | 2 modes (Bollinger Band upper + RSI) |
| **Protection** | Custom stoploss + Confirm trade exit + Trailing stop |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical, numpy |
| **Special Features** | 1h informative timeframe, custom stoploss |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.0181    # Immediate exit: 1.81% profit
}

# Stoploss setting
stoploss = -0.99  # -99% hard stoploss (effectively disabled)

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01      # 1% trailing activation
trailing_stop_positive_offset = 0.03  # 3% offset trigger
```

**Design Logic**:
- **Low ROI**: 1.81% ROI, pursuing quick turnover
- **Almost No Hard Stoploss**: -99% stoploss, relies on custom stoploss
- **Trailing Stop**: 1% trailing activates after 3% profit

### 2.2 Custom Stoploss

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs) -> float:
    # Manage losing trades, make room for better trades
    if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
        return 0.01  # Loss over 280 minutes, stoploss at 1%
    return 0.99  # Otherwise almost no stoploss
```

**Purpose**:
- Stoploss at 1% after loss exceeds 280 minutes (about 4.7 hours)
- Make room for better trades
- Avoid long-term holding

### 2.3 Confirm Trade Exit

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, **kwargs) -> bool:
    if sell_reason == "roi":
        if current_profit > sell_roi_profit_1:
            if last_candle["rsi"] > sell_roi_rsi_1:
                return False  # Block exit, let profits run
        # ... more conditions
    return True
```

**Purpose**:
- Block premature exit based on RSI
- Let profits run in trends

### 2.4 Hyperopt Parameters

```python
# Entry hyperopt parameters
buy_bb40_bbdelta_close = DecimalParameter(0.005, 0.04, default=0.031, space="buy")
buy_bb40_closedelta_close = DecimalParameter(0.01, 0.03, default=0.021, space="buy")
buy_bb40_tail_bbdelta = DecimalParameter(0.2, 0.4, default=0.264, space="buy")
buy_bb20_close_bblowerband = DecimalParameter(0.8, 1.1, default=0.992, space="buy")
buy_bb20_volume = IntParameter(18, 36, default=29, space="buy")
buy_rsi_diff = DecimalParameter(34.0, 60.0, default=50.48, space="buy")
buy_min_inc = DecimalParameter(0.005, 0.05, default=0.01, space="buy")
buy_rsi_1h = DecimalParameter(40.0, 70.0, default=67.0, space="buy")
buy_rsi = DecimalParameter(30.0, 40.0, default=38.5, space="buy")
buy_mfi = DecimalParameter(36.0, 65.0, default=36.0, space="buy")

# Exit hyperopt parameters
sell_rsi_main = DecimalParameter(72.0, 90.0, default=77, space="sell")
```

---

## III. Entry Conditions Explained

### 3.1 Entry Logic (4 Modes)

**Mode 1: BinHV45 Variant**
```python
(
    (close > ema_200_1h) &
    (ema_50 > ema_200) &
    (ema_50_1h > ema_200_1h) &
    (lower.shift().gt(0)) &
    (bbdelta.gt(close * buy_bb40_bbdelta_close)) &
    (closedelta.gt(close * buy_bb40_closedelta_close)) &
    (tail.lt(bbdelta * buy_bb40_tail_bbdelta)) &
    (close.lt(lower.shift())) &
    (close.le(close.shift()))
)
```

**Mode 2: ClucMay72018 Variant**
```python
(
    (close > ema_200) &
    (close > ema_200_1h) &
    (close < ema_slow) &
    (close < buy_bb20_close_bblowerband * bb_lowerband) &
    (volume < volume_mean_slow.shift(1) * buy_bb20_volume)
)
```

**Mode 3: RSI Difference**
```python
(
    (close < sma_5) &
    (ssl_up_1h > ssl_down_1h) &
    (ema_50 > ema_200) &
    (ema_50_1h > ema_200_1h) &
    (rsi < rsi_1h - buy_rsi_diff)
)
```

**Mode 4: RSI + MFI**
```python
(
    (sma_200 > sma_200.shift(20)) &
    (sma_200_1h > sma_200_1h.shift(16)) &
    (rsi_1h > buy_rsi_1h) &
    (rsi < buy_rsi) &
    (mfi < buy_mfi)
)
```

---

## IV. Exit Logic Explained

### 4.1 Technical Sell Signals

**Mode 1: Bollinger Band Upper**
```python
(
    (close > bb_upperband) &
    (close.shift(1) > bb_upperband.shift(1)) &
    (close.shift(2) > bb_upperband.shift(2))
)
```

**Mode 2: RSI Overbought**
```python
(rsi > sell_rsi_main)
```

### 4.2 Custom Stoploss

```python
if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
    return 0.01  # Loss over 280 minutes, stoploss 1%
return 0.99  # Otherwise almost no stoploss
```

### 4.3 Confirm Trade Exit

```python
if sell_reason == "roi":
    if current_profit > sell_roi_profit_1:
        if last_candle["rsi"] > sell_roi_rsi_1:
            return False  # Block exit
    elif current_profit > sell_roi_profit_2:
        if last_candle["rsi"] > sell_roi_rsi_2:
            return False  # Block exit
    elif current_profit > sell_roi_profit_3:
        if last_candle["rsi"] > sell_roi_rsi_3:
            return False  # Block exit
return True
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|---------|---------|------|------|
| **Volatility** | Bollinger Bands | 40 periods, 2x std dev | BinHV45 variant |
| **Volatility** | Bollinger Bands | 20 periods, 2x std dev | Cluc variant |
| **Trend** | EMA | 50, 200 periods | Trend judgment |
| **Trend** | SMA | 200 periods | Trend judgment |
| **Momentum** | RSI | 14 periods | Overbought/Oversold |
| **Momentum** | MFI | 14 periods | Money flow |
| **Trend** | SSL Channels | 20 periods | Trend direction |

### 5.2 Informative Timeframe (1h)

The strategy uses 1-hour informative timeframe:

| Indicator | Purpose |
|------|------|
| ema_50_1h | 1h medium-term trend |
| ema_200_1h | 1h long-term trend |
| sma_200_1h | 1h long-term trend |
| rsi_1h | 1h overbought/oversold |
| ssl_down_1h, ssl_up_1h | 1h trend direction |

---

## VI. Risk Management Features

### 6.1 Custom Stoploss

```python
if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
    return 0.01
```

**Purpose**:
- Stoploss at 1% after loss exceeds 280 minutes
- Make room for better trades
- Avoid long-term holding

### 6.2 Confirm Trade Exit

```python
if current_profit > sell_roi_profit_1:
    if last_candle["rsi"] > sell_roi_rsi_1:
        return False  # Block exit
```

**Purpose**:
- Block premature exit based on RSI
- Let profits run in trends

### 6.3 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.03
trailing_only_offset_is_reached = True
```

**Working Mechanism**:
1. Trailing stop activates after 3% profit
2. Exit triggers when 1% pullback from highest point

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Multi-Strategy Combination**: 4 entry modes, covering different scenarios
2. **Informative Timeframe**: 1h confirms trend, reduces false signals
3. **Custom Stoploss**: Manages losing trades, frees up space
4. **Confirm Trade Exit**: Blocks premature exit based on RSI
5. **Hyperopt Optimization**: Supports Hyperopt for key parameters
6. **Trailing Stop**: Locks profits, protects gains

### ⚠️ Limitations

1. **High Complexity**: Multi-strategy + multi-indicator, difficult to debug
2. **No BTC Correlation**: Does not detect Bitcoin market trend
3. **Parameter Sensitive**: Hyperopt results may overfit
4. **High Computation**: Multi-indicator + informative timeframe increases computation
5. **Almost No Hard Stoploss**: -99% stoploss relies on custom stoploss

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Ranging Market** | Default configuration | Multi-strategy combination suitable for ranging markets |
| **Uptrend** | Default configuration | Informative timeframe + trailing stop performs well |
| **Downtrend** | Pause or light position | Informative timeframe blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Applicable Market Environments

CombinedBinHAndClucV7 is a strategy based on the core philosophy of "multi-strategy combination + informative timeframe".

### 9.1 Strategy Core Logic

- **Multi-Strategy Combination**: 4 entry modes, covering different scenarios
- **Informative Timeframe**: 1h confirms trend, reduces false signals
- **Custom Stoploss**: Manages losing trades
- **Confirm Trade Exit**: Let profits run

### 9.2 Performance in Different Markets

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ★★★★★ | Multi-strategy + informative timeframe + trailing stop, perfect match |
| 🔄 Wide Ranging | ★★★★☆ | Multi-strategy combination suitable for ranging markets |
| 📉 Single-sided Crash | ★★★☆☆ | Informative timeframe blocks most trades, auto lies flat |
| ⚡️ Extreme Sideways | ★★★☆☆ | Too little volatility, signals decrease |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------|--------|------|
| **Number of Pairs** | 20-60 | Recommended 20-60 pairs |
| **Max Open Trades** | 4-6 | Recommended 4-6 open trades |
| **Position Mode** | Unlimited stake | Recommended unlimited stake |
| **Timeframe** | 5m | Mandatory requirement |

---

## X. Important Notes: Informative Timeframe Usage

### 10.1 High Learning Cost

Strategy code is about 300 lines, requires understanding multi-strategy combination, informative timeframe, custom stoploss concepts.

### 10.2 Moderate Hardware Requirements

Multi-indicator + informative timeframe increases computation:

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------|---------|---------|
| 20-40 pairs | 1GB | 2GB |
| 40-80 pairs | 2GB | 4GB |

### 10.3 Informative Timeframe Advantages

- **Trend Confirmation**: 1h trend more reliable than 5m
- **Reduces False Signals**: Only trades when 1h trend is up
- **Auto Lies Flat**: Auto stops trading when 1h trend is down

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's multi-strategy approach:
- Observe both 5m and 1h trends simultaneously
- Use multi-strategy combination to cover different scenarios
- Set custom stoploss to manage losing trades

---

## XI. Summary

**CombinedBinHAndClucV7** is a well-designed multi-strategy combination strategy, its core value lies in:

1. **Multi-Strategy Combination**: 4 entry modes, covering different scenarios
2. **Informative Timeframe**: 1h confirms trend, reduces false signals
3. **Custom Stoploss**: Manages losing trades, frees up space
4. **Confirm Trade Exit**: Blocks premature exit based on RSI
5. **Hyperopt Optimization**: Supports Hyperopt for key parameters
6. **Trailing Stop**: Locks profits, protects gains

For quantitative traders, this is an excellent multi-strategy learning template. Recommendations:
- Use as an advanced case for learning multi-strategy combination
- Understand informative timeframe usage
- Learn custom stoploss and confirm trade exit
- Note that hyperopt parameters may overfit, testthoroughly before live trading

---
