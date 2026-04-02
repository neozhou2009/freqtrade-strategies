# CombinedBinHAndCluc Strategy: Two Old Masters "Fused Together"

> **Nickname**: Twin Swords Combined
> **Profession**: Bollinger Band Combo Strategy Player
> **Timeframe**: 5 Minutes (short-term trading)

---

## 1. What's This Strategy?

**CombinedBinHAndCluc** literally means "Combine Bollinger Bands and Cluc." Simply put:
- Two old strategies **BinHV45** and **ClucMay72018** forcibly merged together
- Whichever one says buy, you listen (OR gate logic)
- Specifically hunts for "hammer" patterns near Bollinger Bands

Think of it as a general with two military advisors: "Military Advisor A says buy, buy! Military Advisor B says buy, also buy! As long as one of them nods, we place the order!" 🧙‍♂️

---

## 2. Core Settings: Simple and Brutal

### Take-Profit Rules
```
Make 5%? → Run!
```
**Plain English**: 5% and done, not greedy, take profits and go!

### Stop-Loss Rules
```
Lose 10%? → Cut!
```
**Plain English**: Allowing a 10% loss, giving you enough rope!

### Trading Frequency
```
Max 2 positions
```
**Plain English**: Don't put all eggs in one basket, 2 at a time is enough!

---

## 3. Entry Conditions: 2 Modes, Either One Works

This strategy has two buy modes — triggering buy when either is satisfied:

### 🎯 Mode 1: BinHV45 (Hammer Pattern)

**Trigger Conditions** (Plain English version):
1. Bollinger Band width wide enough (> 0.8% of price)
2. Price fluctuation large enough (> 1.75% of price)
3. Lower wick short (< 25% of width)
4. **Close breaks below Bollinger lower band**
5. **Close lower than previous candle**

**Plain English**:
> "Price dropped below the Bollinger lower band, and it's a hammer pattern (long lower wick) — isn't this stable? Buy it!"

### 🎯 Mode 2: ClucMay72018 (Shrinking Volume Rebound)

**Trigger Conditions** (Plain English version):
1. Price below EMA50
2. Price < 98.5% of Bollinger lower band
3. **Volume extremely low** (< 1/20th of average)

**Plain English**:
> "Price dropped below the Bollinger lower band, nobody's trading (ground volume) — isn't this abnormal? Buy it!"

**Summary**: Though the two modes have different angles, their core message is the same — "Price dropped below Bollinger Bands, might rebound!"

---

## 4. Protection Mechanisms: Just One Stop-Loss

This strategy's protection mechanism is extremely simple:

| Protection Type | Trigger | Plain English |
|----------------|---------|---------------|
| **Hard Stop-Loss** | Lose 10% | "Lost 10%, don't hold on, bail out!" |
| **Take-Profit** | Make 5% | "Made 5%, take profits and go!" |

**Commentary**: That's it? Yes, simple and brutal! 😅

---

## 5. Exit Logic: Just One Condition

### Technical Sell: Breaking Bollinger Middle Band

```python
Price > Bollinger middle band
```

**Plain English**:
> "Price rose to the Bollinger middle band, transitioned from downtrend to consolidation — run!"

### Other Exits

| Sell Type | Trigger |
|-----------|---------|
| **ROI Take-Profit** | Make 5% |
| **Stop-Loss** | Lose 10% |

**Plain English**: Just three words — **Run! Run! Run!**

---

## 6. Strategy "Personality"

### Personality Analysis

| Trait | Description |
|-------|-------------|
| **Decisive** | 5% and run, no hesitation |
| **Cautious** | 10% before cutting, gives opportunities |
| **Simple** | No fancy tricks |
| **Dual-Faced** | Two strategies, one will always hit |

### Who's It For?

- ✅ People who like short-term trading
- ✅ People who like simple strategies
- ✅ People who accept 5% small targets
- ❌ People who like long-term holding
- ❌ People who like complex strategies

---

## 7. Applicable Scenarios

### ✅ Recommended Scenarios

1. **Volatile Market**: Price fluctuates up and down
2. **Short-Term Trading**: Just playing 5-minute level
3. **Multi-Coin Allocation**: Run 2 trading pairs simultaneously
4. **Strategy Combination**: Use with other strategies

### ❌ Not Recommended Scenarios

1. **Unilateral Uptrend**: May miss rally
2. **Unilateral Downtrend**: Easily stopped out
3. **Sideways Consolidation**: May get slapped around

---

## 8. Summary

**CombinedBinHAndCluc** = **BinHV45 + ClucMay72018** = **Two Old Masters Combined**

| Item | Value |
|------|-------|
| **Buy Modes** | 2 (either one) |
| **Take-Profit** | 5% |
| **Stop-Loss** | 10% |
| **Timeframe** | 5 Minutes |
| **Complexity** | ⭐⭐ (Simple) |

**One-Line**: Whichever strategy says buy, buy; 5%, 10%, simple and brutal!

---

## 9. Market Performance

### Ideal Situations

- ✅ Excellent performance in volatile markets
- ✅ Captured effective hammer patterns
- ✅ Rebounded after volume shrinkage

### Not Ideal Situations

- ❌ May get stopped out consecutively in unilateral downtrends
- ❌ False breakouts happen
- ❌ May miss opportunities in trending markets

---

## 10. Configuration Suggestions

### Beginner Suggestions

```python
# Conservative Configuration
minimal_roi = {"0": 0.03}  # 3% and run
stoploss = -0.08           # 8% and cut
max_open_trades = 1        # Only play 1
```

### Veteran Configuration

```python
# Aggressive Configuration
minimal_roi = {"0": 0.08}  # 8% before running
stoploss = -0.15           # 15% before cutting
max_open_trades = 3        # Play 3
```

### My Suggestions

1. **Paper trade first**: Run on paper first
2. **Small position**: Try with pocket change first
3. **Watch the market**: Good in bull markets, careful in bear markets
4. **Review regularly**: Check strategy performance weekly

---

## 11. Bonus

### Strategy Founder

This strategy was written by **iterativ**, a quantitative player who likes combining multiple strategies.

### Strategy Evolution

| Version | Characteristics |
|---------|----------------|
| V1 | Original version (this article) |
| V2-V8 | Gradually added more modes |
| Hyper | Added hyperparameter optimization |

### Fun Fact

- This is one of the most classic strategies in the freqtrade community
- Many newcomers start with this strategy
- Simple but effective!

---

## 12. The Bottom Line

**Mindset When Using This Strategy**:

1. **Don't be greedy**: 5% and run, don't dream of overnight riches
2. **Don't fear losses**: 10% stop-loss is normal loss
3. **Don't hesitate**: Write it down when strategy says buy, sell when sold
4. **Don't slack**: Review regularly, check strategy performance

**Remember**: Simple strategy + strict execution = long-term profit 🎯

---

## ⚠️ Risk Reminder

### Main Risks

| Risk | Likelihood | Consequence |
|------|-----------|-------------|
| **Consecutive Stop-Outs** | Medium | Account drawdown |
| **False Breakout** | High | Bought at the top |
| **Missing Rally** | Medium | Missed profit |
| **Trending Market** | Medium | Poor performance |

### Risk Control Suggestions

1. **Set stop-loss**: Don't be sentimental, cut at 10%
2. **Diversify investment**: Don't full-position one coin
3. **Paper trade first**: Don't go naked
4. **Watch the market**: Bull market closes eyes to buy, bear market be careful
5. **Review regularly**: Check monthly strategy performance

### Most Important One Line

> **Strategy is good, but market is bad.**
> **Learn to respect the market, learn to accept losses.**

---

**Happy trading everyone!** 🚀
