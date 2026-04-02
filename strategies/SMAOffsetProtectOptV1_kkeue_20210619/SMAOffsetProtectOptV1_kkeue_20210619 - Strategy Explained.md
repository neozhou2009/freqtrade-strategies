# SMAOffsetProtectOptV1_kkeue_20210619 Strategy: The "Bargain Hunter" with Offset Moving Average

> **Nickname**: The Moving Average Offset Bargain King  
> **Job**: Price detective specializing in "cheap stuff"  
> **Timeframe**: 5-minute + 1-hour support

---

## 1. What is This Strategy?

Simply put, **SMAOffsetProtectOptV1_kkeue_20210619** is a strategy that:

- Buys specifically when prices are "on sale"
- Uses EWO indicator to distinguish between "real bargain" and "falling knife"
- Has trailing stop loss to help you lock in profits

Just like **going to the supermarket to buy discounted items** — you don't buy at full price, but wait for the yellow discount tag (price 2.7% below moving average) before considering. But you also need to check if the item is actually good (EWO indicator), avoiding expired garbage 🤣

---

## 2. Core Configuration: Basically "Strike While the Iron is Hot"

### Take-Profit Rules (ROI Table)

```
Just bought      → Run at 2.8% profit
Wait 10 minutes  → 1.8% is fine too
Wait 30 minutes  → 1% is acceptable
Wait 40 minutes  → 0.5%? Fine, let's go
```

**Translation**: This strategy doesn't like long-term holding, take profits and run. Like guerrilla warfare — strike and retreat, no dragging on.

### Stop Loss Rules

```
Fixed stop loss: -10% (throw in the towel at 10% loss)
Trailing stop: Activates at 1% profit, runs at 0.1% pullback
```

**Translation**:
- If you lose 10%, the system cuts your losses
- If you make more than 1%, the system starts "watching" for you — price pulls back slightly and it automatically sells, protecting your profits

---

## 3. Two Buy Conditions: I've Categorized Them for You

This strategy has **2 buy conditions**, connected by "OR" logic — satisfying either one triggers a buy. I've grouped them into 2 categories:

### 🎯 Category 1: Trend Pullback Buy (Condition #1)

**Core Logic**: In an uptrend, price pulls back below the moving average, time to grab a bargain.

**Plain English**:
> "This stock is going up, now it's pulled back a bit. The RSI isn't overheated yet, good buying opportunity!"

**Specific Conditions**:
```python
Close < SMA(16) × 0.973  # Price is 2.7% below moving average
EWO > 5.672              # In uptrend
RSI < 59                 # Not overbought
Volume > 0               # There's trading
```

**Classic Line**:
- Condition #1: `close < ma_buy × 0.973 AND ewo > 5.672 AND rsi < 59` → "It was rising well and suddenly got cheaper, still a good stock, buy!"

---

### 📉 Category 2: Panic Bottom-Fishing Buy (Condition #2)

**Core Logic**: Price has fallen hard, EWO is deeply negative, might be ready to bounce.

**Plain English**:
> "Everyone's scared and dumping, might be able to pick up some bargains from the panic!"

**Specific Conditions**:
```python
Close < SMA(16) × 0.973  # Price is 2.7% below moving average
EWO < -19.931            # Deep decline
Volume > 0               # There's trading
```

**Classic Line**:
- Condition #2: `close < ma_buy × 0.973 AND ewo < -19.931` → "Dropped so hard, the panic should be ending soon, let's try bottom fishing!"

---

## 4. Protection Mechanism: 3-Layer "Airbag"

This strategy installed triple insurance for itself:

| Protection Type | Parameter | Plain English |
|----------------|-----------|---------------|
| Fixed stop loss | -10% | "I give up at 10% loss, not playing anymore" |
| Trailing stop | Activates at 1% profit, sells at 0.1% pullback | "I'm watching your profits, slightest pullback and we bail" |
| Tiered ROI | Decreases target over time | "The longer it drags on, the lower my standards" |

The EWO indicator is also protection: it helps you distinguish between "real bargain" and "fake bargain."

**Roast**: This strategy has such strong self-protection awareness, afraid you'll lose money. But don't get too excited, more protection doesn't guarantee profits 🤣

---

## 5. Sell Logic: Take the Money and Run

### 5.1 Tiered Take-Profit: How Much to Run With

```
Time        Target Profit
────────────────────
Immediate   2.8%
10 minutes  1.8%
30 minutes  1.0%
40 minutes  0.5%
```

**Plain English**:
- Just bought: I want 2.8%!
- 10 minutes not reached: Fine, 1.8% works
- 30 minutes still not: 1% is okay too
- 40 minutes and still not: 0.5% let's go, at least don't lose

This design tells you: **Run fast! Don't get attached!**

---

### 5.2 Trailing Stop: Let Profits Fly a While

When your position profit reaches 1%:
- Trailing stop activates
- Price keeps rising, stop line rises with it
- Price pulls back 0.1%, immediately sell

**Plain English**:
> "Bro, you've made 1%. I'm watching for you. If price keeps rising, I'll raise the stop line. But if it drops 0.1%, I'll immediately sell for you, protecting what you've earned!"

---

### 5.3 Sell Signal: Price Returns Above Moving Average

```python
Close > SMA(20) × 1.010  # Price is 1% above moving average
```

**Plain English**:
> "Price has risen 1% above the moving average, might be time to take profits."

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Clear Logic**: Just two buy conditions, either pullback or oversold, simple and clear
2. **Strict Risk Control**: Fixed stop loss + trailing stop + tiered take-profit, triple protection
3. **Adjustable Parameters**: 5 buy parameters can all be optimized for different coins
4. **No Chasing Highs**: Condition #1 has RSI limit, prevents buying when overheated

### ⚠️ Cons (Roast Section)

1. **Gets Washed in Ranging Markets**: In sideways markets, price keeps crossing above and below the moving average, frequent buy/sell signals eat into profits through fees
2. **Bottom-Fishing Can Catch Falling Knives**: Condition #2 specializes in bottom fishing, but there's always another bottom below
3. **1-Hour Informative Layer Not Actually Used**: Configured but not used in logic, a bit wasteful
4. **Parameters Might be "Memorizing Answers"**: These default parameters might be optimized against historical data, may not work in the future

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Slow bull rise | ✅ Use it! | Many pullback buying opportunities, trailing stop can lock profits |
| 🔄 Sideways oscillation | ⚠️ Use cautiously | May trigger frequent stop losses, adjust parameters first |
| 📉 One-sided decline | ❌ Don't use | Bottom-fishing signals keep triggering, buying into more losses |
| ⚡ Severe volatility | ⚠️ Be careful | Trailing stop might be triggered by normal volatility |

---

## 8. Summary: How's This Strategy Really?

### One-Sentence Review
> "A clearly-thought-out trend pullback bottom-fishing strategy, suitable for patient traders who don't chase highs."

### Who Should Use It?
- ✅ People who like buying pullbacks
- ✅ People who don't want to chase highs
- ✅ People who like trailing stops to lock profits
- ✅ People willing to spend time optimizing parameters

### Who Shouldn't Use It?
- ❌ People who like chasing rises and selling falls
- ❌ People who want to profit in sideways markets
- ❌ People unwilling to backtest and verify
- ❌ People expecting to double immediately after buying

### My Suggestions
1. **Backtest first**: Check performance with historical data
2. **Then paper trade**: Run for a while without spending money
3. **Optimize parameters**: Different coins may need different parameters
4. **Small capital live trading**: Confirm effectiveness before increasing investment

---

## 9. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Using Offset to Find "Discount Opportunities"

SMAOffsetProtectOptV1_kkeue_20210619 is a mature version of the SMA Offset series. Its money-making philosophy:

**"Only buy when price is below moving average by a certain percentage, either as trend pullback or oversold bounce."**

- **Price Offset**: Must be 2.7% below moving average before considering entry
- **EWO Filter**: Distinguish between "pullback in uptrend" and "crash in downtrend"
- **Tiered Exit**: Longer holding, lower target

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:---------------------------|
| 📈 Slow bull trend | ⭐⭐⭐⭐⭐ | Price goes up and down, plenty of pullback opportunities, perfect fit |
| 📉 One-sided crash | ⭐☆☆☆☆ | Bottom-fishing catches falling knives, buying into more losses |
| 🔄 Sideways oscillation | ⭐⭐☆☆☆ | Frequent buying and selling, fees eat up profits |
| ⚡️ Severe volatility | ⭐⭐⭐☆☆ | Trailing stop can protect, but entry timing is hard to grasp |

**One-Sentence Summary**: **Trend is its best friend, oscillation is its enemy.**

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Comment |
|-------------|------------------|---------|
| Timeframe | 5-minute | Don't change to 1-minute, too many signals |
| Trading pair | Major coins/stablecoins | Don't play with those sketchy coins |
| Informative timeframe | 1-hour | Configured but not used, a bit awkward |

### 10.2 Key Config File Settings

```yaml
# Stop loss related
stoploss: -0.10
trailing_stop: true
trailing_stop_positive: 0.001
trailing_stop_positive_offset: 0.01

# ROI
minimal_roi:
  0: 0.028
  10: 0.018
  30: 0.010
  40: 0.005
```

### 10.3 Hardware Requirements (Important!)

This strategy doesn't have heavy computation, low hardware requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-5 pairs | 2GB | 4GB | Sufficient |
| 5-20 pairs | 4GB | 8GB | Smooth |
| 20+ pairs | 8GB | 16GB | Comfortable |

**Warning**: Although the strategy itself isn't complex, if you run many trading pairs simultaneously, you still need enough memory 😅

### 10.4 Backtesting vs Live Trading

**Backtesting may look great** because parameters are optimized.

**Live trading may not be as good** because:
- Slippage: Actual execution price may not be as ideal as backtesting
- Latency: Network delay may cause missing best prices
- Liquidity: Large capital may have execution difficulties

**Recommended Process**:
1. Backtest to verify strategy logic
2. Paper trade to test actual operation
3. Small capital live verification
4. Gradually increase capital

**Don't go all-in immediately**, even good strategies need fine-tuning!

---

## 11. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **EWO parameters 50/200**:
   > "The author didn't use the common 5/35, but 50/200 — this is an enlarged EWO, slower reaction but more stable signals."

2. **Two buy conditions, one has RSI, one doesn't**:
   > "When bottom-fishing, RSI isn't checked because RSI is definitely low when oversold, checking is pointless. But for trend pullbacks, RSI is checked to prevent chasing highs. Thoughtful!"

3. **Trailing stop's 'delayed activation' design**:
   > "Only starts trailing after 1% profit, this is to avoid being washed out by normal volatility right after buying. Smart!"

---

## 12. The Very Last

### One-Sentence Review
> "A clear-thinking pullback bottom-fishing strategy, suitable for patient traders. But remember, bottom-fishing has risks — there might be another bottom below."

### Who Should Use It?
- ✅ People who like buying on pullbacks
- ✅ People who can accept short holding periods (minutes to tens of minutes)
- ✅ People willing to spend time optimizing parameters
- ✅ People with risk control awareness

### Who Shouldn't Use It?
- ❌ People who like chasing rises and selling falls
- ❌ People who want stable profits in sideways markets
- ❌ People unwilling to backtest and verify
- ❌ People expecting to double immediately after buying

### Suggestions for Manual Traders
If you want to manually use this strategy's logic:
1. Draw a 16-period SMA line
2. Pay attention when price is 2.7% below SMA
3. Use EWO (50/200 EMA difference) to judge trend direction
4. Set 10% stop loss and trailing take-profit
5. Don't be greedy, take profits when you can

---

## 13. ⚠️ Risk Re-emphasis (Must Read!)

### Backtesting is Beautiful, Live Trading Needs Caution

SMAOffsetProtectOptV1_kkeue_20210619's historical backtesting performance may be **impressive** — but there's a trap:

> **Because parameters are optimized, the strategy easily 'fits' the optimal solution for past market conditions, but this doesn't guarantee future profits.**

Simply put: **The exam answers were given beforehand, of course you can score high. But what if the next exam questions change?**

### Hidden Risks of Complex Strategies

In live trading, you may encounter:
- **Slippage risk**: Actual execution price differs from theoretical, profits eaten away
- **Latency risk**: Network delay may cause missing best prices
- **Liquidity risk**: Small coins may not execute or may be hard to sell
- **Psychological pressure**: Hard to stay calm watching floating P&L

### My Advice (Straight Talk)

```
1. First backtest with historical data to understand the strategy's "exam performance" in the past
2. Then paper trade for a while to see "open-book exam" performance
3. Small capital live verification, feel the real market
4. Adjust parameters based on actual performance
5. Don't go all-in, always leave room
```

**Remember**: No matter how good the strategy is, the market won't give advance notice when teaching you a lesson. Light position testing, survival is most important! 🙏