# CombinedBinHAndClucV2 Strategy Analysis

> **Strategy #**: #110 (110th of 465 strategies)
> **Strategy Type**: Multi-Timeframe Bollinger Band Combination Strategy + Three-Layer Signal Filtering
> **Main Timeframe**: 5 Minutes (5m)
> **Auxiliary Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

**CombinedBinHAndClucV2** is an enhanced version of the classic dual-strategy combination **CombinedBinHAndCluc**, developed by iterativ. This strategy introduces **multi-timeframe analysis** and **trend filtering mechanisms** on top of the original version. It uses 1-hour SSL channels to judge the market's big trend and executes trades at the 5-minute level, with three-layer signal verification via MFI money flow and StochRSI momentum indicators, significantly improving signal reliability.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 layers: Big trend (SSL) + Momentum (MFI/StochRSI) + Pattern (BinHV45/ClucMay72018) |
| **Sell Conditions** | 1 basic sell signal + staged ROI take-profit |
| **Protection Mechanism** | StoplossGuard (max 2 trades per pair in 24 candles, 12-candle cooldown) |
| **Timeframe** | Main 5m + Auxiliary 1h |
| **Stop-Loss** | -5% (tighter than original -10%) |
| **Dependencies** | TA-Lib, numpy, qtpylib, technical |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# Staged ROI Take-Profit Table
minimal_roi = {
    "0": 0.10,      # Immediate exit: 10% profit
    "30": 0.05,     # After 30 minutes: 5% profit
    "60": 0.02,     # After 60 minutes: 2% profit
    "120": 0.01,    # After 120 minutes: 1% profit
}

# Stop-Loss Settings
stoploss = -0.05   # -5% hard stop-loss (tighter than original -10%)

# Trading Timeframe
timeframe = '5m'              # Main timeframe: 5 Minutes
informative_timeframe = '1h'  # Auxiliary timeframe: 1 Hour

# Sell Signal Configuration
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = True  # New buy signal can override ROI
```

**Design Philosophy**:
- **Aggressive ROI**: 0% threshold means 10% take-profit immediately, 5% after 30 minutes — suitable for fast short-term profits.
- **Tight Stop-Loss**: -5% stop-loss tighter than original -10%, reducing per-trade maximum loss risk.
- **Multi-Timeframe**: 1h judges trends, 5m executes trades, filtering counter-trend signals.
- **Signal Priority**: `ignore_roi_if_entry_signal = True` allows new buy signals to override ROI exits.

### 2.2 Trading Protection Mechanism

```python
protections = [
    {
        "method": "StoplossGuard",
        "lookback_period_candles": 24,      # Look back 24 candles
        "trade_limit": 2,                   # Max 2 trades
        "stop_duration_candles": 12,        # Cool down 12 candles
        "only_per_pair": True               # Calculate per pair separately
    }
]
```

**Protection Logic**:
- Max 2 trades per pair within 24 candles (2 hours).
- After triggering limits, must wait 12 candles (1 hour) cooldown.
- Prevents frequent openings leading to fee erosion and overtrading.

### 2.3 Trading Pair Suggestions

```python
# Suggested trading pairs
# - Mainstream coins: BTC/USDT, ETH/USDT
# - High-volatility coins: SOL/USDT, ADA/USDT, AVAX/USDT
# - Avoid low-volatility coins
```

---

## III. Entry Conditions Details

V2's entry conditions use **three-layer filtering** — all must be satisfied to trigger a buy signal. This significantly improves signal quality but also reduces signal frequency.

### 3.1 Layer 1: Big Trend Filtering (1h SSL Channel)

**SSL Channel Indicator**: Dynamic support/resistance band adjusted by ATR

```python
# Calculate SSL Channel
ssl_down, ssl_up = SSLChannels(dataframe, length=25)
dataframe['ssl_high'] = (ssl_up > ssl_down).astype('int') * 3

# Trend Judgment Condition
(dataframe['ssl_high'] > 0)  # SSL channel upward, indicating uptrend
```

**Logic Interpretation**:
- SSL channel upward: Price in 1h-level uptrend.
- Only consider buying under the premise of following the big trend.
- Filters counter-trend trades, reducing being trapped risk.

### 3.2 Layer 2: Momentum Filtering (MFI + StochRSI)

```python
# MFI (Money Flow Indicator)
dataframe['mfi'] = ta.MFI(dataframe, timeperiod=30)

# StochRSI (Stochastic RSI)
stoch = ta.STOCHRSI(dataframe, 30, 35, 2, 2)
dataframe['srsi_fk'] = stoch['fastk']   # K value
dataframe['srsi_fd'] = stoch['fastd']   # D value

# Momentum Condition: Both MFI and K value rising
(dataframe['mfi'].shift().rolling(3).mean() > dataframe['mfi']) &
(dataframe['srsi_fk'].shift().rolling(3).mean() > dataframe['srsi_fk'])
```

**Logic Interpretation**:
- **MFI Rising**: Capital inflow increasing, buying pressure strengthening.
- **StochRSI K Value Rising**: Short-term momentum turning stronger.
- **3-Period Moving Average Smoothing**: Avoids single-period noise interference.

### 3.3 Layer 3: Pattern Filtering (BinHV45 OR ClucMay72018)

Layer 3 uses "OR gate" logic — satisfying either pattern is sufficient.

#### 3.3.1 BinHV45 Mode

**Volatility Breakout Pattern**: Captures rebound opportunities after price rapidly breaks BB lower band

```python
(
    dataframe['lower'].shift().gt(0) &                    # BB exists
    dataframe['bbdelta'].gt(dataframe['close'] * 0.008) & # Width > 0.8%
    dataframe['closedelta'].gt(dataframe['close'] * 0.0175) & # Fluctuation > 1.75%
    dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &  # Wicking < 25%
    dataframe['close'].lt(dataframe['lower'].shift()) &  # Breaks lower band
    dataframe['close'].le(dataframe['close'].shift())     # Close weakens
)
```

| Condition | Parameter | Description |
|-----------|-----------|-------------|
| BB exists | lower > 0 | Previous BB lower band valid |
| Width threshold | bbdelta > close × 0.8% | BB opening sufficient |
| Fluctuation threshold | closedelta > close × 1.75% | Price fluctuation sufficient |
| Lower wick limit | tail < bbdelta × 25% | Short lower wick, support after decline |
| Breaks lower band | close < lower.shift() | Price breaks BB lower band |
| Close weakens | close ≤ close.shift() | Current close below previous candle |

#### 3.3.2 ClucMay72018 Mode

**Shrinking Volume Rebound Pattern**: Buys on dips when volume shrinks

```python
(
    (dataframe['close'] < dataframe['ema_slow']) &        # Below EMA50
    (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) & # Breaks lower band
    (dataframe['volume'] < dataframe['volume_mean_slow'].shift(1) * 20) # Shrinking volume
)
```

| Condition | Parameter | Description |
|-----------|-----------|-------------|
| Below EMA | close < EMA50 | Price in weak position below long-term MA |
| Breaks lower band | close < 98.5% × lower | Price breaks BB lower band |
| Volume shrinks | volume < 20 × avg | Current volume extremely low, selling pressure exhausted |

### 3.4 Entry Conditions Summary

| Filter Layer | Condition Name | Core Logic | Timeframe |
|-------------|----------------|-----------|-----------|
| Layer 1 | SSL Channel | Uptrend confirmation | 1h |
| Layer 2 | MFI | Capital inflow confirmation | 5m |
| Layer 2 | StochRSI | Momentum strengthening confirmation | 5m |
| Layer 3 | BinHV45 | Volatility breakout pattern | 5m |
| Layer 3 | ClucMay72018 | Shrinking volume rebound pattern | 5m |

---

## IV. Exit Conditions Details

### 4.1 Technical Sell: BB Upper Band Breakdown

**Trigger Condition**:

```python
qtpylib.crossed_below(dataframe['close'], dataframe['bb_upperband'])
```

**Logic Interpretation**:
- Triggers sell when price crosses below BB upper band.
- Indicates price may transition from uptrend to pullback.
- Symmetric with the lower band breakout at entry.

### 4.2 ROI Staged Take-Profit

| Holding Time | Take-Profit Threshold | Design Logic |
|------------|---------------------|-------------|
| 0 minutes (immediate) | 10% | Capture instant large swings |
| 30 minutes | 5% | Mid-wave target |
| 60 minutes | 2% | Prevent profit retreat |
| 120 minutes | 1% | Prevent holding indefinitely |

### 4.3 Stop-Loss Exit

**Trigger Condition**: Forced liquidation when loss reaches 5%.

**Logic Interpretation**:
- -5% stop-loss tighter than original -10%.
- Paired with multi-timeframe filtering, wrong trades should be fewer.
- Per-trade maximum loss controllable.

---

## V. Technical Indicator System

### 5.1 Auxiliary Timeframe Indicators (1h)

| Indicator | Calculation Method | Purpose |
|---------|-------------------|---------|
| **SSL Channel** | ATR-adjusted MA channel (period 25) | Trend judgment |
| **MFI** | 30-period money flow indicator | Capital flow verification |
| **StochRSI** | Stochastic RSI (30, 35, 2, 2) | Momentum conversion verification |

### 5.2 Main Timeframe Indicators (5m)

| Indicator | Calculation Method | Purpose |
|---------|-------------------|---------|
| **BB (40,2)** | Bollinger Bands | BinHV45 pattern judgment |
| **BB (20,2)** | Bollinger Bands | ClucMay72018 pattern |
| **EMA50** | 50-period exponential moving average | Trend verification |
| **Volume Average** | 30-period average volume | Shrinking volume verification |

### 5.3 Custom Calculated Indicators

| Indicator | Formula | Purpose |
|---------|---------|---------|
| **bbdelta** | \|middle - lower\| | BB width |
| **closedelta** | \|close - previous close\| | Price fluctuation magnitude |
| **tail** | \|close - low\| | Lower wick length |
| **ssl_high** | SSL channel direction tag | Trend state |

---

## VI. Risk Management Features

### 6.1 Stop-Loss Strategy

| Stop-Loss Type | Threshold | Description |
|---------------|-----------|-------------|
| **Hard Stop-Loss** | -5% | Forced liquidation at 5% loss |

**Comparison with Original**:
- Original CombinedBinHAndCluc: -10%
- V2 Version: -5%
- Tightened by half, reflecting confidence in three-layer filtering signals.

### 6.2 Take-Profit Strategy

| Take-Profit Type | Threshold | Description |
|----------------|-----------|-------------|
| **Instant Take-Profit** | 10% | Immediate exit |
| **Staged ROI** | 1%-5% | Timed exit |

**Design Features**:
- Instant take-profit threshold higher (original 5% → V2 10%).
- Staged take-profit balances fast profit capture with holding duration.

### 6.3 Trading Protection

| Protection Mechanism | Parameters | Description |
|--------------------|------------|-------------|
| **StoplossGuard** | 24/2/12 | Trade frequency limit |

**Protection Effect**:
- Max 2 trades per pair within 2 hours.
- 1-hour cooldown.
- Effectively prevents overtrading and emotional operations.

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-Timeframe Analysis**: 1h trend filtering + 5m signal execution, avoids counter-trend trades.
2. **Three-Layer Signal Filtering**: Trend + momentum + pattern, significantly improves buy signal quality.
3. **Dynamic Trend Recognition**: SSL channel automatically identifies market direction.
4. **Capital Flow Verification**: MFI confirms capital inflow, avoids false breakouts.
5. **Trading Protection**: Prevents overtrading and emotional decisions from fee erosion.
6. **Tight Stop-Loss**: -5% stop-loss reduces per-trade risk.
7. **Staged Take-Profit**: Multi-layer profit protection.

### Cons

1. **Scarce Signals**: Three-layer filtering overlay may significantly reduce buy frequency.
2. **Timeframe Dependency**: 1h trend judgment may lag.
3. **Parameter Coupling**: Layers' parameters interact, making optimization difficult.
4. **Simple Exit Logic**: Only relies on upper band breakout, lacks trailing stop.
5. **No Dynamic Stop-Loss**: May miss trending opportunities.

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|--------------------------|-------------|
| **Trending Uptrend** | max_open_trades=2-3 | SSL channel upward, high signal quality |
| **Volatile Market** | Use cautiously | SSL frequently flips, signal unstable |
| **Mainstream Coins** | BTC/ETH/SOL | Good liquidity, controllable slippage |
| **High-Volatility Coins** | Participate moderately | BB opening wide, patterns clearer |

---

## IX. Applicable Market Environment Details

CombinedBinHAndClucV2 is positioned as a **trend pullback-type multi-timeframe combination strategy** in the Freqtrade ecosystem. Based on its code architecture and three-layer filtering, it is best suited for **clear uptrend pullback opportunities** and may perform poorly in **volatile or declining** environments.

### 9.1 Core Strategy Logic

- **Trend is King**: SSL channel judges 1h-level big trend, only trades following the major direction.
- **Capital Verification**: MFI confirms capital inflow, avoids non-fundamental rebounds.
- **Momentum Confirmation**: StochRSI verifies short-term momentum, avoids chasing highs.
- **Pattern Entry**: BinHV45 or ClucMay72018 pattern confirms entry point.

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Trending Uptrend | ⭐⭐⭐⭐⭐ | SSL channel upward, three-layer filtering highest signal quality |
| Volatile Market | ⭐⭐☆☆☆ | SSL frequently flips, signals unstable, may miss opportunities |
| Sustained Decline | ⭐☆☆☆☆ | SSL channel downward, buy signals completely filtered |
| Extreme Volatility | ⭐⭐⭐☆☆ | MFI and StochRSI may generate false signals |

---

## X. Summary

**CombinedBinHAndClucV2** is a **multi-timeframe trend pullback strategy** for moderately experienced traders. Its core value:

1. **Multi-Dimensional Signal Verification**: Through 1h SSL trend + 5m MFI/StochRSI momentum + pattern three-layer filtering, significantly improves buy signal quality.
2. **Tight Risk Control**: -5% stop-loss paired with staged ROI, balancing risk and return.
3. **Trading Protection**: StoplossGuard prevents overtrading.

For quantitative traders, this strategy suits users who understand multi-timeframe analysis, can accept lower signal frequency, and pursue signal reliability. Not recommended for high-frequency traders or users who like frequent operations. Conduct sufficient backtesting and paper trading verification before live trading.
