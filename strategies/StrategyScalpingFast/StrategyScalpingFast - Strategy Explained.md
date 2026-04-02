# StrategyScalpingFast: The Lightning Scalper

> **Nickname**: The Flash, Oversold Harvester  
> **Job**: Quick-draw specialist focused on "buying the dip"  
> **Timeframe**: 1 minute (blink and you'll miss it)

---

## I. What Is This Strategy?

Simply put, **StrategyScalpingFast** is:

- **Super Fast**: 1-minute candles, gone in a blink
- **Super Strict**: 6 conditions must ALL be met before buying
- **Super Cautious**: Only acts when prices are "brutally oversold"

It's like a **hunter specializing in "sniping bargains"** 🏹 —— usually crouching still, only striking when prices drop to "miserable" levels, then grabbing 1% and running!

---

## II. Core Configuration: "Grab a Little and Run"

### Profit Taking Rules (ROI Table)

```
After 0 minutes → 1% profit and done
```

**Translation**: Pretty stingy, right? But small gains add up! Do 10 trades a day, that's 10% return (ideally).

### Stop Loss Rules

```
Loss reaches 10% → Admit defeat and leave
```

**Translation**: Although I'm stingy (only making 1%), I'm brave (can handle 10% loss). This setting is a bit odd... Typically scalping strategies have smaller stop losses. You might want to change it to 3-5%.

---

## III. Buy Conditions: Stricter Than Your Mom Pushing Marriage

This strategy's buy conditions, in one sentence:

> **Price must crash hard + trend must have strength + money flow must dry up + indicators must oversold + golden cross must confirm + CCI must be extreme**

Let me translate to plain English:

### 🎯 Condition Breakdown (ALL must be met!)

| Condition | Threshold | Plain English |
|-----------|-----------|---------------|
| Open price < EMA lower band | - | "Price is already on the floor" |
| ADX > 30 | 30 | "Trend is still there, not dead water" |
| MFI < 30 | 30 | "Sellers are exhausted" |
| FastK < 30 AND FastD < 30 | 30 | "Stochastic indicators are lying at the bottom" |
| FastK crosses above FastD | - | "Golden cross! Ready to fly!" |
| CCI < -150 | -150 | "Extreme oversold, can't get any worse" |

**Classic line**:
> "6 conditions, if one isn't met, no buy. I'm not being difficult, I want certainty!"

---

## IV. Sell Logic: Take Profit and Go

### 4.1 Sell Conditions (Pick one + mandatory)

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| Scenario 1 | Price touches EMA upper band + CCI > 150 | "Hit the ceiling, time to go" |
| Scenario 2 | FastK crosses above 70 + CCI > 150 | "Stochastic overbought, run!" |
| Scenario 3 | FastD crosses above 70 + CCI > 150 | "D line overbought too, retreat!" |

**Translation**: Three sell signals, just need one to trigger, plus CCI confirming overbought, sell immediately!

### 4.2 Symmetric Beauty

Look at this:
- Buy: CCI < -150 (extreme oversold)
- Sell: CCI > 150 (extreme overbought)

**Perfect symmetry!** This strategy is designed like art 🎨

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Time for Compliments)

1. **Clean code**: 100 lines, no fluff, beginners can understand
2. **Strict signals**: 6 confirmations, few false signals
3. **Symmetric design**: Buy/sell logic symmetric, OCD heaven
4. **Fast capital turnover**: 1% profit taking, quick flips
5. **Hardware friendly**: No need for powerful servers, small VPS works

### ⚠️ Cons (Time to Roast)

1. **Low trigger frequency**: 6 conditions simultaneously? I'll wait until flowers wilt 🥀
2. **Stop loss too wide**: Scalping strategy with 10% stop loss? Are you serious?
3. **No trailing stop**: Trend comes, you take 1% and leave, missing out?
4. **1-minute timeframe**: Too much noise, frequent false breakouts
5. **Some indicators unused**: RSI, MACD, Bollinger Bands all calculated but not used in signals, purely decorative

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|----------------|--------|
| 📊 Sideways ranging | ✅ Recommended | Best battlefield for oversold bounces |
| 🐢 Mild trend | ⚠️ Cautious | Can work, but may sell too early |
| 📉 One-way decline | ❌ Not recommended | Catching falling knife, easy to get cut |
| 🎢 High volatility | ❌ Not recommended | Too much noise, false signals everywhere |

---

## VII. Summary: How Good Is This Strategy?

### One-Sentence Review
> "Clean and elegant oversold sniper, but stop loss setting is a bit odd."

### Who Should Use It?
- ✅ Beginners wanting to learn scalping strategies (clean, understandable code)
- ✅ Traders mainly in ranging markets
- ✅ People who demand high signal quality (hate being fooled by false signals)
- ✅ Patient people who can wait for opportunities (low trigger frequency)

### Who Should NOT Use It?
- ❌ People chasing high-frequency trading
- ❌ People who like trend following
- ❌ People who don't want to watch the screen (1-minute timeframe)
- ❌ Trend tracking enthusiasts

### My Suggestions

1. **Adjust stop loss**: Change 10% stop loss to 3-5%, more fitting for scalping
2. **Relax CCI threshold**: -150 is too extreme, try -100
3. **Test with small capital**: Run with small money first to see results
4. **Pair with other strategies**: This strategy fits as part of a combination, don't bet all your money here

---

## VIII. What Market Can This Strategy Make Money In?

### 8.1 Core Logic: Greed in Panic

StrategyScalpingFast's money-making philosophy is simple:

> **"Be greedy when others are fearful" — Warren Buffett**

- **Oversold reversal**: When everyone panics and sells, I step in to grab bargains
- **Quick profit taking**: Make 1% and run, not greedy
- **Multiple confirmation**: Through 6 indicators ensure it's not "catching a falling knife"

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:------------|:-------|:--------------------------|
| 📊 Sideways ranging | ⭐⭐⭐⭐⭐ | "This is my home turf! Prices swing back and forth, lots of oversold bounce opportunities" |
| 🐢 Mild trend | ⭐⭐⭐☆☆ | "Okay, can make money, but might sell too early" |
| 📉 One-way decline | ⭐⭐☆☆☆ | "After oversold comes more oversold, am I here to donate money?" |
| 🎢 High volatility | ⭐⭐☆☆☆ | "Too much noise, pile of false signals, wallet can't handle it" |

**One-sentence summary**: Ranging markets are my home turf, trending markets I'm a bystander.

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration | Recommendation | Comment |
|---------------|----------------|---------|
| Number of pairs | 5-15 | Too many will be overwhelming |
| Pair type | Major coins | Small coins have too much noise |
| Minimum volume | Medium or above | Liquidity matters |

### 9.2 Key Configuration File Settings

```yaml
# Stop loss (recommended adjustment)
stoploss: -0.05  # Originally -0.10, recommend tightening

# Profit taking
minimal_roi:
  "0": 0.01  # 1% profit taking

# Timeframe
timeframe: 1m
```

### 9.3 Hardware Requirements (Important!)

This strategy is lightweight, no need for high-end servers:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|------------|
| 1-10 pairs | 1GB | 2GB | Smooth |
| 10-30 pairs | 2GB | 4GB | Normal |
| 30+ pairs | 4GB | 8GB | Might be a bit slow |

**Warning**: If you run 100 pairs on 1-minute timeframe, forget what I said 😅

### 9.4 Backtesting vs Live Trading

Backtesting performance might be beautiful, but live trading has issues:

- **Slippage**: 1-minute high-frequency trading, slippage can eat profits
- **Latency**: Time difference between signal trigger and execution
- **Liquidity**: Small coins may not buy or sell quickly

**Recommended Process**:
1. Backtest first to see results
2. Run paper trading for a week
3. Small capital live testing
4. Gradually increase position

**Don't go all-in from the start**, no matter how good the strategy, it needs to be calibrated!

---

## X. Bonus: Strategy Author's "Little Secrets"

Look carefully at the code, you'll find some interesting things:

1. **RSI, MACD, Bollinger Bands calculated but not used**
   > "Can't I just calculate for fun? Doesn't cost anything."

2. **Defined 5-minute timeframe but didn't use it**
   ```python
   timeframe_support = '5m'
   timeframe_main = '5m'
   ```
   > "Reserved interface, might use later, wrote it first."

3. **Stop loss 10% is 10x bigger than profit taking 1%**
   > "I'm willing to lose 10%, but only make 1% and run. What spirit is this?"

4. **Code only 100 lines**
   > "Less is more, as long as it works."

---

## XI. Final Words

### One-Sentence Review
> "Clean and elegant oversold sniper, but needs patience to wait for opportunities."

### Who Should Use It?
- ✅ Beginners learning scalping strategies
- ✅ Oversold bounce trading in ranging markets
- ✅ Traders who want signal quality
- ✅ Small capital quant beginners

### Who Should NOT Use It?
- ❌ High-frequency trading seekers
- ❌ Trend following enthusiasts
- ❌ People who don't like waiting for opportunities
- ❌ Large capital high-frequency operators

### Manual Trader Advice

**Not recommended to manually replicate**! Reasons:

1. 1-minute timeframe, watching will drive you crazy
2. 6 indicators to monitor simultaneously, eyes will go blind
3. Low trigger frequency, high waiting cost
4. Let machines do these repetitive tasks

---

## XII. ⚠️ Risk Emphasis Again (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

StrategyScalpingFast's historical backtesting may **perform quite well** — but here's the trap:

> **Because signals are strict, triggers are rare, backtesting results might just be "lucky" instances.**

Simply put: **Past performance doesn't guarantee future results.**

### Hidden Risks of Scalping Strategies

In live trading, you might encounter:

- **Slippage eats profits**: 1% profit, slippage can eat 0.3%
- **Latency impact**: Network lag 1 second, price might have changed
- **Liquidity risk**: Small coins difficult to buy/sell
- **Fee erosion**: High-frequency trading fees are also costs

### My Advice (Truth)

```
1. Change stop loss from 10% to 3-5%
2. Relax CCI threshold to -100
3. Small capital testing, don't go all-in
4. Use together with other strategies
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it doesn't warn you first. Light position testing, survival is most important! 🙏

---

**Final Reminder**: This is a great learning template, code is clean and easy to understand. But before live trading, must do sufficient testing and parameter optimization!