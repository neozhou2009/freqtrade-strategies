# NostalgiaForInfinityX2 — Strategy Analysis

> **Strategy ID**: #310 (out of 465 strategies)  
> **Strategy Type**: Multi-Timeframe Trend Following + Dynamic Profit-Taking System  
> **Timeframe**: 5 minutes (5m) + Informative (15m/1h/4h/1d)

---

## I. Strategy Overview

NostalgiaForInfinityX2 is a strategy from the iterativ team, utilizing five different time dimensions for technical analysis. It uses RSI oversold conditions to capture entry timing and implements a unique 26-level dynamic profit-taking mechanism for profit protection.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 main signal group with dual-timeframe trend + RSI oversold |
| **Sell Conditions** | 8 base sell + 26-level dynamic profit-taking + emergency stop loss |
| **Protection** | BTC market awareness, slippage protection, trade confirmation, trailing stop |
| **Timeframe** | Main: 5m + Informative: 15m/1h/4h/1d |
| **BTC Correlation** | Independent BTC data (5 timeframes) |
| **Dependencies** | talib, qtpylib, numpy, pandas |

### Design Philosophy

1. **Trend Priority**: Only trade in confirmed trend directions, avoid counter-trend risk
2. **Oversold Entry**: Wait for pullbacks to oversold territory before entering
3. **Profit-Aware Exit**: Dynamically adjust exit conditions based on accumulated profit
4. **Multi-Dimensional Risk Control**: Fixed stop, trailing stop, dynamic exit, slippage protection

---

## II. Buy Condition Details

### The Only Entry: Multi-Timeframe Uptrend + RSI Oversold

```python
# Condition 1 - Long Mode Bull (Uptrend)

# Dual-Timeframe Trend Confirmation
dataframe['sma_50'] > dataframe['sma_200']         # 5m: SMA50 > SMA200
dataframe['sma_50_1h'] > dataframe['sma_200_1h'] # 1h: SMA50 > SMA200

# Oversold Entry
dataframe['rsi_14'] < 30.0

# Data Validity
dataframe['volume'] > 0
```

**Logic**: Both 5m and 1h SMAs must show golden cross (SMA50 > SMA200), AND RSI must drop below 30.

**Design Advantages**:
- Dual timeframe verification prevents false signals from 5m alone
- RSI < 30 in confirmed uptrend = optimal pullback entry price
- Only enters in clear uptrends — avoids counter-trend trades

### Slippage Protection

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, ...):
    slippage = (rate / dataframe['close']) - 1.0
    if slippage >= 0.038:  # 3.8% threshold
        return False  # Cancel trade
    return True
```

Slippage > 3.8% = trade cancelled. Prevents entry during extreme volatility or low liquidity.

---

## III. Sell Logic (The Real Innovation)

### 26-Level Dynamic Profit-Taking System

**Above SMA200_1h (Strong Market)**:

| Profit Range | RSI Threshold | Signal Name |
|-------------|--------------|------------|
| 0.1%–1% | < 26 | sell_long_bull_o_0 |
| 1%–2% | < 30 | sell_long_bull_o_1 |
| 2%–3% | < 32 | sell_long_bull_o_2 |
| 3%–4% | < 34 | sell_long_bull_o_3 |
| 4%–5% | < 36 | sell_long_bull_o_4 |
| 5%–6% | < 38 | sell_long_bull_o_5 |
| 6%–7% | < 40 | sell_long_bull_o_6 |
| 7%–8% | < 42 | sell_long_bull_o_7 |
| 8%–9% | < 44 | sell_long_bull_o_8 |
| 9%–10% | < 46 | sell_long_bull_o_9 |
| 10%–12% | < 48 | sell_long_bull_o_10 |
| 12%–20% | < 46 | sell_long_bull_o_11 |
| >20% | < 44 | sell_long_bull_o_12 |

**Below SMA200_1h (Weak Market)**:

| Profit Range | RSI Threshold | Signal Name |
|-------------|--------------|------------|
| 0.1%–1% | < 28 | sell_long_bull_u_0 |
| 1%–2% | < 32 | sell_long_bull_u_1 |
| 10%–12% | < 50 | sell_long_bull_u_10 |
| >20% | < 46 | sell_long_bull_u_12 |

**Design Philosophy**:
1. **Profit Tier Progression**: 0.1%–20%+ divided into 13 fine-grained tiers
2. **RSI Threshold Escalation**: Profit up → RSI exit threshold rises (26→48), more willing to hold
3. **Market Self-Adaptation**: Below SMA200_1h → slightly higher RSI thresholds (more conservative)
4. **High-Profit Fast Exit**: >12% profit → RSI threshold decreases (46→44), faster profit locking

### Base Sell Signals (8)

| Signal | Trigger | Interpretation |
|--------|---------|---------------|
| #1 | RSI > 78 + 5 candles > BB upper | Extreme overbought + sustained breakout |
| #2 | RSI > 79 + 3 candles > BB upper | Slightly earlier extreme signal |
| #3 | RSI > 81 | Pure RSI overbought — no questions asked |
| #4 | 5m RSI > 77 AND 1h RSI > 77 | Multi-timeframe resonance overbought |
| #6 | Close < EMA200, > EMA50, RSI > 78.5 | Trend reversal warning |
| #7 | 1h RSI > 79 AND EMA12 crosses below EMA26 | Death cross + overbought |
| #8 | Close > 1h BB upper × 1.07 | Extreme price deviation |

### Emergency Stop Loss

```python
if current_profit < -0.05:  # Loss exceeds 5%
    return 'sell_long_bull_stoploss_doom'
```

Before the -10% hard stop, a -5% warning stop activates. Half the loss of the hard stop — strategic early exit.

---

## IV. Technical Indicator System

### Core Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| RSI | 14 | Overbought/oversold, dynamic exit thresholds |
| EMA | 12/26/50/200 | Trend direction, golden/death cross |
| SMA | 50/200 | Trend filtering (buy condition) |
| Bollinger Bands | 20, 2STD | Price deviation, extreme identification |
| Williams %R | 14/480 | Overbought/oversold auxiliary |

### Multi-Timeframe Data

| Timeframe | Indicators |
|-----------|------------|
| 15m | RSI |
| 1h | RSI, SMA 50/100/200, BB, Williams %R |
| 4h | RSI, SMA 200, Williams %R |
| 1d | RSI |
| BTC (5m/15m/1h/4h/1d) | RSI, SMA 200, not_downtrend state |

**Note**: BTC data is computed but not used in current buy/sell conditions — available for future expansion.

---

## V. Risk Management Features

### Multi-Dimensional Trend Confirmation

Only triggers buy when BOTH:
- 5m SMA50 > SMA200 (short-term uptrend)
- 1h SMA50 > SMA200 (medium-term uptrend)

### 4-Layer Stop Protection

| Protection | Trigger | Purpose |
|-----------|---------|---------|
| Emergency Stop | -5% loss | Early warning exit |
| Hard Stop | -10% loss | Last resort |
| Trailing Stop | 3% profit + 1% drawdown | Lock profits |
| Dynamic Exit | Profit + RSI conditions | Adaptive exit |

### Slippage Protection

3.8% slippage threshold prevents entry during extreme volatility.

---

## VI. Strategy Pros & Cons

### ✅ Advantages

1. **Multi-Timeframe Synergy**: 5m/15m/1h/4h/1d + BTC — comprehensive market view
2. **Dynamic Exit Innovation**: 26-level profit-aware exit system — biggest innovation
3. **Multi-Dimensional Risk Control**: 4 layers — hard stop, trailing, dynamic, slippage
4. **Calculation Efficiency**: process_only_new_candles = True reduces unnecessary computation
5. **Clear Code Structure**: Timeframe modules clearly organized

### ⚠️ Limitations

1. **Single Buy Condition**: Only 1 buy signal group — entry opportunities relatively limited
2. **Underutilized Information**: BTC data and multi-timeframe indicators computed but not all used
3. **Trend Dependence**: Core buy depends on SMA golden cross — may underperform in choppy markets
4. **High Resource Needs**: Multi-timeframe indicators require good hardware
5. **Backtest Age Filter**: bt_min_age_days = 3 excludes some valid pairs

---

## VII. Summary

NostalgiaForInfinityX2 is a meticulously designed trend-following strategy. Its core value:

1. **Multi-Timeframe Verification**: Dual SMA verification ensures trend-following trading
2. **Dynamic Profit-Taking Innovation**: 26-level system adapts to market state via RSI
3. **Complete Risk Control**: Trailing stop + dynamic exit + emergency stop + slippage protection

For quantitative traders, the dynamic profit-taking design is most worth studying — combining profit level and market state (RSI) for adaptive exits can be applied across various strategy types.

Recommended usage: Use as reference framework for strategy development, or start with small capital testing. Entry opportunities are fewer but signal quality is higher due to strict trend requirements.
