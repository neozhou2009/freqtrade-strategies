# Obelisk_TradePro_Ichi_v1_1 Strategy In-Depth Analysis

## Overview

**Obelisk_TradePro_Ichi_v1_1** is a classic technical analysis strategy based on the Ichimoku Kinko Hyo (Ichimoku Cloud) indicator, published by strategy developer Obelisk in March 2021. The core concept derives from the renowned trading education platform Trade Pro's video tutorial "Crazy Results Best Ichimoku Cloud Trading Strategy Proven 100 Trades," which systematically applies the five core elements of the Ichimoku indicator to construct a complete trend-following trading system.

The strategy employs cryptocurrency-optimized Ichimoku parameter configurations, combined with a rigorous multi-condition entry screening mechanism and clear stop-loss exit rules, demonstrating substantial profitability in historical backtesting on the FTX exchange. The strategy's core advantage lies in its multi-dimensional trend confirmation mechanism, which effectively filters false breakout signals by simultaneously examining price position relative to the cloud, the crossover relationship between the Tenkan-sen and Kijun-sen lines, and the lagging span position status, thereby improving win rate and risk-reward ratio.

---

## Chapter 1: Strategy Background and Theoretical Origins

### 1.1 Origins and Development of the Ichimoku Cloud

The Ichimoku Kinko Hyo was developed by Japanese journalist Goichi Hosoda (pen name Ichimoku Sanjin) in the late 1930s. The Japanese term "Ichimoku Kinko Hyo" translates to "one-glance equilibrium chart," embodying the design philosophy of intuitively presenting market equilibrium states. After decades of market validation, Ichimoku has become one of the widely used trend-following tools by traders worldwide.

The traditional Ichimoku system consists of five core components:

1. **Tenkan-sen (Conversion Line)**: 9-period median price, reflecting short-term market momentum
2. **Kijun-sen (Base Line)**: 26-period median price, representing medium-term market trend
3. **Senkou Span A (Leading Span A)**: Average of Tenkan-sen and Kijun-sen, displaced 26 periods forward
4. **Senkou Span B (Leading Span B)**: 52-period median price, displaced 26 periods forward
5. **Chikou Span (Lagging Span)**: Current closing price displaced 26 periods backward

These five components collectively form a complete "market map," allowing traders to judge market trend direction and momentum strength by observing the relationship between price and the cloud, crossovers between lines, and the position of the lagging span.

### 1.2 Cryptocurrency Market Specifics

Cryptocurrency markets possess significant differences compared to traditional financial markets: 24-hour continuous trading, higher volatility, more pronounced trends but also greater susceptibility to sharp corrections. These characteristics render the traditional Ichimoku parameters (9-26-52-26 configuration) less effective in cryptocurrency markets.

Obelisk_TradePro_Ichi_v1_1 systematically optimizes the traditional parameters for cryptocurrency market characteristics. By increasing the period parameters, the strategy better captures medium-to-long-term trends in cryptocurrency markets while reducing interference from short-term noise signals, thereby improving signal reliability.

### 1.3 Core Philosophy of the Trade Pro Strategy

The Trade Pro Ichimoku trading strategy emphasizes the principle of multiple confirmation: a single signal is often insufficient for reliable entry; traders should only consider entering when multiple independent technical signals simultaneously point in the same direction. This philosophy profoundly influenced this strategy's design, embodied in its rigorous five-condition entry screening mechanism.

---

## Chapter 2: Strategy Parameter Configuration Details

### 2.1 Timeframe Settings

The strategy selects **1 hour (1h)** as the primary timeframe. This choice is deliberate: the 1-hour timeframe captures sufficient price movement for substantial profits while avoiding excessive trading signals that would increase transaction costs and slippage losses. In cryptocurrency markets, the 1-hour timeframe is a classic choice for trend-following strategies, maintaining sufficient trading opportunities while filtering out most short-term noise.

The strategy sets `startup_candle_count = 120`, meaning the strategy requires at least 120 candles of historical data before generating valid trading signals. This setting ensures the Ichimoku indicator calculations have an adequate data foundation, particularly for the cryptocurrency-optimized parameter configuration where larger period parameters require more historical data to generate stable cloud and line formations.

### 2.2 Ichimoku Cryptocurrency-Optimized Parameters

The strategy's core innovation lies in its Ichimoku parameter configuration optimized for cryptocurrency markets:

```
displacement = 30
conversion_line_period = 20  (Conversion line period: standard is 9)
base_line_periods = 60       (Base line period: standard is 26)
lagging_span = 120           (Lagging span period: standard is 52)
```

The logic behind this parameter adjustment: cryptocurrency market trends are often more persistent and pronounced than traditional markets, so using larger period parameters better captures the essential characteristics of trends, avoiding misleading short-term fluctuations.

**Conversion Line Period 20**: Compared to the standard 9-period, the 20-period better reflects short-term trend changes in cryptocurrency markets, reducing the frequency of false signals.

**Base Line Period 60**: Increasing the base line period from 26 to 60 makes it a more robust medium-term trend indicator, providing more reliable support/resistance references in highly volatile cryptocurrency markets.

**Lagging Span Period 120**: The significantly increased lagging span period (from 52 to 120) ensures the cloud's lower boundary has stronger support significance, while also meaning formed trend signals are more reliable.

**Displacement 30**: The increased displacement value (from 26 to 30) makes the cloud more "forward-looking," giving traders more warning time to prepare for potential entry opportunities.

### 2.3 ROI and Stop-Loss Configuration

The strategy employs a progressive ROI (Return on Investment) setting:

```
minimal_roi = {
    "0": 0.10,    # Immediate: 10%
    "30": 0.05,   # After 30 minutes: 5%
    "60": 0.02,   # After 60 minutes: 2%
}
```

This declining ROI design reflects an important trading principle: **the longer a profitable position is held, the lower the profit requirement should be**. When a trade immediately enters profit, the strategy gives price more room to rise (10%); while if a position has been held for 30 minutes or longer, the strategy lowers the profit target to avoid profit erosion.

**Stop-Loss Setting**: The strategy uses a fixed stop-loss of `-0.015` (i.e., -1.5%). This is a relatively tight stop-loss setting, reflecting the strategy's philosophy of pursuing high win rates and quick exits. When price moves against the position by more than 1.5%, the strategy exits decisively to avoid larger losses.

---

## Chapter 3: Indicator Calculation Logic

### 3.1 Ichimoku Cloud Calculation

The strategy calculates the complete Ichimoku indicator system through the `technical.indicators.ftt.ichimoku()` function. The calculation follows standard Ichimoku formulas:

**Tenkan-sen (Conversion Line)**:
```
Tenkan = (Highest High + Lowest Low) / 2  (20 periods)
```

**Kijun-sen (Base Line)**:
```
Kijun = (Highest High + Lowest Low) / 2  (60 periods)
```

**Senkou Span A (Leading Span A)**:
```
Senkou A = (Tenkan + Kijun) / 2  (Displaced 30 periods forward)
```

**Senkou Span B (Leading Span B)**:
```
Senkou B = (Highest High + Lowest Low) / 2  (120 periods, displaced 30 periods forward)
```

**Cloud Color Determination**: When Senkou A > Senkou B, the cloud is green (bullish); when Senkou A < Senkou B, the cloud is red (bearish).

### 3.2 Leading Cloud and Lagging Span Processing

A key "danger zone" processing logic exists in the strategy, related to the Ichimoku indicator's time displacement characteristics:

**Leading Cloud**: Since the cloud itself is displayed displaced forward, the `leading_senkou_span_a` and `leading_senkou_span_b` accessed directly in the strategy actually represent the "future" cloud state. The strategy determines the future cloud color by comparing these two values:

```python
dataframe['future_green'] = (dataframe['leading_senkou_span_a'] > dataframe['leading_senkou_span_b']).astype('int') * 2
```

This mechanism enables the strategy to proactively judge whether future market conditions favor holding positions.

**Lagging Span**: The lagging span is the result of the current closing price displaced backward, so at the current moment, we cannot see the current period's lagging span value. The strategy restores the lagging span to its normal chart position by displacing it forward by `displacement` periods:

```python
dataframe['chikou_high'] = (
    (dataframe['chikou_span'] > dataframe['senkou_a']) &
    (dataframe['chikou_span'] > dataframe['senkou_b'])
).shift(displacement).fillna(0).astype('int')
```

This processing ensures the strategy uses "known" historical data for judgment, not "future" data, guaranteeing backtest reliability.

---

## Chapter 4: Entry Condition In-Depth Analysis

### 4.1 Multiple Confirmation Mechanism

The strategy's entry signal consists of five independent conditions, embodying the principle of rigorous multiple confirmation:

```python
dataframe['go_long'] = (
    (dataframe['tenkan_sen'] > dataframe['kijun_sen']) &      # Condition 1
    (dataframe['close'] > dataframe['senkou_a']) &             # Condition 2
    (dataframe['close'] > dataframe['senkou_b']) &             # Condition 3
    (dataframe['future_green'] > 0) &                           # Condition 4
    (dataframe['chikou_high'] > 0)                              # Condition 5
).astype('int') * 3
```

### 4.2 Condition 1: Tenkan-sen Above Kijun-sen

**Condition Content**: `tenkan_sen > kijun_sen`

This is the classic Ichimoku entry signal. When the short-term momentum line (Tenkan-sen) crosses above the medium-term trend line (Kijun-sen), it indicates market short-term momentum has shifted to the bullish direction. With cryptocurrency-optimized parameters, this signal reflects that price's average position over the past 20 periods is higher than over the past 60 periods, meaning short-term buying power has exceeded the medium-term equilibrium level.

Note that this condition detects a state rather than the crossover event itself. The strategy uses the subsequent `crossed_above` function to identify the actual entry timing.

### 4.3 Conditions 2 & 3: Price Above the Cloud

**Condition Content**: `close > senkou_a` AND `close > senkou_b`

These two conditions jointly ensure price is above the current cloud. The cloud represents the market's equilibrium zone; price breaking above the cloud's upper boundary is a strong bullish signal. By requiring price to be above both the cloud's upper boundary (senkou_a, typically the cloud's upper edge) and lower boundary (senkou_b), the strategy ensures signal validity, avoiding situations where price just enters the cloud zone.

When price is above the cloud, it means current price has exceeded the equilibrium range formed over approximately the past 30 periods (displacement value), and the market is in a clear uptrend.

### 4.4 Condition 4: Future Cloud is Green

**Condition Content**: `future_green > 0`

This is a forward-looking condition checking the future cloud state. When `leading_senkou_span_a > leading_senkou_span_b`, it means within the next 30 periods, the cloud will present a green (bullish) state.

The significance of this condition: it ensures that when trading occurs, the market environment remains bullish for some time in the future. This avoids the risk of entering when a trend is about to reverse, because if the future cloud has already turned red, it indicates market momentum has weakened, making it unsuitable to establish new long positions.

### 4.5 Condition 5: Lagging Span Above the Cloud

**Condition Content**: `chikou_high > 0`

The lagging span is a unique "confirmation" indicator in the Ichimoku system. When the lagging span (actually historical price) is above the cloud, it confirms that past price movement aligns with the current trend direction. This condition's core idea: if past closing prices are above the cloud, then the current trend is reliable.

After displacement processing, the strategy uses actual known historical data for judgment, avoiding "peeking at the future."

### 4.6 Entry Trigger Mechanism

When all five conditions are met, the strategy generates a `go_long` signal (value 3). The actual entry occurs at the moment the signal transitions from absent to present:

```python
dataframe.loc[
    qtpylib.crossed_above(dataframe['go_long'], 0),
'buy'] = 1
```

The `crossed_above` function detects the moment when `go_long` changes from 0 to positive, precisely when all conditions are first satisfied. This design ensures the strategy captures the exact moment when the trend is established.

---

## Chapter 5: Exit Condition Analysis

### 5.1 Trend Reversal Signal

The strategy uses Ichimoku-based trend reversal signals as the primary exit basis:

```python
dataframe.loc[
    qtpylib.crossed_below(dataframe['tenkan_sen'], dataframe['kijun_sen']) 
    | 
    qtpylib.crossed_below(dataframe['close'], dataframe['kijun_sen']),
'sell'] = 1
```

The exit condition consists of two independent triggers:

**Trigger 1: Tenkan-sen Crosses Below Kijun-sen**

When the Tenkan-sen crosses from above to below the Kijun-sen (death cross), this is the most classic trend reversal signal in the Ichimoku system. It indicates short-term market momentum has shifted to the bearish direction, with buying power insufficient to maintain the previous upward momentum.

**Trigger 2: Close Price Falls Below Kijun-sen**

The Kijun-sen is an important support/resistance reference line in the Ichimoku system. When price falls below the Kijun-sen, it means price has retreated below the medium-term average price, and the market may enter a correction or reversal phase.

### 5.2 Stop-Loss Mechanism

Besides technical signal-based exits, the strategy is configured with a hard stop-loss of `-0.015` (1.5%). This is a relatively tight stop-loss setting, with its design philosophy being:

1. **Quick Stop-Loss**: When a trade is wrong, exit immediately to avoid larger losses
2. **Capital Protection**: Strict stop-loss ensures maximum loss per trade is controlled
3. **Improved Win Rate**: Tight stop-loss combined with multi-condition entry screening, although potentially increasing "shaken out" probability, overall improves the win rate of surviving trades

From backtest data, stop-loss triggered 145 trades (69.7% of total trades), but average loss was only -1.54%, while the 63 trades exited via technical signals had an average profit of 14.01%, giving a risk-reward ratio of approximately 9:1.

### 5.3 ROI Exit Mechanism

The progressive ROI setting provides another layer of exit protection. When position holding time extends but price hasn't reached higher profit targets, the strategy gradually lowers profit expectations, automatically exiting when lower targets are reached. This mechanism prevents profitable trades from turning into losses while ensuring effective capital turnover.

---

## Chapter 6: Risk Management System

### 6.1 Multi-Layer Protection Mechanism

Obelisk_TradePro_Ichi_v1_1 strategy constructs multiple risk management protections:

**Layer 1: Entry Screening** — Five independent conditions jointly screen, significantly reducing false signal entry rates. Entry signals only trigger when the market is in a clear uptrend, price is above the cloud, future cloud is bullish, and historical prices confirm trend consistency.

**Layer 2: Dynamic Stop-Loss** — Although the 1.5% fixed stop-loss is simple, it provides clear exit discipline in highly volatile cryptocurrency markets.

**Layer 3: Trend Reversal Exit** — When technical indicators clearly show trend reversal, the strategy proactively exits, avoiding passive holding of losing positions.

**Layer 4: Time Decay Exit** — ROI mechanism ensures the longer the position is held, the lower the exit threshold, preventing profit erosion.

### 6.2 Position Management and Maximum Positions

From backtest settings, the strategy is configured for a maximum of 5 concurrent positions. This setting balances risk diversification with concentrated firepower. A moderate number of positions both diversifies single-asset risk and doesn't over-diversify attention leading to management difficulties.

### 6.3 Backtest Performance Analysis

According to provided backtest data (February 1 to March 24, 2021, approximately 52 days):

**Overall Performance**:
- Total trades: 208
- Total profit: 131.9% (approximately 52 days)
- Win rate: 50 wins / 158 losses (approximately 24% win rate)
- Maximum drawdown: 39.83%

**Profit/Loss Analysis**:
- Stop-loss exits: 145 trades, average loss -1.54%
- Signal exits: 63 trades, average profit +14.01%
- Risk-reward ratio: approximately 9:1

**Key Insights**:
1. Low win rate (24%), but very high risk-reward ratio (approximately 9:1), typical of trend-following strategies
2. Maximum drawdown near 40%, indicating the strategy may suffer significant losses during ranging markets or false breakouts
3. Best performing pairs showed excellent results (BTMX/USD +459.2%), demonstrating the strategy's ability to capture major trends

---

## Chapter 7: Strategy Advantages and Characteristics

### 7.1 Multi-Dimensional Trend Confirmation

The strategy's greatest advantage is its multi-dimensional trend confirmation mechanism. By simultaneously examining:
- Short-term momentum (Tenkan-sen vs Kijun-sen)
- Price position (price vs cloud)
- Future trend (leading cloud color)
- Historical confirmation (lagging span position)

The strategy effectively filters most false breakout signals, only entering in high-probability trend environments.

### 7.2 Cryptocurrency-Optimized Parameters

The parameter optimization for cryptocurrency market characteristics is the strategy's core innovation. Larger period parameters (20-60-120-30) compared to traditional parameters (9-26-52-26) can:
- Better capture cryptocurrency market medium-to-long-term trends
- Reduce interference from short-term noise signals
- Provide more reliable support/resistance references
- Lower trading frequency, improve individual trade quality

### 7.3 Clear Entry and Exit Logic

The strategy's entry and exit conditions are clear and unambiguous, without subjective judgment factors. All signals can be calculated programmatically, avoiding human emotional interference, suitable for automated trading execution.

### 7.4 Strict Discipline

Tight stop-loss (1.5%) combined with progressive ROI exit mechanism ensures trading discipline. Regardless of market volatility, the strategy strictly executes preset exit rules, not deviating from the plan due to greed or fear.

---

## Chapter 8: Strategy Limitations and Risks

### 8.1 Insufficient Adaptability to Ranging Markets

As a typical trend-following strategy, Obelisk_TradePro_Ichi_v1_1 performs poorly in ranging or consolidation markets. From backtest data, approximately 76% of trades ended in losses, mainly occurring during periods lacking clear trends. In such market environments, tight stop-loss leads to frequent "shake-outs," accumulating small losses.

### 8.2 High Maximum Drawdown

The near 40% maximum drawdown indicates the strategy may suffer significant losses during certain market phases. For traders with lower risk tolerance, this drawdown level may be unacceptable. This risk needs to be managed through position control, scaled entry, and other methods.

### 8.3 Parameter Overfitting Risk

The cryptocurrency-optimized parameters used by the strategy, while performing well during the backtest period, may carry the risk of overfitting to historical data. These parameters were optimized for specific market conditions and may perform differently in different market phases.

### 8.4 Stop-Loss May Be Too Tight

A 1.5% stop-loss may be too tight in highly volatile cryptocurrency markets, causing normal price pullbacks to trigger stop-loss exits, followed by price continuing in the expected direction, resulting in "stop-loss being swept" regret.

---

## Chapter 9: Strategy Improvement Suggestions

### 9.1 Dynamic Stop-Loss Optimization

Consider introducing an ATR (Average True Range)-based dynamic stop-loss mechanism, allowing stop-loss distance to automatically adjust based on market volatility. Widen stop-loss during high volatility periods, tighten during low volatility periods, improving stop-loss effectiveness.

### 9.2 Market Environment Filtering

Add market environment recognition mechanism to reduce or pause trading during clear ranging markets or low volatility periods. ADX (Average Directional Index) or volatility indicators can be introduced as auxiliary judgment.

### 9.3 Scaled Position Management

Consider making the stop-loss for a single position a certain proportion of total capital, rather than a fixed percentage of a single asset. Control each trade's risk exposure through position size adjustment.

### 9.4 Trend Strength Weighting

When entry signal strength varies, use different position sizes. When all Ichimoku conditions are perfectly met, positions can be increased; when conditions are barely met, positions can be reduced.

---

## Chapter 10: Practical Application Guide

### 10.1 Applicable Markets and Coins

The strategy is most suitable for the following market environments:
- Clear single-direction trend markets
- Coins with moderate-to-high volatility
- Liquid mainstream coins

From backtest data, the strategy performed excellently on certain coins (e.g., BTMX/USD, LINA/USD) while performing poorly on others (e.g., SRM/USD, ADABULL/USD). This suggests traders should conduct independent testing and screening for different coins when applying the strategy.

### 10.2 Timeframe Selection

The strategy defaults to a 1-hour timeframe. Traders can adjust based on their trading style:
- Short-term traders: Can try 15-minute or 30-minute timeframes
- Swing traders: Can try 4-hour or daily timeframes

Note that when adjusting timeframes, Ichimoku parameters should also be adjusted accordingly.

### 10.3 Capital Management Recommendations

Recommended capital management principles:
- Single trade risk not exceeding 1-2% of total capital
- Maximum position count controlled at 5-10
- Reserve sufficient capital to withstand maximum drawdown

### 10.4 Monitoring and Adjustment

During strategy operation, regularly monitor:
- Whether win rate and risk-reward ratio remain in reasonable ranges
- Whether maximum drawdown exceeds preset thresholds
- Performance differences across different coins

Based on monitoring results, timely adjust parameters or pause trading on poorly performing coins.

---

## Chapter 11: Summary and Outlook

### 11.1 Core Value Summary

Obelisk_TradePro_Ichi_v1_1 is a thoughtfully designed Ichimoku trend-following strategy. Its core values include:

1. **Solid Theory**: Based on mature Ichimoku technical analysis system
2. **Parameter Optimization**: Professionally tuned for cryptocurrency market characteristics
3. **Clear Logic**: Entry and exit conditions are clear, easy to understand and execute
4. **Controlled Risk**: Multi-layer risk management mechanism protects capital safety

### 11.2 Suitable Trader Profile

This strategy is suitable for the following types of traders:
- Traders who believe in trend-following philosophy
- Traders who can accept lower win rates in exchange for high risk-reward ratios
- Traders with sufficient capital to withstand certain drawdowns
- Traders with some technical analysis foundation

### 11.3 Future Development Directions

As cryptocurrency markets continue to evolve, the strategy can develop in the following directions:
- Introduce machine learning models to assist trend judgment
- Add multi-timeframe collaborative analysis
- Integrate on-chain data and market sentiment indicators
- Develop adaptive parameter adjustment mechanisms

In summary, Obelisk_TradePro_Ichi_v1_1 provides a solid Ichimoku strategy framework for cryptocurrency quantitative trading. Traders can make personalized adjustments and optimizations based on understanding its principles, according to their own needs and market changes.

---

## Appendix: Strategy Parameter Quick Reference

| Parameter Category | Parameter Name | Value | Description |
|-------------------|----------------|-------|-------------|
| Timeframe | timeframe | 1h | Primary timeframe |
| Startup Candles | startup_candle_count | 120 | Minimum historical data requirement |
| Ichimoku | conversion_line_period | 20 | Conversion line period |
| Ichimoku | base_line_periods | 60 | Base line period |
| Ichimoku | lagging_span | 120 | Lagging span period |
| Ichimoku | displacement | 30 | Displacement value |
| ROI | immediate | 10% | Immediate profit target |
| ROI | 30min | 5% | 30-minute profit target |
| ROI | 60min | 2% | 60-minute profit target |
| Stop-Loss | stoploss | -1.5% | Fixed stop-loss percentage |

---

*Document Version: v1.0*
*Generated Date: March 27, 2026*