# NostalgiaForInfinityNext_ChangeToTower_V6 Strategy Analysis

## Chapter 1: Strategy Overview

### 1.1 Strategy Background and Source

NostalgiaForInfinityNext_ChangeToTower_V6 is a customized quantitative trading strategy based on the renowned NostalgiaForInfinityV8 strategy, designed specifically for the Freqtrade trading framework. This strategy inherits the core design philosophy of the original version while incorporating innovative elements from the "ChangeToTower" series, forming a unique trading logic system.

The development team, iterativ, has deep technical expertise in the cryptocurrency quantitative trading field. The original NostalgiaForInfinity series enjoys a stellar reputation in the community, known for its multi-dimensional signal triggering mechanism and refined risk control system. Version V6, building on the strengths of previous generations, systematically reconstructs and optimizes the buy signal architecture.

### 1.2 Core Design Philosophy

The core design philosophy can be summarized as "Multi-Dimensional Resonance, Trend is King, Risk is Paramount":

**Multi-Dimensional Resonance**: The strategy employs 40 independent buy conditions and 8 sell conditions, covering technical indicators, price patterns, volume changes, and more. Only when multiple dimensions form resonance does the strategy trigger a trading signal, effectively reducing interference from false signals.

**Trend is King**: The strategy introduces multiple trend judgment tools, including EMA systems, SMA systems, Ichimoku Cloud, and SSL channels, ensuring trade direction aligns with the prevailing trend and avoiding counter-trend trading risks.

**Risk is Paramount**: The strategy embeds multi-layered risk control mechanisms, including dynamic stoploss, trailing stop, and profit protection mechanisms. It also incorporates BTC market trend filtering to suppress buy signals when the overall market declines, embodying a "survival first" risk management philosophy.

### 1.3 Applicable Scenarios and Trading Cycle

This strategy is specifically designed for 5-minute (5m) trading cycles and is applicable to cryptocurrency spot markets. The strategy recommends using USDT, BUSD, and other stablecoin trading pairs, avoiding BTC or ETH as quote currencies to reduce price volatility risks.

In practical application, the strategy recommends managing 4-6 concurrent positions simultaneously, with a dynamic screening list of 40-80 trading pairs, reducing single-pair risk exposure through diversification. The strategy strongly recommends adding leveraged tokens (such as *BULL, *BEAR, *UP, *DOWN) to the blacklist to avoid uncontrollable risks from abnormal volatility.

---

## Chapter 2: Technical Indicator System

### 2.1 Moving Average Systems

The strategy employs a comprehensive moving average analysis system, comprising Exponential Moving Averages (EMA) and Simple Moving Averages (SMA).

**EMA System**: Covers 10 periods — 12, 13, 15, 20, 25, 26, 35, 50, 100, and 200. EMA assigns higher weight to recent prices, responding more sensitively to price changes and serving as a crucial tool for short-term trend judgment. In the strategy, EMA200 is viewed as the dividing line for long-term trends — price above EMA200 indicates a bull market, below indicates a bear market.

**SMA System**: Covers 5 periods — 5, 15, 20, 30, and 200. SMA assigns equal weight to all price points, smoothing price fluctuations and being more suitable for judging medium-to-long-term trend direction. The strategy particularly monitors SMA200 slope changes — when SMA200 rises consecutively, it indicates the market is in a healthy bull trend.

### 2.2 Oscillator Combinations

**RSI (Relative Strength Index)**: The strategy uses multiple RSI periods, including 4, 14, and 20. RSI measures the speed and magnitude of price changes on a scale of 0-100. The strategy typically seeks buy opportunities when RSI falls below a certain threshold and sell opportunities when RSI exceeds a threshold. Notably, the strategy introduces 1-hour RSI as an auxiliary judgment, forming a multi-timeframe RSI resonance system.

**MFI (Money Flow Index)**: MFI combines price and volume information to determine capital inflow and outflow. The strategy requires MFI to be below a specific threshold in buy signals, indicating current capital outflow has reached an extreme and a rebound opportunity may exist.

**CTI (Cycle Trend Indicator)**: CTI measures the strength of price trends on a scale of -1 to 1. The strategy requires CTI to be below a specific negative value in buy signals, indicating the current trend has reached an oversold state.

**Williams %R**: Williams %R is a momentum indicator used to identify overbought/oversold zones. The strategy uses a 480-period Williams %R — an ultra-long-cycle overbought/oversold indicator capable of capturing extreme price deviations.

### 2.3 Volatility Indicators

**Bollinger Bands**: The strategy uses two Bollinger Band configurations — 20-period and 40-period. Bollinger Bands consist of middle, upper, and lower bands; price touching the lower band is typically viewed as an oversold signal. The strategy requires price to be below a certain percentage of the lower Bollinger Band in multiple buy conditions, seeking extreme price deviation opportunities.

**ATR (Average True Range)**: ATR measures market volatility. The strategy uses ATR to calculate dynamic stoploss levels and risk control levels, adjusting risk parameters based on market volatility to achieve adaptive risk management.

**Choppiness Index**: Used to determine if the market is in a ranging state. The Chop index ranges from 0-100, with higher values indicating a more ranging market. The strategy requires the Chop index to be below a specific threshold in certain buy conditions, avoiding trading in ranging markets.

### 2.4 Trend Judgment Tools

**Ichimoku Cloud**: The strategy introduces the Ichimoku system, comprising five core elements: Tenkan-sen (Conversion Line), Kijun-sen (Baseline), Leading Span A, Leading Span B, and Chikou Span (Lagging Span). The cloud provides rich trend judgment information — price above the cloud indicates a bull trend, below indicates a bear trend.

**SSL Channels**: SSL channels are a trend judgment tool that forms upper and lower bands by calculating moving averages of high/low prices combined with ATR. When the close breaks above the upper band, it's a bull signal; breaking below the lower band is a bear signal.

**Modified Elder Ray Index (MODERI)**: This is a modified Elder Ray index that combines volume-weighted moving averages to judge trend direction. The strategy uses 32, 64, and 96-period MODERI, forming a multi-layered trend confirmation system.

---

## Chapter 3: Buy Signal System

### 3.1 Buy Protection Mechanisms

The strategy configures independent protection parameters for each buy condition, forming a "goalkeeper" system for buy signals.

**EMA Trend Protection**: Divided into fast EMA protection and slow EMA protection. Fast EMA protection requires a specific-period EMA (such as 50 or 100 period) to be above EMA200, indicating an upward mid-term trend. Slow EMA protection requires the 1-hour-period EMA to be above EMA200, indicating a higher timeframe trend is upward.

**Price Position Protection**: Requires the close price to be above a specific EMA, ensuring no buying in an obvious downtrend. For example, requires close price above the 200-period EMA, indicating price is in a medium-to-long-term uptrend.

**SMA Slope Protection**: Requires SMA200 to continuously rise over a specific prior period, such as requiring SMA200 to maintain an upward trend over the past 28 periods, confirming trend stability.

**Safe Dips Protection**: One of the strategy's core protection mechanisms. By checking price drop magnitude across multiple time periods, it ensures no buying during excessively severe declines. The strategy defines 13 levels of safe dip thresholds, from 10 to 130, with each level corresponding to different drop tolerance levels.

**Safe Pump Protection**: Prevents buying after price surges. The strategy checks price gains within three time windows — 24h, 36h, and 48h. Buying is only permitted if the gain has not exceeded the threshold or if sufficient pullback has occurred.

**BTC Market Filtering**: The strategy introduces BTC's 1-hour trend as market environment filtering. When BTC is in a downtrend, specific buy signals are suppressed, avoiding position-building in environments with high systemic risk.

### 3.2 Buy Condition Details

The strategy defines 40 independent buy conditions, each targeting different market patterns and trading opportunities. Below are representative conditions explained in detail:

**Condition 1: Basic Trend-Following Buy**
- Trigger: Price gain relative to the lowest price of the past 36 candles exceeds a specific threshold, RSI in a reasonable range (below 36), MFI below 50, CTI below -0.92
- Protection requirement: SMA200 rising over the past 28 periods
- Trading logic: Seek pullback buying opportunities while the trend remains upward

**Condition 2: RSI Divergence Buy**
- Trigger: Current RSI diverging from 1h RSI, price below 98.3% of Bollinger lower band
- Protection requirement: Slow EMA protection active, requiring EMA20 1h value above EMA200
- Trading logic: Use RSI divergence to capture price reversal signals

**Condition 3: Bollinger Band Extreme Deviation Buy**
- Trigger: Price below the 40-period Bollinger lower band, bandwidth meeting specific conditions, price deviation from EMA200 within a reasonable range
- Protection requirement: Both fast and slow EMA protection active simultaneously
- Trading logic: Capture mean reversion after extreme deviation from the Bollinger lower band

**Condition 8: MODERI Confirmation Buy**
- Trigger: 96-period MODERI is bullish, CTI below -0.88, price below 99% of Bollinger lower band
- Protection requirement: Close price above 200-period EMA, slow EMA protection active
- Trading logic: Seek short-term oversold opportunities under multi-period trend confirmation

**Condition 18: Multi-Trend Confirmation Buy**
- Trigger: RSI below 33, price below 98.6% of Bollinger lower band, low volume
- Protection requirement: Fast EMA protection, slow EMA protection, close above EMA, SMA200 rising, 1h SMA200 rising — all active
- Trading logic: One of the strictest buy conditions, requiring all trend indicators to confirm upward

**Condition 27: Williams %R Extreme Buy**
- Trigger: 480-period Williams %R below -90, 1h Williams %R also below -90, RSI sum below 50, CTI below -0.93
- Protection requirement: BTC non-downtrend filter active
- Trading logic: Capture extreme oversold signals and await price reversal

**Conditions 32-38: Quick Trade Mode**
- Conditions 32 through 38 employ more aggressive buy logic, paired with dedicated fast exit logic
- These conditions typically complete trades in shorter timeframes, pursuing quick profits

**Condition 39: Ichimoku Trend Buy**
- Trigger: Tenkan line above Kijun line, price above the cloud, leading span A above leading span B, lagging span above the cloud, EFI positive, SSL channel bullish
- Protection requirement: BTC non-downtrend filter active
- Trading logic: Confirm bull trend via Ichimoku elements, buy on price pullback to SSL channel lower rail

**Condition 40: ZLEMA Crossover Buy**
- Trigger: 2-period ZLEMA crosses above 4-period ZLEMA, HRSI below 30, CCI below -200, RSI below 30
- Protection requirement: BTC non-downtrend filter active, TD Sequential meeting specific conditions
- Trading logic: Capture fast price reversal signals, confirmed by TD Sequential trend shift

---

## Chapter 4: Sell Signal System

### 4.1 Profit Target System

The strategy constructs a refined profit target system, setting differentiated sell conditions based on different profit ranges.

**Above EMA200 Profit Targets**:
- 1.2% profit: RSI below 34
- 2% profit: RSI below 35, CMF negative
- 3% profit: RSI below 36, CMF negative
- And so on, up to 20% profit target
- When MODERI96 is bullish (bull mode), profit targets are relatively loose; when bearish (bear mode), profit targets are stricter and include RSI upper bound conditions

**Below EMA200 Profit Targets**:
- Uses a similar but more conservative profit target system
- Given the downtrend environment, requires stricter RSI conditions at the same profit levels

**Pump Coin Profit Targets**:
- For coins that have surged beyond thresholds within 48h, 36h, and 24h windows
- Sets an independent profit target system across 5 tiers from 1% to 20%
- At higher profit ranges, requires lower RSI values, indicating possible short-term top

### 4.2 Trailing Stop Mechanisms

The strategy implements multi-level trailing stop mechanisms:

**Trailing Stop 1**: Profit between 3%-5%, RSI in 10-20 range, max profit exceeds current profit by more than 5%, and MODERI96 is bearish

**Trailing Stop 2**: Profit between 10%-40%, RSI in 20-50 range, max profit exceeds current profit by more than 3%, and EMA25 below EMA50

**Trailing Stop 3**: Profit between 6%-20%, max profit exceeds current profit by more than 5%, and 1h SMA200 is falling

**Trailing Stop 4**: Profit between 3%-6%, max profit exceeds current profit by more than 2%, and SMA200 is falling with CMF negative

### 4.3 Stoploss Mechanisms

**ATR Dynamic Stoploss**: Calculates dynamic stoploss levels based on ATR. When price falls below the threshold formed by the highest price minus an ATR multiplier, stoploss triggers. Different loss ranges use different ATR multipliers:
- -8% to -12% range: uses 5.4x ATR
- -12% to -16% range: uses 5.2x ATR
- -16% to -20% range: uses 5.0x ATR
- Below -20%: uses 2.0x ATR

**Recovery Stoploss**: When max loss exceeds a specific threshold (such as 12%) and profit recovers to a specific level (such as 6%), a sell is triggered. This is a protective mechanism against profit retracement.

**Long-Hold Stoploss**: For trades held longer than 900 minutes, sets an independent profit target range (3%-4%), avoiding long-term capital occupation.

### 4.4 Signal-Based Sells

The strategy defines 8 signal-based sell conditions:

**Sell Signal 1**: RSI above 79.5, price above Bollinger upper band for 5 consecutive candles

**Sell Signal 2**: RSI above 81, price above Bollinger upper band for 3 consecutive candles

**Sell Signal 4**: RSI above 73.4, 1h RSI above 79.6, dual RSI confirming overbought

**Sell Signal 6**: Price below EMA200 but above EMA50, RSI above 79, seeking rebound highs in a downtrend

**Sell Signal 7**: 1h RSI above 81.7, EMA12 crosses below EMA26, capturing trend shifts

**Sell Signal 8**: Price above 110% of 1h Bollinger upper band, extreme overbought signal

---

## Chapter 5: Risk Control Mechanisms

### 5.1 Multi-Timeframe Filtering

The strategy employs a "primary timeframe + auxiliary timeframe" dual confirmation mechanism. The primary timeframe is 5 minutes; the auxiliary is 1 hour. All buy signals require confirmation from the 1-hour timeframe trend, ensuring trade direction aligns with higher-level trends.

This design avoids the "can't see the forest for the trees" problem. When a buy signal appears on the 5-minute chart, the 1-hour chart confirms the overall trend direction, effectively reducing false signal rates.

### 5.2 BTC Market Environment Filtering

The strategy introduces BTC's market trend as a judgment basis for systemic risk. BTC, as a barometer of the cryptocurrency market, its movement often represents overall market risk appetite.

Implementation: Fetch BTC/USDT 1-hour candle data, calculate RSI and price change. When BTC is in a downtrend (close below close 2 candles ago and RSI below 50), specific buy signals are suppressed. This provides an extra layer of protection during market panic periods.

### 5.3 Hold Trade Support

The strategy provides Hold trade support, allowing users to specify via config file that particular trade IDs must be held until profitable. This feature applies to scenarios where users have special confidence in certain coins and wish to maintain positions beyond strategy signals.

Configuration: Create a `hold-trades.json` file in the strategy directory:
```json
{"trade_ids": [1, 3, 7], "profit_ratio": 0.005}
```
Or specify independent profit targets for each trade ID:
```json
{"trade_ids": {"1": 0.001, "3": -0.005, "7": 0.05}}
```

### 5.4 Backtesting Age Filtering

In backtesting mode, the strategy can simulate exchange age filtering. By setting the `bt_min_age_days` parameter, the strategy ignores trading pairs that have been listed for fewer than the specified days, avoiding judgment distortion due to insufficient data.

### 5.5 Exchange Outage Protection

In live and dry-run trading modes, the strategy monitors data continuity. If any zero-volume candles exist among the past 72 candles, this is treated as a data interruption and corresponding buy signals are suppressed. This mechanism prevents erroneous trades caused by exchange API interruptions or network issues.

---

## Chapter 6: Indicator Calculation Details

### 6.1 Auxiliary Indicator Functions

The strategy defines multiple auxiliary indicator calculation functions, enriching the technical analysis toolkit:

**EWO (Elliott Wave Oscillator)**:
```
EWO = (EMA5 - EMA35) / Close * 100
```
Used to identify momentum changes within Elliott Wave structures. Positive values typically indicate bull momentum; negative values indicate bear momentum.

**CMF (Chaikin Money Flow)**:
```
MFV = ((Close - Low) - (High - Close)) / (High - Low) * Volume
CMF = Sum(MFV, 20) / Sum(Volume, 20)
```
Combines price position and volume to measure money flow direction. Positive indicates capital inflow; negative indicates outflow.

**Williams %R**:
```
%R = (Highest High - Close) / (Highest High - Lowest Low) * (-100)
```
An overbought/oversold indicator ranging from -100 to 0. Below -80 is oversold; above -20 is overbought.

**HULL Moving Average**:
```
HULL = WMA(2 * WMA(Close, n/2) - WMA(Close, n), sqrt(n))
```
A low-lag moving average that responds to price changes more quickly while maintaining smoothness.

**ZLEMA (Zero-Lag EMA)**:
```
ZLEMA = EMA(Close + (Close - Close[lag]), period)
```
Achieves faster trend response by compensating for price lag.

### 6.2 PMAX Indicator

PMAX (Profit Maximizer) is one of the strategy's core indicators, combining moving averages and ATR:

Calculation steps:
1. Calculate the base moving average (supports EMA, DEMA, T3, SMA, VIDYA, TEMA, WMA, VWMA, ZEMA, and more)
2. Calculate ATR
3. Calculate base upper and lower bands:
   - Base upper band = MA + (multiplier/10) * ATR
   - Base lower band = MA - (multiplier/10) * ATR
4. Calculate final upper and lower bands through a specific algorithm
5. PMAX value switches between upper and lower bands, forming trend judgment

When price is below PMA, it serves as a support reference; when above PMA, it serves as a stoploss reference. This indicator combines trend following and dynamic stoploss functions.

### 6.3 Kalman Filter

The strategy introduces the Kalman filter for price data smoothing:

The Kalman filter is an adaptive filtering algorithm that reduces noise by estimating the price's "true value." The strategy applies it to HLC3 ((High+Low+Close)/3) and Low prices, forming a more stable signal foundation.

Calculation logic:
1. Calculate price change rate
2. Calculate true range
3. Calculate Lambda value (ratio of change rate to range)
4. Calculate Alpha value (adaptive smoothing coefficient)
5. Output filtered price

### 6.4 MODERI Indicator

Modified Elder Ray Index is a volume-weighted modified Elder Ray index:

```
VWMA_n = SMA(Close * Volume, n) / SMA(Volume, n)
EMA_VWMA = EMA(VWMA_n, n)
MODERI = EMA_VWMA >= EMA_VWMA[1]
```

When MODERI is True, it indicates the volume-weighted trend is upward; False indicates downward. The strategy uses 32, 64, and 96-period MODERI, forming a multi-layered trend confirmation system.

---

## Chapter 7: Strategy Parameter Configuration

### 7.1 Core Parameter Settings

**Timeframe Parameters**:
- `timeframe = '5m'`: Primary timeframe is 5 minutes
- `info_timeframe = '1h'`: Auxiliary timeframe is 1 hour
- `startup_candle_count = 480`: Strategy requires 480 candles of data for warmup

**Stoploss Parameters**:
- `stoploss = -0.10`: Fixed stoploss at -10%
- `trailing_stop = True`: Enable trailing stop
- `trailing_only_offset_is_reached = True`: Trail only activates after offset is reached
- `trailing_stop_positive = 0.01`: Trailing stop positive at 1%
- `trailing_stop_positive_offset = 0.03`: Trailing activation offset at 3%

**ROI Settings**:
```python
minimal_roi = {
    "0": 0.10,    # Immediate 10% take-profit
    "30": 0.05,   # 5% take-profit after 30 minutes
    "60": 0.02,   # 2% take-profit after 60 minutes
}
```

### 7.2 Buy Protection Parameter Matrix

Each buy condition (1-40) has an independent set of protection parameters:

| Parameter Name | Description | Example Value |
|---------------|-------------|--------------|
| ema_fast | Fast EMA protection | True/False |
| ema_fast_len | Fast EMA period | 50, 100 |
| ema_slow | Slow EMA protection | True/False |
| ema_slow_len | Slow EMA period | 20, 50, 100 |
| close_above_ema_fast | Close above fast EMA | True/False |
| close_above_ema_fast_len | Fast EMA period | 200 |
| sma200_rising | SMA200 rising | True/False |
| sma200_rising_val | SMA200 rising check period | 28 |
| safe_dips | Safe dips protection | True/False |
| safe_dips_type | Safe dips level | 50-130 |
| safe_pump | Safe pump protection | True/False |
| safe_pump_type | Safe pump level | 10-130 |
| safe_pump_period | Pump check period | 24, 36, 48 |
| btc_1h_not_downtrend | BTC non-downtrend | True/False |

### 7.3 Safe Dip Threshold Parameters

The strategy defines 13 levels of safe dip thresholds, each containing thresholds for 4 time periods:

Level 50 (normal dip) as an example:
- `buy_dip_threshold_50_1 = 0.02`: Current candle drop not exceeding 2%
- `buy_dip_threshold_50_2 = 0.14`: 2-candle drop not exceeding 14%
- `buy_dip_threshold_50_3 = 0.32`: 12-candle drop not exceeding 32%
- `buy_dip_threshold_50_4 = 0.5`: 144-candle drop not exceeding 50%

Lower levels (such as 10) are stricter — only dip-buy on tiny drops; higher levels (such as 130) are more permissive, allowing buying on larger declines.

### 7.4 Safe Pump Threshold Parameters

For the 24-hour, 36-hour, and 48-hour time windows, 13 levels of pump thresholds are defined:

Level 50, 24-hour as an example:
- `buy_pump_threshold_50_24 = 0.6`: 24-hour gain not exceeding 60%
- `buy_pump_pull_threshold_50_24 = 1.75`: Pullback coefficient

Pullback mechanism: Even if the gain exceeds the threshold, buying is still permitted if sufficient pullback has occurred (the gap between max price and current price is large enough). This avoids chasing at high prices.

---

## Chapter 8: Trade Execution Flow

### 8.1 Data Processing Flow

The strategy's data processing flow has several stages:

**Stage 1: Fetch Data**
- Fetch 5-minute candle data for the current trading pair
- Fetch 1-hour candle data for the current trading pair
- Fetch BTC/USDT 5-minute and 1-hour candle data

**Stage 2: Calculate Indicators**
- Calculate all technical indicators for the 5-minute timeframe
- Calculate all technical indicators for the 1-hour timeframe
- Calculate BTC RSI and trend judgment indicators

**Stage 3: Merge Data**
- Merge 1-hour indicators into 5-minute data
- Merge BTC indicators into current trading pair data

**Stage 4: Generate Signals**
- Check 40 buy conditions in sequence
- Check sell conditions
- Generate trading signals

### 8.2 Buy Signal Trigger Logic

Buy signal triggering uses a "protection conditions + trigger conditions" dual judgment mechanism:

```
Buy Signal = All Protection Conditions Met AND All Trigger Conditions Met
```

Protection condition example:
```python
if global_buy_protection_params["ema_fast"]:
    item_buy_protection_list.append(dataframe['ema_50'] > dataframe['ema_200'])
if global_buy_protection_params["sma200_rising"]:
    item_buy_protection_list.append(dataframe['sma_200'] > dataframe['sma_200'].shift(28))
```

Trigger condition example (Condition 1):
```python
item_buy_logic.append(((dataframe['close'] - dataframe['open'].rolling(36).min()) / dataframe['open'].rolling(36).min()) > self.buy_min_inc_1.value)
item_buy_logic.append(dataframe['rsi_14_1h'] > 20.0)
item_buy_logic.append(dataframe['rsi_14_1h'] < 84.0)
item_buy_logic.append(dataframe['rsi_14'] < 36.0)
item_buy_logic.append(dataframe['mfi'] < 50.0)
item_buy_logic.append(dataframe['cti'] < -0.92)
```

Only when all conditions are simultaneously met does the buy signal trigger. Each triggered buy condition is tagged in the `buy_tag` field for subsequent analysis.

### 8.3 Sell Signal Trigger Logic

Sell signal triggering uses a priority judgment mechanism:

1. First check if it's a quick trade mode (buy tags 32-38, 40) — if so, execute dedicated fast exit logic
2. Check if it's an Ichimoku trade (buy tag 39) — if so, execute Ichimoku sell logic
3. Check various sell signal types in sequence:
   - EMA200 above profit targets
   - EMA200 below profit targets
   - Pump coin profit targets
   - Downtrend coin profit targets
   - Trailing stops
   - Holding-time-related sells
   - Small profit exit below EMA200
   - Stoploss signals
   - Dump after downtrend sell
   - Pump coin extra sells
   - Post-recovery sells
   - Williams %R series sells
   - Signal-based sells

Once any sell signal triggers, immediately return the sell instruction and stop checking subsequent conditions.

### 8.4 Order Type Settings

The strategy configures detailed order types:

```python
order_types = {
    'buy': 'limit',              # Buy uses limit order
    'sell': 'limit',             # Sell uses limit order
    'trailing_stop_loss': 'limit', # Trailing stop uses limit order
    'stoploss': 'limit',         # Stoploss uses limit order
    'stoploss_on_exchange': False # Do not execute stoploss on exchange
}
```

The advantage of using limit orders is better fill prices, though they may not fill during extreme market conditions.

---

## Chapter 9: Strategy Optimization Suggestions

### 9.1 Parameter Optimization Directions

The strategy provides a large number of optimizable parameters; users can adjust them via Freqtrade's hyperparameter optimization:

**Buy Threshold Optimization**:
- RSI thresholds: Adjust upper and lower RSI limits across buy conditions
- CTI thresholds: Adjust trend strength thresholds
- Bollinger Band offset: Adjust price deviation tolerance relative to the lower band

**Protection Parameter Optimization**:
- EMA period selection: Choose appropriate EMA period combinations based on different market characteristics
- Safe dips level: Choose appropriate drop tolerance based on risk appetite
- Safe pump level: Adjust post-pump buy tolerance

**Profit Target Optimization**:
- Thresholds for each profit tier
- RSI conditions corresponding to each profit tier

### 9.2 Backtesting Verification Points

Before live trading use, thorough backtesting is recommended:

**Time Range Selection**:
- Cover at least one complete bull-bear cycle
- Include various market states (trending, ranging, extreme)

**Trading Pair Selection**:
- Choose pairs with good liquidity
- Avoid small-cap coins where slippage causes actual return deviation

**Fee Settings**:
- Set reasonable trading fees (typically 0.1%)
- Consider slippage impact

**Evaluation Metrics**:
- Focus on Max Drawdown
- Focus on Annual Return
- Focus on Sharpe Ratio
- Focus on Win Rate
- Focus on Profit Factor

### 9.3 Live Deployment Suggestions

**Capital Management**:
- Single trade amount should not exceed 10-20% of total capital
- Total positions should not exceed 50-60% of total capital
- Retain sufficient cash for extreme market conditions

**Risk Control Settings**:
- Adjust stoploss levels based on personal risk tolerance
- Consider enabling exchange-side stoploss as the last line of defense

**Monitoring and Alerts**:
- Set up Telegram or email notifications
- Regularly check strategy operation status
- Monitor API call frequency and balance changes

**Gradual Launch**:
- Test with small capital first
- Confirm strategy behavior matches expectations before increasing capital
- Review trading records regularly

---

## Chapter 10: Strategy Pros and Limitations

### 10.1 Strategy Advantages

**Multi-Dimensional Signal System**:
- 40 buy conditions covering various market patterns
- 8 sell conditions providing flexible exit mechanisms
- Multi-condition resonance effectively reduces false signal rates

**Refined Risk Management**:
- Multi-layered stoploss mechanisms
- Dynamic profit targets
- Trailing stop protecting profits
- BTC market environment filtering

**Strong Adaptability**:
- ATR dynamically adjusts risk parameters
- Multi-level dip/pump protection adapting to different market rhythms
- Support for multiple moving average types

**High Customizability**:
- Each buy condition can be independently toggled
- Detailed parameter configuration satisfying personalized needs
- Hold trade support for special position management

### 10.2 Strategy Limitations

**High Parameter Complexity**:
- Numerous parameters increase optimization difficulty
- Enormous parameter combination space, easy to overfit
- Requires deep understanding for effective tuning

**Computational Resource Requirements**:
- 40 buy conditions and numerous indicator calculations
- Requires 480-candle warmup period
- Multi-timeframe data fetching increases API calls

**Market Adaptability**:
- Specifically designed for cryptocurrency markets
- 5-minute cycle may not suit all trading styles
- May fail during extreme market conditions

**Data Quality Dependency**:
- Requires stable data sources
- API interruptions may cause strategy suspension
- Historical data quality impacts backtest accuracy

---

## Chapter 11: Summary and Outlook

### 11.1 Strategy Summary

NostalgiaForInfinityNext_ChangeToTower_V6 is a fully-featured, well-designed quantitative trading strategy. It inherits the excellent genes of the NostalgiaForInfinity series, constructing a multi-dimensional trading signal system through 40 carefully designed buy conditions and 8 sell conditions. The strategy particularly emphasizes risk management, introducing multi-layered protection mechanisms and BTC market environment filtering, embodying a prudent trading philosophy.

### 11.2 Target Users

This strategy is suitable for:
- Users with some quantitative trading background
- Return-seeking, risk-averse investors
- Users willing to spend time researching and optimizing strategy parameters
- Traders with a basic understanding of cryptocurrency markets

### 11.3 Future Outlook

As the cryptocurrency market evolves, the strategy requires continuous refinement:
- May introduce machine learning models to assist signal judgment
- Consider adding on-chain data as auxiliary judgment basis
- Optimize computational efficiency to reduce resource consumption
- Enhance capability to handle extreme market conditions

Continuous strategy optimization requires users to constantly summarize experience during use and adjust parameters in line with market changes to maximize its value.

---

*Document Version: V1.0*
*Generated: March 26, 2026*
*Strategy Source: iterativ / NostalgiaForInfinityV8*
