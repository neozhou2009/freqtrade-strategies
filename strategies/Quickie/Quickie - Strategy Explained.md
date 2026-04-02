# Quickie Strategy: The Fast-Handed Sniper

> **Nickname**: Fast-Handed Sniper  
> **Occupation**: Momentum Quick-Shot Specialist, catching short-term bounces  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **Quickie** is:
- Only 1 buy signal, 1 sell signal
- Specifically catches bounces in downtrends
- Makes money and runs, never overstays

Like a **short-term sniper**—take aim, shoot, and retreat 🎯

---

## II. Core Configuration: "Get In Fast, Get Out Fast"

### Profit-taking Rules (ROI Table)

```
10 minutes → 15% profit and run
15 minutes → 6% profit and run
30 minutes → 3% profit and run
100 minutes → 1% profit, still run
```

**Translation**: Shorter time, bigger appetite; longer holding, lower target. Simply put: **"Run fast, don't dawdle."**

### Stop-loss Rule

```
Lose 25% before stopping
```

**Translation**: Stop-loss is set pretty wide, giving price enough "breathing room." But it also means—when you lose, it really hurts 😅

---

## III. One Buy Condition: Four Checkpoints Must All Pass

This strategy has only one buy condition, but sets up **four checkpoints**—all must be satisfied:

### 🎯 Buy Signal: Four-in-One

| Checkpoint | Condition | Plain English |
|------------|-----------|----------------|
| Check 1 | ADX > 30 | Market has a clear trend, not random oscillation |
| Check 2 | TEMA < Bollinger middle band | Price at relative low |
| Check 3 | TEMA starts rising | Momentum starting to go up |
| Check 4 | Close price < 200-day SMA | Long-term trend down, "buying the dip" |

**Plain English Translation**:
> "Market has a clear trend (ADX > 30), but price is at relative low (below Bollinger middle band), and momentum is starting to go up (TEMA rising), while price is below 200-day SMA—**this is the time to buy the dip!**"

**In One Sentence**: **Catching short-term bounces in downtrends** 📈

---

## IV. Sell Condition: Three Checkpoints to Retreat

### 📉 Sell Signal: Three-in-One

| Checkpoint | Condition | Plain English |
|------------|-----------|----------------|
| Check 1 | ADX > 70 | Trend strong to extreme (might reverse) |
| Check 2 | TEMA > Bollinger middle band | Price at relative high |
| Check 3 | TEMA starts declining | Momentum starting to go down |

**Plain English Translation**:
> "Trend is extremely strong (ADX > 70), price is above Bollinger band, momentum starting to go down—**time to run!**"

**In One Sentence**: **Lock in profits when momentum peaks** 💰

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Super Simple Logic**: One buy, one sell, no纠结 about which to choose
2. **Solid Trend Confirmation**: ADX filters out most false signals in ranging markets
3. **Quick Profit-taking**: Tiered ROI keeps you from being greedy—make money and run
4. **Multi-dimensional Filtering**: Trend + momentum + position, triple confirmation before shooting

### ⚠️ Cons (Complaint Time)

1. **Stop-loss Too Wide**: 25% stop-loss, losing really hurts 😅
2. **No Trailing Stop**: Can't lock in floating profits, might gain 20% then lose it all
3. **Counter-trend Buy Risk**: Buying dips in downtrend is "catching a falling knife"
4. **ADX > 70 Sell Might Be Too Early**: Strong trends might get even stronger

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Moderate Uptrend | ✅ Recommended | Perfect match for strategy logic |
| Bounce in Downtrend | ✅ Suitable | This is the strategy's home turf |
| Range-bound Consolidation | ⚠️ Not Recommended | Few signals, easy to get slapped |
| Extreme Pump/Dump | ❌ Don't Use | ADX sell signal might be too early |

---

## VII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A clean and efficient short-term bounce strategy, clear logic, good for learning and modifying."

### Who Should Use It?
- ✅ Beginners: Simple logic, easy to understand
- ✅ Short-term Lovers: 5-minute timeframe, in and out fast
- ✅ Strategy Development Learners: Small codebase, good for beginners
- ✅ Bounce Traders: Counter-trend buy logic

### Who Shouldn't Use It?
- ❌ Conservative Traders: 25% stop-loss too wide
- ❌ Long-term Investors: Holding period too short
- ❌ Trailing Stop Wanters: Strategy doesn't have this feature
- ❌ Range-bound Market Traders: Few signals, low efficiency

### My Recommendations
1. **Backtest First, Then Live**: Tiered ROI looks good in backtests, live might differ
2. **Consider Tightening Stop-loss**: -25% can be changed to -15% or -20%
3. **Can Add Trailing Stop**: Lock in floating profits
4. **Don't Use in Range-bound Markets**: ADX > 30 doesn't mean much there

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Catch Bounces in Downtrends

Quickie's money-making philosophy:
> **"Market drops are temporary, bounces always come—I just enter when the bounce starts, make money and run."**

- **Trend Filter**: ADX > 30 ensures entry only when there's a trend
- **Momentum Confirmation**: Rising TEMA confirms bounce has started
- **Position Judgment**: Below Bollinger middle band = relative low = cheap
- **Long-term Trend Hedge**: Close < 200-day SMA = indeed in downtrend

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Moderate Uptrend | ⭐⭐⭐⭐⭐ | ADX > 30 with rising price, perfect! |
| 📉 Bounce in Downtrend | ⭐⭐⭐⭐☆ | Strategy designed for this, can catch bounces |
| 🔄 Range-bound Consolidation | ⭐⭐☆☆☆ | ADX consistently < 30, basically no signals |
| ⚡️ Extreme Pump | ⭐⭐☆☆☆ | Sells at ADX > 70, might miss big moves |

**One Sentence Summary**: **Performs best in markets with "clear trend but price at relative low."**

---

## IX. Want to Run This Strategy? Check These Configs First

### 9.1 Trading Pair Configuration

| Config Item | Recommended Value | Note |
|-------------|------------------|-------|
| Timeframe | 5m | Don't change, strategy designed for short-term |
| Stop-loss | -0.15 ~ -0.20 | Default -0.25 is too wide |
| ADX Threshold | 25~30 | Can lower a bit to increase signals |

### 9.2 Key Config File Settings

```yaml
# Recommended configuration
timeframe: '5m'
stoploss: -0.18  # Tighten a bit

# If you want more signals, can lower ADX threshold
# But need to modify code: change (dataframe['adx'] > 30) to > 25
```

### 9.3 Hardware Requirements (Not Critical)

This strategy has minimal computation, any computer can run it:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | No problem |
| 50+ pairs | 8GB | 16GB | Solid |

**Warning**: Strategy simplicity is a pro, but don't get greedy with too many pairs 😅

### 9.4 Backtest vs Live

- **Backtest Looks Beautiful**: Tiered ROI makes curves look nice
- **Live Might Be Different**: Quick profit-taking might miss big moves

**Recommended Flow**:
1. Backtest with default config first
2. Try tightening stop-loss
3. Small position live testing
4. Adjust based on results

**Don't go all-in right away**—even the best strategy needs breaking in!

---

## X. Bonus: Strategy Author's "Little Quirks"

Looking carefully at the code, you'll find some interesting things:

1. **sma_50 Bug**: Code calculates `sma_50` and `sma_200` both using `timeperiod=200`
   > "Probably forgot to change it when copy-pasting, luckily sma_50 isn't used at all 😂"

2. **MACD Calculated for Nothing**: Code calculates a bunch of MACD indicators, but buy/sell signals don't use them at all
   > "Maybe for plotting? Or changed mind after planning to use it?"

3. **Selling Too Early?**: ADX > 70 is indeed high, but strong trends might get even stronger
   > "Maybe author is conservative, would rather make less but lock in profits"

---

## XI. Final Words

### One-Sentence Review
> "Clean and efficient short-term strategy, good for learning and modifying, but watch out for the wide stop-loss issue."

### Who Should Use It?
- ✅ Quant Beginners: Simple code, clear logic
- ✅ Short-term Lovers: 5-minute timeframe, in and out fast
- ✅ Strategy Improvers: Good base framework, can add your own features
- ✅ People with Time to Watch: Can manually add trailing stop

### Who Shouldn't Use It?
- ❌ Conservative Traders: 25% stop-loss too wide
- ❌ Long-term Investors: Holding too short
- ❌ Range-bound Market Traders: Few signals
- ❌ Passive Income Seekers: Needs adjustment and optimization

### Manual Trader Recommendations
If manually using this logic:
1. Wait for ADX > 30 (confirm trend)
2. Watch when price is below Bollinger middle band
3. Enter when TEMA starts rising
4. Set 15% profit target and 20% stop-loss
5. Run if 15% reached within 10 minutes

---

## XII. ⚠️ Risk Emphasis Again (Must Read)

### Backtest is Beautiful, Live Trading Be Careful

Quickie's historical backtest might look good—but there are traps:

> **Tiered ROI performs well in backtests because it's designed as "shorter time, higher profit," and backtests often catch quick rises. But live trading might not be so lucky.**

Simply put: **"Backtest is like an open-book exam, live trading is like a closed-book exam."**

### Complexity Risks

Although the strategy is simple, there are risk points:
- **Wide Stop-loss Risk**: 25% stop-loss, really hurts when you lose
- **Counter-trend Buy Risk**: Buying dips in downtrend is catching falling knives
- **Early Sell Risk**: ADX > 70 might sell too early, missing follow-up gains

### My Recommendations (Real Talk)

```
1. Make stop-loss smaller, like -15% or -20%
2. Consider adding trailing stop to lock in floating profits
3. Test with small positions first, don't go all-in
4. Look at max drawdown in backtests, not just returns
```

**Remember**: No matter how simple the strategy, when the market teaches you a lesson, it doesn't knock first. Light position testing, survival is most important! 🙏

---