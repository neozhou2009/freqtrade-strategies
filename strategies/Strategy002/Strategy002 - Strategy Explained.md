# Strategy002: The Bottom-Fishing Specialist

> **Nickname**: Hammer Hunter
> **Occupation**: Professional Bottom-Fisher
> **Timeframe**: 5-minute chart

---

## I. What is This Strategy?

Simply put, **Strategy002** is:
- Specifically looking for "oversold" opportunities
- Using four indicators stacked together to confirm the bottom
- Waiting for the hammer candlestick before taking action

It's like a cautious bottom-fisher who needs four "witnesses" all saying "this is really the bottom" before making a move 🤣

---

## II. Core Configuration: "Take Profit and Run"

### Take-Profit Rules (ROI Table)

```
Holding Time     Target Profit
─────────────────────────────
Just bought      5%
20 minutes later 4%
30 minutes later 3%
60 minutes later 1%
```

**Translation**: When you first buy, you want 5% profit. But if the market drags on, you'll settle for 1% after an hour. It's like dating - high standards at first, but as time passes... you know how it goes.

### Stop-Loss Rules

```
Hard Stop-Loss: Forced exit at 10% loss
Trailing Stop: If you've made 2%, exit when it drops back 1%
```

**Translation**: Accept a 10% loss and move on. But if you've already made more than 2%, the strategy watches your profit for you - drop 1% and it's time to take profits and leave.

---

## III. Buy Conditions: All Four Witnesses Must Agree

This strategy's buy conditions are very "picky" - all four indicators must be satisfied:

### 🎯 Buy Conditions Overview

| Condition # | Indicator | Requirement | Plain English |
|-------------|-----------|-------------|---------------|
| #1 | RSI | < 30 | "Oversold! Oversold!" |
| #2 | Stochastic Slow K | < 20 | "Momentum confirms too!" |
| #3 | Close vs Bollinger Lower Band | Price < Lower Band | "Broke support!" |
| #4 | Hammer Pattern | == 100 | "Look! A hammer!" |

**Plain English Translation**:

> Strategy: "RSI, are you telling me it's oversold?"
> RSI: "Yes! Below 30!"
>
> Strategy: "Stochastic, what about you?"
> Stochastic: "Slow K is below 20 too!"
>
> Strategy: "Has the price broken below the Bollinger lower band?"
> Price: "Yes, it's floating down there right now!"
>
> Strategy: "So... is there a hammer pattern?"
> Candlestick: "Yes! A perfect hammer!"
>
> Strategy: "Great! All four witnesses agree, **BUY!**"

It's like a background check for dating - all four conditions must be met 😂

---

## IV. Protection Mechanism: Two Layers of "Fuses"

| Protection Type | Trigger Condition | Plain English |
|-----------------|-------------------|---------------|
| Fixed Stop-Loss | 10% loss | "Lost too much, time to give up and leave" |
| Trailing Stop | Profit drawdown 1% (after profit > 2%) | "You made money and want to run? Not so fast!" |

**Critique**: This strategy's stop-loss setting is moderately conservative. The 10% stop-loss gives the price some room to "breathe," but the trailing stop locks in your profits. It's like... a mom who worries you'll fail but also worries you'll get too proud if you succeed 😅

---

## V. Sell Logic: Two Conditions Must Both Be Met

The sell signal is also simple:

```python
SAR > Close Price  AND  Fisher RSI > 0.3
```

**Plain English**:

1. **SAR > Close Price**: Price broke below the SAR "umbrella," trend might be changing
2. **Fisher RSI > 0.3**: Momentum has exited the oversold zone, time to go

> Strategy: "SAR has flipped, Fisher RSI has also left oversold..."
> Strategy: "**SELL!**"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Clear Logic**: Four conditions written clearly, no BS
2. **Conservative and Cautious**: Multi-indicator confirmation reduces fake signals
3. **Comprehensive Risk Control**: Fixed stop-loss + trailing stop + tiered take-profit, triple protection
4. **Pattern Confirmation**: Hammer is a classic bottom reversal signal

### ⚠️ Cons (Critique Time)

1. **Limited Opportunities**: Four conditions all met? You'll be waiting forever
2. **Bottom-Fishing Can Catch Falling Knives**: Oversold can get more oversold, we all know how that goes
3. **5-Minute Frame is Noisy**: Short-term volatility, plenty of fake breakouts
4. **No Volume Check**: Only price signals, no volume confirmation

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|----------------|--------|
| Oscillation followed by sudden crash | ✅ Recommended | Perfect for oversold bounce opportunities |
| Sideways oscillation | ✅ Can use | Can catch some volatility |
| Continuous one-way decline | ⚠️ Use cautiously | Oversold can get even more oversold |
| One-way uptrend | ❌ Don't use | No buy signals at all |

---

## VIII. Summary: How Good Is This Strategy?

### One-Sentence Review
> "A cautious bottom-fisher who needs all four witnesses to agree"

### Who Should Use It?
- ✅ Quantitative trading beginners (simple, easy-to-understand code)
- ✅ People who like bottom-fishing style
- ✅ Those who can accept fewer trading opportunities
- ✅ Conservative traders who prioritize risk control

### Who Should NOT Use It?
- ❌ People who want frequent trades
- ❌ Trend-following style traders
- ❌ People who don't like waiting for signals
- ❌ Gamblers expecting high win rates

### My Recommendations

1. **Run backtests first**: Don't jump into live trading, check historical performance
2. **Parameters can be tweaked**: RSI 30, Stochastic 20 can be adjusted based on market
3. **Consider the big picture**: If the overall market is crashing too, bottom-fishing is riskier
4. **Start with small positions**: This strategy has few signals, suitable for light positions

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: The Art of Oversold Bouncing

Strategy002 is a classic **oversold bounce strategy**. Its philosophy is: **If it drops enough, it will eventually bounce - the key is finding the right timing.**

It's like a spring - the more you compress it, the stronger the bounce. But only if the spring doesn't break 🙃

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Reversal after oscillation | ⭐⭐⭐⭐⭐ | Main course! This is what the strategy was designed for |
| 🔄 Sideways oscillation | ⭐⭐⭐⭐☆ | Can get some meat, but don't expect a feast |
| 📉 Continuous crash | ⭐⭐☆☆☆ | Bottom-fishing halfway up the mountain, we all know |
| ⚡️ One-way uptrend | ⭐☆☆☆☆ | Nothing for you here, go home and rest |

**One-Sentence Summary**: **Find markets with oversold opportunities, not markets that are going crazy.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Number of trading pairs | 10-30 | Too few means not enough signals, too many is hard to manage |
| Timeframe | 5m | Default setting, don't change it |

### 10.2 Hardware Requirements

This strategy doesn't need much computing power, very low hardware requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 | 2GB | 4GB | Smooth |
| 10-50 | 4GB | 8GB | Stable |

**Warning**: This is a lightweight strategy, you basically don't need to worry about hardware 😅

### 10.3 Backtesting vs Live Trading

Backtesting data might look better than live trading, reasons:

1. **Candlestick patterns**: Might be more "perfect" in backtesting than live
2. **Limit order execution**: In live trading, orders might not get filled
3. **Oversold continuation**: In backtesting, oversold is oversold; in live trading, oversold can get more oversold

**Recommended Process**:
1. First backtest to see results
2. Run paper trading for a while
3. Test with small position live trading
4. Slowly increase position

**Don't go all-in on day one**. Even bottom-fishing strategies can catch falling knives!

---

## XI. Bonus: The Strategy Author's "Little Tricks"

Looking carefully at the code, you'll find some interesting designs:

1. **Fisher RSI Transformation**: Converts regular RSI to [-1, 1] range, making extreme values more sensitive
   > "The author felt regular RSI wasn't exciting enough, added some math magic 🧙"

2. **Four Conditions with "AND" Relationship**: Not "OR", but "AND"
   > "Better to miss an opportunity than make a mistake - all four conditions must be met!"

3. **Tiered ROI**: The longer you hold, the lower the requirement
   > "Making money is good, don't be greedy"

---

## XII. The Very End

### One-Sentence Review
> "A simple and effective bottom-fishing strategy, suitable for beginners to learn, for veterans to modify"

### Who Should Use It?
- ✅ Quantitative beginners (simple code, clear logic)
- ✅ Bottom-fishing enthusiasts (matches their style)
- ✅ Conservative traders (comprehensive risk control)
- ✅ Strategy modifiers (solid foundation, easy to customize)

### Who Should NOT Use It?
- ❌ Trend-following traders
- ❌ High-frequency trading enthusiasts
- ❌ People expecting daily trades
- ❌ People who don't like waiting

### Manual Trader Recommendations

If you're a manual trader, this strategy's logic can be applied directly:

1. Watch for coins with RSI < 30
2. Check if Stochastic is also oversold
3. Check if price has broken below Bollinger lower band
4. Wait for a hammer pattern to appear
5. All four conditions met? Enter!

---

## XIII. ⚠️ Risk Reminder Again (Read This Part!)

### Backtesting Looks Great, Live Trading Needs Caution

Strategy002's historical backtesting might look good - but there's a trap:

> **Oversold can get even more oversold.**

Simply put: **Bottom-fishing halfway up the mountain, with 18 more bends at the top.**

### Hidden Risks of Complex Strategies

Although this strategy isn't complex, in live trading note:

- **Consecutive stop-losses**: Crashing markets may trigger multiple buys and sells, fees eating profits
- **Fake hammers**: Candlestick patterns in live trading may have deviations
- **Limit order slippage**: In rapid drops, orders might not get filled

### My Recommendations (Real Talk)

```
1. Run backtest once, get a feel for it
2. Paper trade for two weeks, see signal frequency
3. Test with small position, no more than 5% of total capital
4. Record every trade, review and analyze
5. Adjust parameters based on your risk preference
```

**Remember**: No matter how good the strategy is, the market will humble you without warning. Light positions for testing, staying alive is most important! 🙏

---