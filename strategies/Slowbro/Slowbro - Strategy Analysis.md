# Slowbro Strategy Deep Dive

> **Strategy Number**: #385 (385th of 465 strategies)  
> **Strategy Type**: Minimalist Trend Following + Range Breakout  
> **Timeframe**: 1 Hour (1h) + Daily Information Layer (1d)

---

## I. Strategy Overview

Slowbro is a minimalist trend-following strategy whose design philosophy can be summarized as "slow is fast." The strategy name is derived from the Pokémon "Slowbro," symbolizing its slow but steady operational style. The core concept is to track a 30-day price range—buying when price touches the 30-day low and selling when it touches the 30-day high—achieving trend following through buying low and selling high.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal: price crosses above 30-day low |
| **Sell Condition** | 1 sell signal: price crosses above 30-day high |
| **Protection Mechanism** | No independent protection mechanism, relies on ROI and stop-loss |
| **Timeframe** | 1-hour main frame + 1-day information frame |
| **Dependencies** | qtpylib (crossover detection), merge_informative_pair (data merging) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,      # Immediate: 10% profit
    "1440": 0.20,   # After 1 day: 20% profit
    "2880": 0.30,   # After 2 days: 30% profit
    "10080": 1.0    # After 7 days: 100% profit
}

# Stop-loss setting
stoploss = -0.10   # 10% fixed stop-loss
```

**Design Rationale**:
- Adopts a time-graded ROI strategy—longer holding periods yield higher target profits
- 10% stop-loss matches the first-tier ROI, reflecting the risk-reward symmetry principle
- 100% target profit after 7 days, suitable for capturing major trend movements

### 2.2 Order Type Configuration

The strategy does not explicitly configure `order_types`, using Freqtrade defaults:
- Buy: Limit order
- Sell: Limit order
- Stop-loss: Market order

---

## III. Buy Condition Details

### 3.1 Core Buy Logic

Slowbro employs a single range breakout buy logic:

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            qtpylib.crossed_above(dataframe['close'], dataframe[f"30d-low_{self.inf_timeframe}"])
        ),
        'buy'] = 1
    return dataframe
```

**Trigger Condition**:
- Close price crosses above the 30-day lowest price line from below

### 3.2 Role of Information Timeframe

The strategy uses daily (1d) as an information layer to calculate the 30-day price range:

```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.inf_timeframe)
    informative['30d-low'] = informative['close'].rolling(30).min()
    informative['30d-high'] = informative['close'].rolling(30).max()
    
    dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.inf_timeframe, ffill=True)
    return dataframe
```

**Key Calculations**:
- `30d-low`: Lowest closing price over the past 30 days
- `30d-high`: Highest closing price over the past 30 days
- Uses forward-fill (ffill) to map daily data to hourly data

---

## IV. Sell Logic Details

### 4.1 Sell Signal

Symmetric to the buy logic, employing range breakout selling:

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            qtpylib.crossed_above(dataframe['close'], dataframe[f"30d-high_{self.inf_timeframe}"])
        ),
        'sell'] = 1
    return dataframe
```

**Trigger Condition**:
- Close price crosses above the 30-day highest price line from below

### 4.2 Sell Configuration

```python
use_sell_signal = True       # Enable sell signal
sell_profit_only = True      # Only sell when profitable
ignore_roi_if_buy_signal = False  # Buy signal has lower priority than ROI
```

**Design Rationale**:
- `sell_profit_only = True` ensures no selling at a loss (relies on stop-loss protection)
- Sell signal works in conjunction with ROI mechanism

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Price Range | 30-day rolling low | Buy trigger line |
| Price Range | 30-day rolling high | Sell trigger line |
| Crossover Detection | qtpylib.crossed_above | Signal trigger judgment |

### 5.2 Information Timeframe Indicators (Daily)

The strategy uses daily data as an information layer, providing higher-dimensional trend judgment:

- **30-day lowest price**: Serves as buy trigger line; price touching this line indicates entering oversold territory
- **30-day highest price**: Serves as sell trigger line; price breaking this line indicates entering overbought territory
- **Forward-fill**: Seamlessly maps daily data to hourly data, maintaining signal continuity

---

## VI. Risk Management Features

### 6.1 Range Trading Concept

Slowbro's core risk management lies in range definition:
- **Buy Boundary**: 30-day lowest price as the "floor"
- **Sell Boundary**: 30-day highest price as the "ceiling"
- **Holding Period**: Trend following from floor to ceiling

### 6.2 Time-Graded ROI

| Holding Time | Target Profit | Risk-Reward Ratio |
|-------------|--------------|-------------------|
| Immediate | 10% | 1:1 |
| 1 day | 20% | 2:1 |
| 2 days | 30% | 3:1 |
| 7 days | 100% | 10:1 |

### 6.3 Stop-Loss Protection

- **Fixed stop-loss**: -10%, symmetric with first-tier ROI
- **Profitable sell restriction**: `sell_profit_only = True` prevents premature exit during losses

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Minimalist design**: Only about 100 lines of code, easy to understand and maintain
2. **Trend following**: Based on 30-day range, captures medium-to-long-term trends
3. **Few parameters**: No need to optimize numerous indicator parameters, reducing overfitting risk
4. **Low resource consumption**: Small computational load, suitable for large-scale parallel operation

### ⚠️ Limitations

1. **Sparse signals**: Single buy condition may result in low trading frequency
2. **Lag**: 30-day range responds slowly to market changes
3. **Oscillating market risk**: May frequently trigger false signals during sideways consolidation
4. **No dynamic adjustment**: Does not adjust parameters based on market volatility

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|-------------------------|-------|
| Slow bull market | Default configuration | Perfectly captures slow bull trends |
| Oscillating market | Reduce timeframe or disable | High risk of false signals |
| Rapid decline | Tighter stop-loss | Range will shift downward quickly |
| Unexpected events | Manual intervention | Range calculation lags |

---

## IX. Applicable Market Environment Details

Slowbro is a classic **range breakout trend-following strategy**. Based on its code architecture and design philosophy, it is best suited for **slow bull markets with clear trends**, and performs poorly in **severe oscillation or rapid decline** scenarios.

### 9.1 Core Strategy Logic

- **Range definition**: Uses 30-day rolling window to define "floor" and "ceiling"
- **Follow the trend**: Buy on floor breakout, sell on ceiling breakout
- **Nested timeframe**: Daily range + hourly trigger, balancing stability and sensitivity

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 Slow bull market | ⭐⭐⭐⭐⭐ | Price rises steadily, range gradually shifts up, perfectly matches strategy logic |
| 🔄 Oscillating market | ⭐⭐☆☆☆ | Price repeatedly crosses range boundaries, triggers numerous false signals |
| 📉 Bear market | ⭐⭐⭐☆☆ | Range shifts down during process, short signals possible but designed for long |
| ⚡ High volatility | ⭐⭐☆☆☆ | Price volatility causes rapid range changes, signals lag |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|------------------|-------|
| Timeframe | 1h (default) | Balances signal frequency and reliability |
| Stop-loss | -10% (default) | Symmetric with ROI, can adjust based on risk preference |
| Trading pairs | Major coins | Good liquidity, relatively clear trends |

---

## X. Important Reminder: The Price of Simplicity

### 10.1 Learning Cost

Slowbro is one of the simplest strategies among the 465 strategies, with extremely low learning cost:
- Small codebase, clear logic
- No complex indicator calculations
- Very few parameters, easy to understand

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 512MB | 1GB |
| 10-50 pairs | 1GB | 2GB |
| 50+ pairs | 2GB | 4GB |

### 10.3 Differences Between Backtesting and Live Trading

The advantage of simple strategies is higher consistency between backtesting results and live performance:
- No complex condition combinations, reducing overfitting risk
- Note: Range breakout strategies perform very differently across different market cycles

### 10.4 Suggestions for Manual Traders

Slowbro's logic is very suitable for manual trading reference:
- Directly observe 30-day highs and lows as support/resistance levels
- Breakout signals are clear, easy for manual confirmation
- Recommend combining with volume to confirm signal validity

---

## XI. Summary

**Slowbro** is a **minimalist range breakout trend-following strategy**. Its core values are:

1. **Simplicity is beauty**: About 100 lines of code implement complete trading logic
2. **Trend capturing**: Captures medium-term trends through 30-day range
3. **Low maintenance cost**: Few parameters, simple logic, easy to understand

For quantitative traders, Slowbro is suitable as a **benchmark strategy** or **basic component of portfolio strategies**. While it may generate sparse signals when used alone, its simplicity makes it an excellent example for learning Freqtrade strategy development.