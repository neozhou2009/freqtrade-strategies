# NotAnotherSMAOffsetStrategy_uzi3 Strategy Analysis

## Table of Contents

1. [Strategy Overview and Design Philosophy](#1-strategy-overview-and-design-philosophy)
2. [Technical Indicator System](#2-technical-indicator-system)
3. [Entry Signal Logic](#3-entry-signal-logic)
4. [Exit Signal Logic](#4-exit-signal-logic)
5. [Risk Management System](#5-risk-management-system)
6. [Dynamic Parameter Adjustment Mechanism](#6-dynamic-parameter-adjustment-mechanism)
7. [Protection Mechanisms and Exit Confirmation](#7-protection-mechanisms-and-exit-confirmation)
8. [Timeframe and Startup Configuration](#8-timeframe-and-startup-configuration)
9. [Strategy Parameter Optimization](#9-strategy-parameter-optimization)
10. [Strategy Strengths and Limitations](#10-strategy-strengths-and-limitations)
11. [Live Trading Application Advice](#11-live-trading-application-advice)

---

## 1. Strategy Overview and Design Philosophy

### 1.1 Strategy Background

NotAnotherSMAOffsetStrategy_uzi3 is a quantitative trading strategy based on the Moving Average Offset (SMA Offset) technique, originally designed by developer @Rallipanos and later optimized by Uzirox. The "Not Another" in its name signals that this is not a typical trend-following strategy — it carves out an innovative path by using unique offset calculations within a traditional technical analysis framework.

### 1.2 Core Design Philosophy

The strategy's core philosophy rests on several key convictions:

**Blending Mean Reversion with Trend Following**: Rather than relying purely on trend following or mean reversion, the strategy uses multiple signal combinations to switch between different entry logics across varying market environments. This enables the strategy to capture main-wave moves in trending markets while also profiting from oversold rebounds in ranging markets.

**Dynamic Application of Offset Coefficients**: The strategy uses offset coefficients to adjust the triggering thresholds of moving averages, rather than simply using direct price-versus-moving-average crossovers. This approach increases flexibility, allowing the entry and exit sensitivity to be tuned across a wider range.

**Quantitative Implementation of Elliott Wave Theory**: Through the EWO (Elliott Wave Oscillator) indicator, the strategy translates the classic wave theory into quantifiable signals used to assess the market's bullish/bearish momentum state.

**Multi-Dimensional Confirmation Mechanism**: The strategy requires multiple technical conditions to be satisfied simultaneously before a trade signal is triggered, which significantly reduces the probability of false signals and improves trade reliability.

### 1.3 Strategy Positioning

The strategy is suited for medium-to-short-term trading, primarily designed for the cryptocurrency market using the 5-minute timeframe. Its characteristics include relatively conservative signals with a strong emphasis on risk control, making it suitable for traders pursuing steady returns rather than aggressive speculation.

---

## 2. Technical Indicator System

### 2.1 Moving Average System

The strategy builds a comprehensive moving average system comprising multiple types of moving averages:

**EMA (Exponential Moving Average) System**:
- EMA_100: The core long-term trend MA, used to distinguish bull from bear markets
- EMA_10: Short-term trend judgment, using the ZLEMA2 algorithm to reduce lag
- Dynamic EMA system: `ma_buy_X` and `ma_sell_X`, where X ranges from 5 to 80, generating MAs of different periods for buy/sell signals

**SMA (Simple Moving Average)**:
- SMA_9: An important reference for short-term exit signals, used to determine whether the price has broken through recent average cost

**HMA (Hull Moving Average)**:
- HMA_50: Medium-cycle trend judgment, using the Hull algorithm to further reduce lag; plays an important role in exit logic

### 2.2 ZLEMA2 Zero-Lag Moving Average

The strategy custom-implements the ZLEMA2 indicator, an improved version of the traditional EMA:

```python
def zlema2(dataframe, fast):
    zema1 = ta.EMA(df['close'], fast)
    zema2 = ta.EMA(zema1, fast)
    d1 = zema1 - zema2
    df['zlema2'] = zema1 + d1
```

The calculation first computes the EMA, then computes the EMA of that EMA, and finally adds the difference back to the original EMA. This double-smoothing technique effectively reduces noise from price fluctuations while lowering lag, making the indicator more responsive to price changes.

### 2.3 EWO (Elliott Wave Oscillator)

EWO is one of the strategy's core innovative indicators, calculated as:

```python
EWO = (EMA_5 - EMA_200) / Close × 100
```

This indicator draws inspiration from Elliott Wave theory, measuring market momentum through the difference between fast and slow MAs:
- When EWO is positive and rising, it indicates strengthening bullish momentum
- When EWO is negative and falling, it indicates strengthening bearish momentum
- When EWO is near the zero axis, the market is in consolidation or a turning point

The strategy uses the 50-period and 200-period combination, which is smoother than the traditional 5/35 combination and better suited for medium-to-long-term trend judgment.

### 2.4 RSI Relative Strength Index System

The strategy constructs a triple RSI system:

- **RSI_14**: Standard-period RSI for judging overall overbought/oversold status
- **RSI_4**: Fast RSI for capturing short-term price momentum changes
- **RSI_20**: Slow RSI for confirming medium-to-long-term trend direction

The crossover between fast and slow lines serves as part of the exit signal, ensuring exits are executed only after trend reversal is confirmed.

### 2.5 Bollinger Bands System

The strategy uses two sets of Bollinger Bands parameters:

**BinHV45 Strategy Bollinger Bands**:
- Period: 40
- Standard deviation: 2
- Used to calculate `bbdelta` (distance between BB middle and lower band), `closedelta` (closing price change), `tail` (lower wick length)

**ClucMay72018 Strategy Bollinger Bands**:
- Period: 20
- Standard deviation: 2
- Uses Typical Price = (High + Low + Close) / 3
- Used to determine whether price has broken below the Bollinger Bands lower band

These two sets of parameters each have their own focus — the former pays more attention to volatility changes and price patterns, while the latter more directly identifies oversold opportunities.

---

## 3. Entry Signal Logic

### 3.1 EWO1 Signal

EWO1 is one of the strategy's primary buy signals, with the following conditions:

1. **RSI_4 < 35**: Requires short-term RSI to be in the oversold zone, ensuring the price has had sufficient pullback
2. **Price < MA_buy × low_offset**: Price needs to be below the dynamic MA's offset value (default 0.986)
3. **EWO > ewo_high**: EWO needs to be above the set threshold (default 4.179), indicating bullish momentum still exists
4. **RSI_14 < rsi_buy**: Medium-term RSI needs to be below the threshold (default 58)
5. **Price < MA_sell × high_offset**: Ensures price has not yet reached the sell zone
6. **Volume > 0**: Ensures the market has sufficient liquidity

The signal's logic is: buy during a pullback in an uptrend, confirm bullish momentum is still present through EWO, and ensure sufficient pullback magnitude through RSI and price offset.

### 3.2 EWO2 Signal

The EWO2 signal supplements EWO1 with similar but different parameters:

1. **RSI_4 < 35**
2. **Price < MA_buy × low_offset_2** (deeper offset, default 0.944)
3. **EWO > ewo_high_2** (default -2.609, negative values allowed)
4. **RSI_14 < rsi_buy**
5. **Price < MA_sell × high_offset**
6. **RSI_14 < 25**: Additional requirement for deeply oversold RSI

EWO2 is designed to capture deeper pullback opportunities. When EWO is negative, the market is in a downtrend, but if the negative value is extreme and RSI is deeply oversold, it may signal a rebound opportunity.

### 3.3 EWO Low Signal

The EWO Low signal targets weak markets specifically:

1. **RSI_4 < 35**
2. **Price < MA_buy × low_offset**
3. **EWO < ewo_low** (default -16.917)
4. **Price < MA_sell × high_offset**
5. **Volume > 0**

This signal triggers when EWO is at an extremely low value, with the logic that when the market is excessively fearful, a technical rebound often follows.

### 3.4 BB_Bull Bull Market Bollinger Bands Signal

The BB_Bull signal contains two parallel condition groups, satisfying either one triggers the signal:

**Condition Group 1**:
1. EMA_10's 10-period mean > EMA_100's 10-period mean (confirm bull market)
2. Previous Bollinger Bands lower band > 0
3. bbdelta > closing price × 3.1% (Bollinger Bands wide enough)
4. closedelta > closing price × 1.8% (price change large enough)
5. tail < bbdelta × 23.3% (lower wick not too long)
6. Closing price < previous Bollinger Bands lower band
7. Closing price ≤ previous closing price
8. Volume > 0

**Condition Group 2**:
1. EMA_10's 10-period mean > EMA_100's 10-period mean
2. Closing price > EMA_100
3. Closing price < EMA_50
4. Closing price < Bollinger Bands lower band × 0.993
5. Volume < 21× the average volume of the previous 30 periods
6. Volume > 0

This group of signals specifically seeks buy opportunities near the Bollinger Bands lower band in bull market environments, using multi-dimensional confirmation to reduce false signals.

---

## 4. Exit Signal Logic

### 4.1 Primary Exit Signal

The strategy uses two parallel exit conditions:

**Condition 1**:
1. **Closing price > SMA_9**: Price breaks through the short-term MA
2. **Closing price > MA_sell × high_offset_2** (default 1.018): Price reaches the higher sell target
3. **RSI_14 > 50**: Confirms bullish momentum
4. **Volume > 0**
5. **RSI_4 > RSI_20**: Short-term momentum stronger than long-term momentum

**Condition 2**:
1. **SMA_9 > SMA_9 previous value × 1.005**: Short-term MA rising rapidly
2. **Closing price < HMA_50**: Price retraces below the Hull MA
3. **Closing price > MA_sell × high_offset**: Price still in the sell zone
4. **Volume > 0**
5. **RSI_4 > RSI_20**

The design logic of these two conditions is: after a price increase, confirm trend reversal through MA relationships and RSI momentum, and close positions promptly to lock in profits.

### 4.2 ROI Forced Exit

The strategy configures a stepped ROI:

```python
minimal_roi = {
    "0": 0.215,    # Immediate profit target 21.5%
    "40": 0.032,   # After 40 minutes: profit target 3.2%
    "87": 0.016,   # After 87 minutes: profit target 1.6%
}
```

This means when holding period returns reach the corresponding threshold, the strategy forcibly closes the position to prevent profit erosion.

---

## 5. Risk Management System

### 5.1 Fixed Stop-Loss

The strategy uses a -10% fixed stop-loss:

```python
stoploss = -0.1
```

When a single trade's loss reaches 10%, the system automatically exits with a stop-loss.

### 5.2 Trailing Stop

The strategy enables a trailing stop mechanism:

```python
trailing_stop = True
trailing_stop_positive = 0.005      # Activates after 0.5% profit
trailing_stop_positive_offset = 0.025  # Sets at 2.5% profit
trailing_only_offset_is_reached = True
```

How the trailing stop works:
1. When profit reaches 2.5%, trailing stop activates
2. The stop level follows the highest price upward, maintaining a 0.5% distance
3. When price retraces to touch the stop level, automatic position closing occurs

This mechanism protects profits while giving the price a certain amount of fluctuation space, avoiding being stopped out by small pullbacks.

### 5.3 Profit-Only Exit Protection

```python
use_sell_signal = True
sell_profit_only = True
sell_profit_offset = 0.005
```

The strategy is configured to only respond to sell signals when profit exceeds 0.5%, avoiding premature exits due to false signals while in a loss position.

---

## 6. Dynamic Parameter Adjustment Mechanism

### 6.1 Market State Judgment

One innovation of the strategy is dynamically adjusting parameters based on market state. In the `populate_indicators` method, the strategy checks the price change of the last two candles:

```python
if (((dataframe['close'].iloc[-1] - dataframe['close'].iloc[-2]) / 
     dataframe['close'].iloc[-2]) * 100) < -2:
    # Crash mode
    self.stoploss = -0.3
    self.trailing_stop_positive_offset = 0.03
    # Adjust buy offset to deeper levels
else:
    # Normal mode
    # Use standard parameters
```

### 6.2 Crash Mode Parameters

When a price drop exceeding 2% is detected, the strategy enters "crash mode":

| Parameter | Normal Mode | Crash Mode |
|-----------|-------------|------------|
| Stop-loss | -10% | -30% |
| Trailing Stop Offset | 2.5% | 3% |
| low_offset | 0.986 | 0.975 |
| low_offset_2 | 0.944 | 0.955 |
| ewo_low | -16.917 | -20.988 |
| ewo_high | 4.179 | 2.327 |
| ewo_high_2 | -2.609 | -2.327 |
| rsi_buy | 58 | 69 |

The design logic of crash mode:
- Widen stop-loss space to avoid being shaken out during panic selling
- Adjust buy offset to seek entry at deeper levels
- Loosen RSI threshold to accept higher RSI entries

---

## 7. Protection Mechanisms and Exit Confirmation

### 7.1 confirm_trade_exit Method

The strategy implements the `confirm_trade_exit` method for secondary confirmation after a sell signal is triggered:

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, 
                       time_in_force, sell_reason, current_time, **kwargs):
```

### 7.2 Sell Signal Filtering

For `sell_signal` type sells:

```python
if (last_candle['hma_50'] * 1.149 > last_candle['ema_100']) and \
   (last_candle['close'] < last_candle['ema_100'] * 0.951):
    return False
```

When HMA_50 is close to EMA_100 (within 14.9%) and the price is below 95.1% of EMA_100, the sell signal is rejected. This situation may indicate the market is undergoing a deep adjustment, and selling rashly could result in missing out on a rebound.

### 7.3 Slippage Protection

The strategy implements slippage protection:

```python
slippage_protection = {
    'retries': 3,
    'max_slippage': -0.02
}
```

When slippage exceeding 2% is detected, the strategy refuses the trade and retries up to 3 times. This prevents trading in unfavorable liquidity environments and protects traders from excessive slippage losses.

---

## 8. Timeframe and Startup Configuration

### 8.1 Timeframe

The strategy uses the 5-minute timeframe:

```python
timeframe = '5m'
```

This choice balances signal frequency and noise filtering. A timeframe too short generates excessive false signals, while one too long may miss entry opportunities.

### 8.2 Startup Candle Count

```python
startup_candle_count = 400
```

The strategy requires at least 400 historical candles to calculate all indicators. This is because:
- EMA_200 needs 200 candles
- EWO needs complete long-period MAs
- Bollinger Bands and rolling calculations need sufficient historical data

### 8.3 Processing Mode

```python
process_only_new_candles = True
```

The strategy only processes when new candles form, avoiding frequent calculations during candle formation, improving efficiency, and reducing false signals.

---

## 9. Strategy Parameter Optimization

### 9.1 Optimizable Parameters

The strategy defines multiple `IntParameter` and `DecimalParameter` with `optimize=False` by default:

**Buy Parameters**:
- `base_nb_candles_buy`: MA period (5-80, default 14)
- `low_offset`: Buy offset coefficient (0.9-0.99)
- `low_offset_2`: Deep buy offset coefficient
- `ewo_low`, `ewo_high`, `ewo_high_2`: EWO thresholds
- `rsi_buy`: RSI threshold

**Sell Parameters**:
- `base_nb_candles_sell`: Sell MA period
- `high_offset`, `high_offset_2`: Sell offset coefficients

### 9.2 Optimization Suggestions

After changing `optimize=False` to `optimize=True`, Freqtrade's hyperparameter optimization can be used for backtesting. Suggested optimization directions:

1. Adjust offset coefficients based on different trading pair characteristics
2. Optimize EWO thresholds for different market cycles (bull/bear markets)
3. Adjust RSI thresholds to adapt to different volatility environments

---

## 10. Strategy Strengths and Limitations

### 10.1 Strategy Strengths

**Multi-Signal Confirmation**: The strategy requires multiple technical conditions to be satisfied simultaneously, effectively reducing false signal rates. A single indicator's false breakout rarely triggers a trade — only when price, MAs, momentum, and volatility dimensions are aligned does an entry occur.

**Dynamic Adaptation**: The strategy automatically adjusts parameters based on market state (crash/normal), demonstrating good environmental adaptability. This design avoids the limitation of "one parameter set for all markets."

**Comprehensive Exit Mechanisms**: Combining signal exits, ROI exits, fixed stops, and trailing stops provides four exit methods — both active profit-taking and passive protection mechanisms.

**Slippage Protection**: Through slippage detection and retry mechanisms, traders are protected from unfavorable execution prices.

**Trend and Pullback Combination**: The strategy captures both trending moves and pullback entries within trends, resulting in relatively abundant trading opportunities.

### 10.2 Strategy Limitations

**Parameter Complexity**: The large number of parameters makes understanding and tuning the strategy time-consuming, presenting a learning curve for beginners.

**Lag Risk**: Although ZLEMA2 and HMA reduce lag, they may still not respond timely enough during violent market changes.

**Ranging Market Risk**: In sideways markets, the strategy may frequently trigger false signals, leading to consecutive small losses.

**Simple Crash Mode Judgment**: Market state is judged based solely on single-candle price drop, which may result in misjudgment.

**No Capital Management**: The strategy does not implement position sizing; users need to independently configure the monetary proportion for each trade.

---

## 11. Live Trading Application Advice

### 11.1 Market Selection

The strategy is best suited for the following market environments:

1. **Clearly trending markets**: When the market is in a clear uptrend or downtrend, the strategy's MA system can effectively identify direction
2. **Moderate-volatility trading pairs**: Excessively volatile pairs may generate too many false signals, while low-volatility pairs lack trading opportunities
3. **High-liquidity trading pairs**: Ensures execution quality and slippage control

### 11.2 Configuration Advice

**Initial Configuration**:
- Use default parameters for initial testing
- Set a reasonable position size (recommended single trade no more than 2-5% of total capital)
- Enable trailing stop to protect profits

**Advanced Optimization**:
- Adjust offset coefficients based on backtesting results
- Optimize parameters for specific trading pairs
- Consider adding maximum position count limits

### 11.3 Risk Warnings

1. Backtesting performance does not represent future returns
2. The strategy requires sufficient startup candles to function properly
3. In extreme market conditions (flash crashes, sharp rises), stop-losses may not execute as expected
4. It is recommended to test in a simulated account first, and only go live after confirming stability

### 11.4 Metrics to Monitor

The following indicators are recommended for evaluating strategy performance:

- **Win Rate**: Ratio of profitable trades to total trades
- **Profit/Loss Ratio**: Ratio of average profit to average loss
- **Maximum Drawdown**: Maximum drop from peak to trough in account equity
- **Sharpe Ratio**: Risk-adjusted return rate
- **Signal Frequency**: Average trades per day/week

---

## Conclusion

NotAnotherSMAOffsetStrategy_uzi3 is a meticulously designed quantitative strategy that achieves a good balance between trend following and mean reversion through multi-dimensional technical analysis and dynamic parameter adjustment. The strategy's core highlights include the innovative application of the EWO indicator and the dual-mode parameter adjustment mechanism.

However, no strategy is a silver bullet. Users need to fully understand the strategy's principles and make appropriate adjustments based on their own risk tolerance and market environment. It is recommended to go live only after sufficient backtesting and simulated verification.

---

*Document Version: 1.0*
*Strategy File: NotAnotherSMAOffsetStrategy_uzi3.py*
*Date: 2024*
