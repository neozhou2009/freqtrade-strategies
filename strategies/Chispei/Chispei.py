# Freqtrade_backtest_validation_freqtrade1.py
# This script is 1 of a pair the other being freqtrade_backtest_validation_tradingview1
# These should be executed on their respective platforms for the same coin/period/resolution
# The purpose is to test Freqtrade backtest provides like results to a known industry platform.
#
# --- Do not remove these libs ---
#
#
#
# - EDIT: "Maybe the sucess of a trading system is part of strategy and also a good config.son too!"
#
#
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy


class Chispei(IStrategy):
    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.10,
        "60": 0.07,
        "120": 0.05,
        "240": 0.03
    }

    max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.3234 (已禁用), 改为 +0.10 (止损启用)
    ticker_interval = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - Simple Moving Average
        dataframe['fastMA'] = ta.SMA(dataframe, timeperiod=13)
        dataframe['slowMA'] = ta.SMA(dataframe, timeperiod=25)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=21)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['mom'] < 15) &
                (dataframe['fastMA'] > dataframe['slowMA'])
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['mom'] < 80) &
                (dataframe['fastMA'] < dataframe['slowMA'])
            ),
            'sell'] = 1
        return dataframe
