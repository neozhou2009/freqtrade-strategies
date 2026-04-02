# STRATEGY_RSI_BB_CROSS Strategy: The Percentage Crossover Master

> **Nickname**: Percentage Hero, Symmetry Freak  
> **Occupation**: Oscillating Market Trader  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **STRATEGY_RSI_BB_CROSS** is a strategy that:
- Converts Bollinger Band position to a percentage (0-1)
- Converts RSI position to a percentage too (0-1)
- The two percentages fight each other, trade when they cross

It's like **two thermometers comparing who's hotter** — one measures "price heat" (Bollinger Band position), one measures "momentum heat" (RSI position), whoever overtakes whom triggers a signal! 🌡️

---

## II. Core Configuration: Also "Four-Level Take Profit + Loose Stop Loss"

### Take Profit Rules (ROI Table)

```
Just bought → Target 4%
30 minutes later → Target drops to 2%
60 minutes later → Target drops to 1%
```

**Translation**: When entering, want 4%; waited longer, lowered expectations, 1% will let you exit too. Same ROI setting as STRATEGY_RSI_BB_BOUNDS_CROSS.

### Stop Loss Rule

```
Cut at 10% loss
```

**Translation**: Giving enough room for fluctuation, 10% stop loss. Enough for oscillating coins, may not be enough for trending coins.

---

## III. Core Concept: Turn Everything into Percentages

### Bollinger Band Percentage (BB%)

**Formula**:
```
BB% = (Price - Bollinger Band Lower) / (Bollinger Band Upper - Bollinger Band Lower)
```

**Plain English**:
- BB% = 0: Price stepping on Bollinger Band lower band
- BB% = 1: Price hitting Bollinger Band upper band
- BB% = 0.5: Price at Bollinger Band middle

### RSI Percentage (RSI%)

**Formula**:
```
RSI% = (RSI - 30) / (100 - 30 - 30) = (RSI - 30) / 40
```

**Plain English**:
- RSI% = 0: RSI at oversold line (30)
- RSI% = 1: RSI at overbought line (70)
- RSI% = 0.5: RSI at neutral zone (50)

### Why Do This?

**Because now you can compare them directly!**

Bollinger Band position (price dimension) and RSI position (momentum dimension) were originally two different things, now both become 0-1 percentages, compare directly:

- **BB% > RSI%**: Price position higher than momentum position → possibly overbought
- **BB% < RSI%**: Price position lower than momentum position → possibly oversold

**Genius idea!** 🧠

---

## IV. Buy Condition: Crossover + Zone + Trend

### 🎯 Buy Signal: BB% Crosses Above RSI%

**Condition Combination**:

| Condition | Code | Human Translation |
|-----------|------|-------------------|
| Crossover signal | `crossed_above(bb_percent, rsi_percent)` | BB% just exceeded RSI% |
| Zone restriction | `bb_percent < 0.5` | BB% still in lower half |
| Zone restriction | `rsi_percent < 0.5` | RSI% also in lower half |
| Trend confirmation | `bb_below_rsi_count.shift(1)` | Previous 14 candles BB% all below RSI% |

**Plain English**:
> "Bro, BB% just overtook RSI%! And both are in the lower half (both relatively low). Key is, for the past 14 candles BB% was being suppressed by RSI%, now finally turning around! Buy!" 🚀

---

## V. Sell Condition: Perfect Symmetry

### 🎯 Sell Signal: BB% Crosses Below RSI%

**Condition Combination**:

| Condition | Code | Human Translation |
|-----------|------|-------------------|
| Crossover signal | `crossed_below(bb_percent, rsi_percent)` | BB% just got overtaken by RSI% |
| Zone restriction | `bb_percent > 0.5` | BB% in upper half |
| Zone restriction | `rsi_percent > 0.5` | RSI% also in upper half |
| Trend confirmation | `bb_above_rsi_count.shift(1)` | Previous 14 candles BB% all above RSI% |

**Plain English**:
> "BB% got overtaken by RSI%! And both are in the upper half (both relatively high). For the past 14 candles BB% was the boss, now got taken down. Sell!" 💰

### Symmetry Display

| Dimension | Buy | Sell |
|-----------|-----|------|
| Crossover Direction | BB% crosses above RSI% | BB% crosses below RSI% |
| Zone Requirement | Both < 0.5 (lower half) | Both > 0.5 (upper half) |
| Trend Confirmation | BB% continuously below RSI% | BB% continuously above RSI% |

**Perfect symmetry! This is the OCD art of the strategy author!** 🎨

---

## VI. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Section)

1. **Perfect Logic Symmetry**: Buy and sell conditions correspond one-to-one, OCD patients rejoice
2. **Normalized Comparison**: Unifying indicators from different dimensions to percentages, genius idea
3. **Zone Filter**: Ensures buying in lower half, selling in upper half, won't trade randomly
4. **Trend Confirmation**: 14-period confirmation, not decided by one candle

### ⚠️ Disadvantages (Critique Section)

1. **Crossover Signal Lag**: Crossover is post-confirmation, may miss optimal entry point
2. **No Trailing Stop**: Floating profit can turn into loss, watching profits slip away
3. **Hardcoded Parameters**: Trend confirmation period and RSI limit are both hardcoded
4. **Fixed Bollinger Band Window**: 20 period may not suit all coins

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ | Perfect match! Percentage crossover signals clear in oscillation |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐⭐ | Also home turf! Buy low sell high, perfect |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Buy signals will trigger, but may buy into losing positions |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Percentage positions jump around, signals may be unstable |

---

## VIII. Summary: How is This Strategy Really?

### One-Sentence Review
> "Perfect logic symmetry, genius percentage comparison, elegant dancer in oscillating markets."

### Who Should Use It?
- ✅ Oscillating market lovers
- ✅ People who like logic symmetry
- ✅ People interested in percentage normalization
- ✅ People who can accept crossover signal lag

### Who Should NOT Use It?
- ❌ People seeking instant entry (crossover signals have lag)
- ❌ One-way trend markets
- ❌ People who need trailing profit
- ❌ High volatility coins (percentages will jump around)

### My Recommendations
1. **Oscillating coins first**: This strategy is naturally designed for oscillation
2. **Watch crossover confirmation**: Crossover signals have lag, be mentally prepared
3. **Consider adding trailing stop**: Locking in floating profit is important
4. **Compare test with RSI_BB_BOUNDS_CROSS**: Both strategies are RSI+Bollinger Band, can compare effectiveness

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: The Game of Percentage Positions

This strategy's innovation is **normalized percentage comparison**:

**Bollinger Band Percentage says**: "Where is price in the statistical volatility range"
**RSI Percentage says**: "Where is momentum in the overbought/oversold range"

When crossovers occur between them:
- **BB% crosses above RSI%**: Price position starting to exceed momentum position → possible bounce
- **BB% crosses below RSI%**: Price position starting to weaken relative to momentum position → possible pullback

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:------------|:-------|:--------------------------|
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ | Percentage positions stable, crossover signals clear, perfect |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐⭐ | This is home turf! Buy low sell high, symmetrical signals |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Buy signals trigger but stop losses bleed |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Percentage positions jumping around, crossovers may repeat |

**One-Sentence Summary**: A "symmetrical artist" for oscillating markets, may not adapt well to one-way trends.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Note |
|-------------------|-----------------|------|
| Timeframe | 5m | Default design, don't change |
| Bollinger Band Window | 20 | Standard 20, can consider optimization |
| RSI Period | 14 | Classic setting, no need to change |
| Trend Confirmation Period | 14 | Consistent with RSI period, logically coherent |

### 10.2 Key Settings in Configuration File

```yaml
# Suggest adding trailing stop
trailing_stop = True
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.03
trailing_only_offset_is_reached = True
```

### 10.3 Hardware Requirements (Important!)

This strategy has moderate calculation requirements, not demanding on VPS:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 | 2GB | 4GB | Smooth |
| 10-50 | 4GB | 8GB | No problem |

**Warning**: Crossover judgment needs `qtpylib.crossed_above/crossed_below`, small calculation but watch for latency 😎

### 10.4 Backtesting vs Live Trading

- **Backtesting looks great**: Crossover signals clear, buy/sell symmetrical
- **Live trading note**: Crossover is post-confirmation, may have slippage

**Suggested Process**:
1. Backtest 3 months of data first
2. Paper trade for 1-2 weeks
3. Small position live testing
4. Compare effectiveness with STRATEGY_RSI_BB_BOUNDS_CROSS

**Don't go all-in right away**, no matter how good the strategy, it needs tuning!

---

## XI. Easter Egg: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Perfect Symmetry**: Buy and sell conditions correspond one-to-one, the author must have OCD
   > "Symmetry is beauty, buying and selling both"

2. **Trend Confirmation Matches RSI Period**: `_trend_length = 14`, same as RSI period
   > "Using RSI's period to confirm trend, logical loop closed"

3. **Bollinger Band Window Uses 20**: More standard than STRATEGY_RSI_BB_BOUNDS_CROSS's 14
   > "Standard Bollinger Band setting, classic never goes out of style"

4. **RSI Limit 30**: `rsi_limit = 30`, using oversold line as percentage lower bound
   > "Below oversold doesn't count, above oversold is the market"

---

## XII. The Very Last Thing

### One-Sentence Review
> "Percentage crossover, symmetrical buy/sell, elegant solution for oscillating markets."

### Who Should Use It?
- ✅ Oscillating market lovers
- ✅ People who like symmetrical logic
- ✅ People interested in normalization methods
- ✅ People who can accept signal lag

### Who Should NOT Use It?
- ❌ People seeking instant entry
- ❌ One-way trend seekers
- ❌ People who need trailing profit
- ❌ People who don't like crossover signal lag

### Suggestions for Manual Traders

If you're trading manually, you can use this strategy's concept like this:

1. **Calculate BB%**: (Price - Lower Band) / (Upper Band - Lower Band)
2. **Calculate RSI%**: (RSI - 30) / 40
3. **Wait for Crossover**: BB% crosses above RSI% and both < 0.5 → Buy
4. **Wait for Crossover**: BB% crosses below RSI% and both > 0.5 → Sell
5. **Trend Confirmation**: 14 consecutive candles maintaining trend before crossover

---

## XIII. ⚠️ Risk Re-emphasis (Must Read Section)

### Backtesting is Beautiful, Live Trading Needs Caution

STRATEGY_RSI_BB_CROSS's historical backtest performance may be **quite good** — but there's a trap:

> **Crossover signals are post-confirmation, meaning you're always one step behind the optimal entry point.**

Simply put: **"When you see the crossover, the best price has already passed."**

### Hidden Risks of Percentage Crossover

In live trading, percentage calculation may lead to:
- **Signal Lag**: Crossover needs confirmation, not an instant signal
- **Zone Boundary Blurriness**: Judgments near 0.5 may change frequently
- **Repeated Triggering in Oscillation**: Back-and-forth crossovers may eat up fees

### My Suggestion (Heartfelt Words)

```
1. Oscillating coins first, trend coins avoid
2. Add trailing stop, lock in floating profit
3. Accept signal lag, don't pursue perfect entry
4. Compare test with STRATEGY_RSI_BB_BOUNDS_CROSS
```

**Remember**: No matter how good the strategy, crossover signals are always post-confirmation. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: Percentage comparison is a genius idea, but genius ideas also need live verification. Good luck! 🍀