from pandas import DataFrame
from technical.indicators import cmf

from freqtrade.strategy.interface import IStrategy


class TechnicalExampleStrategy(IStrategy):
    minimal_roi = {
        "0": 0.01
    }

    stoploss = -0.05

    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '5m'

    process_only_new_candles = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['cmf'] = cmf(dataframe, 21)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    (dataframe['cmf'] < 0)

                )
            ),
            'buy'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # different strategy used for sell points, due to be able to duplicate it to 100%
        dataframe.loc[
            (
                (dataframe['cmf'] > 0)
            ),
            'sell'] = 1
        return dataframe
