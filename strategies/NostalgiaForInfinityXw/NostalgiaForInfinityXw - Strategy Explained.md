# NostalgiaForInfinityXw Strategy Explained

## Foreword

This article explains the NostalgiaForInfinityXw cryptocurrency quantitative strategy in plain, simple language. Whether you're a complete beginner or an experienced trader looking to quickly grasp the strategy's core, this is for you.

---

## 1. What Does This Strategy Do?

Simply put, this is a program that **automatically buys and sells cryptocurrencies**.

Its core idea is: **when prices drop, buy in batches; when prices rise, sell in batches to make a profit.**

Think of it like a smart shopper at a supermarket — buying when prices are discounted and selling when they're marked up. This strategy is your "automated shopping bot" that does exactly that.

### Who is this strategy for?

- People with some programming skills who know how to use Freqtrade
- Those who want to steadily make money in the crypto market
- Investors who can accept occasional losses and pursue long-term profitability

---

## 2. How Does the Strategy Work?

Imagine you're watching a coin's price chart:

```
Price
  ↑
  │      ○───○  Sell Zone
  │     ╱     ╲
  │    ╱       ╲
  │   ╱         ○───○  Buy Zone
  │  ╱         ╱
  │ ╱         ╱
  │○─────────○
  └─────────────→ Time
```

The strategy's workflow:

1. **Monitor**: 24/7 watching coin prices
2. **Find opportunities**: When a coin drops to a "bargain" level
3. **Buy**: Auto-place buy orders
4. **Hold**: Wait for prices to rise
5. **Sell**: Auto-sell at target prices to lock in profits

---

## 3. The Strategy's Core Secret — "69 Different Doors"

The most powerful feature of this strategy is that it has **69 different buy conditions**.

What does that mean? It's like opening 69 different stores, each selling different stuff. As long as customers come to ANY store, you make money.

### How are these buy conditions categorized?

#### Type 1: Bargain Hunting

**Characteristics**: Wait until the coin price has crashed badly before buying — catching bargains.

Example: A coin dropped from $100 to $50, half off. The strategy thinks "too cheap!" and starts buying.

**How it looks in code**:
```python
rsi_14 < 35.0       # RSI below 35, meaning significant drop
r_14 < -90.0        # Price change rate below -90, severely oversold
```

#### Type 2: Trend Pullback

**Characteristics**: The coin is generally rising, but has a small pullback. Buy during the pullback.

Example: Bitcoin rose from $30,000 to $40,000, pulled back to $38,000. Buy here, wait for it to continue to $45,000.

**How it looks in code**:
```python
ema_200 > ema_200.shift(12)   # 200 MA is rising, major trend is up
close < ema_20 * 0.97         # Price below MA by 3%, a pullback opportunity
```

#### Type 3: Support Bounce

**Characteristics**: Price drops to a certain "support level" — historically, every time it dropped here it bounced back. So buy at the support level.

Example: A coin always bounces when it hits $100. Now it's near $100 again, strategy buys.

**How it looks in code**:
```python
close > sup_level_1d          # Price above daily support
low < sup_level_1d * 0.99     # Low touched the support level
```

---

## 4. Exit Strategy — "Tiered Profit Taking"

The strategy's exit logic is interesting, called **Tiered Profit Taking**.

### What is Tiered Profit Taking?

Simply: **The more you profit, the easier it is to let you sell.**

Example:

- Just bought, profiting 1%: Exit conditions are very strict, because you haven't earned enough yet
- Profiting 5%: Exit conditions get looser, you can lock in gains
- Profiting 10%: Extremely easy to sell — grab the profit and run

### Why design it this way?

Let's say you bought a coin:

1. **Just bought**: You definitely don't want to sell yet
2. **Profiting 3%**: Small profit, but want to see if it goes higher
3. **Profiting 8%**: Good enough, if anythingthings shift happens, sell
4. **Profiting 15%**: Too much! Sell immediately and lock in profits!

The strategy simulates this human exit decision-making process.

---

## 5. What "Tools" Does the Strategy Use?

The strategy is like a mechanic with many tools to judge when to buy and when to sell.

### Tool 1: RSI Indicator

**What it is**: A number from 0 to 100, telling you if the coin price is "too expensive" or "too cheap".

- RSI > 70: Too expensive, may drop
- RSI < 30: Too cheap, may rise

**How the strategy uses it**:
```python
rsi_14 < 35.0   # RSI below 35, coin is cheap, consider buying
rsi_14 > 70.0   # RSI above 70, coin is expensive, consider selling
```

### Tool 2: EMA Moving Average

**What it is**: Average the prices from a recent period and draw it as a line.

- EMA12: Average price of last 12 candles, reflects short-term trend
- EMA200: Average price of last 200 candles, reflects long-term trend

**How the strategy uses it**:
```python
close > ema_200    # Price above long-term MA, major trend is up
ema_12 > ema_26    # Short-term MA crosses above long-term MA, golden cross, bullish
```

### Tool 3: Bollinger Bands

**What it is**: Draw two lines above and below the moving average, forming a "channel".

- Price touching upper band: May drop
- Price touching lower band: May rise

**How the strategy uses it**:
```python
close < bb20_2_low * 0.98   # Price breaks below Bollinger lower band, oversold, buying opportunity
```

### Tool 4: CMF Money Flow

**What it is**: Checks how much money is flowing into this coin.

- CMF > 0: Money flowing in, good
- CMF < 0: Money flowing out, bad

**How the strategy uses it**:
```python
cmf < -0.1    # Money flowing out, may drop, sell quickly
cmf > 0.1     # Money flowing in, may rise
```

### Tool 5: R Indicator (Strategy's Own Creation)

**What it is**: An indicator the strategy developed itself, measuring the speed and degree of price changes.

```python
r_14 < -90    # Price dropped a lot within 14 candles, bottom-fishing opportunity
r_480 > -30   # Long-term decline not severe, not a bear market
```

---

## 6. The Strategy's "Safety Belt" — Risk Management

Driving requires seatbelts; trading needs risk management. The strategy has several protection mechanisms:

### Protection 1: Stop-Loss

What if it keeps dropping after buying? The strategy helps you stop-loss.

```python
stoploss = -0.10   # Auto-sell if loss reaches 10%
```

Example: Bought at $100, drops to $90, auto-sells to prevent further losses.

### Protection 2: Trailing Stop

How to protect profits after earning money? Use trailing stop.

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.03
```

Example:
- Bought at $100
- Rose to $103, trailing stop activates
- Rose to $110, stop price becomes $109
- Dropped to $109, auto-sells, gained 9%

### Protection 3: BTC Correlation

Bitcoin is the big brother; when big brother drops, little brothers usually drop too.

```python
if btc_not_downtrend_1h:   # If Bitcoin isn't falling
    allow buying             # Then and only then allow buying
```

This way, when BTC crashes, the strategy reduces buying and avoids "catching a falling knife".

---

## 7. Multi-Timeframe — "Telescope + Microscope"

The strategy watches 4 time cycles simultaneously, like using both a telescope and a microscope:

### Four Time Cycles

| Time Cycle | Role | Analogy |
|-----------|------|---------|
| Daily (1d) | See major trend | Telescope, look far |
| Hourly (1h) | See medium-term trend | Telescope, look closer |
| 15-Min (15m) | Find precise entry | Microscope, look closely |
| 5-Min (5m) | Execute trades | Hands-on operation |

### Why this approach?

Example:

1. **Daily shows trend**: Bitcoin daily is rising, major trend up ✓
2. **Hourly shows pullback**: Hourly shows a pullback, reaching support ✓
3. **15-minute finds entry**: 15-minute RSI oversold, short-term bottom ✓
4. **5-minute executes**: Buy now!

This is the perfect entry point: "Major trend is up + small trend is pulling back."

---

## 8. The Strategy's "Brain" — Buy Condition Details

Let's look at some typical buy conditions:

### Condition 1: Semi-Swing Bottom-Fishing

**Plain English explanation**:
- Coin price has recently risen (has momentum)
- Now dropped a bit (RSI < 35)
- But hasn't crashed (hourly RSI still healthy)
- Conclusion: This is a pullback, can buy

**Suitable scenario**: Short-term pullback in an uptrend.

### Condition 3: Bollinger Lower Band Bottom-Fishing

**Plain English explanation**:
- Bollinger Bands are wide enough (enough volatility)
- Price breaks below lower band (oversold)
- Candle wick is short (real drop, not fake)
- Conclusion: Rebound opportunity coming

**Suitable scenario**: Volatile ranging markets.

### Condition 17: Deep Bottom-Fishing

**Plain English explanation**:
- Short-term dropped a lot (R14 < -99)
- Long-term also dropped a lot (R480 < -90)
- Hourly also dropped a lot (R480_1h < -93)
- RSI at historical lows
- Conclusion: This is a crash-style drop, but also a good bottom-fishing opportunity

**Suitable scenario**: Extreme decline markets (high risk, potentially high returns).

### Condition 22: Daily Support Bounce

**Plain English explanation**:
- Price reached daily support level
- Low touched but closed above support
- Support level is valid
- Conclusion: Support bounce opportunity

**Suitable scenario**: Pullback trading near key support levels.

---

## 9. Exit Condition "Triggers"

### Exit Signal 1: RSI Overbought

```python
rsi_14 > 74.0    # RSI too high
cti > 0.85       # Trend is strong
cci > 240.0      # Price too far from average
```

**Plain English**: Risen too fast, time to rest, sell to lock in gains.

### Exit Signal 2: Capital Outflow

```python
rsi_14 > 68.0    # RSI still at high level
cmf < -0.1       # But money is starting to flow out
cmf_15m < 0      # Short-term money also flowing out
```

**Plain English**: Price is still high, but money is running away, sell quickly.

### Exit Signal 3: Trend Deterioration

```python
sma_200_dec_20   # 200 MA continuously declining
rsi_14 > 68.0    # RSI still at high level
```

**Plain English**: Major trend starting to deteriorate, don't be greedy, sell.

---

## 10. How to Use This Strategy?

### Step 1: Install Freqtrade

```bash
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
./setup.sh -i
```

### Step 2: Install Dependencies

```bash
pip install pandas_ta ta-lib technical
```

### Step 3: Configuration File

Set in `config.json`:

```json
{
    "timeframe": "5m",
    "use_sell_signal": true,
    "sell_profit_only": false,
    "ignore_roi_if_buy_signal": true,
    "max_open_trades": 6
}
```

### Step 4: Run

```bash
freqtrade trade --strategy NostalgiaForInfinityXw
```

---

## 11. Live Trading Advice

### Trading Pair Selection

**Recommended**:
- Major coins: BTC, ETH, BNB
- Stablecoin pairs: BTC/USDT, ETH/USDT
- Liquid altcoins

**Avoid**:
- Leveraged tokens (BULL, BEAR)
- New coins (insufficient data)
- Low-liquidity coins

### Capital Management

- Hold 4-6 positions simultaneously
- Equal capital per position
- Total capital should not exceed what you can afford to lose

### Mindset Advice

1. **Accept losses**: Strategy can't win every trade, there will be losses
2. **Think long-term**: Look at monthly, quarterly returns, not daily
3. **Regular checks**: Review strategy performance weekly, adjust parameters if needed

---

## 12. FAQ

### Q1: How much can this strategy earn?

**A**: No fixed answer. Based on historical backtesting and live experience, annualized returns may range from 20%-100%, depending on market conditions and parameter settings.

### Q2: Can it lose everything?

**A**: Strategy has 10% stop-loss, maximum loss per trade is 10%. With proper capital management, you won't lose everything. But extreme markets may cause consecutive losses.

### Q3: Does it need the computer running all the time?

**A**: Yes. A cloud server (VPS) running 24/7 is recommended. AWS, DigitalOcean, etc. are recommended providers.

### Q4: How to know if the strategy works?

**A**:
1. Run historical backtesting first
2. Then paper trading (dry-run)
3. Then small-capital live trading
4. Increase capital after confirming profitability

### Q5: Do parameters need frequent adjustment?

**A**: Quarterly re-optimization is recommended. Crypto markets change quickly; last year's good parameters may not work this year.

---

## 13. Summary

### Strategy's Core Logic

1. **Multi-condition buying**: 69 different buy conditions, one will always catch the opportunity
2. **Tiered profit taking**: The more you earn, the easier to sell, protecting profits
3. **Multi-timeframe**: Daily for trend, hourly for pullback, minutes for entry timing
4. **Risk control**: Stop-loss, trailing stop, BTC correlation — multiple layers of protection

### Who is it suitable for?

- People with some programming skills
- Who can accept occasional losses
- Willing to spend time learning and optimizing
- Pursuing long-term stable returns

### Final Thoughts

This strategy is not a "guaranteed profit" holy grail, but a tool that helps you systematize trading. Its success depends on:

- Correct understanding and configuration
- Appropriate market environment
- Continuous monitoring and optimization
- Reasonable risk expectations

**Remember**: Quantitative trading is a marathon, not a sprint. Patience, learning, and persistence are what get you further.

---

*Document Version: 1.0*
*Generated: 2026-03-27*
*Strategy Version: NostalgiaForInfinityXw v10.9.80*
