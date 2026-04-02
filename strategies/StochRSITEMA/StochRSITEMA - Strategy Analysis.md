# StochRSITEMA Strategy In-Depth Analysis

> **Strategy Number**: #390 (390th of 465 strategies)  
> **Strategy Type**: Triple Indicator Confirmation + TEMA Exit System  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

StochRSITEMA is a trend-following strategy based on triple technical indicator confirmation, generating trading signals through the combination of Stochastic Oscillator, Relative Strength Index (RSI), and Triple Exponential Moving Average (TEMA). The strategy name directly reflects its core: Stoch (Stochastic) + RSI (Relative Strength) + TEMA (Triple Exponential MA).

Developed by werkkrew, referencing TradingSim's 5-minute bar strategy, the design philosophy is simple and clear: wait for multiple indicators to confirm together before entering, using TEMA breakthrough as the exit signal.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 4 independent signals must confirm simultaneously (triple confirmation mechanism) |
| **Sell Conditions** | TEMA breakthrough exit + ROI + stop-loss + trailing stop |
| **Protection Mechanism** | Tight stop-loss (-2.2%) + trailing stop to lock profits |
| **Timeframe** | 5 minutes |
| **Dependencies** | numpy, pandas, talib, qtpylib |
| **Hyperparameter Optimization** | Parameters adjusted through hyperparameter optimization |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.19503,     # Immediate: 19.5% profit target
    "13": 0.09149,    # After 13 minutes: 9.1% profit target
    "36": 0.02891,    # After 36 minutes: 2.9% profit target
    "64": 0           # After 64 minutes: close position
}

# Stop-loss setting
stoploss = -0.02205   # 2.2% hard stop-loss (very tight!)

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.17251       # Activates when profit > 17.25%
trailing_stop_positive_offset = 0.2516  # Trailing distance 25.16%
trailing_only_offset_is_reached = False # Start trailing immediately
```

**Design Philosophy**:
- Adopts very tight 2.2% stop-loss, reflecting "quick in, quick out" trading style
- Trailing stop set aggressively: starts trailing when profit exceeds 17.25%
- ROI targets set relatively high, giving trailing stop enough room

### 2.2 Order Type Configuration

```python
use_sell_signal = True          # Enable sell signals
sell_profit_only = True         # Only use sell signals when profitable
sell_profit_offset = 0.01       # Profit offset 1%
ignore_roi_if_buy_signal = False # Follow ROI even when buy signal active
```

### 2.3 Buy Parameters

```python
buy_params = {
    'rsi-lower-band': 36,      # RSI lower threshold
    'rsi-period': 15,          # RSI period
    'stoch-lower-band': 48     # Stochastic lower threshold
}
```

### 2.4 Sell Parameters

```python
sell_params = {
    'tema-period': 5,           # TEMA period
    'tema-trigger': 'close'    # TEMA trigger method: close price
}
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Quadruple Confirmation Mechanism

The strategy requires 4 conditions to be **simultaneously met** to trigger a buy signal:

| Condition # | Indicator | Condition | Meaning |
|-------------|-----------|-----------|---------|
| 1 | RSI | `RSI(15) > 36` | RSI has rebounded from oversold area |
| 2 | Stoch D | `slowd` crosses above lower band (48) | Stochastic D line rising from low |
| 3 | Stoch K | `slowk` crosses above lower band (48) | Stochastic K line rising from low |
| 4 | Stoch Cross | `slowk` crosses above `slowd` | K line golden cross confirms trend reversal |
| 5 | Volume | `volume > 0` | Valid candle with volume |

### 3.2 Buy Signal Logic Detailed

```python
conditions.append(dataframe[f"rsi({params['rsi-period']})"] > params['rsi-lower-band'])
# RSI(15) > 36: RSI has broken above from oversold area

conditions.append(qtpylib.crossed_above(dataframe['stoch-slowd'], params['stoch-lower-band']))
# Stoch D line crosses above 48: Stochastic D line rising from low

conditions.append(qtpylib.crossed_above(dataframe['stoch-slowk'], params['stoch-lower-band']))
# Stoch K line crosses above 48: Stochastic K line rising from low

conditions.append(qtpylib.crossed_above(dataframe['stoch-slowk'], dataframe['stoch-slowd']))
# K crosses above D: Stochastic golden cross confirms trend reversal
```

### 3.3 Condition Interpretation

**Why These Conditions?**

1. **RSI > 36**: RSI has exited severe oversold area (typically RSI < 30 is oversold), indicating price has started to rebound
2. **Stoch K/D Cross Above 48**: Stochastic rising from relatively low area, below 50 is still considered low
3. **K Crosses Above D**: Classic stochastic buy signal, confirms short-term trend reversal

**Advantages of This Design**:
- Triple confirmation reduces false signals
- All conditions point to "rebounding from lows"
- Avoids buying during mid-downtrend

---

## IV. Sell Logic Detailed Analysis

### 4.1 TEMA Exit System

The strategy uses TEMA (Triple Exponential Moving Average) as the primary exit signal:

```python
# Sell trigger method (adjustable via parameter)
if params.get('tema-trigger') == 'close':
    # Close price breaks below TEMA
    conditions.append(dataframe['close'] < dataframe[f"tema({params['tema-period']})"])

if params.get('tema-trigger') == 'both':
    # Both close and open prices break below TEMA
    conditions.append(
        (dataframe['close'] < dataframe[f"tema({params['tema-period']})"]) & 
        (dataframe['open'] < dataframe[f"tema({params['tema-period']})"])
    )

if params.get('tema-trigger') == 'average':
    # Average of open and close breaks below TEMA
    conditions.append(
        ((dataframe['close'] + dataframe['open']) / 2) < dataframe[f"tema({params['tema-period']})"]
    )
```

**TEMA Trigger Methods**:

| Trigger Method | Condition | Characteristic |
|-----------------|-----------|-----------------|
| `close` | Close price < TEMA | Most sensitive |
| `both` | Both close and open < TEMA | More conservative |
| `average` | (Close + Open)/2 < TEMA | Medium sensitivity |

### 4.2 Multi-Layer Exit Mechanism

The strategy adopts a multi-layer exit system:

| Exit Type | Trigger Condition | Description |
|-----------|-------------------|-------------|
| **Stop-Loss** | Profit < -2.2% | Hard stop-loss, quick exit |
| **TEMA Exit** | Price breaks below TEMA(5) | Trend reversal exit |
| **ROI Exit** | Profit > target | Stepped profit targets |
| **Trailing Stop** | Profit > 17.25% | Lock in profits |

### 4.3 ROI Steps

```
Time (minutes)    Profit Target
─────────────────────
0                 19.5%
13                9.1%
36                2.9%
64                Close position
```

**Interpretation**:
- Highest target at entry (19.5%)
- Target decreases over time
- Forced close after 64 minutes

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| **RSI** | RSI(5-30), using RSI(15) | Relative strength judgment |
| **Stochastic** | Stochastic(14, 3, 3) | Stochastic oscillator |
| **TEMA** | TEMA(5-50), using TEMA(5) | Trend judgment and exit |

### 5.2 Indicator Calculation Range

The strategy prepares multi-period indicators for hyperparameter optimization:

```python
# RSI range (for hyperparameter optimization)
rsiStart = 5
rsiEnd = 30

# TEMA range (for hyperparameter optimization)
temaStart = 5
temaEnd = 50

# Stochastic parameters (fixed)
fastkPeriod = 14
slowkPeriod = 3
slowdPeriod = 3
```

### 5.3 Stochastic Calculation Detailed

```python
stoch_slow = ta.STOCH(dataframe, 
                      fastk_period=14,
                      slowk_period=3, 
                      slowd_period=3)
# slowk: K line (fast line)
# slowd: D line (slow line)
```

**Stochastic Indicator Principles**:
- K line is more sensitive, reflecting short-term momentum
- D line is smoother, reflecting trend direction
- K crossing above D is golden cross (buy signal)
- K crossing below D is death cross (sell signal)

---

## VI. Risk Management Features

### 6.1 Tight Stop-Loss Strategy

The strategy adopts a very tight stop-loss (-2.2%), reflecting a "quick in, quick out" trading style:

```python
stoploss = -0.02205  # Only 2.2%
```

**Advantages**:
- Controllable single trade loss
- Quick stop-loss, avoids deep entrapment
- Suitable for high-frequency trading

**Risks**:
- May be triggered by normal volatility
- Requires precise entry timing

### 6.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.17251       # Activates at 17.25% profit
trailing_stop_positive_offset = 0.2516  # 25.16% trailing distance
```

**Interpretation**:
- When profit exceeds 17.25%, trailing stop activates
- Trailing distance is 25.16% (triggers when price retraces 25.16% from high)
- This gives price enough room for fluctuation

### 6.3 Triple Confirmation Mechanism

Four buy conditions ensure entry only when multiple indicators resonate:

| Indicator | Function | Risk Filter |
|-----------|----------|-------------|
| RSI | Filter oversold rebound | Avoid chasing highs |
| Stoch K | Confirm short-term momentum | Filter weak rebounds |
| Stoch D | Confirm trend direction | Filter false breakouts |
| K/D Cross | Final confirmation | Multiple verification |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Triple Confirmation Mechanism**: Multiple indicators confirm together, reducing false signals
2. **Tight Stop-Loss Controls Risk**: 2.2% stop-loss, controllable single trade loss
3. **Trailing Stop Locks Profits**: Protection when large profits occur
4. **Simple Clear Logic**: Easy to understand and debug
5. **Optimized Parameters**: Parameters after hyperparameter optimization

### ⚠️ Limitations

1. **Stop-Loss Too Tight**: May be frequently triggered by normal volatility
2. **Strict Buy Conditions**: Four confirmations may miss opportunities
3. **Dependent on Hyperparameter Optimization**: Parameters may be overfitted
4. **Single Timeframe**: No informative layer for auxiliary judgment

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Ranging Market | Default parameters | Strategy design intent, suitable for catching rebounds |
| Trending Market | Adjust stop-loss | May need to loosen stop-loss to avoid being shaken out |
| High Volatility Market | Increase stop-loss | 2.2% stop-loss may be too tight |
| Low Volatility Market | Default parameters | Wait for confirmation signals before entering |

---

## IX. Applicable Market Environment Detailed Analysis

StochRSITEMA is a **ranging market rebound-catching strategy**. Based on its triple confirmation mechanism and tight stop-loss design, it is best suited for **ranging markets with clear support levels**, while performing poorly in one-sided trend markets.

### 9.1 Strategy Core Logic

- **Wait for Confirmation**: Four buy conditions, only enter when multiple indicators resonate
- **Quick Stop-Loss**: 2.2% tight stop-loss, quick exit when wrong
- **Trend-Following Exit**: TEMA breakthrough as trend reversal signal
- **Profit Protection**: Trailing stop locks in gains

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|-------------|--------|----------|
| 📈 Ranging Uptrend | ⭐⭐⭐⭐⭐ | Triple confirmation catches rebounds, tight stop-loss controls risk |
| 🔄 Sideways Range | ⭐⭐⭐⭐☆ | Catches support level rebounds, good results |
| 📉 One-sided Decline | ⭐⭐☆☆☆ | Tight stop-loss frequently triggered, fee losses |
| ⚡ One-sided Rally | ⭐⭐⭐☆☆ | May miss fast rally opportunities |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| `stoploss` | -0.02 ~ -0.03 | Can appropriately loosen to avoid being shaken out |
| `rsi-lower-band` | 30-40 | Controls entry timing aggressiveness |
| `stoch-lower-band` | 40-50 | Higher = more aggressive, lower = more conservative |
| `tema-period` | 5-10 | Shorter period = more sensitive exit |

---

## X. Important Note: Double-Edged Sword of Parameter Optimization

### 10.1 Learning Curve

Strategy logic is relatively simple, but requires understanding basic principles of RSI, Stochastic, and TEMA. Recommend learning these indicators' meanings first.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-10 pairs | 1 GB | 2 GB |
| 10-30 pairs | 2 GB | 4 GB |
| 30+ pairs | 4 GB | 8 GB |

### 10.3 Backtest vs. Live Trading Differences

Strategy parameters have been hyperparameter optimized:
- Backtest parameters: `47/50: 19 trades. 7/6/6 Wins/Draws/Losses. Avg profit -0.35%`
- These parameters may be "overfitted" results
- Live performance may differ from backtest

### 10.4 Manual Trading Recommendations

If wanting to manually use this logic:
1. Wait for RSI to rebound from oversold area (<30) to above 36
2. Confirm both Stochastic K and D cross above 48
3. Wait for K to cross above D forming golden cross
4. After entering, set 2-3% stop-loss
5. Exit when price breaks below TEMA

---

## XI. Summary

**StochRSITEMA** is a **ranging market rebound-catching strategy**. Its core value lies in:

1. **Triple Confirmation Mechanism**: RSI + Stochastic + TEMA multiple verification, reducing false signals
2. **Tight Stop-Loss Control**: 2.2% stop-loss, quick exit from wrong trades
3. **Trailing Stop Protection**: Automatically locks in gains at large profits
4. **Simple Clear Logic**: Easy to understand and debug

For quantitative traders, this is a strategy suitable for ranging markets, but note:
- Tight stop-loss may lead to frequent stop-outs
- Parameters have been optimized, may need readjustment
- Single timeframe, recommend combining with higher timeframe for trend judgment