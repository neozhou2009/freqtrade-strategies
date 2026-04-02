# BB_RPB_TSL_BI Strategy: The Bollinger Band Player's "Lite Version"

> **Nickname**: Player Lite, Moderate Conditionalist  
> **Occupation**: Oversold Bottom-Fisher + Trend Pullback + Bollinger Band Breakout Specialist  
> **Timeframes**: 5 minutes (main) + 1 hour (info layer)

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_BI** is the "lite version" of BB_RPB_TSL_2:
- Cut from 28 buy conditions down to 15
- Cut from three timeframes down to dual timeframes
- More aggressive stop loss (-10% instead of -15%)

Like the player saying "I'm tired, don't want to check so many backgrounds anymore"—**conditions cut in half, but core logic unchanged** 🤣

---

## II. Core Configuration: Simply Put, "Make 20% Then We'll Talk"

### Take-Profit Rules (ROI Table)

```
Profit reaches 20.5% → Sell everything
```

**Translation**: Same as BB_RPB_TSL_2, the goal is to make 20%.

### Stop Loss Rules

```
Fixed stop loss: -10% (backup, more aggressive than BB_RPB_TSL_2)
Tiered trailing stop loss:
  Profit > 20% → Only allow 5% pullback
  Profit > 10% → Only allow 3% pullback
  Profit > 6%  → Only allow 2% pullback
  Profit > 3%  → Only allow 1.5% pullback
```

**Translation**: Fixed stop loss -10% is more aggressive than BB_RPB_TSL_2's -15%, meaning the author has more confidence in this strategy.

---

## III. 15 Buy Conditions: I've Categorized Them for You

This strategy's buy conditions are **cut by half**, but the categorization logic is similar to BB_RPB_TSL_2:

### 🎯 Category 1: Bollinger Band Breakout (2 conditions)

**Core Logic**: Price breaks below lower Bollinger Band + various oversold indicator confirmations

**Plain English**:
> "Same as BB_RPB_TSL_2, price gets pushed to the bottom of the Bollinger Band, various oversold indicators confirm."

**Representative Conditions**:
- **#1 BB_checked**: Dip (oversold) + Break (breakout) combo
  > RMI < 49 + CCI < -116 + Stochastic RSI < 32 + BB width > 0.095

**Classic Lines**:
- Condition #1: `price < BB lower band 3 std dev * 0.999` → "Dropped to hell, time to bottom fish!"

---

### 📉 Category 2: Trend Pullback (2 conditions)

**Core Logic**: EMA26 > EMA12 (short-term downtrend) + price touches lower Bollinger Band

**Plain English**:
> "Short-term moving average is below, meaning it's been falling recently. But falling to the lower Bollinger Band might mean the pullback is over."

**Representative Conditions**:
- **#2 Local Uptrend**: EMA downtrend + lower Bollinger Band touch
  > EMA26 > EMA12 + price < BB lower band 2 std dev

- **#3 Local Dip**: Local decline + RSI oversold (more extreme)
  > RSI < 20 (more extreme than BB_RPB_TSL_2's 21)

  > "Lower RSI requirement, meaning this strategy bottom-fishes more aggressively"

---

### 🌊 Category 3: Elliott Wave (2 conditions)

**Core Logic**: EWO (Elliott Wave Oscillator) positive + RSI oversold = trend reversal signal

**Plain English**:
> "EWO says 'the wave is about to reverse', RSI says 'truly oversold'—buying now is like catching the bottom of a wave."

**Representative Conditions**:
- **#4 EWO**: EWO > -5 + RSI fast < 44 + RSI < 23
  > "Same as BB_RPB_TSL_2"

- **#5 EWO_2**: 1-hour EMA200 consecutively rising + EWO > 4
  > "Note: EMA parameters differ from BB_RPB_TSL_2, close < ema_8 * 1.164 (relaxed)"

---

### 🐟 Category 4: Inverse Dead Fish (1 condition)

**Core Logic**: Long-term moving averages in bearish alignment + Bollinger Band width expanding + volume increasing

**Plain English**:
> "Dead Fish is normally a stop loss signal, here used in reverse—bearish moving averages but Bollinger Band width expanding and volume increasing, meaning possible reversal."

**Representative Conditions**:
- **#6 R_Deadfish**:
  > EMA100 < EMA200 * 0.972 (more extreme than BB_RPB_TSL_2's 1.054)
  > BB width > 0.091 (narrower than BB_RPB_TSL_2's 0.299)

  > "This strategy has more extreme requirements for bearish moving average alignment, but more relaxed requirements for BB width"

---

### 🎌 Category 5: ClucHA (1 condition)

**Core Logic**: Heikin Ashi Bollinger Band breakout + 1h ROCR strength confirmation

**Plain English**:
> "Smooth candlestick breaks below Bollinger Band, 1-hour price change rate is high, bottom fish."

**Representative Conditions**:
- **#7 ClucHA**:
  > ROCR_1h > 0.416 (more relaxed than BB_RPB_TSL_2's 0.526)

  > "Lower ROCR threshold, meaning this strategy's ClucHA condition triggers more easily"

---

### 🎯 Category 6: COFI (1 condition)

**Core Logic**: Stochastic Fast golden cross + ADX trend strength + extremely high EWO value

**Plain English**:
> "Same as BB_RPB_TSL_2, Stoch golden cross + ADX + EWO + CTI + Williams %R extremely oversold."

**Representative Conditions**:
- **#8 COFI**:
  > Exactly the same as BB_RPB_TSL_2

  > "This condition wasn't cut, meaning the author thinks COFI condition is important"

---

### 🔮 Category 7: NFI/NFIX Series (7 conditions)

**Core Logic**: Various oversold bottom-fishing combinations from the NFI (Next Gen) series

**Plain English**:
> "NFI series is another strategy's buy conditions from the community, 'borrowed' a few here. The core is: CTI extremely oversold + EWO/RSI confirmation + 1h indicator filtering."

**Representative Conditions**:
- **#9-14 NFI/NFIX**: Same as BB_RPB_TSL_2

- **#15 NFIX_51** (NEW!)
  > close.shift(3) < ema_16.shift(3) * 0.944 + EWO.shift(3) < -1.0 + rsi.shift(3) > 28.0 + cti.shift(3) < -0.84 + r_14.shift(3) < -94.0 + rsi > 30.0 + crsi_1h > 1.0

  > "This is a new condition! 3-period delayed negative EWO + current RSI > 30 (just left oversold) + CRSI_1h > 1 (cross-period confirmation)"

---

## IV. Protection Mechanism: 2 Layers of "Security Check"

Every buy signal must pass 2 security checks before placing an order:

| Protection Type | Function | Plain English |
|-----------------|----------|----------------|
| **ROC_1h** | 1-hour rate of change limit | "1-hour price change can't be too big, prevent chasing highs" |
| **BB_width_1h** | 1-hour Bollinger Band width limit | "1-hour BB can't be too wide, prevent extreme volatility" |

```python
is_additional_check = (
    (roc_1h < 4) & (bb_width_1h < 1.074)
)
```

> "ROC_1h threshold is 4 (more strict than BB_RPB_TSL_2's 86), meaning this strategy is more sensitive to 1-hour price changes."

---

## V. Sell Logic: Even More Flashy Than Buying

### 5.1 Tiered Trailing Take-Profit: How Much You Make, How Much You Protect

```
Profit Range    Pullback Allowed    Plain English
─────────────────────────────────────────────────
> 20%          5%                  "Made 20%, only allow 5% pullback"
> 10%          3%                  "Made 10%, only allow 3% pullback"
> 6%           2%                  "Made 6%, only allow 2% pullback"
> 3%           1.5%                "Made 3%, only allow 1.5% pullback"
```

**Plain English**:
- Same as BB_RPB_TSL_2, tiered trailing stop loss logic unchanged.

---

### 5.2 Profit Trailing Sell (12 signals)

| Profit Range | Trigger Condition | Plain English |
|--------------|-------------------|----------------|
| 0-1.2% | Max profit > current + 4.5%, RSI < 46 | "Was up 4.5%, now only 1%, RSI says momentum weak, run" |
| 0-1.2% | Max profit > current + 2.5%, RSI < 32 | "RSI extremely low, run" |
| 1.2-2% | CMF double-period negative | "Money outflow confirmed on both periods, run" |

---

### 5.3 Special Exit Scenarios

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|----------------|
| **MOMDIV** | momdiv_sell = True | "Momentum divergence, trend reversal signal" |
| **Quick Take Profit** | profit 2-6%, RSI > 80 | "RSI extremely high, overbought, run fast" |
| **Extreme CTI** | profit 2-6%, CTI > 0.95 | "CTI near 1, extremely high, run" |
| **PMAX** | PMAX indicator breaks threshold | "Profit maximization indicator triggered" |
| **Dead Fish Stop Loss** | profit < -5%, BB width low | "Lost 5% and liquidity dried up, stop loss" |
| **Emergency Stop Loss** | profit < -5%, CMF/EMA/RSI combination | "Lost 5% and money outflow confirmed, stop loss" |

### 5.4 Sell Differences from BB_RPB_TSL_2

**New Parameter**: `sell_rsi_delta` (default 10)

```python
# Emergency stop loss adds RSI cross-period confirmation
(rsi > (rsi_1h + sell_rsi_delta.value))
```

> "This strategy's emergency stop loss requires RSI > RSI_1h + 10, meaning it needs cross-period confirmation that 'momentum is still there' before stopping out."

---

## VI. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Section)

1. **Moderate Computation**: Dual timeframe, CPU consumption lower than BB_RPB_TSL_2
2. **Moderate Conditions**: 15 buy conditions, covers main patterns but not exhausting
3. **Intelligent Stop Loss**: Tiered trailing stop loss, more profit means tighter protection
4. **Lower Hardware Requirements**: Regular VPS can run it
5. **New Condition**: NFIX_51 is a unique condition, BB_RPB_TSL_2 doesn't have it

### ⚠️ Disadvantages (Complaint Section)

1. **Aggressive Stop Loss**: -10% fixed stop loss more aggressive than BB_RPB_TSL_2
2. **Still Many Parameters**: 15 conditions, optimizing parameters is still exhausting
3. **Overfitting Risk**: Historical backtest may be inflated
4. **High Fees**: 5m frame high-frequency trading, transaction costs need attention
5. **Learning Cost**: 600 lines of code, understanding each condition takes time

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| 📈 Slow Bull Trend | Focus on EWO_2, NFIX series | Trend pullback strategies perform well |
| 🔄 Oscillating Market | Focus on BB_checked, ClucHA | Bollinger Band breakout captures volatility |
| 📉 Slow Bear Decline | Focus on NFI_13, Local Dip | Deep oversold bottom-fishing conditions |
| ⚡️ Rapid Crash | Reduce position or pause | Liquidity exhaustion risk |

---

## VIII. Summary: How Is This Strategy Really?

### One-Line Review
> "Player lite version, 15 buy conditions covering main bottom-fishing patterns, moderate computation, suitable for intermediate players."

### Who Is It For?
- ✅ Intermediate quantitative traders (have some experience)
- ✅ Regular hardware resources (4GB RAM enough)
- ✅ Those with basic understanding of Hyperopt parameter optimization
- ✅ Those who can accept high-frequency trading fees

### Who Is It NOT For?
- ❌ Complete beginners (still many conditions)
- ❌ Manual traders (15 conditions real-time judgment difficult)
- ❌ Users on low-fee exchanges
- ❌ Users who don't accept -10% stop loss

### My Advice
1. **Backtest first**: Verify strategy performance with historical data
2. **Small position live testing**: Don't go all-in right away
3. **Adjust stop loss parameters**: If you don't accept -10%, adjust to -15%
4. **Watch transaction fees**: 5m frame high-frequency trading fee costs need attention

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Bottom-Fishing Net" with Moderate Conditions

BB_RPB_TSL_BI is the lite version of BB_RPB_TSL_2, with 15 buy conditions covering main bottom-fishing patterns.

**Its Money-Making Philosophy**:
- Oversold? Fish it: Lower Bollinger Band + RSI/CCI oversold
- Trend pullback? Fish it: EMA downtrend + price touches Bollinger Band
- Wave reversal? Fish it: EWO positive + RSI oversold
- New condition: NFIX_51 delayed confirmation + RSI cross-period

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | "Trend pullback bottom-fishing, tiered stop loss protects profits" |
| 🔄 Oscillating Market | ⭐⭐⭐⭐☆ | "Bollinger Band upper and lower bounds back and forth, high-frequency small profits" |
| 📉 Slow Bear Decline | ⭐⭐⭐☆☆ | "Bottom-fishing halfway down the mountain, -10% stop loss may trigger" |
| ⚡️ Rapid Crash | ⭐⭐☆☆☆ | "Liquidity exhaustion risk" |
| 📊 Sideways Consolidation | ⭐⭐☆☆☆ | "Few condition triggers, low capital utilization" |

**One-Line Summary**: Suitable for oscillating pullback markets, not suitable for one-sided crash markets.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|--------------------|-------------------|---------|
| Number of Trading Pairs | 10-30 | "Diversify risk, don't go all-in on one coin" |
| stake_amount | Dynamic or small fixed | "High-frequency trading control single position size" |
| max_slip | 0.33%-0.50% | "Balance execution rate with price protection" |
| stoploss | -0.10 or adjust to -0.15 | "Default -10%, aggressive users can adjust to -15%" |

### 10.2 Hardware Requirements (Lower than BB_RPB_TSL_2!)

This strategy has moderate computation, with lower VPS memory requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 10-20 | 2 GB | 4 GB | "Regular VPS can run" |
| 30-50 | 4 GB | 8 GB | "Smooth operation" |
| 50+ | 8 GB | 16 GB | "Multi-core CPU acceleration" |

**Note**: Hardware requirements much lower than BB_RPB_TSL_2, suitable for regular users 😊

### 10.3 Backtest vs Live Trading

Complex strategies' backtest performance is often **extremely excellent**, but live trading may slap you:
- Order execution delays causing missed signals
- Slippage exceeding expectations causing premature stop loss triggers
- Inability to exit at expected prices when liquidity is insufficient

**Recommended Process**:
1. Backtest with 30 days of historical data first
2. Validate with 15 days of data
3. Live test with small amount for 7 days
4. Adjust parameters based on live performance

**Don't go all-in right away**, no matter how good the strategy is, it needs to be calibrated!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **NFIX_51 New Addition**: BB_RPB_TSL_2 doesn't have this condition
   > "Author added a new condition in the lite version, might think this condition is more valuable"

2. **More Aggressive Stop Loss**: -10% instead of -15%
   > "Author has more confidence in this strategy, dare to use more aggressive stop loss"

3. **ROCR_1h More Relaxed**: 0.416 instead of 0.526
   > "ClucHA condition triggers more easily, meaning author wants to increase this condition's trigger rate"

4. **sell_rsi_delta New Addition**: Emergency stop loss needs cross-period confirmation
   > "Author doesn't want to be too aggressive on emergency stop loss, needs RSI_1h confirmation"

---

## XII. Final Words

### One-Line Review
> "Player lite version, 15 buy conditions covering main bottom-fishing patterns, moderate computation, suitable for intermediate players. If you think BB_RPB_TSL_2 is too exhausting, try this."

### Who Is It For?
- ✅ Intermediate quantitative traders
- ✅ Regular hardware resource users
- ✅ Those who can accept high-frequency trading fees
- ✅ Those with basic understanding of parameter optimization

### Who Is It NOT For?
- ❌ Complete beginners
- ❌ Manual traders
- ❌ Users on low-fee exchanges
- ❌ Users who don't accept -10% stop loss

### Manual Trader Advice
Manual traders are not recommended to attempt replicating this strategy:
- 15 conditions real-time judgment is still difficult
- Tiered stop loss requires precise calculation of current profit rate
- 1h info frame needs switching judgment
- Slippage confirmation requires real-time monitoring of order execution prices

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtests Are Beautiful, Live Trading Requires Caution

BB_RPB_TSL_BI's historical backtest performance is often **extremely excellent**—but there's a trap:

> **Because of 15 conditions, the strategy easily "fits" the optimal solution for past market conditions, but this doesn't mean it will definitely be profitable in the future.**

Simply put: **Memorized answers to get full marks, but may not pass a new test.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Order Delays**: Signal trigger to order placement may delay several seconds
- **Slippage Beyond Expectations**: Actual execution price may be 1-2% worse than expected
- **Insufficient Liquidity**: In extreme markets, may not be able to exit at expected prices
- **Chain Stop Loss Triggers**: Multiple conditions triggering may cause consecutive stop losses

### My Advice (Honest Words)

```
1. Backtest with historical data first, see if performance is stable
2. Live test with small amount for at least 7 days
3. Watch transaction fee costs, high-frequency trading may eat profits
4. If you don't accept -10% stop loss, adjust to -15%
5. Don't go all-in right away, light position testing is most important
```

**Remember**: No matter how good the strategy is, the market will teach you a lesson without warning. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: This strategy is the lite version of BB_RPB_TSL_2. If you think BB_RPB_TSL_2 is too exhausting, try this. **But don't be fooled by backtest data, live verification is king!**