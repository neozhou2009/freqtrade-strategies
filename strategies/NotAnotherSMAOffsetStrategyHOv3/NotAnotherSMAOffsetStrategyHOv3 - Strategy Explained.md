# NotAnotherSMAOffsetStrategyHOv3: Strategy Explained

## 1. What Does This Strategy Do?

### One-Line Summary

Think of supermarket shopping — prices fluctuate around a "fair price." Buy when far below, sell when far above. The twist: it also checks "market mood" (EWO indicator) to confirm whether the "cheap" or "expensive" is real.

### Strategy Name Meaning

**NotAnotherSMAOffsetStrategyHOv3** = "Not just another SMA Offset Strategy · Auto-Optimized · Version 3"

In plain terms: "A MA offset strategy that's been fine-tuned into a machine."

---

## 2. Core Indicators in Plain English

### 2.1 MA — "Fair Price" Line

Strategy uses several MAs:
- **ma_buy**: EMA 8 candles → judges "is it cheap?"
- **ma_sell**: EMA 16 candles → judges "is it expensive?"
- **ema_100**: EMA 100 candles → major trend
- **sma_9**: SMA 9 candles → short-term trend
- **hma_50**: HMA 50 candles → mid-term trend, faster and smoother

### 2.2 EWO — "Market Momentum"

EWO = difference between two EMAs, telling if the market is "energetic" or "exhausted":
- **Positive and large**: Market rising vigorously
- **Negative and large**: Market falling hard
- **Near zero**: Momentum fading, may reverse

### 2.3 RSI — "Temperature Gauge"

- **RSI > 70**: Too hot, may cool down
- **RSI < 30**: Too cold, may warm up

Three RSIs used:
- RSI(14): Standard
- RSI(4): Extra fast
- RSI(20): Extra slow

---

## 3. When to Buy? Three Signals

### 3.1 ewo1 — Strong Trend Pullback (Most Common)

**Trigger**: Uptrend continuing, suddenly pulled back.

**Conditions**:
1. Fast RSI < 35: Short-term price fell quickly
2. Price < MA × 0.986: 1.4% below average
3. EWO > 4.179: Still a strong uptrend
4. RSI(14) < 58: Not overheated

**Plain English**: "Big trend still up, today suddenly dipped, go buy!"

### 3.2 ewo2 — Deep Pullback

**Trigger**: Price fell even deeper.

**Conditions**:
1. Fast RSI < 35
2. Price < MA × 0.944: 5.6% below average (bigger discount!)
3. EWO > -2.609: Momentum not completely dead
4. RSI(14) < 58
5. RSI(14) < 25: DOUBLE oversold confirmation

**Plain English**: "Price dropped hard, but hasn't collapsed completely — opportunity!"

### 3.3 ewolow — Market Panic

**Trigger**: Everyone panicking and selling.

**Conditions**:
1. Fast RSI < 35
2. Price < MA × 0.986: 1.4% below
3. EWO < -16.917: Extremely pessimistic

**Plain English**: "Everyone's scared, selling frantically — time to be greedy."

### Signal Comparison

| Signal | Best Scenario | Risk | Expected Return |
|--------|--------------|------|----------------|
| ewo1 | Strong trend normal pullback | Low | Stable |
| ewo2 | Deep pullback | Medium | Higher |
| ewolow | Market panic | High | Could be huge |

---

## 4. When to Sell? Two Conditions

### 4.1 Sell Set 1: Rose Enough, Get Out

**Conditions**:
1. Price > SMA 9
2. Price > ma_sell × 1.018: Above average 1.8%
3. RSI > 50
4. Fast RSI > Slow RSI: Momentum still up

**Plain English**: "Rose to the target, still trending up but — take the money and run."

### 4.2 Sell Set 2: Trend Weakening, Run

**Conditions**:
1. Price < HMA 50: Broke below mid-term trend line
2. Price > ma_sell × 1.054: Still above baseline
3. Fast RSI > Slow RSI

**Plain English**: "Trend showing signs of weakness while still profitable — protect gains!"

### 4.3 Special: Cancel Sell?

If sell signal triggered BUT:
- HMA 50 still above EMA 100 (major trend intact)
- Price fell below EMA 100's 95%

Strategy says: "NO! Don't sell — major trend fine, wait!"

---

## 5. Risk Control — Your Safety Net

### 5.1 Fixed Stop-Loss: Max 30% Loss

```python
stoploss = -0.3
```

Bought $100 → drops to $70 → forced sell. This is slightly tighter than the first version (-35%).

### 5.2 Trailing Stop: Smart Profit Locker

- Activates at 2.5% profit
- Stop follows price, 0.5% below peak
- Example: Bought $100 → $102.50 activates → $110 peak → $109.45 stop → sell at $109.45, lock 9.45%

### 5.3 ROI Targets

| Time | Target |
|------|--------|
| Start | 10% |
| 30 min | 5% |
| 60 min | 2% |

### 5.4 Slippage Protection

If execution price is 2%+ worse than expected → reject and retry (up to 3 times).

---

## 6. Parameters

### 6.1 Buy Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| base_nb_candles_buy | 8 | MA period for buying |
| low_offset | 0.986 | Buy when 1.4% below MA |
| low_offset_2 | 0.944 | Deep buy when 5.6% below MA |
| ewo_high | 4.179 | Must be above this to buy |
| ewo_low | -16.917 | Must be below this for ewolow |
| rsi_buy | 58 | RSI must be below this |

### 6.2 Sell Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| base_nb_candles_sell | 16 | MA period for selling |
| high_offset | 1.054 | Price 5.4% above MA to sell |
| high_offset_2 | 1.018 | Price 1.8% above MA to sell |

---

## 7. Best & Worst Markets

### Good Markets
- **Bull market**: ewo1 triggers often, trailing stop catches big moves
- **Ranging market**: Both ewo1 and ewo2 trigger, offset catches oscillations
- **Mild bear**: ewolow catches oversold rebounds

### Bad Markets
- **One-sided rally**: Strategy may sell too early, missing big gains
- **One-sided crash**: ewolow may catch falling knives
- **Dead quiet**: Price barely moves, no signals, fees eat profits

---

## 8. How to Use

### Step 1: Backtest
```bash
freqtrade backtesting --strategy NotAnotherSMAOffsetStrategyHOv3 --timerange 20230101-20231231 --timeframe 5m
```

### Step 2: Paper Trade
```bash
freqtrade trade --strategy NotAnotherSMAOffsetStrategyHOv3 --dry-run
```
Run at least 2 weeks.

### Step 3: Small Live
Start with money you can afford to lose. Verify:
- Signal frequency
- Actual slippage
- Performance vs backtest

### Step 4: Monitor & Adjust
- Weekly: review performance
- Monthly: re-optimize parameters if needed

---

## 9. Pros & Cons Summary

### Pros
- Clear logic: buy cheap, sell expensive
- Three signals: covers different markets
- Complete risk control
- Many adjustable parameters

### Cons
- Past-optimal parameters may not work in future
- Ranging markets = losses
- Designed to catch dips, not chase rallies
- Requires active management

---

## 10. Key Takeaway

**"Buy when price is below MA by a set percentage in a confirmed trend, sell when price rises above MA by a set percentage, with complete stop-loss and trailing protection."**

Remember: **No strategy is perfect**. Backtesting ≠ future results. Quant trading needs continuous learning, monitoring, and adjustment. Trade only with funds you can afford to lose.

*Plain English guide. For detailed technical analysis, see the formal version.*
