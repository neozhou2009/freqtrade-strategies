# BigPete: The High-Return Hunter with "Smart Bodyguard"

> **Nickname**: Smart Bodyguard Strategy  
> **Profession**: Quant World's "Risk Control Master"  
> **Timeframe**: 5 minutes (entry) + 1 hour (confirmation)

---

## 1. What Is This Thing?

Simply put, **BigPete** is:
- An "upgraded version" based on BigZ04
- Core selling point: Adaptive trailing stop system
- 10% target return, much more aggressive than original

Like a hunter with a smart bodyguard, can chase big prey, but also has safety net 🎯

**One-Sentence Summary**: "Conservative aggressive investor" who wants high returns but fears big losses

---

## 2. Core Config: Simply "Boldly Chase, Carefully Retreat"

### Profit-Taking Rules (ROI Table)

```
Holding 0-30 min: Make 10% and run
Holding 30-60 min: Make 5% is also okay
Holding 60+ min: Make 2% makes do
```

**Translation**: Target is 10%, this is quite aggressive. But if you can't wait, 5% is also acceptable.

### Stoploss Rules (Core Innovation!)

```
Hard stoploss: -8% (maximum loss 8%)

Profit protection mechanism:
- Profit < 1.6%: Hard stoploss -8%
- Profit 1.6%-8%: Stoploss line moves from -8% up to -4%
- Profit > 8%: Stoploss line continues moving up, lock more profits
```

**Translation**: This is the "smart bodyguard" — the more you earn, the tighter the protection!

---

## 3. 13 Entry Conditions: In Line with BigZ04

BigPete inherited BigZ04's 13 entry conditions, I'll categorize them:

### 🎯 Category 1: RSI Oversold Type

**Core Logic**: RSI falling to extremely low means "cheap"

**In Plain English**:
> "5-minute RSI fell to 11? This is panic selling, buy the dip!"

**Representative Conditions**:
- **Condition 0**: RSI < 11.2 + Significant drop in recent 3 days + 1-hour RSI < 81.7

---

### 📉 Category 2: Lower Bollinger Band Type

**Core Logic**: Buy when price near lower Bollinger Band

**In Plain English**:
> "Price fell to lower Bollinger Band? Buy! Bearish close? Even more certain!"

**Representative Conditions**:
- **Condition 1**: Price < Lower Band × 0.999 + Bearish close + Volume contraction
- **Condition 2**: Price < Lower Band × 1.01 (looser condition)

---

### 🔄 Category 3: MACD Momentum Type

**Core Logic**: MACD golden cross + low price = enter

**In Plain English**:
> "MACD golden crossed? Price still at bottom? Let's go!"

**Representative Conditions**:
- **Condition 5**: MACD golden cross + Price at lower band + EMA200 trend up

---

### 💰 Category 4: Special Pattern Type

**Representative Conditions**:
- **Condition 11**: Consecutive 10 candles range < 1% → "Sideways consolidation, may break out anytime"
- **Condition 12**: False breakout pattern → "Broke below lower band then recovered, fake!"

---

## 4. Protection: Smart Trailing Stoploss (Core Feature)

This is BigPete's soul — **dynamically adjust stoploss line based on profit**:

### Stoploss Line Change Diagram

```
Profit:   -8%   0%    1.6%   4%    8%    12%   16%   20%
          |-----|-----|------|-----|-----|-----|-----|
Stoploss: -8%  -8%   -8%   -1.1% -4%   -8%  -12%  -16%
               ^           ^     ^              ^
               |           |     |              |
            Hard       Trailing  Level 1    Continue
            Stoploss   Activates             Following
```

**Plain English Explanation**:

| Profit Range | Stoploss Line | What It Means |
|-------------|--------------|---------------|
| Losing | -8% | Maximum loss 8%, baseline |
| Earn 1.6%-8% | -1.1% to -4% | Made some profit, start protecting |
| Earn > 8% | Follows increase | The more you earn, the tighter the protection |

### Example

Suppose you bought, then price started rising:

- **Rose to 5% profit**: Stoploss line moves to "2% loss" position, if falls back sell, protect 2-3% profit
- **Rose to 10% profit**: Stoploss line moves to "6% profit" position, even if falls at least earn 6%
- **Continues to 15%**: Stoploss line follows to "11% profit" position

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

1. **Smart Stoploss**: Not "one-size-fits-all" like fixed stoploss, dynamically adjusts based on profit
2. **High Return Target**: 10% target much more aggressive than BigZ04's 2.8%
3. **Can Catch Big Moves**: Trailing stop lets you eat more gains
4. **Hard Stoploss Protection**: Maximum loss 8%, won't lose everything

### ⚠️ Cons (Roast Session)

1. **Target Too High**: 10% not achievable every time, may miss some opportunities
2. **Complex Parameters**: Trailing stop has multiple layers of parameters, needs experience to adjust
3. **Volatility Sensitive**: Trailing stop may be triggered by normal fluctuations, exit early
4. **Needs Patience**: High targets mean may need to wait longer

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Bull Market | ✅ Key Use | Enough volatility to reach 10% target |
| Large Rebound | ✅ Very Suitable | Trailing stop can eat more gains |
| Range Market | ⚠️ Caution | 10% target may often not be reached |
| Low Volatility Period | ❌ Don't Use | Not enough volatility, strategy basically dormant |

---

## 8. Bottom Line: How Is This Strategy?

### One-Sentence Review
> "Middle-ground's gospel for those who want high returns but don't want to bear infinite risk"

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

BigPete's profit philosophy: **Don't ask to win every time, but when winning make it big enough**.

Trailing stop design lets you eat more gains when catching big moves, instead of selling after 3-5% rise.

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Bull Market Big Rebound | ⭐⭐⭐⭐⭐ | Best environment, trailing stop can eat full |
| 🔄 Wide Range Oscillation | ⭐⭐⭐⭐☆ | Enough volatility, opportunity to reach 10% |
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
   - Continue following: Eat full move

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
If you trade manually, can borrow BigPete's stoploss thinking:
- Set a hard stoploss (like 8%)
- Gradually move stoploss line up after making money
- The more you earn, the tighter the stoploss
- This way can eat big moves, but won't lose too much

---

## 13. ⚠️ Final Risk Reminder (Must Read This Section)

### 10% Target Not Every Time

BigPete's 10% first target looks very tempting, but:

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
