# RalliV1_disable56 Strategy In-Depth Analysis

> **Strategy ID**: #344 (344th out of 465 strategies)
> **Strategy Type**: Multi-condition Trend Following + Elliott Wave Oscillator Fusion Strategy
> **Timeframe**: 5 minutes (5m) + 1 hour information layer (1h)

---

## I. Strategy Overview

RalliV1_disable56 is a trend following strategy based on Elliott Wave Oscillator (EWO) and multiple moving average cross combinations. Developed by @Rallipanos, this strategy identifies entry opportunities during market pullbacks by detecting price deviation from moving averages, combined with RSI momentum indicators and EWO oscillator. The "disable56" in the strategy name indicates that this version disables buy conditions #5 and #6 from the original strategy.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 4 independent buy signals, divided into bear market (MA<EMA100) and bull market (MA>EMA100) scenarios |
| **Sell Conditions** | 2 base sell signals, combining trend reversal and price breakthrough determination |
| **Protection Mechanisms** | Custom stop-loss + trailing stop + time stop triple protection |
| **Timeframe** | 5m main timeframe + 1h information timeframe |
| **Dependencies** | talib, numpy, pandas, qtpylib, technical |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.04,     # Immediately: 4% profit
    "40": 0.032,   # After 40 minutes: 3.2% profit
    "87": 0.018,   # After 87 minutes: 1.8% profit
    "201": 0       # After 201 minutes: any profit can exit
}

# Stop-loss setting
stoploss = -0.3   # 30% fixed stop-loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.005        # 0.5% positive trailing
trailing_stop_positive_offset = 0.03  # 3% activation threshold
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- ROI uses tiered decreasing design, encouraging longer holding while locking minimum profits
- 30% fixed stop-loss is relatively loose, relying on trailing stop to protect profits
- Trailing stop activates at 3% profit, trailing 0.5% positively, balancing profit protection with volatility tolerance

### 2.2 Order Type Configuration

```python
order_time_in_force = {
    'buy': 'gtc',   # Good Till Cancelled
    'sell': 'gtc'
}
```

### 2.3 Optimizable Parameters

| Parameter Type | Parameter Name | Range | Default |
|---------------|----------------|-------|---------|
| **Buy Parameters** | base_nb_candles_buy | 5-80 | 14 |
| | low_offset | 0.9-0.99 | 0.975 |
| | low_offset_2 | 0.9-0.99 | 0.955 |
| | ewo_high | 2.0-12.0 | 2.327 |
| | ewo_high_2 | -6.0-12.0 | -2.327 |
| | ewo_low | -20.0--8.0 | -20.988 |
| | rsi_buy | 30-70 | 60 |
| | rsi_buy_2 | 30-70 | 45 |
| **Sell Parameters** | base_nb_candles_sell | 5-80 | 24 |
| | high_offset | 0.95-1.1 | 0.991 |
| | high_offset_2 | 0.99-1.5 | 0.997 |

---

## III. Buy Conditions In Detail

### 3.1 Core Technical Indicators

The strategy uses the following indicators to build buy logic:

| Indicator | Parameters | Purpose |
|-----------|-----------|---------|
| **MA_buy** | EMA(variable period, default 14) | Dynamic buy baseline |
| **MA_sell** | EMA(variable period, default 24) | Dynamic sell baseline |
| **EMA_100** | 100-period EMA | Trend direction determination |
| **SMA_9** | 9-period SMA | Short-term trend confirmation |
| **HMA_50** | 50-period Hull MA | Smooth trend line |
| **EWO** | 5/200 EMA difference | Elliott Wave Oscillator |
| **RSI** | 14-period | Momentum indicator |
| **RSI_fast** | 4-period | Fast momentum |
| **RSI_slow** | 20-period | Slow momentum |

### 3.2 Four Buy Conditions In Detail

#### Condition #1: Bear Market EWO High Positive Value Buy
```python
# Logic
- MA_buy < EMA_100 (in downtrend)
- SMA_9 < MA_buy (short-term confirms downtrend)
- RSI_fast between 4-35 (oversold but not extreme)
- Close price < MA_buy * 0.975 (price deviation)
- EWO > 2.327 (momentum strengthening)
- RSI < 45 (not overheated)
- Volume > 0
- Close price < MA_sell * 0.991 (sell pressure still exists)
```

#### Condition #2: Bear Market EWO Negative-to-Positive Buy (Deep Drop Reversal)
```python
# Logic
- MA_buy < EMA_100 (bear market)
- SMA_9 < MA_buy (confirms downtrend)
- RSI_fast between 4-35
- Close price < MA_buy * 0.955 (greater deviation)
- EWO > -2.327 (momentum improving)
- RSI < 25 (deep oversold)
- RSI < 45 (confirms oversold)
```

#### Condition #3: Bear Market EWO Extreme Negative Value Buy
```python
# Logic
- MA_buy < EMA_100 (bear market)
- SMA_9 < MA_buy (confirms downtrend)
- RSI_fast between 4-35
- Close price < MA_buy * 0.975
- EWO < -20.988 (extreme oversold)
- Volume > 0
```

#### Condition #4: Bull Market Pullback Buy
```python
# Logic
- MA_buy > EMA_100 (bull market)
- RSI_fast between 4-35 (short-term oversold)
- Close price < MA_buy * 0.975 (pullback buy)
- EWO > 2.327 (momentum maintained)
- RSI < 60 (not overheated)
- Volume > 0
```

### 3.3 Buy Conditions Classification

| Condition Group | Condition # | Core Logic |
|----------------|------------|------------|
| Bear Market Reversal | #1, #2, #3 | Below EMA100, catching oversold rebounds |
| Bull Market Pullback | #4 | Above EMA100, catching trend pullbacks |

---

## IV. Sell Logic In Detail

### 4.1 Multi-Layer Take-Profit System

The strategy uses a tiered take-profit mechanism:

```
Profit Range       Threshold    Signal Name
──────────────────────────────────
0-40 minutes       4%           ROI_1
40-87 minutes      3.2%         ROI_2
87-201 minutes     1.8%         ROI_3
After 201 minutes  0%           ROI_4 (any profit)
```

### 4.2 Custom Stop-Loss Logic

```python
def custom_stoploss(...):
    # If held over 140 minutes and profit < 0.1%, force stop
    if current_profit < 0.001 and current_time - timedelta(minutes=140) > trade.open_date_utc:
        return -0.005  # -0.5% stop-loss
    return 1  # Otherwise maintain original stop-loss logic
```

### 4.3 Two Sell Signals

**Sell Signal #1: Bull Market Trend Reversal**
```python
# Conditions
- HMA_50 > EMA_100 (long-term trend upward)
- Close price > SMA_9 (breaking short-term MA)
- Close price > MA_sell * 0.997 (breaking sell baseline)
- RSI_fast > RSI_slow (momentum accelerating)
- Volume > 0
```

**Sell Signal #2: Bear Market Price Breakthrough**
```python
# Conditions
- Close price < EMA_100 (still in bear market)
- Close price > MA_sell * 0.991 (breaking short-term baseline)
- RSI_fast > RSI_slow (momentum improving)
- Volume > 0
```

### 4.4 Sell Confirmation Filter

```python
def confirm_trade_exit(...):
    # If sell_signal and RSI < 45 and HMA_50 > EMA_100, reject sell
    if sell_reason == 'sell_signal':
        if last_candle['rsi'] < 45 and last_candle['hma_50'] > last_candle['ema_100']:
            return False
    return True
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|--------------------|--------------------|---------|
| **Moving Averages** | EMA(variable), EMA_100, EMA_14, EMA_9, SMA_9, HMA_50 | Trend determination and price deviation calculation |
| **Oscillators** | EWO (5/200 EMA difference) | Elliott Wave momentum analysis |
| **Momentum** | RSI(14), RSI_fast(4), RSI_slow(20) | Overbought/oversold determination |

### 5.2 Elliott Wave Oscillator (EWO)

```python
def EWO(dataframe, ema_length=5, ema2_length=200):
    ema1 = ta.EMA(df, timeperiod=ema_length)   # Fast line
    ema2 = ta.EMA(df, timeperiod=ema2_length)  # Slow line
    emadif = (ema1 - ema2) / df['low'] * 100   # Normalized difference
    return emadif
```

EWO is the core indicator of this strategy, used to determine market momentum:
- Positive value > 2.327: Strong momentum, suitable for buying
- Negative value < -20.988: Extreme oversold, bounce opportunity

---

## VI. Risk Management Features

### 6.1 Triple Stop-Loss Protection

| Protection Type | Parameter | Description |
|----------------|-----------|-------------|
| **Fixed Stop-Loss** | -30% | Last line of defense, prevents single huge loss |
| **Trailing Stop** | 0.5% @ 3% profit | Locks floating profits |
| **Time Stop** | 140 minutes @ 0.1% profit | Avoids long-term capital occupation |

### 6.2 Sell Signal Filter

The strategy implements smart filtering in `confirm_trade_exit`:
- When RSI < 45 and HMA_50 > EMA_100, reject sell signal
- Prevents premature exit during upward trend

### 6.3 Scenario-Based Buy/Sell Logic

- **Bear Market (MA < EMA100)**: Three buy conditions, more aggressively catching reversals
- **Bull Market (MA > EMA100)**: One buy condition, cautious pullback buying

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-scenario adaptation**: Both bear market reversal and bull market pullback have corresponding buy conditions
2. **EWO unique indicator**: Uses Elliott Wave Oscillator to identify momentum changes, rarely used
3. **Dynamic parameter optimization**: Many parameters support Hyperopt optimization, tunable for different coins
4. **Triple stop-loss protection**: Fixed + trailing + time stop, comprehensive risk management

### ⚠️ Limitations

1. **Parameter sensitive**: Multiple parameters rely on optimization, possible overfitting risk
2. **EWO extreme values fixed**: ewo_low = -20.988 may not apply to all markets
3. **Few sell conditions**: Only 2 sell signals, may miss some exit opportunities
4. **Fixed timeframe**: Only supports 5m, not suitable for other time cycles

---

## VIII. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|--------------------------|-------------|
| Oscillating market | Enable all conditions | Many oversold reversal opportunities |
| Slow bull | Focus on condition #4 | Pullback buying works well |
| Rapid decline | Enable condition #3 | Extreme oversold catching |
| Sideways consolidation | Reduce trading frequency | Avoid RSI false signals |

---

## IX. Applicable Market Environment In Detail

RalliV1_disable56 is a variant of the Rallipanos strategy series. Based on its code architecture and community long-term live trading verification experience, it is most suitable for **oscillating downward markets**, while performing average in **one-sided surges**.

### 9.1 Core Strategy Logic

- **EWO driven**: Identifies momentum reversal points through Elliott Wave Oscillator
- **Trend filtering**: Uses EMA100 to distinguish bull and bear markets, applying different strategies
- **Price deviation**: Uses MA deviation to catch oversold opportunities
- **Multiple confirmation**: RSI + EWO + MA triple confirmation, reduces false signals

### 9.2 Performance in Different Markets

| Market Type | Rating | Reason Analysis |
|:-----------:|:------:|-----------------|
| 📈 Slow bull trend | ⭐⭐⭐⭐☆ | Pullback buying works well, trailing take-profit locks gains |
| 🔄 Oscillating market | ⭐⭐⭐⭐⭐ | Frequent overbought/oversold alternation, strategy design perfectly adapts |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Many bear market conditions, but reversal timing hard to grasp |
| ⚡️ Rapid surge | ⭐⭐☆☆☆ | Strategy is conservative, may miss strong rallies |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------------|-------------------|-------------|
| ewo_high | 2.0-3.0 | Too high misses opportunities, too low false signals |
| ewo_low | -15.0--25.0 | Adjust based on coin volatility |
| trailing_stop_positive | 0.005-0.01 | High volatility coins can increase slightly |
| Timeframe | 5m | Recommend 5 minutes, other cycles need re-optimization |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

This strategy uses Elliott Wave Oscillator and multiple MA combinations, need to understand:
- EWO indicator meaning and extreme value determination
- Different MA period trend significance
- RSI_fast and RSI_slow crossover signals

### 10.2 Hardware Requirements

| Trading Pairs | Minimum Memory | Recommended Memory |
|--------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Backtest vs. Live Trading Differences

- Strategy uses `process_only_new_candles = True`, backtest and live behavior consistent
- Custom stop-loss function executed correctly in backtest
- Note `startup_candle_count = 200`, need sufficient historical data

### 10.4 Manual Trader Recommendations

If want to manually use this strategy's signals:
1. Focus on EWO rising from extreme negative values
2. Combine EMA100 to determine current bull or bear market
3. Start watching entry when RSI_fast < 35
4. Don't chase highs, wait for pullbacks after MA deviation

---

## XI. Summary

**RalliV1_disable56** is a **multi-scenario trend following strategy based on Elliott Wave Oscillator**. Its core value lies in:

1. **Dual-scenario adaptation**: Bull and bear markets each have buy logic, not afraid of market transitions
2. **Momentum reversal catching**: EWO indicator identifies oversold rebounds, unique and effective
3. **Triple stop-loss protection**: Fixed + trailing + time stop, comprehensive risk control

For quantitative traders, this is a stable strategy suitable for **oscillating markets**, but need to pay attention to parameter optimization to avoid overfitting, recommend sufficient testing in simulation environment first.