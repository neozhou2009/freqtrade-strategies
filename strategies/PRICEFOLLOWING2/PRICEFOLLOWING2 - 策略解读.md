# PRICEFOLLOWING2 策略深度解读

> **策略编号**: #334 (465 个策略中的第 334 个)  
> **策略类型**: 均线交叉趋势跟踪 + 多重确认机制  
> **时间框架**: 15 分钟 (15m)

---

## 一、策略概览

PRICEFOLLOWING2 是 PRICEFOLLOWING 策略的升级版本，采用更长的时间框架（15 分钟）和更严格的买卖确认机制。策略在保留核心均线交叉逻辑的基础上，增加了价格与 Heikin Ashi 收盘价的关系判断以及 EMA 差值百分比过滤，提高了信号的可靠性。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 2 种模式，默认包含 EMA 差值百分比过滤 |
| **卖出条件** | 2 种模式，默认包含 3 重确认机制 |
| **保护机制** | 止损 -10% + 追踪止损机制 |
| **时间框架** | 主时间框架 15m + 信息时间框架 15m |
| **依赖库** | talib, qtpylib, numpy, pandas |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "60": 0.025,  # 60分钟后盈利2.5%退出
    "30": 0.03,   # 30分钟后盈利3%退出
    "0": 0.04     # 立即盈利4%退出
}

# 止损设置
stoploss = -0.1  # 固定止损10%

# 追踪止损
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.02      # 盈利2%后启动追踪
trailing_stop_positive_offset = 0.03  # 触发点3%
```

**设计思路**：
- 分时递减的 ROI 目标，鼓励短期盈利
- 追踪止损伤在盈利 3% 后启动，锁定利润
- 固定止损 10% 提供最后一道防线

### 2.2 订单类型配置

```python
order_types = {
    'buy': 'limit',           # 限价买入
    'sell': 'limit',          # 限价卖出
    'stoploss': 'limit',      # 限价止损
    'stoploss_on_exchange': False  # 止损不在交易所执行
}

order_time_in_force = {
    'buy': 'gtc',    # Good Till Cancelled
    'sell': 'gtc'
}
```

---

## 三、买入条件详解

### 3.1 可优化参数

策略提供多个可优化参数，支持 Hyperopt 超参数优化：

| 参数名称 | 类型 | 范围 | 默认值 | 说明 |
|---------|------|------|--------|------|
| `rsi_value` | Int | 1-50 | 30 | RSI 买入阈值 |
| `rsi_enabled` | Boolean | - | False | 是否启用 RSI 过滤 |
| `ema_pct` | Decimal | 0.0001-0.1 | 0.004 | EMA 差值百分比阈值 |

### 3.2 买入条件逻辑

#### 模式 1：RSI 过滤开启（rsi_enabled = True）
```python
条件 1: RSI < rsi_value (默认 < 30)
条件 2: EMA7 下穿 TEMA（交叉信号）
```

**逻辑说明**：
- RSI 低于阈值表示超卖状态
- EMA7 下穿 TEMA 表示短期趋势可能向上转换

#### 模式 2：RSI 过滤关闭（rsi_enabled = False，默认）
```python
条件 1: EMA7 下穿 TEMA（交叉信号）
条件 2: ((last_tema - last_ema7) / last_tema) < ema_pct (默认 0.004)
```

**逻辑说明**：
- EMA7 与 TEMA 的差值相对于 TEMA 的比例小于阈值
- 这要求两条均线足够接近，减少假突破

### 3.3 与 PRICEFOLLOWING 的区别

| 对比项 | PRICEFOLLOWING | PRICEFOLLOWING2 |
|-------|----------------|-----------------|
| 时间框架 | 5 分钟 | 15 分钟 |
| 买入条件（RSI关闭） | EMA 交叉 + TEMA 下降 | EMA 交叉 + EMA 差值百分比 |
| 卖出条件（RSI关闭） | 仅 EMA 交叉 | EMA 交叉 + 价格确认 + 百分比 |

---

## 四、卖出逻辑详解

### 4.1 可优化参数

| 参数名称 | 类型 | 范围 | 默认值 | 说明 |
|---------|------|------|--------|------|
| `sell_rsi_value` | Int | 25-100 | 70 | RSI 卖出阈值 |
| `sell_rsi_enabled` | Boolean | - | True | 是否启用 RSI 卖出过滤 |
| `ema_sell_pct` | Decimal | 0.0001-0.1 | 0.003 | EMA 差值卖出阈值 |

### 4.2 卖出条件逻辑

#### 模式 1：RSI 卖出过滤开启（sell_rsi_enabled = True，默认）
```python
条件 1: RSI < sell_rsi_value (默认 < 70)
条件 2: EMA7 上穿 TEMA
```

**逻辑说明**：
- RSI 条件确保在价格未过热时卖出
- EMA7 上穿 TEMA 表示短期动能转弱

#### 模式 2：RSI 卖出过滤关闭（sell_rsi_enabled = False）
```python
条件 1: EMA7 上穿 TEMA
条件 2: best_bid < ha_close（买一价低于 Heikin Ashi 收盘价）
条件 3: ((last_tema - last_ema7) / last_ema7) < ema_sell_pct
```

**逻辑说明**：
- 三个条件必须同时满足，形成严格的卖出确认
- best_bid < ha_close 表示当前价格低于平滑价格
- EMA 差值百分比确保趋势已确认反转

### 4.3 卖出信号对比

| 策略 | 条件数量 | 确认机制 |
|------|---------|---------|
| PRICEFOLLOWING | 1 个 | 仅 EMA 交叉 |
| PRICEFOLLOWING2 | 3 个 | EMA 交叉 + 价格确认 + 百分比 |

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| **均线类** | EMA7, EMA24, TEMA(7) | 趋势判断、交叉信号 |
| **动量类** | RSI, ADX | 超买超卖判断、趋势强度 |
| **趋势类** | MACD, SAR | 趋势确认、止损参考 |
| **K 线类** | Heikin Ashi | 平滑价格波动、价格确认 |
| **周期类** | Hilbert Transform (Sine) | 周期识别 |

### 5.2 信息时间框架指标（15m）

策略使用 15 分钟作为信息层，提供更高维度的趋势判断：

- **ETH/USDT 15m**: 以太坊趋势参考
- **BTC/USDT 15m**: 比特币趋势参考
- **RVN/USDT 15m**: 山寨币市场情绪参考

### 5.3 指标计算代码

```python
# 核心指标计算
dataframe['ema7'] = ta.EMA(dataframe, timeperiod=7)
dataframe['ema24'] = ta.EMA(dataframe, timeperiod=24)
dataframe['tema'] = ta.TEMA(dataframe, timeperiod=7)
dataframe['rsi'] = ta.RSI(dataframe)
dataframe['adx'] = ta.ADX(dataframe)
dataframe['sar'] = ta.SAR(dataframe)

# MACD
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']
dataframe['macdhist'] = macd['macdhist']

# Heikin Ashi
heikinashi = qtpylib.heikinashi(dataframe)
dataframe['ha_open'] = heikinashi['open']
dataframe['ha_close'] = heikinashi['close']

# Hilbert Transform
hilbert = ta.HT_SINE(dataframe)
dataframe['htsine'] = hilbert['sine']
dataframe['htleadsine'] = hilbert['leadsine']
```

---

## 六、风险管理特色

### 6.1 分层止盈系统

策略采用分级止盈机制，结合 ROI 表和追踪止损：

```
持仓时间    目标收益率    触发条件
────────────────────────────────
0 分钟      4%           立即生效
30 分钟     3%           时间衰减
60 分钟     2.5%         进一步衰减
盈利 3%    追踪止损启动   锁定利润
```

### 6.2 追踪止损机制

```python
trailing_stop = True                    # 启用追踪止损
trailing_only_offset_is_reached = True  # 仅在达到偏移后启动
trailing_stop_positive = 0.02           # 追踪距离 2%
trailing_stop_positive_offset = 0.03   # 触发点 3%
```

**工作原理**：
- 盈利达到 3% 后，追踪止损开始工作
- 止损线跟随最高价上移，距离为 2%
- 价格回撤超过 2% 时触发止损卖出

### 6.3 多重确认机制

PRICEFOLLOWING2 的卖出信号比 PRICEFOLLOWING 更严格：

```python
# 默认卖出需要三个条件同时满足
conditions.append(qtpylib.crossed_above(dataframe['ema7'], dataframe['tema']))
conditions.append(dataframe['best_bid'] < haclose)
conditions.append(((last_tema - last_ema7) / last_ema7) < self.ema_sell_pct.value)
```

---

## 七、策略优势与局限

### ✅ 优势

1. **信号更可靠**：多重确认机制减少假信号
2. **时间框架更长**：15 分钟框架过滤短期噪音
3. **价格确认**：Heikin Ashi 收盘价提供额外确认
4. **参数可优化**：支持 Hyperopt 超参数优化

### ⚠️ 局限

1. **入场机会更少**：多重确认导致信号频率降低
2. **滞后性更明显**：15 分钟框架反应更慢
3. **单一方向**：仅做多，无法做空获利
4. **信息层未充分利用**：定义了但未在策略逻辑中使用

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **趋势向上** | 默认配置（sell_rsi_enabled=True） | 多重确认减少假突破 |
| **震荡市场** | sell_rsi_enabled=False | 严格卖出条件减少频繁交易 |
| **快速波动** | 不推荐使用 | 信号滞后可能错过机会 |
| **慢牛市场** | 默认配置 | 追踪止损伤能吃到趋势 |

---

## 九、适用市场环境详解

PRICEFOLLOWING2 是一个中等复杂度的趋势跟踪策略，相比 PRICEFOLLOWING 更保守。基于其代码架构和逻辑设计，它最适合 **稳定趋势市场**，而在 **快速波动** 时表现不佳。

### 9.1 策略核心逻辑

- **时间框架升级**：15 分钟框架比 5 分钟更稳定，过滤短期噪音
- **多重确认**：卖出需要三个条件，比单一条件更可靠
- **价格参考**：Heikin Ashi 收盘价提供平滑的价格参考

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 **趋势向上** | ⭐⭐⭐⭐⭐ | 多重确认确保吃到趋势，追踪止损伤锁定利润 |
| 🔄 **震荡横盘** | ⭐⭐⭐☆☆ | 信号频率低，减少手续费损失 |
| 📉 **趋势向下** | ⭐⭐☆☆☆ | 仅做多，下跌市场无机会 |
| ⚡️ **剧烈波动** | ⭐⭐☆☆☆ | 信号滞后，可能错过快速机会 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| `rsi_enabled` | False | 默认关闭，使用百分比过滤 |
| `sell_rsi_enabled` | True | 开启 RSI 卖出过滤更稳健 |
| `ema_pct` | 0.003-0.005 | 根据交易对波动调整 |
| `stoploss` | -0.08 ~ -0.12 | 根据风险偏好调整 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

策略逻辑比 PRICEFOLLOWING 稍复杂，需要理解：
- EMA 差值百分比的计算和意义
- Heikin Ashi 的平滑原理
- 多重确认机制的协同作用

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 1-10 对 | 2GB | 4GB |
| 10-50 对 | 4GB | 8GB |
| 50+ 对 | 8GB | 16GB |

### 10.3 回测与实盘的差异

- 多重确认在回测中可能表现良好，但实盘中可能因延迟错过最佳点位
- 15 分钟框架信号较少，需要更长时间验证效果
- 订单簿数据（best_bid）在回测中可能不完整

### 10.4 手动交易者建议

如果想手动交易类似逻辑：
1. 使用 EMA7 和 TEMA(7) 作为主信号
2. 计算 EMA 差值百分比确认信号强度
3. 参考 Heikin Ashi 收盘价判断价格位置
4. 设置固定止损 8-10%
5. 盈利 3% 后开启追踪止损

---

## 十一、总结

**PRICEFOLLOWING2** 是 PRICEFOLLOWING 的保守升级版。它的核心价值在于：

1. **信号更可靠**：多重确认机制减少假信号，提高胜率
2. **框架更稳定**：15 分钟时间框架过滤短期噪音
3. **风控更完善**：追踪止损 + 多重确认双重保护
4. **适合趋势**：在明确趋势市场中能有效捕捉利润

对于量化交易者而言，这是一个比 PRICEFOLLOWING 更稳健的选择。信号频率虽然降低，但质量提高。适合那些宁愿少交易也要保证成功率的交易者。在稳定趋势市场中，该策略能够有效捕捉趋势利润；在震荡市场中，由于信号频率低，手续费损失也相对较少。

---