# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib



# --------------------------------


class adxbbrsi2(IStrategy):
    """

    author@: Gert Wohlgemuth

    converted from:

        https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/AdxMomentum.cs

    """

    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.10,
        "60": 0.07,
        "120": 0.05,
        "240": 0.03
    }

    # Optimal stoploss designed for the strategy
    max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.3224 (已禁用), 改为 +0.10 (止损启用)

    # Optimal timeframe for the strategy
    timeframe = '1h'

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 20

    ##Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.1195
    trailing_stop_positive_offset = 0.1568
    trailing_only_offset_is_reached = True


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']

        # dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        # dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        # dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)

        ## Stochastic
        stoch_fast = ta.STOCHF(dataframe)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']

        # MFI
        dataframe['mfi'] = ta.MFI(dataframe)

        #SAR
        dataframe['sar'] = ta.SAR(dataframe)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['adx'] > 47) &
                (dataframe['fastd'] < 41)&
                (dataframe['close'] < dataframe['bb_lowerband'])
                    # (dataframe['mom'] > 0) &
                    # (dataframe['minus_di'] > 25) &
                    # (dataframe['plus_di'] > dataframe['minus_di'])

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['adx'] > 67) &
                (dataframe['mfi'] > 97) &
                # (dataframe['rsi'] > 97) &
                (dataframe['fastd'] < 74)
                # (dataframe['sar'] < 97)
                #fastd 74
                #mfi 97
                # (dataframe['mom'] < 0) &
                # (dataframe['minus_di'] > 25) &
                # (dataframe["close"] > dataframe['bb_upperband'])
                # (dataframe['plus_di'] < dataframe['minus_di'])
            ),
            'sell'] = 1
        return dataframe
