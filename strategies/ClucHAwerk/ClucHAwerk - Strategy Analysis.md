# ClucHAwerk Strategy Analysis

## I. Strategy Overview

ClucHAwerk is a trading strategy that combines **Heikin Ashi (HA)** with **Bollinger Bands**, using a 1-minute short-term timeframe with 1-hour trend filtering. The strategy uses multiple technical indicator combinations to filter entry timing, implementing risk control through dynamic take-profit and trailing stop mechanisms.

### Core Features

| Item | Content |
|------|---------|
| Strategy Name | ClucHAwerk |
| Main Timeframe | 1 Minute |
| Informative Timeframe | 1 Hour |
| Core Indicators | Heikin Ashi, Bollinger Bands, ROCR, EMA, Volume Mean |
| Buy Logic | Dual conditions (either): Bollinger Band breakout + momentum OR extreme oversold |
| Sell Logic | Trend reversal signal + price reaching Bollinger middle band |
| Stop-Loss | -2.139% |
| Trailing Stop | Enabled (activates at 9.291%, triggers at 10.651%) |
| Applicable Pairs | Multi-coin (ETH, BTC, USD independently optimized versions) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Parameters

```python
timeframe = '1m'
startup_candle_count: int = 168  # Requires 168 candles for warmup

use_exit_signal = True
exit_profit_only = True           # Sell only when profitable
exit_profit_offset = 0.0
ignore_roi_if_entry_signal = True # Ignore ROI limits when buy signal appears
```

### 2.2 Entry Parameters (Hyperopt Optimized Results)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `bbdelta-close` | 0.01021 | Bollinger Band width to close price ratio threshold |
| `bbdelta-tail` | 0.88118 | Lower wick to Bollinger Band width ratio |
| `close-bblower` | 0.0022 | Close price to Bollinger lower band ratio |
| `closedelta-close` | 0.00519 | Price change magnitude threshold |
| `rocr-1h` | 0.50931 | 1-hour ROCR threshold (trend filter) |
| `volume` | 35 | Volume multiple threshold |

### 2.3 Sell Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `sell-bbmiddle-close` | 1.01283 | Close price to Bollinger middle band ratio |
| `sell-rocr-1h` | 0.95269 | 1-hour ROCR sell threshold |

### 2.4 ROI (Profit Target) Table

| Holding Time (Minutes) | Minimum Return |
|----------------------|----------------|
| 0 | 11.054% |
| 2 | 5.569% |
| 10 | 3.055% |
| 16 | 2.311% |
| 82 | 1.267% |
| 238 | 0.301% |
| 480+ | 0% |

---

## III. Entry Conditions Details

ClucHAwerk's entry conditions use a **dual-track parallel** design — meeting **any one condition** triggers a buy signal:

### Condition A: Bollinger Band Convergence Breakout

```
Conditions:
1. rocr_1h > 0.50931 (1-hour trend upward)
2. lower.shift(1) > 0 (Bollinger lower band exists)
3. bbdelta > ha_close × 0.01021 (Bollinger Band spread wide enough)
4. closedelta > ha_close × 0.00519 (price volatility sufficient)
5. tail < bbdelta × 0.88118 (lower wick short)
6. ha_close < lower.shift(1) (close below previous lower band)
7. ha_close ≤ ha_close.shift(1) (close not higher than previous candle)
```

**Logic Interpretation**: This condition captures **a surge in selling pressure followed by exhaustion of bearish momentum**, suggesting a potential reversal.

### Condition B: Extreme Oversold Rebound

```
Conditions:
1. ha_close < ema_slow (price below long-term EMA, in weak position)
2. ha_close < close-bblower × bb_lowerband (i.e., < 0.0022 × lower band)
3. volume < volume_mean_slow.shift(1) × volume (volume shrinking)
```

**Logic Interpretation**: This condition captures **extreme low-volume oversold rebound opportunities**, similar to buying in the extreme zone of Williams %R.

---

## IV. Exit Conditions Details

Exit conditions require **all three conditions to be met simultaneously**:

```
1. rocr_1h < 0.95269 (1-hour trend turning bad)
2. ha_close × 1.01283 > bb_middleband (price reaching or breaking Bollinger middle band)
3. volume > 0 (excluding volume anomalies)
```

**Core Logic**:
- Uses 1-hour ROCR to judge medium-to-long-term trend reversal.
- Bollinger middle band serves as a **dynamic take-profit level** (sell when price rises from bottom to middle band).
- This design lets profits run while exiting promptly when trends weaken.

---

## V. Technical Indicator System

### 5.1 Heikin Ashi (HA)

The strategy uses qtpylib.heikinashi to compute average candles:
- ha_open = (previous ha_open + previous ha_close) / 2
- ha_close = (open + high + low + close) / 4
- ha_high = max(high, ha_open, ha_close)
- ha_low = min(low, ha_open, ha_close)

**Purpose**: Smooth price fluctuations, filter market noise, display trends more clearly.

### 5.2 Bollinger Bands

```python
# Custom Bollinger Bands (for entry)
mid, lower = bollinger_bands(ha_close, window_size=40, num_of_std=2)
# Standard Bollinger Bands (for exit)
bollinger = qtpylib.bollinger_bands(ha_typical_price, window=20, stds=2)
```

- **40-period Bollinger Bands**: Used for entry judgment, larger window, more stable.
- **20-period Bollinger Bands**: Used for exit judgment, smaller window, more sensitive.

### 5.3 ROCR (Rate of Change)

```python
# 1-minute ROCR
dataframe['rocr'] = ta.ROCR(ha_close, timeperiod=28)

# 1-hour ROCR (trend filter)
informative['roft'] = ta.ROCR(informative['ha_close'], timeperiod=168)
```

- 28-period ROCR: Measures short-term momentum.
- 168-period (1-hour × 168) ROCR: Measures long-term trend.

### 5.4 Auxiliary Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| EMA | 50 | Judge price relative position |
| Volume Mean | 30 | Volume filtering |
| bbdelta | Dynamic | Bollinger Band spread width |
| closedelta | Dynamic | Price change magnitude |
| tail | Dynamic | Lower wick length |

---

## VI. Risk Management Features

### 6.1 Stop-Loss Mechanism

```python
stoploss = -0.02139  # Fixed stop-loss -2.139%
```

Compared to typical strategies with -5% or -10% stop-loss, this strategy's stop-loss is very tight, reflecting **high-frequency trading** characteristics.

### 6.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.09291     # Activates after 9.291% profit
trailing_stop_positive_offset = 0.10651  # Trigger level
trailing_only_offset_is_reached = False
```

**Characteristics**:
- Low activation threshold (9.291%).
- Trailing range approximately 10.651%.
- Suitable for capturing large mid-trend swings.

### 6.3 Dynamic ROI

The strategy uses **progressive ROI** — the longer the holding time, the lower the take-profit target:

| Holding Time | Minimum Profit Target |
|-------------|----------------------|
| Immediate | 11.054% |
| Within 2 minutes | 5.569% |
| Within 10 minutes | 3.055% |
| After 480 minutes (8 hours) | 0% (relies only on trailing stop) |

This design encourages **longer holding** for greater profits while giving **shorter holding** clear quick-profit targets.

---

## VII. Strategy Pros & Cons

### 7.1 Pros

1. **Multi-Timeframe Combination**: 1-minute for short-term, 1-hour for trend filtering, reduces false signals.
2. **Dual Entry Conditions**: Captures both reversals and oversold bounces, strong adaptability.
3. **Tight Stop-Loss**: -2.139% stop-loss is narrow; single loss is controllable.
4. **Dynamic Take-Profit**: ROI + trailing stop double protection.
5. **Multi-Coin Optimization**: Provides ETH, BTC, USD three variants, more targeted.

### 7.2 Cons

1. **High Parameter Sensitivity**: All entry parameters are hyperopt-optimized; direct use may be less effective.
2. **Depends on Trending Markets**: In ranging markets, ROCR may hover in middle values, reducing trading frequency.
3. **High Trading Frequency**: 1-minute timeframe requires sufficient liquidity and low fee environment.
4. **High Complexity**: Multi-indicator combinations increase understanding and parameter-tuning difficulty.

---

## VIII. Applicable Scenarios

### Recommended For

- **Coins**: Mainstream coins (BTC, ETH, high-liquidity coins)
- **Market Environment**: Markets with clear trends (buying pullbacks in uptrends works best)
- **Timeframe**: Only 1-minute recommended (if longer periods needed, must re-Hyperopt)
- **Capital Management**: Suggest controlling per-trade risk exposure at 1%-2%

### Not Recommended For

- Markets with extremely low volatility (volume shrinkage causes Condition B to fail)
- Highly manipulated junk coins (easily exploited by smart money using technical indicators)
- Exchanges with high fees (high-frequency trading erodes profits)

---

## IX. Applicable Market Environment Details

### 9.1 Best Environments

- **Trending Markets**: When uptrends pull back to the Bollinger lower band, Condition A triggers most frequently.
- **High Volatility Markets**: Large price swings → bbdelta and closedelta more easily satisfy thresholds.
- **Sufficient Liquidity**: Ensures orders fill quickly, avoids slippage.

### 9.2 Average Performance Environments

- **Sideways Ranging**: ROCR hovers between 0.5-0.95, fewer buy signals.
- **Rapid Decline**: Condition A may fail (needs price contraction), Condition B may be too sensitive causing failed bottom-fishing.

### 9.3 Environments Requiring Caution

- **Extreme Volatility**: Surges/crashes may cause indicators to fail.
- **Exchange Maintenance**: 1-hour data interruption causes strategy anomalies.

---

## X. Important Reminder: The Cost of Complexity

ClucHAwerk is a **highly parameterized** strategy — all key parameters come from Hyperopt optimization. This means:

1. **Overfitting Risk**: Default parameters may overfit historical data.
2. **Market Changes**: Parameter effectiveness may decline as market structure changes.
3. **Understanding Threshold**: Effectively optimizing requires understanding Heikin Ashi, Bollinger Bands, and ROCR simultaneously.

**Recommendations**:
- First verify with default parameters in paper trading.
- Evaluate after running at least 1 month.
- If adjustment needed, prioritize `stoploss` and `trailing_stop` series parameters.
- Avoid adjusting all entry parameters at once.

---

## XI. Summary

ClucHAwerk is a **technical indicator-driven high-frequency trend-following strategy**. It smooths price fluctuations using Heikin Ashi, identifies support/resistance using Bollinger Bands, and judges trend momentum using ROCR — forming a relatively complete **trend reversal capture system**.

The strategy's core idea is:
> Under the premise of upward trend, wait for price to pull back to the Bollinger lower band and appear with a reversal signal to buy, then hold until the trend weakens or price reaches the middle band to sell.

Its strength is **tight stop-loss, good risk control, multi-timeframe signal filtering**; its weakness is **high parameter dependency, sensitivity to market conditions, and need for low-fee environment** to sustain.

Recommended for traders with some technical analysis background, and be sure to fully verify in paper trading before going live.
