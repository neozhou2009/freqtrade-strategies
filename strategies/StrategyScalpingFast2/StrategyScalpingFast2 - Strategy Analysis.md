# StrategyScalpingFast2 Strategy Analysis

> **Strategy ID**: #398 (391st of 465 strategies)  
> **Strategy Type**: Multi-Timeframe Scalping Strategy + Parameterized Configurable System  
> **Timeframe**: 1 minute (1m) + Resampled 5-minute trend confirmation

---

## I. Strategy Overview

StrategyScalpingFast2 is an **enhanced upgraded version** of StrategyScalpingFast, improved based on the ReinforcedSmoothScalp strategy. While retaining the original scalping core logic, it adds **multi-timeframe trend confirmation** and **parameterized configuration system**, making the strategy more flexible and tunable.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Condition** | Parameterized buy signal, supports 4 optional conditions |
| **Sell Condition** | Parameterized sell signal, supports 5 optional conditions |
| **Protection Mechanism** | Tiered ROI profit taking + fixed stop loss 32.6% |
| **Timeframe** | 1m execution + 5m resampled trend confirmation |
| **Dependencies** | talib, qtpylib, technical, numpy |
| **Special Features** | Parameterized buy/sell conditions, multi-timeframe, resampled SMA trend filter |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table (tiered profit taking)
minimal_roi = {
    "0": 0.082,   # After 0 minutes, 8.2% profit target
    "18": 0.06,   # After 18 minutes, 6% profit target
    "51": 0.012,  # After 51 minutes, 1.2% profit target
    "123": 0      # After 123 minutes, sell at any profit
}

# Stop loss setting
stoploss = -0.326  # 32.6% fixed stop loss

# Sell signal configuration
use_sell_signal = False  # Don't use custom sell signal
```

**Design Rationale**:
- **Tiered ROI**: Decreasing profit targets over time, adapting to different market conditions
- **Large stop loss space**: 32.6% stop loss gives the strategy greater fluctuation tolerance
- **Conservative profit taking**: Longer holding time means lower profit threshold, ensuring eventual exit

### 2.2 Buy Parameter Configuration

```python
buy_params = {
    "mfi-value": 19,        # MFI threshold
    "fastd-value": 29,      # FastD threshold
    "fastk-value": 19,      # FastK threshold
    "adx-value": 30,        # ADX threshold
    "mfi-enabled": False,   # MFI condition enabled
    "fastd-enabled": False, # FastD condition enabled
    "adx-enabled": False,   # ADX condition enabled
    "fastk-enabled": False, # FastK condition enabled
}
```

### 2.3 Sell Parameter Configuration

```python
sell_params = {
    "sell-mfi-value": 89,       # Sell MFI threshold
    "sell-fastd-value": 72,      # Sell FastD threshold
    "sell-fastk-value": 68,      # Sell FastK threshold
    "sell-adx-value": 86,        # Sell ADX threshold
    "sell-cci-value": 157,       # Sell CCI threshold
    "sell-mfi-enabled": True,    # MFI sell condition enabled
    "sell-fastd-enabled": True,  # FastD sell condition enabled
    "sell-adx-enabled": True,    # ADX sell condition enabled
    "sell-cci-enabled": False,   # CCI sell condition enabled
    "sell-fastk-enabled": False, # FastK sell condition enabled
}
```

---

## III. Buy Conditions Explained

### 3.1 Core Buy Logic

The strategy uses a **base conditions + optional conditions** flexible architecture:

```python
# Base conditions (must meet)
conditions.append(dataframe["volume"] > 0)           # Has volume
conditions.append(dataframe['open'] < dataframe['ema_low'])  # Price below EMA lower band
conditions.append(dataframe['resample_sma'] < dataframe['close'])  # Resampled SMA confirms trend

# Optional conditions (enabled based on parameters)
if self.buy_params['adx-enabled']:
    conditions.append(dataframe["adx"] < self.buy_params['adx-value'])
if self.buy_params['mfi-enabled']:
    conditions.append(dataframe['mfi'] < self.buy_params['mfi-value'])
if self.buy_params['fastk-enabled']:
    conditions.append(dataframe['fastk'] < self.buy_params['fastk-value'])
if self.buy_params['fastd-enabled']:
    conditions.append(dataframe['fastd'] < self.buy_params['fastd-value'])
if self.buy_params['fastk-enabled'] == True & self.buy_params['fastd-enabled'] == True:
    conditions.append(qtpylib.crossed_above(dataframe['fastk'], dataframe['fastd']))
```

### 3.2 Condition Classification

| Condition Group | Condition | Default Status | Description |
|-----------------|----------|---------------|-------------|
| **Base Conditions** | volume > 0 | Required | Ensures there's volume |
| **Base Conditions** | open < ema_low | Required | Price below EMA lower band |
| **Base Conditions** | resample_sma < close | Required | 5-minute trend up confirmation |
| **Optional Conditions** | ADX < 30 | Disabled | Trend strength filter |
| **Optional Conditions** | MFI < 19 | Disabled | Money flow oversold |
| **Optional Conditions** | FastK < 19 | Disabled | Stochastic K oversold |
| **Optional Conditions** | FastD < 29 | Disabled | Stochastic D oversold |
| **Optional Conditions** | K crosses above D | Disabled | Golden cross confirmation |

### 3.3 Multi-Timeframe Trend Confirmation

This is the most important upgrade of StrategyScalpingFast2 compared to the original:

```python
# Resample factor
resample_factor = 5  # 1 minute * 5 = 5 minute trend

# Calculate 5-minute SMA
tf_res = timeframe_to_minutes(self.timeframe) * self.resample_factor  # = 5
df_res = resample_to_interval(dataframe, tf_res)  # Resample to 5 minutes
df_res['sma'] = ta.SMA(df_res, 50, price='close')  # 50-period SMA
dataframe = resampled_merge(dataframe, df_res, fill_na=True)  # Merge back to 1 minute

# Trend confirmation condition
dataframe['resample_sma'] < dataframe['close']  # Price above 5-minute SMA
```

**Significance**: Only buy when price is above the 5-minute SMA, ensuring trend-following trading, avoiding counter-trend bottom fishing.

---

## IV. Sell Logic Explained

### 4.1 Sell Signal Structure

```python
# Base condition
conditions.append(dataframe['open'] >= dataframe['ema_high'])  # Price touches EMA upper band

# Optional conditions
if self.sell_params['sell-fastd-enabled']:
    conditions.append(
        (qtpylib.crossed_above(dataframe['fastk'], self.sell_params['sell-fastk-value'])) |
        (qtpylib.crossed_above(dataframe['fastd'], self.sell_params['sell-fastd-value']))
    )
if self.sell_params['sell-mfi-enabled']:
    conditions.append(dataframe['mfi'] > self.sell_params['sell-mfi-value'])
if self.sell_params['sell-adx-enabled']:
    conditions.append(dataframe["adx"] < self.sell_params['sell-adx-value'])
```

### 4.2 Default Sell Conditions

Based on default configuration, sell conditions are:

| Condition | Threshold | Purpose |
|-----------|-----------|---------|
| open >= ema_high | - | Price touches EMA upper band |
| fastk crosses above 68 or fastd crosses above 72 | 68/72 | Stochastic overbought |
| MFI > 89 | 89 | Money flow overbought |
| ADX < 86 | 86 | Trend strength weakening |

### 4.3 Tiered ROI Mechanism

| Time Range | ROI Target | Description |
|------------|------------|-------------|
| 0-18 minutes | 8.2% | Pursuing high returns |
| 18-51 minutes | 6% | Slightly lower target |
| 51-123 minutes | 1.2% | Even lower target |
| After 123 minutes | Any profit | Sell as long as profitable |

**Design Philosophy**: Longer holding time means lower profit requirements, ensuring eventual exit.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Category | Indicator | Parameters | Purpose |
|----------|-----------|------------|---------|
| Trend | EMA | Period 5 | Price envelope |
| Trend | SMA (resampled) | Period 50 | 5-minute trend confirmation |
| Oscillator | Stochastic Fast | 5, 3, 0, 3, 0 | Overbought/oversold |
| Trend Strength | ADX | Default | Trend momentum |
| Money Flow | MFI | Default | Money flow |
| Oscillator | CCI | Period 20 | Overbought/oversold |
| Trend | RSI | Period 14 | Calculated (not used) |
| Volatility | Bollinger Bands | 20, 2 | Chart display |

### 5.2 Resampling System

```python
# Resampling configuration
timeframe = '1m'          # Execution timeframe
resample_factor = 5       # Resample factor

# Actual usage: 1-minute data → 5-minute trend confirmation
```

**Advantages**:
- Execute trades on 1-minute timeframe
- Use 5-minute trend to filter signals
- Reduce false signals, improve win rate

---

## VI. Risk Management Features

### 6.1 Tiered Profit Taking Mechanism

```python
minimal_roi = {
    "0": 0.082,   # 8.2%
    "18": 0.06,   # 6%
    "51": 0.012,  # 1.2%
    "123": 0      # Any
}
```

- **High target start**: Initially pursuing 8.2% return
- **Time decreasing**: Lower profit expectations over holding time
- **Ensured exit**: After 123 minutes, any profit is acceptable

### 6.2 Large Stop Loss Design

```python
stoploss = -0.326  # 32.6%
```

- **Giving space**: 32.6% stop loss space, avoiding being stopped by normal fluctuations
- **Risk warning**: Such a large stop loss needs appropriate position management

### 6.3 Parameterized Risk Control

Through `buy_params` and `sell_params` can flexibly adjust:

- Adjust buy thresholds to control signal frequency
- Enable/disable specific conditions
- Optimize parameters based on market environment

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Parameterized design**: Buy/sell conditions configurable, adapting to different markets
2. **Multi-timeframe**: 5-minute trend confirmation reduces false signals
3. **Tiered ROI**: Flexible profit taking mechanism improves capital efficiency
4. **Modular code**: Uses reduce function to combine conditions, clean code
5. **Official recommendation**: Suggests running 60+ parallel trades to diversify risk

### ⚠️ Limitations

1. **Large stop loss risk**: 32.6% stop loss is too large for scalping
2. **Conservative default parameters**: Most buy conditions disabled by default, may miss opportunities
3. **Increased complexity**: 50% more code than original
4. **Technical library dependency**: Requires additional dependency installation
5. **Resampling delay**: 5-minute confirmation may miss quick reversals

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|--------------------|---------------------------|-------|
| Ranging | Enable MFI, FastK/D conditions | Increase signal frequency |
| Trending | Enable trend confirmation, rely on SMA filter | Trend-following |
| High volatility | Disable some conditions, reduce signal frequency | Reduce false signals |
| Low volatility | Enable more buy conditions | Increase trading opportunities |

---

## IX. Applicable Market Environment Details

StrategyScalpingFast2 is a **parameterized scalping strategy**. Based on its code architecture and author recommendations, it's best suited for **multi-currency parallel operation**, reducing single trading pair risk through diversification.

### 9.1 Strategy Core Logic

- **Trend filtering**: 5-minute SMA confirms overall trend direction
- **Position confirmation**: Look for oversold below EMA lower band
- **Parameterized control**: Flexibly enable/disable various conditions
- **Tiered profit taking**: Adjust return expectations based on holding time

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:------------|:-------|:---------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | 5-minute SMA confirms trend, trend-following works well |
| 🔄 Sideways ranging | ⭐⭐⭐⭐☆ | Oversold reversal logic effective, but trend filter may miss opportunities |
| 📉 Downtrend | ⭐⭐☆☆☆ | SMA filter prevents counter-trend buying, but may trigger stop loss |
| ⚡️ High volatility | ⭐⭐☆☆☆ | Noise interference, increased false signals |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended | Notes |
|---------------|-------------|-------|
| Parallel trading pairs | 60+ | Author suggests diversification |
| Stop loss | -0.15 ~ -0.20 | Recommend tightening from 32.6% |
| Buy MFI | True | Enable MFI condition |
| Buy FastK/D | True | Enable stochastic conditions |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

Compared to original StrategyScalpingFast, this version adds:

- Resampling system
- Parameterized configuration
- Condition combination logic

Need to understand more concepts to configure correctly.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|-------------|-----------------|
| 1-20 pairs | 2GB | 4GB |
| 20-60 pairs | 4GB | 8GB |
| 60+ pairs | 8GB | 16GB |

### 10.3 Backtesting vs Live Trading Differences

The strategy author specifically emphasizes:

> "We recommend running at least 60 parallel trades to cover inevitable losses"

This means:
- Single trading pair win rate may not be high
- Need sufficient capital to support multi-currency operation
- Diversification reduces single failure impact

### 10.4 Manual Trading Recommendations

Not recommended to manually replicate this strategy:

1. Complex parameter configuration, difficult to adjust in real-time
2. Multi-timeframe needs simultaneous monitoring
3. Recommended to use quantitative platform for automated execution

---

## XI. Summary

**StrategyScalpingFast2** is an **enhanced parameterized scalping strategy**. Its core value lies in:

1. **Multi-timeframe confirmation**: 5-minute trend filtering improves signal quality
2. **Parameterized design**: Flexible adjustment for different markets
3. **Tiered profit taking**: Time-decreasing ROI improves exit probability
4. **Parallel trade design**: Suitable for multi-currency risk diversification

For quantitative traders, this is a **strategy suitable as a scalping strategy foundation**. Through parameter adjustment can adapt to different market environments, but need to note:

- Default parameters may be too conservative
- Stop loss is large, recommend adjusting based on actual situation
- Need sufficient capital to support multi-currency operation

---