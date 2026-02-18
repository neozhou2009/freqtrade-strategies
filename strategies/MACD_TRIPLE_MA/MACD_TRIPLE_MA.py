# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# --------------------------------


class MACD_TRIPLE_MA(IStrategy):
   
    
    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    
    # Optimal stoploss designed for the strategy
    # ROI table:
    minimal_roi = {  # 已优化: 从 15.8% 标准化为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }# Stoploss:
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.0300 (已禁用), 改为 +0.10 (止损启用)

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.1455
    trailing_stop_positive_offset = 0.15434
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '5m'
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 26

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        SMA6 = 6
        SMA14 = 14
        SMA26 =26
        # MACD 
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
       
        # SMA - Simple Moving Average
        dataframe['sma6'] = ta.SMA(dataframe, timeperiod=SMA6)
        dataframe['sma26'] = ta.SMA(dataframe, timeperiod=SMA26)
        dataframe['sma14'] = ta.SMA(dataframe, timeperiod=SMA14)
        


        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']) &
                qtpylib.crossed_above(dataframe['sma6'], dataframe['sma14']) &
                (dataframe['sma26'] > dataframe['sma6']) 

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                     qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']) &
                qtpylib.crossed_below(dataframe['sma6'], dataframe['sma14']) &
                (dataframe['sma26'] < dataframe['sma6']) &
                (dataframe['sma26'] < dataframe['sma14'])

            ),
            'sell'] = 1
        return dataframe
