# BB_RPB_TSL_RNG_TBS 策略深度解读

> **策略编号**: #444 (465 个策略中的第 444 个)  
> **策略类型**: 布林带突破 + 回调买入 + 自定义追踪止损 + 追踪买入  
> **时间框架**: 5 分钟 (5m) + 动态信息层

---

## 一、策略概览

BB_RPB_TSL_RNG_TBS 是 BB_RPB_TSL_RNG_2 的增强版本，增加了 **Trailing Buy Strategy (TBS)** 追踪买入机制。策略名称中的 TBS 代表 Trailing Buy Strategy（追踪买入策略），即在买入信号出现后不立即下单，而是等待价格进一步下跌后再买入，以获取更优的入场价格。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 7 个独立买入信号 + 追踪买入机制 |
| **卖出条件** | 2 组卖出信号组合 + 自定义追踪止损 |
| **保护机制** | 分级追踪止损（3 档） + 追踪买入保护 |
| **时间框架** | 5m 主框架 |
| **依赖库** | qtpylib, numpy, talib, pandas_ta, technical |
| **特殊功能** | 追踪买入（仅限 live/dry_run 模式） |
| **兼容性** | 不支持回测/Hyperopt |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表 - 固定 10% 止盈
minimal_roi = {
    "0": 0.10,
}

# 止损设置 - 固定 10%（由自定义止损覆盖）
stoploss = -0.10

# 启用自定义追踪止损
use_custom_stoploss = True
use_sell_signal = True
process_only_new_candles = True  # 仅处理新K线，减少计算开销
```

### 2.2 分级追踪止损参数

```python
# 硬止损（亏损时）
pHSL = -0.178  # -17.8%

# 第一档：盈利 1.9% 触发
pPF_1 = 0.019
pSL_1 = 0.019

# 第二档：盈利 6.5% 触发
pPF_2 = 0.065
pSL_2 = 0.062
```

### 2.3 追踪买入参数

```python
# TrailingBuyStrat2 类参数
trailing_buy_order_enabled = True  # 启用追踪买入
trailing_expire_seconds = 1800  # 30分钟超时

# 追踪买入上限控制
trailing_buy_max_stop = 0.02   # 价格高于起始价2%时停止追踪
trailing_buy_max_buy = 0.000   # 价格低于起始价时买入

# 上升趋势快速买入（可选）
trailing_buy_uptrend_enabled = False  # 默认关闭
trailing_expire_seconds_uptrend = 90  # 90秒超时
min_uptrend_trailing_profit = 0.02  # 最小追踪利润
```

---

## 三、追踪买入机制详解

### 3.1 追踪买入工作原理

追踪买入的核心思想：**买入信号出现后，等待价格继续下跌，在更好的价格入场**。

```
时序图：

时间  价格    动作
─────────────────────────────────
T0    100    买入信号出现，开始追踪
T1    99     价格下跌，更新上限
T2    98     价格继续下跌，更新上限
T3    99     价格反弹，触发买入！
─────────────────────────────────
      入场价：99（比信号价100更优）
```

### 3.2 追踪买入状态机

```python
init_trailing_dict = {
    'trailing_buy_order_started': False,  # 是否已开始追踪
    'trailing_buy_order_uplimit': 0,      # 当前上限价格
    'start_trailing_price': 0,            # 起始追踪价格
    'buy_tag': None,                      # 买入标签
    'start_trailing_time': None,          # 开始追踪时间
    'offset': 0,                          # 当前偏移值
    'allow_trailing': False,              # 是否允许追踪
}
```

### 3.3 追踪买入触发条件

| 场景 | 条件 | 动作 |
|------|------|------|
| 开始追踪 | buy信号 + allow_trailing | 记录起始价格，等待 |
| 价格下跌 | current < uplimit | 更新上限价格 |
| 价格反弹 | current > uplimit 且 current < start * (1 + max_buy) | **触发买入** |
| 价格过高 | current > start * (1 + max_stop) | 停止追踪 |
| 超时 | 超过1800秒 | 停止追踪或强制买入 |

### 3.4 追踪买入偏移函数

```python
def trailing_buy_offset(self, dataframe, pair, current_price):
    current_trailing_profit_ratio = (start_price - current_price) / start_price
    
    # 分级偏移
    trailing_buy_offset = {
        0.06: 0.02,  # 价格跌6%，反弹2%就买
        0.03: 0.01,  # 价格跌3%，反弹1%就买
        0: 0.005,    # 默认：反弹0.5%就买
    }
    
    # 超时强制买入
    if duration > 1800 seconds and profit > 0 and buy_signal_active:
        return 'forcebuy'
    
    # 价格高于起始价，返回默认偏移
    if profit_ratio < 0:
        return 0.005
```

---

## 四、买入条件详解

### 4.1 七个基础买入条件（继承自 BB_RPB_TSL_RNG_2）

| 条件编号 | 条件名称 | 核心逻辑 | Buy Tag |
|---------|---------|---------|---------|
| #1 | BB_checked | 超卖+突破组合 | bb |
| #2 | local_uptrend | 上升趋势回调 | local uptrend |
| #3 | ewo | Elliott波回调 | ewo |
| #4 | ewo_2 | EWO动量向上 | ewo2 |
| #5 | cofi | 随机金叉确认 | cofi |
| #6 | nfi_32 | 深度回调 | nfi 32 |
| #7 | nfi_33 | 极端超卖反弹 | nfi 33 |

### 4.2 追踪买入的增强逻辑

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force, **kwargs):
    # 仅在 live/dry_run 模式启用追踪买入
    if self.trailing_buy_order_enabled and self.config['runmode'].value in ('live', 'dry_run'):
        
        # 获取最新K线数据
        dataframe = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        current_price = rate
        
        # 追踪买入逻辑
        if trailing_buy['allow_trailing']:
            if buy_signal and not trailing_started:
                # 开始追踪
                start_trailing(price, buy_tag)
            elif price_rebounds:
                # 触发买入
                return True
            elif price_too_high:
                # 停止追踪
                reset_trailing()
```

---

## 五、卖出逻辑详解

### 5.1 卖出信号组合（同 BB_RPB_TSL_RNG_2）

**卖出条件组 1**：
```python
(close > sma_9) &
(close > ma_sell * high_offset_2) &
(rsi > 50) &
(volume > 0) &
(rsi_fast > rsi_slow)
```

**卖出条件组 2**：
```python
(sma_9 > sma_9.shift(1) * 1.005) &
(close < hma_50) &
(close > ma_sell * high_offset) &
(volume > 0) &
(rsi_fast > rsi_slow)
```

### 5.2 卖出参数差异

| 参数 | RNG_2 默认值 | RNG_TBS 默认值 | 说明 |
|------|-------------|---------------|------|
| base_nb_candles_sell | 23 | 24 | 卖出均线周期 |
| high_offset | 1.051 | 0.991 | 高位偏移 |
| high_offset_2 | 1.02 | 0.997 | 低位偏移 |
| sell_btc_safe | -325 | -389 | BTC保护阈值 |

**差异解读**：TBS版本的卖出偏移更保守（<1），意味着更快触发卖出信号。

---

## 六、技术指标体系

### 6.1 核心指标（同 RNG_2）

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| 布林带 | BB(20,2), BB(20,3) | 价格通道、突破信号 |
| EMA | EMA(8,12,13,16,26,100) | 趋势判断 |
| SMA | SMA(9,15,30) | 价格均线 |
| RSI | RSI(4,14,20) | 超买超卖 |
| CCI | CCI(26,170) | 商品通道指标 |
| RMI | RMI(可变周期) | 相对动量 |
| EWO | Elliott Wave(50,200) | 波动震荡 |
| HMA | HMA(50) | Hull移动平均 |
| Williams %R | WR(14) | 超买超卖 |
| CTI | CTI(20) | 相对趋势 |

### 6.2 动态信息层配置

```python
def informative_pairs(self):
    # 动态获取当前交易对的计价货币
    if self.config['stake_currency'] in ['USDT','BUSD','USDC','DAI','TUSD','PAX','USD','EUR','GBP']:
        btc_info_pair = f"BTC/{self.config['stake_currency']}"
    else:
        btc_info_pair = "BTC/USDT"
    
    informative_pairs.append((btc_info_pair, self.timeframe))
```

**设计优势**：自动适配不同计价货币的交易所。

---

## 七、风险管理特色

### 7.1 双重追踪机制

| 追踪类型 | 方向 | 目的 |
|---------|------|------|
| 追踪买入 | 买入前 | 获取更优入场价格 |
| 追踪止损 | 买入后 | 锁定利润，限制亏损 |

### 7.2 追踪买入风险控制

```python
# 价格上涨上限
trailing_buy_max_stop = 0.02  # 价格高于起始价2%停止追踪

# 价格下跌买入
trailing_buy_max_buy = 0.000  # 价格低于起始价即买入

# 时间限制
trailing_expire_seconds = 1800  # 30分钟超时
```

### 7.3 追踪买入注意事项

⚠️ **重要警告**：追踪买入功能 **不兼容回测和Hyperopt**！

原因：
- 回测假设买入信号出现即刻成交
- 追踪买入依赖实时价格变化
- 无法在历史数据中模拟追踪过程

---

## 八、策略优势与局限

### ✅ 优势

1. **更优入场价格**：追踪买入机制可能获取更低的入场价
2. **双重追踪保护**：买入前追踪价格，买入后追踪止损
3. **动态适配**：自动适配不同计价货币
4. **时间效率**：process_only_new_candles减少计算开销
5. **继承完整逻辑**：保留BB_RPB_TSL_RNG_2所有买入条件

### ⚠️ 局限

1. **不支持回测**：追踪买入无法在回测中正确模拟
2. **不支持Hyperopt**：参数优化需使用基础版本
3. **实盘依赖实时价格**：API延迟可能影响追踪效果
4. **参数复杂度更高**：增加追踪买入参数
5. **超时风险**：30分钟超时可能错过入场机会

---

## 九、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 波动上升 | 启用追踪买入 | 获取更优入场价 |
| 快速趋势 | 关闭追踪买入 | 信号出现即刻买入 |
| 低波动 | 调整超时参数 | 增加超时时间等待入场 |
| 高波动 | 收紧追踪参数 | 减少等待时间 |

---

## 十、与 BB_RPB_TSL_RNG_2 的对比

### 10.1 核心差异

| 特性 | RNG_2 | RNG_TBS |
|------|-------|---------|
| 追踪买入 | ❌ | ✅ |
| 回测支持 | ✅ | ❌ |
| Hyperopt支持 | ✅ | ❌ |
| 信息层配置 | 固定BTC/USDT | 动态适配 |
| 卖出偏移 | 保守 | 更保守 |
| 计算模式 | 每tick | 仅新K线 |

### 10.2 使用建议

| 场景 | 推荐版本 |
|------|---------|
| 回测/参数优化 | BB_RPB_TSL_RNG_2 |
| 实盘（追求更优入场） | BB_RPB_TSL_RNG_TBS |
| 实盘（追求速度） | BB_RPB_TSL_RNG_2 |

---

## 十一、总结

**BB_RPB_TSL_RNG_TBS** 是 BB_RPB_TSL_RNG_2 的 **实盘增强版本**。它的核心价值在于：

1. **追踪买入**：等待价格进一步下跌后入场，可能获取更优价格
2. **双重追踪**：买入前追踪价格，买入后追踪止损，全程保护
3. **动态适配**：自动适配不同计价货币的交易所
4. **继承完整逻辑**：保留基础版本所有成熟的买入条件

对于量化交易者而言：
- **参数优化阶段**：使用 BB_RPB_TSL_RNG_2 进行回测和Hyperopt
- **实盘部署阶段**：使用 BB_RPB_TSL_RNG_TBS 获取追踪买入优势
- **同时运行**：可在不同交易对分别使用两个版本进行对比