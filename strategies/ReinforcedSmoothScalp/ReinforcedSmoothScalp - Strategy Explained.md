# ReinforcedSmoothScalp Strategy: The "Mosquito Blood-Sucking Method" for High-Frequency Scalping

> **Nickname**: Mosquito Blood-Sucker  
> **Profession**: Professional Vampire (no wait, professional scalper)  
> **Timeframe**: 1 Minute

---

## I. What is This Strategy?

Simply put, **ReinforcedSmoothScalp** is:
- High-frequency trading,疯狂刷单
- Only make 2% each time, mosquito meat is still meat
- Strict conditions, layer after layer of screening, won't act easily

Like a **mosquito** 🦟—one bite doesn't take much, but with many bites, it adds up! As long as you don't get swatted, you can keep sucking.

---

## II. Core Configuration: Basically "Run After Making 2%"

### Take Profit Rule (ROI Table)

```
Make 2% → Run immediately
```

**Translation**: This strategy is a "run after making a little" type. 2%? Enough! Lock it in!

### Stop Loss Rule

```
Lose 10% → Cut and stop
```

**Translation**: Gives plenty of breathing room, not the "glass heart" type that stops out at every little move.

**Risk-Reward Ratio**: Make 2%, lose 10%, ratio 1:5.

What does this mean? You can lose 5 times, win once, and still break even! Of course, if you can get a 50% win rate, that's a guaranteed profitable business.

---

## III. One Buy Condition: But You Must Pass 5 Checkpoints

The strategy nominally has only 1 buy condition, but it's actually **5 sub-conditions that ALL must be met**!

Like checking three generations of family history before a blind date, can't miss any! 🤣

### 🎯 Full Condition Analysis

**Plain English Translation**:

| # | Condition | Human Translation |
|---|-----------|-------------------|
| 1 | Open < EMA_Low | Open price should be below EMA lower band, meaning price is relatively low |
| 2 | ADX > 30 | Trend must be clear, can't be that wishy-washy ranging |
| 3 | MFI < 30 | Money must be flowing out, meaning people are panic selling |
| 4 | FastK < 30 AND FastD < 30 AND golden cross | Stochastic must be oversold, AND just started turning up |
| 5 | Close > resampled SMA | Big direction must be up, can't go against trend |

**Summary**:
> "All 5 conditions must be met before this strategy acts. This isn't decision paralysis—this is **OCD at its finest**!"

---

## IV. Protection Mechanism: Trend Filter + Multi-Layer Confirmation

### 4.1 Resampled Trend Filter

This strategy has a clever trick—**resampling**.

What does it mean? Simply put:
- You're trading at 1-minute level
- But checking 5-minute level trend
- Only when big direction is up, dare to enter

**Plain English**:
> "Like looking for a job—not only checking if the position is good, but also if the company is solid, if the industry is hot. Triple insurance!"

### 4.2 Stop Loss Protection

| Protection Type | Parameter | Purpose |
|-----------------|-----------|---------|
| Hard stop loss | 10% | Maximum 10% loss, survival tool |
| Trend filter | Resampled SMA | Don't enter against trend |
| ADX filter | > 30 | Don't enter in ranging market |

---

## V. Sell Logic: Run After Making Enough, No Greed

### 5.1 Take Profit: Simple and Direct

```
Make 2% → Run immediately
```

**Plain English**:
- Not greedy, mosquito meat is still meat
- Quick in-and-out, accumulation leads to significant gains

### 5.2 Sell Signals

Strategy also actively judges when to sell:

| Scenario | Condition | Plain English |
|----------|-----------|---------------|
| Price shot up | Open ≥ EMA_High | Price hit upper band, about done |
| Stochastic overbought | FastK or FastD crosses above 70 | Rose too much, time to rest |
| CCI confirmation | CCI > 100 | Confirms overbought, can exit |

**Classic Line**:
> "Made money, that's about enough, don't be greedy!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Doesn't Act Randomly**: 5 layers of screening, high signal quality
2. **Follows Major Trend**: Resampled filter, no counter-trend trading
3. **Friendly Risk-Reward**: Lose 5 times, win once, still break even
4. **High-Frequency Accumulation**: Mosquito meat adds up to full stomach

### ⚠️ Cons (Roast Section)

1. **High Trading Frequency**: Fees are a big problem, need low-fee exchange
2. **Slippage Sensitive**: 1-minute level, slippage can eat your profits
3. **Goes on Strike in Ranging Markets**: ADX > 30 required, basically lying flat in ranging markets
4. **Long Only**: Can only watch during downtrends

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|----------------|--------|
| Clear Uptrend | 🚀 Heavy Position | ADX filter effective, trend-following is sweet |
| Ranging Sideways | 🛌 Lie Flat and Wait | Few signals, might as well rest |
| Downtrend | 🍿 Watch Show | Long only, cannot short |
| High Volatility Chaos | 🤔 Cautious | Slippage will eat profits |

---

## VIII. Summary: How's This Strategy Really?

### One-Liner Review
> "Master of high-frequency scalping, but extremely sensitive to fees and slippage."

### Who Should Use It?
- ✅ Those with low-fee exchanges
- ✅ Can run 60+ trading pairs
- ✅ Have quant experience
- ✅ Pursue stable small profits

### Who Shouldn't Use It?
- ❌ High-fee exchanges
- ❌ Can only run a few trading pairs
- ❌ Want to get rich overnight
- ❌ No patience to watch charts

### My Advice
1. **Find a low-fee exchange**: High-frequency trading is extremely sensitive to fees
2. **Multiple pairs for diversification**: Strategy author suggests at least 60
3. **Watch slippage**: Main gap between backtest and live is here
4. **Paper trade first**: Get familiar before going live

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Accumulate Small Gains

ReinforcedSmoothScalp is a classic **scalping strategy**. Its money-making philosophy:

> "Don't pursue one big win, pursue countless small wins. Mosquito meat adds up!"

- **Multi-Layer Confirmation**: 5 conditions layer by layer, ensure signal quality
- **Trend Filter**: Resampling ensures following major trend
- **Quick Take Profit**: 2% and run, not greedy

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:------------|:-------|:---------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Clear trend, trend-following, sweet |
| 🔄 Ranging Sideways | ⭐⭐☆☆☆ | ADX condition not met, few signals |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Long only, can only watch during drops |
| ⚡ High Volatility Chaos | ⭐⭐☆☆☆ | Slippage too big, fees eat profits |

**One-line summary**: Performs best in clear trends, lies flat and waits in ranging markets.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Note |
|-------------|-------------------|------|
| Number of pairs | ≥ 60 | Strategy author explicitly recommends, diversify risk |
| Timeframe | 1m | Don't change, this is the lifeline of high-frequency |
| Trading fees | ≤ 0.1% | Lower is better, otherwise fees eat profits |

### 10.2 Key Configuration Settings

```yaml
# Take profit
minimal_roi:
  "0": 0.02  # 2% take profit

# Stop loss
stoploss: -0.10  # 10% stop loss

# Timeframe
timeframe: 1m
```

### 10.3 Hardware Requirements (Important!)

This strategy is high-frequency, has system requirements:

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|---------------|----------------|---------------------|------------|
| Under 60 | 4 GB | 8 GB | Decent |
| Over 60 | 8 GB | 16 GB | Smooth |

**Warning**: Don't run this on an old VPS, it'll lag until you question life! 😅

### 10.4 Backtest vs Live

**Backtest looks beautiful**:
- No slippage
- Perfect execution
- Impressive profits

**Live reality is harsh**:
- 1-minute level slippage is huge
- High-frequency trading fee accumulation
- Exchange API latency

**Recommended Process**:
1. Run backtest first, understand logic
2. Paper trade to test
3. Small capital live verification
4. Confirm stability before adding position

**Don't go all-in right away**, no matter how good the strategy, it needs to be calibrated!

---

## XI. Bonus: The Strategy Author's "Little Tricks"

Looking carefully at the code, you'll find some interesting things:

1. **Adjustable resampling factor**: `resample_factor = 5`
   > "Think signals are too few? Can lower this value. Think signals are too noisy? Can raise it."

2. **EMA channel design**: Calculates EMA for High/Close/Low separately
   > "Upper and lower bands both available, clear where resistance and support are."

3. **Commented-out backup conditions**: There's a commented-out buy condition section in the code
   > "Author probably thought too many conditions would reduce signal frequency, so commented it out."

---

## XII. Final Words

### One-Liner Review
> "Model student of high-frequency scalping, but needs low fees and many pairs to work with."

### Who Should Use It?
- ✅ Those with low-fee exchanges
- ✅ Can run many trading pairs
- ✅ Pursue stable small profits
- ✅ Have quant experience

### Who Shouldn't Use It?
- ❌ High fees
- ❌ Can only run a few pairs
- ❌ Want to get rich overnight
- ❌ Don't like high-frequency trading

### Manual Trader Recommendations
**Strongly NOT recommended for manual trading**:
- High signal frequency, humans can't keep up
- 1-minute level requires continuous monitoring
- Execution speed requirements too high

---

## XIII. ⚠️ Risk Re-emphasis (Must Read Section)

### Backtests Are Beautiful, Live Trading Requires Caution

ReinforcedSmoothScalp's historical backtest performance often **looks beautiful**—but there's a trap:

> **High-frequency strategies in backtests usually have no slippage, but live slippage can eat half your profits.**

Simply put: **Backtest is ideal state, live is a battlefield.**

### Hidden Risks of Complex Strategies

In live trading, complex logic can lead to:
- **Slippage eroding profits**: 1-minute level, slippage may be bigger than take profit target
- **Fee accumulation**: High-frequency trading fee accumulation is shocking
- **API latency**: Exchange API latency may miss best prices

### My Advice (Real Talk)

```
1. Find an exchange with fees ≤ 0.1%
2. Run at least 60 trading pairs to diversify risk
3. Test with small capital for at least 1 month first
4. Observe live vs backtest differences, adjust expectations
```

**Remember**: Mosquito blood-sucking strategy—sucking a lot can fill you up, but only if you survive without getting swatted! 🙏

---

**Final Reminder**: No matter how good the strategy, when the market teaches you a lesson, it doesn't give notice. Test with small positions—staying alive is most important!