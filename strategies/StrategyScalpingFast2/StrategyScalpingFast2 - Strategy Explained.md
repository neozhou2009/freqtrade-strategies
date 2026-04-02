# StrategyScalpingFast2: The Parameterized Lightning Scout

> **Nickname**: Configuration Wizard, Multi-Timeframe Master  
> **Job**: Smart scalper with trend filtering  
> **Timeframe**: 1-minute execution + 5-minute trend confirmation

---

## I. What Is This Strategy?

Simply put, **StrategyScalpingFast2** is the **upgraded version** of StrategyScalpingFast:

- **Smarter**: Added 5-minute trend confirmation, won't trade against the trend
- **More flexible**: Parameters can be configured, turn on whatever conditions you want
- **More complex**: 50% more code, 50% more features

It's like a **sniper with a telescope** 🎯 —— not just looking at what's in front, but checking the big picture too, ensuring you don't fight against the wind!

---

## II. Core Configuration: "Smart Profit Taking"

### Profit Taking Rules (Tiered ROI Table)

```
After 0 minutes  → 8.2% profit target
After 18 minutes → 6% profit target
After 51 minutes → 1.2% profit target
After 123 minutes → Any profit, just sell
```

**Translation**:
- Just bought, appetite big, want 8.2%
- As time goes on, getting less patient, anything is fine
- Over 2 hours? As long as there's profit, run!

### Stop Loss Rules

```
Loss reaches 32.6% → Admit defeat and leave
```

**Translation**: This stop loss is way too wide! 32.6%! Is this scalping or long-term investing? 😅

**Recommendation**: Change to 10-15% to be more reasonable.

---

## III. Buy Conditions: More Flexible Than Original

### 3.1 Base Conditions (MUST meet!)

| Condition | Plain English |
|-----------|---------------|
| volume > 0 | "Someone must be trading" |
| open < ema_low | "Price is on the floor" |
| resample_sma < close | "5-minute trend is up, not counter-trend bottom fishing" |

### 3.2 Optional Conditions (Turn on if you want)

| Condition | Default Threshold | Default Status | Plain English |
|-----------|-------------------|----------------|---------------|
| MFI < 19 | 19 | Off | "Money flow dried up" |
| FastK < 19 | 19 | Off | "K line oversold" |
| FastD < 29 | 29 | Off | "D line oversold" |
| ADX < 30 | 30 | Off | "Trend not too strong" |

**Classic line**:
> "Base conditions ensure big direction, optional conditions you add yourself. I give you freedom, but freedom has a price — you need to tune parameters yourself!"

### 3.3 The Coolest Feature: 5-Minute Trend Confirmation

This is StrategyScalpingFast2's biggest upgrade:

```python
# Resample 1-minute data to 5-minute
resample_factor = 5  # 1 minute × 5 = 5 minutes

# Calculate 5-minute SMA (50 periods)
sma = SMA(50)  # In 5-minute timeframe

# Only buy when 5-minute SMA is below close price
# Meaning: price is above 5-minute SMA
```

**Plain English**:
> "I look at 1-minute chart to trade, but first confirm the 5-minute big trend. If 5-minute trend is up, I'll act; otherwise, no deal!"

**It's like**: Before buying stocks, check the monthly trend first. If big trend is bad, don't buy. Even though you're doing short-term trading, you have to follow the long-term trend 👀

---

## IV. Sell Logic: Tiered Retreat

### 4.1 Sell Conditions (Default Configuration)

| Condition | Threshold | Status | Plain English |
|-----------|-----------|--------|---------------|
| open >= ema_high | - | Required | "Price hit the ceiling" |
| FastK crosses above 68 | 68 | On | "K line overbought" |
| FastD crosses above 72 | 72 | On | "D line overbought" |
| MFI > 89 | 89 | On | "Money flow too strong" |
| ADX < 86 | 86 | On | "Trend about to end" |

**Translation**: Price reaches upper band, plus some overbought confirmation, then sell.

### 4.2 The Wisdom of Tiered ROI

| Holding Time | Profit Target | Mindset Change |
|--------------|---------------|----------------|
| 0-18 minutes | 8.2% | "Big appetite, give me 8.2%!" |
| 18-51 minutes | 6% | "Fine, 6% is okay too" |
| 51-123 minutes | 1.2% | "Just give me some profit" |
| After 123 minutes | Any | "Finally some profit, run!" |

**Plain English**:
> "When I first buy I want big money, but as time goes on I become more zen-like."

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Time for Compliments)

1. **Parameterized design**: Turn on whatever conditions you want, freedom maxed out
2. **Multi-timeframe**: 5-minute confirms big trend, no counter-trend bottom fishing
3. **Tiered profit taking**: Adjust targets based on holding time, more flexible
4. **Modular code**: Uses reduce function to combine conditions, elegant code
5. **Official recommendation**: Suggests 60+ parallel trades, diversify risk

### ⚠️ Cons (Time to Roast)

1. **Stop loss too big**: 32.6% stop loss, is this scalping or long-term investing?
2. **Default parameters conservative**: Many buy conditions off by default, signals are pitifully few
3. **High complexity**: 50% more complex than original, increased learning cost
4. **More dependencies**: Need to install technical library
5. **Resampling delay**: 5-minute confirmation may miss quick reversals

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|----------------|--------|
| 📈 Uptrend | ✅ Highly recommended | 5-minute SMA filter, go with the trend |
| 🔄 Sideways ranging | ⚠️ Usable | Trend filter may miss some opportunities |
| 📉 Downtrend | ❌ Not recommended | SMA filter prevents buying |
| 🎢 High volatility | ⚠️ Cautious | False signals may increase |

---

## VII. Parameter Configuration Guide: How to Tune?

### 7.1 Buy Parameter Recommendations

```python
buy_params = {
    "mfi-value": 25,        # Slightly relax
    "fastd-value": 30,       # Slightly relax
    "fastk-value": 25,       # Slightly relax
    "adx-value": 25,         # Slightly relax
    "mfi-enabled": True,     # Turn ON!
    "fastd-enabled": True,   # Turn ON!
    "adx-enabled": False,    # Can leave off
    "fastk-enabled": True,   # Turn ON!
}
```

**Translation**: Default parameters are too strict, relax them a bit to increase signal count.

### 7.2 Sell Parameter Recommendations

```python
sell_params = {
    "sell-mfi-value": 80,    # Lower threshold, sell earlier
    "sell-fastd-value": 70,
    "sell-fastk-value": 75,
    "sell-adx-value": 25,    # Lower threshold
    # Keep others default
}
```

### 7.3 Stop Loss Recommendation

```python
stoploss = -0.15  # Change to 15%, much more reasonable than 32.6%
```

---

## VIII. Summary: How Good Is This Strategy?

### One-Sentence Review
> "Upgraded version of the original, added trend confirmation and parameterization, but stop loss setting is a bit ridiculous."

### Who Should Use It?
- ✅ Traders who need flexible configuration
- ✅ People who want trend filtering
- ✅ Quantitative players running multiple currency pairs in parallel
- ✅ People with time to study parameter optimization

### Who Should NOT Use It?
- ❌ People who like simple, plug-and-play solutions (too many parameters)
- ❌ Single currency pair players (need multi-currency diversification)
- ❌ People who don't want to tune parameters
- ❌ People pursuing ultimate simplicity

### My Suggestions

1. **Adjust stop loss**: Change 32.6% to 10-15%
2. **Turn on buy conditions**: All off by default, signals are pitifully few
3. **Multi-currency run**: Author suggests 60+ parallel, diversify risk
4. **Tiered ROI can be adjusted**: 8.2% is too high, can change to 3-5%

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Sniper with Telescope

StrategyScalpingFast2's money-making philosophy:

> **"Small timeframe execution, big timeframe confirmation"**

- **1-minute execution**: Quick reaction, capture short-term opportunities
- **5-minute confirmation**: Filter counter-trend signals, improve win rate
- **Parameterized control**: Adjust strategy based on market

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:------------|:-------|:--------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | "5-minute SMA filter makes me only buy uptrends, sweet!" |
| 🔄 Sideways ranging | ⭐⭐⭐⭐☆ | "Still works, but trend filter may miss some opportunities" |
| 📉 Downtrend | ⭐⭐☆☆☆ | "SMA filter prevents buying, but positions already bought may lose" |
| 🎢 High volatility | ⭐⭐☆☆☆ | "Too much noise, pile of false signals" |

**One-sentence summary**: Trending markets are my home turf, ranging markets I can still manage.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration | Recommended | Comment |
|---------------|-------------|---------|
| Number of pairs | 60+ | Author's suggestion! One loses, another gains |
| Pair type | Major coins | Good liquidity, less noise |
| Capital allocation | Equal distribution | Don't bet on just one |

### 10.2 Key Configuration File Settings

```yaml
# Stop loss (STRONGLY recommend adjusting!)
stoploss: -0.15  # Originally -0.326, too big

# Profit taking
minimal_roi:
  "0": 0.05    # 5% is reasonable
  "15": 0.03
  "30": 0.015
  "60": 0

# Timeframe
timeframe: 1m

# Buy parameters (recommend turning on more conditions)
buy_params:
  mfi-enabled: true
  fastk-enabled: true
  fastd-enabled: true
```

### 10.3 Hardware Requirements (Important!)

This strategy is more complex than original, and suggests multi-currency running:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|------------|
| 1-20 pairs | 2GB | 4GB | Okay |
| 20-60 pairs | 4GB | 8GB | Normal |
| 60+ pairs | 8GB | 16GB | Author's suggested config |

**Warning**: 60 trading pairs + resampling calculations, not enough memory will be very laggy!

### 10.4 Backtesting vs Live Trading

Author explicitly says:

> "We recommend running at least 60 parallel trades to cover inevitable losses"

**Translation**:
- Single trading pair may lose money
- Need diversified investment
- Capital must be sufficient

**Recommended Process**:
1. First backtest single trading pair
2. Find well-performing trading pairs
3. Small capital multi-currency test
4. Gradually increase position

**Don't run 60 pairs right away**, insufficient capital will get liquidated!

---

## XI. Bonus: Strategy Author's "Little Secrets"

Look carefully at the code, you'll find some interesting things:

1. **32.6% stop loss**
   > "I calculated, 32.6% stop loss has mystical significance... actually might just be an optimized number 😅"

2. **Tiered ROI time points**
   ```python
   "0": 0.082,    # 8.2%
   "18": 0.06,    # 18 minutes
   "51": 0.012,   # 51 minutes
   "123": 0       # 123 minutes
   ```
   > "These numbers look random, probably optimized from many backtests..."

3. **More sell conditions than buy**
   > "When buying I'm very cautious (default conditions all off), when selling I'm very aggressive (default conditions all on). What's the logic?"

4. **Depends on technical library**
   > "Need to install this library to use, don't forget!"

---

## XII. Final Words

### One-Sentence Review
> "Powerful parameterized scalping strategy, but needs tuning and sufficient capital support."

### Who Should Use It?
- ✅ Traders who want flexible configuration
- ✅ Multi-currency strategy players
- ✅ People willing to study parameter tuning
- ✅ Quantitative players with sufficient capital

### Who Should NOT Use It?
- ❌ People who like plug-and-play
- ❌ Small capital players (need 60+ parallel)
- ❌ People who don't want to learn tuning
- ❌ Single currency pair enthusiasts

### Manual Trader Advice

**Even more not recommended to manually replicate**! Reasons:

1. Too many parameters, manual adjustment is troublesome
2. Multi-timeframe needs simultaneous monitoring
3. Recommended to use quantitative platform for automated execution
4. 60+ trading pairs, manual will drive you crazy

---

## XIII. ⚠️ Risk Emphasis Again (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

StrategyScalpingFast2's historical backtesting may **perform very well** — but:

> **Because parameters can be optimized, it's easy to overfit historical data.**

Simply put: **Backtesting is a god, live trading is a ghost.**

### Multi-Currency Diversification Risks

Author suggests 60+ parallel trades, but:

- **High capital requirement**: 60 trading pairs, each needs certain position size
- **Complex management**: Monitoring 60 trading pairs' status
- **Correlation risk**: When market crashes, all pairs may fall together

### Parameter Optimization Trap

Configurable parameters look great, but:

- **Overfitting risk**: Optimized parameters only work on historical data
- **Future not guaranteed**: Today's optimal parameters may fail tomorrow
- **Need continuous monitoring**: Parameters may need periodic adjustment

### My Advice (Truth)

```
1. Change stop loss to 10-15%, don't use 32.6%
2. Turn on more buy conditions, increase signals
3. Lower ROI target, 3-5% is more realistic
4. Start with 10-20 trading pairs, don't do 60+ right away
5. Continuously monitor performance, adjust parameters timely
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it doesn't warn you first. Light position testing, survival is most important! 🙏

---

**Final Reminder**: This strategy is suitable for experienced quantitative traders, needs tuning ability and capital support. Beginners should start with simpler strategies to practice!