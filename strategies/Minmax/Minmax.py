# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from scipy.signal import argrelextrema
import numpy as np


class Minmax(IStrategy):

    minimal_roi = {  # 已优化: 从最大 1000% 改为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.0500 (已禁用), 改为 +0.10 (止损启用)

    timeframe = '1h'

    trailing_stop = True
process_only_new_candles = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe_copy = dataframe.copy()
        frame_size = 500
        len_df = len(dataframe)
        dataframe['buy_signal'] = False
        dataframe['sell_signal'] = False
        lookback_size = 100
        # Let's calculate argrelextrema on separated data slices and get only last result to avoid lookahead bias!
        for i in range(len_df):
            if i + frame_size < len_df:
                slice = dataframe_copy[i : i+frame_size]
                min_peaks = argrelextrema(slice['close'].values, np.less, order=lookback_size)
                max_peaks = argrelextrema(slice['close'].values, np.greater, order=lookback_size)
                # Somehow we never getting last index of a frame as min or max. What a surprise :)
                # So lets take penultimate result and use it as a signal to buy/sell.
                if len(min_peaks[0]) and min_peaks[0][-1] == frame_size - 2:
                    # signal that penultimate candle is min
                    # lets buy here
                    dataframe.at[i + frame_size,'buy_signal'] = True
                if len(max_peaks[0]) and max_peaks[0][-1] == frame_size - 2:
                    # oh it seams that penultimate candle is max
                    # lets sell ASAP
                    dataframe.at[i + frame_size, 'sell_signal'] = True

                if i + frame_size == len_df - 1:
                    print(min_peaks)

        #                                                                               A
        # Wow what a pathetic results!!!Where is my Trillions of BTC?!?!?!              |
        # Let's make it in a lookahead way to make more numbers in backtesting!!        |
        #                                                                               |
        #                                                                               |
        # Comment this section!!  ------------------------------------------------------|
        # Uncomment this section ASAP!
        #           |
        #           |
        #           |
        #           |
        #           V

        # min_peaks = argrelextrema(dataframe['close'].values, np.less, order=loockback_size)
        # max_peaks = argrelextrema(dataframe['close'].values, np.greater, order=loockback_size)
        #
        #
        # for mp in min_peaks[0]:
        #     dataframe.at[mp, 'buy_signal'] = True
        #
        # for mp in max_peaks[0]:
        #     dataframe.at[mp, 'sell_signal'] = True

        # Uhhh that's better! Ordering Lambo now!

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        print(dataframe.tail(30))


        dataframe.loc[
            (
                dataframe['buy_signal']
) & (dataframe["volume"] > 0)),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:


        dataframe.loc[
            (
                dataframe['sell_signal']
            ),
            'sell'] = 1
        return dataframe