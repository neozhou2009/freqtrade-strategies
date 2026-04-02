# SampleStrategy: The "Player" of Quant Trading - The Crazy World of 26 Buy Conditions

> **Nickname**: Chronic Indecision Sufferer  
> **Occupation**: Trend Following Specialist + Multi-layer Defense Master  
> **Timeframe**: 5-minute main battlefield + 1-hour intelligence agency

---

## I. What is This Strategy?

Simply put, **SampleStrategy** is:
- 26 buy conditions (is that a lot or what?)
- 8 sell conditions + custom_sell dynamic take-profit
- Each buy condition has independent protection parameter groups
- Multi-timeframe verification (5m + 1h)

Like a cautious investor who wants to check three generations of family history before a date, every entry must pass through layers of scrutiny 🤣

---

## II. Core Configuration: "Layer upon Layer of Insurance"

### Take-Profit Rules (ROI Table)

```
Just bought → Run at 10% profit
After 30 min → Run at 5% profit
After 60 min → Run at 2% profit
```

**Translation**: Time is the enemy of money. The longer you hold, the lower your profit target. This isn't greed - it's preventing profit giveback.

### Stop-Loss Rules

```
Fixed stop loss: -10%
Trailing stop: Activates after 3% profit, locks profit at 1% pullback
```

**Translation**: Lose 10% and accept it. After making 3%, start protecting profits. Don't let the cooked duck fly away.

---

## III. 26 Buy Conditions: I've Categorized Them For You

This strategy's buy conditions are frighteningly many. I've grouped them into 6 categories:

### 🎯 Category 1: Trend Confirmation (Conditions 1-5)
**Core Logic**: EMA/SMA trend upward + protection filtering

**Plain English**:
> "Only enter when the trend is good. Don't catch falling knives."

**Representative Condition**: #1

**Classic Lines**:
- Condition #1: EMA fast > EMA200 + SMA200 rising + Safe Dip + Safe Pump → "The market is going up, but let me check if there's a crash or surge first"

---

### 📊 Category 2: RSI+MFI (Conditions 6-8)
**Core Logic**: RSI oversold area + money flow verification

**Plain English**:
> "Others are fearful, I'm greedy. But first let me see if money is flowing in."

**Representative Condition**: #6

**Classic Lines**:
- Condition #6: RSI low + EMA slow confirmation + Safe protection → "RSI says buy, but hold on, let me check for traps first"

---

### 📉 Category 3: Bollinger Band (Conditions 9-12)
**Core Logic**: Price touches BB lower band + RSI verification

**Plain English**:
> "Price broke below the Bollinger band, might be an oversold rebound opportunity."

**Representative Condition**: #9

**Classic Lines**:
- Condition #9: MA deviation + BB deviation + 1h RSI range → "Price deviated too much from MA, BB says oversold too. Let's see if we can catch a bargain"

---

### 🌀 Category 4: EWO (Conditions 13, 16, 17)
**Core Logic**: Elliott Wave Oscillator signals

**Plain English**:
> "Wave theory signals, trying to catch the rhythm of fluctuations."

**Classic Lines**:
- Condition #13: MA deviation + EWO negative value → "Waves say buy, but MA deviation is the hard indicator"

---

### 🔀 Category 5: Composite (Conditions 14-24, 26)
**Core Logic**: Multi-indicator combination verification

**Plain English**:
> "Not satisfied with a single condition? Let's combine them!"

**Representative Condition**: #14

**Classic Lines**:
- Condition #14: EMA deviation + BB deviation + SMA200 rising confirmation → "Multiple verifications, layers of checkpoints"

---

### ⭐ Category 6: Special (Condition 25)
**Core Logic**: Reserved special signal conditions

---

## IV. Protection Mechanisms: 26 Layers of "Fuses"

Each buy condition comes with a set of protection parameters, like assigning a bodyguard to every entry point:

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| **EMA Fast/Slow Filter** | Check trend direction | "Don't buy on the way down" |
| **Close Above EMA** | Confirm price position | "Price must stand above the MA" |
| **SMA200 Rising** | Long-term trend confirmation | "Market direction must be right before entering" |
| **1h SMA200 Rising** | Large cycle verification | "1-hour chart must also confirm trend upward" |
| **Safe Dip** | Prevent crash entry | "Don't impulsively buy the dip during a crash" |
| **Safe Pump** | Prevent chasing highs | "Don't chase after a surge, wait for pullback" |

This strategy's protection parameters are so many it's like writing a small novel 🤣

---

## V. Sell Logic: Even More Fancy Than Buying

### 5.1 Tiered Take-Profit: Run at How Much Profit

```
Profit > 20% → Sell if RSI < 34
Profit 12-20% → Sell if RSI < 42
Profit 10-12% → Sell if RSI < 54
Profit 8-10% → Sell if RSI < 54
Profit 7-8% → Sell if RSI < 48
Profit 6-7% → Sell if RSI < 45
Profit 5-6% → Sell if RSI < 43
Profit 4-5% → Sell if RSI < 42
Profit 3-4% → Sell if RSI < 37
Profit 2-3% → Sell if RSI < 35
Profit 1-2% → Sell if RSI < 34
Profit 0-1% → Sell if RSI < 34
```

**Plain English**:
- Higher profit means lower RSI threshold → "Made enough, don't be greedy, take it home"
- Lower profit means stricter requirements → "Just started making money, don't rush to leave"

---

### 5.2 Special Exit Scenarios

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| **Below EMA200 Take-Profit** | Price below EMA200 + RSI condition | "Broke below long-term MA, retreat quickly" |
| **Post-Pump Take-Profit** | Identify 48h/36h/24h pump | "Coin that pumped, take profit if enough" |
| **SMA Declining Take-Profit** | SMA200 declining + profit range | "Market started falling, don't wait" |
| **Trailing Take-Profit** | Pullback from high | "Pulled back too much, lock profits" |

---

### 5.3 Base Sell Signals (8 Total)

**Classic Lines**:

1. **Signal #1**: `RSI > 79.5 + near BB upper band`
   > "RSI is too high, BB also says overbought, let's run"

2. **Signal #2**: `RSI > 81`
   > "RSI at 81, this is real overbought"

3. **Signal #3**: `RSI > 82`
   > "RSI at 82, even more confirmed overbought"

4. **Signal #4**: `5m RSI > 73.4 + 1h RSI > 79.6`
   > "Small and large timeframe both overbought, double confirmation"

5. **Signal #5**: `EMA deviation + RSI difference`
   > "Price deviated too much from MA, let's see what RSI says"

6. **Signal #6**: `RSI > 79`
   > "Above 79, overbought pullback confirmed"

7. **Signal #7**: `1h RSI > 81.7`
   > "1-hour RSI says overbought, large cycle signal"

8. **Signal #8**: `Price exceeds BB middle band by 110%`
   > "Bollinger band deviation too big, time to retreat"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Impenetrable Defense**: 26 protection parameter groups, almost every entry must pass inspection
2. **Flexible Combination**: Buy conditions can be individually toggled, use whichever you want
3. **Dynamic Take-Profit**: custom_sell isn't a simple ROI table, it adjusts dynamically based on profit
4. **Multi-timeframe**: 1h confirms big trend, 5m executes entry

### ⚠️ Cons (Complaint Section)

1. **Too Many Conditions**: 26 buy conditions, can barely remember them all 🤣
2. **Parameter Explosion**: Over 300 parameters, tuning is a nightmare
3. **Heavy Computation**: Needs 400 candles of startup data
4. **Overfitting Risk**: Too many parameters can easily "memorize answers"

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| **Mild Uptrend** | Enable all conditions | Good trend, multi-layer protection can catch pullbacks |
| **Oscillating Sideways** | Enable BB + RSI conditions | Use volatility boundary signals |
| **Slow Decline** | Enable strict Dip protection | Wait for deep drops before bottom fishing |
| **Fast Surge** | Enable strict Pump protection | Don't chase highs, wait for pullback |

---

## VIII. Summary: How Is This Strategy Really?

### One-sentence Review
> "Defense score: perfect. Complexity score: also perfect. Good for veterans to tune, not for newbies to go all-in."

### Who Should Use It?
- ✅ Quant veterans with Freqtrade experience
- ✅ Developers wanting to learn complex strategy architecture
- ✅ Patient investors with time to dry-run test
- ✅ Hardcore players who can handle tuning pain

### Who Shouldn't Use It?
- ❌ Complete beginners (too many parameters will make you dizzy)
- ❌ Manual traders (conditions too complex)
- ❌ Users in a hurry to go live (need thorough testing)
- ❌ Users with limited computing resources

### My Advice
1. **Dry-run first**: Don't go live right away, run dry-run for at least a week
2. **Enable conditions gradually**: Start with 5-6 buy conditions, gradually add more
3. **Focus on protection parameters**: Dip and Pump protections are key, don't disable them easily
4. **Adjust take-profit thresholds**: Tune custom_sell parameters based on market volatility

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Defense Net" with Complexity

SampleStrategy has over 1500 lines of code. What does that mean? Equivalent to writing a small quant novel 📚

**Its Money-Making Philosophy**: Better to miss than to make mistakes

- **Multi-layer Protection**: 26 parameter groups like 26 security checkpoints, direct rejection if not qualified
- **Dynamic Take-Profit**: Lock profits when you have enough, don't be greedy
- **Multi-timeframe**: 1h sees the big picture, 5m catches entries

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Mild Uptrend | ⭐⭐⭐⭐⭐ | Trend upward, multi-layer protection effectively catches pullback entries |
| 🔄 Oscillating Sideways | ⭐⭐⭐☆☆ | BB+RSI can catch fluctuations, but maybe too many signals |
| 📉 Slow Decline | ⭐⭐☆☆☆ | Dip protection works, but stop losses will be frequent |
| ⚡ Fast Surge | ⭐☆☆☆☆ | Pump protection too strict, missing opportunities |

**One-sentence Summary**: Suitable for mild trend markets, not for extreme conditions.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Note |
|--------------------|-------------------|------|
| Number of Trading Pairs | 40-80 pairs | Official recommendation, don't be greedy |
| Parallel Trades | 4-6 | Balance risk diversification and capital utilization |
| Timeframe | 5m (fixed) | This strategy's timeframe cannot be changed! |

### 10.2 Key Config File Settings

```yaml
use_sell_signal: true
sell_profit_only: false
ignore_roi_if_buy_signal: true
```

These are officially recommended settings, don't change them randomly!

### 10.3 Hardware Requirements (Important!)

This strategy has huge computation, has requirements for VPS memory:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 20-40 | 4GB | 8GB | Normal |
| 40-80 | 8GB | 16GB | Smooth |

**Warning**: Not enough memory may cause calculation timeouts, missing signals 😅

### 10.4 Backtest vs Real Trading

Complex strategies often look "too good" in backtests - because with many parameters, it's easy to find historical optimal solutions, but that doesn't mean they'll work in the future.

**Recommended Process**:
1. Read the code first, understand the logic
2. Run dry-run for at least a week
3. Enable buy conditions gradually, observe signal quality
4. Test with small position in live trading
5. Adjust parameters based on results

**Don't go all-in from the start**. No matter how good the strategy is, it needs to be broken in!

---

## XI. Bonus: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Dip Protection 12-Level Design**: From 10 to 110, strict to loose steps
   > "Crash entries need to be graded, can't一刀切 (one size fits all)"

2. **Pump Protection Time Windows**: 24h, 36h, 48h three types
   > "Pump judgment needs to look at time span, short-term and long-term pumps are different"

3. **custom_sell Profit Tiers**: 0-20% divided into 12 levels
   > "The more profit, the more conservative. Don't be greedy when you've made enough"

---

## XII. Final Words

### One-sentence Review
> "Defense: perfect. Complexity: perfect. Good for experienced quant players to deeply tune."

### Who Should Use It?
- ✅ Freqtrade veterans
- ✅ Strategy developer learners
- ✅ Users with patience to dry-run test
- ✅ Hardcore players who can handle tuning pain

### Who Shouldn't Use It?
- ❌ Complete beginners
- ❌ Manual traders
- ❌ Users in a hurry to go live
- ❌ Users with limited resources

### Manual Trader Advice
Manual trading with this strategy? Forget it. 26 buy conditions, each with protection parameters. You'll be exhausted watching the charts manually. Let the bot run itself.

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Backtests Are Beautiful, Live Trading Be Careful

SampleStrategy's historical backtest performance is often **extremely excellent** - but this has a trap:

> **Because there are so many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but that doesn't mean it will definitely profit in the future.**

Simply put: **A student who memorizes answers tests well, but doesn't necessarily understand.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Signal Delay**: Heavy computation may miss optimal entry points
- **Slippage Amplification**: Limit orders may fail due to market volatility
- **Maintenance Difficulty**: Too many parameters, hard to troubleshoot when problems occur

### My Advice (Heartfelt)

```
1. Dry-run for at least a week, observe signal quality
2. Enable buy conditions gradually (start with 5-6)
3. Focus on Dip and Pump protection parameters
4. Test with small positions (don't go all-in)
5. Adjust based on actual performance, don't blindly trust backtests
```

**Remember**: No matter how good the strategy is, when the market teaches you a lesson, it won't give advance notice. Test with small positions, staying alive is most important! 🙏

---

**Final Reminder**: This strategy is good for learning complex strategy architecture, but live trading needs thorough testing and experience. Newbies please be cautious!