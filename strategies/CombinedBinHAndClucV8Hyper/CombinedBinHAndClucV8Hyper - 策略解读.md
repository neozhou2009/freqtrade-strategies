# CombinedBinHAndClucV8Hyper 策略深度解读

> **策略编号**: #119 (第12批第119个策略)
> **策略类型**: 多因子均值回归型 · 超跌反弹策略
> **时间框架**: 5分钟 (5m)

---

## 一、策略概览

CombinedBinHAndClucV8Hyper 是一款**多因子均值回归型**交易策略，是 V8 版本的**Hyperoptable优化版**。该策略通过融合 **BinHV45** 和 **ClucMay72018** 两套经典超跌反弹逻辑，并引入**自定义止盈机制**与**自定义止损保护**，实现了在震荡市场中更精准地捕捉超跌反弹机会。

V8Hyper 版本的核心设计理念是：**在 V8 基础上引入可优化的超参数，使策略能够通过 Hyperopt 进一步适配不同市场环境**。

**V8Hyper 版本相较于 V8 的核心升级**：
- 新增可优化的买入参数：BB40参数、BB20参数、RSI参数、MFI参数等
- 新增可优化的卖出参数：RSI阈值
- 自定义止盈机制：根据不同盈利级别动态止盈（4级ROI + 2级追踪止盈）
- 自定义止损机制：基于时间和趋势的智能止损
- 更灵活的追踪止损配置：盈利达到3.11%后启动，回撤3.14%触发

---

## 二、策略配置解析

### 2.1 基础参数

| 参数 | 取值 | 说明 |
|------|------|------|
| `timeframe` | 5m | 5分钟K线，适合短线交易 |
| `inf_1h` | 1h | 1小时信息框架，用于趋势判断 |
| `minimal_roi` | {"0": 0.107, "15": 0.047, "75": 0.013, "106": 0} | 多级ROI止盈 |
| `stoploss` | -0.274 | 硬止损 -27.4% |
| `use_exit_signal` | True | 启用退出信号判断 |
| `exit_profit_only` | True | 仅在盈利状态下触发卖出信号 |
| `exit_profit_offset` | 0.001 | 盈利偏移 0.1% 后才允许卖出 |
| `ignore_roi_if_entry_signal` | True | 入场信号出现时忽略 ROI 限制 |

### 2.2 追踪止损配置

| 参数 | 取值 | 说明 |
|------|------|------|
| `trailing_stop` | True | 启用追踪止损 |
| `trailing_only_offset_is_reached` | False | 无论是否达到偏移量都启用追踪 |
| `trailing_stop_positive` | 0.314 | 追踪止损幅度 31.4% |
| `trailing_stop_positive_offset` | 0.411 | 盈利达到 41.1% 时启动追踪 |

> **V8Hyper 关键变化**：追踪止损启动点和回撤幅度都较大，适合长线趋势行情。

### 2.3 订单类型

```python
order_types = {
    'entry': 'limit',    # 限价单入场
    'exit': 'limit',     # 限价单出场
    'stoploss': 'market' # 止损单使用市价
}
```

---

## 三、买入条件详解

策略的买入信号由**五套独立条件**组合，只要满足任一套即触发买入：

### 3.1 条件一：BinHV45 策略（急跌反弹型）

```python
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['ema_50'] > dataframe['ema_200']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
dataframe['lower'].shift().gt(0) &
dataframe['bbdelta'].gt(dataframe['close'] * self.buy_bb40_bbdelta_close.value) &
dataframe['closedelta'].gt(dataframe['close'] * self.buy_bb40_closedelta_close.value) &
dataframe['tail'].lt(dataframe['bbdelta'] * self.buy_bb40_tail_bbdelta.value) &
dataframe['close'].lt(dataframe['lower'].shift()) &
dataframe['close'].le(dataframe['close'].shift()) &
(dataframe['volume'] > 0)
```

**信号解读**：

| 条件 | 含义 |
|------|------|
| `close > ema_200_1h` | 1小时级别价格在200日均线上方，确认长线上涨趋势 |
| `ema_50 > ema_200` | 5分钟级别短期均线在长期均线上方，确认短线强势 |
| `ema_50_1h > ema_200_1h` | 1小时级别短期均线在长期均线上方，确认1小时级别强势 |
| `rolling(2).max - close < threshold_1` | 2根K线内最高点与收盘价差距小于阈值，确认小幅回调 |
| `rolling(12).max - close < threshold_2` | 12根K线内最高点与收盘价差距小于阈值，确认不是高位 |
| `bbdelta > close * 0.029` | 布林带通道宽度至少为当前价格的2.9% |
| `closedelta > close * 0.012` | 当日收盘价与前收盘价差值超过1.2% |
| `tail < bbdelta * 0.212` | 下影线长度小于通道宽度的21.2% |
| `close < lower.shift()` | 收盘价跌破前一交易日的布林带下轨 |
| `close <= close.shift()` | 收盘价不高于前一日收盘 |

**综合逻辑**：在大级别上涨趋势中，价格小幅回调并刺穿布林带下轨，同时波动率足够、下影线短——这是典型的**超跌反弹**形态。

### 3.2 条件二：ClucMay72018 策略（缩量超跌型）

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['ema_50_1h'] > dataframe['ema_100_1h']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
(dataframe['close'] < dataframe['ema_slow']) &
(dataframe['close'] < self.buy_bb20_close_bblowerband.value * dataframe['bb_lowerband']) &
(dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * self.buy_bb20_volume.value))
```

**信号解读**：

| 条件 | 含义 |
|------|------|
| `close > ema_200` | 价格在200日均线上方 |
| `close > ema_200_1h` | 1小时级别价格在200日均线上方 |
| `ema_50_1h > ema_100_1h > ema_200_1h` | 1小时级别均线多头排列 |
| `close < ema_slow` | 价格在50日EMA下方，属于回调区域 |
| `close < 0.991 * bb_lowerband` | 价格跌破布林带下轨0.991倍 |
| `volume < volume_mean_slow * 34` | 成交量低于30日均量的34倍 |

**综合逻辑**：在大级别上涨趋势中，价格回调至布林带下轨附近，同时成交量萎缩——这是典型的**缩量超跌**形态。

### 3.3 条件三：RSI背离型（V8新增）

```python
(dataframe['close'] < dataframe['sma_5']) &
(dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &
(dataframe['ema_50'] > dataframe['ema_200']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
(((dataframe['open'].rolling(144).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_3.value) &
(dataframe['rsi'] < dataframe['rsi_1h'] - self.buy_rsi_diff.value)
```

**信号解读**：

| 条件 | 含义 |
|------|------|
| `close < sma_5` | 价格在5日均线下方，短期弱势 |
| `ssl_up_1h > ssl_down_1h` | 1小时级别SSL通道显示上涨趋势 |
| `rsi < rsi_1h - 45.82` | 5分钟RSI低于1小时RSI超过45.82，存在RSI背离 |

**综合逻辑**：短期价格创新低但RSI未创新低，形成**底背离**信号。

### 3.4 条件四：趋势回调型

```python
(dataframe['sma_200'] > dataframe['sma_200'].shift(20)) &
(dataframe['sma_200_1h'] > dataframe['sma_200_1h'].shift(16)) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
(((dataframe['open'].rolling(144).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_3.value) &
(((dataframe['open'].rolling(24).min() - dataframe['close']) / dataframe['close']) > self.buy_min_inc.value) &
(dataframe['rsi_1h'] > self.buy_rsi_1h.value) &
(dataframe['rsi'] < self.buy_rsi.value) &
(dataframe['mfi'] < self.buy_mfi.value)
```

**信号解读**：

| 条件 | 含义 |
|------|------|
| `sma_200 > sma_200.shift(20)` | 200日均线向上倾斜20天 |
| `sma_200_1h > sma_200_1h.shift(16)` | 1小时200日均线向上倾斜16天 |
| `rolling(24).min - close > 0.05` | 24根K线内最低点与当前价差超过5% |
| `rsi_1h > 42.66` | 1小时RSI高于42.66 |
| `rsi < 34.94` | 5分钟RSI低于34.94 |
| `mfi < 57.29` | MFI低于57.29 |

**综合逻辑**：在长线上涨趋势中，价格回调至支撑位，同时RSI和MFI都处于超卖区域。

### 3.5 条件五：EMA交叉型

```python
(dataframe['close'] > dataframe['ema_100_1h']) &
(dataframe['ema_50_1h'] > dataframe['ema_100_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
(((dataframe['open'].rolling(144).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_3.value) &
(dataframe['volume'].rolling(4).mean() * self.buy_volume_1.value > dataframe['volume']) &
(dataframe['ema_26'] > dataframe['ema_12']) &
((dataframe['ema_26'] - dataframe['ema_12']) > (dataframe['open'] * self.buy_ema_open_mult_1.value)) &
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > (dataframe['open'] / 100)) &
(dataframe['close'] < (dataframe['bb_lowerband']))
```

**信号解读**：

| 条件 | 含义 |
|------|------|
| `close > ema_100_1h` | 价格在1小时100日均线上方 |
| `ema_50_1h > ema_100_1h` | 1小时级别EMA50上穿EMA100 |
| `volume rolling(4) * 2 > volume` | 4根K线平均成交量大于当前成交量2倍 |
| `ema_26 > ema_12` | EMA26在EMA12上方（多头排列） |
| `close < bb_lowerband` | 价格在布林带下轨下方 |

**综合逻辑**：在1小时级别上涨趋势中，EMA形成金叉，同时价格跌破布林带下轨。

---

## 四、卖出条件详解

### 4.1 条件一：布林带上轨突破（连续确认）

```python
(dataframe['close'] > dataframe['bb_upperband']) &
(dataframe['close'].shift(1) > dataframe['bb_upperband'].shift(1)) &
(dataframe['close'].shift(2) > dataframe['bb_upperband'].shift(2)) &
(dataframe['volume'] > 0)
```

**信号解读**：连续3根K线收盘价都在布林带上轨上方，确认有效突破。

### 4.2 条件二：RSI超买

```python
(dataframe['rsi'] > self.sell_rsi_main.value) &
(dataframe['volume'] > 0)
```

**信号解读**：RSI超过76.4，进入超买区域。

---

## 五、指标计算详解

### 5.1 SSL Channels（1小时）

```python
def SSLChannels(dataframe, length = 20):
    df = dataframe.copy()
    df['ATR'] = ta.ATR(df, timeperiod=14)
    df['smaHigh'] = df['high'].rolling(length).mean() + df['ATR']
    df['smaLow'] = df['low'].rolling(length).mean() - df['ATR']
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, 
                np.where(df['close'] < df['smaLow'], -1, np.nan))
    df['hlv'] = df['hlv'].ffill()
    df['sslDown'] = np.where(df['hlv'] < 0, df['smaHigh'], df['smaLow'])
    df['sslUp'] = np.where(df['hlv'] < 0, df['smaLow'], df['smaHigh'])
    return df['sslDown'], df['sslUp']
```

### 5.2 1小时时间框架指标

- EMA: 50, 100, 200
- SMA: 200（用于判断趋势方向）
- RSI: 14周期
- SSL Channels: 20周期

### 5.3 5分钟时间框架指标

- Bollinger Bands: 40周期（用于BB40条件）, 20周期（用于BB20条件）
- EMA: 12, 26, 50, 200
- SMA: 5, 200
- RSI: 14周期
- MFI: 14周期
- 成交量均线: 30周期

---

## 六、自定义止损机制（custom_stoploss）

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
    # 亏损超过280分钟后，如果还在亏损，直接平仓
    if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
        return 0.01
    
    # 如果跌幅超过-5%且SMA200同时下行，则平仓
    elif (current_profit < self.sell_custom_stoploss_1.value):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        if (last_candle is not None):
            if (last_candle['sma_200_dec']) & (last_candle['sma_200_dec_1h']):
                return 0.01
    
    return 0.99
```

**止损逻辑**：
1. **时间止损**：亏损状态持续280分钟（约4.7小时）后强制平仓
2. **趋势止损**：亏损超过5%且200日均线同时下行时平仓

---

## 七、自定义退出机制（custom_exit）

```python
def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                current_profit: float, **kwargs):
    # 4级ROI止盈
    if (current_profit > 0.14) & (last_candle['rsi'] < 58):
        return 'roi_target_4'
    elif (current_profit > 0.08) & (last_candle['rsi'] < 56):
        return 'roi_target_3'
    elif (current_profit > 0.04) & (last_candle['rsi'] < 50):
        return 'roi_target_2'
    elif (current_profit > 0.01) & (last_candle['rsi'] < 50):
        return 'roi_target_1'
    elif (current_profit > 0) & (current_profit < 0.04) & (last_candle['sma_200_dec']):
        return 'roi_target_5'
    
    # 2级追踪止盈
    if (current_profit > 0.1) & (current_profit < 0.4) & (最高点回撤 > current_profit + 0.03):
        return 'trail_target_1'
    elif (current_profit > 0.02) & (current_profit < 0.1) & (最高点回撤 > current_profit + 0.015):
        return 'trail_target_2'
```

**止盈逻辑**：
- **ROI止盈**：根据不同盈利级别和RSI条件退出
- **追踪止盈**：根据最高点回撤幅度退出

---

## 八、参数优化空间

### 8.1 可优化买入参数

| 参数 | 默认值 | 优化范围 | 说明 |
|------|--------|----------|------|
| `buy_bb40_bbdelta_close` | 0.029 | 0.005 - 0.04 | BB40通道宽度系数 |
| `buy_bb40_closedelta_close` | 0.012 | 0.01 - 0.03 | 收盘价变化系数 |
| `buy_bb40_tail_bbdelta` | 0.212 | 0.2 - 0.4 | 下影线系数 |
| `buy_bb20_close_bblowerband` | 0.991 | 0.8 - 1.1 | BB20下轨倍数 |
| `buy_bb20_volume` | 34 | 18 - 36 | 成交量系数 |
| `buy_rsi_diff` | 45.82 | 34 - 60 | RSI差异阈值 |
| `buy_min_inc` | 0.05 | 0.005 - 0.05 | 最小涨幅 |
| `buy_rsi_1h` | 42.66 | 40 - 70 | 1小时RSI阈值 |
| `buy_rsi` | 34.94 | 30 - 40 | 5分钟RSI阈值 |
| `buy_mfi` | 57.29 | 36 - 65 | MFI阈值 |

### 8.2 可优化卖出参数

| 参数 | 默认值 | 优化范围 | 说明 |
|------|--------|----------|------|
| `sell_rsi_main` | 76.4 | 72 - 90 | RSI超买阈值 |

---

## 九、风险提示

1. **硬止损较宽**：-27.4%的止损幅度较大，可能导致较大亏损
2. **追踪止损启动门槛高**：盈利41.1%才启动追踪止损，可能错失部分利润
3. **多因子条件复杂**：5套买入条件增加了过拟合风险
4. **时间框架依赖**：1小时信息框架的计算结果会影响5分钟交易决策
5. **市场适应性**：策略在震荡市场表现较好，在单边下跌市场可能亏损

---

## 十、适用场景

1. **震荡市场**：价格在布林带上下轨之间波动时
2. **趋势回调**：大级别上涨趋势中的回调机会
3. **波动率高**：布林带通道宽度较大时
4. **成交量活跃**：市场流动性充足的交易对

---

## 十一、总结

CombinedBinHAndClucV8Hyper 是一款融合了多种超跌反弹逻辑的**多因子均值回归型**策略。相比V8版本，它引入了更多可优化的超参数，使策略能够通过Hyperopt进一步适配不同市场环境。

**核心优势**：
- 多套买入条件，覆盖多种超跌反弹形态
- 自定义止盈机制，4级ROI + 2级追踪止盈
- 自定义止损机制，时间止损 + 趋势止损
- 可优化的超参数，增强市场适应性

**核心风险**：
- 硬止损较宽，可能导致较大亏损
- 参数优化空间大，需要谨慎过拟合
- 追踪止损门槛高，可能错失部分利润

**使用建议**：
- 建议配合使用 4-6 个交易对
- 建议使用 Volume Pairlist
- 建议排除杠杆代币（*BULL, *BEAR, *UP, *DOWN等）
- 建议在 USDT 交易对中使用