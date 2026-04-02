# CBPete9 Strategy Analysis

> **Strategy ID**: Batch 08  
> **Strategy Type**: Multi-Condition Oversold Reversal + Fast Exit  
> **Timeframe**: 5 minutes (primary) | 1 hour (informational)

---

## I. Strategy Overview

CBPete9 (Combined Bin H Cluc And MAD V9) is an optimized trading strategy derived from ilya's CombinedBinHClucAndMADV9. The strategy's core design philosophy is **capturing short-term rebound opportunities while controlling drawdowns**, using multi-dimensional technical indicator combinations to implement a "buy low, sell fast" trading logic.

| Core Attribute | Value |
|--------------|-------|
| Strategy Name | CBPete9 |
| Author | ilya (original), based on iterativ's CombinedBinHAndCluc series |
| Timeframe | 5 minutes |
| Informational Timeframe | 1 hour |
| Minimal ROI | 0.028 (0 min) → 0.018 (10 min) → 0.005 (40 min) |
| Stop-Loss | -0.99 (substantially disabled, uses custom stop-loss) |
| Trailing Stop | Enabled |
| Buy Signals | 10 independent conditions |
| Sell Signal | Price breaks Bollinger Band middle band 1.01× |

**Core Design Philosophy**:
- Minimize drawdowns as much as possible
- Buy when price has fallen significantly (counter-trend/left-side trading)
- Sell quickly (release capital for next trade)
- Soft-check market uptrend (uptrend confirmation)
- Hard-check market decline (downtrend confirmation)
- Custom stop-loss mechanism to prevent single catastrophic losses

---

## II. Strategy Configuration Analysis

### 2.1 Timeframe Configuration

```python
timeframe = '5m'      # Primary trading: 5-minute candles
inf_1h = '1h'         # Informational: 1-hour candles (for trend filtering)
```

### 2.2 Take-Profit and Stop-Loss Configuration

```python
minimal_roi = {
    "0": 0.028,      # Immediately available 2.8% profit
    "10": 0.018,     # After 10 minutes: 1.8% profit
    "40": 0.005,     # After 40 minutes: 0.5% profit
}

stoploss = -0.99     # Base stop-loss set to -99%, substantially disabled
```

**Design Intent**: The strategy does not rely on traditional stop-loss, but implements finer risk control through a custom stop-loss function. The minimal ROI curve indicates the strategy expects to complete trades within a short period (40 minutes).

### 2.3 Trailing Stop Configuration

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.003        # Activates when profit reaches 1.87%
trailing_stop_positive_offset = 0.0187
```

### 2.4 Order Type Configuration

```python
order_types = {
    'entry': 'market',
    'exit': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

All use market orders for immediate execution.

---

## III. Entry Conditions Details

CBPete9 contains **10 independent buy conditions**, combined through Boolean "OR" logic. Meeting any one condition triggers a buy signal.

### Condition 1: Dual Timeframe EMA Filter + Bollinger Band Rebound

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['close'] < dataframe['bb_lowerband'] * 0.99) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['open'] - dataframe['close'] < dataframe['bb_upperband'].shift(2) - dataframe['bb_lowerband'].shift(2))
```

**Logic**: Price is in an uptrend (dual-timeframe EMA confirmed), but briefly touched the Bollinger Band lower band forming a rebound point, with volume showing a "first surge then contract" accumulation pattern.

### Condition 2: Single Timeframe EMA + Bollinger Band Extreme Oversold

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] < dataframe['bb_lowerband'] * 0.982) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4) &
(dataframe['volume'] < dataframe['volume'].shift() * 4)
```

**Logic**: Compared to Condition 1, relaxes the 1-hour EMA requirement but requires price closer to the Bollinger Band lower band (0.982×).

### Condition 3: 1-Hour Trend Confirmation + RSI Oversold

```python
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['close'] < dataframe['bb_lowerband']) &
(dataframe['rsi'] < 14.2) &
(dataframe['volume'] < dataframe['volume'].shift() * 4)
```

**Logic**: 1-hour confirms uptrend, 5-minute shows RSI extreme oversold (<14.2), forming high-probability short-term rebound entry.

### Condition 4: 1-Hour RSI Extreme Oversold

```python
(dataframe['rsi_1h'] < 16.5) &
(dataframe['close'] < dataframe['bb_lowerband']) &
(dataframe['volume'] < dataframe['volume'].shift() * 4)
```

**Logic**: Uses 1-hour RSI to determine if the overall market is in an extreme oversold state.

### Condition 5: Dual Timeframe EMA Trend + MACD Golden Cross

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['ema_26'] > dataframe['ema_12']) &
((dataframe['ema_26'] - dataframe['ema_12']) > dataframe['open'] * 0.02) &
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > dataframe['open']/100) &
(dataframe['close'] < dataframe['bb_lowerband'])
```

**Logic**: Multi-timeframe trend confirmation with MACD golden cross forms a "trend + momentum" dual-confirmation entry.

### Condition 6: MACD Strong Golden Cross

```python
(dataframe['ema_26'] > dataframe['ema_12']) &
((dataframe['ema_26'] - dataframe['ema_12']) > dataframe['open'] * 0.03) &
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > dataframe['open']/100) &
(dataframe['close'] < dataframe['bb_lowerband']) &
(dataframe['volume'] < dataframe['volume'].shift() * 4)
```

**Logic**: Compared to Condition 5, places greater emphasis on MACD momentum strength (difference requirement increased from 0.02 to 0.03).

### Condition 7: 1-Hour RSI Oversold + MACD Golden Cross

```python
(dataframe['rsi_1h'] < 15.0) &
(dataframe['ema_26'] > dataframe['ema_12']) &
((dataframe['ema_26'] - dataframe['ema_12']) > dataframe['open'] * 0.02) &
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > dataframe['open']/100) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4)
```

**Logic**: Combines 1-hour RSI oversold and MACD golden cross for "long-cycle oversold + short-cycle momentum reversal" dual entry.

### Condition 8: Dual Timeframe RSI Oversold

```python
(dataframe['rsi_1h'] < 20.0) &
(dataframe['rsi'] < 28.0) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4)
```

**Logic**: Both 5-minute and 1-hour RSI are in oversold territory simultaneously (<28 and <20), suggesting the market may be at a short-term bottom.

### Condition 9: 1-Hour RSI Moderate Oversold + 5-Minute RSI Extreme Oversold

```python
(dataframe['rsi_1h'] < 35.0) &
(dataframe['rsi'] < 10.0) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4)
```

**Logic**: Allows 1-hour RSI in a relatively moderate oversold zone (<35), but requires 5-minute RSI extremely oversold (<10), suitable for fast rebound scenarios.

### Condition 10: Trend Reversal Combined Signal

```python
(dataframe['close'] < dataframe['sma_5']) &
(dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(dataframe['rsi'] < dataframe['rsi_1h'] - 43.276) &
(dataframe['volume'] > 0)
```

**Logic**: Complex trend reversal signal combining SSL Channel, EMA crossovers, and RSI divergence.

---

## IV. Exit Logic Details

### 4.1 Main Sell Condition

```python
dataframe.loc[
    (
        (dataframe['close'] > dataframe['bb_middleband'] * 1.01) &
        (dataframe['volume'] > 0)
    ),
    'sell'
] = 1
```

**Design Philosophy**: The strategy's core philosophy is "sell quickly." When price rebounds to 1% above the Bollinger Band middle band, immediately take profit and exit, freeing capital for the next trade.

---

## V. Risk Management Highlights

### 5.1 Custom Stop-Loss Mechanism

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    # Profit state: trailing stop
    if current_profit > 0:
        return 0.99

    # Loss state: time-based stop
    trade_time_50 = current_time - timedelta(minutes=50)

    if trade_time_50 > trade.open_date_utc:
        try:
            number_of_candle_shift = int((trade_time_50 - trade.open_date_utc).total_seconds() / 300)
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            candle = dataframe.iloc[-number_of_candle_shift].squeeze()

            # Price still falling: stop-loss
            if current_rate * 1.015 < candle['open']:
                return 0.01  # Stop-loss exit
        except IndexError:
            return 0.01

    return 0.99
```

**Logic**:
1. **When profitable** (current_profit > 0): Returns 0.99, essentially not disabling trailing stop, letting trailing stop rules manage it
2. **After holding over 50 minutes and at a loss**:
   - Checks if price continued falling during holding period
   - If current price is 1.5% below the opening price 50 minutes ago, immediately stop-loss
   - This is the strategy's core mechanism to "prevent catastrophic drops"

---

## VI. Strategy Pros & Cons

### Strengths

1. **Multi-Dimensional Signal Filtering**: 10 independent buy conditions, verifying signals from multiple dimensions including trend, momentum, and volume
2. **Dual-Period Analysis**: Combines 5-minute and 1-hour periods, capturing short-term opportunities while filtering counter-trend trades
3. **Fast Trading**: Completes trades within 40 minutes, improving capital utilization
4. **Custom Stop-Loss**: Specifically designed for "continued decline" scenarios, avoiding long-term holding in losing positions
5. **No Optimization Needed**: Pre-set parameters ready to use, reducing the usage barrier

### Weaknesses

1. **High Trading Frequency**: Preset 2–4 simultaneous positions may generate high trading fees
2. **Conservative Profit Targets**: Maximum 2.8% profit target may be frequently stopped out in ranging markets
3. **Simple Sell Logic**: Only relies on Bollinger Band middle band for exits, may miss significant rallies
4. **Volume Dependency**: Multiple conditions rely on volume contraction confirmation, may fail in low-liquidity markets
5. **Parameter Sensitivity**: Some parameters (RSI thresholds, volume ratios) need market-specific adjustment

---

## VII. Summary

CBPete9 is a meticulously designed short-term trading strategy with the core philosophy of **"capturing short-term rebound opportunities while controlling drawdowns"**.

Its main features:
1. **10 Independent Buy Conditions**: Multi-dimensional signal verification including trend, momentum, and volume
2. **Dual-Period Analysis**: Combines 5-minute and 1-hour periods for sensitivity and robustness
3. **Custom Stop-Loss**: Specifically designed for "continued decline" scenarios, effectively controlling risk
4. **Fast Trading**: Completes trades within 40 minutes, high capital efficiency
5. **No Optimization Needed**: Pre-set parameters ready to use

**Risk Warning**:
- High trading frequency may generate significant fees
- May underperform in one-sided trending markets
- Strategy complexity is high; requires thorough understanding before personalizing

---

*This document is auto-generated based on the CBPete9 strategy source code.*
