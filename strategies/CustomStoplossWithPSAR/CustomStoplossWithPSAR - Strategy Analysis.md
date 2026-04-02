# CustomStoplossWithPSAR Strategy: In-Depth Analysis

## Chapter 1: Strategy Overview and Design Philosophy

### 1.1 Strategy Background

In quantitative trading, stoploss strategy is one of the most critical components of risk management. Traditional fixed-percentage stoploss methods have obvious flaws: a stop distance set too small gets triggered by normal market fluctuations, causing unnecessary losses; a stop distance set too large fails to effectively protect capital. CustomStoplossWithPSAR is precisely designed to resolve this contradiction — it uses Parabolic SAR as the basis for dynamic stoploss, implementing the trading philosophy of "letting profits run while cutting losses short."

### 1.2 Core Design Philosophy

The strategy's design philosophy stems from two core understandings:

**First, market trends have inertia.** When a price forms a clear trend, it often continues for some time. The Parabolic SAR indicator can effectively identify and track this trend. Its unique parabolic design allows the stop level to progressively tighten as the trend develops, protecting existing profits while giving price adequate breathing room.

**Second, stoploss should be dynamically adjusted.** Fixed stoploss ignores the dynamic changes in market volatility. CustomStoplossWithPSAR reads the PSAR indicator value in real-time, using it as a dynamic stop level, enabling the stoploss strategy to adapt to market conditions.

### 1.3 Strategy Positioning

This strategy's position within the Freqtrade framework is a "stoploss strategy template" rather than a complete trading strategy. The documentation explicitly states: "you are supposed to take the `custom_stoploss()` and `populate_indicators()` parts and adapt it to your own strategy." This means the primary value of this strategy lies in demonstrating how to implement PSAR-based custom stoploss functionality — the entry signal portion is designed as a simple placeholder implementation.

---

## Chapter 2: Parabolic SAR Indicator — In-Depth Analysis

### 2.1 PSAR Indicator Basics

Parabolic SAR (Parabolic Stop and Reverse) was first introduced by J. Welles Wilder in 1978 in his book "New Concepts in Technical Trading Systems." This indicator appears on charts as a series of dot markers above or below prices, forming a parabolic curve.

### 2.2 Calculation Formula

PSAR calculation involves multiple variables, with core formulas as follows:

**SAR Calculation in Uptrend:**
```
SAR(n) = SAR(n-1) + AF × (EP(n-1) - SAR(n-1))
```

**SAR Calculation in Downtrend:**
```
SAR(n) = SAR(n-1) - AF × (EP(n-1) - SAR(n-1))
```

Where:
- SAR(n): Current period's SAR value
- SAR(n-1): Previous period's SAR value
- AF (Acceleration Factor): Starts at 0.02, increases by 0.02 each time price makes a new high (uptrend) or new low (downtrend), maximum 0.20
- EP (Extreme Price): Highest price in current uptrend or lowest price in current downtrend

### 2.3 Indicator Characteristics

PSAR has the following key characteristics:

**Trend-Following Characteristic:** PSAR is always positioned on one side of the price curve — below price in uptrends and above price in downtrends. This design enables the indicator to continuously follow trend development.

**Dynamic Acceleration Characteristic:** The AF increment mechanism causes SAR values to progressively approach price during trend continuation. The longer the trend persists and the more times new highs/lows are made, the more tightly SAR tracks. This characteristic perfectly suits trailing stoploss needs.

**Reversal Signal Characteristic:** When price crosses the SAR value, the indicator switches to the other side of price and resets the acceleration factor. This reversal mechanism can be used to determine trend changes.

### 2.4 Application in This Strategy

CustomStoplossWithPSAR computes the indicator via `ta.SAR(dataframe)`, using TA-Lib's SAR function with default parameters (acceleration factor start: 0.02, maximum: 0.20), storing results in the DataFrame's `sar` column.

---

## Chapter 3: Strategy Architecture and Code Structure

### 3.1 Class Inheritance

```python
class CustomStoplossWithPSAR(IStrategy):
```

The strategy inherits from Freqtrade's `IStrategy` interface class, the base class for all Freqtrade strategies, which defines the core method framework that strategies must implement.

### 3.2 Core Attribute Configuration

```python
timeframe = '1h'
stoploss = -0.2
custom_info = {}
use_custom_stoploss = True
```

**timeframe = '1h'**: The strategy uses a 1-hour timeframe. This balances signal frequency against noise filtering.

**stoploss = -0.2**: A 20% hard stoploss is set as final protection — a floor mechanism ensuring maximum loss does not exceed 20%.

**custom_info = {}**: A dictionary used to store SAR data per trading pair, primarily for backtesting.

**use_custom_stoploss = True**: The key switch enabling custom stoploss. When True, Freqtrade calls `custom_stoploss()` after each candle update.

### 3.3 Method Architecture

```
CustomStoplossWithPSAR
├── populate_indicators()    # Calculate technical indicators
│   └── Calculate SAR indicator
│   └── Store data to custom_info (backtest mode)
├── populate_entry_trend()   # Generate entry signals
│   └── Buy when SAR drops
├── populate_exit_trend()    # Generate exit signals
│   └── Signals disabled — exits via stoploss only
└── custom_stoploss()        # Custom stoploss logic
    └── Get latest SAR value
    └── Calculate relative stoploss distance
    └── Return stoploss ratio
```

---

## Chapter 4: populate_indicators Method Details

### 4.1 SAR Indicator Calculation

```python
dataframe['sar'] = ta.SAR(dataframe)
```

Uses TA-Lib's abstract interface to calculate the PSAR indicator. With default parameters, the function uses acceleration factor start: 0.02, maximum: 0.20.

### 4.2 Backtest Mode Data Storage

```python
if self.dp.runmode.value in ('backtest', 'hyperopt'):
    self.custom_info[metadata['pair']] = dataframe[['date', 'sar']].copy().set_index('date')
```

This code reflects the architectural difference between backtest and live trading modes. In backtest mode, data is stored for `custom_stoploss()` callbacks; in live mode, data is fetched in real-time via DataProvider.

---

## Chapter 5: custom_stoploss Method Deep Dive

### 5.1 Method Signature

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
```

Parameters:
- `pair`: Trading pair symbol (e.g., 'BTC/USDT')
- `trade`: Trade object containing position details
- `current_time`: Current time
- `current_rate`: Current price
- `current_profit`: Current profit/loss ratio

### 5.2 Stoploss Distance Calculation

```python
if (relative_sl is not None):
    new_stoploss = (current_rate - relative_sl) / current_rate
    result = new_stoploss - 1
```

This is the core algorithm of the strategy. The return value represents the stoploss trigger threshold relative to the current price. Freqtrade interprets the return value as: "trigger stoploss when price drops by this percentage from current price."

**Example:**
- current_rate = 100, SAR = 95
- new_stoploss = (100 - 95) / 100 = 0.05
- result = 0.05 - 1 = -0.95
- This means: trigger stoploss when price drops 5%

---

## Chapter 6: Entry Signal Logic Analysis

### 6.1 populate_entry_trend Method

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (dataframe['sar'] < dataframe['sar'].shift())
        ),
        'buy'] = 1
    return dataframe
```

The entry logic is deliberately minimal: buy when the current SAR value is lower than the previous candle's SAR value. The documentation explicitly notes this is a "nonsensical" placeholder entry — users should replace it with their own entry strategy.

---

## Chapter 7: Exit Signal Logic Analysis

### 7.1 populate_exit_trend Method

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[:, 'sell'] = 0
    return dataframe
```

Signals are explicitly disabled — all `sell` column values are set to 0. This means exits are managed entirely via the custom stoploss mechanism. This is the correct design choice.

### 7.2 Actual Exit Mechanisms

With signal exits disabled, trades will end via:
1. **Custom stoploss triggered**: PSAR stop level is touched
2. **Hard stoploss triggered**: Loss reaches 20%
3. **Manual intervention**: User manually closes position

---

## Chapter 8: Backtest vs. Live Differences

### 8.1 Run Mode Detection

```python
if self.dp.runmode.value in ('backtest', 'hyperopt'):
```

Freqtrade provides the current run mode via `dp.runmode`: `backtest`, `hyperopt`, `live`, or `dry_run`.

### 8.2 Backtest Mode Workflow

**Initialization:** Historical OHLCV data is loaded, `populate_indicators()` computes all indicators once, and SAR data is stored in `custom_info`.

**Trading Simulation:** Freqtrade simulates price sequence movement, calling `custom_stoploss()` whenever stoploss is checked.

### 8.3 Live Mode Workflow

**Real-time Operation:** DataProvider continuously receives new candle data, `populate_indicators()` is called on each candle update, and `custom_stoploss()` fetches the latest analyzed data via `get_analyzed_dataframe()`.

---

## Chapter 9: Strategy Optimization Recommendations

### 9.1 Entry Logic Improvements

**Trend Confirmation:**
```python
dataframe['sar_trend'] = np.where(dataframe['close'] > dataframe['sar'], 1, -1)
dataframe.loc[
    (
        (dataframe['sar'] < dataframe['sar'].shift()) &
        (dataframe['sar_trend'] == 1)
    ),
    'buy'] = 1
```

**Multi-Indicator Combination:**
```python
dataframe['rsi'] = ta.RSI(dataframe)
dataframe.loc[
    (
        (dataframe['sar'] < dataframe['sar'].shift()) &
        (dataframe['rsi'] < 70)
    ),
    'buy'] = 1
```

### 9.2 Stoploss Logic Optimization

**Profit Protection:**
```python
if current_profit > 0.05:
    sar_stoploss = (current_rate - relative_sl) / current_rate
    result = max(sar_stoploss - 1, -0.03)  # Lock in at least 3% profit
```

---

## Chapter 10: Risk Analysis and Precautions

### 10.1 Strategy Risks

**Parameter Sensitivity:** PSAR is sensitive to acceleration factor parameters. Default parameters may be too aggressive or too conservative in certain market conditions.

**Trend Reversal Risk:** PSAR assumes trends will continue. In sideways markets, SAR frequently crosses price, causing repeated stoploss triggers.

**Gap Risk:** PSAR stoploss is based on historical prices and cannot predict gaps. Major news or events may cause price to gap through the stop level.

### 10.2 Implementation Risks

**Data Latency:** In live trading, data from `get_analyzed_dataframe()` may have brief delays.

**Exception Handling:** Current code lacks robust exception handling. If data is empty or SAR is NaN, code may crash or return incorrect results.

---

## Chapter 11: Summary and Application Recommendations

### 11.1 Strategy Value Summary

The core value of CustomStoplossWithPSAR lies in demonstrating the correct implementation of Freqtrade custom stoploss:

**Architecture Demonstration:** Shows how to use DataProvider for real-time data access, how to correctly use `.iloc[-1]` in callback methods, and how to handle backtest vs. live data access differences.

**PSAR Application:** Demonstrates applying technical indicators to stoploss decisions.

**Simplicity:** Strategy code is clean and easy to understand.

### 11.2 Applicable Scenarios

- **Trending Markets:** PSAR stoploss is most effective in clear trends, effectively tracking trends and protecting profits.
- **Medium-to-Long-Term Trading:** 1-hour timeframe suits medium-to-long-term trading, avoiding short-term noise.

### 11.3 Non-Applicable Scenarios

- **High-Frequency Trading:** Stoploss calculation requires data access — not suitable for high-frequency scenarios.
- **Ranging Markets:** Sideways consolidation causes frequent stoploss triggers.
- **Extreme Volatility:** SAR may not provide effective protection during violent market swings.

### 11.4 Final Recommendations

1. **Use as a Template:** Extract the stoploss logic and apply it to your own strategy.
2. **Optimize Entry Logic:** Replace the simple SAR-drop signal with a more reliable entry strategy.
3. **Add Risk Control Layers:** On top of PSAR stoploss, add maximum holding time and maximum loss limits.
4. **Sufficient Backtesting:** Test strategy performance under different market conditions.
5. **Small Fund Verification:** Verify strategy behavior matches expectations before going live with significant capital.
