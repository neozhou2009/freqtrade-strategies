# CombinedBinHAndClucV6H Strategy Explained: The "Precision Radar" Oversold Rebound Expert

> **Nickname**: Precision Radar / Optimized V6
> **Profession**: Oversold Rebound Expert
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy?

**CombinedBinHAndClucV6H** is V6's **"finely renovated"** version—merged from two old strategies (BinHV45 and ClucMay72018), then **hyperparameter auto-optimized** as a "precision radar" edition.

Its work is simple: **find opportunities where price "dropped too much" and wait for it to recover.**

Works on **5-minute** level. Best suited for volatile, up-and-down markets.

**V6H Version Upgrades** (vs V6):
- **Hyperparameter auto-search optimization**, more precise parameters
- Take-profit stays at 2.2%
- Trailing stop stays "bold" (3.0% activation + 1.5% pullback)
- Exit stays cautious (7 candles confirmation)
- Retains EMA200 trend filter (prevents chasing highs)
- ⚠️ But adds **overfitting risk** (Hyperoptable version's common issue)

---

## 2. Core Settings: "V6, Optimized"

| Setting | Value | Plain English |
|---------|-------|---------------|
| Timeframe | 5 minutes | Short-term, high frequency |
| Take-profit | 2.2% | Grab 2.2% and run |
| Stop-loss | -99% | Almost no limit |
| Trailing stop | Activates at 2.75% profit | Won't protect until you're up 2.75% |
| Trailing pullback | 1.5% | Drops 1.5% from high triggers stop |
| Sell only in profit | True | No selling when losing |
| Trend filter | EMA200 | Prevents chasing highs |
| Hyperparameter optimized | Yes | Through automated search |

> **V6H Note**: Parameters optimized through hyperparameter auto-search—**may have overfitting risk**: looks great in backtesting, but live may underperform.

---

## 3. Entry Conditions (2 Base Sets + EMA200 Filter)

### Set 1: BinHV45 Style (Rapid Sell-off Rebound)
Price suddenly crashes, breaks below the lower Bollinger Band, but can't drop further—bottom fishing!

**Requirements**: Valid lower band, width > 0.8%, close change > 1.75%, short lower wick, close below band, flat/down close, volume > 0.

### Set 2: ClucMay72018 Style (Volume-Shrinking Oversold)
Price breaks below lower Bollinger Band, but volume tiny—nobody's selling.

**Requirements**: Below 50-day MA, below 98.5% of lower band, volume < 20x average, volume > 0.

### EMA200 Trend Filter (V6H Retained Anti-Chase Feature)
**Requirements**: Price within 5% above EMA200, volume > 0.

**Plain English**: Price can't be too far above the moving average—won't buy if it's risen too much.

---

## 4. Protection Mechanisms: 4 Layers

| Protection | Trigger | Plain English |
|------------|---------|---------------|
| Fixed stop-loss | Loss 99% | Almost never triggers |
| Time stop-loss | >5 hrs and losing | "5 hours and still losing? Done" |
| Trailing stop | Profit 3.0% then activates | "Up 3%, 1.5% pullback and I'm gone" |
| Sell only in profit | Sell signal but losing | "No selling when losing" |

---

## 5. V6H vs V6 vs V5: Summary

| Setting | V5 | V6 | V6H | Impact |
|---------|-----|-----|-----|--------|
| Take-profit | 2.0% | 2.2% | 2.2% | V6 raised, V6H maintained |
| Stop-loss | -99% | -99% | -99% | Unchanged |
| Trailing activation | 2.75% | 3.0% | 3.0% | V6 later, V6H maintained |
| Trailing pullback | 1.25% | 1.5% | 1.5% | V6 deeper, V6H maintained |
| Time stop-loss | 5 hrs | 5 hrs | 5 hrs | Unchanged |
| Exit confirmation | 6 candles | 7 candles | 7 candles | V6 stricter |
| Trend filter | None | EMA200 | EMA200 | V6 new |
| Hyperoptable | No | No | ✅ Yes | V6H unique |

---

## 6. ⚠️ Most Important: Overfitting Risk

**V6H's biggest hidden risk!**

> **Historical backtest looks like "memorizing exam answers"—high scores, but new questions might fail.**

**Why?** Algorithm may "memorize" historical market patterns that don't hold in the future.

**Avoiding Overfitting**:
```
1. Find optimization period (e.g., Jan-Jun 2023)
2. Use Jul-Dec 2023 for out-of-sample verification
3. Pass verification before live trading
4. Continuous monitoring, adjust if anomalies appear
```

---

## 7. Final Word

### One-Word Verdict
> **"V6H = V6 + hyperparameter optimization + overfitting risk"**

### Who Should Use It?
- ✅ People who like short-term trading
- ✅ People wanting better returns in specific markets
- ✅ People who can accept 5-hour stop-loss exits
- ✅ People who understand overfitting risks
- ✅ People willing to do out-of-sample verification

### Who Should NOT Use It?
- ❌ People looking for a "universal strategy"
- ❌ People who don't understand parameter optimization limitations
- ❌ People who don't want to verify

---

## 8. ⚠️ Risk Re-emphasis

### V6H's Hidden Risks

1. **Overfitting**: Parameters optimized for history, live may underperform
2. **Poor Parameter Generalizability**: Like "custom suit"—only fits same body type
3. **Must Do Out-of-Sample Testing!**
4. **Loose Stop-Loss**: -99% almost disabled
5. **High-Frequency Costs**: Fees add up

### Sincere Advice

```
1. Don't worship V6H: optimized parameters aren't necessarily better
2. Always do out-of-sample testing
3. Keep monitoring live performance
4. Prepare backup plans: strategy failure is normal
5. Survival first: test with light positions
```

**Remember**: Optimization is a tool, not a holy grail. Backtesting is past, markets are alive. Light positions, survival first! 🙏
