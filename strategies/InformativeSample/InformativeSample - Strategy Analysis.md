# InformativeSample Strategy Analysis

## Chapter 1: Strategy Overview and Design Philosophy

### 1.1 Strategy Positioning

InformativeSample is a teaching example strategy written by Freqtrade core developer xmatthias. Its primary purpose is to demonstrate to users how to use the **Informative Pairs** feature within the Freqtrade framework. This feature allows a strategy to reference data from related trading pairs while analyzing a primary pair, enabling more comprehensive and accurate trading decisions.

As a teaching-focused strategy, InformativeSample does not pursue extreme trading performance. Instead, it emphasizes clear code structure and complete feature demonstration, making it an excellent introductory material for learning Freqtrade's advanced features.

### 1.2 Design Background

In quantitative trading, technical analysis of a single trading pair often has limitations. For example, when analyzing an altcoin pair, focusing only on that pair's price movements may overlook the overall market trend and sentiment. Bitcoin, as the benchmark of the cryptocurrency market, often has a significant impact on other coins' movements.

The InformativeSample strategy is designed around this insight: by introducing BTC/USDT data as a market reference and comparing the primary pair's technical indicators with Bitcoin's trend, trading signal reliability is improved.

### 1.3 Core Innovations

The strategy's core innovation lies in demonstrating the correct usage of the Freqtrade framework's **`informative_pairs()`** method. Specifically:

- How to define additional trading pair data to fetch
- How to handle data merging across different timeframes
- How to reference indicators from informative pairs in trading signals
- How to achieve data fusion using the `merge_informative_pair` function

These concepts are highly valuable for developing more complex cross-pair strategies.

---

## Chapter 2: Strategy Architecture and Parameter Configuration

### 2.1 Timeframe Design

The strategy employs a dual-timeframe design:

**Primary Timeframe: 5 Minutes (5m)**
- Used for technical analysis of the main trading pair
- Serves as the base period for generating buy and sell signals
- Suitable for capturing short-to-medium-term trading opportunities

**Informative Timeframe: 15 Minutes (15m)**
- Used for BTC/USDT reference pair data acquisition
- A relatively longer period filters short-term noise
- Provides more stable market trend reference

This design follows the principle of "short-term trading, medium-term reference," ensuring trading sensitivity while avoiding overly frequent signal switching.

### 2.2 Take Profit Configuration (minimal_roi)

The strategy uses a staged take-profit mechanism:

```python
minimal_roi = {
    "60":  0.01,   # After 60 minutes: 1% profit target
    "30":  0.03,   # After 30 minutes: 3% profit target
    "20":  0.04,   # After 20 minutes: 4% profit target
    "0":   0.05    # Immediately: 5% profit target
}
```

This configuration embodies the wisdom of dynamic profit-taking:
- Early positions get more room to run (5%)
- As holding time increases, take-profit requirements gradually decrease
- Long-held positions shift to a break-even or minimal-profit mindset

### 2.3 Stop Loss Configuration

**Fixed Stop Loss: -10%**
```python
stoploss = -0.10
```

This stop-loss range is relatively loose, giving the strategy sufficient volatility tolerance. Considering cryptocurrency markets' high volatility, a 10% stop loss prevents being forced out by short-term pullbacks.

**Trailing Stop Configuration:**
```python
trailing_stop = True
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.04
```

Trailing stop mechanism:
1. Activates when profit reaches 4% (positive_offset)
2. Stop line follows the highest point, retreating by 2% (positive)
3. Once price retraces more than 2% from the high, stop-loss sell triggers

This configuration locks in partial profits while leaving room for continued price increases.

### 2.4 Order Type Settings

```python
order_types = {
    'buy': 'limit',           # Buy using limit orders
    'sell': 'limit',          # Sell using limit orders
    'stoploss': 'market',     # Stop loss using market orders
    'stoploss_on_exchange': False  # Stop loss not executed on exchange
}
```

Limit orders offer better control over fill prices, while market orders for stop loss ensure rapid exit in emergencies.

---

## Chapter 3: Technical Indicator System

### 3.1 Indicator Selection Logic

The InformativeSample strategy uses a concise but effective combination of technical indicators:

**Main Trading Pair Indicators:**
- EMA 20: Short-term trend reference line
- EMA 50: Medium-term trend reference line
- EMA 100: Long-term trend reference line

**Reference Pair (BTC/USDT) Indicators:**
- SMA 20: 20-period simple moving average

This indicator system advantages:
1. Uses moving averages to capture trend direction
2. Uses different-period moving average combinations to assess trend strength
3. Introduces external reference to enhance signal reliability
4. Streamlined indicator count, high computational efficiency

### 3.2 EMA Indicator Details

Exponential Moving Average (EMA), compared to Simple Moving Average (SMA), gives higher weight to recent prices and responds to price changes more quickly.

**EMA 20:**
- Represents approximately 20-period weighted average price
- Sensitive to price changes, commonly used for short-term trend judgment
- When price is above EMA 20, short-term trend is upward

**EMA 50:**
- Important medium-term trend reference
- Often used as the bull/bear dividing line
- Price above EMA 50 typically indicates a bullish market

**EMA 100:**
- Long-term trend indicator
- Less volatile, suitable for judging large-cycle trends
- Forms a complete multi-cycle analysis system with EMA 20 and EMA 50

### 3.3 SMA Indicator Description

Simple Moving Average (SMA) gives equal weight to all data points, making it smoother than EMA.

The strategy uses BTC/USDT's SMA 20 as a market trend reference baseline. When BTC price is above its SMA 20, Bitcoin is in a short-term uptrend and overall cryptocurrency market sentiment may be optimistic.

### 3.4 Indicator Calculation Code Analysis

```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    # Main trading pair indicator calculation
    dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
    dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
    
    if self.dp:
        # Get informative pair data
        inf_tf = '15m'
        informative = self.dp.get_pair_dataframe(pair=f"BTC/USDT", timeframe=inf_tf)
        
        # Calculate informative pair indicators
        informative['sma20'] = informative['close'].rolling(20).mean()
        
        # Merge dataframes
        dataframe = merge_informative_pair(dataframe, informative,
                                           self.timeframe, inf_tf, ffill=True)
    
    return dataframe
```

Code execution flow:
1. Calculate three EMA indicators for the main trading pair
2. Check if DataProvider is available
3. Get BTC/USDT data on 15-minute timeframe
4. Calculate BTC's SMA 20 indicator
5. Use merge_informative_pair to merge the two dataframes

---

## Chapter 4: Deep Dive into the Informative Pairs Mechanism

### 4.1 The informative_pairs Method

This is the key method for defining additional data sources in the Freqtrade framework:

```python
def informative_pairs(self):
    return [(f"BTC/USDT", '15m')]
```

This method returns a list of tuples, each containing:
- Trading pair name (e.g., "BTC/USDT")
- Timeframe (e.g., '15m')

Freqtrade automatically fetches and caches this data during runtime for the strategy to use.

### 4.2 Role of DataProvider

DataProvider (self.dp) is the data access interface provided by Freqtrade, with main functions:

1. **Historical data retrieval**: Get OHLCV data for specified trading pairs and timeframes via `get_pair_dataframe`
2. **Real-time data access**: Provides current market state information
3. **Wallet state queries**: Get current account balance and similar information
4. **Trade state management**: Query current positions and order status

In InformativeSample, DataProvider is primarily used to fetch BTC/USDT historical data.

### 4.3 The merge_informative_pair Function

This is the core technical point of this strategy. The function merges dataframes from two different timeframes into one:

```python
dataframe = merge_informative_pair(dataframe, informative,
                                   self.timeframe, inf_tf, ffill=True)
```

**Parameter explanation:**
- `dataframe`: Primary dataframe (5-minute period)
- `informative`: Informative dataframe (15-minute period)
- `self.timeframe`: Primary timeframe ('5m')
- `inf_tf`: Informative timeframe ('15m')
- `ffill`: Whether to use forward fill for missing values

**Post-merge column naming convention:**
- Informative pair price columns are renamed in format: `{column}_{timeframe}`
- E.g., `close_15m`, `sma20_15m`

This naming convention ensures uniqueness in the merged dataframe, avoiding column name conflicts.

### 4.4 Timeframe Alignment Principle

When merging data of different periods, Freqtrade must solve the timestamp alignment problem:

- 5-minute candles produce one candle every 5 minutes
- 15-minute candles produce one candle every 15 minutes
- Each 15-minute candle corresponds to 3 five-minute candles

The `merge_informative_pair` function automatically handles this relationship, "broadcasting" 15-minute data to the corresponding 3 five-minute candles. Forward fill (`ffill=True`) ensures 5-minute candles can use the most recent valid values before the 15-minute update.

---

## Chapter 5: Buy Signal Logic Analysis

### 5.1 Buy Conditions Explained

The strategy's buy signal consists of two conditions that must be met simultaneously:

```python
dataframe.loc[
    (
        (dataframe['ema20'] > dataframe['ema50']) &
        (dataframe['close_15m'] > dataframe['sma20_15m'])
    ),
    'buy'] = 1
```

**Condition 1: EMA 20 > EMA 50**

This is a classic moving average golden cross condition. When the short-term moving average (EMA 20) is above the medium-term moving average (EMA 50):
- Recent price momentum is relatively strong
- Short-term trend is upward
- Bulls have the upper hand

**Condition 2: BTC/USDT Price > SMA 20**

This is an innovative condition using external reference:
- `close_15m` is BTC/USDT's 15-minute closing price
- `sma20_15m` is BTC's 20-period simple moving average
- When BTC price is above its SMA 20, Bitcoin is in a short-term uptrend

### 5.2 Significance of Dual Verification

This combination of two conditions reflects a "trade with the trend" philosophy:

1. **Primary pair confirmation**: EMA 20 > EMA 50 ensures we only enter when long signals are clear
2. **Market environment confirmation**: BTC uptrend ensures overall market sentiment is favorable

This dual verification mechanism effectively filters risky signals:
- Primary pair rising but BTC falling (possibly isolated, low sustainability)
- BTC rising but primary pair falling (overall market good but the target is weak)

Only when both resonate does a buy signal generate.

### 5.3 Visual Understanding of Buy Signal

Imagine a coordinate system:
- X-axis represents the main trading pair's trend strength (position of EMA 20 relative to EMA 50)
- Y-axis represents market environment (BTC's position relative to its SMA 20)

Buy signals only appear in the first quadrant: both dimensions are positive. This design, while possibly missing some independent moves, greatly improves signal reliability.

### 5.4 Potential Improvement Space

The current buy logic can be further expanded:

1. **Add volume confirmation**:
   ```python
   (dataframe['volume'] > dataframe['volume'].rolling(20).mean())
   ```

2. **Add RSI filter**:
   ```python
   (ta.RSI(dataframe, timeperiod=14) < 70)  # Avoid buying in overbought zone
   ```

3. **Consider BTC's relative strength**:
   Not just whether BTC is above SMA, but also BTC's performance relative to other major coins

---

## Chapter 6: Sell Signal Logic Analysis

### 6.1 Sell Conditions Explained

The sell signal consists of two conditions:

```python
dataframe.loc[
    (
        (dataframe['ema20'] < dataframe['ema50']) &
        (dataframe['close_15m'] < dataframe['sma20_15m'])
    ),
    'sell'] = 1
```

**Condition 1: EMA 20 < EMA 50**

When the short-term moving average falls below the medium-term moving average:
- Short-term trend turns downward
- Possible trend reversal signal
- Advised to exit promptly for risk avoidance

**Condition 2: BTC/USDT Price < SMA 20**

When BTC price falls below its short-term moving average:
- Bitcoin's trend weakens
- Overall market sentiment may turn pessimistic
- Other coins may follow the decline

### 6.2 Symmetry of Sell Logic

Notice that sell logic is perfectly symmetrical with buy logic:
- Buy: EMA 20 > EMA 50 AND BTC > SMA 20
- Sell: EMA 20 < EMA 50 AND BTC < SMA 20

This symmetric design ensures strategy consistency and logical integrity. Entry and exit conditions form a mirror relationship, avoiding inconsistent strategy behavior in different market phases.

### 6.3 Sell Signal Execution Timing

Note that sell signals are just one trigger condition. Actual sell decisions also need to consider:

1. **Profit requirement**:
   ```python
   sell_profit_only = True
   ```
   Only executes signal sell when in profit, avoiding premature exit during losses.

2. **ROI constraint**:
   The minimal_roi configuration auto-sells upon reaching specific profit levels

3. **Stop-loss trigger**:
   Trailing stop executes sell while protecting profits

These three mechanisms work together to form a complete exit strategy.

### 6.4 Limitations of Current Sell Logic

The current sell logic is relatively simple and may have the following issues:

1. **Lagging**: Moving average crossover itself is a lagging indicator, potentially missing optimal exit timing
2. **False signals**: Frequent crossovers in ranging markets may cause unnecessary trades
3. **Lacks dynamic exit logic**: No adjustment of sell conditions based on holding time and profit

---

## Chapter 7: Risk Management Mechanisms

### 7.1 Layered Stop-Loss System

InformativeSample establishes a three-layer stop-loss protection mechanism:

**Layer 1: Fixed Stop Loss (-10%)**
- Acts as the last line of defense, preventing unlimited loss expansion
- Gives the strategy sufficient volatility tolerance space
- Suitable for extreme market conditions

**Layer 2: Trailing Stop (2% Retracement)**
- Activates when profit reaches 4%
- Stop line moves up with the highest point
- Locks in most floating profits

**Layer 3: ROI Take Profit**
- Dynamically adjusts based on holding time
- Short-term targets higher returns
- Long-term shifts to profit protection

### 7.2 Trailing Stop Explained

Trailing stop is an important risk control feature of this strategy:

```python
trailing_stop = True
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.04
```

**Mechanism:**
1. After opening, initial stop is set at -10%
2. When profit reaches 4%, trailing stop activates
3. Stop line set below the highest point by 2%
4. As price continues rising, stop line follows upward
5. When price retraces more than 2%, auto-sell triggers

**Example scenario:**
- Entry price: 100 USDT
- Initial stop: 90 USDT (-10%)
- When price rises to 104 USDT: trailing stop activates
- Stop line position: 101.92 USDT (104 × 0.98)
- When price rises to 120 USDT: stop line follows to 117.6 USDT
- When price retraces to below 117.6 USDT: auto-sells

### 7.3 ROI Strategy Analysis

The internal logic of the staged ROI configuration:

| Holding Time | Target Return | Design Intent |
|------------|--------------|---------------|
| 0 minutes | 5% | Sufficient profit room in early stage |
| 20 minutes | 4% | Short-term trade, seek quick profit |
| 30 minutes | 3% | Medium-term position, moderate expectations |
| 60 minutes | 1% | Long-term position, protect minimal profit exit |

This design reflects the "time is risk" philosophy: the longer the holding time, the greater the uncertainty, so gradually lowering profit requirements ensures securing some gains.

### 7.4 Comprehensive Risk Management Evaluation

**Advantages:**
1. Multi-layer stop-loss mechanism, controllable risk
2. Trailing stop effectively locks in profits
3. Dynamic ROI adapts to different holding periods
4. Fixed stop loss provides bottom-line protection

**Shortcomings:**
1. Large stop-loss range (10%), may incur significant drawdowns
2. High trailing stop trigger point (4%), may miss some profit opportunities
3. Lacks volatility-adaptive mechanism (e.g., ATR stop loss)

---

## Chapter 8: Strategy Optimization Suggestions

### 8.1 Indicator-Level Optimization

**Add volume confirmation:**
```python
# Volume expansion as entry confirmation
dataframe['volume_sma'] = dataframe['volume'].rolling(20).mean()
volume_confirm = dataframe['volume'] > dataframe['volume_sma'] * 1.2
```

**Introduce RSI filter:**
```python
# Avoid buying in overbought zone
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
rsi_filter = (dataframe['rsi'] > 30) & (dataframe['rsi'] < 70)
```

**Add MACD confirmation:**
```python
# Use MACD as trend strength confirmation
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']
macd_confirm = dataframe['macd'] > dataframe['macdsignal']
```

### 8.2 Informative Pair-Level Optimization

**Multi-coin reference:**
```python
def informative_pairs(self):
    return [
        ("BTC/USDT", '15m'),
        ("ETH/USDT", '15m'),  # Add ETH as reference
    ]
```

**Market-cap weighted reference:**
Assign different weights to reference coins based on trading pair market cap or importance.

**Relative strength reference:**
Not just whether BTC is above moving average, but also consider BTC's performance strength relative to other major coins.

### 8.3 Stop-Loss Strategy Optimization

**ATR dynamic stop loss:**
```python
dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
# Dynamically set stop-loss distance based on ATR
stop_loss_distance = dataframe['atr'] * 2
```

**Time-decay stop loss:**
```python
# The longer the holding time, the stricter the stop
if holding_time > 60:
    trailing_stop_positive = 0.01
elif holding_time > 30:
    trailing_stop_positive = 0.015
```

### 8.4 Hyperopt Parameter Optimization

Recommended optimization parameters:

1. **EMA period combinations**: Test different moving average combinations
2. **Trailing stop parameters**: Optimize trigger point and retracement range
3. **SMA period**: Test BTC reference's moving average period
4. **ROI configuration**: Optimize take-profit nodes based on historical data

---

## Chapter 9: Backtesting and Live Trading Considerations

### 9.1 Backtesting Recommendations

Key points for strategy backtesting:

**Time range selection:**
- Recommended to cover at least one complete bull-bear cycle (2-3 years)
- Include different market environments: uptrend, downtrend, oscillating
- Avoid selecting only periods with good performance

**Trading pair selection:**
- Test multiple different trading pairs
- Focus on pairs with good liquidity
- Avoid pairs highly correlated with BTC (would weaken the informative pair's effect)

**Fee settings:**
- Ensure backtesting sets reasonable trading fees
- Consider slippage impact
- Maker vs. taker fee differences for market vs. limit orders

### 9.2 Informative Pair Data Requirements

When using the informative pairs feature:

**Data completeness:**
- Ensure BTC/USDT data covers the same time range as the main trading pair
- Missing informative pair data will cause the strategy to fail

**Data synchronization:**
- Different exchange data may have time differences
- Ensure using data from the same exchange source

**Cache configuration:**
- Configure data cache reasonably to reduce API calls
- Monitor memory usage (informative pairs increase memory consumption)

### 9.3 Live Deployment Considerations

**Exchange compatibility:**
- Ensure exchange supports all trading pairs (including informative pairs)
- Check API limits and data fetching frequency

**Runtime environment:**
- Ensure server stability
- Monitor memory usage (informative pairs increase consumption)
- Set reasonable log levels

**Monitoring indicators:**
- Monitor informative pair data acquisition status
- Pay attention to signal generation frequency
- Track overall strategy P&L

---

## Chapter 10: Strategy Applicable Scenarios Analysis

### 10.1 Best Applicable Scenarios

InformativeSample is best suited for:

**Market environments:**
- Markets with clear trends (unilateral rise or fall)
- Periods when Bitcoin and other coins have high correlation
- Markets with moderate volatility

**Trading pair selection:**
- Medium-market-cap mainstream altcoins
- Pairs with some correlation to BTC but not completely synchronized
- Pairs with good liquidity and small spreads

**Timeframe:**
- Suitable for intraday and short-term swing trading
- Not suitable for high-frequency trading
- Not suitable for long-term investment

### 10.2 Not Applicable Scenarios

**Ranging markets:**
- Frequent moving average crossovers generate many false signals
- Trading costs may eat up profits
- Recommended to pause the strategy during ranging periods

**Extreme market conditions:**
- During rapid drops, stop loss may not execute in time
- During rapid rises, may exit too early
- Recommended to set market anomaly detection mechanisms

**Low-correlation coins:**
- Coins with low BTC correlation (e.g., some DeFi tokens)
- Informative pair reference value decreases
- Strategy advantages may not manifest

### 10.3 Strategy Variant Suggestions

Consider the following variants for different market environments:

**Trend-enhanced version:**
- Add trend strength filtering
- Use looser parameters in strong trends
- Tighten conditions in weak trends

**Hedging version:**
- Trade multiple coins simultaneously
- Use inter-coin correlation to build hedging portfolios
- Reduce systematic risk

**Multi-timeframe version:**
- Add longer timeframes (e.g., 1-hour, 4-hour)
- Use multi-cycle resonance to confirm signals
- Improve signal reliability

---

## Chapter 11: Summary and Outlook

### 11.1 Strategy Value Summary

As a teaching example strategy, InformativeSample's core value lies in:

**Technical educational value:**
- Completely demonstrates informative pairs usage
- Provides a reusable code structure
- Shows best practices for multi-timeframe data processing

**Design philosophy reference:**
- Dual-verification signal design concept
- Framework for introducing external reference to enhance decision-making
- Multi-layer risk management concept

**Scalability:**
- Clear strategy structure, easy to modify and expand
- Can easily add more indicators and conditions
- Supports combination with other strategy components

### 11.2 Limitation Analysis

Acknowledge the strategy's limitations:

**Performance:**
- The author explicitly states strategy performance is not ideal
- As an example, it hasn't been fully optimized
- Parameter settings may not suit actual trading

**Functionality:**
- Informative pair only uses BTC as a single reference
- Indicator combination is relatively simple
- Lacks market environment adaptive mechanism

**Applicability:**
- Primarily suitable for specific market environments
- Needs optimization based on actual conditions
- Not recommended for direct live trading

### 11.3 Learning Suggestions

For users wanting to deeply learn Freqtrade:

1. **Understand core concepts**: Focus on understanding `informative_pairs` and `merge_informative_pair` usage
2. **Hands-on practice**: Try modifying the strategy, adding new indicators and conditions
3. **Backtesting verification**: Test strategy performance in different market environments
4. **Parameter optimization**: Use Hyperopt to optimize strategy parameters
5. **Combinatorial innovation**: Combine informative pairs functionality with other strategy ideas

### 11.4 Future Outlook

The cross-pair reference concept demonstrated by InformativeSample has broad application prospects:

**Multi-dimensional reference:**
- Introduce more reference dimensions (e.g., market sentiment indicators, on-chain data)
- Build a more comprehensive market analysis framework

**Smart weighting:**
- Dynamically adjust reference weights based on market state
- Implement adaptive informative pair fusion

**Machine learning integration:**
- Use machine learning methods to automatically discover effective references
- Dynamically select optimal informative pair combinations

By deeply understanding InformativeSample's design philosophy and implementation details, developers can build more powerful and intelligent trading strategies on this foundation.
