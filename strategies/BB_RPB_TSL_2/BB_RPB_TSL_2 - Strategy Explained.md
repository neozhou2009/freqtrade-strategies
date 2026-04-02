# BB_RPB_TSL_2 Strategy: The Bollinger Band Player's 28 Tricks

> **Nickname**: The Quant World's Player, Condition Maniac  
> **Occupation**: Oversold Bottom-Fisher + Trend Pullback + Bollinger Band Breakout All-Rounder  
> **Timeframes**: 3 minutes (main) + 5 minutes + 1 hour (info layer)

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_2** is:
- A "player" strategy with 28 buy conditions
- Uses Bollinger Bands to find oversold points, uses trends to find pullback points
- A "greedy ghost" where the more profit, the tighter the stop loss

Like a Virgo checking backgrounds on dates—**so many conditions you'll question your life choices** 🤣

---

## II. Core Configuration: Simply Put, "Make 20% Then We'll Talk"

### Take-Profit Rules (ROI Table)

```
Profit reaches 20.5% → Sell everything
```

**Translation**: This strategy's goal is to make 20%. How much you can make in between depends on the market. Anyway, once you've made enough, run.

### Stop Loss Rules

```
Fixed stop loss: -15% (backup, rarely used)
Tiered trailing stop loss:
  Profit > 20% → Only allow 5% pullback
  Profit > 10% → Only allow 3% pullback
  Profit > 6%  → Only allow 2% pullback
  Profit > 3%  → Only allow 1.5% pullback
```

**Translation**: Like a greedy landlord—once rent goes up, they don't want it to go down. The more it goes up, the harder it is to lower. After making 20%, only allow 5% pullback. After making 10%, only allow 3% pullback.

---

## III. 28 Buy Conditions: I've Categorized Them for You

This strategy has **an outrageous number** of buy conditions. I've grouped them into 7 major categories:

### 🎯 Category 1: Bollinger Band Breakout (4 conditions)

**Core Logic**: Price breaks below lower Bollinger Band + various oversold indicator confirmations

**Plain English**:
> "Price gets pushed to the bottom of the Bollinger Band, RMI, CCI, Stochastic RSI all say 'oversold, oversold'—time to buy like picking up cheap goods."

**Representative Conditions**:
- **#1 BB_checked**: Dip (oversold) + Break (breakout) combo
  > RMI < 49 + CCI < -116 + Stochastic RSI < 32 + BB width > 0.095

**Classic Lines**:
- Condition #1: `price < BB lower band 3 std dev * 0.999` → "Dropped to hell, time to bottom fish!"

---

### 📉 Category 2: Trend Pullback (4 conditions)

**Core Logic**: EMA26 > EMA12 (short-term downtrend) + price touches lower Bollinger Band

**Plain English**:
> "Short-term moving average is below, meaning it's been falling recently. But falling to the lower Bollinger Band might mean the pullback is over."

**Representative Conditions**:
- **#2 Local Uptrend**: EMA downtrend + lower Bollinger Band touch
  > EMA26 > EMA12 + price < BB lower band 2 std dev

- **#3 Local Dip**: Local decline + RSI oversold
  > RSI < 21 + CRSI > 10 → "RSI says oversold, but CRSI says not that extreme, can buy"

---

### 🌊 Category 3: Elliott Wave (4 conditions)

**Core Logic**: EWO (Elliott Wave Oscillator) positive + RSI oversold = trend reversal signal

**Plain English**:
> "EWO says 'the wave is about to reverse', RSI says 'truly oversold'—buying now is like catching the bottom of a wave."

**Representative Conditions**:
- **#4 EWO**: EWO > -5 + RSI fast < 44 + RSI < 23
  > "EWO hasn't fully turned positive yet, but is already above -5, meaning the wave is about to reverse"

- **#5 EWO_2**: 1-hour EMA200 consecutively rising + EWO > 4
  > "Big trend is up, small wave pullback, time to bottom fish"

---

### 🐟 Category 4: Inverse Dead Fish (2 conditions)

**Core Logic**: Long-term moving averages in bearish alignment + Bollinger Band width expanding + volume increasing

**Plain English**:
> "Dead Fish is normally a liquidity-exhausted dead fish pattern. Here we use it in reverse—bearish moving averages but Bollinger Band width expanding and volume increasing, meaning despite the bad trend, money is flowing in, possible reversal."

**Representative Conditions**:
- **#6 R_Deadfish**:
  > EMA100 < EMA200 + BB width > 0.299 + volume increasing + CTI < -0.115

  > "Although long-term moving averages are in bearish alignment, BB width, volume, and CTI all say 'signs of reversal'"

---

### 🎌 Category 5: ClucHA (2 conditions)

**Core Logic**: Heikin Ashi Bollinger Band breakout + 1h ROCR strength confirmation

**Plain English**:
> "Heikin Ashi is a special type of candlestick, smoother. Price breaks below HA lower Bollinger Band, while 1h ROCR says 'recent price change rate is high'—time to buy."

**Representative Conditions**:
- **#7 ClucHA**:
  > HA close < BB40 lower band + ROCR_1h > 0.526

  > "Smooth candlestick breaks below Bollinger Band, 1-hour price change rate is high, bottom fish"

---

### 🎯 Category 6: COFI (2 conditions)

**Core Logic**: Stochastic Fast golden cross + ADX trend strength + extremely high EWO value

**Plain English**:
> "COFI conditions are the most demanding—Stoch golden cross (short-term MA crosses above long-term) + ADX says there's a trend + EWO says wave reversal + CTI and Williams %R both say oversold."

**Representative Conditions**:
- **#8 COFI**:
  > fastk crosses above fastd + fastk < 39 + ADX > 13 + EWO > 8.594 + CTI < -0.892 + r_14 < -85

  > "Stoch golden cross but values not too high, ADX says there's a trend but not too strong, EWO high positive, CTI and Williams %R extremely oversold—this isn't bottom fishing, this is 'bottom fishing on the tip of a diamond'"

---

### 🔮 Category 7: NFI/NFIX Series (8 conditions)

**Core Logic**: Various oversold bottom-fishing combinations from the NFI (Next Gen) series

**Plain English**:
> "NFI series is another strategy's buy conditions from the community, 'borrowed' a few here. The core is: CTI extremely oversold + EWO/RSI confirmation + 1h indicator filtering."

**Representative Conditions**:
- **#9 NFI_13**:
  > EMA50_1h > EMA100_1h + CTI < -0.92 + EWO < -5.585 + CTI_1h < -0.88

  > "1h moving averages in bullish alignment but 3m CTI and EWO both say extremely oversold, bottom fish"

- **#14 NFIX_49**:
  > Conditions are calculated with 3-period delay—shift(3) series conditions

  > "This isn't a real-time condition, it's a combination from 3 candles ago. Meaning 'conditions were met 3 candles ago, place order now'."

---

## IV. Protection Mechanism: 2 Layers of "Security Check"

Every buy signal must pass 2 security checks before placing an order:

| Protection Type | Function | Plain English |
|-----------------|----------|----------------|
| **ROC_1h** | 1-hour rate of change limit | "1-hour price change can't be too big, prevent chasing highs" |
| **BB_width_1h** | 1-hour Bollinger Band width limit | "1-hour BB can't be too wide, prevent extreme volatility" |

```python
is_additional_check = (
    (roc_1h < 86) & (bb_width_1h < 0.954)
)
```

> "These two conditions are like airport security—no matter what VIP you are, you have to go through security to board."

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
- After 20% profit: Only allow falling back to 15%, otherwise sell
- After 10% profit: Only allow falling back to 7%, otherwise sell
- After 6% profit: Only allow falling back to 4%, otherwise sell
- After 3% profit: Only allow falling back to 1.5%, otherwise sell

---

### 5.2 Profit Trailing Sell (12 signals)

| Profit Range | Trigger Condition | Plain English |
|--------------|-------------------|----------------|
| 0-1.2% | Max profit > current + 4.5%, RSI < 46 | "Was up 4.5%, now only 1%, RSI says momentum weak, run" |
| 0-1.2% | Max profit > current + 2.5%, RSI < 32 | "RSI extremely low, run" |
| 1.2-2% | CMF double-period negative | "Money outflow confirmed on both periods, run" |
| 1.2-2% | CTI_1h > 0.8 + CMF negative | "1h CTI high + CMF negative, run" |

---

### 5.3 Special Exit Scenarios

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|----------------|
| **MOMDIV** | momdiv_sell = True | "Momentum divergence, trend reversal signal" |
| **Quick Take Profit** | profit 2-6%, RSI > 80 | "RSI extremely high, overbought, run fast" |
| **Extreme CTI** | profit 2-6%, CTI > 0.95 | "CTI near 1, extremely high, run" |
| **PMAX** | PMAX indicator breaks threshold | "Profit maximization indicator triggered" |
| **Dead Fish Stop Loss** | profit < -5%, BB width low | "Lost 5% and liquidity dried up, stop loss" |
| **Emergency Stop Loss** | profit < -5%, CMF/EMA combination | "Lost 5% and money outflow confirmed, stop loss" |

---

## VI. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Section)

1. **Wide Coverage**: 28 buy conditions, can almost bottom-fish any pattern
2. **Intelligent Stop Loss**: Tiered trailing stop loss, more profit means tighter protection
3. **Strict Verification**: Slippage confirmation + additional checks, filter low-quality signals
4. **Cross-Period Confirmation**: 5m + 1h info layers, more reliable signals
5. **Tunable Parameters**: Supports Hyperopt optimization

### ⚠️ Disadvantages (Complaint Section)

1. **Too Many Conditions**: 28 conditions, optimizing parameters is exhausting
2. **High Computation**: Three-timeframe indicator calculations, high CPU consumption
3. **Overfitting Risk**: Historical backtest may be inflated, live trading may slap you
4. **High Fees**: 3m frame high-frequency trading, transaction costs need attention
5. **High Learning Cost**: 800 lines of code, understanding each condition takes time

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
> "The quant world's player, 28 buy conditions covering all bottom-fishing patterns, but so many conditions you can't even remember them yourself."

### Who Is It For?
- ✅ Experienced quantitative traders
- ✅ Those with adequate hardware resources (multi-core CPU, 16GB+ RAM)
- ✅ Those with deep understanding of Hyperopt parameter optimization
- ✅ Those who can accept high-frequency trading fees

### Who Is It NOT For?
- ❌ Beginners (too many conditions, hard to understand)
- ❌ Users with insufficient hardware
- ❌ Manual traders (28 conditions real-time judgment impossible)
- ❌ Users on low-fee exchanges (high-frequency trading fees are high)

### My Advice
1. **Backtest first**: Verify strategy performance with historical data
2. **Small position live testing**: Don't go all-in right away
3. **Adjust stop loss parameters**: Adjust stop loss range based on coin volatility
4. **Watch transaction fees**: High-frequency trading fee costs need attention

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Bottom-Fishing Net" with Multiple Conditions

BB_RPB_TSL_2 is a typical "bottom-fishing strategy". 28 buy conditions are like a bottom-fishing net—catching every pattern.

**Its Money-Making Philosophy**:
- Oversold? Fish it: Lower Bollinger Band + RSI/CCI oversold
- Trend pullback? Fish it: EMA downtrend + price touches Bollinger Band
- Wave reversal? Fish it: EWO positive + RSI oversold
- Money flowing in? Fish it: Inverse Dead Fish + volume increasing

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | "Trend pullback bottom-fishing, tiered stop loss protects profits, easy money" |
| 🔄 Oscillating Market | ⭐⭐⭐⭐☆ | "Bollinger Band upper and lower bounds back and forth, high-frequency small profits" |
| 📉 Slow Bear Decline | ⭐⭐⭐☆☆ | "Bottom-fishing halfway down the mountain, stop loss may trigger too early" |
| ⚡️ Rapid Crash | ⭐☆☆☆☆ | "Liquidity exhaustion, Dead Fish stop loss fails, get slapped" |
| 📊 Sideways Consolidation | ⭐⭐☆☆☆ | "Few condition triggers, low capital utilization, waste of time" |

**One-Line Summary**: Suitable for oscillating pullback markets, not suitable for one-sided crash markets.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|--------------------|-------------------|---------|
| Number of Trading Pairs | 10-30 | "Diversify risk, don't go all-in on one coin" |
| stake_amount | Dynamic or small fixed | "High-frequency trading control single position size" |
| max_slip | 0.33%-0.50% | "Balance execution rate with price protection" |

### 10.2 Hardware Requirements (Important!)

This strategy has massive computation, with requirements for VPS memory:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 10-20 | 4 GB | 8 GB | "Can run, but CPU might lag" |
| 30-50 | 8 GB | 16 GB | "Smooth operation" |
| 50+ | 16 GB | 32 GB | "Multi-core CPU acceleration" |

**Warning**: Three-timeframe indicator calculations will cause high CPU load. Old computers might lag 😅

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

1. **Mirrored Conditions**: 14 conditions on 3m frame fully replicated on 5m frame
   > "The author really wanted to cover all patterns, even replicated the timeframe"

2. **Delayed Conditions**: NFIX_49 uses shift(3) to delay 3 candles
   > "Conditions met 3 candles ago, place order now. Author afraid of chasing highs?"

3. **Dead Fish Used in Reverse**: Originally a stop loss signal, here used as buy signal
   > "Author thinks liquidity exhaustion is actually a bottom-fishing opportunity? Contrarian thinking"

4. **Tiered Stop Loss Precise to Decimals**: 1.5% stop loss
   > "Profit rate calculation precise to decimals, this isn't something manual trading can do"

---

## XII. Final Words

### One-Line Review
> "Player strategy, 28 buy conditions covering all bottom-fishing patterns, but so many conditions it's exhausting. Suitable for experienced quant players, not for beginners and manual traders."

### Who Is It For?
- ✅ Experienced quantitative traders
- ✅ Those with adequate hardware resources
- ✅ Those who can accept high-frequency trading fees
- ✅ Those with deep understanding of parameter optimization

### Who Is It NOT For?
- ❌ Beginners
- ❌ Users with insufficient hardware
- ❌ Manual traders
- ❌ Users on low-fee exchanges

### Manual Trader Advice
Manual traders are not recommended to attempt replicating this strategy:
- 28 conditions real-time judgment is nearly impossible
- Tiered stop loss requires precise calculation of current profit rate
- Multi-timeframe switching judgment is difficult
- Slippage confirmation requires real-time monitoring of order execution prices

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtests Are Beautiful, Live Trading Requires Caution

BB_RPB_TSL_2's historical backtest performance is often **extremely excellent**—but there's a trap:

> **Because of 28 conditions, the strategy easily "fits" the optimal solution for past market conditions, but this doesn't mean it will definitely be profitable in the future.**

Simply put: **Memorized answers to get full marks, but may not pass a new test.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Order Delays**: Signal trigger to order placement may delay several seconds, missing best prices
- **Slippage Beyond Expectations**: Actual execution price may be 1-2% worse than expected
- **Insufficient Liquidity**: In extreme markets, may not be able to exit at expected prices
- **Chain Stop Loss Triggers**: Multiple conditions triggering may cause consecutive stop losses

### My Advice (Honest Words)

```
1. Backtest with historical data first, see if performance is stable
2. Live test with small amount for at least 7 days
3. Watch transaction fee costs, high-frequency trading may eat profits
4. Don't go all-in right away, light position testing is most important
```

**Remember**: No matter how good the strategy is, the market will teach you a lesson without warning. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: This strategy has so many conditions it's exhausting, but if you have experience, hardware, and patience, it might be a good choice. **But don't be fooled by backtest data, live verification is king!**