# AlligatorStrategy Strategy In-Depth Analysis

> **Strategy ID**: #418 (418th of 465 strategies)  
> **Strategy Type**: EMA Perfect Alignment + Stoch RSI Oversold Reversal  
> **Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

AlligatorStrategy is a trend-following strategy based on multi-period EMA perfect bullish alignment and Stoch RSI oversold reversal. Originating from Crypto Robot's video tutorial, the core concept is to wait for Stoch RSI oversold bounce entries during perfect bullish alignment trends, pursuing high risk-reward ratio trend trading.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 composite buy signal (6 EMA perfect bullish alignment + Stoch RSI oversold) |
| **Sell Conditions** | 1 base sell signal + trailing stop + tiered ROI |
| **Protection Mechanism** | Trailing stop + hyperparameter optimization |
| **Timeframe** | 1 hour (medium timeframe) |
| **Dependencies** | ta (Technical Analysis Library) |
| **Hyperparameters** | buy_stoch_rsi (0.5-1.0), sell_stoch_rsi (0-0.5) |

### Backtest Performance (Author Provided)

| Metric | Value |
|--------|-------|
| Backtest Period | 2020-09-11 to 2021-08-26 |
| Total Trades | 258 |
| Starting Capital | 1,000 USDT |
| Final Capital | 14,245 USDT |
| Total Return | 1324.51% |
| Maximum Drawdown | 169.59% |
| Best Trade | 305.28% |
| Worst Trade | -10.69% |
| Win Rate Days | 8 wins / 275 flat / 19 losses |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,   # Immediately: 10% profit target
    "30": 0.05,  # After 30 min: 5% profit target
    "60": 0.02   # After 60 min: 2% profit target (actually inactive)
}

# Stop-loss setting
stoploss = -0.99  # 99% stop-loss (essentially disabled)

# Trailing stop
trailing_stop = True
```

**Design Rationale**:
- Tiered ROI design: Higher profits, more aggressive targets
- 99% stop-loss is essentially disabled, relying on trailing stop to protect capital
- Trailing stop gives profitable trades more room

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',
    'sell': 'gtc'
}
```

**Design Rationale**:
- Buy and sell use limit orders to reduce slippage
- Stop-loss uses market orders to ensure quick execution

### 2.3 Hyperparameter Configuration

```python
# Buy hyperparameter
buy_stoch_rsi = DecimalParameter(0.5, 1, decimals=3, default=0.82, space="buy")

# Sell hyperparameter
sell_stoch_rsi = DecimalParameter(0, 0.5, decimals=3, default=0.2, space="sell")
```

**Design Rationale**:
- Buy threshold default 0.82: Only consider buying when Stoch RSI is below 82% (oversold zone)
- Sell threshold default 0.2: Consider selling when Stoch RSI is above 20%
- Hyperparameter ranges support Hyperopt optimization

---

## III. Buy Conditions Detailed

### 3.1 Only Buy Signal: Perfect Bullish Alignment + Oversold Reversal

```python
# Buy conditions
(
    (dataframe['ema7'] > dataframe['ema30']) &      # EMA7 > EMA30
    (dataframe['ema30'] > dataframe['ema50']) &      # EMA30 > EMA50
    (dataframe['ema50'] > dataframe['ema100']) &     # EMA50 > EMA100
    (dataframe['ema100'] > dataframe['ema121']) &    # EMA100 > EMA121
    (dataframe['ema121'] > dataframe['ema200']) &    # EMA121 > EMA200
    (dataframe['stoch_rsi'] < self.buy_stoch_rsi.value) &  # Stoch RSI oversold
    (dataframe['volume'] > 0)                        # Has volume
)
```

**Interpretation**:
1. **Perfect Bullish Alignment**: 6 EMAs arranged in order from short to long, representing strong uptrend
2. **Stoch RSI Oversold**: Wait for pullback entry opportunities during uptrend
3. **Volume Confirmation**: Ensure actual trading activity

### 3.2 Buy Condition Breakdown

| Condition Part | Logic | Function |
|---------------|-------|----------|
| EMA7 > EMA30 | Short-term trend up | Confirm short-term momentum |
| EMA30 > EMA50 | Short-medium term trend up | Confirm trend continuation |
| EMA50 > EMA100 | Medium-term trend up | Confirm trend stability |
| EMA100 > EMA121 | Medium-long term trend up | Bullish alignment confirmation |
| EMA121 > EMA200 | Long-term trend up | Strong trend confirmation |
| Stoch RSI < 0.82 | Oversold zone | Wait for pullback entry |
| Volume > 0 | Has volume | Avoid false signals |

### 3.3 EMA Period Design Analysis

| EMA Period | Purpose | Design Logic |
|-----------|---------|-------------|
| EMA7 | Ultra-short-term trend | Capture immediate price movement |
| EMA30 | Short-term trend | Filter short-term noise |
| EMA50 | Short-medium term trend | Common medium-term MA |
| EMA100 | Medium-term trend | Key support level reference |
| EMA121 | Medium-long term trend | Special period (11²) |
| EMA200 | Long-term trend | Bull/bear dividing line |

---

## IV. Sell Logic Detailed

### 4.1 Only Sell Signal: Trend Reversal + Overbought

```python
# Sell conditions
(
    (dataframe['ema121'] > dataframe['ema7']) &      # EMA121 > EMA7 (trend reversal)
    (dataframe['stoch_rsi'] > self.sell_stoch_rsi.value) &  # Stoch RSI overbought
    (dataframe['volume'] > 0)                        # Has volume
)
```

**Interpretation**:
1. **EMA121 > EMA7**: Price breaks below EMA121, suggesting trend reversal
2. **Stoch RSI overbought**: Momentum indicator shows possible overbought
3. **Volume confirmation**: Ensure actual trading activity

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
```

**Trailing Stop Logic**:
- After profit, stop-loss moves up as price rises
- Protects existing profits, gives profitable trades more room
- Combined with tiered ROI, achieves dynamic take-profit

### 4.3 Tiered ROI Mechanism

```
Time      Profit Target
──────────────────
0 min     10%
30 min    5%
60 min    2%
```

**Interpretation**:
- Requires 10% profit on entry, relatively high target
- After 30 min drops to 5%, shortening holding time
- After 60 min drops to 2%, quick in and out

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA(7, 30, 50, 100, 121, 200) | Bullish alignment judgment |
| Momentum Indicators | Stoch RSI(14, 3, 3) | Oversold/overbought judgment |
| Volume | Volume | Signal confirmation |

### 5.2 Indicator Calculation Notes

**EMA (Exponential Moving Average)**:
- Calculated using `ta.trend.ema_indicator`
- Gives higher weight to recent prices
- More sensitive than SMA, reacts faster

**Stoch RSI (Stochastic Relative Strength Index)**:
- Calculated using `ta.momentum.stochrsi`
- Parameters: window=14, smooth1=3, smooth2=3
- Value range: 0-1
- Oversold zone: < 0.2 (buy signal)
- Overbought zone: > 0.8 (sell signal)

### 5.3 Startup Period Requirements

```python
startup_candle_count = 200  # EMA200 needs 200 candles
```

**Note**:
- Strategy requires 200 candles for warm-up period
- 1-hour cycle needs about 8.3 days of historical data
- Ensures all EMA indicators calculate accurately

---

## VI. Risk Management Features

### 6.1 Trailing Stop

```python
trailing_stop = True
```

**Advantages**:
- Protects existing profits
- Gives profitable trades more room to develop
- Automatically adjusts stop-loss level

### 6.2 Tiered ROI

```python
minimal_roi = {
    "0": 0.10,
    "30": 0.05,
    "60": 0.02
}
```

**Advantages**:
- High target on entry (10%)
- Lowers target as time passes
- Avoids long holding periods

### 6.3 Hyperparameter Optimization

Supports Hyperopt optimization of:
- `buy_stoch_rsi`: Stoch RSI threshold when buying
- `sell_stoch_rsi`: Stoch RSI threshold when selling

**Advantages**:
- Adapt to different market environments
- Optimize strategy performance
- Improve risk-reward ratio

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Strict Trend Confirmation**: 6 EMA bullish alignment ensures only trading strong trends
2. **Precise Entry Timing**: Enter during trend pullbacks, high risk-reward ratio
3. **Trailing Stop Protection**: Automatically protects profits, avoiding profit turning to loss
4. **Hyperparameter Optimization**: Can adjust parameters for different markets
5. **Excellent Backtest Performance**: Author's backtest data shows 1324% return

### ⚠️ Limitations

1. **Few Entry Opportunities**: Perfect bullish alignment rarely appears
2. **Large Drawdown**: Author's data shows 169.59% maximum drawdown
3. **Trend Dependent**: Ranging markets may trigger frequent stop-losses
4. **Single Sell Signal**: Sell logic is relatively simple
5. **Many Rejected Signals**: 3045 buy signals rejected

---

## VIII. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Strong Bull Market | Standard configuration | Perfectly captures uptrend |
| Ranging Market | Raise buy_stoch_rsi | Reduce entry frequency |
| Bear Market | Disable strategy | Bullish alignment won't appear |
| High Volatility | Adjust stop-loss | May need wider stop-loss |

---

## IX. Applicable Market Environment Details

AlligatorStrategy is a **strong trend-following strategy**. Based on its code architecture and backtest data, it performs best in **obvious uptrend markets**, while unable to work effectively in **ranging and downtrend markets**.

### 9.1 Strategy Core Logic

- **Bullish Alignment Filter**: 6 EMAs arranged in order, only trading strongest trends
- **Pullback Entry**: Enter after Stoch RSI oversold during trend
- **Trend Reversal Exit**: Exit when EMA crossover reversal occurs

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:-----------|:------------------|:----------------|
| 📈 Strong Bull Market | ⭐⭐⭐⭐⭐ | Perfectly captures uptrend, profit on entry |
| 🔄 Ranging Market | ⭐⭐☆☆☆ | Bullish alignment rarely forms, few entry opportunities |
| 📉 Bear Market | ☆☆☆☆☆ | No bullish alignment, strategy basically doesn't work |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | May get stopped out, but can follow trends when they come |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|------------------|-------|
| buy_stoch_rsi | 0.75-0.85 | Moderate oversold threshold |
| sell_stoch_rsi | 0.15-0.25 | Moderate overbought threshold |
| trailing_stop | True | Keep enabled |
| stoploss | -0.15 ~ -0.25 | Consider setting actual stop-loss |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

Strategy logic is clear, but requires understanding:
- Meaning of EMA bullish alignment
- Stoch RSI oversold/overbought zones
- How trailing stop works

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

**Note**: Needs to calculate 6 EMAs + Stoch RSI, moderate computation.

### 10.3 Backtesting vs Live Trading Differences

Author's backtest data looks impressive, but note:
- Backtest period was 2020-2021 major bull market
- 169.59% maximum drawdown indicates high risk
- 3045 rejected signals, only 258 valid signals

### 10.4 Manual Trader Recommendations

Strategy can be executed manually:
1. Open 1-hour chart
2. Add EMA(7, 30, 50, 100, 121, 200) and Stoch RSI
3. Wait for 6 EMAs to align from top to bottom (perfect bullish)
4. Wait for Stoch RSI below 0.82
5. Enter position, enable trailing stop

---

## XI. Summary

**AlligatorStrategy** is a **high risk-reward ratio strong trend-following strategy**. Its core value lies in:

1. **Strict Trend Filtering**: 6 EMA bullish alignment ensures only trading in strongest trends
2. **Precise Entry Timing**: Stoch RSI oversold provides high cost-performance entry points
3. **Automatic Risk Control**: Trailing stop protects profits, tiered ROI manages holding time

For quantitative traders, this strategy performs excellently in bull markets, but needs to withstand large drawdowns. Recommendations:
- Only use in clear bull markets
- Set reasonable stop-loss (-0.99 is too loose)
- Combine with position management to control risk
- Optimize parameters through Hyperopt

---

*Strategy Source: Crypto Robot*