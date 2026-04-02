# BB_RPB_TSL_RNG Strategy: Streamlined "Oversold Catcher"

> **Nickname**: "Streamlined Swiss Army Knife"—removed 7 blades, kept only the sharpest 7
> **Profession**: Oversold capture expert + smooth stop loss bodyguard
> **Timeframe**: Works on 5-minute, watches BTC barometer

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_RNG** is a strategy that:
- Streamlined from 14 buy conditions to 7, keeping only core oversold logic
- Uses mathematical formula for stop loss, smoother than tiered stop loss
- Has a BTC barometer, pauses entry when market wind direction is wrong
- Can individually switch certain buy conditions on/off, flexible adjustment

Like **removing half the blades from a Swiss Army knife**, keeping only the most commonly used ones, traveling light 🗡️

---

## II. Core Configuration: Simply "Bottom Fishing + Smooth Stop Loss"

### Take-Profit Rules (ROI Table)

```
Target Profit: Auto take-profit at 10%
```

**Translation**: This strategy is more conservative than BIV1, takes profit at 10%. But in practice, still mainly relies on trailing stop loss to do the work.

### Stop Loss Rules: Calculated by Mathematical Formula!

```
Hard Stop Loss: -17.8% (used when profit below 1.9%)
Trailing Stop Loss: Higher profit = tighter stop loss (calculated by formula)
```

**Translation**: This strategy's stop loss is **calculated continuously by formula**, not tiered like BIV1:

| Profit | Stop Loss (Plain English) |
|------|---------------|
| 0% | -17.8% (hard stop loss as baseline) |
| 1.9% | 1.9% (start trailing) |
| 6.5% | 6.2% (tighter trailing) |
| 10% | 9.7% (profit difference continues to accumulate) |

**Mathematical Formula Translated to Human Language**:
- Profit between 1.9% ~ 6.5%: Stop loss smoothly transitions from 1.9% to 6.2%
- Profit exceeds 6.5%: Stop loss continues to rise with profit

**This is smoother than BIV1's tiered stop loss**, like continuously changing lanes on a highway, not braking in sections 🚗

---

## III. 7 Buy Conditions: I've Categorized Them for You

Compared to BIV1's 14 conditions, RNG version is streamlined to **3 major categories**:

### 🎯 Category 1: Bollinger Band Oversold Combination (1 condition)
**Core Logic**: Price breaks below Bollinger Band lower band + oversold indicator resonance

**In Plain English**:
> "Price has been beaten into the basement (breaks lower band), heart indicator (RMI), blood pressure indicator (CCI), breathing indicator (SRSI) all show it's done—time to enter and pick up the corpse!"

**Representative Condition**: is_BB_checked (dip + break combination)

**Feature**: **Can be individually switched!** Using `buy_is_dip_enabled` and `buy_is_break_enabled` parameters, can enable only dip or only break.

---

### 📉 Category 2: Trend Pullback Combination (4 conditions)
**Core Logic**: Capture pullback opportunities in uptrend

**In Plain English**:
> "Big brother (EMA) is standing upstairs, little brother (price) has been knocked downstairs—time to catch little brother, big brother will eventually pull him back up!"

**Representative Conditions**: is_local_uptrend, is_ewo, is_ewo_2, is_cofi

**Classic Lines**:
- `[ema_26 > ema_12]` → "Long moving average is higher than short, trend is up"
- `[EWO > -5.585]` → "Elliott Wave Oscillator shows trend is okay"

---

### 🌊 Category 3: Extreme Oversold Combination (2 conditions)
**Core Logic**: CTI, Williams %R at extreme values simultaneously

**In Plain English**:
> "Heart nearly stopped (CTI<-0.86), blood pressure exploded (Williams %R<-98)—this is the golden moment to pick up corpses!"

**Representative Conditions**: is_nfi_32, is_nfi_33

**Classic Lines**:
- `[cti < -0.86]` → "CTI dropped to -0.86, heartbeat nearly stopped"
- `[r_14 < -98]` → "Williams %R at -98, blood pressure at lowest point"

---

## IV. Protection Mechanisms: 2-Layer "Bodyguards"

Compared to BIV1's 3-layer bodyguards, RNG version is simplified to **2 layers**:

| Protection Type | Function | In Plain English |
|---------|------|--------|
| BTC Bodyguard | Pause buying when market crashes | "Watching BTC barometer, don't sacrifice yourself when big brother crashes" |
| Condition Switches | Can individually switch buy conditions | "Think a condition is too strict? Turn it off!" |

**Note**: RNG version **has no 1h information layer bodyguard**! This is its biggest difference from BIV1.

**Roast**: Without the 1h bodyguard, entry threshold is lower, more opportunities, but false signal risk is also higher 🤣

---

## V. Sell Logic: Calculated by Mathematical Formula

### 5.1 Smooth Trailing Stop Loss: Tighter as Profit Increases

```
Profit Range           Stop Loss Logic
──────────────────────────────────────────
<1.9%                  Hard stop loss -17.8%
1.9%~6.5%              Linear interpolation, transitions from 1.9% to 6.2%
>6.5%                  6.2% + (profit-6.5%)
```

**In Plain English**:
- **Profit < 1.9%**: Use hard stop loss, run only if it drops 17.8%—give enough rebound space
- **Profit 1.9%~6.5%**: Stop loss smoothly transitions from 1.9% to 6.2%—like a ramp, not stairs
- **Profit > 6.5%**: Stop loss rises with profit, the more you earn the tighter it locks

**Mathematical Formula (for those who want to see)**:
```python
# Linear interpolation between profit range PF_1 to PF_2
sl_profit = SL_1 + ((profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
```

---

### 5.2 Base Sell Signals

| Scenario | Trigger Condition | In Plain English |
|------|---------|--------|
| Trend Reversal | close>SMA9 + RSI>50 | "Price above short-term moving average, heart indicator returned to normal—time to run" |
| Price Deviation | SMA9 rising + close<HMA50 | "Short-term moving average rose but price fell back below HMA50—take profit while you can" |

---

## VI. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Simple and efficient**: Only 7 buy conditions, easier to understand than BIV1's 14
2. **Smooth stop loss**: Calculated by mathematical formula, stop loss value changes continuously, not tiered jumps
3. **Flexible switches**: Can individually switch dip/break conditions, adjust entry strictness
4. **Smaller computation load**: No 1h information layer, faster calculation than BIV1

### ⚠️ Weaknesses (Roast Session)

1. **Missing 1h bodyguard**: No big boss signature, higher false signal risk
2. **Complex stop loss formula**: Although smooth, 5 parameters are a bit difficult to tune
3. **BTC data dependency**: Needs BTC/USDT trading pair, strategy will error without BTC data
4. **Many Hyperopt parameters**: Although conditions are streamlined, still quite a few parameters

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| Oscillating decline | ✅ Use as main strategy | Oversold capture mechanism matches this market |
| Moderate trend | ⚠️ Use cautiously | Pullback opportunities might miss main rally |
| Crash market | ❌ BTC protection pauses | Strategy auto-stops when market crashes |
| High volatility oscillation | ⚠️ Switch partial conditions | Can reduce entry frequency through condition switches |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "Streamlined version of BIV1—removed half the blades, traveling light, but missing big boss signature"

### Who Is It Suitable For?
- ✅ Quantitative players who like simple strategies
- ✅ People who understand linear interpolation stop loss mathematics
- ✅ Live trading players with BTC/USDT data support
- ✅ Bottom-fishing enthusiasts in oscillating markets

### Who Is It NOT Suitable For?
- ❌ People who like multi-layer validation—missing 1h bodyguard
- ❌ Players who don't understand mathematical formulas—stop loss is calculated
- ❌ Environments without BTC data—will error
- ❌ Strong trend chasers—this is a bottom-fishing strategy

### My Suggestions
1. **Understand stop loss formula**: Figure out the relationship between pHSL, pPF_1, pSL_1 these parameters
2. **Coordinate with BTC data**: Ensure you have BTC/USDT trading pair data
3. **Try condition switches**: Can try turning off a condition, see the effect
4. **Small position testing**: Less 1h validation, entry might be more frequent, test first

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using Streamlining to Build a "Fast Attack Team"

BB_RPB_TSL_RNG's profit philosophy: **Streamlined bottom fishing + Smooth stop loss = Fast response**

- **Streamlined conditions**: 7 core buy conditions, not 14, faster entry judgment
- **Smooth stop loss**: Calculated by mathematical formula, not tiered, smoother transition
- **BTC barometer**: Watching big brother (BTC) movements, pause when wind direction is wrong
- **Flexible switches**: Can adjust entry conditions, adapt to different market sensitivity

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Strong uptrend | ⭐⭐☆☆☆ | Price keeps rising, no pullback opportunities—strategy stands there dumbly waiting for oversold, misses main rally |
| 🔄 Oscillating decline | ⭐⭐⭐⭐⭐ | Price drops back and forth, lots of oversold opportunities—strategy bottom-fishes happily |
| 📉 Continuous crash | ⭐⭐☆☆☆ | BTC bodyguard pauses entry—strategy says "big brother crashed, I'm not doing it" |
| ⚡️ High volatility oscillation | ⭐⭐⭐☆☆ | Condition switches can adjust sensitivity—flexible response |

**One-sentence summary**: Oscillating decline is home court, strong trend is blind spot. Compared to BIV1, faster entry judgment, but missing big boss validation.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Roast |
|--------|--------|------|
| Number of trading pairs | 10-30 | No 1h calculation, can run a few more than BIV1 |
| Trading pair selection | High volatility coins | Calm coins have no oversold opportunities |
| BTC data | Must have BTC/USDT | Strategy will error without BTC data! |

### 10.2 Configuration File Key Settings

```yaml
# Stop loss parameters (core)
pHSL: -0.178      # Hard stop loss
pPF_1: 0.019      # Profit threshold 1
pSL_1: 0.019      # Stop loss value 1
pPF_2: 0.065      # Profit threshold 2
pSL_2: 0.062      # Stop loss value 2

# Condition switches
buy_is_dip_enabled: true
buy_is_break_enabled: true
```

### 10.3 Hardware Requirements

This strategy has smaller computation load than BIV1 (no 1h information layer), more friendly to hardware:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 10-20 pairs | 4GB | 8GB | Normal |
| 50+ pairs | 8GB | 12GB | Light and fast |

**Good news**: Runs faster than BIV1, old computers can handle it!

### 10.4 Backtest vs Live Trading

**Backtest might be good**: 7 conditions, dozens of parameters, might be easier to tune than 14 conditions.

**Live trading potential issues**:
- **BTC protection triggers**: Might pause entry when BTC fluctuates
- **Stop loss parameter sensitivity**: 5 stop loss parameters, might be too tight or loose if not tuned well
- **No 1h validation**: Might have more entry signals than BIV1, but also more false signals

**Suggested Process**:
1. Backtest first to see effect
2. Understand stop loss formula parameters
3. Small position test (10% capital)
4. Observe if entry frequency is reasonable

---

## XI. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Condition Switch Design**
   > `buy_is_dip_enabled` and `buy_is_break_enabled` use `CategoricalParameter`
   > "Author designed them to be individually switchable, shows he also knows 14 conditions might be too many"

2. **Stop Loss Parameter Naming**
   > pHSL, pPF_1, pSL_1, pPF_2, pSL_2
   > "Parameters start with p, might be abbreviation for Profit, clearly expressing profit-related"

3. **BTC Protection Comments**
   > `# BTC info` has `# BTC 5m dump protection` and `# BTC 1d dump protection` below
   > "Author designed two time dimension BTC protections: 5-minute and 1-day"

---

## XII. Last But Not Least

### One-Sentence Evaluation
> "Streamlined version of BIV1—missing big boss validation, faster entry judgment, but need to be alert to false signals"

### Who Is It Suitable For?
- ✅ People who like simple strategies
- ✅ Players who understand mathematical formula stop loss
- ✅ Live trading environments with BTC data
- ✅ Traders pursuing fast response

### Who Is It NOT Suitable For?
- ❌ Conservative players who like multi-layer validation
- ❌ People who don't understand linear interpolation
- ❌ Environments without BTC data
- ❌ Strong trend chasers

### Manual Trader Suggestions
Don't directly imitate this strategy for manual trading! Stop loss is calculated by formula, you'll die of exhaustion calculating manually. Just understand its approach:
- Streamline buy conditions, keep only core logic
- Stop loss uses mathematical formula for smooth transition, not tiered jumps
- Pause when BTC wind direction is wrong

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtest Is Beautiful, Be Cautious in Live Trading

BB_RPB_TSL_RNG's backtest might be good—but there's a trap:

> **Although conditions are streamlined, 5 stop loss parameters + multiple buy parameters can still "fit" historical optimal solution.**

Simply put: **Streamlined doesn't mean safe, parameter tuning still needs caution**

### RNG Version's Hidden Risks

Compared to BIV1, RNG has unique risks:
- **No 1h validation**: Might have more entry signals, but false signal risk is higher
- **Stop loss formula sensitivity**: These 5 parameters pHSL, pPF_1, pSL_1, pPF_2, pSL_2—if not tuned well, stop loss might be too tight or too loose
- **BTC data dependency**: If exchange doesn't have BTC/USDT data, strategy will error

### My Suggestions (Honest Words)

```
1. Understand stop loss formula: Figure out how 5 parameters calculate stop loss value
2. Coordinate with BTC data: Ensure environment has BTC/USDT trading pair
3. Try condition switches: Turn off partial conditions to test effect
4. Start with small positions: Less 1h validation, entry might be more frequent, test small first
```

**Remember**: Streamlined doesn't mean simple, understand the stop loss formula thoroughly before playing. Light position testing, staying alive is most important! 🙏
