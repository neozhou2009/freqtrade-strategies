# NotAnotherSMAOffsetStrategy Strategy Analysis

## Chapter 1: Strategy Overview and Design Philosophy

### 1.1 Strategy Positioning

NotAnotherSMAOffsetStrategy is a quantitative trading strategy based on Simple Moving Average Offset (SMA Offset) technology, specifically designed for the Freqtrade trading platform. The strategy's core design philosophy is "finding value entry points during trend pullbacks." By combining price deviation from moving averages with Elliott Wave Oscillator (EWO) momentum judgment, it constructs a complete entry, exit, and risk control system.

The "NotAnother" in the name hints this is not a simple MA crossover strategy, but a deep improvement on traditional MA strategies. Instead of relying on simple golden/dead cross signals, it uses precise price offset calculations to capture trading opportunities when prices deviate from the MA.

### 1.2 Core Design Principles

**Mean Reversion + Momentum Combination**: The strategy believes prices deviating too far from the MA in the short term often revert. Combined with EWO for market momentum, it avoids entering too early at trend reversals.

**Multi-Dimensional Filtering**: RSI, volume, price position, and other conditions filter trading signals from multiple dimensions, ensuring signal quality.

**Controlled Risk**: Tiered ROI targets, trailing stop, and hard stop-loss三重保护 ensure per-trade risk is controllable.

### 1.3 Applicable Scenarios

- 5-minute cryptocurrency trading
- High volatility market environments
- Markets with clear trends but obvious pullbacks
- Liquid trading pairs

---

## Chapter 2: Technical Indicator System

### 2.1 Moving Average System

**Buy MA System**: Uses EMA as baseline, parameter `base_nb_candles_buy` default 14, optimizable 5-80.

Two offset coefficients:
- `low_offset`: Default 0.975
- `low_offset_2`: Default 0.955

**Sell MA System**: EMA, parameter `base_nb_candles_sell` default 24, optimizable 5-80.

Offset coefficients:
- `high_offset`: Default 0.991
- `high_offset_2`: Default 0.997

### 2.2 Elliott Wave Oscillator (EWO)

```
EWO = (EMA(5) - EMA(35)) / Low × 100
```

Default parameters: fast_ewo=50, slow_ewo=200.

Three key EWO thresholds:
- `ewo_high`: 2.327, for positive momentum
- `ewo_high_2`: -2.327, for second buy signal
- `ewo_low`: -20.988, for negative momentum

### 2.3 RSI Multi-Period System

- **RSI-14 (Standard)**: Period 14, buy threshold default 69, optimizable 30-70
- **RSI-4 (Fast)**: Period 4, trigger threshold < 35
- **RSI-20 (Slow)**: Period 20, used with fast RSI comparison

### 2.4 Hull Moving Average (HMA)

HMA-50 used for sell signal secondary confirmation. Features fast response and low lag, effectively filtering market noise.

---

## Chapter 3: Entry Signal Details

### 3.1 Buy Signal 1: ewo1

```
1. RSI_fast < 35 (fast RSI oversold)
2. Close < EMA_buy × low_offset (price below buy MA offset)
3. EWO > ewo_high (EWO shows positive momentum)
4. RSI < rsi_buy (standard RSI not at overbought)
5. Volume > 0 (volume verification)
6. Close < EMA_sell × high_offset (price below sell MA threshold)
```

**Signal Interpretation**: "Momentum-confirmed pullback buy." When EWO is positive and high, market momentum is upward; if price pulls back (below buy MA threshold) and RSI_fast shows oversold, it's an ideal entry point.

### 3.2 Buy Signal 2: ewo2

```
1. RSI_fast < 35
2. Close < EMA_buy × low_offset_2 (stricter offset, 0.955 vs 0.975)
3. EWO > ewo_high_2 (lower threshold, default -2.327)
4. RSI < rsi_buy
5. Volume > 0
6. Close < EMA_sell × high_offset
7. RSI < 25 (additional condition: standard RSI deeply oversold)
```

**Signal Interpretation**: "Deep oversold rebound." Price must fall below 95.5% of MA, RSI must be below 25 (extremely oversold) — captures extreme panic rebounds.

### 3.3 Buy Signal 3: ewolow

```
1. RSI_fast < 35
2. Close < EMA_buy × low_offset
3. EWO < ewo_low (EWO extremely negative, default -20.988)
4. Volume > 0
5. Close < EMA_sell × high_offset
```

**Signal Interpretation**: "Contrarian buy signal." When EWO is at extreme negative values, market is severely oversold. Higher risk but higher potential return.

---

## Chapter 4: Exit Signal Details

### 4.1 Exit Signal System Overview

Strategy's exit signal uses composite conditions, requiring multiple conditions simultaneously to trigger.

### 4.2 Primary Exit Condition

```
1. Close > SMA_9 (price above 9-period simple MA)
2. Close > EMA_sell × high_offset_2 (price above sell MA offset)
3. RSI > 50 (RSI shows bullish advantage)
4. Volume > 0
5. RSI_fast > RSI_slow (short-term momentum stronger than long-term)
```

**Interpretation**: "Momentum-confirmed high exit." When price rebounds above SMA-9 and reaches sell channel, RSI > 50 and RSI_fast > RSI_slow confirm sustained momentum.

### 4.3 Auxiliary Exit Condition

```
1. Close < HMA_50 (price below Hull MA)
2. Close > EMA_sell × high_offset (price still above sell MA baseline)
3. Volume > 0
4. RSI_fast > RSI_slow
```

**Interpretation**: "Trend reversal warning exit." When price falls below HMA-50 but remains above sell MA, indicates potential momentum weakening.

### 4.4 Exit Signal Comprehensive Mechanism

Uses OR logic:
```python
Exit = Condition Set 1 OR Condition Set 2
```

Ensures:
- Can follow price up in trending markets
- Can exit timely on trend reversals

---

## Chapter 5: Risk Management System

### 5.1 Tiered ROI Design

```
ROI Config:
- 0 min: 21.5% (immediate target)
- 40 min: 3.2%
- 87 min: 1.6%
- 201 min: 0% (unconditional exit)
```

### 5.2 Fixed Stop-Loss

```python
stoploss = -0.35  # 35% hard stop-loss
```

### 5.3 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.005  # 0.5% trail distance
trailing_stop_positive_offset = 0.03  # 3% activation threshold
trailing_only_offset_is_reached = True
```

**Mechanism**: Activates at 3% profit; stop follows highest price at 0.5% distance; price retraces triggers exit.

### 5.4 Trade Confirmation

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, ...):
    # Prevents premature selling in specific trends
    if (last_candle['hma_50'] * 1.149 > last_candle['ema_100']) and \
       (last_candle['close'] < last_candle['ema_100'] * 0.951):
        return False  # Reject exit
```

---

## Chapter 6: Parameter Optimization

### 6.1 Optimizable Parameters

**Buy Parameters**:

| Parameter | Type | Default | Range |
|-----------|------|---------|-------|
| base_nb_candles_buy | Int | 14 | 5-80 |
| low_offset | Decimal | 0.975 | 0.9-0.99 |
| low_offset_2 | Decimal | 0.955 | 0.9-0.99 |
| ewo_high | Decimal | 2.327 | 2.0-12.0 |
| ewo_high_2 | Decimal | -2.327 | -6.0-12.0 |
| ewo_low | Decimal | -20.988 | -20.0 to -8.0 |
| rsi_buy | Int | 69 | 30-70 |

**Sell Parameters**:

| Parameter | Type | Default | Range |
|-----------|------|---------|-------|
| base_nb_candles_sell | Int | 24 | 5-80 |
| high_offset | Decimal | 0.991 | 0.95-1.1 |
| high_offset_2 | Decimal | 0.997 | 0.99-1.5 |

---

## Chapter 7: Time Frame and Data Requirements

### 7.1 Primary Time Frame

Default 5-minute candles:
```python
timeframe = '5m'
```

### 7.2 Auxiliary Time Frame

```python
inf_1h = '1h'
```

### 7.3 Startup Candles

```python
startup_candle_count = 200
```

---

## Chapter 8: Strategy Pros & Cons

### 8.1 Advantages

1. **Multi-dimensional signal confirmation**: EWO, RSI, MA offset combinations ensure reliability
2. **Flexible entry strategies**: Three buy signals cover different market states
3. **Complete risk control**: Three-layer protection
4. **Highly optimizable**: 12 adjustable parameters

### 8.2 Limitations

1. **Range-bound market performance**: May produce more false signals in non-trending markets
2. **Parameter sensitivity**: Many parameters require market-specific optimization
3. **Event risk**: Pure technical indicators lack protection against news events
4. **Wide stop-loss**: 35% may cause significant losses in extreme conditions

---

## Chapter 9: Live Application Advice

### 9.1 Market Selection

**Recommended**:
- Major cryptocurrency pairs (BTC, ETH, etc.)
- Moderate volatility pairs
- Liquid markets

**Avoid**:
- Extremely calm markets
- One-sided downward trends
- Low-liquidity small coins

### 9.2 Parameter Tuning Advice

**Conservative config**:
- Increase ewo_high (e.g., 5.0)
- Decrease low_offset (e.g., 0.96)
- Increase rsi_buy (e.g., 60)

**Aggressive config**:
- Decrease ewo_high (e.g., 2.0)
- Increase low_offset (e.g., 0.99)
- Decrease rsi_buy (e.g., 50)

---

## Chapter 10: Summary and Outlook

### 10.1 Core Value

NotAnotherSMAOffsetStrategy is a carefully designed quantitative trading strategy combining mean reversion, momentum theory, and Elliott Wave theory. Its core value:

1. **Sound theory**: Combines mean reversion, momentum, Elliott Wave
2. **Clear logic**: Entry, exit, risk control each have rigorous logic
3. **Strong operability**: Adjustable parameters adapt to different markets
4. **Controllable risk**: Multi-layer protection mechanism

### 10.2 Improvement Directions

1. **Machine learning enhancement**: Use ML models to dynamically adjust parameters
2. **Multi-timeframe integration**: Deeper use of 1-hour cycle data
3. **Volatility adaptation**: Dynamically adjust thresholds based on market volatility
4. **Sentiment indicator integration**: Add market sentiment data

---

*Disclaimer: This document is for technical learning and research reference only, not investment advice. Cryptocurrency trading involves high risk; please make prudent decisions and bear your own risk.*
