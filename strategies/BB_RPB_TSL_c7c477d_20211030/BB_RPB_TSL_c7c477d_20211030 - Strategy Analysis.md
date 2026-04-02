# BB_RPB_TSL_c7c477d_20211030 Strategy Analysis

> **Strategy Number**: #41
> **Strategy Type**: Multi-Condition Trend Following + Protection Mechanisms + Dynamic Trailing Stop
> **Timeframe**: 5 minutes (5m) + 1-hour information layer

---

## I. Strategy Overview

BB_RPB_TSL_c7c477d_20211030 is a complex trend-following strategy based on Bollinger Bands combined with multiple technical indicators. The strategy integrates Real Pull Back (RPB) concepts and dynamic trailing stop mechanisms, aiming to capture pullback buying opportunities while reducing risk through multi-layer protection mechanisms.

Strategy author jilv220 states that the strategy was inspired by blog posts and GeorgeMurAlkh's Real Pullback strategy, while also borrowing Perkmeister's BigZ04_TSL trailing stop implementation.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 7 independent entry signals (can be enabled/disabled independently) |
| **Exit Conditions** | Base exit signals + multi-layer dynamic take-profit + BTC protection mechanisms |
| **Protection** | BTC 5-minute/1-day dump protection |
| **Timeframe** | Main timeframe 5m + information timeframe 1h |
| **Dependencies** | technical, talib, pandas_ta |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,      # Exit at 10% profit immediately after entry
}

# Stoploss setting
stoploss = -0.10   # Base stoploss -10%

# Trailing stop
use_custom_stoploss = True
```

**Design Logic**:
- Single ROI threshold of 10% means a 10% take-profit target is set immediately after entry
- Base stoploss set at -10%, working with custom trailing stop to "let profits run"
- Dynamic trailing stop adjusts the stoploss line based on position profit level

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (2 groups)

Each entry condition requires passing BTC protection mechanism checks:

| Protection Type | Parameter Description | Default Value Example |
|-----------------|----------------------|----------------------|
| BTC 5m Dump Protection | Detects if BTC drops more than threshold within 5 minutes | buy_threshold: 0.003 |
| BTC 1d Dump Protection | Detects if BTC has significant drop within 1 day | buy_btc_safe_1d: -0.05 |
| BTC Difference Threshold | BTC threshold calculation | buy_btc_safe: -289 |

**BTC Protection Logic**:
```python
is_btc_safe = (
    (dataframe["btc_diff"] > self.buy_btc_safe.value)
    & (dataframe["btc_5m"] - dataframe["btc_1d"] > dataframe["btc_1d"] * self.buy_btc_safe_1d.value)
    & (dataframe["volume"] > 0)
)
```

### 3.2 Typical Entry Condition Examples

#### Condition #1: BB_Dip (Bollinger Band Dip Buy)
```python
# Logic
- RMI < 49
- CCI <= -116
- STOCHRSI FastK < 32
- bb_delta > 0.025 (Bollinger Band opening width)
- bb_width > 0.095
- close_delta > close * 0.012
- close < bb_lowerband3 * 0.999
```

#### Condition #2: Local Uptrend
```python
# Logic
- ema_26 > ema_12
- (ema_26 - ema_12) > open * 0.022
- (ema_26.shift() - ema_12.shift()) > open / 100
- close < bb_lowerband2 * 0.999
- close_delta > close * 0.012
```

#### Condition #3: EWO (Elliot Wave Oscillator) - Classic Version
```python
# Logic
- rsi_fast < 21
- close < ema_8 * 0.970
- EWO > 2.055
- close < ema_16 * 1.087
- rsi < 30
```

#### Condition #4: EWO2 (Elliot Wave Oscillator) - Aggressive Version
```python
# Logic
- rsi_fast < 21
- close < ema_8 * 0.970
- EWO > 2.055 (higher threshold)
- close < ema_16 * 1.087
- rsi < 30
```

#### Condition #5: Cofi (Confirmation Trend Buy)
```python
# Logic
- open < ema_8 * 0.98
- fastk crosses above fastd
- fastk < 30
- fastd < 21
- adx > 20
- EWO > 2.055
```

#### Condition #6: NFI 32 (NFI Series Condition)
```python
# Logic
- rsi_slow < rsi_slow.shift(1)
- rsi_fast < 46
- rsi > 19
- close < sma_15 * 0.942
- cti < -0.86
```

#### Condition #7: NFI 33 (NFI Series Condition)
```python
# Logic
- close < ema_13 * 0.978
- EWO > 8
- cti < -0.88
- rsi < 32
- r_14 < -98
- volume < volume_mean_4 * 2.5
```

### 3.3 Classification of 7 Entry Conditions

| Condition Group | Condition Numbers | Core Logic |
|-----------------|-------------------|------------|
| Bollinger Breakout | bb | Wait for price to touch lower Bollinger Band then rebound |
| Trend Pullback | local_uptrend | Price pulls back to lower Bollinger Band while short-term EMA moves up |
| Momentum Reversal | ewo/ewo2 | EWO indicator shows strong upward momentum |
| Trend Confirmation | cofi | Confirms trend direction with Ichimoku Cloud |
| NFI Series | nfi_32/nfi_33 | Fast entry signals from multi-indicator combinations |

---

## IV. Exit Conditions Details

### 4.1 Multi-Layer Dynamic Take-Profit System

The strategy uses a custom trailing stop mechanism that dynamically adjusts stoploss points based on position profit level:

```python
# Trailing stop parameters
pHSL = -0.178    # Hard stoploss profit threshold
pPF_1 = 0.01     # Take-profit zone 1 trigger point (1%)
pSL_1 = 0.009    # Take-profit zone 1 stoploss line
pPF_2 = 0.048    # Take-profit zone 2 trigger point (4.8%)
pSL_2 = 0.043    # Take-profit zone 2 stoploss line
```

**Trailing Stop Logic**:
- Profit > 4.8%: Stoploss moves up (current profit - 4.3%)
- Profit 1%-4.8%: Linear interpolation adjusts stoploss line
- Profit < 1%: Uses hard stoploss -17.8%

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|------------------|-------------|
| BTC 5m sharp drop | btc_diff < -389 | sell_btc_safe |
| EMA200 breakdown | close < ema_200 * 0.988 | sell_ema |
| Capital flow deterioration | cmf < -0.046 | sell_cmf |
| RSI rise confirmation | rsi > rsi.shift(1) | rsi confirmation |

### 4.3 Base Exit Signals

```python
# Exit condition combination
- BTC protection triggered: btc_diff < sell_btc_safe (-389)
- Or EMA200 combination exit:
  - close < ema_200 * 0.988
  - cmf < -0.046
  - (ema_200 - close) / close < 0.022
  - rsi is rising
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|-------------------|--------------------|-------|
| Trend Indicators | EMA 8/12/13/16/26/200, SMA 9/15/30 | Judge price trend direction |
| Momentum Indicators | RSI (4/14/20), EWO, RMI | Detect overbought/oversold and momentum changes |
| Volatility Indicators | Bollinger Bands (20,2), CCI, Williams %R | Identify price volatility range |
| Volume Indicators | CMF, Volume Mean | Confirm validity of price breakouts |

### 5.2 Information Timeframe Indicators (1h)

Strategy uses 1-hour as information layer, providing higher-dimensional trend judgment:

- **Ichimoku Cloud Indicators**:
  - Tenkan-sen (Conversion Line)
  - Kijun-sen (Base Line)
  - Senkou Span A/B (Cloud Leading Span)
  - Chikou Span (Lagging Span)
  
- **Trend Confirmation Logic**:
  ```python
  is_ichi_ok = (
      (tenkan_sen > kijun_sen)
      & (close > cloud_top)
      & (leading_senkou_span_a > leading_senkou_span_b)
      & (chikou_span_greater)
  )
  ```

---

## VI. Risk Management Features

### 6.1 BTC Dump Protection Mechanism

Strategy has built-in dual BTC protection mechanisms to prevent losses from buying during BTC sharp declines:

- **5-minute level protection**: Monitors whether BTC dropped rapidly in recent 5 minutes
- **1-day level protection**: Monitors whether BTC declined significantly in past 24 hours

### 6.2 Dynamic Trailing Stop

Compared to fixed stoploss, dynamic trailing stop can:

- Lock more profits when market rises
- Give breathing room when market pulls back
- Adopt different strategies based on different profit zones

### 6.3 Multi-Condition Confirmation Mechanism

Each entry condition goes through multiple validations:

- Technical indicator confirmation (RSI, CCI, EWO, etc.)
- Trend direction confirmation (EMA relationships)
- Volatility confirmation (BB width)
- Volume confirmation (CMF, Volume)

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Multi-condition coverage**: 7 different entry conditions can adapt to different market environments
2. **BTC protection**: Effectively avoids systemic risk in crypto markets
3. **Dynamic take-profit**: Lets profits run while controlling drawdown
4. **Multi-timeframe**: Combines 1h information layer for trend confirmation

### ⚠️ Cons

1. **Complex parameters**: Large number of hyperparameters need optimization through hyperopt
2. **Computationally intensive**: Multi-timeframe and multi-indicator calculations demand high hardware requirements
3. **Overfitting risk**: Multi-condition strategies easily overfit historical data
4. **Signal conflicts**: Different entry conditions may trigger different signals at same moment

---

## VIII. Parameter Optimization

| Parameter Category | Optimization Priority | Notes |
|-------------------|----------------------|-------|
| BTC Protection | High | Critical for risk control |
| Entry Thresholds | High | Affects signal frequency |
| Trailing Stop | Medium | Profit protection mechanism |
| Indicator Periods | Low | Default values generally work |

---

## IX. Live Trading Notes

### 9.1 Learning Curve

This strategy involves multiple technical indicators and multi-timeframe analysis. Beginners need to spend considerable time understanding the logic of each entry condition. Recommended to test on demo account first, observing trigger frequency and performance of each entry condition.

### 9.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|-------------|-----------------|
| 10-20 | 2GB | 4GB |
| 20-50 | 4GB | 8GB |
| 50+ | 8GB | 16GB |

### 9.3 Differences Between Backtest and Live Trading

- Multi-timeframe strategies require downloading more historical data
- Ichimoku indicators have forward-looking issues, requiring sufficient warmup period
- Network latency in live trading may affect signal execution

### 9.4 Manual Trader Suggestions

Manual traders can focus on these conditions:
- Price touches lower Bollinger Band
- RSI in oversold region
- EWO crosses above zero axis
- 1-hour trend upward (EMA200)

---

## X. Summary

BB_RPB_TSL_c7c477d_20211030 is a well-designed Bollinger Band trend-following strategy. Its core value lies in:

1. **Multi-condition coverage**: 7 entry conditions adapt to different market environments
2. **Risk control**: Dual protection from BTC protection + dynamic trailing stop
3. **Trend confirmation**: Multi-timeframe analysis improves signal quality
4. **Community validation**: Improved from mature strategies with some live trading validation

For quantitative traders, this strategy suits investors with certain quantitative foundation. Before use, recommended to:
1. Fully understand logic of each entry condition
2. Conduct sufficient testing on demo account
3. Adjust parameters based on target market
4. Pay attention to risk management, don't heavily position on single strategy

---

*This document is based on strategy code v1.0*
