# CBPete9 策略解读

## 一、策略概览

CBPete9（Combined Bin H Cluc And MAD V9）是基于 ilya 的 CombinedBinHClucAndMADV9 策略优化而来的交易策略。该策略的核心设计理念是**在控制回撤的前提下捕捉短期反弹机会**，通过多维度的技术指标组合实现"低买快卖"的交易逻辑。

| 核心属性 | 值 |
|---------|-----|
| 策略名称 | CBPete9 |
| 作者 | ilya（原始作者），基于 iterativ 的 CombinedBinHAndCluc 系列 |
| 时间周期 | 5分钟 |
| 信息周期 | 1小时 |
| 最小ROI | 0.028（0分钟）→ 0.018（10分钟）→ 0.005（40分钟） |
| 止损 | -0.99（实质禁用，采用自定义止损） |
| 追踪止损 | 启用 |
| 买入信号数量 | 10个独立条件 |
| 卖出信号 | 价格突破布林带中轨1.01倍 |

**核心设计哲学**：
- 尽可能降低回撤
- 在价格深跌时买入（左侧交易）
- 快速卖出（释放资金用于下一笔交易）
- 软性检查市场趋势（上涨确认）
- 硬性检查市场下跌（下跌确认）
- 自定义止损机制，防止单笔巨额亏损

---

## 二、策略配置解析

### 2.1 时间框架配置

```python
timeframe = '5m'      # 主交易周期：5分钟K线
inf_1h = '1h'         # 信息周期：1小时K线（用于辅助判断）
```

策略采用双时间周期框架，5分钟K线用于实际交易决策，1小时K线用于过滤市场整体趋势。

### 2.2 止盈止损配置

```python
minimal_roi = {
    "0": 0.028,      # 持仓立即可获得2.8%利润
    "10": 0.018,     # 持仓10分钟后可获得1.8%利润
    "40": 0.005,     # 持仓40分钟后可获得0.5%利润
}

stoploss = -0.99     # 基础止损设置为-99%，实质禁用
```

**设计意图**：该策略不依赖传统止损，而是通过自定义止损函数实现更精细的风险控制。最小ROI曲线表明策略预期在短时间内（40分钟内）完成交易。

### 2.3 追踪止损配置

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.003        # 利润达到1.87%时激活
trailing_stop_positive_offset = 0.0187
```

### 2.4 订单类型配置

```python
order_types = {
    'entry': 'market',
    'exit': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

全部采用市价单执行，确保订单即时成交。

---

## 三、买入条件详解

CBPete9策略包含**10个独立的买入条件**，通过布尔逻辑"或"运算组合。只要满足任意一个条件，即可触发买入信号。

### 条件1：双周期EMA过滤 + 布林带反弹

```python
(dataframe['close'] > dataframe['ema_200']) &                           # 5分钟价格 > 200EMA
(dataframe['close'] > dataframe['ema_200_1h']) &                        # 1小时价格 > 200EMA
(dataframe['close'] < dataframe['bb_lowerband'] * 0.99) &              # 价格接近布林下轨
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4) &  # 成交量放大
(dataframe['volume'] < dataframe['volume'].shift() * 4) &              # 成交量萎缩
(dataframe['open'] - dataframe['close'] < dataframe['bb_upperband'].shift(2) - dataframe['bb_lowerband'].shift(2))  # 实体较小
```

**逻辑**：价格处于上升趋势（双周期EMA确认），但短期触及布林下轨形成反弹点，同时成交量呈现"先放大后萎缩"的洗盘特征。

### 条件2：单周期EMA + 布林带极端超卖

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] < dataframe['bb_lowerband'] * 0.982) &             # 更接近布林下轨
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
```

**逻辑**：相比条件1，放宽了1小时周期EMA的限制，但要求价格更加接近布林下轨（0.982倍），适用于5分钟周期的独立反弹行情。

### 条件3：1小时趋势确认 + RSI超卖

```python
(dataframe['close'] > dataframe['ema_200_1h']) &                       # 1小时趋势向上
(dataframe['close'] < dataframe['bb_lowerband']) &                     # 5分钟触及布林下轨
(dataframe['rsi'] < 14.2) &                                             # RSI超卖
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
```

**逻辑**：1小时周期确认上涨趋势，5分钟周期出现RSI极端超卖（<14.2），形成短期反弹概率较高的买入点。

### 条件4：1小时RSI极端超卖

```python
(dataframe['rsi_1h'] < 16.5) &                                         # 1小时RSI极端超卖
(dataframe['close'] < dataframe['bb_lowerband']) &                     # 价格触及布林下轨
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
```

**逻辑**：利用1小时RSI判断市场整体是否处于极端超卖状态，结合5分钟K线的布林下轨支撑。

### 条件5：双周期EMA趋势 + MACD金叉

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['ema_26'] > dataframe['ema_12']) &                          # MACD当前金叉
((dataframe['ema_26'] - dataframe['ema_12']) > dataframe['open'] * 0.02) &  # MACD差值足够大
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > dataframe['open']/100) &  # 前一MACD也已金叉
(dataframe['close'] < dataframe['bb_lowerband']) &                     # 价格低于布林下轨
```

**逻辑**：多周期趋势确认配合MACD金叉信号，在价格超卖位置形成"趋势+动量"双重确认的买入点。

### 条件6：MACD强势金叉

```python
(dataframe['ema_26'] > dataframe['ema_12']) &
((dataframe['ema_26'] - dataframe['ema_12']) > dataframe['open'] * 0.03) &  # MACD差值更大
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > dataframe['open']/100) &
(dataframe['close'] < dataframe['bb_lowerband']) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
```

**逻辑**：相比条件5，更强调MACD的动能强度（差值要求从0.02提升到0.03），适用于MACD信号较强的反弹行情。

### 条件7：1小时RSI超卖 + MACD金叉

```python
(dataframe['rsi_1h'] < 15.0) &
(dataframe['ema_26'] > dataframe['ema_12']) &
((dataframe['ema_26'] - dataframe['ema_12']) > dataframe['open'] * 0.02) &
((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > dataframe['open']/100) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4) &
```

**逻辑**：结合1小时RSI超卖和MACD金叉，形成"长周期超卖+短周期动能转向"的双重买入信号。

### 条件8：双周期RSI超卖

```python
(dataframe['rsi_1h'] < 20.0) &
(dataframe['rsi'] < 28.0) &
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30') * 0.4) &
```

**逻辑**：5分钟和1小时RSI同时处于超卖区域（分别为<28和<20），表明市场可能处于短期底部。

### 条件9：1小时RSI次级超卖 + 5分钟RSI极端超卖

```python
(dataframe['rsi_1h'] < 35.0) &                                         # 1小时RSI次级超卖
(dataframe['rsi'] < 10.0) &                                            # 5分钟RSI极端超卖
(dataframe['volume'] < dataframe['volume'].shift() * 4) &
(dataframe['volume_mean_slow'] > dataframe['volume_mean_slow'].shift(30) * 0.4) &
```

**逻辑**：允许1小时RSI在相对温和的超卖区域（<35），但要求5分钟RSI极度超卖（<10），适用于快速反弹场景。

### 条件10：趋势反转组合信号

```python
(dataframe['close'] < dataframe['sma_5']) &                            # 价格低于5日均线
(dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &                  # 1小时SSL通道上升
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &                   # 1小时EMA金叉
(dataframe['rsi'] < dataframe['rsi_1h'] - 43.276) &                    # 5分钟RSI相对1小时足够低
(dataframe['volume'] > 0)
```

**逻辑**：这是一个复杂的趋势反转信号组合：
- SSL通道确认1小时周期价格处于上升通道
- EMA50上穿EMA200确认长期趋势转多
- 5分钟RSI相对1小时RSI足够低（差值>43.276），表明短期超卖更严重
- 价格低于SMA5提供买入安全边际

---

## 四、卖出逻辑详解

### 4.1 主卖出条件

CBPete9的卖出逻辑相对简单：

```python
dataframe.loc[
    (
        (dataframe['close'] > dataframe['bb_middleband'] * 1.01) &      # 价格突破布林中轨1.01倍
        (dataframe['volume'] > 0)
    ),
    'sell'
] = 1
```

**设计理念**：策略的核心哲学是"快速卖出"，当价格回升到布林带中轨上方1%时，立即止盈离场，让出资金给下一笔交易。

### 4.2 卖出配置

```python
use_exit_signal = False         # 不使用退出信号
exit_profit_only = True         # 只在盈利时卖出
exit_profit_offset = 0.001      # 最小盈利门槛0.1%
ignore_roi_if_entry_signal = False  # 不忽略ROI检查
```

---

## 五、技术指标体系

### 5.1 趋势指标

| 指标 | 周期 | 用途 |
|------|------|------|
| EMA200 | 5分钟 | 短期长期趋势判断 |
| EMA200 | 1小时 | 长周期趋势确认 |
| EMA50 | 1小时 | 中期趋势判断 |
| EMA26/EMA12 | 5分钟 | MACD计算基础 |
| SMA5 | 5分钟 | 快速趋势判断 |

### 5.2 波动率指标

| 指标 | 参数 | 用途 |
|------|------|------|
| 布林带 | 20周期，2倍标准差 | 识别超买超卖区间 |
| ATR | 14周期 | 波动率计算 |

### 5.3 动量指标

| 指标 | 周期 | 用途 |
|------|------|------|
| RSI | 14 | 5分钟动量判断 |
| RSI | 14 | 1小时动量判断 |
| MACD | (12,26,9) | 趋势动量转换 |

### 5.4 成交量指标

| 指标 | 周期 | 用途 |
|------|------|------|
| volume_mean_slow | 30 | 成交量移动平均 |
| volume_drop | 4倍 | 成交量萎缩确认 |

### 5.5 特殊指标

| 指标 | 来源 | 用途 |
|------|------|------|
| SSL Channel | 自定义函数 | 趋势通道识别 |

---

## 六、风险管理特色

### 6.1 自定义止损机制

CBPete9最核心的风险管理在于其自定义止损函数：

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    # 盈利状态：追踪止损
    if current_profit > 0:
        return 0.99
    
    # 亏损状态：时间止损
    trade_time_50 = current_time - timedelta(minutes=50)
    
    if trade_time_50 > trade.open_date_utc:
        try:
            number_of_candle_shift = int((trade_time_50 - trade.open_date_utc).total_seconds() / 300)
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            candle = dataframe.iloc[-number_of_candle_shift].squeeze()
            
            # 价格仍在下跌：止损
            if current_rate * 1.015 < candle['open']:
                return 0.01  # 止损退出
        except IndexError:
            return 0.01
    
    return 0.99
```

**逻辑解析**：
1. **盈利时**（current_profit > 0）：返回0.99，实质不禁用追踪止损，由追踪止损规则接管
2. **持仓超过50分钟且亏损**：
   - 检查持仓期间价格是否继续下跌
   - 如果当前价格比50分钟前的开盘价还低1.5%，立即止损
   - 这是该策略"防止大跌"的核心机制

### 6.2 追踪止损

```python
trailing_stop_positive = 0.003          # 利润达到0.3%时激活
trailing_stop_positive_offset = 0.0187  # 基准利润1.87%
```

当利润达到1.87%时激活追踪止损，止损位设置为利润的0.3%。

---

## 七、策略优势与局限

### 7.1 优势

1. **多维度信号过滤**：10个独立的买入条件，从趋势、动量、成交量多个维度验证信号
2. **双周期分析**：5分钟和1小时周期结合，既捕捉短期机会又过滤逆势交易
3. **快速交易**：40分钟内完成交易，提高资金利用率
4. **自定义止损**：针对"持续下跌"场景的智能止损，避免长时间套牢
5. **无需优化**：预设参数即可使用，降低使用门槛

### 7.2 局限

1. **高交易频率**：预设2-4个同时持仓，可能产生较高的交易手续费
2. **利润目标保守**：最大2.8%的利润目标在震荡行情中可能被频繁止损
3. **卖出信号简单**：仅依靠布林中轨卖出，可能错过大幅上涨行情
4. **对成交量依赖**：多个条件依赖成交量萎缩确认，在低流动性市场可能失效
5. **参数敏感**：部分参数（如RSI阈值、成交量比例）需要根据市场调整

---

## 八、适用场景建议

### 8.1 推荐的交易环境

- **高波动性市场**：策略设计用于捕捉快速反弹，需要市场有足够的波动空间
- **主流币种**：建议用于市值较大的币种（如BTC、ETH），确保流动性
- **震荡市场**：在震荡市中"低买快卖"策略表现较好
- **有时间监控的场景**：虽然不需要HyperOpt优化，但建议有时间监控持仓

### 8.2 不适用的场景

- **单边下跌市场**：持续下跌可能导致连续止损
- **低波动市场**：波动不足时难以触发买入条件
- **低流动性币种**：成交量条件难以满足
- **长期持仓**：策略设计为短线交易，不适合长期持有

### 8.3 建议配置

```json
{
    "max_open_trades": 2,
    "stake_amount": "unlimited",
    "timeframe": "5m",
    "exit_profit_only": false,
    "dry_run": true
}
```

- 建议同时持仓2-4个交易对
- 使用"unlimited" stake_amount让策略自行管理仓位
- 建议先进行dry_run测试

---

## 九、适用市场环境详解

### 9.1 牛市环境

在牛市中，价格回调幅度通常有限，策略可能面临：
- 买入条件难以触发（价格较少触及布林下轨）
- 卖出信号过早触发（价格快速突破中轨）
- 整体表现可能不如简单持有

**建议**：可以适当放宽买入条件（如降低RSI阈值）

### 9.2 熊市环境

熊市中反弹频繁，策略表现较好：
- 频繁触及布林下轨提供买入机会
- 快速反弹触发卖出实现盈利
- 自定义止损有效控制单笔亏损

**建议**：密切关注止损触发频率，调整止损参数

### 9.3 震荡市场

最适合策略的环境：
- 价格在区间内波动，反复触及上下轨
- "低买快卖"逻辑完美契合
- 可以实现稳定的积少成多

**建议**：这是策略的最佳应用场景

---

## 十、重要提醒：复杂性的代价

### 10.1 信号过于复杂

CBPete9策略包含10个独立买入条件，这带来以下问题：

1. **难以理解**：每个条件都有其特定的适用场景，理解全部条件需要较长时间
2. **难以调试**：当策略表现不佳时，难以定位是哪个条件导致问题
3. **过度拟合风险**：多个条件组合可能只是对历史数据的过度拟合

### 10.2 参数众多

策略包含大量可调参数（虽然预设了默认值）：
- 11个买入条件开关
- 多个RSI阈值参数
- 成交量比例参数
- MACD阈值参数

### 10.3 建议

1. **充分理解后再调整**：在调整任何参数前，必须理解该参数的含义和影响
2. **逐个测试**：建议逐个启用买入条件，测试每个条件的表现
3. **记录基准**：在修改参数前记录策略的基准表现，以便对比
4. **长期观察**：至少观察2-4周的实际表现再决定是否调整

---

## 十一、总结

CBPete9是一个设计精良的短线交易策略，其核心理念是"**在控制回撤的前提下，通过多维度信号捕捉短期反弹机会**"。策略的主要特点包括：

1. **10个独立买入条件**：提供多维度的信号验证，包括趋势、动量、成交量等
2. **双周期分析**：结合5分钟和1小时周期，既敏感又稳健
3. **自定义止损**：专门针对"持续下跌"场景设计，有效控制风险
4. **快速交易**：40分钟内完成交易，资金利用效率高
5. **无需优化**：预设参数可直接使用，降低使用门槛

**使用方法**：
- 直接使用预设参数即可
- 建议配合2-4个同时持仓
- 建议先进行dry_run测试
- 密切关注自定义止损的触发情况

**风险提示**：
- 高交易频率可能导致较高手续费
- 在单边趋势行情中可能表现不佳
- 策略复杂度较高，需要充分理解后再进行个性化调整

---

*本文档基于CBPete9策略源码自动生成*