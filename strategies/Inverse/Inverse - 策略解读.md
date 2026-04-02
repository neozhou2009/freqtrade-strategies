# Inverse 策略解读

## 一、策略概述

Inverse 策略是一款基于逆费舍尔变换（Inverse Fisher Transform）的中长期趋势跟踪策略。该策略巧妙运用数学变换技术，将商品通道指数（CCI）转化为更具操作性的信号指标，结合多时间框架分析和 SSL 通道确认，构建了一套完整的趋势交易体系。

策略名称"Inverse"直接来源于其核心技术——逆费舍尔变换。这种数学变换能够将任意分布的数据映射到有限区间内，有效平滑噪声信号，同时保留关键的趋势转折特征。通过这一技术，策略成功地将复杂的震荡指标转化为清晰的买卖信号。

从设计理念来看，Inverse 策略属于典型的趋势跟踪与均值回归相结合的系统。它既捕捉中长期趋势的延续，又在超卖区域寻找反弹机会，实现了对市场双重机会的把握。策略的运行周期为 1 小时，配合 4 小时时间框架的趋势确认，适合中短线交易者使用。

## 二、理论基础

### 2.1 逆费舍尔变换原理

费舍尔变换（Fisher Transform）最初由 J.F. Ehlers 提出，是一种将任意概率分布转换为正态分布的数学方法。其计算公式为：

```
Fisher(x) = 0.5 * ln((1 + x) / (1 - x))
```

逆费舍尔变换则是费舍尔变换的逆过程，其公式为：

```
Inverse Fisher(x) = (exp(2x) - 1) / (exp(2x) + 1)
```

该变换的核心价值在于：它能将输入数据映射到 [-1, 1] 的有限区间内，同时增强输入数据在边界区域的响应灵敏度。当输入接近极值时，输出会产生更剧烈的变化，这正好满足了交易信号对拐点识别的需求。

策略中将逆费舍尔变换应用于 CCI 指标，处理步骤如下：

1. 计算 CCI 值（周期由参数 buy_fisher_length 决定，默认 31）
2. 对 CCI 进行缩放处理：`cci_scaled = 0.1 * (cci / 4)`
3. 计算加权移动平均：`wmacci = WMA(cci_scaled, 9)`
4. 应用逆费舍尔变换：`fisher_cci = (exp(2*wmacci) - 1) / (exp(2*wmacci) + 1)`

这种处理方式使得 Fisher CCI 指标具有以下优势：
- 数值范围固定在 [-1, 1]，便于设置统一阈值
- 平滑性更好，减少假信号
- 对极端值更敏感，能更快识别转折点

### 2.2 CCI 指标特性

商品通道指数（CCI）是由 Donald Lambert 开发的动量指标，用于衡量当前价格相对于历史平均价格的偏离程度。其计算公式为：

```
CCI = (Typical Price - SMA(TP, n)) / (0.015 * Mean Deviation)
```

其中：
- Typical Price = (High + Low + Close) / 3
- SMA(TP, n) = 典型价格的 n 周期简单移动平均
- Mean Deviation = 典型价格与其移动平均的绝对偏差均值

CCI 的传统解读是：
- CCI > +100：超买区域，可能回调
- CCI < -100：超卖区域，可能反弹
- CCI 在 ±100 之间：正常波动区间

策略选择 CCI 作为基础指标的原因：
1. CCI 没有上限限制，能更真实反映极端行情
2. CCI 对趋势变化反应迅速
3. 经过逆费舍尔变换后，CCI 的超买超卖特征更加明显

### 2.3 SSL 通道原理

SSL（SSL Channels）是一种趋势判断指标，通过计算价格的上下通道来判断市场方向。策略中的 SSL 通道实现方式如下：

```python
def SSLChannels(self, dataframe, length = 7):
    df['ATR'] = ATR(dataframe, 14)
    df['smaHigh'] = df['high'].rolling(length).mean() + df['ATR']
    df['smaLow'] = df['low'].rolling(length).mean() - df['ATR']
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, 
                         np.where(df['close'] < df['smaLow'], -1, np.NAN))
    df['hlv'] = df['hlv'].ffill()
    df['sslDown'] = np.where(df['hlv'] < 0, df['smaHigh'], df['smaLow'])
    df['sslUp'] = np.where(df['hlv'] < 0, df['smaLow'], df['smaHigh'])
    return df['sslDown'], df['sslUp']
```

SSL 通道的核心逻辑：
1. 计算 SMA 高低通道：基于价格均值 ± ATR 波动幅度
2. 判断趋势状态：收盘价突破上轨为多头（hlv=1），跌破下轨为空头（hlv=-1）
3. 趋势状态延续：使用前向填充保持趋势状态直到下次突破
4. 生成上下轨：根据趋势状态动态切换上下轨位置

SSL 通道的优势在于结合了趋势判断和波动率适应，能够有效过滤震荡市场的假信号。

## 三、策略架构

### 3.1 时间框架设计

策略采用双时间框架架构：

**主时间框架（1小时）**
- 用于生成买卖信号
- 计算细粒度的 Fisher CCI 指标
- 执行入场和出场操作

**信息时间框架（4小时）**
- 用于趋势方向确认
- 计算 SSL 通道和 EMA 均线
- 提供更高层级的市场背景

这种设计的优势在于：
1. 利用 4 小时级别的趋势稳定性，避免逆势交易
2. 在 1 小时级别寻找精确入场点，提高交易效率
3. 当两个时间框架趋势一致时，交易胜率显著提升

### 3.2 参数体系

策略使用 Hyperopt 可优化参数系统，主要参数如下：

**买入参数**
| 参数名 | 默认值 | 优化范围 | 说明 |
|--------|--------|----------|------|
| buy_fisher_length | 31 | [13, 55] | Fisher CCI 计算周期 |
| buy_fisher_cci_1 | -0.42 | [-0.6, -0.3] | 主入场阈值 |
| buy_fisher_cci_2 | 0.41 | [0.3, 0.6] | 次入场阈值 |

**卖出参数**
| 参数名 | 默认值 | 优化范围 | 说明 |
|--------|--------|----------|------|
| sell_fisher_cci_1 | 0.42 | [0.3, 0.6] | 主出场阈值 |
| sell_fisher_cci_2 | -0.34 | [-0.6, -0.3] | 次出场阈值 |

**止损止盈参数**
| 参数 | 值 | 说明 |
|------|-----|------|
| stoploss | -0.2 | 固定止损 20% |
| trailing_stop | True | 启用追踪止损 |
| trailing_stop_positive | 0.078 | 盈利 7.8% 后启动追踪 |
| trailing_stop_positive_offset | 0.174 | 追踪止损起始偏移 17.4% |
| minimal_roi | {"0": 0.10, "30": 0.05, "60": 0.02} | 分阶段止盈 |

### 3.3 指标计算流程

策略的指标计算分为两部分：

**信息时间框架指标（4小时）**
```python
def informative_indicators(self, dataframe, metadata):
    # EMA 均线系统
    informative_p['ema_50'] = ta.EMA(informative_p, timeperiod=50)
    informative_p['ema_100'] = ta.EMA(informative_p, timeperiod=100)
    informative_p['ema_200'] = ta.EMA(informative_p, timeperiod=200)
    
    # SSL 通道
    ssl_down, ssl_up = self.SSLChannels(informative_p, 20)
    informative_p['ssl_down'] = ssl_down
    informative_p['ssl_up'] = ssl_up
```

**主时间框架指标（1小时）**
```python
def normal_tf_indicators(self, dataframe, metadata):
    # Fisher CCI 计算
    for cci_length in self.buy_fisher_length.range:
        dataframe[f'cci'] = ta.CCI(dataframe, timeperiod=cci_length)
        cci = 0.1 * (dataframe[f'cci'] / 4)
        wmacci = ta.WMA(cci, timeperiod=9)
        dataframe[f'fisher_cci_{cci_length}'] = (numpy.exp(2 * wmacci) - 1) / (numpy.exp(2 * wmacci) + 1)
    
    # 趋势确认指标
    dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
    dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)
    dataframe['adx'] = ta.ADX(dataframe, timeperiod=3)
    dataframe['di_up'] = ta.PLUS_DI(dataframe, timeperiod=3) > ta.MINUS_DI(dataframe, timeperiod=3)
```

## 四、入场逻辑

### 4.1 入场条件详解

策略的入场逻辑采用复合条件设计，必须同时满足以下所有条件：

**条件组一：Fisher CCI 信号**
```python
(qtpylib.crossed_above(dataframe[f'fisher_cci_{self.buy_fisher_length.value}'], self.buy_fisher_cci_1.value))
|
(
    (qtpylib.crossed_below(dataframe[f'fisher_cci_{self.buy_fisher_length.value}'], self.buy_fisher_cci_2.value).rolling(8).max() == 1) &
    (qtpylib.crossed_above(dataframe[f'fisher_cci_{self.buy_fisher_length.value}'], self.buy_fisher_cci_2.value))
)
```

这包含两种入场场景：

**场景 A：超卖反弹入场**
- Fisher CCI 上穿 -0.42 阈值
- 这是最直接的入场信号，捕捉从超卖区域的反弹

**场景 B：趋势确认入场**
- Fisher CCI 最近 8 根 K 线内曾下穿 0.41
- 当前 Fisher CCI 上穿 0.41
- 这种设计捕捉趋势延续中的回调入场机会

**条件组二：多时间框架趋势确认**
```python
(dataframe[f'ssl_up_{self.info_timeframe}'] > dataframe[f'ssl_down_{self.info_timeframe}']) &
(dataframe['ema_50'] > dataframe['ema_200']) &
(dataframe[f'ema_50_{self.info_timeframe}'] > dataframe[f'ema_100_{self.info_timeframe}']) &
(dataframe[f'ema_50_{self.info_timeframe}'] > dataframe[f'ema_200_{self.info_timeframe}'])
```

这包含四个必须同时满足的趋势条件：

1. **4小时 SSL 通道多头**：ssl_up > ssl_down，确认中期趋势向上
2. **1小时 EMA 多头排列**：EMA50 > EMA200，确认短期趋势向上
3. **4小时 EMA 多头排列（一）**：EMA50 > EMA100，确认中期动能
4. **4小时 EMA 多头排列（二）**：EMA50 > EMA200，确认中期趋势

**条件组三：成交量过滤**
```python
(dataframe['volume'] > 0)
```

确保市场有足够的流动性。

### 4.2 入场逻辑图解

```
┌─────────────────────────────────────────────────────────────┐
│                      入场信号判断流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────┐                                     │
│  │ Fisher CCI 信号   │                                     │
│  │                   │                                     │
│  │ 场景A: 上穿-0.42  │                                     │
│  │ 场景B: 上穿0.41   │                                     │
│  │       (8根内曾下穿)│                                     │
│  └─────────┬─────────┘                                     │
│            │ 满足任一                                      │
│            ▼                                               │
│  ┌───────────────────┐                                     │
│  │ 4小时趋势确认     │                                     │
│  │                   │                                     │
│  │ SSL通道: 上>下    │                                     │
│  │ EMA50>EMA100      │                                     │
│  │ EMA50>EMA200      │                                     │
│  └─────────┬─────────┘                                     │
│            │ 全部满足                                       │
│            ▼                                               │
│  ┌───────────────────┐                                     │
│  │ 1小时趋势确认     │                                     │
│  │                   │                                     │
│  │ EMA50 > EMA200    │                                     │
│  └─────────┬─────────┘                                     │
│            │ 满足                                          │
│            ▼                                               │
│  ┌───────────────────┐                                     │
│  │ 成交量 > 0        │                                     │
│  └─────────┬─────────┘                                     │
│            │ 满足                                          │
│            ▼                                               │
│      ✅ 生成买入信号                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 五、出场逻辑

### 5.1 卖出信号条件

策略的出场逻辑相对简洁，主要依赖 Fisher CCI 指标的拐点信号：

```python
def populate_exit_trend(self, dataframe, metadata):
    dataframe.loc[
        (
            (qtpylib.crossed_below(dataframe[f'fisher_cci_{self.buy_fisher_length.value}'], self.sell_fisher_cci_1.value)) 
            | (qtpylib.crossed_below(dataframe[f'fisher_cci_{self.buy_fisher_length.value}'], self.sell_fisher_cci_2.value))    
        ) &
        (dataframe['volume'] > 0)
    ), 'sell'] = 1
```

卖出条件包含两种情况：

**情况一：高位反转卖出**
- Fisher CCI 下穿 0.42
- 捕捉从超买区域的趋势反转

**情况二：趋势减弱卖出**
- Fisher CCI 下穿 -0.34
- 在多头趋势明显减弱时离场

### 5.2 退出确认机制

策略实现了 `confirm_trade_exit` 方法，对卖出信号进行二次确认：

```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, current_time, **kwargs):
    dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    last_candle = dataframe.iloc[-1]
    previous_candle_1 = dataframe.iloc[-2]

    if (last_candle is not None):
        if (sell_reason in ['sell_signal']):
            if last_candle['di_up'] and (last_candle['adx'] > previous_candle_1['adx']):
                return False
    return True
```

**退出确认逻辑：**
- 仅针对 sell_signal 触发的卖出进行过滤
- 如果当前 DI+ > DI-（多头动能占优）且 ADX 上升（趋势强度增加）
- 则阻止卖出，继续持仓

这是一个防止在强势趋势中被洗出场的保护机制。

### 5.3 止损止盈机制

**固定止损**
- 止损比例：-20%
- 当亏损达到 20% 时自动平仓

**追踪止损**
```python
trailing_stop = True
trailing_stop_positive = 0.078
trailing_stop_positive_offset = 0.174
trailing_only_offset_is_reached = False
```

追踪止损逻辑：
1. 当盈利达到 7.8% 时，启动追踪止损
2. 止损线从最高点回撤固定比例
3. `trailing_only_offset_is_reached = False` 表示立即开始追踪，不需要等待达到偏移值

**分阶段止盈（ROI）**
```python
minimal_roi = {
    "0": 0.10,    # 开仓后立即生效：10% 目标
    "30": 0.05,   # 30分钟后：5% 目标
    "60": 0.02    # 60分钟后：2% 目标
}
```

ROI 机制解读：
- 开仓后，止盈目标为 10%
- 持仓 30 分钟后，止盈目标降为 5%（获利了结倾向）
- 持仓 60 分钟后，止盈目标降为 2%（快速平仓倾向）

这种设计鼓励快速盈利了结，避免长时间持仓的风险。

## 六、风险控制体系

### 6.1 多层风控架构

策略构建了完整的多层风险控制体系：

**第一层：信号过滤**
- Fisher CCI 阈值过滤，避免噪音信号
- 趋势确认过滤，避免逆势交易
- 成交量过滤，确保流动性

**第二层：趋势确认**
- 双时间框架趋势一致性验证
- 多维度均线系统确认
- SSL 通道方向确认

**第三层：持仓管理**
- 固定止损保护本金
- 追踪止损锁定利润
- 分阶段止盈控制风险敞口

**第四层：退出确认**
- ADX/DI 趋势强度过滤
- 防止在强势趋势中被洗出场

### 6.2 风控参数分析

| 风控类型 | 参数值 | 风险等级 | 作用机制 |
|----------|--------|----------|----------|
| 固定止损 | -20% | 中高 | 保护本金，防止单笔大亏 |
| 追踪启动 | 7.8% | 低 | 利润达到一定程度后保护 |
| 追踪偏移 | 17.4% | 低 | 确保有足够利润缓冲 |
| ROI 第一阶段 | 10% | 低 | 快速获利了结 |
| ROI 第二阶段 | 5% | 中 | 持仓 30 分钟后降低预期 |
| ROI 第三阶段 | 2% | 中 | 持仓 60 分钟后快速出场 |

### 6.3 市场适应性分析

**适合的市场环境：**
- 明显的单边趋势市场
- 波动率适中的交易品种
- 流动性充足的交易对

**不适合的市场环境：**
- 剧烈震荡的盘整市场
- 低流动性的小币种
- 极端行情（暴涨暴跌）

**原因分析：**
1. 趋势跟踪系统在震荡市场容易频繁止损
2. EMA 均线系统在极端行情中滞后严重
3. Fisher CCI 在极端波动时可能失真

## 七、参数优化空间

### 7.1 可优化参数

策略提供了丰富的 Hyperopt 可优化参数：

**买入参数范围**
- `buy_fisher_length`：[13, 55]，影响 Fisher CCI 的敏感度
- `buy_fisher_cci_1`：[-0.6, -0.3]，控制超卖入场阈值
- `buy_fisher_cci_2`：[0.3, 0.6]，控制趋势回调入场阈值

**卖出参数范围**
- `sell_fisher_cci_1`：[0.3, 0.6]，控制超买出场阈值
- `sell_fisher_cci_2`：[-0.6, -0.3]，控制趋势减弱出场阈值

### 7.2 参数优化策略

**Fisher Length 优化**
- 较小值（13-20）：信号更灵敏，适合快速市场
- 较大值（40-55）：信号更稳定，适合趋势市场
- 建议根据回测结果选择最优值

**CCI 阈值优化**
- 入场阈值越接近 0，信号越多，假信号也越多
- 入场阈值越接近极值，信号越少，质量越高
- 建议通过 Hyperopt 寻找平衡点

**止损止盈优化**
- 当前止损 -20% 较为激进
- 可根据交易品种波动率调整
- 追踪止损参数可通过回测优化

### 7.3 优化建议

1. **数据准备**
   - 确保至少 6 个月的历史数据
   - 包含不同市场状态（牛市、熊市、震荡）
   - 避免过度拟合单一市场环境

2. **优化方法**
   - 使用 Hyperopt 的 Sharpe Ratio 作为目标
   - 设置合理的参数边界
   - 进行样本外测试验证

3. **验证指标**
   - 最大回撤控制在可接受范围
   - 胜率与盈亏比平衡
   - 年化收益率与风险匹配

## 八、实盘应用建议

### 8.1 部署准备

**环境配置**
```python
# 推荐配置
timeframe = '1h'
startup_candle_count = 200
process_only_new_candles = True  # 建议开启
```

**交易对选择**
- 选择流动性充足的主流交易对
- 避免新币种和低市值币种
- 优先选择趋势性强的品种

**资金管理**
- 单笔交易风险控制在总资金的 2-5%
- 设置最大持仓数量限制
- 预留足够的保证金应对波动

### 8.2 监控指标

**核心监控项**
1. Fisher CCI 指标值变化
2. SSL 通道状态切换
3. EMA 均线排列状态
4. ADX/DI 趋势强度

**异常预警**
- 连续止损次数
- 单日最大回撤
- 信号频率异常

### 8.3 风险提示

1. **趋势失效风险**
   - 在趋势转折点可能产生连续亏损
   - 建议设置连续亏损后的熔断机制

2. **滑点风险**
   - 策略使用限价单买入
   - 在快速行情中可能无法成交

3. **参数失效风险**
   - 市场状态变化后优化参数可能失效
   - 建议定期重新优化参数

## 九、策略优势与局限

### 9.1 策略优势

**技术优势**
1. **指标创新**：逆费舍尔变换提升了信号质量
2. **多时间框架**：利用 4 小时确认趋势，降低假信号
3. **复合条件**：多重过滤条件提高信号可靠性
4. **动态风控**：追踪止损和分阶段止盈

**实践优势**
1. **参数可优化**：所有关键参数都支持 Hyperopt
2. **逻辑清晰**：入场出场规则明确，易于理解和维护
3. **可视化友好**：提供 plot_config 配置，便于分析
4. **计算效率高**：指标计算量适中，适合实时交易

### 9.2 策略局限

**技术局限**
1. **趋势依赖**：在震荡市场表现不佳
2. **滞后性**：EMA 系统存在固有滞后
3. **参数敏感**：不同市场环境需要不同参数
4. **单一指标**：主要依赖 Fisher CCI，缺乏多指标验证

**实践局限**
1. **止损较大**：20% 止损可能超出部分交易者承受能力
2. **追踪止损激进**：启动阈值 7.8% 可能过早锁定利润
3. **出场简单**：出场条件相对入场较为简单
4. **缺乏加仓机制**：没有利用趋势优势加仓

## 十、改进方向

### 10.1 指标层面改进

**增加辅助指标**
```python
# 建议添加
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
dataframe['macd'] = ta.MACD(dataframe)
dataframe['bb_upperband'] = ta.BBANDS(dataframe, timeperiod=20)['upperband']
```

增加多指标验证可以提高信号可靠性。

**优化 Fisher 变换**
```python
# 当前使用 WMA 平滑
wmacci = ta.WMA(cci, timeperiod=9)

# 可考虑使用 EMA 或 ALMA
wmacci = ta.EMA(cci, timeperiod=9)
```

### 10.2 逻辑层面改进

**增强出场逻辑**
- 添加 RSI 背离检测
- 添加 MACD 死叉确认
- 添加价格形态识别

**改进止损机制**
```python
# 建议实现 ATR 动态止损
dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
stoploss = -2 * dataframe['atr'] / dataframe['close']
```

**添加仓位管理**
```python
# 根据 ADX 强度调整仓位
position_size = base_size * (adx / 25)  # ADX 越强，仓位越大
```

### 10.3 执行层面改进

**订单类型优化**
```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': True  # 建议开启交易所止损
}
```

**添加时间过滤**
```python
# 避免低流动性时段交易
if current_time.hour in [0, 1, 2, 3, 4]:
    return False
```

## 十一、总结

Inverse 策略是一款设计精良的趋势跟踪策略，其核心创新在于将逆费舍尔变换应用于 CCI 指标，有效提升了信号质量。策略通过多时间框架分析和复合过滤条件，在保持信号准确率的同时，实现了对趋势行情的有效捕捉。

策略的主要价值在于：
1. **数学理论基础扎实**：逆费舍尔变换有明确的数学意义
2. **风险控制完善**：多层风控保护本金和利润
3. **可优化性强**：参数体系支持 Hyperopt 自动优化
4. **实盘可用性高**：逻辑清晰，计算高效

策略的主要风险在于对趋势市场的依赖，在震荡行情中可能产生较多假信号。建议交易者：
1. 选择趋势性强的交易对
2. 根据市场环境调整参数
3. 严格控制单笔风险
4. 定期监控和优化策略

总体而言，Inverse 策略为量化交易者提供了一个可靠的框架，通过适当的优化和改进，可以进一步提升其在不同市场环境下的表现。