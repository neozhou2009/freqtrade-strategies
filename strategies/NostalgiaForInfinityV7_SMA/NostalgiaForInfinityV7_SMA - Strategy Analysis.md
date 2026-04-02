# NostalgiaForInfinityV7_SMA — Strategy Analysis

> **Strategy ID**: #306 (out of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + SMA Protection + Dynamic Profit-Taking  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h) Informative Layer

---

## I. Strategy Overview

NostalgiaForInfinityV7_SMA is an important variant of the NostalgiaForInfinity series. This strategy strengthens the SMA (Simple Moving Average) related trend judgment and protection mechanisms on top of the V7 version. Developed by the iterativ team, it is one of the most popular strategy series in the Freqtrade quantitative trading framework.

The "SMA" in the name emphasizes its special reliance on Simple Moving Averages — unlike other variants that favor EMA, this strategy extensively uses SMA200 as the core trend reference, combined with EMA fast/slow lines to build multi-layered entry filters.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent signals (#1–#26, #25 missing) |
| **Sell Conditions** | 8 base sell signals + multi-layer dynamic profit-taking |
| **Protection** | 7–10 groups per condition (EMA, SMA, Safe Dips, Safe Pump) |
| **Timeframe** | Main: 5m, Informative: 1h |
| **Dependencies** | freqtrade.vendor.qtpylib, numpy, talib, pandas, functools.reduce, technical.indicators.zema |
| **Startup Candles** | 400 |

---

## II. Strategy Configuration

### 2.1 Basic Risk Parameters

```python
minimal_roi = {
    "0": 0.10,    # Immediate: 10% profit
    "30": 0.05,   # After 30 min: 5% profit
    "60": 0.02,   # After 60 min: 2% profit
}

stoploss = -0.10  # 10% fixed stop loss

trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005      # 0.5% trailing
trailing_stop_positive_offset = 0.03  # Activates after 3% profit
```

### 2.2 Key Switches

```python
use_sell_signal = True
sell_profit_only = True
ignore_roi_if_buy_signal = True
process_only_new_candles = True
```

---

## III. Buy Conditions Details

### 3.1 Protection Architecture (26 Groups)

Each buy condition has an independent protection parameter group:

| Protection Type | Parameter | Description | Default |
|----------------|-----------|-------------|---------|
| EMA Fast | ema_fast | EMA fast > EMA200 | True/False |
| EMA Fast Period | ema_fast_len | Period selection | 26/50/100/200 |
| EMA Slow | ema_slow | 1h EMA > EMA200 | True/False |
| Close Above EMA Fast | close_above_ema_fast | Close > fast EMA | True/False |
| SMA200 Rising | sma200_rising | SMA200 rising | True/False |
| SMA200 Rising Period | sma200_rising_val | Lookback | 20/30/36/44/50 |
| SMA200_1h Rising | sma200_1h_rising | 1h SMA200 rising | True/False |
| Safe Dips | safe_dips | Enable pullback protection | True/False |
| Safe Dips Level | safe_dips_type | Strictness | 10/50/80/100 |
| Safe Pump | safe_pump | Enable surge protection | True/False |
| Safe Pump Level | safe_pump_type | Strictness | 10/50/100/120 |
| Safe Pump Period | safe_pump_period | Time window | 24/36/48 hours |

### 3.2 Key Buy Conditions

**Condition #1** (Trend Following + Oversold):
```python
# Core Logic
- 36-period min rise > 2.2%
- 1h RSI in 30–84 range
- 5m RSI < 36
- MFI < 36

# Protection
- SMA200 rising (28 periods)
- Safe Dips Level 80
- Safe Pump Level 70 (24h)
```

**Condition #3** (BB40 Bandwidth Breakout):
```python
# Core Logic
- BB40 width > close × 5.9%
- Close change > close × 2.3%
- Lower wick < BB width × 41.8%
- Close < previous BB40 lower band
- Close ≤ previous close

# Protection
- EMA100 > EMA200
- EMA100_1h > EMA200_1h
- Safe Pump Level 100, 36h
```

**Condition #8** (Volume Price Reversal):
```python
# Core Logic
- RSI < 29
- Volume > previous × 2 (expansion)
- Close > Open (bullish candle)
- (Close - Low) > (Close - Open) × 3.5

# Protection
- Close > EMA200
- Safe Pump Level 120 (24h)
```

**Condition #24** (CMF Shift + EMA Golden Cross):
```python
# Core Logic
- 12 periods ago: EMA12_1h < EMA35_1h → now: EMA12_1h > EMA35_1h
- 12 periods ago: CMF_1h < 0 → now: CMF_1h > 0
- RSI < 60, RSI_1h > 66.9

# Protection
- SMA200 rising (30 periods)
- SMA200_1h rising (36 periods)
- Safe Dips Level 10
```

### 3.3 26 Conditions Classification

| Category | Condition IDs | Core Logic |
|----------|--------------|------------|
| RSI Oversold | #1, #11, #20, #21 | RSI below threshold + trend protection |
| Bollinger Band | #2, #3, #4, #5, #6, #14, #18, #23 | Price touches BB lower band |
| EMA Deviation | #5, #6, #7, #14, #15 | EMA26 > EMA12 with sufficient gap |
| EWO Oscillator | #12, #13, #16, #17, #22 | Elliott Wave Oscillator values |
| RSI Dual Timeframe | #20, #21, #23 | 5m + 1h RSI combination |
| CMF Fund Flow | #24 | Chaikin Money Flow shift |
| ZEMA | #26 | Zero-lag EMA support |
| Multi-Factor | #8, #9, #10, #19 | Volume, oscillation, trend combination |

---

## IV. Sell Logic Details

### 4.1 Multi-Level Profit-Taking (custom_sell)

| Profit Range | RSI Threshold | Signal |
|-------------|--------------|--------|
| > 20% | < 34 | signal_profit_11 |
| 10%–12% | < 42 | signal_profit_10 |
| 9%–10% | < 55 | signal_profit_9 |
| 8%–9% | < 54 | signal_profit_8 |
| 7%–8% | < 48 | signal_profit_7 |
| 6%–7% | < 45 | signal_profit_6 |
| 5%–6% | < 43 | signal_profit_5 |
| 4%–5% | < 42 | signal_profit_4 |
| 3%–4% | < 37 | signal_profit_3 |
| 2%–3% | < 35 | signal_profit_2 |
| 1%–2% | < 34 | signal_profit_1 |
| 0.1%–1% | < 34 | signal_profit_0 |

### 4.2 Below EMA200 Profit Table

Uses independent parameters (signal_profit_u_*) — more aggressive when below the main MA.

### 4.3 Pump After Profit-Taking

Detects 24h/36h/48h rises and uses dedicated parameters for "pumped" coins.

### 4.4 Trailing Stop (3 Sets)

| Set | Profit Range | RSI Range | Drawdown |
|-----|-------------|-----------|----------|
| Trail 1 | 16%–60% | 20–50 | 3% |
| Trail 2 | 10%–40% | 20–50 | 3% |
| Trail 3 | 6%–20% | — | 5% |

### 4.5 Recovery Exit

```python
# Recovery 1
sell_custom_recover_profit_1 = 0.04  # Recover to 4% profit
sell_custom_recover_min_loss_1 = 0.12  # Was down > 12%

# Recovery 2
sell_custom_recover_profit_min_2 = 0.01
sell_custom_recover_profit_max_2 = 0.05
sell_custom_recover_min_loss_2 = 0.06
sell_custom_recover_rsi_2 = 46
```

---

## V. Technical Indicators

### 5.1 Core Indicators

| Category | Indicators | Purpose |
|----------|-----------|---------|
| **EMA** | 12, 15, 20, 26, 35, 50, 100, 200 | Trend, golden/death cross, price position |
| **SMA** | 5, 30, 200 | Trend direction, MA offset entry |
| **RSI** | 4, 14, 20 | Overbought/oversold, momentum |
| **Bollinger** | BB20-2STD, BB40-2STD | Volatility channel, mean reversion |
| **MFI** | 14 | Money flow |
| **EWO** | 50–200 | Elliott Wave Oscillator |
| **CMF** | 20 | Chaikin Money Flow |
| **ZEMA** | 61 | Zero-lag EMA |
| **Choppiness** | 14 | Trending vs choppy |

---

## VI. Risk Management

### 6.1 Multi-Layer Buy Protection

| Layer | Type | Risk Avoidance |
|-------|------|----------------|
| Layer 1 | EMA Trend | Avoid counter-trend |
| Layer 2 | SMA200 Direction | Avoid bottom-fishing in downtrends |
| Layer 3 | Safe Dips | Avoid chasing highs |
| Layer 4 | Safe Pump | Avoid buying after surges |
| Layer 5 | Close Position | Ensure price in reasonable range |

### 6.2 Dynamic Stop Loss

**EMA200 Near Stop Loss**: Current profit > 0 but < 2.4%, close < EMA200, EMA200 deviation < 2.4%, RSI > RSI_1h + 4.4

**Long Holding Stop Loss**: Holding > 1200 min (20 hours), profit in -8% to -4%, current > -max_loss + 10%, close < EMA200, RSI > RSI_1h + 4, SMA200 falling

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Extremely Adaptive**: 26 conditions cover trend, oscillation, reversal — always suitable for current market
2. **Solid Defense**: Each entry has multi-layer protection, like wearing bulletproof vest + helmet
3. **Fine-Grained Profit-Taking**: Layered system makes "locking in profits" systematic
4. **Community Validated**: NostalgiaForInfinity series has years of real-trader validation
5. **Customizable**: Each condition independently switchable

### ⚠️ Limitations

1. **Overwhelming Complexity**: 26 conditions + hundreds of parameters, high learning cost
2. **Overfitting Risk**: Too many parameters, easily "fitted" to historical data
3. **High Computation**: 400 candle startup + multi-timeframe indicators, old computers may struggle
4. **Signal Conflicts**: Condition 1 says buy, Condition 10 may say wait
5. **Manual Execution Impossible**: 5-minute level + complex logic, not for humans

---

## VIII. Summary

**NostalgiaForInfinityV7_SMA** is a well-designed multi-condition trend-following strategy. Its core value:
1. **Comprehensive**: 26 conditions cover various market forms
2. **Defensive**: Multi-layer protection filters high-risk signals pre-entry
3. **Flexible**: Each condition independently configurable
4. **Mature**: NostalgiaForInfinity series has years of community validation

**Recommendations**:
- Selectively enable subset of conditions rather than all
- Maintain protection mechanism integrity
- Verify with live data against backtest parameters
- Adjust dynamically based on market environment
