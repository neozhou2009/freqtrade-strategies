# CBPete9: The "Choice Paralysis Late-Stage" Dip-Buying King

> **Nickname**: Dip-Buying King, Ten-Tonic Soup  
> **Vibe**: Supermarket sale aisle lurker  
> **Timeframe**: 5 minutes (reference 1 hour)

---

## 1. What's This Strategy All About?

Simply put, **CBPete9** is:
- A strategy that buys when prices have crashed (dip-buying professional)
- Sells slightly after making a profit (not greedy)
- Uses 10 different conditions to decide whether to buy (choice paralysis late-stage)

Like a **"supermarket sale hunter"**: spots a price drop and "bargain hunts," makes a small rebound (2–3%) and immediately exits, takes the money out and waits for the next "sale."

**Core Goal**: Not to "make big money," but to **"lose as little as possible."** The author explicitly stated: minimize drawdowns.

---

## 2. Core Settings: "Fast In, Fast Out"

### Take-Profit Rules (ROI Table)

| Holding Time | Minimum Profit Required | Plain English |
|-------------|------------------------|---------------|
| Just bought | 2.8% | Got lucky and made 2.8%? Run! |
| After 10 minutes | 1.8% | Waited 10 minutes, 1.8% will do |
| After 40 minutes | 0.5% | Dragged for 40 minutes, 0.5% and out |

**Translation**: The longer you hold, the lower the required profit. Essence: encourage "fast in, fast out," don't fall in love with positions!

### Stop-Loss Rules

```
Official stop-loss: -99% (basically nonexistent)
Trailing stop: On (activates after 1.87% profit)
Smart stop-loss: Check after 50 minutes if still losing
```

**Translation**: Official stop-loss is basically useless — what you rely on is your own "smart stop-loss" mechanism. Like your mom saying "do whatever you want," but she's actually arranged everything for you.

---

## 3. The 10 Buy Conditions: Organized by Category

This strategy's buy conditions are absurdly numerous — **10 independent conditions**, buy if ANY one is satisfied. Organized into 4 categories:

### 🎯 Category 1: Trend Confirmation Type (Conditions 1, 2, 5)

**Core Logic**: Trend is up + short-term oversold = dip-buying opportunity

**Representative Conditions**:

**Condition #1**: Dual-timeframe EMA + Bollinger Band lower band
- 5-minute price > 200-day MA (short-term trend up)
- 1-hour price > 200-day MA (long-term trend also up)
- Price broke below Bollinger Band lower band (on sale!)
- Volume contracted (washout complete)

**Condition #5**: MACD golden cross + trend confirmation
- Dual-timeframe trend up
- MACD golden cross (momentum starting to shift)
- Price oversold

---

### 📉 Category 2: RSI Oversold Type (Conditions 3, 4, 8, 9)

**Core Logic**: RSI too low = oversold = may rebound

**Representative Conditions**:

**Condition #3**: 1-hour trend protection + RSI extreme oversold
- 1-hour trend up
- RSI < 14.2 (extremely oversold)

**Condition #4**:只看1-hour RSI
- 1-hour RSI < 16.5 (1-hour level oversold)
- Nothing else matters — simple and brutal

**Condition #8**: Dual RSI oversold
- 1-hour RSI < 20
- 5-minute RSI < 28
- Both timeframes oversold simultaneously = resonance signal

---

### 🔀 Category 3: MACD Momentum Type (Conditions 6, 7)

**Core Logic**: MACD golden cross + oversold = momentum reversal

**Condition #6**: MACD strong signal
- MACD golden cross, difference large enough (strong momentum)
- Price oversold

**Condition #7**: 1-hour RSI + MACD combo
- 1-hour RSI < 15 (oversold)
- 5-minute MACD golden cross (momentum shifting)
- Dual-period coordination

---

### 🧩 Category 4: Comprehensive Combo Type (Condition 10)

**Core Logic**: Throw every usable indicator together

**Condition #10**: Comprehensive reversal signal
- SSL Channel rising (trend up)
- EMA50 > EMA200 (mid-term trend up)
- Price < SMA5 (short-term weak, perfect for buying bargains)
- 5-minute RSI lower than 1-hour RSI by 43+ (short-term oversold more severe)

---

## 4. Exit Logic: Simpler Than Entry

Sell condition is super simple:

> **Price breaks above Bollinger Band middle band 1.01× (+1%) = sell!**

That's it. Direct.

**Strategy Philosophy**: **Don't be greedy, take profits when available.** Price just bounced a bit and you immediately exit — take the money and wait for the next opportunity.

---

## 5. The Strategy's "Personality"

### ✅ Strengths

1. **Very Cautious**: 10 buy conditions, fully verified before striking
2. **Strong Discipline**: At stop-loss point, exits without hesitation
3. **Not Greedy**: Makes 1% and runs, takes what's available
4. **Hardworking**: Monitors multiple timeframe signals simultaneously
5. **Smart Stop-Loss**: Checks after 50 minutes if still losing, whether to cut

### ⚠️ Weaknesses

1. **Too Many Conditions**: 10 buy conditions — normal people can't understand them all
2. **Overly Complex**: So many conditions you can't remember them
3. **Easy to Overfit**: So many parameters, might just be "memorizing answers"
4. **High Fees**: Frequent trading, fees eat into profits
5. **High Win Rate Demanded**: Each trade earns little, must guarantee win rate

---

## 6. Summary: What's the Verdict?

### One-Line Rating

> "Conditions so many you want to curse, but the logic is still a reliable dip-buying king."

### Who's It For?
- ✅ Short-term trading enthusiasts
- ✅ People who can accept frequent operations
- ✅ People with high drawdown control requirements
- ✅ People who have time to monitor positions

### Who's It NOT For?
- ❌ People who want to lie flat and do nothing
- ❌ People who hate frequent operations
- ❌ Fee-sensitive people
- ❌ People who can't decipher 10 buy conditions

---

## 7. ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Live Trading Needs Caution

CBPete9's historical backtesting often looks **extremely impressive** — but there's a trap:

> **With so many parameters, the strategy easily "fits" the best solutions for past market conditions — but that doesn't mean it will definitely profit in the future.**

### My Advice (Genuinely)

```
1. Must paper trade first (dry_run), at least 2–4 weeks
2. Start with small capital in live trading, scale up only after confirming stability
3. Choose major coins (BTC, ETH), good liquidity
4. Watch stop-loss trigger frequency, frequent triggers = market not suitable
5. Don't randomly tune parameters — author says default settings work
```

**Remember**: Strategy再好, 市场教做人时也不会打招呼. Test with small positions — survival is what matters! 🙏

---

**Final Reminder**: 10 buy conditions sound impressive but also mean possible overfitting. Don't be fooled by complex logic — the market is always right. Respect it, control risk! 🙏
