# CombinedBinHAndClucHyperV0 Strategy: The Hyperparameter-Optimized "Twin Swords Combined"

> **Nickname**: Super Evolved Twin Swords Combined
> **Profession**: 1-Minute High-Frequency Trading + Hyperparameter Optimization Player
> **Feature**: 12 parameters to tweak — you brave enough?

---

## 1. What's This Strategy?

**CombinedBinHAndClucHyperV0** literally means "Combined Bollinger Bands and Cluc Hyperparameter Optimized Version V0."

Simply put:
- Two old strategies **BinHV45** and **ClucMay72018** forcibly merged together
- Whichever one says buy, you listen (OR gate logic)
- **Here's the key**: This is a "super evolved version" with 12 parameters you can freely adjust!
- Timeframe is **1 minute**, "fast"!

Think of it as a general with two super military advisors: "Advisor A says buy, buy! Advisor B says buy, also buy! And I can adjust their judgment standards based on market conditions anytime!" 🧙‍♂️⚡

---

## 2. Core Settings: So Many Parameters Your Scalp Will Tingle

### Take-Profit Rules (Staged)
```
At 0 minutes:    Make 10%? → Run!
After 30 mins:  Make 5%? → Run!
After 60 mins:  Make 2%? → Run!
```
**Plain English**: High bar initially (10%), lower requirement as time passes (2%) — time space!

### Stop-Loss Rules
```
Lose 10%? → Cut!
```
**Plain English**: Allowing 10% loss, giving you enough rope!

### Trailing Stop
```
Activates after profit exceeds 0.8%
```
**Plain English**: Don't celebrate too early after making money — if profit drops below 0.8%, run!

### Adjustable Parameters (12!)

| Parameter | Default | Meaning |
|-----------|---------|---------|
| buy_a_bbdelta_rate | 0.016 | How wide BB must be to buy |
| buy_a_closedelta_rate | 0.0088 | How big the fluctuation must be to buy |
| buy_a_tail_rate | 0.9 | How short the wick must be to buy |
| buy_a_time_window | 21 | How many days to look at for BB |
| buy_a_min_sell_rate | 1.03 | Sell safety cushion |
| buy_b_close_rate | 0.979 | How far from BB lower band to buy |
| buy_b_ema_slow | 50 | How many days to look at for MA |
| buy_b_time_window | 20 | BB period |
| buy_b_volume_mean_slow_window | 30 | How many days to look at for volume MA |
| buy_b_volume_mean_slow_num | 20 | How many times volume shrinks |
| sell_bb_middleband_window | 91 | How many days to look at for BB to sell |
| sell_trailing_stop_positive_offset | 0.008 | Trailing stop trigger point |

**Plain English**: This is why it's called Hyper (hyperparameter optimization) version — so many parameters you can't even remember them all! 😅

---

## 3. Entry Conditions: 2 Modes, Either One Works

This strategy has two buy modes — buy when either is satisfied:

### 🎯 Mode 1: BinHV45 (Hammer Pattern Plus)

**Trigger Conditions** (optimized version):
1. BB width wide enough (> 1.6% of close)
2. Price fluctuation large enough (> 0.88% of close)
3. Lower wick short (< 90% of width)
4. **Close breaks below BB lower band**
5. **Close lower than previous**
6. BB middle band above 1.03× close

**Plain English**:
> "Price dropped below BB, and it's a hammer pattern (short lower wick), plus BB middle band is supporting above — isn't this stable? Buy it!"

### 🎯 Mode 2: ClucMay72018 (Shrinking Volume Rebound Plus)

**Trigger Conditions** (optimized version):
1. Price below EMA50
2. Price < 97.9% of BB lower band
3. **Volume extremely low** (< 1/20th of average)

**Plain English**:
> "Price dropped below BB, nobody's trading (ground volume), isn't this abnormal? Buy it!"

**Summary**: Both modes essentially say the same thing — "Price dropped below BB, might rebound!"

---

## 4. Protection Mechanisms: Triple Protection

This strategy's protection is relatively comprehensive:

| Protection Type | Trigger | Plain English |
|----------------|---------|---------------|
| **Hard Stop-Loss** | Lose 10% | "Lost 10%, don't hold, bail out!" |
| **ROI Take-Profit** | Make 10%/5%/2% | "Exit in stages, don't be greedy!" |
| **Trailing Stop** | Profit exceeds 0.8% | "Made money, don't give it back, activate protection!" |

**Plain English**: Triple protection — you scared yet! 😅

---

## 5. Exit Logic: Multiple Options

### Technical Sell: Breaking BB Middle Band

```python
Price > BB middle band (91-day MA)
```

**Plain English**:
> "Price rose to BB middle band, transitioned from downtrend to consolidation — run!"

### Other Exit Options

| Exit Type | Trigger |
|-----------|---------|
| **ROI Take-Profit** | 10% (immediate) / 5% (after 30 mins) / 2% (after 60 mins) |
| **Trailing Stop** | Profit drops below 0.8% |
| **Stop-Loss** | Lose 10% |

**Plain English**: So many exit options, can't remember? My advice — just remember "run"! 🏃‍♂️

---

## 6. Strategy "Personality"

### Personality Analysis

| Trait | Description |
|-------|-------------|
| **Aggressive** | 1-minute level itself is high-frequency aggressive |
| **Greedy** | Doesn't run until 10%, has big appetite |
| **Cautious** | Doesn't cut until 10%, gives opportunities |
| **Flexible** | 12 parameters adjustable, adaptable |
| **Complex** | Two systems superimposed, many parameters |

### Who's It For?

- ✅ People who like high-frequency trading
- ✅ People with Hyperopt optimization experience
- ✅ People who can accept 10% stop-loss
- ✅ People with low trading fees (high-frequency needs!)
- ❌ Beginner newcomers (too many parameters will overwhelm)
- ❌ People with high fees (1-minute level gets eaten by fees)
- ❌ People who like long-term holding

---

## 7. Applicable Scenarios

### ✅ Recommended Scenarios

1. **High-Frequency Trading**: Just playing 1-minute level
2. **High-Volatility Markets**: Many opportunities when price jumps around
3. **Parameter Optimization**: Want to find optimal parameters via Hyperopt
4. **Multi-Coin Allocation**: Run multiple pairs simultaneously
5. **Strategy Combination**: Use with other strategies

### ❌ Not Recommended Scenarios

1. **High Fees**: 1-minute level trades too frequently, fees hurt
2. **Low-Volatility Markets**: 1 minute with no movement = watching a show
3. **Unilateral Uptrend**: May miss rally
4. **Unilateral Downtrend**: Easily stopped out

---

## 8. Summary

**CombinedBinHAndClucHyperV0** = **BinHV45 + ClucMay72018 + 12 Adjustable Parameters**

| Item | Value |
|------|-------|
| **Buy Modes** | 2 (either one) |
| **Adjustable Parameters** | 12 |
| **Take-Profit** | 10%/5%/2% staged |
| **Stop-Loss** | 10% |
| **Trailing Stop** | 0.8% activation |
| **Timeframe** | 1 Minute |
| **Complexity** | ⭐⭐⭐⭐ (Complex) |

**One-Line**: Two strategies combined + 12 parameters to adjust = 1-minute high-frequency trading nuclear weapon! But — you gotta know how to tune parameters! 😅

---

## 9. Market Performance

### Ideal Situations

- ✅ Excellent performance in high-volatility markets
- ✅ Captured effective hammer patterns
- ✅ Rebounded after shrinking volume
- ✅ Found best configuration after parameter optimization

### Not Ideal Situations

- ❌ High fees eat all profits
- ❌ May get stopped out consecutively in unilateral downtrends
- ❌ False breakouts happen
- ❌ Parameter optimization overfits historical data

---

## 10. Configuration Suggestions

### Beginner Suggestions (Conservative Configuration)

```python
# Don't tweak parameters first, use defaults
minimal_roi = {"0": 0.05, "30": 0.03}  # Lower expectations
stoploss = -0.08           # Cut at 8%
trailing_stop_positive_offset = 0.005  # Activate trailing earlier
max_open_trades = 1        # Only play 1
```

**Plain English**: Beginners, don't tweak parameters — use defaults! Otherwise you'll die without knowing how! 😅

### Veteran Configuration (Aggressive)

```python
# After Hyperopt optimization
minimal_roi = {"0": 0.15, "60": 0.08}  # Higher targets
stoploss = -0.12           # Cut at 12%
trailing_stop_positive_offset = 0.015  # Give more room
max_open_trades = 3        # Play 3
```

**Plain English**: Veterans go wild, but remember to run Hyperopt!

### My Suggestions

1. **Don't tweak parameters first**: Run with defaults for a while
2. **Use Hyperopt**: Run hundreds of rounds to find optimal parameters
3. **Start with small position**: Try with pocket change first
4. **Watch fees**: Fee over 0.2%? Don't play
5. **Review regularly**: Check strategy performance weekly
6. **Don't over-optimize**: Don't tune parameters too "perfect" — or you'll crash!

---

## 11. Bonus

### Strategy Founder

This strategy was written by **iterativ**, a quantitative player who likes combining multiple strategies and tweaking parameters.

### Strategy Evolution

| Version | Characteristics |
|---------|----------------|
| Basic Version | CombinedBinHAndCluc |
| V7 | Added more modes |
| HyperV0 | Hyperparameter optimized version (this article) |
| HyperV3 | Higher version of optimization |

### What's Special About This Version?

1. **12 Adjustable Parameters**: This is the signature of the Hyper version
2. **1-Minute Level**: More aggressive than 5 minutes
3. **Custom Stop-Loss**: Considers slippage, more precise
4. **Trailing Stop**: Let profits run

### Fun Facts

- 1-minute backtesting needs lots of data to be reliable
- One round of Hyperopt can take hours to days
- Not more parameters = better — easy to overfit!

---

## 12. The Bottom Line

**Mindset When Using This Strategy**:

1. **Don't randomly tweak parameters**: Beginners use defaults, veterans use Hyperopt
2. **Watch fees**: 1-minute level is extremely sensitive to fees!
3. **Don't be greedy**: 10% and run, don't dream of overnight riches
4. **Don't fear losses**: 10% stop-loss is normal loss
5. **Don't slack**: Review regularly, check strategy performance

**Remember**: High-frequency strategy + random parameter tweaking = losing money! 🤑

---

## ⚠️ Risk Reminder

### Main Risks

| Risk | Likelihood | Consequence |
|------|-----------|-------------|
| **Fees Eat Profits** | Extremely High | The fatal wound of high-frequency trading |
| **Consecutive Stop-Outs** | Medium | Account drawdown |
| **Parameter Overfitting** | High | Perfect backtest, poor live |
| **False Breakout** | High | Bought at the top |
| **Missing Rally** | Medium | Missed profit |

### Risk Control Suggestions

1. **Check fees first**: Abandon exchanges with fees over 0.15%
2. **Use default parameters**: Beginners don't tweak, wait until familiar
3. **Don't over-optimize**: Hyperopt parameters may just be "historically optimal"
4. **Set stop-loss**: Don't be sentimental, cut at 10%
5. **Diversify investment**: Don't full-position one coin
6. **Paper trade**: Run months of paper trading before live
7. **Watch the market**: Good in bull markets, careful in bear markets
8. **Review regularly**: Check monthly strategy performance

### Most Important One Line

> **High-frequency strategy plays execution, not parameters!**
> **Fees are your biggest enemy!**
> **Learn to respect the market, learn to accept losses.**

---

**Happy trading everyone! Remember: Stay steady, we can win!** 🚀💰

---

**Appendix: Default Parameters (For Reference)**

```python
buy_params = {
    'buy_a_bbdelta_rate': 0.0160,
    'buy_a_closedelta_rate': 0.0088,
    'buy_a_tail_rate': 0.9,
    'buy_a_time_window': 21,
    'buy_a_min_sell_rate': 1.03,
    'buy_b_close_rate': 0.979,
    'buy_b_time_window': 20,
    'buy_b_ema_slow': 50,
    'buy_b_volume_mean_slow_num': 20,
    'buy_b_volume_mean_slow_window': 30,
}

sell_params = {
    'sell_bb_middleband_window': 91,
    "sell_trailing_stop_positive_offset": 0.008,
}
```
