# NowoIchimoku1hV1 Strategy Analysis

## Table of Contents

1. [Strategy Overview](#1-strategy-overview)
2. [Theoretical Foundation](#2-theoretical-foundation)
3. [Technical Indicator System](#3-technical-indicator-system)
4. [Entry Signal Construction](#4-entry-signal-construction)
5. [Exit Signal Logic](#5-exit-signal-logic)
6. [Risk Management System](#6-risk-management-system)
7. [Parameter Configuration](#7-parameter-configuration)
8. [Trading Execution Process](#8-trading-execution-process)
9. [Strategy Advantages Analysis](#9-strategy-advantages-analysis)
10. [Strategy Limitations](#10-strategy-limitations)
11. [Optimization Suggestions](#11-optimization-suggestions)

---

## 1. Strategy Overview

NowoIchimoku1hV1 is a trend-following trading strategy that combines the Ichimoku Kinko Hyo (Ichimoku Cloud) with the Stochastic Relative Strength Index (Stochastic RSI). Designed for the 1-hour (1h) timeframe, this strategy identifies high-quality entry opportunities in medium-to-long-term trends through multi-layered technical indicator confirmation.

The core philosophy centers on "follow the trend, multi-dimensional confirmation." It not only uses the price-to-cloud relationship to judge trend direction but also incorporates the Bollinger Bands upper band, the relative positions of the Conversion Line and Base Line, and a unique "buy cooldown" mechanism to construct a relatively complete trend trading system.

### 1.1 Strategy Positioning

This strategy belongs to the **medium-to-low-frequency trend-following** category, suitable for cryptocurrency markets with moderate volatility. As noted in the code comment "This version of the strategy is broken!", this strategy version may be in an experimental or debugging stage, requiring sufficient backtesting validation before actual use.

### 1.2 Timeframe

The strategy adopts 1 hour (1h) as its primary timeframe, with the following considerations:
- Balances trading signal quality and frequency
- Effectively filters high-frequency market noise
- Suitable for traders not requiring full-time market monitoring
- Reserves 100 candles for the startup period, ensuring indicator calculation stability

---

## 2. Theoretical Foundation

### 2.1 Ichimoku Cloud Theory

The Ichimoku Cloud was invented by Japanese technical analyst Goshu Hosoda in the 1960s. It is a comprehensive trend analysis tool consisting of five core curves:

**Conversion Line (Tenkan-sen)**
- Calculation: (Highest High + Lowest Low) over the past 9 periods ÷ 2
- Function: Reflects short-term market trends as a fast signal line

**Base Line (Kijun-sen)**
- Calculation: (Highest High + Lowest Low) over the past 26 periods ÷ 2
- Function: Reflects medium-term market trends as a support/resistance reference

**Leading Span A (Senkou Span A)**
- Calculation: (Conversion Line + Base Line) / 2, shifted forward 26 periods
- Function: Forms the upper (or lower) boundary of the cloud

**Leading Span B (Senkou Span B)**
- Calculation: (Highest High + Lowest Low) over the past 52 periods ÷ 2, shifted forward 26 periods
- Function: Forms the other boundary of the cloud

**Chikou Span (Lagging Span)**
- Calculation: Current closing price shifted backward 26 periods
- Function: Used to confirm trend direction

This strategy primarily leverages the cloud's color (green for bullish, red for bearish) and the relative position of the Conversion Line versus the Base Line.

### 2.2 Stochastic Relative Strength Index

Stochastic RSI applies the stochastic formula to RSI values, offering higher sensitivity than plain RSI or stochastic indicators. The calculation:

1. Calculate 14-period RSI first
2. Apply 14-period stochasticization to RSI values
3. Smooth the result (K line with 3-period smoothing, D line with 3-period smoothing)

Stochastic RSI oscillates between 0 and 100:
- K value above 80 indicates overbought
- K value below 20 indicates oversold

### 2.3 Bollinger Bands Theory

This strategy uses the Bollinger Bands upper band based on the Hull Moving Average (HMA) as an auxiliary tool. Traditional Bollinger Bands use SMA, while this strategy uses HMA, which has faster response speed and less lag.

Upper band formula:
```
Upper Band = HMA(close, 20) + 2.5 × STDDEV(close, 20)
```

The 2.5× multiplier is more relaxed than the traditional 2.0×, designed to reduce false breakout signals.

---

## 3. Technical Indicator System

### 3.1 Bollinger Bands Upper Band

The strategy uses a custom `bollinger_bands` function to calculate the upper band:

```python
def bollinger_bands(series, moving_average='sma', length=20, mult=2.0):
    basis = hma(series, length)
    dev = mult * ta.STDDEV(series, length)
    return {'upper': basis + dev}
```

HMA calculation involves weighted moving average (WMA) combinations:

```python
def hma(series, length):
    h = 2 * wma(series, length/2) - wma(series, length)
    return wma(h, sqrt(length))
```

HMA's characteristics: good smoothness with low lag, capturing price changes more quickly.

### 3.2 Ichimoku Indicators

The strategy uses the `technical.indicators.ichimoku` function:

```python
ichi = indicators.ichimoku(df)
df['conversion_line'] = ichi['tenkan_sen']
df['base_line'] = ichi['kijun_sen']
df['lead_1'] = ichi['leading_senkou_span_a']
df['lead_2'] = ichi['leading_senkou_span_b']
df['cloud_green'] = ichi['cloud_green']
```

The strategy also calculates cloud boundaries:
- `upper_cloud`: the larger of Leading Span A and B
- `lower_cloud`: the smaller of Leading Span A and B

With 25-period displacement:
- `shifted_upper_cloud`: displaced upper cloud boundary
- `shifted_lower_cloud`: displaced lower cloud boundary

### 3.3 Stochastic RSI Indicator

The strategy manually implements Stochastic RSI:

```python
smoothK = 3
smoothD = 3
lengthRSI = 14
lengthStoch = 14

df['rsi'] = ta.RSI(df, timeperiod=14)

stochrsi = (rsi - rsi_min) / (rsi_max - rsi_min)
df['srsi_k'] = stochrsi.rolling(3).mean() * 100
df['srsi_d'] = df['srsi_k'].rolling(3).mean()
```

---

## 4. Entry Signal Construction

### 4.1 Buy Signal Conditions

The strategy's buy signal uses an AND-logic combination of multiple conditions:

**Condition 1: Bullish Candle**
```python
df['close'] > df['open']
```
Current candle is bullish — closing price higher than opening price, showing buyers have the upper hand.

**Condition 2: Break Above Upper Cloud**
```python
df['close'] > df['shifted_upper_cloud'] * 1.04
```
Closing price exceeds 104% of the displaced upper cloud boundary, indicating effective breakout above Ichimoku resistance.

**Condition 3: Above Lower Cloud**
```python
df['close'] > df['shifted_lower_cloud']
```
Closing price above the displaced lower cloud boundary, ensuring price is above the cloud's support.

**Condition 4: Bullish Cloud**
```python
df['is_cloud_green'] = df['lead_1'] > df['lead_2']
```
Leading Span A above Leading Span B, forming a green (bullish) cloud.

**Condition 5: Conversion Line Above Base Line**
```python
df['conversion_line'] > df['base_line']
```
Conversion Line above Base Line — short-term trend upward.

**Condition 6: Price Above Displaced Conversion Line**
```python
df['close'] > df['conversion_line'].shift(25)
```
Closing price above the 25-period-displaced Conversion Line, confirming trend continuation.

**Condition 7: Double-Displaced Cloud Confirmation**
```python
df['close'] > df['upper_cloud'].shift(50)
```
Closing price above the 50-period-displaced upper cloud boundary, providing stronger trend confirmation.

### 4.2 Buy Cooldown Mechanism

The strategy implements a unique "buy cooldown" mechanism to prevent consecutive buying after the cloud turns green:

```python
df['buy_allowed'] = -df['is_cloud_green']

for i in range(101, len(df)):
    df.loc[i, 'buy_allowed'] = df.loc[i - 1, 'buy_allowed']
    if df.loc[i - 1, 'buy']:
        df.loc[i, 'buy_allowed'] = False
    elif not df.loc[i, 'is_cloud_green']:
        df.loc[i, 'buy_allowed'] = True
```

Logic:
1. When the cloud turns from green to red, reset the buy permission flag
2. When the cloud turns green again, allow new buy signals
3. After buying, prohibit continued buying until the cloud turns red again

Note: There is a potential bug in the code — `df[i, 'buy_allowed']` should be `df.loc[i, 'buy_allowed']`.

---

## 5. Exit Signal Logic

### 5.1 Custom Sell Function

The strategy implements exit logic through the `custom_sell` function with four exit conditions:

**Condition 1: Stochastic RSI Overbought Profit-Taking**
```python
if last_candle['srsi_k'] > 80 & current_profit > 1.1:
    return 'srsi_k above 80 with profit above 10%'
```
When Stochastic RSI K value exceeds 80 and profit exceeds 10%, close for profit.

**Condition 2: Bollinger Upper Band Break Profit-Taking**
```python
if current_rate > last_candle['upper'] & current_profit > 1.01:
    return 'current rate above upper band with profit above 1%'
```
When current price breaks the Bollinger upper band and profit exceeds 1%, close for profit.

**Condition 3: Dynamic Target Price Reached**
```python
limit = trade_candle['close'] + ((trade_candle['close'] - trade_candle['shifted_lower_cloud']) * 2)
if current_rate > limit:
    return 'current rate above limit'
```
Dynamic target price formula:
```
Target Price = Entry Closing Price + 2 × (Entry Closing Price - Entry Displaced Lower Cloud)
```

**Condition 4: Below Stop-Loss Level**
```python
if current_rate < trade_candle['shifted_lower_cloud']:
    return 'current rate below stop'
```
When current price falls below the entry's displaced lower cloud boundary, execute stop-loss.

### 5.2 Important Warning

The code has a logic error — it uses the bitwise operator `&` instead of the logical `and`:
```python
# Wrong
last_candle['srsi_k'] > 80 & current_profit > 1.1

# Correct
(last_candle['srsi_k'] > 80) and (current_profit > 1.1)
```

The `&` operator has higher precedence than comparison operators, causing logic errors.

---

## 6. Risk Management System

### 6.1 Stop-Loss Settings

The strategy configures -8% fixed stop-loss:
```python
stoploss = -0.08
```

When losses reach 8%, the system auto-closes the position.

### 6.2 Custom Stop-Loss Function

```python
def custom_stoploss(...):
    return 1
```

This function returns 1, meaning the custom stop-loss is actually disabled (a return value of 1 means 100% trailing stop, i.e., never triggers). This contradicts `use_custom_stoploss = True` and may be a placeholder implementation or misconfiguration.

### 6.3 Minimal ROI

The strategy adopts a stepped ROI configuration:
```python
minimal_roi = {
    "0": 0.10,   # Immediately after opening: target 10%
    "30": 0.05,  # After 30 minutes: target drops to 5%
    "60": 0.02   # After 60 minutes: target drops to 2%
}
```

This reflects a **time-decaying profit expectation**:
- Early trade (first 30 minutes): higher return expectation (10%)
- As time passes: lower return expectation
- After 1 hour: only 2% required to close for profit

### 6.4 Disabled Sell Signal

```python
use_sell_signal = False
```

The strategy disables standard sell signals, relying entirely on `custom_sell` and ROI/stop-loss mechanisms for exits.

---

## 7. Parameter Configuration

### 7.1 Core Parameters Overview

| Parameter | Value | Description |
|-----------|-------|-------------|
| timeframe | '1h' | Primary timeframe |
| startup_candle_count | 100 | Candles needed at startup |
| use_sell_signal | False | Disable standard sell signals |
| use_custom_stoploss | True | Enable custom stop-loss |
| stoploss | -0.08 | Fixed stop-loss 8% |

### 7.2 Bollinger Bands Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| length | 20 | Moving average period |
| mult | 2.5 | Standard deviation multiplier |
| moving_average | 'hma' | Hull Moving Average |

### 7.3 Stochastic RSI Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| smoothK | 3 | K line smoothing period |
| smoothD | 3 | D line smoothing period |
| lengthRSI | 14 | RSI calculation period |
| lengthStoch | 14 | Stochastic period |

---

## 8. Trading Execution Process

### 8.1 Signal Generation Flow

```
1. Data Preparation
   └─ Load at least 100 1-hour candles

2. Indicator Calculation
   ├─ Calculate Bollinger upper band (HMA-based)
   ├─ Calculate Ichimoku Cloud lines
   └─ Calculate Stochastic RSI

3. Entry Judgment
   ├─ Check seven buy conditions
   ├─ Check buy cooldown status
   └─ Generate buy signal

4. Position Management
   ├─ Monitor stop-loss level
   ├─ Monitor ROI targets
   └─ Check custom sell conditions

5. Exit Execution
   ├─ Stop-loss triggered
   ├─ ROI target reached
   └─ Custom sell condition met
```

### 8.2 Buy Signal Example

When the following conditions are met, a buy is triggered:
- 1-hour candle closed higher than it opened
- Closing price: 50,000 USDT
- Displaced upper cloud: 47,000 USDT (50,000 > 47,000 × 1.04 = 48,880)
- Displaced lower cloud: 46,000 USDT (50,000 > 46,000)
- Cloud is green (bullish)
- Conversion Line above Base Line
- Closing price above 25-period-displaced Conversion Line
- Closing price above 50-period-displaced upper cloud

### 8.3 Sell Signal Examples

**Scenario 1: Stochastic RSI Overbought**
- K value reaches 85
- Current profit 12%
- Sell triggered: "srsi_k above 80 with profit above 10%"

**Scenario 2: Bollinger Upper Band Break**
- Current price 52,000 USDT
- Bollinger upper band 51,500 USDT
- Current profit 4%
- Sell triggered: "current rate above upper band with profit above 1%"

**Scenario 3: Dynamic Target Reached**
- Dynamic target = 50,000 + 2 × (50,000 - 46,000) = 58,000 USDT
- Current price 58,500 USDT
- Sell triggered: "current rate above limit"

**Scenario 4: Cloud Support Broken**
- Current price 45,500 USDT
- Below displaced lower cloud 46,000 USDT
- Sell triggered: "current rate below stop"

---

## 9. Strategy Advantages Analysis

### 9.1 Multi-Dimensional Confirmation Mechanism

With seven-condition combination for buy signals, this multi-dimensional confirmation:
- Effectively filters false breakouts
- Improves signal reliability
- Reduces incorrect trade probability
- Follows multi-timeframe trends

### 9.2 Dynamic Cloud Support/Resistance

Using the Ichimoku Cloud as dynamic support/resistance:
- Cloud boundaries adjust dynamically with market changes
- Predicts future support/resistance zones 26 periods ahead
- Cloud thickness reflects market volatility

### 9.3 Unique Buy Cooldown Mechanism

The buy cooldown mechanism:
- Prevents consecutive buying during trend oscillations
- Ensures entries only at early trend stages
- Resets buy state through cloud color changes

### 9.4 Tiered Exit Strategy

Through the combination of stop-loss, ROI, and custom sell conditions:
- Quick profit: Bollinger upper band breakout
- Overbought profit: Stochastic RSI overbought
- Target profit: Dynamic target price
- Protective stop: Cloud support broken

---

## 10. Strategy Limitations

### 10.1 Code Defects

**Bitwise Operator Error**
```python
# Problem code
last_candle['srsi_k'] > 80 & current_profit > 1.1

# Correct
(last_candle['srsi_k'] > 80) and (current_profit > 1.1)
```

**Index Error**
```python
# Problem code
df[i, 'buy_allowed'] = True

# Correct
df.loc[i, 'buy_allowed'] = True
```

**Custom Stop-Loss Ineffective**
```python
def custom_stoploss(...):
    return 1  # Return of 1 means stop-loss never triggers
```

### 10.2 Strategy Defects

**Lack of Short-Selling Mechanism**
The strategy only implements long logic and cannot profit in downtrends.

**Lag Issue**
Multiple displacement operations may cause signal lag:
- 25-period displaced cloud
- 50-period double-displaced confirmation

**Fixed Parameters**
All parameters are fixed values, lacking adaptive mechanisms, potentially unable to adapt to different market environments.

### 10.3 Known Issues

The code header explicitly states "This version of the strategy is broken!", indicating known issues exist and live trading is not recommended.

---

## 11. Optimization Suggestions

### 11.1 Code Fixes

**Fix Bitwise Operator**
```python
if last_candle['srsi_k'] > 80 and current_profit > 0.1:
    return 'srsi_k above 80 with profit above 10%'
```

**Fix Index Error**
```python
df.loc[i, 'buy_allowed'] = True
```

**Implement Effective Custom Stop-Loss**
```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if current_profit > 0.05:
        return current_profit - 0.03
    return self.stoploss
```

### 11.2 Strategy Enhancement

**Add Short-Selling Logic**
```python
def populate_entry_trend(self, df, metadata):
    # Existing long logic
    ...
    
    # Add short logic
    df.loc[
        (df['close'] < df['open']) &
        (df['close'] < df['shifted_lower_cloud'] * 0.96) &
        (df['conversion_line'] < df['base_line']) &
        (~df['is_cloud_green']),
        'sell_short'
    ] = 1
```

**Add ADX Filter**
```python
df['adx'] = ta.ADX(df, timeperiod=14)
df['should_buy'] = df['should_buy'] & (df['adx'] > 25)
```

### 11.3 Backtesting Recommendations

1. **Historical Data Backtesting**: At least 1 year, multiple trading pairs, 0.1% buy + 0.1% sell fees
2. **Parameter Optimization**: Use Hyperopt, perform Walk-Forward Analysis, avoid overfitting
3. **Stress Testing**: Test extreme conditions, check maximum drawdown, evaluate consecutive loss days
4. **Simulated Trading**: Run in Paper Trading for 1-3 months, record all signals and execution

---

## Summary

NowoIchimoku1hV1 is an Ichimoku Cloud-based trend-following system that identifies trading opportunities through multi-condition confirmation and dynamic support/resistance levels. Its core advantages lie in the multi-dimensional confirmation mechanism and unique buy cooldown design, but it currently has code defects and strategy limitations.

Before using this strategy, known code errors must be fixed and sufficient backtesting validation is required. It is recommended to adjust parameters according to market conditions and consider adding short-selling logic and adaptive mechanisms to improve strategy stability and profitability.

---

*Document Version: v1.0*
*Applicable Strategy Version: NowoIchimoku1hV1*
*Generated: March 27, 2026*
