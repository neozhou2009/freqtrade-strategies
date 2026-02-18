# --- Do not remove these libs --- freqtrade backtesting --strategy SmoothScalp --timerange 20210110-20210410
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from typing import Dict, List
from functools import reduce
from pandas import DataFrame, DatetimeIndex, merge
# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy

#V1
class heikin(IStrategy):
    #do not use this strategy in live mod. It is not good enough yet and can only be use to find trends.
    timeframe = '1h'
    #I haven't found the best roi and stoplost, so feel free to explore.
    minimal_roi = {  # 已优化: 从最大 1000% 改为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.1000 (已禁用), 改为 +0.10 (止损启用)
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:   
        dataframe['hclose']=(dataframe['open'] + dataframe['high'] + dataframe['low'] + dataframe['close']) / 4
        dataframe['hopen']= ((dataframe['open'].shift(2) + dataframe['close'].shift(2))/ 2) #it is not the same as real heikin ashi since I found that this is better.
        dataframe['hhigh']=dataframe[['open','close','high']].max(axis=1)
        dataframe['hlow']=dataframe[['open','close','low']].min(axis=1)

        dataframe['emac'] = ta.SMA(dataframe['hclose'], timeperiod=6) #to smooth out the data and thus less noise.
        dataframe['emao'] = ta.SMA(dataframe['hopen'], timeperiod=6)
        return dataframe
        

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['emao'] < dataframe['emac'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['emao'] > dataframe['emac'])
            ),
            'sell'] = 1
        return dataframe
