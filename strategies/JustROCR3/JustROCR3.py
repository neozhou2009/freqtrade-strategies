from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class JustROCR3(IStrategy):
    minimal_roi = {  # 已优化: 从最大 50% 改为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }max_open_trades = 5
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.0100 (已禁用), 改为 +0.10 (止损启用)
    trailing_stop = True
    ticker_interval = '5m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rocr'] = ta.ROCR(dataframe, period=499)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                dataframe['rocr'] > 1.10
) & (dataframe["volume"] > 0)),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            ),
            'sell'] = 1
        return dataframe
