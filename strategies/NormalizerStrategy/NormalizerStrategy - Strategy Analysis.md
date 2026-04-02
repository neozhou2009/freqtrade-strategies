# NormalizerStrategy Strategy Analysis

> **Strategy ID**: #283 (283rd of 465 strategies)  
> **Strategy Type**: Price Normalization Mean Reversion Strategy  
> **Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

**NormalizerStrategy** is a quantitative trading strategy based on Price Normalization technology. Unlike the complex multi-condition architecture of the Nostalgia series, this strategy adopts a minimalist design philosophy, focusing on identifying extreme price deviations through normalization techniques to capture mean reversion opportunities.

### Core Concept

Normalization is a mathematical method that converts price data into a standardized range. The strategy normalizes the current price relative to the historical price range, converting it to a standardized value between 0-1 (or 0-100). When the normalized value approaches the range boundary, it means the price is at an extreme position, presenting potential for mean reversion.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Extreme value detection based on normalized price |
| **Exit Conditions** | Normalized price mean reversion or target profit achieved |
| **Protection Mechanisms** | Extremely relaxed hard stop-loss setting |
| **Timeframe** | 1 Hour (suitable for capturing medium-term trends) |
| **Dependencies** | TA-Lib, technical, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.18    # Immediate exit: 18% profit
}

# Stop-Loss Settings
stoploss = -0.99  # -99% hard stop-loss
```

**Design Philosophy**:

- **High Target ROI (18%)**: The strategy pursues large single-trade profit margins, indicating its design is to capture medium-term mean reversion opportunities rather than accumulating small profits through frequent trading.
- **Extremely Relaxed Stop-Loss (-99%)**: Nearly equivalent to no stop-loss, granting trading extreme volatility tolerance. This reflects the strategy's confidence in mean reversion — even if price temporarily fluctuates unfavorably, it will ultimately revert to the mean.

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'limit',
    'exit': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

**Configuration Notes**:
- Entry and exit both use limit orders for better fill prices
- Stop-loss uses market orders to ensure timely exit during extreme market conditions

---

## III. Entry Conditions Details

### 3.1 Core Principle: Price Normalization

The strategy uses price normalization technology to identify trading opportunities:

**Normalization Formula**:
```
Normalized_Price = (Current_Price - Lowest_Price) / (Highest_Price - Lowest_Price)
```

Where:
- `Current_Price`: Current price
- `Lowest_Price`: Lowest price in the observation period
- `Highest_Price`: Highest price in the observation period

**Normalized Value Interpretation**:
| Normalized Value | Price Position | Trading Signal |
|-----------------|----------------|----------------|
| Close to 0 | Price near lower range boundary | Potential buy opportunity |
| Close to 1 | Price near upper range boundary | Potential sell opportunity |
| Close to 0.5 | Price in middle of range | No clear signal |

### 3.2 Entry Condition Logic

```python
# Typical entry condition
def populate_entry_trend(self, dataframe, metadata):
    # Buy when normalized price is below threshold
    conditions.append(
        (dataframe['normalized'] < self.buy_threshold.value)
    )
```

**Trigger Conditions**:
- Normalized price drops below the set buy threshold (typically 0.2 or lower)
- Indicates current price is at a low point relative to historical range
- Expects price to revert upward to the mean

### 3.3 Entry Threshold Parameters

| Parameter | Typical Value | Description |
|-----------|--------------|-------------|
| `buy_threshold` | 0.15-0.25 | Normalized price buy threshold |
| `lookback_period` | 20-50 | Historical period for normalization calculation |

---

## IV. Exit Logic Details

### 4.1 Take-Profit Mechanism

```
Profit Target       Exit Rule
─────────────────────────────────
>= 18%             Exit immediately
```

**Design Philosophy**:
- Fixed target profit, no tiered take-profit
- The 18% target reflects the strategy's "one big score" trading style
- Once the target is reached, exit immediately to lock in profits

### 4.2 Mean Reversion Exit

Exit triggered when normalized price reverts near the mean:

```python
# Sell when normalized price reverts to mean
conditions.append(
    (dataframe['normalized'] > self.sell_threshold.value)
)
```

**Exit Conditions**:
- Normalized price breaks above the sell threshold (typically 0.8 or higher)
- Indicates price has reverted from low to high
- Realizes mean reversion profit

### 4.3 Base Sell Signals

| Signal Type | Trigger Condition | Description |
|------------|-------------------|-------------|
| ROI Take-Profit | Profit >= 18% | Fixed target take-profit |
| Mean Reversion | Normalized value > sell threshold | Price reverted to high |
| Stop-Loss Trigger | Loss >= 99% | Extreme protection (rarely triggered) |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Normalized Indicator | Price normalization | Identify extreme price positions |
| Trend Indicators | EMA/SMA | Assist trend direction judgment |
| Volatility Indicators | ATR | Calculate price range |

### 5.2 Normalization Calculation Details

**Standard Normalization Method**:
```
1. Determine lookback period
2. Calculate highest and lowest prices in the period
3. Map current price to [0, 1] range
```

**Advantages**:
- Eliminates magnitude differences across different price ranges
- Enables strategy application to trading pairs at various price levels
- Intuitively displays price's relative position

### 5.3 Auxiliary Indicators

- **EMA (Exponential Moving Average)**: Used to confirm trend direction, avoid counter-trend trading
- **ATR (Average True Range)**: Used to dynamically adjust the normalization price range

---

## VI. Risk Management Features

### 6.1 Extremely Tolerant Stop-Loss Strategy

The strategy adopts a -99% hard stop-loss, which is extremely rare in quantitative strategies:

**Design Considerations**:
| Advantage | Disadvantage |
|-----------|--------------|
| Grants price ample room to fluctuate | Lacks downside protection |
| Avoids being stopped out by normal volatility | Extreme market conditions cause huge losses |
| Fits mean reversion logic | Requires strong risk tolerance |

### 6.2 Single High Target Take-Profit

The 18% single take-profit target reflects the strategy's trading philosophy:

- **Pursuing quality over quantity**: Prefers waiting for one big profit over frequently trading small gains
- **Lower trading costs**: Fewer trades mean lower fees and slippage
- **Fits mean reversion characteristics**: Mean reversion opportunities themselves are infrequent but offer larger profit potential

### 6.3 Risk Exposure Management

```python
# Recommended configuration
max_open_trades = 2      # Limit concurrent position count
stake_amount = 'unlimited'  # Recommended to change to fixed amount
```

---

## VII. Strategy Pros & Cons

### Advantages

1. **Clear and Simple Logic**: Normalization concept is intuitive, strategy structure is simple, easy to understand and optimize
2. **Strong Universality**: Normalization method applicable to trading pairs at any price range, no need to adjust parameters for different coins
3. **Captures Extreme Opportunities**: Focuses on identifying extreme price deviations, high theoretical risk-reward ratio
4. **Low Overfitting Risk**: Fewer parameters, simple logic, not prone to overfitting historical data
5. **Low Trading Costs**: Relatively low trading frequency, minimal fee and slippage impact

### Limitations

1. **Extremely Wide Stop-Loss Risk**: -99% stop-loss means potential for enormous losses in extreme market conditions
2. **Low Signal Frequency**: Extreme price opportunities don't appear often, may have long periods without trades
3. **Depends on Mean Reversion**: In strong trending markets, price may continuously deviate from the mean, causing strategy failure
4. **Lacks Tiered Take-Profit**: Single target may cause realized profits to give back
5. **Sensitive to Parameters**: Normalization period and threshold choices greatly impact strategy performance

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Ranging Market | Standard configuration | Optimal environment for normalization strategy, price fluctuates within range |
| Weak Trend | Use with caution | May produce false signals, recommended to pair with trend filter |
| Strong Trend | Not recommended | Price continuously deviates from mean, strategy logic fails |
| High Volatility | Adjust parameters | Expand normalization period, lower buy threshold |

---

## IX. Applicable Market Environment Details

NormalizerStrategy is a typical **mean reversion strategy**. Based on its code architecture and strategy logic, it is best suited for **ranging markets** and performs poorly in **strong trending markets**.

### 9.1 Strategy Core Logic

- **Mean Reversion Assumption**: Price will revert to the mean after extreme deviations
- **Range Trading Mindset**: Buy low and sell high at price range boundaries
- **Extreme Value Identification**: Quantifies how extreme a price is through normalization

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:---|:---|:---|
| Slow Bullish | StarsStarsStars (Moderate) | Continuous upward price may miss buy opportunities but catches pullbacks |
| Slow Bearish | StarsStars (Poor) | Continuous downward price may cause premature buying, waiting for reversion takes too long |
| Wide Ranging | StarsStarsStarsStarsStars (Best) | Optimal environment, price fluctuates repeatedly within range |
| Narrow Ranging | StarsStarsStars (Moderate) | Small price swings may be insufficient to reach target profit |
| Extreme Volatility | StarsStars (Poor) | Price breaks original range, normalization parameters fail |
| Sideways Consolidation | StarsStarsStarsStars (Good) | Secondary optimal environment, suitable for capturing range fluctuations |

### 9.3 Key Configuration Recommendations

| Config Item | Recommended Value | Description |
|-------------|-------------------|-------------|
| Normalization Period | 30-50 candles | Balance sensitivity and stability |
| Buy Threshold | 0.15-0.25 | Lower is more conservative, fewer signals |
| Sell Threshold | 0.75-0.85 | Higher is more aggressive, larger profit potential |
| ROI Target | 10%-20% | Adjust based on market volatility |

---

## X. Important Reminder

### 10.1 Learning Curve

While NormalizerStrategy's core concept is simple, deep understanding of how normalization behaves under different market environments requires learning and practice:

- Understanding the dynamic changing characteristics of normalized values
- Mastering parameter optimization methods
- Identifying market conditions where strategy fails

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|-------------|-----------------|
| 1-5 pairs | 1GB | 2GB |
| 5-20 pairs | 2GB | 4GB |
| 20+ pairs | 4GB | 8GB |

**Note**: Strategy computational demand is low, suitable for running on lightweight VPS.

### 10.3 Backtesting vs. Live Trading Differences

Normalization strategy may exhibit differences between backtesting and live trading:

| Difference | Backtest Performance | Live Performance |
|------------|----------------------|-------------------|
| Price Range | Uses complete historical data | Real-time calculation may be unstable |
| Extreme Value Identification | Hindsight bias | Real-time judgment more difficult |
| Liquidity | Ignores liquidity issues | May be unable to fill in extreme markets |

### 10.4 Manual Trader Advice

For manual traders wishing to learn from NormalizerStrategy:

1. **Understand normalization concept**: Learn to identify price's relative position
2. **Set reasonable ranges**: Don't use periods that are too short or too long
3. **Combine with trend judgment**: Use in ranging markets, avoid strong trending markets
4. **Strict risk management**: Must set reasonable stop-loss, don't copy the -99% stop-loss

---

## XI. Summary

**NormalizerStrategy** is a **simple but requires cautious use** mean reversion strategy. Its core value lies in:

1. **Methodological Innovation**: Quantifies extreme price degrees through normalization technology, providing a unique market perspective
2. **Clear Logic**: Strategy structure is simple, easy to understand and optimize, reducing overfitting risk
3. **Strong Universality**: Normalization eliminates price magnitude differences, widely applicable to different trading pairs

For quantitative traders, NormalizerStrategy provides a valuable insight: **using mathematical methods to quantify "expensive" and "cheap"**. However, its extremely relaxed stop-loss and mean reversion dependency require users to have strong risk tolerance and accurate market environment judgment.

**Final Recommendation**: Before using this strategy, fully backtest with historical data, understand its performance characteristics under different market environments, and adjust stop-loss settings according to your own risk tolerance. Remember, no strategy performs well under all market conditions, and risk management is always the top priority.

**Risk Warning**: This strategy uses an extremely relaxed stop-loss setting (-99%), which may cause significant losses in extreme market conditions. Please adjust parameters according to your own risk tolerance and do not blindly follow.
