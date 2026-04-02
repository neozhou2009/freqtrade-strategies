# BinHV45: The 1-Minute Ultra-Fast Scalp King!

> **Nickname**: 1-Minute Champion / Thin Margins, High Volume / Bollinger Band Catcher  
> **Vibe**: Ultra-short-term intraday trader who takes 1.25% and runs!  
> **Timeframe**: 1 minute  
> **Core**: Bollinger Band breakout + ultra-short-term scalp + 80% win rate required

---

## 1. What's This Strategy All About?

Simply put, **BinHV45** is:
- A **1-minute ultra-short-term** trading strategy (it might have traded several rounds in the time it takes you to light a cigarette)
- A Bollinger Band-based mean reversion strategy
- After price breaks below the Bollinger Band lower band, **takes 1.25% profit and runs!**
- **5% stop-loss** — lose more if you're slow!

Think of it as a **smart small-store owner**:

> "Don't talk to me about doubling! I only want 1.25%! Do dozens or hundreds of trades a day, each earning a little, accumulating small wins into big profits! This isn't greed — it's the art of thin margins, high volume!"

This strategy comes from Slack community guru **BinH**, representing the HV (High Volatility) series. But unlike other HV series, BinHV45 takes the **ultra-short route**:

| HV Series | Target | Style |
|-----------|--------|-------|
| BinHV27 | 100% | Long-term violent rebound |
| **BinHV45** | **1.25%** | **Short-term thin margins, high volume** |

---

## 2. Core Settings: 1.25% to Run, 5% to Cut!

### Take-Profit (ROI Table)

```python
minimal_roi = {"0": 0.0125}  # Hold for any duration → Sell at 1.25% profit!
```

**Translation**: This strategy is super stingy! Goes for 1.25% right from the start. Reached it? Get out immediately, no greed! Didn't reach it? Wait for stop-loss!

> "Double? Not happening! I only want 1.25%, accumulating wins is the way!"

### Stop-Loss

```python
stoploss = -0.05  # Fixed 5% stop-loss
```

**Translation**: Maximum loss is 5%. If it drops 5% after buying, admit defeat, get out.

### Timeframe

```python
timeframe = '1m'  # 1-minute candles
```

Suited for intraday ultra-short-term trading, quickly validating strategy effectiveness.

### Adjustable Parameters

| Parameter | Default | Range | Meaning |
|-----------|---------|-------|---------|
| buy_bbdelta | 7 | 1–15 | Bollinger Band spread threshold (‰) |
| buy_closedelta | 17 | 15–20 | Closing price change threshold (‰) |
| buy_tail | 25 | 20–30 | Lower wick length limit (‰) |

These can be auto-optimized through backtesting.

---

## 3. The 6 Buy Conditions: ALL Must Be Satisfied Simultaneously!

Before buying, must pass all 6 gates (all must be met simultaneously):

### Condition 1: Bollinger Band Lower Band Valid

```
lower.shift() > 0
```

**Plain English**:
> "The previous candle's Bollinger Band lower band must exist and be greater than 0 — don't give me division-by-zero errors! This is basic, no valid Bollinger Band means everything after is worthless."

---

### Condition 2: Bollinger Band Spread Wide Enough

```
bbdelta > close × 0.7%
```

**Plain English**:
> "The gap between the middle and lower band of Bollinger must be wide — can't be one of those nearly-closed narrow channels! Must exceed 0.7% of closing price. Why? Narrow spread means low volatility — I need an active market!"

---

### Condition 3: Obvious Intraday Movement

```
closedelta > close × 1.7%
```

**Plain English**:
> "Today gotta move! The difference between today's and yesterday's close must exceed 1.7%. A stagnant market with zero action? Get lost! I need living water, not stagnant pond!"

---

### Condition 4: Lower Wick Cannot Be Too Long

```
tail < bbdelta × 2.5%
```

**Plain English**:
> "The lower wick (distance from close to low) can't be too long! Can't exceed 2.5% of the Bollinger Band spread. Too long means it was a one-sided dump with a recovery — I avoid those setups!"

---

### Condition 5: Price Broke Below Bollinger Band

```
close < lower.shift()
```

**Plain English**:
> "Closing price must be below the previous candle's Bollinger Band lower band! I want this exact 'break below support' feeling! This is the core of the strategy — price below the lower band, ready to bounce!"

---

### Condition 6: Closing Price Didn't Rise

```
close <= close.shift()
```

**Plain English**:
> "Closing price must be less than or equal to the previous candle's close! Can't be chasing a rally — I want to enter while it's falling or consolidating. Chasing? Never!"

---

### Buy Conditions Summary Table

| # | Formula | Plain English |
|---|---------|---------------|
| 1 | lower.shift() > 0 | Bollinger lower band must be valid |
| 2 | bbdelta > close × 0.7% | Bollinger Band spread must be wide enough |
| 3 | closedelta > close × 1.7% | Price must be moving |
| 4 | tail < bbdelta × 2.5% | Lower wick can't be too long |
| 5 | close < lower.shift() | Price broke below Bollinger lower band |
| 6 | close <= close.shift() | Closing price didn't rise |

**Plain English Summary**:
> "What I'm looking for: Bollinger Bands spread wide, price clearly moving, broke below the lower band on close, but didn't keep falling, wick not too long — classic pre-rebound signal!"

---

## 4. Protection Mechanisms: Three Lines of Defense

This strategy's protection mechanisms are simple but have three lines of defense:

### First Line: Bollinger Band Spread Filter

Bollinger Band spread (bbdelta) must be large enough:
- Filters out markets with too little volatility
- Avoids frequent trading in narrow channels
- Ensures sufficient rebound space

### Second Line: Movement Amplitude Requirement

closedelta must exceed 1.7%:
- Ensures the market has sufficient activity
- Avoids trading in stagnant markets
- Needs obvious intraday price changes

### Third Line: 5% Stop-Loss Hard Line

```
stoploss = -5%
```

**Plain English**:
> "What, expecting more protection? These three lines are all there is! Relying on the 5% stop-loss to hold the fort! So this strategy has extremely high win rate demands — you MUST win over 80% of trades, otherwise you're just losing money!"

---

## 5. Exit Logic: None! All Automatic!

### 🚪 Exit Mechanism

This strategy has **no custom sell signals**!

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    no sell signal
    """
    dataframe.loc[:, 'sell'] = 0
    return dataframe
```

**Plain English**:
> "No sell signals from me! Just two ways out:
> 1. Made 1.25%, bot auto-sells
> 2. Lost 5%, bot auto-cuts
> That's it! No brain work, conditions met = get out!

---

## 6. The Strategy's "Personality"

### 🧠 Personality Profile

| Trait | Description |
|-------|-------------|
| **High Frequency** | 1-minute chart, trades疯狂 |
| **Conservative** | Target is low, 1.25% and out |
| **Harsh Stop-Loss** | 5% stop-loss hurts |
| **Impatient** | No patience for big gains, takes profit and runs |
| **Mechanical** | Fully automated, doesn't care about market mood |

### 🗣️ The Strategy's Inner Monologue

> "What, I need to analyze the trend? No way!
>
> Bollinger Bands opened? Opened!
> Price broke below lower band? Broke!
> There's movement? Yes!
> Good, ALL IN!
>
> Hit 1.25%? Out!
> Hit 5%? Cut!
>
> Next one! Faster, faster! Can't sleep if I don't do dozens of trades a day!"

---

## 7. When to Use It?

| Scenario | Suitability | Notes |
|---------|-------------|-------|
| High-Volatility Ranging | ★★★★★ | Perfect! Price repeatedly touches Bollinger Bands |
| Consolidation | ★★★★☆ | Bollinger Bands repeatedly converge/diverge |
| One-Sided Decline | ★★☆☆☆ | Stop-loss triggers until you question your life |
| One-Sided Rally | ★★★☆☆ | Some buy signals decrease |
| Low-Volatility Market | ★☆☆☆☆ | closedelta doesn't meet threshold |
| Extreme Boom/Bust | ★★★☆☆ | Too much volatility may lead to frequent trading |

**Best suited markets**:
- Coins with intense intraday swings
- High-liquidity major coins
- Products with clear support/resistance levels

**Not suited for**:
- Low-volatility stagnant markets
- One-sided bear markets
- Illiquid niche coins

---

## 8. Summary: What's the Verdict?

### One-Line Rating

> **BinHV45 = 1-minute + Bollinger Band lower band breakout + 1.25% and out**

### Who's It For?
- ✅ High-frequency trading enthusiasts
- ✅ Traders with low-fee channels
- ✅ Investors pursuing small-target, multiple-accumulation
- ✅ Veterans who understand Bollinger Bands
- ✅ Experts who can maintain 80%+ win rate

### Who's It NOT For?
- ❌ Newbies (win rate requirement too high)
- ❌ People without low-fee channels (fees eat profits)
- ❌ Conservative investors (too risky)
- ❌ Low-volatility market players (signals too few)
- ❌ One-sided market traders (will get stopped out repeatedly)

### Strengths

1. Frequent trading, plenty of opportunities
2. Clear objectives, takes profit when reached
3. Simple logic, easy to understand
4. Parameters can be optimized
5. Fully automated

### Weaknesses

1. Win rate demand extremely high (80%+)
2. High-frequency trading fees eat into profits
3. No trend judgment, loses in one-sided markets
4. 5% stop-loss hurts
5. No dynamic adjustment capability

---

## 9. ⚠️ Final Warning (Must Read!)

### The Brutal Truth About Win Rate

**Say it three times: You need 80%+ win rate to profit!**

Let's do the math:

Assume 10 trades:
- 70% win rate: 7 wins × 1.25% = 8.75%, 3 losses × 5% = 15%, net loss **-6.25%**
- 75% win rate: 7.5 wins × 1.25% = 9.375%, 2.5 losses × 5% = 12.5%, net loss **-3.125%**
- 80% win rate: 8 wins × 1.25% = 10%, 2 losses × 5% = 10%, **just barely breakeven**
- 85% win rate: 8.5 wins × 1.25% = 10.625%, 1.5 losses × 5% = 7.5%, net profit **3.125%**

**Conclusion: Only win rate exceeding 80% generates profit! This is extremely demanding — most quantitative strategies can't reach this level.**

### Fee Assassin

1-minute timeframe means:
- Dozens or hundreds of trades per day possible
- Every trade has fees
- 1.25% profit, fees might eat 0.1%–0.3%
- **Your actual profit might only be 0.95%–1.15%**

**Must choose a low-fee exchange!**

### One-Sided Market Killer

If encountering continuous one-sided decline:
- Price repeatedly breaks below Bollinger Band lower band
- You repeatedly buy
- Stop-loss repeatedly triggers
- **You'll lose until your mother doesn't recognize you**

### Slippage Risk

1-minute timeframe:
- Price changes extremely fast
- Price may have moved by the time your order fills
- 1.25% profit, slippage might eat most of it

### Newbie Warning

1. **Calculate first**: 1.25% profit vs 5% stop-loss — must win 80%+ to make money!
2. **Calculate fees**: High-frequency trading, fees might be your biggest cost
3. **Pick the market**: Must be high-volatility, low-volatility won't work
4. **Use small capital**: Test for a few months first, don't YOLO
5. **Watch slippage**: 1-minute timeframe slippage can be brutal

---

**Final Note**: Strategy looks simple but demands extreme execution discipline, market selection, and fee control. Thin margins, high volume only works if win rate is high — otherwise it's thin margins, huge losses! Survival first! 🙏
