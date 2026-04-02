# BB_RPB_TSL_RNG_TBS_GOLD Strategy: The "Smart Buyer" That Chases Prices

> **Nickname**: Price-Chasing Gold Digger  
> **Profession**: Bollinger Band Pullback Hunter + Trailing Buy Master  
> **Timeframe**: 5 minutes (5m)

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_RNG_TBS_GOLD** is a strategy that:
- Specializes in "picking up bargains" at the Bollinger Band lower rail
- Doesn't rush to buy when it spots a signal—first chases the price around for a bit
- Uses three layers of insurance to lock in profits after buying

Like a shrewd used car buyer: first checks the car's condition (indicators), spots a good car (signal), then haggles with the owner (trailing buy), and finally signs three contracts for return protection after purchase (three-layer stoploss) 🤣

---

## II. Core Configuration: Simply Put, "Three-Layer Insurance + Chase Buying"

### Take-Profit Rules (ROI Table)

```
0 minutes → 10%
```

**Translation**: Boss says "wrap up when you make 10%", but in actual work it uses three-layer stoploss—ROI is just for show 🎭

### Stoploss Rules (Three-Layer Dynamic Stoploss)

```
Profit < 1.9%    → Hard stoploss -17.8% (run if losing too much)
1.9% - 6.5%     → Tiered stoploss (the more you earn, the looser the stoploss)
Profit > 6.5%    → Chase the profit (stoploss follows the rise)
```

**Translation**:
- Just after buying: strict management,强制 stoploss at 17.8% loss
- Made some money: relax, stoploss line moves up with profit
- Made big money: free-range farming, stoploss line chases profit, locking in most gains

---

## III. 7 Buy Conditions: I've Categorized Them for You

This strategy has many fancy buy conditions, I've grouped them into 3 categories:

### 🎯 Category 1: Bollinger Band Pullback Group (1 condition)

**Core Logic**: Price drops to Bollinger Band bottom, and drops deep enough

**In Plain English**:
> "Boss, this price has dropped to the Bollinger Band basement (triple lower band), and all kinds of oversold indicators are flashing red—time to bottom fish, right?"

**Representative Condition**: Condition #1 `is_BB_checked`

**Classic Lines**:
- `bb_delta > 0.025` → "Gap between Bollinger Band lower band and triple lower band is big enough, this is a real drop"
- `close < bb_lowerband3` → "Price broke below triple lower band, we're in the basement"
- `rmi < 49` → "Momentum indicator says 'really oversold'"
- `cci <= -116` → "CCI also says 'oversold'"
- `srsi_fk < 32` → "Stochastic RSI fast line agrees"

This condition is a "combo punch": must simultaneously satisfy oversold (is_dip) + BB expansion (is_break) two sub-conditions, neither can be missing 🥊

---

### 📊 Category 2: Trend Pullback Group (2 conditions)

**Core Logic**: Big trend is upward, but price pulls back to low levels, buying the trend's dip

**In Plain English**:
> "The big trend is clearly upward (EMA26 > EMA12), price suddenly dropped back—isn't this a 'pullback within the trend'? Get on board quick!"

**Representative Conditions**:
- Condition #2 `is_local_uptrend`: EMA trend + BB pullback
- Condition #3 `is_ewo`: Elliott Wave low entry
- Condition #4 `is_ewo_2`: Elliott Wave high entry

**Classic Lines**:
- `ema_26 > ema_12` → "Trend is upward, no problem"
- `close < bb_lowerband2` → "Price dropped to Bollinger Band lower rail"
- `EWO > -5.585` → "Elliott Wave Oscillator is positive, trend hasn't changed"

---

### 🔄 Category 3: Indicator Cross Group (3 conditions)

**Core Logic**: Various indicator golden crosses/oversold triggers entry

**In Plain English**:
> "Indicators are 'holding a meeting to vote', someone had a golden cross, someone's oversold, someone's ADX confirmed the trend—consensus reached, buy!"

**Representative Conditions**:
- Condition #5 `is_cofi`: Stochastic golden cross + ADX trend strength
- Condition #6 `is_nfi_32`: CTI oversold + RSI combo
- Condition #7 `is_nfi_33`: Extreme oversold (William%R < -98)

**Classic Lines**:
- `crossed_above(fastk, fastd)` → "Fast line golden crossed slow line, buy signal!"
- `adx > 20` → "ADX confirms trend is strong enough, not a fake signal"
- `r_14 < -98.0` → "William%R broke below -98, this is called 'extreme oversold'"
- `cti < -0.88` → "CTI correlation indicator says 'price is too low'"

Condition #7 is the most "extreme"—William%R needs to break below -98, this is basically "can't drop anymore" state 😱

---

## IV. Trailing Buy: The Strategy's "Price-Chasing Artifact"

This strategy has a special feature called **TrailingBuyStrat2**, simply put:

> "After spotting a buy signal, don't rush to place the order—first chase the price around for a bit, wait until the price has dropped enough before buying"

### 4.1 Trailing Buy Process

```
Step 1: Spot signal → Mark "start tracking"
Step 2: Price drops → Record lowest price (update upper limit)
Step 3: Price rebounds → Wait until rebound exceeds offset before buying
Step 4: Timeout/price too high → Cancel tracking, wait for next signal
```

**Plain English Translation**:
Like setting a price drop alert when shopping online—you don't rush to buy, first set a "lowest price record", wait for price to rebound a bit before placing order—this way you can buy at a cheaper price 🛒

### 4.2 Key Parameters

| Parameter | Value | Plain English |
|------|-----|--------|
| trailing_expire_seconds | 1800 | Track for 30 minutes, give up if timeout |
| trailing_buy_max_stop | 0.02 | Don't chase if price rises over 2%, too expensive |
| trailing_buy_max_buy | 0.00 | Must be cheaper than initial price to buy |

### 4.3 Important Warning ⚠️

**Trailing buy is incompatible with backtesting!** What you're running in backtest is the parent class (no trailing buy functionality), live trading enables the subclass. So:

> "Backtest data looks good, doesn't mean live trading will be the same—trailing buy's live trading效果 needs separate testing!"

---

## V. Sell Logic: Even Fancier Than Buying

### 5.1 Three-Layer Stoploss: Run When You've Made Enough

```
Profit Range         Stoploss Strategy       Plain English
──────────────────────────────────────────
< 1.9%             Hard stoploss -17.8%    "强制 stoploss if losing too much"
1.9% - 6.5%        Tiered stoploss         "The more you earn, the looser the stoploss"
> 6.5%             Trailing stoploss       "Stoploss chases profit"
```

**Plain English**:
- **Just bought**: Like strict management school,强制 kicked out at 17.8% loss
- **Made some money**: Like loose supervision, stoploss line moves up with profit
- **Made big money**: Like free-range farming, stoploss line chases profit, locking in most gains

### 5.2 Base Sell Signals

**Signal #1**: Trend weakening
```python
close > sma_9  → Price above short-term moving average
rsi > 50       → RSI no longer oversold
rsi_fast > rsi_slow → Fast line above slow line
```

**Plain English**:
> "Price has risen, RSI is normal too, oversold state is over—time to exit"

**Signal #2**: Moving average divergence
```python
sma_9 > sma_9.shift * 1.005 → Moving average accelerating upward
close < hma_50 → But price below HMA50
```

**Plain English**:
> "Moving average is upward but price can't keep up, this is a 'divergence' signal—might pull back"

---

## VI. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Diversified Entry**: 7 buy conditions cover various scenarios, no fear of single signal misjudgment
2. **Price-Chasing Artifact**: Trailing buy lets you wait for cheaper entry price
3. **Three-Layer Insurance**: Dynamic stoploss locks profits while preserving upside potential
4. **Rich Indicators**: Bollinger Bands, EMA, RSI, EWO, CTI, Williams%R... has everything

### ⚠️ Weaknesses (Complaint Session)

1. **Too many parameters**: Dozens of adjustable parameters, headache when optimizing 🤯
2. **Trailing buy incompatible with backtest**: Backtest runs parent class, live trading runs subclass—effects may differ
3. **High computational overhead**: Pile of indicators + BTC informative layer, old machines might lag
4. **Depends on BTC market**: Optional BTC protection needs extra data source

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Operation | Reason |
|---------|---------|------|
| 📈 Oscillating Uptrend | ✅ Use full power | Pullback entry + trailing stoploss works best |
| 📊 Sideways Oscillation | ✅ Can use | Bollinger Band pullback logic effective |
| 📉 Single-Side Downtrend | ❌ Don't use | Buy signals trigger frequently but price keeps dropping |
| ⚡ High Volatility | ⚠️ Use carefully | Trailing buy might miss opportunities |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "Pullback Hunter + Price-Chasing Master = Smart Buyer in Oscillating Uptrend Markets"

### Who Should Use It?
- ✅ Users with live trading experience (need to understand trailing buy mechanism)
- ✅ Oscillating uptrend market traders
- ✅ People who want to use multi-layer stoploss to protect profits
- ✅ Users who like diversified entry signals

### Who Shouldn't Use It?
- ❌ Newbies (too many parameters, complex logic)
- ❌ People who only do backtest analysis (trailing buy incompatible with backtest)
- ❌ Single-side downtrend market traders
- ❌ Users who don't want to track BTC market

### My Suggestions
1. **Understand trailing buy first**: Figure out TrailingBuyStrat2 logic before live trading
2. **Oscillating uptrend is best**: This strategy is designed for "trend pullbacks"
3. **Don't use in downtrend markets**: Buy signals will trigger frequently but stoploss won't stop
4. **Configure hardware well**: High computational load, recommend at least 8GB memory

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Defense Net" with Complexity

BB_RPB_TSL_RNG_TBS_GOLD is a pullback entry strategy. Code volume 500+ lines, what concept? Equivalent to writing a small strategy novel 📚

**Its money-making philosophy**: Enter on trend pullbacks, use trailing buy to optimize entry price, use three-layer stoploss to lock profits

- **Pullback Entry**: Wait for price to drop to Bollinger Band bottom before buying, buy cheaper
- **Trailing Buy**: Chase price around after spotting signal, wait for lower price before placing order
- **Three-Layer Stoploss**: Strict management when just bought, relax after earning, chase run after earning big

### 9.2 Different Market Performance (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Oscillating Uptrend | ⭐⭐⭐⭐⭐ | Perfect match, pullback entry + trailing stoploss works best |
| 📊 Sideways Oscillation | ⭐⭐⭐⭐☆ | Bollinger Band pullback effective, but stoploss may trigger frequently |
| 📉 Single-Side Downtrend | ⭐☆☆☆☆ | Buy signals trigger frequently, stoploss won't stop, lose money |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | Trailing buy might miss opportunities, stoploss exits too early |

**One-Sentence Summary**:
> "Make money in oscillating uptrend, small profit in sideways, lose money in downtrend, be careful in high volatility"

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Complaint |
|--------|--------|------|
| timeframe | 5m | 5 minutes enough to capture pullbacks |
| startup_candle_count | 100+ | Need enough historical data to calculate indicators |
| BTC data | BTC/USDT 5m | Optional protection needs BTC data |

### 10.2 Configuration File Key Settings

```yaml
# Trailing buy parameters (live trading effective)
trailing_buy_order_enabled: true
trailing_expire_seconds: 1800
trailing_buy_max_stop: 0.02

# Three-layer stoploss parameters
pHSL: -0.178  # Hard stoploss
pPF_1: 0.019  # Tier 1 trigger
pSL_1: 0.019  # Tier 1 stoploss
pPF_2: 0.065  # Tier 2 trigger
pSL_2: 0.062  # Tier 2 stoploss
```

### 10.3 Hardware Requirements (Important!)

This strategy has huge computational load, has requirements for VPS memory:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 1-20 pairs | 4GB | 8GB | Normal |
| 20-50 pairs | 8GB | 16GB | Smooth |
| 50+ pairs | 16GB | 32GB | Stable |

**Warning**: Insufficient memory will cause calculation timeout, signal delays 😅

### 10.4 Backtest vs Live Trading

**Key Difference**: Trailing buy subclass incompatible with backtest!

```
Backtest → Use parent class (no trailing buy functionality)
Live Trading → Use subclass (enable trailing buy)
```

**Suggested Process**:
1. Backtest to verify base strategy logic
2. Demo test trailing buy effects
3. Small position live trading verification
4. Gradually increase position

**Don't go all-in right away**, no matter how good the strategy, it needs breaking in!

---

## XI. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll discover some interesting things:

1. **BTC protection is commented out**:
   > "Code has BTC 5-minute/1-day drop protection, but default commented out—maybe author thought it was too conservative 🤔"

2. **Condition naming is casual**:
   > "is_nfi_32, is_nfi_33, is_cofi... this naming seems随手 done, but logic is rigorous"

3. **Trailing buy class inherits parent class**:
   > "TrailingBuyStrat2 inherits parent class strategy—this way backtest uses parent class, live trading uses subclass, clever!"

4. **Author left sources in comments**:
   > "Each buy condition marks source blog/repository, academic attitude is rigorous 📚"

---

## XII. Last But Not Least

### One-Sentence Evaluation
> "Shrewd pullback hunter, but only suitable for oscillating uptrend markets"

### Who Should Use It?
- ✅ Quantitative traders with live trading experience
- ✅ Oscillating uptrend market enthusiasts
- ✅ People who want to use trailing buy to optimize entry
- ✅ Multi-layer stoploss protection fans

### Who Shouldn't Use It?
- ❌ Pure backtest analysts (trailing buy incompatible)
- ❌ Newbie whites
- ❌ Single-side downtrend market traders
- ❌ People who don't want to manage complex parameters

### Manual Trader Suggestions
If you want to borrow from this strategy for manual trading:
- Bollinger Band lower rail pullback entry thinking is worth learning
- Three-layer dynamic stoploss mechanism has reference value
- Trailing buy's "wait for lower price" thinking can be manually applied
- But monitoring 7 buy conditions manually is too tiring, recommend simplifying

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtest Is Beautiful, Live Trading Needs Caution

BB_RPB_TSL_RNG_TBS_GOLD's backtest performance often **looks good**—but there's a trap:

> **Trailing buy subclass is incompatible with backtest! Backtest runs parent class without trailing buy functionality, live trading enables trailing buy—effects may be completely different.**

Simply put: **Backtest data and live trading are two sets of logic, don't be fooled by backtest!**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Trailing buy timeout**: Price doesn't rebound within 30 minutes, signal cancels
- **Three-layer stoploss conflict**: Different tier stoplosses may cause unexpected exits
- **BTC data missing**: Optional protection needs BTC data source
- **Calculation delay**: Too many indicators may cause signal delays

### My Suggestions (Truth)

```
1. Understand trailing buy logic first, don't go live trading directly
2. Use demo to test trailing buy effects
3. Only enable in oscillating uptrend markets, disable in downtrend markets
4. Start with small positions, don't go all-in right away
```

**Remember**: No matter how smart the pullback hunter is, it can only make money in the right market. Choose the wrong market, smart becomes stupid! 🙏

---

**Final Reminder**: No matter how good the strategy, the market won't say hello when teaching you a lesson. Light position testing, staying alive is most important! 🙏
