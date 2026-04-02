# Schism2 策略深度解读

> **策略编号**: #376 (465 个策略中的第 376 个)  
> **策略类型**: 多条件趋势跟踪 + 动态止盈止损 + 实时仓位感知 + 多货币适配  
> **时间框架**: 5 分钟 (5m) + 1 小时信息层 (1h)

---

## 一、策略概览

Schism2 是 Schism 策略的进化版本，由 @werkkrew 和 @JimmyNixx 开发，在原有框架基础上增加了多货币适配、动态信息对、Per-pair 参数支持等高级功能。策略核心保持"粘性买入信号"和"动态止损机制"的设计理念，同时扩展了对 BTC 和 ETH 作为 stake currency 的完整支持。

**演进说明**：作者明确指出 "This strategy is an evolution of our previous framework 'Schism'"，Schism2 是对原版 Schism 的全面升级。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 2 组独立买入信号（新仓位买入 + 持仓延续信号），支持 BTC/ETH stake 扩展条件 |
| **卖出条件** | 动态止损 + ROI 分级止盈，结合其他交易状态决策 |
| **保护机制** | 订单超时保护、入场确认、价格滑点保护、Per-pair 参数隔离 |
| **时间框架** | 主框架 5m + 信息框架 1h + 动态 COIN/FIAT 信息对 |
| **子策略** | Schism2_BTC（15m 框架）、Schism2_ETH（5m 框架） |
| **依赖库** | numpy, talib, qtpylib, arrow, pandas, typing, functools, datetime, freqtrade.persistence.Trade, technical.indicators.RMI, statistics.mean, cachetools.TTLCache |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.05,     # 立即需要 5% 利润
    "10": 0.025,   # 10分钟后需要 2.5%
    "20": 0.015,   # 20分钟后需要 1.5%
    "30": 0.01,    # 30分钟后需要 1%
    "720": 0.005,  # 12小时后需要 0.5%
    "1440": 0      # 24小时后接受任何利润
}

# 止损设置
stoploss = -0.30  # 30% 硬止损（比 Schism 更保守）

# 信号配置
use_sell_signal = True
sell_profit_only = True
ignore_roi_if_buy_signal = True  # 核心机制：买入信号延续时忽略 ROI
```

**设计思路**：
- ROI 阈值比 Schism 更激进，从 5% 起步（Schism 是 10%）
- 止损更保守：-30%（Schism 是 -40%）
- 时间维度扩展到 12 小时（720 分钟），适应更长持仓

### 2.2 买入参数

```python
buy_params = {
    'inf-pct-adr': 0.83534,    # ADR 百分位阈值（更精确）
    'inf-rsi': 57,             # 信息层 RSI 下限（比 Schism 高）
    'mp': 64,                   # Momentum Pinball 上限（比 Schism 高）
    'rmi-fast': 49,             # 快速 RMI 上限（比 Schism 高）
    'rmi-slow': 24,             # 慢速 RMI 下限（比 Schism 高）
    'xinf-stake-rmi': 45,       # STAKE/FIAT 信息层 RMI 上限（BTC/ETH 专用）
    'xtf-fiat-rsi': 28,         # COIN/FIAT RSI 下限（BTC/ETH 专用）
    'xtf-stake-rsi': 90         # STAKE/FIAT RSI 上限（BTC/ETH 专用）
}
```

**参数对比（Schism vs Schism2）**：

| 参数 | Schism | Schism2 | 变化解读 |
|------|--------|---------|---------|
| inf-rsi | 30 | 57 | 更高的 RSI 阈值，避免极端超卖 |
| mp | 50 | 64 | 更宽松的动量限制 |
| rmi-fast | 20 | 49 | 允许更高的快速 RMI |
| rmi-slow | 20 | 24 | 更高的慢速 RMI 下限 |
| inf-pct-adr | 0.8 | 0.83534 | 更精确的 ADR 计算 |

### 2.3 订单类型配置

策略未显式定义 `order_types`，使用 Freqtrade 默认配置。

---

## 三、买入条件详解

### 3.1 技术指标体系

Schism2 继承 Schism 的核心指标体系，并扩展了多货币支持：

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **动量指标** | RMI-slow | length=21, mom=5 | 趋势方向判断 |
| **动量指标** | RMI-fast | length=8, mom=4 | 快速信号捕捉 |
| **动量指标** | ROC | timeperiod=6 | 变化率测量 |
| **综合指标** | Momentum Pinball | RSI(ROC, 6) | 超买超卖定位 |
| **趋势指标** | RMI-up-trend/dn-trend | rolling(3) >= 2 | 趋势确认 |
| **信息层** | RSI_1h | timeperiod=14 | 高维度趋势判断 |
| **信息层** | 1d_high/3d_low | rolling(24/72) | 价格区间定位 |
| **BTC/ETH 专用** | STAKE_rsi | timeperiod=14 | STAKE/FIAT RSI |
| **BTC/ETH 专用** | STAKE_rmi_1h | length=21, mom=5 | STAKE/FIAT RMI |
| **BTC/ETH 专用** | FIAT_rsi | timeperiod=14 | COIN/FIAT RSI |

### 3.2 动态信息对

当 stake currency 为 BTC 或 ETH 时，策略自动添加额外信息对：

```python
def informative_pairs(self):
    pairs = self.dp.current_whitelist()
    informative_pairs = [(pair, self.inf_timeframe) for pair in pairs]
    
    # BTC/ETH Stake 扩展
    if self.config['stake_currency'] in ('BTC', 'ETH'):
        for pair in pairs:
            coin, stake = pair.split('/')
            coin_fiat = f"{coin}/{self.custom_fiat}"  # 如 XLM/USD
            informative_pairs += [(coin_fiat, self.timeframe)]
        
        stake_fiat = f"{self.config['stake_currency']}/{self.custom_fiat}"  # 如 BTC/USD
        informative_pairs += [(stake_fiat, self.timeframe)]
        informative_pairs += [(stake_fiat, self.inf_timeframe)]
    
    return informative_pairs
```

**信息对矩阵**：

| Stake Currency | 额外信息对 | 时间框架 |
|---------------|-----------|---------|
| USDT/USDC | 无 | - |
| BTC | COIN/USD, BTC/USD | 5m + 1h |
| ETH | COIN/USD, ETH/USD | 5m + 1h |

### 3.3 买入条件分类

#### 条件组 #1：新仓位买入信号（无活跃交易时）

**基础条件（所有 stake currency）**：

```python
条件 = [
    close <= 3d_low_1h + 0.83534 * ADR_1h,           # 价格定位
    RSI_1h >= 57,                                     # 信息层 RSI
    rmi-dn-trend == 1,                                # RMI 下降趋势
    rmi-slow >= 24,                                   # 慢速 RMI 下限
    rmi-fast <= 49,                                   # 快速 RMI 上限
    mp <= 64,                                         # Momentum Pinball
    volume > 0                                        # 成交量
]
```

**BTC/ETH Stake 扩展条件**：

```python
if stake_currency in ('BTC', 'ETH'):
    条件 += [
        (STAKE_rsi < 90) | (FIAT_rsi > 28),           # STAKE 或 FIAT 条件
        STAKE_rmi_1h < 45                             # STAKE 信息层 RMI
    ]
```

**逻辑解读**：
- **STAKE_rsi < 90**：如果 stake（BTC/ETH）RSI 不太高，说明 stake 本身没有超买
- **FIAT_rsi > 28**：或者 COIN/FIAT（如 XLM/USD）RSI 不是极端超卖
- **STAKE_rmi_1h < 45**：STAKE/FIAT 的 1 小时 RMI 不太高

**设计哲学**：当用 BTC 或 ETH 作为 stake 时，不仅要看交易对本身，还要看 stake 的表现。如果 BTC 正在暴涨（RSI 高），可能不是好的入场时机。

#### 条件组 #2：持仓延续买入信号（有活跃交易时）

```python
# profit_factor 计算
profit_factor = 1 - (rmi_slow / 400)  # 与 Schism 相同

# rmi_grow 计算 (线性增长)
rmi_grow = linear_growth(30, 70, 180, 720, open_minutes)

条件 = [
    rmi-up-trend == 1,                                # RMI 上升趋势
    current_profit > peak_profit * profit_factor,     # 动态利润因子
    rmi-slow >= rmi_grow                              # RMI 动态阈值
]
```

### 3.4 买入条件总结

| 条件组 | 适用场景 | 核心逻辑 |
|-------|---------|---------|
| 新仓位买入 | 无活跃交易 | 信息层定位 + RMI 逆势抄底 + 动量确认 + BTC/ETH 扩展 |
| 持仓延续 | 有活跃交易 | 趋势确认 + 动态利润因子 + RMI 增长阈值 |

---

## 四、卖出逻辑详解

### 4.1 分级止盈系统（ROI）

策略采用时间递减 ROI 机制：

```
持仓时间      利润阈值    说明
────────────────────────────────
0 分钟        5%          快速止盈目标
10 分钟       2.5%        中短期目标
20 分钟       1.5%        降低期望
30 分钟       1%          接受小利
720 分钟      0.5%        12小时后
1440 分钟     0%          24小时后接受任何利润
```

**与 Schism 对比**：

| 时间 | Schism ROI | Schism2 ROI | 变化 |
|------|-----------|-------------|------|
| 0 | 10% | 5% | 更激进 |
| 15/10 | 5% | 2.5% | 更激进 |
| 30 | 2.5% | 1% | 更激进 |
| 60/720 | 1% | 0.5% | 扩展到 12 小时 |
| 120/1440 | 0.5% | 0% | 一致 |

### 4.2 动态止损卖出

卖出逻辑与 Schism 一致，用于"动态止损"：

```python
if active_trade:
    loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
    
    条件 = [
        current_profit < loss_cutoff,
        current_profit > stoploss,                    # -30% vs Schism 的 -40%
        rmi-dn-trend == 1,
        volume > 0
    ]
    
    if peak_profit > 0:
        条件 += [rmi-slow crossed_below 50]
    else:
        条件 += [rmi-slow crossed_below 10]
    
    # 全局仓位感知
    if other_trades:
        if free_slots > 0:
            max_market_down = -0.04
            hold_pct = (1 / free_slots) * max_market_down
            条件 += [avg_other_profit >= hold_pct]
        else:
            条件 += [biggest_loser == True]
```

### 4.3 Per-pair 参数支持

Schism2 新增 `get_pair_params` 方法，支持为不同交易对设置独立参数：

```python
def get_pair_params(self, pair: str, params: str) -> Dict:
    buy_params = self.buy_params
    sell_params = self.sell_params
    minimal_roi = self.minimal_roi
    
    if self.custom_pair_params:
        custom_params = next(
            (item for item in self.custom_pair_params if pair in item['pairs']),
            None
        )
        if custom_params:
            if custom_params['buy_params']:
                buy_params = custom_params['buy_params']
            if custom_params['sell_params']:
                sell_params = custom_params['sell_params']
            if custom_params['minimal_roi']:
                minimal_roi = custom_params['minimal_roi']
    
    return {'buy': buy_params, 'sell': sell_params, 'minimal_roi': minimal_roi}
```

**配置示例**：

```python
custom_pair_params = [
    {
        'pairs': ['BTC/USDT', 'ETH/USDT'],
        'buy_params': {'inf-rsi': 40, 'mp': 50},
        'minimal_roi': {"0": 0.08, "30": 0.04}
    },
    {
        'pairs': ['DOGE/USDT'],
        'buy_params': {'inf-rsi': 25, 'mp': 70},
        'minimal_roi': {"0": 0.15, "60": 0.05}
    }
]
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| **相对动量指数** | RMI-slow (21, 5) | 主趋势判断 |
| **相对动量指数** | RMI-fast (8, 4) | 快速信号 |
| **变化率** | ROC (6) | 动量测量 |
| **动量弹球** | MP = RSI(ROC, 6) | 超买超卖定位 |
| **趋势方向** | RMI-up/dn | 单周期方向 |
| **趋势强度** | RMI-up-trend/dn-trend | 三周期确认 |

### 5.2 信息时间框架指标（1h）

与 Schism 一致：
- **RSI_1h**: 14 周期 RSI
- **1d_high**: 24 小时最高价
- **3d_low**: 72 小时最低价
- **ADR**: 平均日波动范围

### 5.3 BTC/ETH 专用指标

| 指标 | 时间框架 | 用途 |
|------|---------|------|
| **STAKE_rsi** | 5m | STAKE/FIAT（如 BTC/USD）RSI |
| **STAKE_rmi_1h** | 1h | STAKE/FIAT RMI 信息层 |
| **FIAT_rsi** | 5m | COIN/FIAT（如 XLM/USD）RSI |

---

## 六、风险管理特色

### 6.1 硬止损与动态止损结合

| 止损类型 | Schism | Schism2 | 变化 |
|---------|--------|---------|------|
| 硬止损 | -40% | -30% | 更保守 |
| 动态止损 | -3% → 0% | -3% → 0% | 一致 |

**Schism2 止损更保守**：从 -40% 调整到 -30%，降低单笔最大亏损。

### 6.2 Per-pair ROI 支持

Schism2 新增 `min_roi_reached` 方法，支持按交易对获取 ROI 阈值：

```python
def min_roi_reached_entry(self, trade_dur: int, pair: str = 'backtest'):
    minimal_roi = self.get_pair_params(pair, 'minimal_roi')
    roi_list = list(filter(lambda x: x <= trade_dur, minimal_roi.keys()))
    if not roi_list:
        return None, None
    roi_entry = max(roi_list)
    return roi_entry, minimal_roi[roi_entry]

def min_roi_reached(self, trade: Trade, current_profit: float, current_time: datetime):
    trade_dur = int((current_time.timestamp() - trade.open_date_utc.timestamp()) // 60)
    _, roi = self.min_roi_reached_entry(trade_dur, trade.pair)
    if roi is None:
        return False
    return current_profit > roi
```

### 6.3 订单超时与入场确认

与 Schism 一致：
- `check_buy_timeout`: 滑点 > 1% 取消买单
- `check_sell_timeout`: 滑点 > 1% 取消卖单
- `confirm_trade_entry`: 入场前滑点 > 1% 拒绝

### 6.4 价格缓存机制

```python
custom_current_price_cache: TTLCache = TTLCache(maxsize=100, ttl=300)  # 5 分钟 TTL
```

---

## 七、策略优势与局限

### ✅ 优势

1. **多货币适配**：完整支持 BTC/ETH 作为 stake currency，自动添加相关信息对

2. **Per-pair 参数隔离**：可为不同交易对设置独立的买入参数、卖出参数、ROI

3. **子策略扩展**：内置 Schism2_BTC 和 Schism2_ETH 子类，针对不同 stake 优化

4. **更保守的止损**：-30% vs Schism 的 -40%，降低单笔最大亏损

5. **更激进 ROI**：从 5% 起步（Schism 是 10%），适应更快节奏

### ⚠️ 局限

1. **仅限实盘**：与 Schism 相同，核心功能不兼容回测

2. **参数更多**：买入参数 8 个（Schism 是 5 个），优化难度更大

3. **信息对依赖**：BTC/ETH stake 需要额外的 API 调用，增加延迟风险

4. **复杂度更高**：多货币适配 + Per-pair 参数，配置复杂度显著增加

5. **过拟合风险**：更多参数意味着更高的过拟合风险

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **BTC Stake** | Schism2_BTC 子策略 | 15m 时间框架，针对 BTC 优化 |
| **ETH Stake** | Schism2_ETH 子策略 | 5m 时间框架，针对 ETH 优化 |
| **USDT Stake** | 基础 Schism2 | 无需额外信息对 |
| **多交易对** | 配置 custom_pair_params | 为不同币种设置独立参数 |

---

## 九、适用市场环境详解

Schism2 系列是 **"进化版抄底型趋势跟踪策略"**。基于其代码架构和 Schism 系列的实盘验证经验，它最适合 **震荡下跌后的反弹行情**，同时增加了对 BTC/ETH stake 的专项优化。

### 9.1 策略核心逻辑

- **抄底有扩展**：除了原版 Schism 的条件，还检查 STAKE/FIAT 和 COIN/FIAT 的状态
- **趋势延续**：与 Schism 相同的持仓延续机制，最大化趋势收益
- **Per-pair 定制**：不同币种可以使用不同参数，避免"一刀切"
- **子策略隔离**：BTC 和 ETH stake 有独立优化的子类

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 **慢牛行情** | ⭐⭐⭐⭐⭐ | 趋势延续机制充分发挥，持仓收益最大化 |
| 🔄 **震荡行情** | ⭐⭐⭐⭐☆ | Per-pair 参数可针对不同币种优化 |
| 📉 **单边暴跌** | ⭐⭐☆☆☆ | 抄底信号可能过早触发，止损风险存在 |
| ⚡️ **急涨急跌** | ⭐⭐☆☆☆ | 订单保护可能失效，滑点风险高 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| `max_open_trades` | 3-5 | 配合全局仓位感知 |
| `stake_currency` | USDT/BTC/ETH | 三种均支持 |
| `timeframe` | 5m（ETH）/ 15m（BTC） | 根据子策略调整 |
| `custom_pair_params` | 可选 | 为特殊币种配置 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

Schism2 代码约 350 行，包含：
- 多时间框架指标计算
- 动态信息对管理
- Per-pair 参数系统
- 子策略继承机制
- 实时数据库查询

建议先熟练掌握 Schism，再升级到 Schism2。

### 10.2 硬件要求

| 交易对数量 | Stake 类型 | 最低内存 | 推荐内存 |
|-----------|-----------|---------|---------|
| 1-10 对 | USDT | 2 GB | 4 GB |
| 1-10 对 | BTC/ETH | 4 GB | 8 GB |
| 10-30 对 | USDT | 4 GB | 8 GB |
| 10-30 对 | BTC/ETH | 8 GB | 16 GB |
| 30+ 对 | 任意 | 16 GB | 32 GB |

**注意**：BTC/ETH stake 需要额外的信息对 API 调用，内存和网络开销显著增加。

### 10.3 回测与实盘的差异

与 Schism 相同：
- `ignore_roi_if_buy_signal` 和持仓延续信号 **仅在实盘/干跑中生效**
- 回测时无法获取 `Trade.get_trades()` 数据
- 回测结果可能与实盘表现有显著差异

**建议流程**：
1. 先用 Schism 熟悉核心逻辑
2. 用 dry_run 验证 Schism2 的扩展功能
3. 最后小仓位实盘验证

### 10.4 手动交易者建议

Schism2 的核心思想可借鉴：
- **多维度确认**：不仅看交易对本身，还看 stake currency 的状态
- **Per-pair 定制**：不同币种有不同的"脾气"，参数可以差异化
- **子策略隔离**：针对不同场景使用不同配置

---

## 十一、总结

**Schism2** 是一个 **"进化版抄底型趋势跟踪策略"**，在 Schism 基础上增加了多货币适配、Per-pair 参数、子策略扩展等高级功能。它的核心价值在于：

1. **多货币完整支持**：BTC/ETH stake 自动添加 COIN/FIAT 和 STAKE/FIAT 信息对
2. **Per-pair 参数隔离**：不同交易对可以使用不同的买入参数和 ROI
3. **子策略扩展**：Schism2_BTC 和 Schism2_ETH 针对不同场景优化
4. **更保守的风险控制**：止损 -30%（vs Schism 的 -40%），ROI 更激进（5% 起步）

对于量化交易者而言，Schism2 是一个 **进阶版实盘策略**，适合已经熟悉 Schism、需要更多灵活性和多货币支持的交易者。建议先掌握 Schism 的核心逻辑，再升级到 Schism2。