# AlwaysBuy Strategy In-Depth Analysis

> **Strategy ID**: #419 (419th of 465 strategies)  
> **Strategy Type**: Minimalist Test Strategy / Benchmark Reference Strategy  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

AlwaysBuy is a minimalist strategy with the core design philosophy of "unconditional buying." It has no technical indicator analysis, and the buy condition is always true, primarily used for testing framework functionality, verifying exchange connections, or serving as a benchmark reference for other strategies.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 (unconditional trigger) |
| **Exit Conditions** | No active exit signals, relies on ROI and stop loss |
| **Protection Mechanisms** | Trailing stop |
| **Timeframe** | 5 minutes (5m) |
| **Dependencies** | None (only basic freqtrade library) |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 1,      # After 0 minutes, exit at 100% profit
    "100": 2,    # After 100 minutes, exit at 200% profit
    "200": 3,    # After 200 minutes, exit at 300% profit
    "300": -1    # After 300 minutes, disable ROI (-1 means no exit)
}

# Stop loss settings
stoploss = -0.2  # 20% fixed stop loss
```

**Design Rationale**:
- The ROI table configuration is unusual, with the first three entries setting extremely high profit targets (100%, 200%, 300%) that are almost impossible to reach in actual trading
- The last entry `-1` indicates disabling ROI exit after 300 minutes, meaning complete reliance on the stop loss mechanism
- This configuration suggests the strategy is more of a testing framework than an actual trading strategy

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.005     # Activate after 0.5% profit
trailing_stop_positive_offset = 0.03  # Start trailing after 3% profit
trailing_only_offset_is_reached = True  # Only activate after offset reached
```

**Design Rationale**:
- Trailing stop activates when profit reaches 3%
- Once activated, a 0.5% pullback triggers a sell
- Relatively conservative configuration, suitable for low volatility markets

### 2.3 Order Type Configuration

```python
use_exit_signal = False  # Disable exit signals
```

The strategy doesn't use any exit signals, relying entirely on ROI and stop loss mechanisms to exit.

---

## 3. Entry Conditions Detailed

### 3.1 Single Entry Condition: Unconditional Buy

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[:, ["enter_long", "enter_tag"]] = (1, "entry_reason")
    return dataframe
```

**Logic Analysis**:
- No conditional judgment whatsoever
- All candlesticks are marked as buy signals
- `enter_tag` uniformly marked as `"entry_reason"`

**Practical Effect**:
- Every candlestick generates a buy signal
- In backtesting, will continuously buy when funds are available
- In live trading, limited by `max_open_trades` configuration

---

## 4. Exit Logic Detailed

### 4.1 No Active Exit Signals

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    return dataframe
```

The strategy's `populate_exit_trend` method returns an empty dataframe, meaning:
- No technical analysis-driven exit logic
- Complete reliance on ROI table and stop loss mechanisms

### 4.2 Passive Exit Mechanisms

| Exit Type | Trigger Condition | Description |
|-----------|-------------------|-------------|
| Fixed Stop Loss | 20% loss | Hard stop loss line |
| Trailing Stop | Pullback of 0.5% after profit ≥ 3% | Dynamic profit protection |
| ROI Exit | Profit ≥ 100%/200%/300% | Extremely difficult to trigger |

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|--------------------|---------------------|-------|
| None | None | None |

```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    return dataframe
```

The strategy calculates no technical indicators, which is its most distinctive feature.

---

## 6. Risk Management Features

### 6.1 Minimalist Risk Control

| Risk Control Type | Parameter | Description |
|-------------------|-----------|-------------|
| Fixed Stop Loss | -20% | Traditional hard stop |
| Trailing Stop | Enabled | Profit protection mechanism |
| ROI Limitation | Extremely high threshold | Actually ineffective |

### 6.2 No Protection Mechanisms

Unlike complex strategies, AlwaysBuy has no protection mechanisms configured:
- No cooldown period
- No maximum drawdown protection
- No consecutive stop loss protection

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Minimalist Design**: Very little code, easy to understand and debug
2. **Framework Testing Friendly**: Excellent for testing various Freqtrade framework features
3. **Benchmark Reference Value**: Can serve as a control group for other strategies to evaluate the actual value of technical analysis
4. **Low Resource Consumption**: No indicator calculations, minimal CPU and memory usage

### ⚠️ Limitations

1. **No Trading Logic**: No market analysis whatsoever, purely random trading
2. **Large Risk Exposure**: No protection mechanisms, potential for consecutive losses
3. **Not Suitable for Live Trading**: ROI configuration unreasonable, stop loss too loose
4. **Backtesting Distortion**: May produce unrealistic trading frequency in backtesting

---

## 8. Applicable Scenario Recommendations

| Use Case | Recommended Configuration | Description |
|----------|---------------------------|-------------|
| Framework Testing | Default configuration | Verify exchange connection, order execution, etc. |
| Strategy Comparison | As benchmark | Compare with other strategies to evaluate technical analysis effectiveness |
| Learning Research | Read code | Understand the minimal required structure of Freqtrade strategies |
| Live Trading | ❌ Not Recommended | This strategy has no live trading value |

---

## 9. Applicable Market Environment Details

AlwaysBuy is a **test/benchmark strategy**. It has no market analysis capability and doesn't rely on any technical indicators, so it cannot adapt to any specific market environment.

### 9.1 Strategy Core Logic

- **Unconditional Buy**: No judgment, direct position opening
- **Passive Exit**: Relies on stop loss and ROI, no active exit
- **No Protection Mechanisms**: No risk management layer protection

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Strong Uptrend | ⭐⭐⭐☆☆ | Random buying might profit, but no trend recognition |
| 🔄 Oscillating Market | ⭐☆☆☆☆ | Frequent trading, serious fee loss |
| 📉 Downtrend | ⭐☆☆☆☆ | No risk avoidance beyond stop loss protection |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | May be frequently triggered by trailing stop |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| max_open_trades | 1-3 | Limit position count, reduce risk exposure |
| stake_amount | Minimum amount | Only for testing, avoid real fund risk |
| dry_run | True | Strongly recommended for simulation testing only |

---

## 10. Important Reminder: The Nature of Test Strategies

### 10.1 Purpose Positioning

AlwaysBuy is a **tool-type strategy**, not a trading strategy:
- Used for testing Freqtrade framework functionality
- Used for verifying exchange API connections
- Used as a starting template for strategy development
- Used for comparative evaluation of other strategies

### 10.2 Not Suitable for Live Trading

| Risk Type | Description |
|-----------|-------------|
| No Trading Logic | Buying is completely random, no analysis basis |
| Fund Risk | May generate many ineffective trades, serious fee loss |
| Stop Loss Too Loose | 20% stop loss is too loose for most trading pairs |

### 10.3 Correct Usage

1. **Framework Testing**: Verify Freqtrade installation correctness
2. **API Testing**: Confirm exchange connection and order execution
3. **Strategy Template**: As a starting point for developing new strategies
4. **Performance Comparison**: Evaluate other strategies' advantage over "random buying"

---

## 11. Summary

**AlwaysBuy** is a minimalist test strategy whose core value lies in:

1. **Framework Verification**: Quickly verify whether Freqtrade installation and configuration are correct
2. **Benchmark Reference**: Provide a "zero technical analysis" reference for evaluating other strategies
3. **Learning Template**: Demonstrate the minimal required structure of Freqtrade strategies

For quantitative traders, this strategy should only be used for testing and learning purposes, **never for live trading**. If a simple benchmark strategy is needed, consider using an equal-weight buy-and-hold strategy as a comparison benchmark instead.