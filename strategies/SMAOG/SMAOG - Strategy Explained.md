# SMAOG Strategy: The "Three-Layer Bulletproof Vest" Upgraded Dip-Buyer

> **Nickname**: Bulletproof Dip-Buyer, OG Veteran
> **Occupation**: Steady dip-buyer with three layers of protection
> **Timeframe**: 5 minutes (suitable for day trading)

---

## I. What Is This Strategy?

Simply put, **SMAOG** is a strategy that:
- Added "three layers of bulletproof vest" on top of SMAIP3v2
- More "picky" when selling, only sells when momentum weakens
- Uses "progressive take-profit," the longer you hold, the lower the target

Like an "enhanced version" of SMAIP3v2, wearing three more layers of bulletproof vests, more cautious when buying dips, smarter when selling 🛡️

---

## II. Core Configuration: Basically "Run When You've Made Enough"

### Take-Profit Rules (ROI Table)

```
Just entered       → Run when 10% profit
After 30 minutes   → Run when 5% profit
After 60 minutes   → Run when 2% profit
```

**Translation**: Target is high when just entering (10%), but gets more "impatient" over time, eventually running at 2%. This design is pretty smart - don't let capital get locked up too long.

### Stop Loss Rules

```
Lose 23% → Admit defeat and exit
Profit reaches 2% → Start trailing stop, pull back 0.5% and run
```

**Translation**:
- Stop loss same as SMAIP3v2, quite "generous"
- But trailing stop is more sensitive (0.5% vs SMAIP3v2's 0.3%), locks in profits faster

---

## III. 1 Buy Condition: But Protection Is Thick

This strategy also has 1 buy signal, but more protection mechanisms:

### 🎯 Core Buy: Trend Up + Price Pullback + No Crash (Three-Layer Detection)

**Plain English**:
> "Major trend is up (EMA50 > EMA200), price is above long-term moving average, now pulled back below buy line, and - here's the key - no crash in the past 10 minutes, 1 hour, or 12 hours, then I buy!"

**Code Translation**:
```python
EMA50 > EMA200                    # Medium-term trend up
Price > EMA200                     # Long-term trend also up
pair_is_bad < 1                   # Three-layer crash detection all untriggered
Price < buy threshold(MA × 0.968) # Pullback in place
Has volume                         # Not a dead coin
→ Buy!
```

---

## IV. Protection Mechanism: 3 Layers of "Crash Protection Net"

SMAOG has one more layer of long-term protection than SMAIP3v2, and uses rolling method:

| Protection Layer | Time Range | Threshold | Plain English |
|-----------------|------------|-----------|---------------|
| Layer 1 | 10 minutes (2 candles) | 19.8% | "Just crashed 20%, don't touch!" |
| Layer 2 | 1 hour (12 candles) | 17.2% | "Crashed 17% this hour, wait a bit!" |
| Layer 3 | 12 hours (144 candles) | 55.5% | "Crashed 55% today, this coin has problems!" |

This design is more comprehensive than SMAIP3v2 - short, medium, long-term all have protection, preventing you from "catching falling knives" at various time scales 🛡️

---

## V. Sell Logic: More "Picky" Than Buying

### 5.1 Basic Sell: Above Line + Momentum Weakening

```
Price > sell threshold(EMA × 0.985)
AND (any one of the following)
  - Open lower than previous candle (price weakening)
  - RSI < 50 (momentum insufficient)
  - RSI declining (momentum decaying)
→ Sell
```

**Plain English**:
> "Price above sell line? Wait, let me check momentum... hmm, open is lower / RSI weak / RSI dropping, okay then, time to sell."

This is different from SMAIP3v2 - SMAIP3v2 sells when price reaches the line, SMAOG checks momentum again, keeps holding if strong 😎

### 5.2 Comparison: SMAIP3v2 vs SMAOG

| Dimension | SMAIP3v2 | SMAOG |
|-----------|----------|-------|
| Crash Protection Layers | 2 layers | 3 layers (added 12 hours) |
| Protection Method | Fixed shift candles | Rolling sliding window |
| Sell Momentum Filter | None | Yes (3 conditions) |
| Smart Exit Rejection | Yes | No |
| ROI Design | Fixed 2.6% | Progressive (10%/5%/2%) |

**One Sentence**: SMAOG is more "cautious," has more protection, but lost SMAIP3v2's "smart exit rejection" feature.

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Three-Layer Protection in Place**: Short, medium, long-term crash detection, more comprehensive falling knife prevention
2. **Smarter Selling**: Momentum filter avoids premature selling
3. **Progressive Take-Profit**: The longer you hold, the easier to exit, doesn't let capital get locked up
4. **Protection Parameters Optimizable**: All three thresholds support Hyperopt optimization

### ⚠️ Cons (Roast Time)

1. **Limited Parameter Optimization**: Buy/sell core parameters can't be optimized, only protection parameters can
2. **More Computation**: 3 rolling windows, older machines might struggle a bit
3. **Protection May Be Too Sensitive**: Three layers might miss some opportunities after "fake crashes"

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clear Uptrend | 🔥 Use it! | Three-layer protection safer |
| High Volatility Market | ✅ Very suitable | Crash detection helps avoid fake pullbacks |
| Downtrend | ❌ Don't use | Trend filter will block buying |
| After Extreme Crash | ⚠️ Use cautiously | Three-layer protection might all trigger, can't buy |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Evaluation
> "A dip-buyer wearing three bulletproof vests, more cautious than SMAIP3v2, but might miss some opportunities."

### Who Should Use It?
- ✅ Trend traders pursuing safety
- ✅ Victims of "crash dip-buying getting trapped"
- ✅ People who can accept 23% stop loss
- ✅ Steady traders doing major coins

### Who Shouldn't Use It?
- ❌ Short-termers pursuing high-frequency trading
- ❌ Adventurers wanting to buy crashed coins
- ❌ Conservatives with strict stop losses (like 5%)
- ❌ People who don't want to spend time tuning parameters

### My Suggestions
1. **Pick Coins with Moderate Volatility**: Three-layer protection might be too sensitive on high volatility coins
2. **Adjust Protection Thresholds**: Tune the three thresholds based on coin characteristics
3. **Comparative Testing**: Compare with SMAIP3v2, see which fits your trading pairs better
4. **Watch Momentum Exit**: Observe if momentum filter effectively avoids premature selling

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Three-Layer Protection + Momentum Exit

SMAOG is the "enhanced bulletproof version" of the SMAIP series. Code has three more protection calculations and momentum exit filtering than SMAIP3v2.

**Its Money-Making Philosophy**:
- **Safety First**: Three layers of protection, don't buy crashes
- **Trend is King**: EMA50 > EMA200, only trade uptrends
- **Momentum Exit**: Don't sell when strong, wait for momentum to weaken

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------:|:-----------------:|---------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Home field! Three-layer protection helps avoid fake pullbacks |
| 🔄 Oscillating Uptrend | ⭐⭐⭐⭐☆ | Still can make money, protection reduces fake signals |
| 📉 Downtrend | ⭐☆☆☆☆ | Can't get buy signals, capital sleeps |
| ⚡ High Volatility Sideways | ⭐⭐☆☆☆ | Three-layer protection might all trigger, can't buy |

**One-Sentence Summary**: Safer when trends are good, but might miss some opportunities after "fake crashes."

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|-------------------|------------------|------------|
| Number of Pairs | 5-20 pairs | Rolling calculation a bit heavy, don't do too many |
| Coin Selection | Major coins | Altcoins have high volatility, three-layer protection might all trigger |

### 10.2 Key Configuration File Settings

```yaml
# Recommended configuration
timeframe: 5m
stoploss: -0.23  # Or adjust based on risk preference
minimal_roi:
  "0": 0.10    # Just entered target 10%
  "30": 0.05   # After 30 minutes target 5%
  "60": 0.02   # After 60 minutes target 2%

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.005
trailing_stop_positive_offset: 0.02

# Protection thresholds (can adjust based on coins)
pair_is_bad_0_threshold: 0.555  # 12 hours
pair_is_bad_1_threshold: 0.172  # 1 hour
pair_is_bad_2_threshold: 0.198  # 10 minutes
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Normal |
| 50+ pairs | 8GB | 16GB | Rolling calculation has pressure |

**Note**: 3 rolling window calculations are more than SMAIP3v2, older machines might struggle a bit.

### 10.4 Backtesting vs Live

Rolling window performance in backtesting and live might differ, suggestions:

**Recommended Process**:
1. Backtest and tune parameters first (protection parameters are optimizable)
2. Run simulation for at least 1 month
3. Observe actual trigger frequency of three-layer protection
4. Small capital live test
5. Gradually increase capital

**Don't go all-in right away**, three layers of protection is good, but might also miss opportunities!

---

## XI. Bonus: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **OG's Meaning**: Strategy name SMAOG, might mean "Original Gangster" (veteran level)
   > "I'm the enhanced version of SMAIP series, I have bulletproof vests!" 🛡️

2. **Three-Layer Rolling Protection**: Uses rolling windows instead of fixed shift
   > "No matter when the crash happens, I can detect it!"

3. **Buy Parameters Not Optimized**: Core parameters locked, only protection optimized
   > "Core logic can't be messed with, but protection thresholds can adjust per coin"

4. **Momentum Exit**: More "picky" than SMAIP3v2
   > "Above the line isn't enough, I only sell when momentum weakens"

---

## XII. Final Words

### One-Sentence Evaluation
> "A dip-buyer wearing three bulletproof vests, safer but might miss some opportunities."

### Who Should Use It?
- ✅ Trend traders pursuing safety
- ✅ Steady traders doing major coins
- ✅ People who can accept 23% stop loss
- ✅ People with time to tune parameters

### Who Shouldn't Use It?
- ❌ Short-termers pursuing high-frequency trading
- ❌ Adventurers wanting to buy crashed coins
- ❌ Conservatives with strict stop losses
- ❌ People who don't want to spend time understanding three-layer protection

### Manual Trader Suggestions
If you're trading manually, you can borrow the core ideas from this strategy:
- Use EMA50/EMA200 to judge trend
- Set three-layer crash detection rules (10 minutes, 1 hour, 12 hours)
- Check momentum when selling, keep holding if strong
- Use progressive take-profit, the longer you hold, the lower the target

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtesting Looks Beautiful, Live Trading Needs Caution

SMAOG's three-layer protection looks perfect - but be aware:

> **Three-layer protection might be too sensitive, on high volatility coins might trigger frequently, leading to missed opportunities after some "fake crashes."**

Simply put: **Wearing too much bulletproof gear, sometimes you can't run fast.**

### Hidden Risks of Complex Strategies

Be careful in live trading:
- **Protection Oversensitivity**: Three-layer protection might miss some rebounds after "fake crashes"
- **Calculation Delay**: Rolling window calculations might have delay in high-frequency situations
- **Parameter Dependency**: Protection thresholds have big impact on strategy performance

### My Suggestions (Real Talk)

```
1. Adjust three-layer protection thresholds based on coins
2. Test with SMAIP3v2 first, then compare with SMAOG
3. Observe actual trigger frequency of three-layer protection
4. Can appropriately relax thresholds for high volatility coins
5. Don't expect protection to stop all crashes
```

**Remember**: Three bulletproof vests are good things, but sometimes wearing too much you get hot and can't run. Light position testing, staying alive is most important! 🙏