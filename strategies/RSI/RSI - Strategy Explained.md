# RSI Strategy: The Oversold/Overbought Sniper

> **Nickname**: Bottom-Fisher Extraordinaire  
> **Occupation**: Oversold bounce specialist, greedy when others are fearful  
> **Timeframe**: 15 minutes + 30 minutes dual-timeframe warfare

---

## I. What is This Strategy?

Simply put, **RSI Strategy** is:
- Buy when RSI is oversold (< 30)
- Sell when RSI is overbought (> 70)
- Use Williams %R to double-confirm
- Has trailing stop to protect floating profits

Like an **oversold/overbought sniper**—when others panic, I'm greedy; when others get greedy, I panic 🎯

---

## II. Core Configuration: "Bottom-Fishing and Top-Escaping"

### Profit-taking Rules (ROI Table)

```
Immediately → 9% profit and run
```

**Translation**: Once you make 9%, get out immediately. Simple and brutal!

### Stop-loss Rule

```
Lose 10% then stop
Trailing stop: Activates after 1% profit, triggers on 2% pullback
```

**Translation**:
- Lose 10% and accept it, not too harsh
- After making 1%, if price pulls back 2%, lock in profits and run

**This has trailing stop**: Way better than Quickie's "hold to death" strategy—at least you can lock in floating profits!

---

## III. Buy Condition: Oversold + More Oversold = Action

This strategy has only one buy condition, but needs **dual confirmation**:

### 🎯 Buy Signal: Two Conditions Must Both Be Met

| Condition | Meaning | Plain English |
|-----------|---------|----------------|
| RSI < 30 | Entered oversold zone | Price dropped too hard, might bounce |
| Williams %R < -80 | Extremely oversold | Williams indicator also confirms "dropped too much" |

**Plain English Translation**:
> "RSI below 30 (oversold), Williams %R also below -80 (extremely oversold)—**this is the time to bottom-fish!**"

**One Sentence**: **When others panic, I'm greedy—but confirm it's real panic** 📉→📈

---

## IV. Sell Condition: Overbought + More Overbought = Retreat

### 📉 Sell Signal: Two Conditions Must Both Be Met

| Condition | Meaning | Plain English |
|-----------|---------|----------------|
| RSI_30m > 70 | Entered overbought zone (30-minute) | Price rose too hard, might pull back |
| Williams %R_30m > -20 | Extremely overbought (30-minute) | Williams indicator also confirms "rose too much" |

**Note**: Sell signal uses **30-minute timeframe**, more stable than the 15-minute buy timeframe.

**Plain English Translation**:
> "30-minute RSI above 70 (overbought), Williams %R also above -20 (extremely overbought)—**time to run!**"

**One Sentence**: **When others are greedy, I'm panic—but confirm on 30-minute first** 📈→📉

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Classic Indicator**: RSI is the OG indicator, most people use it
2. **Dual Confirmation**: RSI + Williams %R, reduces false signals
3. **Has Trailing Stop**: Can lock in floating profits, this beats Quickie
4. **Strict Risk Control**: 10% stop-loss + trailing stop, two layers of protection
5. **Dual Timeframe**: 15-minute buy, 30-minute sell, more stable

### ⚠️ Cons (Complaint Time)

1. **Only One Signal**: One buy, one sell, no choices
2. **Many False Signals in Ranging Markets**: RSI keeps crying "wolf" in ranging markets
3. **Might Sell Too Early**: 9% profit target might miss big moves
4. **Oversold Doesn't Mean Up**: RSI < 30 might keep dropping, drop until you doubt life 😅

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Range-bound Oversold Bounce | ✅ Strongly Recommended | This is the strategy's comfort zone |
| Range-bound Consolidation | ✅ Suitable | Many overbought/oversold signals |
| One-way Pump | ❌ Don't Use | RSI will stay overbought, you'll sell too early |
| One-way Dump | ❌ Don't Use | RSI will stay oversold, you'll buy too early |

---

## VII. Summary: How's This Strategy Really?

### One-Sentence Review
> "Classic oversold/overbought strategy, trailing stop is a plus, but easy to get slapped in one-way trends."

### Who Should Use It?
- ✅ Bottom-Fishers: This is your destiny strategy
- ✅ Risk-Averse Traders: Strict stop-loss + trailing stop, sleep well
- ✅ Range-bound Market Traders: Overbought/oversold works best in ranging markets
- ✅ Beginners: Classic indicators, easy to understand

### Who Shouldn't Use It?
- ❌ Trend Followers: This strategy is counter-trend
- ❌ One-way Move Lovers: RSI will "malfunction" in one-way markets
- ❌ Big Move Hunters: 9% profit target might miss 2x gains
- ❌ High-Frequency Traders: Not many signals, not every day

### My Recommendations
1. **Use in Range-bound Markets**: You'll get wrecked in one-way markets
2. **Can Raise ROI**: 9% might be too conservative
3. **Set Trailing Stop Well**: This is the strategy's biggest strength
4. **Combine with Trend Judgment**: If clearly trending, don't use this first

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Mean Reversion

RSI strategy's money-making philosophy:
> **"What goes up must come down, what goes down must come up—I reverse trade at extreme positions."**

- **Oversold Buy**: RSI < 30 + Williams %R < -80 = excessive panic
- **Overbought Sell**: RSI > 70 + Williams %R > -20 = excessive greed
- **Trailing Stop**: Protect floating profits, don't let the duck fly away
- **Dual Timeframe**: 15-minute for buy points, 30-minute to confirm sell points

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📉 Oversold Bounce | ⭐⭐⭐⭐⭐ | This is the strategy's comfort zone |
| 🔄 Range-bound Consolidation | ⭐⭐⭐⭐☆ | Many overbought/oversold signals, good results |
| 📈 One-way Pump | ⭐⭐☆☆☆ | RSI will stay overbought, you sold long ago |
| 📉 One-way Dump | ⭐☆☆☆☆ | RSI will stay oversold, buy more lose more |

**One Sentence Summary**: **Performs best in "range-bound + oversold bounce" markets, gets slapped in one-way trend markets**.

---

## IX. Want to Run This Strategy? Check These Configs First

### 9.1 Trading Pair Configuration

| Config Item | Recommended Value | Note |
|-------------|------------------|-------|
| Timeframe | 15m + 30m | Keep default, don't mess with it |
| Stop-loss | -0.10 | Decent, not too harsh |
| ROI | 0.09 | A bit conservative, can change to 0.15 |
| Trailing Stop | Keep Default | This is a highlight, don't touch |

### 9.2 Key Config File Settings

```yaml
# Recommended configuration
timeframe: '15m'
stoploss: -0.10

# Trailing stop (keep default)
trailing_stop: true
trailing_stop_positive: 0.01
trailing_stop_positive_offset: 0.02

# If you want to be more aggressive, can raise ROI
minimal_roi: { "0": 0.15 }  # 15% profit target
```

### 9.3 Hardware Requirements (Not Critical)

This strategy has minimal computation, any computer can run it:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | No problem |
| 50+ pairs | 8GB | 16GB | Solid |

**Warning**: Strategy is simple, but don't use in one-way trend markets, you'll get slapped 😅

### 9.4 Backtest vs Live

- **Backtest Might Be Inflated**: Historical data makes oversold bounces look successful
- **Live Might Slap You**: RSI can stay in oversold zone for a long time
- **Trailing Stop is Your Lifesaver**: At least can save some profit

**Recommended Flow**:
1. Test in range-bound markets first
2. Observe trailing stop's actual effect
3. Small position live verification
4. Adjust based on market conditions

**Don't force it in obvious trend markets**—this strategy eats range-bound!

---

## X. Bonus: Strategy Author's "Little Quirks"

Looking carefully at the code, you'll find some interesting things:

1. **Buy uses 15-minute, Sell uses 30-minute**
   > "Author thinks buy should be fast, sell should be stable—good logic"

2. **ROI is only 9%**
   > "Maybe author is conservative, or knows oversold/overbought strategies shouldn't be greedy"

3. **Has trailing stop but no fancy features**
   > "Simplicity is beauty, unlike some strategies with hundreds of lines of code"

4. **`process_only_new_candles = True`**
   > "Only calculates on candle close, saves resources—nice attention to detail"

---

## XI. Final Words

### One-Sentence Review
> "Classic oversold/overbought strategy, trailing stop is a highlight, but works best in range-bound markets."

### Who Should Use It?
- ✅ Bottom-Fishers: Oversold bounces are your jam
- ✅ Risk-Averse Traders: Stop-loss + trailing stop, sleep well
- ✅ Range-bound Market Traders: Strategy designed for ranging
- ✅ Beginners: Classic indicators, easy to understand

### Who Shouldn't Use It?
- ❌ Trend Traders: This strategy is counter-trend
- ❌ One-way Move Lovers: RSI will hang out in overbought/oversold zones
- ❌ Greedy Traders: 9% ROI might not satisfy you
- ❌ High-Frequency Traders: Not many signals, need patience

### Manual Trader Recommendations
If manually using this logic:
1. Watch RSI and Williams %R on 15-minute chart
2. Buy when RSI < 30 and Williams %R < -80
3. Set 9% profit target and 10% stop-loss
4. After 1% profit, set 2% pullback trailing stop
5. Sell when 30-minute RSI > 70 and Williams %R > -20

---

## XII. ⚠️ Risk Emphasis Again (Must Read)

### Backtest is Beautiful, Live Trading Be Careful

RSI strategy backtest might look decent—but there are traps:

> **RSI can stay in overbought or oversold zones for a long time**, especially in strong trend markets. You think it's oversold, but it can get even more "oversold."

Simply put: **"Bottom-fish at halfway up the mountain, escape at the foot of the mountain."**

### Mean Reversion Pitfalls

Mean reversion strategies have a fatal problem:
- **Oversold doesn't mean immediate bounce**: Might drop another 20% before bouncing
- **Overbought doesn't mean immediate pullback**: Might rise another 20% before pulling back
- **Only works in range-bound markets**: You'll get repeatedly slapped in one-way trend markets

### My Recommendations (Real Talk)

```
1. Always watch the big trend: Obviously one-way market? Don't use this
2. Set trailing stop well: This is your lifeline
3. Don't go all-in at once: Scale in, safer
4. Can combine with trend indicators: Like add a 200-day SMA filter
```

**Remember**: RSI tells you overbought/oversold, but it won't tell you "oversold can get even more oversold." Light position testing, survival is most important! 🙏

---