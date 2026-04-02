# Obelisk_TradePro_Ichi_v2_1 Strategy In-Depth Analysis

## Table of Contents

1. [Strategy Overview](#1-strategy-overview)
2. [Theoretical Foundation and Design Philosophy](#2-theoretical-foundation-and-design-philosophy)
3. [Ichimoku Cloud System Detailed Explanation](#3-ichimoku-cloud-system-detailed-explanation)
4. [Auxiliary Indicator Analysis](#4-auxiliary-indicator-analysis)
5. [Entry Signal Mechanism](#5-entry-signal-mechanism)
6. [Exit Signal Mechanism](#6-exit-signal-mechanism)
7. [Risk Management System](#7-risk-management-system)
8. [Parameter Configuration Optimization](#8-parameter-configuration-optimization)
9. [Backtesting and Practical Recommendations](#9-backtesting-and-practical-recommendations)
10. [Strategy Advantages and Limitations](#10-strategy-advantages-and-limitations)
11. [Summary and Outlook](#11-summary-and-outlook)

---

## 1. Strategy Overview

### 1.1 Strategy Background

Obelisk_TradePro_Ichi_v2_1 is a quantitative trading strategy based on the Ichimoku Cloud technical analysis system. The strategy was published by developer Obelisk in April 2021, with its core concept originating from the Trade Pro channel's "Crazy Results Best Ichimoku Cloud Trading Strategy," after special optimization for cryptocurrency markets.

The strategy's original inspiration comes from mature Ichimoku analysis methods in traditional financial markets, but the developer fully considered the high volatility characteristics of cryptocurrency markets during implementation, performing cryptocurrency-specific optimization on classic parameters. This parameter adjustment reflects the strategy designer's deep understanding of market fundamentals—different markets have significantly different volatility characteristics, and blindly copying traditional financial market parameters often fails to achieve ideal results.

### 1.2 Core Characteristics

The strategy's core characteristics are manifested across multiple dimensions. First, from a timeframe perspective, the strategy uses a 1-hour cycle as the primary timeframe. This choice balances the relationship between signal quality and trading frequency. Shorter cycles produce excessive noise signals, while longer cycles may miss important entry opportunities. The 1-hour cycle effectively filters intraday noise while maintaining sensitivity to medium-term trends.

Second, the strategy employs a multi-dimensional confirmation mechanism. Entry signals must simultaneously satisfy eight independent conditions. This rigorous filtering mechanism significantly reduces the triggering probability of false signals. In quantitative trading, signal quality is far more important than signal quantity—it's better to miss some opportunities than to ensure success rate for each entry.

Finally, the strategy employs a multi-layer protection system in risk management. Fixed stop-loss as the first line of defense, trailing stop-loss as the second line of defense, and minimum return targets as dynamic adjustment mechanisms—these three work synergistically to build a complete risk control framework.

### 1.3 Applicable Scenarios

The strategy was designed to provide trend-following solutions for cryptocurrency markets. From parameter configuration, the strategy is suitable for trading mainstream cryptocurrencies with good liquidity and moderate volatility. Recommended pair screening conditions in strategy documentation include: trading volume ranked top 50, listed for at least 10 days, price not exceeding $20, spread not exceeding 0.2%, sufficient price fluctuation in the past 3 days. These screening conditions ensure the strategy operates in market environments with strong liquidity and relatively regular price behavior.

---

## 2. Theoretical Foundation and Design Philosophy

### 2.1 Historical Origins of Ichimoku Cloud

The Ichimoku Cloud was invented by Japanese technical analyst Goichi Hosoda in the 1930s. Its Japanese name "Ichimoku Kinko Hyo" literally translates to "one-glance equilibrium chart," embodying the core philosophy of this analysis system—comprehensively grasping market trends, momentum, and support-resistance relationships through a single chart.

Unlike traditional Western technical analysis which treats trend, momentum, and support-resistance separately, Ichimoku organically integrates these elements into a unified framework. The Tenkan-sen and Kijun-sen reflect price momentum, the cloud displays support-resistance zones, and the Chikou Span verifies trend strength. This integration allows traders to quickly identify market overview without switching between multiple indicators.

### 2.2 Adaptive Adjustment of Design Philosophy

The original Ichimoku parameters (Tenkan-sen 9 periods, Kijun-sen 26 periods, lagging line 52 periods) were designed for Japanese stock markets, reflecting typical volatility characteristics of Japanese stocks at that time. However, cryptocurrency markets have completely different market microstructure—24-hour continuous trading, higher volatility, relatively shorter trend duration.

The strategy developer adjusted parameters to Tenkan-sen 20 periods, Kijun-sen 60 periods, lagging line 120 periods, and displacement period from 26 to 30. The intrinsic logic of these adjustments is to adapt to cryptocurrency markets' more dramatic price fluctuations. Longer calculation periods can filter short-term noise, avoiding being triggered by normal volatility. Meanwhile, increased displacement provides the cloud with a farther "forward-looking" distance, helping to earlier identify potential trend changes.

### 2.3 Philosophical Foundation of Multiple Confirmation

The strategy design embodies a conservative trading philosophy of "better to miss than to make mistakes." Eight entry conditions must be simultaneously satisfied. This strict AND logic ensures every entry undergoes multi-dimensional verification. From probability theory perspective, assuming each condition is independent with 70% accuracy, the signal accuracy when eight conditions are simultaneously satisfied will significantly improve.

The cost of this multiple confirmation mechanism is missing some valid trading opportunities. In early trend stages, not all conditions will be immediately satisfied, waiting for all conditions to be complete may mean missing part of profits. But the strategy designer chose quality over quantity, which is statistically sound—one major loss requires multiple profits to recover, so avoiding losses is more important than acquiring profits.

---

## 3. Ichimoku Cloud System Detailed Explanation

### 3.1 Tenkan-sen and Kijun-sen

The Tenkan-sen is the average of the highest high and lowest low over the past 20 periods. This line can be understood as the short-term price axis, reflecting current price position relative to recent price ranges. When price is above Tenkan-sen, it means current price is in the upper half of recent price range, with bullish forces dominant; conversely, bearish forces are dominant.

The Kijun-sen is the average of the highest high and lowest low over the past 60 periods. Compared to Tenkan-sen, Kijun-sen fluctuates more smoothly, representing the medium-term price axis. Kijun-sen plays an important support-resistance role in the strategy—in uptrends, price pulling back to Kijun-sen often finds support; in downtrends, price bouncing to Kijun-sen often encounters resistance.

Tenkan-sen and Kijun-sen crossover is an important trend signal. When Tenkan-sen crosses from below to above Kijun-sen, it's called bullish TK cross, suggesting short-term momentum has turned strong; conversely, it's called bearish TK cross. The entry condition in the strategy requires Tenkan-sen to be above Kijun-sen, i.e., in bullish TK cross state.

### 3.2 Cloud System

The cloud consists of Senkou Span A and Senkou Span B, together forming an area rather than a single line. This regional design embodies Ichimoku's unique understanding of support-resistance—support-resistance is not a precise price point but a price interval.

Senkou Span A calculation is the average of Tenkan-sen and Kijun-sen, then displaced 30 periods forward. This line represents the combined level of short-term and medium-term price axes, reacting faster. Senkou Span B calculation is the average of highest high and lowest low over past 120 periods, also displaced 30 periods forward, reacting slower.

The cloud's direction and thickness both contain important information. When Senkou Span A is higher than Senkou Span B, the cloud is green, representing a bullish market; conversely, the cloud is red, representing a bearish market. Cloud thickness (the gap between Senkou Span A and Senkou Span B) reflects market uncertainty—thicker cloud means stronger support-resistance; thinner cloud means higher possibility of trend conversion.

### 3.3 Chikou Span (Lagging Span)

The Chikou Span is the current closing price displaced 30 periods forward. This design seems counter-intuitive—why use historical data to judge current trend? The answer lies in verification.

The Chikou Span's core function is to verify whether current trend is supported by historical prices. In a healthy bullish trend, Chikou Span should be above the cloud, meaning current price has exceeded price levels from the past 30 periods. If Chikou Span is below the cloud, even if price is currently above the cloud, the trend may not be sufficiently stable.

The `chikou_high` variable in the strategy checks whether Chikou Span is higher than both Senkou Span A and Senkou Span B, which is exactly verification of trend strength. This verification mechanism effectively avoids entering during false breakouts or short-term fluctuations.

### 3.4 Cryptocurrency-Specific Parameter Interpretation

The Ichimoku parameters used in the strategy differ significantly from traditional parameters. Tenkan-sen period increased from 9 to 20, meaning short-term momentum judgment baseline is widened, reducing signal noise from short-term fluctuations. For highly volatile cryptocurrency markets, 9-period short-term moving average produces too many invalid crossovers, 20 periods can better filter this noise.

Kijun-sen period increased from 26 to 60, lagging line period increased from 52 to 120, these adjustments all point to the same goal—adapting to cryptocurrency markets' larger volatility amplitude. In traditional stock markets, 26 days approximately represents one month of trading time, 60 days represents one quarter; but in 24-hour continuous cryptocurrency markets, these timeframes need recalibration.

Displacement period adjusted from 26 to 30 also reflects adaptation to market characteristics. Larger displacement means the cloud extends further into the future, providing longer-term support-resistance expectations. For highly volatile assets like cryptocurrency, farther expectation range can better accommodate price fluctuations.

---

## 4. Auxiliary Indicator Analysis

### 4.1 SSL Channel

The SSL Channel is a relatively new technical indicator, introduced to this strategy from developer community contributions. Its calculation is based on moving average and Average True Range (ATR): upper channel equals the moving average of specified period highest prices plus ATR, lower channel equals the moving average of specified period lowest prices minus ATR.

The SSL Channel's core logic uses ATR to measure market volatility, dynamically adjusting channel width. When market volatility increases, channels automatically widen; when market volatility decreases, channels automatically narrow. This adaptive characteristic makes it more capable of adapting to different market states than fixed-parameter moving averages.

The strategy uses 10-period SSL Channel, a relatively sensitive parameter setting. When closing price is above upper channel, market is considered to be in uptrend; when closing price is below lower channel, market is considered to be in downtrend. The strategy requires ssl_up greater than ssl_down to enter, i.e., price must be in SSL Channel's bullish zone.

The SSL Channel's introduction adds an independent momentum judgment dimension for the strategy that's separate from Ichimoku. Since SSL Channel mainly reflects short-term price momentum, it can identify short-term trend changes that Ichimoku might miss.

### 4.2 Rate of Change Ratio (ROCR)

The Rate of Change Ratio measures the ratio relationship between current price and price N periods ago. The strategy uses 28-period ROCR, calculated as current closing price divided by closing price 28 periods ago.

ROCR greater than 1 means price has risen, ROCR less than 1 means price has fallen. But the strategy focuses not on ROCR's absolute value but its change direction—the strategy requires current ROCR greater than previous period's ROCR, i.e., ROCR must be in rising state.

The deeper meaning of this condition is price momentum must maintain or strengthen. If ROCR is in rising zone but starting to decline, it means upward momentum is weakening, possibly a precursor to trend reversal. The strategy requires ROCR to continuously rise, ensuring entry occurs when price upward momentum is abundant.

### 4.3 Relative Momentum Index (RMI)

The Relative Momentum Index is a variant of Relative Strength Index (RSI), but with different calculation method. RMI uses the difference between current price and price N periods ago in calculation, rather than adjacent period price changes used in traditional RSI.

The strategy uses fast RMI, parameters being length 9 and momentum period 3. This means calculation compares current price with price 3 periods ago. This setting makes RMI more sensitive to price changes, able to faster capture trend changes.

Entry condition requires current RMI-fast greater than RMI-fast 2 periods ago. This condition's design logic is similar to ROCR—ensuring momentum is in strengthening state. But as an overbought-oversold indicator, RMI's change angle provides a different perspective. RMI rising means buyer strength increasing, RMI falling means seller strength increasing.

### 4.4 Indicator Synergistic Effect

These four indicators—Ichimoku, SSL Channel, ROCR, RMI—although all trend judgment tools, focus on different time dimensions and market characteristics. Ichimoku provides medium-to-long-term trend framework, SSL Channel captures short-term momentum changes, ROCR measures price change rate, RMI evaluates momentum strength.

When these four indicators simultaneously emit bullish signals, the probability of market being in highly consistent bullish state significantly increases. This multi-indicator resonance design approach effectively reduces the risk of single indicator misjudgment. From information theory perspective, multi-source information consistency significantly improves signal reliability.

---

## 5. Entry Signal Mechanism

### 5.1 Eightfold Confirmation Conditions Detailed Explanation

The strategy's entry signal consists of eight conditions, all must be simultaneously satisfied to trigger buy signal. Let's analyze each condition's meaning and function:

Condition 1: Tenkan-sen above Kijun-sen (tenkan_sen > kijun_sen). This is the most basic trend judgment condition, ensuring short-term momentum direction is upward. When Tenkan-sen crosses above Kijun-sen, it suggests recent prices are starting to rise, market entering bullish state.

Conditions 2 and 3: Close price above Senkou Span A and above Senkou Span B (close > senkou_a and close > senkou_b). These two conditions jointly ensure price is above the cloud. Above cloud is bulls' safe zone, price here means bulls have advantage. Separate checking above both span lines is to confirm price has completely exited cloud area, not merely above cloud's lower edge.

Condition 4: Future cloud is green (future_green > 0). This condition checks whether forward-displaced Senkou Span A is higher than Senkou Span B, i.e., future cloud direction. This is a forward-looking indicator, by observing cloud state 30 periods ahead, judging future support-resistance pattern. Future cloud being green means future market expectation is bullish.

Condition 5: Chikou Span above cloud (chikou_high > 0). This is verification of historical prices, ensuring current price has exceeded price range from past 30 periods. Chikou Span above cloud means current trend is supported by historical prices, trend strength is verified.

Condition 6: SSL Channel bullish (ssl_high > 0). SSL Channel in bullish state, indicating short-term momentum also supports upward direction. This condition provides short-term momentum confirmation for Ichimoku's medium-to-long-term judgment.

Condition 7: ROCR rising (rocr > rocr.shift()). Rate of change ratio rising indicates price change rate is accelerating, upward momentum is strengthening. This condition ensures entry occurs when market is in accelerated rising phase, not momentum decaying phase.

Condition 8: RMI-fast strengthening (rmi-fast > rmi-fast.shift(2)). Relative momentum index higher than 2 periods ago indicates buyer strength is increasing. This condition verifies upward momentum strength from another angle.

### 5.2 Signal Trigger Logic

When all eight conditions first transition from unsatisfied to all satisfied, the strategy triggers buy signal. The `qtpylib.crossed_above(dataframe['go_long'], 0)` function implements this logic—detecting the moment go_long signal changes from 0 to positive.

This design has an important characteristic: entry only occurs when conditions are first satisfied. If market continues rising after satisfying conditions, the strategy won't repeatedly enter. This avoids the risk of multiple positions in a single trend, entering only once per trend.

### 5.3 Condition Weight Analysis

Although eight conditions have equal weight in code implementation, from market analysis perspective, their importance differs. Ichimoku's four conditions (TK cross, price above cloud, future cloud direction, Chikou Span verification) constitute the core framework of trend judgment, having highest weight. SSL Channel condition provides independent short-term momentum confirmation, having secondary weight. ROCR and RMI as auxiliary confirmation have relatively lower weight but are indispensable.

Understanding condition weights helps evaluate signal quality. When core conditions (Ichimoku) are strongly satisfied while auxiliary conditions are marginally satisfied, the signal may be less reliable than when all conditions are strongly satisfied. In practical application, traders can consider adjusting position size based on condition satisfaction degree.

---

## 6. Exit Signal Mechanism

### 6.1 Exit Condition Analysis

The strategy's exit signal design is relatively looser than entry signal. Exit signal consists of two parts: main condition is SSL Channel no longer bullish (ssl_high == 0), secondary condition is Tenkan-sen below Kijun-sen or close price below Kijun-sen.

Exit logic uses OR relationship: when SSL Channel turns bearish state, simultaneously satisfying (Tenkan-sen below Kijun-sen or close price below Kijun-sen), sell signal triggers. This design ensures exit occurs when trend has clearly turned, not merely due to short-term fluctuations.

### 6.2 Design Philosophy of Exit Signal

The reason exit conditions are looser than entry conditions is because timing exit is harder than timing entry. Exiting too early loses profits, exiting too late may suffer larger drawdowns. The strategy chose a balance point: exit when multiple indicators simultaneously point to trend weakening, not waiting for all indicators to turn bearish.

Specifically, exit signal requires SSL Channel to first turn bearish, which is independent confirmation outside Ichimoku. Then also requires Ichimoku showing bearish signal (TK cross downward or price below Kijun-sen), this dual confirmation avoids erroneous exits due to single indicator fluctuation.

### 6.3 Coordination with Stop-Loss Mechanism

Exit signal and stop-loss mechanism form a complementary relationship. Stop-loss as hard exit mechanism, forces exit when price drops beyond preset threshold, protecting capital safety. Exit signal as soft exit mechanism, proactively exits when trend clearly turns, locking profits.

Their division of labor is clear: stop-loss responsible for defense, exit signal responsible for offense. Ideally, exit signal identifies trend reversal and exits before stop-loss triggers. Stop-loss as final line of defense only triggers when market sharply drops or abnormal volatility occurs.

---

## 7. Risk Management System

### 7.1 Fixed Stop-Loss Strategy

The strategy's fixed stop-loss ratio is set at -7.5%, i.e., forced liquidation when position loss reaches 7.5%. This stop-loss distance setting needs to balance two factors: too small stop-loss gets triggered by normal volatility, too large stop-loss cannot effectively control risk.

A 7.5% stop-loss distance is relatively reasonable for cryptocurrency markets. Cryptocurrency intraday volatility of 5-10% is normal range, 7.5% stop-loss can survive most normal volatility while timely stopping loss when trend truly reverses.

### 7.2 Trailing Stop-Loss Mechanism

Trailing stop-loss is an important component of the strategy's risk management. Related parameters include: trailing stop activation threshold (trailing_stop_positive_offset) is 3%, trailing stop distance (trailing_stop_positive) is 0.5%, and only activates after price gain exceeds threshold (trailing_only_offset_is_reached = True).

Trailing stop-loss working principle: when position profit reaches 3%, system starts tracking highest price. If price pulls back more than 0.5% from highest point, sell triggers. This mechanism can keep profits while letting profits continue running.

Example: suppose entry price is $100, when price rises to $103 (3% profit), trailing stop starts activating. If price continues rising to $110, trailing stop line is at $109.45 (110 * 0.995). As long as price doesn't go below $109.45, position continues holding. If price pulls back from $110 to below $109.45, sell triggers, locking approximately 9.45% profit.

### 7.3 Minimum Return Target

The strategy configures progressive minimum return targets: immediate target 10% at opening, drops to 5% after 30 minutes, drops to 2% after 60 minutes. This design embodies the philosophy of "let profits run, but don't be greedy."

In early trend stages, market momentum is abundant, target is set higher to fully capture profits. As time passes, if trend fails to develop quickly, possibly indicating insufficient trend strength, then lowering target ensures profitable exit. This dynamic adjustment mechanism avoids missing exit opportunities by waiting for too high targets in late trend stages.

### 7.4 Synergistic Effect of Multi-Layer Protection

Fixed stop-loss, trailing stop-loss, and minimum return targets work synergistically, building a complete risk management system. Fixed stop-loss as basic protection, effective in all situations. Trailing stop-loss takes over after profit reaches threshold, providing tighter protection. Minimum return targets provide profit exit mechanism, proactively locking profits when trend is unclear.

Trigger logic of three-layer mechanism: if price quickly drops, fixed stop-loss triggers first, protecting principal. If price first rises then pulls back, trailing stop triggers, protecting profits. If price slowly rises but doesn't reach trailing stop condition, minimum return target triggers, ensuring profitable exit.

---

## 8. Parameter Configuration Optimization

### 8.1 Ichimoku Parameters

The Ichimoku parameter configuration in the strategy is the result of cryptocurrency market optimization. The combination of Tenkan-sen 20 periods, Kijun-sen 60 periods, lagging line 120 periods, displacement 30 periods, significantly extended compared to traditional parameters, to adapt to cryptocurrency markets' larger volatility.

These parameters can be optimized based on historical backtest data. Optimization goal is to find optimal balance point between capturing trends and avoiding noise. If Tenkan-sen period is too short, too many false signals are produced; if period is too long, early stages of trend launch are missed.

### 8.2 SSL Channel Parameters

SSL Channel uses 10-period calculation, a relatively sensitive setting. Channel width is determined by ATR, ATR itself uses 14-period calculation. These parameters can be adjusted based on market characteristics—in high volatility markets can increase periods to reduce noise, in low volatility markets can decrease periods to increase sensitivity.

### 8.3 Confirmation Indicator Parameters

ROCR uses 28 periods, RMI-fast uses length 9 and momentum period 3. These parameters are chosen based on empirical values, can achieve better effects through optimization. During optimization, need to be careful about avoiding overfitting—parameters too specifically optimized for historical data may perform poorly in live trading.

### 8.4 Risk Control Parameters

Stop-loss -7.5%, trailing stop threshold 3%, trailing stop distance 0.5% all need adjustment based on trader's risk tolerance and market characteristics. Conservative traders can set tighter stop-loss, aggressive traders can set wider stop-loss to give trend more development room.

---

## 9. Backtesting and Practical Recommendations

### 9.1 Backtesting Configuration Key Points

Strategy documentation provides detailed backtest pair screening configuration, these configurations are crucial for backtest result reliability. Volume screening ensures sufficient liquidity, listing time screening ensures data stability, price screening excludes extremely low-priced coins, spread screening lowers transaction costs, volatility screening ensures market has sufficient trading opportunities.

During backtesting, need to note startup candle count set to 180, which is minimum data volume required for Ichimoku calculation. If data is insufficient, strategy will produce unstable signals in early stages.

### 9.2 Market Adaptability Analysis

The strategy is most suitable for strong trending market environments. In clear bullish or bearish trends, Ichimoku can effectively identify trend direction and track trend development. In ranging or sideways consolidation markets, the strategy may produce more false signals.

Recommend conducting sufficient market state classification testing before live trading, evaluating strategy performance in different market environments. Can consider adding market state recognition module, pausing trading or reducing position size in ranging markets.

### 9.3 Capital Management Recommendations

Although the strategy itself doesn't contain position management logic, reasonable capital management is crucial for long-term success. Recommend single trade risk not exceeding 1-2% of total capital, this way even consecutive multiple stop-losses won't cause fatal damage to account.

According to Kelly formula, given win rate and risk-reward ratio, optimal position ratio can be calculated. But considering market uncertainty, recommend using half-Kelly or more conservative position ratio in practical application.

---

## 10. Strategy Advantages and Limitations

### 10.1 Core Advantages

The strategy's main advantages are reflected in the following aspects:

First, high degree of systemization. All rules in the strategy have clear definitions, no space for subjective judgment. This avoids human weaknesses like fear and greed interfering with trading decisions, ensuring every trade is based on the same logic.

Second, multiple confirmation mechanism reduces false signal probability. The combination of eight entry conditions significantly improves signal quality, statistically significantly lowering erroneous entry probability.

Third, comprehensive risk management. Multi-layer protection system of fixed stop-loss, trailing stop-loss, and dynamic return targets provides multiple guarantees for capital safety.

Fourth, parameters optimized for cryptocurrency markets. Ichimoku's cryptocurrency-specific parameters make it more suitable for cryptocurrency market characteristics than strategies that blindly copy traditional market parameters.

### 10.2 Potential Limitations

The strategy's limitations also need objective recognition:

First, strict entry conditions may cause missing some opportunities. In early trend stages, some conditions may not be satisfied yet, waiting for all conditions to be complete may miss front segment profits of trend.

Second, insufficient adaptability to ranging markets. Ichimoku is essentially a trend-following system, may frequently trigger stop-losses in trendless ranging markets.

Third, parameter sensitivity. The strategy contains multiple parameters, different parameter combinations may produce significantly different results. Over-optimized parameters may perform excellently on historical data but fail in live trading.

Fourth, dependence on historical data quality. Strategy effectiveness highly depends on accuracy and completeness of historical price data, data anomalies may cause erroneous signals.

### 10.3 Improvement Directions

The strategy can be improved in the following directions:

First, add market state recognition. Identify current market state through volatility indicators or trend strength indicators, reduce trading frequency or pause trading in ranging markets.

Second, dynamic parameter adjustment. Dynamically adjust stop-loss distance and Ichimoku parameters based on market volatility, making strategy maintain adaptability in different market environments.

Third, multi-timeframe confirmation. Introduce higher timeframe trend judgment, only enter when higher timeframe trend direction is consistent, improving signal quality.

Fourth, machine learning enhancement. Use machine learning methods to optimize entry and exit conditions, or for recognizing market states, improving strategy's self-adaptive capability.

---

## 11. Summary and Outlook

### 11.1 Strategy Summary

Obelisk_TradePro_Ichi_v2_1 is a quant trading strategy with rigorous design and clear logic. It uses Ichimoku as core trend recognition framework, supplemented by SSL Channel, ROCR, RMI and other confirmation indicators, building a multi-verification entry mechanism. Risk management system is comprehensive, fixed stop-loss, trailing stop-loss, and dynamic return targets work synergistically, protecting principal while maximizing profit acquisition.

The strategy design embodies core principles of quantitative trading: systematic execution, risk control priority, multiple confirmation to reduce noise. These principles enable it to stably profit in suitable conditions, being an excellent example of medium-to-long-term trend-following strategy.

### 11.2 Applicable Recommendations

The strategy is suitable for traders with some quantitative trading experience. Beginners are recommended to first test sufficiently in simulated environment, understand strategy logic before considering live trading. The strategy has certain requirements for market liquidity, recommend applying to mainstream cryptocurrency trading pairs.

Before live trading, must conduct sufficient backtest verification, and adjust risk control parameters based on personal risk preference. Remember that any strategy has applicable conditions, no all-powerful strategy exists, continuous monitoring and timely adjustment are keys to long-term success.

### 11.3 Future Outlook

With cryptocurrency market development, market characteristics may change. Strategy needs regular effectiveness evaluation, parameter adjustment when necessary. Combining new technical analysis methods and machine learning technology can further enhance strategy adaptability and profitability on existing framework basis.

Quantitative trading is a continuous optimization process, no endpoint, only continuous improvement. Hope this strategy interpretation helps traders deeply understand strategy logic, achieving ideal returns in live trading.

---

*Document Version: v1.0*
*Strategy Version: Obelisk_TradePro_Ichi_v2_1*
*Applicable Timeframe: 1 Hour*
*Update Date: 2024*