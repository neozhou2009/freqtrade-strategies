# Strategy005: The "Blood Test Report" School of Quant

> **Nickname**: Blood Test Report, Indicator Family Bucket  
> **Profession**: Multi-indicator combination diagnostician  
> **Timeframe**: 5 minutes

---

## 1. What Is This Thing?

Simply put, **Strategy005** is:
- A strategy that puts RSI, STOCHF, MACD, SAR, Fisher RSI at one table playing mahjong
- Can also "tune parameters" to optimize performance
- Volume must be 4x normal before entering
- Doesn't touch zero coins (filters out too low prices directly)

Like going to hospital for checkup, blood test report has a dozen indicators, doctor must read all before daring to diagnose. This strategy is same, RSI says oversold? No, STOCHF must also golden cross. STOCHF golden crossed? Wait, Fisher RSI not in position yet. All indicators aligned, volume must also be 4x — "Okay, you may enter" 🤣

This is a classic from Freqtrade official strategy library, developed by Gerald Lonlas, specifically as teaching material for students wanting to learn "multi-indicator combination" and "hyperopt optimization".

---

## 2. Core Config: Basically "Seek Progress While Maintaining Stability"

### Profit-Taking Rules (ROI Table)

```
Immediate exit: 5% profit
After 20 min: 4% profit
After 40 min: 3% profit
After 80 min: 2% profit
After 1440 min (24 hours): 1% profit
```

**Translation**: Right after buying, run at 5% profit; if dragged 20 min and not at 5%, then 4% also acceptable; drag longer, threshold lower and lower. Like blind dating, start with high standards, later requirements lower and lower 🤣

**But note**: This strategy max aims for 5% profit, not the type that "catches doubling coins". It's here to make small money, accumulate little by little.

### Stoploss Rules

```
Hard stoploss: -10%
Trailing stop: Trigger after 2% profit, run if 1% pullback
```

**Translation**: Force cut at 10% loss, don't give you any fantasy space. If made 2%+ profit, start "take what you can get", clear position and leave if 1% pullback from highest point.

---

## 3. Entry Conditions: Family Bucket Style Indicator Confirmation

This strategy's entry conditions like talent show, contestants must pass five trials and six cuts:

### 🎯 Trial 1: Price Filter

**Core Logic**: Price must be > 0.00000200

**In Plain English**:
> "Don't touch too low prices, that's graveyard of zero coins. I don't play with those air coins, altcoinshitcoins."

---

### 📊 Trial 2: Volume Confirmation

**Core Logic**: Volume > Rolling average × 4

**In Plain English**:
> "Normally 1M daily volume, today must be 4M before I enter. Places without popularity, entering is being exit liquidity."

**Roast**: 4x average volume, this threshold is a bit high. But right, low liquidity coins are traps.

---

### 📉 Trial 3: SMA Pullback

**Core Logic**: Price < SMA40 (40-period simple moving average)

**In Plain English**:
> "Only buy when price drops below SMA40. This is buy on pullback — don't chase when up too much, wait for pullback then get on."

**Classic Lines**:
- Condition #1: `close < sma` → "Don't chase highs, I get on after pullback"

---

### 🔄 Trial 4: STOCHF Golden Cross

**Core Logic**: fastd > fastk (Stochastic fast line golden cross)

**In Plain English**:
> "STOCHF fast line crosses above slow line, this is short-term momentum turning strong signal. Golden cross appears, means downward momentum may reverse."

---

### 📈 Trial 5: RSI Confirmation

**Core Logic**: RSI > Threshold (default 30, optimized 26)

**In Plain English**:
> "RSI don't be too low, otherwise still in crash. I want oversold rebound, not oversold continuing to fall."

**Roast**: Default RSI > 30, but optimized suggestion is 26. This means more aggressive, dare to bottom fish when more oversold.

---

### 🎯 Trial 6: Fisher RSI Confirmation

**Core Logic**: Fisher RSI (normalized) < Threshold (default 30, optimized 5)

**In Plain English**:
> "Fisher RSI is ordinary RSI transformed, makes it more 'normal distribution'. Normalized below threshold, means really oversold."

**Roast**: Optimized suggestion value is 5, very extreme! Shows this strategy likes to bottom fish when "extremely oversold".

---

### 📋 Summary: 6 Trials

| Trial | Condition | In Plain English |
|-------|-----------|------------------|
| 1 | Price > 0.00000200 | Don't touch zero coins |
| 2 | Volume > Average × 4 | Don't enter without popularity |
| 3 | Price < SMA40 | Buy on pullback, don't chase highs |
| 4 | fastd > fastk | STOCHF golden cross |
| 5 | RSI > Threshold | Don't bottom fish in crash |
| 6 | Fisher RSI < Threshold | Confirm oversold |

**One Line**: This is not "one indicator says buy then buy", but "six indicators hold meeting, all agree before buy". Very cautious.

---

## 4. Protection Mechanisms: Trailing Stop + Hard Stoploss

This strategy's protection mechanisms are relatively simple, just two defense lines:

| Protection Type | Function | In Plain English |
|----------------|----------|------------------|
| Hard Stoploss | -10% force exit | "Cut at 10% loss, don't think about comeback" |
| Trailing Stop | Trigger after 2% profit, exit on 1% pullback | "Secure after making profit, don't give back" |

**Roast**: This strategy's protection mechanisms aren't fancy, just two classic stoploss ways. But enough, too manyrather confuse yourself.

---

## 5. Exit Logic: Two Modes for You to Choose

This strategy's exit is interesting, it gives **two modes**, you can choose in hyperopt optimization:

### 5.1 Exit Mode A: RSI-MACD-minusDI Combination

**Trigger Conditions**:
- RSI crosses above threshold (default 70)
- MACD < 0 (negative)
- -DI > Threshold (default 50)

**In Plain English**:
> "RSI overbought, MACD still in negative zone, -DI momentum indicator also high — time to go, short-term may have topped."

---

### 5.2 Exit Mode B: SAR-FisherRsi Combination

**Trigger Conditions**:
- SAR > Price (SAR indicator above price, trend turning weak)
- Fisher RSI > Threshold (default 50)

**In Plain English**:
> "SAR indicator originally tracks trend, now above price, means trend may reverse. Plus Fisher RSI also high, time to withdraw."

---

### 5.3 Which Should You Choose?

**Answer: Let Hyperopt help you test**. This strategy specifically designed `sell_trigger` hyperparameter, let optimizer decide which mode is better.

**Roast**: This is also this strategy's essence — don't guess, let data tell you.

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Multi-Indicator Confirmation**: 6 indicators hold meeting, false signals few
2. **Volume Filter**: Must be 4x average volume before entering, excludes junk coins
3. **Hyperopt Optimization**: Can tune parameters yourself, find configuration most suitable for your pairs
4. **Trailing Stop**: Secures profits, not greedy
5. **Official Strategy**: Classic from Freqtrade official library, quality guaranteed

---

### ⚠️ Cons (Roast Section)

1. **High Complexity**: 6 indicators + hyperopt optimization, beginners easy to get dizzy
2. **No BTC Correlation**: Doesn't watchmarket, may suffer when Bitcoin crashes
3. **SMA Pullback Logic**: Must be below SMA40 to buy, may miss out in strong trends
4. **Overfitting Risk**: Hyperopt optimization too aggressive, may lead to "memorizing answers" — perfect historical backtest, sucks in live
5. **Exit Mode to Choose**: Two modes, beginners may not know which to choose

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Ranging Up** | ✅ Recommended | Multi-indicator combo performs well in ranging |
| **Wide Ranging** | ✅ Recommended | Momentum indicators like RSI, STOCHF suitable for ranging |
| **One-Way Crash** | ❌ Not Recommended | No BTC correlation, crashes withmarket |
| **Extreme Sideways** | ⚠️ Average | Too little volatility, volume filter may have no signals |
| **High Volatility** | ⚠️ Need Adjustment | May need to adjust stoploss thresholds |

---

## 8. Summary: How Is This Strategy Really?

### One-Line Review
> **"Medical checkup school player, indicator family bucket. More verification fewer mistakes, but missing opportunities also normal."**

### Who Should Use It?
- ✅ Beginners wanting to learn multi-indicator combination
- ✅ Quant enthusiasts wanting to learn hyperopt optimization
- ✅ People who like conservative entry style
- ✅ Short-term traders who can accept 5% profit target

### Who Should NOT Use It?
- ❌ Gamblers wanting to catch doubling coins
- ❌ Lazy people who don't want to tune parameters
- ❌ People who only want to use simple strategies
- ❌ People who don't want to do hyperopt optimization

### My Recommendations
1. **As Teaching Material First**: This is good Hyperopt learning case, run through default parameters first
2. **Then Optimize**: Use Hyperopt to find parameters suitable for your pairs
3. **Verify Verify Then Verify**: Remember to verify after optimization, don't be fooled by overfitting
4. **Add BTC Correlation**: If using in live, recommend adding BTC trend filter

---

## 9. What Markets Make Money With This?

### 9.1 Core Logic: Reduce False Signals with Multi-Indicators

Strategy005 is Freqtrade official classic strategy, core philosophy is "multi-indicator confirmation + hyperopt optimization".

**Its Money-Making Philosophy**: Better to miss than to do wrong.

- **Multi-Indicator Confirmation**: 6 indicators hold meeting, false signals naturally few
- **Volume Filter**: Must be 4x average volume before entering, ensures market active
- **Pullback Entry**: Only buy when below SMA40, don't chase highs

---

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|------------|-------------------|--------------------------|
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐☆ | Multi-indicator combo performs well in uptrends, pullback entry can catch meat |
| 🔄 Wide Ranging | ⭐⭐⭐⭐☆ | Ranging market is its home field, RSI oversold rebound, STOCHF golden cross can catch |
| 📉 One-Way Crash | ⭐⭐☆☆☆ | No BTC correlation, crashes withmarket, may stoploss consecutively |
| ⚡ Extreme Sideways | ⭐⭐☆☆☆ | Too little volatility, volume can't reach 4x, signals very few |

**One-Line Summary**: Most comfortable in ranging up, be careful in sideways and crash.

---

## 10. Want to Run This? Check These Configs First

### 10.1 Pair Configuration

| Config | Recommended Value | Roast |
|--------|------------------|-------|
| Number of Pairs | 30-60 pairs | Too few signals not enough, too many computation heavy |
| Max Open Trades | 5-10 orders | Don't be greedy, control risk |
| Position Mode | Fixed Position | Simple and effective, don't do fancy stuff |

### 10.2 Config File Key Settings

```yaml
# Timeframe mandatory 5 minutes
timeframe: 5m

# ROI Table
minimal_roi:
  0: 0.05      # 5%
  20: 0.04     # 4%
  40: 0.03     # 3%
  80: 0.02     # 2%
  1440: 0.01   # 1%

# Stoploss
stoploss: -0.10

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.01
trailing_stop_positive_offset: 0.02
```

### 10.3 Hardware Requirements (Important!)

This strategy has medium computation, multiple indicators add some calculation:

| Pairs | Minimum RAM | Recommended RAM | Experience |
|-------|-------------|-----------------|------------|
| 30-60 | 1GB | 2GB | Silky smooth |
| 60-100 | 2GB | 4GB | Okay |
| 100+ | 4GB | 8GB | May lag |

**Warning**: If you run Hyperopt optimization, memory requirements double. Don't use 512MB VPS to run optimization!

### 10.4 Backtest vs Live Trading

**Backtest Trap**: This strategy supports hyperopt optimization, easy to "memorize answers" — perfect performance on historical data, sucks in live.

**Recommended Process**:
1. Run backtest with default parameters first, understand baseline performance
2. Optimize parameters with Hyperopt (recommend `--epochs 500`+)
3. Verify optimized parameters with data from different time periods
4. Small position live test
5. Continuous monitoring, re-optimize if necessary

**Don't go all-in immediately**, no matter how good the strategy needsbreak-in period!

---

## 11. Easter Egg: The Author's "Little Tricks"

Look carefully at the code, you'll find interesting things:

1. **Price Filter > 0.00000200**:
   > "This is excluding those extremely low price zero coins. Author may have been hurt byshitcoins coins."

2. **Volume 4x Average Before Entry**:
   > "Author doesn't like cold coins. Places nobody trades, entering is sending death."

3. **Two Exit Modes Optional**:
   > "Author also struggled with how to exit, might as well let user choose. Or let Hyperopt help you choose."

4. **Fisher RSI Normalization**:
   > "Transform RSI into more 'normal distribution' form. This is advanced player's approach, beginners may not know what Fisher transform is."

---

## 12. Final Final Words

### One-Line Review
> **"Official product, must be quality. Textbook-level case of multi-indicator combination, top choice for learning Hyperopt."**

### Who Should Use It?
- ✅ Quant beginners wanting to learn multi-indicator combination
- ✅ Enthusiasts wanting to learn hyperopt optimization
- ✅ People who like conservative entry style
- ✅ 5-minute framework short-term traders
- ✅ Steady players who can accept 5% profit target

### Who Should NOT Use It?
- ❌ Aggressive players wanting to catch doubling coins
- ❌ Lazy people who don't want to tune parameters
- ❌ People who only want to use simple strategies
- ❌ People who don't want to do backtest verification

### Manual Trading Recommendations

If you're manual trading, can reference this strategy's approach:
- Observe RSI, STOCHF, Fisher RSI multiple indicators simultaneously
- Enter only when volume amplifies (at least 2x average)
- Use trailing stop to protect profits
- Set price filter, avoid zero coins

---

## 13. ⚠️ Risk Reminder Again (MUST READ This Section)

### Backtests Are Beautiful, Live Trading Needs Caution

Strategy005 supports hyperopt optimization, backtest performance often **extremely excellent** — but here's a trap:

> **Hyperopt optimization easily "overfits" historical data, like memorizing answers. Exam questions change, scores drop.**

Simply put: **That perfect backtest result you see, may only be valid for that historical period.**

---

### Hidden Risks of Complex Strategies

In live trading, multi-indicator combination may lead to:
- **Signals Reduce**: Probability of 6 indicators confirming simultaneously is low, signals may be fewer than you think
- **Miss Opportunities**: SMA pullback logic in strong trends may lead to missing out
- **Exit Timing Vague**: Two exit modes, choosing wrong may sell early or late
- **Parameter Drift**: Parameters optimized yesterday may not apply tomorrow

---

### My Recommendations (Real Talk)

```
1. Run 3 months backtest with default parameters first, see baseline performance
2. Optimize with Hyperopt, but don't just look at profit, look at Sharpe ratio and max drawdown
3. Verify optimized parameters with different time periods, at least 3 periods
4. Live test with small position first, e.g., 10% of total capital
5. Check once a month, if performance declines, re-optimize
```

**Remember**: No matter how good the strategy, the market won't say hello before teaching you a lesson. Hyperopt optimization is double-edged sword, use well make money, use badly "memorize answers". Light positions for testing, survival is most important!

---

**Final Reminder**: This is official classic strategy, worth learning. But don't treat optimized parameters as gospel, market is always right. 🙏
