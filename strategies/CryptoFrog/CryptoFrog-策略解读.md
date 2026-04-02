# CryptoFrog 策略深度解读

> **策略编号**: #133 (465 个策略中的第 133 个)  
> **策略类型**: 平滑 Heiken Ashi + 布林带扩张 + 动态 ROI/止损  
> **时间框架**: 5 分钟 (5m) + 1 小时信息层

---

## 一、策略概览

**CryptoFrog** 是一个复杂的多条件买入策略，由社区开发者创建并分享。该策略融合了多种技术指标，包括平滑 Heiken Ashi、布朗带扩张、随机 RSI、DMI、VFI 等，构建了一套独特的趋势跟踪与波动率捕捉系统。策略的核心特点在于使用自定义的线性衰减止损和动态 ROI 系统。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 多重条件组合（基于 Heiken Ashi、BB 扩张、随机 RSI、DMI） |
| **卖出条件** | 多重条件组合（基于 Heiken Ashi、BB 扩张、MFI、DMI） |
| **保护机制** | 线性衰减自定义止损 + 动态 ROI + 追踪止损 |
| **时间框架** | 5 分钟 + 1 小时信息层 |
| **依赖库** | TA-Lib, finta, technical (qtpylib) |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.213,      # 0-39 分钟：21.3% 利润
    "39": 0.103,     # 39-96 分钟：10.3% 利润
    "96": 0.037,     # 96-166 分钟：3.7% 利润
    "166": 0         # 166 分钟后：自由退出
}

# 止损设置
stoploss = -0.085   # -8.5% 起始止损（由自定义线性衰减接管）

# 追踪止损
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.047
trailing_only_offset_is_reached = False
```

**设计思路**：
- **激进 ROI**：首目标 21.3%，是 Freqtrade 策略中较高的设定之一
- **阶梯式退出**：从 21.3% → 10.3% → 3.7% 逐级降低
- **线性衰减止损**：从 -8.5% 起始，在 166 分钟内线性衰减至 -2%

### 2.2 自定义止损参数

```python
custom_stop = {
    # 线性衰减参数
    'decay-time': 166,           # 衰减时间（分钟）
    'decay-delay': 0,            # 延迟开始时间
    'decay-start': -0.085,       # 起始止损
    'decay-end': -0.02,          # 终止止损
    
    # 利润与动量
    'cur-min-diff': 0.03,        # 当前与最小利润差值
    'cur-threshold': -0.02,      # 考虑移动止损的阈值
    'roc-bail': -0.03,           # ROC 动态退出值
    'rmi-trend': 50,             # RMI 趋势阈值
    
    # 正向追踪
    'pos-trail': True,           # 启用正向追踪
    'pos-threshold': 0.005,     # 触发追踪的利润阈值
    'pos-trail-dist': 0.015      # 追踪距离
}
```

---

## 三、买入条件详解

### 3.1 核心买入逻辑

CryptoFrog 的买入信号是一个复杂的多层过滤系统：

```
买入信号 = (价格条件) & (信息层条件) & (多个备选条件组合) & (成交量条件)
```

#### 3.1.1 价格条件层

```python
# 收盘价必须低于 5 分钟平滑 Heiken Ashi 低点
(dataframe['close'] < dataframe['Smooth_HA_L'])
```

#### 3.1.2 信息层条件

```python
# 1 小时 Hansen HA EMA 确认趋势
(dataframe['emac_1h'] < dataframe['emao_1h'])
```

### 3.2 备选买入条件（三种模式）

策略提供三种独立的买入模式，通过 `|` 连接，只要满足任一模式即可：

#### 模式 A：BB 扩张 + 动量过滤

```python
# 布林带扩张 + 布林带挤压结束
(dataframe['bbw_expansion'] == 1) & (dataframe['sqzmi'] == False)
& (
    (dataframe['mfi'] < 20)  # MFI 超卖
    |
    (dataframe['dmi_minus'] > 30)  # DMI- 强劲
)
```

#### 模式 B：SAR + 随机 RSI 超卖

```python
# 价格低于 SAR
(dataframe['close'] < dataframe['sar'])
& ((dataframe['srsi_d'] >= dataframe['srsi_k']) & (dataframe['srsi_d'] < 30))
& ((dataframe['fastd'] > dataframe['fastk']) & (dataframe['fastd'] < 23))
& (dataframe['mfi'] < 30)
```

#### 模式 C：DMI 交叉 + 布林带底

```python
# DMI- 上穿 DMI+
((dataframe['dmi_minus'] > 30) & qtpylib.crossed_above(dataframe['dmi_minus'], dataframe['dmi_plus']))
& (dataframe['close'] < dataframe['bb_lowerband'])
# 或
# SQZMI 挤压模式
(dataframe['sqzmi'] == True)
& ((dataframe['fastd'] > dataframe['fastk']) & (dataframe['fastd'] < 20))
```

### 3.3 成交量过滤

```python
# VFI 为负且有成交量
(dataframe['vfi'] < 0.0) & (dataframe['volume'] > 0)
```

---

## 四、卖出逻辑详解

### 4.1 核心卖出逻辑

```python
# 收盘价高于 Heiken Ashi 高点
(dataframe['close'] > dataframe['Smooth_HA_H'])
& # 1 小时 Hansen HA EMA 确认
(dataframe['emac_1h'] > dataframe['emao_1h'])
& # BB 扩张 + MFI/DMI 超买
(
    (dataframe['bbw_expansion'] == 1)
    &
    (
        (dataframe['mfi'] > 80)
        |
        (dataframe['dmi_plus'] > 30)
    )
)
& # 成交量确认
(dataframe['vfi'] > 0.0) & (dataframe['volume'] > 0)
```

### 4.2 动态 ROI 系统

策略实现了 `min_roi_reached_dynamic` 函数，根据市场趋势动态调整 ROI：

```python
# 趋势检测
droi_trend_type = ['rmi', 'ssl', 'candle', 'any']  # 可配置

# 趋势判断逻辑
- RMI 趋势：rmi-up-trend == 1
- SSL 趋势：ssl-dir == 'up'
- K线趋势：candle-up-trend == 1

# 在趋势中：允许利润更高时才退出
# 回撤时：根据 pullback_value 允许提前退出
```

### 4.3 自定义止损逻辑

```python
def custom_stoploss(...):
    # 如果利润低于阈值
    if current_profit < cstp_threshold.value:
        # ROC 模式
        if cstp_bail_how in ('roc', 'any'):
            if (sroc/100) <= cstp_bail_roc.value:
                return 0.001  # 立即退出
        
        # 时间模式
        if cstp_bail_how in ('time', 'any'):
            if trade_dur > cstp_bail_time.value:
                return 0.001  # 立即退出
```

---

## 五、技术指标体系

### 5.1 核心自定义指标

| 指标名称 | 计算方法 | 用途 |
|---------|---------|------|
| **Smoothed HA** | Heiken Ashi 平滑 (EMA 4) | 过滤市场噪音，确认价格位置 |
| **Hansen HA EMA** | 基于 6 周期 HA 的 SMA | 1 小时趋势确认 |
| **BB 扩张** | 布林带宽度突破 4 周期最高值的 1.1 倍 | 波动率爆发信号 |
| **SQZMI** | 布林带挤压指标 (finta) | 静默期检测 |
| **VFI** | Volume Flow Indicator | 资金流向确认 |
| **RMI** | Relative Momentum Index | 动量趋势判断 |
| **SROC** | Smoothed Rate of Change | 平滑变化率 |

### 5.2 标准技术指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **趋势指标** | EMA, SMA | 多周期 | 趋势判断 |
| **动量指标** | RSI, 随机 RSI, RMI | 14/24 周期 | 超买超卖 |
| **波动指标** | 布林带 | 20,1 | 支撑阻力 |
| **趋势指标** | DMI/ADX | 14 周期 | 趋势强度 |
| **成交量** | VFI, MFI | - | 资金流向 |

### 5.3 信息时间框架指标（1 小时）

- Hansen HA EMA (emac_1h, emao_1h)
- 其他指标通过 merge_informative_pair 合并

---

## 六、风险管理特色

### 6.1 线性衰减止损

这是 CryptoFrog 最独特的风控机制：

```
时间轴（分钟）：0 ---- 166 ---->
止损值：     -8.5% ----> -2%
```

**工作原理**：
- 开仓后立即应用 -8.5% 止损
- 随着时间推移，止损线逐渐向 0 移动
- 166 分钟后，止损线稳定在 -2%
- 这样既保护本金，又给亏损仓位更多反弹机会

### 6.2 动态 ROI

| 条件 | ROI 行为 |
|------|---------|
| **趋势中** | 忽略 ROI 表，持续持有直到趋势结束 |
| **回撤时** | 当利润从高点回落到 pullback_value 时，卖出的一半仓位 |
| **震荡市** | 回退到标准 ROI 表 |

### 6.3 正向追踪止损

当盈利超过 0.5% 时启动：
- 追踪止损设置在当前价格下方 1.5%
- 只在盈利时启用，保护利润

---

## 七、策略优势与局限

### ✅ 优势

1. **独特指标组合**：平滑 HA + Hansen HA EMA 提供独特的趋势视角
2. **波动率捕捉**：BB 扩张检测能在波动爆发前入场
3. **线性衰减止损**：给予亏损仓位更多时间恢复
4. **动态 ROI**：趋势中不停盈，让利润奔跑
5. **多模式买入**：三种独立模式，覆盖更多场景

### ⚠️ 局限

1. **参数众多**：自定义参数超过 20 个，优化难度大
2. **计算密集**：多指标 + 多时间框架，VPS 压力大
3. **激进 ROI**：21.3% 首目标在低波动市场难以达到
4. **复杂逻辑**：自定义止损和动态 ROI 需要深入理解

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **高波动币种** | 保持默认参数 | 21.3% 目标适合大幅波动 |
| **主流币稳健** | 降低 ROI 目标 | 调整到 10-15% |
| **趋势明确行情** | 启用动态 ROI | 让利润奔跑 |
| **震荡行情** | 调整 decay-end | 更激进的止损 |

---

## 九、适用市场环境详解

CryptoFrog 是一个高度专业化的策略，最适合**高波动、强趋势**市场。

### 9.1 策略核心逻辑

- **趋势确认**：1 小时 Hansen HA EMA 确保顺势交易
- **波动率过滤**：BB 扩张确保在波动爆发时入场
- **动量验证**：随机 RSI、DMI、SRSI 多重过滤假信号
- **买入逻辑**：价格低于 HA 低点 + 多种超卖条件

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 强上涨趋势 | ⭐⭐⭐⭐⭐ | 多重趋势确认 + 动态 ROI 能抓住大波段 |
| 📉 下跌趋势 | ⭐⭐⭐ | 买入条件偏多，可能逆势入场 |
| 🔄 宽幅震荡 | ⭐⭐⭐⭐ | BB 扩张能捕捉波动转折点 |
| ⚡️ 快速波动 | ⭐⭐⭐⭐⭐ | 21.3% 目标 + 波动率检测 |
| 📊 横盘整理 | ⭐⭐ | 条件复杂，可能长时间无信号 |

### 9.3 关键配置建议

| 配置项 | 默认值 | 建议 | 说明 |
|--------|--------|------|------|
| minimal_roi."0" | 0.213 | 0.10-0.20 | 根据波动率调整 |
| decay-time | 166 | 120-240 | 根据持仓习惯调整 |
| decay-end | -0.02 | -0.03~ -0.01 | 更保守的止损 |
| droi_trend_type | any | rmi | 更严格的趋势判断 |

---

## 十、重要提醒：复杂策略的代价

### 10.1 学习成本

CryptoFrog 代码量约 400 行，包含多种自定义指标和复杂的退出逻辑。新手建议先理解核心指标（HA、BB 扩张、RMI），再逐步深入自定义止损和动态 ROI。

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 10-20 对 | 2GB | 4GB |
| 20-50 对 | 4GB | 8GB |
| 50+ 对 | 8GB | 16GB |

### 10.3 回测与实盘的差异

- 线性衰减止损在回测中可能表现较好，实盘中滑点更大
- 动态 ROI 在趋势明显的品种上表现优异
- 多时间框架策略在实盘中可能有信号延迟

### 10.4 手动交易者建议

建议手动交易者关注以下核心信号：
- **BB 扩张 + MFI < 20**：波动爆发 + 资金流出
- **价格 < SAR + 随机 RSI 超卖**：技术性超卖反弹
- **DMI- 上穿 DMI+**：动量转换

---

## 十一、总结

**CryptoFrog** 是一个高度专业化的趋势跟踪策略，核心价值在于：

1. **独特视角**：平滑 Heiken Ashi 提供清晰的价格结构
2. **波动率检测**：BB 扩张指标捕捉波动爆发点
3. **智能风控**：线性衰减止损 + 动态 ROI
4. **多模式覆盖**：三种买入模式适应不同场景

对于量化交易者而言，CryptoFrog 适合有一定 Freqtrade 使用经验且追求专业级策略的投资者。建议从默认参数开始，小资金实盘验证，再根据具体交易对和市场环境进行微调。

**使用建议**：该策略设计初衷是为高波动市场设计的，在使用时注意选择波动性较高的交易对，并确保 VPS 有足够的计算资源。

---

**文档版本**: v1.0  
**策略作者**: 社区贡献  
**最后更新**: 2024