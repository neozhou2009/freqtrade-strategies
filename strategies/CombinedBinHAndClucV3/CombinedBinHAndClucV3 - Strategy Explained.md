# CombinedBinHAndClucV3 Strategy Explained: Bollinger Band Double-Knife Style

> **Nickname**: Bollinger Band Double-Knife  
> **Profession**: Oversold Rebound Expert  
> **Timeframe**: 5 Minutes (5m)

---

## 1. What's This Strategy?

Put simply, **CombinedBinHAndClucV3** is a "double-knife" oversold rebound strategy:

- Merged from two classic strategies: **BinHV45** + **ClucMay72018**
- Each strategy has its own special move—buy if either one triggers
- Specifically catches opportunities where price "drops too much and bounces back"

Think of it like an experienced fisherman casting two nets—one catches rapid sell-off rebound fish, the other catches volume-shrinking oversold fish. Fish can enter either net—there's always a match for you. 🐟

---

## 2. Core Settings: "Take profits quick, cut losses deep"

### Take-Profit Rule (ROI Table)

```
Cumulative return ≥ 1.8% → Take-profit triggered
```

**Translation**: Grab 1.8% and run, don't get greedy. Lock in profits, move on.

### Stop-Loss Rules

```
Fixed stop-loss: -10%
Trailing stop: Activates after 3% profit, protects 1% of gains
Time stop-loss: Force exit at market price if still in loss after 36.7 hours
```

**Translation**:
- Max loss 10%, hit the line and admit defeat
- After 3% profit, activate the "shield"—exit if price drops 1% from high
- Still losing after 36 hours? No more waiting, get out at market

### Other Settings

| Setting | Value | Plain English |
|---------|-------|---------------|
| Timeframe | 5 minutes | Short-term, high frequency |
| Sell only in profit | True | Can't sell when losing money |
| Profit offset | 0.1% | Must earn at least 0.1% before selling triggers |

---

## 3. Two Sets of Entry Conditions: Here's the breakdown

This strategy has two sets of buy conditions—**trigger a buy if either one is met**:

### 🎯 Set 1: BinHV45 Style (Rapid Sell-off Rebound)

**Core Logic**: Price suddenly crashes, breaks below the lower Bollinger Band, but can't drop anymore—bottom fishing!

**Plain English**:
> "This coin dropped so fast it punched through the Bollinger Band lower rail. The lower wick is short, meaning the close is near the day's low—no one's buying. Hey, this might be the last drop, a rebound is coming!"

**Specific Conditions (Plain English Version)**:

| Condition | Plain Translation |
|-----------|-------------------|
| Previous day's lower Bollinger Band is valid | Confirm it's not a calculation error |
| Bollinger Band width > 0.8% of price | Enough volatility, there's meat to eat |
| Closing price change > 1.75% | The day really did crash hard |
| Lower wick < 25% of channel width | Close near the low, hit bottom |
| Close < previous day's lower Bollinger Band | Broke below the rail, oversold |
| Close ≤ previous day's close | Continued dropping or flat, confirms downtrend |

**One-liner**: Price rapidly pierces the lower Bollinger Band with a short wick and high volatility—classic "last drop" pattern.

---

### 📉 Set 2: ClucMay72018 Style (Volume-Shrinking Oversold)

**Core Logic**: Price breaks below the lower Bollinger Band, but volume is abnormally low—selling pressure has dried up, a rebound may come.

**Plain English**:
> "Price broke below the Bollinger Band lower rail, but the volume is so tiny? That means no one's willing to sell. Selling pressure has exhausted, a rebound might be coming."

**Specific Conditions (Plain English Version)**:

| Condition | Plain Translation |
|-----------|-------------------|
| Close < 50-day moving average | Confirm medium-term downtrend |
| Close < 98.5% of Bollinger Band lower rail | Clearly broke below the rail, oversold |
| Volume < 20x the 30-day average | Volume abnormally shrunken |

**One-liner**: Price breaks below the lower Bollinger Band with shrinking volume in a downtrend—selling pressure exhausted, waiting for rebound.

---

## 4. Protection Mechanisms: 4 Layers of "Protective Charms"

This strategy has 4 layers of protection to keep you from losing your shorts:

| Protection Type | Trigger Condition | Effect | Plain English |
|-----------------|-------------------|--------|---------------|
| Fixed stop-loss | Loss reaches 10% | Hard stop | "10% loss and you're out, don't hold on" |
| Time stop-loss | Holding > 36.7 hours and losing | Force exit | "Held almost two days still losing? I'm done waiting" |
| Trailing stop | Profit reaches 3% then activates | Lock in profits | "Gained enough, pull back 1% and I'm gone" |
| Sell only in profit | Sell signal triggers but losing | Forbid selling | "No selling when losing, wait for break-even" |

These 4 layers are like wearing a bulletproof vest, a helmet, and hiring a bodyguard, all at once. Solid! 🛡️

---

## 5. Exit Logic: Simpler Than Entry

### 5.1 Take-Profit Exit

```
Cumulative return ≥ 1.8% → Sell
```

**Plain English**: Grab 1.8% and run, fast entry and exit, don't get greedy.

### 5.2 Signal Exit

When **5 consecutive candles** are above the Bollinger Band upper rail, sell triggers.

**Plain English**:
> "Five straight 5-minute candles sitting above the Bollinger Band upper rail? This rally is too strong, a correction is likely—bail out first."

### 5.3 Trailing Stop Trigger

Price goes up then drops? Exit when the trailing stop line is hit.

**Plain English**:
> "Alright, it's climbing, I'll watch it. Drop 1% from the high? Goodbye, locking in profits."

---

## 6. Strategy "Personality"

If the strategy were a person:

### ✅ Pros (The Praise Section)

1. **Dual-Knife Hunter**: Two entry logics covering both rapid sell-off rebounds and volume-shrinking rebounds, stronger adaptability
2. **Aggressive Stop-Loss**: 4 layers of protection, exits when needed, no hesitation
3. **Not Greedy**: 1.8% take-profit, takes small profits and runs, accumulates over time
4. **Time Stop-Loss**: Exits forcefully if still losing after 36 hours, won't wait around with you

### ⚠️ Cons (The Roast Section)

1. **Sell-and-Miss Master**: 1.8% take-profit too conservative, could soar right after you sell and watch helplessly
2. **5-Minute Noise**: Short timeframe is easily fooled by false signals, and fees are high too
3. **Gets Slaughtered in One-Direction**: One-directional rallies will sell you out repeatedly, one-directional drops will trigger stops repeatedly
4. **Exit Conditions Too Strict**: Must have 5 consecutive candles break the upper rail to sell, could miss the best exit

---

## 7. When to Use: Applicable Scenarios

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Wide-range sideways | ✅ Use heavily | Price repeatedly hits Bollinger Band rails, many signals |
| High-volatility coins | ✅ Suitable | Higher volatility, easier to trigger conditions |
| Rapid drop then rebound | ✅ Perfect match | BinHV45 conditions designed for this scenario |
| Shrinking-volume drop | ✅ Suitable | Cluc condition specializes in catching exhausted selling pressure |
| One-directional uptrend | ❌ Don't use | Will sell you out repeatedly, miss the main wave |
| One-directional downtrend | ❌ Absolutely don't | Will trigger stops repeatedly, lose you serious money |
| Low-volatility consolidation | ❌ No signals | Too little volatility, can't trigger entry conditions |

---

## 8. Summary: What Does This Strategy Actually Do?

### One-Word Verdict
> "A cash cow in sideways markets, a money burner in trending markets."

### Who Should Use It?
- ✅ Day traders who like short-term trading
- ✅ People who can handle high-frequency trading fees
- ✅ People who think "grab small profits and run" is great
- ✅ Traders skilled at identifying sideways markets

### Who Should NOT Use It?
- ❌ People who want to hold long-term and ride major trends
- ❌ People who hate frequent operations
- ❌ People using high-fee platforms
- ❌ Traders who only do one-directional moves

### My Suggestions
1. **Backtest first**: Run at least 3 months of historical data, ensure strategy works on your chosen coin
2. **Pick volatile coins**: BTC, ETH, or highly volatile altcoins
3. **Watch fees**: 5-minute high-frequency trading, fees can eat most of your profits
4. **Don't use in bull markets**: One-directional rallies will sell you out, switch strategies

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Mean Reversion

CombinedBinHAndClucV3 is a typical **mean reversion strategy**. Its profit philosophy is:

> "When price drops too much it bounces back, when it rises too much it falls back."

**Its three defining traits**:

- **Doesn't predict direction**: Only looks for oversold opportunities, doesn't care about big trends
- **Fast in, fast out**: 5-minute level, grabs 1.8% and runs
- **Casts two nets**: Two entry logics, covers more scenarios

### 9.2 Different Market Performance (Plain English)

| Market Type | Rating | Plain Explanation |
|:-----------|:-------|:------------------|
| 📈 Wide-range sideways | ⭐⭐⭐⭐⭐ | Perfect match, price hits Bollinger Bands repeatedly, many signals |
| 🔄 High volatility | ⭐⭐⭐⭐ | Big swings, conditions trigger easily, lots of eating opportunities |
| 📉 Rapid drop rebound | ⭐⭐⭐⭐⭐ | BinHV45 conditions tailor-made for this scenario |
| 🎯 Shrinking-volume drop | ⭐⭐⭐⭐ | Cluc condition catches exhausted selling pressure rebounds |
| 📊 Sustained rally | ⭐⭐☆☆☆ | Buy and immediately sell out, miss the main wave |
| 📉 Sustained drop | ⭐☆☆☆☆ | Repeated stops, losses mount up |
| 😴 Low-volatility consolidation | ⭐⭐☆☆☆ | Too little volatility, conditions don't trigger, wasted trip |

**Bottom line**: Swims freely in sideways markets, drowns in trending ones.

---

## 10. Want to Run This Strategy? Check These Settings First

### 10.1 Trading Pair Settings

| Setting | Suggested Value | Notes |
|---------|----------------|-------|
| Timeframe | 5 minutes | Don't change, strategy is designed for 5m |
| Take-profit line | 1.8% | Can raise if you feel too conservative, but stay under 5% |
| Stop-loss line | -10% | Don't widen it, you'll lose more |
| Trailing stop | Activates at 3% profit | Adjust based on your risk tolerance |

### 10.2 Key Config Settings

```yaml
# Minimum return target
minimal_roi: {"0": 0.018}  # 1.8% take-profit

# Stop-loss
stoploss: -0.10  # 10% hard stop

# Trailing stop
trailing_stop: True
trailing_stop_positive: 0.01  # Protect 1% of profits
trailing_stop_positive_offset: 0.03  # Activate after 3% profit
```

### 10.3 Hardware Requirements (Important!)

5-minute strategy computational load is manageable, but trading frequency is high:

| Number of Pairs | Minimum | Recommended | Experience |
|-----------------|---------|--------------|------------|
| 1-10 pairs | 2-core 2GB | 2-core 4GB | Smooth |
| 10-30 pairs | 2-core 4GB | 4-core 8GB | Fluid |
| 30+ pairs | 4-core 8GB | 4-core 16GB | May need optimization |

**Warning**: High trading frequency, API rate limits could be a bottleneck—don't run too many pairs!

### 10.4 Backtesting vs Live Trading

Backtesting looks great, but live trading differs:

1. **Slippage**: Backtesting fills at ideal prices, live trading may have slippage
2. **Fees**: High-frequency trading fees add up considerably
3. **Latency**: Network delay could cause missing optimal prices
4. **Liquidity**: Small-cap coins may not be sellable

**Suggested Process**:
1. Backtest 3 months of historical data first
2. Small-capital live test for 1-2 weeks
3. Scale up capital after confirming profitability
4. Regularly check and adjust parameters

**Don't go all-in from the start**, even the best strategy needs a break-in period!

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Look closely at the code and you'll find some interesting design choices:

1. **Dual-strategy merge**: BinHV45 and ClucMay72018 are both ~2018-era old strategies; the author merged them, essentially combining the skills of two generations of masters.

   > "I want all the special moves from both old masters!"

2. **Time stop-loss**: Exit forcefully if holding at a loss for over 36 hours. This shows the author knows—when it comes to oversold rebounds, dragging it out turns you into a "bag holder."

   > "Oversold rebounds must be fast; hold too long and you're stuck forever."

3. **Sell only in profit**: No selling when losing money. This is to prevent you from selling at the bottom.

   > "No selling when losing! Wait until profitable before I let you sell!"

4. **5 consecutive candles break upper rail before selling**: Exit conditions are strict, meaning the author wants to confirm it's a real breakout, not a false one.

   > "5 consecutive breakouts above the upper rail? This rally is real, exit first."

---

## 12. The Final Word

### One-Word Verdict
> "A tool for raking in pocket change in sideways markets, a machine for losing money in trending markets. Used right, you score big; used wrong, you get shot."

### Who Should Use It?
- ✅ Traders who can identify sideways markets
- ✅ People who like short-term, high-frequency, fast in/fast out
- ✅ Users of low-fee platforms (or with fee rebates)
- ✅ People who can strictly follow stop-loss discipline

### Who Should NOT Use It?
- ❌ People who want to hold long-term and ride big trends
- ❌ People who hate frequent operations and like to lie flat (do nothing)
- ❌ Users of high-fee platforms
- ❌ Beginners who can't read market conditions

### Manual Trading Suggestions

If you want to manually execute this strategy's logic:

1. **Watch the lower Bollinger Band**: Start paying attention when price drops below it
2. **Check volume**: Abnormally shrinking volume may mean exhausted selling pressure
3. **Look at the lower wick**: Short wick means close near the low, possibly at the bottom
4. **Set stop-loss**: Must set 10% stop-loss after buying, don't have illusions
5. **Don't be greedy**: Grab 2-3% and leave, don't wait for a big rally

---

## 13. ⚠️ Risk Re-emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Requires Caution

CombinedBinHAndClucV3's historical backtest performance often **looks good**—but there's a trap:

> **Mean reversion strategies perform well in sideways markets but fail badly in trending markets.**

Simply put: **History doesn't simply repeat; past sideways markets don't guarantee future ones.**

### Hidden Risks of Complex Strategies

In live trading, you may encounter:

- **Slippage risk**: High-frequency trading, slippage adds up and can eat profits
- **Fee erosion**: 5-minute period trading is frequent, fees are no small matter
- **API rate limits**: Trading too frequently may trigger exchange rate limits
- **One-directional markets**: Sustained rallies sell you out, sustained drops trigger stops, caught in both directions

### My Suggestions (Sincere Advice)

```
1. Judge market conditions first: Use in sideways markets, switch strategies in trending ones
2. Small capital testing: Don't go all-in, test with small capital for 1-2 weeks first
3. Watch fees: Choose low-fee platforms, otherwise all profits go to fees
4. Strictly follow stop-loss: The 10% stop-loss is your lifeline, don't have illusions
5. Don't expect to get rich: This is a strategy for raking in pocket change, not a money-making secret
```

**Remember**: No matter how good a strategy is, the market won't announce when it teaches you a lesson. Test with light positions—survival is the top priority! 🙏

---

**Final Reminder**: Mean reversion's essence is "dropped too much, bounces back"—but what if it truly just "dropped and never came back"? The stop-loss is your last line of defense. Don't complain that the 10% stop-loss is harsh; protecting your capital matters more than making money!
