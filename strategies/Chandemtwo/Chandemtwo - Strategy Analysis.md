# Chandemtwo Strategy In-Depth Analysis

> **Strategy ID**: 5th in Batch 81-90
> **Strategy Type**: CMO Momentum Breakout + Bollinger Band Trend Confirmation + CMO Pullback Sell
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**Chandemtwo** is an enhanced version of the Chandem strategy, with stricter optimization on both buy and sell conditions. The core logic remains based on the Chande Momentum Oscillator (CMO) capturing momentum turning points, but compared to the original version, it adds CMO continuity confirmation and a CMO pullback sell mechanism. The strategy pursues higher returns with an initial ROI of 75.2%, paired with a looser stop-loss (-33.6%) to accommodate larger price fluctuations.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | CMO continuous 3-period confirmation crossing above zero (shift(2) crossed, shift(1)>=0, current>=0) |
| **Sell Conditions** | Price breaks Bollinger upper band OR CMO crosses below -35 |
| **Protection** | Trailing stop (+1.523% activation, +10.329% trigger) |
| **Timeframe** | 5m |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table (Staged Profit-Taking)
minimal_roi = {
    "0": 0.75242,      # 0 minutes: 75.2% profit
    "827": 0.39114,    # ~14 hours later: 39.1% profit
    "2168": 0.34123,   # ~36 hours later: 34.1% profit
    "3527": 0          # ~59 hours later: break-even exit
}

# Stop-Loss Setting
stoploss = -0.33572  # -33.6% hard stop-loss (very loose)
```

**Design Philosophy**:
- **Extremely High ROI Target**: Initial ROI of 75.2%, far exceeding Chandem's 28.4%; indicates strategy pursues massive profits
- **Extremely Loose Stop-Loss**: -33.6% stop-loss provides massive room for price fluctuation
- **Staged Exit**: 4-tier ROI settings; profit targets decrease over time but remain far above ordinary strategies

### 2.2 Trailing Stop Configuration

```python
# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.01523    # Activates at 1.523% profit
trailing_stop_positive_offset = 0.10329  # Triggers at 10.329% profit
trailing_only_offset_is_reached = True
```

**Logic**:
- Trailing stop activates when profit reaches 1.523%
- Locks in 10.329% - 1.523% = 8.806% profit when reached
- More flexible than the 33.6% hard stop-loss; can lock in partial profits in trending markets

### 2.3 Order Type Configuration

```python
use_exit_signal = True
exit_profit_only = True  # Exit only when profitable
ignore_roi_if_entry_signal = False  # Do not ignore entry signal ROI
```

---

## III. Entry Conditions Details

### 3.1 Complete Buy Logic Analysis

```python
dataframe.loc[
    (
        # Condition 1: CMO 2 periods ago crossed above zero
        (qtpylib.crossed_above(dataframe["CMO"].shift(2), 0))
        # Condition 2: CMO 1 period ago >= 0
        & (dataframe["CMO"].shift(1) >= 0)
        # Condition 3: CMO current >= 0
        & (dataframe["CMO"] >= 0)
    ),
    'buy'] = 1
```

**Logic Analysis**:

1. **CMO Indicator 3-Consecutive-Period Confirmation Above Zero**:
   - This is a **stricter momentum confirmation mechanism**
   - Requires CMO not only to cross above zero but to stay above zero for 3 consecutive periods
   - Compared to Chandem's single-period cross (shift(1)), Chandemtwo dramatically reduces false signal probability

2. **Triple Timing Filter**:
   - `crossed_above(dataframe["CMO"].shift(2), 0)`: Confirmed cross 2 periods ago
   - `dataframe["CMO"].shift(1) >= 0`: Stayed positive 1 period ago
   - `dataframe["CMO"] >= 0`: Currently stays positive
   - This design ensures buy signals occur during a **sustained momentum strengthening** phase

### 3.2 Indicator Calculations

```python
# CMO Calculation
dataframe['CMO'] = ta.CMO(dataframe, timeperiod=50)

# Bollinger Bands Calculation (qtpylib version)
bollinger = qtpylib.bollinger_bands(
    qtpylib.typical_price(dataframe),  # Typical Price = (H+L+C)/3
    window=25,
    stds=3.5  # 3.5x standard deviation
)
dataframe['bb_lowerband'] = bollinger['lower']
dataframe['bb_middleband'] = bollinger['mid']
dataframe['bb_upperband'] = bollinger['upper']

# Bollinger Bands Calculation (TA-Lib version, for reference only)
bollingerTA = ta.BBANDS(dataframe, timeperiod=25, nbdevup=3.2, nbdevdn=3.2)
```

---

## IV. Exit Logic Details

### 4.1 Sell Conditions (Dual Trigger Mechanism)

```python
dataframe.loc[
    (
        # Condition 1: Price breaks Bollinger upper band
        (qtpylib.crossed_above(dataframe['close'], dataframe['bb_upperband']))
        # Condition 2: CMO crosses below -35
        | (qtpylib.crossed_below(dataframe["CMO"], -35))
    ),
    'sell'] = 1
```

**Logic Analysis**:

1. **Bollinger Upper Band Breakout**:
   - Price breaking above the Bollinger upper band indicates **price is at an extreme high**
   - This is a **trend reversal warning signal**
   - Same as Chandem strategy's sell condition

2. **CMO Pullback Sell (New Addition)**:
   - When CMO crosses from above to below -35, sell is triggered
   - This is a **momentum decay signal**; indicates upward momentum has exhausted
   - This is the key improvement of Chandemtwo over Chandem

3. **Dual Trigger Logic**:
   - The two sell conditions are in an **OR relationship**
   - Either condition satisfied triggers the sell signal
   - Increases sell mechanism flexibility

### 4.2 ROI Exit Mechanism

| Holding Time | Minimum Profit Rate | Triggers Exit |
|-------------|---------------------|---------------|
| 0 minutes | 75.2% | Exit immediately when reached |
| 827 minutes (~14 hours) | 39.1% | Exit if exceeded |
| 2168 minutes (~36 hours) | 34.1% | Exit if exceeded |
| 3527 minutes (~59 hours) | 0% | Break-even exit |

**Special Note**: Chandemtwo's initial ROI is as high as 75.2%, an extremely aggressive target. This target may be difficult to achieve quickly in most market environments.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameter | Purpose |
|-------------------|-------------------|-----------|---------|
| **Momentum Indicator** | CMO | 50 periods | Captures momentum turning points and momentum decay |
| **Volatility Indicator** | Bollinger Bands | 25 periods, 3.5σ | Identifies price extremes |
| **Price Type** | Typical Price | (H+L+C)/3 | Bollinger Band calculation basis |

### 5.2 Indicator Details

#### CMO (Chande Momentum Oscillator)

- **Calculation**: Momentum indicator similar to RSI
- **Range**: -100 to +100
- **Strategy Logic**:
  - CMO < 0 → Recent downward momentum dominates
  - CMO > 0 → Recent upward momentum dominates
  - CMO turns from negative to positive → Momentum shifts from bearish to bullish; buy signal
  - CMO crosses from high to below -35 → Momentum shifts from bullish to bearish; sell signal

#### Bollinger Bands

- **Parameters**: 25 periods, 3.5x standard deviation (relatively wide)
- **Why wider?**: Using 3.5σ instead of the conventional 2σ filters noise more effectively
- **Strategy Logic**:
  - Price touching upper band → Overbought signal; triggers sell

---

## VI. Risk Management Features

### 6.1 Hard Stop-Loss Mechanism

```python
stoploss = -0.33572  # -33.6% hard stop-loss
```

- **33.6% Stop-Loss**: Very loose; provides ample room for price fluctuation
- **Design Purpose**: Accommodates the 75.2% high ROI target; allows larger drawdowns
- **Risk Alert**: Maximum single-trade loss can reach 33.6%

### 6.2 Trailing Stop Mechanism

- **Activation Condition**: Profit ≥ 1.523%
- **Trigger Condition**: Profit ≥ 10.329%
- **Locked Profit**: 10.329% - 1.523% = 8.806%

### 6.3 ROI Exit Mechanism

- **Staged Exit**: 4 tiers; targets decrease in sequence
- **Logic**: Pursue extremely high profit early; exit steadily later

### 6.4 Risk Alerts

- **No Volume Filtering**: Buy signals don't verify volume; may produce false breakouts
- **Extremely High Stop-Loss Risk**: 33.6% stop-loss requires extremely high win rate or high reward-to-risk ratio
- **75.2% ROI Difficult to Achieve**: Initial target may cause extended holding periods
- **Trading Frequency**: 5m framework; due to stricter buy conditions, signals may be fewer

---

## VII. Strategy Pros & Cons

### Advantages

1. **Stricter Buy Signal**: CMO 3-consecutive-period confirmation dramatically reduces false signal probability
2. **Dual Sell Mechanism**: Bollinger upper band + CMO pullback; more flexible exits
3. **Momentum Decay Detection**: New CMO cross below -35 sell condition; exits timely when momentum weakens
4. **Extremely High ROI Target**: 75.2% target; suitable for strong trending markets
5. **Loose Stop-Loss**: 33.6% stop-loss with extremely high ROI; provides ample price fluctuation room
6. **Trailing Stop Protection**: Automatically locks in profits; prevents givebacks

### Limitations

1. **Parameter Sensitive**: CMO period (50) and Bollinger parameters (25, 3.5) significantly impact results
2. **75.2% ROI Too High**: Initial target may be difficult to achieve in short term; causes extended holding
3. **33.6% High Stop-Loss**: Requires extremely high win rate or high reward-to-risk ratio to be profitable
4. **No Trend Filter**: Strategy has no MA trend confirmation; may trade counter-trend
5. **No Volume Verification**: Volume is not used to filter signals
6. **Not Suitable for Ranging Markets**: High ROI target is difficult to achieve in ranging markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|---------------------------|-------|
| **Trending Uptrend** | Default parameters | CMO continuous confirmation + Bollinger upper band; suitable for momentum moves |
| **Trending Downtrend** | Use with caution | May generate counter-trend buy signals |
| **Ranging Market** | Not recommended | 75.2% ROI target difficult to achieve |
| **Extreme Volatility** | Adjust CMO parameters | CMO signals more reliable during high volatility |

---

## IX. Applicable Market Environment Details

### 9.1 Core Strategy Logic

Chandemtwo is an **enhanced momentum breakout strategy**, with core logic at three levels:

1. **Momentum Enhancement Layer**: Uses CMO 3-consecutive-period confirmation to capture momentum turning points from bearish to bullish
2. **Momentum Decay Layer**: Uses CMO crossing below -35 to detect momentum decay; exits timely
3. **Price Extreme Layer**: Uses Bollinger upper band to identify price extremes; triggers sell

### 9.2 Chandem vs Chandemtwo Comparison

| Feature | Chandem | Chandemtwo |
|---------|---------|------------|
| Buy Conditions | CMO crosses zero (single period) | CMO 3-consecutive-period confirmation (stricter) |
| Sell Conditions | Bollinger upper band breakout | Bollinger upper band + CMO below -35 |
| Initial ROI | 28.4% | 75.2% |
| Stop-Loss | -28% | -33.6% |
| Trailing Stop Activation | 1.013% | 1.523% |
| Trailing Stop Trigger | 10.858% | 10.329% |

**Conclusion**: Chandemtwo is an aggressive version of Chandem; stricter buys, more flexible sells, higher profit targets.

### 9.3 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Uptrend | Five Stars | CMO continuous confirmation at early trend; CMO pullback and BB upper band at late trend; fully captures |
| Downtrend | Two Stars | CMO may frequently cross above producing false signals; lacks trend filtering |
| Ranging Market | Two Stars | 75.2% ROI target difficult to achieve; extended holding |
| Extreme Volatility | Four Stars | CMO is sensitive to extreme price movements; BB parameters need adjustment |

### 9.4 Key Configuration Suggestions

| Configuration | Suggested Value | Notes |
|---------------|-----------------|-------|
| Trading Pairs | High-liquidity trending coins | Best results in trending markets |
| Trading Fees | < 0.1% | High ROI target requires low fees |
| ROI | 50%-75% | Initial target; adjust per market |
| Stop-Loss | -25% to -35% | Match initial ROI |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

- **Indicator Understanding**: Need to understand CMO and Bollinger Band meanings and calculations
- **Parameter Sensitivity**: 50-period CMO and 25-period 3.5σ Bollinger Bands need per-market adjustment
- **Signal Frequency**: 5m framework; due to stricter buy conditions, signals fewer than Chandem
- **Holding Time**: 75.2% ROI target may cause extended holding periods

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|----------------|
| 5-10 pairs | 1 GB | 2 GB |
| 20-30 pairs | 2 GB | 4 GB |

### 10.3 Backtesting vs Live Trading Differences

- **Slippage Impact**: 5m framework has moderate slippage sensitivity
- **Signal Delay**: CMO calculation requires some historical data
- **Liquidity Risk**: Using typical price for Bollinger Bands; slightly different from close price
- **ROI Achievement Rate**: 75.2% initial target may show high returns in backtesting but difficult to achieve live

### 10.4 Manual Trading Suggestions

1. Monitor CMO staying above zero for 3 consecutive periods
2. Confirm volume accompanies CMO cross
3. Observe CMO crossing below -35; prepare to sell
4. Observe Bollinger Band position; prepare to sell when price approaches upper band
5. Combine with trend MAs; avoid counter-trend trades

---

## XI. Summary

**Chandemtwo** is an **enhanced momentum breakout trading strategy**, with key improvements over Chandem:

1. **Stricter Buy Signal**: CMO 3-consecutive-period confirmation above zero; dramatically reduces false signals
2. **New CMO Pullback Sell**: CMO crossing below -35 triggers sell; exits timely when momentum weakens
3. **Higher Profit Target**: Initial ROI 75.2%; pursues greater profits
4. **Looser Stop-Loss**: -33.6% stop-loss; provides ample price fluctuation room

For quantitative traders, Chandemtwo is suitable for those **pursuing high profits in trending markets**, but need to pay attention to:

- 75.2% ROI target too high may cause extended holding periods
- 33.6% stop-loss requires extremely high win rate or high reward-to-risk ratio
- No trend filter may produce counter-trend trades
- Parameter sensitivity needs per-market adjustment

It is recommended to conduct sufficient testing on a paper trading account before live trading.
