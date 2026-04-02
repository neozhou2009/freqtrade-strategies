# Chandem Strategy In-Depth Analysis

> **Strategy ID**: 4th in Batch 81-90
> **Strategy Type**: CMO Momentum Breakout + Bollinger Band Trend Confirmation
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**Chandem** is a momentum breakout strategy based on the Chande Momentum Oscillator (CMO), incorporating Bollinger Band breakout signals for sell decisions. The core logic is concise: use the CMO indicator to capture momentum turning points, buying when CMO crosses above zero from negative territory, and selling when price breaks above the Bollinger upper band.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | CMO crosses above zero from negative (today's CMO >= 0 AND yesterday's CMO < 0) |
| **Sell Conditions** | Price breaks above Bollinger upper band (BB parameters: 25 periods, 3.5x standard deviation) |
| **Protection** | Trailing stop (+1.013% activation, +10.858% trigger) |
| **Timeframe** | 5m |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table (Staged Profit-Taking)
minimal_roi = {
    "0": 0.28396,      # 0 minutes: 28.4% profit
    "974": 0.09268,    # ~16 hours later: 9.3% profit
    "1740": 0.06554,   # ~29 hours later: 6.6% profit
    "3087": 0          # ~51 hours later: break-even exit
}

# Stop-Loss Setting
stoploss = -0.28031  # -28% hard stop-loss (relatively loose)
```

**Design Philosophy**:
- **High ROI Target**: Initial ROI at 28.4%, indicating the strategy pursues substantial profits
- **Loose Stop-Loss**: -28% stop-loss provides ample room for price fluctuation
- **Staged Exit**: 4-tier ROI settings, progressively lowering profit targets as holding time extends

### 2.2 Trailing Stop Configuration

```python
# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.01013    # Activates at 1.013% profit
trailing_stop_positive_offset = 0.10858  # Triggers at 10.858% profit
trailing_only_offset_is_reached = True
```

**Logic**:
- Trailing stop activates when profit reaches 1.013%
- Locks in 10.858% - 1.013% = 9.845% profit when reached
- More flexible compared to the 28% hard stop-loss

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
        # Condition 1: Today's CMO >= 0
        (dataframe["CMO"] >= 0)
        # Condition 2: Yesterday's CMO < 0 (crossed above zero)
        & (qtpylib.crossed_above(dataframe["CMO"].shift(1), 0))
    ),
    'buy'] = 1
```

**Logic Analysis**:

1. **CMO Indicator Crosses Above Zero**:
   - CMO (Chande Momentum Oscillator) is a momentum indicator
   - When CMO turns from negative to positive, short-term momentum strengthens
   - This is a classic **momentum reversal signal**

2. **Timing Confirmation**:
   - `dataframe["CMO"].shift(1)` retrieves yesterday's CMO value
   - `crossed_above` ensures it actually crossed rather than simply being above zero
   - Avoids false signals from oscillation near the zero line

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

### 4.1 Sell Conditions

```python
dataframe.loc[
    (
        # Condition: Price crosses above Bollinger upper band
        (qtpylib.crossed_above(dataframe['close'], dataframe['bb_upperband']))
    ),
    'sell'] = 1
```

**Logic Analysis**:

1. **Bollinger Upper Band Breakout**:
   - Price breaking above the Bollinger upper band typically indicates **price is at an extreme high**
   - This is a **trend reversal warning signal**
   - Combined with the high ROI target, the strategy locks in profits when price reaches extremes

2. **Coordination with Other Exit Mechanisms**:
   - After sell signal triggers, must satisfy `exit_profit_only = True`
   - Must have profit to actually sell

### 4.2 ROI Exit Mechanism

| Holding Time | Minimum Profit Rate | Triggers Exit |
|-------------|---------------------|---------------|
| 0 minutes | 28.4% | Exit immediately when reached |
| 974 minutes (~16 hours) | 9.3% | Exit if exceeded |
| 1740 minutes (~29 hours) | 6.6% | Exit if exceeded |
| 3087 minutes (~51 hours) | 0% | Break-even exit |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameter | Purpose |
|-------------------|-------------------|-----------|---------|
| **Momentum Indicator** | CMO | 50 periods | Captures momentum turning points |
| **Volatility Indicator** | Bollinger Bands | 25 periods, 3.5σ | Identifies price extremes |
| **Price Type** | Typical Price | (H+L+C)/3 | Bollinger Band calculation basis |

### 5.2 Indicator Details

#### CMO (Chande Momentum Oscillator)

- **Calculation**: Similar to RSI momentum indicator
- **Range**: -100 to +100
- **Strategy Logic**:
  - CMO < 0 → Recent downward momentum dominates
  - CMO > 0 → Recent upward momentum dominates
  - CMO turns from negative to positive → Momentum shifts from bearish to bullish; buy signal

#### Bollinger Bands

- **Parameters**: 25 periods, 3.5x standard deviation (relatively wide)
- **Why wider?**: Using 3.5σ instead of the conventional 2σ filters noise more effectively
- **Strategy Logic**:
  - Price touching upper band → Overbought signal; triggers sell

---

## VI. Risk Management Features

### 6.1 Hard Stop-Loss Mechanism

```python
stoploss = -0.28031  # -28% hard stop-loss
```

- **28% Stop-Loss**: Very loose; provides ample room for price fluctuation
- **Design Purpose**: Accommodates high ROI targets; allows short-term larger drawdowns
- **Risk Alert**: Maximum single-trade loss can reach 28%

### 6.2 Trailing Stop Mechanism

- **Activation Condition**: Profit ≥ 1.013%
- **Trigger Condition**: Profit ≥ 10.858%
- **Locked Profit**: 10.858% - 1.013% = 9.845%

### 6.3 ROI Exit Mechanism

- **Staged Exit**: 4 tiers; targets decrease in sequence
- **Logic**: Pursue high profit early; exit steadily later

### 6.4 Risk Alerts

- **No Volume Filtering**: Buy signals don't verify volume; may produce false breakouts
- **Loose Stop-Loss**: 28% stop-loss requires high win rate or high reward-to-risk ratio
- **Trading Frequency**: 5m timeframe has moderate trading frequency

---

## VII. Strategy Pros & Cons

### Advantages

1. **Concise Signals**: Buy and sell conditions each have only one criterion; clear and easy to understand
2. **Momentum Capture**: CMO crossing above zero is a classic momentum strengthening signal
3. **Loose Stop-Loss**: 28% stop-loss with 28% ROI; suitable for trending markets
4. **Bollinger Band Assist**: 3.5σ wide Bollinger Bands filter false breakouts
5. **Trailing Stop Protection**: Automatically locks in profits; prevents givebacks

### Limitations

1. **Parameter Sensitive**: CMO period (50) and Bollinger parameters (25, 3.5) significantly impact results
2. **Single Buy Signal**: No other indicator confirmation; may produce false signals
3. **High Stop-Loss Risk**: 28% stop-loss requires high win rate or high reward-to-risk ratio
4. **No Trend Filter**: Strategy has no moving average trend confirmation; may trade counter-trend
5. **No Volume Verification**: Volume is not used to filter signals

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|---------------------------|-------|
| **Trending Uptrend** | Default parameters | CMO cross + Bollinger upper band; suitable for momentum moves in trends |
| **Trending Downtrend** | Use with caution | May generate counter-trend buy signals |
| **Ranging Market** | Adjust BB parameters | Wide BB reduces false signals |
| **Extreme Volatility** | Adjust CMO parameters | CMO signals more reliable during high volatility |

---

## IX. Applicable Market Environment Details

### 9.1 Core Strategy Logic

Chandem is a **momentum breakout strategy**, with core logic at two levels:

1. **Momentum Layer**: Uses CMO to identify price momentum turning points from bearish to bullish
2. **Breakout Layer**: Uses Bollinger upper band to identify price extremes; triggers sell

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Uptrend | Five Stars | CMO cross occurs at early trend; Bollinger upper band breakout at late trend; fully captures |
| Downtrend | Two Stars | CMO may frequently cross above producing false signals; lacks trend filtering |
| Ranging Market | Three Stars | CMO oscillates near zero; may generate multiple signals |
| Extreme Volatility | Four Stars | CMO is sensitive to extreme price movements; BB parameters need adjustment |

### 9.3 Key Configuration Suggestions

| Configuration | Suggested Value | Notes |
|---------------|-----------------|-------|
| Trading Pairs | High-liquidity trending coins | Best results in trending markets |
| Trading Fees | < 0.1% | High ROI target requires low fees |
| ROI | 20%-30% | Initial target; adjust per market |
| Stop-Loss | -20% to -30% | Match initial ROI |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

- **Indicator Understanding**: Need to understand CMO and Bollinger Band meanings and calculations
- **Parameter Sensitivity**: 50-period CMO and 25-period 3.5σ Bollinger Bands need per-market adjustment
- **Signal Frequency**: 5m framework has moderate signal frequency; requires continuous monitoring

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|----------------|
| 5-10 pairs | 1 GB | 2 GB |
| 20-30 pairs | 2 GB | 4 GB |

### 10.3 Backtesting vs Live Trading Differences

- **Slippage Impact**: 5m framework has moderate slippage sensitivity
- **Signal Delay**: CMO calculation requires some historical data
- **Liquidity Risk**: Using typical price for Bollinger Bands; slightly different from close price

### 10.4 Manual Trading Suggestions

1. Monitor CMO crossing from negative to positive
2. Confirm volume accompanies CMO cross
3. Observe Bollinger Band position; prepare to sell when price approaches upper band
4. Combine with trend MAs; avoid counter-trend trades

---

## XI. Summary

**Chandem** is a **momentum breakout trading strategy**, with core value in:

1. **Concise Signal Logic**: CMO cross above for buy; Bollinger upper band breakout for sell
2. **High ROI Target**: Initial 28.4% profit target; pursues substantial gains
3. **Loose Stop-Loss**: 28% stop-loss provides ample price fluctuation room
4. **Trailing Stop Protection**: Automatically locks in profits; prevents givebacks

For quantitative traders, Chandem is suitable for those **pursuing substantial profits in trending markets**, but need to pay attention to:
- Loose stop-loss带来的单笔较大亏损风险
- No trend filter may produce counter-trend trades
- Parameter sensitivity needs per-market adjustment

It is recommended to conduct sufficient testing on a paper trading account before live trading.
