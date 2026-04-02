# Dracula 策略深度解读

> **策略编号**: #151 (465 个策略中的第 151 个)  
> **策略类型**: 布林带支撑阻力 + 资金流多条件策略  
> **时间框架**: 1 分钟 (1m) + 5 分钟信息层

---

## 一、策略概览

**Dracula** 是一个复杂的多条件买入策略，由作者 6h057 开发。策略核心逻辑基于布林带支撑/阻力位识别、Chaikin Money Flow (CMF) 资金流指标以及EMA趋势判断，在价格触及布林带下轨且资金流入时买入。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 2 个独立买入信号组 |
| **卖出条件** | 5 个自定义卖出信号（通过 custom_exit 实现） |
| **保护机制** | 1 组买入保护参数（止损保护） |
| **时间框架** | 1 分钟（主）+ 5 分钟（信息层） |
| **依赖库** | TA-Lib, ta, numpy |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表（时间：分钟）
minimal_roi = {
    "0": 0.10,     # 立即退出：10% 利润
    "30": 0.05,    # 30 分钟后：5% 利润
    "60": 0.02     # 60 分钟后：2% 利润
}

# 止损设置
stoploss = -0.20   # -20% 硬止损

# 追踪止损
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01        # 1% 追踪启动点
trailing_stop_positive_offset = 0.03  # 3% 偏移触发
```

**设计思路**：
- **高首级 ROI**：10% 的首级 ROI 表明策略预期捕捉较大波动
- **中等止损**：-20% 的硬止损给予交易适度波动空间
- **激进追踪**：1% 利润即启动追踪，但需要 3% 偏移才触发，适合趋势延续

### 2.2 订单类型配置

```python
# 使用 Freqtrade 默认配置
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False
}
```

---

## 三、买入条件详解

### 3.1 保护机制

策略内置了"止损保护"机制 (`lost_protect`)：

```python
lost_protect = (dataframe["ema"] > (dataframe["close"] * 1.07)).rolling(10).sum() == 0
```

**保护逻辑**：过去10根K线中，EMA从未高于收盘价的107%，确保不在大幅上涨后追高。

### 3.2 买入条件组

#### 条件 #1：布林带下轨突破 + 资金流入 + 支撑确认

```python
item_buy_logic = []
item_buy_logic.append(dataframe["volume"] > 0)                     # 有成交量
item_buy_logic.append(dataframe["cmf"] > 0)                        # CMF > 0（资金流入）
item_buy_logic.append(prev["bb_bbl_i"] == 1)                       # 前一K线触及布林带下轨
item_buy_logic.append(prev["close"] >= prev1["support"])           # 价格不低于支撑位
item_buy_logic.append(prev["ema"] < prev["close"])                 # EMA下行趋势
item_buy_logic.append((dataframe["open"] < dataframe["close"]))     # 当前K线收阳
item_buy_logic.append(prev["open"] > prev["close"])                # 前一K线收阴（倒锤形态）
item_buy_logic.append((dataframe["bb_bbt"] > self.buy_bbt.value))  # 布林带宽度满足条件
item_buy_logic.append(lost_protect)                                # 止损保护
```

#### 条件 #2：布林带下轨突破 + 直接支撑

```python
item_buy_logic = []
item_buy_logic.append(dataframe["volume"] > 0)
item_buy_logic.append(dataframe["cmf"] > 0)
item_buy_logic.append(dataframe["bb_bbl_i"] == 1)                 # 当前K线触及布林带下轨
item_buy_logic.append(dataframe["open"] >= prev1["support"])      # 开盘价高于支撑
item_buy_logic.append(prev["ema"] < prev["close"])
item_buy_logic.append((dataframe["open"] < dataframe["close"]))
item_buy_logic.append((dataframe["bb_bbt"] > self.buy_bbt.value))
item_buy_logic.append(lost_protect)
```

### 3.3 核心参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| buy_bbt | 0.023 | 布林带宽度阈值 |
| ewo_high | 5.638 | EWO 高位阈值 |
| ewo_low | -19.993 | EWO 低位阈值 |
| low_offset | 0. | 买入价格偏移 |


| rsi_buy | 61 | RSI 买入阈值 |

---

## 四、卖出逻辑详解

### 4.1 自定义卖出信号

策略通过 `custom_exit` 函数实现复杂的卖出逻辑：

| 场景 | 触发条件 | 信号名称 |
|------|---------|---------|
| 阻力位反转 | 前一K突破布林带上轨 + 当前K收阴 + 接近阻力位 | sell_signal_1 |
| 强势反转 | 当前K突破布林带上轨 + 当前K收阴 + 远离阻力位 | sell_signal_2 |
| 趋势反转 | 当前K收阴 + EMA高于收盘价107% | stop_loss |
| 布林带下轨 | 当前K收阴 + 接近布林带下轨 + 有利润 | take_profit |
| SMA信号 | 买入标记包含"sma" + 利润>=1% | sma |
| SMA止损 | 买入标记包含"sma" + 价格高于EMA49*high_offset | stop_loss_sma |

### 4.2 ROI 退出优先级

| 持仓时间 | 最小利润率 | 触发退出 |
|---------|-----------|---------|
| 0 分钟 | 10% | 达到即退出 |
| 30 分钟 | 5% | 30 分钟后达到即退出 |
| 60 分钟 | 2% | 60 分钟后达到即退出 |

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **趋势指标** | EMA | 150 周期 | 长期趋势判断 |
| **波动指标** | Bollinger Bands | 20 周期，2 倍标准差 | 支撑阻力位 |
| **资金流指标** | CMF (Chaikin Money Flow) | 20 周期 | 资金流入/流出 |
| **动量指标** | RSI | 14 周期 | 超买超卖辅助 |

### 5.2 自定义指标

策略包含两个自定义类：

1. **SupResFinder**：支撑/阻力位识别器
   - `isSupport()`：识别支撑位
   - `isResistance()`：识别阻力位
   - `getSupport()`：获取支撑位序列
   - `getResistance()`：获取阻力位序列

2. **EWO**：Elliot Wave Oscillator（简化版）
   ```python
   def EWO(dataframe, ema_length=5, ema2_length=35):
       ema1 = ta.EMA(df, timeperiod=ema_length)
       ema2 = ta.EMA(df, timeperiod=ema2_length)
       emadif = (ema1 - ema2) / df["close"] * 100
       return emadif
   ```

---

## 六、风险管理特色

### 6.1 追踪止损机制

```python
trailing_stop = True
trailing_stop_positive = 0.01      # 1% 利润后启动追踪
trailing_stop_positive_offset = 0.03  # 从最高点回撤 3% 触发
trailing_only_offset_is_reached = True  # 仅在达到启动点后追踪
```

**工作机制**：
1. 利润达到 1% 后，追踪止损启动
2. 从最高点回撤 3% 时触发退出
3. 适合捕捉趋势延续行情

### 6.2 硬止损保护

```python
stoploss = -0.20  # -20%
```

---

## 七、策略优势与局限

### ✅ 优势

1. **多条件确认**：买入需要满足多个条件（CMF、支撑、趋势等），信号质量高
2. **资金流过滤**：CMF > 0 确保资金流入，减少假突破
3. **支撑阻力位结合**：使用 SupResFinder 动态识别支撑阻力
4. **保护机制完善**：lost_protect 防止在高位追涨
5. **自定义卖出**：5 种不同卖出场景，覆盖多种情况

### ⚠️ 局限

1. **信号频率较低**：条件复杂，满足条件的交易机会较少
2. **时间框架过短**：1分钟K线噪声大，容易产生假信号
3. **无趋势过滤**：没有 EMA200 等趋势判断，可能逆势交易
4. **参数较多**：buy_bbt、ewo_high、ewo_low 等参数需要精细调优

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **高波动币种** | 默认配置 | 布林带策略适合高波动 |
| **趋势行情** | 启用追踪止损 | 捕捉趋势延续 |
| **横盘震荡** | 减少交易对 | 信号质量优先 |
| **低波动市场** | 暂停使用 | 布林带收窄，无交易机会 |

---

## 九、适用市场环境详解

Dracula 是基于支撑阻力位的均值回归+资金流策略。

### 9.1 策略核心逻辑

- **布林带下轨买入**：价格触及布林带下轨时买入，属于极端超卖
- **资金流确认**：CMF > 0 确认资金流入，提高信号质量
- **支撑位验证**：买入价格不低于动态计算的支撑位
- **多场景卖出**：根据不同市场情况触发不同卖出信号

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★★☆ (较好) | 资金流确认能捕捉上涨趋势 |
| 🔄 宽幅震荡 | ★★★★★ (最佳) | 布林带支撑阻力在震荡市效果最好 |
| 📉 单边暴跌 | ★★☆☆☆ (较差) | 支撑位可能无效，持续创新低 |
| ⚡️ 极端横盘 | ★★★☆☆ (中等) | 布林带收窄，信号减少 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 20-40 个 USDT 交易对 | 信号少，需要较多交易对 |
| **最大持仓数** | 3-5 个订单 | 条件严格，持仓不宜过多 |
| **时间框架** | 1m（建议改为 5m） | 1m 噪声太大 |
| **止损** | -20% | 保持默认 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

策略包含约 300 行代码，包含自定义类和方法，学习曲线较陡。建议：

1. 先理解 SupResFinder 的支撑阻力计算逻辑
2. 理解 CMF 资金流指标的原理
3. 逐步调整参数，观察信号变化

### 10.2 硬件要求

策略计算量适中，对 VPS 要求不高：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 20-40 对 | 512MB | 1GB |
| 40-80 对 | 1GB | 2GB |

### 10.3 回测与实盘的差异

1分钟K线数据在回测和实盘中可能存在差异，建议：
- 先在模拟交易（Dry-Run）运行 2-4 周
- 观察信号触发频率是否符合预期
- 小资金实盘测试 1 个月后再加大资金

### 10.4 手动交易者建议

手动交易者可参考此策略的买入逻辑：
- 价格触及布林带下轨 + CMF > 0 + 接近支撑位 = 买入信号
- 结合大盘趋势判断（BTC 走势）
- 可将时间框架改为 5m 减少噪声

---

## 十一、总结

**Dracula** 是一个复杂的多条件策略，它的核心价值在于：

1. **资金流过滤**：CMF 指标确保资金流入，提高信号质量
2. **动态支撑阻力**：SupResFinder 实时计算支撑阻力位
3. **多场景卖出**：custom_exit 覆盖 5 种不同卖出场景
4. **保护机制**：lost_protect 防止高位追涨

对于量化交易者而言，这是一个优秀的进阶策略模板。建议：
- 首先理解每个指标的原理
- 可将时间框架从 1m 改为 5m 减少噪声
- 调整 buy_bbt 参数适应不同波动性的币种
- 考虑添加趋势过滤（如 EMA200 趋势判断）

---