# NowoIchimoku1hV1: What's This Strategy Actually Doing?

## Preface

This article breaks down this strategy in the most accessible way possible. Don't worry about technical jargon — we'll go step by step, and by the end, you'll understand exactly how this strategy makes money, when to use it, and how to use it.

---

## 1. What Is This Strategy?

In simple terms, this is a program that **automatically decides when to buy and when to sell**. You set it up, it watches the charts for you, and executes trades automatically — no need to stare at candlestick charts all day.

Breaking down the name:
- **Nowo**: Probably the author's name or handle — nothing special
- **Ichimoku**: Japanese for "Ichimoku Cloud," a Japanese-invented technical analysis tool, often called "cloud chart"
- **1h**: Uses 1-hour candlesticks for analysis — each candle represents 1 hour of price action
- **V1**: Version 1, meaning V2, V3 may come later

So this is essentially **a 1-hour-level trading strategy using the Ichimoku Cloud (Ichimoku Kinko Hyo)**. Its core idea: only buy in uptrends, confirm with multiple conditions, then sell with discipline.

---

## 2. Why Would You Use This Strategy?

Trading is tough. You've probably run into these situations:

### Problem 1: No clue when to buy

You see the price rising and want to chase it, but you buy at the top and it immediately drops. You see the price falling and want to bottom-fish, but you catch a falling knife and keep buying lower. You agonize back and forth, end up buying nothing, and watch it all go up without you.

### Problem 2: No clue when to sell

After buying, it rises — you want to hold for more, but it then falls and your gains evaporate. After buying, it drops — you hold for a bounce, but it keeps falling, small loss becomes big loss. Finally it breaks even, you sell in relief, and then it goes up even more.

### Problem 3: Emotions spiral out of control

Watching prices bounce around, you frantically buy and sell. You chase losses trying to get even, and keep losing more. You're up but afraid of giving it back, you sell too early and miss the big move.

This strategy solves these problems. It uses **multiple layers of defense** to confirm buy opportunities and **multiple conditions** to decide when to sell, making your trading systematic and disciplined. Best of all, it's executed by a machine — no emotional interference, no fear or greed messing things up.

---

## 3. What Are the Core Tools?

The strategy uses three main tools:

### 3.1 The Ichimoku Cloud (Cloud Chart)

Invented by a Japanese person named Goshu Hosoda, the Ichimoku Cloud draws what looks like a "cloud" on your chart. This cloud isn't drawn randomly — it's calculated from past prices.

The cloud has five lines:

**Conversion Line (Fast Line)**
Calculated from the highest and lowest prices over the past 9 periods — responds quickly, captures short-term trends.

**Base Line (Slow Line)**
Calculated from the highest and lowest prices over the past 26 periods — responds more slowly, judges medium-term trends.

**Leading Span A**
Averages the fast and slow lines, then shifted forward 26 periods. Sounds complex — basically it plots today's value 26 hours into the future!

**Leading Span B**
Averages the highest and lowest prices over the past 52 periods, then shifted forward 26 periods.

**Lagging Span**
Plots the current closing price 26 hours in the past.

These five lines together form a "cloud." The cloud comes in two colors:
- **Green cloud**: Leading Span A > Leading Span B — uptrend
- **Red cloud**: Leading Span A < Leading Span B — downtrend

The cloud's upper and lower boundaries are like floors and ceilings:
- Price above the cloud → strong uptrend
- Price inside the cloud → sideways consolidation
- Price below the cloud → downtrend

### 3.2 Bollinger Bands Upper Band

Bollinger Bands are like an "elastic band" around prices, fluctuating with the market.

Three lines:
- **Middle band**: 20-period moving average
- **Upper band**: Middle band + 2.5× standard deviation
- **Lower band**: Middle band − 2.5× standard deviation

This strategy uses the Hull Moving Average (HMA) instead of regular MAs — HMA responds faster and has less lag.

The upper band is the upper edge of this band. Prices rarely break above it. When they do, it's either a strong breakout signal or an overbought warning. This strategy uses breaking the upper band as a profit-taking condition.

### 3.3 Stochastic RSI

RSI (Relative Strength Index) judges whether the market is overbought or oversold.

Stochastic RSI takes RSI and applies "randomization" once more, making it even more sensitive. It ranges from 0-100:
- K value > 80: Overbought — a pullback may be coming
- K value < 20: Oversold — a bounce may be coming

This strategy uses the Stochastic RSI's K value to judge whether it's time to take profits. When K exceeds 80 and profit is above 10%, the strategy exits.

---

## 4. When Does It Buy?

The strategy checks **7 conditions** before buying — ALL must be satisfied. Like clearing checkpoints, you must pass every single one:

### Condition 1: Bullish Candle

The current candle closes above its open — buyers won this hour, price is rising.

```
Close > Open → Bullish candle → Condition 1 PASSED
```

### Condition 2: Price Breaks Above Cloud Upper Boundary by 4%+

A mere touch isn't enough — it must exceed by 4%. Why 4%? Because prices often do "fake breakouts" — break out a little then reverse. Exceeding 4% suggests the breakout is more likely real.

```
Close > Cloud Upper × 1.04 → Condition 2 PASSED
```

### Condition 3: Price is Above Cloud Lower Boundary

This is double insurance. Price must be above both the cloud's upper AND lower boundaries, fully separated from the cloud zone.

```
Close > Cloud Lower → Condition 3 PASSED
```

### Condition 4: Cloud is Green

Green cloud = uptrend, red cloud = downtrend. This strategy **only buys in uptrends** — no bottom-fishing in downtrends. This is "going with the flow."

```
Leading Span A > Leading Span B → Green cloud → Condition 4 PASSED
```

### Condition 5: Fast Line Above Slow Line

The Ichimoku Cloud has two lines:
- **Conversion Line (Fast)**: More responsive, 9-period
- **Base Line (Slow)**: Less responsive, 26-period

Fast line above slow line is like short-term MAs above long-term MAs — recent gains are outpacing the average, trend is upward.

```
Conversion Line > Base Line → Condition 5 PASSED
```

### Condition 6: Price is Above the 25-Hour-Ago Fast Line

The 25-hour-ago position of the fast line matters, because the cloud is plotted 25 periods ahead. If current price is above where the fast line was 25 hours ago, the trend is continuing — not a fleeting spike.

```
Current Close > 25-hour-ago Conversion Line → Condition 6 PASSED
```

### Condition 7: Price is Above the 50-Hour-Ago Cloud Upper Boundary

This is further confirmation — 50 hours is 2× displacement, making trend confirmation more reliable. This condition avoids buying on false breakouts.

```
Current Close > 50-hour-ago Cloud Upper → Condition 7 PASSED
```

### There's Also a Cooldown Mechanism

This strategy has a clever "cooldown" design:

- Once you buy, it won't buy again immediately
- It waits until the cloud goes from green to red (trend weakens), then from red to green (trend recovers), before allowing the next buy

This is like adding a "fuse" to your trading — prevents repeated buying losses in ranging markets. Specific logic:

1. Cloud turns green → buying allowed
2. Buy triggered → buying prohibited
3. Cloud turns red → state reset
4. Cloud turns green again → buying allowed

---

## 5. What Happens After Buying?

After buying, the strategy automatically monitors for you. It watches:

### Monitoring 1: Stop-Loss Level

Uses the cloud lower boundary at your entry price as the stop-loss level. If price drops below this, the trend may be reversing — run for the exits.

### Monitoring 2: Target Level

The strategy calculates a dynamic target price based on your entry price and the cloud lower boundary at that time. When price hits this level, it locks in profits.

### Monitoring 3: Overbought Monitoring

Uses Stochastic RSI to monitor market heat. If K value goes too high (> 80), the market may be overheated and could pull back — get out.

### Monitoring 4: Bollinger Band Breakout

If price surges above the Bollinger upper band, it may be overextended and could pull back — consider taking quick profits.

---

## 6. When Does It Sell?

The strategy has four exit methods:

### Method 1: Stochastic RSI Overbought + Sufficient Profit

When Stochastic RSI K exceeds 80 AND profit is above 10%, it sells.

Why this design?
- K > 80 means the market bought too aggressively — a pullback may come
- 10%+ profit means the trade has already succeeded — don't be greedy
- Selling here protects profits AND avoids pullback risk

```
K > 80 AND Profit > 10% → SELL
```

### Method 2: Bollinger Upper Band Break + Small Profit

When price breaks above the Bollinger upper band AND profit exceeds 1%, it sells.

This is a "quick profit" approach:
- Price broke above the Bollinger upper band — it ran up hard
- 1% isn't huge, but accumulates
- Take the money and run, don't wait for the big move

```
Price > Bollinger Upper AND Profit > 1% → SELL
```

### Method 3: Dynamic Target Price Reached

The strategy calculates a target based on your entry:

```
Target = Entry Price + 2 × (Entry Price - Cloud Lower at Entry)
```

For example: You buy at 50,000, cloud lower was 46,000:
Target = 50,000 + 2 × (50,000 - 46,000) = 50,000 + 2 × 4,000 = 50,000 + 8,000 = 58,000

Why 2×? The distance from entry price to cloud lower is the "risk distance." Setting the target at 2× risk distance gives a 1:2 risk-reward ratio. Risking 4,000 to make 8,000 — worth it!

```
Price reaches dynamic target → SELL
```

### Method 4: Cloud Lower Boundary Broken (Stop-Loss)

If price falls below the cloud lower at your entry, it executes a stop-loss.

This is the last line of defense:
- Cloud lower at entry was a key support level
- Breaking below it suggests trend reversal
- Better a small loss than a big one

```
Price < Cloud Lower at Entry → Stop-loss SELL
```

---

## 7. How Does It Control Risk?

### 7.1 Fixed Stop-Loss

The strategy sets an **8% hard stop**. No matter what, when losses exceed 8%, it force-closes.

This is the "hard floor" — the last line of defense. Even if all other conditions fail, 8% loss means you're out.

```
Loss ≥ 8% → Force Close
```

### 7.2 Time-Decaying Profit Targets

The strategy has a clever design:

| Time | Profit Target |
|------|--------------|
| Just bought | 10% |
| After 30 minutes | 5% |
| After 60 minutes | 2% |

Why?

**Right after buying**: Hope to catch a big move — target is 10%.

**After 30 minutes without much rise**: This trade may not be that strong, target drops to 5%.

**After 1 hour still flat**: The trend may have weakened, better to take what you can get — target drops to 2%.

This is "time decay": the longer you hold, the lower your profit expectation. Avoids the scenario of "waited forever, ended up losing anyway."

### 7.3 Four Exit Conditions

Four exit conditions are like four doors — whichever opens first, you take:

| Exit Condition | Trigger | Good For |
|---------------|---------|----------|
| Stochastic RSI Overbought | K > 80 AND Profit > 10% | Fast surge |
| Bollinger Breakout | Price breaks upper band AND Profit > 1% | Short-term spike |
| Dynamic Target | 2× risk distance reached | Normal gains |
| Stop-Loss | Cloud lower boundary broken | Trend reversal |

### 7.4 Cooldown Prevents Overtrading

After buying, you must wait for the cloud to go red then green again before buying more. This cooldown prevents:
- Repeated buy-stops in ranging markets
- Chasing and panic-selling
- Excessive trading eating into profits with fees

---

## 8. What Are the Advantages?

### Advantage 1: Strict Conditions, Few False Signals

Seven conditions must ALL be met to buy — not "buy on a whim," but "multiple layers of verification."

Like hiring:
- Few conditions → many candidates, poor quality
- Many conditions → few candidates, high quality

This strategy uses the "many conditions" approach: "better to miss an opportunity than to make a mistake."

### Advantage 2: Goes With the Flow, Never Fights Trends

Only buys green clouds (uptrend), never buys red clouds (downtrend) — trend trading.

As the saying goes, "the trend is your friend." This strategy follows the trend, never fights it.

### Advantage 3: Has a Cooldown, Won't Overtrade

Cloud turns green before buying is allowed; after buying, must wait for red then green again. This avoids:
- Repeated stop-losses in ranging markets
- Emotional overtrading
- Fee erosion from excessive trading

### Advantage 4: Diverse Exit Conditions, Flexible Responses

Four exit conditions adapt to different situations:
- Fast rise → overbought exit
- Spike → Bollinger exit
- Normal rise → target price exit
- Drop → stop-loss exit

No matter how things play out, there's a response.

### Advantage 5: Reasonable Timeframe, No Need to Watch Constantly

Uses 1-hour candles — no need to watch like 5-minute charts, no waiting days like daily charts.

Perfect for:
- Office workers
- Part-time traders
- People with other things to do

### Advantage 6: Solid Risk Control

Has fixed stop-loss (8%), dynamic stop-loss (cloud lower), and time-decaying targets — three layers of protection.

Whatever happens, you won't lose your mind over a single trade.

---

## 9. What Are the Disadvantages?

### Disadvantage 1: Code Has Bugs

The strategy code has problems — the file header literally says "This version of the strategy is broken!"

Main issues:
- **Operator errors**: Used `&` (bitwise operator) instead of `and` (logical operator), causing condition judgment errors
- **Array index errors**: Some places have wrong index syntax
- **Custom stop-loss not implemented**: Custom stop-loss function returns 1, essentially doing nothing

**So DO NOT use it before fixing the bugs!**

### Disadvantage 2: Long Only, No Shorting

This strategy only buys on the way up — cannot short on the way down.

In a big bear market, you can only:
- Stay in cash waiting
- Watch helplessly as it falls

Can't profit from falling prices like a short strategy can.

### Disadvantage 3: Parameters Are Fixed, No Auto-Adjustment

All parameters are hardcoded:
- Cloud displacement: 25 periods
- RSI period: 14
- Bollinger Bands: 20 periods, 2.5× standard deviation

These don't auto-adjust to market changes. Different market environments might need different parameters — this strategy can't do that.

### Disadvantage 4: May Miss Opportunities

Because conditions are so strict (all 7 must be met), it may miss some good opportunities.

Like finding a partner — too high standards, fewer matches. "Better to miss than to be wrong" is an advantage AND a disadvantage.

### Disadvantage 5: Loses Money in Ranging Markets

In sideways markets, the cloud keeps changing colors:
- Green → buy
- Red → stop-loss
- Green → buy again
- Red → stop again

Repeated stop-losses eat into fees. While the cooldown helps, severe oscillations can still cause losses.

### Disadvantage 6: Lag Issue

The strategy uses multiple displacement operations:
- 25-period displaced cloud
- 50-period double-displaced confirmation

These displacements cause signal lag. By the time you confirm a buy, price may have already moved.

---

## 10. What to Watch Out For?

### Warning 1: Fix the Bugs First

Don't use it directly — the code has problems! Fix these first:

**Fix Operator Error**:
```python
# Wrong
if last_candle['srsi_k'] > 80 & current_profit > 1.1:

# Correct
if last_candle['srsi_k'] > 80 and current_profit > 0.1:
```

**Fix Array Index**:
```python
# Wrong
df[i, 'buy_allowed'] = True

# Correct
df.loc[i, 'buy_allowed'] = True
```

**Implement Custom Stop-Loss**:
```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if current_profit > 0.05:
        return current_profit - 0.03
    return self.stoploss
```

### Warning 2: Must Backtest

After fixing the code, test it on historical data:
- How did it perform last year?
- Maximum drawdown? (worst loss)
- Win rate?
- Reasonable profit/loss ratio?
- Sharpe ratio?

If backtesting looks bad, don't use it.

### Warning 3: Paper Trade First

Don't start with real money — paper trade for a month first:
- Are signals triggering as expected?
- Any execution issues?
- Gap between backtesting and live?

### Warning 4: Watch Out for Fees

Crypto trading fees aren't low, usually:
- Buy: 0.1%
- Sell: 0.1%
- Total: 0.2%

If a trade only nets 1%, fees leave you with 0.8% — barely worth it.

The strategy needs enough profit margin to cover fees.

### Warning 5: Monitor Cloud Server Operation

If running on a cloud server:
- Server stable, not frequently down
- Network smooth, not frequently disconnecting
- API connection normal, not frequently dropping

---

## 11. Who Is This For?

### Suitable For

1. **Those with some programming basics**: Can read Python, fix bugs, adjust parameters themselves
2. **Freqtrade familiar**: Know how to configure, backtest, deploy
3. **Stable mindset**: Can accept strategy losses, won't intervene emotionally
4. **Enough capital**: At least a few thousand USD, or fees will eat profits
5. **Office workers**: 1-hour timeframe, no need to watch constantly
6. **Medium-to-long-term traders**: Not pursuing intraday high frequency, willing to let trends develop

### Not Suitable For

1. **No coding knowledge whatsoever**: Sees Python and panics, can't fix bugs
2. **Want to get rich quick**: Strategies aren't money printers, don't expect to 10× in a month
3. **Emotional traders**: See losses and want to shut it down, see gains and want to add position
4. **Very small capital**: A few hundred dollars — can't afford the fees
5. **High-frequency traders**: This strategy might see only 1-2 signals per day, not exciting enough
6. **Bottom-fishers**: Like to catch falling knives — this strategy won't satisfy you

---

## 12. What Does an Actual Trade Look Like?

Let's simulate a complete trade:

### Scenario Setup

- Pair: BTC/USDT
- Timeframe: 1 hour
- Current time: 2 PM Beijing time
- Current price: 50,000 USDT

### Buy Signal Appears

Strategy detects:

1. ✅ This 1-hour candle is bullish (close 50,200 > open 49,800)
2. ✅ Price 5% above cloud upper (cloud upper 47,600; 50,200 > 47,600 × 1.04 = 49,500)
3. ✅ Price above cloud lower (cloud lower 46,000; 50,200 > 46,000)
4. ✅ Cloud is green (Leading A 48,000 > Leading B 45,000)
5. ✅ Fast line above slow line (Conversion 48,500 > Base 47,000)
6. ✅ Price above 25-hour-ago fast line (25h ago: 47,800; 50,200 > 47,800)
7. ✅ Price above 50-hour-ago cloud upper (50h ago: 49,000; 50,200 > 49,000)
8. ✅ Cooldown allows buying (cloud just turned from red to green)

**All met! Strategy auto-buys at 50,000 USDT, 0.1 BTC bought.**

### Holding Period — Hour 1

30 minutes after buying, price rises to 51,000 (2% profit).

Strategy checks:
- Stochastic RSI K: 65 (not 80 yet) ❌
- Bollinger upper: 51,500 (not broken) ❌
- Dynamic target: 50,000 + 2 × (50,000 - 46,000) = 58,000 (not reached) ❌
- Cloud lower: 46,000 (price well above) ❌
- Time-decay target: first 30 min, target 10% (only 2% now) ❌

**Keep holding.**

### Holding Period — Hour 2

1 hour after buying, price rises to 53,000 (6% profit).

Strategy checks:
- Stochastic RSI K: 72 (not 80) ❌
- Bollinger upper: 52,000 — BROKEN! But profit is 6%, is that > 1%? Yes! ✅

Wait, let me check the condition again... Bollinger break condition is "Price > Bollinger upper AND Profit > 1%."

Now price 53,000 > Bollinger upper 52,000, profit 6% > 1%.

**Condition 2 triggered! Strategy sells, reason: "current rate above upper band with profit above 1%"**

This trade made ~6%, minus fees (~0.2%), net ~5.8%.

Entry 50,000, exit 53,000, gross 3,000 USDT, fees ~103 USDT (50 USDT buy + 53 USDT sell), net ~2,897 USDT.

### Alternative Scenario — Stop-Loss Triggered

Say price dropped after buying:

1 hour after buying, price falls to 45,500 (9% loss).

Strategy checks:
- Cloud lower: 46,000 (price 45,500 < 46,000) ✅

**Condition 4 triggered! Strategy stop-loss sells, reason: "current rate below stop"**

Loss 9%, exceeding 8% fixed stop — this reveals a problem: the dynamic stop (cloud lower) and fixed stop (8%) may conflict.

---

## 13. Final Thoughts

The strategy's thinking is clear: **use multiple conditions to verify, enter only when trends are clear, protect profits and control risk in multiple ways.**

However, **the current version's code has bugs and cannot be used directly.** If you want to use it:

1. Fix code errors
2. Backtest with historical data
3. Paper trade for a while
4. Small capital live test
5. Only increase position after confirming stability

Don't rush to live trading. There's no holy grail in trading, and any strategy can lose money. Strategies are tools — whether you make money depends on how you use them.

My recommendation:
- First learn, understand the strategy's logic
- Then backtest, check historical performance
- Then paper trade, get familiar with actual operation
- Then small capital live, build experience
- Confirm it works, then increase capital

One final piece of advice: **Respect the market, control risk, test with small capital, make money with big positions.**

Happy trading!

---

*Document Version: v1.0*
*Applicable Strategy Version: NowoIchimoku1hV1*
*Generated: March 27, 2026*
