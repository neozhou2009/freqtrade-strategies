# SMAOffsetV2 Strategy: The Simple and Straightforward Trend Follower

> **Nickname**: The Trend Puppy  
> **Job**: Only flies kites when the wind is strong  
> **Timeframe**: 5-minute + 1-hour for trend watching

---

## 1. What is This Strategy?

Simply put, **SMAOffsetV2** is a strategy that:

- Only buys when the trend is upward
- Waits for a 4% price discount before entering
- Runs when the trend changes or profit target is reached

Like **flying a kite** — you only go out to fly when the wind is strong (uptrend), and you wait for the kite to be 4% cheaper before buying. When the wind direction changes or the kite has flown enough, immediately reel in and go home 🪁

---

## 2. Core Configuration: Basically "Watch the Wind Before Acting"

### Take-Profit Rules (ROI Table)

```
Immediate: Run at 100% profit
```

**Translation**: ROI set to 100%, basically saying "I won't rely on ROI for profit-taking, all on sell signals and stop loss". Simple and straightforward!

### Stop Loss Rules

```
Fixed stop loss: -20% (throw in the towel at 20% loss)
Dynamic stop loss: Held 40 minutes + lost 10% → tighten stop loss to -1%
```

**Translation**:
- If you just bought and it's losing, don't panic yet, give the strategy 40 minutes to "self-rescue"
- After 40 minutes if still losing more than 10%, forget it, stop loss and run
- If you stubbornly hold to -20% loss, the system forces you to cut

---

## 3. One Buy Condition: Simplicity is Beauty

This strategy has only one buy condition, not fancy like some other strategies.

### 🎯 Buy Condition: Trend Up + Price Discount

**Core Logic**: 1-hour trend up + price 4% below moving average

**Plain English**:
> "The big trend is rising, now price has pulled back 4%, great opportunity to grab a bargain!"

**Specific Conditions**:
```python
go_long > 0           # 1-hour EMA fast line > slow line (trend up)
close < sma_30_offset  # Price below SMA(20) × 0.96 (4% discount)
volume > 0            # There's trading
```

**Classic Line**:
> "Wind is strong, kite happens to be on sale, buy!"

---

## 4. Protection Mechanism: Give Opportunity But Don't Be Stubborn

### 4.1 Dynamic Stop Loss: Gentle Waiting

This stop loss mechanism is quite interesting:

```python
if holding_time > 40 minutes AND loss > 10%:
    stop_loss = -1%  # Tighten!
else:
    stop_loss = -99%  # Ignore for now
```

**Plain English**:
> "Bro, you just bought in, I'll give you 40 minutes to see if you can make it back. If you're still losing 10% after 40 minutes, I'll help you stop loss."

This is a **"give opportunity first, retreat if it doesn't work"** mechanism, quite human.

### 4.2 Trend Filter: Ignore Downtrends

Only buys when 1-hour EMA golden cross (fast line above slow line).

**Plain English**:
> "Wind blows east, I run east; wind blows west, I run west. Wind stopped? I go home and sleep, not running around."

---

## 5. Sell Logic: Two Signals, Satisfy One and Run

### 5.1 Sell Signals

```
Signal #1: Trend reversal (EMA death cross)
Signal #2: Price rises 1.2% above moving average
```

**Plain English**:

| Signal | Condition | Human Translation |
|--------|-----------|-------------------|
| #1 Trend reversal | 1-hour EMA fast line < slow line | "Wind direction changed, reel in quick!" |
| #2 Price breakout | Price > SMA(20) × 1.012 | "Kite flew enough, made enough, retreat!" |

### 5.2 Only Sell When Profitable

```python
sell_profit_only = True  # Only use sell signal when profitable
```

**Plain English**:
> "If you're losing, ignore the sell signal. Wait until you're profitable."

This design is to avoid being stopped by sell signals during floating losses, giving the strategy more recovery opportunity.

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simple and straightforward**: Just one buy condition, two sell conditions, crystal clear
2. **Trend protection**: Only buys in uptrend, avoids counter-trend bottom-fishing
3. **Dynamic stop loss**: Gives opportunity to recover, retreats if it doesn't work, quite human
4. **Small codebase**: Suitable for learning Freqtrade strategy development

### ⚠️ Cons (Roast Section)

1. **Hardcoded parameters**: 4% offset, 20/25 EMA are all hardcoded, can't optimize
2. **Offset too large**: 4% discount is a bit harsh, might miss some opportunities
3. **No trailing stop**: After price goes up, if it comes back down, might "ride the rollercoaster"
4. **Struggles in ranging markets**: EMA frequently crosses, trend judgment fails

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Slow bull rise | ✅ Use it! | Trend upward, plenty of pullback buying opportunities |
| 🔄 Sideways oscillation | ❌ Don't use | EMA frequently crosses, signals distorted |
| 📉 One-sided decline | ⚠️ Stay out | Trend filter will block buying, that's good |
| ⚡ Severe volatility | ⚠️ Use cautiously | 4% offset may be penetrated |

---

## 8. Summary: How's This Strategy Really?

### One-Sentence Review
> "A simple and clean trend-following strategy, suitable for learning and understanding Freqtrade strategy framework."

### Who Should Use It?
- ✅ Beginners wanting to learn Freqtrade strategy development
- ✅ People who like simple logic
- ✅ People who only trade in uptrends
- ✅ People who can accept 40 minutes of "self-rescue time"

### Who Shouldn't Use It?
- ❌ People wanting complex strategies
- ❌ People wanting to profit in ranging markets
- ❌ People hoping for optimizable parameters
- ❌ People wanting trailing take-profit

### My Suggestions
1. **Use for learning**: Simple code, great for entry
2. **Modify and upgrade**: Add HyperOpt parameters, trailing stop, etc.
3. **Backtest to verify**: Check historical performance first
4. **Small capital live trading**: Confirm effectiveness before increasing investment

---

## 9. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Follow the Trend

SMAOffsetV2's money-making philosophy:

**"Where the wind blows, I run. No wind? I go home and sleep."**

- **Trend filter**: Use 1-hour EMA to judge wind direction
- **Price offset**: Wait for price discount before buying
- **Dual exit**: Leave when wind direction changes, also leave when profit is made

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:---------------------------|
| 📈 Slow bull trend | ⭐⭐⭐⭐⭐ | Wind is strong, plenty of pullback opportunities, perfect fit |
| 📉 One-sided crash | ⭐⭐⭐⭐☆ | Trend filter blocks buying, stay out safely! |
| 🔄 Sideways oscillation | ⭐⭐☆☆☆ | EMA keeps crossing, says up today and down tomorrow, dizzy |
| ⚡️ Severe volatility | ⭐⭐⭐☆☆ | 4% offset may be instantly penetrated |

**One-Sentence Summary**: **Trend is its best friend, oscillation is its enemy, in decline it just lies flat.**

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Comment |
|-------------|------------------|---------|
| Timeframe | 5-minute | Default is fine, don't mess with it |
| Informative timeframe | 1-hour | Used to judge trend direction |
| Trading pair | Major coins | Clear trends, don't play sketchy coins |

### 10.2 Key Parameters (Hardcoded, Can't Change)

```python
# SMA offset parameters
sma_offset = 0.96         # Buy: 4% below moving average
sma_offset_pos = 1.012    # Sell: 1.2% above moving average
base_nb_candles = 20      # SMA period

# EMA parameters
ema_fast = 20             # Fast line
ema_slow = 25             # Slow line
```

**Roast**: These parameters are all hardcoded in the code, you need to modify the code yourself if you want to optimize 🤣

### 10.3 Hardware Requirements (Almost None)

This strategy is so simple, almost no hardware requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | More than enough |
| 10-30 pairs | 4GB | 8GB | Very relaxed |
| 30+ pairs | 8GB | 16GB | Run whatever |

**Warning**: Strategy is simple, but if you run too many trading pairs you still need memory 😅

### 10.4 Backtesting vs Live Trading

**Backtesting may be mediocre**, because:
- Parameters are fixed, never optimized
- Large offset, may miss some opportunities

**Live trading may be okay**, because:
- Simple logic, hard to have bugs
- Trend filter can avoid many losing trades

**Recommended Process**:
1. Backtest to see what markets it performs well in
2. Paper trade for a while
3. If you want, you can modify the code to add parameter optimization
4. Small capital live verification

---

## 11. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **EMA uses 20/25 instead of traditional 12/26**:
   > "The author used an uncommon combination. 20/25 is closer together, reacts faster, but also more easily fooled by false signals."

2. **Dynamic stop loss's 40 minutes + 10% design**:
   > "This design is quite human: give the strategy 40 minutes to self-rescue, if it doesn't work then retreat. Not stopping immediately on loss, but not holding stubbornly either."

3. **go_long uses *2 instead of *1**:
   > "Actually *1 and *2 have the same effect, the author might have wanted to distinguish other signals later. A bit redundant in the code, but doesn't affect functionality."

4. **Thanks to tirail**:
   > "The code comments thank tirail for sharing the original SMAOffset, showing this is an improved version standing on the shoulders of giants."

---

## 12. The Very Last

### One-Sentence Review
> "A clean and sharp trend strategy, suitable for entry learning, also suitable for modification and upgrade."

### Who Should Use It?
- ✅ People wanting to learn Freqtrade strategy development
- ✅ People who like simple logic
- ✅ People who only trade in uptrends
- ✅ People willing to modify code themselves

### Who Shouldn't Use It?
- ❌ People wanting "out of the box" complex strategies
- ❌ People wanting to profit in ranging markets
- ❌ People not wanting to modify code to optimize parameters
- ❌ People expecting perfect performance

### Suggestions for Manual Traders
If you want to manually use this strategy's logic:
1. Draw 1-hour EMA(20) and EMA(25)
2. Wait for fast line above slow line (uptrend)
3. Wait for price to pull back 4% below 20 SMA
4. Buy, set 20% stop loss
5. If still losing 10% after 40 minutes, stop loss and leave
6. If EMA death cross or price rises 1.2% above SMA, sell

---

## 13. ⚠️ Risk Re-emphasis (Must Read!)

### Simple Doesn't Mean Profitable

SMAOffsetV2 has simple logic, but that doesn't mean it definitely makes money:

> **Simple strategy doesn't mean easy profits, the market never plays by logic.**

Simply put: **The simpler the strategy, the easier it is to "be figured out". If everyone knows this logic, who's paying whom?**

### Hidden Risks of Simple Strategies

In live trading, you may encounter:
- **Missing opportunities**: 4% offset is too large, many opportunities missed
- **Ranging losses**: Trend judgment fails, frequent stop losses
- **Parameter aging**: Hardcoded parameters may not suit current market
- **Chasing rises selling falls**: May sell at low prices when trend reverses

### My Advice (Straight Talk)

```
1. Treat it as learning material, understand Freqtrade strategy framework
2. Backtest to see performance, understand what markets it works in
3. If you want to use it, consider modifying: add parameter optimization, trailing stop, etc.
4. Don't expect too much, simple strategies have simple limitations
```

**Remember**: No matter how simple the strategy is, the market won't give advance notice when teaching you a lesson. Light position testing, survival is most important! 🙏