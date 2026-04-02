# SmoothScalp Strategy: The "Take the Money and Run" Scalper

> **Nickname**: King of Oversold Bottom-Fishing  
> **Profession**: 1-Minute Short-Term Scalping Specialist  
> **Timeframe**: 1 minute (1m)

---

## I. What Is This Strategy?

Simply put, **SmoothScalp** is:
- Specifically looking for "over-dropped" moments to bottom-fish
- Take 1% profit and run, never greedy
- Needs to trade dozens of coins simultaneously, winning by volume

Like **waiting at the supermarket entrance for discounts, grabbing a small deal and immediately reselling it** 🤣

---

## II. Core Configuration: Simply Put, "Take 1% and Run"

### Take-Profit Rule (ROI Table)

```
As soon as you open a position, target 1% profit
Make enough, run, never linger
```

**Translation**: This strategy is a "cigarette butt picker" - only makes a little on each trade, but takes it and runs.

### Stop-Loss Rule

```
Only stop-loss when loss exceeds 10%
```

**Translation**: Wait, 10% stop-loss? Isn't this a scalping strategy? Stop-loss is 10 times larger than take-profit?

> Yep, that's the most nerve-wracking part of this strategy.

---

## III. Buy Conditions: 5 Gates, Can't Enter Without Passing All

This strategy's buy conditions are extremely strict - 5 conditions must **all be met simultaneously**:

### 🎯 Single Entry Signal (All 5 conditions required)

**In plain English**:
> "I want to wait until price breaks below short-term MA, trend is strong enough, money outflow is sufficient, stochastic golden cross, AND CCI extremely oversold - then I buy!"

**Translated to human language**:

| Condition | Code | Plain English |
|------|------|--------|
| Price Position | `open < ema_low` | Opening price fell below moving average |
| Trend Strength | `adx > 30` | Market has clear direction, not oscillating randomly |
| Money Flow | `mfi < 30` | Money outflow is enough, time to rebound? |
| Stochastic | `fastk < 30 & fastd < 30 & golden cross` | Stochastic also bottom golden cross |
| Oversold Degree | `cci < -150` | CCI extremely oversold (more extreme than normal oversold) |

**Rant**:
> If all 5 conditions are met, basically it's a "can't fall any further" state. Problem is - can't fall any further doesn't mean it won't keep falling 😅

---

## IV. Sell Logic: Two Paths, Same Destination

### 4.1 Exit Paths

**Path A: Back to MA High**
> Opening price >= EMA high AND CCI > 150

**Plain English**:
- "Price climbed back to short-term MA high, and CCI shows overbought - time to go!"

**Path B: Stochastic Overbought**
> fastk crosses above 70 OR fastd crosses above 70, AND CCI > 150

**Plain English**:
- "Stochastic rushed into overbought zone (>70), and CCI also overbought - running, running!"

### 4.2 Sell Signal Summary

| Sell Signal | Trigger Condition | Plain English |
|---------|---------|--------|
| #1 | Back to MA high + overbought | Rose enough, time to lock in profits |
| #2 | Stochastic overbought + overbought | Indicators all screaming overbought, still not running? |

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **High Signal Quality**: 5-fold AND condition filters most noise
2. **Simple Clear Logic**: Just oversold rebound, easy to understand
3. **Fast Action**: 1-minute timeframe, fast capital turnover
4. **Visually Friendly**: Reserved Bollinger, MACD, RSI for easy chart reading

### ⚠️ Cons (Rant Time)

1. **Absurd Risk-Reward Ratio**: 1% take-profit, 10% stop-loss - one loss wipes 10 wins
2. **Stop-Loss Too Loose**: Using 10% stop-loss for scalping is like "using a cannon to swat a mosquito"
3. **Extremely High Win Rate Required**: Needs 90%+ win rate to offset single large stop-loss
4. **Fee Killer**: High-frequency trading, fees will eat significant profits
5. **Needs Multi-Coin Parallel**: Single coin risk too high

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| Uptrend Pullback | ✅ Use | High ADX + oversold rebound = Best scenario |
| Sideways Ranging | ⚠️ Use Less | ADX filter will limit signals |
| One-way Decline | ❌ Don't Use | Oversold can become more oversold |
| High Volatility Coins | ✅ Use | Many overbought/oversold opportunities |

---

## VII. Conclusion: How's This Strategy Really?

### One-Sentence Verdict
> "Take 1% and run, stop-loss at 10% - either you're a god-tier bottom fisher, or you're sending money to the exchange"

### Who Should Use It?
- ✅ Veterans with 60+ trading pair resources
- ✅ Low fee platform users
- ✅ People who can accept high-risk high-reward
- ✅ Those who've backtested and confirmed high win rate

### Who Shouldn't Use It?
- ❌ Small retail traders playing just a few coins
- ❌ High fee rate platforms
- ❌ People seeking stable returns
- ❌ Manual traders (can't handle 1-minute timeframe)

### My Recommendations
1. **Adjust Stop-Loss**: 10% is too large, consider 3-5%
2. **Parallel Positions**: At least 60 trading pairs
3. **Backtest Verification**: Must verify win rate can reach 80%+
4. **Watch Slippage**: Scalping is extremely sensitive to slippage

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Oversold Bottom-Fishing

SmoothScalp is a typical representative of **scalping ecosystem**. Less than 100 lines of code, clean and clear.

**Its Profit Philosophy**:
- When it falls too much, it will rebound
- When trend exists, oversold is more reliable
- Take a little and go, never greedy

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Uptrend Pullback | ⭐⭐⭐⭐⭐ | Big trend up, oversold rebound most reliable |
| 🔄 Sideways Ranging | ⭐⭐☆☆☆ | ADX filter reduces signals, but quality still okay |
| 📉 One-way Decline | ⭐☆☆☆☆ | Oversold can get more oversold, bottom-fishing at halfway point |
| ⚡️ High Volatility | ⭐⭐⭐⭐☆ | Many overbought/oversold opportunities, rich signals |

**One-Sentence Summary**:
> "Only in trending oversold rebound markets can this strategy truly shine. Ranging and plunging markets, it can't handle."

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Rant |
|--------|--------|------|
| Simultaneous Positions | ≥ 60 | Less is gambling, more is investing |
| Trading Pair Selection | High liquidity | Scalping needs deep order books |
| Fee Rate | ≤ 0.1% | Above this, profits eaten by fees |

### 9.2 Hardware Requirements (Important!)

This strategy may have simple code, but 1-minute timeframe + 60+ trading pairs has hardware requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 60 pairs | 4GB | 8GB | Usable |
| 100+ pairs | 8GB | 16GB | Smooth |

### 9.3 Backtest vs. Live Trading

**Backtest Might Show**:
- 85%+ win rate
- 200% annual return

**Live Trading Might Encounter**:
- Slippage eats 0.5%
- Fees eat 0.2%
- Insufficient liquidity causes execution difficulty

**Recommended Process**:
1. First backtest 1+ year of data
2. Paper trade for 1-2 weeks
3. Small position live test
4. Gradually increase position after confirmation

**Don't go all-in from the start** - scalping strategies look simple but are actually treacherous!

---

## X. Bonus: Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Reserved a bunch of indicators but didn't use them**: RSI, Bollinger, MACD all calculated
   > "Maybe reserved for future extension, or copied from other strategies 😂"

2. **EMA used three lines**: high, close, low each with one line
   > "Opening price compared to EMA low, closing price compared to EMA high - this design is interesting"

3. **CCI threshold extremely extreme**: < -150 to buy, > 150 to sell
   > "Normal strategies use -100/100, this strategy uses -150/150 - pursuing extreme oversold"

---

## XI. Finally, Finally

### One-Sentence Verdict
> "The extreme sport of scalping - make small money fast, lose big money slow. For high-frequency players, not for the faint-hearted."

### Who Should Use It?
- ✅ Enough trading pair resources
- ✅ Low fee platform users
- ✅ Can accept high-frequency trading risk
- ✅ Sufficient hardware support

### Who Shouldn't Use It?
- ❌ Only playing a few coins
- ❌ High fee rate platforms
- ❌ Seeking stable low-risk returns
- ❌ Manual traders

### Manual Trader Advice
**Don't try**. 1-minute timeframe + 60+ trading pairs, manual operation is unrealistic.

---

## XII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtest Is Beautiful, Live Trading Needs Caution

SmoothScalp's historical backtest performance might be **very impressive** - but there's a trap:

> **Because 1% take-profit + multi-condition filtering, the strategy easily performs well on historical data, but this doesn't guarantee future profitability.**

Simply put: **Historical record is King rank, live trading might drop to Bronze.**

### Hidden Risks of Scalping Strategies

In live trading, you might encounter:
- **Slippage erodes profits**: 1% profit, 0.3% slippage, actually only 0.7%
- **Fees unbearable**: Every trade has fees, adds up to big money in high frequency
- **Liquidity issues**: Small coins have shallow order books, can't buy when want to buy, can't sell when want to sell
- **Single stop-loss fatal**: 10% stop-loss once triggered, needs 10 profitable trades to recover

### My Recommendations (Real Talk)

```
1. Adjust stop-loss to 3-5%, don't use 10%
2. Ensure fee rate ≤ 0.1%
3. Only run on high liquidity trading pairs
4. If backtest win rate doesn't reach 85%, don't go live
5. Paper trade first, then small position test
```

**Remember**: Scalping strategies look simple, but are the most sensitive to trading costs. Fees, slippage, liquidity - any small issue can eat your profits.

---

**Final Reminder**: No matter how good the strategy, when the market teaches you a lesson, it won't give notice. Light position testing, survival is most important! 🙏