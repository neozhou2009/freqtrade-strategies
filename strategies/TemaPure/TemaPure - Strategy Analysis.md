# TemaPure Strategy In-Depth Analysis

> **Strategy ID**: #410 (410th of 465 strategies)  
> **Strategy Type**: TEMA Bollinger Band Range Trading Strategy  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

TemaPure is a trend-following strategy based on Triple Exponential Moving Average (TEMA) and Bollinger Band range judgment, combined with Chande Momentum Oscillator (CMO) to confirm entry timing. This strategy enters when price touches the Bollinger lower band and momentum turns positive, exits when price touches the Bollinger upper band, pursuing complete trend returns within the range.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 combined buy signal, requiring both TEMA position condition and CMO crossover condition |
| **Sell Condition** | 1 basic sell signal, based on TEMA crossing above Bollinger upper band |
| **Protection Mechanism** | Four-level ROI take-profit + trailing stop system |
| **Timeframe** | 5 minute primary timeframe |
| **Informative Timeframe** | stake_currency/USDT as reference pair |
| **Dependencies** | talib.abstract, qtpylib.indicators |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table (four-level take-profit)
minimal_roi = {
    "0": 0.40505,    # Immediate target 40.505%
    "265": 0.24708,  # Target 24.708% after 265 minutes
    "743": 0.05892,  # Target 5.892% after 743 minutes
    "1010": 0        # Break-even exit after 1010 minutes
}

# Stop loss setting
stoploss = -0.09754  # 9.754% hard stop loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.2126        # Activate after 21.26% profit
trailing_stop_positive_offset = 0.2225  # Allow pullback to 22.25% after activation
trailing_only_offset_is_reached = True  # Only activate after reaching offset
```

**Design Rationale**:
- Four-level decreasing ROI: Pursuing high short-term returns, gradually lowering targets over time
- Trailing stop parameters highly close (21.26% vs 22.25%), quickly locking in after profit
- Hard stop loss at ~9.75%, providing final defense line

### 2.2 Order Type Configuration

```python
use_sell_signal = True      # Enable sell signal
sell_profit_only = True     # Only sell when profitable
ignore_roi_if_buy_signal = False  # Buy signal doesn't override ROI
ta_on_candle = False        # Calculate indicators on every tick
```

---

## III. Buy Condition Details

### 3.1 Core Buy Logic

The strategy uses a single combined buy condition:

```python
# Buy signal
(
    (dataframe['TEMA'] <= dataframe['bb_lowerbandTA'])
    & 
    (qtpylib.crossed_above(dataframe['CMO'], 0))
)
```

#### Condition Analysis

| Condition Component | Logic Description | Technical Meaning |
|---------------------|-------------------|-------------------|
| **TEMA <= Bollinger lower band TA** | TEMA is at or below bb_lowerbandTA | Price is in oversold territory |
| **CMO crosses above 0** | CMO crosses from negative to positive | Momentum turns from negative to positive confirmation |

### 3.2 Technical Indicator Parameters

| Indicator | Parameter | Purpose |
|-----------|-----------|---------|
| **TEMA** | Period 25 | Triple Exponential Moving Average, for price position judgment |
| **Bollinger lower band TA** | Period 25, upper std 3.5, lower std 1.0 | Oversold territory judgment |
| **CMO** | Period 50 | Momentum confirmation, identifying trend transition |

### 3.3 Dual Bollinger Band System

The strategy uses two sets of Bollinger Band parameters:

```python
# Bollinger Band Group 1: Standard Bollinger
bollinger = qtpylib.bollinger_bands(..., window=25, stds=2.0)

# Bollinger Band Group 2: Asymmetric Bollinger (used for signal judgment)
bollingerTA = ta.BBANDS(..., timeperiod=25, nbdevup=3.5, nbdevdn=1.0)
```

**Asymmetric Bollinger Design**:
- Upper band uses 3.5 times standard deviation (more lenient upper limit)
- Lower band uses 1.0 times standard deviation (stricter lower limit)
- Purpose: Buy signals more cautious (tighter lower band), sell signals more lenient (looser upper band)

---

## IV. Sell Logic Details

### 4.1 Sell Signal System

The strategy defines a single sell signal:

```python
# Sell signal
(qtpylib.crossed_above(dataframe["TEMA"], dataframe["bb_upperbandTA"]))
```

| Signal ID | Trigger Condition | Signal Meaning |
|-----------|-------------------|----------------|
| **Sell Signal** | TEMA crosses above Bollinger upper band TA from below | Price enters overbought territory, trend may reverse |

### 4.2 Sell Logic Design Rationale

- **Range Trading Logic**: Buy at lower band, sell at upper band, capturing trends within Bollinger range
- **Asymmetric Design**: Buy uses 1.0x standard deviation lower band (strict), sell uses 3.5x standard deviation upper band (lenient)
- **Combined with ROI**: Technical signal and four-level take-profit together protect profits

### 4.3 Commented Out Sell Condition

There is a commented-out sell condition in the code:

```python
# (qtpylib.crossed_below(dataframe['close'], dataframe['bb_upperbandTA']))
# & 
# (dataframe["CMO"] >= 35)
```

This indicates the author considered a momentum-confirmed sell condition, but ultimately chose the simpler TEMA crossing upper band logic.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicator** | TEMA(25) | Price trend tracking |
| **Volatility Indicator** | Bollinger Bands(25, 2.0) | Standard Bollinger (not used for signals) |
| **Volatility Indicator** | Bollinger TA(25, 3.5/1.0) | Asymmetric Bollinger (used for signals) |
| **Momentum Indicator** | CMO(50) | Momentum confirmation, identifying trend transition |

### 5.2 Significance of Asymmetric Bollinger

| Parameter | Standard Bollinger | Signal Bollinger TA | Difference |
|-----------|-------------------|---------------------|------------|
| Period | 25 | 25 | Same |
| Upper band std | 2.0 | 3.5 | Upper band loosened |
| Lower band std | 2.0 | 1.0 | Lower band tightened |

**Design Intent**:
- Tighter lower band: Only trigger buy when price is clearly oversold
- Looser upper band: Allow price more upside room before triggering sell
- Result: Potentially longer holding time, capturing larger trends

### 5.3 Informative Timeframe

The strategy uses `stake_currency/USDT` as informative pair:

```python
def informative_pairs(self):
    return [(f"{self.config['stake_currency']}/USDT", self.timeframe)]
```

---

## VI. Risk Management Features

### 6.1 Four-Level ROI Take-Profit System

| Time | Target Return | Description |
|------|--------------|-------------|
| 0 minutes | 40.505% | Immediate pursuit of high returns |
| 265 minutes (~4.4 hours) | 24.708% | Lower target over time |
| 743 minutes (~12.4 hours) | 5.892% | Further lowering |
| 1010 minutes (~16.8 hours) | 0% | Break-even exit |

**Design Rationale**:
- Short-term pursuit of high returns, not rushing to take profit
- Gradually lower return expectations as holding time increases
- Break-even exit after ~17 hours with no significant returns

### 6.2 Trailing Stop Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| `trailing_stop_positive` | 21.26% | Profit threshold to trigger trailing stop |
| `trailing_stop_positive_offset` | 22.25% | Reference high point for trailing stop |
| `trailing_only_offset_is_reached` | True | Only activate after reaching offset |

**Feature**: Parameter difference is extremely small (only 1%), meaning after profit reaches 22.25%, stop loss line will follow closely, almost immediately locking in ~21% profit.

### 6.3 Stop Loss and Take Profit Configuration

| Type | Value | Description |
|------|-------|-------------|
| Hard Stop Loss | -9.754% | Maximum loss tolerance |
| ROI Target | 40.5% → 0% | Four-level decreasing take-profit |
| Profit Protection | Dynamic trailing | Almost locks in all profits |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Strict Entry**: Asymmetric Bollinger tightened lower band + CMO crossing above 0 dual confirmation, reducing false signals
2. **Large Holding Space**: Upper band loosened to 3.5x standard deviation, allowing price full upside potential
3. **Multi-Level Take-Profit**: Four-level ROI combined with trailing stop, balancing profit space and risk control
4. **Clear Logic**: Clear buy/sell conditions, targeted parameter design

### ⚠️ Limitations

1. **Single Sell Signal**: Only relies on TEMA crossing upper band, no momentum confirmation
2. **No Weakness Exit**: Unlike TemaMaster3, no weakness zone sell signal, may hold too long
3. **Fixed Parameters**: No protection mechanism group, lacking flexibility
4. **May Miss Opportunities**: Strict buy conditions, may generate fewer signals in mild markets

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Range Oscillation** | Default configuration | Ideal scenario, clear upper and lower bands |
| **Trending Up** | Can use | Loose upper band design allows longer holding |
| **Trending Down** | Use cautiously | CMO crossing above 0 filter may be insufficient |
| **High Volatility** | May adjust parameters | Increase standard deviation to avoid frequent signals |

---

## IX. Applicable Market Environment Details

TemaPure is a range trading strategy. Based on its asymmetric Bollinger design and four-level ROI configuration, it is best suited for **trend capture in oscillating markets**, and may underperform in one-sided trends.

### 9.1 Strategy Core Logic

- **Range Trading**: Buy at lower band, sell at upper band, complete Bollinger range strategy
- **Asymmetric Design**: Strict buy (1.0x std), lenient sell (3.5x std)
- **Momentum Confirmation**: CMO crossing above 0 ensures trend strengthening
- **Multi-Level Take-Profit**: Time-decreasing ROI combined with trailing stop

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 **Slow Bull Trend** | ⭐⭐⭐⭐☆ | Loose upper band design allows holding to capture trend |
| 🔄 **Sideways Oscillation** | ⭐⭐⭐⭐⭐ | Ideal scenario, frequent upper and lower band touches |
| 📉 **Trending Down** | ⭐⭐☆☆☆ | CMO filter may be insufficient, risk of catching falling knives |
| ⚡️ **High Volatility** | ⭐⭐⭐☆☆ | Fewer signals but higher quality |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Timeframe | 5 minutes (default) | Balance signal frequency and noise |
| Stop Loss Adjustment | May tighten appropriately | -9.75% may be too wide for short-term |
| Bollinger Parameters | Try adjusting standard deviation | Based on specific pair volatility |
| CMO Threshold | Can raise to 5 or 10 | Stricter momentum confirmation |

---

## X. Important Reminder: Cost of Range Strategies

### 10.1 Longer Holding Time

Four-level ROI design means:
- Strategy expects to hold positions for several hours
- Pursuing larger profit space
- Need patience waiting for signals

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 4GB | 8GB |
| 10-20 pairs | 8GB | 16GB |
| 20+ pairs | 16GB | 32GB+ |

### 10.3 Backtest vs Live Trading Differences

Range strategies may perform well in backtesting, but live trading needs attention:
- Bollinger parameters sensitive to specific trading pairs
- Asymmetric design may fail in extreme market conditions
- CMO parameters need adjustment based on market

### 10.4 Manual Trader Recommendations

5-minute timeframe is relatively friendly:
- Can consider manual execution
- Need TradingView or similar tools to set alerts
- Strictly execute buy/sell conditions, avoid emotional interference

---

## XI. Summary

**TemaPure** is a strategy focused on Bollinger band range trading. Its core value lies in:

1. **Asymmetric Bollinger Design**: Strict buy, lenient sell, pursuing larger trend space
2. **Multi-Level Take-Profit System**: Four-level ROI combined with trailing stop, balancing profit and risk
3. **Momentum Confirmed Entry**: CMO crossing above 0 ensures trend strengthening
4. **Range Trading Logic**: Buy at lower band, sell at upper band, complete strategy logic

For quantitative traders, this is a range strategy suitable for oscillating and mild trending markets, but note:
- Strict buy conditions, may have fewer signals
- Single sell condition, may hold too long
- Parameters may need optimization for specific trading pairs and market environments
- Recommend thorough backtesting for verification

---