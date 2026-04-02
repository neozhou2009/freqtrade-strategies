# ClucHAwerk Strategy: The "Tai Chi Master" on Bollinger Bands

> **Nickname**: Tai Chi Master, Average Candle Sect Founder
> **Profession**: Short-Term Trend Pullback Hunter
> **Timeframe**: 1 Minute (main) + 1 Hour (trend filter)

---

## 1. What's This Strategy?

The name ClucHAwerk sounds weird, but it's actually a **double combo**:
- **Cluc**: From a classic strategy series, skilled at Bollinger Band operations
- **HA**: Heikin Ashi (Average Candles), a special candle smoothing technique

Simply put, **ClucHAwerk** is:
- 🥋 Uses **average candles** to filter noise and see the "real" trend direction
- 📉 On the premise that the trend is upward, waits for price to **pull back to the Bollinger lower band**
- 🎯 When a reversal signal appears, **bottom-fishes the buy**
- 🏃 When price rises to the middle band or the trend weakens, **bails out fast**

It's like **Tai Chi pushing hands** — no head-on collisions, waits for the opponent to exhaust their force and lose balance, then uses their momentum against them 🤣

**One-Line Summary**:
> "Trend upward, buy on pullback, make a profit and run, never be greedy."

---

## 2. Core Settings: Basically "Fast In, Fast Out + Multi-Layer Protection"

### Take-Profit Rules (ROI Table)

| Holding Time | Min Profit Target | Plain English |
|-------------|------------------|---------------|
| 0 minutes | 11.054% | If it instantly rises 11% after buying, bail |
| 2 minutes | 5.569% | Held 2 minutes, 5.5% is enough |
| 10 minutes | 3.055% | Held 10 minutes, 3% is fine to exit |
| 16 minutes | 2.311% | Held 16 minutes, 2% works too |
| 82 minutes | 1.267% | Held over an hour, 1% |
| 238 minutes | 0.301% | Held almost 4 hours, 0.3% also exits |
| 480 minutes+ | 0% | Held over 8 hours, no hard take-profit anymore |

**Translation**: Initially targeting 11%, but if the market doesn't cooperate, the target drops the longer you hold. Like **dinner** — when the food arrives you want a full course, but once you've waited long enough, just getting full is fine 🍜

### Stop-Loss Rules

| Stop-Loss Type | Trigger | Plain English |
|---------------|---------|---------------|
| Fixed Stop-Loss | Loss -2.139% | Exit after 2% loss, never hold losers |
| Trailing Stop | Activates after 9.291% profit | Starts protecting profit around 10% |
| Trailing Trigger | Pulls back 10.651% from high | Sell if profit retreats more than 10% |

**Translation**: The stop-loss is extremely tight (only 2%) — this is a **high-frequency short-term strategy**, emphasizing fast in, fast out.

### Variant Versions

ClucHAwerk has three "avatars":

| Version | Characteristics | For Who |
|---------|----------------|---------|
| ETH Version | More trades, 64% win rate, breakeven | People seeking stable income |
| BTC Version | Fewer trades, 90% win rate, higher per-trade profit | Steady players |
| USD Version | Fewest trades, 94% win rate, highest per-trade profit | Ultra-conservative |

---

## 3. 2 Entry Conditions: Either One Gets You In

The strategy's entry conditions are cleverly designed — **meeting any one condition triggers a buy**:

### 🎯 Condition A: Rebound After Bollinger Band Contraction (Main Attack)

**Core Logic**: Wait for Bollinger Bands to narrow, then price breaks below the lower band, while the overall trend is still rising — time to bottom-fish.

**Translation into plain English**:
> "Bollinger Bands are compressed like a rubber band → price suddenly breaks below the lower band → but someone catches it below (short lower wick) → major trend is still upward → **Buy it!**"

Requires 7 conditions simultaneously (don't panic, let me simplify):

| Condition | Code Parameter | Plain English |
|----------|----------------|---------------|
| 1-hour trend upward | ROCR > 0.509 | Big picture is fine |
| Bollinger lower band exists | lower.shift(1) > 0 | Has support level |
| Bollinger Band wide enough | bbdelta > 0.01021 × close | Volatility big enough, there's meat to eat |
| Price volatility sufficient | closedelta > 0.00519 × close | People are trading this coin |
| Lower wick short | tail < 0.88118 × bbdelta | Strong buying below |
| Close below previous lower band | ha_close < lower.shift(1) | Dropped to the level |
| Close not higher than yesterday | ha_close ≤ previous close | Still adjusting |

**Classic Line**:
> "Trend still there, pullback complete, someone supporting the bottom — time to get in!"

### 📉 Condition B: Extreme Oversold Rebound (Conservative)

**Core Logic**: Price has fallen too much, volume has shrunk to freezing point — likely to bounce.

**Translation**:
> "Price is below the long-term moving average → fallen below the Bollinger lower band → nobody's selling anymore (volume shrunk) → **Time to bottom-fish, high probability of bounce!**"

Requires 3 conditions simultaneously:

| Condition | Plain English |
|----------|---------------|
| Price below 50-day EMA | In a weak position |
| Price far below Bollinger lower band | Oversold, should bounce |
| Volume significantly shrunk | Selling pressure exhausted |

**Classic Line**:
> "Can't fall further, nothing to sell, bounce is coming, small bet for fun."

---

## 4. Protection Mechanisms: Three-Layer Fuse

Each entry condition has matching protection mechanisms, like **three insurance fuses**:

### 🛡️ First Layer: Trend Filtering

**Check 1-hour ROCR before buying**:
- ROCR > 0.509 to buy → major trend must be upward
- ROCR < 0.953 to sell → major trend starting to weaken

**Plain English**:
> "Don't trade against the trend, follow the trend. If the big picture is bad, even great entry points aren't worth it."

### 🛡️ Second Layer: Fixed Stop-Loss

- Stop-loss line: **-2.139%**
- Extremely tight — strategy **prefers small losses over holding losers**

**Plain English**:
> "Cut losses at 2%, don't try to averaging down. Preserve capital for better opportunities."

### 🛡️ Third Layer: Trailing Stop

- Activation threshold: After **9.291%** profit
- Trigger condition: Pull back **10.651%** from high to sell

**Plain English**:
> "Once you're up more than 9%, start watching closely. If profit retreats more than 10%, lock in gains immediately."

**Commentary**: These three fuses work together quite tightly — essentially eliminating "one trade kills the account" scenarios 🤣

---

## 5. Exit Logic: All Three Must Align

Exit is stricter than entry — requires **all 3 conditions simultaneously**:

### 5.1 The Three Musketeers

| Condition | Code | Plain English |
|----------|------|---------------|
| 1-hour trend weakening | ROCR < 0.95269 | Big picture starting to deteriorate |
| Price rising to middle band | ha_close × 1.01283 > bb_middleband | Rose from bottom to the "ceiling" |
| Volume present | volume > 0 | Not a fat-finger trade |

**Plain English**:
> "Major trend turning bad + price hit Bollinger middle band + volume normal → **Retreat!**"

### 5.2 Exit Philosophy

Why use Bollinger middle band as the take-profit level?

**Middle Band = Bull/Bear Divide**:
- Price below middle band → bearish market
- Price above middle band → bullish market

So the strategy logic is:
> "Bottom-fished from the lower band, risen to the middle — exit now, don't chase the tail."

This is a classic **"eat the body, not the tail"** strategy — steady, but misses some profit.

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Extremely tight stop-loss**: -2% stop-loss, controllable per-loss, won't get crippled in one trade
2. **Multi-layer filtering**: Trend filtering + indicator filtering + volume filtering, high signal quality
3. **Doesn't eat the tail**: Sells at middle band, not greedy, secures profits
4. **Dual entry conditions**: Can catch both trend pullbacks and extreme oversold bounces, wide adaptability
5. **Has variant versions**: ETH/BTC/USD three versions, more targeted

### ⚠️ Cons

1. **All parameters are optimized**: Every number came from Hyperopt runs, may just be "historical coincidence"
2. **Timeframe too short**: 1-minute candles, need constant monitoring, requires low fees
3. **No signals in ranging markets**: When price isn't moving, ROCR hovers in the middle, waiting with no opportunity
4. **High understanding barrier**: Heikin Ashi + Bollinger Bands + ROCR, three-indicator combo, beginners may get dizzy

**Commentary**:
> "Parameters precise to 5 decimal places — I ask you, isn't this overfitting?" 😅

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clearly Rising | ✅ Recommend | Condition A triggers frequently, pullback buying works great |
| Declining Trend | ❌ Don't Use | ROCR filter prevents buys, forced buys get stopped out |
| Sideways Volatility | ⚠️ Use Cautiously | Few signals, fees may eat all profits |
| High Volatility | ✅ Recommend | Bollinger Bands wide enough, conditions easily met |
| Junk Coins | ❌ Don't Use | Easily trapped by manipulators drawing candles |

**Best Environment**:
> "Mainstream coins (BTC/ETH) in upward trend, with some volatility, low fees (like Binance VIP)."

---

## 8. Summary: How Does This Strategy Really Stack Up?

### One-Line Verdict
> "A conservative trend pullback strategy, eats the body not the tail, suitable for patient people who can monitor the screen."

### Who's It For?
- ✅ People with time to monitor the screen (1-minute candles)
- ✅ People trading mainstream coins (BTC/ETH)
- ✅ People seeking stable win rates
- ✅ People with low fees (VIP or rebate)
- ✅ People who can accept 2% stop-loss

### Who's It NOT For?
- ❌ People without time to monitor
- ❌ People who hold losers hoping for recovery
- ❌ People trading junk coins
- ❌ People with high fees
- ❌ People seeking overnight riches

### My Recommendations
1. **Paper trade for one month first**: Don't jump in with real money right away
2. **Prefer the ETH version**: Balances trading frequency and win rate
3. **Don't mess with parameters**: These parameters were optimized, changing may make it worse
4. **Watch the fees**: Hidden cost of high-frequency trading is significant

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Use Average Candles to "See the Truth"

The uniqueness of ClucHAwerk is its use of **Heikin Ashi (Average Candles)**.

Problems with regular candles:
- Too much up-and-down noise
- May look like it's rising when actually it's a bounce in a downtrend
- Easily fooled by false breakouts

Average candle solution:
- "Smooth" the price
- Filter out noise
- Easier to see the real trend

**Plain English**:
> "Regular candles are like wearing glasses with the wrong prescription — everything's blurry; average candles are like getting high-definition lenses — see direction clearly at a glance."

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:------------------------|
| Rising Trend Pullback | ⭐⭐⭐⭐⭐ | Home turf! Waiting for pullback to buy, excellent effect |
| Sideways Volatility | ⭐⭐☆☆☆ | Few signals, might wait all day with no opportunity |
| Declining Trend | ⭐☆☆☆☆ | ROCR filters out most buys, basically doesn't trade |
| High Volatility Surge | ⭐⭐⭐☆☆ | Has opportunities but easily shaken out |

**One-Line Summary**:
> "Trend market body-eater, sideways market fee-contributor."

---

## 10. Want to Run This Strategy? Check These Settings First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Recommended Coins | BTC, ETH | Mainstream coins have better liquidity |
| Timeframe | 1 minute | Must use 1 minute, changing invalidates parameters |
| Informative Period | 1 hour | Trend filtering, don't change |
| Fee Rate | <0.1% | High-frequency trading, fees are a hidden cost |

### 10.2 Hardware Requirements

1-minute candles mean calculations every minute, but computational load isn't too high:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|------------|
| 1-5 pairs | 2GB | 4GB | Smooth |
| 5-20 pairs | 4GB | 8GB | No problem |
| 20+ pairs | 8GB | 16GB | May lag |

**Commentary**:
> "Much more resource-efficient than those strategies with dozens of indicators." 😌

### 10.3 Backtest vs. Live

**Backtest Performance** (historical data):

| Version | # of Trades | Win Rate | Avg Profit |
|---------|-------------|---------|-----------|
| ETH Version | ~1890 | ~64% | 0.86% |
| BTC Version | ~637 | ~90% | 1.69% |
| USD Version | ~730 | ~94% | 2.91% |

**But!** Good backtest doesn't guarantee good live:
- All parameters were optimized, may be **overfitted**
- Live slippage, network delay, exchange restrictions all affect results
- Market environment is changing

**Recommended Process**:
1. Paper trade for 1 month
2. Observe signal quality and actual fills
3. Adjust position sizing
4. Small capital live test
5. Gradually increase position

---

## 11. Bonus: Strategy Author's "Little Tricks"

Look closely at the code and you'll find some interesting things:

### 1. Two Bollinger Band Periods

- Entry uses **40-period** Bollinger Bands → More stable, not easily fooled by false breakouts
- Exit uses **20-period** Bollinger Bands → More sensitive, detects reversals earlier

**Plain English**:
> "Enter slowly, see clearly first; exit quickly, run faster than anyone."

### 2. Two ROCR Periods

- 1-minute ROCR (28 periods) → Short-term momentum
- 1-hour ROCR (168 periods) → Long-term trend

**Plain English**:
> "One telescope to see far trends, one microscope to see short-term fluctuations — perfect team."

### 3. Three Variant Versions

ETH, BTC, USD versions all have different parameters — author **specifically optimized for different coins**:

**Plain English**:
> "Not one-size-fits-all, but tailored tailoring. ETH is volatile so parameters are looser; BTC is less volatile so parameters are tighter."

---

## 12. The Bottom Line

### One-Line Verdict
> "A carefully tuned trend pullback strategy — tight stop-loss, multiple protections, suitable for steady high-frequency traders."

### Who's It For?
- ✅ People with time to monitor
- ✅ People seeking stable win rates
- ✅ People trading mainstream coins
- ✅ People with low fees
- ✅ People who can accept small stop-losses

### Who's It NOT For?
- ❌ People without time to monitor
- ❌ People who hold losers
- ❌ People seeking overnight riches
- ❌ People trading junk coins
- ❌ People with high fees

### Manual Trading Recommendations

If you want to manually execute this strategy without Freqtrade:

1. **Open 1-minute candle chart**: Available on Binance/OKX and other exchanges
2. **Load Heikin Ashi**: Most exchanges support switching candle types
3. **Add Bollinger Bands**: Period 40, std 2 (entry); Period 20, std 2 (exit)
4. **Add ROCR indicator**: Period 28
5. **Add EMA**: Period 50
6. **Wait for signals**: Manually buy when Condition A or B is met
7. **Set stop-loss**: -2% stop-loss, +9% trailing stop

**But honestly**:
> "Manually running a 1-minute strategy is exhausting — recommend using a bot for automation."

---

## ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Be Careful in Live Trading

ClucHAwerk's backtest data looks beautiful — especially BTC version 90% win rate, USD version 94% win rate.

But there's a huge trap here:

> **All entry parameters were Hyperopt-optimized, precise to 5 decimal places!**

What does this mean? These parameters may **perfectly match historical data** but may not work in the future.

Simply put:
> "Like memorizing exam answers — getting 100% on past papers doesn't mean you truly understood. Switch the question format and you might fail." 📝

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Parameter overfitting**: Historical optimum ≠ future optimum
- **Slippage eating profits**: High-frequency trading, 0.1% slippage each time accumulates terrifyingly
- **Exchange restrictions**: API rate limits may cause missing optimal buy/sell points
- **Extreme market failure**: Technical indicators collectively fail during surges/crashes
- **Network delay**: 1-minute candles, seconds of delay may miss signals

### My Recommendations (Sincere Advice)

```
1. Paper trade at least 1 month, confirm signal quality
2. Live trade starting with small capital, like 5%-10% of capital
3. Must factor in fees, find rebate channels
4. Record every trade, review regularly
5. If market environment changes, stop using — don't hold on blindly
6. Never go all-in!
```

**Remember**:
> "Strategy is just a tool — making money depends on discipline and risk management."
>
> "Better to miss an opportunity than make a bad trade. Survival is the top priority." 🙏

**Final Reminder**: No matter how good a strategy is, the market doesn't care. Paper trade with light positions, survival is the top priority!
