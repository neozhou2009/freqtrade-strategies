# Cluc4 Strategy: Bollinger Bands + ROCR "Trend Hunter"

> **Nickname**: 1-Minute Speed Demon
> **Profession**: Ultra short-term hunter, specializing in trend pullback captures
> **Timeframe**: 1 Minute (main) + 1 Hour (auxiliary)

---

## 1. What's This Strategy All About?

Simply put, **Cluc4** is a strategy that:

- First checks the big picture (1-hour uptrend), then looks for small opportunities (1-minute Bollinger Band signals)
- Fast entry, fast exit; positions usually held minutes to tens of minutes
- Has two entry modes: one catches crash rebounds, one catches "low volume bottom"

Think of it like an **astute short-term hunter**: confirms direction is correct first (ROCR trend), then acts on the small cycle. Its personality is — **cautious but fast-acting**, takes profit and runs, cuts losses fast.

> This strategy is like an experienced fisherman: checks weather first (ROCR trend) before casting net, doesn't fish against the wind, only casts where fish are abundant.

---

## 2. Core Settings: Basically "Make 1.5% and Run, Lose 1% and Admit Defeat"

### Take-Profit Rule (ROI Table)

| Holding Time | Target Profit | Plain English |
|-------------|---------------|----------------|
| 0-20 minutes | 1.5% | Quick profit; don't linger |
| 20-30 minutes | 0.5% | Didn't surge quickly? Lower expectations |
| After 30 minutes | 0.1% | Break-even and run |

**Translation**: This is a typical short-term strategy; satisfied with a little profit; not like those greedy strategies that won't sell until doubling.

### Stop-Loss Rule

```
stoploss = -1%
```

**Translation**: Cut losses at 1% and admit defeat; absolutely no holding through. This stop-loss is extremely tight — means you may frequently get stopped out, but each loss is small.

---

## 3. Two Entry Conditions: I've Categorized Them for You

This strategy's entry has a **hard gate**: must pass ROCR filter first, then look at specific signals.

### 🚪 First, the Hard Gate: ROCR Trend Filter

```
1-hour ROCR > 0.65
```

**Plain English**:
> "I'll only consider buying when the 1-hour timeframe shows an uptrend. Counter-trend? Don't even think about it!"

This is like checking both ways for cars before crossing the street. ROCR is a rate-of-change indicator; 168-period ROCR on the 1-hour chart equals **one week** of price changes. ROCR > 0.65 means price has risen significantly over the past week; trend clearly upward.

### 🎯 Mode 1: BinHV Variant — Catch Crash Rebounds

**Core Logic**: Price suddenly crashes hard then closes near the lower band; short lower shadow means it can't fall further and likely rebounds!

**Plain English**:
> "Price got beaten to the floor but didn't break too far; someone is buying. Time to get in and捡便宜!"

**6 conditions must all be met**:

| Condition | Plain English Translation |
|-----------|--------------------------|
| BB lower band valid | Data normal; not an anomaly |
| BB bandwidth > close × 0.6% | Enough volatility; room to maneuver |
| Price change > close × 1.3% | This candle volatile enough |
| Lower shadow < bandwidth × 96.8% | Short lower shadow; not fake drop |
| Price < previous BB lower band | Price broke below lower band; "on sale" |
| Price ≤ previous close | Price didn't bounce back; still at lows |

**One-liner**:
> "Price suddenly crashed hard then closed near lower band; short lower shadow, can't fall further; rebound likely!"

---

### 📉 Mode 2: Cluc Variant — Catch "Low Volume Bottom"

**Core Logic**: Price drops to extremely low levels; volume extremely shrinks (nobody willing to sell); bottom likely!

**Plain English**:
> "Price has fallen so much nobody wants to sell; volume shrunk to extremes. This is捡带血筹码!"

**3 conditions must all be met**:

| Condition | Plain English Translation |
|-----------|--------------------------|
| Price < EMA50 | Below mid-term MA; weak position |
| Price < BB lower band × 0.013 | Price at extremely low level |
| Volume < 30-day avg × 28 | Volume extremely low (floor volume) |

**One-liner**:
> "Nobody willing to sell (floor volume); price also at floor; bottom likely!"

---

### Entry Logic Summary

```
Buy = (1-hour ROCR > 0.65) AND (BinHV mode OR Cluc mode)
```

---

## 4. Protection Mechanisms: Three "Life Preservers"

Cluc4 has 3 protection layers ensuring you don't lose too badly:

| Protection Layer | Mechanism | Plain English |
|-----------------|-----------|---------------|
| **Layer 1** | ROCR trend filter | Only trade with-trend; don't catch falling knives |
| **Layer 2** | 1% tight stop-loss | Cut losses small; don't linger |
| **Layer 3** | Multi-timeframe confirmation | View both 1-minute and 1-hour; dual confirmation |

These 3 layers are like a fisherman's life jacket, lifebuoy, and lifeboat — layered protection ensures you won't capsize from one mistake.

---

## 5. Sell Logic: Simple and Brutal

### 5.1 Main Sell Condition

```
Price crosses above BB middle band AND has volume
```

**Plain English**:
> "Price rose to BB's middle position; likely hit resistance. Exit strategy, lock in profits!"

BB middle band is usually the 20-day MA; price rebounding from lower to middle band often meets resistance. Strategy chooses to take profit here rather than greedily waiting for the upper band.

### 5.2 Sell Priority

```
ROI take-profit > Signal sell > Stop-loss
```

This means:
- If price quickly rises to ROI target → exit via ROI
- If price breaks through middle → sell via signal
- If neither met and loss hits 1% → stop-loss

### 5.3 Only Sell When Profitable

```python
exit_profit_only = True
```

**Plain English**: Only proactively sell when making money; wait for stop-loss if losing. No mercy, no blind cutting.

---

## 6. Strategy "Personality"

### ✅ Strengths

1. **Has trend protection**: ROCR filter ensures no counter-trend trades; avoids catching knives
2. **Dual entry modes**: Two modes increase opportunities without lowering quality
3. **Tight stop-loss**: 1% stop-loss; small losses many times; won't cripple from one loss
4. **Fast entry/exit**: 1-minute timeframe; short holding; high capital efficiency
5. **Simple and clear**: Logic straightforward; Bollinger + ROCR; no complex conditions

### ⚠️ Weaknesses

1. **May miss trend starts**: Won't buy until ROCR > 0.65; by the time trend confirms, price may have risen significantly
2. **High trading frequency**: 1-minute timeframe; many signals; fees are a big problem
3. **Many false breakouts**: 1-minute false breakouts frequent; 1% stop-loss may trigger repeatedly
4. **Needs monitoring**: Short-term strategy; needs stable network and fast execution

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ Actively use | Best scenario; ROCR filter effective; trend-following |
| 🔄 Wide-range oscillation | ⭐⭐⭐⭐☆ Can use | BB signals effective; opportunities plentiful |
| ⚡ High volatility | ⭐⭐⭐⭐☆ Can use | Large moves; many condition triggers, but watch for false breakouts |
| 📉 Downtrend | ⭐⭐☆☆☆ Use carefully | ROCR filter stops most trades; may stay in cash |
| 🌙 Low-volatility consolidation | ⭐⭐☆☆☆ Not recommended | Too little movement; signals unclear |
| 🌃 Late night/holidays | ⭐☆☆☆☆ Not recommended | Low volatility; sparse signals |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> "A strategy with strong survival instincts; takes profit and runs, cuts losses fast; never drags."

### Who's It For?
- ✅ People who have time to monitor
- ✅ People who can accept 1% tight stop-loss
- ✅ Users with low fees (< 0.2%)
- ✅ People trading high-liquidity coins
- ✅ People who understand trend + pullback logic

### Who's It NOT For?
- ❌ People without time to monitor
- ❌ People who don't want frequent trading
- ❌ Platforms with high fees (> 0.2%)
- ❌ People chasing single big gains
- ❌ People who only want long-term holds

### My Suggestions
1. **Fees are critical**: Ensure total fees < 0.2%; otherwise this strategy may not profit
2. **Network latency must be low**: 1-minute timeframe; speed is money
3. **Iron discipline**: Strictly execute stop-loss; no fantasies
4. **Reasonable expectations**: Earn a little each time; accumulate through repetition

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: First Check Trend, Then Find Opportunities

Cluc4's money-making philosophy:

1. **ROCR filter**: Only trades when trend is up; avoids catching falling knives
2. **Bollinger positioning**: Buy near lower band; sell near middle band
3. **Fast exit**: 1.5% starting ROI; accumulates small wins

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | Best scenario; trend protection effective; trend-following feels great |
| 🔄 Wide-range oscillation | ⭐⭐⭐⭐☆ | BB signals frequent; profits good, but mind those fees |
| 📉 Downtrend | ⭐⭐☆☆☆ | ROCR filter stops most trades; basically staying in cash |
| ⚡️ High volatility | ⭐⭐⭐⭐☆ | Many opportunities, but watch false breakouts getting stopped out |

**Bottom Line**: Best performance in uptrends and wide-range oscillation markets; basically flat in downtrends.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| Number of pairs | 10-20 | Diversify risk; increase signal opportunities |
| Max positions | 2-4 | Control total risk exposure |
| Single position | 2-5% | 1% stop-loss = 0.02%-0.05% per trade risk |
| Timeframe | 1m (forced) | Strategy design requires |

### 10.2 Coin Selection

| Type | Recommendation | Reason |
|------|----------------|--------|
| Mainstream coins | ✅ Recommended | Good liquidity; moderate volatility |
| Altcoins | ⚠️ Use carefully | High volatility, but slippage risk also large |
| New coins | ❌ Not recommended | Poor liquidity; inaccurate data |

### 10.3 Hardware Requirements

1-minute timeframe needs **fast execution**:

| Number of Pairs | Minimum RAM | Recommended RAM | Note |
|----------------|-------------|----------------|------|
| 10-20 pairs | 512MB | 1GB | Sufficient |
| 20-40 pairs | 1GB | 2GB | More stable |

**Warning**: Network latency > 100ms may miss best prices 😅

### 10.4 Backtesting vs Live Trading

- Backtesting may look great
- Live has slippage, latency, fees
- Suggest running paper trading at least a week first

**Recommended Process**:
1. Test on low-fee exchange first
2. Paper trade for a week to verify
3. Small-capital live test
4. Gradually increase position

**Don't go all-in right away**, even good strategies need a磨合 period!

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Looking closely at the code, you'll find interesting things:

### 11.1 Dual Bollinger Bands' Secret

Cluc4 uses two sets of Bollinger Bands:

- **40-period BB**: Smoother; used in BinHV mode
- **20-period BB**: More sensitive; used in Cluc mode

**Plain English**:
> "Two eyes viewing the market: one looking far (40-period), one looking near (20-period); only act when both align!"

### 11.2 ROCR's Secret

ROCR (Rate of Change Ratio) measures price change rate:

```
ROCR = Today's close / N-periods-ago close
```

168-period ROCR on 1-hour chart = 168 hours = **7 days** (one week)

So ROCR > 0.65's real meaning:
> "Price rose significantly over the past week; trend up; can trade with trend!"

### 11.3 Manual Trading Simplified Version

If you want to follow manually, simplify it:

1. Open 1-hour chart; confirm ROCR > 0.65 (or price clearly trending up)
2. Switch to 1-minute chart; add Bollinger Bands (20 periods, 2x std dev)
3. Wait for price touching near lower band
4. Buy; set 1% stop-loss
5. Sell when price breaks through middle band

---

## 12. The Final Word

### One-Line Verdict
> "High-frequency strategies earn 'hard work money,' not 'get rich quick money.' Survival matters more than making money!"

### Who's It For?
- ✅ People with time to monitor
- ✅ People who can accept 1% tight stop-loss
- ✅ Users with low fees (< 0.2%)
- ✅ People trading high-liquidity coins
- ✅ People who understand trend + pullback logic
- ✅ People pursuing steady small gains who can accept high-frequency trading

### Who's It NOT For?
- ❌ People without time to monitor
- ❌ People who don't want frequent trading
- ❌ Platforms with high fees (> 0.2%)
- ❌ People chasing single big gains
- ❌ People who only want long-term holds
- ❌ People with poor psychology who easily anxious

### Manual Trading Suggestions

If you want to follow Cluc4 manually:

1. **View 1-hour trend first**: Confirm ROCR > 0.65 or price clearly up
2. **Switch to 1-minute chart**: Add Bollinger Band indicator
3. **Wait for signal**: Price touching near lower band + volume shrinking
4. **Set stop-loss immediately**: Set 1% stop-loss right after buying
5. **Fast entry/exit**: Sell when price breaks through middle band; don't be greedy

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Hidden Costs of High-Frequency Trading

Cluc4 is a **1-minute-level** high-frequency strategy, meaning:

| Risk Item | Description |
|-----------|-------------|
| **Fees** | Each trade may consume 0.1%-0.2% profit |
| **Slippage** | Market orders may buy expensive or sell cheap |
| **Signal delay** | Network latency may cause missing best prices |
| **False breakouts** | 1-minute false breakouts frequent |

**Do the math**:
- Assume each trade profits 1.5%
- Subtract buy fees 0.1% + sell fees 0.1% = 0.2%
- Subtract slippage 0.1%
- **Actual profit ≈ 1.2%**

**If fees > 0.2%, this strategy may not profit!**

### ROCR Filter Risks

ROCR filter avoids counter-trend trades but also has risks:

> At the **start of a trend**, ROCR may not yet reach 0.65; at this time the strategy will **miss the best entry point**.

When ROCR > 0.65, price may have already risen significantly.

### Possibility of Consecutive Stop-Outs

1% tight stop-loss in these situations may lead to **consecutive losses**:

- Frequent false breakouts
- High volatility markets
- Data delays

**Psychological preparation**: 5 consecutive stop-outs = -5%; need 5.3% profit to recover.

### Live Trading Checklist

| Item | Description |
|------|-------------|
| Sufficient backtesting | Backtest across different market cycles |
| Paper trade first | Run paper at least a week before live |
| Select low-fee platform | Lower Maker/Taker fees better |
| Watch network latency | Choose server with latency < 100ms |
| Control pair count | Don't be greedy; 10-20 is fine |
| Regular parameter checks | May need adjustment when market changes |

### Risk Warning Checklist

```
1. ⚠️ Fees are critical! Ensure total fees < 0.2%
2. ⚠️ 1-minute false breakouts frequent; 1% stop-loss may trigger repeatedly
3. ⚠️ ROCR filter may miss trend start opportunities
4. ⚠️ High-frequency trading needs stable network and fast execution
5. ⚠️ Consecutive stop-outs are normal; be mentally prepared
6. ⚠️ Don't use this strategy on high-fee platforms
```

### The Final Word

> **Remember: High-frequency strategies are no holy grail; they're "hard-work-gets-rich" trading methods.**

Cluc4 is a meticulously designed short-term strategy; its success depends on:

1. **Low-fee environment** — the most critical factor
2. **Fast execution** — network latency must be low
3. **Iron discipline** — strictly execute 1% stop-loss
4. **Reasonable expectations** — earn a little each time; accumulate through repetition

If you can do all four, Cluc4 may become your **steady profit tool**. But remember:

**Past performance doesn't guarantee future returns; decide based on your own risk tolerance.**

**Survival matters more than making money. Stop-loss is the last line of defense!**
