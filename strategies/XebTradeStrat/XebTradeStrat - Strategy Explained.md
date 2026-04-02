# XebTradeStrat: Simple to Outrageous "Chill" Trader

> **Nickname**: Chill Little Prince  
> **Profession**: Lazy person who only buys never sells (not really)  
> **Timeframe**: 1 minute (So fast eyes don't have time to blink)

---

## 1. What's This Thing?

Simply put, XebTradeStrat is:
- A super simple strategy that **places orders looking at just one moving average**
- A hands-off boss who **doesn't care when to sell at all**
- An impatient player doing short-term on **1-minute K-line**

Like seeing someone run a red light on the street — not because they have bad manners, but because they don't care about traffic lights, only care if there are cars. XebTradeStrat similar, it only cares about "short-term MA shoots up from below" signal, doesn't care about the rest 😂

---

## 2. Core Config: Basically "Take What You Got"

### Profit-Taking Rules (ROI Table)

```
Hold < 2min → Run at 0.2% profit 🤏
Hold 2-4min → Run at 0.5% profit 🏃
Hold > 4min → Must run at 1% profit 🤑
```

**Translation**:
This strategy's core philosophy is "take what you got". No matter how long you hold, just run when made enough. Satisfied with 0.2% in under 2 minutes, only requires 1% after 4 minutes. This isn't "greedy snake swallows elephant", but "mosquito leg is also meat" — main thing is accumulate little into many!

### Stoploss Rules

```
Loss 1% → Admit defeat and leave 🏳️
Profit retracement 0.05% → Lock profits immediately 🪤
```

**Translation**:
Cut at 1% loss, run faster than rabbit. When making money even more exaggerated, as long as profit retraces 0.05% (that's 0.0005), no questions asked directly close position. This is too conservative! Sometimes one K-line fluctuation more than 0.05% 😅

---

## 3. 1 Entry Condition: I've Categorized It for You

This strategy has only **1 entry condition**, simple to outrageous:

### 🎯 Core Logic: EMA Golden Cross

**Code Logic**:
```python
# 5-day MA > 10-day MA (bullish alignment)
# AND Yesterday 5-day MA < 10-day MA (just golden crossed today)
# AND Has volume (not air coin)
→ BUY!
```

**Plain English**:
> "Report boss! 5-day MA just shot up from below and crossed 10-day MA, and today has actual volume, no whale cutting leeks! BUY!"

This is classic **golden cross** — moving average world's "confession successful". Short-term MA breaks through long-term MA from below, typically interpreted as "about to rise" signal.

---

## 4. Protection: 0 Layers "Running Naked"

This strategy's protection mechanism is: **completely no protection** 😱

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| None | Doesn't exist | Just this confident (or stubborn) |

No:
- ❌ RSI overbought/oversold protection
- ❌ Bollinger Band ranging filtering
- ❌ BTC rise/fall protection
- ❌ Volume anomaly filtering (except > 0)

This means:
> "I don't care if market overheated, don't care if at mountain top, I just, golden cross, BUY!"

Courage admirable, but wallet may not withstand 😂

---

## 5. Exit Logic: Even More Chill Than Entry

### 5.1 Hierarchical Take-Profit: Run Based on Profit

| Holding Time | Take-Profit Point | Strategy Psychology |
|-------------|------------------|---------------------|
| < 2 minutes | 0.2% | Run fast, cash is king |
| 2-4 minutes | 0.5% | Slightly greedy |
| > 4 minutes | 1% | This is my final bottom line |

**Plain English**:
Run at 0.2% profit in under 2 minutes — this is too urgent? Sometimes fees more than 0.2%! This is typical "better miss than wrong" mentality.

### 5.2 Special Scenario Exits

| Scenario | Trigger Condition | Plain English |
|----------|------------------|---------------|
| Stoploss | Loss 1% | Admit defeat, no struggle |
| Trailing Stop | Profit retracement 0.05% | "My money is mine, not one cent less!" |

**Translation**:
This strategy's trailing stop set too conservative. What's 0.05% concept? That's rise 1% then immediately run, slightest pullback gets kicked off car. This design in ranging markets gets slapped repeatedly — buy then rise, rise then fall, fall little then stoploss, then watch price rise again... mentality will collapse 😅

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simple to no friends**: Code just few lines, beginners can understand
2. **Runs without effort**: Extremely low computer config requirements, garbage VPS can run
3. **Super fast backtest**: Others run one day backtest, it finishes in 5 minutes
4. **Won't overfit**: Parameters so few, hard to overfit even if wanted
5. **Great for practice**: Perfect material for beginners learning Freqtrade

### ⚠️ Cons (Roast Section)

1. **No exit signals**: Completely doesn't care when to sell, chill holding
2. **Signals too frequent**: 1-minute K-line, too many fake golden crosses
3. **Too conservative**: 0.05% trailing stop, simply is "run as soon as rises" itself
4. **Doesn't care trend**: Same set in bull bear markets, easy counter-trend trading
5. **Low capital utilization**: Buy then run, too many trades, fees hurt

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Strong uptrend | ✅ Usable | Most golden crosses effective |
| Downtrend | ❌ Don't use | Counter-trend catching falling knives |
| Ranging market | ❌ Don't use | Repeatedly slapped |
| High volatility coins | ⚠️ Caution | Too many signals, can't react in time |

---

## 8. Summary: How's This Strategy Really?

### One-Sentence Review
> "Simple is simple, but simple a bit too much — like a first-grade trader, no basic knowledge yet out wandering the jianghu."

### Who Should Use It?
- ✅ **Beginners learning**: Want to understand strategy structure? Come see this
- ✅ **Quick idea validation**: Use it to test new technical indicators
- ✅ **Light quant players**: Don't want spend too much time managing strategies
- ✅ **Run paper trading**: Low cost test trading ideas

### Who Should NOT Use It?
- ❌ **Pursue stable returns**: Signals too casual, easy to step in pits
- ❌ **No time to watch screen**: Needs manual intervention
- ❌ **Loss-averse**: Will get consecutive stoploss in ranging markets
- ❌ **Want to make big money**: Take-profit settings too conservative

### My Suggestions
1. **Don't go live directly**: Run paper trading for a month first
2. **Consider longer periods**: 5-minute or 15-minute more stable than 1-minute
3. **Manually add filtering**: At least check big trend direction
4. **Adjust take-profit/stoploss**: 1% take-profit too little, at least 2-3%

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Passive Chase Rise Kill Fall

XebTradeStrat's profit logic simple to explosion: **Buy when see golden cross, when see death cross... sorry it doesn't have death cross**. It's like a robot that only knows "buy buy buy", completely doesn't care what market saying.

Its core philosophy:
- **No prediction**: Doesn't guess future rise or fall
- **Only following**: Get on car after trend confirmed
- **Run fast**: Make little then run, not greedy

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Uptrend | ⭐⭐⭐⭐ | Most golden crosses real, can make small money |
| 📉 Downtrend | ⭐⭐ | Counter-trend buying = giving heads |
| 🔄 Ranging market | ⭐⭐ | Buy then range, range then stoploss |
| ⚡ High volatility | ⭐ | 1-minute K-line volatility too big, all signals fake |

**One-Sentence Summary**:
> "This strategy is like a reckless youth, only knows charging forward. Drinks some soup in bull market, counts money for others in bear market."

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration Item | Suggested Value | Roast |
|-------------------|-----------------|-------|
| Number of pairs | 3-5 | Don't run too many, can't take care |
| Only mainstream coins | Must | Altcoin volatility too big, 1-minute can't handle |
| Exclude BTC | Suggested | BTC volatility too weird, this strategy can't grasp |

### 10.2 Key Config File Settings

```json
{
    "timeframe": "1m",
    "stoploss": -0.01,
    "minimal_roi": {
        "0": 0.01,
        "2": 0.005,
        "4": 0.002
    },
    "trailing_stop": true,
    "trailing_stop_positive": 0.0005
}
```

### 10.3 Hardware Requirements (Important!)

This strategy computation extremely small, almost no hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 | 256MB | 512MB | Enjoy silk smooth |
| 10-50 | 512MB | 1GB | Might slightly lag |
| 50+ | 1GB | 2GB | Suggest reducing quantity |

**Warning**: 1-minute K-line itself has large data volume, even strategy simple, if running 100+ pairs, API requests very frequent, may trigger exchange rate limits 😅

### 10.4 Backtest vs Live Trading

**Main Differences**:
1. **Slippage**: 1-minute high-frequency trading extremely sensitive to slippage, live execution price often worse than backtest
2. **Liquidity**: Large orders may not buy enough quantity
3. **API Rate Limits**: High-frequency requests may get banned by exchange

**Suggested Process**:
1. **Backtest**: Run 3 months data first to see
2. **Paper trading**: Simulate for 1 month
3. **Small live position**: Test with 5%-10% capital
4. **Gradually add position**: Amplify after confirming effective

**Don't go all-in immediately**, even good strategies need breaking in! Especially this kind of simple strategy, often backtest beautiful as painting, live trading rotten as slag.

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

After reading code, I think author might be:

1. **A minimalist enthusiast**
   > "Why have 40 entry conditions? 1 is enough!"

2. **Possibly poisoned by "frequent trading"**
   > "What's up with 0.05% trailing stop? Too scared to die!"

3. **Possibly writing a "strategy skeleton"**
   > "This is my teaching case for beginners, everyone can modify freely"

4. **Absolutely didn't expect anyone to use it live directly**
   > "I just wrote casually, why you taking it seriously?"

---

## 12. Final Final Thoughts

### One-Sentence Review
> "It's the 'blank paper' of Freqtrade strategies — simplest start, also most honest mirror. Reflects whether you willing spend time learning, willing admit strategy limitations."

### Who Should Use It?
- ✅ Beginners wanting to learn strategy structure
- ✅ Developers wanting to quickly validate ideas
- ✅ People running low-cost paper trading
- ✅ Those using it as "skeleton" then adding functions themselves

### Who Should NOT Use It?
- ❌ Pursue stable compound returns
- ❌ Want "passive income"
- ❌ No time to monitor
- ❌ Think simple = easy money

### Manual Trader Suggestions

If you want to manually reference this strategy:
- **First look at big trend**: At least check 4-hour or daily chart
- **Only use in bull market**: Don't touch in downtrend
- **Set wider stoploss**: 1% too tight, at least 2-3%
- **Manual take-profit**: Don't let machine help you run, returns will be much less

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtest Looks Great, Live Trading Needs Caution

XebTradeStrat's backtest data often looks "okay" — but there's a trap:
- 1-minute K-line historical data may have many "future functions"
- Backtest doesn't consider slippage and fees
- Strategy completely fails in extreme market conditions

Simply put:
> "Backtesting 100x gains means nothing, not losing money in live trading is real skill."

### Hidden Risks of Simple Strategies

In live trading, you'll discover:
- **Too many false signals**: Golden cross fake, buy then fall
- **Stoploss too frequent**: 1% stoploss not enough for fluctuations
- **Fees too high**: Buy buy sell sell all have fees, hundreds gone
- **Mentality collapses**: Consecutive 10 stoploss, you'll doubt life

### My Suggestions (Real Talk)

```
1. Don't use as main strategy, use as practice tool
2. Must paper trade at least 1 month before live
3. Control capital within range can afford loss
4. Prepare for manual intervention anytime
5. Remember: Simple doesn't equal easy money
```

**Remember**:
> "Market specializes in treating various unconvinced. The simpler the strategy, the more complex psychological preparation needed."

---

**Final Reminder**: No matter how good the strategy, the market won't say hello when teaching you lessons. Light position test, staying alive is most important! 🙏

**Friendly Tip**: If really want to use this strategy, suggest at least change timeframe to 5-minute or 15-minute, 1-minute really too small, too much noise. And, widen trailing stop to 1-2%, otherwise you'll be annoyed to death by repeated stoploss.

Wish everyone successful trading, get rich! 🚀💰
