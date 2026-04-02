# Cluc7werk Strategy In-Depth Analysis

> **Strategy ID**: #90 (10th in Batch 9)
> **Strategy Type**: Bollinger Bands + Fisher RSI Filter + Dual Mode Confirmation
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

**Cluc7werk** is an ultra short-cycle trading strategy based on Bollinger Bands and Fisher RSI indicators. The strategy's core feature is using Fisher RSI transformation for oversold filtering, combined with a dual-mode buy mechanism (Bollinger Band rebound + EMA volume-shrinking pullback). Compared to Cluc5werk, Cluc7werk simplifies multi-timeframe analysis and focuses on 1-minute intraday trading.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 modes (Bollinger Band rebound + EMA volume-shrinking pullback) + Fisher RSI filter |
| **Buy Confirmation** | Single signal trigger (no consecutive confirmation) |
| **Sell Conditions** | Price touches Bollinger middle band + EMA downward + Fisher RSI overbought |
| **Protection** | Fisher RSI filter + Hard stop-loss + Trailing stop |
| **Timeframe** | 1 Minute |
| **Dependencies** | TA-Lib, qtpylib, numpy |
| **Special Features** | Inverse Fisher RSI transformation, Dual-mode buy |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,       # Immediate exit: 10% profit
    "60": 0.07,      # After 60 minutes: 7% profit
    "120": 0.05,     # After 120 minutes: 5% profit
    "240": 0.03      # After 240 minutes: 3% profit
}

# Position Management
max_open_trades = 5  # Maximum 5 simultaneous trading pairs

# Stop-Loss Setting
stoploss = -0.10     # -10% hard stop-loss

# Trailing Stop Configuration
trailing_stop = True
trailing_stop_positive = 0.01007     # Activates at 1% profit
trailing_stop_positive_offset = 0.01258  # Triggers at 1.26% profit
trailing_only_offset_is_reached = False

# Exit Signal Configuration
use_sell_signal = True
sell_profit_only = True
sell_profit_offset = 0.01
ignore_roi_if_buy_signal = True
```

**Design Philosophy**:
- **ROI Table**: Uses aggressive profit target; 10% immediately upon entry, gradually lowering as time extends — contrasts with Cluc5werk's conservative style
- **Stop-Loss -10%**: More compact than Cluc5werk's -22.4%; reflects stricter risk control
- **Trailing Stop**: Activates at 1% profit; final stop-loss moves to 1.26% profit position; low activation threshold
- **Maximum 5 Positions**: Allows holding 5 different trading pairs simultaneously; risk diversification

### 2.2 Buy Parameter Configuration

```python
buy_params = {
    'bbdelta-close': 0.00732,      # Bollinger delta as % of close price
    'bbdelta-tail': 0.94138,       # tail to bbdelta ratio
    'close-bblower': 0.0199,       # Close to Bollinger lower band ratio
    'closedelta-close': 0.01825,   # Close delta as % of close price
    'fisher': -0.22987,            # Fisher RSI threshold (buy)
    'volume': 16                   # Volume multiple
}
```

### 2.3 Sell Parameter Configuration

```python
sell_params = {
    'sell-bbmiddle-close': 0.99184,  # Close price as % of Bollinger middle band
    'sell-fisher': 0.26832            # Fisher RSI threshold (sell)
}
```

---

## III. Entry Conditions Details

### 3.1 Core Filter Condition (Must Satisfy)

**Fisher RSI Transformation**:
```python
# Calculation
rsi = ta.RSI(dataframe, timeperiod=9)
rsi_transformed = 0.1 * (rsi - 50)
dataframe['fisher-rsi'] = (np.exp(2 * rsi_transformed) - 1) / (np.exp(2 * rsi_transformed) + 1)

# Filter condition
dataframe['fisher-rsi'].lt(params['fisher'])  # fisher-rsi < -0.22987
```

- Fisher RSI is an Inverse Fisher transformation of traditional RSI, mapping RSI values from [0, 100] to [-1, 1]
- fisher-rsi < -0.22987 indicates RSI below ~38 (oversold zone)
- This is the strategy's first layer of protection; only considers buying in oversold zones

### 3.2 Mode 1: Bollinger Band Rebound Buy

```python
# Condition A: Bollinger Band rebound pattern
(
    dataframe['bb1-delta'].gt(dataframe['close'] * params['bbdelta-close']) &
    dataframe['closedelta'].gt(dataframe['close'] * params['closedelta-close']) &
    dataframe['tail'].lt(dataframe['bb1-delta'] * params['bbdelta-tail']) &
    dataframe['close'].lt(dataframe['lower-bb1'].shift()) &
    dataframe['close'].le(dataframe['close'].shift())
)
```

**Conditions**:
1. `bb1-delta > close × 0.00732`: Distance between BB middle and lower > 0.732% of close; BB has meaningful width
2. `closedelta > close × 0.01825`: Close price has significant rise vs previous candle (1.825%); relatively high threshold
3. `tail < bb1-delta × 0.94138`: Lower shadow < 94.138% of BB bandwidth; lower shadow relatively tight
4. `close < lower-bb1.shift()`: Close below previous candle's BB lower band; forms "breakdown" pattern
5. `close ≤ close.shift()`: Close not higher than previous candle; confirms weak price action

**Pattern Interpretation**: Captures "false breakout" rebound. Price briefly breaks BB lower band then quickly rebounds; forms hammer-like pattern. The higher closedelta requirement (1.825%) means it needs relatively obvious upward momentum.

### 3.3 Mode 2: EMA Volume-Shrinking Pullback Buy

```python
# Condition B: EMA volume-shrinking pullback pattern
(
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < params['close-bblower'] * dataframe['lower-bb2']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * params['volume']))
)
```

**Conditions**:
1. `close < ema_slow`: Close below 48-period EMA; below long-term MA
2. `close < lower-bb2 × 0.0199`: Close below BB lower band by 1.99%; price breaks BB
3. `volume < volume_mean_slow.shift(1) × 16`: Volume below previous 24-period average × 16 (volume shrinkage)

**Pattern Interpretation**: Captures panic drop oversold rebound. Price below EMA and breaks BB, with shrinking volume — indicating selling pressure exhaustion.

### 3.4 Buy Signal Trigger Mechanism

```python
# Buy signal: satisfies Fisher RSI filter + either mode
dataframe.loc[
    (dataframe['fisher-rsi'].lt(params['fisher'])) &
    (
        Mode A conditions | Mode B conditions
    ),
    'buy'
] = 1
```

**Design Intent**: Compared to Cluc5werk's dual confirmation (two consecutive candles), Cluc7werk simplifies the confirmation mechanism — single satisfying condition triggers buy. This makes entry more sensitive but may increase false signal risk.

---

## IV. Exit Logic Details

### 4.1 Sell Conditions

```python
dataframe.loc[
    ((dataframe['close'] * params['sell-bbmiddle-close']) > dataframe['mid-bb2']) &
    dataframe['ema_fast'].gt(dataframe['close']) &
    dataframe['fisher-rsi'].gt(params['sell-fisher']) &
    dataframe['volume'].gt(0)
    ,
    'sell'
] = 1
```

**Conditions**:
1. **Price touching Bollinger middle band**: `close × 0.99184 > mid-bb2`; close reaches 99.184%+ of BB middle band; near middle band
2. **Short-term MA downward**: `ema_fast > close`; 6-period EMA above current price; short-term trend weakening
3. **Fisher RSI overbought**: `fisher-rsi > 0.26832`; corresponds to RSI above ~63; entering overbought zone
4. **Valid volume**: Volume > 0

**Pattern Interpretation**: Sell combines price position (touching BB middle), technical indicator (MA turning + overbought), and volume confirmation. This multi-confirmation ensures exit when price starts weakening.

---

## V. Technical Indicator System

### 5.1 Bollinger Band Indicators

| Indicator Name | Calculation | Parameter | Purpose |
|----------------|-------------|-----------|---------|
| **lower-bb1** | TA-Lib BBANDS | 40 periods | Buy: price vs lower band |
| **bb1-delta** | \|mid-bb1 - lower-bb1\| | - | Buy: BB bandwidth filter |
| **lower-bb2** | qtpylib BBANDS | 20 periods | Buy: price vs lower band |
| **mid-bb2** | qtpylib BBANDS | 20 periods | Sell: price vs middle band |

### 5.2 Moving Average Indicators

| Indicator Name | Calculation | Parameter | Purpose |
|----------------|-------------|-----------|---------|
| **ema_fast** | TA-Lib EMA | 6 periods | Sell: short-term trend judgment |
| **ema_slow** | TA-Lib EMA | 48 periods | Buy: long-term trend judgment |
| **volume_mean_slow** | Rolling mean | 24 periods | Buy: volume filter |

### 5.3 Momentum Indicators

| Indicator Name | Calculation | Parameter | Purpose |
|----------------|-------------|-----------|---------|
| **rsi** | TA-Lib RSI | 9 periods | Fisher RSI calculation base |
| **fisher-rsi** | Inverse Fisher transform | - | Buy/sell filter |
| **closedelta** | \|close - close.shift()\| | - | Buy: price volatility strength |
| **tail** | \|close - low\| | - | Buy: lower shadow length |

### 5.4 Indicator Relationship Diagram

```
┌─────────────────────────────────────────┐
│  Fisher RSI < -0.22987 (oversold filter)│
│  = RSI < ~38                            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Mode A: Bollinger Band rebound          │
│  - bb1-delta > close × 0.732%           │
│  - closedelta > close × 1.825%          │
│  - tail < bb1-delta × 94.138%           │
│  - close < lower-bb1.shift()            │
│  - close ≤ close.shift()                │
│                                          │
│  Mode B: EMA volume-shrinking pullback   │
│  - close < ema_slow (48 EMA)            │
│  - close < lower-bb2 × 1.99%            │
│  - volume < avg × 16                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Buy: Single signal trigger             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Sell: Triple confirmation               │
│  - close > mid-bb2 × 99.184%           │
│  - ema_fast > close (6 EMA downward)    │
│  - fisher-rsi > 0.26832 (overbought)    │
└─────────────────────────────────────────┘
```

---

## VI. Risk Management Features

### 6.1 Multi-Layer Protection

1. **Fisher RSI Filter Layer**: Ensures buying only in oversold zones (RSI < 38)
2. **Dual-Mode Buy Layer**: Two complementary buy modes cover different scenarios
3. **Hard Stop-Loss Layer**: -10% stop-loss; more compact than Cluc5werk
4. **Trailing Stop Layer**: Activates at 1% profit; protects floating profits

### 6.2 Profit-Taking Strategy

- **ROI Progressive Exit**: Gradually lowers profit targets as holding extends (10% → 7% → 5% → 3%)
- **Trailing Stop Protection**: Retains more profit when trend continues
- **Multi-Condition Exit**: Price touching BB middle + MA turning + overbought confirmation

### 6.3 Risk-Return Characteristics

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Maximum positions** | 5 trading pairs | Diversify risk |
| **Profit targets** | 10% / 7% / 5% / 3% | Aggressive targets |
| **Stop-loss** | -10% | Compact stop-loss |
| **Trailing stop activation** | 1% profit | Low threshold activation |
| **Average holding time** | Estimated 1-4 hours | Ultra short-cycle trading |

### 6.4 Risk Management Comparison with Cluc5werk

| Feature | Cluc5werk | Cluc7werk |
|---------|-----------|-----------|
| Stop-loss | -22.4% | -10% |
| First target profit | 2.13% | 10% |
| Trailing stop activation | 18.6% | 1% |
| Trend filter | 1-hour ROCR | Fisher RSI |
| Buy confirmation | 2 consecutive candles | Single signal |

---

## VII. Strategy Pros & Cons

### 7.1 Advantages

1. **Aggressive Profit Target**: 10% first target far exceeds most strategies
2. **Fisher RSI Filter**: Compared to simple RSI, Inverse Fisher transformation provides better overbought/oversold signals
3. **Dual-Mode Buy**: Two complementary buy modes cover different scenarios
4. **Compact Stop-Loss**: -10% stop-loss more conservative than Cluc5werk
5. **Low-Threshold Trailing Stop**: Activates at 1%; timely profit protection
6. **No Multi-Timeframe Dependency**: Simplified analysis; only needs 1-minute data

### 7.2 Limitations

1. **Too Short Timeframe**: 1-minute timeframe susceptible to market noise
2. **Single Confirmation Risk**: Single signal may increase false signal probability vs consecutive confirmation
3. **Aggressive Target Hard to Achieve**: 10% target may be difficult in single trades
4. **Liquidity Requirement**: Needs high-volume trading pairs for normal operation
5. **High Volatility Dependency**: Needs sufficient market volatility to trigger buy conditions

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **High-volatility coins**: ALT, SHIB, newly listed tokens
- **Quick rebound行情**: Strategy excels at capturing oversold quick rebounds
- **Markets with sufficient liquidity**: High-volume pairs to avoid slippage
- **High-return pursuing investors**: 10% target suits aggressive traders

### 8.2 Not Recommended Scenarios

- **Low-volatility coins**: Insufficient volatility to trigger buy conditions
- **Ranging markets**: Fisher RSI filter may be too strict
- **Illiquid trading pairs**: Slippage reduces actual returns
- **Conservative investors**: 10% target may be too aggressive

### 8.3 Variant Suggestions

Based on Cluc7werk, consider these adjustments:

| Adjustment Direction | Suggestion |
|---------------------|------------|
| Conservative | Raise stop-loss to -15%; lower first target to 5% |
| Balanced | Add two-consecutive-candle confirmation |
| Trend-following | Add 1-hour ROCR trend filter |

---

## IX. Applicable Market Environment Details

### 9.1 Best Market Environments

1. **High volatility**: Price frequently fluctuates significantly; triggers Bollinger Band breakouts
2. **Quick drop and rebound**: Fisher RSI < -0.22987 captures oversold opportunities
3. **Sufficient liquidity**: Good trading depth; tight bid-ask spread

### 9.2 Average Performance Markets

1. **Ranging oscillation**: Fisher RSI filter filters out most signals
2. **Slow decline**: Continuous drops may not trigger rebound mode
3. **Low volatility**: Bollinger Bands narrow; difficult to trigger buy conditions

### 9.3 Market Environment Identification

Recommendations for judging market environment:
- **Fisher RSI value**: Below -0.3, closely watch for buy opportunities
- **Bollinger Band width**: Increase trading frequency when expanding
- **Volume**: Higher market activity when volume increases

---

## X. Important Notes: The Cost of Complexity

### 10.1 Aggressive Target Risks

Cluc7werk sets a 10% first target profit; very aggressive. In actual trading:

1. **Slippage impact**: Actual execution price may deviate from signal price
2. **Liquidity risk**: Large orders may not fill at target price
3. **Market impact**: Buying may push price up; reduces actual profit

### 10.2 Parameter Stability Recommendations

- **Use default parameters**: Do not arbitrarily modify optimized parameters
- **Validate across time periods**: Backtest across different time periods
- **Small-capital live testing**: Sufficient paper trading before real capital
- **Close monitoring**: Higher profit targets require more frequent market monitoring

### 10.3 Monitoring Focus

1. **Fill rate**: Whether target orders are filling
2. **Holding time**: Whether reaching target in reasonable time
3. **Signal frequency**: Too few or too many signals both indicate problems
4. **Drawdown**: Whether overall account drawdown is within acceptable range

---

## XI. Summary

Cluc7werk is a aggressively designed ultra short-cycle trading strategy, integrating Fisher RSI transformation, Bollinger Band pattern recognition, and dual-mode buy mechanism. Its core characteristics are high profit target (10%) and compact stop-loss (-10%).

**Key Features**:
- Uses Fisher RSI for oversold filtering; ensures buy safety
- Two complementary buy modes (Bollinger Band rebound + EMA volume-shrinking pullback)
- Single signal trigger; more sensitive entry
- Aggressive profit target setting (10% first target)

**Usage Recommendations**:
- Recommended for experienced traders; beginners should be cautious
- Prioritize high-liquidity trading pairs
- Keep parameters unchanged; avoid over-optimization
- Monitor signal quality combined with market environment
- Practice sound risk management; do not exceed comfortable position sizes

**Risk Warning**:
- 10% profit target may be difficult to achieve in single trades
- 1-minute timeframe susceptible to noise
- Single confirmation may increase false signal probability

The strategy's backtest performance needs further verification; investors should recognize the inherent risks of ultra short-cycle strategies and conduct sufficient live testing before applying real capital.
