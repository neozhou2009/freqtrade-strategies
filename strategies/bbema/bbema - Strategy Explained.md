# bbema: Simplest EMA Crossover + Bollinger Band Auxiliary

> **Nickname**: Strategy World's "Elementary Student", Entry-Level Player, Chill Player  
> **Profession**: Minimalist who places orders when two moving averages cross  
> **Timeframe**: 1 hour (Long-term player)

---

## 1. What's This Thing?

Simply put, **bbema** is:
- A minimalist strategy with **only 2 moving averages**
- A simple logic of **golden cross buy, death cross sell**
- **Bollinger Bands just decoration** — calculated but not used
- A chill player that **runs at 20% profit**
- **One of Freqtrade's official default strategies**

Like a kid just learning to ride a bike — pedals with two legs and goes, no fancy moves 🚲

**Why called bbema?**
- **bb** = Bollinger Bands
- **ema** = Exponential Moving Average

Sounds advanced? Actually Bollinger Bands don't participate in trading signals at all, just "decoration" 😂

---

## 2. Core Config: Basically "Wait for Big Trend"

### Profit-Taking Rules (ROI Table)

```
Hold → Run at 20% profit 🤑
```

**Translation**:
> "I'm not greedy, run after doubling... oh wait, 20% is enough. But honestly, 20% for 1-hour level, a bit hard to trigger."

### Stoploss Rules

```
Loss 10% → Leave
```

**Translation**:
> "I admit defeat at 10% drop, not playing with you anymore. This is standard stoploss line in crypto circle."

### Order Types

| Type | Setting |
|------|---------|
| Entry | Limit order (save fees) |
| Exit | Limit order (save fees) |
| Stoploss | Market order (ensure execution) |

---

## 3. 1 Entry Condition: EMA Golden Cross

This strategy's entry condition **simple to unbelievable** — just one!

### 🎯 Category 1: Trend Confirmation (1 Condition)

**Core Logic**: EMA10 crosses above EMA50

**Plain English**:
> "10-period MA shoots up from below, exceeds 50-period MA — golden cross! BUY!"

**Code looks like**:
```python
# Just this one line, really just this one line
qtpylib.crossed_above(dataframe["ema10"], dataframe["ema50"])
```

**What's Golden Cross?**

Imagine two lines racing:
- EMA10 is **sprinter** (reacts fast, recent prices weighted more)
- EMA50 is **marathon runner** (steady, changes slow)

When sprinter catches up from behind and overtakes marathon runner — this is **golden cross**!

**Why use EMA not SMA?**

EMA more sensitive to recent prices, reacts faster. Like you care more about today's mood than average mood of past month 😄

---

## 4. Protection: ...None!

This strategy has **no protection mechanisms at all**!

Don't look, really none. Like a house with unlocked door — door wide open, anyone can enter 🏠

**What's Protection Mechanism?**

Complex strategies usually have these "fuses":
- Confirmation conditions to prevent false breakouts
- Filtering conditions to prevent ranging markets
- Protection conditions to prevent sharp drops

**bbema's attitude**:
> "Protection? What protection? Golden cross is signal, just do it!"

This is also why said suitable for **beginners learning** — code simple, logic clear, but **live trading easily gets educated by market** 🎓

---

## 5. Exit Logic: EMA Death Cross

Exit logic completely symmetrical with entry — this is "long-short symmetrical design".

### 5.1 Base Exit Signal (1)

**Core Logic**: EMA50 crosses above EMA10

**Plain English**:
> "50-period MA falls from above, crosses through 10-period MA — death cross! SELL!"

**Code looks like**:
```python
# Also one line, completely symmetrical with entry
qtpylib.crossed_above(dataframe["ema50"], dataframe["ema10"])
```

**What's Death Cross?**

Continue using race metaphor:
- Sprinter (EMA10) gets tired while running
- Marathon runner (EMA50) slowly catches up
- When marathon runner overtakes sprinter — this is **death cross**!

Usually means: **short-term momentum weakening, may fall**.

### 5.2 Take-Profit/Stoploss

| Exit Method | Trigger Condition | Plain English |
|-------------|------------------|---------------|
| Take-Profit | Profit ≥ 20% | "Made 20%, done!" |
| Stoploss | Loss ≥ 10% | "Lost 10%, run!" |
| Death Cross | EMA50 crosses above EMA10 | "Trend reversed, retreat!" |

**Problem**: 20% take-profit too high!

For 1-hour level to rise 20%, how long to wait? Might wait until flowers wither 🌸

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simple to no friends**: Code just dozens of lines, beginners understand at a glance
2. **Long-Short Symmetry**: Entry/exit logic consistent, no bias
3. **Few Parameters**: Just two EMAs, small tuning space, hard to overfit
4. **Learning Friendly**: Freqtrade official default strategy, lots of docs, good community support

### ⚠️ Cons (Roast Section)

1. **No Protection**: No filtering at all, tons of false signals
2. **20% Too High**: For 1-hour level, this take-profit basically decoration
3. **Doesn't Distinguish Trend**: Same set in bull/bear markets, gets slapped repeatedly in ranging markets
4. **Bollinger Bands Useless**: Has bb in name, but Bollinger Bands just for looking, isn't this deceiving 🤣

**One-Sentence Summary**:
> "This is teaching entry strategy, not live trading money-making tool."

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clear uptrend | ✅ Usable | Golden cross can catch trend |
| Clear downtrend | ✅ Usable (short) | Death cross can exit timely |
| Ranging sideways | ❌ Don't use | Will get repeatedly stoplossed |
| Violent volatility | ⚠️ Caution | 10% stoploss may trigger frequently |

**Best Scenarios**:
- Crypto big bull market, trend clear
- Or you want to learn strategy code, use it as textbook

**Worst Scenarios**:
- Ranging market, price repeatedly crosses between two MAs
- Will constantly "buy→stoploss→buy→stoploss", fees make you doubt life

---

## 8. Summary: How's This Strategy Really?

### One-Sentence Review
> "Quant trading's 'Hello World' — beginner must-learn, veteran must-abandon."

### Who Should Use It?
- ✅ Quant trading beginners (learning strategy code structure)
- ✅ People wanting to understand EMA crossover principles
- ✅ People wanting to test Freqtrade platform features
- ✅ Beginners who don't mind losing money practicing

### Who Should NOT Use It?
- ❌ People wanting to make money with strategy live trading
- ❌ Ranging market traders
- ❌ Investors with risk control requirements
- ❌ People who mastered basics wanting to advance

### My Suggestions
1. **Use as textbook**: Learn EMA crossover, indicator calculation, strategy structure
2. **Don't go live directly**: Add some protection mechanisms before considering
3. **Adjust parameters**: Change take-profit to 5-10%, don't wait for 20%
4. **Add filtering conditions**: At least add RSI or volume filtering

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Trend Following's "Naked Version"

bbema is simplest **trend following strategy**, code volume maybe just 50 lines, what concept? Length of an intro tutorial 📖

**Its Profit Philosophy**:
> "I follow when trend comes, I retreat when trend leaves."

- **Simple and Brutal**: No complex confirmation conditions
- **Fast Reaction**: EMA more sensitive than traditional MAs
- **No Protection**: Gets repeatedly harvested in ranging markets

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Clear uptrend | ⭐⭐⭐⭐☆ | Golden cross catches trend, can eat big meat |
| 📉 Clear downtrend | ⭐⭐⭐⭐☆ | Death cross exits timely, protects principal |
| 🔄 Ranging sideways | ⭐☆☆☆☆ | Repeated golden/death cross, fees eat you full |
| ⚡️ Sharp rise/fall | ⭐⭐☆☆☆ | Reaction may lag, miss best entry points |

**One-Sentence Summary**:
> "Can drink soup when trend clear, gets repeatedly slapped in ranging markets."

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration Item | Suggested Value | Roast |
|-------------------|-----------------|-------|
| Number of pairs | 1-10 | Don't be greedy, test first |
| Timeframe | 1h (default) | Can also try 4h |
| Min volume | Normal settings | No special requirements |

### 10.2 Parameter Adjustment Suggestions

```python
# Default take-profit (too aggressive)
minimal_roi = {"0": 0.20}  # 20%, wait you to death

# Suggest change to
minimal_roi = {
    "0": 0.10,  # 10% immediate take-profit
    "30": 0.05,  # Run at 5% after 30 min
    "60": 0.02   # Accept 2% after 1 hour
}

# Stoploss can keep
stoploss = -0.10  # 10%, standard setting
```

### 10.3 Hardware Requirements (Important!)

This strategy **very lightweight**, extremely low hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-20 | 512MB | 1GB | Silk smooth |
| 20-50 | 1GB | 2GB | Smooth |
| 50+ | 2GB | 4GB | Enough |

**Roast**:
> "This strategy saves hardware, saves electricity, saves brain cells. Raspberry Pi can run it."

### 10.4 Backtest vs Live Trading

**Backtest Performance**:
- Years with clear trends, backtest data looks good
- Ranging years, gets repeatedly stoplossed

**Live Trading Differences**:
- Slippage may eat part of profits
- False breakouts more than backtest
- Suggest test with small capital first

**Suggested Process**:
1. Backtest recent 1 year data
2. Paper trading test for 1 month
3. Small capital live test
4. Gradually increase position

**Don't go all-in immediately**, even simplest strategies need breaking in!

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

Look carefully at code, you'll find some interesting things:

1. **Bollinger Bands are decoration**
   ```python
   # Calculated Bollinger Bands
   bollinger = qtpylib.bollinger_bands(...)
   # But completely not used in trading signals
   ```
   > "I calculated Bollinger Bands, but I don't want to use them, what you gonna do?"

2. **close10 variable unused**
   ```python
   dataframe["close10"] = dataframe["close"].shift(periods=-10)
   # This line exists, but never referenced
   ```
   > "I defined variable, but I just won't use it, play."

3. **Simplicity extreme**
   > Code so simple can serve as Freqtrade teaching case, author may be intentionally keeping it simple.

**Guess**: This may be Freqtrade official teaching example, not live trading strategy.

---

## 12. Final Final Thoughts

### One-Sentence Review
> "Quant world's 'Hello World' — first strategy you write, not strategy you make money with."

### Who Should Use It?
- ✅ Beginners just entering quant trading
- ✅ People wanting to learn Freqtrade platform
- ✅ People wanting to understand EMA crossover principles
- ✅ Adventurers who don't mind practicing with small money

### Who Should NOT Use It?
- ❌ Investors wanting stable profits
- ❌ People focused on ranging markets
- ❌ Institutions needing complex risk control
- ❌ Veterans who already know how to write strategies

### Manual Trader Suggestions

If you're manual trading, can borrow this approach:
- Use EMA10 and EMA50 to judge trend
- Golden cross go long, death cross observe
- But add your own filtering conditions, like RSI, support/resistance levels
- Take-profit don't wait for 20%, 5-10% more realistic

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtest Looks Great, Live Trading Needs Caution

bbema in historical backtests, may perform well during periods with clear trends — but there's a trap:

> **Because logic too simple, it has no ability to filter false signals.**

Simply put:
> "Drinks soup when trend comes, gets repeatedly beaten when ranging comes."

### Hidden Risks of This Strategy

In live trading, simple logic may cause:

1. **Frequent False Breakouts**
   - EMA golden cross may be false breakout
   - Immediately death cross stoploss after buying
   - Fees make you doubt life

2. **Ranging Market Harvester**
   - Price repeatedly crosses between MAs
   - Buy→stoploss→buy→stoploss
   - Strategy becomes exchange's fee worker

3. **20% Take-Profit is Decoration**
   - 1-hour level rising 20% needs big market
   - Most times can't wait for take-profit
   - Finally exits via stoploss or death cross

### My Suggestions (Real Talk)

```
1. Use as textbook, learn strategy structure
2. Add protection mechanisms on this foundation:
   - RSI filtering overbought/oversold
   - Volume confirming trend
   - Bollinger Band boundary filtering (this time really use it)
3. Adjust take-profit to 5-10%
4. Paper trade test at least 1 month
5. Small capital live verification
```

**Remember**:
> "Simple strategy doesn't equal stable strategy. Market will educate everyone running naked."

---

**Final Reminder**: No matter how simple the strategy, the market won't say hello when teaching you lessons. Light position test, staying alive is most important! 🙏
