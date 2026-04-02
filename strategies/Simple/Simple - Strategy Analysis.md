# Simple Strategy - In-Depth Analysis

> **Strategy ID**: #383 (383rd of 465 strategies)  
> **Strategy Type**: Trend Following + Momentum Confirmation  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

Simple is a trend-following strategy based on the book "The Simple Strategy" by Gert Wohlgemuth. The core concept is elegantly simple: use MACD to determine trend direction, combine with Bollinger Bands to confirm trend strength, and employ RSI as an entry filter to form a simple yet complete trading system.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 buy signal, MACD + Bollinger Band + RSI triple confirmation |
| **Sell Conditions** | 1 sell signal, RSI overbought exit |
| **Protection Mechanism** | Fixed stop-loss + Fixed take-profit |
| **Timeframe** | 5 minutes (5m) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.01  # Exit at 1% profit
}

# Stop-loss setting
stoploss = -0.25  # 25% fixed stop-loss
```

**Design Philosophy**:
- Adopts an ultra-simple take-profit strategy: exit immediately upon reaching 1% profit
- Stop-loss is relatively wide (25%), providing sufficient room for price fluctuation
- This "quick in, quick out" design suits short-term volatility trading

### 2.2 Order Type Configuration

The strategy uses default order type configuration without explicitly defining `order_types`, employing Freqtrade's default market order settings.

---

## III. Buy Conditions Explained

### 3.1 Single Buy Signal

The strategy employs a single-signal entry design with clear logic:

```python
# Buy signal
(
    (dataframe['macd'] > 0) &                              # MACD above zero line
    (dataframe['macd'] > dataframe['macdsignal']) &        # MACD crosses above signal line
    (dataframe['bb_upperband'] > dataframe['bb_upperband'].shift(1)) &  # Bollinger upper band trending up
    (dataframe['rsi'] > 70)                                # RSI above 70 (strong zone)
)
```

**Condition Breakdown**:

| Condition | Technical Meaning | Logic Explanation |
|-----------|-------------------|-------------------|
| MACD > 0 | Trend confirmation | Price above moving average, bullish trend established |
| MACD > Signal | Momentum confirmation | MACD line crosses above signal line, momentum strengthening |
| BB Upper trending up | Volatility expansion | Bollinger upper band moving up, price breaking through upper boundary |
| RSI > 70 | Overbought zone | Price entering strong territory |

### 3.2 Buy Logic Analysis

This is a classic **trend breakout strategy**:
1. **MACD > 0**: Confirms bullish trend, price is supported above moving average
2. **MACD crosses above signal line**: Waits for MACD golden cross confirmation, avoiding false breakouts
3. **Bollinger upper band trending up**: Price breaks through Bollinger band, volatility expansion
4. **RSI > 70**: Although in overbought territory, in strong trends, overbought can become more overbought

---

## IV. Sell Logic Explained

### 4.1 Sell Signal

```python
# Sell signal
(dataframe['rsi'] > 80)
```

**Design Philosophy**:
- Triggers sell when RSI reaches 80 or above
- This is an "extreme overheating" exit mechanism
- Hold between 70-80 to let profits run

### 4.2 Sell Logic Characteristics

| Characteristic | Explanation |
|----------------|-------------|
| **Simple and direct** | Relies only on single RSI indicator |
| **Profit margin** | RSI from 70 to 80 typically has some price gain |
| **Risk control** | Avoid excessive chasing of highs, timely profit-taking |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|--------------------|-------------------|------------|---------|
| Trend Indicator | MACD | Default parameters | Trend direction determination, momentum confirmation |
| Momentum Indicator | RSI | Period 7 | Entry filter, exit signal |
| Volatility Indicator | Bollinger Bands | Period 12, Std Dev 2 | Volatility expansion confirmation |

### 5.2 Indicator Calculation

```python
# MACD indicator
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']
dataframe['macdhist'] = macd['macdhist']

# RSI indicator (period 7, shorter)
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=7)

# Bollinger Bands (period 12, std dev 2)
bollinger = qtpylib.bollinger_bands(dataframe['close'], window=12, stds=2)
dataframe['bb_lowerband'] = bollinger['lower']
dataframe['bb_upperband'] = bollinger['upper']
dataframe['bb_middleband'] = bollinger['mid']
```

---

## VI. Risk Management Features

### 6.1 Fixed Take-Profit and Stop-Loss

| Parameter | Setting | Description |
|-----------|---------|-------------|
| Take-profit | 1% | Quickly lock in profits |
| Stop-loss | 25% | Relatively wide stop-loss space |

**Characteristics**:
- Take-profit is very aggressive, exiting at just 1%
- Stop-loss is relatively wide, avoiding frequent stops
- This design suits high win-rate, quick in-out trading styles

### 6.2 No Trailing Stop

The strategy doesn't configure trailing stop, employing fixed take-profit and stop-loss mechanisms with simple and clear logic.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple logic**: Buy and sell conditions are clear and explicit, easy to understand and debug
2. **Few parameters**: Relies on only 3 core indicators, low overfitting risk
3. **Fast execution**: Low computational load, suitable for high-frequency trading scenarios
4. **Classic strategy**: Based on published trading strategy book with theoretical foundation

### ⚠️ Limitations

1. **Stop-loss too wide**: 25% stop-loss may lead to significant drawdown
2. **Take-profit too early**: 1% take-profit may miss major trend movements
3. **RSI 70 entry**: Entering in overbought territory carries pullback risk
4. **No trailing stop**: Cannot lock in floating profits, may give back gains

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Explanation |
|--------------------|---------------------------|-------------|
| Strong trend market | Default configuration | Quick profit-taking to capture short-term volatility |
| Ranging market | Not recommended | RSI strategy prone to repeated whipsaws in ranging markets |
| High volatility market | Narrower stop-loss | 25% stop-loss may be too large |
| Low volatility market | Wider take-profit | 1% may be too small |

---

## IX. Applicable Market Environment Details

Simple strategy is a classic **short-term trend breakout strategy**. Based on its code architecture and design philosophy, it is most suitable for **strong trend markets** and performs poorly in ranging markets.

### 9.1 Strategy Core Logic

- **Follow the trend**: MACD > 0 confirms bullish trend
- **Momentum confirmation**: MACD golden cross validates momentum
- **Breakout entry**: Bollinger upper band trending up confirms breakout
- **Extreme holding**: Hold when RSI > 70, exit when above 80

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Strong trend market | ⭐⭐⭐⭐☆ | RSI overbought can become more overbought, trend-following works well |
| 🔄 Ranging market | ⭐⭐☆☆☆ | RSI repeatedly crosses 70-80 zone, prone to whipsaws |
| 📉 Downtrend | ⭐☆☆☆☆ | Buy conditions difficult to trigger, may miss or trade against trend |
| ⚡️ High volatility | ⭐⭐⭐☆☆ | Wide stop-loss may save the trade, but carries higher risk |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| timeframe | 5m | Keep default, optimal for short-term |
| stoploss | -0.10 ~ -0.15 | Recommend narrowing stop-loss |
| minimal_roi | 0.02 | Consider raising take-profit target |

---

## X. Important Note: The Cost of Simplification

### 10.1 Learning Curve

Simple strategy has an extremely low learning curve:
- Only 3 indicators, approximately 60 lines of code
- No complex parameters, beginner-friendly
- Intuitive logic, easy to understand and modify

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-10 pairs | 1GB | 2GB |
| 10-50 pairs | 2GB | 4GB |
| 50+ pairs | 4GB | 8GB |

### 10.3 Backtest vs Live Trading Differences

- Backtesting may overestimate gains in RSI 70-80 zone
- In live trading, slippage and fees may erode the 1% profit
- Recommend reserving 0.1-0.2% profit buffer

### 10.4 Recommendations for Manual Traders

This strategy has clear logic suitable for manual traders to learn:
1. Observe if MACD is above zero line
2. Wait for MACD golden cross confirmation
3. Confirm Bollinger upper band trending up
4. Enter after RSI breaks above 70
5. Exit when RSI reaches 80 or profit hits 1%

---

## XI. Summary

**Simple** lives up to its name as a "simple" strategy. Its core value lies in:

1. **Minimalist design**: Builds complete trading system with only 3 indicators
2. **Clear logic**: Buy and sell conditions are explicit, no ambiguity
3. **Easy to optimize**: Few parameters, clear optimization space

For quantitative traders, Simple strategy is an excellent entry choice and can serve as a foundational framework for expanding into more complex strategies. However, attention must be paid to its overly wide stop-loss and premature take-profit issues, and parameter adjustment based on actual market conditions is recommended.

---