# NowoIchimoku5mV2 Strategy Analysis

## Table of Contents

1. [Strategy Overview and Technical Framework](#1-strategy-overview-and-technical-framework)
2. [Market Theory Foundation](#2-market-theory-foundation)
3. [Indicator System](#3-indicator-system)
4. [Entry Signal Logic](#4-entry-signal-logic)
5. [Exit Mechanism Design](#5-exit-mechanism-design)
6. [Risk Control System](#6-risk-control-system)
7. [Parameter Optimization Space](#7-parameter-optimization-space)
8. [Backtesting Framework Configuration](#8-backtesting-framework-configuration)
9. [Live Deployment Advice](#9-live-deployment-advice)
10. [Strategy Pros & Cons Analysis](#10-strategy-pros--cons-analysis)
11. [Conclusion and Improvement Directions](#11-conclusion-and-improvement-directions)

---

## 1. Strategy Overview and Technical Framework

### 1.1 Strategy Positioning

NowoIchimoku5mV2 is a trend-following strategy designed specifically for the cryptocurrency market, adopting a dual-timeframe analysis method with 5 minutes as the primary trading timeframe and 1 hour as the informative timeframe. The "Nowo" in the name implies innovative improvement, while "Ichimoku" indicates the core logic is built upon the classic Ichimoku Cloud indicator system.

### 1.2 Technical Architecture

Built on the Freqtrade quantitative trading framework, an open-source cryptocurrency trading engine, the strategy uses object-oriented design, inheriting from the IStrategy base class and implementing complete lifecycle hook functions.

```python
class NowoIchimoku5mV2(IStrategy):
    timeframe = '5m'
    informative_timeframe = '1h'
```

### 1.3 Core Design Philosophy

The strategy's design philosophy can be summarized as "follow the trend, cloud as the boundary." It identifies market trend direction through the Ichimoku Cloud, dynamically adjusts risk exposure using Bollinger Bands, enters after trend confirmation, and exits when trends reverse or risks accumulate.

⚠️ **Important Note**: The strategy file header states "This version of the strategy is broken!" — indicating this version may have issues and direct live trading is not recommended. However, the strategy's ideas are valuable for learning.

---

## 2. Market Theory Foundation

### 2.1 Ichimoku Cloud Theory

The Ichimoku Cloud (Ichimoku Kinko Hyo) was invented by Japanese journalist Goshu Hosoda in the 1930s as a technical analysis tool whose core value lies in simultaneously displaying support/resistance, trend direction, and momentum strength.

**Conversion Line (Tenkan-sen)**: The fast-reacting line, calculated as the average of the highest and lowest prices over 9 periods. When price is above this line, short-term sentiment is bullish; below indicates bearish sentiment.

**Base Line (Kijun-sen)**: The medium-term reference line, calculated as the average of the highest and lowest prices over 26 periods. Price above this line indicates relatively strong market status.

**Leading Span A**: Average of Conversion and Base Lines, shifted forward 26 periods. Forms one boundary of the cloud.

**Leading Span B**: Average of the highest and lowest prices over 52 periods, shifted forward 26 periods. Forms the other cloud boundary.

**Chikou Span (Lagging Span)**: Current closing price shifted backward 26 periods, used to confirm trend direction.

### 2.2 Bollinger Bands Theory

Bollinger Bands, developed by John Bollinger in the 1980s, consists of three bands: a middle band (SMA) and upper/lower bands at K× standard deviations. This strategy uses HMA instead of SMA for the middle band, offering lower lag and better smoothness.

### 2.3 StochRSI Theory

StochRSI applies stochastic calculation to RSI values, targeting identification of overbought/oversold extremes. Values above 80 indicate extreme overbought conditions; below 20 indicates extreme oversold.

---

## 3. Indicator System

### 3.1 Timeframe Design

The strategy uses a dual-timeframe structure: 5-minute primary, 1-hour informative. Benefits:

- Reduces noise interference
- Provides forward-looking warning via 1h indicators
- Low-timeframe high-frequency trading risks reduced by multi-timeframe confirmation

### 3.2 Hull Moving Average Algorithm

```python
def hma(series: Series, length: int) -> Series:
    h = 2 * wma(series, math.floor(length / 2)) - wma(series, length)
    hma = wma(h, math.floor(math.sqrt(length)))
    return hma
```

HMA achieves a balance between low lag and high smoothness through a clever weighted combination.

### 3.3 Ichimoku Calculation

```python
ichi_1h = indicators.ichimoku(df_1h)
df_1h['conversion_line'] = ichi_1h['tenkan_sen']
df_1h['base_line'] = ichi_1h['kijun_sen']
df_1h['lead_1'] = ichi_1h['leading_senkou_span_a']
df_1h['lead_2'] = ichi_1h['leading_senkou_span_b']
df_1h['is_cloud_green'] = ichi_1h['cloud_green']
```

Cloud color: Leading Span A > Leading Span B = green (bullish); reverse = red (bearish).

---

## 4. Entry Signal Logic

### 4.1 Multi-Timeframe Data Merge

```python
df = merge_informative_pair(df_5m, df_1h, self.timeframe, self.informative_timeframe, ffill=True)
```

Uses forward fill (ffill) to ensure each 5-minute candle gets the latest 1-hour indicator values.

### 4.2 Core Entry Conditions

Seven conditions must be simultaneously satisfied:

**Condition 1: Bullish Candle** — `close > open`
**Condition 2: Close > shifted_upper_cloud × close_above_shifted_upper_cloud** (default 0.603)
**Condition 3: Close > shifted_lower_cloud**
**Condition 4: `is_cloud_green`** — Leading A > Leading B
**Condition 5: `conversion_line > base_line`** — short-term momentum upward
**Condition 6: `close > conversion_line.shift(25 × time_factor)`** — above 25-period-displaced Conversion Line
**Condition 7: `close > upper_cloud.shift(50 × time_factor)`** — above 50-period-displaced cloud upper

### 4.3 Cooldown Mechanism

```python
df['buy_allowed'] = True
for i in range(1, len(df)):
    if df.at[i - 1, 'buy']:
        df.loc[i, 'buy_allowed'] = False
    if not df.at[i, 'is_cloud_green']:
        df.loc[i, 'buy_allowed'] = True
    df.loc[i, 'buy'] = df.at[i, 'buy_allowed'] & df.at[i, 'should_buy']
```

Logic: Allow buying by default → prohibit after buy → reset when cloud turns red → allow when cloud turns green again. Prevents over-positioning in single trends.

---

## 5. Exit Mechanism Design

### 5.1 Fixed Stop-Loss

```python
stoploss = -0.293
```

A generous -29.3% hard stop — the designer wanted sufficient price fluctuation room.

### 5.2 Custom Stop-Loss Function

Four dynamic stop-loss/exit conditions:

**Trigger 1: StochRSI Overbought**
```python
if (last_candle['srsi_k'] > 80) & (current_profit > srsi_k_min_profit.value):
    return -0.0001
```
When K > 80 AND profit > 3.6% (default), lock in profits.

**Trigger 2: Bollinger Upper Break**
```python
if (previous_candle['close'] < previous_candle['upper']) & \
   (current_rate > last_candle['upper']) & \
   (current_profit > above_upper_min_profit.value):
    return -0.0001
```
When price breaks above upper band AND profit > 1.1% (default), exit.

**Trigger 3: Dynamic Limit**
```python
limit = trade.open_rate + ((trade.open_rate - trade_candle['shifted_lower_cloud']) * limit_factor.value)
if current_rate > limit:
    return -0.0001
```
Target based on entry price minus displaced cloud lower × limit_factor (default 1.918).

**Trigger 4: Cloud Lower Support Failure**
```python
if current_rate < (trade_candle['shifted_lower_cloud'] * lower_cloud_factor.value):
    return -0.0001
```
When price drops below 97.1% (default) of displaced cloud lower, exit.

---

## 6. Risk Control System

### 6.1 Multi-Layer Filter

Seven-entry-condition combination builds a multi-layer risk filter. Each condition verifies trend validity from different angles.

### 6.2 Trailing Stop
```python
trailing_stop = True
```
Trailing stop moves upward with price, locking in profits.

### 6.3 Time-Decaying ROI
```python
minimal_roi = {
    "0": 0.10,
    "30": 0.05,
    "60": 0.02
}
```
Immediate target 10% → 5% after 30 min → 2% after 60 min.

### 6.4 Five Optimizable Parameters
```python
srsi_k_min_profit = DecimalParameter(0.01, 0.99, default=0.036, space="sell")
above_upper_min_profit = DecimalParameter(0.001, 0.5, default=0.011, space="sell")
limit_factor = DecimalParameter(0.5, 5, default=1.918, space="sell")
lower_cloud_factor = DecimalParameter(0.5, 1.5, default=0.971, space="sell")
close_above_shifted_upper_cloud = DecimalParameter(0.5, 2, default=0.603, space="buy")
```

---

## 7. Parameter Optimization Space

**close_above_shifted_upper_cloud** (0.5-2.0, default 0.603): Lower = looser entry; higher = stricter, fewer but higher-quality signals.

**srsi_k_min_profit** (0.01-0.99, default 0.036): Higher = more holding, bigger potential gains but more drawdown risk.

**limit_factor** (0.5-5, default 1.918): Higher = higher targets, longer holding; lower = shorter trades.

**lower_cloud_factor** (0.5-1.5, default 0.971): Lower = tighter stop; higher = more room.

---

## 8. Backtesting Framework Configuration

### 8.1 Startup Candles
```python
startup_candle_count = int(100 * time_factor)  # 500 candles for 5m
```

Requires 500 5-minute candles minimum.

### 8.2 Time Factor
```python
time_factor = int(60 / 5)  # = 12
```

Each 1-hour candle = 12 5-minute candles.

### 8.3 Backtesting Notes

- Ensure complete historical data with no gaps
- Set reasonable slippage parameters (0.5%-1%)
- Set appropriate fee rates (0.1%+)
- Ensure capital management can handle consecutive losses

---

## 9. Live Deployment Advice

### 9.1 Exchange Selection
High-liquidity pairs only: BTC/USDT, ETH/USDT, etc.

### 9.2 Position Management
With -29.3% stop, risk per trade should be 1-3% of total capital.

### 9.3 Key Metrics to Monitor
- Signal frequency (too frequent = adjust parameters)
- Average holding time
- Maximum drawdown
- Win rate and profit/loss ratio

---

## 10. Strategy Pros & Cons Analysis

### Pros
- Strong trend-following capability (Ichimoku is time-tested)
- Dynamic risk management (custom stop-loss)
- Multi-timeframe confirmation (filters noise)
- Flexible parameters (tunable)
- Clean code structure

### Cons
- Stop-loss too wide (-29.3%) — aggressive for most traders
- Entry conditions too strict (7 conditions) — may miss opportunities
- No explicit profit-taking mechanism
- No market state adaptation
- **File header explicitly warns: "strategy is broken"**

---

## 11. Conclusion and Improvement Directions

NowoIchimoku5mV2 has a clear Ichimoku Cloud trend-following design, combining Bollinger Bands volatility analysis with StochRSI overbought/oversold judgment. The dual-timeframe and multi-layer filter mechanisms reflect emphasis on signal quality.

The wide stop-loss and strict entry conditions make it more suitable for traders with higher risk tolerance. The file header warning indicates it may still be in development — caution advised before live use.

**Improvement suggestions**:
1. Tighten stop to -10% ~ -15%
2. Add market state filter (ADX)
3. Optimize entry conditions (5-out-of-7 rather than all-7)
4. Add partial profit-taking mechanism
5. Fix known bugs before use

---

*This document is for Freqtrade strategy learning and research. Please fully understand strategy logic and conduct sufficient backtesting validation before use.*
