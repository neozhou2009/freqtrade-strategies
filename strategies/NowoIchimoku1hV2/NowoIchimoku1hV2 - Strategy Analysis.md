# NowoIchimoku1hV2 Strategy Analysis

## Table of Contents

1. [Strategy Overview and Technical Background](#1-strategy-overview-and-technical-background)
2. [Core Technical Indicators](#2-core-technical-indicators)
3. [Entry Signal System Construction](#3-entry-signal-system-construction)
4. [Stop-Loss System Deep Dive](#4-stop-loss-system-deep-dive)
5. [Risk Management Framework](#5-risk-management-framework)
6. [Parameter System and Hyperparameter Optimization](#6-parameter-system-and-hyperparameter-optimization)
7. [Strategy Advantages and Innovations](#7-strategy-advantages-and-innovations)
8. [Strategy Limitations and Risk Warnings](#8-strategy-limitations-and-risk-warnings)
9. [Live Trading Application Advice](#9-live-trading-application-advice)
10. [Strategy Extension Directions](#10-strategy-extension-directions)
11. [Summary and Evaluation](#11-summary-and-evaluation)

---

## 1. Strategy Overview and Technical Background

NowoIchimoku1hV2 is a quantitative trading strategy based on the Ichimoku Kinko Hyo and Bollinger Bands, specifically designed for the 1-hour time cycle. This strategy integrates the essence of Eastern traditional technical analysis with modern statistical volatility theory, capturing medium-to-long-term trend opportunities in high-volatility cryptocurrency markets through multi-layered trend confirmation mechanisms and dynamic risk management systems.

The "Nowo" in the strategy name implies innovative improvement, "Ichimoku" explicitly points to the core technical system, "1h" indicates the applicable timeframe, and "V2" identifies this as the second version iteration. This naming convention reflects the strategy developer's professional attitude toward version management and strategy classification.

From a technical philosophy perspective, the strategy embodies the dual philosophy of "following the trend" and "risk control first." The Ichimoku Cloud, as the core analytical framework, provides a panoramic view of market trends, momentum, and support/resistance levels. Bollinger Bands serve as auxiliary indicators, offering dynamic assessment of price volatility. Their organic combination enables the strategy to grasp major-level trends while performing refined risk management at key levels.

---

## 2. Core Technical Indicators

### 2.1 Hull Moving Average Bollinger Bands

The strategy employs an innovative Bollinger Bands construction method. Unlike traditional Bollinger Bands using SMA, this strategy uses the Hull Moving Average (HMA) as the middle band basis. HMA was developed by Alan Hull in 2005, with its core advantage being effective reduction of lag in traditional MAs while maintaining good smoothness.

Bollinger Bands parameters: length 20 periods, standard deviation multiplier 2.5. This 2.5× setting is more relaxed than the traditional 2.0×, meaning the strategy tolerates higher price volatility and better adapts to cryptocurrency market characteristics. The upper band formula:

```
Upper Band = HMA(close, 20) + 2.5 × STDDEV(close, 20)
```

The strategy only uses the Bollinger Bands upper band; the lower band is intentionally ignored, clearly indicating the strategy is positioned as long-only, focused on capturing upside opportunities in uptrends. The upper band plays an important role in stop-loss logic — when price breaks above the upper band and then pulls back, the strategy promptly locks in profits.

### 2.2 Ichimoku Cloud System

The Ichimoku Cloud is the strategy's core technical framework, invented by Japanese analyst Goshu Hosoda in the 1960s. It is a comprehensive technical analysis tool integrating trend identification, momentum analysis, and support/resistance judgment. The strategy fully implements the five standard Ichimoku components:

**Conversion Line (Tenkan-sen)**: Period parameter uses standard setting 9, calculated as the average of the highest and lowest prices over 9 periods. Represents short-term market sentiment and price momentum, an important reference for short-term trend direction.

**Base Line (Kijun-sen)**: Period parameter uses standard setting 26, calculated as the average of the highest and lowest prices over 26 periods. Represents medium-term market trends and is often used as a reference for moving stop-losses.

**Leading Span A**: The average of Conversion Line and Base Line, shifted forward 26 periods. Reflects the combined strength of short and medium-term trends, forming a key component of the cloud.

**Leading Span B**: The average of the highest and lowest prices over 52 periods, shifted forward 26 periods. Represents longer-term market trends, and together with Leading Span A forms the cloud's two boundaries.

**Cloud (Kumo)**: The area between Leading Span A and Leading Span B is the core visual element distinguishing bull/bear markets. When Leading Span A is above Leading Span B, the cloud is green (bullish); otherwise it is red (bearish). Cloud thickness reflects market volatility — thick clouds mean strong trends and distant support/resistance, thin clouds suggest consolidation or trend reversal.

### 2.3 Stochastic RSI

The strategy introduces Stochastic RSI as an auxiliary indicator to identify market overbought/oversold states. Stochastic RSI applies the stochastic formula to RSI values, offering higher sensitivity to extreme values than plain RSI.

Parameters: RSI period 14, stochastic period 14, K-line smoothing 3, D-line smoothing 3. The final `srsi_k` value oscillates between 0 and 100. The strategy sets 80 as the overbought threshold — when `srsi_k` exceeds 80 and current profit exceeds the preset minimum, the stop-loss logic is triggered.

This design reflects the strategy's alertness to market overheating — when rapid price increases cause short-term overbought conditions, the strategy proactively reduces stop-loss tolerance to ensure already-gained profits aren't swallowed by potential pullbacks.

---

## 3. Entry Signal System Construction

### 3.1 Multi-Dimensional Trend Confirmation Mechanism

The strategy's entry logic adopts a strict "one-vote veto" system — all conditions must be simultaneously satisfied to trigger a buy signal. While this strict design may miss some trading opportunities, it significantly improves signal quality and reduces losses from false breakouts.

The core buy condition set is named "should_buy," consisting of seven conditions:

**Condition 1: Bullish Candle Confirmation**
```python
close > open
```
Current candle must be bullish — closing price above opening price, showing buyers had the upper hand in the current period. Alone this seems simple, but combined with other conditions it becomes an effective false breakout filter.

**Condition 2: Closing Price Exceeds Cloud Upper Boundary**
```python
close > shifted_upper_cloud × close_above_shifted_upper_cloud
```
Requires closing price to exceed the 25-period-displaced cloud upper boundary by a factor (default 0.603). `shifted_upper_cloud` is the cloud upper boundary shifted forward 25 periods (because the standard Ichimoku Cloud shifts forward 26 periods, it must be "pulled back" to align with current prices).

The deeper meaning: price must significantly break away from the cloud area, entering clearer upside space. Adjusting this parameter controls entry threshold — higher values mean stricter requirements, fewer signals but potentially higher quality.

**Condition 3: Closing Price Exceeds Cloud Lower Boundary**
```python
close > shifted_lower_cloud
```
Ensures price is above the cloud's lower support boundary. The cloud lower acts as dynamic support in uptrends — price consistently above it means the bull pattern is solid.

**Condition 4: Green Cloud Confirmation**
```python
lead_1 > lead_2 (is_cloud_green = True)
```
Requires the current cloud to show a bullish form (Leading Span A above Leading Span B). Cloud color is a key indicator of overall market trend status, providing macro background support. Note the cloud color uses the original un-displaced values, as the cloud is inherently designed for the future — its current color directly reflects the trend expectation for the next 26 periods.

**Condition 5: Conversion Line Above Base Line**
```python
conversion_line > base_line
```
Short-term momentum line above medium-term trend line — a classic long signal. When the Conversion Line crosses above the Base Line, short-term momentum is strengthening, usually signaling a trend acceleration. This ensures the strategy doesn't enter when momentum is weakening.

**Condition 6: Closing Price Exceeds Displaced Conversion Line**
```python
close > shifted_conversion_line
```
The 25-period-displaced value of the Conversion Line. This requires price to be above not only the current Conversion Line but also above the historical Conversion Line position, further confirming trend persistence. This "double confirmation" design philosophy runs throughout the strategy.

**Condition 7: Closing Price Exceeds Double-Displaced Cloud Upper**
```python
close > double_shifted_upper_cloud
```
`double_shifted_upper_cloud` is the cloud upper boundary shifted forward 50 periods (25 × 2). This condition requires price to break not only recent resistance but also longer-term resistance. This is a deep inspection of trend strength.

### 3.2 Intelligent Entry Control Mechanism

The strategy designs a unique "buy_allowed" mechanism controlling entry timing and frequency — an important innovation distinguishing it from ordinary trend strategies.

**Core Logic**:
1. Initial state allows buying (`buy_allowed = True`)
2. Once a buy is executed, immediately prohibit subsequent buys (`buy_allowed = False`)
3. When the cloud turns red (bearish), re-allow buying (`buy_allowed = True`)

The profound meaning: after each successful entry, the strategy enters a "cooldown period," not reopening the entry channel until the market environment changes (cloud turns red then green). This effectively prevents position over-concentration risk from repeated entries in a single trend and gives the strategy sufficient time to observe existing positions.

---

## 4. Stop-Loss System Deep Dive

### 4.1 Custom Stop-Loss Architecture

The strategy employs a fully custom stop-loss system (`use_custom_stoploss = True`), closing the traditional trailing stop function (`trailing_stop = True` but overridden by custom logic), meaning stop-loss behavior is entirely controlled by code logic, providing great flexibility.

The `custom_stoploss` function is called on each tick, dynamically calculating the stop-loss price based on current market state. Return value represents the percentage of the stop-loss trigger price: e.g., -0.05 means stop triggers when current price drops 5%, -0.0001 means nearly immediate stop (used for profit locking), -0.99 means nearly no stop (floor protection).

### 4.2 Four-Tier Stop-Loss Trigger Conditions

**Trigger 1: Stochastic RSI Overbought Profit-Taking**
```python
if (last_candle['srsi_k'] > 80) & (current_profit > srsi_k_min_profit):
    return -0.0001
```
When the latest candle's Stochastic RSI K exceeds 80 (overbought threshold) AND current profit exceeds `srsi_k_min_profit` (default 3.6%), profit-taking triggers. The core concept: when the market shows clear overheating signals, rather than waiting for a pullback, proactively lock in profits. The -0.0001 return means any price drop (even 0.01%) triggers a sell.

**Trigger 2: Bollinger Upper Band Break Profit-Taking**
```python
if (previous_candle['close'] < previous_candle['upper']) & \
   (current_rate > last_candle['upper']) & \
   (current_profit > above_upper_min_profit):
    return -0.0001
```
When the previous candle's close is below the Bollinger upper band, current price breaks above the Bollinger upper band, AND current profit exceeds `above_upper_min_profit` (default 1.1%), profit-taking triggers. This captures the classic "breakout then pullback" trading pattern — price often retraces after breaking the Bollinger upper band; the strategy chooses to lock in profits at the breakout moment.

**Trigger 3: Dynamic Target Profit-Taking**
```python
limit = trade.open_rate + ((trade.open_rate - trade_candle['shifted_lower_cloud']) * limit_factor)
if current_rate > limit:
    return -0.0001
```
A dynamic profit target based on entry price. First calculates the distance between entry price and the displaced cloud lower at entry, multiplies by `limit_factor` (default 1.918×) as the profit target, then adds to entry price.

The calculation's brilliance: the profit target is directly tied to the market structure (cloud lower) at entry, not a fixed percentage. In high-volatility markets, the cloud lower distance from entry price is larger, so profit targets are correspondingly higher; in low-volatility environments, targets are lower — more flexibly adapting to the market.

**Trigger 4: Cloud Lower Stop-Loss**
```python
if current_rate < (trade_candle['shifted_lower_cloud'] * lower_cloud_factor):
    return -0.0001
```
When price falls below the entry's displaced cloud lower (multiplied by `lower_cloud_factor`, default 0.971), stop-loss triggers. This is a typical structural support stop — the cloud lower is viewed as a key support level in the strategy framework, and a break below it suggests possible trend reversal.

`lower_cloud_factor` of 0.971 means the stop is actually set at 97.1% of the cloud lower, providing some error tolerance and avoiding premature stops from minor touches.

### 4.3 Default Stop-Loss Protection

If none of the above four conditions trigger, the function returns -0.99 — essentially "infinitely tolerant," with the real protection coming from the `stoploss = -0.345` (34.5% fixed stop-loss) and `minimal_roi` time decay mechanism set at startup.

---

## 5. Risk Management Framework

### 5.1 Fixed Stop-Loss

The strategy sets `stoploss = -0.345`, meaning any trade's maximum loss is capped at 34.5%. This is a medium-to-relaxed stop in cryptocurrency markets, reflecting the strategy's tolerance for price volatility.

Notably, this fixed stop-loss is the strategy's last line of defense — in actual operation, most cases are triggered earlier by custom stop-loss logic, so its practical role is more about preventing catastrophic losses from extreme black swan events.

### 5.2 Minimal ROI (Time-Decaying)

The strategy configures a layered, declining minimum return target system:
```
"0": 0.427 (42.7%)
"448": 0.202 (20.2%)
"1123": 0.089 (8.9%)
"2355": 0 (0%)
```

This configuration means:
- Immediately at position open, initial target is 42.7% profit
- After 448 hours of holding, minimum target drops to 20.2%
- After 1,123 hours of holding, minimum target drops to 8.9%
- After 2,355 hours of holding, any profit is acceptable to exit

This time-decaying ROI design reflects the strategy's consideration for holding time — if reasonable profits aren't achieved in the short term, the strategy gradually reduces expectations and "takes the money and runs" within a reasonable time window. The parameters indicate the strategy expects a complete trading cycle of approximately 98 days (2,355 hours), further confirming its medium-to-long-term positioning.

### 5.3 Trailing Stop Configuration

While the strategy enables `trailing_stop = True`, due to the custom stop-loss function's existence, trailing stop's actual behavior is entirely overwritten by custom logic. This configuration is more of a backup protection, ensuring the system can still provide basic trailing stop functionality if custom logic fails.

---

## 6. Parameter System and Hyperparameter Optimization

### 6.1 Optimizable Parameters Overview

The strategy defines five optimizable parameters using `DecimalParameter` decorators, tunable through Freqtrade's hyperparameter optimization framework:

| Parameter | Space | Default | Range | Description |
|-----------|-------|---------|-------|-------------|
| srsi_k_min_profit | sell | 0.036 | 0.01-0.99 | Stochastic RSI overbought profit-taking minimum profit threshold |
| above_upper_min_profit | sell | 0.011 | 0.001-0.5 | Bollinger upper band break profit-taking minimum profit threshold |
| limit_factor | sell | 1.918 | 0.5-5.0 | Dynamic target profit-taking multiplier |
| lower_cloud_factor | sell | 0.971 | 0.5-1.5 | Cloud lower stop-loss discount factor |
| close_above_shifted_upper_cloud | buy | 0.603 | 0.5-2.0 | Entry price minimum requirement relative to cloud upper |

### 6.2 Parameter Sensitivity Analysis

**srsi_k_min_profit**: Controls the overbought profit-taking threshold. Default 3.6% means even with an overbought signal, the strategy only considers profit-taking if profit exceeds 3.6%. Raising this increases holding time, potentially capturing more gains but facing more pullback risk; lowering it is more conservative, suitable for highly volatile markets.

**limit_factor**: The strategy's most creative parameter, directly determining profit target distance. Default 1.918× means the strategy expects to capture nearly twice the distance from entry price to cloud lower as profit. In strong trending markets, raising this may yield higher returns; in ranging markets, lowering it helps more frequently lock in profits.

**close_above_shifted_upper_cloud**: The only parameter in the buy space, directly affecting the number and quality of entry signals. Default 0.603 means price only needs to reach 60.3% of the cloud upper to meet the condition — relatively relaxed. If seeking fewer but higher-quality signals, raise this value.

---

## 7. Strategy Advantages and Innovations

### 7.1 Multi-Layered Trend Confirmation

The strategy's biggest highlight is its multi-layered entry confirmation mechanism. Through strict screening of seven conditions, it effectively filters most false breakouts and weak signals. Each condition verifies trend validity from a different dimension: candle pattern (bullish), price position (relative to cloud), trend state (cloud color), momentum strength (Conversion Line vs Base Line), and historical resistance (double displacement). This "full checkup" style entry logic ensures every trade has solid technical foundations.

### 7.2 Adaptive Risk Management

The strategy's risk management system shows high adaptability. First, stop-loss and profit targets aren't fixed values but dynamically tied to market structure (cloud lower) at entry. Second, multi-tiered profit-taking triggers cover various market scenarios — overbought, breakout, target, support break — providing corresponding responses regardless of how the market moves.

### 7.3 Intelligent Cooldown Mechanism

The buy_allowed mechanism's design is another major innovation. Through "one buy, one stop, red-green restart" logic, the strategy effectively prevents over-positioning in a single trend, while providing a built-in mechanism for identifying trend transitions. This reflects deep understanding of market rhythm — trends don't move in a straight line; the strategy gives existing positions sufficient room to develop.

### 7.4 Time-Decaying Profit Targets

The minimal_roi time decay design reflects the strategy's consideration for "time value." The longer the holding period without achieving expected returns, the lower the strategy's profit expectation, aligning with the market's "mean reversion" pattern. Long holdings without expected returns often signal weakening trend momentum — exiting promptly is wiser than continuing to wait.

---

## 8. Strategy Limitations and Risk Warnings

### 8.1 One-Sided Long-Only Limitation

The strategy uses only the upper Bollinger Band, clearly indicating a pure long-only strategy. In bear or ranging markets, the strategy may find few suitable entry opportunities for extended periods, causing capital idleness. For investors wishing to trade around the clock, consider pairing with other short strategies or asset allocation.

### 8.2 High-Volatility Market Adaptability

The strategy may face challenges in extreme volatility environments. Although the 34.5% fixed stop-loss provides protection, in black swan events, prices may break through stop-loss levels in extremely short timeframes, causing actual losses to exceed expectations. Additionally, stop-loss logic relies on technical indicator calculations, which may not execute as expected during price gaps.

### 8.3 Parameter Over-Fitting Risk

Five optimizable parameters, while providing tuning space, also increase the risk of over-fitting historical data. Parameter combinations performing extremely well in backtesting may not replicate the same performance in future markets. It is recommended to conduct sufficient forward testing and cross-market validation before actual use.

### 8.4 Ichimoku Cloud's Inherent Lag

Despite using HMA to reduce lag, the Ichimoku Cloud's calculation method inherently causes some response delay to price changes. In fast reversal markets, the strategy may miss optimal entry or exit timing. The 26-period Base Line and 52-period Leading Span B represent 26 and 52 hours respectively on an hourly chart — this time span may be too long for some traders.

### 8.5 Liquidity Dependence

The strategy's stop-loss logic relies on executing orders at specific prices; in insufficient-liquidity markets, it may face excessive slippage or inability to fill. This requires particular attention for lower-liquidity trading pairs.

---

## 9. Live Trading Application Advice

### 9.1 Market Selection

The strategy is best suited for markets with clear trends, such as mainstream cryptocurrencies (BTC, ETH) during bull or recovery phases. For ranging or trend-ambiguous periods, it is recommended to temporarily disable or pair with other ranging strategies.

### 9.2 Parameter Tuning Strategy

**Walk-Forward Analysis**: Divide historical data into multiple training/testing windows, ensuring parameters perform well across different time periods.

**Cross-Market Validation**: Test the same parameters across multiple trading pairs, verifying their universality.

**Stress Testing**: Test strategy performance under extreme conditions (post-crash rebounds, post-surge pullbacks), assessing anti-risk capability.

**Step-by-Step Tuning**: Prioritize optimizing the parameter with the greatest strategy impact (e.g., limit_factor), then gradually refine other parameters.

### 9.3 Supplementary Risk Control

**Position Sizing**: Single trade risk should not exceed 2-5% of total capital; total exposure should be controlled within 20%.

**Diversified Investment**: Run the strategy across multiple less-correlated trading pairs, reducing single-market risk.

**Human Intervention Mechanism**: Set up major news alerts, evaluating whether to pause strategy operation at critical moments.

**Regular Review**: Analyze strategy performance weekly/monthly, identifying issues and adjusting parameters promptly.

### 9.4 Execution Environment Requirements

`startup_candle_count` is set to 100, requiring at least 100 historical candles to properly calculate indicators. Ensure the exchange can provide sufficient historical data before live operation.

The strategy closes `use_sell_signal`, relying on stop-loss and ROI mechanisms for exits, requiring high order execution reliability from the exchange. It is recommended to select mainstream exchanges with good liquidity and stable APIs.

---

## 10. Strategy Extension Directions

### 10.1 Short-Selling Extension

Consider adding symmetric short logic, using Bollinger lower band and red cloud signals to capture downtrend opportunities. This would enable the strategy to profit bidirectionally during bull-bear transitions, improving capital efficiency.

### 10.2 Multi-Timeframe Fusion

Current strategy only uses the 1-hour period; consider introducing higher timeframes (4-hour, daily) for trend confirmation, forming multi-period resonance entry signals to further improve signal quality.

### 10.3 Market State Recognition

Add a market state recognition module to distinguish trending vs. ranging markets. Reduce entry frequency or pause trading in ranging markets, resume normal operations in trending markets. This can be implemented through ADX or cloud thickness.

### 10.4 Dynamic Parameter Adjustment

Dynamically adjust parameters based on market volatility — relax stop distance in high-volatility environments, tighten stop and lower profit targets in low-volatility environments. This would make the strategy more adaptive.

### 10.5 Machine Learning Enhancement

Consider introducing machine learning models to identify optimal entry timing through historical data training, or predict cloud signal success probability, providing probability weighting for strategy decisions.

---

## 11. Summary and Evaluation

NowoIchimoku1hV2 is a meticulously designed trend-following system. Its core advantages:

**Solid Theoretical Foundation**: Based on the Ichimoku Cloud, a time-tested technical analysis system, combined with Bollinger Bands volatility theory, forming a complete analytical framework.

**Rigorous Logic**: Seven-tier entry conditions construct a strict signal filter mechanism, effectively controlling false signals; four-tier stop conditions cover various market scenarios, forming a three-dimensional risk protection network.

**Outstanding Innovation**: The buy_allowed mechanism, dynamic stop-loss targets, and time-decaying ROI reflect the strategy developer's deep insight into market patterns.

**Flexible Parameters**: Five optimizable parameters provide sufficient tuning space, adapting to different market environments and trading styles.

The strategy's main limitations are one-sided long-only operation, adaptability to high-volatility markets, and Ichimoku Cloud's inherent lag. These limitations can be gradually improved through strategy extensions.

Overall, NowoIchimoku1hV2 is a mature strategy suitable for medium-to-long-term traders, particularly those interested in trend following who can withstand some drawdown. Under correct understanding of strategy logic, reasonable parameter settings, and strict risk management execution, this strategy is expected to generate steady returns in trending markets.

---

*This analysis is based on strategy source code for technical analysis only. It serves as a reference and does not constitute investment advice. Quantitative trading involves risk — please use caution after fully understanding strategy logic and risks.*
