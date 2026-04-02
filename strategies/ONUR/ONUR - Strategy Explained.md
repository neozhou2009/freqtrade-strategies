# ONUR: The "Lazy Strategy" That Waits for Wind + Chill Holding

> **Nickname**: Fisherman Waiting for Wind  
> **Profession**: As long as price is above middle band, I hold  
> **Timeframe**: 15 minutes (Medium-short term player)

---

## 1. What's This Thing?

Simply put, ONUR is:
- A simple strategy that **buys when price is above middle band**
- A chill player that **needs 13% to run**
- A conservative who **allows 10% loss to exit**
- A carefree soul that **allows 29% profit retracement before selling**

Like going fishing 🎣, you cast the bait, then just wait. Fish comes, you catch it; fish doesn't come, you keep waiting. ONUR is the same — after buying, just wait, either wait for 13% profit, or wait for 10% stoploss — the process in between? Sorry, I don't care 😎

---

## 2. Core Config: Basically "Either Win Big or Lose Small"

### Profit-Taking Rules (ROI Table)

```
Hold < 109min (~7 hours) → Must make 13.1% to run 🤑
Hold 109-226min (7-15 hours) → Run at 8% 📈
Hold > 226min (>15 hours) → Run at 3% 💨
```

**Translation**:
This strategy's core philosophy is "want to earn, earn big". What's the concept of 13.1% immediate take-profit threshold? After you buy, price must rise 13% to run. On 15-minute K-line, this requires considerable upward movement to trigger.

This design's intent is obvious:
- **Early (<7 hours)**: Needs significant rise to take-profit, shows author expects big trends
- **Mid (7-15 hours)**: Slightly lower expectations, but still requires 8%
- **Late (>15 hours)**: Drops to 3%, gives more time for profits to run

### Stoploss Rules

```
Loss 10% → Admit defeat and leave 🏳️
Profit retracement 29% → Lock profits immediately 🪤
```

**Translation**:
10% stoploss is relatively loose in crypto market, gives price sufficient fluctuation space. But trailing stop is exaggerated — allows 29% profit retracement before leaving! What kind of big trend can withstand this...

> "My goal is to catch a big swing, fluctuations in between are all clouds!"

---

## 3. 1 Entry Condition: Scarily Simple

This strategy has only **1 entry condition**, so simple it's touching:

### 🎯 Core Logic: Price > Bollinger Band Middle Band

**Code Logic**:
```python
# RSI less than 74 (basically no restriction)
# AND Close price > Bollinger Band middle band
→ BUY!
```

**Plain English**:
> "Report boss! Price is above middle band! And RSI hasn't risen to sky yet (<74), can buy!"

Wait, what's up with RSI < 74? Isn't normal overbought above 70? You set 74, isn't that saying nothing? This condition is basically decoration 😅

What really works is actually **price > Bollinger Band middle band**. Middle band is 20-day simple moving average, price above it means now in "strong state" — like students scoring above average on exam, not first place, but at least not failing!

---

## 4. Protection: 1 Layer of "Running Naked"

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| RSI Filtering | RSI < 74, almost ineffective | "Just for show" |

This strategy basically has no substantial protection mechanisms. RSI < 74 condition:
- 74 is too high, normal overbought area is 70+
- Almost never triggers any filtering effect
- Basically decoration

---

## 5. Exit Logic: Even More Chill Than Entry

### 5.1 Hierarchical Take-Profit: Run Based on Profit

| Holding Time | Take-Profit Point | Strategy Psychology |
|-------------|------------------|---------------------|
| < 7 hours | 13.1% | Leave only on big money! |
| 7-15 hours | 8% | Slightly lower expectations |
| > 15 hours | 3% | Final ultimatum, must leave |

**Plain English**:
This take-profit setting is too aggressive! 13.1% on 15-minute K-line means needs super big market to trigger. Normal coins fluctuate 5-10% a day is good, need continuous 13% rise requires very strong trend.

### 5.2 Trailing Stop

| Condition | Effect |
|-----------|--------|
| Profit < 36.2% | Don't activate trailing stop |
| Profit > 36.2% | Activate tracking, allow 29% retracement |

**Plain English**:
> "Want me to leave? Unless I make over 36%, then drop all back!"

This design is typical "let profits run" — as long as trend is strong enough, keep holding. 29% retracement space means strategy is prepared for "roller coaster ride".

### 5.3 Special Scenario Exits

| Scenario | Trigger Condition | Plain English |
|----------|------------------|---------------|
| Stoploss | Loss 10% | Admit defeat, no struggle |
| Trailing Stop | Profit retracement 29% | "Where's my profit???" |

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Scarily simple**: Just two conditions, kindergarten kids understand
2. **Medium-term thinking**: Not intraday, holds longer
3. **Loose stoploss**: 10% space given enough
4. **Aggressive trailing**: Profits can run far
5. **Exchange stoploss**: Fast response, can escape even in extreme market

### ⚠️ Cons (Roast Section)

1. **RSI condition is useless**: 74 same as nothing
2. **Take-profit too hard to trigger**: 13.1% too high
3. **No active exit**: Completely passive
4. **Many false signals**: Conditions too loose, buys everything
5. **Doesn't time market**: Doesn't care what trend, just buy

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Strong uptrend | ✅ Usable | Price continuously above MA |
| Downward rebound | ⚠️ Caution | Counter-trend may fail |
| Ranging market | ❌ Don't use | Middle band crossing, frequent trading |
| Sideways consolidation | ❌ Don't use | Can't reach take-profit |

---

## 8. Summary: How's This Strategy Really?

### One-Sentence Review
> "A strategy that looks simple, but scary when you think about it. Entry conditions so simple they have no real meaning, take-profit settings so high they almost never trigger."

### Who Should Use It?
- ✅ **Medium-term investors**: Willing to hold for a while
- ✅ **Trend traders**: Want to catch big trends
- ✅ **Lazy players**: Don't want frequent operations
- ✅ **High risk tolerators**: Can accept 10% stoploss

### Who Should NOT Use It?
- ❌ **Pursue stability**: Take-profit too hard to trigger
- ❌ **Frequent traders**: Doesn't match strategy rhythm
- ❌ **Loss-averse**: 10% stoploss still hurts

### My Suggestions
1. **Lower take-profit threshold**: 13.1% too high, 3-5% more reasonable
2. **Tighten stoploss**: 10% can drop to 5-7%
3. **Add filtering conditions**: RSI set like this equals not set
4. **Coordinate with trend filtering**: At least look at big trend direction

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Buy on Strong Pullback

ONUR's core philosophy:
- **Price > Middle Band** = Strong state
- **RSI < 74** = Hasn't risen to end yet (this condition basically decoration)
- **Take-Profit/Stoploss** = Responsible for exit decisions

Its profit logic is:
> "I don't care what trend you are, as long as above middle band I buy. After buying just wait, either make big money and run, or lose 10% and admit defeat."

This is typical **trend pullback strategy + hold-on strategy** combination.

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Uptrend | ⭐⭐⭐⭐ | Continuously above middle band, can make big wave |
| 📉 Downtrend | ⭐⭐ | Counter-trend buying = catching falling knives |
| 🔄 Ranging market | ⭐⭐⭐ | Middle band crossing, will have signals but effect average |
| ⚡ High volatility | ⭐⭐⭐⭐ | Big volatility easy to trigger take-profit |

**One-Sentence Summary**:
> "This strategy is a 'waiting for wind' chill player. Might make fortune in bull market, lose like dog in bear market."

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration Item | Suggested Value | Roast |
|-------------------|-----------------|-------|
| Number of pairs | 10-20 | Diversify risk |
| Only mainstream coins | Must | Altcoin volatility too big |
| Exclude strong pump coins | Suggested | Easy to get cut |

### 10.2 Key Config File Settings

```json
{
    "timeframe": "15m",
    "stoploss": -0.10,
    "minimal_roi": {
        "0": 0.131,
        "109": 0.08,
        "226": 0.03
    },
    "trailing_stop": true,
    "trailing_stop_positive": 0.293,
    "trailing_stop_positive_offset": 0.362,
    "order_types": {
        "stoploss_on_exchange": true
    }
}
```

### 10.3 Hardware Requirements (Important!)

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-20 | 1GB | 2GB | Smooth |
| 20-50 | 2GB | 4GB | Might lag |

**Warning**: 15-minute K-line data volume relatively large, if running many pairs, memory may be stressed.

### 10.4 Backtest vs Live Trading

**Main Differences**:
1. **Take-profit hard to trigger**: 13.1% may rarely trigger historically
2. **Stoploss may execute at worse price**: 10% stoploss may breach in extreme market
3. **RSI condition ineffective**: Historical backtest may produce too many signals

**Suggested Process**:
1. **Adjust ROI**: Suggest change to 3-5%, otherwise hard to trigger
2. **Paper trading test**: Run at least 1 month
3. **Manual intervention**: Manually close when necessary

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

After reading code, I think author might be:

1. **Wants to catch big trends**
   > "My goal is buy then hold until make big!"

2. **Casual about RSI condition**
   > "Just randomly set 74, don't really know why myself"

3. **Believer in trend trading**
   > "As long as trend exists, keep holding. Fluctuations are clouds!"

4. **May not realize exit conditions commented out**
   > "Crap, why are exit signals gone???"

---

## 12. Final Final Thoughts

### One-Sentence Review
> "A 'chill to the extreme' strategy. Simple entry, exit by waiting. Whether makes money depends entirely on market giving face."

### Who Should Use It?
- ✅ Medium-term investors wanting to catch big trends
- ✅ Lazy people not wanting frequent operations
- ✅ Can accept 10% stoploss
- ✅ Willing to wait

### Who Should NOT Use It?
- ❌ Pursue stable returns
- ❌ Like frequent trading
- ❌ Impatient
- ❌ Want to make quick money

### Manual Trader Suggestions

If you want to manually reference this strategy:
- **First look at big trend**: Can only use when daily level trend upward
- **Wait for pullback then buy**: Don't chase highs, wait for price to return near middle band
- **Set more reasonable take-profit**: 5% around enough, don't be greedy
- **Set stoploss well**: 7-8% more appropriate

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtest Looks Great, Live Trading Needs Caution

ONUR's backtest data may be deceptive:
- 13.1% take-profit may rarely trigger historically
- RSI < 74 condition has almost no filtering effect
- Backtest may show "long-term holding makes big money", but live trading may frequently stoploss

Simply put:
> "Those get-rich-quick cases seen in backtest, likely survivorship bias."

### Hidden Risks of Simple Strategies

In live trading, you'll discover:
- **Take-profit very hard to trigger**: 13.1% too hard, often ends up loss
- **Stoploss too easy to trigger**: 10% looks loose, but actually 10% daily fluctuation common in crypto
- **Too many false signals**: Conditions too loose, buys everything
- **No exit point**: Can only rely on passive take-profit/stoploss

### My Suggestions (Real Talk)

```
1. Must adjust ROI: Change 13.1% to 3-5%
2. Reduce pair count: 5-10 enough
3. Add filtering conditions: At least check if RSI in reasonable range
4. Manual intervention: Don't fully rely on auto exit
5. Prepare mentally: Most trades may be stoploss
```

**Remember**:
> "This strategy's biggest problem isn't too simple, but too 'chill' — chill to the point of completely handing fate to market."

---

**Final Reminder**: No matter how good the strategy, the market won't say hello when teaching you lessons. Light position test, staying alive is most important! 🙏

**Friendly Tip**: This strategy most needs optimization is ROI setting, change 13.1% to 3-5%, otherwise you may wait long time without triggering take-profit once. Also suggest adding more reasonable entry conditions like RSI < 30 or price returning near MA.

Wish everyone successful trading, get rich! 🚀💰
