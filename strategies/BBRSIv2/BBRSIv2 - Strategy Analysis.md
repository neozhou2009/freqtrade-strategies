# BBRSIv2 Strategy Deep Dive

> **Strategy ID**: #437 (437th of 465 strategies)  
> **Strategy Type**: Bollinger Band + RSI Dual Indicator Reversal Strategy + Dynamic Stop Loss Protection  
> **Time Frame**: 15 minutes (15m)

---

## I. Strategy Overview

BBRSIv2 is a classic Bollinger Band and RSI combination reversal strategy. Originating from traditional technical analysis theory, it captures oversold reversal opportunities when price touches the lower Bollinger Band, combined with RSI indicator confirmation for entry timing. The strategy was originally created by Gert Wohlgemuth and customized/optimized by StrongManBR, making it a well-known entry-level reversal strategy in the Freqtrade community.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals (BB lower band bounce + RSI oversold confirmation) |
| **Sell Conditions** | 2 basic sell signals (RSI overbought + price breakout high) |
| **Protection Mechanism** | Dynamic stop loss (tiered profit protection) |
| **Time Frame** | 15-minute main frame |
| **Dependencies** | talib, qtpylib |
| **Startup Candles** | 144 candles (approximately 36 hours of data) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.3  # 30% profit target
}

# Stop loss setting
stoploss = -0.10  # 10% hard stop loss

# Custom stop loss enabled
use_custom_stoploss = True
```

**Design Rationale**:
- Single-level ROI setting (30%) gives the strategy sufficient profit margin
- 10% hard stop loss serves as the bottom-line protection
- Custom stop loss enabled for tiered profit locking

### 2.2 Order Type Configuration

The strategy uses standard order types by default, suitable for most exchange configurations.

### 2.3 Sell Signal Configuration

```python
use_sell_signal = True       # Enable signal-based selling
sell_profit_only = True      # Only use sell signals when profitable
sell_profit_offset = 0.01    # 1% profit threshold
ignore_roi_if_buy_signal = False  # ROI and signals work independently
```

---

## III. Buy Conditions Detailed Explanation

### 3.1 Core Buy Logic

The strategy employs two classic Bollinger Band bounce buy conditions, both based on oversold reversal theory:

#### Condition #1: RB1 - Classic BB Lower Band Bounce

```python
RB1 = (
    (qtpylib.crossed_above(dataframe['rsi'], 35)) &  # RSI crosses above 35
    (dataframe['close'] < dataframe['bb_lowerband'])  # Close price below BB lower band
)
```

**Logic Interpretation**:
- Price breaks below the lower Bollinger Band, indicating extreme oversold market condition
- RSI crosses above 35 from below, suggesting reversal momentum is starting
- Both conditions met together confirms the reversal signal

#### Condition #2: RB2 - TEMA-Confirmed Deep Oversold

```python
RB2 = (
    (dataframe['rsi'] < 23) &                        # RSI extremely oversold
    (dataframe["tema"] < dataframe["bb_lowerband"]) & # TEMA below BB lower band
    (dataframe["tema"] > dataframe["tema"].shift(1)) & # TEMA starting to rise
    (dataframe["volume"] > 0)                         # Valid volume
)
```

**Logic Interpretation**:
- RSI < 23 indicates extreme oversold, market sentiment extremely pessimistic
- TEMA (Triple Exponential Moving Average) below BB lower band confirms deep price deviation
- TEMA starting to rise hints at reversal trend initiation
- Volume > 0 excludes invalid data

### 3.2 Buy Condition Classification Table

| Condition ID | Core Logic | Trigger Scenario |
|--------------|------------|-------------------|
| RB1 | RSI crosses above 35 + price below BB lower band | Early stage of BB lower band bounce |
| RB2 | RSI < 23 + TEMA rise confirmation | Deep oversold reversal |

---

## IV. Sell Logic Detailed Explanation

### 4.1 Basic Sell Signals

The strategy has two basic sell signals:

#### Signal #1: RS1 - RSI Overbought Exit

```python
RS1 = (dataframe['rsi'] > 70)
```

**Logic Interpretation**:
- RSI above 70 indicates market has entered overbought territory
- Classic RSI overbought exit signal

#### Signal #2: RS2 - Price Breakout High

```python
RS2 = (dataframe["high"] > dataframe["close_max"])
```

**Logic Interpretation**:
- Triggers when highest price breaks above the highest price of past 60 candles
- Indicates price has broken recent high, may enter new uptrend or correction

### 4.2 Dynamic Stop Loss System

The core protection mechanism is a tiered dynamic stop loss:

```python
def custom_stoploss(...):
    sl_new = 1
    
    if self.config['runmode'].value in ('live', 'dry_run'):
        sl_new = 0.001  # Live trading base stop loss
    
    if (current_profit > 0.2):
        sl_new = 0.05   # Profit >20%, lock 5%
    elif (current_profit > 0.1):
        sl_new = 0.03   # Profit >10%, lock 3%
    elif (current_profit > 0.06):
        sl_new = 0.02   # Profit >6%, lock 2%
    elif (current_profit > 0.03):
        sl_new = 0.01   # Profit >3%, lock 1%
    
    return sl_new
```

**Stop Loss Logic Table**:

| Profit Range | Stop Loss Lock | Protection Effect |
|---------------|----------------|-------------------|
| >20% | 5% | Retains at least 15% profit |
| >10% | 3% | Retains at least 7% profit |
| >6% | 2% | Retains at least 4% profit |
| >3% | 1% | Retains at least 2% profit |
| Other | 0.001 | Live trading base protection |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| **Momentum** | RSI(14) | Overbought/oversold determination |
| **Trend** | Bollinger Bands(20, 2) | Price deviation assessment |
| **Trend** | TEMA(9) | Reversal confirmation |
| **Statistical** | Rolling High(60) | Breakout determination |

### 5.2 Auxiliary Indicators

```python
# Market state indicators
dataframe['close_max'] = dataframe['close'].rolling(window=60).max()  # 60-period highest price
dataframe['close_min'] = dataframe['close'].rolling(window=60).min()  # 60-period lowest price
dataframe['dropped_by_percent'] = (1 - (dataframe['close'] / dataframe['close_max']))  # Drop percentage
dataframe['pumped_by_percent'] = (dataframe['high'] - dataframe['close_min']) / dataframe['high']  # Pump percentage
```

---

## VI. Risk Management Features

### 6.1 Tiered Stop Loss Protection

The strategy uses a 5-tier stop loss, with the core design philosophy:
- Higher profit, tighter stop loss
- Each tier retains at least 2% profit margin
- Prevents "letting profits slip away"

### 6.2 Only Sell When Profitable

```python
sell_profit_only = True
sell_profit_offset = 0.01
```

This configuration ensures:
- Sell signals only trigger when profit > 1%
- Avoids triggering sell signals during small losses
- Relies on hard stop loss for protection during losses

### 6.3 New Candle Processing Mode

```python
process_only_new_candles = True
```

Only processes signals when new candles form, avoids repeated calculations, saves computational resources.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Clear and Simple Logic**: Only uses two classic indicators - Bollinger Bands and RSI, easy to understand and debug
2. **Reversal Capture Ability**: Focuses on oversold reversal opportunities, suitable for oscillating markets
3. **Dynamic Stop Loss Protection**: Tiered stop loss effectively locks in profits, prevents excessive drawdowns
4. **Low Startup Data Requirement**: 144 candles (approximately 36 hours), suitable for quick backtesting

### ⚠️ Limitations

1. **Poor Performance in Trending Markets**: As a reversal strategy, may frequently enter against the trend in strong trending markets
2. **ROI Target Too Large**: 30% ROI target may result in excessively long holding periods
3. **Missing Informative Time Frame**: No higher timeframe trend judgment, may misjudge major trend direction
4. **Overbought Exit May Be Too Early**: RSI>70 sell may exit too early during strong uptrends

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Oscillating Market** | Default configuration | Many oversold reversal opportunities, strategy performs best |
| **Slow Bull Trend** | Adjust ROI to lower value | Avoid selling too early, follow the trend |
| **Sharp Drop Market** | Use with caution | May catch falling knives, risk of being trapped |
| **Sideways Consolidation** | Default configuration | Suitable for range-bound oscillation trading |

---

## IX. Applicable Market Environment Detailed Analysis

BBRSIv2 is a typical **oversold reversal strategy**. Based on its code architecture and community live trading experience, it performs best in **oscillating volatile markets**, while performing poorly in **one-sided strong trending markets**.

### 9.1 Core Strategy Logic

- **Oversold Capture**: Relies on BB lower band and RSI low positions to determine entry timing
- **Reversal Confirmation**: Uses TEMA rise to confirm reversal trend initiation
- **Tiered Protection**: Dynamic stop loss locks in profits, prevents drawdowns

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Slow Bull Uptrend | ⭐⭐⭐☆☆ | May exit too early on overbought, missing some gains |
| 🔄 Oscillating Volatile | ⭐⭐⭐⭐⭐ | Many oversold reversal opportunities, strategy performs best |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | Buying against the trend may result in being trapped, high risk |
| ⚡️ Rapid Surge | ⭐☆☆☆☆ | Cannot catch explosive moves, may exit too early |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| minimal_roi | {"0": 0.15} | Lower target in oscillating markets for faster turnover |
| stoploss | -0.08 | Can appropriately tighten stop loss |
| Time Frame | 15m (default) | Suitable for most scenarios |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

BBRSIv2 is an entry-level strategy with low learning cost:
- Only need to understand two major indicators: Bollinger Bands and RSI
- Buy and sell logic is intuitive and easy to understand
- Suitable for beginners to learn and debug

### 10.2 Hardware Requirements

| Pair Count | Minimum Memory | Recommended Memory |
|-----------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

Strategy has low computational requirement, suitable for low-spec VPS.

### 10.3 Backtesting vs Live Trading Differences

As a simple strategy, backtesting and live trading differences are small:
- No complex parameter fitting risk
- Indicator calculations are stable and reliable
- Main differences come from slippage and liquidity

### 10.4 Manual Trader Recommendations

Manual traders can directly apply:
- Consider entry when RSI < 35 and price touches BB lower band
- Consider exit when RSI > 70 or breaking recent highs
- After profit exceeds threshold, tighten stop loss to lock in gains

---

## XI. Summary

**BBRSIv2** is a classic and concise oversold reversal strategy. Its core value lies in:

1. **Clear Logic**: Bollinger Bands + RSI combination, classic technical analysis theory
2. **Dynamic Protection**: Tiered stop loss effectively locks in profits
3. **Easy Debugging**: Few parameters, simple logic, suitable for learning

For quantitative trading beginners, BBRSIv2 is an excellent starting point for learning strategy development. It's recommended to test in oscillating markets first, verify the effectiveness of reversal logic, then gradually expand to other market environments.

---

*Strategy ID: #437*
*Document Version: v1.0*