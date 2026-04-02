# BB_RPB_TSL_RNG_VWAP Strategy In-Depth Analysis

> **Strategy Number**: #446 (446th out of 465 strategies)  
> **Strategy Type**: Bollinger Band Pullback + VWAP Support + Multi-Layer Dynamic Stoploss  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

BB_RPB_TSL_RNG_VWAP is a trend-following strategy based on Bollinger Band pullback principles, integrating VWAP (Volume Weighted Average Price) support judgment and custom trailing stoploss mechanism. This strategy adds VWAP-related buy conditions and independent stoploss parameter configuration on the basis of the BB_RPB_TSL series, providing more refined volume-weighted price entry judgment.

### Core Features

| Feature | Description |
|------|------|
| **Buy Conditions** | 8 independent buy signals (including VWAP-exclusive conditions) |
| **Sell Conditions** | 2 base sell signals + multi-layer dynamic take-profit logic |
| **Protection Mechanisms** | 3-layer trailing stoploss parameters + VWAP-exclusive stoploss configuration |
| **Timeframe** | Main timeframe 5m + BTC informative layer 5m |
| **Dependencies** | freqtrade, talib, pandas_ta, technical (RMI, zema) |
| **Special Features** | VWAP Bands + top_percent_change indicators |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,   # 10% profit target
    "30": 0.05,  # Drop to 5% after 30 minutes
    "60": 0.02,  # Drop to 2% after 60 minutes
}

# Stoploss Settings
stoploss = -0.10  # 10% hard stoploss (disabled, uses custom stoploss)

# Custom Stoploss
use_custom_stoploss = True

# Startup Candle Count
startup_candle_count = 120
```

**Design Philosophy**:
- ROI setting uses tiered递减, allowing strategy to have different exit standards at different holding times
- Hard stoploss set at -10%, relatively loose to adapt to VWAP entry scenarios
- Custom stoploss logic includes VWAP-exclusive parameter configuration
- Startup requires 120 candles of historical data to calculate indicators

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'emergencysell': 'limit',
    'forcebuy': 'limit',
    'forcesell': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False,
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
}
```

**Design Philosophy**: All use limit orders, ensuring executable prices are controllable.

---

## III. Buy Conditions Detailed Analysis

### 3.1 VWAP-Exclusive Conditions

Strategy adds VWAP-related buy conditions, based on volume-weighted price support judgment:

#### Condition #8: VWAP Lower Rail Entry (is_vwap)

```python
is_vwap = (
    (dataframe['close'] < dataframe['vwap_low']) &
    (dataframe['tcp_percent_4'] > 0.04) &
    (dataframe['cti'] < -0.8) &
    (dataframe['rsi'] < 35) &
    (dataframe['rsi_84'] < 60) &
    (dataframe['rsi_112'] < 60) &
    (dataframe['volume'] > 0)
)
```

**Core Logic**:
- `close < vwap_low`: Price breaks below VWAP lower rail (volume-weighted support)
- `tcp_percent_4 > 0.04`: top_percent_change > 4%, indicating price dropped more than 4% from recent high
- `cti < -0.8`: Correlation Trend Indicator shows oversold
- `rsi < 35`: RSI oversold
- `rsi_84 < 60` & `rsi_112 < 60`: Long-term RSI not overheated
- `volume > 0`: Ensure there is trading volume

**VWAP Bands Calculation**:

```python
def vmap_b(dataframe, window_size=20, num_of_std=1):
    df['vwap'] = qtpylib.rolling_vwap(df, window=window_size)
    rolling_std = df['vwap'].rolling(window=window_size).std()
    df['vwap_low'] = df['vwap'] - (rolling_std * num_of_std)
    df['vwap_high'] = df['vwap'] + (rolling_std * num_of_std)
    return df['vwap_low'], df['vwap'], df['vwap_high']
```

### 3.2 Seven Inherited Buy Conditions

Strategy inherits 7 buy conditions from BB_RPB_TSL series:

#### Condition #1: BB Pullback Combo (is_BB_checked)

```python
is_dip = (
    (dataframe[f'rmi_length_{self.buy_rmi_length.value}'] < 49) &
    (dataframe[f'cci_length_{self.buy_cci_length.value}'] <= -116) &
    (dataframe['srsi_fk'] < 32)
)

is_break = (
    (dataframe['bb_delta'] > 0.025) &
    (dataframe['bb_width'] > 0.095) &
    (dataframe['closedelta'] > dataframe['close'] * 12.148 / 1000) &
    (dataframe['close'] < dataframe['bb_lowerband3'] * 0.999)
)

is_BB_checked = is_dip & is_break
```

#### Condition #2: Local Uptrend (is_local_uptrend)

```python
is_local_uptrend = (
    (dataframe['ema_26'] > dataframe['ema_12']) &
    (dataframe['ema_26'] - dataframe['ema_12'] > dataframe['open'] * 0.022) &
    (dataframe['ema_26'].shift() - dataframe['ema_12'].shift() > dataframe['open'] / 100) &
    (dataframe['close'] < dataframe['bb_lowerband2'] * 0.999) &
    (dataframe['closedelta'] > dataframe['close'] * 12.148 / 1000)
)
```

#### Conditions #3-7: EWO/COFI/NFI Series

See BB_RPB_TSL_RNG_TBS_GOLD strategy documentation, logic is consistent.

### 3.3 Buy Conditions Classification Summary

| Condition Group | Condition Numbers | Core Logic |
|-------|---------|---------|
| Bollinger Band Pullback | #1 | RMI/CCI/SRSI + BB breakout combo |
| Trend Pullback | #2 | EMA trend + BB lower rail pullback |
| EWO Series | #3, #4 | Elliott Wave indicator low/high entry |
| Indicator Cross | #5 | Stochastic golden cross + ADX strength |
| NFI Series | #6, #7 | CTI oversold + RSI/Williams%R extreme values |
| **VWAP Entry** | #8 | VWAP lower rail breakout + volume confirmation |

---

## IV. Sell Logic Detailed Analysis

### 4.1 VWAP-Exclusive Stoploss Configuration

Strategy uses independent stoploss parameters for trades entered via VWAP:

```python
if len(buy_tags) == 1 and "vwap" in buy_tags:
    PF_1 = 0.01   # VWAP-exclusive: Tier 1 trigger
    SL_1 = 0.01   # VWAP-exclusive: Tier 1 stoploss
    PF_2 = 0.05   # VWAP-exclusive: Tier 2 trigger
    SL_2 = 0.042  # VWAP-exclusive: Tier 2 stoploss
```

**Design Philosophy**: VWAP entry scenarios use looser stoploss parameters (PF_1=0.01, SL_1=0.01), allowing more volatility space.

### 4.2 Multi-Layer Take-Profit System

Regular stoploss configuration:

```
Profit Range         Stoploss Threshold    Take-Profit Trigger
──────────────────────────────────────────────
Profit < 1.9%       HSL (-25%)            Hard stoploss (looser)
1.9% < Profit < 6.5%  SL_1 Linear Interpolation    Tiered stoploss
Profit > 6.5%       SL_2 + Dynamic Add-on    Trailing stoploss
```

**Comparison with VWAP Stoploss Parameters**:

| Parameter Type | Regular Configuration | VWAP-Exclusive Configuration |
|---------|---------|-------------|
| HSL | -0.25 | Same as regular |
| PF_1 | 0.019 | **0.01** |
| SL_1 | 0.019 | **0.01** |
| PF_2 | 0.065 | **0.05** |
| SL_2 | 0.062 | **0.042** |

### 4.3 Base Sell Signals

```python
# Sell Signal 1: Trend weakening
(dataframe['close'] > dataframe['sma_9']) &
(dataframe['close'] > dataframe[f'ma_sell_{val}'] * 0.997) &
(dataframe['rsi'] > 50) &
(dataframe['volume'] > 0) &
(dataframe['rsi_fast'] > dataframe['rsi_slow'])

# Sell Signal 2: Moving average divergence
(dataframe['sma_9'] > dataframe['sma_9'].shift(1) * 1.005) &
(dataframe['close'] < dataframe['hma_50']) &
(dataframe['close'] > dataframe[f'ma_sell_{val}'] * 0.991) &
(dataframe['volume'] > 0) &
(dataframe['rsi_fast'] > dataframe['rsi_slow'])
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|---------|---------|------|
| Bollinger Bands | BB_2std, BB_3std | Pullback entry judgment |
| **VWAP** | VWAP/VWAP_low/VWAP_high | Volume-weighted support judgment |
| Moving Average System | EMA 8/12/13/16/26, SMA 9/15/30, HMA 50 | Trend judgment |
| Momentum Indicators | RSI 4/14/20/**84/112**, RMI, CCI | Overbought/oversold judgment |
| Oscillator Indicators | Stochastic RSI, Stochastic Fast, Williams %R | Entry timing |
| Trend Strength | ADX, EWO | Trend confirmation |
| Custom | CTI, **top_percent_change** | Trend correlation + price change |

### 5.2 VWAP-Exclusive Indicators

```python
# VWAP Bands (20 period, 1 standard deviation)
vwap_low, vwap, vwap_high = vmap_b(dataframe, 20, 1)

# top_percent_change (4 period)
tcp_percent_4 = (dataframe['open'].rolling(4).max() - dataframe['close']) / dataframe['close']
```

### 5.3 Long-Period RSI Indicators

Strategy adds RSI 84 and RSI 112 indicators for judging long-term trend state:

```python
dataframe['rsi_84'] = ta.RSI(dataframe, timeperiod=84)
dataframe['rsi_112'] = ta.RSI(dataframe, timeperiod=112)
```

---

## VI. Risk Management Features

### 6.1 VWAP-Exclusive Stoploss Strategy

For trades entered via VWAP, strategy uses looser stoploss parameters:

| Profit Range | VWAP Stoploss Configuration | Description |
|---------|-------------|------|
| < 1% | HSL (-25%) | Hard stoploss is looser |
| 1%-5% | Linear Interpolation | Tiered stoploss |
| > 5% | Dynamic Trailing | Trailing stoploss |

**Design Reason**: VWAP entry is based on volume-weighted price judgment, may experience greater volatility, needs looser stoploss space.

### 6.2 Layered Trailing Stoploss

Three-tier stoploss protection:
- **Tier 1**: Profit < PF_1, use hard stoploss
- **Tier 2**: Profit PF_1 ~ PF_2, linear interpolation stoploss
- **Tier 3**: Profit > PF_2, dynamic trailing stoploss

### 6.3 BTC Market Protection (Optional)

Monitor BTC/USDT 5-minute price, but default code is commented out.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **VWAP Support Judgment**: Adds volume-weighted price entry conditions, based on real volume support
2. **VWAP-Exclusive Stoploss**: Uses independent stoploss parameters for VWAP entries, more refined risk management
3. **Long-Period RSI**: Adds 84/112 period RSI to judge long-term trend state
4. **Diversified Entry**: 8 buy conditions cover Bollinger Bands, VWAP, EWO and other scenarios
5. **Tiered ROI**: Time-decreasing ROI settings allow different exit standards for different holding times

### ⚠️ Limitations

1. **VWAP Computational Overhead**: Rolling VWAP and standard deviation calculations increase computational burden
2. **Complex Parameters**: Multiple stoploss parameter configurations (regular + VWAP-exclusive) increase maintenance complexity
3. **VWAP Entry Frequency**: VWAP conditions are strict, may trigger less frequently
4. **BTC Data Dependency**: Requires BTC/USDT 5-minute data (fixed configuration)

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| Oscillating Uptrend | Enable all buy conditions | Bollinger Band + VWAP dual pullback entry |
| Active Volume | Enable VWAP conditions | VWAP is more accurate when volume is active |
| High Volatility | Enable VWAP stoploss configuration | VWAP stoploss is looser, adapts to large volatility |
| Downtrend | Disable or use cautiously | Strategy design not suitable for shorting |

---

## IX. Applicable Market Environment Detailed Analysis

BB_RPB_TSL_RNG_VWAP is a hybrid strategy integrating Bollinger Band pullback, VWAP support judgment, and multi-layer stoploss. Based on code architecture and design logic, it is most suitable for **oscillating uptrend markets with active volume**, and VWAP conditions may be invalid in **low volume markets**.

### 9.1 Strategy Core Logic

- **Bollinger Band Pullback**: Entry when price drops near Bollinger Band lower rail
- **VWAP Support**: Entry when price breaks below volume-weighted support line
- **Volume Confirmation**: top_percent_change and volume judge real pullback
- **Layered Stoploss**: Regular stoploss + VWAP-exclusive stoploss dual protection

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Oscillating Uptrend (Active Volume) | ⭐⭐⭐⭐⭐ | Best scenario, Bollinger Band + VWAP dual pullback effective |
| 📊 Sideways Oscillation (Normal Volume) | ⭐⭐⭐⭐☆ | Bollinger Band pullback effective, VWAP conditions may trigger |
| 📉 Single-Side Downtrend | ⭐☆☆☆☆ | Buy signals trigger frequently but price continues falling |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | VWAP stoploss is looser, may withstand large volatility |
| 📉 Low Volume | ⭐⭐☆☆☆ | VWAP conditions may be inaccurate |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------|--------|------|
| VWAP Stoploss PF_1 | 0.01 | VWAP entry first tier trigger |
| VWAP Stoploss SL_1 | 0.01 | VWAP entry first tier stoploss |
| VWAP Stoploss PF_2 | 0.05 | VWAP entry second tier trigger |
| VWAP Stoploss SL_2 | 0.042 | VWAP entry second tier stoploss |
| startup_candle_count | 120 | Ensure enough historical data |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

This strategy contains 8 buy conditions and dual-layer stoploss configuration (regular + VWAP), requiring deep understanding of VWAP indicators and Bollinger Band pullback logic. Recommended to understand BB_RPB_TSL base strategy before using this strategy.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------|---------|---------|
| 1-20 pairs | 4GB | 8GB |
| 20-50 pairs | 8GB | 16GB |
| 50+ pairs | 16GB | 32GB |

### 10.3 Backtest vs Live Trading Differences

Strategy is fully compatible with backtesting and hyperopt, but VWAP conditions may perform poorly in backtest data with low volume.

### 10.4 Manual Trader Recommendations

- VWAP entry conditions require price to drop more than 4% from recent high
- Long-period RSI (84/112) used to judge overall trend is not overheated
- VWAP stoploss is looser, suitable for large volatility scenarios

---

## XI. Summary

**BB_RPB_TSL_RNG_VWAP** is a hybrid strategy integrating Bollinger Band pullback, VWAP support judgment, and dual-layer stoploss configuration. Its core value lies in:

1. **VWAP Support Judgment**: Entry based on volume-weighted price's real support
2. **VWAP-Exclusive Stoploss**: Independent stoploss parameters for VWAP entries, more refined risk management
3. **Long-Period Trend Confirmation**: RSI 84/112 judge long-term trend state
4. **Diversified Entry**: 8 buy conditions cover Bollinger Bands, VWAP, EWO and other scenarios

For quantitative traders, this strategy is suitable for oscillating uptrend markets with active volume, VWAP conditions may perform poorly in low volume markets. Recommended to prioritize enabling VWAP conditions on trading pairs with active volume, and note the differences between VWAP stoploss configuration and regular stoploss.
