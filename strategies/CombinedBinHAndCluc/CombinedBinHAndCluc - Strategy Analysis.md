# CombinedBinHAndCluc Strategy Analysis

> **Strategy #**: #105 (5th in Batch 11)
> **Strategy Type**: Bollinger Bands + Dual Strategy Combination
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHAndCluc** is a classic dual-strategy combination trading strategy developed by iterativ. The strategy cleverly combines **BinHV45** and **ClucMay72018**, two classic Bollinger Band trend strategies, using an "OR gate" logic for buy signal composite filtering. The strategy is designed to be clean and efficient, focusing on capturing Bollinger Band convergence breakout opportunities.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 modes combined (BinHV45 OR ClucMay72018) |
| **Sell Conditions** | Price breaking above Bollinger middle band |
| **Protection Mechanism** | Fixed stop-loss -10% |
| **Timeframe** | 5 Minutes |
| **Dependencies** | TA-Lib, numpy, qtpylib |
| **Special Features** | Multi-strategy combination, custom Bollinger Band calculation |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.05    # Immediate exit: 5% profit
}

# Stop-Loss Settings
stoploss = -0.10  # -10% hard stop-loss

# Trading Timeframe
timeframe = '5m'

# Sell Signal Settings
use_sell_signal = True
sell_profit_only = True
ignore_roi_if_buy_signal = False
```

**Design Philosophy**:
- **Medium ROI**: 5% profit exit, consistent with swing trading thinking.
- **Fixed Stop-Loss**: -10% hard stop, simple and direct.
- **5-Minute Level**: Captures short-term fluctuation opportunities.

### 2.2 Trading Pair Settings

```python
# Suggested trading pairs (based on strategy characteristics)
# - Mainstream coins: BTC/USDT, ETH/USDT
# - High-volatility coins: ADA/USDT, SOL/USDT
# - Avoid low-volatility coins
```

---

## III. Entry Conditions Details

The strategy's entry conditions use "OR gate" logic — either BinHV45 or ClucMay72018 mode, satisfying either triggers a buy signal.

### 3.1 BinHV45 Mode

**Trigger Conditions**:

```python
(
    # Previous candle's Bollinger lower band exists
    dataframe['lower'].shift().gt(0) &

    # Bollinger Band width wide enough (> 0.8% of close price)
    dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &

    # Price fluctuation large enough (> 1.75% of close price)
    dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &

    # Lower wick short (< 25% of Bollinger Band width)
    dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &

    # Price breaks below previous Bollinger lower band
    dataframe['close'].lt(dataframe['lower'].shift()) &

    # Close not higher than previous close (confirms decline)
    dataframe['close'].le(dataframe['close'].shift())
)
```

**Logic Interpretation**:
1. **Bollinger Band width verification**: Ensures sufficient market volatility space.
2. **Price fluctuation verification**: Filters sideways consolidation markets.
3. **Pattern verification**: Hammer pattern (short lower wick).
4. **Breakout verification**: Price breaks below Bollinger lower band support.
5. **Trend confirmation**: Close price weakening.

### 3.2 ClucMay72018 Mode

**Trigger Conditions**:

```python
(
    # Price below long-term moving average
    (dataframe['close'] < dataframe['ema_slow']) &

    # Price below 98.5% of Bollinger lower band
    (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &

    # Volume abnormally low (< 1/20th of average)
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20))
)
```

**Logic Interpretation**:
1. **Trend verification**: Price below EMA50, in downtrend.
2. **Support verification**: Price near or below Bollinger lower band.
3. **Shrinking volume verification**: Volume extremely low, suggesting imminent reversal.

---

## IV. Exit Conditions Details

### 4.1 Technical Sell: Bollinger Middle Band Breakout

**Trigger Condition**:

```python
(dataframe['close'] > dataframe['bb_middleband'])
```

**Logic Interpretation**:
- Triggers sell when price breaks above Bollinger middle band (20-day MA).
- Indicates price transitioning from downtrend to consolidation or uptrend.
- Suitable for swing trading logic.

### 4.2 ROI Take-Profit

**Trigger Condition**:
- Auto-exit when profit reaches 5%.

**Logic Interpretation**:
- 5% is a relatively reasonable swing take-profit level.
- Paired with 5-minute level, suitable for short-term operations.

### 4.3 Stop-Loss Exit

**Trigger Condition**:
- Forced liquidation when loss reaches 10%.

**Logic Interpretation**:
- -10% stop-loss line is relatively wide.
- Gives price some callback space.
- Avoids being stopped out by market noise.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Calculation Method | Function |
|-----------|-------------------|---------|
| **Bollinger Middle Band** | 20-day SMA | Sell signal trigger line |
| **Bollinger Lower Band** | 20-day SMA - 2σ | Buy signal trigger line |
| **EMA50** | 50-day exponential moving average | Trend judgment |
| **Volume Average** | 30-day volume average | Shrinking volume verification |

### 5.2 Custom Indicators

| Indicator | Calculation Method | Function |
|-----------|-------------------|---------|
| **bbdelta** | \|middle band - lower band\| | Bollinger Band width |
| **closedelta** | \|close price - previous close\| | Price fluctuation magnitude |
| **tail** | \|close price - low price\| | Lower wick length |

### 5.3 Indicator Parameters

```python
# BinHV45 Bollinger Band parameters
window_size = 40
num_of_std = 2

# ClucMay72018 Bollinger Band parameters
window = 20
stds = 2

# Other parameters
ema_slow_period = 50
volume_mean_slow_period = 30
```

---

## VI. Risk Management Features

### 6.1 Stop-Loss Strategy

| Stop-Loss Type | Threshold | Description |
|---------------|-----------|-------------|
| **Hard Stop-Loss** | -10% | Forced liquidation at 10% loss |

### 6.2 Take-Profit Strategy

| Take-Profit Type | Threshold | Description |
|-----------------|-----------|-------------|
| **ROI Take-Profit** | 5% | Auto-exit at 5% profit |

### 6.3 Trading Frequency

- **Maximum concurrent trades**: Suggest 2 pairs.
- **Suggested position**: Use smaller positions per pair, accumulate more pairs.

---

## VII. Strategy Pros & Cons

### 7.1 Pros

1. **Dual Strategy Combination**: Two independent strategies complement each other, improving signal reliability.
2. **Pattern Recognition**: BinHV45 mode effectively identifies hammer patterns.
3. **Shrinking Volume Signal**: ClucMay72018 mode captures rebounds after volume dryness.
4. **Clean and Efficient**: Code logic is clear, easy to understand and modify.
5. **Backtest Friendly**: Parameters optimized, stable historical performance.

### 7.2 Cons

1. **Timeframe Limitation**: Only applicable to 5-minute level.
2. **Trend Adaptability**: May fail in strong trending markets.
3. **False Breakout Risk**: Bollinger breakout may produce false signals.
4. **Fixed Parameters**: No hyperparameter optimization space provided.

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

| Scenario | Description |
|----------|-------------|
| **Volatile Market** | Bollinger Band convergence breakout opportunities |
| **Swing Trading** | Short-term operations with 5% profit target |
| **Multi-Coin Allocation** | Run 2-3 trading pairs simultaneously |
| **Strategy Combination** | Use with trend strategies |

### 8.2 Not Recommended Scenarios

| Scenario | Description |
|----------|-------------|
| **Strong Trending Market** | May get stopped out frequently in trends |
| **Low-Volatility Market** | Bollinger Bands narrow, signals scarce |
| **Long-Term Holding** | 5% take-profit target too small |

---

## IX. Applicable Market Environment Details

### 9.1 Best Market Environment

- **Volatile Bull Market**: Price fluctuates near the middle band repeatedly.
- **Moderate Volatility**: Bollinger Band width moderate, not too narrow or wide.
- **Active Volume**: Clear volume changes.

### 9.2 Average Performance Markets

- **Unilateral Uptrend**: May miss subsequent rally.
- **Unilateral Downtrend**: Relies on stop-loss protection.
- **Sideways Consolidation**: May produce frequent false signals.

### 9.3 Notes

- Pay close attention during high-volatility periods (e.g., before/after major crypto events).
- Suggest pairing with market sentiment indicators.
- Can adjust take-profit/stop-loss thresholds based on market conditions.

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Strategy Complexity

**CombinedBinHAndCluc**, though code is concise, contains two different trading logics:

1. **BinHV45 Mode**: Based on hammer pattern and Bollinger Band breakout.
2. **ClucMay72018 Mode**: Based on shrinking volume rebound and MA support.

The superposition of these two modes gives the strategy some adaptability but also increases understanding difficulty.

### 10.2 Potential Risks

1. **Signal Conflict**: Two modes may give opposite signals.
2. **Overfitting**: Historical data optimization may cause overfitting.
3. **Parameter Sensitivity**: Fixed parameters may not suit all markets.

### 10.3 Recommendations

- Fully understand both buy mode logics.
- Conduct sufficient backtesting verification before live trading.
- Adjust parameters based on personal risk preference.
- Suggest testing with paper trading account.

---

## XI. Summary

**CombinedBinHAndCluc** is a classic dual-strategy combination trading strategy that combines BinHV45 and ClucMay72018, achieving adaptation to different market states. The strategy is clean, logically clear, and suitable for investors with some trading experience.

**Core Points**:
- ✅ Dual strategy combination, improves signal reliability.
- ✅ 5% take-profit target, suitable for short-term operations.
- ✅ -10% stop-loss protection, controls maximum loss.
- ⚠️ Suitable for volatile markets, be cautious in trending markets.
- ⚠️ Suggest pairing with other strategy combinations.

**Usage Suggestions**:
- New investors should understand strategy principles before using.
- Experienced investors can try parameter optimization.
- Suggest forming combinations with other strategies to reduce single-strategy risk.
