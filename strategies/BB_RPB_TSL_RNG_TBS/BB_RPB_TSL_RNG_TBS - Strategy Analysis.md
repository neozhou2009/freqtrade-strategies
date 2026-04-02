# BB_RPB_TSL_RNG_TBS Strategy In-Depth Analysis

> **Strategy Number**: #444 (444th of 465 strategies)  
> **Strategy Type**: Bollinger Bands Breakout + Pullback Buy + Custom Trailing Stop + Trailing Buy  
> **Timeframe**: 5 minutes (5m) + Dynamic Information Layer

---

## I. Strategy Overview

BB_RPB_TSL_RNG_TBS is an enhanced version of BB_RPB_TSL_RNG_2, adding a **Trailing Buy Strategy (TBS)** mechanism. The TBS in the strategy name represents Trailing Buy Strategy, meaning that after a buy signal appears, the strategy doesn't immediately place an order but waits for the price to fall further before buying, thereby obtaining a better entry price.

### Core Features

| Feature | Description |
|------|------|
| **Buy Conditions** | 7 independent buy signals + trailing buy mechanism |
| **Sell Conditions** | 2 groups of sell signal combinations + custom trailing stop |
| **Protection Mechanism** | Tiered trailing stop (3 levels) + trailing buy protection |
| **Timeframe** | 5m main framework |
| **Dependencies** | qtpylib, numpy, talib, pandas_ta, technical |
| **Special Features** | Trailing buy (live/dry_run mode only) |
| **Compatibility** | Does not support backtesting/Hyperopt |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table - Fixed 10% Take Profit
minimal_roi = {
    "0": 0.10,
}

# Stop Loss Setting - Fixed 10% (overridden by custom stop)
stoploss = -0.10

# Enable Custom Trailing Stop
use_custom_stoploss = True
use_sell_signal = True
process_only_new_candles = True  # Process only new candles, reduce computational overhead
```

### 2.2 Tiered Trailing Stop Parameters

```python
# Hard Stop Loss (when at loss)
pHSL = -0.178  # -17.8%

# Level 1: Triggered at 1.9% profit
pPF_1 = 0.019
pSL_1 = 0.019

# Level 2: Triggered at 6.5% profit
pPF_2 = 0.065
pSL_2 = 0.062
```

### 2.3 Trailing Buy Parameters

```python
# TrailingBuyStrat2 Class Parameters
trailing_buy_order_enabled = True  # Enable trailing buy
trailing_expire_seconds = 1800  # 30-minute timeout

# Trailing Buy Upper Limit Control
trailing_buy_max_stop = 0.02   # Stop tracking when price is 2% above starting price
trailing_buy_max_buy = 0.000   # Buy when price is below starting price

# Upward Trend Quick Buy (Optional)
trailing_buy_uptrend_enabled = False  # Disabled by default
trailing_expire_seconds_uptrend = 90  # 90-second timeout
min_uptrend_trailing_profit = 0.02  # Minimum trailing profit
```

---

## III. Trailing Buy Mechanism Detailed Analysis

### 3.1 Trailing Buy Working Principle

The core idea of trailing buy: **After a buy signal appears, wait for the price to continue falling, then enter at a better price**.

```
Timeline:

Time  Price    Action
─────────────────────────────────
T0    100    Buy signal appears, start tracking
T1    99     Price falls, update upper limit
T2    98     Price continues falling, update upper limit
T3    99     Price rebounds, trigger buy!
─────────────────────────────────
      Entry Price: 99 (better than signal price 100)
```

### 3.2 Trailing Buy State Machine

```python
init_trailing_dict = {
    'trailing_buy_order_started': False,  # Whether tracking has started
    'trailing_buy_order_uplimit': 0,      # Current upper limit price
    'start_trailing_price': 0,            # Starting tracking price
    'buy_tag': None,                      # Buy tag
    'start_trailing_time': None,          # Tracking start time
    'offset': 0,                          # Current offset value
    'allow_trailing': False,              # Whether trailing is allowed
}
```

### 3.3 Trailing Buy Trigger Conditions

| Scenario | Condition | Action |
|------|------|------|
| Start Tracking | buy signal + allow_trailing | Record starting price, wait |
| Price Falls | current < uplimit | Update upper limit price |
| Price Rebounds | current > uplimit and current < start * (1 + max_buy) | **Trigger Buy** |
| Price Too High | current > start * (1 + max_stop) | Stop tracking |
| Timeout | Exceed 1800 seconds | Stop tracking or force buy |

### 3.4 Trailing Buy Offset Function

```python
def trailing_buy_offset(self, dataframe, pair, current_price):
    current_trailing_profit_ratio = (start_price - current_price) / start_price
    
    # Tiered offset
    trailing_buy_offset = {
        0.06: 0.02,  # Price falls 6%, buy on 2% rebound
        0.03: 0.01,  # Price falls 3%, buy on 1% rebound
        0: 0.005,    # Default: buy on 0.5% rebound
    }
    
    # Timeout force buy
    if duration > 1800 seconds and profit > 0 and buy_signal_active:
        return 'forcebuy'
    
    # Price above starting price, return default offset
    if profit_ratio < 0:
        return 0.005
```

---

## IV. Buy Conditions Detailed Analysis

### 4.1 Seven Base Buy Conditions (Inherited from BB_RPB_TSL_RNG_2)

| Condition Number | Condition Name | Core Logic | Buy Tag |
|---------|---------|---------|---------|
| #1 | BB_checked | Oversold + Breakout combination | bb |
| #2 | local_uptrend | Uptrend pullback | local uptrend |
| #3 | ewo | Elliott Wave pullback | ewo |
| #4 | ewo_2 | EWO momentum upward | ewo2 |
| #5 | cofi | Stochastic golden cross confirmation | cofi |
| #6 | nfi_32 | Deep pullback | nfi 32 |
| #7 | nfi_33 | Extreme oversold rebound | nfi 33 |

### 4.2 Trailing Buy Enhancement Logic

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force, **kwargs):
    # Enable trailing buy only in live/dry_run mode
    if self.trailing_buy_order_enabled and self.config['runmode'].value in ('live', 'dry_run'):
        
        # Get latest candle data
        dataframe = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        current_price = rate
        
        # Trailing buy logic
        if trailing_buy['allow_trailing']:
            if buy_signal and not trailing_started:
                # Start tracking
                start_trailing(price, buy_tag)
            elif price_rebounds:
                # Trigger buy
                return True
            elif price_too_high:
                # Stop tracking
                reset_trailing()
```

---

## V. Sell Logic Detailed Analysis

### 5.1 Sell Signal Combinations (Same as BB_RPB_TSL_RNG_2)

**Sell Condition Group 1**:
```python
(close > sma_9) &
(close > ma_sell * high_offset_2) &
(rsi > 50) &
(volume > 0) &
(rsi_fast > rsi_slow)
```

**Sell Condition Group 2**:
```python
(sma_9 > sma_9.shift(1) * 1.005) &
(close < hma_50) &
(close > ma_sell * high_offset) &
(volume > 0) &
(rsi_fast > rsi_slow)
```

### 5.2 Sell Parameter Differences

| Parameter | RNG_2 Default | RNG_TBS Default | Description |
|------|-------------|---------------|------|
| base_nb_candles_sell | 23 | 24 | Sell MA period |
| high_offset | 1.051 | 0.991 | High position offset |
| high_offset_2 | 1.02 | 0.997 | Low position offset |
| sell_btc_safe | -325 | -389 | BTC protection threshold |

**Difference Interpretation**: TBS version sell offsets are more conservative (<1), meaning sell signals trigger faster.

---

## VI. Technical Indicator System

### 6.1 Core Indicators (Same as RNG_2)

| Indicator Category | Specific Indicators | Usage |
|---------|---------|------|
| Bollinger Bands | BB(20,2), BB(20,3) | Price channel, breakout signals |
| EMA | EMA(8,12,13,16,26,100) | Trend judgment |
| SMA | SMA(9,15,30) | Price MA |
| RSI | RSI(4,14,20) | Overbought/oversold |
| CCI | CCI(26,170) | Commodity Channel Index |
| RMI | RMI(variable period) | Relative Momentum |
| EWO | Elliott Wave(50,200) | Wave Oscillator |
| HMA | HMA(50) | Hull Moving Average |
| Williams %R | WR(14) | Overbought/oversold |
| CTI | CTI(20) | Relative Trend |

### 6.2 Dynamic Information Layer Configuration

```python
def informative_pairs(self):
    # Dynamically get quote currency for current trading pair
    if self.config['stake_currency'] in ['USDT','BUSD','USDC','DAI','TUSD','PAX','USD','EUR','GBP']:
        btc_info_pair = f"BTC/{self.config['stake_currency']}"
    else:
        btc_info_pair = "BTC/USDT"
    
    informative_pairs.append((btc_info_pair, self.timeframe))
```

**Design Advantage**: Automatically adapts to exchanges with different quote currencies.

---

## VII. Risk Management Features

### 7.1 Dual Trailing Mechanism

| Trailing Type | Direction | Purpose |
|---------|------|------|
| Trailing Buy | Before buying | Obtain better entry price |
| Trailing Stop | After buying | Lock in profits, limit losses |

### 7.2 Trailing Buy Risk Control

```python
# Price rise upper limit
trailing_buy_max_stop = 0.02  # Stop tracking when price is 2% above starting price

# Price fall buy
trailing_buy_max_buy = 0.000  # Buy when price is below starting price

# Time limit
trailing_expire_seconds = 1800  # 30-minute timeout
```

### 7.3 Trailing Buy Important Notes

⚠️ **Important Warning**: Trailing buy functionality is **NOT compatible with backtesting and Hyperopt**!

Reasons:
- Backtesting assumes immediate execution when buy signal appears
- Trailing buy relies on real-time price changes
- Cannot simulate trailing process in historical data

---

## VIII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Better Entry Price**: Trailing buy mechanism may obtain lower entry prices
2. **Dual Trailing Protection**: Track price before buying, track stop loss after buying
3. **Dynamic Adaptation**: Automatically adapts to different quote currencies
4. **Time Efficiency**: process_only_new_candles reduces computational overhead
5. **Inherits Complete Logic**: Retains all buy conditions from BB_RPB_TSL_RNG_2

### ⚠️ Limitations

1. **No Backtesting Support**: Trailing buy cannot be properly simulated in backtesting
2. **No Hyperopt Support**: Parameter optimization must use base version
3. **Live Trading Depends on Real-Time Prices**: API latency may affect trailing效果
4. **Higher Parameter Complexity**: Additional trailing buy parameters
5. **Timeout Risk**: 30-minute timeout may miss entry opportunities

---

## IX. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| Volatile Rise | Enable trailing buy | Obtain better entry price |
| Fast Trend | Disable trailing buy | Buy immediately when signal appears |
| Low Volatility | Adjust timeout parameters | Increase timeout time waiting for entry |
| High Volatility | Tighten trailing parameters | Reduce waiting time |

---

## X. Comparison with BB_RPB_TSL_RNG_2

### 10.1 Core Differences

| Feature | RNG_2 | RNG_TBS |
|------|-------|---------|
| Trailing Buy | ❌ | ✅ |
| Backtesting Support | ✅ | ❌ |
| Hyperopt Support | ✅ | ❌ |
| Information Pair Configuration | Fixed BTC/USDT | Dynamic adaptation |
| Sell Offset | Conservative | More conservative |
| Calculation Mode | Per tick | Only new candles |

### 10.2 Usage Recommendations

| Scenario | Recommended Version |
|------|---------|
| Backtesting/Parameter Optimization | BB_RPB_TSL_RNG_2 |
| Live Trading (Pursuing Better Entry) | BB_RPB_TSL_RNG_TBS |
| Live Trading (Pursuing Speed) | BB_RPB_TSL_RNG_2 |

---

## XI. Summary

**BB_RPB_TSL_RNG_TBS** is the **live trading enhanced version** of BB_RPB_TSL_RNG_2. Its core value lies in:

1. **Trailing Buy**: Wait for price to fall further before entering, may obtain better prices
2. **Dual Trailing**: Track price before buying, track stop loss after buying, full-process protection
3. **Dynamic Adaptation**: Automatically adapts to exchanges with different quote currencies
4. **Inherits Complete Logic**: Retains all mature buy conditions from base version

For quantitative traders:
- **Parameter Optimization Phase**: Use BB_RPB_TSL_RNG_2 for backtesting and Hyperopt
- **Live Trading Deployment Phase**: Use BB_RPB_TSL_RNG_TBS for trailing buy advantages
- **Run Simultaneously**: Can use both versions on different trading pairs for comparison
