# NfiNextModded Strategy: The Community-Modded NFI Next

> **Nickname**: NFI Next's "Plastic Surgery Plus Version"  
> **Profession**: A trend hunter "modded" by the community  
> **Timeframe**: 5 Minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **NfiNextModded** is:
- NostalgiaForInfinityNext "modded" by the community
- Has **42 entry conditions** (4 more than the original Next!)
- Exit logic is even more varied
- A "optimized version" incorporating community live-trading experience

It's like an already-complex strategy that a group of "enthusiastic netizens" patched and improved a bunch more 🤣

**Modded = Modified = Modified Version**

This strategy is the crystallization of community wisdom, but that also means... versions might be more numerous than stars, and you need to find the right source!

---

## 2. Core Settings: Basically "Make This Much or Cut This Much"

### Take-Profit Rules (ROI Table)

```
Make 10% right after buying? → Run!
Hold for 30 minutes making 5%? → Run!
Hold for 1 hour making 2%? → Run fast!
```

**Translation**: The longer you hold, the lower the standard. Like dating — high standards at first, but as time goes by, "good enough to get by" kicks in 😅

### Stop-Loss Rules

```
Hard stop-loss: Cut at -10% loss, no discussion
Trailing stop: After making money, retreat 1% before running, but must first make 3% to activate
```

**Translation**: Ruthless when losing money, tolerant when making money — classic "cut losses short, let profits run"

---

## 3. 42 Entry Conditions: I've Categorized Them for You

This strategy's entry conditions are absurdly numerous, and I've organized them into 7 categories:

### Target Category 1: Oversold Bargain Hunting (7 conditions)
**Core Logic**: RSI low, MFI low, price dropped too much, time for a rebound

**Plain English**:
> "This coin is beaten down, RSI below 30, money flow is frozen — if not now to bottom-fish, then when?"

**Representative Conditions**: #1, #7, #8, #18, #20, #21, #38

---

### Target Category 2: Bollinger Band Breakout (11 conditions)
**Core Logic**: Price drops below BB lower band, meaning it's oversold and should revert

**Plain English**:
> "Price broke below the BB lower band — like a rubber band pulled too tight, it's gotta bounce back eventually!"

**Representative Conditions**: #2, #3, #4, #5, #6, #9, #10, #14, #18, #22, #23

**Classic Lines**:
- Condition #2: `Close < BB lower band × 0.983` → "Broke below by 1.7%, deep enough, buy!"
- Condition #4: `Close < BB lower band × 0.98 + Volume < average × 10` → "Broke below without volume, probably a fakeout, buy!"

---

### Target Category 3: EMA Golden Cross Trend (7 conditions)
**Core Logic**: Fast EMA crosses above slow EMA, trend is looking up

**Plain English**:
> "EMA12 already golden crossed EMA26, trend is up, get on board!"

**Representative Conditions**: #5, #6, #7, #14, #15, #39, #40

**Classic Lines**:
- `EMA26 - EMA12 > open price × 0.018` → "Golden cross strength is enough, not a fake signal!"

---

### Target Category 4: SMA Offset (7 conditions)
**Core Logic**: Price is below SMA by a certain percentage, meaning undervalued

**Plain English**:
> "Price is 5% below the 30-day MA, such a deal — can't pass this up!"

**Representative Conditions**: #9, #10, #11, #12, #13, #16, #17

---

### Target Category 5: EWO Waves (6 conditions)
**Core Logic**: Elliott Wave Oscillator judges wave position

**Plain English**:
> "EWO shows we're at wave 3 start now — if not boarding now, then when?"

**Representative Conditions**: #12, #13, #16, #17, #22, #23

**Classic Lines**:
- Condition #12: `EWO > 1.8` → "Wave is up, charge!"
- Condition #13: `EWO < -11.4` → "Wave went down too hard, time to bounce, reverse charge!"

---

### Target Category 6: Esoteric Indicators (5 conditions)
**Core Logic**: Uses some relatively niche indicators

**Representative Conditions**: #19, #24, #25, #26, #27

**Indicator List**:
- **Chopiness**: Determines if market is ranging or trending
- **Zema/Hull**: Various modified MAs with less lag
- **Williams %R**: Another version of overbought/oversold indicator

**Plain English**:
> "I can't even pronounce some of these indicator names, but反正 it means 'feeling like it's going up'!"

---

### Target Category 7: Modded New Additions (5 conditions) — Added by the Community!
**Core Logic**: The community felt the original wasn't enough and added 5 more

**Plain English**:
> "37 conditions in the original not enough? Community guys added 5 more!"

**Representative Conditions**: #38, #39, #40, #41, #42

**New Condition Brief**:
- **Condition #38**: Enhanced RSI Rebound → "Extreme oversold RSI + volume confirmation"
- **Condition #39**: EMA Trend Confirmation → "MA bullish alignment, buy on pullback"
- **Condition #40**: Multi-Timeframe Resonance → "5m, 1h, 1d triple confirmation"
- **Condition #41**: Volume Breakout Confirmation → "Buy only when price and volume both rise"
- **Condition #42**: Comprehensive Oversold Rebound → "RSI+MFI double oversold + price stabilization signal"

---

## 4. Protection Mechanisms: 42 Layers of "Fuses"

Each entry condition comes with a set of protection parameters, like insurance for each reason:

| Protection Type | Purpose | Plain English |
|-----------------|---------|---------------|
| **Fast EMA** | Ensures price is above EMA200 | "Major trend must be up, right?" |
| **Slow EMA** | 1h level EMA must also be up | "1-hour timeframe can't be falling either, right?" |
| **SMA200 Rising** | 200-day MA must be rising | "Long-term trend can't break!" |
| **Safe Dip** | Can't buy right after a crash | "Don't catch a falling knife!" |
| **Safe Pump** | Can't chase right after a surge | "Don't chase after a 50% pump!" |
| **BTC Trend** | BTC can't be crashing | "Big brother can't collapse, little brothers can rise!" |
| **Volume Filter** | Volume must confirm (Modded new) | "Why would I buy a coin nobody's buying?" |

**42 sets of protection parameters** = 42 entry conditions × one insurance policy each

This strategy's cautiousness is comparable to checking someone's three generations of family history in a blind date 🤣

---

## 5. Exit Logic: Fancier Than Entry

### 5.1 Tiered Take-Profit: Run When You Make X%

```
Profit Rate      RSI Threshold    Signal Name
────────────────────────────────────────────────
> 20%           < 34            signal_profit_11 (making big money, RSI low also runs)
16%-20%          < 42            signal_profit_10
14%-16%          < 54            signal_profit_9
...
2%-3%           < 34            signal_profit_0 (making small money, RSI low runs fast)
```

**Plain English**:
- Making a lot: Can hold even if RSI is a bit low
- Making a little: RSI drops a bit, run immediately, secure the win

---

### 5.2 Special Scenario Exits

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| **Below EMA200** | Price below EMA200 + making money | "Trend is bad, take the money and run" |
| **Pump Protection** | Detected 24h/36h/48h pump + making money | "This coin pumped 50%, take profit and run, don't be the bag holder" |
| **Downtrend** | SMA200 falling + making money | "Major trend is down, don't be greedy" |
| **Trailing Stop** | Pullback from high + RSI moderate | "Pulled back from the high, trend might be gone" |
| **Holding Duration** | Held over 15 hours + making money | "Held this long, time to rotate to the next one" |
| **Williams %R** | Extreme overbought + making money | "RSI hit 80, what are we waiting for?" |

---

### 5.3 Base Sell Signals

**Classic Lines**:

1. **Signal #1**: `RSI > 79.5 + 5 consecutive candles above BB upper band`
   > "Five consecutive candles outside the upper band, RSI at 80 too, and we're NOT running?"

2. **Signal #2**: `RSI > 81 + 2 consecutive candles above BB upper band`
   > "More aggressive version, runs after just 2 candles!"

3. **Signal #4**: `RSI > 73 + RSI(1h) > 79`
   > "Both 5-minute and 1-hour overbought, double kill!"

4. **Signal #6**: `Price < EMA200 + Price > EMA50 + RSI > 79`
   > "Long-term trend down, short-term overbought, run run run"

5. **Signal #7**: `RSI(1h) > 81 + EMA12 crosses below EMA26`
   > "1-hour overbought + death cross, this is about to crash"

---

## 6. The Strategy's "Personality Traits"

### Advantages (The Praise Section)

1. **Community Optimized**: Live-trading experience incorporated, bugs fixed, more stable
2. **More Conditions**: 42 conditions, one is bound to fit the current market
3. **More Complete Protection**: 42 sets of protection parameters, all sorts of anti-chase and anti-knife protection
4. **Flexible Take-Profit**: Make more, hold longer; make less, run faster
5. **Multi-Timeframe**: 5-minute operation + 1-hour trend + 1-day big picture

### Limitations (The Roast Section)

1. **Version Chaos**: Modded versions may have several branches, you gotta find the right source!
2. **Parameters Overwhelming**: 42 conditions × N parameters, optimization can drive you insane
3. **High Data Demand**: Needs sufficient 1h and 5m historical data, new coins won't work
4. **Depends on External Libraries**: TA-Lib, technical libraries, installation alone can take hours
5. **May Overfit**: 42 conditions, might just be hard-coded "perfect history"
6. **Computationally Heavy**: Each cycle computes 40+ indicators, old computers might lag

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Ranging Market** | Enable Bollinger Band conditions (#2,3,4,9,10,14,18) | Bollinger Bands work best in ranging markets |
| **Uptrend** | Enable EMA trend conditions (#1,5,6,7,15,16,39,40) | When trend comes, get on board |
| **Downtrend** | Enable EWO negative conditions (#12,13,17,26,27) | Oversold rebound logic |
| **High Volatility** | Enable all protection parameters | Open all shields when volatility is high |
| **Low Volatility** | Relax protection thresholds | Don't filter yourself out when volatility is low |
| **BTC Crash** | Pause all conditions | When big brother crashes, little brothers struggle in vain |

---

## 8. Bottom Line: How's This Strategy Really?

### One-Word Verdict
> **"A community-'modded' NFI Next, more conditions, more versions, but also more 'community verified'"**

### Who Should Use It?
- Quantitative enthusiasts who like studying parameters and tinkering
- Experienced traders with sufficient historical data
- Tech-savvy types who can handle complex strategies
- People willing to spend time verifying Modded version sources

### Who Should NOT?
- People wanting "one-click get-rich-quick"
- Friends with low-end computers
- Complete beginners (will be scared off by parameters)
- People unwilling to research version sources

### My Advice
1. **Verify the source first**: Modded versions may have several, find a trustworthy community or developer
2. **Backtest first**: Don't go live immediately, check historical performance first
3. **Reduce conditions**: 42 is too many, pick a few suitable for the current market
4. **Adjust parameters**: Protection parameters can be adjusted based on coin volatility
5. **Watch BTC**: When BTC crashes hard, this strategy can't save you either

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Building a "Defense Net" with Complexity

NfiNextModded is the community-optimized version of the NFI series. Code volume 10,000+ lines. What's that mean? Like writing a short novel! 📚

**Its Money-Making Philosophy**: Not about one trick wonder, but about "I have 42 ways to enter, one is bound to fit the current market".

- **Multi-dimensional entry**: Oversold rebound, trend breakout, pullback confirmation... you don't need to guess the market, the strategy picks for you
- **Strict risk filtering**: Real-time detection of "24h/36h/48h rises" prevents chasing; detects "BTC 1h trend", big brother drops, lie flat
- **Dynamic position management**: Supports "won't exit until profitable" feature, can hold through losses to breakeven
- **Community optimization**: Modded version incorporates live-trading experience, fixes known bugs

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---|:---|
| Slow Bull/Ranging Upward | StarsStarsStarsStarsStars (Best) | When trend is up, strategy疯狂opens entry conditions, buys on pullbacks, makes money lying down |
| Wide Ranging | StarsStarsStars (Okay) | Catches bands but many false breakouts, frequent trades, fees might sting |
| One-Sided Selloff | StarsStars (Poor) | Though has stop-loss and BTC filtering, liquidity is poor during selloffs, stop-loss slippage can be huge |
| Extreme Sideways | Star (Terrible) | Too little volatility, most entry conditions can't trigger, strategy directly "hibernates" |

**One-Line Summary**: **Makes money in bull markets, doesn't lose big in bear markets, lies flat during sideways**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Commentary |
|-------------|------------------|------------|
| **Number of trading pairs** | 40-80 USDT trading pairs | Don't overdo it or underdo it, 40-80 is just right |
| **Quote currency** | USDT | Don't use BTC/ETH as quote, things get messy |
| **Maximum positions** | 4-12 orders | Too many open positions and you can't keep track |
| **Position mode** | Full margin (`unlimited`) | Equal distribution per position |
| **Timeframe** | 5m | Mandatory, don't struggle, can't change |

### 10.2 Key Config File Settings

```yaml
timeframe: 5m                    # Don't change, breaks if you do
use_exit_signal: true            # Use strategy's own sell signal
exit_profit_only: false          # Cut when needed, don't hold desperately
ignore_roi_if_entry_signal: true # When sell signal comes, ROI table takes a back seat
```

### 10.3 Hardware Requirements (Important!)

This strategy is computationally heavy and has RAM demands:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|----------------|------------|
| 20-40 pairs | 2GB | 4GB | Can run, but don't expect speed |
| 40-80 pairs | 4GB | 8GB | Comfortable, recommended config |
| 80+ pairs | 8GB | 16GB | Rich people flex freely |

**Warning**: If RAM isn't enough, the strategy might lag due to calculation timeouts, don't blame the strategy when you lose money 😅

### 10.4 Backtest vs. Live Trading

Modded versions include dynamic position adjustment and Hold Support, hard to fully simulate in regular backtesting.

**Recommended Process**:
1. Backtest first to see approximate performance
2. Dry-Run for 1-3 months
3. Small capital live test
4. Scale up after stability

**Don't go all-in right away**, even the best strategy needs a磨合 period!

---

## 11. Easter Egg: The Modded Version's "Little Tricks"

What's the difference between Modded and original? Look closely:

1. **New Conditions #38-42**: Community felt 37 wasn't enough and added 5 more
   > "Original missed some signals, patch them up!"

2. **Optimized Protection Parameters**: Thresholds may have been adjusted
   > "Original too conservative/aggressive, tweak tweak tweak!"

3. **Bug Fixes**: Some edge cases may have been fixed
   > "Original had a minor bug, community helped fix it!"

4. **Enhanced Stop-Loss Logic**: May be smarter
   > "Original stop-loss too mechanical, optimize it!"

5. **Version Numbers**: Note Modded may have multiple versions
   > "Who modded this Modded? Which version is latest?"

**Friendly Reminder**: Modded versions may have multiple branches, get them from a trusted source!

---

## 12. The Very End

### One-Word Verdict
> **"A community-'modded' NFI Next, more conditions, more versions, but also more 'community verified'"**

### Who Should Use It?
- Quantitative enthusiasts who like studying parameters and tinkering
- Experienced traders with sufficient historical data
- Tech-savvy types who can handle complex strategies
- Friends with VPS RAM above 4GB
- People willing to spend time verifying Modded version sources

### Who Should NOT?
- People wanting "one-click get-rich-quick"
- Friends with low-end computers (2GB RAM, don't try)
- Complete beginners (will be scared off by parameters)
- People expecting to make money during sideways (this strategy can't do that)
- People unwilling to research version sources

### Manual Trader Advice
If you trade manually, NfiNextModded is suitable when **the broader market is above MA20 and MAs are in bullish alignment**; for fully automated operation, it is recommended to enable **Bitcoin trend filtering**, which helps automatically "lie flat" for defense when the broader market turns bearish.

---

## 13. Final Warning (Must Read!)

### Backtests Look Great, Live Trading Requires Caution

NfiNextModded often shows **extremely impressive** historical backtest performance — but there's a trap:

> **Because there are many parameters, the strategy easily "fits" the optimal solution for past market conditions, but that doesn't mean it will definitely profit in the future.**

Simply put: **Backtest data looks good, probably because it's too good at "memorizing answers".**

### Additional Risks of Modded Versions

Beyond the original NFI risks, Modded versions also have:

- **Version Chaos**: May have several Modded branches, quality varies
- **Unknown Source**: No idea who modded it, what they changed
- **Maintenance Issues**: Original updated, Modded may not keep up
- **Compatibility**: May not be compatible with latest Freqtrade version

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Unexpected behavior in extreme markets**: Such as chain stop-losses, condition misfires
- **Calculation delays**: Too many indicators, VPS lag may miss best buy/sell points
- **Protection mechanism failures**: Theoretically has many protections, but may not work as expected in real markets

### My Advice (Sincere Words)

```
1. Verify Modded source is trustworthy (official community or known developers) first
2. Check update logs and change descriptions
3. Test with minimum capital (e.g., 100U)
4. Live run for at least 1 month, observe performance in various extreme markets
5. Compare original and Modded actual performance
6. Verify all protection mechanisms work as expected in real markets
7. Consider scaling up only after stability
```

**Remember**: Strategies are rigid, markets are alive. Even the most complex strategy can't handle black swans. Test with light positions, staying alive is what matters!

---

**Final Reminder**: No matter how good a strategy is, the market doesn't give warnings. Test with light positions, staying alive is what matters!
