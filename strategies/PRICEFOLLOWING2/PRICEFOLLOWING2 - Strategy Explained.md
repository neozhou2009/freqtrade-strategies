# PRICEFOLLOWING2 Strategy: The "Cautious Follower" of the Moving Average School

> **Nickname**: Cautious Follower, Upgraded Little Sidekick  
> **Occupation**: Watching moving average crossovers, but being more careful this time  
> **Timeframe**: 15 minutes (slow jogger)

---

## I. What Is This Strategy?

Simply put, **PRICEFOLLOWING2** is:
- The "upgraded version" of PRICEFOLLOWING
- Timeframe extended to 15 minutes, not so impulsive
- Sell conditions stricter, needs 3 signals to confirm together

Like **that impatient little follower grew up and learned to be steady** 🤣  
No longer rushing at every moving average crossover, now checking price position, difference ratio, confirming everything before acting.

---

## II. Core Configuration: Same as PRICEFOLLOWING

### Take Profit Rules (ROI Table)

```
Holding Time    Target Return
────────────────────────────
0 minutes       4%       ← Want 4% right at the start
30 minutes      3%       ← Dragged on, lower target
60 minutes      2.5%     ← The longer, the lower
```

**Translation**: Same as PRICEFOLLOWING, impatient configuration unchanged.

### Stop Loss Rules

```
Fixed stop loss: -10%
Trailing stop: Activates after 3% profit, trails at 2%
```

**Translation**: Lose 10% and accept defeat; after making 3%+, start locking in profits.

---

## III. What's Different from PRICEFOLLOWING: What Got Upgraded?

### 🎯 Main Upgrade Points

| Comparison Item | PRICEFOLLOWING | PRICEFOLLOWING2 |
|-----------------|----------------|-----------------|
| **Timeframe** | 5 minutes | 15 minutes (steadier) |
| **Buy Confirmation** | 2 conditions | 2 conditions (but different logic) |
| **Sell Confirmation** | 1-2 conditions | 1-3 conditions (stricter) |

**Plain English**: The old follower was too impatient, this time learned to "wait and see."

---

## IV. Buy Logic: More Particular This Time

### 4.1 Mode 1: RSI Filter On Version

**Same as PRICEFOLLOWING**:
- RSI < 30 + EMA7 crosses below TEMA

### 4.2 Mode 2: RSI Filter Off Version (Default)

**Here's the difference!**

```python
Condition 1: EMA7 crosses below TEMA
Condition 2: (TEMA - EMA7) / TEMA < 0.004 (default value)
```

**Plain English**:
> "Moving average crossover is step one, but also need to check if the two lines are close enough. If the difference relative to TEMA ratio is less than 0.4%, it means the two lines are already very close, making the crossover more meaningful."

**Why Designed This Way?**
- Prevent "false crossovers": Sometimes EMA7 seems to cross TEMA, but the lines are actually far apart
- Confirm trend strength: Lines close together means trend change is more definite

---

## V. Sell Logic: More Cautious This Time!

### 5.1 Mode 1: RSI Sell Filter On Version (Default)

**Same as PRICEFOLLOWING**:
- RSI < 70 + EMA7 crosses above TEMA

### 5.2 Mode 2: RSI Sell Filter Off Version

**Big change here!**

```python
Condition 1: EMA7 crosses above TEMA
Condition 2: best_bid < ha_close (best bid below Heikin Ashi close price)
Condition 3: (TEMA - EMA7) / EMA7 < 0.003 (default value)
```

**Plain English**:
> "Time to sell? Not so fast, confirm three things first:
> 1. EMA7 crosses above TEMA —— trend might reverse
> 2. Best bid below smoothed price —— current price is indeed dropping
> 3. EMA difference ratio below threshold —— trend reversal confirmed
> 
> All three must be met, then sell!"

**This is like before it was 'run when you see signal', now it's 'see signal, confirm danger, confirm again, then run'** 🎯

---

## VI. Protection Mechanism: Same Dual Insurance

| Protection Type | Parameter | Plain English |
|----------------|-----------|---------------|
| Fixed Stop Loss | -10% | "Lose 10% and I'm out, not holding on" |
| Trailing Stop | Activates at 3%, trails 2% | "After making 3%, start locking, if it drops 2% I leave" |

Same protection mechanism as PRICEFOLLOWING, **steady as an old dog** 🧯

---

## VII. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Section)

1. **More Reliable Signals**: Multiple confirmation reduces false signals, higher win rate
2. **Longer Timeframe**: 15 minutes filters short-term noise, more stable
3. **Price Confirmation**: References Heikin Ashi smoothed price, not impulsive
4. **Adjustable Parameters**: EMA difference percentage can be tuned per pair

### ⚠️ Cons (Critique Section)

1. **Fewer Entry Opportunities**: More confirmation conditions, lower signal frequency
2. **Slower Reaction**: 15-minute frame, might miss fast opportunities
3. **Still Long Only**: Bear market, just watching
4. **Information Layer Still Decoration**: Loaded ETH/BTC data but not used 😅

---

## VIII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| **Trending Up** | Default configuration | Multiple confirmation captures full trend |
| **Oscillating Sideways** | Turn off RSI sell filter | Let strict conditions work |
| **Trending Down** | Don't use this strategy | Long only, no chance |
| **Violent Volatility** | Not recommended | Reacts too slow, can't keep up |

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Multiple Confirmation + Longer Cycle

PRICEFOLLOWING2 is the **stable upgraded version** of PRICEFOLLOWING. Similar code size, but stricter sell logic.

**Its Money-Making Philosophy**: **Better to do less than do wrong**

- **Longer Cycle**: 15-minute frame, fewer chances to get "fooled" by short-term fluctuations
- **Multiple Confirmation**: Selling needs 3 conditions, more reliable than 1
- **Price Reference**: Heikin Ashi close price smooths price fluctuation

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 **Trending Up** | ⭐⭐⭐⭐⭐ | Steadily captures trend, trailing stop locks profits |
| 🔄 **Oscillating Sideways** | ⭐⭐⭐☆☆ | Low signal frequency, less fee loss |
| 📉 **Trending Down** | ⭐⭐☆☆☆ | Long only, just rest during decline |
| ⚡ **Violent Volatility** | ⭐⭐☆☆☆ | Reacts too slow, might miss opportunities |

**One-sentence Summary**: **Choice for the steady type, prefer safety over speed**

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Notes |
|------------|-------------------|-------|
| Number of pairs | 5-15 | Few signals, don't need too many pairs |
| Mainstream vs Altcoins | Mainstream preferred | Too much volatility might miss |
| Timeframe | 15m (fixed) | This is its feature |

### 10.2 Key Config File Settings

```yaml
# Key parameters
rsi_enabled: false        # RSI filter off by default
rsi_value: 30            # RSI threshold
ema_pct: 0.004           # EMA difference percentage (buy)
sell_rsi_enabled: true   # RSI sell filter on
ema_sell_pct: 0.003      # EMA difference percentage (sell)
stoploss: -0.1           # Stop loss 10%
trailing_stop: true      # Enable trailing stop
```

### 10.3 Hardware Requirements

Similar to PRICEFOLLOWING:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Okay |
| 50+ pairs | 8GB | 16GB | Might be slow |

### 10.4 Backtest vs Live

This strategy is more suitable for live trading than PRICEFOLLOWING:
- **More Reliable Signals**: Multiple confirmation reduces false signals
- **Lower Trading Frequency**: Less impact from fees and slippage
- **Better for Longer Cycles**: 15-minute frame more stable

**Recommended Process**:
1. Backtest to see results
2. Paper trading test
3. Small capital live trading
4. Confirm stable before increasing capital

---

## XI. Easter Egg: The "Brotherhood" with PRICEFOLLOWING

### 11.1 Same Mother, Different Personalities

| Comparison Point | PRICEFOLLOWING | PRICEFOLLOWING2 |
|-----------------|----------------|-----------------|
| **Personality** | Impatient | Steady |
| **Timeframe** | 5 minutes | 15 minutes |
| **Signal Frequency** | High | Low |
| **Signal Quality** | Medium | High |
| **Suitable For** | Fast-paced markets | Stable trends |

### 11.2 How to Choose?

- **Want more trading opportunities** → PRICEFOLLOWING
- **Want more reliable signals** → PRICEFOLLOWING2
- **Beginners** → PRICEFOLLOWING2 (more stable)
- **Experienced** → Try both, see which fits you

---

## XII. The Final End

### One-Line Review
> "Steady version of moving average following strategy, fewer signals but higher quality, for those who want steady not fast gains"

### Who Should Use It?
- ✅ People who want stable signals
- ✅ People who don't like frequent trading
- ✅ Trend-dominated trading environments
- ✅ People willing to wait for opportunities

### Who Shouldn't Use It?
- ❌ People who want high-frequency trading
- ❌ Oscillating market environments
- ❌ People who need shorting mechanism
- ❌ Impatient people

### Manual Trader Recommendations
If you don't run a bot and want to manually trade similar logic:
1. Use 15-minute chart
2. Set EMA7 and TEMA(7)
3. Wait for moving average crossover
4. Check price and EMA difference ratio
5. Only enter after multiple confirmations

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Part)

### Backtest Looks Beautiful, Live Trading Be Careful

PRICEFOLLOWING2's multiple confirmations look great—**but this has problems too**:

> **Fewer signals, you might get "itchy hands" and adjust parameters, making it worse.**

Simply put: **The cost of being steady is fewer opportunities, you might get anxious waiting**

### Hidden Risks of Complex Strategies

Although it's the "steady version", live trading might encounter:
- **Too Few Signals**: Might go days without a trading signal
- **Missing Opportunities**: Price already ran away while waiting for confirmation
- **Psychological Issues**: Watching others frequently trade and make money while you just wait

### My Recommendations (Honest Words)

```
1. Accept low-frequency trading, don't adjust parameters just to "do something"
2. Set reasonable stop loss, better small loss than big loss
3. Use multiple trading pairs to spread, increase opportunities
4. Be patient waiting, this is the characteristic of steady strategies
5. Can combine with PRICEFOLLOWING, one fast one steady
```

**Remember**: Being steady isn't everything, sometimes the market needs quick reactions. PRICEFOLLOWING2 is for traders who prefer "quality over quantity." If you're impatient, stick with PRICEFOLLOWING!

---