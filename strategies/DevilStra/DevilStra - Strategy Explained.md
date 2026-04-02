# DevilStra Strategy: Plain English Edition

## 1. What Does This Strategy Do?

Imagine you have a super-smart trading assistant that can freely combine hundreds of technical indicators and automatically find the best trading rules for each coin — that's DevilStra.

The "Devil" in the name isn't about doing evil — it comes from the author's poetic line: The devil is stronger than God, but only God can create new life, while the devil excels at combining small things into great power. Simply put: **This strategy doesn't invent new indicators — it plays existing ones like a master.**

**Who it's for**:
- Lazy automation enthusiasts
- People with multiple coins to trade simultaneously
- Office workers who don't want to watch charts all day
- People willing to spend time optimizing parameters

**Who it's NOT for**:
- People wanting same-day trading results (needs parameter optimization first)
- People trading only one coin (strategy designed for multi-coin)
- High-frequency traders (4-hour timeframe)

---

## 2. Core Gameplay: The Spell System

The most special thing about this strategy is its "Spell" system.

### 2.1 What Are Spells?

Think of "spells" as **pre-set trading rule packages**. Each spell contains:
- **Buy rules**: 3 conditions, all must be met to buy
- **Sell rules**: 3 conditions, all must be met to sell

The strategy defines 9 base spells with mysterious names:

| Spell | Meaning |
|-------|---------|
| Zi (Purple) | Purple system rules |
| Gu (Ancient) | Classical rules |
| Lu (Path) | Trend path rules |
| La (Pull) | Pull-up capture rules |
| Si (Think) | Deliberate rules |
| Pa (Balance) | Balance派 rules |
| De (German) | Steady rules |
| Ra (Sun) | Solar energy rules |
| Cu (Store) | Inventory rules |

### 2.2 Each Coin Uses a Different Spell

This is the brilliant part — the strategy uses Hyperopt to automatically assign each coin its own spell combination.

For example, after optimization:
```
BTC uses Zi spell
ETH uses Lu spell
SOL uses Ra spell
...
```

Each coin has its own tailored trading rules!

---

## 3. Indicator Library: 150+ Weapons

The strategy calls TA-Lib technical indicator library with over 150 indicators:

**Trend indicators**: MA, EMA, MACD, ADX, etc.
**Momentum indicators**: RSI, KDJ, Williams, etc.
**Volatility indicators**: Bollinger Bands, ATR, etc.
**Volume indicators**: OBV, Volume MA, etc.
**Pattern indicators**: Doji, Hammer, and 60+ candlestick patterns

---

## 4. Operators: 16 Ways to Judge

**Simple comparison**: `>`, `<`, `=`
**Crossover judgment**: `CA` (golden cross = buy), `CB` (death cross = sell)
**Numerical comparison**: `>R`, `<R`, `=R`
**Ratio judgment**: `/>R`, `/<R`, `/=R`
**Trend judgment**: `UT` (rising trend), `DT` (falling trend)
**Crossover trend**: `CUT` (crossover rising sharply), `CDT` (crossover falling sharply)

---

## 5. Practical Performance

According to code comment optimization results:

| Metric | Value | Rating |
|--------|-------|--------|
| Trades | 108 | Medium frequency |
| Win rate | 69% | Pretty high |
| Average profit | 7.77% | Good |
| Total profit | 84% | Very good |
| Avg holding | 3 days | Medium-long term |

---

## 6. Summary

DevilStra is a creative strategy that maximizes "the power of combination." But it's not a "get rich while you sleep" tool — it requires time investment for parameter optimization and continuous performance monitoring.

**Final reminder**: Historical performance doesn't guarantee future returns. No matter how beautiful the backtest, treat real capital with caution!
