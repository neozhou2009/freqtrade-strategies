# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


   
    # https://www.tradingview.com/script/zUaR3Vbb-robotrading-body/  
    # translated for freqtrade: viksal1982  viktors.s@gmail.com
    #  A timeframe of 4 hours to 1 day



class RobotradingBody(IStrategy):
   
    INTERFACE_VERSION = 2

   
    minimal_roi = {  # 已优化: 从最大 90% 改为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.1000 (已禁用), 改为 +0.10 (止损启用)

    for_mult = IntParameter(1, 20, default=3, space='buy', optimize=True)
    for_sma_length = IntParameter(20, 200, default=100, space='buy', optimize=True)

    trailing_stop = True

    timeframe = '4h'
process_only_new_candles = True

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 100

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }
    

    def informative_pairs(self):
       
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe['body'] = (dataframe['close'] - dataframe['open']).abs()
        dataframe['body_sma'] = (ta.SMA(dataframe['body'], timeperiod=int(self.for_sma_length.value))) * int(self.for_mult.value)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['open'] > dataframe['close'] ) &   
                (dataframe['body'] > dataframe['body_sma'] ) &   
                (dataframe['volume'] > 0)  
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['close'] > dataframe['open'] ) &   
                (dataframe['volume'] > 0) 
            ),
            'sell'] = 1
        return dataframe
    