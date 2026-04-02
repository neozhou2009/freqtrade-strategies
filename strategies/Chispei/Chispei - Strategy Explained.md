# Chispei Strategy: Moving Averages + Momentum, Old-School But Practical

> **Nickname**: MA Veteran / Momentum Catcher
> **Profession**: Medium-short-term trend hunter
> **Timeframe**: 4 Hours (4h)

---

## 1. What's This Strategy All About?

Simply put, **Chispei** is a strategy that:
- Uses **moving average crossovers** to judge trend direction
- Uses **momentum indicator** to find buy/sell points
- Specifically boards when **trend starts** and gets off before **trend ends**

Think of it like an **old-school trend hunter**, holding a telescope (MAs) to observe wind direction, spotting prey (trend) appears and decisively shoots (buys), sees prey running away and packs up (sells) 🔫

Its core logic is extremely simple:
> "Fallen too much (low momentum) + MA golden cross = buy buy buy"
> "Can't rise further (momentum down) + MA death cross = sell sell sell"

---

## 2. Core Settings: Basically "Let Profits Run, Cut Losses When Due"

### Take-Profit Rule (ROI Table)

This strategy's take-profit design is interesting — like a **greedy vendor**:

```
⏱️ Holding Time              💰 Take-Profit Line
────────────────────────────────────────────────
0-20 minutes               → 4% and leave
20-30 minutes              → 5% and leave
1-2 hours                  → 10% and run
After 2 days                → 7.9% also fine
After ~30 hours            → Wow 67.6%?! Must run!
After 3.5 days              → Whatever the profit, CLEAR IT!
```

**Translation**: This strategy is hasty early on (satisfied with 4-10%), but has a strange time window (~30 hours) setting 67.6% take-profit... Honestly, I don't know what the author was thinking; might be a backtesting "magic number" 🤷

### Stop-Loss Rule

```
Stop-loss: -32.336%
```

**Translation**: **Cut losses at 30% and admit defeat**! This stop-loss is really high; ordinary people can't handle it.

> "I give you 32% of drawdown room; play however you want, but beyond that, sorry, goodbye 👋"

---

## 3. Two Buy Conditions: I've Categorized Them for You

This strategy's buy conditions are extremely simple — **2 conditions must both be met**:

### 🎯 Category 1: Momentum Oversold (Confirms bottom found)

**Core Logic**: MOM (momentum indicator) below 15 means price has fallen for a while; rebound likely

**Plain English**:
> "Fallen too much; should rebound"

**Key Condition**:
- `dataframe['mom'] < 15` → Momentum indicator below 15; oversold zone

---

### 📈 Category 2: MA Golden Cross (Confirms trend turning up)

**Core Logic**: 13-day MA crosses above 25-day MA from below; "golden cross" forms; short-term strength exceeding long-term

**Plain English**:
> "MA golden cross; trend about to rise"

**Key Condition**:
- `dataframe['fastMA'] > dataframe['slowMA']` → 13-day MA > 25-day MA

---

### Combined Effect

This is like two veterans confirming with each other:
1. **Momentum says**: "Fallen enough; should rebound"
2. **MAs say**: "Trend about to rise; short-term strength exceeds long-term"

The two confer: **"Let's do it!"** 🏃‍♂️💨

---

## 4. Protection Mechanisms: None! Just Going Commando!

Believe it or not, **Chispei has NO additional entry protection mechanisms whatsoever**.

| Protection Type | Availability | Note |
|----------------|-------------|------|
| Volume filter | ❌ | None |
| RSI confirmation | ❌ | None |
| Bollinger Band filter | ❌ | None |
| Time filter | ❌ | None |

**Plain English**: This strategy is like a **naked warrior going into battle**, no protection whatsoever, just relies on two indicators to fight the world.

> "What's there to fear? Cut losses if lose, enjoy life if win!" 💪

**My critique**: Though simplicity is a virtue, it's a bit... brave 😅 Fortunately the strategy itself is simple enough that "over-protection" isn't a concern.

---

## 5. Sell Logic: More Elaborate Than Buy

### 5.1 Take-Profit Exit: Run When Time Comes

As discussed in section 2, the strategy automatically triggers different levels of take-profit based on holding time. Simply put:

- **Early**: Made 4-10% and want to run (conservative)
- **Middle**: Has a weird 67.6% high take-profit (don't know why)
- **Late**: 3.5 days forces liquidation (regardless of profit)

### 5.2 Signal Exit: MA Death Cross + Momentum Pullback

The strategy has **2 sell conditions** (must both be met):

| Condition | Indicator | Threshold | Plain English |
|----------|-----------|-----------|---------------|
| Condition #1 | MOM | < 80 | Momentum pulling back from highs; can't rise |
| Condition #2 | MAs | Death cross | 13-day MA falls below 25-day MA; trend turning bearish |

**Classic dialogue**:
> "Can't rise anymore (momentum down) + trend broken (MA death cross) = Run!"

---

## 6. Strategy "Personality"

### ✅ Strengths

1. **Simple and clear**: Only 3 indicators; even a kindergarten kid can understand 😂
2. **Strong trend capture**: High stop-loss allows profits to run; big gains when trends come
3. **Works both ways**: Can go long or short; works in both bull and bear markets
4. **No fuss**: No pile of protection conditions; trades when signals come

### ⚠️ Weaknesses

1. **Stop-loss too brave**: -32% stop-loss; can get chopped哭 in ranging markets
2. **Many false signals**: MA crossovers especially prone to fakeouts in no-trend conditions
3. **Serious lag**: By the time golden cross confirms, best entry is gone
4. **No protection**: Just relies on two indicators going commando; aren't you nervous? 🤔

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear uptrend | ✅ Highly recommended | MA golden cross hits bullseye;躺着赚钱 |
| 📉 Clear downtrend | ✅ Recommend (short) | Same logic reversed works for shorting |
| 🔄 Ranging market | ❌ Don't use | High stop-loss will lose你到哭 |
| 😴 Consolidation | ❌ Don't use | MA crossovers produce too many false signals |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> **"Old-school but practical trend strategy; simple and brutal; good in trending markets"**

### Who's It For?
- ✅ Old hands with strong psychological endurance who can handle 32% losses
- ✅ Investors who like medium-long-term trend-following
- ✅ Lazy people who don't want to study complex indicators and just want simple money
- ✅ Big capital bosses who aren't afraid of volatility

### Who's It NOT For?
- ❌ Conservative people who can't stomach seeing losses
- ❌ People who like high-frequency trading and daily operations
- ❌ Young people with small capital who can't afford losses
- ❌ Perfectionists who need perfect signals and must have protection conditions

### My Suggestions
1. **Backtest first**: Use 2+ years of data; see if you can handle it
2. **Paper trade first**: Run live with small capital for 3 months
3. **Set stop-loss**: Don't manually interfere; let the strategy execute the 32% stop-loss itself
4. **Read the market**: Only open positions in clear trends; firmly don't open in ranging markets

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Catch Big Trends with Simple Indicators

Chispei's money-making logic is extremely simple and brutal:
- **Trend starts** → MA golden cross → Buy!
- **Trend ends** → MA death cross → Sell!
- **Loss too big** → 32% stop-loss → Admit defeat!

It doesn't care about fundamentals, news, anything — just looks at **price and MAs**, like a **samurai with blinders on**, only watching opponent's movements (price changes), ignoring everything else 👀

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:---|:---|:---|
| 📈 Big surge | ⭐⭐⭐⭐⭐ | MA golden cross精准命中;躺着赚钱 |
| 📉 Big drop | ⭐⭐⭐⭐⭐ | Short selling also earns big with reversed logic |
| 🔄 Ranging | ⭐⭐ | MAs cross back and forth; get whipped both ways |
| ⚡ Wild swings | ⭐⭐⭐ | Volatility too high; stop-loss may get swept |

**Bottom Line**:
> **"This strategy is a 'trend follower'; earns big when trends come, loses big when trends absent."**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| Trading pairs | BTC/USDT, ETH/USDT | Good liquidity; stable trends |
| Timeframe | 4 hours | Don't change; strategy is designed for this |
| Wallet mode | Spot or futures both OK | Remember to short direction for futures |

### 10.2 Key Config Settings

```python
# Strategy parameters
timeframe = '4h'
stoploss = -0.32336

# Take-profit table
minimal_roi = {
    "5127": 0,
    "1836": 0.676,
    "2599": 0.079,
    "120": 0.10,
    "60": 0.10,
    "30": 0.05,
    "20": 0.05,
    "0": 0.04
}
```

### 10.3 Hardware Requirements

This strategy's computation is **extremely light**; computer requirements are very low:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|----------------|------------|
| 1-10 pairs | 1GB | 2GB | No pressure |
| 10-50 pairs | 2GB | 4GB | Easy and pleasant |
| 50+ pairs | 4GB | 8GB | Piece of cake |

**Conclusion**: Any old computer can run it; don't worry 🖥️

### 10.4 Backtesting vs Live Trading

| Difference | Impact | Suggestion |
|-----------|--------|------------|
| Slippage | Execution price worse | Relax both take-profit and stop-loss by 0.2% |
| False signals | More in live | Try adding volume filter |
| Liquidity | Large capital hard to fill instantly | Build positions in batches |

**Recommended Process**:
1. **Backtest first**: 3 years of data; at least 100 trades
2. **Paper trade**: Run paper for 1 month
3. **Live with small**: Use 10% capital first
4. **Gradually increase**: Add capital after stable profits

**Don't go all-in right away**, this strategy's stop-loss is so high it'll kill you! 😱

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Looking closely at the code, I found some interesting things:

1. **Ultra-long -32% stop-loss**
   > "I just don't believe trends can't recoup losses!"

2. **Mysterious 67.6% take-profit**
   > "The 1836-minute (~30 hour) time window... could it be the author's lucky number?"

3. **Code comments**
   > "There's a comment saying 'Maybe the success of a trading system is part of strategy and also a good config.json too!' — the author knows strategy and config are equally important!"

4. **Validation script**
   > "The file header says it's used to 'verify Freqtrade and TradingView backtesting results consistency,' so this is actually a **test strategy**?"

---

## 12. The Final Word

### One-Line Verdict
> **"Simple, brutal trend strategy; a boss when trends come, a loser when trends absent"**

### Who's It For?
- ✅ Experienced old hands with psychological strength
- ✅ Warriors who can handle 32% losses
- ✅ Investors who like medium-long-term trends
- ✅ Big capital bosses

### Who's It NOT For?
- ❌ Beginner newbies (will be scared by stop-loss)
- ❌ Conservative investors
- ❌ Poor people with small capital
- ❌ Traders who like daily operations

### Manual Trading Suggestions

This strategy is fully manual-tradable:
1. Check 4-hour candles before daily close
2. MOM < 15 + MA golden cross → Buy
3. MOM < 80 + MA death cross → Sell
4. Loss exceeds 32% → Blindly cut

**Simple right? Even a kindergarten kid can learn it 👶**

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtesting Looks Good; Live Requires Caution

Chispei's backtesting data may look **pretty good** — but!

> **This strategy's ROI table has a magical "67.6% take-profit" at 30 hours — clearly a backtesting overfitting result; 99% chance unachievable in live trading.**

Simply put: **Past performance doesn't guarantee future returns; don't assume past 67% gains will repeat!**

### Hidden Risks of High Stop-Loss

-32% stop-loss means:
- **3 consecutive losses = 70%+ loss**: 100K becomes 30K 💸
- **Huge psychological pressure**: Who can watch their account shrink and not panic?
- **Needs high win rate**: Must exceed 70% win rate just to break even

### My Suggestions (From the Heart)

```
1. Don't trust the 67.6%; that's just a beautiful misunderstanding
2. Try with 10K first; run 3 months before deciding
3. Firmly don't open positions in ranging markets; don't fight money
4. Strictly follow 32% stop-loss line; don't hold through losses manually!
5. If you lose 3 times consecutively, pause for a week to cool down
```

**Remember**:
> "Strategy is dead; market is alive. No matter how good the strategy, it dies without surviving 32% losses." 🪦

---

**Final Reminder**: This strategy is **simple and brutal**; earns big when used well, loses big when used poorly. **Test with small positions; survival matters most!** 🙏

---

*Strategy Tip*: If -32% stop-loss feels too brave, try changing to 20% yourself; though it'll reduce ability to catch big trends, can protect capital 😌
