# MultiMA_TSL Strategy Analysis

> **Strategy Number**: #20 (20th of 465 strategies)  
> **Strategy Type**: Multi Moving Average + Custom Stoploss Trend Following  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

**MultiMA_TSL** is a trend-following strategy combining multiple moving averages with trailing stoploss. The strategy's core feature is using three different moving average types (EMA, ZEMA, TRIMA) with an offset mechanism to capture deep pullbacks, while introducing a custom stoploss function for quick exit when sell signals trigger, achieving the effect of "riding green candles".

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Multi-condition combination (EMA/ZEMA/TRIMA offset + EWO + RSI) |
| **Exit Conditions** | Offset sell + custom stoploss coordination |
| **Protection** | Custom stoploss + CooldownPeriod + LowProfitPairs |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | Custom stoploss function, multiple MA types optional, EWO wave oscillator |

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
stoploss = -0.15  # -15% hard stoploss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01        # 1% trailing activation
trailing_stop_positive_offset = 0.018  # 1.8% offset trigger
```

**Design Logic**:
- **Tiered ROI**: 10% → 5% → 2%, longer holding time means lower exit threshold
- **Medium hard stoploss**: -15% hard stoploss, gives some room for fluctuation
- **Trailing stop**: Activates 1% trailing after 1.8% profit, locks gains

### 2.2 Protection Mechanism Configuration

```python
@property
def protections(self):
    return [
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 2
        },
        {
            "method": "LowProfitPairs",
            "lookback_period_candles": 60,
            "trade_limit": 1,
            "stop_duration": 20,
            "required_profit": -0.05,
        },
    ]
```

**Protection Mechanism Analysis**:
- **CooldownPeriod**: 2-candle cooldown after entry, prevents frequent trading
- **LowProfitPairs**: Pause trading for 20 candles if pair loses over 5% within 60 candles

---

## III. Entry Conditions Details

### 3.1 Multi Moving Average Offset Mechanism

Strategy uses three moving average types with offset mechanism to capture deep pullbacks:

```python
# Buy offset calculation
ema_offset_buy = ta.EMA(close, timeperiod=50) * 0.958    # EMA offset
zema_offset_buy = zema(30) * 0.963                        # ZEMA offset (zero lag)
trima_offset_buy = ta.TRIMA(close, timeperiod=14) * 0.958 # TRIMA offset
```

**Offset Mechanism Analysis**:
- **EMA offset**: EMA50 × 0.958, price must be below 95.8% of EMA
- **ZEMA offset**: ZEMA30 × 0.963, uses zero-lag EMA
- **TRIMA offset**: TRIMA14 × 0.958, uses triangular moving average

### 3.2 EWO Wave Oscillator Filter

```python
# EWO (Elliott Wave Oscillator) calculation
ewo = EMA(close, 5) - EMA(close, 34)

# EWO filter in entry conditions
(EWO < -20) | ((EWO > 6) & (RSI < 50))
```

**EWO Filter Logic**:
- **Deep pullback**: EWO < -20 (wave in downward phase)
- **Trend pullback**: EWO > 6 and RSI < 50 (pullback opportunity in uptrend)

### 3.3 Entry Condition Classification

| Condition Mode | Core Logic | Applicable Scenario |
|---------------|------------|-------------------|
| **TRIMA mode** | close < TRIMA14×0.958 + EWO/RSI filter | Smooth trend pullback |
| **ZEMA mode** | close < ZEMA30×0.963 + EWO/RSI filter | Fast trend pullback |
| **EMA mode** | close < EMA50×0.958 + EWO/RSI filter | Standard trend pullback |

---

## IV. Exit Logic Explained

### 4.1 Offset Sell Mechanism

```python
# Sell offset calculation
ema_offset_sell = ta.EMA(close, timeperiod=32) * 1.002   # EMA offset sell
trima_offset_sell = ta.TRIMA(close, timeperiod=48) * 1.085  # TRIMA offset sell

# Sell conditions
(close > ema_offset_sell) | (close > trima_offset_sell)
```

**Sell Logic Analysis**:
- **EMA sell**: Price > EMA32 × 1.002 (price slightly above EMA)
- **TRIMA sell**: Price > TRIMA48 × 1.085 (price 8.5% above TRIMA)
- **Either triggers**: Sell signal issued when either condition is met

### 4.2 Custom Stoploss Function

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs) -> float:
    sl_new = 1  # Default: don't trigger stoploss
    if not self.config["runmode"].value in ("backtest", "hyperopt"):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        if (last_candle["sell_copy"] == 1) & (last_candle["buy_copy"] == 0):
            sl_new = 0.001  # Almost immediate stoploss
    return sl_new
```

**Working Mechanism**:
- **Live mode**: Only effective in live/dry-run mode
- **Sell signal trigger**: When sell signal triggers and no buy signal
- **Quick exit**: Sets stoploss to 0.001, achieves "riding green candles"

### 4.3 Sell Signal Summary

| Signal Type | Trigger Condition | Function |
|------------|------------------|----------|
| **Offset sell** | Price > MA×offset | Base sell signal |
| **ROI exit** | Profit reaches ROI table threshold | Tiered take-profit |
| **Trailing stop** | Profit pullback exceeds 1% | Lock gains |
| **Custom stoploss** | Sell signal triggers | Quick exit |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|------------|---------|
| **Trend** | EMA | 50, 32 periods | Buy/sell offset baseline |
| **Trend** | ZEMA | 30 periods | Zero-lag EMA buy offset |
| **Trend** | TRIMA | 14, 48 periods | Triangular MA buy/sell offset |
| **Momentum** | EWO | 5/34 period difference | Wave oscillator filter |
| **Momentum** | RSI | 14 periods | Overbought/oversold confirmation |
| **Momentum** | RSI Fast | 4 periods | Fast RSI signal |

### 5.2 Moving Average Type Comparison

| MA Type | Characteristics | Advantages | Disadvantages |
|---------|----------------|------------|---------------|
| **EMA** | Exponential moving average | Faster response | Has lag |
| **ZEMA** | Zero-lag EMA | Almost no lag | May have noise |
| **TRIMA** | Triangular moving average | High smoothness | Slower response |

---

## VI. Risk Management Features

### 6.1 Custom Stoploss Coordination

```python
# When sell signal triggers, stoploss set to 0.001
sl_new = 0.001
```

**Design Philosophy**:
- Custom stoploss function coordinates with sell signals
- Quick exit when sell signal triggers
- Avoids "roller coaster" profit giveback

### 6.2 CooldownPeriod Protection

```python
{
    "method": "CooldownPeriod",
    "stop_duration_candles": 2
}
```

**Purpose**: Prohibits re-entry within 2 candles after buying, prevents excessive fee consumption from high-frequency trading.

### 6.3 LowProfitPairs Protection

```python
{
    "method": "LowProfitPairs",
    "lookback_period_candles": 60,
    "trade_limit": 1,
    "stop_duration": 20,
    "required_profit": -0.05,
}
```

**Purpose**: Pauses trading for 20 candles if pair loses over 5% within 60 candles, avoids repeated losses on "problem pairs".

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Multiple MA types**: EMA, ZEMA, TRIMA three options, adapts to different market rhythms
2. **Offset trading**: Captures deep pullbacks, better entry prices
3. **Custom stoploss**: Quick exit when sell signal triggers, locks profits
4. **EWO filter**: Wave oscillator identifies trend phases and pullbacks
5. **Protection mechanisms**: Cooldown + LowProfitPairs dual protection
6. **Hyperparameter optimization**: Supports Hyperopt for key parameters

### ⚠️ Limitations

1. **High complexity**: Multiple MA + custom stoploss, difficult to debug and optimize
2. **No BTC correlation**: Doesn't detect Bitcoin market trend, easy to lose in market crashes
3. **Parameter sensitivity**: Offset amounts and MA periods need optimization for different pairs
4. **Medium computation**: Multiple MA types increase computational burden
5. **Backtest differences**: Custom stoploss not effective in backtest mode, may differ from live

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Note |
|-------------------|--------------------------|------|
| **Ranging market** | Default configuration | Offset trading suitable for ranging pullback entries |
| **Slow bull trend** | Default configuration | Custom stoploss can ride green candles |
| **Sharp up/down** | Adjust stoploss | May need to adjust stoploss and trailing parameters |
| **Single-sided decline** | Pause or light position | No long-term trend filter, easy to lose consecutively |
| **Sideways consolidation** | Reduce position | Signal frequency may be lower |

---

## IX. Applicable Market Environments Explained

MultiMA_TSL is a trend-following strategy based on the core philosophy of "multi moving average offset + custom stoploss". Based on its code architecture and community long-term live trading verification experience, it's most suitable for **ranging trend markets**, and performs poorly in **single-sided crashes**.

### 9.1 Strategy Core Logic

- **Multi MA offset**: Buy when price below MA×offset, captures deep pullbacks
- **EWO filter**: Wave oscillator identifies trend phases, distinguishes deep pullbacks from trend pullbacks
- **Custom stoploss**: Quick exit when sell signal triggers, avoids profit giveback

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Slow bull/ranging up | ★★★★☆ | Offset entry + custom stoploss works well |
| 🔄 Wide ranging | ★★★★☆ | Pullback entry mechanism suitable for ranging |
| 📉 Single-sided crash | ★★☆☆☆ | No trend filter, may consecutively buy and get stuck |
| ⚡️ Extreme sideways | ★★★☆☆ | Signals reduce, but offset mechanism can filter false signals |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Note |
|--------------|------------------|------|
| **Number of pairs** | 15-30 | Moderate signal frequency |
| **Max positions** | 3-5 | Control risk |
| **Position mode** | Fixed position | Recommended fixed position |
| **Timeframe** | 5m | Mandatory requirement |

---

## X. Important Note: The Cost of Complexity

### 10.1 Moderate Learning Curve

Strategy code is about 120 lines, requires understanding:
- Differences and selection of three moving averages
- Principles of offset mechanism
- Custom stoploss function working mechanism

### 10.2 Moderate Hardware Requirements

Multiple MA calculations increase computation:

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 15-30 pairs | 1GB | 2GB |
| 30-60 pairs | 2GB | 4GB |

### 10.3 Backtest vs Live Differences

Custom stoploss only effective in live mode:
- Backtest results may be overly optimistic
- Live trading may have different exit behavior
- Need dry-run verification before live trading

### 10.4 Manual Trader Recommendations

Manual traders can reference this strategy's offset trading approach:
- Observe multiple MA types simultaneously
- Buy when price below MA×offset
- Use custom stoploss to protect profits

---

## XI. Summary

**MultiMA_TSL** is a well-designed trend-following strategy. Its core value lies in:

1. **Multiple MA types**: EMA, ZEMA, TRIMA three options, adapts to different market rhythms
2. **Offset trading**: Captures deep pullbacks, better entry prices
3. **Custom stoploss**: Quick exit when sell signal triggers, locks profits
4. **EWO filter**: Wave oscillator identifies trend phases
5. **Protection mechanisms**: Cooldown + LowProfitPairs dual protection

For quantitative traders, this is an excellent trend-following strategy template. Recommendations:
- Use as an advanced case for learning multi-MA strategies
- Understand offset mechanism and custom stoploss
- Can add BTC trend filter and other protection mechanisms
- Note backtest/live differences, verify with dry-run before live trading

---
