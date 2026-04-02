# CombinedBinHAndClucV8XHO Strategy Analysis

> **Strategy Number**: #121 (121st of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Multi-Level Take-Profit
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHAndClucV8XHO** is a multi-condition quantitative trading strategy built on classic technical indicators such as Bollinger Bands, RSI, MFI, and EMA. This strategy is the eighth version (V8) of the CombinedBinHAndCluc series, optimized by XHO (possibly a developer's nickname).

From a code architecture perspective, this strategy combines multiple classic buy trigger conditions, using multi-indicator cross-validation to improve signal reliability. Meanwhile, the exit logic employs a combination of multi-level take-profit and trailing stop mechanisms.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 5 independent buy signals, each containing complex condition combinations |
| **Sell Conditions** | 2 basic sell signals + 4-level dynamic take-profit + 2 trailing stop groups |
| **Protection Mechanisms** | Implicit protection (via EMA trend, SMA trend, etc.) |
| **Timeframe** | 5-minute primary timeframe + 1-hour informational timeframe |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "30": 0.05,   # After 30 minutes: 5% profit
    "60": 0.02,   # After 60 minutes: 2% profit
}

# Stop Loss Settings
stoploss = -0.99  # Effectively disabled hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01      # 1% trailing activation point
trailing_stop_positive_offset = 0.03  # 3% offset trigger
```

**Design Philosophy**:
- The hard stop-loss set to -99% means the strategy hardly relies on hard stops; instead, it manages risk through custom stop-loss logic (`custom_stoploss`)
- The ROI table uses a decreasing strategy: the longer the holding period, the lower the exit threshold, which aligns with long-term trend-following philosophy
- Trailing stop sets a small positive offset (1%) and trigger point (3%), suitable for locking in profits during trending markets

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'limit',      # Limit order entry
    'exit': 'limit',       # Limit order exit
    'stoploss': 'market',  # Market order stop-loss
    'stoploss_on_exchange': False
}
```

**Configuration Notes**:
- Using limit orders for entry and exit achieves better fill prices while reducing trading costs
- Using market orders for stop-loss ensures rapid fills during extreme market conditions, controlling slippage risk
- Exchange-built-in stop-loss is disabled, switching to Freqtrade's local stop-loss logic for greater flexibility

---

## III. Entry Conditions Details

### 3.1 Condition Combination Structure

The strategy's 5 buy conditions are not simple independent checks — each contains multiple layers of compound logic. They can be broadly categorized as follows:

| Condition Group | Condition # | Core Logic |
|----------------|-------------|------------|
| **Bollinger Band 40-Period Rebound** | #1 | BB40 lower band breakout + EMA trend confirmation |
| **Bollinger Band 20-Period Low Volume** | #2 | BB20 lower band low-volume rebound + EMA trend confirmation |
| **RSI Divergence + SSL Channel** | #3 | RSI relative weakness + SSL channel uptrend |
| **RSI/MFI Oversold** | #4 | 1h RSI strong + 5m oversold + MFI low value |
| **EMA Crossover + Bollinger Band** | #5 | EMA golden cross + volume contraction + BB lower band |

### 3.2 Typical Entry Condition Examples

#### Condition #1: Bollinger Band 40-Period Rebound
```python
# Logic
- close > EMA200 (1h)
- EMA50 > EMA200 (5m)
- EMA50 (1h) > EMA200 (1h)
- 2-period high - close < 12%
- 12-period high - close < 28%
- BB40 lower_band.shift() > 0
- BB40 bandwidth > close × 3.7%
- close change > close × 1%
- tail < BB40 bandwidth × 33.8%
- close < BB40 lower_band.shift()
- close <= previous close
- volume > 0
```

**Design Philosophy**: Comprehensively uses 1h-level long-term trend confirmation (EMA200) and 5m-level short-term rebound signals (BB40). Multiple filter conditions ensure entries only occur when trends are clear and price is in oversold territory.

#### Condition #4: RSI/MFI Oversold
```python
# Logic
- SMA200 in uptrend (20 periods ago vs current)
- SMA200 (1h) in uptrend (16 periods ago vs current)
- 2/12/144-period high - close < respective thresholds
- 24-period low - close > 1% (minimum gain)
- RSI (1h) > 66.97
- RSI (5m) < 35.74
- MFI < 44.88
- volume > 0
```

**Design Philosophy**: Uses 1h long-term RSI trend as the dominant direction (must be in strong territory), while seeking oversold opportunities at the 5m level. MFI serves as an auxiliary confirmation of money flow.

#### Condition #5: EMA Crossover + Bollinger Band
```python
# Logic
- close > EMA100 (1h)
- EMA50 (1h) > EMA100 (1h)
- 4-period volume average × 2.65 > current volume
- EMA26 > EMA12 (death cross, but reverse logic here)
- EMA difference > open price × 1.8%
- Previous period EMA difference > open price × 1%
- close < BB20 lower_band
- volume > 0
```

**Design Philosophy**: This is a reverse-momentum strategy. It waits for an EMA death cross followed by a price touch on the Bollinger lower band — a mean-reversion opportunity.

### 3.3 Entry Condition Parameter Table

```python
# Core Buy Parameters
buy_bb40_bbdelta_close = 0.037        # BB40 bandwidth coefficient
buy_bb40_closedelta_close = 0.01     # Close change coefficient
buy_bb40_tail_bbdelta = 0.338        # Tail/bandwidth coefficient

buy_bb20_close_bblowerband = 0.982   # BB20 lower band multiplier
buy_bb20_volume = 35                 # Volume multiple

buy_rsi = 35.74                      # 5m RSI threshold
buy_rsi_1h = 66.97                   # 1h RSI threshold
buy_rsi_diff = 49.29                 # RSI difference threshold

buy_mfi = 44.88                      # MFI threshold
buy_min_inc = 0.01                   # Minimum gain

buy_ema_open_mult_1 = 0.018          # EMA difference coefficient
buy_volume_1 = 2.65                  # Volume coefficient

# Dip Thresholds
buy_dip_threshold_0 = 0.015          # 2-period dip threshold
buy_dip_threshold_1 = 0.12           # 12-period dip threshold
buy_dip_threshold_2 = 0.28           # 144-period dip threshold
buy_dip_threshold_3 = 0.36           # 144-period dip threshold (longest)
```

---

## IV. Exit Conditions Details

### 4.1 Multi-Level Take-Profit System

The strategy employs a 4-level dynamic take-profit mechanism, dynamically adjusting RSI exit thresholds based on profit rate zones:

```
Profit Rate Zone      RSI Threshold    Signal Name
─────────────────────────────────────────────────────
> 14%                 < 58             roi_target_4
> 8%                  < 56             roi_target_3
> 4%                  < 50             roi_target_2
> 1%                  < 55.4           roi_target_1
Positive but < 4%     Trend-confirmed  roi_target_5
```

**Design Logic**:
- Higher profit rates allow longer holding (more relaxed RSI thresholds)
- Small profits of 1%-4% require stricter RSI conditions (< 50-55), preventing trend reversals
- Large profits above 14% are more tolerant (< 58), letting profits run

### 4.2 Trailing Stop System

The strategy implements two trailing stop groups:

| Trailing Group | Min Profit | Max Profit | Drawdown Trigger | Signal Name |
|----------------|------------|------------|-------------------|-------------|
| **#1** | 10% | 40% | 3% drawdown | trail_target_1 |
| **#2** | 2% | 10% | 1.5% drawdown | trail_target_2 |

**Design Logic**:
- Group #1 is suitable for capturing medium-to-long-term trends (10%-40% profit range)
- Group #2 is suitable for short-term operations (2%-10% profit range), with more sensitive drawdown triggers

### 4.3 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit):
    # Scenario 1: Holding > 280 minutes and at a loss
    if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
        return 0.01  # Exit immediately
    
    # Scenario 2: Custom stop-loss threshold triggered AND in downtrend
    elif current_profit < -5%:  # -5%
        if sma_200_dec (5m) & sma_200_dec (1h):
            return 0.01  # Exit
    
    # Scenario 3: X-version special - attempt to capture minor pullbacks
    elif 0 >= current_profit >= -5%:
        if sma_200_dec &
           close > bb_middleband &
           rsi > 45.95:  # sell_rsi_parachute
            return 0.01  # Exit
    
    return 0.99  # Keep position
```

**Design Highlights**:
- 280-minute (approximately 4.7 hours) forced exit mechanism prevents long-holding of losing positions
- X-version special feature: adds "parachute" logic — attempts to capture a rebound before exiting during small losses

### 4.4 Basic Sell Signals

```python
# Sell Signal 1: Consecutive Bollinger Upper Band Breakouts
- close > BB20 upper band (4 consecutive candles)
- volume > 0

# Sell Signal 2: RSI Overbought
- RSI > 72.45
- volume > 0
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|-------------------|---------|
| **Trend Indicators** | EMA(12, 26, 50, 100, 200), SMA(5, 200) | Trend judgment, multi-timeframe confirmation |ion |
| **Bollinger Band** | BB40, BB20 (upper/lower/middle bands) | Overbought/oversold, breakout signals |
| **Momentum Indicators** | RSI(14), MFI(14) | Overbought/oversold, money flow |
| **Volatility Indicators** | ATR(14) | SSL channel calculation |

### 5.2 Custom Indicators

#### SSL Channels (Custom Function)
```python
def SSLChannels(dataframe, length=7):
    # Calculate ATR channel
    ATR = ta.ATR(df, timeperiod=14)
    smaHigh = high.rolling(length).mean() + ATR
    smaLow = low.rolling(length).mean() - ATR
    
    # Determine trend direction
    hlv = np.where(close > smaHigh, 1,
                   np.where(close < smaLow, -1, np.nan))
    
    # Generate SSL upper/lower bands
    sslDown = np.where(hlv < 0, smaHigh, smaLow)
    sslUp = np.where(hlv < 0, smaLow, smaHigh)
```

### 5.3 Informational Timeframe Indicators (1h)

The strategy uses the 1-hour chart as an informational layer for higher-dimensional trend judgment:

- **EMA Series**: EMA50, EMA100, EMA200 — Long-term trend confirmation
- **SMA200**: 200-period simple moving average for trend direction
- **SMA200_dec**: Whether SMA200 is in a downtrend (current value < value 20 periods ago)
- **RSI**: 14-period RSI for 1h-level momentum
- **SSL Channel**: 20-period SSL channel for medium-to-long-term trend

---

## VI. Risk Management Features

### 6.1 Multi-Timeframe Confirmation

The core risk management philosophy cross-validates 1h and 5m indicators to filter false signals:
- Almost all buy conditions require EMA200 (1h) to be in an uptrend
- SMA200_dec is used for downtrend detection and stop-loss triggering

### 6.2 Custom Stop-Loss Mechanism

Unlike traditional hard stops, this strategy uses complex custom stop-loss logic:
- 280-minute forced exit mechanism
- Multi-level conditional stops (-5% and 0% as two trigger points)
- "Parachute" logic attempts to capture rebounds during losses

### 6.3 Take-Profit Strategy Combination

| Take-Profit Type | Trigger Condition | Count |
|-----------------|------------------|-------|
| **ROI Take-Profit** | Profit rate + RSI condition | 4 levels |
| **Trailing Stop** | Profit rate zone + drawdown | 2 groups |
| **Basic Signals** | BB upper band breakout / RSI overbought | 2 signals |

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Condition Filtering**: 5 independent buy conditions each contain complex compound logic, effectively filtering false signals
2. **Multi-Timeframe**: 1h informational layer provides long-term trend confirmation; 5m captures entry timing
3. **Flexible Take-Profit System**: 4-level ROI + 2 trailing stop groups, adapting to different profit zones
4. **Custom Stop-Loss**: Targeted handling of various loss scenarios, including forced exits and "parachute" logic
5. **No Hard Stop-Loss Dependency**: -99% stop-loss setting gives the strategy ample room for error

### Limitations

1. **Many Parameters**: buy_params and sell_params contain 20+ parameters, making optimization difficult
2. **Trend-Dependent**: Most buy conditions require EMA200 in an uptrend; may fail in sideways or declining markets
3. **Complex Take-Profit Logic**: Multi-level take-profit may cause premature exits in some situations
4. **Computational Resources**: Multi-timeframe calculations consume some resources

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|-------------------------|-------|
| **Trending Upward** | Recommended | Multi-condition requires 1h uptrend, suitable for trending markets |
| **Volatile Market** | Use with caution | Dip thresholds and oversold conditions may trigger frequently |
| **Trending Downward** | Not recommended | Buy conditions mostly unsatisfied |
| **High-Volatility Coins** | Adjust parameters | Dip thresholds may need to be loosened |

---

## IX. Live Trading Notes

**CombinedBinHAndClucV8XHO** is the eighth version of the CombinedBinHAndCluc series, using a multi-condition compound strategy. It is best suited for **markets with clear upward trends**, improving signal quality through multi-timeframe trend confirmation and multi-indicator filtering.

### 9.1 Core Strategy Logic

- **Trend Priority**: Nearly all buy conditions require the long-term trend to be rising
- **Dip Buying**: Dip thresholds (dip_threshold) control entry positions
- **Momentum Confirmation**: RSI, MFI, etc. confirm oversold/overbought status
- **Multi-Level Take-Profit**: Dynamically adjusts exit strategy based on profit rate

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Trending Up | ⭐⭐⭐⭐⭐ | Core design scenario; multi-condition filtering effective |
| Volatile Market | ⭐⭐⭐☆☆ | Dip conditions may trigger frequently; take-profit premature |
| Trending Down | ⭐☆☆☆☆ | Buy conditions mostly unsatisfied |
| High Volatility | ⭐⭐⭐☆☆ | Dip thresholds need adjustment |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|------------------|-------|
| Number of Pairs | 20-40 | Moderate number, suitable for trend strategy |
| Open Positions | 4-6 | Recommended limit on open positions |
| Pair Type | USDT stable pairs | Avoid BTC/ETH-dominated weak markets |
| Blacklist | Leveraged tokens | Strongly recommend adding *BULL, *BEAR, *UP, *DOWN |

---

## X. Summary

**CombinedBinHAndClucV8XHO** is a meticulously designed multi-condition trend-following strategy. Its core value lies in:

1. **Multi-Timeframe Analysis**: 1h confirms trend, 5m captures timing
2. **Multi-Condition Compound Filtering**: 5 independent conditions each contain multiple layers of compound logic
3. **Flexible Risk Control System**: Combination of custom stop-loss + multi-level take-profit + trailing stop

For quantitative traders, this strategy is suitable for those with some Freqtrade experience. When using it, note:
- Fully understand each buy condition's logic
- Adjust parameters based on target market
- Use sufficiently long backtesting periods to verify strategy effectiveness
- Start with minimum position sizes during live trading observation

---

*This strategy is developed from CombinedBinHAndClucV8 and optimized by themoz.*
