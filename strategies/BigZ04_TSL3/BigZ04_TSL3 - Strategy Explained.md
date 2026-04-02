# BigZ04_TSL3: The High-Return Hunter with "Smart Tail"

> **Nickname**: Smart Tail Strategy  
> **Profession**: Quant World's "High Return + Strong Protection" Expert  
> **Timeframe**: 5 minutes (entry) + 1 hour (confirmation)

---

## 1. What Is This Thing?

Simply put, **BigZ04_TSL3** is:
- BigZ04 + adaptive trailing stop
- Target return skyrockets from 2.8% to 10%
- Multi-layer protection mechanism, the more profit the tighter the protection

Like a hunter with a smart tail, can chase big prey, but also has safety net 🎯

**One-Sentence Summary**: "Rational party" who wants high returns but doesn't want to bear infinite risk

---

## 2. Core Config: Simply "Boldly Chase, Carefully Retreat"

### Profit-Taking Rules (ROI Table)

```
Holding 0-30 min: Make 10% and run
Holding 30-60 min: Make 5% is also okay
Holding 60+ min: Make 2% makes do
```

**Translation**: Target is 10%, this is much more aggressive than BigZ04's 2.8%.

### Stoploss Rules (Core Innovation!)

```
Hard stoploss: -8% (maximum loss 8%)

Multi-level trailing stop:
- Profit < 1.6%: Hard stoploss -8%
- Profit 1.6%-8%: Stoploss line moves from -8% up to -1.1%
- Profit 8%-10%: Stoploss line moves from -1.1% up to -4%
- Profit > 10%: Stoploss line continues following upward
```

**Translation**: This is the "smart tail" — the more you earn, the tighter the tail!

---

## 3. 13 Entry Conditions: Same as BigZ04

BigZ04_TSL3 completely inherited BigZ04's 13 entry conditions:

### Core Condition: Condition 10 (1-hour Oversold + MACD Reversal)

This is the most important entry source:

```python
Condition 10:
- 1-hour RSI < 35
- 1-hour price < lower Bollinger Band
- MACD just golden crossed
- 5-minute RSI < 40.5
- MACD histogram strong enough
- Bullish confirmation
```

**In Plain English**:
> "Big cycle oversold + momentum reversal + small cycle cooperation = big-level rebound opportunity!"

### Other Conditions

Conditions 0-9 and conditions 11-12 exactly same as BigZ04, won't elaborate.

---

## 4. Protection: Adaptive Trailing Stop (Soul)

This is TSL3 version's core innovation — **dynamically adjust stoploss line based on profit**:

### Stoploss Line Change Diagram

```
Profit:   -8%   0%    1.6%   4%    8%    10%   14%   18%
          |-----|-----|------|-----|-----|-----|-----|
Stoploss: -8%  -8%   -8%   -1.1% -4%   -6%   -10%  -14%
               ^           ^     ^     ^
               |           |     |     |
            Hard       Trailing  Level 1  Continue
            Stoploss   Activates          Following
```

### Plain English Explanation

| Profit Range | Stoploss Line | What It Means |
|-------------|--------------|---------------|
| Losing | -8% | Maximum loss 8%, baseline |
| Earn 0-1.6% | -8% | Haven't made money yet, use hard stoploss |
| Earn 1.6%-8% | -1.1% to -4% | Made some profit, start protecting |
| Earn 8%-10% | -4% to -6% | Good returns, strengthen protection |
| Earn > 10% | Continues following | The more you earn, the tighter the protection |

### Example

Suppose you bought, then price started rising:

1. **Rose to 3% profit**: Stoploss line moves to around "2% loss"
   - If falls back, protect around 1% profit
   
2. **Rose to 8% profit**: Stoploss line moves to "4% profit"
   - Even if falls, at least earn 4%
   
3. **Rose to 12% profit**: Stoploss line moves to "8% profit"
   - Continue falling? Protect 8% profit

**Core Idea**: The more you earn, the more you need to protect the fruits of victory!

---

## 5. Exit Logic: ROI + Trailing Stop Double Insurance

### 5.1 ROI Take-Profit

10% first target is ideal state, if market is strong, directly reach target and sell.

### 5.2 Trailing Stop Baseline

If market isn't that strong, didn't reach 10%, trailing stop will protect existing profits.

**In Plain English**:
> "Best to make 10%, if can't make it back, trailing stop gives you baseline."

---

## 6. This Strategy's "Personality"

### ✅ Pros (Praise Session)

1. **Smart Trailing Stop**: Dynamically adjusts based on profit, not "one-size-fits-all"
2. **High Return Target**: 10% target much more aggressive than BigZ04's 2.8%
3. **Can Catch Big Moves**: Trailing stop lets you eat more gains
4. **Hard Stoploss Protection**: Maximum loss 8%, won't lose everything
5. **Inherited Condition 10**: Big cycle reversal signal quality high

### ⚠️ Cons (Roast Session)

1. **Target Too High**: 10% not achievable every time
2. **May Sell Too Early**: Trailing stop may exit early
3. **Higher Signal Requirements**: Only capturing big rebounds can reach target
4. **Less Friendly to Small Capital**: Need larger capital tolerance

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Rebound After Big Drop | ✅ Best | Condition 10 + trailing stop = perfect combination |
| Big Volatility Market | ✅ Suitable | Enough volatility to reach 10% |
| Range Market | ⚠️ Caution | 10% target may often not be reached |
| Low Volatility Period | ❌ Don't Use | Not enough volatility, strategy dormant |

---

## 8. Bottom Line: How Is This Strategy?

### One-Sentence Review
> "Rational party's gospel for wanting high returns but not wanting to bear infinite risk"

### Who Should Use It?
- ✅ Pursuing higher returns
- ✅ Can accept certain volatility
- ✅ Have patience to wait for market
- ✅ Understand trailing stop logic

### Who Should NOT Use It?
- ❌ Pursuing stable small returns
- ❌ Can't accept 8% maximum loss
- ❌ Running in low volatility market
- ❌ Complete newcomers

### My Recommendations
1. **Understand trailing stop first**: This is strategy's soul, don't use if you don't understand
2. **Suitable for big volatility markets**: Need enough volatility to reach 10%
3. **Set good position management**: Don't exceed 30% of total capital per trade
4. **Have psychological expectations**: 10% not every time, missing is normal

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Use Trailing Stop to Eat Big Moves

BigZ04_TSL3's profit philosophy: **Don't ask to win every time, but when winning make it big enough**.

Trailing stop design lets you eat more gains when catching big moves, instead of selling after 3-5% rise.

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Rebound After Big Drop | ⭐⭐⭐⭐⭐ | Best environment, trailing stop can eat full |
| 🔄 Big Volatility Market | ⭐⭐⭐⭐☆ | Enough volatility, opportunity to reach 10% |
| 📉 Continuous Decline | ⭐⭐☆☆☆ | Occasional rebounds, but may not reach target |
| ⚡️ Low Volatility Sideways | ⭐☆☆☆☆ | Basically no opportunities, strategy dormant |

**One-Sentence Summary**: "Hunter" in big volatility markets, "spectator" in small volatility markets.

---

## 10. Want to Run This Strategy? Check These First

### 10.1 Pair Configuration

| Configuration Item | Recommended Value | Roast |
|-------------------|------------------|-------|
| Maximum Positions | 3 | Can't watch too many |
| Pair Type | Major coins | Small coins too volatile |
| Single Trade Capital | 20-30% of total | Don't go all-in |

### 10.2 Key Parameters

```python
# Trailing stop core parameters
pHSL = -0.08    # Hard stoploss 8%, maximum loss this much
pPF_1 = 0.016   # 1.6% profit triggers first-level trailing
pSL_1 = 0.011   # Corresponding stoploss 1.1%
pPF_2 = 0.080   # 8% profit triggers second-level
pSL_2 = 0.040   # Corresponding stoploss 4%
pPF_3 = 0.100   # 10% profit triggers third-level
pSL_3 = 0.060   # Corresponding stoploss 6%
```

### 10.3 Hardware Requirements

This strategy computation not large, ordinary VPS can run:

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|---------------|-------------------|
| 1-3 pairs | 2GB | 4GB |
| 4-5 pairs | 4GB | 8GB |

### 10.4 Backtest vs Live Trading

**Backtest Performance**: Usually better than live, because historical data "perfect"

**Live Reality**:
- Trailing stop may be falsely triggered by "normal fluctuations"
- 10% target not every time
- Need patience to wait

**Recommended Process**:
1. Simulated trading for 2-4 weeks
2. Understand trailing stop behavior
3. Small capital live test
4. Gradually increase position

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Looking carefully at code, you'll find:

1. **Hard Stoploss Set to 8% Not 10%**
   > "Better to lose less, don't gamble too big" — author's risk preference

2. **Trailing Stop Level Design Very Careful**
   - 1.6% activate: Protect after making some
   - 8% upgrade: Protect more when making big
   - 10% continue: Eat full move

3. **Inherited BigZ04's 13 Conditions**
   > "Enter well to sell well" — author deeply understands entry importance

---

## 12. Last But Not Least

### One-Sentence Review
> "Rational party's first choice for wanting high returns but fearing big losses"

### Who Should Use It?
- ✅ Traders with some experience
- ✅ Understand trailing stop logic
- ✅ Pursuing larger single-trade returns
- ✅ Can patiently wait for opportunities

### Who Should NOT Use It?
- ❌ Pursuing high-frequency trading
- ❌ Low volatility markets
- ❌ Complete newcomers
- ❌ Can't accept 8% maximum loss

### Manual Trader Recommendations
If you trade manually, can borrow BigZ04_TSL3's stoploss thinking:
- Set a hard stoploss (like 8%)
- Gradually move stoploss line up after making money
- The more you earn, the tighter the stoploss
- This way can eat big moves, but won't lose too much

---

## 13. ⚠️ Final Risk Reminder (Must Read This Section)

### 10% Target Not Every Time

BigZ04_TSL3's 10% first target looks very tempting, but:

> **Big moves don't happen every day, most of the time you can only rely on trailing stop to protect small profits.**

If you expect to make 10% every time, you'll be very disappointed.

### Trailing Stop's Double-Edged Sword

Trailing stop can protect profits, but may also:

1. **Be Triggered by Normal Fluctuations**: Normal pullbacks in trends may make you exit early
2. **Miss Bigger Moves**: Continues rising after you sell, mentality will collapse
3. **Needs Precise Parameters**: If parameters set wrong, may protect too loose or too tight

### Hard Stoploss 8% Is Real Loss

Don't think 8% isn't much:

- Lose 3 times consecutively, capital only 0.92³ ≈ 78%
- Need to rise 28% to break even

**This isn't a small amount!**

### My Recommendations (Real Talk)

```
1. 10% target is "ideal state", not "normal state"
2. Trailing stop is "baseline", not "perfect"
3. Set reasonable expectations: Average 3-5% per trade is good enough
4. Control position: Don't exceed 30% of total capital per trade
5. Record trades: Analyze which signals make money, which lose
```

**Remember**: No matter how smart the strategy, can't beat market's unpredictability. Light position test, staying alive is most important! 🙏

*This article is for entertainment and learning only, not investment advice. Investment involves risks, enter the market with caution.*
