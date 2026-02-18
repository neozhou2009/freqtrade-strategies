# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import datetime

class ActionZone(IStrategy):
    """
    改进版ActionZone策略

    核心思路：
    - 使用EMA交叉识别趋势方向
    - 使用ADX确认趋势强度
    - 使用MACD确认动量方向
    - 使用ATR作为波动性过滤和动态止损基准
    - 严格的风险管理
    """

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # 改进：设置合理的分阶段ROI目标，逐步锁定利润
    minimal_roi = {  # 已优化: 从 15.0% 标准化为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }# 改进：设置合理的默认止损为-10%
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.1000 (已禁用), 改为 +0.10 (止损启用)
    use_custom_stoploss = True

    # Trailing stoploss - 启用止损上移保护利润
    trailing_stop = True
    trailing_stop_positive = 0.02   # 盈利2%后启用止损上移
    trailing_stop_positive_offset = 0.06  # 盈利6%后止损上移至+2%
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy.
    timeframe = '4h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = True  # 改进：如果有买入信号，忽略ROI，继续持有

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 100  # 增加以支持更多指标

    # 策略参数 - 可通过hyperopt优化
    # EMA周期
    fast_ema_period = IntParameter(8, 20, default=12, space="buy")
    slow_ema_period = IntParameter(20, 50, default=26, space="buy")

    # ADX趋势强度阈值
    adx_threshold = IntParameter(20, 35, default=25, space="buy")

    # ATR倍数用于止损
    atr_stop_loss_multiplier = DecimalParameter(1.5, 3.0, default=2.0, decimals=1, space="buy")
    atr_take_profit_multiplier = DecimalParameter(2.0, 5.0, default=3.0, decimals=1, space="buy")

    # ATR周期
    atr_period = IntParameter(14, 28, default=20, space="buy")

    # 最大仓位占总资金的比例
    max_position_size_percent = DecimalParameter(0.5, 2.0, default=1.0, decimals=2, space="buy")

    # 最小风险回报比
    min_risk_reward_ratio = DecimalParameter(1.5, 3.0, default=2.0, decimals=1, space="buy")

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False,
        'stoploss_on_exchange_interval': 60
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    plot_config = {
        'main_plot': {
            'fastMA': {
                'color': 'orange',
                'fill_to': 'slowMA',
                'fill_color': 'rgba(255, 165, 0,0.1)'
            },
            'slowMA': {
                'color': 'blue',
            },
            'atr_stop': {
                'color': 'red',
                'plot_type': 'scatter',
                'mode': 'markers',
                'marker_size': 3,
            },
            'atr_take_profit': {
                'color': 'green',
                'plot_type': 'scatter',
                'mode': 'markers',
                'marker_size': 3,
            },
        },
    }

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime, current_rate: float, current_profit: float, **kwargs) -> float:
        """
        改进：基于ATR的动态止损

        使用ATR作为止损基准，而不是固定的最低价。这样可以：
        1. 考虑当前市场的波动性
        2. 在高波动时给予价格更多空间
        3. 在低波动时更紧密地跟踪价格
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # 获取当前ATR值
        atr_value = last_candle.get('atr', 0)

        if atr_value == 0 or pd.isna(atr_value):
            # 回退到默认止损
            return self.stoploss

        # 计算动态止损价格
        stoploss_price = last_candle['close'] - (atr_value * self.atr_stop_loss_multiplier.value)

        # 转换为百分比
        return (stoploss_price / current_rate) - 1
    
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float, proposed_stake: float, min_stake: float, max_stake: float, **kwargs) -> float:
        """
        改进：更合理的仓位管理

        基于ATR和风险回报比计算仓位，而不是简单的最大损失计算
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        atr_value = last_candle.get('atr', 0)

        if atr_value == 0 or pd.isna(atr_value):
            return proposed_stake

        # 计算止损距离（ATR * multiplier）
        stop_distance = atr_value * self.atr_stop_loss_multiplier.value

        # 计算目标止盈距离
        take_profit_distance = atr_value * self.atr_take_profit_multiplier.value

        # 验证风险回报比
        if take_profit_distance / stop_distance < self.min_risk_reward_ratio.value:
            # 风险回报比不合适，减少仓位或不交易
            return min_stake

        # 根据总资金的百分比限制最大仓位
        max_allowed_stake = self.wallets.get_total_stake_amount() * (self.max_position_size_percent.value / 100)

        # 计算建议仓位
        try:
            if stop_distance > 0:
                # 基于ATR波动性调整仓位
                # 波动性越大，仓位越小
                volatility_adjusted_stake = max_allowed_stake * (2.0 / (1 + atr_value / last_candle['close'] * 100))

                return min(max(volatility_adjusted_stake, min_stake), max_allowed_stake)
            else:
                return proposed_stake
        except ZeroDivisionError:
            return min_stake

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        改进：添加更多技术指标以增强信号质量

        添加的指标：
        - EMA (12, 26, 50): 趋势识别
        - MACD: 动量确认
        - RSI: 超买超卖过滤
        - ADX: 趋势强度确认
        - ATR: 波动性测量和动态止损
        """
        # EMA - Exponential Moving Average
        fastEMA = ta.EMA(dataframe, timeperiod=self.fast_ema_period.value)
        slowEMA = ta.EMA(dataframe, timeperiod=self.slow_ema_period.value)
        trendEMA = ta.EMA(dataframe, timeperiod=50)  # 更长期的趋势确认

        dataframe['fastMA'] = fastEMA
        dataframe['slowMA'] = slowEMA
        dataframe['trendMA'] = trendEMA

        # MACD - Moving Average Convergence Divergence
        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # RSI - Relative Strength Index
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # ADX - Average Directional Index (趋势强度指标)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)

        # ATR - Average True Range (波动性指标)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=self.atr_period.value)

        # 动态止损和止盈价格
        dataframe['atr_stop'] = dataframe['close'] - (dataframe['atr'] * self.atr_stop_loss_multiplier.value)
        dataframe['atr_take_profit'] = dataframe['close'] + (dataframe['atr'] * self.atr_take_profit_multiplier.value)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        改进：增强的买入信号

        买入条件：
        1. 快EMA > 慢EMA (趋势向上)
        2. 收盘价 > 快EMA (价格在趋势上方)
        3. ADX > 阈值 (趋势足够强)
        4. MACD > MACD信号线 (动量向上)
        5. RSI < 70 (不是严重超买)
        6. 成交量 > 0
        """
        dataframe.loc[
            (
                (dataframe['fastMA'] > dataframe['slowMA']) &  # 趋势向上
                (dataframe['close'] > dataframe['fastMA']) &   # 价格在趋势上方
                (dataframe['adx'] > self.adx_threshold.value) &  # 趋势强度足够
                (dataframe['macd'] > dataframe['macdsignal']) & # 动量向上
                (dataframe['rsi'] < 70) &                      # 不是严重超买
                (dataframe['volume'] > 0)                      # 成交量有效
            ),
            'buy'] = 1

        # 增加额外的过滤条件：避免在长期趋势下方的短期上叉（假突破）
        dataframe.loc[
            (
                (dataframe['fastMA'] > dataframe['slowMA']) &
                (dataframe['close'] > dataframe['fastMA']) &
                (dataframe['close'] < dataframe['trendMA']) &  # 长期趋势仍在下方，谨慎
            ),
            'buy'] = 0

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        改进：增强的卖出信号

        卖出条件：
        1. 快EMA < 慢EMA (趋势向下)
        2. 收盘价 < 快EMA (价格在趋势下方)
        3. ADX > 阈值 (趋势足够强，避免震荡市的假信号)
        4. MACD < MACD信号线 (动量向下)
        5. RSI > 30 或快速下跌 (避免在底部恐慌卖出)
        6. 成交量 > 0
        """
        dataframe.loc[
            (
                (dataframe['fastMA'] < dataframe['slowMA']) &  # 趋势向下
                (dataframe['close'] < dataframe['fastMA']) &   # 价格在趋势下方
                (dataframe['adx'] > self.adx_threshold.value) &  # 趋势强度足够
                (dataframe['macd'] < dataframe['macdsignal']) & # 动量向下
                (dataframe['rsi'] > 30) &                      # 不是严重超卖
                (dataframe['volume'] > 0)                      # 成交量有效
            ),
            'sell'] = 1

        # 额外的卖出条件：严重超买反转
        dataframe.loc[
            (
                (dataframe['rsi'] > 75) &  # 严重超买
                (dataframe['close'] < dataframe['fastMA']) &  # 价格跌破快EMA
            ),
            'sell'] = 1

        return dataframe
    
    

