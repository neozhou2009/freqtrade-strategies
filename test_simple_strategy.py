from freqtrade.strategy import IStrategy
from pandas import DataFrame

INTERFACE_VERSION = 3

class SimpleTestStrategy(IStrategy):
    minimal_roi = {"0": 0.01}
    stoploss = -0.10
    timeframe = "5m"
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            dataframe["volume"] > 0,
            "enter_long",
        ] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            dataframe["volume"] > 0,
            "exit_long",
        ] = 1
        return dataframe
