# SMA_BBRSI Strategy Deep Dive

> **Strategy ID**: #367 (367th of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + RSI Bollinger Bands + Custom Stop Loss  
> **Timeframe**: 5 minutes (5m) + 1-hour informational layer

---

## I. Strategy Overview

SMA_BBRSI is a composite quantitative trading strategy that integrates Simple Moving Average (SMA) offset, Elliott Wave Oscillator (EWO), RSI Bollinger Bands, and anti-pump mechanisms. Through the combination and validation of multiple technical indicators, the strategy captures trend reversal opportunities while utilizing multi-layered protection mechanisms to reduce risk exposure.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 independent buy signals, individually optimizable via parameters |
| **Sell Conditions** | 2 base sell signals + custom dynamic stop loss |
| **Protection Mechanisms** | 3 protection parameter groups (LowProfitPairs, MaxDrawdown, Anti-pump threshold) |
| **Timeframe** | Main timeframe 5m + informational timeframe 1h |
| **Dependencies** | talib, numpy, pandas_ta, technical, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.028,    # Immediate 2.8% profit target
    "10": 0.018,   # After 10 candles: 1.8%
    "30": 0.010,   # After 30 candles: 1.0%
    "40": 0.005    # After 40 candles: 0.5%
}

# Stop loss setting
stoploss = -0.10   # Fixed stop loss at -10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.001
trailing_stop_positive_offset = 0.01
trailing_only_offset_is_reached = True
```

**Design Rationale**:
- ROI uses a tiered declining structure to quickly lock in small profits
- Fixed stop loss at -10% provides baseline protection
- Trailing stop activates after 1% profit, allowing profits to run further

### 2.2 Order Type Configuration

```python
# Order types (using default configuration)
order_time_in_force = {
    'buy': 'gtc',
    'sell': 'gtc',
}
```

### 2.3 Custom Dynamic Stop Loss System

The strategy implements a tiered dynamic stop loss mechanism:

```python
# Dynamic stop loss parameters
pHSL = -0.178    # Hard stop loss profit threshold
pPF_1 = 0.01     # Profit threshold 1 (1%)
pSL_1 = 0.009    # Stop loss level 1 (0.9%)
pPF_2 = 0.048    # Profit threshold 2 (4.8%)
pSL_2 = 0.043    # Stop loss level 2 (4.3%)
```

**Dynamic Stop Loss Logic**:
- Profit < 1%: Use hard stop loss at -17.8%
- Profit between 1% - 4.8%: Linear interpolated stop loss (0.9% - 4.3%)
- Profit > 4.8%: Stop loss floats upward with profit

---

## III. Buy Conditions Detailed

### 3.1 Protection Mechanisms (3 Groups)

The strategy has built-in triple protection mechanisms:

| Protection Type | Parameter Description | Default Value |
|-----------------|----------------------|---------------|
| **Anti-pump** | antipump_threshold | 0.25 |
| **LowProfitPairs** | Pause trading for 60 minutes after 5% loss | trade_limit=1 |
| **MaxDrawdown** | Circuit breaker at 20% max drawdown | lookback=24 candles |

### 3.2 Three Buy Conditions Detailed

#### Condition #1: EMA Offset + EWO High + RSI Low Combination

```python
# Logic
- Close < EMA(buy_candles) × low_offset (price below MA * 0.973)
- EWO > ewo_high (5.672) (EWO indicator shows upward momentum)
- RSI < rsi_buy (59) (RSI not overbought)
- Volume > 0
```

**Applicable Scenario**: Pullback buying opportunities in an uptrend

#### Condition #2: EMA Offset + EWO Low Combination

```python
# Logic
- Close < EMA(buy_candles) × low_offset (price below MA * 0.973)
- EWO < ewo_low (-19.931) (EWO shows oversold condition)
- Volume > 0
```

**Applicable Scenario**: Bottom-fishing opportunities after deep decline

#### Condition #3: RSI Bollinger Bands + EWO Validation Combination (Most Complex)

```python
# Logic
- RSI < basis - (dev × for_sigma) (RSI below Bollinger lower band)
- EWO in reasonable range:
  - (EWO > ewo_high_bb AND EWO < 10) OR
  - (EWO >= 10 AND RSI < 40)
- RSI(4) < 25 (Short-term RSI oversold)
- CCI(fast) < 100 (CCI not overbought)
- moderi_96 == True (Long-term trend upward)
- Volume > 0
```

**Applicable Scenario**: Multi-indicator confluence oversold reversal signal

### 3.3 Three Buy Conditions Classification

| Condition Group | Condition # | Core Logic |
|-----------------|-------------|-----------|
| **Trend Pullback** | #1 | EMA offset + EWO confirmation + RSI filter |
| **Deep Bottom-Fishing** | #2 | EMA offset + EWO extreme negative |
| **Oversold Confluence** | #3 | RSI Bollinger Bands + EWO + CCI + moderi multi-indicator validation |

---

## IV. Sell Logic Detailed

### 4.1 Multi-Layer Take Profit System

The strategy uses a tiered take profit mechanism:

```
Profit Range      Stop Loss Threshold    Signal Name
───────────────────────────────────────────────────
< 1%             -17.8%                  Hard stop protection
1% ~ 4.8%        Dynamic interpolation   Tiered stop loss
> 4.8%           Floats with profit      Trailing stop
```

### 4.2 Two Sell Conditions

**Sell Signal #1: EMA Offset Sell**

```python
# Condition
- Close > EMA(sell_candles) × high_offset (1.010)
- Volume > 0
```
**Interpretation**: Price rises above 1.01x of MA, take profit

**Sell Signal #2: RSI Bollinger Upper Band Break + ATR Stop Loss**

```python
# Condition (satisfy any)
- RSI > basis + (dev × for_sigma_sell) AND moderi_96 == True
- Price falls below ATR_high (3.5x ATR dynamic stop loss)
- Volume > 0
```
**Interpretation**: Sell when RSI touches Bollinger upper band or price triggers ATR stop loss

### 4.3 Anti-Pump Mechanism

```python
dont_buy_conditions.append(
    (dataframe['pump_strength'] > self.antipump_threshold.value)
)
```

When `pump_strength` exceeds the threshold, buying is forcefully prohibited to prevent chasing highs.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend** | EMA(16/20), ZEMA(30/200) | MA trend determination |
| **Oscillators** | RSI(14/4/30), StochRSI | Overbought/oversold determination |
| **Volatility** | ATR(14), Bollinger Bands | Volatility and channels |
| **Momentum** | EWO, CTI(20), CCI(240/20) | Momentum and trend strength |
| **Custom** | moderi_96, pump_strength | Long-term trend, anti-pump |

### 5.2 Informational Timeframe Indicators (1h)

The strategy uses 1 hour as the informational layer, providing higher-dimensional trend confirmation:

- Long-term EMA trend confirmation
- Cross-timeframe moderi indicator
- Base data for pump strength calculation

### 5.3 Elliott Wave Oscillator (EWO)

```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(df, timeperiod=ema_length)
    ema2 = ta.EMA(df, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / df['close'] * 100
    return emadif
```

EWO measures market momentum through the percentage difference between fast and slow EMAs.

---

## VI. Risk Management Features

### 6.1 Triple Protection Mechanism

| Protection Type | Parameter | Function |
|-----------------|-----------|----------|
| **LowProfitPairs** | 5% loss trigger | Pause trading pair after loss |
| **MaxDrawdown** | 20% drawdown | Global circuit breaker protection |
| **Anti-pump Threshold** | 0.25 | Prohibit chasing highs |

### 6.2 Custom Dynamic Stop Loss

The strategy implements progressive stop loss protection:

```python
if (current_profit > PF_2):  # Profit > 4.8%
    sl_profit = SL_2 + (current_profit - PF_2)
elif (current_profit > PF_1):  # Profit between 1% - 4.8%
    sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
else:  # Profit < 1%
    sl_profit = HSL  # -17.8%
```

### 6.3 HyperOpt Optimization Parameters

The strategy provides rich optimizable parameters:

| Parameter Category | Count | Examples |
|-------------------|-------|----------|
| Buy Parameters | 7 | base_nb_candles_buy, ewo_high, rsi_buy, etc. |
| Sell Parameters | 8 | base_nb_candles_sell, high_offset, rsi_high, etc. |
| Dynamic Stop Loss Parameters | 5 | pHSL, pPF_1, pSL_1, pPF_2, pSL_2 |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-dimensional Validation**: Buy signals require confirmation from multiple indicators, reducing false signal probability
2. **Anti-pump Mechanism**: Built-in pump_strength indicator effectively avoids chasing-high risks
3. **Dynamic Stop Loss**: Tiered stop loss mechanism maximizes profits while protecting capital
4. **HyperOpt Friendly**: Many optimizable parameters, easy for backtesting and tuning

### ⚠️ Limitations

1. **Too Many Parameters**: Over 20 adjustable parameters, prone to overfitting historical data
2. **Computationally Complex**: Multiple indicator calculations require significant computing resources
3. **5-minute Timeframe**: Sensitive to market noise, requires good market liquidity

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Oscillating Uptrend** | Default parameters | Suitable for pullback buying strategy |
| **Sideways Oscillation** | Lower ewo_high | Capture oversold bounces |
| **One-way Downtrend** | Raise stoploss | Reduce stop loss trigger frequency |
| **High Volatility** | Lower antipump_threshold | Stricter anti-pump protection |

---

## IX. Applicable Market Environment Detailed

SMA_BBRSI is a variant of the NostalgiaForX10 series. Based on its code architecture and long-term community live trading validation experience, it is best suited for **oscillating uptrend trending markets**, while performing poorly in **extreme volatility or one-way crashes**.

### 9.1 Strategy Core Logic

- **EMA Offset Buying**: Capture pullback opportunities in uptrends
- **EWO Momentum Confirmation**: Ensure sufficient momentum support when buying
- **RSI Bollinger Bands**: Use statistical channels to identify extreme prices

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | EMA offset strategy naturally fits pullback buying |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐☆ | RSI Bollinger Bands perform excellently in oscillation |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Stop loss may trigger frequently |
| ⚡️ Extreme Volatility | ⭐⭐☆☆☆ | Anti-pump mechanism helps, but volatility itself is hard to handle |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| timeframe | 5m | Default value, suitable for most scenarios |
| stoploss | -0.10 | Adjustable based on risk preference |
| antipump_threshold | 0.15~0.25 | Lower for high-volatility coins |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

The strategy involves EWO, RSI Bollinger Bands, CTI, CCI and other technical indicators, requiring some quantitative trading foundation to deeply understand each parameter's function.

### 10.2 Hardware Requirements

| Trading Pair Count | Minimum Memory | Recommended Memory |
|-------------------|----------------|-------------------|
| 1-5 pairs | 2GB | 4GB |
| 5-20 pairs | 4GB | 8GB |
| 20+ pairs | 8GB | 16GB |

### 10.3 Difference Between Backtesting and Live Trading

Parameters optimized via HyperOpt may perform excellently on historical data, but live trading may encounter:
- Slippage causing execution price deviation
- Market environment changes causing parameter failure
- Overfitting leading to poor adaptability to new market conditions

### 10.4 Manual Trader Recommendations

Manual execution of this strategy is not recommended because:
- Signal determination requires real-time calculation of multiple indicators
- Dynamic stop loss requires programmatic execution
- Anti-pump mechanism requires real-time monitoring

---

## XI. Summary

**SMA_BBRSI** is a technically dense multi-indicator composite strategy. Its core value lies in:

1. **Multi-layer Validation**: EMA, EWO, RSI, CCI and other indicators cross-validate
2. **Dynamic Risk Control**: Tiered stop loss + trailing stop + anti-pump triple protection
3. **Optimizability**: Rich HyperOpt parameters for strategy tuning

For quantitative traders, this is a strategy template worth in-depth study, but be aware of parameter overfitting risks. It's recommended to conduct thorough backtesting and paper trading validation before live trading.

---