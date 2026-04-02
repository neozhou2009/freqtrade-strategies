# TemaMaster Strategy Deep Dive

> **Strategy Number**: #408 (408th of 465 strategies)  
> **Strategy Type**: Multi-Indicator Trend Following + Trailing Take-Profit  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

TemaMaster is a trend-following strategy based on Triple Exponential Moving Average (TEMA) and Bollinger Band breakout. The core idea is to capture price reversal opportunities near the Bollinger lower band, combined with momentum indicator (CMO) filtering, while using trailing stop to lock in large profits.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 composite buy signal (TEMA crosses above BB lower band + CMO filter) |
| **Sell Condition** | No active sell signals, relies on ROI and trailing stop |
| **Protection Mechanism** | Trailing stop + Profit-only sell |
| **Timeframe** | 5 minutes (5m) |
| **Dependencies** | talib, qtpylib |
| **Info Pair** | stake_currency/USDT (reference exchange rate) |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.20937,      # Any time: 20.937% profit
    "238": 0.06449,    # After 238 minutes: 6.449% profit
    "1931": 0.01703,   # After 1931 minutes: 1.703% profit
    "3474": 0          # After 3474 minutes: exit at any profit
}

# Stop-loss setting
stoploss = -0.14791  # 14.791% stop-loss
```

**Design Philosophy**:
- ROI setting is very aggressive, initial target as high as 20.937%
- As time progresses, lower profit expectations to ensure eventual profit-taking
- Stop-loss is relatively wide (-14.791%), giving trends enough room to fluctuate

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.17017       # Start trailing after 17.017% profit
trailing_stop_positive_offset = 0.26713  # Trailing distance 26.713%
trailing_only_offset_is_reached = True   # Only start trailing after offset reached
```

**Trailing Stop Logic**:
- Only start trailing stop when profit reaches 26.713%
- Trailing stop distance is 17.017%, meaning sell only when price retraces 17% from peak
- This is an aggressive "let profits run" configuration

### 2.3 Sell Signal Configuration

```python
use_sell_signal = True
sell_profit_only = True              # Only sell when profitable
ignore_roi_if_buy_signal = False     # Don't ignore ROI when buy signal exists
```

---

## 3. Buy Condition Details

### 3.1 Protection Mechanism

This strategy mainly relies on trailing stop and ROI exit, without traditional buy protection parameters.

### 3.2 Buy Condition Details

#### Condition #1: TEMA Breakout of Bollinger Lower Band

```python
# Logic
- TEMA(18) crosses above Bollinger Band lower band
- CMO(14) > -5
```

**Core Indicator Explanation**:

| Indicator | Parameter | Purpose |
|-----------|-----------|---------|
| TEMA (Triple EMA) | Period 18 | Smooth price trend |
| Bollinger Bands | Period 26, StdDev 1.4 | Volatility channel |
| CMO (Chande Momentum Oscillator) | Period 14 | Momentum filter |

**Buy Logic Interpretation**:

1. **TEMA crosses above BB lower band**: Price breaking above Bollinger lower band from below may indicate oversold rebound
2. **CMO > -5**: Momentum indicator not too negative, excluding extreme downtrends

---

## 4. Sell Logic Details

### 4.1 Tiered ROI Exit System

The strategy uses a multi-tier ROI exit mechanism:

```
Time (minutes)    Minimum Profit Rate    Description
─────────────────────────────────────────────────────
0                 20.937%               Initial aggressive target
238               6.449%                Lower expectations after ~4 hours
1931              1.703%                Further lower after ~32 hours
3474              0%                    Forced exit after ~58 hours
```

**Design Philosophy**:
- Pursue high returns at position opening (20%+)
- Lower expectations over time to avoid prolonged holding
- Force exit after ~2.5 days to avoid overnight risk

### 4.2 Trailing Take-Profit Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| trailing_stop_positive | 17.017% | Trailing distance |
| trailing_stop_positive_offset | 26.713% | Activation threshold |
| trailing_only_offset_is_reached | True | Only activate after threshold |

**How It Works**:
- After profit reaches 26.713%, trailing stop activates
- Sell when price retraces more than 17% from peak
- This means: even if price rises to +30%, it won't sell until dropping to +13%

### 4.3 Sell Signal

```python
# Sell condition: None (no active sell signal)
```

The strategy doesn't rely on technical indicators for selling, completely relying on ROI and trailing stop.

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend Indicator | TEMA (Triple EMA) | Smooth price, identify trend direction |
| Volatility Indicator | Bollinger Bands | Identify overbought/oversold zones |
| Momentum Indicator | CMO | Filter extreme momentum situations |
| Statistical Indicator | STDDEV, MA, COEFFV | Auxiliary volatility calculation |

### 5.2 Indicator Calculation Details

#### TEMA (Triple Exponential Moving Average)

```python
TEMA = 3 * EMA - 3 * EMA(EMA) + EMA(EMA(EMA))
```

- Period: 18
- Characteristics: Smoother than regular EMA, lower lag

#### Bollinger Bands

```python
Middle Band = SMA(26)
Upper Band = Middle Band + 1.4 × Standard Deviation
Lower Band = Middle Band - 1.4 × Standard Deviation
```

- Period: 26
- Standard deviation multiplier: 1.4 (narrower than default 2)

#### CMO (Chande Momentum Oscillator)

```python
CMO = 100 × (Sum of Up Days - Sum of Down Days) / (Sum of Up Days + Sum of Down Days)
```

- Period: 14
- Range: -100 to +100

### 5.3 Info Timeframe Indicator

The strategy uses `informative_pairs` to get stake_currency/USDT exchange rate:

```python
def informative_pairs(self):
    return [(f"{self.config['stake_currency']}/USDT", self.timeframe)]
```

**Purpose**: Reference mainstream coin movement, but not actually used in code.

---

## 6. Risk Management Features

### 6.1 Tiered ROI System

The strategy uses progressive ROI:

| Stage | Time Range | Target Profit | Risk Preference |
|-------|-----------|---------------|-----------------|
| Aggressive | 0-238 minutes | 20.937% | High risk high return |
| Transitional | 238-1931 minutes | 6.449% | Medium risk |
| Conservative | 1931-3474 minutes | 1.703% | Low risk |
| Forced | > 3474 minutes | 0% | Forced exit |

### 6.2 Trailing Take-Profit

| Scenario | Trigger Condition | Result |
|----------|-------------------|--------|
| Fast rise | Profit > 26.713% | Trailing stop activates |
| Retracement protection | Retrace > 17% from peak | Sell to lock profit |
| Below threshold | Profit < 26.713% | Rely on ROI or stop-loss only |

### 6.3 Profit-Only Sell

```python
sell_profit_only = True
```

Ensures sell signals only work when profitable, avoiding selling at a loss.

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Trailing take-profit design**: Let profits run, suitable for catching big trends
2. **Multi-indicator combination**: TEMA + BB + CMO triple filtering
3. **Tiered ROI**: Balances profit expectations with holding time
4. **Info pair configuration**: Supports reference exchange rate information

### ⚠️ Limitations

1. **No active sell**: Completely relies on ROI and trailing stop
2. **Aggressive parameters**: Initial ROI target 20%+ may be hard to achieve
3. **High trailing stop threshold**: 26.7% to activate, may miss medium gains
4. **Wide stop-loss**: -14.8% stop-loss is wide, single trade loss may be large

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Strong Trend Market | Default configuration | Trailing take-profit plays its role |
| Ranging Market | Lower ROI target | Avoid prolonged holding |
| High Volatility Coins | Tighten stop-loss | Reduce single trade risk |
| Low Volatility Coins | Expand BB parameters | Adapt to narrower volatility |

---

## 9. Applicable Market Environment Details

TemaMaster is an aggressive trend-following strategy. Based on its trailing take-profit and high ROI target design, it is best suited for **strong trend markets**, while performance in ranging markets may be poor.

### 9.1 Strategy Core Logic

- **Breakout buy**: TEMA breaks above BB lower band, catching oversold reversals
- **Let profits run**: Trailing take-profit allows capturing excess returns in big trends
- **Time for space**: Tiered ROI balances profit expectations with holding time

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 Strong Trend | ⭐⭐⭐⭐⭐ | Trailing take-profit maximizes returns |
| 🔄 Ranging | ⭐⭐☆☆☆ | Frequent breakout false signals, stop-loss may trigger multiple times |
| 📉 Downtrend | ⭐☆☆☆☆ | Few buy signals, frequent stop-losses |
| ⚡ High Volatility | ⭐⭐⭐⭐☆ | BB breakouts more effective, more room for trailing take-profit |

### 9.3 Key Configuration Recommendations

| Configuration Item | Suggested Value | Description |
|-------------------|-----------------|-------------|
| trailing_stop_positive_offset | 0.15-0.20 | Lower activation threshold, protect profits faster |
| minimal_roi["0"] | 0.10-0.15 | Lower initial ROI target |
| stoploss | -0.10 | Tighten stop-loss, control single trade risk |

---

## 10. Important Reminder: Risks of Aggressive Strategy

### 10.1 Double-edged Sword of Trailing Take-Profit

Trailing take-profit design is beautiful under high return expectations, but:

- **High threshold problem**: 26.7% to start trailing, medium gains cannot be protected
- **Wide retracement space**: 17% retracement space, may give back a lot from peak

### 10.2 Aggressiveness of ROI Parameters

| ROI Stage | Target | Problem |
|-----------|--------|---------|
| Initial | 20.937% | 20% in a day in crypto is uncommon |
| After 4 hours | 6.449% | Relatively reasonable |
| After 32 hours | 1.703% | May be too low |

### 10.3 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

The strategy has moderate computation, requiring adequate hardware support.

### 10.4 Difference Between Backtesting and Live Trading

Aggressive parameters may perform well in backtesting (because optimal parameters were selected), but in live trading:

- **High ROI target hard to achieve**: 20% gains aren't common
- **Trailing take-profit may not be used**: Most trades won't reach 26.7%

---

## 11. Summary

**TemaMaster** is an aggressive trend-following strategy. Its core value lies in:

1. **Trailing take-profit mechanism**: Suitable for catching big trends, letting profits run
2. **Multi-indicator combination**: TEMA + BB + CMO provides multiple filtering
3. **Tiered ROI**: Balances profit expectations with holding time

For quantitative traders, it's recommended to adjust trailing take-profit threshold and ROI targets based on backtesting results to make them more suitable for live trading.

---

*Strategy Number: #408*