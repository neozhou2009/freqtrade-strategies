# RSIv2 Strategy Deep Dive

> **Strategy ID**: #342 (342nd of 465 strategies)
> **Strategy Type**: Dual Timeframe RSI + Williams %R Oversold Rebound Strategy
> **Timeframe**: 15 Minutes (15m) + 30 Minutes (30m)

---

## I. Strategy Overview

RSIv2 is an oversold rebound strategy based on dual confirmation from RSI and Williams %R indicators. The core concept is: enter when both indicators simultaneously confirm oversold conditions, then exit when the market reaches overbought territory. The strategy employs a dual timeframe design where buy signals are generated on the main timeframe (15m), while sell signals reference higher timeframe (30m) trend judgment.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal, requires consecutive two-candle oversold confirmation |
| **Sell Condition** | 1 sell signal, requires consecutive two-candle overbought confirmation |
| **Protection Mechanism** | Fixed stop-loss at -10% + trailing stop mechanism |
| **Timeframe** | 15 minutes (main) + 30 minutes (informative) |
| **Dependencies** | talib (RSI, WILLR), qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.01  # Exit at 1% profit
}

# Stop-loss setting
stoploss = -0.10  # Fixed stop-loss at 10%
custom_stop = -0.1  # Custom stop-loss confirmation
```

**Design Rationale**:
- Single ROI target (1%), seeking quick profit realization
- Relatively wide stop-loss space (-10%), allowing price to continue dipping in oversold territory
- Strategy relies more on trailing stop mechanism to protect profits

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.01      # Activate trailing after 1% profit
trailing_stop_positive_offset = 0.02  # Trigger stop when price retraces 2% from high
```

**Trailing Stop Logic**:
- When profit reaches 1%, trailing stop is activated
- Stop-loss line moves up as price increases
- Sell is triggered when price retraces more than 2% from highest point

### 2.3 Order Type Configuration

```python
order_types = {
    'buy': 'limit',           # Limit buy
    'sell': 'limit',          # Limit sell
    'stoploss': 'market',     # Stop-loss as market order
    'stoploss_on_exchange': False  # Don't set stop-loss on exchange
}
```

---

## III. Buy Condition Details

### 3.1 Single Buy Signal

The strategy has only one buy condition, but requires consecutive two candles to simultaneously meet oversold conditions, which to some extent reduces false signal risk.

#### Buy Condition: Dual Indicator Dual-Period Confirmation

```python
# Buy logic
dataframe.loc[
    (dataframe['rsi'] < 30) &           # Current RSI < 30 (oversold)
    (dataframe['rperc'] < -80) &         # Current Williams %R < -80 (oversold)
    (dataframe['rsi'].shift(1) < 30) &   # Previous RSI < 30
    (dataframe['rperc'].shift(1) < -80), # Previous Williams %R < -80
    'buy'
] = 1
```

**Condition Breakdown**:

| Condition # | Indicator | Parameter | Description |
|-------------|-----------|-----------|-------------|
| 1 | RSI(14) | < 30 | Current candle RSI enters oversold zone |
| 2 | Williams %R(14) | < -80 | Current candle oversold confirmation |
| 3 | RSI(14).shift(1) | < 30 | Previous candle also oversold |
| 4 | Williams %R(14).shift(1) | < -80 | Previous candle also oversold confirmation |

### 3.2 Buy Signal Characteristics

- **Dual Confirmation Mechanism**: Both RSI and Williams %R must simultaneously meet oversold conditions
- **Consecutive Requirement**: Requires consecutive two candles to both meet conditions, avoiding single-candle false signals
- **Strict Oversold Definition**: RSI < 30 is standard oversold, Williams %R < -80 is deep oversold

---

## IV. Sell Logic Details

### 4.1 Single Sell Signal

The sell signal also uses dual indicator dual-period confirmation, but uses 30-minute timeframe data.

```python
# Sell logic (using 30m data)
dataframe.loc[
    (dataframe['rsi_30m'] > 70) &              # 30m RSI > 70 (overbought)
    (dataframe['rperc_30m'] > -20) &           # 30m Williams %R > -20 (overbought)
    (dataframe['rsi_30m'].shift(1) > 70) &     # Previous 30m RSI > 70
    (dataframe['rperc_30m'].shift(1) > -20),   # Previous 30m Williams %R > -20
    'sell'
] = 1
```

**Sell Condition Breakdown**:

| Condition # | Indicator | Parameter | Description |
|-------------|-----------|-----------|-------------|
| 1 | RSI_30m(14) | > 70 | 30-minute RSI enters overbought zone |
| 2 | Williams %R_30m(14) | > -20 | 30-minute overbought confirmation |
| 3 | RSI_30m(14).shift(1) | > 70 | Previous 30-minute candle also overbought |
| 4 | Williams %R_30m(14).shift(1) | > -20 | Previous 30-minute candle also overbought confirmation |

### 4.2 Sell Logic Characteristics

- **Cross-Timeframe Selling**: Uses 30-minute timeframe to judge sell timing, providing higher-dimension trend confirmation
- **Overbought Exit**: Exits when market enters overbought status rather than chasing higher profits
- **Consecutive Verification**: Also requires consecutive two candles to confirm, avoiding false signals

### 4.3 Other Exit Mechanisms

| Exit Type | Trigger Condition | Description |
|-----------|-------------------|-------------|
| ROI Take-Profit | Profit ≥ 1% | Quick profit realization |
| Fixed Stop-Loss | Loss ≥ 10% | Bottom-line protection |
| Trailing Stop | Retracement ≥ 2% after profit ≥ 1% | Protect existing profits |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|---------------------|---------|
| Trend | RSI(14) | Overbought/oversold judgment, 15-minute main frame |
| Trend | RSI_30m(14) | Overbought/oversold judgment, 30-minute informative layer |
| Oscillator | Williams %R(14) | Oversold confirmation, 15-minute main frame |
| Oscillator | Williams %R_30m(14) | Overbought confirmation, 30-minute informative layer |

### 5.2 Informative Timeframe Indicators (30m)

The strategy uses 30 minutes as an informative layer, providing higher-dimension trend judgment:

```python
@informative('30m')
def populate_indicators_30m(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
    dataframe['rperc'] = ta.WILLR(dataframe, timeperiod=14)
    return dataframe
```

**Design Philosophy**:
- Buy signals generated on 15-minute timeframe, capturing short-term oversold opportunities
- Sell signals reference 30-minute timeframe, avoiding interference from short-term fluctuations
- This "fast-in, slow-out" design helps capture more profit in rebound markets

---

## VI. Risk Management Features

### 6.1 Multiple Stop-Loss Mechanisms

The strategy employs triple stop-loss protection:

```
Stop-Loss Priority: ROI Take-Profit > Trailing Stop > Fixed Stop-Loss

1. ROI Take-Profit: Exit immediately when profit reaches 1%
2. Trailing Stop: Protects profits after becoming profitable, allows price to continue rising
3. Fixed Stop-Loss: Bottom-line protection, limits maximum loss
```

### 6.2 Risk Characteristics of Oversold Rebound

| Risk Type | Description | Mitigation Measure |
|-----------|-------------|-------------------|
| Downtrend Risk | Oversold conditions may persist in downtrend | Consecutive two-candle confirmation |
| False Rebound Risk | May continue falling after oversold | Dual indicator cross-verification |
| Range-Bound Market Risk | Frequent entries/exits cause fee losses | Strict entry/exit conditions |

### 6.3 Signal Filter Configuration

```python
process_only_new_candles = True     # Process only on new candles
use_sell_signal = True              # Enable sell signals
sell_profit_only = True            # Only respond to sell signals when profitable
ignore_roi_if_buy_signal = False    # ROI takes priority
```

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple and Clear Logic**: Strategy core is just RSI and Williams %R overbought/oversold, easy to understand and optimize
2. **Dual Confirmation Mechanism**: Two indicators confirm simultaneously, reducing false signal probability
3. **Consecutive Verification**: Requires two consecutive candles to confirm, further filtering noise
4. **Cross-Timeframe Design**: 15m for entry, 30m reference for exit, "fast-in, slow-out" concept is sound
5. **Trailing Stop Protection**: Can protect profits while not exiting too early

### ⚠️ Limitations

1. **Single Entry Signal**: Only one buy condition, may have too few signals in some market environments
2. **May Underperform in Range-Bound Markets**: Frequent overbought/oversold signals in sideways oscillation may cause repeated losses
3. **Trending Market Risk**: In strong downtrends, oversold conditions may persist longer, leading to larger holding losses
4. **Fixed Parameters**: RSI period and thresholds are hardcoded, cannot be adjusted through hyperparameter optimization
5. **Lacks Trend Filter**: No mechanism to judge major trend, may bottom-fish against trend

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|--------------------|---------------------------|-------|
| Oscillating Uptrend | Default configuration | Suitable for buying on dips, selling on rebounds |
| Sideways Oscillation | Reduce position | Frequent overbought/oversold signals may increase trading costs |
| One-way Downtrend | Use cautiously | Oversold may persist, stop-losses may trigger frequently |
| One-way Uptrend | Not recommended | Rarely generates oversold signals, misses uptrend |

---

## IX. Applicable Market Environment Details

RSIv2 is a typical **oversold rebound strategy**. Based on its code architecture, it is best suited for **oscillating uptrend or range-bound market environments**, and underperforms in trending markets.

### 9.1 Strategy Core Logic

- **Bottom-Fishing Mindset**: Buy when RSI < 30 and Williams %R < -80, essentially counter-trend bottom-fishing
- **Fast In, Fast Out**: 1% ROI target with trailing stop, pursuing quick profit realization
- **Dual-Timeframe Confirmation**: 15-minute entry, 30-minute exit, avoiding short-term fluctuation interference

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:-----------------|
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ | Buy on dips, sell on rebounds, perfect match for strategy logic |
| 🔄 Range-Bound Oscillation | ⭐⭐⭐⭐☆ | Boundary oscillations frequently trigger buy/sell signals, stable profits |
| 📉 One-way Downtrend | ⭐☆☆☆☆ | Oversold may intensify, consecutive stop-losses cause severe losses |
| ⚡️ Rapid Rally | ⭐⭐☆☆☆ | Rarely generates oversold signals, misses main rally |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| Trading pair selection | Major coins | Good liquidity, oversold rebounds more reliable |
| Timeframe | Keep 15m | Not recommended to modify |
| Stop-loss adjustment | Can tighten appropriately | -5% to -8% can be considered |
| ROI target | Can adjust by asset | Higher volatility assets can increase |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

RSIv2 is a relatively simple strategy with less than 100 lines of code. Beginners can quickly understand through reading the source code:
- RSI and Williams %R calculation and application
- Dual timeframe design concepts
- Basic architecture of oversold rebound strategies

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-5 pairs | 1GB | 2GB |
| 5-20 pairs | 2GB | 4GB |
| 20+ pairs | 4GB | 8GB |

Strategy has small computational load, low hardware requirements.

### 10.3 Backtest vs Live Trading Differences

- **Backtest Performance**: May perform excellently in range-bound market backtests
- **Live Trading Risks**: Slippage, latency, and liquidity issues may erode profits in live trading
- **Recommendation**: Test with paper trading first, verify signal quality before live trading

### 10.4 Manual Trading Suggestions

If you want to apply RSIv2's concepts to manual trading:
1. You can use RSI(14) and Williams %R(14) combination to judge overbought/oversold
2. Consecutive two-candle confirmation can effectively filter false signals
3. Trailing stop is a good method to protect profits
4. Pay attention to position control, oversold rebound strategies have risks in strong trends

---

## XI. Summary

**RSIv2** is a **concise and practical oversold rebound strategy**. Its core value lies in:

1. **Clear Logic**: Dual indicator confirmation + consecutive verification, high signal quality
2. **Simple Execution**: Small codebase, few parameters, easy to understand and maintain
3. **Controllable Risk**: Multiple stop-loss mechanisms, protecting principal and profits

For quantitative traders, RSIv2 is an excellent example for learning oversold rebound strategies. It demonstrates how to build effective trading logic with minimal indicators, while also reminding us: simple doesn't mean ineffective, and overcomplication may lead to overfitting.

When using this strategy, recommend:
- Use in oscillating uptrend market environments
- Focus on major coins, avoid low-liquidity assets
- Appropriately adjust stop-loss and ROI parameters for different assets
- Practice good money management, don't over-concentrate in a single strategy

---