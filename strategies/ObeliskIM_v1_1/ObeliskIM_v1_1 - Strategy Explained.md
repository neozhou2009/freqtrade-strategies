# ObeliskIM_v1_1: Plain English Breakdown

## 1. What Is This Strategy?

### Origin Story
The name sounds fancy, but here's how it was born: the author watched a YouTube video about the Ichimoku Cloud, couldn't sleep at 3 AM, and wrote this strategy. So it's an "insomnia + inspiration" creation.

### One-Line Summary
**Wait for a trend to form, then get in; run when the trend dies.**

### What It Trades
Trend-following on 5-minute candles — short-term strategy that might trade several times a day or not at all depending on the market.

### Who Is This For?
- Trend followers who believe "the trend is your friend"
- People who don't like catching falling knives — this only follows established trends
- Those who can handle some drawdowns during ranging periods

---

## 2. How Does It Make Money?

**Core logic**: "Ride the winners, cut the losers."

Steps:
1. **Wait for trend**: Don't move until trend confirms
2. **Trend starts → enter**: Multiple signals confirm trend has begun
3. **Ride the trend**: Hold as long as trend continues
4. **Trend reverses → exit**: Get out fast at the first sign

**Example**: Watching Bitcoin on 5-minute chart:
1. Price oscillating in a range — strategy waits ("waiting for the wind")
2. Suddenly, price breaks the range, indicators say "this up move looks real"
3. Strategy auto-enters long
4. Price keeps climbing, strategy holds
5. Climb slows, momentum fades — strategy exits
6. Locked in a few percent profit

**Why this makes money**: Markets spend most time ranging, but when trends form they tend to continue. This strategy tries to grab that continuation profit.

---

## 3. The Indicators Explained

### EMA Triple (EMA3, EMA5, EMA10)
Three super-short moving averages.

**What's EMA?** Smoothed average price — tells you "what's the recent average price?"

**Why so short?** 5-minute chart = fast moves. Short MAs react quickly.

**How used?** Strategy watches the arrangement:
- EMA3 > EMA5 > EMA10 = short-term trend UP → candidate for buying
- Reversed = short-term trend DOWN → don't buy

### RSI (Defined But Not Used — Funny Story)
The code defines RSI but never actually uses it! Like buying groceries but forgetting to cook. Maybe the author planned to use it, found it didn't help, and left it there.

### Recent High
Records the highest price of the last 12 candles (1 hour). Only buys when current price breaks above this recent high — confirms "this up move is for real, not just noise."

---

## 4. What Is the Ichimoku Cloud?

### One Look = Market State
Japanese invention, name literally means "one lookbalance" — see the whole market at a glance.

### Five Lines

**1. Conversion Line (Tenkan-sen)** — period 20 (strategy's custom, not standard 9)
- Average of highest/lowest of last 20 candles
- Fast-responding short-term trend line

**2. Base Line (Kijun-sen)** — period 60 (not standard 26)
- Average of highest/lowest of last 60 candles
- Slower medium-term trend line

**3. Leading Span A** — (Conversion + Base)/2, shifted right 30 candles
- Upper (or lower) cloud edge

**4. Leading Span B** — period 120, shifted right 30
- Other cloud edge

**5. Lagging Span (Chikou Span)** — current close shifted left 120
- "Look back in time" confirmation line

### The Cloud (Kumo)
The area between Leading Span A and B.

- **Green cloud**: A > B → uptrend
- **Red cloud**: A < B → downtrend

### Strategy's Special: "Strong Green Cloud"
Must satisfy THREE things simultaneously:
1. Cloud is green
2. Conversion Line above Base Line
3. Base Line above the cloud

All three = **very clearly bullish**. This is the strategy's top-tier bull signal.

---

## 5. When Does It Buy? (Six Gates)

Six conditions must ALL pass — like clearing security checkpoints, one fail = no buy.

### Gate 1: Strong Green Cloud
Cloud must be green, Conversion above Base, Base above cloud. "Big trend must be up."

### Gate 2: TK Cross Up
Conversion Line just crossed above Base Line — short-term trend STARTING to turn up. This signal stays valid for 3 candles (the triggering one + 2 more).

### Gate 3: EMA Bullish
EMA3 > EMA5 > EMA10 — short-term momentum all pointing up.

### Gate 4: Bullish Candle
Current candle closed higher than previous candle.

### Gate 5: Broke Recent High
Close price above the 1-hour high.

### Gate 6: No Spike
Price hasn't risen >3.6% in the last 3 candles — not chasing a hot price.

### Real Example
ETH at $1,950 on a 5-minute chart:
1. Cloud green, Conversion above Base, Base above cloud → Gate 1 ✅
2. Conversion just crossed above Base 2 minutes ago → Gate 2 ✅
3. EMA3 > EMA5 > EMA10 → Gate 3 ✅
4. This candle closed higher than previous → Gate 4 ✅
5. Close $1,950 > 1-hour high $1,945 → Gate 5 ✅
6. 3 candles ago was $1,880, rose <4% → Gate 6 ✅

**ALL SIX = BUY!**

---

## 6. When Does It Sell?

Simpler than buying — just two triggers:

**Trigger 1: TK Cross Down**
Conversion crosses below Base — trend might be reversing.

**Trigger 2: Price Below Base Line**
Close drops below the Kijun-sen — trend clearly weakening.

Either one = sell.

### Why So Simple?

1. **Trend reversal = exit fast**: Complex sell logic = slow response = profits given back
2. **Simple = more reliable**: Complicated exits produce false signals
3. **4% stop-loss as backup**: If sell signal is too slow, the stop catches it

### The ROI (Profit Targets)
Stepped approach:
- **Right after buy**: Target 10%
- **30 minutes in, still not at 10%**: Target drops to 5%
- **60 minutes in**: Target drops to 2%

**Meaning**: The longer it takes, the lower your aim. Time = uncertainty = lower expectations. Don't be greedy.

---

## 7. Risk Control: Three Layers

### Layer 1: Strict Entry Conditions
Six gates = inherent risk control. Tighter conditions = higher-quality entries = lower risk of being wrong.

### Layer 2: -4% Stop-Loss
No matter what, if it drops 4% = exit. Hard floor. Never hold hoping for a comeback.

### Layer 3: Spike Detection
If price jumped >3.6% recently, don't buy — prevents catching a falling knife after a spike.

---

## 8. Parameters

### Timeframe
**Fixed at 5 minutes** — don't change. The whole logic is built around this.

### Ichimoku Parameters (Non-Standard!)
| Parameter | Standard | Strategy | Why |
|-----------|----------|----------|-----|
| Conversion | 9 | 20 | Less noise, more stable signals |
| Base | 26 | 60 | Adapted for 5-min framework |
| Lagging | 52 | 120 | More stability |
| Displacement | 26 | 30 | Fine-tuned |

Bigger parameters = slower but stabler signals.

### EMA: 3/5/10 (Key!)
Change these and the strategy behaves differently. Bigger = slower; smaller = noisier.

### Stop-Loss: -4%
Adjust based on your coin's volatility:
- High-vol altcoins: widen to -5% or -6%
- Stable large caps: tighten to -3%

### ROI: 10% → 5% → 2%
Adjust to your risk preference:
- Aggressive: raise initial target to 15%
- Conservative: lower to 8%

---

## 9. Best Market Conditions

### Best: Clear Trends
Single-direction moves up (or down — but this is long-only) = perfect. High signal accuracy, big gains possible, longer holds.

### Okay: Post-Consolidation Breakouts
After a long consolidation, a breakout can be traded. But some false signals in the consolidation period itself.

### Bad: Ranging/Sideways
Price going up and down with no clear direction:
- Entry conditions might occasionally trigger but reverse quickly
- Small losses accumulate
- Stop-losses might trigger frequently

**BUT**: Because entry is so strict, signals are rare in ranging markets, so won't lose too much. Better to miss than to be wrong.

---

## 10. Downsides

1. **Ranging market pain**: All trend-following strategies suffer here
2. **Late entry**: Waits for trend confirmation, may miss early gains ("eats the fish body, not the head")
3. **RSI unused**: Code defines it but doesn't use — wasted potential
4. **Long only, no short**: Can't profit in downtrends
5. **Single timeframe**: No higher-timeframe trend confirmation
6. **No volume analysis**: Volume confirms breakouts; this ignores it
7. **Author flagged improvements**: Mentions two areas needing work in comments

---

## 11. How to Improve

### Author's Suggested Fixes

**Fix 1: Fewer false signals in ranges**
- Add ADX: below 25 = no trend = don't trade
- Use ATR: too low volatility = don't trade
- Cloud thickness: too thin = weak support = don't trade

**Fix 2: Faster entry in strong trends**
- Current logic waits for TK Cross — in strong trends price may have already moved
- Add: price on cloud + breaking highs = lower other conditions
- Add: price retracing to Base Line then bouncing = entry

### Other Improvements

- **Add volume filter**: Breakout with high volume = real; low volume = fake
- **Add RSI filter**: Don't buy if RSI > 70 (overbought zone)
- **Multi-timeframe**: Check 1h trend before 5m entries
- **Dynamic stop**: Use cloud as trailing stop line
- **Add shorting logic**: When strong red cloud + TK cross down = consider shorting

---

## 12. Newbie Tips

### Before Using

**1. Backtest first**
Don't go live immediately! Test on historical data.

**2. Pick right coins**
- Mainstream coins (BTC, ETH): good liquidity, moderate volatility
- Not too small (too volatile), not too stable (no profits)
- Avoid brand new coins (no history)

**3. Account for fees**
5-minute chart = frequent trades. Fees add up. Set at least 0.1% in backtesting.

**4. Size positions properly**
Based on -4% stop:
- $10,000 account, risk 1-2% per trade = $100-200 max loss
- Stop is 4%, so position = $100/0.04 = $2,500 (conservative) or $200/0.04 = $5,000 (aggressive)

**5. Monitor these metrics**
- Win rate: should be 50%+
- Profit/loss ratio: what you make per win vs. per loss
- Max drawdown: biggest peak-to-valley drop
- Trade frequency: too high = parameter problem

**6. Don't tweak parameters constantly**
Don't change just because a few days look bad. Look at long-term (months).

### Common Mistakes

**Mistake 1: Changing strategy after losses**
Strategies won't win every trade. Consecutive losses are normal. Look at the big picture.

**Mistake 2: Over-optimizing**
Too-perfect parameters on history = won't work in the future. Keep parameters somewhat general.

**Mistake 3: Ignoring fees and slippage**
High-frequency strategies especially get eaten by fees. Set conservative fees in backtesting.

---

## 13. Summary

### One Line
ObeliskIM_v1_1 is a **trend-following strategy using Ichimoku for trend, EMA for momentum confirmation, and multi-condition filtering for entries.**

### Pros
- **Clear logic**: Trend → Signal → Confirm → Enter — straightforward
- **Strict conditions**: Six gates reduce false signals
- **Solid risk control**: Stop-loss, profit targets, anti-chase — three layers
- **Tunable**: Can adjust to market conditions

### Cons
- **Ranging market weakness**: Trend-following's common flaw
- **Late entry**: Waits for confirmation
- **Long only**: No shorting
- **Single timeframe**: No higher-timeframe check

### Who Should Use It
- Believers in trend-following
- Those who can accept ranging-period losses
- Patient people who wait for signals
- Disciplined traders who follow the system

### Final Thought

The author says this was written at 3 AM when he couldn't sleep. So trade this strategy with a clear head too:
- **Don't expect overnight riches**
- **Accept small losses as part of the game**
- **Long-term stability is the goal**
- **Most importantly: get a good night's sleep**

---
