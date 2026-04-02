# TemaMaster3 Strategy In-Depth Analysis

> **Strategy ID**: #409 (409th of 465 strategies)  
> **Strategy Type**: TEMA Bollinger Band Breakout + CMO Momentum Confirmation Strategy  
> **Timeframe**: 1 minute (1m)

---

## I. Strategy Overview

TemaMaster3 is a short-term trading strategy based on Triple Exponential Moving Average (TEMA) and Bollinger Band breakout, combined with Chande Momentum Oscillator (CMO) for signal confirmation. This strategy pursues high-probability entries, capturing rebound opportunities when price touches the Bollinger Band lower band and momentum turns strong.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 combined buy signal, requiring both TEMA crossing above Bollinger lower band and CMO filter condition |
| **Sell Condition** | 2 basic sell signals, based on CMO indicator dynamic take-profit logic |
| **Protection Mechanism** | Trailing stop system (three-parameter configuration) |
| **Timeframe** | 1 minute primary timeframe |
| **Informative Timeframe** | stake_currency/USDT as reference pair |
| **Dependencies** | talib.abstract, qtpylib.indicators |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.25574  # Immediate target 25.574%
}

# Stop loss setting
stoploss = -0.08848  # 8.848% hard stop loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.12943      # Activate after 12.943% profit
trailing_stop_positive_offset = 0.17942  # Allow pullback to 17.942% after activation
trailing_only_offset_is_reached = True  # Only activate after reaching offset
```

**Design Rationale**:
- Single ROI target set high (25.574%), aiming to capture large-scale rebounds
- Trailing stop parameters finely tuned, activating protection after ~13% profit, allowing maximum pullback to 17.942%
- Hard stop loss at ~8.8%, providing final defense against extreme market conditions

### 2.2 Order Type Configuration

```python
use_sell_signal = True      # Enable sell signal
sell_profit_only = True     # Only sell when profitable
ignore_roi_if_buy_signal = False  # Buy signal doesn't override ROI
ta_on_candle = False        # Calculate indicators on every tick (high-frequency strategy characteristic)
```

---

## III. Buy Condition Details

### 3.1 Core Buy Logic

The strategy uses a single but strict combined buy condition:

```python
# Buy signal
(
    (qtpylib.crossed_above(dataframe["TEMA"], dataframe["bb_lowerband"]))
    & 
    (dataframe['CMO'] > -3)
)
```

#### Condition Analysis

| Condition Component | Logic Description | Technical Meaning |
|---------------------|-------------------|-------------------|
| **TEMA crosses above Bollinger lower band** | TEMA crosses bb_lowerband from below | Price starts rebounding after oversold condition |
| **CMO > -3** | Chande Momentum Oscillator greater than -3 | Excludes extreme weakness state |

### 3.2 Technical Indicator Parameters

| Indicator | Parameter | Purpose |
|-----------|-----------|---------|
| **TEMA** | Period 60 | Triple Exponential Moving Average, for price trend judgment |
| **Bollinger lower band** | Period 60, standard deviation 1.4 | Dynamic support level reference |
| **CMO** | Period 180 | Momentum confirmation, filtering false breakouts |

### 3.3 Auxiliary Indicators (Not Used for Signals)

```python
# Standard deviation and coefficient of variation
dataframe['STDDEV'] = ta.STDDEV(dataframe, timeperiod=26, nbdev=1.4)
dataframe['MA'] = ta.MA(dataframe, timeperiod=26, matype=0)
dataframe["COEFFV"] = dataframe['STDDEV'] / dataframe['MA']
```

These indicators are not used in the current version, possibly reserved for future expansion or legacy code.

---

## IV. Sell Logic Details

### 4.1 Sell Signal System

The strategy defines two independent sell signals:

```python
# Sell signals
(
    (qtpylib.crossed_below(dataframe["CMO"], -22)) 
    |
    (qtpylib.crossed_below(dataframe["CMO"], 25))
)
```

| Signal ID | Trigger Condition | Signal Meaning |
|-----------|-------------------|----------------|
| **Sell Signal #1** | CMO crosses below -22 from above | Momentum weakening, possible further decline |
| **Sell Signal #2** | CMO crosses below 25 from above | Momentum falling from overbought territory |

### 4.2 Sell Logic Design Rationale

- **Dual Exit Mechanism**: One exits in weakness zone (-22), one exits when falling from strength zone (25)
- **Asymmetric Exit**: Earlier identification of momentum exhaustion, avoiding profit giveback
- **Combined with Trailing Stop**: Technical signal + dynamic stop loss dual protection

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| **Trend Indicator** | TEMA(60) | Price trend tracking |
| **Volatility Indicator** | Bollinger Bands(60, 1.4) | Dynamic support/resistance judgment |
| **Momentum Indicator** | CMO(180) | Momentum strength confirmation |
| **Volatility Rate Indicator** | STDDEV(26), MA(26) | Volatility calculation (auxiliary) |

### 5.2 Informative Timeframe

The strategy uses `stake_currency/USDT` as informative pair:

```python
def informative_pairs(self):
    return [(f"{self.config['stake_currency']}/USDT", self.timeframe)]
```

This allows the strategy to reference the quote currency's trend against USDT for macro judgment when trading non-USDT pairs.

---

## VI. Risk Management Features

### 6.1 Trailing Stop Mechanism

The three-parameter trailing stop system provides flexible profit protection:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `trailing_stop_positive` | 12.943% | Profit threshold to trigger trailing stop |
| `trailing_stop_positive_offset` | 17.942% | Reference high point for trailing stop |
| `trailing_only_offset_is_reached` | True | Only activate after reaching offset |

**How It Works**:
1. When trade profit reaches 17.942%, trailing stop activates
2. Stop loss line is set at approximately 17.942% - 12.943% = 5% pullback position
3. Dynamically adjusts with price increase, protecting existing profits

### 6.2 Stop Loss and Take Profit Configuration

| Type | Value | Description |
|------|-------|-------------|
| Hard Stop Loss | -8.848% | Maximum loss tolerance |
| ROI Target | 25.574% | Ideal profit target |
| Profit Protection | Dynamic trailing | Profit locking mechanism |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Rigorous Entry**: TEMA breakout of Bollinger lower band + CMO momentum confirmation dual filtering, reducing false breakout risk
2. **Flexible Exit**: Dual CMO signals cover both strength zone pullback and weakness zone stop loss scenarios
3. **Refined Parameters**: Trailing stop three-parameters optimized, balancing profit protection and holding space
4. **High-Frequency Adaptation**: 1-minute timeframe with ta_on_candle=False, suitable for short-term operations

### ⚠️ Limitations

1. **Single Parameters**: Only one set of buy/sell conditions each, lacking multi-scenario adaptation capability
2. **No Protection Mechanism Group**: Buy protection parameter group not implemented, relying on stop loss system
3. **Ultra-Short-Term Risk**: 1-minute timeframe may produce more false signals, sensitive to slippage
4. **Indicator Redundancy**: STDDEV, MA, COEFFV calculated but not used, increasing computational burden

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Oscillating Rebound** | Default configuration | Capture Bollinger lower band rebound opportunities |
| **Trending Down** | Disable or raise CMO threshold | Avoid "catching falling knife" risk |
| **Trending Up** | May adjust Bollinger parameters | Lower band touches occur less frequently |
| **High Volatility** | Increase standard deviation multiplier | Reduce false breakout signals |

---

## IX. Applicable Market Environment Details

TemaMaster3 is a short-term rebound capture strategy. Based on its code architecture and indicator parameters, it is best suited for **rebound opportunities in oscillating markets**, and may underperform in trending markets.

### 9.1 Strategy Core Logic

- **Rebound Capture**: TEMA crossing above Bollinger lower band means price is briefly oversold
- **Momentum Confirmation**: CMO > -3 ensures non-extreme weakness, avoiding failed catch attempts
- **Dual Exit Mechanism**: Strength zone (25) and weakness zone (-22) each have exit channels
- **High-Frequency Execution**: 1-minute timeframe requires low-latency execution

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 **Slow Bull Trend** | ⭐⭐⭐☆☆ | Can capture pullback rebounds, but may exit too early in main trend |
| 🔄 **Sideways Oscillation** | ⭐⭐⭐⭐⭐ | Ideal scenario, frequent lower band touches, rebound potential |
| 📉 **Trending Down** | ⭐⭐☆☆☆ | High risk of catching falling knives, CMO > -3 filter may be insufficient |
| ⚡️ **High Volatility** | ⭐⭐⭐☆☆ | Frequent signals but many false breakouts, need to adjust Bollinger parameters |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Trading Pair Selection | High liquidity pairs | 1-minute timeframe is sensitive to slippage |
| Stop Loss Adjustment | May tighten appropriately | -8.8% may be too wide for short-term |
| CMO Threshold | Consider raising to 0 | Stricter momentum confirmation |
| Bollinger Standard Deviation | Try 1.2-1.6 | Adjust based on market volatility |

---

## X. Important Reminder: Cost of High-Frequency Strategies

### 10.1 Execution Costs

1-minute timeframe means:
- **High-Frequency Signals**: Many trades, significant cumulative fees
- **Slippage Sensitivity**: Slippage on each trade significantly impacts returns
- **API Limits**: Frequent calls may trigger exchange rate limits

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-5 pairs | 4GB | 8GB |
| 5-10 pairs | 8GB | 16GB |
| 10+ pairs | 16GB | 32GB+ |

### 10.3 Backtest vs Live Trading Differences

High-frequency strategy backtest results often outperform live trading:
- Backtests cannot simulate slippage and latency
- Market depth changes significantly affect execution prices
- Liquidity may dry up during extreme market conditions

### 10.4 Manual Trader Recommendations

Not recommended for manual execution of this strategy:
- 1-minute candles require constant monitoring
- Signal judgment requires real-time technical indicator calculation
- Emotional interference may cause strategy deviation

---

## XI. Summary

**TemaMaster3** is a short-term strategy focused on capturing Bollinger lower band rebounds. Its core value lies in:

1. **Dual Indicator Confirmation**: TEMA breakout + CMO momentum filtering, improving signal quality
2. **Flexible Exit**: Dual CMO signals cover different market states
3. **Refined Stop Loss**: Three-parameter trailing stop balances protection and space
4. **High-Frequency Adaptation**: Designed specifically for short-term operations

For quantitative traders, this is a short-term strategy suitable for oscillating markets, but note:
- High-frequency trading fees and slippage costs
- Parameters may need optimization for specific trading pairs and market environments
- Recommend thorough backtesting and paper trading verification first

---