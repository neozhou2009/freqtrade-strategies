# BbandRsi: The "Classic Recipe" 1-Hour Dip-Buyer

> **Nickname**: Classic Remake  
> **Profession**: Quant world's "old school" — using 20-year-old classic indicators, making 2026 money  
> **Timeframe**: 1 hour (office-worker friendly)

---

## 1. What Is This Thing?

Simply put, **BbandRsi** is:
- A strategy with only **1 entry condition**
- A strategy with only **1 exit condition**
- A strategy using **1-hour timeframe** (no need to stare at screens!)

Like an old-school investor who only checks two indicators before buying: "Is RSI oversold? Did it break Bollinger Band? Both good? BUY!" 🤣

---

## 2. Core Config: Basically "Classic Recipe"

### Profit-Taking Rules (ROI Table)

```
Make 10%? → RUN! (Only this one level)
```

**Translation**: This strategy is practical, runs at 10% profit, not greedy,pursuing quick turnover.

### Stoploss Rules

```
Hard stoploss: Cut at 25% loss (more conservative than BBRSI21's 30%)
Trailing stop: None (exits on technical signals)
```

**Translation**: Admit defeat at 25% loss, exits on RSI overbought signal after profits — classic "take profits and run" 😅

---

## 3. Entry Conditions: Classic RSI 30 + Bollinger Bands

This strategy's entry conditions are textbook classic:

### 🎯 RSI Oversold + Bollinger Lower Band

**Core Logic**: RSI < 30 + Price breaks below lower Bollinger Band

**In Plain English**:
> "RSI is already below 30 (classic oversold line), and price broke below lower Bollinger Band — if this isn't a dip-buying opportunity, what is?"

**Code Translation**:
```python
# Entry conditions
(RSI < 30) AND (Price < Lower Bollinger Band)
```

**Classic Lines**:
- "RSI 30 is the classic oversold line, way looser than BBRSI21's 21!"
- "2 standard deviations is enough, don't need BBRSI21's 3x!"

---

## 4. Protection: Basically Relies on "Classic"

This strategy's protection is so simple it's nostalgic:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **Hard Stoploss** | Cut at 25% loss | "25% loss means we were wrong, admit defeat" |
| **Timeframe** | 1-hour level | "1-hour candles are way more stable than 5-minute" |

**Roast**: This strategy's protection is so simple it's heartbreaking, but it's a classic recipe, simple and effective! 🤣

---

## 5. Exit Logic: Even Simpler Than Entry

### 5.1 Technical Exit: Just 1 Condition

**Trigger**:
```python
RSI > 70  # Classic overbought line
```

**In Plain English**:
> "RSI is already above 70 (classic overbought line), if you don't run now what are you waiting for?"

**Roast**: Exit condition is just RSI > 70, way looser than BBRSI21's RSI > 99, much easier to exit!

---

### 5.2 ROI Exit: Just One Level, 10%

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
10%        Anytime      Run when reached
```

**Translation**:
> "Don't be greedy! 10% is enough, take the money and run!"

---

### 5.3 Stoploss: 25% Hard Cut

```
Loss        Action
─────────────────────────────────────
25%        Cut immediately
```

**Translation**:
> "25% loss means our judgment was wrong, cut it without hesitation!"

---

## 6. This Strategy's "Personality"

### ✅ Pros (Praise Session)

1. **Super Simple**: Even my grandma could understand it 😂
2. **Minimal Code**: Less than 100 lines, easy to modify
3. **Fast Running**: Low computation, doesn't lag your computer
4. **Easy Backtest**: Can run historical data in seconds
5. **Perfect for Learning**: Best choice for beginners!

### ⚠️ Cons (Roast Session)

1. **Too Simple**: Simple to the point of possibly not making money
2. **No Protection**: Like driving without a seatbelt
3. **Poor Adaptability**: May miss bull runs, catch falling knives in bear markets
4. **Single Timeframe**: Only looks at 1-hour, can get crushed by larger trends

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 🎢 Range-bound Market | ✅ Use it! | High probability of rebound after touching lower band |
| 📈 Uptrend | ⚠️ Use with Caution | Counter-trend buying may miss the main rally |
| 📉 Downtrend | ❌ Don't Use! | Catching falling knives = dying miserably |
| ⚡️ High Volatility | ⚠️ Makeshift Use | Frequent signals, but also many false signals |

---

## 8. Bottom Line: How Is This Strategy?

### One-Sentence Review
> "Quant world's 'elementary student' — simple and crude but effective"

### Who Should Use It?
- ✅ Beginners learning quantitative trading
- ✅ Want to quickly validate trading ideas
- ✅ Running simulated trading for practice
- ✅ Users with low-spec computers

### Who Should NOT Use It?
- ❌ Experienced traders seeking high returns
- ❌ Risk-averse individuals
- ❌ People wanting complex strategies

### My Recommendations
1. **Start with Simulated Trading**: Don't jump in with real money immediately
2. **Observe for a While**: Run at least one month of simulation
3. **Test with Small Capital**: Add more only after confirming effectiveness
4. **Mental Preparation**: May have consecutive losses

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Using Simplest Indicators to "Buy Dips"

This strategy's profit logic in one sentence:
> "What falls too much will rise, what rises too much will fall"

Like a spring — compressed too low will bounce back. RSI < 30 means "compressed too low", lower Bollinger Band means "the bottom of the price spring".

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Uptrend | ⭐⭐☆☆☆ | Counter-trend buying = catching falling knives, may miss main rally |
| 🔄 Range Consolidation | ⭐⭐⭐⭐☆ | Hits the mark every time in range-bound markets! |
| 📉 Downtrend | ⭐⭐☆☆☆ | Keep catching dips until you lose faith in life |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | High volatility = many signals, but also many false signals |

**One-Sentence Summary**:
> "Best for range-bound markets, other markets either miss out or get trapped"

---

## 10. Want to Run This Strategy? Check These First

### 10.1 Pair Configuration

| Configuration Item | Recommended Value | Roast |
|-------------------|------------------|-------|
| Number of Pairs | 5-10 | Don't add too many, we can't watch them all |
| Take-Profit Target | 8-12% | Adjust based on coin volatility |
| Stoploss Target | 20-30% | Loosen for high volatility |

### 10.2 Key Config File Settings

```json
{
    "strategy": "BbandRsi",
    "timeframe": "1h",
    "minimal_roi": {
        "0": 0.1
    },
    "stoploss": -0.25
}
```

### 10.3 Hardware Requirements (Important!)

This strategy has minimal computation, basically doesn't care about hardware:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|---------------|-------------------|------------|
| 10 pairs | 256MB | 512MB | Buttery smooth |
| 50 pairs | 512MB | 1GB | No pressure at all |

**Warning**: This strategy's hardware requirements are so low it might make you think it's unreliable 😅

### 10.4 Backtest vs Live Trading

**Differences**:
- 10% take-profit may be easily reached in backtests
- Slippage and liquidity issues in live trading may affect execution

**Recommended Process**:
1. Backtest at least 1 year of data first
2. Then simulated trading for 1 month
3. Small capital live test
4. Increase position only after confirming effectiveness

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Looking at the code, you'll find some interesting things:

1. **Minimize Code**
   > "Delete if possible, simplify if possible"

2. **Classic Indicator Combination**
   > "RSI + Bollinger Bands, the MVP combo of technical analysis"

3. **Fixed Parameters**
   > "Not changing it, RSI is 14 periods, Bollinger is 20,2"

---

## 12. Last But Not Least

### One-Sentence Review
> "Quantitative trading's 'Hello World' — simple and crude but effective"

### Who Should Use It?
- ✅ Beginners wanting to learn quantitative
- ✅ People wanting simple strategies
- ✅ Low-spec computers
- ✅ Want to quickly validate ideas

### Who Should NOT Use It?
- ❌ Seeking high returns
- ❌ Risk-averse
- ❌ Wanting complex strategies

### Manual Trader Recommendations

If you don't want to use quant, you can also trade manually:

1. Open any market software
2. Add RSI (14) and Bollinger Bands (20, 2)
3. When RSI < 30 and price touches lower Bollinger Band → Buy
4. Profit 10% or RSI > 70 → Sell
5. Loss 25% → Stoploss

**Remember**: Manual trading requires overcoming greed and fear, harder than programmatic trading!

---

## 13. ⚠️ Final Risk Reminder (Must Read This Section)

### Backtests Look Beautiful, Live Trading Requires Caution

BbandRsi's historical backtests may look good, but there's a big pitfall:
- 10% take-profit target is too small, may be eaten up by fees and slippage
- 25% stoploss is large, a single loss may require 3-4 wins to recover

Simply put:
> "Earning 10% ten times isn't enough to cover losing 25% three times!"

### Hidden Risks of Simple Strategies

This strategy looks simple, but live trading may lead to:
- **Low Win Rate**: Consecutive stoplosses ten-plus times, mentality explodes
- **Unfavorable Risk-Reward**: Earn 10% lose 25%, need 40% win rate to break even
- **Ugly Equity Curve**: May be losing most of the time

### My Recommendations (Real Talk)

```
1. Don't expect this strategy to make you rich, it's just an entry-level "elementary student"
2. Run simulated trading first, consider live trading after half a year
3. Small capital! Small capital! Small capital! Can't stress this enough
4. Mental preparation: may have consecutive losses
5. If consecutive losses exceed 10 times, consider changing strategies
```

**Remember**:
> "In crypto, staying alive is more important than making money! Light position testing, don't go all-in!"

---

**Final Reminder**: The strategy may be simple, but the market is complex. Tread carefully 🙏

*This article is for entertainment and learning only, not investment advice. Investment involves risks, enter the market with caution.*
