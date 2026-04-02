# Obelisk_3EMA_StochRSI_ATR Strategy Analysis

## Table of Contents

1. [Strategy Overview](#1-strategy-overview)
2. [Theoretical Foundation](#2-theoretical-foundation)
3. [Technical Indicator Details](#3-technical-indicator-details)
4. [Entry Signal Analysis](#4-entry-signal-analysis)
5. [Exit Mechanism Design](#5-exit-mechanism-design)
6. [Risk Management Framework](#6-risk-management-framework)
7. [Timeframe Strategy](#7-timeframe-strategy)
8. [Parameter Configuration](#8-parameter-configuration)
9. [Backtesting and Optimization](#9-backtesting-and-optimization)
10. [Live Trading Notes](#10-live-trading-notes)
11. [Summary](#11-summary)

---

## 1. Strategy Overview

### 1.1 Background

Obelisk_3EMA_StochRSI_ATR, released April 2021 by Obelisk, draws inspiration from Trade Pro's YouTube video "76% Win Rate Highly Profitable Trading Strategy." The strategy combines EMA for trend direction, StochRSI for timing, and ATR for dynamic stop-loss/take-profit sizing.

⚠️ **Important**: Code explicitly states "DO NOT RUN LIVE" — for research and backtesting only.

### 1.2 Core Philosophy

Multi-indicator synergy: EMA identifies trend, StochRSI confirms momentum turning points, ATR dynamically sizes stops. Trend-following with momentum confirmation.

### 1.3 Positioning

**Long-only** trend-following strategy. Suitable for:
- Quantitative strategy research and learning
- Backtesting analysis
- Hyperparameter optimization experiments
- Risk management mechanism study

---

## 2. Theoretical Foundation

### 2.1 Trend-Following Theory

Assumption: "Trends persist" — once a clear up/down trend forms, it likely continues for a period. Triple EMA arrangement identifies trend via multi-period MA stacking.

### 2.2 Momentum Oscillator Theory

StochRSI applies stochastic formula to RSI, providing higher sensitivity than plain RSI. Identifies momentum turning points for precise entries.

### 2.3 Volatility Measurement Theory

ATR measures true range, capturing actual market volatility. Dynamic stops adapt to volatility — wider in volatile markets, tighter in calm markets.

---

## 3. Technical Indicator Details

### 3.1 Triple EMA

- **EMA8**: Fast line, short-term momentum (N=8)
- **EMA14**: Middle line, medium-term smoothing (N=14)
- **EMA50**: Slow line, main trend filter (N=50)

EMA formula: `EMA(t) = α × Price(t) + (1-α) × EMA(t-1)`, where α = 2/(N+1)

### 3.2 Stochastic RSI

Custom implementation:
- RSI period: 14
- StochRSI period: 14
- K smoothing: 3
- D smoothing: 3

```python
df['rsi'] = ta.RSI(dataframe, timeperiod=14)
stochrsi = (rsi - rsi_min) / (rsi_max - rsi_min)
df['srsi_k'] = stochrsi.rolling(3).mean() * 100
df['srsi_d'] = df['srsi_k'].rolling(3).mean()
```

### 3.3 ATR

```python
dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
```

Stop-loss: entry - 3 × ATR
Take-profit: entry + 2 × ATR

---

## 4. Entry Signal Analysis

### 4.1 Entry Conditions

Both conditions must be true simultaneously:

**Condition 1: EMA Bullish Arrangement**
```python
(dataframe['ema8'] > dataframe['ema14']) & (dataframe['ema14'] > dataframe['ema50'])
```
EMA8 > EMA14 > EMA50 = clear uptrend.

**Condition 2: StochRSI Golden Cross**
```python
qtpylib.crossed_above(dataframe['srsi_k'], dataframe['srsi_d'])
```
K-line crosses above D-line = short-term momentum starting to strengthen.

### 4.2 Signal Generation Logic

```python
dataframe.loc[
    (ema8 > ema14) & (ema14 > ema50) &
    qtpylib.crossed_above(srsi_k, srsi_d),
    'go_long'
] = 1
```

### 4.3 Signal Filtering

Multi-confirmation: EMA arrangement filters trend, StochRSI confirms momentum — two conditions must coincide.

---

## 5. Exit Mechanism Design

### 5.1 Dynamic Stop-Loss/Take-Profit

```python
dataframe['take_profit'] = close + atr * 2
dataframe['stop_loss'] = close - atr * 3
dataframe['stop_pct'] = (atr * 3) / close
```

### 5.2 Custom Stop-Loss Function

```python
def custom_stoploss(...):
    # If current rate > take_profit → close for profit
    if current_rate > take_profit:
        return 0.001
    # Otherwise maintain stop distance from entry
    return stoploss_from_open(-stop_pct, current_profit)
```

### 5.3 Exit Signal

```python
def populate_exit_trend(...):
    dataframe['sell'] = 0
    return dataframe
```

No active exit signals — all exits through stop-loss/take-profit mechanism.

---

## 6. Risk Management Framework

### 6.1 Stop-Loss Analysis
- **Dynamic**: Based on ATR, adapts to volatility
- **Fixed ratio**: Always 3× ATR from entry
- **Upper bound**: `stoploss = -0.10` caps max loss at 10%

### 6.2 Take-Profit Analysis
- **Fixed ratio**: 2× ATR from entry
- **Fixed target**: Does not move with price

### 6.3 Risk/Reward Ratio

Assuming ATR ≈ 2% of price:
- Stop distance = 3 × 2% = 6%
- Target distance = 2 × 2% = 4%
- Risk/reward = 4%/6% ≈ 0.67

Strategy needs ≈ 60% win rate to break even.

---

## 7. Timeframe Strategy

### 7.1 Dual Timeframe Design

**Backtest timeframe**: 5 minutes
**Signal timeframe**: 1 hour (via informative pairs)

### 7.2 Rationale

5-minute backtesting: more precise price simulation, avoids "whipsaw" issues where a single candle crosses both stop and target.

1-hour signals: reduces noise, prevents overtrading.

### 7.3 Timeframe Conversion

```python
time_factor = int(60 / 5)  # = 12
```

---

## 8. Parameter Configuration

### 8.1 Core Parameters
- `startup_candle_count = 500`
- `minimal_roi = {"0": 1}` (100% — only ATR take-profit is used)
- `stoploss = -0.10`

### 8.2 Indicator Parameters
- EMA periods: 8, 14, 50
- RSI: 14
- StochRSI: 14, smoothing 3/3
- ATR: 14

---

## 9. Backtesting and Optimization

### 9.1 Recommended Backtest Setup
- Use 5m or 1m timeframe
- At least 6 months data
- Include bull, bear, and ranging periods
- Set realistic slippage (0.5%-1%)

### 9.2 Optimization Suggestions
Optimizable: EMA periods, StochRSI parameters, ATR multiples, stop-loss cap.

Avoid overfitting — use out-of-sample validation.

---

## 10. Live Trading Notes

⚠️ **Developer Warning**: "DO NOT RUN LIVE"

Limitations for live use:
- Trend-dependent: poor in ranging/volatile markets
- Lag: EMA-based indicators lag in fast reversals
- Long-only: cannot profit in downtrends

### Suggested Improvements for Live
- Add RSI filter
- Add volume confirmation
- Implement true trailing stop
- Add shorting logic

---

## 11. Summary

A structurally clean trend-following strategy demonstrating:
- EMA trend + StochRSI momentum combination
- ATR-based dynamic risk management
- Dual-timeframe implementation

⚠️ Not recommended for live trading per developer. Excellent for learning.

Key learning points: multi-indicator synergy, dynamic stops, multi-timeframe design, risk/reward balance.

---

*Strategy Author: Obelisk (brookmiles)*
*Reference: Trade Pro "76% Win Rate Strategy"*
*Disclaimer: For learning only, not investment advice.*
