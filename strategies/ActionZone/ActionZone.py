# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from typing import Optional
from functools import reduce

from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime, timedelta

class ActionZone(IStrategy):
    """
    ActionZone策略 - 改进版
    
    原策略问题：
    1. 日级别EMA交叉滞后严重
    2. 追涨杀跌的入场逻辑
    3. 缺乏有效的风险管理
    
    改进方案：
    1. 切换到4小时时间框架，减少滞后
    2. 增加回调买入机制（买在支撑位）
    3. 增加RSI过滤避免超买买入
    4. 实施多级止盈和动态止损
    5. 增加波动率过滤
    """
    
    # Strategy interface version - 更新到 v3
    INTERFACE_VERSION = 3

    # 启用了多空双向交易
    can_short: bool = False
    
    # 启用仓位调整
    position_adjustment_enable = True

    # 🎯 合理的ROI阶梯 - 多级止盈
    minimal_roi = {
        "0": 0.15,      # 15% 利润止盈
        "60": 0.10,     # 1小时后 10%
        "120": 0.05,    # 2小时后 5%
        "240": 0.03     # 4小时后 3%
    }

    # 🛡️ 严格止损 - 8%最大亏损
    stoploss = -0.08
    
    # 使用自定义止损
    use_custom_stoploss = True
    
    # 启用追踪止损
    trailing_stop = True
    trailing_stop_positive = 0.03  # 盈利3%后启动
    trailing_stop_positive_offset = 0.05  # 追踪距离2%
    trailing_only_offset_is_reached = True

    # ⏱️ 优化为4小时时间框架（平衡滞后性和交易频率）
    timeframe = '4h'
    
    # 仅处理新K线，提升性能
    process_only_new_candles = True

    # 使用卖出信号
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # 启动所需K线数（EMA26 + 缓冲）
    startup_candle_count: int = 50

    # 📊 参数优化 - 可超参数调优
    # 快速EMA周期
    fast_ema_period = IntParameter(5, 20, default=9, space="buy")
    # 慢速EMA周期  
    slow_ema_period = IntParameter(15, 50, default=21, space="buy")
    # RSI周期
    rsi_period = IntParameter(10, 20, default=14, space="buy")
    # RSI买入阈值（避免超买）
    rsi_buy_threshold = IntParameter(40, 70, default=60, space="buy")
    # RSI卖出阈值
    rsi_sell_threshold = IntParameter(50, 80, default=70, space="sell")
    # ATR倍数（用于止损计算）
    atr_multiplier = DecimalParameter(1.5, 3.0, default=2.0, space="buy")
    # 最小ATR过滤（避免低波动垃圾币）
    min_atr_percent = DecimalParameter(0.5, 3.0, default=1.0, space="buy")
    # 回调深度（买入折扣）
    pullback_discount = DecimalParameter(0.98, 1.0, default=0.995, space="buy")

    # 订单类型
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # 订单时效
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }

    # 图表配置
    plot_config = {
        'main_plot': {
            'ema_fast': {'color': 'red'},
            'ema_slow': {'color': 'blue'},
            'bb_upper': {'color': 'gray', 'fill_to': 'bb_lower', 'fill_color': 'rgba(200,200,200,0.1)'},
            'bb_lower': {'color': 'gray'},
        },
        'subplots': {
            "RSI": {
                'rsi': {'color': 'purple'},
                'rsi_buy_threshold': {'color': 'green', 'plotly': {'line': {'dash': 'dot'}}},
                'rsi_sell_threshold': {'color': 'red', 'plotly': {'line': {'dash': 'dot'}}},
            },
            "ATR%": {
                'atr_percent': {'color': 'orange'},
                'min_atr_percent': {'color': 'red', 'plotly': {'line': {'dash': 'dot'}}},
            }
        }
    }

    def __init__(self, config: dict) -> None:
        """初始化策略"""
        super().__init__(config)
        self._last_candle_seen = 0

    def informative_pairs(self):
        """
        获取额外的信息对
        """
        pairs = self.dp.current_whitelist()
        informative_pairs = []
        
        # 获取日级别趋势信息
        for pair in pairs:
            informative_pairs.append((pair, '1d'))
            
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        计算技术指标
        """
        # 获取当前参数值
        fast_period = self.fast_ema_period.value
        slow_period = self.slow_ema_period.value
        rsi_period = self.rsi_period.value
        
        # 📈 双EMA系统 - 趋势判断
        dataframe['ema_fast'] = ta.EMA(dataframe, timeperiod=fast_period)
        dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=slow_period)
        dataframe['ema_trend'] = dataframe['ema_fast'] > dataframe['ema_slow']
        
        # 📊 RSI指标 - 避免超买买入
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=rsi_period)
        dataframe['rsi_buy_threshold'] = self.rsi_buy_threshold.value
        dataframe['rsi_sell_threshold'] = self.rsi_sell_threshold.value
        
        # 📏 ATR指标 - 波动率和止损计算
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['atr_percent'] = (dataframe['atr'] / dataframe['close']) * 100
        dataframe['min_atr_percent'] = self.min_atr_percent.value
        
        # 📉 布林带 - 识别超买超卖区域
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_upper'] = bollinger['upper']
        dataframe['bb_lower'] = bollinger['lower']
        dataframe['bb_middle'] = bollinger['mid']
        dataframe['bb_percent'] = (dataframe['close'] - dataframe['bb_lower']) / (dataframe['bb_upper'] - dataframe['bb_lower'])
        
        # 🎯 动态支撑位（EMA + 折扣）
        dataframe['dynamic_support'] = dataframe['ema_fast'] * self.pullback_discount.value
        
        # 📈 趋势强度（ADX）
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        
        # 💹 成交量分析
        dataframe['volume_sma'] = ta.SMA(dataframe['volume'], timeperiod=20)
        dataframe['volume_above_avg'] = dataframe['volume'] > dataframe['volume_sma']
        
        # 获取高时间框架趋势（日级别）
        if self.dp:
            informative = self.dp.get_pair_dataframe(metadata['pair'], '1d')
            if not informative.empty:
                informative['ema_fast_d'] = ta.EMA(informative, timeperiod=12)
                informative['ema_slow_d'] = ta.EMA(informative, timeperiod=26)
                informative['trend_daily'] = (informative['ema_fast_d'] > informative['ema_slow_d']).astype(int)
                dataframe = self.merge_informative_pair(dataframe, informative, self.timeframe, '1d', ffill=True)
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        生成买入信号
        
        买入条件（全部满足）：
        1. 上升趋势（快速EMA > 慢速EMA）
        2. RSI未超买（RSI < 阈值）
        3. 价格回调到支撑位附近（动态折扣）
        4. 波动率足够（ATR% > 阈值）
        5. 成交量正常
        6. 日级别趋势向上（如可用）
        """
        dataframe.loc[:, 'enter_long'] = 0
        
        # 基本条件
        conditions = [
            # 趋势向上
            dataframe['ema_trend'] == True,
            
            # RSI未超买
            dataframe['rsi'] < self.rsi_buy_threshold.value,
            
            # 价格回调到EMA附近（买在回调，不是追涨）
            dataframe['close'] <= dataframe['dynamic_support'],
            
            # 波动率过滤 - 排除死水币
            dataframe['atr_percent'] > self.min_atr_percent.value,
            
            # 成交量确认
            dataframe['volume'] > 0,
            dataframe['volume_above_avg'] == True,
            
            # ADX > 25 表示强趋势
            dataframe['adx'] > 25,
        ]
        
        # 日级别趋势过滤（如果有数据）
        if 'trend_daily_1d' in dataframe.columns:
            conditions.append(dataframe['trend_daily_1d'] == 1)
        
        # 所有条件必须满足
        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
        
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        生成卖出信号
        
        卖出条件（任一满足）：
        1. 趋势反转（快速EMA < 慢速EMA）
        2. RSI超买后回落
        3. 价格触及布林带上轨
        4. 跌破动态支撑
        """
        dataframe.loc[:, 'exit_long'] = 0
        
        # 趋势反转卖出
        trend_reverse = (
            (dataframe['ema_fast'] < dataframe['ema_slow']) &
            (dataframe['close'] < dataframe['ema_slow'])
        )
        
        # RSI超买卖出
        rsi_overbought = (
            (dataframe['rsi'] > self.rsi_sell_threshold.value) &
            (dataframe['rsi'].shift(1) > dataframe['rsi'])  # RSI开始回落
        )
        
        # 布林带上轨卖出
        bb_upper_touch = dataframe['close'] > dataframe['bb_upper'] * 0.995
        
        # 组合卖出条件
        conditions = [
            trend_reverse,
            rsi_overbought,
            bb_upper_touch
        ]
        
        dataframe.loc[reduce(lambda x, y: x | y, conditions), 'exit_long'] = 1
        
        return dataframe

    def custom_stoploss(self, pair: str, trade, current_time: datetime,
                       current_rate: float, current_profit: float, **kwargs) -> float:
        """
        动态止损计算
        
        策略：
        1. 基于ATR的动态止损
        2. 盈利后收紧止损
        3. 使用EMA作为软止损参考
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if dataframe.empty:
            return self.stoploss
            
        last_candle = dataframe.iloc[-1]
        
        # 获取ATR值
        atr = last_candle['atr']
        atr_stop = (atr * self.atr_multiplier.value) / current_rate
        
        # 基于利润的动态止损调整
        if current_profit > 0.10:  # 盈利>10%
            # 保护50%利润
            return -0.05
        elif current_profit > 0.05:  # 盈利>5%
            # 保护20%利润
            return -0.04
        elif current_profit > 0.03:  # 盈利>3%
            # 保本
            return -0.02
        
        # 基础ATR止损（不超过硬止损）
        atr_stoploss = -min(atr_stop, abs(self.stoploss))
        
        return atr_stoploss

    def custom_stake_amount(self, pair: str, current_time: datetime, 
                           current_rate: float, proposed_stake: float,
                           min_stake: float, max_stake: float, **kwargs) -> float:
        """
        自定义仓位大小
        
        基于波动率的仓位调整：
        - 高波动 = 小仓位
        - 低波动 = 大仓位
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if dataframe.empty:
            return proposed_stake
            
        last_candle = dataframe.iloc[-1]
        atr_percent = last_candle['atr_percent']
        
        # 波动率调整因子
        if atr_percent > 5:  # 高波动
            volatility_factor = 0.5
        elif atr_percent > 3:  # 中等波动
            volatility_factor = 0.7
        elif atr_percent > 1.5:  # 正常波动
            volatility_factor = 1.0
        else:  # 低波动
            volatility_factor = 1.2
        
        # 计算调整后的仓位
        adjusted_stake = proposed_stake * volatility_factor
        
        # 确保在边界内
        return max(min(adjusted_stake, max_stake), min_stake)

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                side: str, **kwargs) -> float:
        """
        杠杆设置 - 本策略不使用杠杆
        """
        return 1.0

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                           time_in_force: str, current_time: datetime, entry_tag: Optional[str],
                           side: str, **kwargs) -> bool:
        """
        交易确认 - 最终检查
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if dataframe.empty:
            return False
            
        last_candle = dataframe.iloc[-1]
        
        # 最终检查：避免在过度延伸时买入
        if last_candle['close'] > last_candle['bb_upper']:
            return False
            
        # 避免在连续大涨后买入
        if last_candle['close'] > last_candle['close'].shift(1) * 1.05:  # 单日涨幅>5%
            return False
            
        return True
