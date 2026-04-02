# TemaPure Strategy: The "Range Catcher" in Bollinger Bands

> **Nickname**: Range Catcher  
> **Occupation**: Bollinger Lower Band Bottom-Fishing Specialist  
> **Timeframe**: 5 minutes (Just the right pace)

---

## I. What is This Strategy?

Simply put, **TemaPure** is:
- A bottom-fisher waiting for bargains at the Bollinger lower band
- A "confirmationist" who waits for momentum to turn positive before acting
- A "range player" who buys at lower band and sells at upper band

Like waiting during store sales season, buying when the price drops below your mental price point, then selling when it hits the high point 🛍️

---

## II. Core Configuration: "Patient Money Making"

### Take Profit Rules (Four-Level ROI Table)

```
0 minutes: Make 40.5% and run (greedy version)
265 minutes (~4.4 hours): 24.7% is fine too
743 minutes (~12.4 hours): 5.9% is acceptable
1010 minutes (~16.8 hours): Break even and run
```

**Translation**: This strategy is very patient! Target is 40% when just entering, but the longer you hold, the lower the target gets. After 17 hours without making money, exit at break-even.

### Stop Loss Rules

```
Hard stop loss: -9.75% (Cut losses here)
Trailing stop: Activates after 21.26% profit, almost locks in all profits
```

**Translation**: Once profit exceeds 21%, trailing stop follows closely, almost never letting profits escape.

---

## III. 1 Buy Condition: This Strategy is Very "Picky"

Although there's only one buy condition, it's double confirmation:

### 🎯 Buy Condition: TEMA Touches Bollinger Lower Band + CMO Momentum Turns Positive

**Technical Implementation**:
```python
# TEMA is below or equal to Bollinger lower band TA
# AND CMO crosses above 0 from below
```

**Plain English Translation**:
> "Price has fallen outside or right on the Bollinger lower band, meaning it's oversold. But don't rush - wait for CMO momentum indicator to go from negative to positive, meaning the trend is starting to strengthen, then get on board!"

**Simple Understanding**:
- TEMA <= lower band = price is "cheap"
- CMO crosses above 0 = momentum goes from negative to positive, trend confirmed
- Both conditions together = not a dead cat bounce, real rebound

---

## IV. 1 Sell Signal: Simple and Direct, Run at Upper Band

Sell logic is very simple:

### Sell Signal

| Signal | Trigger Condition | Plain English |
|--------|-------------------|----------------|
| **Sell** | TEMA crosses above Bollinger upper band TA | "Enough gains, run!" |

**Plain English Translation**:
> "Price has gone outside the Bollinger upper band, meaning it's overbought, might be topping out, quickly sell and lock in gains."

### An Interesting Design

This strategy's Bollinger parameters are "asymmetric":

| Position | Standard Deviation Multiplier | Function |
|----------|------------------------------|----------|
| **Upper band** | 3.5x | Very loose, price needs to rise a lot to sell |
| **Lower band** | 1.0x | Very strict, price barely oversold triggers |

**Translation**:
- Buying is very cautious (tightened lower band, doesn't buy easily)
- Selling is very lenient (loosened upper band, gives price more upside room)
- Result: Longer holding time, capturing larger trends

---

## V. Technical Indicators: How Does This Strategy "Read the Market"?

### Core Indicators

| Indicator | Parameter | Function |
|-----------|-----------|----------|
| **TEMA** | 25 period | Triple Exponential Moving Average, judging price position |
| **Bollinger TA** | 25 period, upper 3.5/lower 1.0 std | Asymmetric range, used for buy/sell signals |
| **CMO** | 50 period | Momentum confirmation, identifying trend transition |

### Also a Set of Unused Bollinger

```python
# Standard Bollinger (window 25, standard deviation 2.0)
# But completely unused in code!
```

> Like buying two sets of tools but only using one 🤣

Could be legacy, or author changed their mind later.

---

## VI. Strategy "Personality Traits"

### ✅ Pros (Praise Section)

1. **Cautious Entry**: Asymmetric Bollinger + CMO dual confirmation, not easy to step into traps
2. **Large Holding Space**: Upper band loosened to 3.5x standard deviation, giving price full upside room
3. **Flexible Take-Profit**: Four-level ROI combined with trailing stop, can lock in profits
4. **Clear Logic**: Buy at lower band, sell at upper band, complete range trading logic

### ⚠️ Cons (Criticism Section)

1. **Too Simple Selling**: Only looks at TEMA crossing upper band, no momentum confirmation
2. **No Weakness Exit**: Unlike other strategies with "dropped too much, run" logic
3. **Fewer Signals**: Strict buy conditions, might not have signals for days
4. **May Hold Too Long**: Lenient sell condition, sometimes never gets there

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Sideways Oscillation** | ✅ First choice | Upper and lower bands touched repeatedly, perfect for range trading |
| **Slow Bull Trend** | ✅ Recommended | Loose upper band design, can catch the trend |
| **Trending Down** | ❌ Use cautiously | CMO filter may not be enough, risk of catching falling knives |
| **Extreme Volatility** | ⚠️ Adjust parameters | Standard deviation may need adjustment |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "Bollinger range catcher, steady player in oscillating markets, cautious buyer and lenient seller."

### Who Should Use It?
- ✅ People who like range trading
- ✅ Patient investors (few signals but high quality)
- ✅ People pursuing steady returns
- ✅ Technical analysts familiar with Bollinger and momentum indicators

### Who Shouldn't Use It?
- ❌ People who like high-frequency trading
- ❌ People pursuing short-term quick profits
- ❌ People without patience to wait for signals
- ❌ One-sided trend enthusiasts

### My Advice
1. **Choose Right Pairs**: Medium volatility pairs work best
2. **Be Patient**: Strict buy conditions, don't rush
3. **Trust the Strategy**: Loose upper band is by design, don't sell manually too early
4. **Adjust Parameters**: Different pairs may need different Bollinger parameters

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Range Trading Expert

TemaPure is a **pure range strategy**. The logic is clear:

- **Wait**: Price falls near Bollinger lower band
- **Confirm**: CMO momentum goes from negative to positive
- **Buy**: Both conditions met, enter position
- **Hold**: Patiently wait for price to reach upper band
- **Sell**: TEMA crosses above Bollinger upper band, run

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 **Slow Bull Trend** | ⭐⭐⭐⭐☆ | Loose upper band design can catch most of the trend |
| 🔄 **Sideways Oscillation** | ⭐⭐⭐⭐⭐ | Home territory! Upper and lower bands hit repeatedly, make range money |
| 📉 **Trending Down** | ⭐⭐☆☆☆ | CMO filter is limited, might bottom-fish halfway down |
| ⚡️ **High Volatility** | ⭐⭐⭐☆☆ | Fewer signals but high quality, needs patience |

**One-Sentence Summary**: Make range money in oscillating markets, can catch mild trends, don't touch trending down markets.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Timeframe | 5 minutes | Not too fast, not too slow, just right |
| Number of Trading Pairs | 5-20 pairs | Few signals, configure more |
| Liquidity | Medium or above | Don't touch too obscure coins |

### 10.2 Key Configuration File Settings

```yaml
# Key configurations
timeframe: '5m'
stake_currency: 'USDT'

# Stop loss and take profit
stoploss: -0.09754
minimal_roi: 
  0: 0.40505
  265: 0.24708
  743: 0.05892
  1010: 0

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.2126
trailing_stop_positive_offset: 0.2225
```

### 10.3 Hardware Requirements (Reasonable)

5-minute timeframe isn't too demanding:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 pairs | 4GB | 8GB | Smooth |
| 10-20 pairs | 8GB | 16GB | No problem |
| 20+ pairs | 16GB | 32GB+ | Rock solid |

### 10.4 Backtest vs Live Trading

Range strategy backtest and live trading gap is relatively small:
- Bollinger parameters sensitive to specific pairs
- Recommend adjusting parameters for different pairs

**Recommended Process**:
1. Test Bollinger parameters with historical data
2. Optimize standard deviation multipliers for specific pairs
3. Small capital live trading verification
4. Gradually increase position

---

## XI. Bonus: The Strategy Author's "Little Tricks"

Looking carefully at the code, you'll find some interesting things:

1. **Asymmetric Bollinger**: Lower band 1.0x standard deviation, upper band 3.5x
   > "Author is very 'greedy', wants to buy cheap, sell higher!"

2. **Two Sets of Bollinger**: One standard (2.0x), one asymmetric
   > "The standard set is completely unused, probably legacy from early versions"

3. **Commented Out Sell Condition**:
   ```python
   # (qtpylib.crossed_below(dataframe['close'], dataframe['bb_upperbandTA']))
   # & (dataframe["CMO"] >= 35)
   ```
   > "Author originally wanted CMO > 35 to sell, then changed their mind"

---

## XII. Final Words

### One-Sentence Review
> "Range trading steady player, picky buyer and lenient seller, money-making tool for oscillating markets."

### Who Should Use It?
- ✅ Range trading enthusiasts
- ✅ Patient investors
- ✅ People pursuing steady returns
- ✅ 5-minute timeframe players

### Who Shouldn't Use It?
- ❌ High-frequency trading fans
- ❌ People pursuing short-term quick profits
- ❌ People without patience to wait for signals
- ❌ One-sided trend chasers

### Manual Trader Advice

This strategy **can be executed manually**:
- 5-minute timeframe is quite friendly
- Clear signal conditions
- Use TradingView to set alerts
- Strictly execute according to signals

Manual execution tips:
1. Load Bollinger and CMO indicators on TradingView
2. Set alert for TEMA touching lower band + CMO crossing above 0
3. Set alert for TEMA touching upper band for sell
4. Execute quickly when alert received

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Backtests Are Beautiful, Live Trading Needs Caution

TemaPure's backtest may look steady - but range strategies have their traps:

> **Bollinger parameters are very sensitive to specific trading pairs, the same parameters can perform very differently on different pairs.**

Simply put: **Parameters that make money on BTC might lose money on altcoins.**

### Hidden Risks of Range Strategies

In live trading, range strategies may cause:
- **Breakout Failure**: Price breaks through Bollinger band and may continue, won't pull back every time
- **Parameter Sensitivity**: Standard deviation multiplier slightly off, signals may be very different
- **Trend Risk**: In one-sided trends, range strategies get slapped repeatedly

### My Advice (Heartfelt)

```
1. Test Bollinger parameters for specific pairs with historical data first
2. Asymmetric design may not suit all pairs, try adjusting
3. Add enough slippage and fees during backtesting
4. Live trade with small capital first, run at least a month
```

**Remember**: Range strategies make money in oscillating markets, lose money in trending markets. Recognizing current market environment is most important!

---

**Final Reminder**: Range catcher, picky buyer and lenient seller, money-making tool in oscillating markets, be careful of getting trapped in trending markets! 🙏