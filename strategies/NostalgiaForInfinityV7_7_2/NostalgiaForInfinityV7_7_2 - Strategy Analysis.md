# NostalgiaForInfinityV7_7_2 — Strategy Analysis

> **Strategy ID**: #305 (out of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + Multi-Layer Dynamic Profit-Taking + Comprehensive Protection  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h)

---

## I. Strategy Overview

NostalgiaForInfinityV7_7_2 is an important version of the NostalgiaForInfinity series, developed and maintained by the iterativ team. This strategy inherits the series' signature complex architecture design, constructing a highly defensive trend-following trading system through extensively designed buy conditions, rigorous protection mechanisms, and multi-layered sell logic.

As one of the most well-known open-source strategies in the Freqtrade ecosystem, the NostalgiaForInfinity series is famous for its "conditions so numerous it's outrageous" characteristic. Version V7_7_2 continues this tradition, containing **44 independent buy conditions** and **8 base sell conditions**, complemented by highly complex custom sell logic, aiming to capture trend opportunities in the crypto market while minimizing damage from incorrect signals as much as possible.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 44 independent buy signals, all independently enableable/disableable |
| **Sell Conditions** | 8 base sell signals + multi-layer dynamic profit-taking (graded profit-taking, trailing stop, special scenario exits) |
| **Protection** | 44 groups of buy protection parameters (EMA trend, SMA rising trend, Safe Dips, Safe Pump, BTC trend filtering, etc.) |
| **Timeframe** | Main: 5m, Informative: 1h, Optional: BTC reference timeframe |
| **Dependencies** | pandas_ta (required), talib, technical |
| **Stop Loss** | Static -10%, Trailing +1% (activates after 3% rise) |

---

## II. Strategy Configuration

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,   # Immediate: 10% profit
    "30": 0.05,  # After 30 min: 5% profit
    "60": 0.02,  # After 60 min: 2% profit
}

# Stop Loss
stoploss = -0.10  # 10% stop loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01       # 1% trailing
trailing_stop_positive_offset = 0.03  # Activates after 3% profit
```

### 2.2 Startup Period

```python
startup_candle_count: int = 480  # 480 × 5-minute candles ≈ 40 hours
```

### 2.3 Key Configuration

| Parameter | Recommended Value | Notes |
|-----------|------------------|-------|
| Trading pairs | 40–80 | Volume-sorted |
| Max open trades | 4–6 | Balanced risk |
| Quote currency | USDT/BUSD | Avoid BTC/ETH pairs |
| Blacklist | *BULL, *BEAR, *UP, *DOWN | Leverage tokens |

---

## III. Buy Conditions Details

### 3.1 Protection Mechanisms (44 Groups)

Each of the 44 buy conditions is equipped with an independent protection parameter group. Each protection group contains:

| Protection Type | Description |
|----------------|-------------|
| **EMA Fast Trend** | Fast EMA above EMA200 |
| **EMA Slow Trend** | 1h EMA above EMA200_1h |
| **Close Above EMA Fast** | Close price above fast EMA |
| **Close Above EMA Slow** | Close price above 1h EMA |
| **SMA200 Rising** | SMA200 rising in specified periods |
| **SMA200_1h Rising** | 1h SMA200 rising |
| **Safe Dips** | 13 levels of thresholds to prevent catching falling knives |
| **Safe Pump** | 12 levels × 3 time windows to prevent chasing |
| **BTC Trend Filter** | Buy only when BTC is not in a downtrend on 1h |

### 3.2 Safe Dips/Pump Threshold System

13 levels of dips thresholds and pump thresholds, from most conservative (Level 10) to most aggressive (Level 130):

**Dips Example — Level 10 (Most Conservative)**:
```python
buy_dip_threshold_10_1 = 0.015  # Current candle max drop: 1.5%
buy_dip_threshold_10_2 = 0.1    # 2-candle max drop: 10%
buy_dip_threshold_10_3 = 0.24   # 12-candle max drop: 24%
buy_dip_threshold_10_4 = 0.42   # 144-candle max drop: 42%
```

**Dips Example — Level 130 (Most Aggressive)**:
```python
buy_dip_threshold_130_1 = 0.028
buy_dip_threshold_130_2 = 0.3
buy_dip_threshold_130_3 = 0.48
buy_dip_threshold_130_4 = 0.9   # Allows 90% drop!
```

### 3.3 Key Buy Conditions

**Condition #1** (Trend Confirmation):
```python
# Protections
- ema_slow: True (EMA100_1h > EMA200_1h)
- sma200_rising: True (SMA200 up in 28 periods)

# Core Logic
- 36-period min rise > 2.2%
- RSI_1h in 20–84 range (not extreme)
- RSI_5m < 36
- MFI < 50
- CTI < -0.92 (extremely low trend strength)
```

**Condition #3** (BB Breakout Pullback):
```python
# Protections
- ema_fast: True
- ema_slow: True
- safe_dips: True (Level 70)
- safe_pump: True (Level 100, 36 periods)

# Core Logic
- Close > EMA200_1h * 0.986
- BB40 lower band exists
- BB40 width > close * 4.5%
- Close change > close * 2.3%
- Lower wick < BB width * 41.8%
- Close < BB40 lower band
- Close ≤ previous close
- CTI < -0.5
```

**Condition #19** (EMA Retest):
```python
# Core Logic
- Previous candle close > EMA100_1h
- Current candle low < EMA100_1h
- Current candle close > EMA100_1h (hammer/retest)
- RSI_1h > 30
- Choppiness < 21.3
- moderi_32/64/96 all True (trend up)
```

**Condition #39** (Ichimoku Trend):
```python
# Protections
- btc_1h_not_downtrend: True

# Core Logic
- Conversion Line > Baseline (Tenkan > Kijun)
- Close > Cloud top
- Leading Span A > Leading Span B (cloud up)
- Chikou Line > Cloud
- EFI > 0 (momentum up)
- SSL upper > SSL lower
- Close < SSL upper (pullback entry)
- CTI < -0.77
- Williams %R > -60
- RSI_1h rising in 12 periods
```

### 3.4 44 Buy Conditions Classification

| Category | Condition IDs | Core Logic |
|----------|--------------|------------|
| **Trend Confirmation** | 1, 9, 18, 23 | EMA alignment up, RSI pullback |
| **BB Retest** | 2, 3, 4, 5, 6, 14, 42, 43 | Price touches BB lower band then bounces |
| **SMA Deviation** | 10, 11, 12, 13, 22, 25 | Price deviates from MA, mean reversion |
| **EWO Oscillation** | 12, 13, 16, 17, 22, 29, 30, 31, 34, 36, 44 | Elder Wave Oscillator signals |
| **CTI Trend Strength** | 1, 3, 7, 8, 18, 20, 21, 26, 27, 28 | CTI extremely low for entry |
| **Williams %R** | 23, 26, 27, 38, 40, 41, 43 | Williams %R oversold signals |
| **Quick Mode** | 32, 33, 34, 35, 36 | Simplified conditions, fast entry |
| **PMax Signal** | 35, 36, 37, 38 | Profit Maximizer indicator |
| **Ichimoku** | 39 | Complete Ichimoku signals |
| **ZLEMA Cross** | 40 | Zero-lag EMA cross |
| **EMA200 Trend** | 41, 42, 43 | EMA200 sustained rise on 1h |

---

## IV. Sell Logic Details

### 4.1 Multi-Layer Profit-Taking System

**Above EMA200 (Bull Market) Profit Table**:

| Profit Range | RSI Threshold | CMF Condition | Signal Name |
|-------------|--------------|---------------|-------------|
| ≥ 20% | < 30 | — | signal_profit_o_bull_11 |
| 12%–20% | < 42 | — | signal_profit_o_bull_10 |
| 10%–12% | < 46 | — | signal_profit_o_bull_9 |
| 9%–10% | < 50 | — | signal_profit_o_bull_8 |
| 8%–9% | < 54 | — | signal_profit_o_bull_7 |
| 7%–8% | < 50 | CMF<0 | signal_profit_o_bull_6 |
| 6%–7% | < 49 | CMF<0 | signal_profit_o_bull_5 |
| 5%–6% | < 42 | CMF<0 | signal_profit_o_bull_4 |
| 4%–5% | < 37 | CMF<0 | signal_profit_o_bull_3 |
| 3%–4% | < 35 | CMF<0 | signal_profit_o_bull_2 |
| 2%–3% | < 35 | CMF<0 | signal_profit_o_bull_1 |
| 1.2%–2% | < 34 | CMF<0 | signal_profit_o_bull_0 |

**Below EMA200 (Bear Market) Profit Table**: More aggressive, allows selling at higher RSI (because rebounds can end anytime).

### 4.2 Pump Special Profit-Taking

For coins that surged significantly recently, dedicated profit logic applies:

```python
# 48h surge judgment
sell_pump_threshold_48_1 = 0.9   # 48h rise > 90%
sell_pump_threshold_48_2 = 0.7   # 48h rise > 70%
sell_pump_threshold_48_3 = 0.5   # 48h rise > 50%
```

### 4.3 Special Sell Scenarios

| Scenario | Trigger | Signal Name |
|---------|---------|------------|
| **SMA Downtrend Exit** | SMA200 falling 20 periods + 5%–12% profit | signal_profit_d_1 |
| **Below EMA100 Exit** | Close < EMA100 + 7%–16% profit | signal_profit_d_2 |
| **Trailing Stop 1** | Profit 3%–5% + RSI 10–20 + drawdown > 5% | signal_profit_t_1 |
| **Trailing Stop 2** | Profit 10%–40% + RSI 20–50 + drawdown > 3% | signal_profit_t_2 |
| **Trailing Stop 3** | Profit 6%–20% + drawdown > 5% + SMA200_1h falling | signal_profit_t_3 |
| **Recovery Exit 1** | Max loss > 12% + current profit > 6% | signal_profit_r_1 |
| **Recovery Exit 2** | Max loss > 6% + 1%–5% profit + RSI<46 | signal_profit_r_2 |
| **Pump+Drop Exit** | Pump + SMA200 falling + 0.5%–9% profit | signal_profit_p_d_1~4 |
| **Long Holding Exit** | Profit 3%–4% + holding > 900 min (15 hours) | signal_profit_l_1 |
| **Pump Fast Exit** | Pump 24h + 7%–20% profit + holding < 30 min | signal_profit_p_s_1 |

### 4.4 Smart Stop Loss (ATR Dynamic)

```python
# Loss Range         ATR Stop Threshold       Signal Name
# ----------------------------------------------------------------
# -8% ~ -12%      Price < ATR_high - 5.4*ATR  signal_stoploss_atr_1
# -12% ~ -16%     Price < ATR_high - 5.2*ATR  signal_stoploss_atr_2
# -16% ~ -20%     Price < ATR_high - 5.0*ATR  signal_stoploss_atr_3
# < -20%          Price < ATR_high - 2.0*ATR  signal_stoploss_atr_4
```

### 4.5 Base Sell Signals (8)

```python
# Sell 1: RSI Overbought + BB Breakout
- RSI_14 > 79.5
- Close > BB20 upper (6 consecutive candles)

# Sell 2: Extreme RSI + BB Breakout
- RSI_14 > 81
- Close > BB20 upper (3 consecutive candles)

# Sell 4: Dual Timeframe RSI Overbought
- RSI_14 > 73.4
- RSI_14_1h > 79.6

# Sell 6: Bearish Rebound Overbought
- Close < EMA200
- Close > EMA50
- RSI_14 > 79

# Sell 7: 1h RSI Overbought + EMA Death Cross
- RSI_14_1h > 81.7
- EMA12 crosses below EMA26

# Sell 8: 1h BB Extreme Breakout
- Close > BB20_1h upper * 1.1
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Moving Averages** | EMA 12/13/15/16/20/25/26/35/50/100/200, SMA 5/15/20/30/200 | Trend, support/resistance |
| **Bollinger Bands** | BB20-2STD, BB40-2STD | Volatility, overbought/oversold |
| **Momentum** | RSI 4/14/20, MFI, CTI | Overbought/oversold judgment |
| **Trend** | EWO, CMF, Choppiness, moderi | Trend strength, fund flow |
| **Volatility** | Williams %R 480, ATR 14 | Extreme judgment, stop loss |
| **Special** | StochRSI 96, PMax, Hull 75, ZLEMA 68, SSL Channels | Advanced signals |
| **Ichimoku** | Tenkan/Kijun/Senkou/Chikou | Trend direction |

### 5.2 1h Informative Timeframe Indicators

- EMA series: 12/15/20/25/26/35/50/100/200
- SMA200 + 20-period fall judgment
- RSI_14
- BB20-2STD
- CMF 20
- Williams %R 480
- CTI 1h
- Ichimoku complete indicators
- EFI (Elder's Force Index)
- SSL Channels

### 5.3 BTC Informative Timeframe

```python
# 1h BTC trend judgment
btc_not_downtrend_1h = ((BTC_close > BTC_close.shift(2)) | (BTC_rsi > 50))
```

---

## VI. Risk Management Features

### 6.1 Multi-Layer Protection Filters

Each buy signal must pass protection parameter checks, forming layered filtering:

1. **Trend Filters**: EMA/SMA direction confirmation
2. **Price Position Filters**: Close above specific MAs
3. **Safe Dips Filters**: Prevent catching falling knives
4. **Safe Pump Filters**: Prevent chasing after surges
5. **BTC Filters**: Some conditions require BTC not in downtrend

### 6.2 Hold Support

The strategy supports "hold for profit" via `hold-trades.json`:
```json
{"trade_ids": [1, 3, 7], "profit_ratio": 0.005}
```
Forces specified trades to only sell when they achieve target profit.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Extremely Defensive**: 44 protection groups, 13 levels of dip/pump thresholds — covers almost all market risk scenarios
2. **Signal Diversity**: 44 buy conditions covering trend-following, mean reversion, BB retest, Ichimoku, and more
3. **Fine-Grained Profit-Taking**: Graded profit-taking, trailing stop, special scenario exits — dynamically adjusts based on profit and market state
4. **Timeframe Fusion**: 5m + 1h + BTC triple confirmation
5. **Community Validated**: Most famous open-source strategy in Freqtrade ecosystem
6. **Highly Customizable**: Each condition independently toggleable

### ⚠️ Limitations

1. **Extremely High Complexity**: 4000+ lines of code, 44 buy conditions — understanding and debugging is extremely costly
2. **High Resource Requirements**: 480 candles startup, heavy indicator computation, needs good VPS
3. **Overfitting Risk**: Many parameters, risk of overfitting to historical data
4. **Backtest/Live Gap**: Complex logic performs excellently in backtest; live may differ due to slippage, delays, liquidity
5. **Steep Learning Curve**: Newcomers find strategy logic difficult to grasp

---

## VIII. Summary

**NostalgiaForInfinityV7_7_2** is a defensive trend-following strategy that pushes "complexity" to its extreme. Its core value lies in:

1. **Comprehensive Risk Control**: 44 protection groups covering almost all market risk scenarios
2. **Flexible Signal System**: 44 buy conditions providing diverse entry logic options
3. **Intelligent Profit/Loss**: Multi-layer, dynamically adjusted profit-taking system

For quantitative traders, this strategy is better used as a "reference library" than directly deployed:
- Beginners: Don't use directly — study its design philosophy
- Intermediate: Select understood condition subsets, optimize and simplify
- Advanced: Backtest optimize, but be vigilant about overfitting

**Final recommendation**: Strategy complexity is a double-edged sword. Provides extreme defensiveness but also brings overfitting risk and debugging difficulty. Before use, conduct sufficient backtesting and small-capital live verification.
