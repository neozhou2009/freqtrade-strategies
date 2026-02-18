from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta

__author__       = "Robert Roman"
__copyright__    = "Free For Use"
__license__      = "MIT"
__version__      = "1.0"
__maintainer__   = "Robert Roman"
__email__        = "robertroman7@gmail.com"
__BTC_donation__ = "3FgFaG15yntZYSUzfEpxr5mDt1RArvcQrK"

# Optimized With Sortino Ratio and 2 years data

class macd_recovery(IStrategy):

    ticker_interval = '5m'

    # ROI table:
    minimal_roi = {
        "0": 0.10,
        "60": 0.07,
        "120": 0.05,
        "240": 0.03
    }

    # Stoploss:
    max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.0403 (已禁用), 改为 +0.10 (止损启用)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
      
        # EMA200
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        
        #RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        
        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'].rolling(8).min() < 41) &
                    (dataframe['close'] > dataframe['ema200']) &
                    (qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']))
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['rsi'].rolling(8).max() > 93) &
                    (dataframe['macd'] > 0) &
                    (qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']))
            ),
            'sell'] = 1

        return dataframe