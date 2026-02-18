# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
# --------------------------------

class Babico_SMA5xBBmid(IStrategy):

    minimal_roi = {  # 已优化: 从最大 9999999900% 改为阶梯式

        "0": 0.10,  # 10%
        "24": 0.07,  # 7%
        "72": 0.05,  # 5%
        "168": 0.03  # 3%
    }stoploss = 0.10  # [-10%] 已优化: 原值为 -0.9900 (已禁用), 改为 +0.10 (止损启用)

    # Trailing stoploss (not used)
    trailing_stop = False
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.03

    use_sell_signal = True
    sell_profit_only = True
    process_only_new_candles = True

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'trailing_stop_loss': 'limit',
        'stoploss': 'limit',
        'stoploss_on_exchange': False
    }

    # Optimal timeframe for the strategy
    timeframe = '1d'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        bb = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_low'] = bb['lower']
        dataframe['bb_mid'] = bb['mid']
        dataframe['bb_upp'] = bb['upper']

        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['ema5'], dataframe['bb_mid']) 
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['bb_mid'], dataframe['ema5']) 
            ),
            'sell'] = 1
        return dataframe
