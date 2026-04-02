# BB_RPB_TSL_BIV1 Strategy: The "Swiss Army Knife" of Oversold Capture

> **Nickname**: "Swiss Army Knife" of Quantitative Trading—14 buy modes, there's always one for you
> **Profession**: Oversold capture expert + dynamic stop loss bodyguard
> **Timeframe**: Works on 5-minute, observes on 1-hour

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_BIV1** is a strategy that:
- Specializes in bottom-fishing when prices crash to the Bollinger Band lower band
- Has 14 different buy modes covering various oversold scenarios
- Comes with a smart stop loss bodyguard that watches tighter as profits increase
- Has a BTC bodyguard that prevents entry when the overall market crashes

Like an **old fisherman with 14 different fishing tools**, no matter which layer of water the fish are in, there's a suitable net waiting 🎣

---

## II. Core Configuration: Simply "Bottom Fishing + Bodyguards"

### Take-Profit Rules (ROI Table)

```
Target Profit: Auto take-profit at 20.5%
```

**Translation**: This strategy doesn't rely on ROI for auto take-profit, mainly depends on the smart stop loss and sell signals later. ROI is just the last line of defense, like emptying a piggy bank only when it's full.

### Stop Loss Rules

```
Fixed Stop Loss: -10% (backup)
Actual Stop Loss: Dynamic trailing, locks tighter as profit increases
```

**Translation**: There's a -10% hard stop loss as insurance, but the real worker is that smart bodyguard:
- Profit above 3% → Lock 1.5%, run if it drops back 1.5%
- Profit above 6% → Lock 2%, run if it drops back 2%
- Profit above 10% → Lock 3%, run if it drops back 3%
- Profit above 20% → Lock 5%, run if it drops back 5%

**The bodyguard's logic**: The more money you make, the more afraid you are of losing it back, so the tighter it watches! 💰

---

## III. 14 Buy Conditions: I've Categorized Them for You

The buy conditions in this strategy are mind-boggling, so I've grouped them into **5 major categories**:

### 🎯 Category 1: Bollinger Band Oversold Combination (1 condition)
**Core Logic**: Price breaks below Bollinger Band lower band, simultaneous oversold indicator resonance

**In Plain English**:
> "Price has been beaten into the basement (breaks lower band), and heart indicator (RMI), blood pressure indicator (CCI), breathing indicator (SRSI) all show it's nearly dead—time to enter and pick up the corpse!"

**Representative Condition**: is_BB_checked (dip + break combination)

**Classic Lines**:
- `[bb_delta > 0.025]` → "The Bollinger Band gap is wide enough, not a fake fall"
- `[close < bb_lowerband3]` → "Price breaks 3σ lower band, truly beaten into the basement"

---

### 📉 Category 2: Trend Pullback Combination (3 conditions)
**Core Logic**: In an uptrend, price pulls back to support levels

**In Plain English**:
> "Big brother (EMA26) is standing upstairs, little brother (price) has been knocked downstairs—time to catch little brother, big brother will eventually pull him back up!"

**Representative Conditions**: is_local_uptrend, is_local_dip, is_ewo

**Classic Lines**:
- `[ema_26 > ema_12]` → "Long moving average is higher than short, trend is up"
- `[close < bb_lowerband2 * 0.995]` → "Price returns near lower band, discounted entry"

---

### 🌊 Category 3: Extreme Oversold Combination (4 conditions)
**Core Logic**: CTI, Williams %R, EWO all at extreme values simultaneously

**In Plain English**:
> "All extreme indicators are flashing red—heart nearly stopped (CTI<-0.88), blood pressure exploded (Williams %R<-98), EEG abnormal (EWO extreme)—this is the golden moment to pick up corpses!"

**Representative Conditions**: is_nfi_13, is_nfi_32, is_nfi_33, is_nfi_38

**Classic Lines**:
- `[cti < -0.92]` → "CTI dropped to -0.92, heartbeat nearly stopped"
- `[r_14 < -98]` → "Williams %R at -98, blood pressure at lowest point"
- `[EWO < -5.585]` → "EWO negative value very large, trend extremely weak"

---

### 🐟 Category 4: Special Pattern Combination (4 conditions)
**Core Logic**: Deadfish rebound, ClucHA, Cofi, Reverse Deadfish

**In Plain English**:
> "These are the 'dead fish翻身' series—capturing those 'dead fish' that might suddenly jump up in long-term weak environments"

**Representative Conditions**: is_r_deadfish, is_clucHA, is_cofi, is_nfix_49

**Classic Lines**:
- `[is_r_deadfish]` → "Fish is nearly dead (long-term weak), but suddenly someone's feeding it (volume increasing), might翻身!"
- `[is_clucHA]` → "Heikin Ashi smoothed price breaks 40-period BB—using 'noise reduction glasses' to see oversold"

---

### 🔭 Category 5: 1h Information Layer Validation Combination (2 conditions)
**Core Logic**: 1-hour period trend confirmation

**In Plain English**:
> "Saw opportunity on 5-minute chart, but still need to run to 1-hour chart and ask the big boss 'Boss, is this direction reliable?'—only enter when big boss nods"

**Representative Conditions**: is_ewo_2, is_nfix_5

**Classic Lines**:
- `[ema_200_1h > ema_200_1h.shift(12)]` → "On 1-hour chart, EMA200 moving up for 12 consecutive candles, big boss confirms trend is up"

---

## IV. Protection Mechanisms: 3-Layer "Bodyguards"

Each buy condition comes with a set of protection parameters, like **three bodyguards taking shifts**:

| Protection Type | Function | In Plain English |
|---------|------|--------|
| BTC Bodyguard | Pause buying when market crashes | "Big brother (BTC) is crashing, little brother (other coins) don't go sacrifice yourself" |
| 1h Validation Bodyguard | 1-hour period confirmation | "Go to big boss's office for signature, confirm this direction is okay" |
| Slippage Bodyguard | Entry price filter | "Don't let entry price be too ridiculous, won't do it if premium exceeds 0.668%" |

**Roast**: This strategy's bodyguards are stricter than the buy conditions, like checking three generations of family history when dating 🤣

---

## V. Sell Logic: Even Fancier Than Buying

### 5.1 Tiered Take-Profit: Run Based on How Much You Made

```
Profit Range      Trailing Stop
─────────────────────────────────
>20%              Lock 5%
>10%              Lock 3%
>6%               Lock 2%
>3%               Lock 1.5%
```

**In Plain English**:
- Made 3% or more: Run if it drops back 1.5%, keep 1.5% profit
- Made 6% or more: Run if it drops back 2%, keep 4% profit
- Made 10% or more: Run if it drops back 3%, keep 7% profit
- Made 20% or more: Run if it drops back 5%, keep 15% profit

**This is the quantitative version of "take profit and run, don't be greedy"** 💰

---

### 5.2 Special Scenario Exits

| Scenario | Trigger Condition | In Plain English |
|------|---------|--------|
| Profit Drawdown | Max profit drawdown 4.5% + RSI<46 | "Made money but starting to drop, heart indicator says time to run" |
| Quick Take-Profit | RSI>80 | "Heart beating too fast, take profit while you can" |
| MOMDIV Exit | Momentum divergence signal | "Momentum indicator says trend is about to reverse" |
| Deadfish Stop Loss | Loss>5% + BB narrow | "Thought it was bottom fishing, but caught a real deadfish—stop loss quickly" |

---

### 5.3 Base Sell Signals (Relies on custom_sell)

**Classic Lines**:

1. **Signal #sell_profit_t_1_1**
   > "Profit 1.2%-2%, dropped 1% from peak, RSI<39—run with small profit"

2. **Signal #signal_profit_q_1**
   > "Profit 2%-6%, RSI>80—heart exploding, run quickly"

3. **Signal #sell_stoploss_deadfish**
   > "Loss over 5%, price below EMA200, BB very narrow, volume very low—this is a real deadfish, don't keep holding"

---

## VI. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Wide coverage**: 14 buy modes, from trend pullback to extreme oversold, all covered
2. **Smart stop loss**: Locks tighter as profit increases, much smarter than regular stop loss
3. **Multi-layer protection**: BTC bodyguard, 1h validation, slippage filter—triple insurance
4. **Flexible exit**: Trailing stop loss, signal exit, quick take-profit—multiple ways

### ⚠️ Weaknesses (Roast Session)

1. **Too complex**: 14 buy conditions + multi-layer sell, 600+ lines of code, makes you dizzy 🤯
2. **Too many parameters**: Dozens of Hyperopt parameters, "perfect backtest" might just be memorizing answers
3. **High hardware requirements**: Large computation load, old computers might not handle it
4. **Few entry opportunities**: Too many bodyguards, entry conditions strict, sometimes no trades all day

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| Oscillating decline | ✅ Use as main strategy | Oversold capture mechanism perfectly matches this market |
| Moderate trend | ⚠️ Use cautiously | Few pullback opportunities, might miss main rally |
| Crash market | ❌ BTC protection pauses | Strategy auto-stops buying when market crashes |
| High volatility oscillation | ⚠️ Fees hurt | Multiple entries/exits, profits might be eaten by fees |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "This is a 'Swiss Army Knife type' strategy—many tools, powerful, but too complex, easy to confuse yourself"

### Who Is It Suitable For?
- ✅ Quantitative players familiar with Bollinger Bands and oversold indicators
- ✅ Enthusiasts with time to deeply research strategy logic
- ✅ Traders wanting stable profits in oscillating markets
- ✅ Live trading players with sufficient hardware support

### Who Is It NOT Suitable For?
- ❌ Newbie beginners—will get dizzy looking at the code
- ❌ People who like simple strategies—this strategy is more complex than college entrance exam questions
- ❌ Low-spec computer users—might calculation timeout
- ❌ People who just want to make money following strong trends—this strategy is bottom-fishing type

### My Suggestions
1. **Understand before using**: Don't jump into live trading immediately, first understand the 14 buy conditions
2. **Simplify and optimize**: Try turning off some buy conditions, keep only those you understand
3. **Watch for overfitting**: Be alert if backtest performance is too good, might just be memorizing answers
4. **Small position testing**: Test with small positions in live trading first, verify strategy's real performance

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using Complexity to Build a "Defense Net"

BB_RPB_TSL_BIV1's profit philosophy: **Bottom fishing + Bodyguards = Safe corpse picking**

- **Oversold capture**: Price beaten into basement, various indicators say it's done, time to enter
- **Multi-layer validation**: BTC bodyguard (market don't crash), 1h bodyguard (big trend confirmation), slippage bodyguard (price don't be too ridiculous)
- **Dynamic stop loss**: After making profit, watch the profit, run if it drops a bit

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Strong uptrend | ⭐⭐☆☆☆ | Price keeps running up, no pullback opportunities at all—strategy stands there dumbly waiting for oversold, misses main rally |
| 🔄 Oscillating decline | ⭐⭐⭐⭐⭐ | Price drops back and forth, tons of oversold opportunities—strategy bottom-fishes happily |
| 📉 Continuous crash | ⭐⭐☆☆☆ | BTC bodyguard pauses buying—strategy says "big brother crashed, I'm not doing it", but what you hold might still lose |
| ⚡️ High volatility oscillation | ⭐⭐⭐☆☆ | Lots of oversold opportunities, but also lots of fees—profits might get eaten by fees partially |

**One-sentence summary**: Oscillating decline is its home court, strong trend is its blind spot.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Roast |
|--------|--------|------|
| Number of trading pairs | 10-30 | Too few = not enough opportunities, too many = computation explosion |
| Trading pair selection | High volatility coins | Calm coins have no oversold opportunities for half a day |
| Timeframe | Stick with 5m | Don't change to 1m or 1h, parameters are tuned for 5m |

### 10.2 Configuration File Key Settings

```yaml
# Stop loss config (actually overridden by custom_stoploss)
stoploss: -0.10

# ROI (basically don't rely on this)
minimal_roi: { "0": 0.205 }

# Enable signal sell
use_sell_signal: true
```

### 10.3 Hardware Requirements (Important!)

This strategy has huge computation load, requires VPS memory:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 10-20 pairs | 4GB | 8GB | Normal |
| 50+ pairs | 8GB | 16GB | A bit laggy |

**Warning**: Running 50+ pairs on old computer, each candle calculation might take several seconds—miss entry timing 😅

### 10.4 Backtest vs Live Trading

**Backtest might be beautiful**: 14 condition combinations, dozens of parameters, easy to "fit" historical optimal solution.

**Live trading might slap your face**:
- BTC protection reduces entry opportunities (pauses during market volatility)
- Slippage might exceed expectations (live trading isn't ideal price)
- Too many conditions might cause slow judgment (calculation delay)

**Suggested Process**:
1. Backtest first to understand strategy characteristics
2. Simplify conditions (turn off conditions you don't understand)
3. Small position live test (10% capital)
4. Observe for a few months before deciding to increase position

**Don't go all-in immediately**, no matter how good the strategy is, it needs breaking in!

---

## XI. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **BTC Bodyguard's Name**
   > `buy_btc_safe` default -200, `buy_btc_safe_1d` default -0.05
   > "Author set two defense lines for BTC crash: 5-minute crash and 1-day crash"

2. **NFI Series Numbering**
   > Conditions called nfi_13, nfi_32, nfi_33, nfi_38, nfix_5, nfix_49, nfix_51
   > "This numbering looks like author's development notes, who knows what 13 and 32 represent"

3. **Deadfish Stop Loss Name**
   > `sell_stoploss_deadfish`
   > "Author calls stop loss scenario 'deadfish'—bottom-fished a real deadfish, don't keep holding"

---

## XII. Last But Not Least

### One-Sentence Evaluation
> "Strategy is powerful, but complexity is a double-edged sword—used well it's a Swiss Army knife, used poorly it's a self-harm tool"

### Who Is It Suitable For?
- ✅ Players familiar with Bollinger Band theory
- ✅ People who understand oversold indicator meanings
- ✅ Quantitative enthusiasts with patience to research strategy details
- ✅ Live trading traders in oscillating markets

### Who Is It NOT Suitable For?
- ❌ Newbie beginners—learn basics first before playing with this
- ❌ People who like simple strategies—this one is too complex
- ❌ Strong trend chasers—this strategy bottom-fishes, doesn't chase rallies
- ❌ Low-spec players—computation load will eat your CPU

### Manual Trader Suggestions
Don't directly imitate this strategy for manual trading! 14 conditions, multi-layer stop loss, BTC bodyguard—you'll die of exhaustion staring at the screen. Just understand its approach:
- Price breaks Bollinger Band lower band + oversold indicator resonance → Entry opportunity
- After making profit, watch tightly, run if it drops back a bit
- Don't enter when market crashes

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtest Is Beautiful, Be Cautious in Live Trading

BB_RPB_TSL_BIV1's historical backtest performance is often **extremely excellent**—but there's a trap:

> **Because of 14 buy conditions + 60+ parameters, the strategy can easily "fit" the optimal solution of past行情, but this doesn't guarantee future profitability.**

Simply put: **Memorizing answers to get high scores doesn't mean you truly learned**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Calculation delay**: Need to calculate dozens of indicators per candle, might miss best entry timing
- **BTC protection triggers frequently**: Pauses buying when market fluctuates slightly, reduces entry opportunities
- **Stop loss triggers frequently**: Trailing stop loss too sensitive, might take profit on small fluctuations

### My Suggestions (Honest Words)

```
1. Understand strategy first, don't jump to live trading immediately
2. Simplify after backtesting—turn off conditions you don't understand
3. Small position testing—10% capital for a few months
4. Observe live performance before deciding to increase
```

**Remember**: No matter how good the strategy is, the market won't say hello when it teaches you a lesson. Light position testing, staying alive is most important! 🙏
