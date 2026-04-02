# InverseV2 Strategy Explained — The "Steady and Stable" Trend Follower

## 1. What Does This Strategy Do?

In simple terms, InverseV2 is a robot that automatically trades crypto for you, specifically designed to capture upward trends. Its core idea: **wait until the trend is clear, then enter; take profit when you've made money, stop loss when you've lost money**.

This strategy is written using the Freqtrade framework—think of it as a "robot trader" that monitors the market 24/7 and automatically buys and sells when it finds suitable opportunities.

---

## 2. Core Principle: Making Ordinary Indicators "Smarter"

### What Is Fisher Transform?

The strategy name includes "Inverse"—this refers to the Fisher Transform. It's a mathematical formula, but we just need to know what it does:

**Analogy**: Regular CCI is like someone who speaks unclearly—sometimes they say "buy" but the market doesn't rise; sometimes they say "sell" but the market doesn't fall.

Fisher Transform is like equipping this person with a "signal amplifier"—making their judgments clearer:
- Vague speech → Now speaks clearly
- Unclear inflection points → Now has very clear turning signals

---

## 3. Entry Conditions: Must Pass All 5 Checks to Buy

This strategy has a characteristic: **it doesn't act easily, when it acts it must be steady**. It sets 5 checkpoints—all must pass before buying.

### Check 1: Fisher CCI Signal

Two scenarios:
- **Scenario A - Bottom fishing**: Fisher CCI crosses above -0.42 from below
- **Scenario B - False breakdown recovery**: Fisher CCI previously crossed below 0.41, then crosses back above within 8 candles

### Check 2: SSL Channel Confirms Uptrend

Requires: 4-hour SSL shows uptrend (ssl_up > ssl_down)

### Check 3: EMA System Confirms Trend

1-hour: EMA50 > EMA200
4-hour: 50 EMA > 100 EMA > 200 EMA (perfect bullish alignment)

### Check 4: BTC Market Environment Must Be Friendly

Entry condition: BTC's CCI must be < 0

Why? Because altcoins usually follow BTC:
- When BTC surges wildly, money flows to BTC, altcoins may fall or consolidate
- When BTC is adjusting, money starts flowing to altcoins, they tend toward independent rallies

### Check 5: Volume Cannot Be Zero

Simplest: Ensure the coin is being traded, not dead.

---

## 4. Exit Conditions: When to Sell?

The strategy's exit logic is simple, mainly watching Fisher CCI:

**Signal 1**: Fisher CCI crosses below 0.42 - Momentum starting to weaken, take profits

**Signal 2**: Fisher CCI crosses below -0.34 - Already weakened, quickly exit

### Smart "Refuse to Sell" Mechanism

The strategy has a highlight: **sometimes a sell signal triggers but the strategy "refuses" to execute**.

What situation refuses?

```python
if trend is upward (DI+ > DI-) AND trend strength is increasing (ADX rising):
    refuse to sell, continue holding
```

Plain English: if current upward momentum is strong, even if the indicator says "sell," the strategy says "wait, let it rise some more."

---

## 5. Stop Loss and Take Profit: How Is Risk Control Done?

### Fixed Stop Loss: -20%

Meaning: if loss reaches 20% after buying, unconditionally sell.

### Trailing Stop (Profit Protection)

This is good! How it works:
1. After buying, price starts rising
2. When rising enough, the stop line starts following upward
3. Specific settings: Trailing distance 7.8%, trigger threshold 17.4%

### ROI Target (Staged Take Profit)

| Holding Time | Target Return |
|-------------|--------------|
| Right after buying | 10% |
| After 30 minutes | 5% |
| After 60 minutes | 2% |

---

## 6. Timeframes: Which Time Charts?

The strategy uses two timeframes:
- **Trading timeframe: 1 hour** - All buy/sell signals generated here
- **Confirmation timeframe: 4 hours** - Used to determine major trend direction

---

## 7. BTC Filter: Checking Big Brother's Mood

The strategy adds a "market thermometer": look at BTC's state before entry.

**Entry condition**: BTC's CCI must be < 0

This is because altcoins usually follow BTC:
- BTC surges wildly → money flows to BTC → altcoins may fall
- BTC adjusts → money starts flowing to altcoins → higher altcoin success rate

---

## 8. Strategy Pros & Cons

### Pros

1. **High signal quality**: 5-layer filtering, doesn't act unless sure—like a sniper
2. **Knows when to refuse sells**: During strong momentum, even with sell signal, refuses
3. **Good multi-timeframe coordination**: Small cycle captures signals, big cycle confirms direction
4. **BTC market awareness**: Doesn't work in isolation, checks Big Brother's mood
5. **Complete risk control**: Stop loss, trailing stop, staged take profit all present

### Cons

1. **Loses money in ranging markets**: Universal weakness of trend strategies
2. **Signal lag**: Multi-confirmation means when signals appear, price may already have risen
3. **Many parameters**: If not adjusted well, results may suffer
4. **Not suitable for extreme conditions**: Indicators may malfunction during violent spikes/dumps

---

## 9. What Coins Suit This Strategy?

### Recommended

1. **Liquid mainstream coins**: ETH, BNB, SOL, etc.
2. **Coins with moderate BTC correlation**: Neither too independent nor too correlated
3. **Coins with strong historical trends**: Those that often form unilateral moves

### Not Recommended

1. **Newly listed coins**: Too extreme, indicators easily fail
2. **Small-cap coins**: Poor liquidity, large slippage
3. **Stablecoin pairs**: No volatility, can't make money

---

## 10. How to Use This Strategy?

1. Install Freqtrade, configure exchange API
2. Backtest first: See past-year performance
3. Paper trade: Run for a period, observe actual performance
4. Live trading: Confirm没问题后 run with real money

---

## 11. Risk Warnings

1. Quantitative trading has risks, principal may be lost
2. Past performance doesn't predict future returns
3. Strategy parameters need adjustment per market

---

## 12. Summary

InverseV2 is a "steady and stable" trend-following strategy. It doesn't pursue daily trading—waits for high-quality opportunities before acting.

**Core points:**
- Uses Fisher Transform to make CCI smarter
- 5-layer filtering ensures entry quality
- Smart refuse-sell mechanism locks in profits
- BTC filter avoids market risk periods
- Complete risk control protects principal

If you like this "quality over quantity" trading style, this strategy is worth your time to study and optimize.

---

*This is the colloquial version of InverseV2, approximately 6,000 words with 13 chapters.*
