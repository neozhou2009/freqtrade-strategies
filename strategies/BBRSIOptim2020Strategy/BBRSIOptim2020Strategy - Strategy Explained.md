# BBRSIOptim2020Strategy: The Daredevil's "Knife-Catcher"

> **Nickname**: The Extreme Bottom-Fisher King  
> **Specialty**: Daredevil member in crash markets  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **BBRSIOptim2020Strategy** is:
- A "gambler" strategy that only strikes during extreme crashes
- Uses 3 standard deviation Bollinger Bands for entry (normal people use 2)
- 33% stop loss, 33.6% first target, all-in style

It's like watching someone jump from the 10th floor and you run to catch them — extremely dangerous, but if you pull it off, you're a hero 💀

---

## II. Core Configuration: Basically "Betting Big on Rebounds"

### Take-Profit Rules (ROI Table)

```
At the start: Get out at 33.6% profit (yes, you read that right, 33.6%!)
After 40 minutes: 7.2% is fine too
After 3.6 hours: 2.1% also acceptable
After 7.6 hours: Break-even is fine
```

**Translation**: This strategy bets on massive rebounds after crashes, so targets are set super high. But if it drags on, lower expectations and take what you can get.

### Stop-Loss Rules

```
Maximum loss: 33.1% (one-third of your capital!)
Trailing stop: ON
```

**Translation**: This stop loss is terrifyingly wide — accept losing one-third before giving up. Either make 33% or lose 33%, it's all or nothing style 😱

---

## III. Entry Conditions: The Daredevil's Ticket

This strategy has **one entry condition**, but it's extremely demanding:

### 🎯 Buy Signal

| Condition | Plain English |
|-----------|---------------|
| Close price < 3 standard deviation Bollinger lower band | Price has crashed to a "statistically almost impossible" level |

**Plain English Translation**:
> "Normal price stays within 3 standard deviations 99.7% of the time. Once it falls outside, it's an extreme anomaly — either an opportunity or a disaster."

**This Strategy's Philosophy**:
- Regular oversold? Not buying!
- Severe oversold? Not buying!
- Extreme crash? **BUY!**

---

## IV. Exit Logic: Take the Money When You Have Enough

### Sell Signal

| Condition | Plain English |
|-----------|---------------|
| Close price > 1 standard deviation Bollinger middle band | Price is back to "normal range" |

**Plain English Translation**:
> "From extreme crash bouncing back to normal levels, close enough, let's get out!"

### Four Layers of Protection (These protections are a bit thin...)

| Exit Method | Trigger Condition | Plain English |
|-------------|-------------------|---------------|
| Signal sell | Price > Middle band | Back to normal |
| ROI take-profit | Lower based on time schedule | Take profits gradually over time |
| Trailing stop | Price drops back | Lock in profits |
| Fixed stop loss | Lose 33.1% | Accept defeat (already lost one-third...) |

---

## V. This Strategy's "Personality"

### ✅ Pros (The Good Stuff)

1. **Few Signals but High Probability**: 3 standard deviation extreme events are rare, but when they happen, bounce probability is high
2. **Clear Target**: 33.6% first target, bold and ambitious
3. **Simple Code**: 70 lines of code, understand at a glance
4. **Trailing Stop Protection**: At least there's a mechanism to lock in profits

### ⚠️ Cons (The Bad Stuff)

1. **Insanely Wide Stop Loss**: 33.1% stop loss, can lose one-third on a single trade!
2. **Too Few Signals**: 3 standard deviation events are so rare, might go a month without a signal
3. **RSI Calculated for Nothing**: Code calculates RSI but never uses it, total waste 🤣
4. **Target Too Hard to Reach**: 33.6% first target is a pipe dream in live trading
5. **High Risk**: Not for the faint-hearted

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|----------------|--------|
| Crash followed by rebound | ⭐⭐⭐⭐⭐ Golden opportunity | This is what the strategy is made for |
| High volatility coins | ⭐⭐⭐☆☆ Can use | More volatility, might get more extreme signals |
| Normal oscillation | ⭐☆☆☆☆ Don't use | Won't touch 3SD lower band at all |
| Single-direction downtrend | ⭐☆☆☆☆ Suicide | Ultimate version of catching falling knives |

---

## VII. Summary: How Good Is This Strategy?

### One-Sentence Verdict
> "Daredevil strategy — either make big money or lose big money. If you have a weak heart, stay away."

### Who Should Use It?
- ✅ Aggressive traders (can handle 30%+ floating losses)
- ✅ Small position testers (use less than 5% of total capital)
- ✅ Crash bottom-fishing enthusiasts (specifically wait for crash opportunities)
- ✅ High-risk high-reward seekers

### Who Shouldn't Use It?
- ❌ Beginners (risk is too high)
- ❌ Conservative traders (30% stop loss is terrifying)
- ❌ People seeking stable returns (too few signals)
- ❌ Large capital traders (absolute loss value would be horrifying)

### My Advice
1. **Use only small positions**: Single trade no more than 5% of total capital, ideally 1%-2%
2. **Pick volatile coins**: Some coins love to crash and surge, more opportunities there
3. **Be mentally prepared**: Floating losses of 20%+ are normal, don't rush to stop out
4. **Combine with other strategies**: Don't put all your capital in this one strategy

---

## VIII. In What Markets Can This Strategy Make Money?

### 8.1 Core Logic: Wait for Extreme Crashes Before Striking

BBRSIOptim2020Strategy is an **extreme event strategy**. Unlike normal strategies that trade frequently, it lies in wait, only striking during extreme crashes.

**Its Money-Making Philosophy**:
> "Statistics tell me the probability of price breaking below 3 standard deviations is only 0.3%. Once it falls outside, it's either a disaster or an opportunity. I'm betting it's an opportunity."

- **3 Standard Deviations**: 99.7% of price fluctuations are inside; falling outside is extreme anomaly
- **High Target Returns**: Since we're betting on extreme events, targets are set high too
- **Forgiving Stop Loss**: Gives extreme volatility enough room, won't get shaken out by normal fluctuations

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Strong Uptrend | ⭐☆☆☆☆ | Price keeps going up, no signals at all, strategy sleeps |
| 🔄 Normal Oscillation | ⭐⭐☆☆☆ | Normal volatility won't touch 3SD, keeps sleeping |
| 📉 Crash Bounce | ⭐⭐⭐⭐⭐ | Home turf! Crash triggers Bollinger band, bet on big rebound |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | High volatility means extreme signals, but real vs fake hard to tell |

**One-Sentence Summary**: This strategy is a "specialist" for crash markets — usually dormant, comes alive during crashes.

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Notes |
|--------------------|-------------------|-------|
| Timeframe | 5m (default) | Short period to catch rebounds |
| Stop loss | -0.2 ~ -0.33 | Depends on how strong your heart is |
| Per-trade position | ≤5% | STRONGLY recommend no more than 5%! |
| Max positions | 1-2 | Don't catch too many falling knives at once |

### 9.2 Configuration File Key Settings

```yaml
# config.json key items
"timeframe": "5m",
"stake_currency": "USDT",
"stake_amount": 50,           # Fixed amount, don't use unlimited!
"max_open_trades": 2,         # Maximum 2 at a time
"stoploss": -0.331            # Default stop loss
```

### 9.3 Hardware Requirements (Relaxed)

Simple strategy, low hardware requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Old computers can run it |
| 10-50 pairs | 4GB | 8GB | No pressure at all |
| 50+ pairs | 8GB | 16GB | Runs easily |

**Comment**: High-risk strategy, but at least it doesn't eat up your machine 😅

### 9.4 Backtesting vs Live Trading

**Watch Out for Differences**:
- Extreme events in backtesting might be more or less frequent than live (depends on historical data)
- 33.6% first target is rarely achieved in live trading
- 33.1% stop loss really tests your nerves in live trading
- During extreme crashes, liquidity is poor, high slippage

**Recommended Process**:
1. Paper trade for at least 1 month, observe signal frequency
2. Start with small capital (recommend less than 5% of total)
3. Be mentally prepared for floating losses, don't change strategy mid-way
4. Record every trade, analyze characteristics of extreme events

**Don't go all-in right away** — this strategy can really lose 33%!

---

## X. Bonus: The Strategy Author's "Little Secrets"

Looking at the code carefully, you'll find some interesting things:

1. **RSI calculated but not used**
   ```python
   dataframe['rsi'] = ta.RSI(dataframe)  # Calculated
   # But never used in buy/sell conditions... 😅
   ```
   > "I calculated RSI, but you don't have to use it. Maybe later?" — Author probably thought this

2. **Profit targets precise to one decimal place**
   ```python
   minimal_roi = {
       "0": 0.336,  # Why 33.6%? Maybe optimized from backtesting
   }
   ```
   > "Precise numbers from backtesting optimization, believe it or not"

3. **Stop loss and first target almost equal**
   ```python
   stoploss = -0.331    # Stop loss 33.1%
   # First target 33.6%
   ```
   > "Either make 33.6% or lose 33.1%, this gamble's risk-reward ratio... 1:1?"

---

## XI. The Final Word

### One-Sentence Verdict
> "Extreme event gambler strategy. Small positions betting on crash rebounds, large positions are suicide."

### Who Should Use It?
- ✅ Aggressive traders
- ✅ People who can handle 30%+ floating losses
- ✅ Small position testers
- ✅ Crash market enthusiasts

### Who Shouldn't Use It?
- ❌ Beginners
- ❌ Conservative investors
- ❌ People with weak hearts
- ❌ People seeking stable returns
- ❌ People with large capital

### Manual Trading Recommendations

If you're not using a quantitative bot and want to execute this strategy manually:
1. Open TradingView, set up Bollinger Bands (20, 3)
2. Switch to 5-minute chart
3. Wait for price to break below 3 standard deviation lower band
4. Enter, set 33% stop loss (scary, right?)
5. Target return to 1 standard deviation middle band or trigger ROI
6. **Keep position under 5% of total capital!**

---

## XII. ⚠️ Risk Re-emphasis (Read This Section!)

### Backtesting is Beautiful, Live Trading Requires Caution

BBRSIOptim2020Strategy has much higher risk than typical strategies:

> **33% stop loss means: A single trade can lose one-third!**

If you use 10% position size, one loss is 3.3% of total capital.
If you use 50% position size, one loss is 16.5% of total capital.
If you go all-in... 😱

### Hidden Risks of Extreme Strategies

In live trading, watch out for:
- **Liquidity risk**: During extreme crashes, liquidity might dry up, can't sell when you want to
- **Slippage risk**: During extreme markets, bid-ask spreads are huge, actual fills are far from expected
- **Psychological pressure**: How does watching 20%, 30% floating loss feel? Can you hold on?
- **Extreme doesn't mean rebound**: Sometimes extreme crashes are just the beginning of even worse crashes

### My Advice (For Real)

```
1. Single position no more than 5% of total capital
2. Maximum 1-2 positions at the same time
3. Be mentally prepared for 30% floating loss
4. Don't fight true disasters (like exchange bankruptcies)
5. Set a total stop, like stop the strategy after 3 consecutive losses
```

**Remember**: This strategy catches falling knives. Catching one feels great, but knives can also pierce right through you. Survival is most important! 🙏

---

**Final Reminder**: The strategy name has "Optim" (optimized) and "2020", possibly meaning the author optimized it for 2020 market conditions. Markets change, parameters might need to change too. Don't blindly trust backtesting results!