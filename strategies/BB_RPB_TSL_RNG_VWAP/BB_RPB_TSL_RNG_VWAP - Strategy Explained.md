# BB_RPB_TSL_RNG_VWAP Strategy: The "Smart Bottom Fisher" with Volume-Weighted Price Support

> **Nickname**: VWAP Bottom Fishing Master  
> **Profession**: Bollinger Band Pullback Hunter + VWAP Support Tracker  
> **Timeframe**: 5 minutes (5m)

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_RNG_VWAP** is a strategy that:
- Specializes in "picking up bargains" at both Bollinger Band lower rail AND VWAP lower rail
- Judges real support based on volume-weighted price
- Uses "VIP-exclusive stoploss" for trades entered via VWAP

Like a shrewd stock buyer: doesn't just look at where price dropped to (Bollinger Band), also looks at where volume support is (VWAP)—measures with two rulers, and got a VIP stoploss package for VWAP entries 🤣

---

## II. Core Configuration: Simply Put, "Dual Support Entry + VIP Stoploss"

### Take-Profit Rules (ROI Table)

```
0 minutes  → 10%
30 minutes → 5%
60 minutes → 2%
```

**Translation**:
- Just bought target 10%, but mainly relies on stoploss
- After holding 30 minutes, drop target to 5% (don't be greedy)
- After holding 60 minutes, drop target to 2% (take profits when you see them)

### Stoploss Rules (Dual-Layer Configuration)

```
Regular Stoploss (other entries):
  Profit < 1.9%  → Hard stoploss -25% (run if losing too much)
  1.9%-6.5%     → Tiered stoploss
  Profit > 6.5%  → Trailing stoploss

VIP Stoploss (VWAP entries):
  Profit < 1%    → Hard stoploss -25%
  1%-5%         → Tiered stoploss (looser)
  Profit > 5%    → Trailing stoploss
```

**Translation**:
- **Regular Entry**: Strict management school, only starts relaxing stoploss after earning 1.9%
- **VWAP Entry (VIP)**: Loose supervision, starts relaxing after earning 1%, gives VWAP entries more volatility space

---

## III. 8 Buy Conditions: I've Categorized Them for You

This strategy has many fancy buy conditions, I've grouped them into 4 categories:

### 🎯 Category 1: Bollinger Band Pullback Group (1 condition)

**Core Logic**: Price drops to Bollinger Band bottom, and drops deep enough

**In Plain English**:
> "Boss, this price has dropped to the Bollinger Band basement (triple lower band), and all kinds of oversold indicators are flashing red—time to bottom fish, right?"

**Representative Condition**: Condition #1 `is_BB_checked`

Same as BB_RPB_TSL_RNG_TBS_GOLD, won't repeat 👆

---

### 📊 Category 2: Trend Pullback Group (2 conditions)

**Core Logic**: Big trend is upward, but price pulls back to low levels

**In Plain English**:
> "The big trend is clearly upward, price suddenly dropped back—isn't this a 'pullback within the trend'? Get on board quick!"

Same as BB_RPB_TSL_RNG_TBS_GOLD, won't repeat 👆

---

### 🔄 Category 3: Indicator Cross Group (3 conditions)

**Core Logic**: Various indicator golden crosses/oversold triggers entry

**In Plain English**:
> "Indicators are 'holding a meeting to vote', reach consensus and buy!"

Same as BB_RPB_TSL_RNG_TBS_GOLD, won't repeat 👆

---

### 🆕 Category 4: VWAP Support Group (1 condition) — This Is New!

**Core Logic**: Price breaks below volume-weighted support line, and dropped enough from high

**In Plain English**:
> "Boss, price broke below VWAP lower rail! This isn't ordinary support, this is **volume-weighted support**—means real buying and selling power all agree on this price! And price dropped more than 4% from recent high, really cheap!"

**Representative Condition**: Condition #8 `is_vwap`

**Classic Lines**:
- `close < vwap_low` → "Price broke below VWAP lower rail, volume-weighted support broken"
- `tcp_percent_4 > 0.04` → "Dropped more than 4% from recent 4-period high, really cheap"
- `cti < -0.8` → "CTI says 'oversold'"
- `rsi < 35` → "RSI also oversold"
- `rsi_84 < 60` → "84-period RSI normal, medium-term not overheated"
- `rsi_112 < 60` → "112-period RSI also normal, overall trend healthy"

**What Is VWAP? Simply Put**:
> VWAP = Volume Weighted Average Price
> 
> Not just a simple average price, but a "real average price" calculated by weighting each trade by volume. Big traders all watch this indicator!

---

## IV. VIP Stoploss: VWAP Entry's "Exclusive Package"

### 4.1 Why Does VWAP Need VIP Stoploss?

**In Plain English**:
> "VWAP entry is based on volume judgment, may experience bigger volatility than Bollinger Band entry—because VWAP also changes when volume changes. So give VWAP entries a VIP package, stoploss is looser!"

### 4.2 VIP Stoploss Parameter Comparison

| Parameter | Regular Entry | VWAP Entry (VIP) | Difference |
|------|---------|-----------------|------|
| Tier 1 Trigger | 1.9% | **1%** | Relax earlier |
| Tier 1 Stoploss | 1.9% | **1%** | Looser |
| Tier 2 Trigger | 6.5% | **5%** | Enter trailing earlier |
| Tier 2 Stoploss | 6.2% | **4.2%** | Looser |

**Plain English Summary**:
> "VWAP entry starts relaxing stoploss after earning 1%, regular entry needs to earn 1.9%—VIP treatment!"

---

## V. Long-Period RSI: This Strategy's "Foresight"

### 5.1 Added Two Long-Period RSI

This strategy has two more "foresight" indicators than the regular version:

| Indicator | Period | Usage |
|------|------|------|
| rsi_84 | 84 periods (about 7 hours) | Medium-term trend judgment |
| rsi_112 | 112 periods (about 9.3 hours) | Long-term trend judgment |

### 5.2 How Used in VWAP Conditions?

```python
rsi_84 < 60  → "Medium-term RSI not overheated"
rsi_112 < 60 → "Long-term RSI also not overheated"
```

**In Plain English**:
> "Short-term RSI oversold (<35) can buy, but medium-term and long-term RSI need to be normal (<60)—ensure you're not buying at the 'mountain top', but at the 'mountain middle' or 'mountain foot'!"

---

## VI. Sell Logic: Similar to Regular Version, But Added VIP Package

### 6.1 Three-Layer Stoploss (Regular)

Same as BB_RPB_TSL_RNG_TBS_GOLD, won't repeat 👆

### 6.2 VIP Stoploss (VWAP Entry)

```
Profit Range         VIP Stoploss          Plain English
──────────────────────────────────────────
< 1%                Hard stoploss -25%    "强制 stoploss if losing too much"
1%-5%               Tiered stoploss       "VIP loose supervision"
> 5%                Trailing stoploss     "VIP chases profit"
```

### 6.3 Base Sell Signals

Same as BB_RPB_TSL_RNG_TBS_GOLD, won't repeat 👆

---

## VII. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **VWAP Support Judgment**: Based on volume-weighted real support, more "grounded" than Bollinger Band
2. **VIP Stoploss Package**: VWAP entries use independent stoploss parameters, more refined risk management
3. **Long-Period Foresight**: RSI 84/112 judge long-term trend, avoid buying at mountain top
4. **Compatible with Backtest**: Unlike trailing buy version, this strategy is fully compatible with backtest!

### ⚠️ Weaknesses (Complaint Session)

1. **VWAP Computational Overhead**: Rolling VWAP + standard deviation, computational load bigger than regular version
2. **VWAP Entry Strict**: Conditions are harsh (tcp_percent_4 > 0.04), may trigger less frequently
3. **Depends on Volume**: VWAP inaccurate when volume is low
4. **Dual-Layer Stoploss Complex**: Regular stoploss + VIP stoploss, configuration maintenance more troublesome

---

## VIII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Operation | Reason |
|---------|---------|------|
| 📈 Oscillating Uptrend (Active Volume) | ✅ Use full power | VWAP most accurate when volume is active |
| 📊 Sideways Oscillation (Normal Volume) | ✅ Can use | Bollinger Band pullback effective |
| 📉 Single-Side Downtrend | ❌ Don't use | Buy signals trigger frequently but price keeps dropping |
| ⚡ High Volatility | ⚠️ VWAP stoploss looser | VIP stoploss can withstand large volatility |
| 💤 Low Volume | ❌ VWAP invalid | VWAP depends on volume, inaccurate when volume low |

---

## IX. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "Bollinger Band Bottom Fishing + VWAP Support + VIP Stoploss = Smart Buyer in Active Volume Markets"

### Who Should Use It?
- ✅ Active volume market traders
- ✅ People who want to use VWAP support judgment
- ✅ Users who need refined stoploss configuration
- ✅ Oscillating uptrend market enthusiasts

### Who Shouldn't Use It?
- ❌ Low volume market traders (VWAP invalid)
- ❌ People who don't want to manage complex stoploss configurations
- ❌ Single-side downtrend market traders
- ❌ Newbie whites

### My Suggestions
1. **Only use VWAP when volume is active**: VWAP conditions may be inaccurate when volume is low
2. **Understand VIP stoploss logic**: VWAP entries and regular entries use different stoploss parameters
3. **Oscillating uptrend is best**: Dual support (Bollinger Band + VWAP) most effective in trend pullbacks
4. **Backtest usable**: Unlike trailing buy version, this strategy is fully compatible with backtest

---

## X. What Markets Can This Strategy Make Money In?

### 10.1 Core Logic: Dual Support Entry + VIP Stoploss

BB_RPB_TSL_RNG_VWAP is a Bollinger Band pullback + VWAP support hybrid strategy. Code volume 600+ lines, even more complex than trailing buy version 📚

**Its money-making philosophy**: Measure price with two rulers (Bollinger Band + VWAP), use VIP stoploss to give VWAP entries more space

- **Bollinger Band Pullback**: Look at where price dropped to (technical analysis)
- **VWAP Support**: Look at where volume-weighted price is (real support)
- **VIP Stoploss**: Give VWAP entries looser stoploss space
- **Long-Period RSI**: Ensure not buying at mountain top

### 10.2 Different Market Performance (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Oscillating Uptrend (Active Volume) | ⭐⭐⭐⭐⭐ | Perfect match, dual support entry most effective |
| 📊 Sideways Oscillation (Normal Volume) | ⭐⭐⭐⭐☆ | Bollinger Band pullback effective, VWAP may trigger |
| 📉 Single-Side Downtrend | ⭐☆☆☆☆ | Buy signals trigger frequently, stoploss won't stop |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | VIP stoploss looser, can withstand large volatility |
| 💤 Low Volume | ⭐⭐☆☆☆ | VWAP inaccurate, VIP stoploss also useless |

**One-Sentence Summary**:
> "Make money in oscillating uptrend markets with active volume, VWAP invalid when volume is low"

---

## XI. Want to Run This Strategy? Check These Configurations First

### 11.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Complaint |
|--------|--------|------|
| timeframe | 5m | 5 minutes enough to capture pullbacks |
| startup_candle_count | 120 | Need enough historical data |
| BTC data | BTC/USDT 5m | Fixed configuration, needs BTC data |

### 11.2 VIP Stoploss Configuration

```yaml
# VWAP Entry Exclusive Stoploss Parameters
VWAP_PF_1: 0.01   # Tier 1 trigger (earlier)
VWAP_SL_1: 0.01   # Tier 1 stoploss (looser)
VWAP_PF_2: 0.05   # Tier 2 trigger (earlier)
VWAP_SL_2: 0.042  # Tier 2 stoploss (looser)
```

### 11.3 Hardware Requirements (Important!)

This strategy has large computational load (VWAP rolling calculation), has requirements for VPS memory:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 1-20 pairs | 4GB | 8GB | Normal |
| 20-50 pairs | 8GB | 16GB | Smooth |
| 50+ pairs | 16GB | 32GB | Stable |

**Warning**: VWAP computational overhead bigger than regular version, insufficient memory may cause calculation delays 😅

### 11.4 Backtest vs Live Trading

**Good News**: This strategy is fully compatible with backtest!

```
Backtest → Same logic as live trading, VWAP conditions effective
Live Trading → Same logic as backtest
```

**Suggested Process**:
1. Backtest to verify strategy logic
2. Choose trading pairs with active volume
3. Demo test VIP stoploss effects
4. Small position live trading verification
5. Gradually increase position

---

## XII. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll discover some interesting things:

1. **VWAP stoploss is "hard-coded"**:
   > "VWAP stoploss parameters aren't Hyperopt parameters, directly written in custom_stoploss—shows author has own views on VWAP stoploss"

2. **Long-period RSI only used once**:
   > "RSI 84/112 only used in VWAP conditions, not used in other conditions—shows VWAP conditions need 'foresight'"

3. **top_percent_change is author's custom function**:
   > "tcp_percent_4 > 0.04 → 'Price dropped more than 4% from recent 4-period high'—this is author's 'custom indicator'"

4. **BTC protection fixed to BTC/USDT**:
   > "Unlike regular version that auto-judges stake_currency, here fixed to BTC/USDT—maybe author only does USDT-denominated trading"

---

## XIII. Last But Not Least

### One-Sentence Evaluation
> "Dual Support Bottom Fishing + VIP Stoploss = Smart Buyer in Active Volume Markets"

### Who Should Use It?
- ✅ Active volume market traders
- ✅ People who want to use VWAP support judgment
- ✅ Oscillating uptrend market enthusiasts
- ✅ Users who need refined stoploss configuration
- ✅ Users who can do backtest analysis (fully compatible)

### Who Shouldn't Use It?
- ❌ Low volume market traders
- ❌ People who don't want to manage complex stoploss
- ❌ Single-side downtrend market traders
- ❌ Newbie whites

### Manual Trader Suggestions
If you want to borrow from this strategy for manual trading:
- VWAP support judgment worth learning (volume-weighted price)
- VIP stoploss's "give VWAP entries more space" thinking can be borrowed
- Long-period RSI method for judging long-term trend state is very useful
- But monitoring 8 conditions manually is too tiring, recommend simplifying

---

## XIV. ⚠️ Risk Re-emphasis (Must Read This Section)

### VWAP Depends on Volume!

BB_RPB_TSL_RNG_VWAP's VWAP conditions **depend on volume**:

> **When volume is low, VWAP calculation is inaccurate, VWAP conditions may fail.**

Simply put: **When no one is trading, volume-weighted price can't be calculated, VWAP support judgment is unreliable!**

### Hidden Risks of Complex Strategies

In live trading, dual-layer stoploss configuration may cause:
- **VIP stoploss trigger confusion**: Buy tag judgment logic complex, may misjudge
- **VWAP conditions trigger rarely**: tcp_percent_4 > 0.04 condition is strict, triggers less frequently
- **Calculation delay**: VWAP rolling calculation overhead large, signals may delay
- **Long-period RSI data insufficient**: startup_candle_count set too low will cause RSI 112 inaccurate

### My Suggestions (Truth)

```
1. Choose trading pairs with active volume, don't use VWAP on coins with low volume
2. Check VWAP condition trigger frequency in backtest, don't use if too low
3. Understand VIP stoploss logic, buy tag judgment needs to be accurate
4. Set startup_candle_count to 120 or above, ensure long-period RSI has enough data
5. Start with small positions, don't go all-in right away
```

**Remember**: VWAP is a good indicator, but depends on volume! When no one is trading, VWAP is just decoration! 🙏

---

**Final Reminder**: No matter how good the strategy, the market won't say hello when teaching you a lesson. Light position testing, staying alive is most important! 🙏
