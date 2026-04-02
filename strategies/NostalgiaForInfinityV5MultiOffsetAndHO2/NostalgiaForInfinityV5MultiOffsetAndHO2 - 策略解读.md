# NostalgiaForInfinityV5MultiOffsetAndHO2 策略深度解读

> **策略编号**: #301  
> **策略类型**: 多指标复合趋势策略 + 多偏移MA系统  
> **时间框架**: 5分钟（主） + 1小时（辅助）

---

## 一、策略概览

NostalgiaForInfinityV5MultiOffsetAndHO2 是一个高度复杂的多指标复合策略，源自经典的 NostalgiaForInfinityV5 策略系列，融合了 MultiOffsetLamboV0 的多偏移均线系统和超参数优化。该策略通过21个买入条件和8个卖出条件构建了一个全方位的交易系统，同时引入了多重保护机制来管理风险。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 21个主条件 + 5个多偏移MA条件 = 26个买入入口 |
| **卖出条件** | 8个主条件 + 5个多偏移MA条件 + 自定义利润卖出 = 多重退出机制 |
| **保护机制** | 下跌保护(safe_dips)、暴涨保护(safe_pump)、追踪止损 |
| **时间框架** | 5m（主）+ 1h（辅助确认） |
| **依赖库** | talib, qtpylib, numpy, pandas |
| **超参数优化** | 大量 DecimalParameter 和 IntParameter |

### 策略演进历史

```
NostalgiaForInfinityV5 (原版)
    ↓
+ MultiOffsetLamboV0 (多偏移均线系统)
    ↓
+ 超参数优化 (Hyper-optimized)
    ↓
NostalgiaForInfinityV5MultiOffsetAndHO2
```

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# Minimal ROI - 极简止盈设置
minimal_roi = {
    "0": 0.01  # 即刻要求1%利润
}

# 止损设置
stoploss = -0.10  # -10%硬止损

# 追踪止损
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.03
```

**设计思路**：
- 1%的即时止盈目标强调快速周转
- 10%的止损空间平衡了风险和趋势空间
- 追踪止损在3%利润后启动，保护已获利润

### 2.2 订单类型配置

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'trailing_stop_loss': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}
```

策略使用限价单执行，有助于减少滑点影响。

### 2.3 多偏移均线系统参数

这是本策略的核心创新之一，支持5种均线类型的偏移计算：

```python
# 多偏移均线类型
ma_types = ['sma', 'ema', 'trima', 't3', 'kama']

# 买入偏移参数（低价入场）
low_offset_sma = 0.919   # SMA偏低0.919倍
low_offset_ema = 0.983   # EMA偏低0.983倍
low_offset_trima = 0.943 # TRIMA偏低0.943倍
low_offset_t3 = 0.975    # T3偏低0.975倍
low_offset_kama = 0.962  # KAMA偏低0.962倍

# 卖出偏移参数（高价出场）
high_offset_sma = 1.047   # SMA偏高1.047倍
high_offset_ema = 1.059   # EMA偏高1.059倍
high_offset_trima = 1.014 # TRIMA偏高1.014倍
high_offset_t3 = 1.072    # T3偏高1.072倍
high_offset_kama = 1.081  # KAMA偏高1.081倍
```

**设计哲学**：通过多种均线类型的组合，策略能够在不同市场环境中找到更精准的入场和出场点。

---

## 三、买入条件详解

策略设计了21个主买入条件，加上5个多偏移MA条件，共26个买入入口。

### 3.1 买入条件 #1：严格下跌捕捉

```python
(
    # 趋势确认（1小时级别）
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    (dataframe['sma_200'] > dataframe['sma_200'].shift(50)) &
    
    # 保护机制
    (dataframe['safe_dips_strict']) &
    (dataframe['safe_pump_24_1h']) &
    
    # RSI和MFI过滤
    (dataframe['rsi_1h'] > 51.4) &
    (dataframe['rsi_1h'] < 84.0) &
    (dataframe['rsi'] < 36.0) &
    (dataframe['mfi'] < 26.0) &
    
    # 最小涨幅确认
    (((dataframe['close'] - dataframe['open'].rolling(36).min()) / 
      dataframe['open'].rolling(36).min()) > 0.022)
)
```

**逻辑解析**：
- 1小时EMA50 > EMA200：确认大趋势向上
- SMA200上涨：确认长期趋势健康
- safe_dips_strict：确保没有过度下跌
- safe_pump_24_1h：确保近期没有暴涨
- RSI和MFI的双重过滤确认超卖反弹机会

### 3.2 买入条件 #2：布林带下轨反弹

```python
(
    # 1小时SMA200上涨趋势
    (dataframe['sma_200_1h'] > dataframe['sma_200_1h'].shift(50)) &
    
    # 严格暴涨保护
    (dataframe['safe_pump_24_strict_1h']) &
    
    # 低成交量确认
    (dataframe['volume_mean_4'] * 2.6 > dataframe['volume']) &
    
    # RSI差异策略
    (dataframe['rsi'] < dataframe['rsi_1h'] - 39.0) &
    
    # MFI和布林带
    (dataframe['mfi'] < 49.0) &
    (dataframe['close'] < (dataframe['bb_lowerband'] * 0.983))
)
```

**逻辑解析**：
- 利用5分钟RSI与1小时RSI的差异捕捉短期超卖
- 价格低于布林带下轨的98.3%，寻找极端下跌买入机会
- 低成交量确认市场没有恐慌性抛售

### 3.3 买入条件 #3：BB40形态突破

```python
(
    # EMA相对位置确认
    (dataframe['close'] > (dataframe['ema_200_1h'] * 0.986)) &
    (dataframe['ema_100'] > dataframe['ema_200']) &
    (dataframe['ema_100_1h'] > dataframe['ema_200_1h']) &
    
    # 严格暴涨保护
    (dataframe['safe_pump_36_strict_1h']) &
    
    # BB40形态
    dataframe['lower'].shift().gt(0) &
    dataframe['bbdelta'].gt(dataframe['close'] * 0.057) &
    dataframe['closedelta'].gt(dataframe['close'] * 0.023) &
    dataframe['tail'].lt(dataframe['bbdelta'] * 0.418) &
    dataframe['close'].lt(dataframe['lower'].shift()) &
    dataframe['close'].le(dataframe['close'].shift())
)
```

**逻辑解析**：
- BB40（40周期布林带）形态识别
- bbdelta > close * 0.057：布林带足够宽
- closedelta > close * 0.023：价格波动明显
- tail < bbdelta * 0.418：下影线不太长（非探底）
- 收盘价低于前一根K线的布林下轨

### 3.4 买入条件 #4：低成交量布林反弹

```python
(
    # 1小时趋势确认
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    
    # 保护机制
    (dataframe['safe_dips_strict']) &
    (dataframe['safe_pump_24_1h']) &
    
    # 价格位置
    (dataframe['close'] < dataframe['ema_50']) &
    (dataframe['close'] < 0.979 * dataframe['bb_lowerband']) &
    
    # 低成交量
    (dataframe['volume'] < (dataframe['volume_mean_30'].shift(1) * 10.0))
)
```

### 3.5 买入条件 #5：EMA分离+布林带

```python
(
    # 趋势确认
    (dataframe['ema_100'] > dataframe['ema_200']) &
    (dataframe['close'] > (dataframe['ema_200_1h'] * 0.982)) &
    
    # 保护机制
    (dataframe['safe_dips']) &
    (dataframe['safe_pump_36_strict_1h']) &
    
    # EMA分离形态
    (dataframe['ema_26'] > dataframe['ema_12']) &
    ((dataframe['ema_26'] - dataframe['ema_12']) > (dataframe['open'] * 0.019)) &
    ((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > (dataframe['open'] / 100)) &
    
    # 布林带位置
    (dataframe['close'] < (dataframe['bb_lowerband'] * 0.999))
)
```

**关键概念 - EMA分离**：
- EMA26 > EMA12 表示短期均线在长期均线下方（下降趋势中的回调）
- 但EMA差值 > open * 0.019 表示分离程度足够大
- 这是一个"均值回归"买点

### 3.6 买入条件 #6-8：变体策略

这三个条件是买入条件5的变体，主要差异在于：
- 条件#6：使用宽松下跌保护(safe_dips_loose)
- 条件#7：增加RSI过滤(< 36)
- 条件#8：特殊蜡烛形态确认

### 3.7 买入条件 #9-11：MA偏移策略

这三个条件使用SMA30和EMA20的偏移价格作为入场点：

```python
# 条件#9示例
(
    (dataframe['ema_50'] > dataframe['ema_200']) &
    (dataframe['ema_100'] > dataframe['ema_200']) &
    (dataframe['safe_dips_strict']) &
    (dataframe['safe_pump_24_loose_1h']) &
    
    # MA偏移入场
    (dataframe['close'] < dataframe['ema_20'] * 0.97) &
    (dataframe['close'] < dataframe['bb_lowerband'] * 0.985) &
    
    # RSI和MFI过滤
    (dataframe['rsi_1h'] > 30.0) &
    (dataframe['rsi_1h'] < 88.0) &
    (dataframe['mfi'] < 30.0)
)
```

### 3.8 买入条件 #12-13：EWO策略

利用Elliott Wave Oscillator（艾略特波浪震荡器）：

```python
# 条件#12：EWO高值策略
(
    (dataframe['sma_200_1h'] > dataframe['sma_200_1h'].shift(24)) &
    (dataframe['safe_dips_strict']) &
    (dataframe['safe_pump_24_1h']) &
    (dataframe['close'] < dataframe['sma_30'] * 0.936) &
    (dataframe['ewo'] > 2.0) &  # EWO高于阈值
    (dataframe['rsi'] < 30.0)
)

# 条件#13：EWO低值策略
(
    (dataframe['ema_50_1h'] > dataframe['ema_100_1h']) &
    (dataframe['ewo'] < -10.4) &  # EWO负值，表示可能的底部
    (dataframe['close'] < dataframe['sma_30'] * 0.978)
)
```

**EWO解读**：
- EWO = (EMA5 - EMA35) / close * 100
- 正值表示上升趋势，负值表示下降趋势
- 条件#12在EWO > 2时买入，捕捉趋势延续
- 条件#13在EWO < -10.4时买入，捕捉底部反转

### 3.9 买入条件 #14-18：综合过滤策略

这组条件结合了多种技术指标和MA偏移：

```python
# 条件#18：严格综合策略
(
    # 多重趋势确认
    (dataframe['close'] > dataframe['ema_200_1h']) &
    (dataframe['ema_100'] > dataframe['ema_200']) &
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    (dataframe['sma_200'] > dataframe['sma_200'].shift(20)) &
    (dataframe['sma_200'] > dataframe['sma_200'].shift(44)) &
    (dataframe['sma_200_1h'] > dataframe['sma_200_1h'].shift(36)) &
    (dataframe['sma_200_1h'] > dataframe['sma_200_1h'].shift(72)) &
    
    # 保护机制
    (dataframe['safe_dips']) &
    (dataframe['safe_pump_24_strict_1h']) &
    
    # RSI和布林带
    (dataframe['rsi'] < 26.0) &
    (dataframe['close'] < (dataframe['bb_lowerband'] * 0.982))
)
```

### 3.10 买入条件 #19：EMA100穿越策略

```python
(
    (dataframe['ema_100_1h'] > dataframe['ema_200_1h']) &
    (dataframe['sma_200'] > dataframe['sma_200'].shift(36)) &
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    
    # EMA100穿越形态
    (dataframe['close'].shift(1) > dataframe['ema_100_1h']) &
    (dataframe['low'] < dataframe['ema_100_1h']) &
    (dataframe['close'] > dataframe['ema_100_1h']) &
    
    # Chopiness指标
    (dataframe['chop'] < 41.8) &
    (dataframe['rsi_1h'] > 51.4)
)
```

**关键概念 - EMA穿越**：
- 前一根K线收盘价在EMA100上方
- 当前K线最低价下探EMA100
- 当前收盘价回到EMA100上方
- 这是一个经典的"假突破回调"买入形态

### 3.11 买入条件 #20-21：极端RSI策略

```python
# 条件#20：双重RSI超卖
(
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    (dataframe['safe_dips']) &
    (dataframe['safe_pump_24_loose_1h']) &
    (dataframe['rsi'] < 26.0) &
    (dataframe['rsi_1h'] < 20.0)  # 1小时RSI极度超卖
)

# 条件#21：更极端RSI
(
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    (dataframe['safe_dips_strict']) &
    (dataframe['rsi'] < 23.0) &
    (dataframe['rsi_1h'] < 24.0)
)
```

### 3.12 多偏移MA买入条件

这是本策略独特的入场机制，为5种均线类型各创建一个买入条件：

```python
for i in self.ma_types:  # ['sma', 'ema', 'trima', 't3', 'kama']
    conditions.append(
        (
            dataframe['close'] < dataframe[f'{i}_offset_buy']) &
            (
                (dataframe['ewo'] < -16.744) |  # EWO低值
                (dataframe['ewo'] > 7.714)      # 或EWO高值
            )
        )
    )
```

**设计哲学**：
- 价格低于偏移均线（偏移系数 < 1）时触发买入
- 同时要求EWO处于极端值（负值或正值）
- 多种均线类型提供多重入场机会

---

## 四、卖出逻辑详解

### 4.1 卖出条件 #1：RSI+布林带上轨确认

```python
(
    (dataframe['rsi'] > 79.5) &
    (dataframe['close'] > dataframe['bb_upperband']) &
    # 连续6根K线在布林上轨上方
    (dataframe['close'].shift(1) > dataframe['bb_upperband'].shift(1)) &
    (dataframe['close'].shift(2) > dataframe['bb_upperband'].shift(2)) &
    (dataframe['close'].shift(3) > dataframe['bb_upperband'].shift(3)) &
    (dataframe['close'].shift(4) > dataframe['bb_upperband'].shift(4)) &
    (dataframe['close'].shift(5) > dataframe['bb_upperband'].shift(5))
)
```

**逻辑解析**：
- RSI > 79.5：极度超买
- 连续6根K线在布林上轨上方：强势延续后的信号
- 这是一个"高位离场"信号

### 4.2 卖出条件 #2：简化版布林上轨

```python
(
    (dataframe['rsi'] > 81) &
    (dataframe['close'] > dataframe['bb_upperband']) &
    (dataframe['close'].shift(1) > dataframe['bb_upperband'].shift(1)) &
    (dataframe['close'].shift(2) > dataframe['bb_upperband'].shift(2))
)
```

只需连续3根K线确认，更加敏感。

### 4.3 卖出条件 #3：纯RSI超买

```python
(dataframe['rsi'] > 82)
```

最简单的卖出信号，RSI超过82即离场。

### 4.4 卖出条件 #4：双重RSI确认

```python
(
    (dataframe['rsi'] > 73.4) &
    (dataframe['rsi_1h'] > 79.6)
)
```

5分钟和1小时RSI同时超买，确认强度更高。

### 4.5 卖出条件 #6：EMA200下方反弹卖出

```python
(
    (dataframe['close'] < dataframe['ema_200']) &
    (dataframe['close'] > dataframe['ema_50']) &
    (dataframe['rsi'] > 79.0)
)
```

**逻辑解析**：
- 价格在EMA200下方（整体趋势偏弱）
- 价格在EMA50上方（短期反弹）
- RSI超买
- 这是一个"弱势反弹卖出"信号

### 4.6 卖出条件 #7：MACD死叉+RSI

```python
(
    (dataframe['rsi_1h'] > 81.7) &
    qtpylib.crossed_below(dataframe['ema_12'], dataframe['ema_26'])
)
```

1小时RSI超买 + EMA12下穿EMA26（MACD死叉）。

### 4.7 卖出条件 #8：1小时布林带相对位置

```python
(
    (dataframe['close'] > dataframe['bb_upperband_1h'] * 1.1)
)
```

价格超过1小时布林上轨的110%。

### 4.8 多偏移MA卖出条件

```python
for i in self.ma_types:
    conditions.append(
        (
            (dataframe['close'] > dataframe[f'{i}_offset_sell']) &
            (dataframe['volume'] > 0)
        )
    )
```

当价格高于偏移均线（偏移系数 > 1）时触发卖出。

### 4.9 自定义利润卖出逻辑

策略还实现了复杂的自定义卖出逻辑(custom_sell)：

```python
def custom_sell(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    # 梯度止盈
    if (current_profit > 0.25) & (rsi < 50.0):
        return 'signal_profit_4'
    elif (current_profit > 0.08) & (rsi < 48.0):
        return 'signal_profit_3'
    elif (current_profit > 0.05) & (rsi < 43.0):
        return 'signal_profit_2'
    elif (current_profit > 0.03) & (rsi < 38.0):
        return 'signal_profit_1'
    elif (current_profit > 0.01) & (rsi < 33.0):
        return 'signal_profit_0'
    
    # EMA200下方止盈
    elif (current_profit > 0.02) & (close < ema_200) & (rsi < 56.0):
        return 'signal_profit_u_1'
    
    # 追踪止盈
    elif (current_profit > 0.15) & (current_profit < 0.46) & \
         (max_profit > current_profit + 0.18):
        return 'signal_profit_t_1'
```

**设计哲学**：
- 梯度止盈：利润越高，RSI阈值越宽松
- 弱势止盈：在EMA200下方时更积极止盈
- 追踪止盈：从高点回落时锁定利润

---

## 五、技术指标体系

### 5.1 核心指标一览

| 指标类别 | 具体指标 | 时间框架 | 用途 |
|---------|---------|---------|------|
| 趋势指标 | EMA(12,20,26,50,100,200) | 5m | 趋势方向和支撑阻力 |
| 趋势指标 | EMA(15,50,100,200) | 1h | 大趋势确认 |
| 趋势指标 | SMA(5,30,200) | 5m | 趋势验证 |
| 趋势指标 | SMA(200) | 1h | 长期趋势 |
| 波动率 | BB(20,2) | 5m/1h | 超买超卖 |
| 波动率 | BB(40,2) | 5m | 形态识别 |
| 动量指标 | RSI(14) | 5m/1h | 超买超卖 |
| 动量指标 | MFI | 5m | 资金流向 |
| 特殊指标 | EWO(50,200) | 5m | 波浪判断 |
| 特殊指标 | Chopiness(14) | 5m | 趋势强度 |

### 5.2 偏移均线系统详解

```python
# 计算公式
ma_offset_buy = MA(close, period) * low_offset  # 买入偏移
ma_offset_sell = MA(close, period) * high_offset  # 卖出偏移
```

| 均线类型 | 买入偏移 | 卖出偏移 | 特点 |
|---------|---------|---------|------|
| SMA | 0.919 | 1.047 | 简单稳定 |
| EMA | 0.983 | 1.059 | 反应敏捷 |
| TRIMA | 0.943 | 1.014 | 平滑稳定 |
| T3 | 0.975 | 1.072 | 超平滑 |
| KAMA | 0.962 | 1.081 | 自适应 |

---

## 六、保护机制详解

### 6.1 下跌保护 (safe_dips)

策略设计了三个级别的下跌保护：

```python
# 标准下跌保护
safe_dips = (
    ((open - close) / close < 0.02) &      # 单根K线跌幅<2%
    ((max_2 - close) / close < 0.14) &      # 2根K线最大跌幅<14%
    ((max_12 - close) / close < 0.32) &     # 12根K线最大跌幅<32%
    ((max_144 - close) / close < 0.5)       # 144根K线最大跌幅<50%
)

# 严格下跌保护 (safe_dips_strict)
# 阈值更紧：0.015, 0.06, 0.24, 0.4

# 宽松下跌保护 (safe_dips_loose)
# 阈值更宽：0.026, 0.24, 0.42, 0.66
```

**设计目的**：避免在暴跌过程中抄底，等待价格稳定后再入场。

### 6.2 暴涨保护 (safe_pump)

同样设计三个级别，覆盖24/36/48小时：

```python
# 24小时暴涨保护
safe_pump_24 = (
    ((max_24 - min_24) / min_24 < threshold) |  # 涨幅在阈值内
    ((max_24 - min_24) / pull_threshold > (close - min_24))  # 或已回调
)
```

| 级别 | 24h阈值 | 36h阈值 | 48h阈值 |
|------|---------|---------|---------|
| 标准 | 0.5/1.75 | 0.56/1.75 | 0.85/1.75 |
| 严格 | 0.4/2.2 | 0.56/2.0 | 0.68/2.0 |
| 宽松 | 0.66/1.7 | 0.7/1.7 | 1.3/1.4 |

### 6.3 追踪止损

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01        # 1%追踪距离
trailing_stop_positive_offset = 0.03  # 3%利润后启动
```

---

## 七、多时间框架协同

### 7.1 5分钟与1小时的配合

```
1小时时间框架
├── 趋势方向确认
│   ├── EMA50 > EMA200
│   ├── SMA200上涨趋势
│   └── EMA100 > EMA200
├── 暴涨保护
│   ├── safe_pump_24_1h
│   ├── safe_pump_36_1h
│   └── safe_pump_48_1h
└── RSI确认
    └── rsi_1h 范围过滤

5分钟时间框架
├── 精确入场点
│   ├── 布林带位置
│   ├── MA偏移价格
│   └── RSI超卖确认
└── 精确出场点
    ├── RSI超买
    ├── 布林上轨
    └── MA偏移卖出
```

### 7.2 时间框架协同示例

**买入条件#1的协同逻辑**：
1. 1小时：EMA50 > EMA200（确认大趋势向上）
2. 1小时：safe_pump_24（确认没有近期暴涨）
3. 5分钟：safe_dips_strict（确认没有过度下跌）
4. 5分钟：RSI < 36（确认短期超卖）
5. 5分钟：MFI < 26（确认资金流出见底）

---

## 八、策略优势与局限

### ✅ 优势

1. **多重入场机会**：26个买入条件覆盖多种市场环境
2. **完善的保护机制**：下跌保护和暴涨保护双保险
3. **多时间框架验证**：1小时趋势确认+5分钟精确入场
4. **多偏移MA系统**：5种均线类型提供多样化参考
5. **梯度止盈设计**：利润越高越积极锁定

### ⚠️ 局限

1. **复杂度高**：26个买入条件难以逐一优化
2. **计算量大**：需要300根K线启动数据
3. **参数众多**：超参数优化空间大但过拟合风险高
4. **依赖多重条件**：可能导致错过快速行情

---

## 九、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 上涨趋势 | 全开条件 | 利用所有买入机会 |
| 震荡上行 | 选择性开启 | 重点关注EWO和RSI条件 |
| 震荡市场 | 减少条件 | 使用严格保护 |
| 下跌趋势 | 谨慎使用 | 只用极端RSI条件 |

---

## 十、配置建议

### 10.1 交易对配置

```yaml
# 建议配置
pair_count: 40-80  # 交易对数量
stake_amount: unlimited
max_open_trades: 4-6
```

### 10.2 黑名单建议

```yaml
# 避免杠杆代币
exchange:
  pair_blacklist:
    - "*BULL*"
    - "*BEAR*"
    - "*UP*"
    - "*DOWN*"
```

### 10.3 关键配置

```yaml
timeframe: 5m
use_sell_signal: true
sell_profit_only: false
ignore_roi_if_buy_signal: true
```

---

## 十一、总结

NostalgiaForInfinityV5MultiOffsetAndHO2 是一个"全副武装"的量化交易策略。它的核心价值在于：

1. **全面覆盖**：26个买入条件覆盖各种市场环境
2. **多重保护**：下跌保护、暴涨保护、追踪止损三重保险
3. **多维度确认**：多时间框架、多指标、多均线系统
4. **灵活止盈**：梯度止盈、追踪止盈、信号止盈

对于有经验的量化交易者，这是一个值得深入研究和优化的策略框架。但同时也需要注意：
- 复杂度高带来的维护成本
- 参数过多可能导致的过拟合
- 在不同市场环境下需要针对性调整

> 策略源自 NostalgiaForInfinityV5 系列，融合 MultiOffsetLamboV0 系统，感谢原策略作者 iterativ 的贡献

---