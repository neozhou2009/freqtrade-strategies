# ClucFiatSlow Strategy: The "Steady Swing Trading Hunter"

> **Nickname**: Big Slow Brother, Steady-Earnings-Seeker  
> **Profession**: Mid-to-low frequency swing trader  
> **Timeframe**: 15 Minutes (15m)

---

## 1. What's This Strategy?

In simple terms, **ClucFiatSlow** is a:
- Strategy that watches the market on **15-minute candles** (3× slower than 5-minute, more steady)
- Specifically **ambushes at places where Bollinger Bands compress**
- **Catches a wave after price breaks out** then runs
- Can **hold positions for an entire day** without rushing

Like a **patient old hunter** — sets up near where prey might appear, doesn't rush, waits for the perfect moment, then takes the shot 🎯

The "Slow" in the name is its personality: **not chasing speed and precision, but steady and gradual earnings!**

It's the "slow big brother" of ClucFiatROI. The two siblings: one impatient (5-minute) and one patient (15-minute), but both share the core Bollinger Band breakout logic.

---

## 2. Core Settings: "Take Profits When You Can, Cut Losses When You Must"

### Take-Profit Rules (ROI Table)

```
Hold Time        Target Profit
──────────────────────────────────
0 minutes        3.56%      ← Buy and immediately take this, then run
15 minutes       2.99%      ← Held for a quarter-hour, expectations lower
30 minutes       1.85%      ← Half an hour passed, lower expectations
60 minutes       1.32%      ← One hour, expectations dropping
180 minutes      0.90%      ← Three hours, expectations dropping
360 minutes      0.50%      ← Six hours, expectations dropping
720+ minutes     0%         ← After 12 hours, all the way down to trailing stop
```

**Translation**: **The sooner you make money, the better. But the good news is, you can hold for a whole day!**

### Stop Loss Rules

```
Hard stop: -25.20% (admit defeat after losing a quarter)
Trailing stop: Activates when profit exceeds 2.58%, locks in 0.91% profit
```

**Translation**:
- **Down 25%?** Fine, this trade didn't work out, retreat!
- **Up more than 2.58%?** Alright, switch to "protect the spoils" mode, at least lock in 0.91%!

---

## 3. Two Types of Entry Conditions: Categorized for You

This strategy's entry conditions fall into two big categories, like dating has "chasing new" vs. "adding to what you've got":

### Type 1: New Position Entry (Must satisfy a bunch of conditions)

**Prerequisite**: Fisher RSI < -0.88923 (market has been beaten down enough, in oversold territory)

Then satisfy **EITHER Group A OR Group B**:

**Group A: Bollinger Band Narrowing Breakout**
> "I noticed the Bollinger Band is starting to compress, price breaks below the lower band, and the lower wick is short — this means seller momentum is weakening, here's an opportunity!"

**Plain English translation**:
- Bollinger Band width is large enough (room for volatility)
- Close breaks below the lower Bollinger Band (it's cheap)
- Lower wick is short (weak seller support, may rebound)
- Price has a clear movement (not dead flat)

**Group B: Trend Pullback**
> "Price is already way below the 72-period EMA, and volume has contracted — this low-volume decline is probably a fake-out, rebound opportunity incoming!"

**Plain English translation**:
- Price below long-period moving average (fallen a lot)
- Volume contracted (no more sellers, may rebound)
- Price deep in the lower Bollinger Band region (oversold)

---

### Type 2: Adding to an Existing Position (Simple and brutal)

If you're already in a position, entry conditions become simpler:

> "Price is rising and the trend is confirmed upward — add more!"

**Plain English translation**:
- Close above previous candle (price is up)
- Close above SAR indicator (uptrend confirmed)

**This logic is similar to**: Already bought this stock, see it still rising, so you buy more!

---

## 4. Protection Mechanisms: Three "Safety Belts"

Every entry action has protection measures, like buckling your seatbelt when driving:

| Protection Type | Effect | Plain English |
|----------------|--------|---------------|
| Buy order timeout | Cancel buy order when price surges 1%+ | "Price jumped after I ordered, this one doesn't count" |
| Sell order timeout | Cancel sell order when price drops 1%+ | "Price crashed after I ordered, this one doesn't count" |
| Volume filtering | Only buy when volume is below 24× the average | "Too much volume means too crazy, don't chase" |

**Commentary**: This strategy is quite cautious — it'd rather miss an opportunity than make a mistake 🤣

---

## 5. Exit Logic: More Sophisticated Than Entries

### 5.1 Tiered Take-Profit: How Much to Take and Run

This strategy's take-profit design is very human-friendly:

| Hold Time | Target | Mindset |
|-----------|--------|---------|
| 0 minutes | 3.56% | Made this much right after buying? Run immediately! |
| 15 minutes | 2.99% | Held for a quarter-hour, not bad |
| 30 minutes | 1.85% | Half an hour passed, lower expectations |
| 1 hour | 1.32% | Been holding a while, good enough |
| 3 hours | 0.90% | Time to think about retreating |
| 6 hours | 0.50% | Getting long in the tooth |
| 12+ hours | 0% (rely on trailing stop) | Whatever happens, happens |

**Plain English**:
- **Made 3.5% right after buying?** Awesome, run!
- **Still under water after half a day?** Forget it, let the trailing stop handle it.

### 5.2 Trailing Stop: Protecting Your Winnings

```
Trigger: Profit exceeds 2.58%
Stop position: Lock in 0.91% profit
```

**Plain English**:
> "Up more than 2.58%? Alright, activate survival mode! If price pulls back, I still get to keep 0.91%."

**Example**:
- You buy at $10, price rises to $10.30 (3% profit)
- Trailing stop activates, stop line set at $10.09 (locking in 0.9% profit)
- If price continues to $10.50, stop line moves up to $10.45
- If price drops back to $10.45, stop triggers and you still pocket 4.5%

### 5.3 Exit Signals

The strategy will actively exit when:
- Close price near Bollinger middle band (price has recovered)
- 9-period EMA starting to turn down (short-term trend weakening)
- Fisher RSI enters overbought zone (gotten too bullish)
- Volume present (not a dead calm)

**Plain English**:
> "It's climbed back to the middle of the Bollinger Band, moving averages are starting to turn, momentum indicator says it's overbought — good enough, take the money and run!"

---

## 6. Strategy Personality

### Pros

1. **Steady**: 15-minute timeframe, not chasing high frequency, less noise
2. **Patient**: 72-period EMA watches longer-term trends, doesn't chase or panic
3. **Flexible exits**: Tiered ROI + trailing stop combo both protects the floor and chases tops
4. **Adding mechanism**: Simplified conditions when holding, trend-following additions
5. **Long hold time**: Can hold an entire day, suitable for office workers

### Cons

1. **Stop loss too large**: -25.20%, getting stopped out really hurts 🤕
2. **Many parameters**: 6 entry parameters + 2 exit parameters, tuning is a headache
3. **Profit-to-loss ratio challenge**: Take-profit 3.56% vs stop-loss 25.2%, need high enough win rate to profit
4. **Bollinger Band dependency**: May失效 in single-trend markets
5. **Overnight risk**: Long holds mean fear of overnight news

---

## 7. When to Use It

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Volatile markets | Recommended | Bollinger Band compression needs volatility for breakout |
| Ranging markets | Recommended | Price swings up and down, good for catching waves |
| Mildly rising | Somewhat recommended | Can catch swings but may sell too early |
| Single-trend bull | Use with caution | May sell too early and miss big rallies |
| Single-trend bear | Use with caution | Stop loss may get triggered |
| Flat, no movement | Not recommended | No volatility means no signals, just waiting |
| High-frequency trading | Not recommended | 15-minute timeframe isn't fast enough |

---

## 8. Bottom Line: Is This Strategy Any Good?

### One-Line Verdict
> "A steady swing trading hunter, suitable for laid-back traders who don't want to trade frequently."

### Who's It For?
- People who work during the day, watch markets at night
- People who don't want to stare at screens constantly
- People who like swing trading
- People who can stomach larger stop losses

### Who's It NOT For?
- People chasing high-frequency thrills
- People sensitive to stop losses (-25% is no joke)
- People who only want to do short-term scalps
- People who can't handle overnight risk

### My Advice
1. **Test with small capital**: Don't go all-in right away, test the waters first
2. **Watch the Bollinger Bands**: Understand the logic of compression and breakout
3. **Set your stop loss properly**: Be able to handle 25% drawdowns
4. **Manage expectations**: This is a swing strategy, not a get-rich-quick scheme

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Trading Time for Space

ClucFiatSlow is the "steady operator" of the Cluc series. Its money-making philosophy:

> "Ambush where Bollinger Bands compress, eat a wave after breakout, plenty of time, keep a calm mindset."

- **15-minute timeframe**: More stable than 5-minute, less noise
- **72-period EMA**: Watches longer-term trends, doesn't chase or panic-sell
- **24× volume filter**: Relaxed to 24× (vs ROI version's 18×)
- **720-minute holds**: Can hold an entire day without rushing

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| Mildly rising | Good | Can catch swings but may sell a bit early |
| Volatile oscillation | Excellent | Home turf! Bollinger Band breakouts most effective |
| Sustained decline | Poor | Stop loss may get hit, or buying the dip gets caught |
| High-frequency volatility | Moderate | 15-minute timeframe may miss quick moves |
| Consolidation | Poor | Bollinger Bands compress but don't break out, sparse signals |

**One-line summary**:
> "Makes money in volatile oscillation, suffers in single trends, useless in consolidation."

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended | Commentary |
|---------------|-------------|------------|
| Number of pairs | 5-15 | Diversify risk, don't put all eggs in one basket |
| Per-trade capital | 3-5% | Control risk exposure under 25% stop loss |
| Backtest period | ≥3 months | Ensure coverage of multiple market states |
| Parameter optimization | Quarterly | Re-optimize regularly, don't slack off |

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 1-5 pairs | 2GB | 4GB | Smooth |
| 5-15 pairs | 4GB | 8GB | Comfortable |
| 15-30 pairs | 8GB | 16GB | Don't skimp on this |

**Warning**: This strategy's computational load is manageable, but running too many pairs will still lag 😅

### 10.3 Backtesting vs. Live Trading

**Backtesting looks great, but live trading needs caution**:
- Backtesting can't simulate slippage and liquidity issues
- Historical data doesn't include all black swan events
- Parameters may be overfitted

**Recommended process**:
1. Historical backtesting (≥3 months)
2. Paper trading (≥1 month)
3. Small-capital live trading (≤10% of capital)
4. Gradually increase position size

**Don't go all-in right away**, even the best strategy needs a磨合 period!

---

## 11. Bonus: The Strategy Author's "Little Tricks"

Looking closely at the code, you can spot some fun design choices:

1. **Fisher transformation**: Normalizes RSI to [-1,1] range
   > "Don't ask why it's so complicated, it's definitely more 'advanced' than plain RSI..."

2. **Two sets of entry logic**: New position and adding conditions differ
   > "Be cautious the first time, can be more aggressive when adding!"

3. **720-minute ROI goes to zero**: After 12 hours, no more ROI target
   > "Holding this long? Forget it, let the trailing stop handle it, whatever will be will be."

4. **Comparison with ROI version**: Slow version parameters are all more conservative
   > "I'm the steady big brother, that ROI kid is too impulsive!"

---

## 12. The Bottom Line

### One-Line Verdict
> "Top pick for steady operators, suitable for laid-back swing traders."

### Who's It For?
- People who work during the day
- People who don't want to trade frequently
- People who can stomach larger stop losses
- People who like swing trading

### Who's It NOT For?
- People chasing high-frequency thrills
- People sensitive to stop losses
- People who want in-and-out quick trades
- People who can't handle overnight risk

### Manual Trading Tips

If you want to manually learn from this strategy's logic:
1. Watch for 15-minute Bollinger Band compression
2. Wait for price to break below the lower band
3. Confirm volume contraction (possibly a fake-out)
4. Enter with a stop loss (~25%)
5. Consider taking profit near 3.5%
6. If it keeps running, use trailing stop to protect winnings

---

## 13. ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great, But Live Trading Is a Different Beast

ClucFiatSlow's historical backtest may **look good** — but here's the trap:

> **Because parameters were optimized, the strategy easily "fits" the optimal solution for past price movements, but this doesn't guarantee future profitability.**

Simply put: **you memorized the test answers, but the next test has different questions** 😅

### Hidden Risks of Complex Strategies

In live trading, watch out for:
- **Stop loss too large**: -25.2%, one trade could wipe out a quarter of your account
- **Profit-to-loss ratio challenge**: Take-profit 3.56% vs stop-loss 25.2%, need at least 87.7% win rate just to break even (impossible in reality)
- **Parameter sensitivity**: 6 entry parameters may need regular optimization
- **Overnight risk**: Long holds mean fear of overnight news

### My Real Advice

```
1. Test with small capital, don't go all-in
2. Understand the logic behind Bollinger Bands and Fisher RSI, don't follow blindly
3. Set your stop loss properly, 25% is no joke
4. Backtest and optimize parameters regularly, don't slack off
5. Watch market conditions, may need to pause during single-trend markets
```

**Remember**: No matter how good the strategy, the market doesn't care when it comes to teach you a lesson. Test with light positions, staying alive is what matters! 🙏

**Final reminder**:
- This is a swing strategy, not a get-rich-quick scheme
- 15-minute timeframe, not a high-frequency strategy
- 25% stop loss, not a small number
- Many parameters, needs continuous optimization

**Markets have risks, invest with caution. Strategy is for reference only, profits and losses are your own responsibility.**
