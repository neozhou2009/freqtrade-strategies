# NormalizerStrategy Strategy: The Mean Reversion Hunter That Turns Prices into "Scores"

> **Nickname**: "The Scorer", "Mean Reversion Professional"  
> **Profession**: Specializes in finding trading opportunities where prices go to extremes  
> **Timeframe**: 1 Hour (unhurried, just right)

---

## 1. What's This Strategy?

Simply put, **NormalizerStrategy** is:
- A strategy that turns prices into "scores" from 0 to 100
- Buy when the score is too low, sell when it's too high
- Make money when price returns to "normal levels"

Think of it like: you got a 10 on your exam, next time you'll probably do better; you got a 98, next time you'll probably do worse — that's **mean reversion**! 🎯

**Core Idea of This Strategy**: Extreme things won't stay extreme forever, prices always return to "normal".

---

## 2. Core Settings: Basically "Either Make 18% or Hold Through"

### Take-Profit Rules (ROI Table)

```
Make 18% → Run immediately, no hesitation!
```

**Translation**: This strategy's goal is clear — make 18% in one trade. Unlike those "short-term traders" who run at 5%, this is a "one big score" player! 💰

### Stop-Loss Rules

```
Stop-loss at -99% before triggering
```

**Translation**: Folks, this is basically **no stop-loss at all**! It means: either make 18% or... you know 🫠

**Commentary**: The mindset of this strategy's designer might be: "Mean reversion will definitely happen, it's just a matter of time" — but sometimes the market teaches you a lesson 😅

---

## 3. Entry Conditions: Buy When the Score is Too Low

This strategy's entry logic is super simple, just one sentence:

### Buy When Normalized Price < Buy Threshold = Do It!

**What's "normalization"?**

Think of it this way:
- Bitcoin's recent 30-day price range is $50,000 to $70,000
- Current price is $52,000
- Normalized score = (52000 - 50000) / (70000 - 50000) = 0.1 (that's a 10)

**What does this 10 mean?**
- Current price is near the "floor" of the last 30 days
- It's a "cheap" price
- Strategy says: "Opportunity! Buy!"

**Classic Line**:
> "Current normalized value 0.15, below buy threshold of 0.2, bottom fishing!"

---

## 4. Exit Logic: Two Ways to Take Money and Run

### 4.1 First Way: Make 18% and Run

The happiest ending:
```
Buy at 100
Target at 118
Reached → See ya!
```

### 4.2 Second Way: Price Reverts to High

Normalized price went up (e.g., from 0.1 to 0.85):
```
Buy normalized value: 0.1 (floor)
Sell normalized value: 0.85 (near ceiling)
→ Price returned to high, exit!
```

**Plain English**: Buy at the floor, sell near the ceiling — that's the essence of mean reversion!

---

## 5. The Strategy's "Personality Traits"

### Advantages (The Praise Section)

1. **Simple and Clear**: Unlike Nostalgia with its 39 entry conditions, this strategy has just one core concept — normalized score!
2. **Strong Universality**: Whether Bitcoin at 60k or Dogecoin at 0.1, after normalization both are 0-1, treated equally!
3. **Logic Makes Sense**: Mean reversion is a classic financial market phenomenon, not random guessing
4. **Low Trading Costs**: Infrequent trading saves on fees

### Limitations (The Roast Section)

1. **No Stop-Loss**: -99% stop-loss is basically non-existent! Extreme markets can make you question your life 🫠
2. **Few Signals**: Extreme prices don't appear often, might not trade for half a month
3. **Afraid of Trends**: If you encounter a one-sided bull or bear market, mean reversion strategy becomes a contrary indicator
4. **All or Nothing**: Either makes 18% or... hard to find middle ground

---

## 6. When to Use It?

| Market Environment | Recommendation | Plain English |
|-------------------|----------------|---------------|
| Wide Ranging | StarsStarsStarsStarsStars | Paradise! Price bounces between ceiling and floor |
| Sideways Consolidation | StarsStarsStarsStars | Not bad either, suitable for range trading |
| Slow Bull | StarsStarsStars | Catches pullbacks but may miss the main rally |
| Slow Bear | StarsStars | Price keeps dropping, normalization parameters may fail |
| Extreme Volatility | Stars | Disaster! Range broken, strategy logic collapses |
| One-Sided Trend | Don't Use | Don't! Mean reversion won't happen in trends |

**One-Line Summary**: This strategy specializes in ranging markets, and takes a nap when trends arrive!

---

## 7. Bottom Line: How's This Strategy Really?

### One-Word Verdict
> "Clear logic, simple design, but stop-loss is too wild — either makes money and runs, or holds on to the bitter end!"

### Who Should Use It?
- Veterans who can withstand large drawdowns
- Believers in mean reversion
- People with patience to wait for signals
- Trading pairs in a ranging period

### Who Should NOT?
- Beginners (no stop-loss = giving away money)
- Risk-averse people
- People who want to trade daily for excitement
- People with small capital who can't handle volatility

### My Advice
1. **Modify the stop-loss**: -99% is too wild, change it to -10% or -15% for sanity
2. **Add a trend filter**: Pair with EMA, don't fight strong trends
3. **Lower the take-profit target**: 18% is a bit high, consider around 10%
4. **Backtest before live trading**: Don't use real money right away, check historical performance first

---

## 8. What Markets Does This Strategy Make Money In?

### 8.1 Core Logic: Scoring, Bottom Fishing, Top Picking

NormalizerStrategy's core is **normalization** — turning prices into 0-100 scores.

**Money-Making Philosophy**:
- Price won't stay at extreme positions forever
- Buy near 0, sell near 100
- Making money from "reversion"

**Analogy**:
> Like stock trading, can't have daily limit up every day, can't have daily limit down every day.
> After a slump it'll rebound, after a rally it'll pull back.
> This strategy capitalizes on this pattern!

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---|:---|
| Wide Ranging | StarsStarsStarsStarsStars | Paradise! Price bounces within range, strategy is like picking money |
| Narrow Ranging | StarsStarsStars | Usable but limited profit potential |
| Slow Bull | StarsStarsStars | Catches pullbacks but may miss the main move |
| Slow Bear | StarsStars | Price keeps making new lows, normalization range fails |
| Extreme Volatility | Stars | Disaster! Range broken, floor has a basement below it |
| One-Sided Trend | Don't Use | Strategy logic completely unsuitable |

**One-Line Summary**: Ranging markets are its home turf, trends are its nightmare!

---

## 9. Want to Run This Strategy? Check These Configs First

### 9.1 Normalization Parameter Settings

| Config Item | Recommended Value | Commentary |
|-------------|-------------------|-------------|
| Normalization period | 30-50 candles | Too short is unstable, too long is slow to react |
| Buy threshold | 0.15-0.25 | Buy only when score below 15-25, extreme enough! |
| Sell threshold | 0.75-0.85 | Run when score above 75-85, not greedy |

### 9.2 Risk Control Configuration (Important!)

```yaml
# Strongly recommend modifying this
stoploss: -0.10  # Change to -10%, don't use original -99%!
minimal_roi: {"0": 0.10}  # 10% take-profit, more realistic than 18%

# Position control
max_open_trades: 2  # Don't open too many positions
stake_amount: 100   # Fixed amount, don't go all-in
```

### 9.3 Hardware Requirements (Very Friendly!)

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|-------------|
| 1-5 pairs | 1GB | 2GB | Silky smooth |
| 5-20 pairs | 2GB | 4GB | No problem |
| 20+ pairs | 4GB | 8GB | Very stable |

**Good News**: This strategy's computational demand is super low, a VPS costing a few hundred per year can run it, unlike those heavyweight strategies with 100+ conditions!

### 9.4 Backtest vs. Live Trading

**Backtest looks great**: Historically, extreme prices always revert...

**Live Trading Pitfalls**:
- Real-time calculated normalization range may be unstable
- In extreme markets, the floor has a basement below it
- When liquidity dries up, you can't even sell

**Recommended Process**:
1. Backtest to see historical performance
2. Paper trade for one month
3. Small capital live test
4. Scale up after confirming viability

**Don't go all-in right away**, even the best strategy needs a磨合 period!

---

## 10. Easter Egg: The Strategy Author's "Little Tricks"

Look closely at this strategy's design and you'll find some interesting things:

1. **Pursuing Simplicity**
   > "I'm not doing all those fancy things, just one normalization, simple enough, right?"

2. **Extremely Tolerant Stop-Loss**
   > "I believe mean reversion will definitely happen, why set a stop-loss? Hold on!" — but might hold all the way to zero 😅

3. **High Target Profit**
   > "Either don't make money, or make one big score!" — 18% target is indeed aggressive

4. **Not Afraid of Trouble Design**
   > Turns prices into scores, uses math to quantify "expensive" and "cheap", way more reliable than gut feeling

---

## 11. The Very End

### One-Word Verdict
> "Simple and powerful, clear logic, but risk management is too aggressive — if you want to use it, definitely adjust the stop-loss!"

### Who Should Use It?
- Quantitative beginners (logic is simple, easy to understand)
- Traders in ranging markets
- Believers in mean reversion
- People with patience to wait for signals

### Who Should NOT?
- Beginner newbies (no stop-loss = seeking death)
- People seeking high-frequency trading
- People who can't sleep when seeing floating losses
- People in one-sided trending markets

### Manual Trader Advice

If you're trading manually instead of using Freqtrade, this strategy's approach is also worth learning:

1. **Learn to score prices**: Use normalization to judge current price's relative position
2. **Trade extreme values**: Consider buying when score is too low, consider selling when too high
3. **Must set stop-loss**: Don't copy the -99%, stop-loss is a lifeline for manual trading
4. **Combine with trend judgment**: Don't short when major trend is up, and vice versa

---

## 12. Classic Lines Collection

> **When Buying**: "Current normalized value 0.12, below buy threshold of 0.2, bottom fishing near the floor!"

> **When Selling**: "Normalized value surged to 0.82, near the ceiling, retreat!"

> **When in Drawdown**: "Mean reversion will definitely happen... right?" 🫠

> **When Taking Profit**: "18% in the bag, steady as a rock!" 💰

---

## 13. Final Warning (Must Read!)

### Backtests Look Great, Live Trading Requires Caution

NormalizerStrategy may perform well in historical backtesting — because historically, prices do mean revert. But there's a trap:

> **Past reversion doesn't guarantee future reversion!**

Simply put: **What history tells you as the "answer", the exam might not test!**

### Hidden Risks of Extremely Wide Stop-Loss

The original strategy's -99% stop-loss sounds scary:

- **Extreme markets**: One-sided crash may really result in -99% loss
- **Zero risk**: Some altcoins may go to zero, not even a chance to stop-loss
- **Psychological pressure**: Holding through drawdowns isn't something just anyone can handle

### This Strategy's Hidden Pitfalls

Although this strategy looks simple, it has traps:

- **Range failure**: After violent swings, the original price range is broken, normalization parameters need recalibration
- **Few signals**: May go weeks without a single trade signal, low capital utilization
- **Trend risk**: Mean reversion becomes a contrary indicator in one-sided trends

### My Advice (Sincere Words)

```
1. Modify the stop-loss! Change to -10% to -15%, don't use -99%!
2. Lower the take-profit target, 10% is already pretty sweet
3. Add a trend filter, don't fight strong trends
4. Test with small capital first, don't go all-in right away
5. Check strategy performance regularly, stop if something's off
```

**Remember**: No matter how good a strategy is, the market doesn't give warnings. Test with light positions, staying alive is what matters! 🙏

**Last Words**: Normalization is a good idea, but risk management is the key to profitability. Don't let "mean reversion" become "mean to zero"! 💀

---

**Final Reminder**: The strategy is just a tool, risk management is king. Stay alive to make money, dead means nothing. Happy trading! 🚀
