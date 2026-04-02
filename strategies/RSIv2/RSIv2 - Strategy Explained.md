# RSIv2 Strategy: The Dual-Indicator Bottom-Fishing Tool

> **Nickname**: Oversold Rebound Little Helper  
> **Occupation**: Professional bottom-fisher, specializes in buying badly beaten-down coins  
> **Timeframe**: 15 Minutes (buy) + 30 Minutes (sell)

---

## I. What is This Strategy?

Simply put, **RSIv2** is a strategy that:
- Specializes in "bottom-fishing"
- Uses two indicators (RSI + Williams %R) together to judge
- Buys when things fall hard, sells when they rally hard

Like going to the supermarket for bargains 🛒: Only strikes when items drop to "cabbage prices" (oversold), then sells when they return to normal prices (overbought)!

---

## II. Core Configuration: "Make 1% and Run"

### Take-Profit Rules (ROI Table)

```
Profit ≥ 1% → Sell immediately
```

**Translation**: This strategy is super "impatient"—just 1% profit and it wants to run! Like those short-term traders who "take a bite and dash" 🏃

### Stop-Loss Rules

```
Fixed stop-loss: Cut at 10% loss
Trailing stop: Activates after 1% profit, triggers on 2% pullback
```

**Translation**:
- Admit defeat at 10% loss, don't stubbornly hold
- After making money, if price starts dropping 2%, immediately run to protect profits

---

## III. One Buy Condition: Simple and Direct

This strategy's buy condition is **extremely simple**, just one rule, but requires "double insurance":

### 🎯 The Only Buy Condition: Dual-Indicator Dual-Period Confirmation

**Core Logic**: Both RSI and Williams %R must **simultaneously** say "oversold!", and it must be **two consecutive candles** saying it!

**Plain English**:
> "I need to see RSI below 30 (oversold zone), AND Williams %R below -80 (deep oversold), AND this situation needs to persist for two consecutive candles before I'll buy!"

**Condition Checklist**:

| Condition | Threshold | Plain English |
|-----------|-----------|----------------|
| Current RSI | < 30 | Oversold! |
| Current Williams %R | < -80 | Really oversold! |
| Previous RSI | < 30 | Previous one also oversold |
| Previous Williams %R | < -80 | Previous one also really oversold |

Translation to human: **"Bro, this coin got crushed, and it's been crushed for two consecutive candles, it's probably really bottomed. Time to bottom-fish!"** 🎣

---

## IV. Protection Mechanism: 3-Layer "Fuse"

This strategy has three layers of stop-loss protection, like three fuses:

| Fuse | Trigger Condition | Plain English |
|------|-------------------|---------------|
| ROI Take-Profit | Make 1% | "Made a little, run! Lock it in!" |
| Trailing Stop | Pullback 2% after making 1% | "Profits are shrinking, run!" |
| Fixed Stop-Loss | Lose 10% | "Give up, cut losses!" |

This design is pretty practical: **If you can profit, run; if not, stop-loss; never overstay!** 🤣

---

## V. Sell Logic: Using Higher Timeframe for Judgment

### 5.1 Single Sell Signal

**Feature**: Selling uses **30-minute timeframe** data!

**Plain English**:
- Buy looks at 15 minutes (fast)
- Sell looks at 30 minutes (steady)

This is called "fast in, slow out"—using a more stable timeframe to judge when to leave.

**Sell Conditions**:

| Condition | Threshold | Plain English |
|-----------|-----------|----------------|
| 30-minute RSI | > 70 | Overbought! |
| 30-minute Williams %R | > -20 | Really overbought! |
| Previous 30-minute RSI | > 70 | Previous one also overbought |
| Previous 30-minute Williams %R | > -20 | Previous one also really overbought |

Translation to human: **"Rally is too hot, two consecutive 30-minute candles both say overbought, time to get out!"** 🏃💨

---

## VI. This Strategy's "Personality"

### ✅ Strengths (The Praise)

1. **Simple Logic**: Just two indicators, one buy one sell, elementary schoolers can understand
2. **Dual Confirmation**: Two indicators must both say "go" before buying, harder to get fooled
3. **Consecutive Verification**: Two consecutive candles must confirm, more stable
4. **Fast In, Slow Out**: 15-minute buy, 30-minute sell, clear thinking
5. **Controllable Risk**: Three layers of stop-loss protection, won't lose too much

### ⚠️ Weaknesses (The Criticism)

1. **Few Signals**: Just one buy condition, might go days without signals
2. **Range-bound Markets Might Get Slapped Repeatedly**: In sideways markets, overbought/oversold signals are too frequent
3. **Bottom-Fishing Has Risks**: In downtrends, oversold might be followed by more oversold 😅
4. **Hardcoded Parameters**: RSI period 14, thresholds 30/70 are hardcoded, can't change
5. **No Trend Judgment**: Doesn't care if big trend is up or down, just knows "fell hard, buy"

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------| ------- |
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ Perfect | Buy on dips, sell on rebounds, steady profits |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐☆ Okay | Bottom-fish and top-sell within range |
| 📉 One-way Downtrend | ⭐☆☆☆☆ Don't use | Oversold might get more oversold, lose more the more you bottom-fish |
| ⚡ Rapid Rally | ⭐⭐☆☆☆ Mediocre | Can't buy in, because oversold won't happen |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "Simple and crude oversold rebound strategy, good for range-bound markets, not for trending markets."

### Who Should Use It?
- ✅ Beginners learning quantitative trading (code is simple and easy to understand)
- ✅ Range-bound market players (like bottom-fishing and top-selling)
- ✅ Short-term enthusiasts (pursuing fast in, fast out)
- ✅ Risk-averse (multiple stop-loss protections)

### Who Shouldn't Use It?
- ❌ Trend followers (this strategy is counter-trend)
- ❌ High-frequency traders (too few signals)
- ❌ One-way downtrend markets (the more you bottom-fish, the more you lose)
- ❌ Get-rich-quick dreamers (1% profit then run)

### My Recommendations
1. **Backtest First**: Run backtests on target coins, see how it performs
2. **Pick the Right Coins**: Choose major coins with regular volatility, not meme coins
3. **Control Position Size**: Don't go all-in, this strategy has risks
4. **Match with Trend**: Best to bottom-fish when big trend is upward

---

## IX. In What Market Can This Strategy Make Money?

### 9.1 Core Logic: Bottom-Fishing Takes Skill

RSIv2 is a classic **"bottom-fishing school"** strategy. Only about 80 lines of code—what does that mean? About the length of a high school essay! 📝

**Its Money-Making Philosophy**:
- Fell hard → Pick up cheap
- Rallied hard → Sell fast

**Three Key Points**:
- **Dual Indicator Verification**: RSI and Williams %R both say "bottomed" before buying
- **Consecutive Confirmation**: Two consecutive candles must confirm, preventing false signals
- **Fast In, Slow Out**: 15-minute buy, 30-minute sell

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:---------------------------|
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ | Bottom-fish on bull market pullbacks, perfect! |
| 🔄 Range-Bound Oscillation | ⭐⭐⭐⭐☆ | Bottom-fish and top-sell back and forth, make small money |
| 📉 One-way Downtrend | ⭐☆☆☆☆ | Bottom-fishing halfway up the mountain, brutal! |
| ⚡️ Rapid Rally | ⭐⭐☆☆☆ | No chance to buy, just watching |

**One-Sentence Summary**: **Range-bound markets are heaven, trending markets are hell.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Side Note |
|-------------------|-------------------|-----------|
| Trading pairs | Major coins (BTC/ETH) | Don't pick meme coins, liquidity too poor |
| Timeframe | 15m | Default is fine, no need to change |
| Startup candles | 20 | Strategy default value |

### 10.2 Hardware Requirements (Important!)

This strategy has **very small** computational load, basically doesn't need much:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|--------------------| ----------- |
| 1-5 pairs | 1GB | 2GB | Smooth as silk |
| 5-20 pairs | 2GB | 4GB | No problem |
| 20+ pairs | 4GB | 8GB | Easy peasy |

**Side Note**: If you can't even run this strategy, time to get a new computer 😂

### 10.3 Backtest vs Live Trading

**Backtesting is Beautiful**, but be careful in live trading:
- In backtests, oversold rebounds look perfect
- In live trading, slippage, latency, and liquidity all eat into profits
- Especially that 1% profit target, actual might only be 0.8%

**Recommended Process**:
1. Backtest first, see if strategy logic is correct
2. Then paper trade for a few weeks, see actual performance
3. Small position live trading, verify real results
4. Confirm it works before increasing position

**Don't go all-in right away**—no matter how good the strategy, it needs testing!

---

## XI. Easter Egg: The Strategy Author's "Little Quirks"

Looking carefully at the code, you'll find some interesting things:

1. **Asymmetric Timeframe**: Buy uses 15m, sell uses 30m
   > "I want to buy fast, sell slow~"

2. **Strict Oversold Threshold**: Williams %R must be < -80, stricter than the standard -50
   > "Not just regular drops, it must be crushed extra hard before I buy!"

3. **Trailing Stop Design**: Activates at 1% profit, triggers on 2% pullback
   > "Made a little and start getting nervous, drop a little and want to run~"

---

## XII. The Very Last Bit

### One-Sentence Review
> "Simple but not simplistic bottom-fishing strategy, a good friend in range-bound markets."

### Who Should Use It?
- ✅ Quantitative beginners (code is easy to understand)
- ✅ Range-bound market players (bottom-fish and top-sell)
- ✅ Conservative types (multiple stop-losses)
- ✅ Short-term enthusiasts (fast in, fast out)

### Who Shouldn't Use It?
- ❌ Trend followers
- ❌ Get-rich-quick dreamers
- ❌ One-way downtrend markets
- ❌ Meme coin players

### For Manual Traders
If you don't want to run a bot and want to use this strategy's concepts for manual trading:
- Open TradingView, add RSI(14) and Williams %R(14)
- Wait for RSI < 30 AND Williams %R < -80
- Two consecutive candles both confirm before buying
- Set trailing stop, protect profits

---

## XIII. ⚠️ Risk Re-emphasis (Read This Section!)

### Backtesting is Beautiful, Live Trading Be Careful

RSIv2's historical backtest performance might be **pretty good**—but there's a trap:

> **Oversold rebound strategies easily find "success stories" in historical data, but in live trading, oversold conditions may persist longer.**

Simply put: **You bottom-fished halfway up the mountain, there's still the foot below.** 😅

### Hidden Risks of Simple Strategies

In live trading, simple strategies may encounter:
- **Slippage Risk**: 1% profit target might get half eaten by slippage
- **Delay Risk**: From signal to order execution, price might have changed
- **Liquidity Risk**: Small-cap coins might not have buyers or sellers

### My Recommendations (Real Talk)

```
1. Choose liquid major coins (BTC/ETH)
2. Backtest is just reference, paper trading is the real thing
3. Control position size, don't go all-in
4. If losing consecutively, stop and check market conditions
```

**Remember**: Bottom-fishing is a skill, not gambling. In downtrends, the cheapest can always get cheaper!

---

**Final Reminder**: No matter how good the strategy, when the market teaches you a lesson, it doesn't warn you first. Test with small positions, staying alive is what matters! 🙏