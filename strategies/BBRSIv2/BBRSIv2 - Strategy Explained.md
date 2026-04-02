# BBRSIv2 Strategy: The Bollinger Band RSI Reversal Specialist

> **Nickname**: The Oversold Bottom Fisher  
> **Occupation**: BB Lower Band Patrolman  
> **Time Frame**: 15 minutes

---

## I. What is This Strategy?

Simply put, **BBRSIv2** is a strategy that:
- Waits for price to drop to the Bollinger Band lower band
- Checks if RSI is also oversold
- Enters when both conditions are met

Like a hunter crouching at the Bollinger Band lower band, waiting for prey (oversold bounces) to pass by 🎯

---

## II. Core Configuration: "Bottom Fishing + Stop Loss Protection"

### Take Profit Rules (ROI Table)

```
Profit > 30% → Sell
```

**Translation**: This strategy aims for 30%, a bit greedy 😅 But thankfully there's stop loss protection as backup.

### Stop Loss Rules

```
Hard Stop Loss: -10%
Dynamic Stop Loss: Higher profit, tighter stop
```

**Translation**: Worst case, run at -10% loss. But if making money, stop loss automatically tightens to prevent "letting the duck fly away."

---

## III. 2 Buy Conditions: Simple and Clear

### 🎯 Condition #1: RB1 - BB Lower Band Bounce

**Core Logic**:
- Price breaks below BB lower band
- RSI crosses above 35 from below

**Plain English**:
> "Price is too low (below BB lower band), RSI is also starting to rise (crossing above 35 from below), this oversold condition might bounce - time to bottom fish!"

**Representative Condition**: RB1

**Classic Lines**:
- `RSI crosses above 35` → "RSI says: Don't panic, I'm starting to bounce"
- `Close < BB lower band` → "Price says: I've dropped too far, outside the BB lower band"

---

### 🎯 Condition #2: RB2 - Deep Oversold Reversal

**Core Logic**:
- RSI < 23 (extremely oversold)
- TEMA below BB lower band and starting to rise
- Valid volume

**Plain English**:
> "RSI dropped below 23, this is extreme panic territory. TEMA is also outside the BB lower band but starting to turn around, indicating reversal has begun. Volume is also normal - time to bottom fish!"

**Classic Lines**:
- `RSI < 23` → "RSI says: I'm panicking hard, come save me"
- `TEMA rising` → "TEMA says: I'm turning back, don't worry"

---

## IV. Protection Mechanism: Tiered Stop Loss

The strategy has a smart stop loss system, like putting multiple layers of armor on profits:

| Profit Range | Stop Loss Lock | Plain English |
|--------------|----------------|---------------|
| >20% | 5% | "Made 20%, guaranteeing you at least 15%" |
| >10% | 3% | "Made 10%, guaranteeing you at least 7%" |
| >6% | 2% | "Made 6%, guaranteeing you at least 4%" |
| >3% | 1% | "Made 3%, guaranteeing you at least 2%" |
| Other | 0.001 | "Live trading base protection, don't lose too much" |

This design is pretty smart - the more you make, the more protection you get 🛡️

---

## V. Sell Logic: Two Simple Signals

### 5.1 RSI Overbought Exit

```
RSI > 70 → Sell
```

**Plain English**:
- RSI > 70 indicates overbought, market is too hot
- "Everyone's buying like crazy, I'm getting out first"

---

### 5.2 Price Breakout High

```
High > Highest price of past 60 candles → Sell
```

**Plain English**:
- Price breaks recent highs
- "New high - could be breakout or pullback, I'll take profit first"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simple Logic**: Just two buy conditions, easy to understand and debug
2. **Strong Reversal Capture**: Performs well when there are many oversold bounce opportunities
3. **Smart Stop Loss**: Tiered stop loss is practical, won't let profits fly away
4. **Beginner Friendly**: First choice for beginners, classic technical indicators

### ⚠️ Cons (Criticism Section)

1. **Suffers in Trending Markets**: During one-sided uptrends or downtrends, this strategy is like riding a bike against the wind - lots of effort, little reward
2. **ROI Target Too Large**: 30% is too greedy, might hold positions for a long time
3. **No Information Frame**: Doesn't look at big trends, might bottom fish during a crash
4. **Overbought Exit May Be Early**: RSI>70 might exit too early, missing subsequent big gains

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating Volatile | ✅ Use it | Many oversold bounce opportunities, perfect for bottom fishing |
| Slow Bull Uptrend | ⚠️ Use with caution | May exit too early on overbought |
| Sharp Drop Market | ❌ Don't use | Buying against the trend will get trapped |
| Sideways Consolidation | ✅ Use it | Range oscillation, bounce back and forth for profit |

---

## VIII. Summary: How's This Strategy Really?

### One-Line Review
> "Oversold bottom fishing specialist in oscillating markets, little leek in trending markets"

### Who Should Use It?
- ✅ Beginner learners
- ✅ Oscillating market traders
- ✅ People wanting to learn BB + RSI
- ✅ People with limited computing resources

### Who Shouldn't Use It?
- ❌ Trend followers
- ❌ People with buy-high-sell-low style
- ❌ Warriors wanting to bottom fish during crashes

### My Recommendations
1. **Test in oscillating markets first**: This is its home field
2. **Lower ROI target**: 30% is too big, change to 15% for faster turnover
3. **Use with big trend judgment**: Check 1-hour or daily charts, don't bottom fish during crashes
4. **Don't easily change stop loss after setting**: The tiered stop loss is well designed, don't manually break it

---

## IX. In What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Camping at BB Lower Band

BBRSIv2 is like a **Bollinger Band Lower Band Patrolman**:

- **Camping**: Staring at the BB lower band, watch when price drops below
- **Confirming**: Check if RSI is also oversold, double confirmation
- **Action**: Enter when both conditions are met
- **Stop Loss Protection**: Automatically tighten stop loss after making money, protect profits

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Slow Bull Uptrend | ⭐⭐⭐☆☆ | "Bottom fishing in bull market is okay, but RSI>70 might run too fast" |
| 🔄 Oscillating Volatile | ⭐⭐⭐⭐⭐ | "Home field for oscillating markets, bouncing back and forth feels great" |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | "Bottom fishing during crashes is catching falling knives, careful of getting hurt" |
| ⚡️ Rapid Surge | ⭐☆☆☆☆ | "No chance to enter during surges, can only watch others make money" |

**One-Line Summary**: Oscillating markets are its home field, trending markets are its graveyard.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Time Frame | 15m | Default value, no need to change |
| Startup Candles | 144 | About 36 hours of data, enough |
| Number of Pairs | 5-20 | More is fine too |

### 10.2 Key Configuration File Settings

```yaml
# Lower ROI target, faster turnover
minimal_roi:
  "0": 0.15  # 15% is enough, don't be greedy for 30%

# Stop loss can be appropriately tightened
stoploss: -0.08
```

### 10.3 Hardware Requirements (Easy!)

This strategy has very low computational needs, even old computers can run it:

| Pair Count | Minimum Memory | Recommended Memory | Experience |
|-----------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | "Silky smooth" |
| 10-50 pairs | 4GB | 8GB | "No problem at all" |

**Warning**: Just don't run too many pairs on a low-spec VPS 😅

### 10.4 Backtesting vs Live Trading

This strategy has small differences between backtesting and live trading because:
- Few parameters, not easy to "memorize answers"
- Indicator calculations are stable
- Main difference is slippage

**Recommended Process**:
1. First backtest oscillating markets (like 2021-2022 sideways period)
2. See if oversold bounces are correctly captured
3. Small position live testing
4. Slowly increase pairs and positions

**Don't go all-in right away** - even oscillating strategies need caution!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Difference between RB1 and RB2**: RB1 is "regular oversold", RB2 is "extreme oversold"
   > "Author says: Use RB1 for mild oversold, RB2 for deep oversold, layered bottom fishing"

2. **TEMA Confirmation**: RB2 uses TEMA rise to confirm reversal
   > "Author says: Don't just look at RSI, TEMA also needs to turn back, double confirmation is more stable"

3. **Dynamic Stop Loss Tiers**: 5 levels of profit protection
   > "Author says: The more you make, the more protection, don't let profits slip away"

---

## XII. The Final Word

### One-Line Review
> "Oversold bottom fishing specialist for oscillating markets, simple and suitable for beginners"

### Who Should Use It?
- ✅ Beginners learning BB + RSI
- ✅ Oscillating market traders
- ✅ People wanting to learn strategy development
- ✅ People with limited computing resources

### Who Shouldn't Use It?
- ❌ Trend followers
- ❌ People wanting to bottom fish during crashes
- ❌ Buy-high-sell-low style traders
- ❌ People only wanting quick riches

### Manual Trader Recommendations
You can manually use this strategy's logic:
- Watch BB lower band, pay attention when price drops outside
- Check RSI, prepare to bottom fish below 35
- After entry, watch profits, tighten stop loss above 3%
- Consider exit when RSI > 70

---

## XIII. ⚠️ Risk Re-emphasis (This Section Must Be Read)

### Backtesting Looks Great, Live Trading Needs Caution

BBRSIv2 backtesting might look solid, but there's a trap:

> **As a reversal strategy, it operates against trends in trending markets and may get trapped.**

Simply put: **Makes money happily in oscillation, loses money painfully in trends**

### Hidden Risks of Complex Strategies

Although this strategy is simple, it still has risks:
- **Bottom fishing against trend**: May get trapped deeper during crashes
- **Early exit**: RSI>70 might run too early
- **Target too large**: 30% ROI might hold positions for a long time

### My Recommendations (Real Talk)

```
1. First determine if market is oscillating or trending
2. Use this strategy in oscillating markets, switch to others in trending markets
3. Lower ROI target to 15%, faster turnover
4. Use with larger timeframe judgment, don't bottom fish during crashes
```

**Remember**: No matter how simple the strategy, the market isn't a well-behaved child. Great bottom fishing in oscillation, don't fight hard in trends!

---

**Final Reminder**: Bottom fishing strategies are most prone to "catching falling knives", test with small positions, staying alive is most important! 🙏