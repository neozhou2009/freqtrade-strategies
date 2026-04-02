# BBRSITV Strategy In-Depth Analysis

> **Strategy ID**: #435 (435th of 465 strategies)  
> **Strategy Type**: RSI Bollinger Band Dispersion + EWO Trend Following  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

BBRSITV is a strategy ported from TradingView indicators. The core concept involves placing the RSI indicator within a Bollinger Band framework, calculating the degree of RSI dispersion relative to its moving average to determine overbought/oversold conditions, while incorporating the Elliott Wave Oscillator (EWO) as a trend filter. This strategy originates from the Pine Script indicator "RSI + BB (EMA) + Dispersion (2.0)" and represents a classic combination of volatility and momentum-based strategy.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 core buy signal (RSI breaks below Bollinger Band lower band + EWO trend confirmation) |
| **Sell Conditions** | 2 sell signals (RSI overbought + RSI breaks above Bollinger Band upper band) |
| **Protection Mechanisms** | 2 protection parameter sets (LowProfitPairs, MaxDrawdown) |
| **Timeframe** | 5-minute primary timeframe |
| **Dependencies** | talib, qtpylib, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.1  # 10% profit exit
}

# Stop loss setting
stoploss = -0.25  # 25% stop loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.005  # Activates after 0.5% profit
trailing_stop_positive_offset = 0.025  # 2.5% profit offset
trailing_only_offset_is_reached = True  # Only activates after offset reached
```

**Design Rationale**:
- ROI set to 10% fixed take-profit, suitable for medium-term trading
- 25% stop loss is relatively wide, giving the strategy sufficient room for volatility
- Trailing stop configuration is refined, requiring 2.5% profit before activation, avoiding being shaken out by normal fluctuations

### 2.2 Order Type Configuration

The strategy uses default order configuration without specifying order_types, meaning it uses exchange defaults.

### 2.3 Protection Mechanism Configuration

```python
protections = [
    {
        "method": "LowProfitPairs",
        "lookback_period_candles": 60,  # Look back 60 candles
        "trade_limit": 1,  # 1 trade
        "stop_duration": 60,  # Pause 60 minutes
        "required_profit": -0.05  # Triggered at 5% loss
    },
    {
        "method": "MaxDrawdown",
        "lookback_period_candles": 24,  # Look back 24 candles
        "trade_limit": 1,  # 1 trade
        "stop_duration_candles": 12,  # Pause 12 candles
        "max_allowed_drawdown": 0.2  # Maximum 20% drawdown
    },
]
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Core Buy Logic

The strategy's buy signal is built on the RSI Bollinger Band dispersion concept:

```python
# Calculation process
basis = EMA(RSI, for_ma_length)  # RSI's EMA baseline
dev = STDDEV(RSI, for_ma_length)  # RSI's standard deviation
disp_down = basis - (dev * for_sigma)  # Lower dispersion threshold

# Buy condition
RSI < disp_down AND EWO > ewo_high AND volume > 0
```

**Core Parameters**:
| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| for_ma_length | 22 | RSI Bollinger Band EMA period |
| for_sigma | 1.74 | Dispersion coefficient |
| ewo_high | 4.86 | EWO filter threshold |

### 3.2 Indicator Calculation Details

#### RSI Bollinger Band Dispersion

The strategy innovatively applies Bollinger Bands to RSI rather than using traditional Bollinger Bands on price:

1. **Calculate RSI(14)**: Base momentum indicator
2. **Calculate RSI's EMA**: As the Bollinger Band middle band
3. **Calculate RSI's Standard Deviation**: To determine Bollinger Band width
4. **Calculate Dispersion Zones**:
   - Upper dispersion threshold = basis + (dev × for_sigma)
   - Lower dispersion threshold = basis - (dev × for_sigma)

**Buy Signal Trigger Conditions**:
- RSI breaks downward below the lower dispersion threshold
- Indicates RSI is at a relatively extreme low position (but not an absolute low value)

#### Elliott Wave Oscillator (EWO)

```python
def EWO(dataframe, ema_length=5, ema2_length=200):
    ema1 = EMA(close, 5)
    ema2 = EMA(close, 200)
    EWO = (ema1 - ema2) / close * 100
```

**Purpose**:
- Deviation between short-term moving average (5-period) and long-term moving average (200-period)
- EWO > ewo_high indicates short-term trend is upward, in a bull market
- Acts as a trend filter, avoiding bottom-fishing in downtrends

### 3.3 Buy Conditions Summary

| Condition # | Condition Name | Logic | Parameters |
|-------------|----------------|-------|------------|
| #1 | RSI Dispersion Oversold | RSI < basis - (dev × for_sigma) | for_ma_length=22, for_sigma=1.74 |
| #2 | EWO Trend Filter | EWO > 4.86 | ewo_high=4.86 |
| #3 | Volume Filter | volume > 0 | - |

---

## IV. Sell Logic Detailed Analysis

### 4.1 Sell Signal Architecture

The strategy employs a dual-signal sell mechanism:

**Signal #1: RSI Absolute Overbought**
```python
RSI > rsi_high  # rsi_high = 72
```
- Triggers sell when RSI absolute value exceeds 72
- Simple and direct momentum reversal signal

**Signal #2: RSI Breaks Above Bollinger Band Upper Band**
```python
RSI > basis + (dev × for_sigma_sell)
```
- Parameters: for_ma_length_sell=65, for_sigma_sell=1.895
- Sells when RSI breaks above the upper dispersion zone
- Captures regression after momentum extremes

### 4.2 Sell Conditions Summary

| Signal | Trigger Condition | Parameter Configuration |
|--------|-------------------|------------------------|
| Sell #1 | RSI > 72 | rsi_high=72 |
| Sell #2 | RSI > basis + (dev × 1.895) | for_ma_length_sell=65 |

### 4.3 Sell Configuration

```python
use_sell_signal = True  # Enable sell signals
sell_profit_only = True  # Only sell when profitable
sell_profit_offset = 0.01  # 1% profit offset
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Momentum Indicator | RSI(14) | Core entry/exit judgment |
| Momentum Indicator | RSI(4) | Short-period RSI used in variants |
| Volatility Indicator | RSI Bollinger Band | Dispersion threshold calculation |
| Trend Indicator | EWO(5,200) | Trend direction filter |
| Auxiliary Indicator | EMA | RSI Bollinger Band baseline calculation |
| Auxiliary Indicator | STDDEV | Dispersion calculation |

### 5.2 Indicator Calculation Code Analysis

```python
# RSI calculation
dataframe['rsi'] = ta.RSI(dataframe['close'], 14)
dataframe['rsi_4'] = ta.RSI(dataframe['close'], 4)

# RSI Bollinger Band (for buy)
dataframe[f'basis_{for_ma_length}'] = ta.EMA(dataframe['rsi'], for_ma_length)
dataframe[f'dev_{for_ma_length}'] = ta.STDDEV(dataframe['rsi'], for_ma_length)

# RSI Bollinger Band (for sell)
dataframe[f'basis_{for_ma_length_sell}'] = ta.EMA(dataframe['rsi'], for_ma_length_sell)
dataframe[f'dev_{for_ma_length_sell}'] = ta.STDDEV(dataframe['rsi'], for_ma_length_sell)

# EWO calculation
dataframe['EWO'] = EWO(dataframe, fast_ewo=50, slow_ewo=200)
```

---

## VI. Risk Management Features

### 6.1 Layered Protection Mechanism

The strategy uses a two-layer protection mechanism to prevent consecutive losses:

**First Layer: Low Profit Pair Protection**
- Lookback period: 60 candles (5 hours)
- Trigger condition: Single trade loss exceeds 5%
- Protection measure: Pause that trading pair for 60 minutes

**Second Layer: Maximum Drawdown Protection**
- Lookback period: 24 candles (2 hours)
- Trigger condition: Cumulative drawdown exceeds 20%
- Protection measure: Pause all trading for 12 candles (1 hour)

### 6.2 Trailing Stop Design

```python
trailing_stop = True
trailing_stop_positive = 0.005  # 0.5%
trailing_stop_positive_offset = 0.025  # 2.5%
trailing_only_offset_is_reached = True
```

**Mechanism Description**:
- Trailing stop only activates when profit reaches 2.5%
- Trailing stop distance is 0.5%
- This design avoids premature activation during minor profits or floating losses

### 6.3 Tiered Exit Control

```python
sell_profit_only = True
sell_profit_offset = 0.01
```

- Only responds to sell signals when profitable
- 1% profit offset ensures minimum profit

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Innovative Indicator Combination**: Applying Bollinger Bands to RSI rather than price creates a new momentum dispersion analysis method, avoiding false signals from traditional price Bollinger Bands in high-volatility markets.

2. **Precise Trend Filtering**: EWO as a trend filter, using 5/200 EMA difference, effectively identifies pullback buying opportunities in uptrends, avoiding "catching falling knives" in downtrends.

3. **Large Parameter Optimization Space**: Provides 5 optimizable parameters (for_ma_length, for_sigma, ewo_high, for_ma_length_sell, for_sigma_sell), suitable for tuning to different market environments.

4. **Rich Variants**: The strategy includes 5 variant versions (BBRSITV1-5), each optimized for different market characteristics, allowing users to choose based on backtest results.

5. **Comprehensive Protection Mechanism**: Dual protection mechanism (low profit protection + max drawdown protection) effectively prevents consecutive losses from expanding.

### ⚠️ Limitations

1. **Timeframe Sensitivity**: 5-minute timeframe demands low network latency and fast execution, unsuitable for high-latency environments or manual trading.

2. **Strong Parameter Sensitivity**: Small changes in sigma parameters (dispersion coefficient) can lead to significantly different trading results, requiring thorough backtesting verification.

3. **Trend Dependency**: The strategy core relies on EWO trend filtering, which may produce consecutive false signals in ranging markets or at trend reversal points.

4. **Wide Stop Loss**: 25% fixed stop loss may be too loose for accounts with lower risk tolerance.

5. **No Volume Analysis**: Only uses basic volume > 0 filter, without incorporating volume trend or volume confirmation mechanisms.

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Uptrend | Use default parameters | EWO filter effectively captures pullback buying opportunities in trends |
| Ranging Market | Adjust ewo_high parameter lower | Or consider using BBRSITV4/BBRSITV5 variants |
| High Volatility Market | Increase for_sigma value | Widen dispersion threshold, reduce trade frequency but improve quality |
| Low Volatility Market | Decrease for_sigma value | Tighten dispersion threshold, capture smaller momentum fluctuations |

---

## IX. Applicable Market Environment Details

BBRSITV is a classic technical analysis strategy in the Freqtrade ecosystem. Based on its code architecture and long-term community live trading verification, it performs best in **trending bull markets**, while performing poorly during **sustained downtrends or剧烈 volatile markets**.

### 9.1 Strategy Core Logic

- **Counter-trend Entry**: When trend is upward, wait for RSI to break below Bollinger Band lower dispersion zone to buy
- **Trend Confirmation**: Use EWO to ensure major trend is upward, avoid bottom-fishing in downtrends
- **Trend-following Exit**: Take profits when RSI enters overbought zone or breaks above upper dispersion zone

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:-----------|:-------------------|:---------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | EWO filter effective, precisely captures pullback entry points, trend continuation high |
| 🔄 Mild Range | ⭐⭐⭐☆☆ | RSI dispersion captures range oscillation, but profit limited without directionality |
| 📉 Sustained Downtrend | ⭐⭐☆☆☆ | EWO filter blocks most buy signals, extremely low trading frequency |
| ⚡ High Volatility No Trend | ⭐☆☆☆☆ | Frequent false breakouts, RSI dispersion signals easily shaken out |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Timeframe | 5m (default) | Can also try 15m to reduce trade frequency |
| Number of Trading Pairs | 3-5 pairs | Avoid over-diversification causing frequent protection triggers |
| Minimum Profit Target | 5-10% | Match ROI and trailing stop configuration |
| Backtest Period | 3-6 months | Need to cover different market environments for verification |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

BBRSITV's core concept "RSI Bollinger Band Dispersion" requires some time to understand. Unlike traditional "RSI < 30 buy", this strategy calculates RSI's deviation from its own mean, requiring users to have good understanding of Bollinger Band principles and momentum indicators.

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-3 pairs | 1GB | 2GB |
| 4-8 pairs | 2GB | 4GB |
| 9+ pairs | 4GB | 8GB |

### 10.3 Differences Between Backtesting and Live Trading

Due to the strategy using relatively complex indicator combinations and dynamic thresholds, pay special attention during backtesting:
- Sufficient startup candles (startup_candle_count = 30)
- Avoid using too short historical data
- Note buy/sell parameter differences (buy uses for_ma_length=22, sell uses for_ma_length_sell=65)

### 10.4 Manual Trader Recommendations

Not recommended for manual traders due to:
- 5-minute timeframe requires frequent monitoring
- Indicator calculations need real-time RSI Bollinger Band updates
- EWO calculation depends on 200-period EMA, manual calculation difficult

---

## XI. Strategy Variants Description

BBRSITV strategy includes 5 variant versions, each designed for different optimization objectives:

### BBRSITV1
- Parameter optimization result, for_ma_length=12 (shorter Bollinger Band period)
- Sell parameters: for_ma_length_sell=78, rsi_high=60
- Suitable for: Quick response to market changes

### BBRSITV2
- Parameter optimization result, for_sigma=2.066 (wider dispersion threshold)
- Sell: rsi_high=87 (looser sell condition)
- Suitable for: Markets with strong trend continuation

### BBRSITV3
- Parameters close to default, but more aggressive trailing stop
- trailing_stop_positive=0.078 (7.8%)
- Suitable for: Pursuing higher profit margins

### BBRSITV4
- Added EWO range limit (EWO < 10 or EWO >= 10 and RSI < 40)
- Added RSI(4) < 25 filter
- Stricter buy conditions, higher win rate

### BBRSITV5
- Most complex version, added custom stop loss function
- Tiered stop loss mechanism: larger profit means tighter stop
- Startup candle count increased to 400
- Suitable for: Users pursuing refined risk control

---

## XII. Conclusion

**BBRSITV** is a strategy that innovatively applies Bollinger Band concepts to the RSI indicator. Its core value lies in:

1. **Indicator Innovation**: RSI dispersion concept provides a new method for momentum overbought/oversold judgment, avoiding limitations of traditional RSI fixed thresholds (30/70).

2. **Robust Trend Filtering**: EWO indicator as a trend filter, using long/short EMA difference, effectively identifies trend direction, avoiding counter-trend trading.

3. **Flexible Parameter Tuning**: Buy and sell parameters are separated, can be independently optimized for different market stages, 5 variants provide rich selection space.

For quantitative traders, it's recommended to start with default parameters, verify on 3-6 months of backtest data, and select the variant best suited for current market environment based on backtest results. Also pay attention to protection mechanism configuration to ensure timely stops during consecutive losses.

---

**Strategy File Location**: `/home/neozh/freqtrade-strategies/strategies/BBRSITV/BBRSITV.py`  
**Strategy Author**: Freqtrade Community  
**Ported From**: TradingView - "RSI + BB (EMA) + Dispersion (2.0)"