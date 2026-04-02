# NFI46Frog Strategy: The Frog That Hops Steadily on Trend Lilypads

> **Nickname**: Frog Strategy  
> **Career**: Professional "hop in, hop out" trend rider  
> **Timeframe**: 5 Minutes (main battlefield) + 1 Hour (telescope)

---

## 1. What's This Strategy?

In simple terms, **NFI46Frog** is:
- Looking for pullback entry opportunities in uptrends
- Has layers of protection against "catching falling knives" and "chasing highs"
- Intellectually takes profits when it's making money

It's like a frog hopping from lily pad to lily pad — when the trend is good, it hops in; when danger strikes, it hops out. Steady and safe, no capsizing 🐸

---

## 2. Core Settings: Plain English — "10% Take-Profit, 10% Stop-Loss"

### Take-Profit Rules (ROI Table)

```
Immediately after buying: wait for 10% profit before exiting
After 30 minutes: exit with 5% profit
After 1 hour: exit with 2% profit
```

**Translation**: Give it time to make money, and take profits when you've made enough — don't be greedy.

### Stop-Loss Rules

```
Stop-loss: -10% (lose a maximum of 10%)
Trailing stop: starts "watching" after making 3%
```

**Translation**: Admit defeat if you lose too much; once you're winning, it helps you guard your profits so you don't "ride a rollercoaster."

---

## 3. 17 Entry Conditions: I've Categorized Them for You

This strategy's entry conditions are terrifyingly numerous. I've organized them into 7 categories:

### 🎯 Category 1: Trend Pullback Type (Conditions 1, 5, 14)
**Core Logic**: Major trend is upward — a minor pullback is an entry opportunity

**Plain English**:
> "The train is moving forward, it just slowed down slightly — quickly hop on!"

**Representative Condition**: Condition #1
- 1-hour trend upward (EMA50 > EMA200)
- Downturn protection activated
- Surge protection activated
- RSI somewhat low (short-term oversold)

---

### 📉 Category 2: Oversold Rebound Type (Conditions 2, 4, 6, 7)
**Core Logic**: It's fallen too much — a rebound is coming

**Plain English**:
> "Fell to grandma's house, time for a rebound, right? Bottom-fishing!"

**Representative Condition**: Condition #2
- RSI is significantly lower than the 1-hour RSI
- Price near Bollinger lower band
- Trading volume is not high

---

### 📊 Category 3: BB Breakout Type (Condition 3)
**Core Logic**: Bollinger Band bandwidth narrows before a breakout

**Plain English**:
> "Price has been compressed to its limit — it's about to explode!"

---

### 🐊 Category 4: Alligator Indicator Type (Condition 8)
**Core Logic**: Use Alligator indicator to determine trends

**Plain English**:
> "The alligator's mouth is open, pointing upward! Follow along!"

**Classic Lines**:
- Condition #8: lips > teeth > jaw, all three lines pointing up
  > "The alligator is ready to eat — quickly get on board!"

---

### 📍 Category 5: Moving Average Deviation Type (Conditions 9, 10, 11)
**Core Logic**: Price deviates too much from the moving average — time to revert

**Plain English**:
> "It's run too far, time to come back, right?"

---

### 🌊 Category 6: EWO Signal Type (Conditions 12, 13, 16, 17)
**Core Logic**: Use Elliott Wave Oscillator to find opportunities

**Plain English**:
> "The wave theory says it's time to go up here!"

---

### 🎯 Category 7: EMA Deviation Type (Condition 15)
**Core Logic**: Short-term moving average deviates too much from the long-term

**Plain English**:
> "Short-term moved too fast — time to catch your breath!"

---

## 4. Protection Mechanisms: Dual Insurance, Scared You'll Buy Recklessly

Each entry condition is equipped with two sets of protection parameters, like two security checkpoints:

### 🛡️ First Line: Dip Protection (Downturn Protection)

| Inspection Dimension | Function | Plain English |
|--------------------|----------|----------------|
| Current candle | Don't catch a single big red candle | "This one candle dropped this much — don't catch it!" |
| 2 periods | Don't catch consecutive declines | "Both candles dropped — wait a bit" |
| 12 periods | Don't catch medium-term decline | "It's been dropping for an hour, stay calm" |
| 144 periods | Don't catch long-term decline | "It's been dropping almost all day — are you really going to catch it?" |

**Three Strictness Levels**:
- **Normal**: Standard protection, use in normal circumstances
- **Strict**: Strict protection, for the fearful
- **Loose**: Loose protection, for the bold

### 🛡️ Second Line: Pump Protection (Surge Protection)

| Inspection Window | Function | Plain English |
|-----------------|----------|----------------|
| 12 hours | Don't chase short-term surges | "Just surged — wait for a pullback" |
| 24 hours | Don't chase medium-term surges | "Surged this much in one day — don't chase" |
| 36 hours | Medium-to-long-term surge check | "It's been surging for a day and a half — be careful" |
| 48 hours | Long-term surge check | "Surged for too long — it might crash" |

**Commentary**: This protection mechanism is more naggy than my mom, but it really can save your life

---

## 5. Exit Logic: More Complex Than Entries!

### 5.1 Tiered Take-Profit: How Much Profit Triggers an Exit?

```
Profit       RSI Threshold    Action
──────────────────────────────────────
> 20%        < 34            Get out! You've made enough!
10-20%       < 42            You can leave now
9-10%        < 50            Wait a bit more
...         
1-2%         < 34            Just made a little — observe
```

**Plain English**:
- Making a lot: RSI requirement loose, let you make more
- Making a little: RSI requirement strict, take profits when you can

### 5.2 Special Scenario Exits

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| Below EMA200 | Price below long MA | "Trend is bad — make money and run" |
| Post-Surge | Surged within 48h | "After a surge — take profits quickly" |
| Trend Decay | SMA200 declining | "Trend is gone -- run!" |
| Trailing Exit | Profit drawdown | "Don't let profits slip away" |

### 5.3 Basic Sell Signals (8)

**Classic Lines**:

1. **Signal #1**: RSI > 79.5 + 6 consecutive candles above BB upper band
   > "Gone wild! Broke through the upper band 6 times in a row — run!"

2. **Signal #3**: RSI > 82
   > "RSI broke 82 — way too hot!"

3. **Signal #4**: 5-minute RSI > 73 + 1-hour RSI > 79
   > "Both short and long timeframe RSI overbought — take profits when you can!"

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (The Praising Section)

1. **Perfect Protection Mechanism**: Won't let you catch falling knives in a crash, won't let you chase at the top
2. **Highly Customizable**: 17 entry conditions — use whichever you want
3. **Dual Timeframe**: 5 minutes to see opportunities, 1 hour to see trends — broad vision
4. **Refined Take-Profit**: 12 levels of take-profit, won't miss money you should earn

### ⚠️ Cons (The Ranting Section)

1. **Too Many Parameters**: 100+ optimizable parameters — your head hurts just looking
2. **Easy to Overfit**: Beautiful backtesting, real trading may slap you in the face
3. **High Computational Load**: Needs 400 candles before signaling — old computers may lag
4. **High Learning Curve**: Don't even try without learning dozens of indicators first

---

## 7. When to Use It: Applicable Scenarios

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Stable Uptrend | 🟢 Recommend using | Strategy design intent, perfect match |
| Wide Ranging | 🟡 Use cautiously | Only use oversold rebound conditions |
| One-Sided Decline | 🔴 Not recommended | Trend conditions not met, no signals |
| High Frequency Volatility | 🔴 Not recommended | Protection mechanisms lock down entries |

---

## 8. Summary: What Do You Think of This Strategy?

### One-Line Rating
> "Frog hops on lily pads — stable, but needs a good pond (uptrend)"

### Who's It For?
- ✅ Those with Freqtrade live trading experience
- ✅ Willing to spend time optimizing parameters
- ✅ Mainly trading stablecoin pairs (USDT)
- ✅ Those with sufficient VPS memory

### Who's It NOT For?
- ❌ Complete beginners
- ❌ People wanting "install and go"
- ❌ Only trading BTC/ETH pairs
- ❌ Manual traders

### My Recommendation
1. **First run dry-run**: Don't put real money in right away
2. **Select good trading pairs**: 40-80 stablecoin pairs, don't touch leveraged tokens
3. **Adjust protection parameters**: Based on market adjust Strict/Loose
4. **Regular checks**: Parameters aren't set-and-forget

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Trend + Protection + Take-Profit

NFI46Frog is a member of the NostalgiaForInfinity series. Code volume 1000+ lines — what does that mean? It's like writing a small novel

**Its Money-Making Philosophy**: Find safe pullback opportunities in uptrends, take profits and run.

- **Trend Confirmation**: Most conditions require EMA50 > EMA200
- **Protection First**: Two gates — downturn protection and surge protection
- **Intelligent Take-Profit**: Decides when to exit based on profit and RSI status

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:--------------------------|
| 📈 Stable Uptrend | ⭐⭐⭐⭐⭐ | This is home turf! Good trend + pullback entry = making bank |
| 🔄 Wide Ranging | ⭐⭐⭐☆☆ | Oversold rebound conditions work, but stop-losses will be frequent |
| 📉 One-Sided Decline | ⭐⭐☆☆☆ | Trend conditions not met, signals are few |
| ⚡ High Frequency Volatility | ⭐☆☆☆☆ | Protection mechanisms block most entries |

**One-Line Summary**: Makes money in uptrends, muddles through in ranging markets, rests during declines.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Commentary |
|-------------|-------------------|-------------|
| Number of Pairs | 40-80 pairs | Too few signals insufficient, too many can't handle |
| Blacklist | Leveraged tokens | Don't touch — they'll blow up |
| Concurrent Positions | 4-6 | Don't be greedy |

### 10.2 Key Config File Settings

```yaml
# config.json key settings
"timeframe": "5m",              # Must be 5 minutes
"use_sell_signal": true,        # Must enable
"sell_profit_only": true,       # Recommend enabling
"ignore_roi_if_buy_signal": true # Must enable
```

### 10.3 Hardware Requirements (Important!)

This strategy has enormous computational load and has requirements for VPS memory:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|-------------------|-------------|
| 40 pairs | 4GB | 8GB | Barely usable |
| 80 pairs | 8GB | 16GB | Runs smoothly |

**Warning**: Insufficient memory will cause freezes, signal delays, missing buy/sell points

### 10.4 Backtesting vs. Live Trading

**Backtesting often looks beautiful** — with so many parameters, you can always "memorize the answers."

**Recommended Process**:
1. Run historical backtesting to see general performance
2. Then run dry-run (paper trading) for at least 1-2 weeks
3. Small-funds live test
4. Confirm stability before increasing position

**Don't go all-in right away**, even the best strategy needs a break-in period!

---

## 11. Easter Eggs: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Frog naming**: Frog might hint at the flexibility of "hopping in and out"
   > "I'm not holding until death — I'm a frog. If the lily pad isn't safe, I hop."

2. **Dip Protection three levels**: Normal/Strict/Loose
   > "I've given you choices: conservative, radical, or in between"

3. **Pump Protection multiple time windows**: 12h/24h/36h/48h
   > "Surges need to be evaluated over time — short-term and long-term surges are different"

---

## 12. The Final Final

### One-Line Rating
> "Frog strategy: hops in when trends are good, hops out when it's dangerous — stable!"

### Who's It For?
- ✅ Those with quantitative experience
- ✅ Willing to tweak parameters
- ✅ Those with stablecoin pair resources
- ✅ Those with good machines

### Who's It NOT For?
- ❌ Beginner newbies
- ❌ Lazy people
- ❌ Manual traders
- ❌ Those with insufficient memory

### Manual Trader Recommendations
Don't try to manually trade this strategy! Signal judgment requires real-time calculation of dozens of indicators — the human brain simply can't compute that.just let let the machine run it.

---

## ⚠️ Risk Re-Emphasis (Must Read This Section)

### Backtesting Looks Great, Live Trading Requires Caution

NFI46Frog's historical backtesting performance is often **extremely impressive** — but there's a trap:

> **Because there are many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but this doesn't mean it can definitely profit in the future.**

Simply put: **Students who memorize answers get high scores, but that doesn't mean they actually understand the material.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Signal delays**: Too much calculation, miss the best entry points
- **Over-optimization**: Parameters perfectly fit history, but markets change
- **Maintenance costs**: When problems arise, they're hard to diagnose
- **Slippage impact**: Many signals mean many trades, slippage costs add up

### My Recommendations (Sincere Advice)

```
1. Don't just look at backtesting returns — look at maximum drawdown
2. Dry-run for at least 2 weeks before live trading
3. Start live trading with small funds
4. Check strategy performance regularly — switch if not working
```

**Remember**: No matter how good a strategy is, the market won'tgive you a heads-up when it comes to teach you a lesson. Test with light positions — survival is the most important thing!

---

**Final Reminder**: Frog hops on lily pads — stable, stable, but without the lily pads (uptrends), the frog gets wet too! Choose the right market to hop steadily!
