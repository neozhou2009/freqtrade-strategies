# BB_RPB_TSL_Tranz Strategy: Bottom-Fisher's "Standard Weapon"

> **Nickname**: Bollinger Band Pullback Hero  
> **Profession**: Left-side trader who chases dips, not pumps  
> **Timeframes**: 5-minute (trading) + 1-hour + 15-minute (auxiliary)

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_Tranz** is a strategy that:
-专门 waits for price to drop to Bollinger Band lower band before buying
- Has 40 buy signals, covering various "bottom-fishing poses"
- Has sell logic even more particular than buy logic, trailing profit-taking is the highlight

Like a professional bottom-fishing hero, before every move needs to check 40 indicators to confirm "this position really hit bottom" 🤣

---

## II. Core Configuration: Simply Put, It's "Batch Retreat"

### Profit-Taking Rules (ROI Table)

```
Profit     Time       Action
──────────────────────────
20.5%   Immediately   Run!
3.8%    81 min later  Run!
0.5%    292 min later Run!
```

**Translation**: This ROI is relatively loose, gives enough profit space. As long as you've made 0.5%+, leave after enough time.

### Stop Loss Rules

```
Profit Rate    Dynamic Stop Loss
──────────────────
>20%     Protect 5% profit
>10%     Protect 3% profit
>6%      Protect 2% profit
>3%      Protect 1.5% profit
Default  Cut loss at 10%
```

**Translation**: Move up the stop loss line when you're making money, put "insurance" on your profits. Lose 10% and admit defeat directly.

---

## III. 40 Buy Conditions: I've Categorized Them for You

This strategy has so many buy conditions it'll dazzle your eyes. I've grouped them into 5 categories:

### 🎯 Category 1: Bollinger Band Pullback (5 conditions)
**Core Logic**: Price drops near BB lower band, time to bottom-fish!

**In Plain English**:
> "Price has dropped too much, it should bounce back, right?"

**Representative Conditions**: `bb`, `is_break`

**Classic Lines**:
- Condition #bb: `close < bb_lowerband3 * 0.999` → "Price broke below 3 standard deviation lower band, oversold!"

---

### 📉 Category 2: Trend Pullback (8 conditions)
**Core Logic**: Wait for pullbacks to buy in an uptrend.

**In Plain English**:
> "Trend is up, now it's pulling back, perfect time to get on board!"

**Representative Conditions**: `local_uptrend`, `local_dip`, `ewo`, `ewo_2`

**Classic Lines**:
- Condition #local_uptrend: `ema_26 > ema_12` → "Moving averages in bullish arrangement, pullback is an opportunity"
- Condition #ewo: `EWO > -5.0` → "Elliott Wave indicator extreme, bottom-fish!"

---

### 🏊 Category 3: NFI Series Signals (20+ conditions)
**Core Logic**: Deep pullback signals from NFI strategy,专门抓大底 (specialized in catching major bottoms).

**In Plain English**:
> "Dropped so hard even its mother doesn't recognize it, if not bottom-fish now, when?"

**Representative Conditions**: `nfi_13`, `nfi_32`, `nfi_33`, `nfix_39`, `nfix_49`...

**Classic Lines**:
- Condition #nfix_39: `close > ema_13 * 0.912` → "Price near EMA13, bottom-fishing opportunity"
- Condition #nfi_38: `cti < -0.95` → "Momentum extreme, buy!"

---

### ⚡ Category 4: Momentum Reversal (5 conditions)
**Core Logic**: Momentum indicator extreme reversals.

**In Plain English**:
> "Too much selling leads to bounce, too much buying leads to pullback"

**Representative Conditions**: `cofi`, `gumbo`, `sqzmom`

---

### 🔍 Category 5: Multi-timeframe Confirmation (5 conditions)
**Core Logic**: Use 15-minute timeframe to confirm signals.

**In Plain English**:
> "5-minute says buy, let's see what 15-minute and 1-hour say"

**Representative Conditions**: `nfix_51`, `nfix_52`, `nfix_53`

---

## IV. Protection Mechanisms: Slippage Protection Is the Highlight

Each buy condition comes with protection mechanisms:

| Protection Type | Function | In Plain English |
|---------|------|--------|
| Slippage Protection | Don't buy if price deviates more than 0.33% | "Price jumping too fast, don't chase" |
| Auxiliary Check | 1h ROC and BB width check | "Don't buy if big trend is wrong" |
| Entry Confirmation | Re-confirm entry price | "Double-check, haven't been screwed, right?" |

---

## V. Sell Logic: Trailing Profit-Taking Is the Core

### 5.1 Trailing Profit-Taking: Run When You've Made Enough

```
Profit Range      Pullback from High    RSI Condition    Signal Name
────────────────────────────────────────────────────────
0% ~ 1.2%        > 4.5%               < 46             profit_t_0_1
0% ~ 1.2%        > 2.5%               < 32             profit_t_0_2
1.2% ~ 2%        > 1%                 < 39             profit_t_1_1
...              ...                  ...              ...
```

**In Plain English**:
- Profit 0-1.2%: Price pulls back 4.5% from highest point, and RSI below 46, run
- Profit 1.2-2%: Price pulls back 1% from highest point, and RSI below 39, run
- The more you've made, the looser the take-profit conditions

---

### 5.2 Special Scenario Exits

| Scenario | Trigger Condition | In Plain English |
|------|---------|--------|
| Quick Profit-Taking | Profit 2-6% and RSI > 80 | "Rose too fast, take profits and go" |
| Momentum Extreme | Profit 2-6% and CTI > 0.95 | "Momentum hit the end, run" |
| PMAX Signal | Price breaks PMAX threshold | "Trend changed, lock in profits" |
| Below Moving Average | Price < EMA200 and profitable | "Trend not good, run if there's profit" |
| Stop Loss - Deadfish | Multiple conditions combined | "This coin is hopeless, cut it" |

---

### 5.3 Base Sell Signals

**Classic Lines**:

1. **Signal #momdiv**: `momdiv_sell == True`
   > "Momentum divergence signal, price is about to turn"

2. **Signal #deadfish**: Multiple conditions combined
   > "This coin's走势 like a dead fish, just cut it"

---

## VI. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Rich Signals**: 40 buy conditions, one of them will catch an opportunity
2. **Clear Code**: More concise than MOD version, suitable for learning
3. **Trailing Profit-Taking**: Automatically locks in profits when price pulls back
4. **Slippage Protection**: Entry confirmation mechanism prevents getting screwed
5. **Multi-timeframe**: Uses 1h and 15m to filter false signals

### ⚠️ Weaknesses (Complaint Session)

1. **Many Parameters**: Requires tuning experience
2. **Tight Stop Loss**: 10% fixed stop loss may stop out too early
3. **Not Suitable for Chasing Highs**: Misses strong upward trends
4. **Heavy Computation**: Multi-timeframe and multi-indicator calculations

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| Slow Bull Trend | Use boldly | Pullback signals precise, profit-taking reasonable |
| Wide Oscillation | Can use | Bollinger Band signals work well |
| Crash Rebound | Use cautiously | Many NFI series signals, but high risk |
| Rapid Pump | Don't use | Strategy偏向 bottom-fishing, will miss opportunities |
| Single-sided Bear | Don't use | Buy and lose, can't stop loss fast enough |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "Classic work of Bollinger Band pullback strategies, clear code suitable for learning"

### Who Should Use It?
- ✅ Quantitative入门 learners
- ✅ "Left-side traders" who like bottom-fishing
- ✅ People who want to二次 develop strategies
- ✅ Traders pursuing stability

### Who Shouldn't Use It?
- ❌ People who like chasing pumps
- ❌ People pursuing explosive profits
- ❌ People with extremely high risk tolerance

### My Suggestions
1. **First Choice for入门**: More concise than MOD version, suitable for learning
2. **Trailing Profit-Taking Is the Highlight**: Automatically locks in profits when price pulls back
3. **Combine with Other Strategies**: Can be used in combination with other strategies
4. **Watch Stop Loss**: 10% stop loss is tight, can adjust based on situation

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Wait for Pullback, Precise Bottom-Fishing

BB_RPB_TSL_Tranz is the core version of the BB_RPB_TSL series. Code volume 1500+ lines, more concise than MOD version.

**Its Money-Making Philosophy**: Only do pullbacks, don't chase pumps

- **Bollinger Band Pullback**: Wait for price to touch lower band
- **Trend Pullback**: Wait for pullbacks in uptrend
- **Trailing Profit-Taking**: Lock in profits when price pulls back from highs
- **Dynamic Stop Loss**: More profit, tighter stop loss

### 9.2 Performance in Different Markets (Human Language Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | "Pullback buys precise, making money lying down" |
| 🔄 Wide Oscillation | ⭐⭐⭐⭐☆ | "Bollinger Band signals work well, steady returns" |
| 📉 Single-sided Decline | ⭐⭐☆☆☆ | "Buy anything and lose, can't stop loss fast enough" |
| ⚡️ Rapid Pump | ⭐☆☆☆☆ | "Strategy偏向 bottom-fishing, missed opportunities" |

**One-Sentence Summary**: Suitable for oscillating upward markets, not suitable for extreme conditions.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Complaint |
|--------|--------|------|
| Number of Pairs | 5-20 pairs | Too many can't calculate |
| Main Market | USDT pairs | Good liquidity |
| Avoid | Low liquidity coins | Slippage will eat you alive |

### 10.2 Configuration File Key Settings

```yaml
# Stop Loss Settings
stoploss: -0.10  # 10% stop loss (tighter)

# Timeframe
timeframe: 5m
informative_timeframe: 1h, 15m

# Enable Custom Stop Loss
use_custom_stoploss: true

# Enable Sell Signals
use_sell_signal: true
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 1-10 pairs | 4GB | 8GB | Okay |
| 10-30 pairs | 8GB | 16GB | Smooth |
| 30+ pairs | 16GB | 32GB | Silky |

---

## XI. Easter Eggs: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **NFI Series Naming**:
   > "nfi_13, nfi_32, nfi_33... Author might be writing a diary"

2. **Sell Lines**:
   > "deadfish, scalp... Vivid and descriptive"

3. **Trailing Buy Subclass**:
   > "There's also a BB_RPB_TSL_Tranz_TrailingBuy subclass, trailing buy functionality"

4. **Slippage Protection**:
   > "max_slip default 0.33%, author might have been screwed before"

---

## XII. Last But Not Least

### One-Sentence Evaluation
> "Classic version of Bollinger Band pullback strategies, clear code suitable for learning"

### Who Should Use It?
- ✅ Quantitative beginners
- ✅ Bottom-fishing enthusiasts
- ✅ People who want to二次 develop
- ✅ People pursuing steady returns

### Who Shouldn't Use It?
- ❌ Pump-chasing enthusiasts
- ❌ People pursuing explosive profits
- ❌ People with extremely high risk tolerance

### Manual Trader Suggestions
If you don't want to run machines, you can reference this logic:
1. Wait for price to drop to Bollinger Band lower band (2-3 standard deviations)
2. Start watching when RSI below 30
3. Wait for a volume candle confirmation
4. Consider taking profit when profit pulls back from highs

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtest Is Beautiful, Be Cautious in Live Trading

BB_RPB_TSL_Tranz's historical backtest performance is often **good**—but remember:

> **Past success doesn't guarantee future profitability.**

### Strategy Risks

- **Tight Stop Loss**: 10% stop loss may stop out too early during violent volatility
- **Bottom-Fishing Risk**: May bottom-fish halfway down the mountain
- **Missed Opportunity Risk**: Strategy偏向 bottom-fishing, misses strong upward trends

### My Suggestions (Heartfelt Words)

```
1. Test in simulation for at least 1 month first
2. Verify with small capital in live trading
3. Watch stop loss settings, 10% may be too tight for some coins
4. Don't chase pumps, this strategy isn't suitable for chasing pumps
5. Withdraw profits when you've made them, don't be greedy
```

**Remember**: No matter how good the strategy, the market won't say hello when it teaches you a lesson. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: This is a classic Bollinger Band pullback strategy, concise code, very suitable as a learning template. But remember: simple ≠ not useful, sometimes simple strategies are more robust.

---
