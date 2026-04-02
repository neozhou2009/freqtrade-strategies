# Cluc5werk Strategy In-Depth Analysis

> **Strategy ID**: #89 (9th in Batch 9)
> **Strategy Type**: Bollinger Bands + ROCR Trend Filter + Dual Mode Confirmation
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

**Cluc5werk** is an ultra short-cycle trading strategy based on Bollinger Bands and ROCR (Rate of Change Ratio) indicators. The strategy's core feature is combining 1-hour ROCR indicator for trend filtering with a dual confirmation mechanism (two consecutive candles must satisfy buy conditions) to reduce false signals. The strategy includes two complementary buy modes: Bollinger Band rebound mode and EMA volume-shrinking pullback mode.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 modes (Bollinger Band rebound + EMA volume-shrinking pullback) |
| **Buy Confirmation** | Two consecutive candles satisfy fake_buy conditions |
| **Sell Conditions** | Price touches Bollinger middle band + Three consecutive down candles pattern |
| **Protection** | ROCR trend filter + Hard stop-loss + Trailing stop |
| **Timeframe** | 1 Minute (main) + 1 Hour (informative) |
| **Dependencies** | TA-Lib, technical, qtpylib, numpy |
| **Special Features** | Multi-timeframe analysis, Dual buy confirmation mechanism |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.02134,    # Immediate exit: 2.134% profit
    "275": 0.01745,  # After 275 minutes: 1.745% profit
    "559": 0.01618,  # After 559 minutes: 1.618% profit
    "621": 0.01310,  # After 621 minutes: 1.310% profit
    "791": 0.00843,  # After 791 minutes: 0.843% profit
    "1048": 0.00443, # After 1048 minutes: 0.443% profit
    "1074": 0,       # After 1074 minutes: 0% (trailing stop only)
}

# Stop-Loss Setting
stoploss = -0.22405  # -22.4% hard stop-loss

# Trailing Stop Configuration
trailing_stop = True
trailing_stop_positive = 0.18622     # Activates at 18.6% profit
trailing_stop_positive_offset = 0.23091  # Triggers at 23.1% profit
trailing_only_offset_is_reached = False

# Exit Signal Configuration
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = True
exit_profit_offset = 0.0
```

**Design Philosophy**:
- **ROI Table**: Uses an aggressive exit strategy; sets 2.1% target profit immediately upon entry, gradually lowering targets as holding time extends — suitable for high-volatility crypto markets
- **Stop-Loss -22.4%**: Very loose stop-loss setting; strategy tolerates significant drawdowns; relies mainly on trailing stop for profit protection
- **Trailing Stop**: Activates at 18.6% profit; final stop-loss moves to 23.1% profit level; provides ample upside room

### 2.2 Buy Parameter Configuration

```python
buy_params = {
    'bbdelta-close': 0.01853,      # Bollinger delta as % of close price
    'bbdelta-tail': 0.78758,       # tail to bbdelta ratio
    'close-bblower': 0.00931,      # Close to Bollinger lower band ratio
    'closedelta-close': 0.00169,   # Close delta as % of close price
    'rocr-1h': 0.8973,            # 1-hour ROCR threshold
    'volume': 35                   # Volume multiple
}
```

### 2.3 Sell Parameter Configuration

```python
sell_params = {
    'sell-bbmiddle-close': 0.97103  # Close price as % of Bollinger middle band
}
```

---

## III. Entry Conditions Details

### 3.1 Core Filter Condition (Must Satisfy)

**1-Hour ROCR Filter**:
```python
dataframe['proch'].gt(params['roch-1h'])  # rocr_1h > 0.8973
```
- Uses 1-hour period ROCR (168 candles) for trend confirmation
- ROCR > 0.8973 means price shows an uptrend in the past 168 hours
- This is the strategy's first layer of protection; only buys in uptrends

### 3.2 Mode 1: Bollinger Band Rebound Buy

```python
# Condition A: Bollinger Band rebound pattern
(
    dataframe['lower'].shift().gt(0) &
    dataframe['bbdelta'].gt(dataframe['close'] * params['bbdelta-close']) &
    dataframe['closedelta'].gt(dataframe['close'] * params['closedelta-close']) &
    dataframe['tail'].lt(dataframe['bbdelta'] * params['bbdelta-tail']) &
    dataframe['close'].lt(dataframe['lower'].shift()) &
    dataframe['close'].le(dataframe['close'].shift())
)
```

**Conditions**:
1. `lower.shift() > 0`: Ensures Bollinger lower band valid (non-zero)
2. `bbdelta > close × 0.01853`: Distance between middle and lower band > 1.853% of close; Bollinger has meaningful width
3. `closedelta > close × 0.00169`: Close price has obvious absolute rise vs previous candle (0.169%)
4. `tail < bbdelta × 0.78758`: Lower shadow length < 78.758% of Bollinger bandwidth; lower shadow relatively tight
5. `close < lower.shift()`: Close below previous candle's Bollinger lower band; forms "breakdown" pattern
6. `close <= close.shift()`: Close not higher than previous candle's close; confirms weak price action

**Pattern Interpretation**: This mode captures "false breakout" rebound opportunities. Price briefly breaks below Bollinger lower band then quickly rebounds; forms a hammer-like pattern.

### 3.3 Mode 2: EMA Volume-Shrinking Pullback Buy

```python
# Condition B: EMA volume-shrinking pullback pattern
(
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < params['close-bblower'] * dataframe['bb_lowerband']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * params['volume']))
)
```

**Conditions**:
1. `close < ema_slow`: Close below 50-period EMA; below long-term MA
2. `close < bb_lowerband × 0.00931`: Close below Bollinger lower band by 0.931%; price deeply breaks below BB
3. `volume < volume_mean_slow.shift(1) × 35`: Volume below previous 30-day average × 35 (volume shrinkage)

**Pattern Interpretation**: This mode captures panic drop oversold rebound opportunities. Price is below EMA and significantly breaks Bollinger lower band, with shrinking volume — indicating selling pressure exhaustion.

### 3.4 Dual Confirmation Mechanism

```python
# fake_buy signal: satisfies either mode above
dataframe.loc[... , 'fake_buy'] = 1

# Actual buy signal: two consecutive candles both satisfy fake_buy
dataframe.loc[
    (dataframe['fake_buy'].shift(1).eq(1)) &
    (dataframe['fake_buy'].eq(1)) &
    (dataframe['volume'] > 0)
    ,
    'buy'
] = 1
```

**Design Intent**: Only triggers actual buy after two consecutive candles both satisfy buy conditions. This filters out single-candle random signals and improves signal reliability.

---

## IV. Exit Logic Details

### 4.1 Sell Conditions

```python
dataframe.loc[
    (dataframe['high'].le(dataframe['high'].shift(1))) &
    (dataframe['high'].shift(1).le(dataframe['high'].shift(2))) &
    (dataframe['close'].le(dataframe['close'].shift(1))) &
    ((dataframe['close'] * params['sell-bbmiddle-close']) > dataframe['bb_middleband']) &
    (dataframe['volume'] > 0)
    ,
    'sell'
] = 1
```

**Conditions**:
1. **Three consecutive down pattern**: `high ≤ high.shift(1) ≤ high.shift(2)`; three consecutive candles' highs gradually decrease or stay flat
2. **Close weakness**: `close ≤ close.shift(1)`; close below or equal to previous candle
3. **Touching Bollinger middle band**: `close × 0.97103 > bb_middleband`; close reaches 97.103%+ of Bollinger middle band
4. **Valid volume**: Volume > 0

**Pattern Interpretation**: Sell combines price pattern (consecutive high decline) and technical indicator (touching Bollinger middle band). This ensures exit when price starts weakening and approaches important resistance.

---

## V. Technical Indicator System

### 5.1 Main Timeframe Indicators (1 Minute)

| Indicator Name | Calculation | Purpose |
|----------------|-------------|---------|
| **lower** | Custom BB lower band (40 periods, 2x std dev) | Buy: price rebound after breaking lower band |
| **bbdelta** | \|mid - lower\| | Buy: Bollinger bandwidth filter |
| **closedelta** | \|close - close.shift()\| | Buy: price volatility strength |
| **tail** | \|close - low\| | Buy: lower shadow length |
| **bb_lowerband** | qtpylib BB lower band (20 periods) | Buy: price vs BB relationship |
| **bb_middleband** | qtpylib BB middle band (20 periods) | Sell: price vs middle band relationship |
| **ema_slow** | 50-period EMA | Buy: price vs MA relationship |
| **volume_mean_slow** | 30-period volume MA | Buy: volume filter |
| **rocr** | 28-period ROCR | Backup trend indicator |

### 5.2 Informative Timeframe Indicators (1 Hour)

| Indicator Name | Calculation | Purpose |
|----------------|-------------|---------|
| **roch_1h** | 168-period ROCR (7 days) | Trend filter: ensures long-term uptrend |

### 5.3 Indicator Relationship Diagram

```
1-hour timeframe: ┌─────────────────────────────────────────┐
                  │  rocr_1h > 0.8973 (uptrend filter)     │
                  └─────────────────────────────────────────┘
                              ↓
1-minute timeframe: ┌─────────────────────────────────────────┐
                    │  Mode A: Bollinger Band rebound          │
                    │  - bbdelta > close × 1.853%             │
                    │  - close < lower.shift()                 │
                    │  - tail < bbdelta × 78.758%             │
                    │                                          │
                    │  Mode B: EMA volume-shrinking pullback   │
                    │  - close < ema_slow                     │
                    │  - close < bb_lower × 0.931%             │
                    │  - volume < avg × 35                    │
                    └─────────────────────────────────────────┘
                              ↓
                    ┌─────────────────────────────────────────┐
                    │  Dual confirmation: fake_buy × 2 candles │
                    └─────────────────────────────────────────┘
                              ↓
                    ┌─────────────────────────────────────────┐
                    │  Sell: Three down + touching BB middle    │
                    └─────────────────────────────────────────┘
```

---

## VI. Risk Management Features

### 6.1 Multi-Layer Protection

1. **Trend Filter Layer**: 1-hour ROCR ensures buying only in uptrends
2. **Pattern Filter Layer**: Dual buy confirmation (two consecutive candles) reduces false signals
3. **Hard Stop-Loss Layer**: -22.4% stop-loss; tolerates large drawdowns
4. **Trailing Stop Layer**: Activates at 18.6% profit; protects floating profits

### 6.2 Profit-Taking Strategy

- **ROI Progressive Exit**: Gradually lowers profit targets as holding extends
- **Trailing Stop Protection**: Retains more profit when trend continues
- **Middle Band Resistance Exit**: Exits when price meets resistance at Bollinger middle band

### 6.3 Risk-Return Characteristics

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Win Rate** | ~90% (331 trades, 305 wins/9 flat/17 losses) | Very high win rate |
| **Average Profit** | 1.54% | Average return per trade |
| **Median Profit** | 2.13% | Typical trade return |
| **Average Holding Time** | 367.3 minutes (~6 hours) | Medium holding period |
| **Total Return** | 509.36% (best of 1000 hyperopt rounds) | Outstanding backtest performance |

---

## VII. Strategy Pros & Cons

### 7.1 Advantages

1. **High Win Rate**: 90%+ win rate provides stable trading experience
2. **Trend Filter**: Uses 1-hour ROCR to avoid counter-trend trades
3. **Dual Confirmation**: Two-consecutive-candle confirmation reduces false signals
4. **Dual Mode Buy**: Two complementary buy modes cover different scenarios
5. **Complete Profit/Loss Management**: ROI + trailing stop combo provides flexible profit protection

### 7.2 Limitations

1. **Too Short Timeframe**: 1-minute timeframe susceptible to market noise
2. **Parameter Sensitive**: Many parameters rely on hyperopt optimization; overfitting risk
3. **Liquidity Requirement**: Needs high-volume trading pairs for normal operation
4. **Lag**: Dual confirmation may slightly delay entry timing
5. **Trend Dependent**: Poor performance in ranging or downtrending markets

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **High-volatility coins**: ALT, SHIB, newly listed tokens
- **Bull or strong-trend markets**: ROCR filter effectively captures trending moves
- **Markets with sufficient liquidity**: High-volume pairs to avoid slippage
- **Intraday trading**: Average holding ~6 hours; suitable for intraday or short-term trades

### 8.2 Not Recommended Scenarios

- **Low-volatility coins**: Insufficient volatility to trigger buy conditions
- **Ranging markets**: Trend filter misses many opportunities
- **Illiquid trading pairs**: Slippage reduces actual returns
- **Around major news events**: Extreme volatility may invalidate strategy

### 8.3 Variant Versions

Strategy includes three optimized variants for different trading pairs:

| Version | Trading Pair | Characteristics |
|---------|-------------|----------------|
| **Cluc5werk** | General | Balanced parameters |
| **Cluc5werk_ETH** | ETH/Stable | More aggressive stop-loss (-33.7%); lower target profit |
| **Cluc5werk_BTC** | BTC/Stable | Conservative parameters; stricter stop-loss (-14.5%) |
| **Cluc5werk_USD** | USD/Stable | Similar to ETH version |

---

## IX. Applicable Market Environment Details

### 9.1 Best Market Environments

1. **Strong uptrend**: 1-hour ROCR consistently above 0.8973
2. **High volatility**: Price frequently fluctuates significantly; triggers Bollinger Band breakouts
3. **Sufficient liquidity**: Good trading depth; tight bid-ask spread

### 9.2 Average Performance Markets

1. **Ranging oscillation**: Trend filter filters out most signals
2. **Trend reversal**: Strategy designed for trend-following; may enter at tops
3. **Low volatility**: Bollinger Bands narrow; difficult to trigger buy conditions

### 9.3 Market Environment Identification

Recommendations for judging market environment:
- **1-hour ROCR value**: Reduce trades when below 0.85
- **Bollinger Band width**: Reduce trading frequency when narrowing
- **Volume**: Stay cautious when shrinking

---

## X. Important Notes: The Cost of Complexity

### 10.1 Overfitting Risk

Cluc5werk has 6 buy parameters and 1 sell parameter, optimized through 1000 rounds of hyperopt. While backtest performance is outstanding (509% return), risks include:

1. **Historical data overfitting**: Parameters may over-adapt to historical data
2. **Look-ahead bias**: Some indicators (like bbdelta) may contain future information
3. **Market changes**: Performance outside the optimization period may significantly decline

### 10.2 Parameter Stability Recommendations

- **Use default parameters**: Do not arbitrarily modify optimized parameters
- **Validate across time periods**: Backtest across different time periods
- **Small-capital live testing**: Sufficient paper trading before real capital

### 10.3 Monitoring Focus

1. **Win rate changes**: Alert when below 80%
2. **Average profit**: Check market environment when persistently below 1%
3. **Signal frequency**: Too few or too many signals both indicate problems

---

## XI. Summary

Cluc5werk is a meticulously designed short-cycle trading strategy, integrating multi-timeframe analysis, Bollinger Band pattern recognition, volume filtering, and dual confirmation mechanisms. Its core advantages are high win rate (90%+) and comprehensive risk management.

**Key Features**:
- Uses 1-hour ROCR for trend filtering; avoids counter-trend trades
- Two complementary buy modes (Bollinger Band rebound + EMA volume-shrinking pullback)
- Dual confirmation mechanism reduces false signals
- Flexible profit-taking (ROI + trailing stop)

**Usage Recommendations**:
- Recommended for bull or strong-trend environments
- Prioritize high-liquidity trading pairs
- Keep parameters unchanged; avoid over-optimization
- Monitor signal quality combined with market environment

The strategy's backtest performance is impressive, but investors should recognize the inherent risks of short-cycle strategies and conduct sufficient live testing before applying real capital.
